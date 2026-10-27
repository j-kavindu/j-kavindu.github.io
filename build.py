"""Build the static portfolio. Python standard library only; no build-time downloads."""
from pathlib import Path
from html import escape as esc
import json
import struct
from datetime import date
ROOT=Path(__file__).resolve().parent
BASE='https://j-kavindu.github.io/'
NAME='Kavindu Heshan Jayawardhana'
PROJECTS=json.loads((ROOT/'projects.json').read_text())
IMAGE_SIZES=json.loads((ROOT/'image-sizes.json').read_text())

def head(title,desc,url,schema,noindex=False):
 return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0b1325">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{NAME}">
<meta name="robots" content="{'noindex, follow' if noindex else 'index, follow, max-image-preview:large'}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:image" content="{BASE}social-preview.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Kavindu Heshan Jayawardhana — Accounting meets technology. Accounting undergraduate at the University of Sri Jayewardenepura.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}social-preview.png">
<meta name="twitter:image:alt" content="Accounting meets technology — Kavindu Heshan Jayawardhana">
<link rel="stylesheet" href="/portfolio.css">
<script src="/portfolio.js" defer></script>
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</','<\\/')}</script>
</head>'''

def header(home=False):
 prefix='' if home else '/'
 return f'''<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header"><div class="shell header-inner">
<a class="brand" href="{prefix}#top" aria-label="{NAME}, home"><span class="monogram" aria-hidden="true">KJ<span>.</span></span><span class="brand-name">Kavindu Heshan<br><strong>Jayawardhana</strong></span></a>
<div class="header-controls"><button class="theme-toggle" type="button" aria-label="Switch to light theme" aria-pressed="false" hidden>Light mode</button><button class="menu-toggle" type="button" aria-controls="primary-nav" aria-expanded="false" hidden>Menu <span aria-hidden="true">☰</span></button></div>
<nav id="primary-nav" class="primary-nav" aria-label="Main navigation"><a href="{prefix}#work">Projects</a><a href="{prefix}#about">About</a><a href="{prefix}#education">Education</a><a href="{prefix}#skills">Skills</a><a class="nav-contact" href="{prefix}#contact">Let’s connect <span aria-hidden="true">↗</span></a></nav>
</div></header>'''

def footer():return f'''<footer class="site-footer"><div class="shell footer-inner"><div><a class="footer-name" href="/#top">{NAME}</a><p>Accounting, finance &amp; thoughtful digital tools.</p><small>© 2026 {NAME}</small></div><nav aria-label="Footer navigation"><a href="/#work">Projects</a><a href="/#contact">Contact</a><a href="https://github.com/j-kavindu">GitHub</a><a href="https://www.linkedin.com/in/jkavindu/">LinkedIn</a></nav><a class="back-top" href="#top">Back to top ↑</a></div></footer></body></html>'''

def badge(text,cls=''):return f'<span class="badge {cls}">{esc(text)}</span>'
def image(p,featured=False):
 if not p.get('image'):return f'<div class="project-symbol" aria-hidden="true">{ "PDF" if p["id"]=="pdf-toolkit" else "LKR"}<span>{esc(p["kind"])}</span></div>'
 w,h=IMAGE_SIZES[p['image']]
 return f'<img src="/{p["image"]}" alt="{esc(p["alt"])}" loading="lazy" decoding="async" width="{w}" height="{h}" class="{ "portrait-image" if p["id"] in ["cse","my24"] else ""}">'

def links(p,detail=True):
 items=[]
 if p.get('demo'):items.append(f'<a class="text-link" href="{p["demo"]}">{"Play game" if p["id"] in ["nation360","ledger-arena"] else "Open demo"} <span aria-hidden="true">↗</span></a>')
 if detail and p.get('detail'):items.append(f'<a class="text-link secondary" href="/project-{p["id"]}.html">Read case study <span aria-hidden="true">→</span></a>')
 items.append(f'<a class="repo-link" href="https://github.com/j-kavindu/{p["repo"]}">{esc(p["source_note"])}</a>')
 return '<div class="project-links">'+''.join(items)+'</div>'

def card(p,i):
 return f'''<article class="project-card {'featured-card' if p['featured'] else ''}" data-project data-category="{p['category']}" id="{p['id']}">
