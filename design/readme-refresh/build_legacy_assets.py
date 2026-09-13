"""Build the profile masthead, wizard note, and delivery-impact SVGs.

The three families share layout primitives, type roles, and palette tokens so
dark/light and desktop/mobile variants cannot drift. The output is deterministic
and self-contained; it uses no network resources or scripts.
"""

from html import escape
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "assets"

PALETTES = {
    "dark": {
        "paper": "#111719",
        "paper_2": "#223137",
        "ink": "#F5F0E8",
        "muted": "#B7C2BD",
        "faint": "#97A39F",
        "rule": "#3B4948",
        "accent": "#E58B78",
        "accent_2": "#CCAC72",
        "blue": "#99B5CB",
        "teal": "#A5BBA7",
        "shade": "#0B1012",
    },
    "light": {
        "paper": "#F7F5EF",
        "paper_2": "#EDEEE8",
        "ink": "#20292B",
        "muted": "#53615E",
        "faint": "#53615E",
        "rule": "#C8CDC5",
        "accent": "#994535",
        "accent_2": "#806329",
        "blue": "#3F627A",
        "teal": "#4B6956",
        "shade": "#FFFEFA",
    },
}

CRITIQUE = "Hallmark · pre-emit critique: P5 H5 E4 S5 R5 V4"
STAMP = (
    "Hallmark · genre: editorial · macrostructure: Map / Diagram · "
    "theme: Atelier · enrichment: hand-built SVG · nav: N6 · footer: Ft2"
)


def token_css(theme: str, animated: bool) -> str:
    motion = ""
    if animated:
        motion = """
.draw{stroke-dasharray:1;stroke-dashoffset:1;animation:draw .8s cubic-bezier(.16,1,.3,1) both}
.enter{animation:enter .5s cubic-bezier(.16,1,.3,1) both}
.enter.d1{animation-delay:.08s}.enter.d2{animation-delay:.16s}.enter.d3{animation-delay:.24s}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes enter{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.draw,.enter,.wizard-motion,.spell-motion{animation:none!important;stroke-dashoffset:0!important;opacity:1!important;transform:none!important}}
"""
    return f"""/* {CRITIQUE} */
/* {STAMP} */
text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;font-kerning:normal}}
.display{{font-family:Georgia,'Times New Roman',serif;font-style:normal}}
.mono{{font-family:'SFMono-Regular',Consolas,monospace;letter-spacing:1.4px}}
{motion}"""


def resolve_tokens(source: str, theme: str) -> str:
    """Emit concrete colors because several README SVG renderers reject CSS vars."""
    for name, value in PALETTES[theme].items():
        source = source.replace(f"var(--{name.replace('_', '-')})", value)
    return source


def frame(title: str, desc: str, width: int, height: int, body: str, theme: str,
          animated: bool, family: str) -> str:
    css = token_css(theme, animated)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc" data-family="{family}" data-static="{str(not animated).lower()}">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><style>{css}</style>
<linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="var(--paper)"/><stop offset="1" stop-color="var(--paper-2)"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="var(--rule)" stroke-width=".6" opacity=".22"/></pattern>
<clipPath id="frame"><rect width="{width}" height="{height}" rx="20"/></clipPath></defs>
<g clip-path="url(#frame)"><rect width="{width}" height="{height}" fill="url(#surface)"/><rect width="{width}" height="{height}" fill="url(#grid)"/>{body}</g>
<rect x=".75" y=".75" width="{width - 1.5}" height="{height - 1.5}" rx="19.25" fill="none" stroke="var(--rule)" stroke-width="1.5"/>
</svg>
'''
    return resolve_tokens(svg, theme)


def txt(x, y, words, size, cls="", fill="ink", weight=400, anchor="start", extra=""):
    fill_token = fill.replace("_", "-")
    return (
        f'<text x="{x}" y="{y}" class="{cls}" fill="var(--{fill_token})" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" {extra}>'
        f'{escape(words)}</text>'
    )


def rule(x1, y1, x2, y2, color="rule", width=1.5, cls="", extra=""):
    color_token = color.replace("_", "-")
    return (
        f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="var(--{color_token})" '
        f'stroke-width="{width}" stroke-linecap="round" class="{cls}" {extra}/>'
    )


def masthead(mobile: bool, animated: bool) -> tuple[int, int, str]:
    if mobile:
        width, height = 360, 488
        body = rule(24, 24, 336, 24, "accent", 1.5, "draw", 'pathLength="1"')
        body += txt(24, 52, "CHICAGO · BUILDING IN PUBLIC", 13, "mono enter", "muted", 700)
        body += txt(24, 112, "Umang Dhawan", 36, "display enter d1", "ink", 600)
        body += txt(24, 148, "Technology consultant", 20, "enter d2", "ink", 700)
        body += txt(24, 176, "Open-source product builder", 18, "enter d2", "blue", 650)
        body += txt(24, 213, "Complex ideas, made reliable", 16, "enter d3", "muted", 500)
        body += txt(24, 239, "enough to ship.", 16, "enter d3", "muted", 500)
        body += rule(24, 258, 336, 258)
        body += txt(24, 286, "FOCUS / 01—04", 13, "mono", "accent", 700)
        cells = [
            (24, 316, "01", "PRODUCT SYSTEMS", "Strategy through software", "accent"),
            (200, 316, "02", "QUALITY ENG.", "Evidence before claims", "blue"),
            (24, 393, "03", "CLOUD", "Observable and resilient", "teal"),
            (200, 393, "04", "APPLIED AI", "Useful and bounded", "accent_2"),
        ]
        for x, y, number, title, detail, color in cells:
            body += txt(x, y, number, 13, "mono", color, 700)
            body += txt(x, y + 24, title, 15, "", "ink", 750)
            body += txt(x, y + 46, detail, 13, "", "muted", 500)
        return width, height, body

    width, height = 1200, 360
    body = rule(52, 30, 1148, 30, "accent", 1.5, "draw", 'pathLength="1"')
    body += txt(52, 62, "CHICAGO · BUILDING IN PUBLIC", 15, "mono enter", "muted", 700)
    body += txt(52, 139, "Umang Dhawan", 68, "display enter d1", "ink", 600)
    body += txt(54, 181, "Technology consultant  ·  Open-source product builder", 23, "enter d2", "ink", 650)
    body += txt(54, 217, "I turn complex ideas into reliable systems that ship.", 19, "enter d3", "muted", 500)
    body += rule(54, 246, 1146, 246)
    body += txt(54, 277, "FOCUS / 01—04", 14, "mono", "accent", 700)
    items = [
        (54, "PRODUCT SYSTEMS", "Strategy through software", "accent"),
        (330, "QUALITY ENGINEERING", "Evidence before claims", "blue"),
        (651, "CLOUD RELIABILITY", "Observable and resilient", "teal"),
        (953, "APPLIED AI", "Useful and bounded", "accent_2"),
    ]
    for index, (x, title, detail, color) in enumerate(items, 1):
        body += txt(x, 314, f"0{index}", 14, "mono", color, 700)
        body += txt(x + 38, 314, title, 16, "", "ink", 750)
        body += txt(x + 38, 338, detail, 14, "", "muted", 500)
    return width, height, body


def wizard_scene(x: int, y: int, scale: float, animated: bool) -> str:
    animation_css = ""
    if animated:
        animation_css = """
<style>
.wizard-motion{transform-origin:72px 122px;animation:wizard 6.4s cubic-bezier(.16,1,.3,1) infinite}
.spell-motion{transform-origin:142px 59px;animation:spell 6.4s cubic-bezier(.16,1,.3,1) infinite}
@keyframes wizard{0%,18%,72%,100%{transform:translateY(0)}34%,50%{transform:translateY(-4px)}}
@keyframes spell{0%,25%,68%,100%{opacity:0;transform:translateX(0) scale(.7)}38%{opacity:1;transform:translateX(0) scale(1)}58%{opacity:.9;transform:translateX(50px) scale(.9)}}
</style>"""
    scene = f'''{animation_css}<g transform="translate({x} {y}) scale({scale})">
