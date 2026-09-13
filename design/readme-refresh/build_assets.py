"""Build original, self-contained SVG artwork for the proposed profile refresh.

Python standard library only. This regenerates only assets/profile-refresh, leaving the opening artwork and README intact.
Run from any working directory. Re-running produces identical SVG bytes.
"""
from pathlib import Path
from html import escape
import json

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / 'assets' / 'profile-refresh'
OUT.mkdir(exist_ok=True)
PALETTES = {
    'dark': dict(bg='#101923', panel='#172432', edge='#35485B', text='#F3EFE7',
                 muted='#B6C3CF', gold='#DEC078', blue='#9EBAF0', teal='#82CDD0', low='#21354A'),
    'light': dict(bg='#FAF8F2', panel='#FFFEFA', edge='#C5CFD7', text='#202D3C',
                  muted='#506173', gold='#8B651A', blue='#365BA0', teal='#206E73', low='#EAF0F4'),
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
 'systems-atlas':'The systems atlas — ten products, one engineering practice',
 'orifold-cutaway':'Orifold — from mixed files to a finished document',
 'voyalier-cutaway':'Voyalier — from scattered travel details to a departure brief',
 'golavo-cutaway':'Golavo — from a forecast to an accountable record',
 'delivery-loop':'Build beyond the demo — define, build, verify, ship',
}
DESCRIPTIONS = {
 'systems-atlas':'A conceptual portfolio map. Orifold, Voyalier, FolioOrb and Golavo address workflows and decisions. Codemble, Dusori and Nindova explore learning, research and finite play. Nimanto, Vidha and PalDawn focus on evidence and deliberate boundaries. Layered sheets at the center represent the shared engineering practice, not shared application infrastructure.',
 'orifold-cutaway':'Conceptual illustration: mixed input files enter a local Mac document workflow and emerge as a finished document. The diagram is an editorial illustration, not an application screenshot.',
 'voyalier-cutaway':'Conceptual illustration: reservations, official advice and plans are assembled into a reviewed, offline-ready departure brief. This is an editorial illustration, not an application screenshot.',
 'golavo-cutaway':'Conceptual illustration: a forecast is sealed before kickoff, then the result is observed and the track record is scored forward. No forecast probabilities or performance results are invented.',
 'delivery-loop':'An engineering practice: define the outcome, build the workflow, verify failure modes, then ship the documentation, installers and updates. Lessons return to the next definition. This describes an approach, not a claim that every project has every release artifact.',
}


def atlas(mobile):
    if mobile:
        w,h=360,780
        s=label(20,36,'THE SYSTEMS ATLAS','gold',15)
        s+=text(20,78,'Many problems.',30,family='serif')+text(20,112,'One engineering practice.',28,family='serif')
        s+=prism(180,187,.49)
        s+=line(180,260,180,286,'gold',2,extra='class="trace" pathLength="1"')
        s+=rect(18,282,324,186)
        s+=dot(38,312,'gold',4)+label(52,317,'WORKFLOWS + DECISIONS','gold',14)
        for x,y,name in [(38,355,'Orifold'),(198,355,'Voyalier'),(38,393,'FolioOrb'),(198,393,'Golavo')]:
            s+=text(x,y,name,20,weight=600)
        s+=text(38,438,'Documents · travel · portfolios · forecasts',15,'muted')
        s+=rect(18,484,324,116)
        s+=dot(38,514,'blue',4)+label(52,519,'LEARNING + EXPLORATION','blue',14)
        s+=text(38,556,'Codemble · Dusori',19,weight=600)+text(38,584,'Nindova',19,weight=600)
        s+=rect(18,616,324,116)
        s+=dot(38,646,'teal',4)+label(52,651,'EVIDENCE + BOUNDARIES','teal',14)
        s+=text(38,688,'Nimanto · Vidha',19,weight=600)+text(38,716,'PalDawn',19,weight=600)
        s+=text(20,760,'Independent products · one standard of care',15,'muted')
        return w,h,s
    w,h=1120,620
    s=label(40,43,'THE SYSTEMS ATLAS','gold')
    s+=text(40,92,'Many problems. One engineering practice.',39,family='serif')
    s+=text(40,126,'Ten products, connected by the care between an idea and a useful artifact.',19,'muted')
    # Lines sit behind the three semantic groupings, never cross through labels.
    s+=path('M334 326 H388 Q408 326 428 311 L455 296','gold',2.2,extra='class="trace" pathLength="1"')
    s+=path('M642 289 L672 272 Q694 260 714 260 H757','blue',2.2,extra='class="trace t1" pathLength="1"')
    s+=path('M642 352 L680 386 Q699 407 720 407 H757','teal',2.2,extra='class="trace t2" pathLength="1"')
    s+=prism(550,290,1.03)
    s+=text(550,494,'Beyond the demo.',26,'text',family='serif',anchor='middle')
    s+=text(550,525,'Reasoning. Failure modes. Ownership.',16,'muted',anchor='middle')
    s+=rect(40,178,294,334)
    s+=label(60,212,'WORKFLOWS + DECISIONS','gold',13)
    for i,(n,d) in enumerate([('Orifold','Finish the document'),('Voyalier','Prepare the departure'),('FolioOrb','Explain the portfolio'),('Golavo','Account for the forecast')]):
        y=251+i*66
        s+=dot(61,y-6,'gold',3)+text(76,y,n,23,weight=600)+text(76,y+23,d,16,'muted')
    s+=rect(757,178,323,167)
    s+=label(778,212,'LEARNING + EXPLORATION','blue',13)
    s+=text(778,249,'Codemble · Dusori',23,weight=600)+text(778,282,'Nindova',23,weight=600)
    s+=text(778,320,'Codebases · research · finite play',16,'muted')
    s+=rect(757,367,323,145)
    s+=label(778,401,'EVIDENCE + BOUNDARIES','teal',13)
    s+=text(778,438,'Nimanto · Vidha · PalDawn',21,weight=600)
    s+=text(778,478,'Matching · rehearsal · learning',16,'muted')
    s+=line(40,563,1080,563)
    s+=label(40,593,'INDEPENDENT PRODUCTS · ONE STANDARD OF CARE',size=15)
    s+=text(1080,593,'Explore below ↓',17,'gold',anchor='end')
    return w,h,s


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
            animated = name in ('systems-atlas','delivery-loop')
            if name=='systems-atlas':w,h,s=atlas(mobile)
            elif name=='delivery-loop':w,h,s=delivery(mobile)
            else:w,h,s=cutaway(name.split('-')[0],mobile)
            for static in ((False,True) if animated else (True,)):
                filename=f'{name}{"-mobile" if mobile else ""}-{theme}{"-static" if animated and static else ""}.svg'
                (OUT/filename).write_text(frame(name,w,h,s,animated,static))
                MANIFEST.append(dict(file=filename,family=name,theme=theme,mobile=mobile,motion=animated and not static,
                                     width=w,height=h,alt=DESCRIPTIONS[name],bytes=(OUT/filename).stat().st_size))
(HERE/'asset-manifest.json').write_text(json.dumps(MANIFEST,indent=2)+'\n')
print(f'Created {len(MANIFEST)} SVG assets; {sum(m["bytes"] for m in MANIFEST):,} bytes total.')
