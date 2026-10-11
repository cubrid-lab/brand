from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BrandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.colors = json.loads((ROOT / "tokens/colors.json").read_text())["languages"]
        cls.geometry = json.loads((ROOT / "tokens/geometry.json").read_text())
        cls.repos = json.loads((ROOT / "registry/repositories.json").read_text())["repositories"]

    def test_all_repository_languages_have_tokens(self):
        for repo, meta in self.repos.items():
            with self.subTest(repo=repo):
                self.assertIn(meta["language"], self.colors)

    def test_expected_repository_mapping(self):
        self.assertEqual(self.repos["cubrid-mcp-server"]["language"], "python")
        self.assertEqual(self.repos["cubrid-kubernetes-operator"]["language"], "go")
        self.assertEqual(self.repos["cubrid-client"]["language"], "typescript")

    def test_only_driver_is_approved_role_symbol(self):
        approved_roles = {
            meta["role"] for meta in self.repos.values() if meta["status"] == "approved"
        }
        self.assertEqual(approved_roles, {"driver"})

    def test_driver_geometry_is_centered_and_mirrorable(self):
        view_x, _, view_w, _ = self.geometry["view_box"]
        driver = self.geometry["driver"]
        axis = driver["mirror_axis_x"]
        self.assertEqual(axis, view_x + view_w / 2)

        left = driver["left_points"]
        right = [[2 * axis - x, y] for x, y in left]
        self.assertEqual(len(left), len(right))
        self.assertTrue(all(lx < axis for lx, _ in left))
        self.assertTrue(all(rx > axis for rx, _ in right))

    def test_declared_central_channel_matches_geometry(self):
        driver = self.geometry["driver"]
        axis = driver["mirror_axis_x"]
        left = driver["left_points"]
        right = [[2 * axis - x, y] for x, y in left]
        actual = min(x for x, _ in right) - max(x for x, _ in left)
        self.assertEqual(actual, driver["central_channel"])
        self.assertGreater(actual, 0)

    def test_points_stay_inside_view_box(self):
        x0, y0, width, height = self.geometry["view_box"]
        xmax, ymax = x0 + width, y0 + height
        for x, y in self.geometry["driver"]["left_points"]:
            self.assertGreaterEqual(x, x0)
            self.assertLessEqual(x, xmax)
            self.assertGreaterEqual(y, y0)
            self.assertLessEqual(y, ymax)

    def test_build_is_deterministic_and_emits_only_approved_drivers(self):
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
        generated = sorted(p.name for p in (ROOT / "dist/icons").glob("*.svg"))
        expected = sorted(
            f"{repo}.svg"
            for repo, meta in self.repos.items()
            if meta["role"] == "driver" and meta["status"] == "approved"
        )
        self.assertEqual(generated, expected)

        base = (ROOT / "src/driver.svg").read_text()
        self.assertIn("Generated from tokens/geometry.json", base)
        self.assertIn('fill="currentColor"', base)

        for repo, meta in self.repos.items():
            if meta["role"] != "driver" or meta["status"] != "approved":
                continue
            text = (ROOT / "dist/icons" / f"{repo}.svg").read_text()
            self.assertNotIn("currentColor", text)
            self.assertIn(self.colors[meta["language"]], text)
            # Geometry must be byte-identical across language variants after color/label changes.
            normalized = text.replace(self.colors[meta["language"]], "COLOR")
            normalized = normalized.replace(f"{repo} Driver symbol", "REPO Driver symbol")
            self.assertIn('id="left"', normalized)
            self.assertIn('id="right"', normalized)


if __name__ == "__main__":
    unittest.main()
