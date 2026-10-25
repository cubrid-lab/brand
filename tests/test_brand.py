from __future__ import annotations

import contextlib
import hashlib
import io
import math
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import build
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
# Driver variants, the Python ORM, MCP and Cookbook symbols (2026-10-14), the
# Go Operator symbol (2026-10-15), the TypeScript, Go and Rust ORM symbols
# (2026-10-20), and the Benchmark and Showcase symbols plus the Docs and
# Community surfaces (2026-10-25), recorded in issue #6. The Driver, ORM and
# MCP geometry was redrawn on 2026-10-25 (issues #30 and #23) with statuses kept.
APPROVED = {
    "pycubrid",
    "cubrid-client",
    "cubrid-go",
    "cubrid-rs",
    "sqlalchemy-cubrid",
    "drizzle-cubrid",
    "gorm-cubrid",
    "sea-orm-cubrid",
    "cubrid-mcp-server",
    "cubrid-cookbook-python",
    "cubrid-kubernetes-operator",
    "cubrid-benchmark",
    "showcase",
    "docs",
    "community",
}
# Wordmark lockups approved on 2026-10-25 (issue #3), each with a dark-background variant.
LOCKUPS = (
    "lockup-horizontal.svg",
    "lockup-horizontal-dark.svg",
    "lockup-stacked.svg",
    "lockup-stacked-dark.svg",
)
WORDMARK_TEXT_CONTRAST = 4.5


def contrast(a: str, b: str) -> float:
    """WCAG 2 contrast ratio of two ``#RRGGBB`` colors."""

    def luminance(color: str) -> float:
        def linear(channel: int) -> float:
            c = channel / 255
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

        r, g, b = (linear(int(color[i : i + 2], 16)) for i in (1, 3, 5))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


