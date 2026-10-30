"""Build CUBRID Lab role icons and organization identity from numeric tokens."""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from xml.etree import ElementTree
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
GEOMETRY = json.loads((ROOT / "tokens/geometry.json").read_text(encoding="utf-8"))
COLOR_TOKENS = json.loads((ROOT / "tokens/colors.json").read_text(encoding="utf-8"))
COLORS = COLOR_TOKENS["languages"]
# Contrast treatments for light language tokens, keyed by the token color (issue #38).
TREATMENTS = {COLORS[language]: spec for language, spec in COLOR_TOKENS.get("treatments", {}).items()}
ORGANIZATION = json.loads((ROOT / "tokens/organization.json").read_text(encoding="utf-8"))
ROLE_CANDIDATES = json.loads((ROOT / "tokens/role-candidates.json").read_text(encoding="utf-8"))["candidates"]
YELLOW_CANDIDATES = json.loads((ROOT / "tokens/python-yellow-candidates.json").read_text(encoding="utf-8"))
REGISTRY_DATA = json.loads((ROOT / "registry/repositories.json").read_text(encoding="utf-8"))
REGISTRY = REGISTRY_DATA["repositories"]
SURFACES = REGISTRY_DATA["surfaces"]
OUT = ROOT / "dist/icons"
STUDY_OUT = ROOT / "studies/icons"
ROLES = ("driver", "orm", "mcp", "cookbook", "benchmark", "operator", "showcase", "docs", "community")
COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
KEY_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def number(value: float) -> str:
    return f"{value:.{GEOMETRY['decimal_places']}f}".rstrip("0").rstrip(".")


def path_data(points: list[tuple[float, float]]) -> str:
    return "M " + " L ".join(f"{number(x)} {number(y)}" for x, y in points) + " Z"


def cube_polygons() -> dict[str, list[tuple[float, float]]]:
    """An isometric top and two inset faces, with visible white seams."""
    cx = GEOMETRY["center"][0]
    half = GEOMETRY["half_width"]
    rise = GEOMETRY["roof_rise"]
    top_y = GEOMETRY["top_y"]
    outer_top = GEOMETRY["face_outer_top_y"]
    center_top = GEOMETRY["face_center_top_y"]
    outer_bottom = GEOMETRY["face_outer_bottom_y"]
    center_bottom = GEOMETRY["face_center_bottom_y"]
    seam = GEOMETRY["seam_half_width"]
    return {
        "top": [(cx, top_y), (cx + half, top_y + rise), (cx, top_y + 2 * rise), (cx - half, top_y + rise)],
        "left": [(cx - half, outer_top), (cx - seam, center_top), (cx - seam, center_bottom), (cx - half, outer_bottom)],
        "right": [(cx + seam, center_top), (cx + half, outer_top), (cx + half, outer_bottom), (cx + seam, center_bottom)],
    }


def cube_outline() -> list[tuple[float, float]]:
    """The cube's outer silhouette, which bounds every role mark."""
    polygons = cube_polygons()
    top, left, right = polygons["top"], polygons["left"], polygons["right"]
    return [top[0], top[1], right[2], right[3], left[2], left[3], top[3]]


def emblem_edges() -> list[list[tuple[float, float]]]:
    """Each face's outer edges, stopping at the seams as the organization emblem does (issue #50)."""
    polygons = cube_polygons()
    top, left, right = polygons["top"], polygons["left"], polygons["right"]
    return [[top[3], top[0], top[1]], [left[0], left[3], left[2]], [right[1], right[2], right[3]]]


def glyph_backing(role: str, glyph: str | None = None) -> str:
    """A solid plate in the cube color: the role mark, filled and widened by ``glyph_backing_pad``.

    It is drawn under the face shading, so it is invisible on the faces and only
    bridges the transparent seams where the white mark crosses or encloses them.
    """
    pad = GEOMETRY["glyph_backing_pad"]
    group = ElementTree.fromstring(f"<g>{GLYPHS[role] if glyph is None else glyph}</g>")
    for node in group.iter():
        stroked = node.get("stroke") == "#fff"
        if not stroked and node.get("fill") != "#fff":
            continue
        width = float(node.get("stroke-width")) if stroked else 0.0
        node.set("fill", "currentColor")
        node.set("stroke", "currentColor")
        node.set("stroke-width", number(width + 2 * pad))
        node.set("stroke-linejoin", "round")
    lines = []
    for child in group:
        child.tail = None
        lines.append("    " + ElementTree.tostring(child, encoding="unicode").replace(" />", "/>"))
    return "\n".join(lines)


