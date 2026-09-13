"""Build original, self-contained SVG artwork for the proposed profile refresh.

Python standard library only. This regenerates only assets/profile-refresh, leaving the opening artwork and README intact.
Run from any working directory. Re-running produces identical SVG bytes.
"""
from pathlib import Path
from html import escape
import json
import base64

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / 'assets' / 'profile-refresh'
OUT.mkdir(exist_ok=True)
PALETTES = {
    'dark': dict(bg='#111719', panel='#1A2326', edge='#3B4948', text='#F5F0E8',
                 muted='#B7C2BD', gold='#E58B78', blue='#99B5CB', teal='#A5BBA7', low='#223137'),
    'light': dict(bg='#F7F5EF', panel='#FFFEFA', edge='#C8CDC5', text='#20292B',
                  muted='#53615E', gold='#994535', blue='#3F627A', teal='#4B6956', low='#EDEEE8'),
}
MANIFEST = []


def text(x, y, words, size=20, color='text', weight=400, family='sans', anchor='start'):
    fonts = {'sans': "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif",
             'serif': "Georgia,'Times New Roman',serif", 'mono': "'SFMono-Regular',Consolas,monospace"}
    return f'<text x="{x}" y="{y}" fill="{C.get(color,color)}" font-size="{size}" font-weight="{weight}" font-family="{fonts[family]}" text-anchor="{anchor}">{escape(words)}</text>'


def path(d, color='edge', width=1.5, fill='none', extra=''):
    return f'<path d="{d}" fill="{C.get(fill,fill)}" stroke="{C.get(color,color)}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def rect(x,y,w,h,fill='panel',stroke='edge',rx=12,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{C.get(fill,fill)}" stroke="{C.get(stroke,stroke)}" {extra}/>'


def dot(x,y,color='gold',r=4,extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C.get(color,color)}" {extra}/>'


def line(x1,y1,x2,y2,color='edge',width=1.5,extra=''):
    return path(f'M{x1} {y1} L{x2} {y2}',color,width,extra=extra)


def label(x,y,s,color='muted',size=14):
    return f'<g letter-spacing="1.8">{text(x,y,s,size,color,600,"mono")}</g>'


def prism(x,y,scale=1):
    p=''
    # Exploded sheets suggest the care between concept and finished artifact.
    for i,(yy,col) in enumerate([(86,'edge'),(55,'teal'),(24,'blue'),(-7,'gold')]):
        p+=f'<g class="sheet s{i}">'
        p+=path(f'M0 {yy-66} L110 {yy-8} L0 {yy+51} L-110 {yy-8} Z',col,1.5,'panel')
        p+=path(f'M-110 {yy-8} L0 {yy+51} L110 {yy-8} L110 {yy+1} L0 {yy+61} L-110 {yy+1} Z',col,1,'low')
        p+=path(f'M-78 {yy-8} L0 {yy-49} L78 {yy-8} L0 {yy+34} Z',col,1,extra='opacity=".28"')
        p+='</g>'
    p+=path('M-45 -14 L-10 5 L48 -26','gold',4)
    p+=dot(-45,-14,'gold',4)+dot(48,-26,'gold',4)
    p+=path('M0 -93 V-71 M0 146 V164','edge',1,extra='stroke-dasharray="3 5"')
    return f'<g transform="translate({x} {y}) scale({scale})">{p}</g>'


