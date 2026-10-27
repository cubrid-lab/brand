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

    def test_all_language_variants_use_white_grooves(self):
        icons = outputs()
        for name, meta in REGISTRY.items():
            if meta["role"] not in {"driver", "orm"}:
                continue
            with self.subTest(icon=name):
                svg = ElementTree.fromstring(icons[ROOT / "dist/icons" / f"{name}.svg"])
                self.assertEqual(svg.get("color"), COLORS[meta["language"]])
                groove = next(g for g in svg.iter(SVG + "g") if g.get("data-layer-grooves") == meta["role"])
                # Python Yellow included (issue #54): one treatment for every language.
                self.assertEqual(groove.get("stroke"), "#fff")


class OperatorKnockoutTests(unittest.TestCase):
    def test_dial_is_a_mask_cutout_not_white_paint(self):
        svg_text = render_icon("operator", "currentColor", "operator")
        svg = ElementTree.fromstring(svg_text)
        mask = next(svg.iter(SVG + "mask"))
        self.assertEqual(mask.get("maskUnits"), "userSpaceOnUse")
        strokes = {e.get("stroke") for e in mask.iter() if e.get("stroke")}
        self.assertEqual(strokes, {"#000"}, "the dial is cut out of the mask in black")
        self.assertNotIn('stroke="#fff"', svg_text, "no white dial strokes remain")
        group = next(g for g in svg.iter(SVG + "g") if g.get("mask") == f"url(#{mask.get('id')})")
        painted = [p.get("d") for p in group.findall(SVG + "path") if p.get("fill") == "currentColor"]
        self.assertEqual(set(painted), {path_data(face) for face in cube_polygons().values()})


class McpJunctionHoleTests(unittest.TestCase):
    def test_hole_is_a_single_mask_circle_at_the_junction(self):
        svg_text = render_icon("mcp", "currentColor", "mcp")
        svg = ElementTree.fromstring(svg_text)
        mask = next(svg.iter(SVG + "mask"))
        circles = list(mask.iter(SVG + "circle"))
        self.assertEqual(len(circles), 1)
        self.assertEqual(circles[0].get("fill"), "#000")
        faces = cube_polygons()
        junction = (faces["top"][2][1] + faces["left"][1][1]) / 2
        self.assertAlmostEqual(float(circles[0].get("cy")), junction, places=3)
        self.assertEqual(float(circles[0].get("cx")), 12)
        self.assertNotIn("#fff\" stroke", svg_text, "no white router glyph remains")
        self.assertEqual(len(list(svg.iter(SVG + "circle"))), 1, "no hub or port circles")
        self.assertEqual(len(list(svg.iter(SVG + "path"))) - 1 - 2, 3, "three faces plus two shades only")


if __name__ == "__main__":
    unittest.main()
