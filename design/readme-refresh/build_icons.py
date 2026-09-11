"""Pin the user's actual project marks and add motion to the three static marks."""
from pathlib import Path
import xml.etree.ElementTree as ET
import json, re, hashlib

HERE=Path(__file__).resolve().parent
OUT=HERE.parent.parent/'assets'/'profile-refresh'/'icons'
OUT.mkdir(parents=True,exist_ok=True)
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
sources=json.loads((HERE/'icon-sources.json').read_text())
manifest=[]

def sub(root,tag,attrs=None,words=None):
    el=ET.SubElement(root,'{'+NS+'}'+tag,attrs or {})
    if words is not None:el.text=words
    return el

def still(svg,name):
    root=ET.fromstring(svg)
    for parent in list(root.iter()):
        for child in list(parent):
            tag=child.tag.split('}')[-1]
            if tag in ('animate','animateTransform','animateMotion','set'):
                # Orifold is a multi-stage fold. The 80% pose is the finished app
                # icon; the final timeline value intentionally fades it to zero.
                if name=='orifold' and tag=='animate' and child.get('values'):
                    vals=child.get('values').split(';')
                    times=[float(x) for x in child.get('keyTimes','').split(';') if x]
                    if len(times)==len(vals):
                        i=max(i for i,t in enumerate(times) if t<=.8)
                        parent.set(child.get('attributeName'),vals[i])
                parent.remove(child)
    sub(root,'style',words='* { animation: none !important; transition: none !important; }')
    return '\n'.join(line.rstrip() for line in ET.tostring(root,encoding='unicode').splitlines())+'\n'

for item in sources:
    name=item['project'].lower()
    # Golavo's dark tile and Nindova's light glyphs suit an inset dark app tile.
    index=1 if name=='nindova' else 0
    source=HERE/'icon-sources'/item['artwork'][index]['file']
    content=source.read_text()
    if name in ('folioorb','nindova','vidha'):
        root=ET.fromstring(content)
        if root.find('{'+NS+'}title') is None:
            sub(root,'title',words=item['project']+' — animated app mark')
        if name=='folioorb':
            art=root.find('{'+NS+'}g')
            root.remove(art)
            motion=sub(root,'g',{'class':'profile-orbit'});motion.append(art)
            css='.profile-orbit {transform-origin:512px 512px;animation:profile-orbit 12s linear infinite}@keyframes profile-orbit {to{transform:rotate(360deg)}}'
        elif name=='nindova':
            root.set('viewBox','-5 -5 58 58')
            root.insert(0,ET.Element('{'+NS+'}rect',{'x':'-5','y':'-5','width':'58','height':'58','rx':'12','fill':'#171623'}))
            for i,p in enumerate(root.findall('{'+NS+'}path')):
                p.set('class','profile-diamond')
                p.set('style',f'animation-delay:{-i*.18}s')
            css='.profile-diamond{transform-box:fill-box;transform-origin:center;animation:profile-diamond 6s ease-in-out infinite}@keyframes profile-diamond{0%,40%,100%{transform:scale(1)}18%{transform:scale(.74)}27%{transform:scale(1.06)}}'
        else:
            art=sub(root,'g',{'class':'profile-courier'})
            bird_started=False
            for el in list(root):
                if el.tag.split('}')[-1]=='path' and el.get('fill')=='#CBBF9F':
                    bird_started=True
                if bird_started and el is not art:
                    root.remove(el);art.append(el)
            css='.profile-courier{transform-origin:256px 256px;animation:profile-courier 7s ease-in-out infinite}@keyframes profile-courier{0%,48%,100%{transform:translateY(0) rotate(0)}20%{transform:translateY(-7px) rotate(-1.4deg)}32%{transform:translateY(-3px) rotate(.7deg)}}'
        css+='@media(prefers-reduced-motion:reduce){*{animation:none!important}}'
        sub(root,'style',words=css)
        content=ET.tostring(root,encoding='unicode')+'\n'
    content='\n'.join(line.rstrip() for line in content.splitlines())+'\n'
    (OUT/f'{name}.svg').write_text(content)
    (OUT/f'{name}-static.svg').write_text(still(content,name))
    manifest.append({'project':item['project'],'file':f'icons/{name}.svg','static':f'icons/{name}-static.svg',
                     'source':item['artwork'][index]['source'],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                     'motion':'Added orbit / diamond / courier motion' if name in ('folioorb','nindova','vidha') else 'Preserved original project animation'})
(HERE/'icon-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Prepared 10 animated app marks and 10 static counterparts.')
