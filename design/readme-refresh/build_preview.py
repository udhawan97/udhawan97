"""Render the README through GitHub and build a truthful local review page."""

from pathlib import Path
import json
import hashlib
import re
import shutil
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
source = ROOT / "README.md"
payload = json.dumps({"text": source.read_text(), "mode": "gfm", "context": "udhawan97/udhawan97"})
result = subprocess.run(
    [shutil.which("gh") or "gh", "api", "markdown", "--method", "POST", "--input", "-"],
    input=payload,
    text=True,
    capture_output=True,
)
if result.returncode == 0:
    rendered = result.stdout
    render_label = "GitHub API-rendered content"
else:
    from markdown_it import MarkdownIt

    rendered = MarkdownIt("commonmark", {"html": True}).enable("table").render(source.read_text())
    render_label = "Locally rendered Markdown (GitHub API unavailable)"
    print("GitHub rendering unavailable; using markdown-it for local review.")

(HERE / "evidence").mkdir(exist_ok=True)
(HERE / "evidence" / "github-rendered.html").write_text(rendered)
body = rendered.replace("./assets/profile-refresh/", "/assets/profile-refresh/")
body = body.replace("./assets/", "/assets/")
# Keep native picture media rules while preventing stale local asset previews.
body = re.sub(r'/assets/[^"<> ]+\.svg', lambda match: match[0] + '?v=' +
              hashlib.sha256((ROOT / match[0].lstrip('/')).read_bytes()).hexdigest()[:12], body)



def heading(match):
    level, attrs, content = match.groups()
    clean = re.sub("<[^>]*>", "", content).lower()
    anchor = re.sub(r"[^\w\- ]", "", clean).replace(" ", "-")
    return f'<h{level}{attrs} id="{anchor}">{content}</h{level}>'


body = re.sub(r"<h([1-6])([^>]*)>(.*?)</h\1>", heading, body)