<div class="project-media">{image(p,p['featured'])}<span class="media-caption">{esc(p['kind'])}</span></div>
<div class="project-copy"><div class="project-topline"><span class="eyebrow">{i:02} / {esc(p['kind'])}</span>{badge(p['status'],'status')}</div><h3>{esc(p['title'])}</h3><p class="project-summary">{esc(p['summary'])}</p>
<div class="tags">{''.join(badge(x) for x in p['tech'])}</div>
{'<p class="project-skills">'+esc(p['skills'])+'</p>' if p.get('skills') else ''}
{links(p)}<details class="project-notes"><summary>Scope &amp; project notes</summary><ul>{''.join('<li>'+esc(x)+'</li>' for x in p['features'])}</ul><p>{esc(p['limits'])}</p></details></div></article>'''

person={'@type':'Person','@id':BASE+'#person','name':NAME,'url':BASE,'jobTitle':'Accounting Undergraduate','description':'Accounting undergraduate and digital project developer in Sri Lanka. Studying B.Sc. (Hons) Accounting Special at the University of Sri Jayewardenepura.','affiliation':{'@type':'CollegeOrUniversity','name':'University of Sri Jayewardenepura','description':'Current undergraduate study in Accounting Special, Sri Lanka'},'sameAs':['https://github.com/j-kavindu','https://www.linkedin.com/in/jkavindu/'],'knowsAbout':['Accounting','Financial reporting','Inventory valuation','Finance','Economics','Microsoft Excel','TypeScript','Web applications']}
schema={'@context':'https://schema.org','@graph':[person,{'@type':'WebSite','@id':BASE+'#website','url':BASE,'name':NAME+' — Accounting & Technology Portfolio','publisher':{'@id':BASE+'#person'}},{'@type':'ProfilePage','@id':BASE+'#profile','url':BASE,'name':NAME+' — Accounting Undergraduate & Digital Project Developer','mainEntity':{'@id':BASE+'#person'}}]}
intro=head(NAME+' | Accounting & Technology Portfolio','Accounting undergraduate at the University of Sri Jayewardenepura. Explore Kavindu Heshan Jayawardhana’s finance tools, economics games and digital projects.',BASE,schema)+header(True)
hero='''<main id="main"><section class="hero shell" id="top"><div class="hero-copy"><p class="eyebrow hero-label"><span class="small-line"></span> Accounting undergraduate · Sri Lanka</p><p class="hero-name">Kavindu Heshan Jayawardhana</p><h1>Accounting meets<br><em>technology.</em></h1><p class="hero-intro">I connect accounting, finance and economics with practical digital projects — from spreadsheets and reporting tools to interactive learning experiences.</p><div class="hero-actions"><a class="button primary" href="#work">Explore projects <span aria-hidden="true">↗</span></a><a class="button quiet" href="#about">About me <span aria-hidden="true">→</span></a></div><p class="hero-contact"><a class="text-link" href="#contact">Contact me <span aria-hidden="true">↗</span></a></p><p class="hero-identity">Accounting Undergraduate <span>Finance &amp; Technology Enthusiast</span> Digital Project Developer</p></div>
<aside class="academic-card" aria-label="Academic profile"><div class="academic-card-top"><span class="eyebrow">An analytical foundation.</span><span class="card-mark" aria-hidden="true">KJ.</span></div><div class="academic-art" aria-hidden="true"><div class="art-column c1"></div><div class="art-column c2"></div><div class="art-column c3"></div><div class="art-column c4"></div><span class="art-rule"></span><span class="art-caption">PRECISION / CURIOSITY / PRACTICE</span></div><p class="academic-status">CURRENT UNDERGRADUATE STUDY</p><h2>B.Sc. (Hons)<br>Accounting Special</h2><p>University of Sri Jayewardenepura<br><span>Sri Lanka</span></p><a href="#education">View academic background <span aria-hidden="true">↗</span></a></aside></section>
<div class="discipline-strip"><div class="shell"><span>Accounting</span><span>Finance</span><span>Economics</span><span>Technology</span><span>Digital innovation</span></div></div>'''
work='''<section class="section shell" id="work" aria-labelledby="work-title"><div class="section-heading"><div><p class="eyebrow">01 / Selected work</p><h2 id="work-title">Ideas, made <em>practical.</em></h2></div><p>Personal projects that connect subject knowledge with tools you can explore. Each project has a clearly stated scope.</p></div><div class="project-toolbar"><div class="filters" role="group" aria-label="Filter projects" hidden>'''+''.join(f'<button type="button" data-filter="{key}" aria-pressed="{str(key=="all").lower()}">{label}</button>' for key,label in [('all','All projects'),('accounting','Accounting'),('finance','Finance'),('economics','Economics'),('tools','Digital tools'),('android','Android')])+'''</div><p id="filter-status" class="filter-status" role="status" aria-live="polite">9 projects</p></div><div class="projects-grid">'''+''.join(card(p,i+1)for i,p in enumerate(PROJECTS))+'''</div><noscript><p>All projects are shown. Category filtering and theme switching require JavaScript; every project link works without it.</p></noscript></section>'''
work=work.replace('>9 projects</p>',f'>{len(PROJECTS)} projects</p>')
about='''<section class="about-section" id="about"><div class="shell section about-grid"><div><p class="eyebrow">02 / About me</p><h2>Numbers give me<br><em>a starting point.</em><br>Building takes them further.</h2></div><div class="about-copy"><p class="lead">I’m Kavindu, an accounting undergraduate at the University of Sri Jayewardenepura with an interest in how financial ideas become useful digital tools.</p><p>My work explores financial reporting, inventory costing, budgeting, portfolio record keeping and economic decision-making. I use spreadsheets and web applications to make these topics easier to examine and understand.</p><p>These are personal and educational projects, including AI-assisted implementation. I focus on understanding the calculations, documenting the assumptions and being clear about what has — and has not — been tested.</p><p>I’m interested in internship opportunities, accounting and finance learning, and thoughtful collaboration at the intersection of business and technology.</p><a class="text-link" href="#contact">Start a conversation <span aria-hidden="true">↗</span></a></div></div></section>
<section class="section shell" id="education"><div class="section-heading"><div><p class="eyebrow">03 / Education</p><h2>A foundation in <em>accounting.</em></h2></div></div><article class="education-card"><span class="education-icon" aria-hidden="true">B.Sc.</span><div><span class="badge status">Undergraduate · In progress</span><h3>B.Sc. (Hons) Accounting Special</h3><p class="degree-long">Bachelor of Science (Honours) in Accounting — Accounting Special</p><p>University of Sri Jayewardenepura, Sri Lanka</p></div></article></section>
<section class="section shell skills-section" id="skills"><div class="section-heading"><div><p class="eyebrow">04 / Skills &amp; interests</p><h2>Subject thinking.<br><em>Practical tools.</em></h2></div><p>Areas demonstrated through the projects above. No proficiency ratings or professional certifications are implied.</p></div><div class="skills-grid">'''
skills=[('Accounting & finance',['Financial reporting workflows','Inventory costing: FIFO & weighted average','Budget-versus-actual analysis','Portfolio and cash-flow record keeping']),('Economics & analytical thinking',['Opportunity cost and trade-offs','Market and policy simulation','Reconciliation and validation','Documenting assumptions and limitations']),('Programming & technology',['HTML, CSS & JavaScript','React & TypeScript','Decimal-based calculation logic','Browser storage & Firebase integration']),('Tools & platforms',['Microsoft Excel: tables, formulas & charts','Git & GitHub Pages','CSV / JSON data workflows','Power BI-ready spreadsheet structures'])]
about+=''.join('<article class="skill-group"><span class="skill-number">0'+str(i+1)+'</span><h3>'+a+'</h3><ul>'+''.join('<li>'+x+'</li>' for x in b)+'</ul></article>' for i,(a,b) in enumerate(skills))+'''</div></section>
<section class="section shell community-section" id="volunteer"><div class="community-copy"><p class="eyebrow">05 / Beyond the projects</p><h2>Learning is worth <em>sharing.</em></h2><p>I also share commerce and accounting learning material through the educational channels linked from my existing portfolio.</p></div><div class="community-links"><a href="https://whatsapp.com/channel/0029VbCz3vvBA1f11d2qRs2r"><span><strong>Commerce Academic Help</strong><small>WhatsApp learning channel</small></span><span aria-hidden="true">↗</span></a><a href="https://youtube.com/@wanijalk"><span><strong>Educational videos</strong><small>YouTube lessons &amp; walkthroughs</small></span><span aria-hidden="true">↗</span></a></div></section>
<section class="contact-section" id="contact"><div class="shell section contact-grid"><div><p class="eyebrow">06 / Get in touch</p><h2>Let’s connect<br><em>ideas with opportunity.</em></h2><p>For internships, project conversations and collaboration in accounting, finance and technology.</p></div><div class="contact-links"><a href="mailto:j.kavindu@outlook.com"><span class="eyebrow">Email</span><strong>j.kavindu@outlook.com</strong><span aria-hidden="true">↗</span></a><a href="https://www.linkedin.com/in/jkavindu/"><span class="eyebrow">Professional profile</span><strong>Connect on LinkedIn</strong><span aria-hidden="true">↗</span></a><a href="https://github.com/j-kavindu"><span class="eyebrow">Code &amp; projects</span><strong>Explore GitHub</strong><span aria-hidden="true">↗</span></a></div></div></section></main>'''
(ROOT/'index.html').write_text(intro+hero+work+about+footer())
for p in PROJECTS:
 if not p.get('detail'):continue
 url=BASE+'project-'+p['id']+'.html'
 code_schema={'@type':'CreativeWork' if p['id']=='nation360' else 'SoftwareSourceCode','name':p['title'],'url':url,'description':p['summary'],'creator':{'@id':BASE+'#person'}}
 if p['id']!='nation360':code_schema['codeRepository']='https://github.com/j-kavindu/'+p['repo'];code_schema['programmingLanguage']=['TypeScript','JavaScript']
 data={'@context':'https://schema.org','@graph':[person,code_schema,{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Portfolio','item':BASE},{'@type':'ListItem','position':2,'name':p['title'],'item':url}]}]}
 body=head(p['title']+' | '+NAME,p['summary']+' A project by accounting undergraduate '+NAME+'.',url,data)+header()+f'''<main id="main"><section class="shell section case-hero" id="top"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Portfolio</a><span aria-hidden="true">/</span><span aria-current="page">{esc(p['title'])}</span></nav><p class="eyebrow">Project case study / {esc(p['kind'])}</p><h1>{esc(p['title'])}</h1><p class="case-summary">{esc(p['summary'])}</p><div class="tags">{badge(p['status'],'status')}{''.join(badge(x)for x in p['tech'])}</div>{links(p,False)}<figure class="case-image">{image(p)}<figcaption>{esc(p['alt'])}. Genuine project screenshot; demonstration figures are synthetic.</figcaption></figure><div class="case-content"><section><p class="eyebrow">The problem</p><h2>What the project addresses</h2><p>{esc(p['problem'])}</p></section><section><p class="eyebrow">The approach</p><h2>A practical workflow</h2><p>{esc(p['solution'])}</p><ul>{''.join('<li>'+esc(x)+'</li>'for x in p['features'])}</ul></section><section><p class="eyebrow">Subject &amp; technology</p><h2>What it demonstrates</h2><p>{esc(p['skills'])}.</p><p>Project stack: {esc(', '.join(p['tech']))}.</p></section><section><p class="eyebrow">Evidence &amp; scope</p><h2>Verification and limitations</h2><p>{esc(p['evidence'])}</p><p>{esc(p['limits'])}</p></section></div><div class="case-bottom"><a class="button quiet" href="/#work">← Back to all projects</a><a class="button primary" href="{p['demo']}">Explore the project ↗</a></div></section></main>'''+footer()
 (ROOT/('project-'+p['id']+'.html')).write_text(body)
not_found=head('Page not found | '+NAME,'This page could not be found. Return to Kavindu Heshan Jayawardhana’s accounting and technology portfolio.',BASE+'404.html',{'@context':'https://schema.org','@type':'WebPage','name':'Page not found'},True)+header()+'''<main id="main"><section class="shell section error-page" id="top"><p class="eyebrow">404 / Page not found</p><h1>Let’s get you<br><em>back on track.</em></h1><p>The page may have moved, or the address may be incomplete.</p><a class="button primary" href="/">Return to portfolio →</a></section></main>'''+footer()
(ROOT/'404.html').write_text(not_found)
urls=[BASE,BASE+'pdf-toolkit/']+[BASE+'project-'+p['id']+'.html'for p in PROJECTS if p.get('detail')]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+u+'</loc></url>\n'for u in urls)+'</urlset>\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /audit/\n\nSitemap: '+BASE+'sitemap.xml\n')
print('Built homepage, three case studies, custom 404, sitemap and robots.txt.')
