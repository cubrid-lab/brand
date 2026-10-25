"""Review sheets for the Python Yellow contrast treatments (issue #38; optional review aid).

Not part of the build or CI. Requires the ``rsvg-convert`` binary (librsvg) and
Pillow. It never writes to ``dist/``, ``src/`` or ``studies/``::

    python scripts/python_yellow_study.py OUT_DIR

writes to ``OUT_DIR``:

- ``family.png``: the organization emblem and the four Python icons, today in
  their current token and in each treatment of ``tokens/python-yellow-candidates.json``,
  next to the unchanged TypeScript, Go and Rust icons, at 24 and 48 px on the
  light and dark review backgrounds.
- ``sizes-<treatment>.png``: the four Python icons in one treatment at 16, 24,
  32, 48, 64 and 128 px, light and dark.
- ``pixels.png``: every treatment at 16 and 24 px, enlarged 6x without smoothing.
- ``checks.md``: mark, edge and face contrast, and the seam and stroke-weight
  checks of ``tests/test_glyph_seams.py`` and ``tests/test_legibility.py``.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import build
from scripts.legibility_study import contrast, rgb, sheet
from scripts.render_previews import BACKGROUNDS, GAP, HEADER, SIZES, rasterize
from tests.test_glyph_seams import seam_contacts
from tests.test_legibility import face_shades, thin_white_marks

LABEL_WIDTH = 230
PYTHON = build.YELLOW_CANDIDATES["repositories"]
# Unchanged language variants of the same roles, and the Go operator.
OTHERS = ("cubrid-client", "drizzle-cubrid", "cubrid-go", "gorm-cubrid", "cubrid-kubernetes-operator", "cubrid-rs", "sea-orm-cubrid")
LIGHT, DARK = BACKGROUNDS[0][1], BACKGROUNDS[1][1]


def current(name: str) -> str:
    meta = build.REGISTRY[name]
    return build.render_icon(meta["role"], build.COLORS[meta["language"]], name, meta["status"])


def treatments() -> list[str]:
    return sorted(build.YELLOW_CANDIDATES["treatments"])


def family_rows() -> list[tuple[str, list[str]]]:
    tail = [current(name) for name in OTHERS]
    emblem = build.render_organization_mark()
    rows = [(f"current: {build.COLORS['python']}", [emblem, *map(current, PYTHON), *tail])]
    for treatment in treatments():
        rows.append((treatment, [emblem, *(build.render_yellow_candidate(treatment, name) for name in PYTHON), *tail]))
    return rows


def family_sheet(out: Path) -> None:
    sizes = (24, 48)
    entries = family_rows()
    count = len(entries[0][1])
    strip = sum(size * count + GAP * count for size in sizes) + GAP
    row = max(sizes) + 2 * GAP
    image = Image.new("RGB", (LABEL_WIDTH + strip * len(BACKGROUNDS), HEADER + row * len(entries)), (238, 240, 243))
    draw = ImageDraw.Draw(image)
    for index, (name, _) in enumerate(BACKGROUNDS):
        draw.text((LABEL_WIDTH + index * strip + GAP, 8), f"{name}: 24 and 48 px", fill=(0, 0, 0))
    draw.text((GAP, 8), "emblem, 4 Python, TS/Go/Rust", fill=(0, 0, 0))
    with tempfile.TemporaryDirectory() as temporary:
        for r, (label, svgs) in enumerate(entries):
            top = HEADER + r * row
            draw.text((GAP, top + row // 2 - 6), label, fill=(0, 0, 0))
            for index, (_, background) in enumerate(BACKGROUNDS):
                left = LABEL_WIDTH + index * strip
                draw.rectangle((left, top, left + strip - 1, top + row - 1), fill=background)
                x = left + GAP
                for size in sizes:
                    for number, svg in enumerate(svgs):
                        path = Path(temporary, f"{r}-{number}.svg")
                        path.write_text(svg, encoding="utf-8")
                        icon = rasterize(path, size)
                        image.paste(icon, (x, top + row - GAP - size), icon)
                        x += size + GAP
    image.save(out, optimize=True)


def files(directory: Path, svgs: dict[str, str]) -> list[Path]:
    paths = []
    for name, svg in svgs.items():
        path = directory / f"{name}.svg"
        path.write_text(svg, encoding="utf-8")
        paths.append(path)
    return paths


def measures(treatment: str) -> dict[str, float | int | str]:
    """Lowest mark-on-face contrast, edge contrast per role group, seam and stroke checks."""
    spec = build.YELLOW_CANDIDATES["treatments"][treatment]
    inks = {key: ink["value"] for key, ink in build.YELLOW_CANDIDATES["inks"].items()}
    mark = (255, 255, 255) if spec["mark"] == "white" else rgb(inks[spec["mark"]])
    result: dict[str, float | int | str] = {}
    marks, contacts, thin = [], 0, 0
    for name in PYTHON:
        role = build.REGISTRY[name]["role"]
        svg = build.render_yellow_candidate(treatment, name)
        shades = face_shades(svg)
        if role in {"driver", "orm"}:
            faces = [rgb(build.YELLOW_CANDIDATES["color"])]  # The layers carry no face shading.
        else:
            faces = list(shades.values())
            marks.append(min(contrast(mark, shade) for shade in faces))
            # The seam check looks for white: recolor only the visible mark group back to white.
            split = svg.rindex("<g clip-path")
            white = svg[:split] + svg[split:].replace(f'"{inks.get(spec["mark"], "#fff")}"', '"#fff"')
            contacts += len(seam_contacts(white))
            thin += len(thin_white_marks(build.GLYPHS[role]))
        group = "layers" if role in {"driver", "orm"} else "cube"
        if spec["keyline"] and role in spec["keyline_roles"]:
            edge = rgb(inks[spec["keyline"]])
            result[f"{group}_edge_light"] = contrast(edge, LIGHT)
            result[f"{group}_edge_dark"] = contrast(edge, DARK)
        else:
            result[f"{group}_edge_light"] = min(contrast(face, LIGHT) for face in faces)
            result[f"{group}_edge_dark"] = min(contrast(face, DARK) for face in faces)
        result[f"{group}_faces_light"] = min(contrast(face, LIGHT) for face in faces)
        result[f"{group}_faces_dark"] = min(contrast(face, DARK) for face in faces)
    result["mark"] = min(marks)
    result["contacts"] = contacts
    result["thin"] = thin
    return result


def checks() -> str:
    lines = [
        "| Treatment | Lowest mark-on-face contrast (MCP, Cookbook) | Driver/ORM outer edge on light / dark | MCP/Cookbook outer edge on light / dark | Yellow faces on light / dark | Mark samples within 0.3 of a seam | Marks under 1 unit |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for treatment in treatments():
        m = measures(treatment)
        lines.append(
            f"| `{treatment}` | {m['mark']:.2f} | {m['layers_edge_light']:.2f} / {m['layers_edge_dark']:.2f} | "
            f"{m['cube_edge_light']:.2f} / {m['cube_edge_dark']:.2f} | {m['cube_faces_light']:.2f} / {m['cube_faces_dark']:.2f} | "
            f"{m['contacts']} | {m['thin']} |"
        )
    return "\n".join(lines) + "\n"


def main(out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    family_sheet(out / "family.png")
    with tempfile.TemporaryDirectory() as temporary:
        everything = []
        for treatment in treatments():
            directory = Path(temporary, treatment)
            directory.mkdir()
            svgs = files(directory, {f"{treatment}-{name}": build.render_yellow_candidate(treatment, name) for name in PYTHON})
            sheet(svgs, SIZES, 1, out / f"sizes-{treatment}.png")
            everything += svgs
        sheet(everything, (16, 24), 6, out / "pixels.png")
    (out / "checks.md").write_text(checks(), encoding="utf-8")
    print((out / "checks.md").read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(Path(sys.argv[1])))
