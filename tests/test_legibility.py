"""Lightweight small-size legibility guards (issue #21).

Two objective checks, with no extra dependencies:

- Contrast: the WCAG 2 contrast ratio of the role mark (white, or the dark ink of a
  treated light token, issue #38) on every face shade
  the generator draws, for every language token used by a repository or surface
  icon that has a role mark. 3:1 is the WCAG 1.4.11 non-text threshold, used
  here as review guidance, not as a compliance claim. Tokens below it are listed
  in ``BELOW_THREE_TO_ONE`` and documented in
  ``docs/studies/small-size-legibility.md``; any new one fails until reviewed.
- Stroke weight: no white stroke or dot in a role mark is thinner than
  ``MIN_WHITE_UNITS`` viewBox units, i.e. one device pixel at 24 px.
"""
from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build import COLORS, GLYPHS, REGISTRY, SURFACES, TREATMENTS, cube_polygons, path_data, render_icon

SVG = "{http://www.w3.org/2000/svg}"
WHITE = (255, 255, 255)
THRESHOLD = 3.0
# Go's existing low contrast and Rust's reintroduced white cube grooves are
# recorded as visual review limitations (issues #21, #41 and #43). Python Yellow
# draws the same white marks as every other language since issue #54.
BELOW_THREE_TO_ONE = {"go", "rust", "python"}
# Driver/ORM now use white grooves too.
UNMARKED_ROLES: set[str] = set()
MIN_WHITE_UNITS = 1.0


def rgb(color: str) -> tuple[int, int, int]:
    digits = color[1:] if len(color) == 7 else "".join(2 * c for c in color[1:])
    return tuple(int(digits[i : i + 2], 16) for i in (0, 2, 4))