<rect width="220" height="150" rx="18" fill="var(--shade)" stroke="var(--rule)"/>
<clipPath id="scene-clip"><rect x="1" y="1" width="218" height="148" rx="17"/></clipPath>
<g clip-path="url(#scene-clip)"><path d="M0 116L110 82L220 116V150H0Z" fill="var(--paper-2)"/><path d="M0 116H220M110 82V150M44 103L63 150M176 103L157 150" fill="none" stroke="var(--rule)" opacity=".5"/>
<g class="wizard-motion"><ellipse cx="71" cy="130" rx="39" ry="7" fill="var(--paper)" opacity=".65"/>
<path d="M39 41H58V29H80V38H94V51H108V64H28V52H39Z" fill="var(--blue)"/><rect x="25" y="59" width="88" height="12" fill="var(--paper)"/><rect x="36" y="61" width="61" height="8" fill="var(--accent)"/>
<rect x="48" y="71" width="45" height="32" fill="var(--accent-2)"/><rect x="53" y="72" width="36" height="27" fill="var(--accent)"/><rect x="58" y="81" width="7" height="6" fill="var(--paper)"/><rect x="78" y="81" width="7" height="6" fill="var(--paper)"/>
<path d="M43 102H98L116 137H27Z" fill="var(--blue)"/><path d="M61 101H81L87 137H55Z" fill="var(--ink)" opacity=".86"/><rect x="65" y="109" width="13" height="13" fill="var(--accent)"/><rect x="22" y="105" width="32" height="23" rx="2" fill="var(--paper)" stroke="var(--faint)"/><path d="M26 110H48M26 116H43" stroke="var(--teal)" stroke-width="3"/>
<path d="M94 101H112V111H126V121H109V112H94Z" fill="var(--blue)"/><rect x="122" y="109" width="11" height="11" fill="var(--accent)"/><path d="M130 112L151 67" stroke="var(--accent)" stroke-width="5" stroke-linecap="square"/></g>
<g class="spell-motion"><path d="M151 61H162V50H171V61H182V70H171V81H162V70H151Z" fill="var(--accent)"/><path d="M171 65C187 52 200 72 218 57" fill="none" stroke="var(--teal)" stroke-width="4" stroke-linecap="round"/><circle cx="197" cy="45" r="4" fill="var(--accent-2)"/><circle cx="211" cy="83" r="3" fill="var(--blue)"/></g></g></g>'''
    return scene


def wizard(mobile: bool, animated: bool) -> tuple[int, int, str]:
    if mobile:
        width, height = 360, 440
        body = txt(24, 37, "AI, WITH GUARDRAILS", 14, "mono", "accent", 700)
        body += wizard_scene(70, 55, 1, animated)
        body += txt(24, 255, "AI can draft the spell.", 25, "display enter d1", "ink", 600)
        body += txt(24, 288, "I still review the blast radius.", 23, "display enter d2", "muted", 500)
        body += rule(24, 316, 86, 316, "accent", 3)
        body += txt(24, 349, "CAST · CHECK · SHIP", 14, "mono", "faint", 700)
        body += txt(24, 391, "DP: LAYLA · MY BERNEDOODLE", 13, "mono", "muted", 650)
        body += txt(24, 414, "AKA “BEAR”", 13, "mono", "accent", 700)
        return width, height, body

    width, height = 1200, 230
    body = wizard_scene(38, 40, 1, animated)
    body += txt(302, 57, "AI, WITH GUARDRAILS", 15, "mono enter", "accent", 700)
    body += txt(302, 113, "AI can draft the spell.", 34, "display enter d1", "ink", 600)
    body += txt(302, 153, "I still review the blast radius.", 30, "display enter d2", "muted", 500)
    body += rule(304, 179, 374, 179, "accent", 3)
    body += txt(394, 185, "CAST · CHECK · SHIP", 14, "mono", "faint", 700)
    body += txt(1148, 203, "DP: LAYLA · MY BERNEDOODLE · AKA “BEAR”", 14, "mono", "muted", 650, "end")
    return width, height, body


IMPACTS = [
    ("100+", "LOCATIONS", "retail platform shipped", "accent"),
    ("ZERO", "AUDIT FINDINGS", "federal cloud delivery", "accent_2"),
    ("4", "CLOUD PRODUCTS", "quality leadership", "blue"),
    ("3", "CONTINENTS", "worked with teams", "teal"),
]


def impact(mobile: bool, animated: bool) -> tuple[int, int, str]:
    # Values have open typographic space, never a fixed-radius enclosure.
    if mobile:
        width, height = 360, 632
        body = txt(24, 38, "SELECTED DELIVERY IMPACT", 14, "mono", "accent", 700)
        body += txt(24, 76, "Experience, in practice.", 27, "display", "ink", 400)
        body += rule(24, 100, 336, 100)
        labels = ["Locations", "Audit findings", "Cloud products", "Continents"]
        details = [("Retail platform", "shipped"), ("Federal cloud", "delivery"),
                   ("Quality", "leadership"), ("Worked with", "teams")]
        for index, ((value, _, _, color), label, detail) in enumerate(zip(IMPACTS, labels, details)):
            y = 134 + index * 119
            body += rule(24, y, 56, y, color, 3, "draw", 'pathLength="1"')
            body += txt(24, y + 55, value, 40 if value == "ZERO" else 46, "display", color, 400)
            body += txt(162, y + 18, label, 20, "", "ink", 650)
            for line_index, words in enumerate(detail):
                body += txt(162, y + 48 + line_index * 28, words, 18, "", "muted", 400)
            if index < 3:
                body += rule(24, y + 94, 336, y + 94)
        body += txt(24, 609, "PROFILE RECORD · 2022—NOW", 13, "mono", "faint", 500)
        return width, height, body

    width, height = 1200, 356
    body = txt(48, 42, "SELECTED DELIVERY IMPACT", 15, "mono", "accent", 700)
    body += txt(1152, 42, "PROFILE RECORD · 2022—NOW", 14, "mono", "faint", 500, "end")
    body += txt(48, 92, "Experience, in practice.", 38, "display", "ink", 400)
    body += rule(48, 119, 1152, 119)
    for index, (value, label, detail, color) in enumerate(IMPACTS):
        x = 48 + index * 282
        if index:
            body += rule(x - 22, 151, x - 22, 315)
        body += rule(x, 151, x + 36, 151, color, 3, "draw", 'pathLength="1"')
        body += txt(x, 212, value, 62 if value == "ZERO" else 72, "display", color, 400)
        body += txt(x, 280, label.title(), 26, "", "ink", 650)
        body += txt(x, 313, detail, 20, "", "muted", 400)
    return width, height, body


FAMILIES = {
    "profile-header": (
        "Umang Dhawan — technology consultant and open-source product builder",
        "An editorial masthead introducing Umang Dhawan and four engineering focus areas: product systems, quality engineering, cloud reliability, and applied AI.",
        masthead,
    ),
    "ai-spell": (
        "AI, with guardrails",
        "A contained pixel-art wizard reviews a laptop and casts a spell. The accompanying line says AI can draft the spell while Umang reviews the blast radius. A note credits Layla, Umang's Bernedoodle, called Bear.",
        wizard,
    ),
    "impact-seals": (
        "Selected delivery impact",
        "Four profile-record figures: a retail platform shipped to more than 100 locations, zero findings on a federal cloud audit, quality leadership across four cloud products, and delivery with teams on three continents.",
        impact,
    ),
}


manifest = []
for theme in PALETTES:
    for mobile in (False, True):
        for name, (title, desc, builder) in FAMILIES.items():
            for static in (False, True):
                width, height, body = builder(mobile, not static)
                suffix = f'{"-mobile" if mobile else ""}-{theme}{"-static" if static else ""}.svg'
                destination = OUT / f"{name}{suffix}"
                destination.write_text(
                    frame(title, desc, width, height, body, theme, not static, name),
                    encoding="utf-8",
                )
                manifest.append({
                    "file": destination.name,
                    "family": name,
                    "theme": theme,
                    "mobile": mobile,
                    "motion": not static,
                    "width": width,
                    "height": height,
                    "bytes": destination.stat().st_size,
                })

(HERE / "legacy-asset-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print("Created 24 legacy-profile SVG variants.")