def frame(name,w,h,content,motion=False,static=False):
    desc = DESCRIPTIONS[name]
    css='''/* Hallmark · pre-emit critique: P5 H5 E4 S5 R5 V4 */
/* Hallmark · genre: editorial · macrostructure: Map / Diagram · theme: Atelier · enrichment: hand-built SVG · nav: N6 · footer: Ft2 */
text{font-kerning:normal}.trace{stroke-dasharray:1;stroke-dashoffset:0}.sheet{transform:translateY(0)}
@keyframes route{from{stroke-dashoffset:1;opacity:.12}to{stroke-dashoffset:0;opacity:1}}
@keyframes assemble{from{transform:translateY(9px);opacity:.5}to{transform:translateY(0);opacity:1}}
@keyframes settle{from{opacity:.3}to{opacity:1}}
'''
    if motion and not static:
        css+='''.trace{animation:route 2.8s ease-out both}.trace.t1{animation-delay:.35s}.trace.t2{animation-delay:.65s}
.sheet{animation:assemble 1.6s ease-out both}.s1{animation-delay:.2s}.s2{animation-delay:.4s}.s3{animation-delay:.6s}
.endpoint{animation:settle 1.2s ease-out 2.2s both}
@media(prefers-reduced-motion:reduce){.trace,.sheet,.endpoint{animation:none!important;stroke-dashoffset:0;opacity:1;transform:none}}
'''
    if motion and not static and name in ('systems-atlas', 'engineering-workbench'):
        css += '''
@keyframes enso-draw{0%,8%{stroke-dashoffset:1;opacity:.15}55%,82%{stroke-dashoffset:0;opacity:.6}100%{stroke-dashoffset:-1;opacity:.15}}
.enso-stroke{stroke-dasharray:1;animation:enso-draw 12s ease-in-out infinite}
@keyframes atlas-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes orbit-turn{to{transform:rotate(360deg)}}
@keyframes signal-run{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}
@keyframes ink-write{0%,12%{stroke-dashoffset:1;opacity:.2}60%,88%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:.2}}
@keyframes node-light{0%,70%,100%{opacity:.25}25%,45%{opacity:1}}
@keyframes cursor-blink{0%,45%{opacity:1}50%,95%{opacity:0}100%{opacity:1}}
.atlas-plane{animation:atlas-float 6s ease-in-out infinite}
.atlas-plane.p1{animation-delay:-2s}.atlas-plane.p2{animation-delay:-4s}
.atlas-orbit{animation:orbit-turn 18s linear infinite;transform-origin:0px 0px}
.atlas-signal,.bench-signal{stroke-dasharray:7 93;animation:signal-run 4.5s linear infinite}
.atlas-signal.p1{animation-delay:-1.5s}.atlas-signal.p2{animation-delay:-3s}
.bench-rotor{animation:orbit-turn 12s linear infinite;transform-origin:55px 48px}
.bench-ink{stroke-dasharray:1;animation:ink-write 6s ease-in-out infinite}
.bench-node{animation:node-light 4s ease-in-out infinite}
.bench-node.n1{animation-delay:.6s}.bench-node.n2{animation-delay:1.2s}.bench-node.n3{animation-delay:1.8s}.bench-node.n4{animation-delay:2.4s}
.bench-cursor{animation:cursor-blink 1.2s steps(1,end) infinite}
@media(prefers-reduced-motion:reduce){.enso-stroke,.atlas-plane,.atlas-orbit,.atlas-signal,.bench-rotor,.bench-ink,.bench-node,.bench-cursor,.bench-signal{animation:none!important;transform:none!important;stroke-dashoffset:0!important;opacity:1!important}}
'''
    grad = f'''<linearGradient id="wash" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{C['bg']}"/><stop offset="1" stop-color="{C['low']}"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{C['edge']}" stroke-width=".6" opacity=".28"/></pattern>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(TITLES[name])}</title><desc id="desc">{escape(desc)}</desc>
<defs>{grad}<style>{css}</style><clipPath id="frame"><rect width="{w}" height="{h}" rx="20"/></clipPath></defs>
<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="url(#wash)"/><rect width="{w}" height="{h}" fill="url(#grid)"/>{content}</g>
<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="19.25" fill="none" stroke="{C['edge']}" stroke-width="1.5"/>
</svg>
'''


TITLES = {
 'engineering-workbench':'The engineering workbench — different tools, deliberate choices',
 'systems-atlas':'The systems atlas — ten products, one engineering practice',
 'orifold-cutaway':'Orifold — from mixed files to a finished document',
 'voyalier-cutaway':'Voyalier — from scattered travel details to a departure brief',
 'golavo-cutaway':'Golavo — from a forecast to an accountable record',
 'delivery-loop':'Build beyond the demo — define, build, verify, ship',
}
DESCRIPTIONS = {
 'engineering-workbench':'A tool palette: Swift and PDFKit; Rust and Tauri; Python, FastAPI and SQLite; TypeScript and Astro. GitHub Actions, AWS and Azure support delivery and cloud work. Original document, chassis, graph and browser-window illustrations represent tool categories, not shared application infrastructure.',
 'systems-atlas':'A conceptual portfolio map. Orifold, Voyalier, FolioOrb and Golavo address workflows and decisions. Codemble, Dusori and Nindova explore learning, research and finite play. Nimanto, Vidha and PalDawn focus on evidence and deliberate boundaries. Three etched planes and ten nodes represent the shared engineering practice, not shared application infrastructure. Every product is shown with its own app icon and purpose.',
 'orifold-cutaway':'Conceptual illustration: mixed input files enter a local Mac document workflow and emerge as a finished document. The diagram is an editorial illustration, not an application screenshot.',
 'voyalier-cutaway':'Conceptual illustration: reservations, official advice and plans are assembled into a reviewed, offline-ready departure brief. This is an editorial illustration, not an application screenshot.',
 'golavo-cutaway':'Conceptual illustration: a forecast is sealed before kickoff, then the result is observed and the track record is scored forward. No forecast probabilities or performance results are invented.',
 'delivery-loop':'An engineering practice: define the outcome, build the workflow, verify failure modes, then ship the documentation, installers and updates. Lessons return to the next definition. This describes an approach, not a claim that every project has every release artifact.',
}


