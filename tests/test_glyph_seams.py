"""Geometric fidelity check: white role marks never touch the cube's transparent seams.

Each generated role template is sampled on a grid. Every sample takes the paint of
the topmost element covering it (white mark, cube color, or nothing), and no white
sample may lie within ``MARGIN`` of an unpainted sample inside the cube silhouette,
that is, a seam. On a light page a seam shows the page color, so a white mark there
would break apart or merge into the background (issue #23). Clearance from the
silhouette's outer edge is a separate composition question and is not checked.
"""
from __future__ import annotations

import math
import re
import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build import ROLES, cube_polygons, outputs

SVG = "{http://www.w3.org/2000/svg}"
STEP = 0.1
# Minimum cube-colored clearance between a white mark and a transparent seam.
MARGIN = 0.3
TOKEN_RE = re.compile(r"[MLHVQZ]|-?\d+(?:\.\d+)?")
Point = tuple[float, float]


def subpaths(d: str) -> list[list[Point]]:
    """Flatten the absolute M/L/H/V/Q/Z path data the generator emits."""
    tokens = TOKEN_RE.findall(d)
    result: list[list[Point]] = []
    index, command, x, y = 0, "", 0.0, 0.0

    def take() -> float:
        nonlocal index
        index += 1
        return float(tokens[index - 1])

    while index < len(tokens):
        if tokens[index].isalpha():
            command = tokens[index]
            index += 1
        if command == "M":
            x, y = take(), take()
            result.append([(x, y)])
            command = "L"
        elif command == "L":
            x, y = take(), take()
            result[-1].append((x, y))
        elif command == "H":
            x = take()
            result[-1].append((x, y))
        elif command == "V":
            y = take()
            result[-1].append((x, y))
        elif command == "Q":
            cx, cy, ex, ey = take(), take(), take(), take()
            for step in range(1, 17):
                t = step / 16
                result[-1].append(
                    ((1 - t) ** 2 * x + 2 * (1 - t) * t * cx + t * t * ex, (1 - t) ** 2 * y + 2 * (1 - t) * t * cy + t * t * ey)
                )
            x, y = ex, ey
        elif command == "Z":
            result[-1].append(result[-1][0])
            x, y = result[-1][0]
        else:
            raise ValueError(f"unsupported path command {command!r}")
    return result


def inside(point: Point, rings: list[list[Point]]) -> bool:
    px, py, crossings = point[0], point[1], 0
    for ring in rings:
        for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
            if (y1 > py) != (y2 > py) and px < x1 + (py - y1) * (x2 - x1) / (y2 - y1):
                crossings += 1
    return crossings % 2 == 1


def distance(point: Point, rings: list[list[Point]], butt: bool) -> float:
    """Distance to the stroked outline; ``butt`` caps add nothing past open ends.

    Joins and other caps are treated as round.
    """
    best = math.inf
    for ring in rings:
        open_ends = butt and ring[0] != ring[-1]
        if len(ring) == 1 and not butt:
            best = min(best, math.dist(point, ring[0]))
        last = len(ring) - 2
        for index, (a, b) in enumerate(zip(ring, ring[1:])):
            dx, dy = b[0] - a[0], b[1] - a[1]
            length = dx * dx + dy * dy
            t = 0.0 if length == 0 else ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / length
            if open_ends and ((index == 0 and t < 0) or (index == last and t > 1)):
                continue
            t = max(0.0, min(1.0, t))
            best = min(best, math.dist(point, (a[0] + t * dx, a[1] + t * dy)))
    return best


class Shape:
    def __init__(self, node: ElementTree.Element, style: dict[str, str], clip: list[list[Point]] | None):
        self.fill, self.stroke = style.get("fill", "black"), style.get("stroke", "none")
        self.half = float(style.get("stroke-width", "1")) / 2
        self.butt = style.get("stroke-linecap", "butt") == "butt"
        self.clip = clip
        if node.tag == SVG + "circle":
            self.circle = (float(node.get("cx")), float(node.get("cy")), float(node.get("r")))
            cx, cy, r = self.circle
            self.box = (cx - r - self.half, cy - r - self.half, cx + r + self.half, cy + r + self.half)
        else:
            self.circle = None
            self.rings = subpaths(node.get("d"))
            xs = [x for ring in self.rings for x, _ in ring]
            ys = [y for ring in self.rings for _, y in ring]
            self.box = (min(xs) - self.half, min(ys) - self.half, max(xs) + self.half, max(ys) + self.half)

    def paint(self, point: Point) -> str | None:
        x, y = point
        if not (self.box[0] <= x <= self.box[2] and self.box[1] <= y <= self.box[3]):
            return None
        if self.clip is not None and not inside(point, self.clip):
            return None
        if self.circle is not None:
            cx, cy, r = self.circle
            gap = math.dist(point, (cx, cy))
            in_fill, on_stroke = gap <= r, abs(gap - r) <= self.half
        else:
            in_fill = inside(point, self.rings)
            on_stroke = self.stroke != "none" and distance(point, self.rings, self.butt) <= self.half
        if on_stroke and self.stroke != "none":
            return self.stroke
        if in_fill and self.fill != "none":
            return self.fill
        return None


