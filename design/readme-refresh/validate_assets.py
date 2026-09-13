"""Validate README SVG structure, variants, determinism, and raster rendering."""

from __future__ import annotations

import hashlib
import ast
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
README = ROOT / "README.md"
EVIDENCE = HERE / "evidence" / "asset-validation.json"
SVG_NS = "{http://www.w3.org/2000/svg}"


def node_value(node: ast.AST):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Dict):
        return {node_value(key): node_value(value) for key, value in zip(node.keys, node.values)}
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict":
        return {item.arg: node_value(item.value) for item in node.keywords}
    raise ValueError(f"unsupported palette expression: {ast.dump(node)}")


def palettes(script: str) -> dict:
    tree = ast.parse((HERE / script).read_text())
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "PALETTES" for target in statement.targets):
            return node_value(statement.value)
    raise ValueError(f"PALETTES not found in {script}")


def luminance(color: str) -> float:
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first: str, second: str) -> float:
    darker, lighter = sorted((luminance(first), luminance(second)))
    return (lighter + 0.05) / (darker + 0.05)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def referenced_svgs() -> list[Path]:
    paths = re.findall(r'(?:src|srcset)="\./([^\"]+\.svg)"', README.read_text())
    return sorted({ROOT / path for path in paths})


def generated_svgs() -> list[Path]:
    paths = list((ROOT / "assets" / "profile-refresh").glob("*.svg"))
    paths.extend((ROOT / "assets" / "profile-refresh" / "icons").glob("*.svg"))
    for family in ("profile-header", "ai-spell", "impact-seals"):
        paths.extend((ROOT / "assets").glob(f"{family}*.svg"))
    return sorted(set(paths))


def run_generators() -> None:
    for script in ("build_legacy_assets.py", "build_icons.py", "build_assets.py"):
        subprocess.run(["python3", str(HERE / script)], cwd=ROOT, check=True, capture_output=True, text=True)