# The atlas uses the same pinned app identities as the README collection.
# Data URLs keep nested SVG IDs/styles isolated and the artwork self-contained.
def atlas_icon(name, x, y, size):
    icon = (OUT / 'icons' / f'{name.lower()}-static.svg').read_bytes()
    encoded = base64.b64encode(icon).decode('ascii')
    return f'<image x="{x}" y="{y}" width="{size}" height="{size}" href="data:image/svg+xml;base64,{encoded}"/>'


ATLAS_GROUPS = [
    ('WORKFLOWS', '+ DECISIONS', 'gold', [
        ('Orifold', 'Finish the document'),
        ('Voyalier', 'Prepare the departure'),
        ('FolioOrb', 'Understand the portfolio'),
        ('Golavo', 'Inspect the forecast'),
    ]),
    ('LEARNING', '+ EXPLORATION', 'blue', [
        ('Codemble', 'Understand the codebase'),
        ('Dusori', 'Research with sources'),
        ('Nindova', 'Play something finite'),
    ]),
    ('EVIDENCE', '+ BOUNDARIES', 'teal', [
        ('Nimanto', 'Explore job matches'),
        ('Vidha', 'Rehearse a contingency'),
        ('PalDawn', 'Explore disease mechanisms'),
    ]),
]


def atlas_sculpture(cx, cy, scale=1):
    # Three etched planes, with 4/3/3 nodes matching the product group counts.
    # This is a conceptual atlas, not a dependency or data-flow graph.
    art = ''
    arc = 'M-177 97C-229 60 -206 -35 -123 -68C-32 -104 104 -78 169 -28C230 18 204 103 128 139C49 176 -74 160 -130 133'
    art += path(arc, 'edge', 1.5, extra='opacity=".7"')
    art += path(arc, 'gold', 3, extra='class="enso-stroke" pathLength="1" opacity=".65"')
    art += path('M-224 35H-207M207 35H224M0 -98V-84M0 155V172', 'edge', 1)
    for plane_index, (yy, col, nodes) in enumerate([(76, 'teal', [(-55, 40), (0, 64), (55, 40)]),
                           (24, 'blue', [(-55, 40), (0, 64), (55, 40)]),
                           (-28, 'gold', [(-90, -12), (-30, 20), (29, -11), (90, -28)])]):
        art += f'<g transform="translate(0 {yy})"><g class="atlas-plane p{plane_index}">'
        art += path('M-154 0L0 -82L154 0L0 82Z', col, 1.5, 'panel')
        art += path('M-154 0V10L0 92L154 10V0L0 82Z', col, 1, 'low')
        art += path('M-122 0L0 -65L122 0L0 65Z', col, .8, extra='opacity=".3"')
        for dx in [-62, 0, 62]:
            art += path(f'M{dx-46} -24L{dx+46} 25', col, .6, extra='opacity=".16"')
        route = 'M' + 'L'.join(f'{x} {y}' for x, y in nodes)
        art += path(route, col, 3, extra='class="trace" pathLength="1"')
        art += path(route, 'text', 2, extra=f'class="atlas-signal p{plane_index}" pathLength="100"')
        for x, y in nodes:
            art += dot(x, y, col, 4)
            art += f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="{C[col]}" opacity=".3"/>'
        art += '</g></g>'
    art += path('M-178 97L-168 103M178 -17L168 -23', 'gold', 2)
    return f'<g aria-hidden="true" transform="translate({cx} {cy}) scale({scale})">{art}</g>'