css = """/* Hallmark · pre-emit critique: P5 H5 E4 S5 R5 V4 */
/* Hallmark · macrostructure: Map / Diagram · tone: editorial · anchor hue: gold */
:root{color-scheme:light;--color-page:#f6f8fa;--color-surface:#fffefa;--color-ink:#1f2328;--color-muted:#59636e;--color-line:#d1d9e0;--color-link:#0969da;--color-hover:#eef3f8;--space-2xs:4px;--space-xs:8px;--space-sm:12px;--space-md:16px;--space-lg:20px;--space-xl:24px;--space-2xl:32px;--space-4xl:64px;--radius-sm:6px;--radius-md:8px;--review-width:914px}
:root[data-theme=dark]{color-scheme:dark;--color-page:#080d14;--color-surface:#0d1117;--color-ink:#f0f6fc;--color-muted:#a9b1ba;--color-line:#3d444d;--color-link:#79b8ff;--color-hover:#172333}
*{box-sizing:border-box}html,body{overflow-x:clip}body{margin:0;background:var(--color-page);color:var(--color-ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:var(--color-link);text-decoration:none}a:hover{text-decoration:underline}button,select{min-height:44px;font:inherit;border:1px solid var(--color-line);border-radius:var(--radius-sm);outline:2px solid transparent;background:var(--color-surface);color:var(--color-ink);padding:var(--space-xs) var(--space-sm);cursor:pointer}button:hover,select:hover{background:var(--color-hover)}button:active,select:active{background:var(--color-page)}button:disabled,select:disabled{opacity:.55;cursor:not-allowed}button:focus-visible,a:focus-visible,summary:focus-visible,select:focus-visible{outline:2px solid var(--color-link);outline-offset:1px}
.toolbar{position:sticky;top:0;z-index:20;background:var(--color-surface);border-bottom:1px solid var(--color-line);padding:var(--space-sm) var(--space-xl);display:flex;gap:var(--space-sm);align-items:center;flex-wrap:wrap}.toolbar strong{margin-right:auto;font-size:14px;line-height:1}.toolbar button,.toolbar label{font-size:13px;line-height:1;white-space:nowrap}.notice{margin:var(--space-lg) auto 0;max-width:914px;padding:0 var(--space-md);color:var(--color-muted);font-size:13px}.mode-note{margin:0 0 var(--space-md);padding:var(--space-xs) var(--space-sm);border-left:2px solid var(--color-link);background:var(--color-page);color:var(--color-muted);font-size:13px}main{width:min(100%,var(--review-width));margin:var(--space-lg) auto var(--space-4xl);padding:var(--space-2xl);background:var(--color-surface);border:1px solid var(--color-line);border-radius:var(--radius-md)}.repo-label{font:12px ui-monospace,monospace;color:var(--color-muted);margin-bottom:var(--space-md)}.diagnostics{font:11px/1.5 ui-monospace,monospace;white-space:pre-wrap;color:var(--color-muted);margin:0 0 var(--space-lg);max-height:180px;overflow:auto}
.markdown-body{overflow-wrap:anywhere;min-width:0}.markdown-body p{margin:0 0 var(--space-md)}.markdown-body h2{font-size:24px;line-height:1.3;margin:var(--space-2xl) 0 var(--space-md);padding-bottom:var(--space-2xs);border-bottom:1px solid var(--color-line)}.markdown-body h3{font-size:20px;margin:var(--space-xl) 0 var(--space-md);line-height:1.3}.markdown-body img{max-width:100%;height:auto;vertical-align:middle}.markdown-body picture{display:block;margin-bottom:var(--space-md)}.markdown-body h3 picture,.markdown-body h4 picture,.markdown-body td picture{display:inline-block;margin:0;vertical-align:middle}.markdown-body table{border-spacing:0;border-collapse:collapse;display:block;max-width:100%;overflow:auto;width:max-content;margin:0 0 var(--space-md)}.markdown-body th,.markdown-body td{padding:var(--space-xs) var(--space-sm);border:1px solid var(--color-line)}.markdown-body tr:nth-child(2n){background:var(--color-page)}.markdown-body details{margin:0 0 var(--space-md)}.markdown-body summary{cursor:pointer;color:var(--color-link);margin-bottom:var(--space-md)}.markdown-body ul{padding-left:2em}.markdown-body li{margin-top:var(--space-xs)}.markdown-body hr{border:0;background:var(--color-line);height:1px;margin:var(--space-2xl) 0}.markdown-body img[src*=shields]{display:inline-block;width:auto;max-height:24px;margin:var(--space-2xs) 1px}
.gallery{display:none}.gallery.visible{display:block}.gallery figure{margin:0 0 var(--space-xl)}.gallery figure>img{display:block;width:100%;height:auto}.gallery figcaption{font:12px/1.5 ui-monospace,monospace;margin:var(--space-xs) 0;color:var(--color-muted)}.icon-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:var(--space-sm);margin-top:var(--space-xl)}.icon-grid figure{margin:0}.icon-grid img{width:64px;height:64px;display:block;margin:auto}.icon-grid figcaption{text-align:center}
@media(max-width:600px){.toolbar{padding:var(--space-xs)}.toolbar strong{width:100%}.notice{padding:0 var(--space-sm)}main{padding:var(--space-md);border-left:0;border-right:0;border-radius:0}.markdown-body td,.markdown-body th{padding:var(--space-xs)}.markdown-body h2{font-size:23px}.icon-grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
"""

gallery_families = [
    ("/assets/profile-header", "profile header"),
    ("/assets/ai-spell", "AI wizard"),
    ("/assets/impact-seals", "selected delivery impact"),
    ("/assets/profile-refresh/systems-atlas", "systems atlas"),
    ("/assets/profile-refresh/orifold-cutaway", "Orifold cutaway"),
    ("/assets/profile-refresh/voyalier-cutaway", "Voyalier cutaway"),
    ("/assets/profile-refresh/golavo-cutaway", "Golavo cutaway"),
    ("/assets/profile-refresh/delivery-loop", "delivery loop"),
    ("/assets/profile-refresh/engineering-workbench", "engineering workbench"),
]
gallery = "".join(
    f'<figure><img class="gallery-asset" data-base="{path}" data-label="{label}" alt="{label}"><figcaption>{label}</figcaption></figure>'
    for path, label in gallery_families
)
icons = "".join(
    f'<figure><img class="gallery-icon" data-base="/assets/profile-refresh/icons/{name}" alt="{name} icon"><figcaption>{name}</figcaption></figure>'
    for name in ("orifold", "voyalier", "folioorb", "golavo", "codemble", "dusori", "nindova", "nimanto", "vidha", "paldawn")
)