class BrandTests(unittest.TestCase):
    def test_organization_emblem_has_scoped_approval(self):
        generated = outputs()
        mark = ROOT / "dist/organization/mark.svg"
        self.assertIn(mark, generated.keys())
        self.assertNotIn(ROOT / "studies/organization/mark.svg", generated)
        svg = ElementTree.fromstring(generated[mark])
        self.assertIn("organization avatar/profile use approved", svg.find(SVG + "desc").text)
        self.assertIn("legal clearance pending", svg.find(SVG + "desc").text)
        self.assertEqual(ORGANIZATION["legal_clearance_status"], "pending")
        self.assertEqual(ORGANIZATION["redistribution_license_status"], "pending")
        with patch.dict(ORGANIZATION, {"emblem": {"design_status": "pending", "organization_use_rights_status": "pending"}}):
            pending = outputs()
        # The emblem and wordmark approvals are independent.
        for name in LOCKUPS:
            path = ROOT / "dist/organization" / name
            self.assertEqual(generated[path], pending[path])

    def test_organization_emblem_requires_both_approvals(self):
        for design, rights in (("pending", "pending"), ("approved", "pending"), ("pending", "approved")):
            with self.subTest(design=design, rights=rights), patch.dict(
                ORGANIZATION, {"emblem": {"design_status": design, "organization_use_rights_status": rights}}
            ):
                generated = outputs()
                self.assertNotIn(ROOT / "dist/organization/mark.svg", generated)
                svg = ElementTree.fromstring(generated[ROOT / "studies/organization/mark.svg"])
                self.assertIn("review pending", svg.find(SVG + "desc").text)

    def test_organization_emblem_rejects_unknown_approval(self):
        for field in ("design_status", "organization_use_rights_status"):
            approval = {"design_status": "approved", "organization_use_rights_status": "approved"}
            approval[field] = "unknown"
            with (
                self.subTest(field=field),
                patch.dict(ORGANIZATION, {"emblem": approval}),
                self.assertRaisesRegex(ValueError, "organization approval"),
            ):
                outputs()

    def test_organization_emblem_cleanup_follows_approval(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.multiple(build, ROOT=root, OUT=root / "dist/icons", STUDY_OUT=root / "studies/icons"):
                approved = root / "dist/organization/mark.svg"
                study = root / "studies/organization/mark.svg"
                build.main()
                self.assertTrue(approved.exists())
                with patch.dict(ORGANIZATION, {"emblem": {"design_status": "approved", "organization_use_rights_status": "pending"}}):
                    build.main()
                    self.assertFalse(approved.exists())
                    self.assertTrue(study.exists())
                build.main()
                self.assertTrue(approved.exists())
                self.assertFalse(study.exists())

    def test_cleanup_preserves_and_reports_unmanaged_svgs(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.multiple(build, ROOT=root, OUT=root / "dist/icons", STUDY_OUT=root / "studies/icons"):
                self.assertEqual(build.main(), 0)
                unmanaged = [
                    root / directory / "unrelated.svg"
                    for directory in ("dist/icons", "studies/icons", "dist/organization", "studies/organization")
                ]
                for path in unmanaged:
                    # No entry is pending-symbol, so the build may not create studies/icons/.
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("<svg/>", encoding="utf-8")
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    status = build.main()
                self.assertEqual(status, 1)
                for path in unmanaged:
                    with self.subTest(path=str(path.relative_to(root))):
                        self.assertEqual(path.read_text(encoding="utf-8"), "<svg/>")
                        self.assertIn(path.relative_to(root).as_posix(), stderr.getvalue())

    def test_cleanup_removes_stale_owned_outputs(self):
        # Treat one entry as pending so both review locations hold a stale owned copy.
        pending = {**REGISTRY["cubrid-benchmark"], "status": "pending-symbol"}
        with TemporaryDirectory() as folder, patch.dict(REGISTRY, {"cubrid-benchmark": pending}):
            root = Path(folder)
            with patch.multiple(build, ROOT=root, OUT=root / "dist/icons", STUDY_OUT=root / "studies/icons"):
                build.main()
                stale = (
                    root / "studies/icons/pycubrid.svg",
                    root / "dist/icons/cubrid-benchmark.svg",
                    root / "studies/organization/mark.svg",
                )
                for path in stale:
                    path.write_text("<svg/>", encoding="utf-8")
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    self.assertEqual(build.main(), 0)
                self.assertEqual(stderr.getvalue(), "")
                for path in stale:
                    with self.subTest(path=str(path.relative_to(root))):
                        self.assertFalse(path.exists())

    def test_cleanup_follows_repository_status_moves(self):
        pending = {**REGISTRY["pycubrid"], "status": "pending-symbol"}
        with TemporaryDirectory() as folder:
            root = Path(folder)
            approved = root / "dist/icons/pycubrid.svg"
            study = root / "studies/icons/pycubrid.svg"
            with patch.multiple(build, ROOT=root, OUT=root / "dist/icons", STUDY_OUT=root / "studies/icons"):
                build.main()
                self.assertTrue(approved.exists())
                with patch.dict(REGISTRY, {"pycubrid": pending}):
                    self.assertEqual(build.main(), 0)
                    self.assertFalse(approved.exists())
                    self.assertTrue(study.exists())
                self.assertEqual(build.main(), 0)
                self.assertTrue(approved.exists())
                self.assertFalse(study.exists())

    def test_wordmark_lockups_have_scoped_approval(self):
        generated = outputs()
        wordmarks = ORGANIZATION["wordmarks"]
        self.assertEqual((wordmarks["design_status"], wordmarks["organization_use_rights_status"]), ("approved", "approved"))
        self.assertEqual(wordmarks["approved_on"], "2026-10-25")
        self.assertIn("Not a license and not legal or trademark clearance", wordmarks["scope"])
        self.assertEqual(ORGANIZATION["legal_clearance_status"], "pending")
        self.assertEqual(ORGANIZATION["redistribution_license_status"], "pending")
        for name in LOCKUPS:
            with self.subTest(name=name):
                self.assertNotIn(ROOT / "studies/organization" / name, generated)
                svg = ElementTree.fromstring(generated[ROOT / "dist/organization" / name])
                self.assertNotIn("study", svg.find(SVG + "title").text)
                self.assertIn("own-organization use approved", svg.find(SVG + "desc").text)
                self.assertIn("legal clearance pending", svg.find(SVG + "desc").text)

    def test_wordmark_lockups_require_both_approvals(self):
        for design, rights in (("pending", "pending"), ("approved", "pending"), ("pending", "approved")):
            wordmarks = {**ORGANIZATION["wordmarks"], "design_status": design, "organization_use_rights_status": rights}
            with self.subTest(design=design, rights=rights), patch.dict(ORGANIZATION, {"wordmarks": wordmarks}):
                generated = outputs()
                self.assertIn(ROOT / "dist/organization/mark.svg", generated)
                for name in LOCKUPS:
                    self.assertNotIn(ROOT / "dist/organization" / name, generated)
                    svg = ElementTree.fromstring(generated[ROOT / "studies/organization" / name])
                    self.assertIn("study", svg.find(SVG + "title").text)
                    self.assertIn("review pending", svg.find(SVG + "desc").text)

    def test_wordmark_lockups_reject_unknown_approval(self):
        for field in ("design_status", "organization_use_rights_status"):
            wordmarks = {**ORGANIZATION["wordmarks"], field: "unknown"}
            with (
                self.subTest(field=field),
                patch.dict(ORGANIZATION, {"wordmarks": wordmarks}),
                self.assertRaisesRegex(ValueError, "wordmark approval"),
            ):
                outputs()

    def test_wordmark_lockup_cleanup_follows_approval(self):
        pending = {**ORGANIZATION["wordmarks"], "design_status": "pending"}
        with TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.multiple(build, ROOT=root, OUT=root / "dist/icons", STUDY_OUT=root / "studies/icons"):
                # Start from the pre-approval layout: light lockups only, under studies/.
                study = root / "studies/organization"
                study.mkdir(parents=True)
                for layout in ("horizontal", "stacked"):
                    (study / f"lockup-{layout}.svg").write_text("<svg/>", encoding="utf-8")
                self.assertEqual(build.main(), 0)
                for name in LOCKUPS:
                    self.assertTrue((root / "dist/organization" / name).exists())
                    self.assertFalse((study / name).exists())
                with patch.dict(ORGANIZATION, {"wordmarks": pending}):
                    self.assertEqual(build.main(), 0)
                    for name in LOCKUPS:
                        self.assertFalse((root / "dist/organization" / name).exists())
                        self.assertTrue((study / name).exists())
                self.assertEqual(build.main(), 0)
                for name in LOCKUPS:
                    self.assertTrue((root / "dist/organization" / name).exists())
                    self.assertFalse((study / name).exists())

    def test_dark_lockups_change_only_the_text_color(self):
        generated = outputs()
        variants = ORGANIZATION["wordmarks"]["variants"]
        for layout in ("horizontal", "stacked"):
            with self.subTest(layout=layout):
                light = ElementTree.fromstring(generated[ROOT / f"dist/organization/lockup-{layout}.svg"])
                dark = ElementTree.fromstring(generated[ROOT / f"dist/organization/lockup-{layout}-dark.svg"])
                self.assertIn("dark backgrounds", dark.find(SVG + "title").text)
                self.assertEqual(ElementTree.tostring(light.find(SVG + "g")), ElementTree.tostring(dark.find(SVG + "g")))
                light_text, dark_text = light.findall(SVG + "text"), dark.findall(SVG + "text")
                self.assertEqual([t.text for t in light_text], ["CUBRID Lab", ORGANIZATION["wordmarks"]["tagline"]])
                self.assertEqual([t.text for t in light_text], [t.text for t in dark_text])
                self.assertEqual([t.get("fill") for t in light_text], [variants["light"]["title"], variants["light"]["tagline"]])
                self.assertEqual([t.get("fill") for t in dark_text], [variants["dark"]["title"], variants["dark"]["tagline"]])
                for a, b in zip(light_text, dark_text):
                    self.assertEqual({k: v for k, v in a.attrib.items() if k != "fill"}, {k: v for k, v in b.attrib.items() if k != "fill"})

    def test_wordmark_text_contrast(self):
        variants = ORGANIZATION["wordmarks"]["variants"]
        self.assertEqual(set(variants), {"light", "dark"})
        for name, colors in variants.items():
            for part in ("title", "tagline"):
                with self.subTest(variant=name, part=part):
                    self.assertGreaterEqual(contrast(colors[part], colors["background"]), WORDMARK_TEXT_CONTRAST)
        # The reason for the dark variant: the light text nearly vanishes on a dark background.
        self.assertLess(contrast(variants["light"]["title"], variants["dark"]["background"]), 1.5)

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
        self.assertEqual(COLORS["python"], "#FFD43B")
        self.assertEqual(COLORS["typescript"], "#3178C6")
        self.assertEqual(COLORS["javascript"], "#F7DF1E")
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
                # Python's contrast treatment (issue #38) is covered in test_python_yellow_candidates.py.
                python = ElementTree.fromstring(render_icon(role, COLORS["typescript"], "sample"))
                rust = ElementTree.fromstring(render_icon(role, COLORS["rust"], "sample"))
                self.assertEqual(python.attrib["color"], COLORS["typescript"])
                self.assertEqual(rust.attrib["color"], COLORS["rust"])
                self.assertEqual(
                    [ElementTree.tostring(node) for node in list(python)[2:]],
                    [ElementTree.tostring(node) for node in list(rust)[2:]],
                )
                shapes.add(tuple(ElementTree.tostring(node) for node in list(python)[2:]))
        self.assertEqual(len(shapes), len(ROLES))

    def test_organization_candidates_and_role_distinction(self):
        generated = outputs()
        driver_svg = ElementTree.fromstring(generated[ROOT / "src/driver.svg"])
        orm_svg = ElementTree.fromstring(generated[ROOT / "src/orm.svg"])
        driver_paths = {p.attrib["d"] for p in driver_svg.findall(".//" + SVG + "path")}
        orm_layer_paths = {p.attrib["d"] for p in orm_svg.findall(".//" + SVG + "path")[1:]}
        candidate_signatures = set()
        for path in (
            ROOT / "dist/organization/mark.svg",
            ROOT / "studies/organization/candidate-monochrome-cube.svg",
            ROOT / "studies/organization/candidate-hex-frame.svg",
        ):
            with self.subTest(path=path.name):
                self.assertIn(path, generated)
                if path.name.startswith("candidate-"):
                    self.assertNotIn(ROOT / "dist/organization" / path.name, generated)
                svg = ElementTree.fromstring(generated[path])
                self.assertIsNone(svg.find(".//" + SVG + "circle"))
                paths = [p.attrib["d"] for p in svg.findall(".//" + SVG + "path")]
                self.assertFalse(set(paths) & orm_layer_paths)
                self.assertNotIn("M 12.6 18.1 L 15.7 16.15 L 17.45 16.15", driver_paths & set(paths))
                fills = tuple(p.attrib["fill"] for p in svg.findall(".//" + SVG + "path"))
                candidate_signatures.add((tuple(paths), fills))
        self.assertEqual(len(candidate_signatures), 3)

    def test_generated_svg_structure(self):
        generated = outputs()
        self.assertEqual(
            len(generated),
            len(ROLES) + len(REGISTRY) + len(SURFACES) + 1 + len(LOCKUPS) + len(ORGANIZATION["candidates"])
            + len(build.role_candidate_files()) + len(build.yellow_candidate_files()),
        )
        for path, content in generated.items():
            with self.subTest(path=path.name):
                svg = ElementTree.fromstring(content)
                self.assertEqual(svg.tag, SVG + "svg")
                expected_view_box = {
                    "lockup-horizontal.svg": "0 0 300 64",
                    "lockup-horizontal-dark.svg": "0 0 300 64",
                    "lockup-stacked.svg": "0 0 200 154",
                    "lockup-stacked-dark.svg": "0 0 200 154",
                }.get(path.name, "0 0 24 24")
                self.assertEqual(svg.attrib["viewBox"], expected_view_box)
                self.assertIsNotNone(svg.find(SVG + "title"))
                self.assertIsNotNone(svg.find(SVG + "desc"))
                self.assertGreater(len(svg.findall(".//" + SVG + "path")), 0)
        organization = ElementTree.fromstring(generated[ROOT / "dist/organization/mark.svg"])
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