def atlas(mobile):
    if mobile:
        w, h = 360, 1385
        s = label(24, 37, 'THE SYSTEMS ATLAS', 'gold', 14)
        s += text(24, 86, 'Different problems.', 31, family='serif')
        s += text(24, 133, 'The same care.', 34, family='serif')
        s += text(24, 176, 'Ten independent products.', 19, 'muted')
        s += atlas_sculpture(180, 255, .5)
        s += line(24, 350, 336, 350)
        starts = [390, 737, 1018]
        for (title, subtitle, col, products), top in zip(ATLAS_GROUPS, starts):
            s += dot(30, top-5, col, 4)
            s += label(46, top, title + ' ' + subtitle, col, 13)
            for i, (name, detail) in enumerate(products):
                y = top + 48 + i * 70
                if i < len(products)-1:
                    s += line(47, y+37, 47, y+66, col, 1, extra='opacity=".45"')
                s += atlas_icon(name, 24, y-18, 46)
                s += text(84, y+3, name, 24, weight=600)
                # Explicit wraps keep descriptions legible at a 288px image width.
                lines = {'FolioOrb':['Understand the portfolio'],
                         'Codemble':['Understand the codebase'],
                         'PalDawn':['Explore disease', 'mechanisms']}.get(name, [detail])
                for j, words in enumerate(lines):
                    s += text(84, y+31+j*25, words, 17, 'muted')
            if top != starts[-1]:
                s += line(24, top+len(products)*70+42, 336, top+len(products)*70+42)
        s += line(24, 1300, 336, 1300)
        s += text(24, 1333, 'Independent by design.', 21, family='serif')
        s += text(24, 1361, 'Explore the collection below ↓', 17, 'muted')
        return w, h, s

    w, h = 1200, 864
    s = label(44, 46, 'THE SYSTEMS ATLAS', 'gold', 15)
    s += text(44, 117, 'Different problems.', 59, family='serif')
    s += text(44, 202, 'The same care.', 64, family='serif')
    s += text(47, 255, 'Ten independent products. One engineering practice.', 22, 'muted')
    s += text(47, 294, 'Built to be used, inspected, and kept.', 22, 'muted')
    s += atlas_sculpture(948, 156, 1.02)
    # Three branches occupy the open band above the product trails.
    s += path('M948 338V350H226Q208 350 208 366V379', 'gold', 1.5,
              extra='class="trace t1" pathLength="1" data-connector="atlas"')
    s += path('M948 338V350H600V379', 'blue', 1.5,
              extra='class="trace t1" pathLength="1" data-connector="atlas"')
    s += path('M948 338V350H992V379', 'teal', 1.5,
              extra='class="trace t2" pathLength="1" data-connector="atlas"')
    for x in [407, 799]:
        s += line(x, 397, x, 774, 'edge', 1)
    for (title, subtitle, col, products), x in zip(ATLAS_GROUPS, [44, 436, 828]):
        s += label(x, 408, title, col, 16)
        s += label(x, 434, subtitle, col, 14)
        for i, (name, detail) in enumerate(products):
            y = 481 + i * 82
            if i < len(products)-1:
                s += line(x+25, y+33, x+25, y+77, col, 1, extra='opacity=".4"')
            s += atlas_icon(name, x, y-21, 50)
            s += text(x+68, y+3, name, 28, weight=600)
            s += text(x+68, y+35, detail, 20, 'muted')
    s += line(44, 793, 1156, 793)
    s += text(44, 833, 'Independent by design.', 26, family='serif')
    s += text(1156, 832, 'Explore the collection below ↓', 20, 'gold', anchor='end')
    return w, h, s


