"""Repository acceptance checks. Does not claim browser, Lighthouse or field results."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,unittest,xml.etree.ElementTree as ET,subprocess
ROOT=Path(__file__).resolve().parent
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__(convert_charrefs=True);self.path=path;self.tags=[];self.ids=[];self.scripts=[];self.in_schema=False;self.schema='';self.feed(path.read_text())
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.tags.append((tag,d))
  if 'id'in d:self.ids.append(d['id'])
  if tag=='script'and d.get('type')=='application/ld+json':self.in_schema=True;self.schema=''
 def handle_data(self,data):
  if self.in_schema:self.schema+=data
 def handle_endtag(self,tag):
  if tag=='script'and self.in_schema:self.scripts.append(json.loads(self.schema));self.in_schema=False
 def select(self,tag,**attrs):return[d for t,d in self.tags if t==tag and all(d.get(k)==v for k,v in attrs.items())]
PAGES=[ROOT/'index.html']+sorted(ROOT.glob('project-*.html'))+[ROOT/'404.html']
class PortfolioChecks(unittest.TestCase):
 def test_unique_h1_and_ids(self):
  for path in PAGES:
   p=Page(path);self.assertEqual(len(p.select('h1')),1,path.name);self.assertEqual(len(p.ids),len(set(p.ids)),path.name)
 def test_titles_and_descriptions_are_unique(self):
  descriptions=[];titles=[]
  for path in PAGES:
   p=Page(path);self.assertEqual(len(p.select('meta',name='description')),1);descriptions.append(p.select('meta',name='description')[0]['content']);titles+=re.findall(r'<title>(.*?)</title>',path.read_text())
  self.assertEqual(len(descriptions),len(set(descriptions)));self.assertEqual(len(titles),len(set(titles)))
 def test_viewport_preserves_zoom(self):
  for path in PAGES:
   p=Page(path);v=p.select('meta',name='viewport');self.assertEqual(len(v),1);self.assertIn('viewport-fit=cover',v[0]['content']);self.assertNotIn('user-scalable',v[0]['content'])
 def test_canonicals_match_routes(self):
  for path in PAGES:
   c=Page(path).select('link',rel='canonical');self.assertEqual(len(c),1);self.assertEqual(c[0]['href'],'https://j-kavindu.github.io/'+(''if path.name=='index.html'else path.name))
 def test_no_empty_or_placeholder_links(self):
  for path in PAGES:
   for a in Page(path).select('a'):
    self.assertTrue(a.get('href'));self.assertNotEqual(a['href'],'#');self.assertNotIn('example.com',a['href']);self.assertFalse(a['href'].lower().startswith('javascript:'))
 def test_local_links_and_anchors_resolve(self):
  for path in PAGES:
   p=Page(path)
   for tag,attrs in p.tags:
    u=attrs.get('href')if tag in ['a','link']else attrs.get('src')if tag in ['img','script']else None
    if not u or u.startswith(('https:','http:','mailto:')):continue
    route,_,anchor=u.partition('#');target=ROOT/route.lstrip('/')if route else path
    if target.is_dir():target=target/'index.html'
    self.assertTrue(target.exists(),str(path)+': '+u)
    if anchor:self.assertIn(anchor,Page(target).ids,u)
 def test_social_metadata(self):
  required=['og:title','og:description','og:type','og:url','og:image','og:image:alt']
  for path in PAGES:
   p=Page(path)
   for key in required:self.assertEqual(len(p.select('meta',property=key)),1,key)
   for key in ['twitter:card','twitter:title','twitter:description','twitter:image']:self.assertEqual(len(p.select('meta',name=key)),1,key)
   self.assertTrue(p.select('meta',property='og:image')[0]['content'].startswith('https://j-kavindu.github.io/'))
 def test_social_png_dimensions(self):
  import struct
  with (ROOT/'social-preview.png').open('rb')as f:h=f.read(24)
  self.assertEqual(h[:8],b'\x89PNG\r\n\x1a\n');self.assertEqual(struct.unpack('>II',h[16:24]),(1200,630))
 def test_images_have_alt_and_dimensions(self):
  for path in PAGES:
   for im in Page(path).select('img'):
    self.assertTrue(im.get('alt'));self.assertTrue(int(im['width'])>0 and int(im['height'])>0);self.assertEqual(im.get('loading'),'lazy')
 def test_education_is_current_not_completed(self):
  s=(ROOT/'index.html').read_text();self.assertIn('B.Sc. (Hons) Accounting Special',s);self.assertIn('Undergraduate · In progress',s);self.assertNotIn('alumniOf',s);self.assertNotIn('hasCredential',s)
 def test_schema_matches_identity(self):
  for path in PAGES[:-1]:
   graph=Page(path).scripts[0]['@graph'];person=next(n for n in graph if n['@type']=='Person');self.assertEqual(person['name'],'Kavindu Heshan Jayawardhana');self.assertEqual(person['jobTitle'],'Accounting Undergraduate');self.assertEqual(len(person['sameAs']),2)
 def test_project_filter_data(self):
  p=Page(ROOT/'index.html');cards=[d for tag,d in p.tags if'data-project'in d];self.assertEqual(len(cards),9);self.assertEqual(sum('featured-card'in d['class']for d in cards),3)
  for c in ['accounting','finance','economics','tools','android']:self.assertTrue(any(c in d['data-category'].split()for d in cards))
 def test_no_invented_cv_or_contact_form(self):
  p=Page(ROOT/'index.html');self.assertEqual(p.select('form'),[]);self.assertFalse(any('download'in d for d in p.select('a')))
 def test_no_runtime_dependencies_or_tracking_on_home(self):
  p=Page(ROOT/'index.html');self.assertEqual([s['src']for s in p.select('script')if'src'in s],['/portfolio.js']);self.assertFalse(any(d.get('href','').startswith('https:')for d in p.select('link')if d.get('rel')=='stylesheet'))
 def test_accessible_controls_and_motion(self):
  p=Page(ROOT/'index.html');self.assertTrue(p.select('a',**{'class':'skip-link'}));self.assertTrue(p.select('button',**{'aria-controls':'primary-nav'}));self.assertTrue(p.select('div',role='group',**{'aria-label':'Filter projects'}));css=(ROOT/'portfolio.css').read_text();self.assertIn('prefers-reduced-motion:reduce',css);self.assertIn(':focus-visible',css);self.assertIn('max-width:370px',css)
 def test_sitemap_and_robots(self):
  root=ET.fromstring((ROOT/'sitemap.xml').read_text());urls=[e.text for e in root.findall('.//{*}loc')];self.assertEqual(len(urls),5);self.assertNotIn('https://j-kavindu.github.io/404.html',urls)
  for u in urls:
   p=ROOT/u.removeprefix('https://j-kavindu.github.io/');p=p/'index.html'if p.is_dir()else p;self.assertTrue(p.exists())
  self.assertIn('Sitemap: https://j-kavindu.github.io/sitemap.xml',(ROOT/'robots.txt').read_text());self.assertIn('noindex',Page(ROOT/'404.html').select('meta',name='robots')[0]['content'])
 def test_pdf_security_mitigation(self):
  s=(ROOT/'pdf-toolkit/index.html').read_text();self.assertEqual(s.count('isEvalSupported: false'),2);self.assertEqual(s.count('getDocument('),2)
 def test_existing_verification_file_preserved(self):self.assertEqual((ROOT/'googleafc6957db7ff01cd.html').read_text().strip(),'google-site-verification: googleafc6957db7ff01cd.html')
 def test_css_braces_and_no_global_overflow_hiding(self):
  s=(ROOT/'portfolio.css').read_text();self.assertEqual(s.count('{'),s.count('}'));self.assertNotIn('overflow-x:hidden',s.replace(' ',''))
 def test_js_syntax(self):subprocess.run(['node','--check',str(ROOT/'portfolio.js')],check=True,capture_output=True)
if __name__=='__main__':unittest.main(verbosity=2)
