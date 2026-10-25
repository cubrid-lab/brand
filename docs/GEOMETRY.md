# Repository icon geometry — Cube Study / 01

The maintainer selected the cube-based icon system shown in the [supplied infographic](studies/repository-icon-system-infographic.png) to replace the prior Driver artwork. The raster is the visual reference; [`tokens/geometry.json`](../tokens/geometry.json) supplies the reproducible numerical construction, and [`scripts/build.py`](../scripts/build.py) renders every role. The vector drawings are deliberate reconstructions of the raster, not claims of pixel-exact source paths.

## Shared 24×24 construction

Let `c = 12`, `h = 10`, `r = 10 / √3` (stored as `5.773502692`), and `t = 1`. The top rhombus is:

1. `(c, t)`
2. `(c + h, t + r)`
3. `(c, t + 2r)`
4. `(c - h, t + r)`

Its internal corners are 60° and 120°. The left and right face vertices are computed from the inset center seam and face-height parameters in the token file. Their gap leaves visible negative space around the top and center seams. Each role uses the same cube grammar. Most roles keep the three cube faces with a distinct white geometric mark. The Driver and ORM roles are drawn as solid layers in the cube color instead, with no white mark (see [Layered Driver and ORM](#layered-driver-and-orm-issue-30)).

### Seam backing (issue #23)

A white mark that crosses or encloses a seam would otherwise sit on transparent negative space and break apart or vanish on a light page. Each cube-based role therefore paints a solid backing in the cube color under its mark: the mark itself, filled and widened by `glyph_backing_pad` (`0.55`) on every side. The backing is drawn before the face shading, so it matches the faces exactly and is visible only where it bridges a seam. Both the backing and the white mark are clipped to the cube's outer silhouette, so neither extends past it. The glyph paths themselves are unchanged. `tests/test_glyph_seams.py` samples every generated role template and fails if any white sample lies within 0.3 units of an unpainted seam.

The role marks are original vector primitives: Driver vertical stack, ORM lateral plates, MCP three-way router, Cookbook book, Benchmark bars, Operator six-spoke control dial, Showcase play triangle, Docs lines, and Community people. The Operator dial is deliberately six-spoke and is not a Kubernetes logo. The Cookbook mark is an open book drawn as one filled page per side face, with the transparent center seam serving as the spine; its text lines are stroked in `currentColor` so they fade out at small sizes. Keeping each page on a single face means the seam gap never cuts through the white mark on dark backgrounds.

### Layered Driver and ORM (issue #30)

The two layered roles use the same construction along two different axes.

- **Driver: vertical stack.** The top rhombus sits over two chevron layers, `M 2 10.1 L 12 15.6 L 22 10.1 L 22 12.15 L 12 17.65 L 2 12.15 Z` and the same shape 4.2 units lower, stacked top to bottom. This was the ORM geometry until 2026-10-25. It now represents the driver as the foundational data-access layer.
- **ORM: lateral plates.** The same idea turned on its side. The left face is a full front plate. Behind it, two bent layers stand side by side along the right axis. Each layer is a strip of the top rhombus joined to a strip of the right face, at `x` 14–17 and 19–22 on the rhombus's front edge, and follows the right face's bottom edge. The corresponding layers side by side suggest object-to-relational mapping.

Neither role has a white mark, so neither needs a seam backing. The Driver stack is drawn flat, as the previous ORM was, and so are the ORM plates.

### MCP three-way router (issue #23)

The MCP mark is a hub at the cube's center vertex, a white circle of radius 1.75 at `(12, 12.95)`. From the hub, one 1.3-unit link runs into each face to a port of radius 1.45: top `(12, 6.9)`, left `(6.5, 15.55)` and right `(17.5, 15.55)`. The hub covers the point where the three seams meet, and the seam backing bridges it. Each link stays on its own face. It replaced the earlier four-node diamond network.

The candidates that were reviewed, including the unselected ones, remain generated under `studies/roles/` from [`tokens/role-candidates.json`](../tokens/role-candidates.json). See [the role redesign study](studies/role-redesign-30.md).

## Color and identity

One role keeps the same geometry across languages. The root SVG color is taken only from [`tokens/colors.json`](../tokens/colors.json). Mixed-language repositories and non-repository surfaces use the Neutral token. ### Light-token treatment (issue #38)

Python Yellow `#FFD43B` is too light for white marks (1.39:1 on its faces) or a bare silhouette on white (1.43:1). [`tokens/colors.json`](../tokens/colors.json) therefore gives the Python token a `treatments` entry, which `light_treatment()` in `scripts/build.py` applies to every icon in that color:

- **Dark marks.** The visible role mark is drawn in the dark ink `#40350F` (the token mixed 75% toward black) instead of white: at least 6.84:1 on every face shade. The seam backing stays in the cube color.
- **Ochre keyline.** A 0.6-unit keyline in `#8C7520` (the token mixed 45% toward black) runs outside the shape: 4.49:1 on `#FFFFFF` and 4.22:1 on `#0D1117`. For the cube roles it is the outline stroke clipped to the outside of the cube, so the seams stay open; for the Driver and ORM layers it is drawn under each layer, so only its outer half shows and each gap narrows by 1.2 units.

Geometry, face shading and every other language are unchanged. The treatment was selected as `t3-ochre-keyline` from [the Python Yellow study](studies/python-yellow-38.md).

The infographic's mismatched labels do not override actual repository languages: Drizzle is TypeScript, Benchmark is mixed-language/Neutral, and Showcase is Neutral until its identity is refined.

The [organization emblem](../dist/organization/mark.svg) uses the same construction grammar but a separate three-color face treatment and no role glyph. Its colors and scoped approvals come from [`tokens/organization.json`](../tokens/organization.json). The maintainer approved this distinct identity for CUBRID Lab's own avatar and profile use on 2026-10-15. Deployment and remaining wordmark/legal review are tracked separately in [issue #3](https://github.com/cubrid-lab/brand/issues/3).

## Provenance and status

The former Connector Study / 02 Driver SVG and its numerical parameters remain unchanged under [`provenance/connector-study-02/`](../provenance/connector-study-02/). They document the superseded design; they are not inputs to the current generator. The current repo-role icons were selected for implementation in [issue #6](https://github.com/cubrid-lab/brand/issues/6). Design selection does not establish trademark clearance or a redistribution license.
