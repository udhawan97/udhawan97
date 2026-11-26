"""Optional authoring step; normal SVG generation needs no font dependency."""

import hashlib
import json
from pathlib import Path
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

HERE = Path(__file__).resolve().parent
metadata = json.loads((HERE / "provenance.json").read_text())
source = Path(sys.argv[1])
if hashlib.sha256(source.read_bytes()).hexdigest() != metadata["source_sha256"]:
    raise SystemExit("Font digest differs from the reviewed source; review provenance before updating.")
font = instantiateVariableFont(TTFont(source), metadata["axes"], inplace=False)
glyph_set, cmap = font.getGlyphSet(), font.getBestCmap()
glyphs = {}
for char in (chr(n) for n in range(32, 127)):
    glyph = glyph_set[cmap[ord(char)]]
    pen = SVGPathPen(glyph_set, ntos=lambda n: format(n, ".2f").rstrip("0").rstrip(".") if n else "0")
    glyph.draw(pen)
    glyphs[char] = {"advance": round(glyph.width, 3), "path": pen.getCommands()}
(HERE / "glyphs.json").write_text(json.dumps({
    "unitsPerEm": font["head"].unitsPerEm, "axes": metadata["axes"], "glyphs": glyphs,
}, separators=(",", ":")) + "\n")