def main() -> None:
    failures: list[str] = []
    warnings: list[str] = []
    referenced = referenced_svgs()
    missing = [str(path.relative_to(ROOT)) for path in referenced if not path.exists()]
    if missing:
        failures.extend(f"missing README asset: {path}" for path in missing)

    active = [path for path in referenced if path.exists()]
    generated = generated_svgs()
    inspected = sorted(set(active) | set(generated))
    for path in inspected:
        rel = str(path.relative_to(ROOT))
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as error:
            failures.append(f"invalid XML: {rel}: {error}")
            continue

        ids = [node.get("id") for node in root.iter() if node.get("id")]
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        if duplicates:
            failures.append(f"duplicate IDs: {rel}: {', '.join(duplicates)}")

        source = path.read_text()
        references = set(re.findall(r"url\(#([^)]+)\)", source))
        references.update(re.findall(r'(?:href|xlink:href)="#([^\"]+)"', source))
        unresolved = sorted(references - set(ids))
        if unresolved:
            failures.append(f"unresolved fragments: {rel}: {', '.join(unresolved)}")

        if root.find(f"{SVG_NS}title") is None or root.find(f"{SVG_NS}desc") is None:
            failures.append(f"missing title/desc: {rel}")
        if any(node.tag in (f"{SVG_NS}script", f"{SVG_NS}foreignObject") for node in root.iter()):
            failures.append(f"disallowed active content: {rel}")
        if re.search(r'(?:href|xlink:href)="https?://', source):
            failures.append(f"remote dependency: {rel}")
        if re.search(r'(?:fill|stroke|stop-color|font-family)\s*[:=]\s*["\']?var\(--', source):
            failures.append(f"unresolved paint/font CSS variable: {rel}")

        if "-static.svg" in path.name:
            active_css = re.findall(r"animation\s*:\s*([^;}]+)", source)
            has_global_stop = re.search(r"animation\s*:\s*none\s*!important", source) is not None
            if any(value.strip().split()[0] != "none" for value in active_css) and not has_global_stop:
                failures.append(f"static asset has active CSS animation: {rel}")
            if any(node.tag.rsplit("}", 1)[-1] in {"animate", "animateMotion", "animateTransform", "set"} for node in root.iter()):
                failures.append(f"static asset has SMIL animation: {rel}")

        if "-mobile-" in path.name and path.parent.name != "icons":
            view_box = root.get("viewBox", "").split()
            text_sizes = [float(node.get("font-size")) for node in root.iter() if node.tag == f"{SVG_NS}text" and node.get("font-size")]
            if len(view_box) == 4 and text_sizes:
                canvas_width = float(view_box[2])
                rendered_min = min(text_sizes) * 288 / canvas_width
                if rendered_min < 10:
                    failures.append(f"mobile text below 10px at a 288px image width: {rel}: {rendered_min:.1f}px")

    expected_legacy = {
        ROOT / "assets" / f'{family}{mobile}-{theme}{static}.svg'
        for family in ("profile-header", "ai-spell", "impact-seals")
        for mobile in ("", "-mobile")
        for theme in ("dark", "light")
        for static in ("", "-static")
    }
    for path in sorted(expected_legacy):
        if not path.exists():
            failures.append(f"missing legacy variant: {path.relative_to(ROOT)}")

    contrast_results: dict[str, float] = {}
    palette_specs = (
        ("legacy", palettes("build_legacy_assets.py"), ("paper", "paper_2"), ("ink", "muted", "faint", "accent", "accent_2", "blue", "teal")),
        ("profile-refresh", palettes("build_assets.py"), ("bg", "panel"), ("text", "muted", "gold", "blue", "teal")),
    )
    for family, themes, background_names, foreground_names in palette_specs:
        for theme, colors in themes.items():
            for background_name in background_names:
                for foreground_name in foreground_names:
                    name = f"{family}/{theme}/{foreground_name}-on-{background_name}"
                    ratio = contrast(colors[foreground_name], colors[background_name])
                    contrast_results[name] = round(ratio, 2)
                    if ratio < 4.5:
                        failures.append(f"text contrast below 4.5:1: {name}: {ratio:.2f}:1")

    before = {str(path.relative_to(ROOT)): digest(path) for path in generated}
    run_generators()
    after = {str(path.relative_to(ROOT)): digest(path) for path in generated_svgs()}
    if before != after:
        failures.append("asset generators are not deterministic or outputs were stale")

    renderer = shutil.which("rsvg-convert")
    render_failures: list[str] = []
    if renderer:
        with tempfile.TemporaryDirectory(prefix="profile-svg-validation-") as temp:
            for index, path in enumerate(inspected):
                result = subprocess.run(
                    [renderer, "-w", "320", str(path), "-o", str(Path(temp) / f"{index}.png")],
                    capture_output=True,
                    text=True,
                )
                if result.returncode:
                    render_failures.append(str(path.relative_to(ROOT)))
        failures.extend(f"raster render failed: {path}" for path in render_failures)
    else:
        warnings.append("rsvg-convert unavailable; raster validation skipped")

    readme = README.read_text()
    for family in ("profile-header", "ai-spell", "impact-seals", "systems-atlas", "delivery-loop", "engineering-workbench"):
        if f"{family}-mobile-dark-static.svg" not in readme:
            failures.append(f"README missing reduced-motion mobile source: {family}")

    preview = HERE / "preview.html"
    node = shutil.which("node")
    if preview.exists() and node:
        match = re.search(r"<script>(.*?)</script>", preview.read_text(), re.S)
        if match:
            with tempfile.NamedTemporaryFile("w", suffix=".js") as script:
                script.write(match.group(1))
                script.flush()
                result = subprocess.run([node, "--check", script.name], capture_output=True, text=True)
                if result.returncode:
                    failures.append("generated preview JavaScript does not parse")
        else:
            failures.append("generated preview has no script")
    elif not node:
        warnings.append("node unavailable; preview JavaScript syntax check skipped")

    evidence = {
        "status": "pass" if not failures else "fail",
        "svg_count": len(list((ROOT / "assets").rglob("*.svg"))),
        "readme_svg_count": len(active),
        "generated_svg_count": len(generated),
        "missing_references": missing,
        "render_failures": render_failures,
        "deterministic_generators": before == after,
        "minimum_palette_contrast": min(contrast_results.values()),
        "palette_contrast_ratios": contrast_results,
        "checks": [
            "XML, unique IDs, and fragment references",
            "README asset existence and reduced-motion variants",
            "accessible SVG title and description",
            "no scripts, foreignObject, remote dependencies, or unresolved paint/font CSS variables",
            "no active animation in static siblings",
            "mobile text floor at a 288px rendered image width",
            "WCAG text contrast across both generated palettes",
            "repeatable generator output",
            "rsvg rasterization at 320px when available",
            "generated review-page JavaScript syntax",
        ],
        "intended_review_matrix": {
            "themes": ["light", "dark"],
            "motion": ["regular", "reduced"],
            "review_widths_px": [320, 375, 390, 414, 768, 914],
            "browser": "Safari",
        },
        "warnings": warnings,
        "failures": failures,
    }
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps(evidence, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
