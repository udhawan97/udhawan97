"""Render the README through GitHub and build a local review page."""
from pathlib import Path
import json, re, subprocess, shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
source=ROOT/'README.md'
payload=json.dumps({'text':source.read_text(),'mode':'gfm','context':'udhawan97/udhawan97'})
r=subprocess.run([shutil.which('gh') or 'gh','api','markdown','--method','POST','--input','-'],input=payload,text=True,capture_output=True)
if r.returncode == 0:
    rendered=r.stdout
    render_label="GitHub API-rendered content"
else:
    from markdown_it import MarkdownIt
    rendered=MarkdownIt('commonmark',{'html':True}).enable('table').render(source.read_text())
    render_label="Locally rendered Markdown (GitHub API unavailable)"
    print('GitHub rendering unavailable; using markdown-it for local review.')
(HERE/'evidence').mkdir(exist_ok=True)
(HERE/'evidence/github-rendered.html').write_text(rendered)
body=rendered
body=body.replace('./assets/profile-refresh/','/assets/profile-refresh/')
body=body.replace('./assets/','/assets/')
# The API returns headings without GitHub's page-shell heading anchors.
def heading(m):
    level,attrs,content=m.groups()
    clean=re.sub('<[^>]*>','',content).lower()
    anchor=re.sub(r'[^\w\- ]','',clean).replace(' ','-')
    return f'<h{level}{attrs} id="{anchor}">{content}</h{level}>'