def shapes(svg: ElementTree.Element) -> list[Shape]:
    clips = {
        clip.get("id"): [ring for path in clip.iter(SVG + "path") for ring in subpaths(path.get("d"))]
        for clip in svg.iter(SVG + "clipPath")
    }
    result: list[Shape] = []

    def walk(node: ElementTree.Element, style: dict[str, str], clip: list[list[Point]] | None) -> None:
        if node.tag in (SVG + "clipPath", SVG + "title", SVG + "desc") or node.get("opacity"):
            return  # Shading overlays only tint the faces beneath them.
        style = {**style, **{key: node.get(key) for key in ("fill", "stroke", "stroke-width", "stroke-linecap") if node.get(key)}}
        reference = node.get("clip-path")
        if reference:
            clip = clips[reference.removeprefix("url(#").removesuffix(")")]
        if node.tag in (SVG + "path", SVG + "circle"):
            result.append(Shape(node, style, clip))
        for child in node:
            walk(child, style, clip)

    walk(svg, {}, None)
    return result


def silhouette() -> list[list[Point]]:
    """The cube's outline: the faces and the seams between them."""
    faces = cube_polygons()
    top, left, right = faces["top"], faces["left"], faces["right"]
    return [[top[0], top[1], right[2], right[3], left[2], left[3], top[3]]]


def seam_contacts(svg_text: str, outline: list[list[Point]] | None = None) -> list[Point]:
    """White samples with an unpainted sample inside ``outline`` within ``MARGIN``."""
    outline = silhouette() if outline is None else outline
    layers = shapes(ElementTree.fromstring(svg_text))
    size = round(24 / STEP)
    grid: dict[tuple[int, int], str] = {}
    for i in range(size + 1):
        for j in range(size + 1):
            point, top = (i * STEP, j * STEP), "clear"
            for shape in layers:
                top = shape.paint(point) or top
            if top == "#fff":
                grid[i, j] = "white"
            elif top == "clear":
                grid[i, j] = "seam" if inside(point, outline) else "outside"
            else:
                grid[i, j] = "color"
    reach = math.ceil(MARGIN / STEP)
    offsets = [(di, dj) for di in range(-reach, reach + 1) for dj in range(-reach, reach + 1) if math.hypot(di, dj) * STEP <= MARGIN]
    return [
        (i * STEP, j * STEP)
        for (i, j), paint in grid.items()
        if paint == "white" and any(grid.get((i + di, j + dj)) == "seam" for di, dj in offsets)
    ]


class GlyphSeamTests(unittest.TestCase):
    def test_role_marks_stay_clear_of_transparent_seams(self):
        generated = outputs()
        for role in ROLES:
            with self.subTest(role=role):
                contacts = seam_contacts(generated[ROOT / "src" / f"{role}.svg"])
                self.assertEqual(contacts[:5], [], f"{len(contacts)} white samples touch a transparent seam")

    def test_checker_detects_a_mark_on_a_seam(self):
        cube = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            '<path d="M 2 2 L 11 2 L 11 22 L 2 22 Z" fill="currentColor"/>'
            '<path d="M 13 2 L 22 2 L 22 22 L 13 22 Z" fill="currentColor"/>'
            "{mark}</svg>"
        )
        inside_face = '<circle cx="6" cy="12" r="1.5" fill="#fff"/>'
        across_seam = '<path d="M 6 12 H 18" fill="none" stroke="#fff" stroke-width="1.2"/>'
        # A butt-capped backing that ends flush with its butt-capped mark
        # leaves the mark's end on the seam; a round cap past the end does not.
        flush = (
            '<path d="M 6 16 V 6" stroke="currentColor" stroke-width="2.3"/>'
            '<path d="M 6 16 V 6" stroke="#fff" stroke-width="1.2"/>'
        )
        cube_with_gap = cube.replace("M 2 2 L 11 2", "M 2 12 L 11 12")
        outline = [[(2, 2), (22, 2), (22, 22), (2, 22)]]
        self.assertEqual(seam_contacts(cube.format(mark=inside_face), outline), [])
        self.assertTrue(seam_contacts(cube.format(mark=across_seam), outline))
        self.assertTrue(seam_contacts(cube_with_gap.format(mark=flush), outline))
        rounded = flush.replace('stroke-width="2.3"', 'stroke-width="2.3" stroke-linecap="round"')
        self.assertEqual(seam_contacts(cube_with_gap.format(mark=rounded), outline), [])


if __name__ == "__main__":
    unittest.main()
