"""Small-size legibility and contrast study for issue #21 (optional review aid).

Not part of the build or CI. Requires the ``rsvg-convert`` binary (librsvg) and
Pillow. It never writes to ``dist/``, ``src/`` or ``studies/``::

    python scripts/legibility_study.py OUT_DIR

writes to ``OUT_DIR``:

- ``contrast.md``: WCAG relative-luminance contrast of the white role mark on
  every face shade of every language token, and of each cube face on the light
  and dark review backgrounds.
- ``sizes.png``: every generated icon and the organization mark at 16, 24, 32,
  48 and 64 px on light and dark backgrounds.
- ``pixels.png``: the 16 and 24 px renderings enlarged 6x without smoothing,
  so each device pixel can be inspected.
- ``proposal-before-after.png``: the icons the study proposes to adjust, before
  and after the proposed treatment (see ``docs/studies/small-size-legibility.md``).
  The proposal is rendered from an in-memory copy of the generator; no
  generated asset changes.
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import build
from scripts.render_previews import BACKGROUNDS, main as before_after, rasterize

SIZES = (16, 24, 32, 48, 64)
ZOOM = 6
GAP = 8
LABEL_WIDTH = 210
HEADER = 28
# The face shading drawn by build.cube_faces(): (overlay color, opacity) per face.
SHADES = {"top": ((255, 255, 255), 0.08), "left": ((0, 0, 0), 0.10), "right": (None, 0.0)}
THRESHOLD = 3.0
# Proposed glyph enlargements about the mark's own bounding-box center. The
# enlargement of the Showcase (x1.3) and Docs (x1.25) marks was approved and
# applied to scripts/build.py on 2026-10-25, so it is no longer a proposal and
# the study renders the current icons (issue #21, study proposal P2).
SCALES: dict[str, float] = {}
KEYLINE_STEP = 0.05
NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")


def rgb(color: str) -> tuple[int, int, int]:
    return tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))


def hex_color(value: tuple[int, int, int]) -> str:
    return "#" + "".join(f"{channel:02X}" for channel in value)


def luminance(value: tuple[int, int, int]) -> float:
    def linear(channel: int) -> float:
        c = channel / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = map(linear, value)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def mix(base: tuple[int, int, int], over: tuple[int, int, int] | None, alpha: float) -> tuple[int, int, int]:
    if over is None:
        return base
    return tuple(round(b * (1 - alpha) + o * alpha) for b, o in zip(base, over))


def face_shades(color: str) -> dict[str, tuple[int, int, int]]:
    return {face: mix(rgb(color), over, alpha) for face, (over, alpha) in SHADES.items()}


def keyline_color(color: str) -> str | None:
    """The lightest darkening of ``color`` on which white reaches 3:1 on every face, if needed."""
    white = (255, 255, 255)
    if min(contrast(white, shade) for shade in face_shades(color).values()) >= THRESHOLD:
        return None
    darken = KEYLINE_STEP
    while True:
        candidate = hex_color(mix(rgb(color), (0, 0, 0), darken))
        if min(contrast(white, shade) for shade in face_shades(candidate).values()) >= THRESHOLD:
            return candidate
        darken = round(darken + KEYLINE_STEP, 2)


def contrast_table() -> str:
    white = (255, 255, 255)
    used: dict[str, list[str]] = {}
    for name, meta in sorted({**build.REGISTRY, **build.SURFACES}.items()):
        used.setdefault(meta["language"], []).append(f"`{name}`" + (" (no white mark)" if meta["role"] in {"driver", "orm"} else ""))
    lines = [
        "| Token | Color | White on top face | White on left face | White on right face | Keyline proposal | Used by |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for language, color in build.COLORS.items():
        shades = face_shades(color)
        cells = []
        for face in ("top", "left", "right"):
            ratio = contrast(white, shades[face])
            cells.append(f"{ratio:.2f} ({'pass' if ratio >= THRESHOLD else 'below 3:1'})")
        keyline = keyline_color(color)
        lines.append(
            f"| {language} | `{color}` | " + " | ".join(cells) + f" | {f'`{keyline}`' if keyline else '—'} | "
            + (", ".join(used.get(language, [])) or "unused") + " |"
        )
    lines += [
        "",
        "| Cube color | Face | On light `#FFFFFF` | On dark `#0D1117` |",
        "| --- | --- | --- | --- |",
    ]
    for language, color in build.COLORS.items():
        for face, shade in face_shades(color).items():
            lines.append(
                f"| {language} `{color}` | {face} `{hex_color(shade)}` | {contrast(shade, BACKGROUNDS[0][1]):.2f} | "
                f"{contrast(shade, BACKGROUNDS[1][1]):.2f} |"
            )
    for face, color in build.ORGANIZATION["face_colors"].items():
        lines.append(
            f"| organization | {face} `{color}` | {contrast(rgb(color), BACKGROUNDS[0][1]):.2f} | "
            f"{contrast(rgb(color), BACKGROUNDS[1][1]):.2f} |"
        )
    return "\n".join(lines) + "\n"


def sheet(svgs: list[Path], sizes: tuple[int, ...], zoom: int, out: Path) -> None:
    strip = sum(size * zoom for size in sizes) + GAP * (len(sizes) + 1)
    width = LABEL_WIDTH + strip * len(BACKGROUNDS)
    row = max(sizes) * zoom + 2 * GAP
    image = Image.new("RGB", (width, HEADER + row * len(svgs)), (238, 240, 243))
    draw = ImageDraw.Draw(image)
    suffix = f" px, shown {zoom}x" if zoom > 1 else " px"
    for index, (name, _) in enumerate(BACKGROUNDS):
        draw.text((LABEL_WIDTH + index * strip + GAP, 8), f"{name}: " + " ".join(map(str, sizes)) + suffix, fill=(0, 0, 0))
    for r, svg in enumerate(svgs):
        top = HEADER + r * row
        draw.text((GAP, top + row // 2 - 6), svg.stem, fill=(0, 0, 0))
        for index, (_, background) in enumerate(BACKGROUNDS):
            left = LABEL_WIDTH + index * strip
            draw.rectangle((left, top, left + strip - 1, top + row - 1), fill=background)
            x = left + GAP
            for size in sizes:
                tile = Image.new("RGBA", (size, size), background + (255,))
                tile.alpha_composite(rasterize(svg, size))
                tile = tile.resize((size * zoom, size * zoom), Image.NEAREST)
                image.paste(tile, (x, top + row - GAP - size * zoom))
                x += size * zoom + GAP
    image.save(out, optimize=True)


def scale_glyph(markup: str, factor: float) -> str:
    """Scale the first path (absolute x y pairs only) about its bounding-box center."""
    d = re.search(r'd="([^"]+)"', markup).group(1)
    values = [float(n) for n in NUMBER_RE.findall(d)]
    cx = (min(values[0::2]) + max(values[0::2])) / 2
    cy = (min(values[1::2]) + max(values[1::2])) / 2
    index = iter(range(len(values)))

    def scaled(match: re.Match[str]) -> str:
        centre = cx if next(index) % 2 == 0 else cy
        return build.number(centre + (float(match.group()) - centre) * factor)

    return markup.replace(d, NUMBER_RE.sub(scaled, d), 1)


def proposed_icon(name: str) -> str:
    meta = {**build.REGISTRY, **build.SURFACES}[name]
    color = build.COLORS[meta["language"]]
    glyphs = dict(build.GLYPHS)
    if meta["role"] in SCALES:
        glyphs[meta["role"]] = scale_glyph(glyphs[meta["role"]], SCALES[meta["role"]])
    original, build.GLYPHS = build.GLYPHS, glyphs
    try:
        svg = build.render_icon(meta["role"], color, name, meta["status"])
    finally:
        build.GLYPHS = original
    keyline = keyline_color(color)
    if keyline and meta["role"] not in {"driver", "orm"}:
        start = svg.index("<g clip-path")
        end = svg.index("</g>", start)
        svg = svg[:start] + svg[start:end].replace("currentColor", keyline) + svg[end:]
    return svg


def proposal_targets() -> list[str]:
    names = []
    for name, meta in sorted({**build.REGISTRY, **build.SURFACES}.items()):
        if meta["role"] in {"driver", "orm"}:
            continue
        if meta["role"] in SCALES or keyline_color(build.COLORS[meta["language"]]):
            names.append(name)
    return names


def main(out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    (out / "contrast.md").write_text(contrast_table(), encoding="utf-8")
    current = sorted((ROOT / "dist/icons").glob("*.svg")) + [ROOT / "dist/organization/mark.svg"]
    sheet(current, SIZES, 1, out / "sizes.png")
    sheet(current, (16, 24), ZOOM, out / "pixels.png")
    with tempfile.TemporaryDirectory() as temporary:
        before, after = Path(temporary, "before"), Path(temporary, "after")
        before.mkdir()
        after.mkdir()
        for name in proposal_targets():
            (before / f"{name}.svg").write_text((ROOT / "dist/icons" / f"{name}.svg").read_text(encoding="utf-8"), encoding="utf-8")
            (after / f"{name}.svg").write_text(proposed_icon(name), encoding="utf-8")
        before_after(before, after, out / "proposal-before-after.png")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(Path(sys.argv[1])))
