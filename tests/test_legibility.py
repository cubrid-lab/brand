"""Lightweight small-size legibility guards (issue #21).

Two objective checks, with no extra dependencies:

- Contrast: the WCAG 2 contrast ratio of the white role mark on every face shade
  the generator draws, for every language token used by a repository or surface
  icon that has a white mark. 3:1 is the WCAG 1.4.11 non-text threshold, used
  here as review guidance, not as a compliance claim. Tokens below it are listed
  in ``BELOW_THREE_TO_ONE`` and documented in
  ``docs/studies/small-size-legibility.md``; any new one fails until reviewed.
- Stroke weight: no white stroke or dot in a role mark is thinner than
  ``MIN_WHITE_UNITS`` viewBox units, i.e. one device pixel at 24 px.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build import COLORS, GLYPHS, REGISTRY, SURFACES, cube_polygons, path_data, render_icon

SVG = "{http://www.w3.org/2000/svg}"
WHITE = (255, 255, 255)
THRESHOLD = 3.0
# Reviewed in docs/studies/small-size-legibility.md; changing a token or the
# treatment needs maintainer design approval (issue #21).
BELOW_THREE_TO_ONE = {"go", "rust"}
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
        if meta["role"] == "orm":
            continue  # The ORM layers have no white mark.
        svg = render_icon(meta["role"], COLORS[meta["language"]], name, meta["status"])
        if min(contrast(WHITE, shade) for shade in face_shades(svg).values()) < THRESHOLD:
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
        shades = face_shades(render_icon("driver", "#00ADD8", "check", "approved"))
        self.assertEqual(shades["right"], rgb("#00ADD8"))
        self.assertEqual(shades["top"], (20, 180, 219))  # 8% white
        self.assertEqual(shades["left"], (0, 156, 194))  # 10% black

    def test_only_reviewed_tokens_fall_below_three_to_one(self):
        self.assertEqual(low_contrast_languages({**REGISTRY, **SURFACES}), BELOW_THREE_TO_ONE)

    def test_a_new_low_contrast_token_is_flagged(self):
        entry = {"example": {"role": "driver", "language": "javascript", "status": "approved"}}
        self.assertEqual(low_contrast_languages(entry), {"javascript"})
        orm = {"example": {"role": "orm", "language": "javascript", "status": "approved"}}
        self.assertEqual(low_contrast_languages(orm), set())


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


if __name__ == "__main__":
    unittest.main()