def cube_faces(role: str, key: str, glyph: str | None = None) -> str:
    default_mark = glyph is None
    glyph = KNOCKOUT_MARKS.get(role, GLYPHS[role]) if glyph is None else glyph
    polygons = cube_polygons()
    clip = f"{key}-cube"
    lines = [f'  <clipPath id="{clip}"><path d="{path_data(cube_outline())}"/></clipPath>']
    lines += [f'  <path d="{path_data(polygons[face])}" fill="currentColor"/>' for face in ("top", "left", "right")]
    lines.append(f'  <g clip-path="url(#{clip})">\n{glyph_backing(role, glyph)}\n  </g>')
    lines.append(f'  <path d="{path_data(polygons["top"])}" fill="#fff" opacity="0.08"/>')
    lines.append(f'  <path d="{path_data(polygons["left"])}" fill="#000" opacity="0.10"/>')
    if role in KNOCKOUT_ROLES and default_mark:
        # The white mark becomes real alpha transparency (issues #59 and #58): the whole
        # painted cube is masked by the mark, so the background shows through.
        mask = f"{key}-knockout"
        cutout = glyph.replace('"#fff"', '"#000"')
        lines = [lines[0]] + [
            f'  <mask id="{mask}" maskUnits="userSpaceOnUse" x="0" y="0" width="24" height="24">',
            '    <rect width="24" height="24" fill="#fff"/>',
            f'    <g clip-path="url(#{clip})">\n{cutout}\n    </g>',
            "  </mask>",
            f'  <g mask="url(#{mask})">',
        ] + ["  " + line for line in lines[1:]] + ["  </g>"]
        return "\n".join(lines)
    lines.append(f'  <g clip-path="url(#{clip})">\n{glyph}\n  </g>')
    return "\n".join(lines)


# Roles whose mark is knocked out to transparency instead of painted white.
KNOCKOUT_ROLES = {"operator", "mcp", "cookbook"}
# Where the knocked-out mark differs from the white mark (issue #57): the open book
# keeps only its two pages, without the text lines, and they are cut out.
KNOCKOUT_MARKS = {
    "cookbook": '''  <path d="M 5.6 13.3 Q 8.6 12.8 10.7 14.5 L 10.7 20.0 Q 8.6 18.3 5.6 18.8 Z M 18.4 13.3 Q 15.4 12.8 13.3 14.5 L 13.3 20.0 Q 15.4 18.3 18.4 18.8 Z" fill="#fff"/>''',
}

# White marks are original geometric drawings. In particular, Operator is a
# generic six-spoke control dial, not a Kubernetes or other third-party logo.
GLYPHS = {
    # MCP "3-Way Router" (issue #23): a hub at the cube's center vertex sends one
    # link into each face. Selected on 2026-10-25 from studies/roles/.
    "mcp": '''  <path d="M 12 12.95 L 12 7.1 M 12 12.95 L 6.7 15.45 M 12 12.95 L 17.3 15.45" fill="none" stroke="#fff" stroke-width="1.3" stroke-linecap="round"/>
  <g fill="#fff"><circle cx="12" cy="12.95" r="1.75"/><circle cx="12" cy="6.9" r="1.45"/><circle cx="6.5" cy="15.55" r="1.45"/><circle cx="17.5" cy="15.55" r="1.45"/></g>''',
    "cookbook": '''  <path d="M 5.6 13.3 Q 8.6 12.8 10.7 14.5 L 10.7 20.0 Q 8.6 18.3 5.6 18.8 Z M 18.4 13.3 Q 15.4 12.8 13.3 14.5 L 13.3 20.0 Q 15.4 18.3 18.4 18.8 Z" fill="#fff"/>
  <path d="M 6.9 15.5 Q 8.6 15.4 9.6 16.1 M 6.9 17.0 Q 8.6 16.9 9.6 17.6 M 17.1 15.5 Q 15.4 15.4 14.4 16.1 M 17.1 17.0 Q 15.4 16.9 14.4 17.6" fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round"/>''',
    "benchmark": '''  <path d="M 5.5 15.2 H 8.4 V 19.1 H 5.5 Z M 10.5 12.7 H 13.4 V 19.1 H 10.5 Z M 15.5 9.9 H 18.4 V 19.1 H 15.5 Z" fill="#fff"/>''',
    "operator": '''  <circle cx="12" cy="13.15" r="4.25" fill="none" stroke="#fff" stroke-width="1.25"/>
  <circle cx="12" cy="13.15" r="1.2" fill="none" stroke="#fff" stroke-width="1.1"/>
  <path d="M 12 7.95 V 11.85 M 12 14.45 V 23 M 1 6.81 L 10.9 12.55 M 13.1 13.75 L 16.5 15.75 M 7.5 15.75 L 10.9 13.75 M 13.1 12.55 L 23 6.81" fill="none" stroke="#fff" stroke-width="1.25" stroke-linecap="round"/>''',
    # Showcase and Docs are enlarged about their own centers (x1.3 and x1.25) so
    # the triangle and the bars stay legible at 16 and 24 px. This is the approved
    # enlargement alternative in docs/studies/small-size-legibility.md; the declined
    # alternative was a darker keyline (issue #21, study proposals P2 and P1).
    "showcase": '''  <path d="M 15.63 13.11 L 20.57 16.1 L 15.63 19.09 Z" fill="#fff"/>''',
    "docs": '''  <path d="M 14.375 13.188 L 20.625 9.688 L 20.625 11.312 L 14.375 14.812 Z M 14.375 16.188 L 20.625 12.688 L 20.625 14.312 L 14.375 17.812 Z M 14.375 19.188 L 20.625 15.688 L 20.625 17.312 L 14.375 20.812 Z" fill="#fff"/>''',
    "community": '''  <g fill="#fff"><circle cx="7" cy="14.2" r="1.2"/><circle cx="12" cy="12.8" r="1.25"/><circle cx="17" cy="14.2" r="1.2"/>
    <path d="M 4.6 17.5 Q 4.6 15.6 7 15.6 Q 9.4 15.6 9.4 17.5 V 19 L 4.6 18.2 Z M 9.5 16.2 Q 9.5 14.4 12 14.4 Q 14.5 14.4 14.5 16.2 V 19.8 L 12 21.2 L 9.5 19.8 Z M 14.6 17.5 Q 14.6 15.6 17 15.6 Q 19.4 15.6 19.4 17.5 V 18.2 L 14.6 19 Z"/></g>''',
}