script = """
const root=document.documentElement,main=document.querySelector('main'),article=document.querySelector('article'),gallery=document.querySelector('.gallery'),diagnostics=document.querySelector('.diagnostics');
let theme=matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light',motion=!matchMedia('(prefers-reduced-motion:reduce)').matches,showGallery=false,width=914;
const staticFamilies=/profile-header|ai-spell|impact-seals|systems-atlas|delivery-loop|engineering-workbench/;
function gallerySource(base){const mobile=width<=700;if(base.includes('/icons/'))return `${base}${motion?'':'-static'}.svg`;let src=`${base}${mobile?'-mobile':''}-${theme}`;if(!motion&&staticFamilies.test(base))src+='-static';return src+'.svg'}
function updateDiagnostics(){const rows=[...article.querySelectorAll('picture img')].map((img,index)=>`${String(index+1).padStart(2,'0')} · ${img.clientWidth}px · ${img.currentSrc.split('/').pop()||'not loaded'}`);diagnostics.textContent=`Native picture selection · viewport ${innerWidth}px · review column ${main.clientWidth}px · system theme ${matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'} · system motion ${matchMedia('(prefers-reduced-motion:reduce)').matches?'reduced':'regular'}\\n`+rows.join('\\n')}
function apply(){root.dataset.theme=theme;root.style.setProperty('--review-width',`${width}px`);document.querySelectorAll('.gallery-asset,.gallery-icon').forEach(img=>img.src=gallerySource(img.dataset.base));article.hidden=showGallery;gallery.classList.toggle('visible',showGallery);diagnostics.hidden=showGallery;document.querySelector('.mode-note').textContent=showGallery?'Forced gallery: theme, motion, and mobile assets follow the controls.':'Native acceptance: picture sources remain intact and follow the browser’s real media preferences.';document.querySelector('#view').textContent=showGallery?'Native README':'Asset gallery';document.querySelector('#theme').textContent=`Gallery: ${theme}`;document.querySelector('#motion').textContent=`Gallery motion: ${motion?'on':'still'}`;requestAnimationFrame(updateDiagnostics)}
document.querySelector('#theme').onclick=()=>{theme=theme==='dark'?'light':'dark';apply()};document.querySelector('#motion').onclick=()=>{motion=!motion;apply()};document.querySelector('#width').onchange=e=>{width=Number(e.target.value);apply()};document.querySelector('#view').onclick=()=>{showGallery=!showGallery;apply();scrollTo(0,0)};addEventListener('resize',()=>requestAnimationFrame(updateDiagnostics));apply();
"""

width_options = "".join(
    f'<option value="{width}"{(" selected" if width == 914 else "")}>{label}</option>'
    for width, label in ((914, "README column"), (768, "768 px"), (414, "414 px"), (390, "390 px"), (375, "375 px"), (320, "320 px"))
)
html = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Umang Dhawan · README design review</title><style>{css}</style><body>
<div class="toolbar"><strong>README / DESIGN REVIEW</strong><button id="theme">Gallery: dark</button><button id="motion">Gallery motion: on</button><label>Review column <select id="width">{width_options}</select></label><button id="view">Asset gallery</button></div>
<div class="notice">{render_label}. The native view preserves the README's picture sources; the gallery provides explicit variant inspection.</div>
<main><div class="repo-label">udhawan97 / README.md</div><p class="mode-note"></p><pre class="diagnostics"></pre><article class="markdown-body">{body}</article><section class="gallery">{gallery}<div class="icon-grid">{icons}</div></section></main><script>{script}</script></body></html>'''
(HERE / "preview.html").write_text(html)
print("Preview created from", source.name)
