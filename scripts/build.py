#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLORS = json.loads((ROOT / "tokens/colors.json").read_text())["languages"]
REGISTRY = json.loads((ROOT / "registry/repositories.json").read_text())["repositories"]
TEMPLATE = (ROOT / "src/driver.svg").read_text()
OUT = ROOT / "dist/icons"


def render(color: str, label: str) -> str:
    svg = TEMPLATE.replace("currentColor", color)
    return svg.replace(
        'aria-label="CUBRID Lab Driver symbol"',
        f'aria-label="{label} Driver symbol"',
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for repo, meta in sorted(REGISTRY.items()):
        if meta["role"] != "driver" or meta["status"] != "approved":
            continue
        color = COLORS[meta["language"]]
        (OUT / f"{repo}.svg").write_text(render(color, repo), encoding="utf-8")


if __name__ == "__main__":
    main()
