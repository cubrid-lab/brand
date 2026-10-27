"""Driver, ORM and MCP role candidates (issue #30, MCP direction from issue #23) and their promotion."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import build
from scripts.build import COLORS, REGISTRY, ROLE_CANDIDATES, TREATMENTS, ROLES, outputs, render_role_candidate, role_candidate_files
from tests.test_glyph_seams import seam_contacts
from tests.test_legibility import BELOW_THREE_TO_ONE, THRESHOLD, WHITE, contrast, face_shades, rgb, thin_white_marks
from tests.test_python_yellow_candidates import KEYLINE_RE, untreated

SVG = "{http://www.w3.org/2000/svg}"


def body(svg_text: str) -> list[bytes]:
    """The drawing below the title and description, without the language color."""
    return [ElementTree.tostring(node) for node in list(ElementTree.fromstring(svg_text))[2:]]


def spec_selected(candidate_id: str) -> bool:
    return ROLE_CANDIDATES[candidate_id]["selection"] == "selected"


class RoleCandidateTests(unittest.TestCase):
    def test_candidates_are_study_only_and_leave_src_dist_and_mapping_alone(self):
        generated = outputs()
        files = role_candidate_files()
        self.assertTrue(files)
        for path in files:
            self.assertEqual(path.parent, ROOT / "studies/roles")
            self.assertIn(path, generated)
        for spec in ROLE_CANDIDATES.values():
            self.assertEqual(spec["status"], "study")
            self.assertIn(spec["role"], ROLES)
        # The registry role mapping is untouched by the study.
        self.assertEqual({REGISTRY[name]["role"] for name in ("pycubrid", "cubrid-client", "cubrid-go", "cubrid-rs")}, {"driver"})
        self.assertEqual(REGISTRY["sqlalchemy-cubrid"]["role"], "orm")
        self.assertEqual(REGISTRY["cubrid-mcp-server"]["role"], "mcp")

    def test_unregistered_or_promoted_candidates_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "study-only"):
            render_role_candidate("orm-unknown", "python")
        with self.assertRaisesRegex(ValueError, "language"):
            render_role_candidate("orm-lateral-slabs", "rust")
        promoted = {**ROLE_CANDIDATES["orm-lateral-slabs"], "status": "approved"}
        original = build.ROLE_CANDIDATES
        build.ROLE_CANDIDATES = {**original, "orm-lateral-slabs": promoted}
        try:
            with self.assertRaisesRegex(ValueError, "study-only"):
                render_role_candidate("orm-lateral-slabs", "python")
        finally:
            build.ROLE_CANDIDATES = original

    def test_language_changes_only_the_color(self):
        for candidate_id, spec in ROLE_CANDIDATES.items():
            self.assertIn("python", spec["languages"])
            self.assertTrue(set(spec["languages"]) - {"python"}, "show at least one non-Python variant")
            first, *others = spec["languages"]
            for language in others:
                with self.subTest(candidate=candidate_id, language=language):
                    a = ElementTree.fromstring(render_role_candidate(candidate_id, first))
                    b = ElementTree.fromstring(render_role_candidate(candidate_id, language))
                    self.assertEqual(a.get("color"), COLORS[first])
                    self.assertEqual(b.get("color"), COLORS[language])
                    strip = lambda text, key: text.replace(f"{candidate_id}-{key}", "id")
                    # A selected candidate in a treated light token (issue #38) also gets its treatment.
                    plain = lambda key: untreated(render_role_candidate(candidate_id, key), TREATMENTS.get(COLORS[key], {}).get("mark", "#fff"))
                    self.assertEqual(
                        [strip(n.decode(), first) for n in body(plain(first))],
                        [strip(n.decode(), language) for n in body(plain(language))],
                    )

    def test_one_selected_candidate_per_role_is_the_promoted_geometry(self):
        selected = {spec["role"]: cid for cid, spec in ROLE_CANDIDATES.items() if spec["selection"] == "selected"}
        self.assertEqual(selected, {"driver": "driver-vertical-stack", "orm": "orm-lateral-plates", "mcp": "mcp-router-hub"})
        self.assertEqual(sum(spec["selection"] == "selected" for spec in ROLE_CANDIDATES.values()), 3)
        self.assertTrue(all(spec["selection"] in {"selected", "not-selected"} for spec in ROLE_CANDIDATES.values()))
        for role, candidate_id in selected.items():
            for language in ROLE_CANDIDATES[candidate_id]["languages"]:
                with self.subTest(role=role, language=language):
                    promoted = build.render_icon(role, COLORS[language], "x", "approved")
                    study = render_role_candidate(candidate_id, language).replace(f"{candidate_id}-{language}", "x")
                    if role in {"driver", "orm", "mcp"}:
                        # #30 stays a historical study; #41/#43 restore the cube;
                        # #58 replaces the MCP router with a hole at the junction.
                        self.assertNotEqual(body(promoted), body(study))
                    else:
                        # #50 opens only the promoted Python Yellow keyline at the seams.
                        self.assertEqual(body(KEYLINE_RE.sub("", promoted)), body(KEYLINE_RE.sub("", study)))
                        self.assertEqual(body(promoted) == body(study), "keyline" not in TREATMENTS.get(COLORS[language], {}))

    def test_unselected_candidates_are_distinct_from_each_other_and_current_roles(self):
        shapes = {tuple(body(build.render_icon(role, "currentColor", "x"))) for role in ROLES}
        for candidate_id, spec in ROLE_CANDIDATES.items():
            if spec["selection"] == "selected":
                continue
            drawing = tuple(n.replace(candidate_id.encode() + b"-python", b"x") for n in body(render_role_candidate(candidate_id, "python")))
            with self.subTest(candidate=candidate_id):
                self.assertNotIn(drawing, shapes)
            shapes.add(drawing)

    def test_white_marks_stay_off_seams_and_are_legible(self):
        for path, (candidate_id, language) in role_candidate_files().items():
            svg = render_role_candidate(candidate_id, language)
            with self.subTest(candidate=candidate_id, language=language):
                mark = TREATMENTS[COLORS[language]]["mark"] if spec_selected(candidate_id) and COLORS[language] in TREATMENTS else None
                self.assertEqual(seam_contacts(untreated(svg, mark) if mark else svg)[:5], [])
                if candidate_id == "mcp-router-hub" and language not in BELOW_THREE_TO_ONE:
                    shades = face_shades(svg)
                    ink = rgb(mark) if mark else WHITE
                    self.assertGreaterEqual(min(contrast(ink, shade) for shade in shades.values()), THRESHOLD)
        self.assertEqual(thin_white_marks(build.ROUTER_GLYPH), [])


if __name__ == "__main__":
    unittest.main()
