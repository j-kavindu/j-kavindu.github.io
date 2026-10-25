const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const code = fs.readFileSync(require('node:path').join(__dirname,'portfolio.js'),'utf8');
function fixture({storageFails=false,mobile=true,saved='dark'}={}) {
 const create=()=>({hidden:true,dataset:{},attrs:{},textContent:'',listeners:{},setAttribute(k,v){this.attrs[k]=v},getAttribute(k){return this.attrs[k]},addEventListener(k,v){this.listeners[k]=v},focus(){this.focused=true}});
 const theme=create(),menu=create(),nav=create(),filters=create(),status=create(),root=create(),meta={};
 const categories=['accounting','accounting','economics','finance','accounting','finance','tools','android','finance tools'];
 const projects=categories.map(category=>({...create(),hidden:false,dataset:{category}}));
 const buttons=['all','accounting','finance','economics','tools','android'].map(category=>({...create(),dataset:{filter:category},textContent:category}));
 filters.querySelectorAll=()=>buttons;
 const media={matches:mobile,addEventListener(k,v){this.listener=v}};
 const doc={documentElement:root,querySelector(s){return {'.theme-toggle':theme,'.menu-toggle':menu,'.filters':filters,'meta[name="theme-color"]':meta}[s]},getElementById(id){return id==='primary-nav'?nav:status},querySelectorAll(){return projects},listeners:{},addEventListener(k,v){this.listeners[k]=v}};
 const store={value:saved,getItem(){if(storageFails)throw Error('blocked');return this.value},setItem(k,v){if(storageFails)throw Error('blocked');this.value=v}};
 vm.runInNewContext(code,{document:doc,window:{matchMedia:()=>media},localStorage:store});
 return {theme,menu,nav,filters,status,root,meta,projects,buttons,doc,store,media};
}
test('filters show correct project sets and restore all nine projects',()=>{const f=fixture();const click=i=>f.filters.listeners.click({target:{closest:()=>f.buttons[i]}});click(1);assert.equal(f.projects.filter(p=>!p.hidden).length,3);assert.equal(f.buttons[1].attrs['aria-pressed'],'true');click(2);assert.equal(f.projects.filter(p=>!p.hidden).length,3);click(3);assert.equal(f.projects.filter(p=>!p.hidden).length,1);click(0);assert.equal(f.projects.filter(p=>!p.hidden).length,9);assert.equal(f.status.textContent,'9 projects');});
test('theme preference restores and toggles with matching label and theme color',()=>{const f=fixture({saved:'light'});assert.equal(f.root.dataset.theme,'light');assert.equal(f.theme.textContent,'Dark mode');f.theme.listeners.click();assert.equal(f.store.value,'dark');assert.equal(f.meta.content,'#0b1325');assert.equal(f.theme.attrs['aria-pressed'],'false');});
test('denied storage does not prevent theme, filters or navigation',()=>{const f=fixture({storageFails:true});assert.equal(f.theme.hidden,false);assert.equal(f.filters.hidden,false);assert.doesNotThrow(()=>f.theme.listeners.click());assert.equal(f.root.dataset.theme,'light');});
test('mobile navigation opens, closes with Escape, and returns keyboard focus',()=>{const f=fixture();assert.equal(f.nav.dataset.mobile,'collapsed');f.menu.listeners.click();assert.equal(f.menu.attrs['aria-expanded'],'true');f.doc.listeners.keydown({key:'Escape'});assert.equal(f.nav.dataset.mobile,'collapsed');assert.equal(f.menu.focused,true);});
test('desktop resize makes links available and mobile toggle no longer visible',()=>{const f=fixture();f.media.matches=false;f.media.listener();assert.equal(f.menu.hidden,true);assert.equal(f.nav.dataset.mobile,'expanded');});