def bench_glyph(x, y, kind, col, scale=1):
    """Original tool illustrations: a document, a chassis, a graph, and a window."""
    shapes = {
        'Swift': 'M24 6H65L86 27V89H24ZM65 6V27H86M37 42H71M37 55H65M37 68H57',
        'Rust': 'M55 8L89 28V68L55 88L21 68V28ZM55 28L72 38V58L55 68L38 58V38ZM55 0V8M55 88V96M13 24L21 28M89 68L97 72M13 72L21 68M89 28L97 24',
        'Python': 'M23 23H55V49H88M23 75H55V49M55 49V13M23 23V75',
        'TypeScript': 'M12 13H98V83H12ZM12 31H98M24 22H25M33 22H34M42 22H43M38 47L27 57L38 67M71 47L82 57L71 67M60 43L50 71',
    }
    art = f'<ellipse cx="55" cy="101" rx="48" ry="8" fill="{C["bg"]}" opacity=".6"/>'
    art += path(shapes[kind], col, 2.4, extra=('class="bench-rotor"' if kind == 'Rust' else 'class="trace" pathLength="1"'))
    if kind == 'Swift':
        art += path('M37 42H71M37 55H65M37 68H57', 'text', 3, extra='class="bench-ink" pathLength="1"')
    if kind == 'TypeScript':
        art += path('M76 74H88', 'text', 3, extra='class="bench-cursor"')
    if kind == 'Python':
        for index, (px, py) in enumerate([(23,23),(23,75),(55,49),(88,49),(55,13)]):
            art += dot(px, py, col, 7, extra=f'class="bench-node n{index}"')
            art += f'<circle cx="{px}" cy="{py}" r="7" fill="none" stroke="{C[col]}" stroke-width="2"/>'
    return f'<g aria-hidden="true" transform="translate({x} {y}) scale({scale})">{art}</g>'


