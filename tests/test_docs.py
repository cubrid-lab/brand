from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build import REGISTRY, SURFACES

FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
LINK = re.compile(r"\]\(([^)\s]+)\)|\bsrc=\"([^\"]+)\"")
ICON_PATH = re.compile(r"\b(dist|studies)/icons/([a-z0-9-]+)\.svg")


def markdown_files() -> list[Path]:
    return sorted(
        p
        for p in ROOT.rglob("*.md")
        if not any(part.startswith(".") for part in p.relative_to(ROOT).parts)
    )


def prose(path: Path) -> str:
    return FENCE.sub("", path.read_text(encoding="utf-8"))


class DocumentationConsistencyTests(unittest.TestCase):
    def test_relative_links_resolve(self):
        for path in markdown_files():
            for match in LINK.finditer(prose(path)):
                target = (match.group(1) or match.group(2)).split("#", 1)[0]
                if not target or re.match(r"[a-z][a-z0-9+.-]*:", target):
                    continue
                with self.subTest(file=str(path.relative_to(ROOT)), link=target):
                    self.assertTrue((path.parent / target).exists())

    def test_icon_paths_in_docs_match_registry_status(self):
        # Guides link to the registry for status; any icon path they do name
        # must agree with it (dist/ for approved, studies/ for pending).
        statuses = {name: meta["status"] for name, meta in {**REGISTRY, **SURFACES}.items()}
        for path in markdown_files():
            for directory, name in ICON_PATH.findall(prose(path)):
                with self.subTest(file=str(path.relative_to(ROOT)), icon=f"{directory}/{name}"):
                    self.assertIn(name, statuses)
                    expected = "dist" if statuses[name] == "approved" else "studies"
                    self.assertEqual(directory, expected)

    def test_gallery_shows_every_approved_icon(self):
        gallery = (ROOT / "docs" / "ICON_GALLERY.md").read_text(encoding="utf-8")
        for name, meta in {**REGISTRY, **SURFACES}.items():
            if meta["status"] == "approved":
                with self.subTest(icon=name):
                    self.assertIn(f"../dist/icons/{name}.svg", gallery)


if __name__ == "__main__":
    unittest.main()
