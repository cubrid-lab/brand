"""Python Yellow contrast treatments (issue #38): study-only renders of the approved Python icons."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import build
from scripts.build import COLORS, REGISTRY, YELLOW_CANDIDATES, outputs, render_icon, render_yellow_candidate, yellow_candidate_files
from tests.test_glyph_seams import seam_contacts
from tests.test_legibility import THRESHOLD, contrast, face_shades, rgb

TREATMENTS = YELLOW_CANDIDATES["treatments"]
INKS = {key: ink["value"] for key, ink in YELLOW_CANDIDATES["inks"].items()}
KEYLINE_RE = re.compile(r'  (?:<clipPath id="[^"]+-outside">.*?</clipPath>|<path [^>]*stroke-width="1\.2" stroke-linejoin="round"(?: clip-path="[^"]+")?/>)\n')


def body(svg_text: str) -> list[str]:
    """The drawing below the title and description."""
    return [ElementTree.tostring(node, encoding="unicode") for node in list(ElementTree.fromstring(svg_text))[2:]]


class PythonYellowCandidateTests(unittest.TestCase):
    def test_study_only_and_tokens_dist_unchanged(self):
        generated = outputs()
        for path, (treatment, name) in yellow_candidate_files().items():
            self.assertEqual(path.parent, ROOT / "studies/python-yellow")
            self.assertIn(path, generated)
            self.assertEqual(REGISTRY[name]["language"], "python")
        self.assertEqual({spec["status"] for spec in TREATMENTS.values()}, {"study"})
        # Phase 1 of issue #38: the language token and approved outputs keep Python Blue.
        self.assertEqual(COLORS["python"], "#3776AB")
        self.assertEqual(YELLOW_CANDIDATES["color"], "#FFD43B")
        self.assertEqual(sorted(YELLOW_CANDIDATES["repositories"]), sorted(n for n, m in REGISTRY.items() if m["language"] == "python"))

    def test_outputs_follow_a_redirected_root(self):
        # The temporary-root fixtures in tests/test_brand.py patch only ROOT, OUT and STUDY_OUT.
        root = Path("/nonexistent-root")
        with patch.object(build, "ROOT", root):
            files = set(yellow_candidate_files())
            self.assertTrue(all(path.parent == root / "studies/python-yellow" for path in files))
            self.assertLessEqual(files, build.owned_outputs())

    def test_inks_follow_their_recorded_derivation(self):
        yellow = rgb(YELLOW_CANDIDATES["color"])
        for key, amount in (("dark", 0.75), ("ochre", 0.45)):
            mixed = "#" + "".join(f"{round(c * (1 - amount)):02X}" for c in yellow)
            self.assertEqual(INKS[key], mixed)

    def test_unregistered_or_promoted_treatments_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "study-only"):
            render_yellow_candidate("t9-unknown", "pycubrid")
        with self.assertRaisesRegex(ValueError, "Python"):
            render_yellow_candidate("t0-naive", "cubrid-go")
        original = build.YELLOW_CANDIDATES
        promoted = {**TREATMENTS["t2-dark-keyline"], "status": "approved"}
        build.YELLOW_CANDIDATES = {**original, "treatments": {**TREATMENTS, "t2-dark-keyline": promoted}}
        try:
            with self.assertRaisesRegex(ValueError, "study-only"):
                render_yellow_candidate("t2-dark-keyline", "pycubrid")
        finally:
            build.YELLOW_CANDIDATES = original

    def test_naive_treatment_is_the_approved_icon_in_yellow(self):
        for name in YELLOW_CANDIDATES["repositories"]:
            meta = REGISTRY[name]
            with self.subTest(icon=name):
                approved = render_icon(meta["role"], YELLOW_CANDIDATES["color"], "x", "approved")
                study = render_yellow_candidate("t0-naive", name).replace(f"t0-naive-{name}", "x")
                self.assertEqual(body(approved), body(study))

    def test_treatments_change_only_mark_color_and_keyline(self):
        for treatment, spec in TREATMENTS.items():
            for name in YELLOW_CANDIDATES["repositories"]:
                with self.subTest(treatment=treatment, icon=name):
                    svg = render_yellow_candidate(treatment, name).replace(treatment, "t0-naive")
                    has_keyline = bool(spec["keyline"]) and REGISTRY[name]["role"] in spec["keyline_roles"]
                    stripped = KEYLINE_RE.sub("", svg)
                    self.assertEqual(stripped != svg, has_keyline)
                    if spec["mark"] != "white":
                        split = stripped.rindex("<g clip-path") if "<g clip-path" in stripped else len(stripped)
                        stripped = stripped[:split] + stripped[split:].replace(f'"{INKS[spec["mark"]]}"', '"#fff"')
                    self.assertEqual(body(stripped), body(render_yellow_candidate("t0-naive", name).replace(treatment, "t0-naive")))

    def test_dark_marks_reach_three_to_one_and_stay_off_seams(self):
        for treatment, spec in TREATMENTS.items():
            for name in ("cubrid-mcp-server", "cubrid-cookbook-python"):
                svg = render_yellow_candidate(treatment, name)
                mark = (255, 255, 255) if spec["mark"] == "white" else rgb(INKS[spec["mark"]])
                low = min(contrast(mark, shade) for shade in face_shades(svg).values())
                split = svg.rindex("<g clip-path")
                white = svg[:split] + svg[split:].replace(f'"{INKS.get(spec["mark"], "#fff")}"', '"#fff"')
                with self.subTest(treatment=treatment, icon=name):
                    self.assertEqual(seam_contacts(white)[:5], [])
                    if spec["mark"] == "white":
                        self.assertLess(low, THRESHOLD)  # The documented T0 problem.
                    else:
                        self.assertGreaterEqual(low, THRESHOLD)

    def test_keylines_reach_three_to_one_on_white(self):
        for treatment, spec in TREATMENTS.items():
            if spec["keyline"]:
                with self.subTest(treatment=treatment):
                    self.assertIn("driver", spec["keyline_roles"])
                    self.assertGreaterEqual(contrast(rgb(INKS[spec["keyline"]]), (255, 255, 255)), THRESHOLD)


if __name__ == "__main__":
    unittest.main()