def workbench(mobile):
    tools = [('Swift', 'PDFKit', 'gold'), ('Rust', 'Tauri', 'blue'),
             ('Python', 'FastAPI · SQLite', 'teal'), ('TypeScript', 'Astro', 'gold')]
    if mobile:
        w, h = 360, 752
        s = label(24, 37, 'THE ENGINEERING WORKBENCH', 'gold', 13)
        s += text(24, 85, 'Different tools.', 32, family='serif')
        s += text(24, 130, 'Deliberate choices.', 31, family='serif')
        for i, (name, detail, col) in enumerate(tools):
            x, y = 24 + (i%2)*168, 166 + (i//2)*230
            s += rect(x, y, 144, 202, 'panel', 'edge', 14)
            s += bench_glyph(x+22, y+15, name, col, .9)
            s += text(x+14, y+144, name, 22, weight=600)
            s += text(x+14, y+177, detail, 15 if name=='Python' else 18, 'muted')
        s += path('M96 616V640H264V616M180 640V662', 'edge', 1.5,
                  extra='class="trace t2" pathLength="1" data-connector="bench"')
        s += path('M96 616V640H264V616', 'gold', 2.5, extra='class="bench-signal" pathLength="100"')
        s += text(24, 695, 'Delivery & cloud', 22, weight=600)
        s += text(24, 726, 'GitHub Actions · AWS · Azure', 18, 'muted')
    else:
        w, h = 1200, 446
        s = label(44, 42, 'THE ENGINEERING WORKBENCH', 'gold', 15)
        s += text(44, 93, 'Different tools. Deliberate choices.', 40, family='serif')
        for i, (name, detail, col) in enumerate(tools):
            x = 44 + i*284
            s += rect(x, 131, 260, 203, 'panel', 'edge', 14)
            s += bench_glyph(x+145, 151, name, col, .85)
            s += line(x+22, 157, x+60, 157, col, 3)
            s += text(x+22, 272, name, 29, weight=600)
            s += text(x+22, 307, detail, 21, 'muted')
            s += path(f'M{x+130} 334V365', col, 1.5,
                      extra='class="trace t1" pathLength="1" data-connector="bench"')
        s += path('M174 365H1026', 'edge', 1.5,
                  extra='class="trace t2" pathLength="1" data-connector="bench"')
        s += path('M174 365H1026', 'gold', 3, extra='class="bench-signal" pathLength="100"')
        s += text(44, 413, 'Delivery & cloud', 25, family='serif')
        s += text(1156, 413, 'GitHub Actions · AWS · Azure', 23, 'muted', anchor='end')
    return w, h, s


def document(x,y,accent='blue',scale=1,seal=False):
    s=path('M0 0H64L88 24V116H0Z','edge',1.8,'panel')
    s+=path('M64 0V24H88',accent,1.7)
    for yy,ll in [(43,60),(58,46),(73,60),(88,35)]:s+=line(14,yy,ll,yy,accent,2)
    if seal:
        s+=f'<circle cx="75" cy="99" r="18" fill="{C[accent]}"/>'
        s+=path('M67 99L73 105L84 93','bg',3)
    return f'<g transform="translate({x} {y}) scale({scale})">{s}</g>'


def cutaway(kind,mobile):
    w,h=(600,580) if mobile else (1120,320)
    col={'orifold':'gold','voyalier':'blue','golavo':'teal'}[kind]
    titles={'orifold':('Orifold','One finished document.'),'voyalier':('Voyalier','Ready before departure.'),'golavo':('Golavo','A forecast with a memory.')}
    a,b=titles[kind]
    s=label(32 if mobile else 40,40,a.upper()+' / ENGINEERING NOTE',col,14)
    s+=text(32 if mobile else 40,89,b,32 if mobile else 37,family='serif')
    captions={'orifold':['MIXED FILES','LOCAL WORKFLOW','FINISHED ARTIFACT'],
              'voyalier':['TRAVEL DETAILS','REVIEW + ASSEMBLE','DEPARTURE BRIEF'],
              'golavo':['SEAL FORECAST','OBSERVE RESULT','SCORE FORWARD']}
    if mobile:
        # A 360-unit vertical composition keeps primary labels readable when the
        # image is displayed in a narrow 320px profile column.
        w,h=360,560
        s=label(20,34,a.upper()+' / ENGINEERING NOTE',col,14)
        s+=text(20,75,b,27,family='serif')
        for i,cap in enumerate(captions[kind]):
            y=112+i*126
            s+=rect(18,y,324,104)
            s+=text(101,y+39,cap,16,col,600)
            detail={'orifold':['PDFs, scans and documents','Repair, edit and protect','Keep the result on your Mac'],
                    'voyalier':['Reservations, advice and plans','Check the brief before you go','Carry the brief offline'],
                    'golavo':['Before kickoff','After the match','Keep the record visible']}[kind][i]
            s+=text(101,y+70,detail,15,'muted')
            if i<2:s+=path(f'M61 {y+104} V{y+126}',col,2)
            if kind=='golavo':
                s+=f'<circle cx="61" cy="{y+52}" r="25" fill="{C["low"]}" stroke="{C[col]}"/>'
                s+=text(61,y+60,['S','→','✓'][i],24,col,500,anchor='middle')
            else:s+=document(40,y+17,col,.55,i==2)
        s+=text(20,536,'Conceptual workflow · not an app screenshot',15,'muted')
        return w,h,s
    # Three stages, read left-to-right, with artifact silhouettes at actual readable scale.
    for x in [48,428,808]:s+=rect(x,129,264,130)
    s+=path('M324 194H414M404 187L414 194L404 201',col,2)
    s+=path('M704 194H794M784 187L794 194L784 201',col,2)
    if kind=='orifold':
        s+=document(70,150,col,.65)+document(97,161,col,.65)
        s+=text(169,178,'Mixed inputs',20,weight=600)+text(169,207,'One workspace',16,'muted')
        s+=prism(478,178,.34)+text(532,183,'On your Mac',20,weight=600)+text(532,211,'Repair · edit · protect',16,'muted')
        s+=document(831,147,col,.72,True)+text(925,181,'Finished',23,weight=600)+text(925,211,'Protected · local',16,'muted')
    elif kind=='voyalier':
        for yy,word in [(164,'Reservations'),(197,'Official advice'),(230,'Plans')]:
            s+=dot(72,yy-6,col,3)+text(88,yy,word,20)
        s+=path('M462 167C509 155 485 228 520 218S551 157 575 177',col,2)
        s+=dot(462,167,col)+dot(575,177,col)
        s+=text(605,188,'Review',20,weight=600)+text(605,219,'Assemble',16,'muted')
        s+=document(831,147,col,.72,True)+text(925,181,'Trip brief',23,weight=600)+text(925,211,'Offline-ready',16,'muted')
    else:
        for x,word,desc in [(48,'Sealed','Before kickoff'),(428,'Observed','After the match'),(808,'Scored','Forward record')]:
            s+=f'<circle cx="{x+47}" cy="186" r="22" fill="{C["low"]}" stroke="{C[col]}" stroke-width="1.5"/>'
            if x==48:s+=path('M86 184V178A9 9 0 0 1 104 178V184M83 184H107V202H83Z',col,1.8)
            elif x==428:s+=path('M462 186Q475 168 488 186Q475 204 462 186Z',col,1.8)+dot(475,186,col,4)
            else:s+=path('M844 187L853 195L867 177',col,2.5)
            s+=text(x+86,182,word,25,weight=600)+text(x+86,213,desc,17,'muted')
    for i,cap in enumerate(captions[kind]):s+=label(48+i*380,291,cap,col,12)
    return w,h,s


def delivery(mobile):
    steps = [('Define', 'The outcome'), ('Build', 'The workflow'),
             ('Verify', 'The failure modes'), ('Ship', 'The whole product')]
    colors = ['gold', 'blue', 'teal', 'gold']
    if mobile:
        w, h = 360, 600
        s = label(24, 36, 'BUILD BEYOND THE DEMO', 'gold', 14)
        s += text(24, 78, 'From intent to release.', 28, family='serif')
        # The feedback circuit stays outside every text block, in its own gutter.
        s += path('M42 450V482Q42 498 58 498H312Q328 498 328 482V118Q328 102 312 102H58Q42 102 42 118V126',
                  'gold', 1.5, extra='class="trace t2" pathLength="1" data-connector="return"')
        s += path('M37 119L42 126L47 119', 'gold', 1.5)
        for i, (title, desc) in enumerate(steps):
            y = 146 + i * 100
            if i < 3:
                s += path(f'M42 {y+20}V{y+80}', 'edge', 2,
                          extra='class="trace" pathLength="1" data-connector="forward"')
            s += dot(42, y, 'panel', 19)
            s += text(42, y+6, str(i+1), 18, colors[i], 600, 'mono', 'middle')
            s += text(78, y+6, title, 28, weight=600)
            s += text(78, y+34, desc, 19, 'muted')
        s += text(24, 543, 'Lessons shape', 20, weight=600)
        s += text(24, 570, 'the next version.', 19, 'muted')
    else:
        w, h = 1120, 356
        s = label(40, 38, 'BUILD BEYOND THE DEMO', 'gold', 15)
        s += text(40, 84, 'From intent to release.', 38, family='serif')
        centers = [166, 428, 690, 952]
        s += path('M166 142H952', 'edge', 2)
        s += path('M166 142H952', 'gold', 2,
                  extra='class="trace" pathLength="1" data-connector="forward"')
        # Rounded return lane is outside the captions, with generous bottom space.
        s += path('M974 142H1062Q1082 142 1082 162V258Q1082 278 1062 278H58Q38 278 38 258V162Q38 142 58 142H138',
                  'gold', 1.5, extra='class="trace t2" pathLength="1" data-connector="return"')
        s += path('M130 137L138 142L130 147', 'gold', 1.5)
        for i, ((title, desc), x) in enumerate(zip(steps, centers)):
            s += dot(x, 142, 'panel', 22)
            s += f'<circle cx="{x}" cy="142" r="22" fill="none" stroke="{C[colors[i]]}" stroke-width="1.5"/>'
            s += text(x, 149, str(i+1), 20, colors[i], 600, 'mono', 'middle')
            s += text(x, 208, title, 32, weight=600, anchor='middle')
            s += text(x, 241, desc, 22, 'muted', anchor='middle')
        s += text(560, 323, 'Lessons shape the next version.', 21, 'muted', anchor='middle')
    return w, h, s


for theme in PALETTES:
    C=PALETTES[theme]
    for mobile in (False,True):
        for name in TITLES:
            animated = name in ('systems-atlas','delivery-loop','engineering-workbench')
            if name=='systems-atlas':w,h,s=atlas(mobile)
            elif name=='delivery-loop':w,h,s=delivery(mobile)
            elif name=='engineering-workbench':w,h,s=workbench(mobile)
            else:w,h,s=cutaway(name.split('-')[0],mobile)
            for static in ((False,True) if animated else (True,)):
                filename=f'{name}{"-mobile" if mobile else ""}-{theme}{"-static" if animated and static else ""}.svg'
                (OUT/filename).write_text(frame(name,w,h,s,animated,static))
                MANIFEST.append(dict(file=filename,family=name,theme=theme,mobile=mobile,motion=animated and not static,
                                     width=w,height=h,alt=DESCRIPTIONS[name],bytes=(OUT/filename).stat().st_size))
(HERE/'asset-manifest.json').write_text(json.dumps(MANIFEST,indent=2)+'\n')
print(f'Created {len(MANIFEST)} SVG assets; {sum(m["bytes"] for m in MANIFEST):,} bytes total.')
