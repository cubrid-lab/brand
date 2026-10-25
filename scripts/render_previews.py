"""Render a before/after contact sheet of generated role icons (optional review aid).

Not part of the build or CI. Requires the ``rsvg-convert`` binary (librsvg) and
Pillow. Every icon is rasterized at each review size on a light and a dark
background, so seams and small-size legibility can be inspected by eye::

    python scripts/render_previews.py BEFORE_DIR AFTER_DIR OUT.png

``BEFORE_DIR`` and ``AFTER_DIR`` hold copies of ``dist/icons/*.svg`` and
``studies/icons/*.svg`` from the two revisions being compared.
"""
from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

SIZES = (16, 24, 32, 48, 64, 128)
BACKGROUNDS = (("light", (255, 255, 255)), ("dark", (13, 17, 23)))
GAP = 8
LABEL_WIDTH = 210
HEADER = 28


def rasterize(svg: Path, size: int) -> Image.Image:
    png = subprocess.run(
        ["rsvg-convert", "-w", str(size), "-h", str(size), str(svg)], check=True, capture_output=True
    ).stdout
    return Image.open(io.BytesIO(png)).convert("RGBA")


def main(before: Path, after: Path, out: Path) -> int:
    names = sorted(p.name for p in after.glob("*.svg"))
    strip = sum(SIZES) + GAP * (len(SIZES) + 1)
    groups = [(label, folder, bg_name, bg) for label, folder in (("before", before), ("after", after)) for bg_name, bg in BACKGROUNDS]
    width = LABEL_WIDTH + strip * len(groups)
    row = max(SIZES) + 2 * GAP
    sheet = Image.new("RGB", (width, HEADER + row * len(names)), (238, 240, 243))
    draw = ImageDraw.Draw(sheet)
    for index, (label, _, bg_name, _) in enumerate(groups):
        draw.text((LABEL_WIDTH + index * strip + GAP, 8), f"{label} / {bg_name}: " + " ".join(map(str, SIZES)) + " px", fill=(0, 0, 0))
    for r, name in enumerate(names):
        top = HEADER + r * row
        draw.text((GAP, top + row // 2 - 6), name.removesuffix(".svg"), fill=(0, 0, 0))
        for index, (_, folder, _, bg) in enumerate(groups):
            left = LABEL_WIDTH + index * strip
            draw.rectangle((left, top, left + strip - 1, top + row - 1), fill=bg)
            x = left + GAP
            for size in SIZES:
                svg = folder / name
                if svg.exists():
                    icon = rasterize(svg, size)
                    sheet.paste(icon, (x, top + row - GAP - size), icon)
                x += size + GAP
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, optimize=True)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])))
