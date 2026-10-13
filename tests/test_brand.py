from __future__ import annotations

import json
import math
import re
import subprocess
import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build import COLORS, GEOMETRY, REGISTRY, driver_polygons, outputs


class BrandTests(unittest.TestCase):
    def test_original_study_parameters(self):
        self.assertEqual(GEOMETRY["design_id"], "connector-study-02")
        self.assertEqual(GEOMETRY["view_box"], [0, 0, 24, 24])
        self.assertEqual(GEOMETRY["seam_width"], 1.5)
        self.assertEqual(GEOMETRY["edge_directions_degrees"], [0, 60, 120])

    def test_study_language_palette(self):
        self.assertEqual(COLORS["python"], "#3776AB")
        self.assertEqual(COLORS["go"], "#00ADD8")
        self.assertEqual(COLORS["rust"], "#DEA384")

    def test_rotation_envelope_and_edges(self):
        left, right = driver_polygons()
        self.assertEqual(len(left), 7)
        self.assertEqual(len(right), 7)
        for (x, y), (u, v) in zip(left, right):
            self.assertAlmostEqual(x + u, 24, places=9)
            self.assertAlmostEqual(y + v, 24, places=9)
        pts = left + right
        self.assertAlmostEqual(max(x for x, _ in pts) - min(x for x, _ in pts), 20)
        self.assertAlmostEqual(max(y for _, y in pts) - min(y for _, y in pts), 8 * math.sqrt(3))
        for polygon in (left, right):
            for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) % 180
                self.assertTrue(any(abs(angle - a) < 1e-8 for a in (0, 60, 120, 180)), angle)

    def test_generated_contour_matches_approved_original(self):
        source = ROOT / "provenance/connector-study-02/driver-python.svg"
        svg = ElementTree.fromstring(source.read_text(encoding="utf-8"))
        paths = svg.findall(".//{http://www.w3.org/2000/svg}path")
        self.assertEqual(len(paths), 2)

        def extract(d):
            values = [float(v) for v in re.findall(r"-?\d+\.\d+", d)]
            return list(zip(values[::2], values[1::2]))

        original_left = extract(paths[0].attrib["d"])
        original_right = extract(paths[1].attrib["d"])
        self.assertEqual([len(original_left), len(original_right)], [7, 8])
        left, right = driver_polygons()
        simplified_right = original_right[:6] + original_right[7:]
        for original, generated in ((original_left, left), (simplified_right, right)):
            for (a, b), (c, d) in zip(original, generated):
                self.assertAlmostEqual(a, c, places=8)
                self.assertAlmostEqual(b, d, places=8)

    def test_mappings(self):
        for meta in REGISTRY.values():
            self.assertIn(meta["language"], COLORS)
        self.assertEqual(REGISTRY["cubrid-mcp-server"]["language"], "python")
        self.assertEqual(REGISTRY["cubrid-kubernetes-operator"]["language"], "go")

    def test_deterministic_outputs(self):
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
        generated = outputs()
        for path, content in generated.items():
            self.assertEqual(path.read_text(encoding="utf-8"), content)
        self.assertEqual(
            {p.name for p in (ROOT / "dist/icons").glob("*.svg")},
            {"pycubrid.svg", "cubrid-client.svg", "cubrid-go.svg", "cubrid-rs.svg"},
        )
        for repo, meta in REGISTRY.items():
            if meta["role"] == "driver" and meta["status"] == "approved":
                svg = (ROOT / "dist/icons" / f"{repo}.svg").read_text()
                self.assertIn(COLORS[meta["language"]], svg)
                self.assertEqual(svg.count("<path "), 2)


if __name__ == "__main__":
    unittest.main()
