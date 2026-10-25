"""Contact sheets for the Driver, ORM and MCP role candidates (issue #30; optional review aid).

Not part of the build or CI. Requires the ``rsvg-convert`` binary (librsvg) and
Pillow. It never writes to ``dist/``, ``src/`` or ``studies/``::

    python scripts/role_candidates_study.py OUT_DIR

writes to ``OUT_DIR``:

- ``contact-sheet.png``: the current Driver, ORM and MCP icons next to every
  candidate in ``tokens/role-candidates.json``, plus the unchanged organization
  emblem and other roles, at 16, 24, 32, 48, 64 and 128 px on the light and
  dark review backgrounds, in the language color and in the Neutral token
  (monochrome).
- ``family.png``: the whole family at 24 and 48 px, as it is today and with
  each combination of candidates, so a departure from the system is obvious.
- ``pixels.png``: the Python candidates at 16 and 24 px enlarged 6x without
  smoothing.
- ``checks.md``: the seam, stroke-weight and contrast checks of
  ``tests/test_glyph_seams.py`` and ``tests/test_legibility.py`` applied to
  every candidate.
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
from scripts.legibility_study import contrast, face_shades, sheet
from scripts.render_previews import BACKGROUNDS, GAP, HEADER, SIZES, rasterize
from tests.test_glyph_seams import seam_contacts
from tests.test_legibility import thin_white_marks

LABEL_WIDTH = 330
COLOR_RE = re.compile(r'color="#[0-9A-Fa-f]{6}"')
WHITE = (255, 255, 255)
# Actual repository colors for the unchanged references.
REFERENCES = ("cubrid-cookbook-python", "cubrid-benchmark", "cubrid-kubernetes-operator", "showcase", "docs", "community")


def current(name: str) -> str:
    meta = {**build.REGISTRY, **build.SURFACES}[name]
    return build.render_icon(meta["role"], build.COLORS[meta["language"]], name, meta["status"])


def monochrome(svg: str) -> str:
    """The same icon in the Neutral token; the organization emblem has no color attribute and is unchanged.

    A light-token treatment (issue #38) belongs to its color, so it is removed too:
    the keyline is dropped and the dark mark goes back to white, as Neutral draws it.
    """
    match = COLOR_RE.search(svg)
    spec = build.TREATMENTS.get(match.group()[7:-1]) if match else None
    if spec:
        svg = re.sub(rf'  <clipPath id="[^"]+-outside">.*?</clipPath>\n|  <path [^>]*stroke="{spec["keyline"]}"[^>]*/>\n', "", svg)
        split = svg.rindex("<g clip-path") if "<g clip-path" in svg else len(svg)
        svg = svg[:split] + svg[split:].replace(f'"{spec["mark"]}"', '"#fff"')
    return COLOR_RE.sub(f'color="{build.COLORS["neutral"]}"', svg, count=1)


def rows() -> list[tuple[str, str | None]]:
    """(label, svg) pairs; ``None`` marks a section heading."""
    candidates = build.ROLE_CANDIDATES
    result: list[tuple[str, str | None]] = []
    for role, current_name in (("driver", "pycubrid"), ("orm", "sqlalchemy-cubrid"), ("mcp", "cubrid-mcp-server")):
        result.append((f"{role.upper()} role", None))
        result.append((f"current: {current_name}", current(current_name)))
        for candidate_id in sorted(candidates):
            if candidates[candidate_id]["role"] != role:
                continue
            for language in candidates[candidate_id]["languages"]:
                result.append((f"{candidate_id} ({language})", build.render_role_candidate(candidate_id, language)))
    result.append(("Unchanged references", None))
    result.append(("organization emblem", build.render_organization_mark()))
    result += [(f"current: {name}", current(name)) for name in REFERENCES]
    return result


def contact_sheet(out: Path) -> None:
    entries = rows()
    groups = [(f"{bg_name}", bg, False) for bg_name, bg in BACKGROUNDS] + [
        (f"monochrome {bg_name}", bg, True) for bg_name, bg in BACKGROUNDS
    ]
    strip = sum(SIZES) + GAP * (len(SIZES) + 1)
    row = max(SIZES) + 2 * GAP
    heading = 30
    height = HEADER + sum(heading if svg is None else row for _, svg in entries)
    image = Image.new("RGB", (LABEL_WIDTH + strip * len(groups), height), (238, 240, 243))
    draw = ImageDraw.Draw(image)
    for index, (name, _, _) in enumerate(groups):
        draw.text((LABEL_WIDTH + index * strip + GAP, 8), f"{name}: " + " ".join(map(str, SIZES)) + " px", fill=(0, 0, 0))
    top = HEADER
    with tempfile.TemporaryDirectory() as temporary:
        for number, (label, svg) in enumerate(entries):
            if svg is None:
                draw.rectangle((0, top, image.width, top + heading - 1), fill=(205, 210, 218))
                draw.text((GAP, top + 9), label, fill=(0, 0, 0))
                top += heading
                continue
            draw.text((GAP, top + row // 2 - 6), label, fill=(0, 0, 0))
            for index, (_, background, mono) in enumerate(groups):
                path = Path(temporary, f"{number}-{index}.svg")
                path.write_text(monochrome(svg) if mono else svg, encoding="utf-8")
                left = LABEL_WIDTH + index * strip
                draw.rectangle((left, top, left + strip - 1, top + row - 1), fill=background)
                x = left + GAP
                for size in SIZES:
                    icon = rasterize(path, size)
                    image.paste(icon, (x, top + row - GAP - size), icon)
                    x += size + GAP
            top += row
    image.save(out, optimize=True)


def families() -> list[tuple[str, list[str]]]:
    by_role: dict[str, list[str]] = {}
    for candidate_id, spec in sorted(build.ROLE_CANDIDATES.items()):
        by_role.setdefault(spec["role"], []).append(candidate_id)
    tail = [current(name) for name in REFERENCES]
    result = [("current family", [build.render_organization_mark(), current("pycubrid"), current("sqlalchemy-cubrid"), current("cubrid-mcp-server"), *tail])]
    for driver in by_role["driver"]:
        for orm in by_role["orm"]:
            for mcp in by_role["mcp"]:
                icons = [build.render_role_candidate(candidate, "python") for candidate in (driver, orm, mcp)]
                result.append((f"{orm} + {mcp}", [build.render_organization_mark(), *icons, *tail]))
    return result


def family_sheet(out: Path) -> None:
    sizes = (24, 48)
    entries = families()
    count = len(entries[0][1])
    strip = sum(size * count + GAP * count for size in sizes) + GAP
    row = max(sizes) + 2 * GAP
    image = Image.new("RGB", (LABEL_WIDTH + strip * len(BACKGROUNDS), HEADER + row * len(entries)), (238, 240, 243))
    draw = ImageDraw.Draw(image)
    for index, (name, _) in enumerate(BACKGROUNDS):
        draw.text((LABEL_WIDTH + index * strip + GAP, 8), f"{name}: 24 and 48 px", fill=(0, 0, 0))
    draw.text((GAP, 8), "emblem, driver, orm, mcp, references", fill=(0, 0, 0))
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


def checks() -> str:
    lines = [
        "| Candidate | Language | White samples within 0.3 of a seam | White marks under 1 unit | Lowest white-mark contrast |",
        "| --- | --- | --- | --- | --- |",
    ]
    for path, (candidate_id, language) in sorted(build.role_candidate_files().items()):
        svg = build.render_role_candidate(candidate_id, language)
        contacts = len(seam_contacts(svg))
        glyph = build.ROUTER_GLYPH if candidate_id == "mcp-router-hub" else ""
        thin = thin_white_marks(glyph) if glyph else []
        if glyph:
            low = min(contrast(WHITE, shade) for shade in face_shades(build.COLORS[language]).values())
            ratio = f"{low:.2f}"
        else:
            ratio = "no white mark"
        lines.append(f"| `{candidate_id}` | {language} | {contacts} | {len(thin)} | {ratio} |")
    return "\n".join(lines) + "\n"


def main(out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    contact_sheet(out / "contact-sheet.png")
    family_sheet(out / "family.png")
    with tempfile.TemporaryDirectory() as temporary:
        svgs = []
        for candidate_id in sorted(build.ROLE_CANDIDATES):
            path = Path(temporary, f"{candidate_id}.svg")
            path.write_text(build.render_role_candidate(candidate_id, "python"), encoding="utf-8")
            svgs.append(path)
        sheet(svgs, (16, 24), 6, out / "pixels.png")
    (out / "checks.md").write_text(checks(), encoding="utf-8")
    print((out / "checks.md").read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(Path(sys.argv[1])))