def vertical_stack_legacy() -> str:
    """Preserve the reviewed #30 floating-stack drawing in historical study assets."""
    top = path_data(cube_polygons()["top"])
    layers = (
        "M 2 10.1 L 12 15.6 L 22 10.1 L 22 12.15 L 12 17.65 L 2 12.15 Z",
        "M 2 14.3 L 12 19.8 L 22 14.3 L 22 16.35 L 12 21.85 L 2 16.35 Z",
    )
    return "\n".join([f'  <path d="{top}" fill="currentColor"/>'] + [f'  <path d="{layer}" fill="currentColor"/>' for layer in layers])


def cube_layers(role: str, key: str) -> str:
    """Keep all three faces of the cube; cut two equal transparent gaps by role (issue #57).

    Driver gaps follow the horizontal edges of the side faces and meet at the
    center seam; the top stays solid. ORM gaps cross the top and continue
    vertically down the right face; the left face stays solid. Gap widths come
    from the shared ``layer_gap`` token and every cut is square-ended, running
    out to the face boundary. The cube is drawn inside a mask whose cutout is
    the gaps, so they are real alpha transparency.
    """
    if role not in {"driver", "orm"}:
        raise ValueError("cube layers are only defined for Driver and ORM")
    faces = cube_polygons()
    gap = GEOMETRY["layer_gap"]
    mask, cuts, clips = f"{key}-layers", [], []

    def edge_y(face: str, x: float) -> float:
        (x0, y0), (x1, y1) = (faces[face][0], faces[face][1]) if face == "left" else (faces[face][1], faces[face][0])
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

    if role == "driver":
        height = faces["left"][3][1] - faces["left"][0][1]
        layer = (height - 2 * gap) / 3
        span = {"left": (0.0, faces["left"][1][0]), "right": (faces["right"][0][0], 24.0)}
        for index in (1, 2):
            start = index * layer + (index - 1) * gap
            for face, (x0, x1) in span.items():
                quad = [(x0, edge_y(face, x0) + start), (x1, edge_y(face, x1) + start),
                        (x1, edge_y(face, x1) + start + gap), (x0, edge_y(face, x0) + start + gap)]
                cuts.append(f'    <path d="{path_data(quad)}" fill="#000"/>')
    else:
        # Three plates along the top's right axis; a gap of horizontal width ``gap``
        # is the same strip on the top (constant u) and on the right face (constant x).
        du = gap / GEOMETRY["half_width"]
        plate = (1 - 2 * du) / 3
        clips = [f'  <clipPath id="{mask}-top"><path d="{path_data(faces["top"])}"/></clipPath>',
                 f'  <clipPath id="{mask}-right"><path d="{path_data(faces["right"])}"/></clipPath>']
        cx, half = GEOMETRY["center"][0], GEOMETRY["half_width"]
        for index in (1, 2):
            a = index * plate + (index - 1) * du
            b = a + du
            strip = [top_point(a, -0.2), top_point(b, -0.2), top_point(b, 1.2), top_point(a, 1.2)]
            x0, x1 = cx + half * a, cx + half * b
            cuts.append(f'    <path d="{path_data(strip)}" fill="#000" clip-path="url(#{mask}-top)"/>')
            cuts.append(f'    <path d="M {number(x0)} 0 H {number(x1)} V 24 H {number(x0)} Z" fill="#000" clip-path="url(#{mask}-right)"/>')
    lines = clips + [
        f'  <mask id="{mask}" maskUnits="userSpaceOnUse" x="0" y="0" width="24" height="24">',
        '    <rect width="24" height="24" fill="#fff"/>',
        *cuts,
        "  </mask>",
        f'  <g mask="url(#{mask})">',
        *[f'    <path d="{path_data(faces[face])}" fill="currentColor"/>' for face in ("top", "left", "right")],
        f'    <path d="{path_data(faces["top"])}" fill="#fff" opacity="0.08"/>',
        f'    <path d="{path_data(faces["left"])}" fill="#000" opacity="0.10"/>',
        "  </g>",
    ]
    return "\n".join(lines)


