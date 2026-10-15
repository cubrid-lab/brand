from __future__ import annotations

import hashlib
import math
import subprocess
import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build import (
    COLORS,
    GEOMETRY,
    ORGANIZATION,
    REGISTRY,
    ROLES,
    SURFACES,
    cube_polygons,
    outputs,
    render_icon,
)

SVG = "{http://www.w3.org/2000/svg}"
# Role symbols the maintainer explicitly approved (AGENTS.md rule 6): the four
# Driver variants, the Python ORM, MCP and Cookbook symbols (2026-10-14), and
# the Go Operator symbol (2026-10-15), recorded in issue #6.
APPROVED = {
    "pycubrid",
    "cubrid-client",
    "cubrid-go",
    "cubrid-rs",
    "sqlalchemy-cubrid",
    "cubrid-mcp-server",
    "cubrid-cookbook-python",
    "cubrid-kubernetes-operator",
}


class BrandTests(unittest.TestCase):
    def test_selected_geometry(self):
        self.assertEqual(GEOMETRY["design_id"], "repository-icon-cube-01")
        self.assertEqual(GEOMETRY["view_box"], [0, 0, 24, 24])
        self.assertEqual(GEOMETRY["rhombus_corner_angles_degrees"], [60, 120])
        self.assertAlmostEqual(GEOMETRY["roof_rise"] / GEOMETRY["half_width"], 1 / math.sqrt(3), places=8)
        top, left, right = (cube_polygons()[face] for face in ("top", "left", "right"))
        self.assertEqual([len(top), len(left), len(right)], [4, 4, 4])
        self.assertEqual(top[0][0], GEOMETRY["center"][0])
        self.assertEqual(left[0][0] + right[1][0], 24)
        self.assertGreater(right[0][0] - left[1][0], 0)
        for x, y in top + left + right:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 24)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 24)

    def test_historical_and_visual_references_are_unchanged(self):
        expected = {
            "provenance/connector-study-02/driver-python.svg": "2dda23aae3d5e418badb4f633ae1a00fbe9983aa35f8c8e2083feb7a3a0ae3b9",
            "docs/studies/repository-icon-system-infographic.png": "aeda456461b4336fc8545335a24629ec7dfe25b701f41760ac120a9e0f9c5716",
        }
        for name, digest in expected.items():
            with self.subTest(name=name):
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)

    def test_color_tokens_and_mappings(self):
        self.assertEqual(COLORS["python"], "#3776AB")
        self.assertEqual(COLORS["go"], "#00ADD8")
        self.assertEqual(COLORS["rust"], "#DEA384")
        self.assertEqual(COLORS["neutral"], "#6B7280")
        self.assertEqual(REGISTRY["drizzle-cubrid"]["language"], "typescript")
        self.assertEqual(REGISTRY["cubrid-benchmark"]["language"], "neutral")
        self.assertEqual(REGISTRY["showcase"]["language"], "neutral")
        self.assertFalse(set(REGISTRY) & set(SURFACES))
        for name, meta in {**REGISTRY, **SURFACES}.items():
            with self.subTest(name=name):
                self.assertIn(meta["role"], ROLES)
                self.assertIn(meta["language"], COLORS)
                self.assertIn(meta["status"], {"approved", "pending-symbol"})
                self.assertEqual(meta["status"] == "approved", name in APPROVED)

    def test_role_geometry_is_shared_across_languages(self):
        shapes = set()
        for role in ROLES:
            with self.subTest(role=role):
                python = ElementTree.fromstring(render_icon(role, COLORS["python"], "sample"))
                rust = ElementTree.fromstring(render_icon(role, COLORS["rust"], "sample"))
                self.assertEqual(python.attrib["color"], COLORS["python"])
                self.assertEqual(rust.attrib["color"], COLORS["rust"])
                self.assertEqual(
                    [ElementTree.tostring(node) for node in list(python)[2:]],
                    [ElementTree.tostring(node) for node in list(rust)[2:]],
                )
                shapes.add(tuple(ElementTree.tostring(node) for node in list(python)[2:]))
        self.assertEqual(len(shapes), len(ROLES))

    def test_generated_svg_structure(self):
        generated = outputs()
        self.assertEqual(len(generated), len(ROLES) + len(REGISTRY) + len(SURFACES) + 3)
        for path, content in generated.items():
            with self.subTest(path=path.name):
                svg = ElementTree.fromstring(content)
                self.assertEqual(svg.tag, SVG + "svg")
                expected_view_box = {
                    "lockup-horizontal.svg": "0 0 300 64",
                    "lockup-stacked.svg": "0 0 200 154",
                }.get(path.name, "0 0 24 24")
                self.assertEqual(svg.attrib["viewBox"], expected_view_box)
                self.assertIsNotNone(svg.find(SVG + "title"))
                self.assertIsNotNone(svg.find(SVG + "desc"))
                self.assertGreater(len(svg.findall(".//" + SVG + "path")), 0)
        organization = ElementTree.fromstring(generated[ROOT / "studies/organization/mark.svg"])
        self.assertEqual(
            {path.attrib["fill"] for path in organization.findall(SVG + "path")},
            set(ORGANIZATION["face_colors"].values()),
        )

    def test_deterministic_outputs(self):
        build = [sys.executable, str(ROOT / "scripts/build.py")]
        subprocess.run(build, check=True)
        expected = outputs()
        first = {path: path.read_bytes() for path in expected}
        subprocess.run(build, check=True)
        for path, content in expected.items():
            with self.subTest(path=path.name):
                self.assertEqual(path.read_text(encoding="utf-8"), content)
                self.assertEqual(path.read_bytes(), first[path])
        self.assertEqual(
            {p.name for p in (ROOT / "dist/icons").glob("*.svg")},
            {f"{name}.svg" for name, meta in {**REGISTRY, **SURFACES}.items() if meta["status"] == "approved"},
        )
        self.assertEqual(
            {p.name for p in (ROOT / "studies/icons").glob("*.svg")},
            {f"{name}.svg" for name, meta in {**REGISTRY, **SURFACES}.items() if meta["status"] == "pending-symbol"},
        )


if __name__ == "__main__":
    unittest.main()