def contrast(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    def luminance(value: tuple[int, int, int]) -> float:
        def linear(channel: int) -> float:
            c = channel / 255
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

        r, g, b = map(linear, value)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def face_shades(svg_text: str) -> dict[str, tuple[int, int, int]]:
    """Each face color as drawn: the cube color under the face's shading overlay."""
    svg = ElementTree.fromstring(svg_text)
    base = rgb(svg.get("color"))
    faces = {path_data(points): face for face, points in cube_polygons().items()}
    shades = {face: base for face in faces.values()}
    for node in svg.iter(SVG + "path"):
        if node.get("opacity") and node.get("d") in faces:
            over, alpha = rgb(node.get("fill")), float(node.get("opacity"))
            face = faces[node.get("d")]
            shades[face] = tuple(round(b * (1 - alpha) + o * alpha) for b, o in zip(shades[face], over))
    return shades


def low_contrast_languages(entries: dict[str, dict[str, str]]) -> set[str]:
    low = set()
    for name, meta in entries.items():
        if meta["role"] in UNMARKED_ROLES:
            continue  # Layered roles have no white mark.
        color = COLORS[meta["language"]]
        svg = render_icon(meta["role"], color, name, meta["status"])
        mark = rgb(TREATMENTS[color]["mark"]) if color in TREATMENTS else WHITE  # Dark marks (issue #38).
        if min(contrast(mark, shade) for shade in face_shades(svg).values()) < THRESHOLD:
            low.add(meta["language"])
    return low


def thin_white_marks(glyph: str) -> list[float]:
    """Widths, in viewBox units, of white strokes and dots below ``MIN_WHITE_UNITS``.

    Fill, stroke and stroke width are inherited from enclosing groups, as in SVG.
    """
    widths: list[float] = []

    def walk(node: ElementTree.Element, style: dict[str, str]) -> None:
        style = {**style, **{key: node.get(key) for key in ("fill", "stroke", "stroke-width") if node.get(key)}}
        if node.tag in ("path", "circle") and style.get("stroke") == "#fff":
            widths.append(float(style.get("stroke-width", "1")))
        elif node.tag == "circle" and style.get("fill") == "#fff":
            widths.append(2 * float(node.get("r")))
        for child in node:
            walk(child, style)

    walk(ElementTree.fromstring(f"<g>{glyph}</g>"), {})
    return [width for width in widths if width < MIN_WHITE_UNITS]


class ContrastTests(unittest.TestCase):
    def test_contrast_formula(self):
        self.assertAlmostEqual(contrast(WHITE, (0, 0, 0)), 21.0, places=2)
        self.assertAlmostEqual(contrast(WHITE, rgb("#767676")), 4.54, places=2)

    def test_face_shades_follow_the_generator_overlays(self):
        shades = face_shades(render_icon("mcp", "#00ADD8", "check", "approved"))
        self.assertEqual(shades["right"], rgb("#00ADD8"))
        self.assertEqual(shades["top"], (20, 180, 219))  # 8% white
        self.assertEqual(shades["left"], (0, 156, 194))  # 10% black

    def test_only_reviewed_tokens_fall_below_three_to_one(self):
        self.assertEqual(low_contrast_languages({**REGISTRY, **SURFACES}), BELOW_THREE_TO_ONE)

    def test_a_new_low_contrast_token_is_flagged(self):
        entry = {"example": {"role": "mcp", "language": "javascript", "status": "approved"}}
        self.assertEqual(low_contrast_languages(entry), {"javascript"})
        # Cube layer grooves are visible marks, not unmarked silhouettes.
        for role in ("driver", "orm"):
            layered = {"example": {"role": role, "language": "javascript", "status": "approved"}}
            self.assertEqual(low_contrast_languages(layered), {"javascript"})


class StrokeWeightTests(unittest.TestCase):
    def test_white_marks_are_at_least_one_pixel_at_24_px(self):
        for role, glyph in GLYPHS.items():
            with self.subTest(role=role):
                self.assertEqual(thin_white_marks(glyph), [])

    def test_a_thin_white_stroke_is_flagged(self):
        glyph = '<path d="M 1 1 L 2 2" stroke="#fff" stroke-width="0.6"/><circle cx="1" cy="1" r="0.4" fill="#fff"/>'
        self.assertEqual(thin_white_marks(glyph), [0.6, 0.8])

    def test_inherited_white_is_checked(self):
        glyph = '<g fill="#fff"><circle cx="1" cy="1" r="0.4"/></g><g stroke="#fff" stroke-width="0.7"><path d="M 1 1 L 2 2"/></g>'
        self.assertEqual(thin_white_marks(glyph), [0.8, 0.7])


def glyph_points(role: str) -> list[list[tuple[float, float]]]:
    """The absolute x y vertices of each subpath of a single-path role mark."""
    d = ElementTree.fromstring(GLYPHS[role]).get("d")
    shapes = []
    for subpath in d.split("Z"):
        values = [float(n) for n in subpath.replace("M", " ").replace("L", " ").split()]
        if values:
            shapes.append(list(zip(values[0::2], values[1::2])))
    return shapes


class EnlargedMarkTests(unittest.TestCase):
    """The approved P2 enlargement (issue #21): Docs x1.25, Showcase x1.3."""

    def test_docs_bars_and_gaps_are_at_least_one_pixel_at_24_px(self):
        bars = glyph_points("docs")
        (x0, y0), (x1, y1) = bars[0][0], bars[0][1]
        cosine = abs(x1 - x0) / math.hypot(x1 - x0, y1 - y0)
        thickness = (bars[0][3][1] - bars[0][0][1]) * cosine
        gap = (bars[1][0][1] - bars[0][3][1]) * cosine
        self.assertAlmostEqual(thickness, 1.13 * 1.25, places=2)
        self.assertAlmostEqual(gap, 0.96 * 1.25, places=2)
        self.assertGreaterEqual(min(thickness, gap), MIN_WHITE_UNITS)

    def test_showcase_triangle_is_scaled_by_1_3(self):
        (triangle,) = glyph_points("showcase")
        xs, ys = [x for x, _ in triangle], [y for _, y in triangle]
        self.assertAlmostEqual(max(xs) - min(xs), 3.8 * 1.3, places=2)
        self.assertAlmostEqual(max(ys) - min(ys), 4.6 * 1.3, places=2)


if __name__ == "__main__":
    unittest.main()
