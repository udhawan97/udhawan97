# Maintaining this profile

This repository publishes the GitHub profile README for `udhawan97`. Keep the
profile useful to someone choosing a project to explore: a short introduction,
three visible starting points, and links to the complete collection.

## Editing guide

- Edit profile copy and destinations in `README.md`. Verify new product claims
  against the project's current documentation; preserve maturity qualifiers.
- Edit illustrations in `design/readme-refresh/build_assets.py`, masthead and
  impact artwork in `build_legacy_assets.py`, and icon handling in `build_icons.py`.
  Regenerate the SVGs instead of hand-editing their outputs.
- Keep light, dark, mobile, and reduced-motion variants together. Retain useful
  image alt text and SVG titles and descriptions.
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
