"""Render a light/dark contact sheet of the wordmark lockups (optional review aid).

Not part of the build or CI. Requires the ``rsvg-convert`` binary (librsvg) and
Pillow. Every generated lockup is rasterized at its review widths on the light
and the dark review background from ``tokens/organization.json``, including the
mismatched pairings, and the WCAG contrast of each text color is printed::

    python scripts/lockup_previews.py OUT.png

The text uses the system ``Arial, Helvetica, sans-serif`` fallback, so the
rendering depends on the fonts installed where it runs.
"""
from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import build
from scripts.legibility_study import contrast, rgb
from scripts.render_previews import GAP, HEADER, LABEL_WIDTH

# Actual display widths in CSS pixels; the view box width is 1x.
WIDTHS = {"horizontal": (150, 240, 300), "stacked": (100, 120, 200)}


def rasterize(svg: Path, width: int) -> Image.Image:
    png = subprocess.run(["rsvg-convert", "-w", str(width), str(svg)], check=True, capture_output=True).stdout
    return Image.open(io.BytesIO(png)).convert("RGBA")


def lockups() -> list[tuple[str, str, Path]]:
    files = [path for path in build.outputs() if path.name.startswith("lockup-")]
    rows = []
    for layout in build.LOCKUP_LAYOUTS:
        for variant in build.ORGANIZATION["wordmarks"]["variants"]:
            name = build.lockup_name(layout, variant)
            (path,) = [path for path in files if path.name == name]
            rows.append((layout, variant, path))
    return rows


def contrast_table() -> str:
    variants = build.ORGANIZATION["wordmarks"]["variants"]
    lines = ["| Variant | Text | Color | " + " | ".join(f"On {name} `{v['background']}`" for name, v in variants.items()) + " |"]
    lines.append("| --- | --- | --- | " + " | ".join("---" for _ in variants) + " |")
    for name, colors in variants.items():
        for part in ("title", "tagline"):
            ratios = " | ".join(f"{contrast(rgb(colors[part]), rgb(v['background'])):.2f}" for v in variants.values())
            lines.append(f"| {name} | {part} | `{colors[part]}` | {ratios} |")
    return "\n".join(lines)


def main(out: Path) -> int:
    variants = build.ORGANIZATION["wordmarks"]["variants"]
    backgrounds = [(name, rgb(v["background"])) for name, v in variants.items()]
    rows = lockups()
    strips = {layout: sum(widths) + GAP * (len(widths) + 1) for layout, widths in WIDTHS.items()}
    strip = max(strips.values())
    heights = {
        layout: max(rasterize(path, max(WIDTHS[layout])).height for lay, _, path in rows if lay == layout) + 2 * GAP
        for layout in WIDTHS
    }
    width = LABEL_WIDTH + strip * len(backgrounds)
    sheet = Image.new("RGB", (width, HEADER + sum(heights[layout] for layout, _, _ in rows)), (238, 240, 243))
    draw = ImageDraw.Draw(sheet)
    for index, (bg_name, _) in enumerate(backgrounds):
        draw.text((LABEL_WIDTH + index * strip + GAP, 8), f"on {bg_name} background", fill=(0, 0, 0))
    top = HEADER
    for layout, variant, path in rows:
        row = heights[layout]
        draw.text((GAP, top + row // 2 - 12), path.name.removesuffix(".svg"), fill=(0, 0, 0))
        widths = WIDTHS[layout]
        draw.text((GAP, top + row // 2 + 2), "widths " + "/".join(map(str, widths)) + " px", fill=(80, 80, 80))
        for index, (bg_name, bg) in enumerate(backgrounds):
            left = LABEL_WIDTH + index * strip
            draw.rectangle((left, top, left + strip - 1, top + row - 1), fill=bg)
            if bg_name != variant:
                draw.text((left + strip - 70, top + 4), "mismatch", fill=(230, 0, 57))
            x = left + GAP
            for size in widths:
                image = rasterize(path, size)
                sheet.paste(image, (x, top + row - GAP - image.height), image)
                x += size + GAP
        top += row
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, optimize=True)
    print(contrast_table())
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(Path(sys.argv[1])))
