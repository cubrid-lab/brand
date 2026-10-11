#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLORS = json.loads((ROOT / "tokens/colors.json").read_text())["languages"]
GEOMETRY = json.loads((ROOT / "tokens/geometry.json").read_text())
REGISTRY = json.loads((ROOT / "registry/repositories.json").read_text())["repositories"]
SRC = ROOT / "src/driver.svg"
OUT = ROOT / "dist/icons"


def number(value: int | float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


def path_data(points: list[list[int | float]]) -> str:
    commands = [f"M{number(points[0][0])} {number(points[0][1])}"]
    commands.extend(f"L{number(x)} {number(y)}" for x, y in points[1:])
    return " ".join(commands) + " Z"


def driver_paths() -> tuple[str, str]:
    driver = GEOMETRY["driver"]
    left = driver["left_points"]
    axis = driver["mirror_axis_x"]
    right = [[2 * axis - x, y] for x, y in left]
    return path_data(left), path_data(right)


def render(color: str, label: str) -> str:
    view_box = " ".join(number(v) for v in GEOMETRY["view_box"])
    left, right = driver_paths()
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" '
        f'role="img" aria-label="{label} Driver symbol">\n'
        "  <!-- Generated from tokens/geometry.json. Do not edit geometry here. -->\n"
        "  <!-- Design-approved direction; legal/trademark clearance pending. -->\n"
        f'  <path id="left" d="{left}" fill="{color}"/>\n'
        f'  <path id="right" d="{right}" fill="{color}"/>\n'
        "</svg>\n"
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # Neutral template is generated too, so geometry.json remains the single source of truth.
    SRC.write_text(render("currentColor", "CUBRID Lab"), encoding="utf-8")

    expected: set[str] = set()
    for repo, meta in sorted(REGISTRY.items()):
        if meta["role"] != "driver" or meta["status"] != "approved":
            continue
        color = COLORS[meta["language"]]
        target = OUT / f"{repo}.svg"
        expected.add(target.name)
        target.write_text(render(color, repo), encoding="utf-8")

    # Prevent stale approved assets when mappings are removed or renamed.
    for target in OUT.glob("*.svg"):
        if target.name not in expected:
            target.unlink()


if __name__ == "__main__":
    main()
