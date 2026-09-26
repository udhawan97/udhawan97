# Original-design polish — 2026-09-26

The original README composition, copy, palette, project identities, systems atlas,
workbench, delivery loop, impact panel, and wizard are preserved.

- Masthead: lighter display type, balanced focus columns, larger supporting text,
  and more breathing room in desktop and mobile versions.
- Shared artwork: finer borders and quieter drafting grids.
- Atlas: clearer category captions and a deliberate wrap for PalDawn's description.
- Workbench: small tool-category labels and slower ambient animation.
- Preview: collapsed diagnostics and unmodified SVG URLs. Safari rendered the
  query-versioned embedded masthead black; native asset URLs restored its wash.

## Validation

`python3 design/readme-refresh/validate_assets.py` passes for all 80 generated
assets: deterministic regeneration, valid XML, references, self-contained SVGs,
static motion variants, mobile text floor, contrast, and raster rendering.
Minimum checked text contrast remains 4.82:1. `git diff --check` passes.

Light desktop masthead, atlas and workbench were visually inspected at 850 px;
mobile masthead was inspected at 360 px. Safari inspection confirmed the original
composition and the preview rendering fix. A complete Safari viewport/theme/motion
matrix and post-publication GitHub acceptance were not performed.
