# Profile field guide

Implemented September 11, 2026. The audience is a recruiter making a quick
assessment and a developer deciding which repository to explore.

## Reading order

1. Preserve the existing name masthead and AI/wizard animation at the top.
2. Put portfolio, LinkedIn, and email links immediately beneath them.
3. State the current role and engineering focus concisely.
4. Introduce the ten-product systems atlas, then feature Orifold, Voyalier,
   and Golavo for native, cross-platform, and evidence-oriented engineering.
5. Show every project with its animated app identity and a concise outcome.
   Keep deeper stories and workflow illustrations in native disclosure blocks.
6. Explain the engineering practice and Agent Toolkit; put career history and
   the preserved impact seals together. Keep commit activity in an optional
   disclosure at the end. Project order no longer implies a commit-count ranking.

The four top-level section numbers match the contents line already in the
preserved masthead. Existing header, wizard, impact, and original project-icon
files are byte-for-byte unchanged.

## Artwork

Five new illustration families produce 28 self-contained SVG files:

- **Systems atlas:** a conceptual portfolio map with an exploded stack of sheets.
  It describes shared engineering practice, not shared code or infrastructure.
- **Orifold:** mixed files, local document workflow, finished artifact.
- **Voyalier:** travel details, review and assembly, departure brief.
- **Golavo:** a sealed forecast, observed result, forward scoring.
- **Delivery loop:** define, build, verify, ship, and return lessons to the next version.

Each has dark/light desktop and independently composed mobile artwork. The atlas
and delivery loop also have explicit static files. Their introductory motion ends
within 3.5 seconds. The illustrations contain no screenshots, invented metrics,
scripts, external stylesheets, remote fonts, or foreignObject content.

The palette continues the existing ink, ivory, and gold identity, adding slate
blue and muted teal for semantic groupings. Georgia carries restrained display
headlines; system sans-serif carries descriptions; monospace carries small labels.
The palette is defined in `build_assets.py`.

The ten project icons use the user's actual artwork, pinned from the sources in
`icon-sources.json`. Seven retain their native animation. FolioOrb, Nindova, and
Vidha receive orbit, diamond, and courier movement respectively. Every icon has a
static counterpart selected by a reduced-motion picture source. The Orifold
static counterpart captures its finished-icon phase at 80% of its existing
animation; the Nimanto static counterpart keeps its original finished base pose. Vidha uses the newly merged
`apps/web/public/vidha-icon.svg` courier-and-envelope artwork (source SHA-256 recorded
in `icon-manifest.json`), not the older icon retained in the legacy assets directory.

The two original opening graphics retain their original 600px responsive switch.
New illustrations switch to their dedicated mobile compositions at 700px.
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
python3 design/readme-refresh/build_assets.py
python3 design/readme-refresh/build_icons.py
python3 design/readme-refresh/build_preview.py
python3 -m http.server 8767 --bind 127.0.0.1
```

Open `http://127.0.0.1:8767/design/readme-refresh/preview.html` in Safari. The preview
uses GitHub's Markdown API when available (with a markdown-it fallback), and a local approximation of the
README column. Theme, 390px/320px column, motion, and gallery controls are review
tools; they are not part of the published README. GitHub's actual profile remains
the final rendering check. The preview builder prefers an authenticated `gh` CLI; its offline fallback needs `markdown-it-py`.

The asset generators use Python's standard library and pinned local source SVGs;
they require no network access. Generated previews and screenshots stay ignored.
The manifests record the intended asset variants and the provenance of app marks.

GitHub picture support: [GitHub documentation](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#the-picture-element).
SVG image restrictions: [MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image).