body=re.sub(r'<h([1-6])([^>]*)>(.*?)</h\1>',heading,body)
css='''
:root{color-scheme:light;--page:#f6f8fa;--surface:#fff;--text:#1f2328;--muted:#59636e;--line:#d1d9e0;--link:#0969da}
:root[data-theme=dark]{color-scheme:dark;--page:#080d14;--surface:#0d1117;--text:#f0f6fc;--muted:#9198a1;--line:#3d444d;--link:#79b8ff}
*{box-sizing:border-box}body{margin:0;background:var(--page);color:var(--text);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}button,select{font:inherit}button,select{border:1px solid var(--line);border-radius:6px;background:var(--surface);color:var(--text);padding:6px 10px;cursor:pointer}button:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid var(--link);outline-offset:3px}
.toolbar{position:sticky;top:0;z-index:20;background:var(--surface);border-bottom:1px solid var(--line);padding:12px 22px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}.toolbar strong{margin-right:auto;font-size:14px}.toolbar button{font-size:13px}.notice{margin:24px auto 0;max-width:900px;padding:0 24px;color:var(--muted);font-size:13px}main{width:min(100% - 32px,914px);margin:24px auto 64px;padding:32px;background:var(--surface);border:1px solid var(--line);border-radius:8px}main.mobile{max-width:390px;padding:16px}main.narrow{max-width:320px;padding:12px}.repo-label{font:12px ui-monospace,monospace;color:var(--muted);margin-bottom:24px}
.markdown-body{overflow-wrap:break-word}.markdown-body p{margin:0 0 16px}.markdown-body h2{font-size:24px;line-height:1.3;margin:30px 0 16px;padding-bottom:.3em;border-bottom:1px solid var(--line)}.markdown-body h3{font-size:20px;margin:26px 0 16px;line-height:1.3}.markdown-body h4{font-size:16px;margin:26px 0 16px}.markdown-body img{max-width:100%;height:auto;vertical-align:middle}.markdown-body picture{display:block;margin-bottom:16px}.markdown-body h4 picture,.markdown-body h3 picture,.markdown-body td picture{display:inline-block;margin:0;vertical-align:middle}.markdown-body table{border-spacing:0;border-collapse:collapse;display:block;max-width:100%;overflow:auto;width:max-content;margin:0 0 16px}.markdown-body th,.markdown-body td{padding:8px 13px;border:1px solid var(--line)}.markdown-body th{font-weight:600}.markdown-body tr:nth-child(2n){background:var(--page)}.markdown-body sub{font-size:12px;color:var(--muted)}.markdown-body details{margin:0 0 16px}.markdown-body summary{cursor:pointer;color:var(--link);margin-bottom:16px}.markdown-body details[open]{padding-bottom:8px}.markdown-body ul{padding-left:2em}.markdown-body li{margin-top:8px}.markdown-body hr{border:0;background:var(--line);height:1px;margin:32px 0}.markdown-body img[src*=shields]{display:inline-block;width:auto;max-height:24px;margin:3px 1px}.contact-sheet{display:none}.contact-sheet.visible{display:block}.contact-sheet figure{margin:0 0 30px}.contact-sheet figcaption{font:13px/1.5 ui-monospace,monospace;margin:8px 0;color:var(--muted)}
@media(max-width:600px){main{width:100%;padding:16px;border:0;border-radius:0;margin-top:14px}.toolbar{padding:10px}.toolbar strong{width:100%}.notice{padding:0 16px}.markdown-body td,.markdown-body th{padding:6px}.markdown-body h2{font-size:23px}}
'''
script='''
const main=document.querySelector('main'), article=document.querySelector('article'),board=document.querySelector('.contact-sheet');
let theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light', motion=!matchMedia('(prefers-reduced-motion: reduce)').matches, width='desktop', showBoard=false;
document.querySelectorAll('picture').forEach(p=>{p.dataset.original=p.innerHTML;p.querySelectorAll('source').forEach(s=>s.remove());});
document.querySelectorAll('picture img').forEach(img=>img.dataset.base=img.getAttribute('src'));
function apply(){
 document.documentElement.dataset.theme=theme;
 const mobile=width!=='desktop'||innerWidth<=700;
 main.className=width==='desktop'?'':width==='mobile'?'mobile':'narrow';
 document.querySelectorAll('picture img').forEach(img=>{
  if(img.dataset.base.includes('/icons/')){img.src=img.dataset.base.replace('-static','').replace('.svg',motion?'.svg':'-static.svg');return;}
  let src=img.dataset.base.replace(/-mobile/g,'').replace(/-(dark|light)/g,'-'+theme).replace(/-static/g,'');
  if(mobile)src=src.replace('-'+theme,'-mobile-'+theme);
  if(!motion&&/systems-atlas|delivery-loop/.test(src))src=src.replace('.svg','-static.svg');
  img.src=src;
 });
 document.querySelectorAll('.contact-sheet img').forEach(img=>{
  let src=img.dataset.base+'-'+theme+'.svg';
  if(mobile)src=src.replace('-'+theme,'-mobile-'+theme);
  if(!motion&&/systems-atlas|delivery-loop/.test(src))src=src.replace('.svg','-static.svg');
  img.src=src;
 });
 document.querySelector('#theme').textContent=theme==='dark'?'Light theme':'Dark theme';
 document.querySelector('#motion').textContent=motion?'Motion: on':'Motion: still';
 article.hidden=showBoard;board.classList.toggle('visible',showBoard);
 document.querySelector('#view').textContent=showBoard?'Read the README':'Asset gallery';
}
document.querySelector('#theme').onclick=()=>{theme=theme==='dark'?'light':'dark';apply()};
document.querySelector('#motion').onclick=()=>{motion=!motion;apply()};
document.querySelector('#width').onchange=e=>{width=e.target.value;apply()};
document.querySelector('#view').onclick=()=>{showBoard=!showBoard;apply();scrollTo(0,0)};
addEventListener('resize',apply);apply();
'''
prefix='/assets/profile-refresh/'
gallery=''.join(f'<figure><img data-base="{prefix}{n}" src="{prefix}{n}-light.svg" width="100%" alt="{n}"><figcaption>{n}</figcaption></figure>' for n in ['systems-atlas','orifold-cutaway','voyalier-cutaway','golavo-cutaway','delivery-loop'])
html=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Umang Dhawan · README design review</title><style>{css}</style><body>
<div class="toolbar"><strong>README / DESIGN REVIEW</strong><button id="theme">Dark theme</button><button id="motion">Motion: on</button><label><span style="font-size:13px">Width </span><select id="width"><option value="desktop">Desktop</option><option value="mobile">390 px</option><option value="narrow">320 px</option></select></label><button id="view">Asset gallery</button></div>
<div class="notice">{render_label} in a local approximation of the README column. Controls force asset variants for inspection; the published README uses native picture media queries. Illustrations are conceptual, not app screenshots.</div>
<main><div class="repo-label">udhawan97 / README.md</div><article class="markdown-body">{body}</article><section class="contact-sheet">{gallery}</section></main><script>{script}</script></body></html>'''
(HERE/'preview.html').write_text(html)
print('Preview created from',source.name)