def vertical_stack(key: str) -> str:
    return cube_layers("driver", key)


def lateral_plates(key: str) -> str:
    return cube_layers("orm", key)


FILL_D_RE = re.compile(r'<path d="([^"]+)" fill="currentColor"/>')


def light_treatment(
    role: str, key: str, shape: str, mark: str | None, keyline: str | None, width: float, open_seams: bool = False
) -> str:
    """Recolor the role mark to ``mark`` and add a ``keyline`` of ``width`` outside the shape.

    Used for light language tokens (issue #38); ``None`` leaves that part unchanged.
    ``open_seams`` draws the keyline along each face's outer edges only, so the
    seams stay open like the organization emblem (issue #50). The #38 studies keep
    the original closed outline.
    """
    if any(value is not None and not COLOR_RE.fullmatch(value) for value in (mark, keyline)):
        raise ValueError("invalid treatment color")
    layered = role in {"driver", "orm"}
    grooved_cube = layered and 'data-layer-grooves=' in shape
    if mark is not None and (not layered or grooved_cube):
        # Recolor only the visible role mark, never the cube or its face shades.
        split = shape.rindex('  <g data-layer-grooves=') if grooved_cube else shape.rindex("<g clip-path")
        shape = shape[:split] + shape[split:].replace('"#fff"', f'"{mark}"')
    if keyline is None:
        return shape
    stroke = f'fill="none" stroke="{keyline}" stroke-width="{number(2 * width)}" stroke-linejoin="round"'
    if layered and not grooved_cube:
        # Historical #30 study: strokes belong under each detached layer.
        lines = [f'  <path d="{d}" {stroke}/>' for d in FILL_D_RE.findall(shape)]
    elif open_seams:
        # Clip to outside every face, so only the outer half shows and no seam is bridged.
        clip = f"{key}-outside"
        faces = " ".join(path_data(points) for points in cube_polygons().values())
        edges = " ".join(path_data(points).removesuffix(" Z") for points in emblem_edges())
        lines = [
            f'  <clipPath id="{clip}"><path d="M 0 0 H 24 V 24 H 0 Z {faces}" clip-rule="evenodd"/></clipPath>',
            f'  <path d="{edges}" {stroke} clip-path="url(#{clip})"/>',
        ]
    else:
        # A single outline leaves the new cube intact; grooves remain inside it.
        clip, outline = f"{key}-outside", path_data(cube_outline())
        lines = [
            f'  <clipPath id="{clip}"><path d="M 0 0 H 24 V 24 H 0 Z {outline}" clip-rule="evenodd"/></clipPath>',
            f'  <path d="{outline}" {stroke} clip-path="url(#{clip})"/>',
        ]
    return "\n".join(lines) + "\n" + shape


def render_icon(role: str, color: str, key: str, status: str = "pending-symbol") -> str:
    if role not in ROLES or not KEY_RE.fullmatch(key):
        raise ValueError("invalid role or identifier")
    if status not in {"approved", "pending-symbol"}:
        raise ValueError("invalid review status")
    if color != "currentColor" and not COLOR_RE.fullmatch(color):
        raise ValueError("invalid color")
    color_attr = "" if color == "currentColor" else f' color="{color}"'
    shape = {"driver": lambda: vertical_stack(key), "orm": lambda: lateral_plates(key)}.get(role, lambda: cube_faces(role, key))()
    if color in TREATMENTS:
        spec = TREATMENTS[color]
        shape = light_treatment(role, key, shape, spec["mark"], spec["keyline"], spec["keyline_width"], open_seams=True)
    review_note = (
        "Design selected; legal clearance pending."
        if status == "approved"
        else "Symbol candidate; design and legal review pending."
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"{color_attr} role="img" aria-labelledby="{key}-title {key}-desc">\n'
        f'  <title id="{key}-title">CUBRID Lab {role} icon — {key}</title>\n'
        f'  <desc id="{key}-desc">Cube-based {role} role symbol. {review_note}</desc>\n'
        f'{shape}\n'
        '</svg>\n'
    )


# Role candidates reviewed for issue #30 (Driver vertical stack, ORM lateral
# stacks) and the MCP "3-Way Router" direction from issue #23. They stay in
# studies/roles/ as the review record; the selected ones (see
# tokens/role-candidates.json) share their drawing functions with src/ and dist/.
TOP_SHADE = '  <path d="{d}" fill="#fff" opacity="0.08"/>'
LEFT_SHADE = '  <path d="{d}" fill="#000" opacity="0.10"/>'


