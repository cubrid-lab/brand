"""Study-only Driver, ORM and MCP role candidates (issue #30, MCP direction from issue #23)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import build
from scripts.build import COLORS, REGISTRY, ROLE_CANDIDATES, ROLES, outputs, render_role_candidate, role_candidate_files
from tests.test_glyph_seams import seam_contacts
from tests.test_legibility import THRESHOLD, WHITE, contrast, face_shades, thin_white_marks

SVG = "{http://www.w3.org/2000/svg}"


def body(svg_text: str) -> list[bytes]:
    """The drawing below the title and description, without the language color."""
    return [ElementTree.tostring(node) for node in list(ElementTree.fromstring(svg_text))[2:]]


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
                    self.assertEqual(
                        [strip(n.decode(), first) for n in body(render_role_candidate(candidate_id, first))],
                        [strip(n.decode(), language) for n in body(render_role_candidate(candidate_id, language))],
                    )

    def test_driver_stack_is_the_current_orm_geometry(self):
        current = body(build.render_icon("orm", "currentColor", "orm"))
        self.assertEqual(body(render_role_candidate("driver-vertical-stack", "python")), current)

    def test_candidates_are_distinct_from_each_other_and_current_roles(self):
        shapes = {tuple(body(build.render_icon(role, "currentColor", "x"))) for role in ROLES if role != "orm"}
        for candidate_id in ROLE_CANDIDATES:
            drawing = tuple(n.replace(candidate_id.encode() + b"-python", b"x") for n in body(render_role_candidate(candidate_id, "python")))
            with self.subTest(candidate=candidate_id):
                self.assertNotIn(drawing, shapes)
            shapes.add(drawing)

    def test_white_marks_stay_off_seams_and_are_legible(self):
        for path, (candidate_id, language) in role_candidate_files().items():
            svg = render_role_candidate(candidate_id, language)
            with self.subTest(candidate=candidate_id, language=language):
                self.assertEqual(seam_contacts(svg)[:5], [])
                if candidate_id == "mcp-router-hub":
                    shades = face_shades(svg)
                    self.assertGreaterEqual(min(contrast(WHITE, shade) for shade in shades.values()), THRESHOLD)
        self.assertEqual(thin_white_marks(build.ROUTER_GLYPH), [])


if __name__ == "__main__":
    unittest.main()
