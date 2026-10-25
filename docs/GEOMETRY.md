# Repository icon geometry — Cube Study / 01

The maintainer selected the cube-based icon system shown in the [supplied infographic](studies/repository-icon-system-infographic.png) to replace the prior Driver artwork. The raster is the visual reference; [`tokens/geometry.json`](../tokens/geometry.json) supplies the reproducible numerical construction, and [`scripts/build.py`](../scripts/build.py) renders every role. The vector drawings are deliberate reconstructions of the raster, not claims of pixel-exact source paths.

## Shared 24×24 construction

Let `c = 12`, `h = 10`, `r = 10 / √3` (stored as `5.773502692`), and `t = 1`. The top rhombus is:

1. `(c, t)`
2. `(c + h, t + r)`
3. `(c, t + 2r)`
4. `(c - h, t + r)`

Its internal corners are 60° and 120°. The left and right face vertices are computed from the inset center seam and face-height parameters in the token file. Their gap leaves visible negative space around the top and center seams. Each role uses the same cube grammar, with a distinct white geometric mark. ORM uses the shared rhombus plus two open chevron layers instead of the cube faces.

The role marks are original vector primitives: Driver connector and node, ORM layers, MCP network, Cookbook book, Benchmark bars, Operator six-spoke control dial, Showcase play triangle, Docs lines, and Community people. The Operator dial is deliberately six-spoke and is not a Kubernetes logo. The Cookbook mark is an open book drawn as one filled page per side face, with the transparent center seam serving as the spine; its text lines are stroked in `currentColor` so they fade out at small sizes. Keeping each page on a single face means the seam gap never cuts through the white mark on dark backgrounds.

## Color and identity

One role keeps the same geometry across languages. The root SVG color is taken only from [`tokens/colors.json`](../tokens/colors.json). Mixed-language repositories and non-repository surfaces use the Neutral token. The infographic's mismatched labels do not override actual repository languages: Drizzle is TypeScript, Benchmark is mixed-language/Neutral, and Showcase is Neutral until its identity is refined.

The [organization emblem](../dist/organization/mark.svg) uses the same construction grammar but a separate three-color face treatment and no role glyph. Its colors and scoped approvals come from [`tokens/organization.json`](../tokens/organization.json). The maintainer approved this distinct identity for CUBRID Lab's own avatar and profile use on 2026-10-15. Deployment and remaining wordmark/legal review are tracked separately in [issue #3](https://github.com/cubrid-lab/brand/issues/3).

## Provenance and status

The former Connector Study / 02 Driver SVG and its numerical parameters remain unchanged under [`provenance/connector-study-02/`](../provenance/connector-study-02/). They document the superseded design; they are not inputs to the current generator. The current repo-role icons were selected for implementation in [issue #6](https://github.com/cubrid-lab/brand/issues/6). Design selection does not establish trademark clearance or a redistribution license.
