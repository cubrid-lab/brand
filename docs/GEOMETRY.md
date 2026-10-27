# Repository icon geometry — Cube Study / 01

The maintainer selected the cube-based icon system shown in the [supplied infographic](studies/repository-icon-system-infographic.png) to replace the prior Driver artwork. The raster is the visual reference; [`tokens/geometry.json`](../tokens/geometry.json) supplies the reproducible numerical construction, and [`scripts/build.py`](../scripts/build.py) renders every role. The vector drawings are deliberate reconstructions of the raster, not claims of pixel-exact source paths.

## Shared 24×24 construction

Let `c = 12`, `h = 10`, `r = 10 / √3` (stored as `5.773502692`), and `t = 1`. The top rhombus is:

1. `(c, t)`
2. `(c + h, t + r)`
3. `(c, t + 2r)`
4. `(c - h, t + r)`

Its internal corners are 60° and 120°. The left and right face vertices are computed from the inset center seam and face-height parameters in the token file. Their gap leaves visible negative space around the top and center seams. Each role uses the same cube grammar. Most roles keep the three cube faces with a distinct white geometric mark. The Driver and ORM now keep the same three cube faces and use two inset grooves to indicate three equal layers, turned in different directions. Their earlier detached-layer constructions remain in the historical [#30 review](studies/role-redesign-30.md). See [Restored cube layers](#restored-cube-layers-issues-41-and-43).

### Seam backing (issue #23)

A white mark that crosses or encloses a seam would otherwise sit on transparent negative space and break apart or vanish on a light page. Each cube-based role therefore paints a solid backing in the cube color under its mark: the mark itself, filled and widened by `glyph_backing_pad` (`0.55`) on every side. The backing is drawn before the face shading, so it matches the faces exactly and is visible only where it bridges a seam. Both the backing and the white mark are clipped to the cube's outer silhouette, so neither extends past it. The glyph paths themselves are unchanged. `tests/test_glyph_seams.py` samples every generated role template and fails if any white sample lies within 0.3 units of an unpainted seam.

The role marks are original vector primitives: Driver vertical stack, ORM lateral plates, MCP three-way router, Cookbook book, Benchmark bars, Operator six-spoke control dial, Showcase play triangle, Docs lines, and Community people. The Operator dial is deliberately six-spoke and is not a Kubernetes logo. The Cookbook mark is an open book drawn as one filled page per side face, with the transparent center seam serving as the spine; its text lines are stroked in `currentColor` so they fade out at small sizes. Keeping each page on a single face means the seam gap never cuts through the white mark on dark backgrounds.

### Operator transparent dial (issue #59)

The Operator dial keeps its approved shape, but it sits 0.55 units higher (hub at `(12, 13.15)`), so its lower vertical spoke lies on the center seam, runs straight out through the cube's flat bottom edge with no rounded end, and its two upper diagonal spokes run out along the top-to-side seams to the cube's outer corners, so each spoke and its seam form one continuous line. Its rim, hub and spokes are real alpha transparency instead of white strokes. The generator draws the cube (faces, seam backing and face shading) inside one `<mask>` whose cutout is the same dial paths in black on a white rectangle, so the page behind the icon shows through. Nothing is painted white or in a background color. The seam backing still surrounds the dial, so the cut-out lines keep the same clearance from the seams. `KNOCKOUT_ROLES` in `scripts/build.py` lists the roles that use this treatment; `tests/test_cube_layers.py` renders the icon and checks the alpha.

### Layered Driver and ORM (issue #30)

The two layered roles use the same construction along two different axes.

- **Driver: vertical stack.** The top rhombus sits over two chevron layers, `M 2 10.1 L 12 15.6 L 22 10.1 L 22 12.15 L 12 17.65 L 2 12.15 Z` and the same shape 4.2 units lower, stacked top to bottom. This was the ORM geometry until 2026-10-25. It now represents the driver as the foundational data-access layer.
- **ORM: lateral plates.** The same idea turned on its side. The left face is a full front plate. Behind it, two bent layers stand side by side along the right axis. Each layer is a strip of the top rhombus joined to a strip of the right face, at `x` 14–17 and 19–22 on the rhombus's front edge, and follows the right face's bottom edge. The corresponding layers side by side suggest object-to-relational mapping.

These floating-plate shapes are historical (#30); they are still rendered under `studies/roles/` and in the earlier Python Yellow `studies/python-yellow/` review, but are no longer the production Driver/ORM artwork.

### Restored cube layers (issues #41 and #43)

Both current roles use the **same** top rhombus and inset left/right faces as the other CUBRID Lab cube icons. The outer cube silhouette is continuous in each role, and there are exactly **two** internal dividing grooves at fractions `1/3` and `2/3`, giving **three equal-thickness layers** along the selected axis.

- **Driver:** each dividing groove follows the diagonal edge direction across the left and right side faces, one third and two thirds of the face height from the top. Grooves stop short of the outer edges and of the transparent center seam, preserving the cube.
- **ORM:** each dividing groove crosses the top rhombus from near back-left to near front-right and continues vertically on the right face, at one third and two thirds of its width. The front left face remains unbroken. This is the same three-part subdivision **turned sideways**, not three detached slabs.
- Both use `1.05`-unit rounded white strokes in every language, Python Yellow included since [issue #54](https://github.com/cubrid-lab/brand/issues/54). Low white-groove contrast remains a documented limitation on Go, Rust and Python Yellow; check the render on actual backgrounds at small sizes.
- The role bodies are generated by `cube_layers()`; historical study functions are kept separate to avoid rewriting the earlier approval evidence.

Review the [Driver/ORM comparison](studies/cube-stacks-41-43.md).

### MCP three-way router (issue #23)

The MCP mark is a hub at the cube's center vertex, a white circle of radius 1.75 at `(12, 12.95)`. From the hub, one 1.3-unit link runs into each face to a port of radius 1.45: top `(12, 6.9)`, left `(6.5, 15.55)` and right `(17.5, 15.55)`. The hub covers the point where the three seams meet, and the seam backing bridges it. Each link stays on its own face. It replaced the earlier four-node diamond network.

The candidates that were reviewed, including the unselected ones, remain generated under `studies/roles/` from [`tokens/role-candidates.json`](../tokens/role-candidates.json). See [the role redesign study](studies/role-redesign-30.md).

## Color and identity

One role keeps the same geometry across languages. The root SVG color is taken only from [`tokens/colors.json`](../tokens/colors.json). Mixed-language repositories and non-repository surfaces use the Neutral token. ### Light-token treatment (issue #38, retired by issue #54)

**Retired on 2026-10-27.** The maintainer chose one treatment for every language ([issue #54](https://github.com/cubrid-lab/brand/issues/54)): `tokens/colors.json` has no `treatments` entry, so Python Yellow icons draw white marks on a bare cube, and only their color differs from the other languages. `light_treatment()` remains for the #38 study renders. The section below records the treatment as it was applied from 2026-10-25 to 2026-10-27.

Python Yellow `#FFD43B` is too light for white marks (1.39:1 on its faces) or a bare silhouette on white (1.43:1). [`tokens/colors.json`](../tokens/colors.json) therefore gives the Python token a `treatments` entry, which `light_treatment()` in `scripts/build.py` applies to every icon in that color:

- **Dark marks.** The visible role mark is drawn in the dark ink `#40350F` (the token mixed 75% toward black) instead of white: at least 6.84:1 on every face shade. The seam backing stays in the cube color.
- **Ochre keyline.** A 0.6-unit keyline in `#8C7520` (the token mixed 45% toward black) runs outside the shape: 4.49:1 on `#FFFFFF` and 4.22:1 on `#0D1117`. For the cube roles it follows only each face's outer edges and is clipped to the outside of the faces, so the seams stay open at the side corners and at the bottom vertex and the silhouette matches the organization emblem ([issue #50](https://github.com/cubrid-lab/brand/issues/50); before/after: [`studies/keyline-emblem-50/before-after.png`](studies/keyline-emblem-50/before-after.png)). The #38 study SVGs keep their original closed outline. For the historical Driver and ORM layers it is drawn under each layer, so only its outer half shows and each gap narrows by 1.2 units.

Geometry, face shading and every other language are unchanged. The treatment was selected as `t3-ochre-keyline` from [the Python Yellow study](studies/python-yellow-38.md).

The infographic's mismatched labels do not override actual repository languages: Drizzle is TypeScript, Benchmark is mixed-language/Neutral, and Showcase is Neutral until its identity is refined.

The [organization emblem](../dist/organization/mark.svg) uses the same construction grammar but a separate three-color face treatment and no role glyph. Its colors and scoped approvals come from [`tokens/organization.json`](../tokens/organization.json). The maintainer approved this distinct identity for CUBRID Lab's own avatar and profile use on 2026-10-15. Deployment and remaining wordmark/legal review are tracked separately in [issue #3](https://github.com/cubrid-lab/brand/issues/3).

## Provenance and status

The former Connector Study / 02 Driver SVG and its numerical parameters remain unchanged under [`provenance/connector-study-02/`](../provenance/connector-study-02/). They document the superseded design; they are not inputs to the current generator. The current repo-role icons were selected for implementation in [issue #6](https://github.com/cubrid-lab/brand/issues/6). Design selection does not establish trademark clearance or a redistribution license.
