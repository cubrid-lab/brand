#!/usr/bin/env python3
"""Generate exact CUBRID Lab Connector Study / 02 Driver contours.

All geometry is constructed analytically from the accepted study,
not copied from the replacement polygon used by the first bootstrap PR.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEOMETRY = json.loads((ROOT / "tokens/geometry.json").read_text(encoding="utf-8"))
COLORS = json.loads((ROOT / "tokens/colors.json").read_text(encoding="utf-8"))["languages"]
REGISTRY = json.loads((ROOT / "registry/repositories.json").read_text(encoding="utf-8"))["repositories"]
OUT = ROOT / "dist/icons"
COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


def driver_polygons() -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    """Two congruent modules separated by the study's mitered 1.5-unit seam."""
    s = math.sqrt(3)
    d = GEOMETRY["seam_width"] / s
    left = [
        (6, 12 - 4 * s),
        (2, 12),
        (6, 12 + 4 * s),
        (12 - d, 12 + 4 * s),
        (10 - d, 12 + 2 * s),
        (14 - d, 12 - 2 * s),
        (12 - d, 12 - 4 * s),
    ]
    cx, cy = GEOMETRY["center"]
    return left, [(2 * cx - x, 2 * cy - y) for x, y in left]


def path_data(points: list[tuple[float, float]]) -> str:
    precision = GEOMETRY["decimal_places"]
    return "M " + " L ".join(f"{x:.{precision}f} {y:.{precision}f}" for x, y in points) + " Z"


def render(color: str, key: str) -> str:
    if color != "currentColor" and not COLOR_RE.fullmatch(color):
        raise ValueError("invalid color")
    if not re.fullmatch(r"[a-z][a-z0-9-]*", key):
        raise ValueError("invalid identifier")
    coords = " ".join(str(n) for n in GEOMETRY["view_box"])
    paths = "\n".join(f'    <path d="{path_data(poly)}"/>' for poly in driver_polygons())
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{coords}" color="{color}"\n'
        f'     role="img" aria-labelledby="{key}-title {key}-desc">\n'
        f'  <title id="{key}-title">CUBRID Lab geometric Driver — {key}</title>\n'
        f'  <desc id="{key}-desc">Connector Study / 02: two matching polygons related by a 180-degree rotation, '
        'with a 1.5-unit mitered seam. Design accepted; legal clearance pending.</desc>\n'
        '  <g fill="currentColor">\n'
        f'{paths}\n'
        '  </g>\n'
        '</svg>\n'
    )


def outputs() -> dict[Path, str]:
    expected = {ROOT / "src/driver.svg": render("currentColor", "driver")}
    for repo, meta in sorted(REGISTRY.items()):
        if meta["role"] == "driver" and meta["status"] == "approved":
            expected[OUT / f"{repo}.svg"] = render(COLORS[meta["language"]], repo)
    return expected


def main() -> None:
    assert GEOMETRY["design_id"] == "connector-study-02"
    assert GEOMETRY["view_box"] == [0, 0, 24, 24]
    assert GEOMETRY["center"] == [12, 12]
    assert GEOMETRY["seam_width"] == 1.5
    expected = outputs()
    OUT.mkdir(parents=True, exist_ok=True)
    for target, content in expected.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    for stale in OUT.glob("*.svg"):
        if stale not in expected:
            stale.unlink()


if __name__ == "__main__":
    main()
