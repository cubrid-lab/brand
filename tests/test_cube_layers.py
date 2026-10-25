"""The common cube grammar for the Driver and ORM (#41, #43)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build import COLORS, LAYER_DIVISIONS, REGISTRY, cube_polygons, outputs, path_data, render_icon

SVG = "{http://www.w3.org/2000/svg}"


class CubeLayerTests(unittest.TestCase):
    def test_equal_thickness_divisions_and_common_faces(self):
        self.assertEqual(LAYER_DIVISIONS, (1 / 3, 2 / 3))
        faces = {path_data(face) for face in cube_polygons().values()}
        grooves = {}
        for role in ("driver", "orm"):
            svg = ElementTree.fromstring(render_icon(role, "currentColor", role))
            painted = [p.get("d") for p in svg.findall(SVG + "path") if p.get("fill") == "currentColor"]
            self.assertEqual(set(painted), faces, "each role must preserve the three complete cube faces")
            mark = next(g for g in svg.iter(SVG + "g") if g.get("data-layer-grooves") == role)
            self.assertEqual(mark.get("stroke-width"), "1.05")
            grooves[role] = [p.get("d") for p in mark.findall(SVG + "path")]
            self.assertEqual(len(grooves[role]), 4, "two grooves over two cube faces")
        self.assertNotEqual(grooves["driver"], grooves["orm"])

    def test_all_language_variants_and_python_treatment(self):
        icons = outputs()
        for name, meta in REGISTRY.items():
            if meta["role"] not in {"driver", "orm"}:
                continue
            with self.subTest(icon=name):
                svg = ElementTree.fromstring(icons[ROOT / "dist/icons" / f"{name}.svg"])
                self.assertEqual(svg.get("color"), COLORS[meta["language"]])
                groove = next(g for g in svg.iter(SVG + "g") if g.get("data-layer-grooves") == meta["role"])
                expected = "#40350F" if meta["language"] == "python" else "#fff"
                self.assertEqual(groove.get("stroke"), expected)


if __name__ == "__main__":
    unittest.main()