def top_point(u: float, v: float) -> tuple[float, float]:
    """A point on the top rhombus: ``u`` runs toward the right corner, ``v`` toward the left."""
    cx, half, rise, top_y = GEOMETRY["center"][0], GEOMETRY["half_width"], GEOMETRY["roof_rise"], GEOMETRY["top_y"]
    return (cx + half * (u - v), top_y + 2 * rise - rise * (u + v))


def right_face_y(x: float, edge: str) -> float:
    """The y of the right face's top or bottom edge at ``x``."""
    face = cube_polygons()["right"]
    (x0, y0), (x1, y1) = (face[0], face[1]) if edge == "top" else (face[3], face[2])
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def shaded(pieces: list[tuple[str, list[tuple[float, float]]]]) -> str:
    """Flat pieces in the cube color, with the cube's top and left face shading."""
    lines = [f'  <path d="{path_data(points)}" fill="currentColor"/>' for _, points in pieces]
    lines += [TOP_SHADE.format(d=path_data(points)) for plane, points in pieces if plane == "top"]
    lines += [LEFT_SHADE.format(d=path_data(points)) for plane, points in pieces if plane == "left"]
    return "\n".join(lines)


def lateral_slabs() -> str:
    """Three slabs side by side along the right axis; the front slab keeps the left face."""
    cx, half, seam = GEOMETRY["center"][0], GEOMETRY["half_width"], GEOMETRY["seam_half_width"]
    gap = 2 * seam
    width = (half - 2 * gap) / 3
    pieces = [("left", cube_polygons()["left"])]
    for index in range(3):
        a = index * (width + gap) / half
        b = a + width / half
        pieces.append(("top", [top_point(a, 0), top_point(b, 0), top_point(b, 1), top_point(a, 1)]))
        x0, x1 = max(cx + half * a, cx + seam), cx + half * b
        pieces.append(("right", [(x0, right_face_y(x0, "top")), (x1, right_face_y(x1, "top")), (x1, right_face_y(x1, "bottom")), (x0, right_face_y(x0, "bottom"))]))
    return shaded(pieces)


def mirrored_rows() -> str:
    """Two half-stacks split at the center seam, with three facing layers on each side."""
    cx, half, rise, top_y, seam = (GEOMETRY[key] for key in ("center", "half_width", "roof_rise", "top_y", "seam_half_width"))
    cx = cx[0]
    slope = rise / half
    pieces = [
        ("top", [(cx - half, top_y + rise), (cx - seam, top_y + seam * slope), (cx - seam, top_y + 2 * rise - seam * slope)]),
        ("top", [(cx + seam, top_y + seam * slope), (cx + half, top_y + rise), (cx + seam, top_y + 2 * rise - seam * slope)]),
    ]
    left, right = cube_polygons()["left"], cube_polygons()["right"]
    height = left[3][1] - left[0][1]
    gap = 1.0
    band = (height - 2 * gap) / 3
    for index in range(3):
        d0 = index * (band + gap)
        d1 = d0 + band
        pieces.append(("left", [(left[0][0], left[0][1] + d0), (left[1][0], left[1][1] + d0), (left[1][0], left[1][1] + d1), (left[0][0], left[0][1] + d1)]))
        pieces.append(("right", [(right[0][0], right[0][1] + d0), (right[1][0], right[1][1] + d0), (right[1][0], right[1][1] + d1), (right[0][0], right[0][1] + d1)]))
    return shaded(pieces)


def lateral_plates_legacy() -> str:
    """Keep the original lateral plates for the #30 review record."""
    cx, half = GEOMETRY["center"][0], GEOMETRY["half_width"]
    lines = [f'  <path d="{path_data(cube_polygons()["left"])}" fill="currentColor"/>']
    for x0, x1 in ((cx + 2.0, cx + 5.0), (cx + 7.0, cx + half)):
        a, b = (x0 - cx) / half, (x1 - cx) / half
        points = [top_point(a, 1), top_point(a, 0), (x0, right_face_y(x0, "bottom")), (x1, right_face_y(x1, "bottom")), top_point(b, 0), top_point(b, 1)]
        lines.append(f'  <path d="{path_data(points)}" fill="currentColor"/>')
    return "\n".join(lines)


ROUTER_HUB = (12.0, 12.95)
# The selected 3-Way Router rendition is the promoted MCP mark.
ROUTER_GLYPH = GLYPHS["mcp"]


def router_channels(key: str) -> str:
    """3-Way Router in negative space: the three seams run into a ring around a solid hub."""
    hx, hy = ROUTER_HUB
    outer, inner, sides = 2.9, 1.8, 48
    ring = [(hx + outer * math.cos(2 * math.pi * i / sides), hy + outer * math.sin(2 * math.pi * i / sides)) for i in range(sides)]
    clip = f"{key}-router"
    faces = cube_polygons()
    body = [f'  <path d="{path_data(faces[face])}" fill="currentColor"/>' for face in ("top", "left", "right")]
    body += [TOP_SHADE.format(d=path_data(faces["top"])), LEFT_SHADE.format(d=path_data(faces["left"]))]
    return "\n".join(
        [f'  <clipPath id="{clip}"><path d="M 0 0 H 24 V 24 H 0 Z {path_data(ring)}" clip-rule="evenodd"/></clipPath>',
         f'  <g clip-path="url(#{clip})">', *body, "  </g>",
         f'  <circle cx="{number(hx)}" cy="{number(hy)}" r="{number(inner)}" fill="currentColor"/>']
    )


