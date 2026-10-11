from __future__ import annotations

import json
import math
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

    def test_driver_languages_have_tokens(self):
        for meta in self.repos.values():
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

    def test_driver_is_mirrored_around_x12(self):
        points = self.geometry["driver"]["left_points"]
        mirrored = [(24 - x, y) for x, y in points]
        self.assertEqual(len(points), len(mirrored))
        self.assertEqual(self.geometry["driver"]["mirror_axis_x"], 12)

    def test_central_channel_is_positive(self):
        self.assertGreater(self.geometry["driver"]["central_channel"], 0)

    def test_build_is_deterministic_and_emits_four_drivers(self):
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
        generated = sorted(p.name for p in (ROOT / "dist/icons").glob("*.svg"))
        self.assertEqual(
            generated,
            ["cubrid-client.svg", "cubrid-go.svg", "cubrid-rs.svg", "pycubrid.svg"],
        )
        for name in generated:
            text = (ROOT / "dist/icons" / name).read_text()
            self.assertNotIn("currentColor", text)


if __name__ == "__main__":
    unittest.main()
