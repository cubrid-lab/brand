"""The common cube grammar for the Driver and ORM (#41, #43) with transparent gaps (#57)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build import GEOMETRY, REGISTRY, cube_polygons, outputs, path_data, render_icon

SVG = "{http://www.w3.org/2000/svg}"


def masked_group(svg: ElementTree.Element) -> tuple[ElementTree.Element, ElementTree.Element]:
    mask = next(svg.iter(SVG + "mask"))
    group = next(g for g in svg.iter(SVG + "g") if g.get("mask") == f"url(#{mask.get('id')})")
    return mask, group


class CubeLayerTests(unittest.TestCase):
    def test_gaps_are_mask_cutouts_over_the_three_complete_faces(self):
        faces = {path_data(face) for face in cube_polygons().values()}
        cuts = {}
        for role in ("driver", "orm"):
            text = render_icon(role, "currentColor", role)
            svg = ElementTree.fromstring(text)
            mask, group = masked_group(svg)
            painted = [p.get("d") for p in group.findall(SVG + "path") if p.get("fill") == "currentColor"]
            self.assertEqual(set(painted), faces, "each role must preserve the three complete cube faces")
            self.assertEqual({p.get("fill") for p in mask.findall(SVG + "path")}, {"#000"})
            self.assertNotIn('stroke="#fff"', text, "no painted white grooves remain")
            cuts[role] = [p.get("d") for p in mask.findall(SVG + "path")]
        self.assertEqual(len(cuts["driver"]), 4, "two gaps across each of the two side faces")
        self.assertEqual(len(cuts["orm"]), 4, "two gaps across the top and down the right face")
        self.assertNotEqual(cuts["driver"], cuts["orm"])

    def test_driver_gaps_are_equal_square_cuts_across_both_side_faces(self):
        mask, _ = masked_group(ElementTree.fromstring(render_icon("driver", "currentColor", "d")))
        faces = cube_polygons()
        thickness = set()
        for path in mask.findall(SVG + "path"):
            numbers = [float(n) for n in path.get("d").replace("M", " ").replace("L", " ").replace("Z", " ").split()]
            xs, ys = numbers[0::2], numbers[1::2]
            self.assertGreater(min(ys), faces["left"][0][1], "the top rhombus stays solid")
            self.assertTrue(min(xs) <= faces["left"][0][0] or max(xs) >= faces["right"][1][0], "cuts run out to the outer edge")
            thickness.add(round(ys[3] - ys[0], 3))
        self.assertEqual(thickness, {GEOMETRY["layer_gap"]}, "every cut has the shared gap thickness")

    def test_gap_width_comes_from_the_shared_token(self):
        self.assertEqual(GEOMETRY["layer_gap"], 1.2)

    def test_all_language_variants_use_transparent_gaps(self):
        icons = outputs()
        for name, meta in REGISTRY.items():
            if meta["role"] not in {"driver", "orm"}:
                continue
            with self.subTest(icon=name):
                text = icons[ROOT / "dist/icons" / f"{name}.svg"]
                svg = ElementTree.fromstring(text)
                self.assertTrue(list(svg.iter(SVG + "mask")))
                self.assertNotIn('stroke="#fff"', text)


class OperatorKnockoutTests(unittest.TestCase):
    def test_dial_is_a_mask_cutout_not_white_paint(self):
        svg_text = render_icon("operator", "currentColor", "operator")
        svg = ElementTree.fromstring(svg_text)
        mask, group = masked_group(svg)
        self.assertEqual(mask.get("maskUnits"), "userSpaceOnUse")
        strokes = {e.get("stroke") for e in mask.iter() if e.get("stroke")}
        self.assertEqual(strokes, {"#000"}, "the dial is cut out of the mask in black")
        self.assertNotIn('stroke="#fff"', svg_text, "no white dial strokes remain")
        painted = [p.get("d") for p in group.findall(SVG + "path") if p.get("fill") == "currentColor"]
        self.assertEqual(set(painted), {path_data(face) for face in cube_polygons().values()})


class McpKnockoutTests(unittest.TestCase):
    def test_router_is_a_mask_cutout_not_white_paint(self):
        svg_text = render_icon("mcp", "currentColor", "mcp")
        svg = ElementTree.fromstring(svg_text)
        mask, group = masked_group(svg)
        self.assertGreaterEqual(len(list(mask.iter(SVG + "circle"))), 4, "hub and three ports are cut out")
        painted_part = svg_text.split("</mask>")[1].replace('fill="#fff" opacity', "")
        self.assertNotIn('"#fff"', painted_part, "no white router paint remains")
        painted = [p.get("d") for p in group.findall(SVG + "path") if p.get("fill") == "currentColor"]
        self.assertEqual(set(painted), {path_data(face) for face in cube_polygons().values()})


class CookbookKnockoutTests(unittest.TestCase):
    def test_book_is_two_symmetric_cut_out_pages_without_text_lines(self):
        svg_text = render_icon("cookbook", "currentColor", "cookbook")
        svg = ElementTree.fromstring(svg_text)
        mask, _ = masked_group(svg)
        pages = [p for p in mask.iter(SVG + "path") if p.get("fill") == "#000"]
        self.assertEqual(len(pages), 1, "one path holding the two pages")
        self.assertEqual(pages[0].get("d").count("M"), 2)
        self.assertEqual(len([e for e in mask.iter() if e.get("stroke")]), 0, "no interior rule")
        painted_part = svg_text.split("</mask>")[1].replace('fill="#fff" opacity', "")
        self.assertNotIn('"#fff"', painted_part, "no white page blocks remain")


if __name__ == "__main__":
    unittest.main()