def render_role_candidate(candidate_id: str, language: str) -> str:
    spec = ROLE_CANDIDATES.get(candidate_id)
    if spec is None or not KEY_RE.fullmatch(candidate_id) or spec.get("status") != "study":
        raise ValueError("role candidates must be registered study-only entries")
    if spec["role"] not in ROLES or language not in spec["languages"] or language not in COLORS:
        raise ValueError("invalid role candidate role or language")
    key = f"{candidate_id}-{language}"
    shapes = {
        "driver-vertical-stack": vertical_stack_legacy,
        "orm-lateral-slabs": lateral_slabs,
        "orm-mirrored-rows": mirrored_rows,
        "orm-lateral-plates": lateral_plates_legacy,
        "mcp-router-hub": lambda: cube_faces("mcp", key, ROUTER_GLYPH),
        "mcp-router-channels": lambda: router_channels(key),
    }
    if candidate_id not in shapes:
        raise ValueError(f"unsupported role candidate: {candidate_id}")
    shape = shapes[candidate_id]()
    if spec["selection"] == "selected" and COLORS[language] in TREATMENTS:
        # A selected candidate keeps drawing exactly its promoted icon (issue #38).
        treatment = TREATMENTS[COLORS[language]]
        shape = light_treatment(spec["role"], key, shape, treatment["mark"], treatment["keyline"], treatment["keyline_width"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" color="{COLORS[language]}" role="img" aria-labelledby="{key}-title {key}-desc">\n'
        f'  <title id="{key}-title">CUBRID Lab {spec["role"]} role study — {candidate_id} ({language})</title>\n'
        f'  <desc id="{key}-desc">{escape(spec["description"])} Study candidate for review; not approved.</desc>\n'
        f'{shape}\n'
        '</svg>\n'
    )


def role_candidate_files() -> dict[Path, tuple[str, str]]:
    return {
        ROOT / "studies/roles" / f"{candidate_id}-{language}.svg": (candidate_id, language)
        for candidate_id in sorted(ROLE_CANDIDATES)
        for language in ROLE_CANDIDATES[candidate_id]["languages"]
    }


# Contrast treatments for the Python Yellow decision (issue #38). Study-only:
# they render the approved Python icons in the candidate color with a dark or
# ochre mark and an optional outer keyline, into studies/python-yellow/.


def render_yellow_candidate(treatment: str, name: str) -> str:
    spec = YELLOW_CANDIDATES["treatments"].get(treatment)
    if spec is None or not KEY_RE.fullmatch(treatment) or spec.get("status") != "study":
        raise ValueError("yellow candidates must be registered study-only entries")
    if name not in YELLOW_CANDIDATES["repositories"] or REGISTRY[name]["language"] != "python":
        raise ValueError("yellow candidates cover the Python repository icons only")
    inks = {key: ink["value"] for key, ink in YELLOW_CANDIDATES["inks"].items()}
    color = YELLOW_CANDIDATES["color"]
    if any(not COLOR_RE.fullmatch(value) for value in [color, *inks.values()]):
        raise ValueError("invalid yellow candidate color")
    role, key = REGISTRY[name]["role"], f"{treatment}-{name}"
    # The Yellow #38 comparison predates cube restoration; keep its study intact.
    shape = {"driver": vertical_stack_legacy, "orm": lateral_plates_legacy}.get(role, lambda: cube_faces(role, key, GLYPHS[role]))()
    mark = None if spec["mark"] == "white" else inks[spec["mark"]]
    keyline = inks[spec["keyline"]] if spec["keyline"] and role in spec["keyline_roles"] else None
    shape = light_treatment(role, key, shape, mark, keyline, YELLOW_CANDIDATES["keyline_width"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" color="{color}" role="img" aria-labelledby="{key}-title {key}-desc">\n'
        f'  <title id="{key}-title">CUBRID Lab {role} icon color study — {name} ({treatment})</title>\n'
        f'  <desc id="{key}-desc">{escape(spec["description"])} Study candidate for review; not approved.</desc>\n'
        f'{shape}\n'
        '</svg>\n'
    )


def yellow_candidate_files() -> dict[Path, tuple[str, str]]:
    return {
        ROOT / "studies/python-yellow" / f"{treatment}-{name}.svg": (treatment, name)
        for treatment in sorted(YELLOW_CANDIDATES["treatments"])
        for name in YELLOW_CANDIDATES["repositories"]
    }


def organization_faces(face_colors: dict[str, str] | None = None) -> str:
    faces = cube_polygons()
    colors = ORGANIZATION["face_colors"] if face_colors is None else face_colors
    if any(not COLOR_RE.fullmatch(value) for value in colors.values()):
        raise ValueError("invalid organization color")
    return "\n".join(f'  <path d="{path_data(faces[face])}" fill="{colors[face]}"/>' for face in ("top", "left", "right"))


def render_organization_candidate(candidate_id: str) -> str:
    candidates = ORGANIZATION.get("candidates", {})
    if candidate_id not in candidates or not KEY_RE.fullmatch(candidate_id):
        raise ValueError("invalid organization candidate")
    spec = candidates[candidate_id]
    if spec.get("status") != "study":
        raise ValueError("organization candidates must remain study-only")
    if candidate_id == "monochrome-cube":
        body = organization_faces(spec["face_colors"])
        desc = "Monochrome slate cube candidate without role glyph; design and rights review pending."
    elif candidate_id == "hex-frame":
        scale = float(spec["inset_scale"])
        if not (0.2 < scale < 0.85):
            raise ValueError("invalid candidate inset scale")
        cx = GEOMETRY["center"][0]
        cy = GEOMETRY["top_y"] + 2 * GEOMETRY["roof_rise"]
        faces = cube_polygons()
        colors = ORGANIZATION["face_colors"]
        lines = []
        for face in ("top", "left", "right"):
            outer = path_data(faces[face])
            inner = path_data([(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in reversed(faces[face])])
            lines.append(f'  <path d="{outer} {inner}" fill="{colors[face]}" fill-rule="evenodd"/>')
        body = "\n".join(lines)
        desc = "Open hexagonal frame candidate without role glyph; design and rights review pending."
    else:
        raise ValueError(f"unsupported organization candidate: {candidate_id}")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img" aria-labelledby="candidate-{candidate_id}-title candidate-{candidate_id}-desc">\n'
        f'  <title id="candidate-{candidate_id}-title">CUBRID Lab organization mark study — {candidate_id}</title>\n'
        f'  <desc id="candidate-{candidate_id}-desc">{desc}</desc>\n'
        f'{body}\n'
        '</svg>\n'
    )


def organization_emblem_approved() -> bool:
    approval = ORGANIZATION["emblem"]
    statuses = (approval["design_status"], approval["organization_use_rights_status"])
    if any(status not in {"approved", "pending"} for status in statuses):
        raise ValueError("invalid organization approval status")
    return all(status == "approved" for status in statuses)


def render_organization_mark() -> str:
    approved = organization_emblem_approved()
    title = "CUBRID Lab organization emblem" + ("" if approved else " study")
    description = (
        "Three-color cube. Design and CUBRID Lab organization avatar/profile use approved; "
        "general redistribution license and legal clearance pending."
        if approved
        else "Three-color cube concept; design and rights review pending."
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img" aria-labelledby="org-title org-desc">\n'
        f'  <title id="org-title">{title}</title>\n'
        f'  <desc id="org-desc">{description}</desc>\n'
        f'{organization_faces()}\n'
        '</svg>\n'
    )


LOCKUP_LAYOUTS = ("horizontal", "stacked")


def organization_wordmarks_approved() -> bool:
    approval = ORGANIZATION["wordmarks"]
    statuses = (approval["design_status"], approval["organization_use_rights_status"])
    if any(status not in {"approved", "pending"} for status in statuses):
        raise ValueError("invalid organization wordmark approval status")
    return all(status == "approved" for status in statuses)


def lockup_name(layout: str, variant: str) -> str:
    """``lockup-<layout>.svg`` for light backgrounds, ``lockup-<layout>-<variant>.svg`` otherwise."""
    return f"lockup-{layout}.svg" if variant == "light" else f"lockup-{layout}-{variant}.svg"


def render_organization_lockup(layout: str, variant: str = "light") -> str:
    wordmarks = ORGANIZATION["wordmarks"]
    if variant not in wordmarks["variants"] or not KEY_RE.fullmatch(variant):
        raise ValueError("invalid lockup variant")
    colors = wordmarks["variants"][variant]
    if any(not COLOR_RE.fullmatch(colors[part]) for part in ("title", "tagline")):
        raise ValueError("invalid lockup text color")
    tagline_text = escape(wordmarks["tagline"])
    if layout == "horizontal":
        view_box, transform = "0 0 300 64", "translate(4 4) scale(2.25)"
        title = f'<text x="68" y="38" font-family="Arial, Helvetica, sans-serif" font-size="29" font-weight="700" fill="{colors["title"]}">CUBRID Lab</text>'
        tagline = f'<text x="69" y="54" font-family="Arial, Helvetica, sans-serif" font-size="8.4" letter-spacing="1" fill="{colors["tagline"]}">{tagline_text}</text>'
    elif layout == "stacked":
        view_box, transform = "0 0 200 154", "translate(64 5) scale(3)"
        title = f'<text x="100" y="117" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="25" font-weight="700" fill="{colors["title"]}">CUBRID Lab</text>'
        tagline = f'<text x="100" y="135" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="7.3" letter-spacing="0.55" fill="{colors["tagline"]}">{tagline_text}</text>'
    else:
        raise ValueError("invalid lockup layout")
    background = "" if variant == "light" else f" for {variant} backgrounds"
    if organization_wordmarks_approved():
        label = f"CUBRID Lab {layout} organization lockup{background}"
        description = (
            "Three-color emblem with the CUBRID Lab wordmark and tagline. Design and CUBRID Lab "
            "own-organization use approved; general redistribution license and legal clearance pending."
        )
    else:
        label = f"CUBRID Lab {layout} organization lockup study{background}"
        description = "Organization identity candidate; design and rights review pending."
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" role="img" aria-labelledby="lockup-title lockup-desc">\n'
        f'  <title id="lockup-title">{label}</title>\n'
        f'  <desc id="lockup-desc">{description}</desc>\n'
        f'  <g transform="{transform}">\n{organization_faces()}\n  </g>\n'
        f'  {title}\n  {tagline}\n'
        '</svg>\n'
    )


def outputs() -> dict[Path, str]:
    if set(REGISTRY) & set(SURFACES):
        raise ValueError("repository and surface names must be distinct")
    expected = {ROOT / "src" / f"{role}.svg": render_icon(role, "currentColor", role) for role in ROLES}
    for name, meta in sorted({**REGISTRY, **SURFACES}.items()):
        if meta["language"] not in COLORS:
            raise ValueError(f"unknown language token for {name}")
        if meta["status"] not in {"approved", "pending-symbol"}:
            raise ValueError(f"unknown review status for {name}")
        destination = OUT if meta["status"] == "approved" else STUDY_OUT
        expected[destination / f"{name}.svg"] = render_icon(
            meta["role"], COLORS[meta["language"]], name, meta["status"]
        )
    organization_directory = "dist/organization" if organization_emblem_approved() else "studies/organization"
    expected[ROOT / organization_directory / "mark.svg"] = render_organization_mark()
    for candidate_id in sorted(ORGANIZATION.get("candidates", {})):
        expected[ROOT / "studies/organization" / f"candidate-{candidate_id}.svg"] = render_organization_candidate(candidate_id)
    lockup_directory = "dist/organization" if organization_wordmarks_approved() else "studies/organization"
    for layout in LOCKUP_LAYOUTS:
        for variant in ORGANIZATION["wordmarks"]["variants"]:
            expected[ROOT / lockup_directory / lockup_name(layout, variant)] = render_organization_lockup(layout, variant)
    for path, (candidate_id, language) in role_candidate_files().items():
        expected[path] = render_role_candidate(candidate_id, language)
    for path, (treatment, name) in yellow_candidate_files().items():
        expected[path] = render_yellow_candidate(treatment, name)
    return expected


def owned_outputs() -> set[Path]:
    """Every path the generator may write, in either review location.

    Only these paths are eligible for stale-output cleanup, so an asset that
    moves between ``studies/`` and ``dist/`` loses its previous copy while any
    other SVG in an output directory is left alone.
    """
    owned = set()
    for name in sorted({**REGISTRY, **SURFACES}):
        owned |= {OUT / f"{name}.svg", STUDY_OUT / f"{name}.svg"}
    owned |= {ROOT / "dist/organization/mark.svg", ROOT / "studies/organization/mark.svg"}
    for candidate_id in sorted(ORGANIZATION.get("candidates", {})):
        owned.add(ROOT / "studies/organization" / f"candidate-{candidate_id}.svg")
    for layout in LOCKUP_LAYOUTS:
        for variant in ORGANIZATION["wordmarks"]["variants"]:
            name = lockup_name(layout, variant)
            owned |= {ROOT / "dist/organization" / name, ROOT / "studies/organization" / name}
    owned |= set(role_candidate_files()) | set(yellow_candidate_files())
    return owned


def main() -> int:
    if GEOMETRY["design_id"] != "repository-icon-cube-01" or GEOMETRY["view_box"] != [0, 0, 24, 24]:
        raise ValueError("unexpected geometry token")
    expected = outputs()
    owned = owned_outputs() | set(expected)
    OUT.mkdir(parents=True, exist_ok=True)
    for target, content in expected.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    unmanaged = []
    for directory in (OUT, STUDY_OUT, ROOT / "dist/organization", ROOT / "studies/organization", ROOT / "studies/roles", ROOT / "studies/python-yellow"):
        for path in sorted(directory.glob("*.svg")):
            if path in expected:
                continue
            if path in owned:
                path.unlink()
            else:
                unmanaged.append(path)
    for path in unmanaged:
        print(
            f"error: unmanaged SVG {path.relative_to(ROOT).as_posix()} is not generated from "
            "registry/ or tokens/; it was left in place. Remove it or move it out of the output directories.",
            file=sys.stderr,
        )
    return 1 if unmanaged else 0


if __name__ == "__main__":
    sys.exit(main())
