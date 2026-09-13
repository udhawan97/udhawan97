# Profile field guide

Implemented September 11, 2026 and polished September 13, 2026. The audience is a recruiter making a quick
assessment and a developer deciding which repository to explore.

## Reading order

1. Name masthead with an original drawn UD monogram; contact links immediately below.
2. A concise introduction, current role, and four working navigation anchors.
3. The illustrated ten-product atlas, three direct starting points, and three
   expandable collections. Each project opens into an icon heading and description,
   avoiding narrow table columns on phones.
4. The delivery loop and four concise engineering principles.
5. The animated engineering workbench, the personal AI/wizard note, and Agent Toolkit.
6. Delivery impact, career history, education, optional activity, and a closing invitation.

The four top-level section anchors are preserved. Masthead, wizard and impact
variants share a deterministic generator. All factual project descriptions,
employment details and existing destinations remain intact.

## Artwork

Six diagram families produce 36 self-contained SVG files:

- **Systems atlas:** three product trails beneath an original etched-plane
  illustration. Its 4/3/3 nodes match the three product groups. Each product has
  its pinned app identity and a concise purpose. It describes shared engineering
  practice, not shared code or infrastructure.
- **Orifold:** mixed files, local document workflow, finished artifact.
- **Voyalier:** travel details, review and assembly, departure brief.
- **Golavo:** a sealed forecast, observed result, forward scoring.
- **Delivery loop:** define, build, verify, ship, and return lessons to the next version.
- **Engineering workbench:** four original illustrated tool modules and a delivery/cloud rail.

Each has dark/light desktop and independently composed 360-unit mobile artwork. The atlas,
delivery loop and engineering workbench also have explicit static files. The delivery-loop entrance settles within 3.5 seconds; the atlas and workbench
now have ongoing, gentle motion with explicit static alternatives. The illustrations contain no screenshots, invented metrics,
scripts, external stylesheets, remote fonts, or foreignObject content.

The final palette takes a modern Japanese editorial direction: charcoal ink,
warm paper, restrained vermilion, slate blue and sage for semantic groupings. Georgia carries restrained display
headlines; system sans-serif carries descriptions; monospace carries small labels.
The palette is defined in `build_assets.py`.

Three opening/impact families produce 24 additional self-contained SVG files:

- **Masthead:** an editorial introduction, original drawn UD mark, and four-part focus index.
- **AI with guardrails:** a contained pixel-wizard scene with stationary copy.
- **Selected delivery impact:** an open four-column typographic ledger with large
  color-coded figures. Mobile uses four spacious rows with wrapped descriptions.
  Fixed-radius seals no longer constrain the values.

Meaningful mobile labels use a 360-unit canvas sized for a 288–320px rendered
image. Effects stay inside local scene clips, connector paths use empty lanes,
and every animated asset has an explicit static sibling for reduced motion and
fallback rendering. The masthead no longer embeds or hides unused project marks.

The ten project icons use the user's actual artwork, pinned from the sources in
`icon-sources.json`. Seven retain their native animation. FolioOrb, Nindova, and
Vidha receive orbit, diamond, and courier movement respectively. Every icon has a
static counterpart selected by a reduced-motion picture source. The Orifold
static counterpart captures its finished-icon phase at 80% of its existing
animation; the Nimanto static counterpart keeps its original finished base pose. Vidha uses the newly merged
`apps/web/public/vidha-icon.svg` courier-and-envelope artwork (source SHA-256 recorded
in `icon-manifest.json`), not the older icon retained in the legacy assets directory.

The opening and impact graphics use a 600px responsive switch. Diagrams switch
to their dedicated mobile compositions at 700px.
App icons stay at a fixed compact display size and do not need mobile copies.

## Copy and evidence

Project descriptions were checked against the public project READMEs recorded in
`evidence/sources.json` on September 11, 2026. These are source-level product claims,
not independent acceptance tests of all ten applications. The profile avoids
pinning volatile release versions or implying uniform maturity. Golavo is labeled
pre-alpha; Vidha remains a local synthetic pre-alpha prototype; PalDawn remains
conceptual, source-linked learning.

Employment, education, and enterprise impact figures are carried forward from
the owner's existing README. They were not independently audited in this refresh.
No adoption, performance, quality, or forecast-accuracy metrics were invented.

## Maintenance

From the repository root:

```sh
python3 design/readme-refresh/build_legacy_assets.py
python3 design/readme-refresh/build_icons.py
python3 design/readme-refresh/build_assets.py
python3 design/readme-refresh/build_preview.py
python3 design/readme-refresh/validate_assets.py
python3 -m http.server 8767 --bind 127.0.0.1
```

Open `http://127.0.0.1:8767/design/readme-refresh/preview.html` in Safari. The preview
uses GitHub's Markdown API when available (with a markdown-it fallback). Native
acceptance retains the README's real `<picture>` sources and reports each loaded
file and image width. The separate gallery can force theme, motion, and mobile
variants for inspection. Its controls do not claim to emulate browser media
preferences. GitHub's actual profile remains the final rendering check. The
preview builder prefers an authenticated `gh` CLI; its offline fallback needs
`markdown-it-py`.

The asset generators and validator use Python's standard library and pinned local
source SVGs; they require no network access. The validator checks all README SVG
references, accessible metadata, fragment integrity, reduced-motion states,
mobile text scale, deterministic output, and librsvg rasterization when available.
Generated previews and screenshots stay ignored. The manifests record intended
variants, generated dimensions, and project-mark provenance.

GitHub picture support: [GitHub documentation](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#the-picture-element).
SVG image restrictions: [MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image).

## September 13 follow-up: reported text bleeding

The two screenshot defects are repaired in their generators and all 16 outputs.
The impact design replaces undersized circles with open metric columns, an
editorial heading, and quieter rules. The delivery diagram uses numbered stages
and a continuous rounded return circuit with a dedicated outer gutter. Captions
and the feedback line no longer share space. Text is stationary; only route and
accent strokes draw in. Both families retain their existing README paths,
source facts, light/dark palettes, and explicit static variants.

For the focused browser regression check, serve the repository and open
`design/readme-refresh/check_layout.html`. It inspects actual SVG text bounds in
Safari for every changed variant under native, Arial and Times fallback fonts,
and samples the delivery connectors for text clearance. It bypasses the browser
fetch cache so earlier artwork cannot produce a misleading result. The visible
art uses external images, matching README embedding. The width controls inspect
image columns, not physical phone viewports or native picture selection.

See `evidence/svg-layout-repair.json` for the precise checks performed. A geometry
pass is supplemented by visual inspection; the rectangle test conservatively
includes font ascent/descent space. These are local checks, not a publication or
live GitHub acceptance claim.

## Systems atlas redesign

The atlas now uses a 1200 × 864 desktop composition with three equal product
trails, instead of placing six names in two secondary boxes. A 360 × 1385 mobile
composition stacks the trails and retains a purpose for each product. Desktop
and mobile headings, labels and descriptions have their own spacing budgets.

The illustration consists of three etched planes, an open brushstroke circle,
and ten nodes in the portfolio's 4/3/3 grouping. Motion gently floats the planes, moves route signals, and draws an open
brushstroke circle; product text and app icons remain stationary. Dark,
light, animated and static siblings come from the same generator.

The ten existing static icon SVGs are embedded as data URLs. This preserves
identity and isolates their styles and IDs without external image requests.
Run `build_icons.py` before `build_assets.py` when changing icon sources; the
validator now follows that dependency order. Each atlas is approximately 260KB,
including all ten icons, and needs no remote fonts or scripts.

Open `check_layout.html?atlas=1` for the atlas gallery. The fixture now checks
48 variants across all six active families, including native,
Arial and Times fallback fonts. `evidence/atlas-redesign.json` records the current
verification and browser limitations; earlier Safari evidence applies only to
the preceding impact/delivery repair.

## Full README acceptance

The workbench replaces the plain stack inventory, retaining every listed tool.
`check_layout.html?bench=1` reviews the workbench in both themes and layouts.
Its original illustrations are category symbols, not third-party language logos.
The document writes, the systems symbol rotates, graph nodes light in sequence,
and a browser cursor blinks. These are illustrations, not live activity indicators.
The masthead monogram is likewise original vector work. Neither introduces a
new dependency. Atlas and workbench motion loops continuously at restrained speeds. Explicit
static siblings and reduced-motion CSS stop the loops.

Full-page review uses GitHub API-rendered Markdown. Local image URLs carry
content hashes so the browser cannot silently reuse an older SVG; media rules
and source order remain native. Collection entries use headings and paragraphs
so long names keep their width on mobile. See `evidence/atlas-redesign.json` for
the exact current verification scope and browser limitations.
