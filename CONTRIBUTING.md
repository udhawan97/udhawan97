# Maintaining this profile

This repository publishes the GitHub profile README for `udhawan97`. Keep the
profile useful to someone choosing a project to explore: a short introduction,
three visible starting points, concrete evidence of maintenance, visual learning,
and links to the complete collection. This repo publishes the profile README;
`udhawan97.github.io` is a separate website and must not be changed implicitly.

## Editing guide

- Edit profile copy and destinations in `README.md`. Verify new product claims
  against the project's current documentation; preserve maturity qualifiers.
- Edit active illustrations and palette tokens in
  `design/readme-refresh/build_profile_assets.py`; regenerate their SVGs and
  `tokens.css`. Existing generators maintain archived artwork and pinned icons.
  Do not hand-edit generated SVGs or the glyph table.
- Keep light/dark and mobile/desktop variants together. All active artwork is
  static, so reduced motion needs no animation fallback. Retain useful image alt
  text, SVG titles/descriptions and selectable explanations next to diagrams.
- Describe automation responsibilities as responsibilities. Verify any new
  completion claim against a concrete PR, release or run; do not imply that CI
  proves native acceptance or that agent review is independent human approval.
- Keep Learnings via Graphics links source-only and beginner-friendly. Never
  infer permission to enable its Actions, Pages or releases from a profile edit.
- Keep employment, education, and impact figures owner-supplied. Repository
  activity is not evidence of adoption or product quality.

See [the design guide](design/readme-refresh/DESIGN.md) for the visual system and
asset provenance.

## Validate a change

Run from the repository root with Python 3.11 or later:

```sh
python3 design/readme-refresh/validate_assets.py
git diff --check
```

The validator uses the Python standard library. It checks SVG structure,
references, accessibility metadata, contrast, mobile text size, static variants,
and generator consistency. It also **regenerates assets**: stale output causes
the first run to fail, so inspect the resulting diff and rerun after accepting
the generated changes. It writes `design/readme-refresh/evidence/asset-validation.json`.

Install `librsvg` for raster checks (`brew install librsvg` on macOS or
`sudo apt-get install librsvg2-bin` on Ubuntu). Without `rsvg-convert`, local
validation reports a warning and skips rasterization. CI installs the renderer.

The **Profile validation** workflow runs these checks on pushes and pull
requests. It also rejects uncommitted changes to generated assets and manifests.
Passing automation does not establish that GitHub's layout looks correct.

## Review the rendered README

With the GitHub CLI installed and authenticated:

```sh
python3 design/readme-refresh/build_preview.py
python3 -m http.server 8767 --bind 127.0.0.1
```

Open <http://127.0.0.1:8767/design/readme-refresh/preview.html> in Safari.
The builder uses GitHub's Markdown API; its optional offline fallback requires
`markdown-it-py`. Previews are ignored by Git.

Check section navigation, collection expansion, project links, and image loading.
Review narrow and wide layouts, light and dark themes, and reduced motion.
The gallery controls select artwork variants; they do not emulate Safari's
native media preferences. Finish by checking the published GitHub profile.
