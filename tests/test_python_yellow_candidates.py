"""Python Yellow contrast treatments (issue #38): the study candidates and the promoted T3 treatment."""
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
from scripts.build import COLORS, REGISTRY, TREATMENTS, YELLOW_CANDIDATES, outputs, render_icon, render_yellow_candidate, yellow_candidate_files
from tests.test_glyph_seams import seam_contacts
from tests.test_legibility import THRESHOLD, contrast, face_shades, rgb

TREATMENTS_STUDY = YELLOW_CANDIDATES["treatments"]
INKS = {key: ink["value"] for key, ink in YELLOW_CANDIDATES["inks"].items()}
SVG = "{http://www.w3.org/2000/svg}"
KEYLINE_RE = re.compile(r'  (?:<clipPath id="[^"]+-outside">.*?</clipPath>|<path [^>]*stroke-width="1\.2" stroke-linejoin="round"(?: clip-path="[^"]+")?/>)\n')


def untreated(svg_text: str, mark: str) -> str:
    """The SVG without its keyline, with the visible ``mark`` color back to white."""
    stripped = KEYLINE_RE.sub("", svg_text)
    if "<g clip-path" not in stripped:
        return stripped
    split = stripped.rindex("<g clip-path")
    return stripped[:split] + stripped[split:].replace(f'"{mark}"', '"#fff"')


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
        self.assertEqual({spec["status"] for spec in TREATMENTS_STUDY.values()}, {"study"})
        self.assertEqual(COLORS["python"], "#FFD43B")
        self.assertEqual(YELLOW_CANDIDATES["color"], COLORS["python"])
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
        promoted = {**TREATMENTS_STUDY["t2-dark-keyline"], "status": "approved"}
        build.YELLOW_CANDIDATES = {**original, "treatments": {**TREATMENTS_STUDY, "t2-dark-keyline": promoted}}
        try:
            with self.assertRaisesRegex(ValueError, "study-only"):
                render_yellow_candidate("t2-dark-keyline", "pycubrid")
        finally:
            build.YELLOW_CANDIDATES = original

    def test_naive_treatment_is_the_approved_icon_in_yellow(self):
        for name in YELLOW_CANDIDATES["repositories"]:
            meta = REGISTRY[name]
            with self.subTest(icon=name):
                # An untreated token draws the same geometry; only the color attribute differs.
                approved = render_icon(meta["role"], COLORS["typescript"], "x", "approved")
                study = render_yellow_candidate("t0-naive", name).replace(f"t0-naive-{name}", "x")
                if meta["role"] in {"driver", "orm"}:
                    # The #38 study predates the restored cube shapes.
                    self.assertNotEqual(body(approved), body(study))
                else:
                    self.assertEqual(body(approved), body(study))

    def test_promoted_python_icons_are_the_selected_t3_candidate(self):
        # Maintainer decision on 2026-10-25 (issue #38): t3-ochre-keyline.
        spec = TREATMENTS[COLORS["python"]]
        self.assertEqual(
            (spec["mark"], spec["keyline"], spec["keyline_width"]),
            (INKS["dark"], INKS["ochre"], YELLOW_CANDIDATES["keyline_width"]),
        )
        t3 = TREATMENTS_STUDY["t3-ochre-keyline"]
        self.assertEqual((t3["mark"], t3["keyline"], len(t3["keyline_roles"])), ("dark", "ochre", 4))
        generated = outputs()
        for name in YELLOW_CANDIDATES["repositories"]:
            with self.subTest(icon=name):
                promoted = generated[ROOT / "dist/icons" / f"{name}.svg"]
                study = render_yellow_candidate("t3-ochre-keyline", name).replace(f"t3-ochre-keyline-{name}", name)
                self.assertEqual(ElementTree.fromstring(promoted).get("color"), "#FFD43B")
                if REGISTRY[name]["role"] in {"driver", "orm"}:
                    # Preserve reviewed yellow treatments as historical evidence.
                    self.assertNotEqual(body(promoted), body(study))
                else:
                    # #50 opens the promoted keyline at the seams; the #38 study keeps its
                    # closed outline. Everything else is the selected T3 drawing.
                    self.assertNotEqual(body(promoted), body(study))
                    self.assertEqual(body(KEYLINE_RE.sub("", promoted)), body(KEYLINE_RE.sub("", study)))

    def test_promoted_icons_draw_the_treatment_colors(self):
        spec = TREATMENTS[COLORS["python"]]
        generated = outputs()
        for name in YELLOW_CANDIDATES["repositories"]:
            svg = generated[ROOT / "dist/icons" / f"{name}.svg"]
            root = ElementTree.fromstring(svg)
            strokes = [node.get("stroke") for node in root.iter() if node.get("stroke-width") == "1.2" and node.get("fill") == "none"]
            with self.subTest(icon=name):
                self.assertTrue(strokes)
                self.assertEqual(set(strokes), {spec["keyline"]})
                if REGISTRY[name]["role"] in {"mcp", "cookbook"}:
                    # The visible mark is the last clipped group; it must not be white any more.
                    mark = [g for g in root.iter(SVG + "g") if g.get("clip-path")][-1]
                    paints = {node.get(key) for node in mark.iter() for key in ("fill", "stroke")} - {None, "none", "currentColor"}
                    self.assertEqual(paints, {spec["mark"]})

    def test_promoted_keylines_keep_the_emblem_silhouette(self):
        # Issue #50: the organization emblem is the baseline cube. Its seams stay open at
        # the side corners and the bottom vertex, so the keyline may only run along a
        # face's outer edges and never join two faces.
        # An allowed segment lies on the cube's silhouette and is an edge of a single face.
        silhouette = build.cube_outline()
        sides = list(zip(silhouette, silhouette[1:] + silhouette[:1]))

        def on_silhouette(p, q):
            # Both ends on one silhouette side: collinear and within its span.
            return any(
                all(
                    abs((b[0] - a[0]) * (r[1] - a[1]) - (b[1] - a[1]) * (r[0] - a[0])) < 1e-6
                    and min(a[0], b[0]) - 1e-6 <= r[0] <= max(a[0], b[0]) + 1e-6
                    and min(a[1], b[1]) - 1e-6 <= r[1] <= max(a[1], b[1]) + 1e-6
                    for r in (p, q)
                )
                for a, b in sides
            )

        outer_edges = {
            frozenset(map(self._rounded, (a, b)))
            for points in build.cube_polygons().values()
            for a, b in zip(points, points[1:] + points[:1])
            if on_silhouette(a, b)
        }
        self.assertEqual(len(outer_edges), 6)
        generated = outputs()
        for name in YELLOW_CANDIDATES["repositories"]:
            root = ElementTree.fromstring(generated[ROOT / "dist/icons" / f"{name}.svg"])
            keyline = [node for node in root.iter(SVG + "path") if node.get("stroke-width") == "1.2"]
            with self.subTest(icon=name):
                self.assertEqual(len(keyline), 1)
                for subpath in re.findall(r"M[^M]+", keyline[0].get("d")):
                    points = [tuple(map(float, xy)) for xy in re.findall(r"(-?[\d.]+) (-?[\d.]+)", subpath)]
                    for a, b in zip(points, points[1:]):
                        self.assertIn(frozenset((a, b)), outer_edges)

    @staticmethod
    def _rounded(point: tuple[float, float]) -> tuple[float, float]:
        return tuple(round(c, build.GEOMETRY["decimal_places"]) for c in point)

    def test_promoted_contrast_matches_the_review(self):
        spec = TREATMENTS[COLORS["python"]]
        white, dark = (255, 255, 255), (13, 17, 23)
        for name in ("cubrid-mcp-server", "cubrid-cookbook-python"):
            svg = outputs()[ROOT / "dist/icons" / f"{name}.svg"]
            low = min(contrast(rgb(spec["mark"]), shade) for shade in face_shades(svg).values())
            with self.subTest(icon=name):
                self.assertAlmostEqual(low, 6.84, places=2)
                self.assertEqual(seam_contacts(untreated(svg, spec["mark"]))[:5], [])
        self.assertAlmostEqual(contrast(rgb(spec["keyline"]), white), 4.49, places=2)
        self.assertAlmostEqual(contrast(rgb(spec["keyline"]), dark), 4.22, places=2)

    def test_treatments_change_only_mark_color_and_keyline(self):
        for treatment, spec in TREATMENTS_STUDY.items():
            for name in YELLOW_CANDIDATES["repositories"]:
                with self.subTest(treatment=treatment, icon=name):
                    svg = render_yellow_candidate(treatment, name).replace(treatment, "t0-naive")
                    has_keyline = bool(spec["keyline"]) and REGISTRY[name]["role"] in spec["keyline_roles"]
                    self.assertEqual(KEYLINE_RE.sub("", svg) != svg, has_keyline)
                    plain = untreated(svg, INKS.get(spec["mark"], "#fff"))
                    self.assertEqual(body(plain), body(render_yellow_candidate("t0-naive", name)))

    def test_dark_marks_reach_three_to_one_and_stay_off_seams(self):
        for treatment, spec in TREATMENTS_STUDY.items():
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
        for treatment, spec in TREATMENTS_STUDY.items():
            if spec["keyline"]:
                with self.subTest(treatment=treatment):
                    self.assertIn("driver", spec["keyline_roles"])
                    self.assertGreaterEqual(contrast(rgb(INKS[spec["keyline"]]), (255, 255, 255)), THRESHOLD)


if __name__ == "__main__":
    unittest.main()
