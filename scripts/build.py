"""Build CUBRID Lab role icons and organization identity from numeric tokens."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
GEOMETRY = json.loads((ROOT / "tokens/geometry.json").read_text(encoding="utf-8"))
COLORS = json.loads((ROOT / "tokens/colors.json").read_text(encoding="utf-8"))["languages"]
ORGANIZATION = json.loads((ROOT / "tokens/organization.json").read_text(encoding="utf-8"))
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


def glyph_backing(role: str) -> str:
    """A solid plate in the cube color: the role mark, filled and widened by ``glyph_backing_pad``.

    It is drawn under the face shading, so it is invisible on the faces and only
    bridges the transparent seams where the white mark crosses or encloses them.
    """
    pad = GEOMETRY["glyph_backing_pad"]
    group = ElementTree.fromstring(f"<g>{GLYPHS[role]}</g>")
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


def cube_faces(role: str, key: str) -> str:
    polygons = cube_polygons()
    clip = f"{key}-cube"
    lines = [f'  <clipPath id="{clip}"><path d="{path_data(cube_outline())}"/></clipPath>']
    lines += [f'  <path d="{path_data(polygons[face])}" fill="currentColor"/>' for face in ("top", "left", "right")]
    lines.append(f'  <g clip-path="url(#{clip})">\n{glyph_backing(role)}\n  </g>')
    lines.append(f'  <path d="{path_data(polygons["top"])}" fill="#fff" opacity="0.08"/>')
    lines.append(f'  <path d="{path_data(polygons["left"])}" fill="#000" opacity="0.10"/>')
    lines.append(f'  <g clip-path="url(#{clip})">\n{GLYPHS[role]}\n  </g>')
    return "\n".join(lines)


# White marks are original geometric drawings. In particular, Operator is a
# generic six-spoke control dial, not a Kubernetes or other third-party logo.
GLYPHS = {
    "driver": '''  <path d="M 12.6 18.1 L 15.7 16.15 L 17.45 16.15" fill="none" stroke="#fff" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="18.35" cy="16.15" r="1.7" fill="#fff"/>''',
    "mcp": '''  <g fill="none" stroke="#fff" stroke-width="1.2" stroke-linecap="round">
    <path d="M 12 9.2 L 7.8 15.1 L 12 20.0 L 16.2 15.1 Z"/>
    <path d="M 7.8 15.1 L 16.2 15.1"/>
  </g>
  <g fill="#fff"><circle cx="12" cy="9.2" r="1.65"/><circle cx="7.8" cy="15.1" r="1.55"/><circle cx="16.2" cy="15.1" r="1.55"/><circle cx="12" cy="20" r="1.55"/></g>''',
    "cookbook": '''  <path d="M 5.6 13.3 Q 8.6 12.8 10.7 14.5 L 10.7 20.0 Q 8.6 18.3 5.6 18.8 Z M 18.4 13.3 Q 15.4 12.8 13.3 14.5 L 13.3 20.0 Q 15.4 18.3 18.4 18.8 Z" fill="#fff"/>
  <path d="M 6.9 15.5 Q 8.6 15.4 9.6 16.1 M 6.9 17.0 Q 8.6 16.9 9.6 17.6 M 17.1 15.5 Q 15.4 15.4 14.4 16.1 M 17.1 17.0 Q 15.4 16.9 14.4 17.6" fill="none" stroke="currentColor" stroke-width="0.9" stroke-linecap="round"/>''',
    "benchmark": '''  <path d="M 5.5 15.2 H 8.4 V 19.1 H 5.5 Z M 10.5 12.7 H 13.4 V 19.1 H 10.5 Z M 15.5 9.9 H 18.4 V 19.1 H 15.5 Z" fill="#fff"/>''',
    "operator": '''  <circle cx="12" cy="13.7" r="4.25" fill="none" stroke="#fff" stroke-width="1.25"/>
  <circle cx="12" cy="13.7" r="1.2" fill="none" stroke="#fff" stroke-width="1.1"/>
  <path d="M 12 8.5 V 12.4 M 12 15 V 22 M 7.5 11.1 L 10.9 13.1 M 13.1 14.3 L 16.5 16.3 M 7.5 16.3 L 10.9 14.3 M 13.1 13.1 L 16.5 11.1" fill="none" stroke="#fff" stroke-width="1.25" stroke-linecap="round"/>''',
    "showcase": '''  <path d="M 16.2 13.8 L 20 16.1 L 16.2 18.4 Z" fill="#fff"/>''',
    "docs": '''  <path d="M 15 13.6 L 20 10.8 L 20 12.1 L 15 14.9 Z M 15 16 L 20 13.2 L 20 14.5 L 15 17.3 Z M 15 18.4 L 20 15.6 L 20 16.9 L 15 19.7 Z" fill="#fff"/>''',
    "community": '''  <g fill="#fff"><circle cx="7" cy="14.2" r="1.2"/><circle cx="12" cy="12.8" r="1.25"/><circle cx="17" cy="14.2" r="1.2"/>
    <path d="M 4.6 17.5 Q 4.6 15.6 7 15.6 Q 9.4 15.6 9.4 17.5 V 19 L 4.6 18.2 Z M 9.5 16.2 Q 9.5 14.4 12 14.4 Q 14.5 14.4 14.5 16.2 V 19.8 L 12 21.2 L 9.5 19.8 Z M 14.6 17.5 Q 14.6 15.6 17 15.6 Q 19.4 15.6 19.4 17.5 V 18.2 L 14.6 19 Z"/></g>''',
}


def orm_faces() -> str:
    top = path_data(cube_polygons()["top"])
    layers = (
        "M 2 10.1 L 12 15.6 L 22 10.1 L 22 12.15 L 12 17.65 L 2 12.15 Z",
        "M 2 14.3 L 12 19.8 L 22 14.3 L 22 16.35 L 12 21.85 L 2 16.35 Z",
    )
    return "\n".join([f'  <path d="{top}" fill="currentColor"/>'] + [f'  <path d="{layer}" fill="currentColor"/>' for layer in layers])


def render_icon(role: str, color: str, key: str, status: str = "pending-symbol") -> str:
    if role not in ROLES or not KEY_RE.fullmatch(key):
        raise ValueError("invalid role or identifier")
    if status not in {"approved", "pending-symbol"}:
        raise ValueError("invalid review status")
    if color != "currentColor" and not COLOR_RE.fullmatch(color):
        raise ValueError("invalid color")
    color_attr = "" if color == "currentColor" else f' color="{color}"'
    shape = orm_faces() if role == "orm" else cube_faces(role, key)
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


def render_organization_lockup(layout: str) -> str:
    if layout == "horizontal":
        view_box, transform = "0 0 300 64", "translate(4 4) scale(2.25)"
        title = '<text x="68" y="38" font-family="Arial, Helvetica, sans-serif" font-size="29" font-weight="700" fill="#071B43">CUBRID Lab</text>'
        tagline = '<text x="69" y="54" font-family="Arial, Helvetica, sans-serif" font-size="8.4" letter-spacing="1" fill="#284679">Open Source for a More Connected World</text>'
    elif layout == "stacked":
        view_box, transform = "0 0 200 154", "translate(64 5) scale(3)"
        title = '<text x="100" y="117" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="25" font-weight="700" fill="#071B43">CUBRID Lab</text>'
        tagline = '<text x="100" y="135" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="7.3" letter-spacing="0.55" fill="#284679">Open Source for a More Connected World</text>'
    else:
        raise ValueError("invalid lockup layout")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" role="img" aria-labelledby="lockup-title lockup-desc">\n'
        f'  <title id="lockup-title">CUBRID Lab {layout} organization lockup study</title>\n'
        '  <desc id="lockup-desc">Organization identity candidate; design and rights review pending.</desc>\n'
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
    for layout in ("horizontal", "stacked"):
        expected[ROOT / "studies/organization" / f"lockup-{layout}.svg"] = render_organization_lockup(layout)
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
    for layout in ("horizontal", "stacked"):
        owned.add(ROOT / "studies/organization" / f"lockup-{layout}.svg")
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
    for directory in (OUT, STUDY_OUT, ROOT / "dist/organization", ROOT / "studies/organization"):
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
