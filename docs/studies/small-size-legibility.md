# Small-size legibility and contrast study (issue #21)

Date: 2026-10-25, against `main` at [`2de5d23`](https://github.com/cubrid-lab/brand/commit/2de5d23). Renderer: librsvg (`rsvg-convert`), composited with Pillow.

This study measures how the approved role icons and the organization mark hold up at 16, 24, 32, 48 and 64 px on a light (`#FFFFFF`) and a dark (`#0D1117`) page. It is design guidance. It is not an accessibility audit or a claim of WCAG conformance: WCAG 1.4.11 exempts logotypes, and its 3:1 non-text threshold is used here only as a yardstick.

**No generated asset changes.** Proposed adjustments are rendered from an in-memory copy of the generator for review. Any of them needs the maintainer's design approval before it reaches `dist/`.

## Review sheets

- [`small-size-legibility/sizes.png`](small-size-legibility/sizes.png): every generated icon in `dist/` and the organization mark at 16, 24, 32, 48 and 64 px, light and dark.
- [`small-size-legibility/pixels.png`](small-size-legibility/pixels.png): the 16 and 24 px renderings enlarged 6x without smoothing, one block per device pixel.
- [`small-size-legibility/proposal-before-after.png`](small-size-legibility/proposal-before-after.png): the five icons the proposals below would change, current and proposed, at 16 to 128 px, light and dark.

Regenerate them, and the contrast tables below, with `python scripts/legibility_study.py OUT_DIR` (optional; needs `rsvg-convert` and Pillow; not used by the build or CI).

## Criteria

| Id | Criterion | Measure | Pass |
| --- | --- | --- | --- |
| C1 | Mark contrast | WCAG contrast of the white mark on each face shade it sits on (token color, top face with the 8% white overlay, left face with the 10% black overlay) | ≥ 3:1 |
| C2 | Mark weight | Thinnest essential white stroke or shape, in device pixels: viewBox units × size / 24 | ≥ 1 px |
| C3 | Separation | Narrowest essential gap between white parts of one mark, in device pixels | ≥ 1 px |
| C4 | Recognition | The mark reads as its role shape in the render (one observer, rsvg, both backgrounds) | yes |

A size **passes** when all four hold, is **marginal** when a measure is within 0.1 px of its limit or C4 is uncertain, and **fails** otherwise. Detail that is meant to drop out at small sizes (the Cookbook text lines, which are stroked in `currentColor` by design) is reported but not graded. Seam continuity is already enforced by `tests/test_glyph_seams.py` and is not repeated here.

## Contrast measurements

White role mark on each face shade (the shading is the overlay `scripts/build.py` draws in `cube_faces()`):

| Token | Color | White on top face | White on left face | White on right face | Keyline proposal | Used by |
| --- | --- | --- | --- | --- | --- | --- |
| python | `#3776AB` | 4.16 (pass) | 5.73 (pass) | 4.84 (pass) | — | `cubrid-cookbook-python`, `cubrid-mcp-server`, `pycubrid`, `sqlalchemy-cubrid` (no white mark) |
| typescript | `#3178C6` | 3.94 (pass) | 5.39 (pass) | 4.53 (pass) | — | `cubrid-client`, `drizzle-cubrid` (no white mark) |
| go | `#00ADD8` | 2.45 (below 3:1) | 3.21 (pass) | 2.64 (below 3:1) | `#0093B8` | `cubrid-go`, `cubrid-kubernetes-operator`, `gorm-cubrid` (no white mark) |
| rust | `#DEA384` | 2.03 (below 3:1) | 2.66 (below 3:1) | 2.17 (below 3:1) | `#A67A63` | `cubrid-rs`, `sea-orm-cubrid` (no white mark) |
| javascript | `#F7DF1E` | 1.32 (below 3:1) | 1.68 (below 3:1) | 1.35 (below 3:1) | `#948612` | unused |
| ocaml | `#A34CC3` | 4.20 (pass) | 5.68 (pass) | 4.80 (pass) | — | unused |
| neutral | `#6B7280` | 4.13 (pass) | 5.70 (pass) | 4.83 (pass) | — | `community`, `cubrid-benchmark`, `docs`, `showcase` |

Cube faces against the page (informative: this is the silhouette, which carries the color identity, not a white mark):

| Cube color | Face | On light `#FFFFFF` | On dark `#0D1117` |
| --- | --- | --- | --- |
| python `#3776AB` | top `#4781B2` | 4.16 | 4.55 |
| python `#3776AB` | left `#326A9A` | 5.73 | 3.30 |
| python `#3776AB` | right `#3776AB` | 4.84 | 3.91 |
| typescript `#3178C6` | top `#4183CB` | 3.94 | 4.81 |
| typescript `#3178C6` | left `#2C6CB2` | 5.39 | 3.51 |
| typescript `#3178C6` | right `#3178C6` | 4.53 | 4.17 |
| go `#00ADD8` | top `#14B4DB` | 2.45 | 7.73 |
| go `#00ADD8` | left `#009CC2` | 3.21 | 5.89 |
| go `#00ADD8` | right `#00ADD8` | 2.64 | 7.18 |
| rust `#DEA384` | top `#E1AA8E` | 2.03 | 9.32 |
| rust `#DEA384` | left `#C89377` | 2.66 | 7.12 |
| rust `#DEA384` | right `#DEA384` | 2.17 | 8.72 |
| javascript `#F7DF1E` | top `#F8E230` | 1.32 | 14.34 |
| javascript `#F7DF1E` | left `#DEC91B` | 1.68 | 11.24 |
| javascript `#F7DF1E` | right `#F7DF1E` | 1.35 | 13.99 |
| ocaml `#A34CC3` | top `#AA5AC8` | 4.20 | 4.51 |
| ocaml `#A34CC3` | left `#9344B0` | 5.68 | 3.33 |
| ocaml `#A34CC3` | right `#A34CC3` | 4.80 | 3.95 |
| neutral `#6B7280` | top `#777D8A` | 4.13 | 4.58 |
| neutral `#6B7280` | left `#606773` | 5.70 | 3.32 |
| neutral `#6B7280` | right `#6B7280` | 4.83 | 3.91 |
| organization | top `#006BDA` | 5.10 | 3.71 |
| organization | left `#00A36F` | 3.25 | 5.83 |
| organization | right `#E60039` | 4.75 | 3.99 |

Findings:

- Go and Rust are the only used tokens where the white mark falls below 3:1. The Driver mark sits on the right face (Go 2.64, Rust 2.17). The Operator dial covers all three faces (Go 2.45 to 3.21).
- On a white page the Go (2.45 to 3.21) and Rust (2.03 to 2.66) cubes, including the ORM layers, have a lower-contrast silhouette than the other tokens. All tokens are at least 3.30:1 on the dark page.
- JavaScript (unused today) would give a white mark only 1.32 to 1.68:1. A JavaScript role icon needs a reviewed treatment before it is added; `tests/test_legibility.py` fails if one is added without updating this study.
- The organization mark's faces are at least 3.25:1 on both pages.

## Mark weight and separation

Measured from the glyph geometry in `scripts/build.py` (viewBox units, then device pixels at 16 and 24 px):

| Role | Limiting essential feature | Units | 16 px | 24 px |
| --- | --- | --- | --- | --- |
| Driver | connector stroke | 1.35 | 0.90 | 1.35 |
| MCP | link stroke | 1.2 | 0.80 | 1.20 |
| Cookbook | gap between the pages (seam) | 2.6 | 1.73 | 2.60 |
| Cookbook (detail, not graded) | text-line stroke / paper between lines | 0.9 / 0.6 | 0.60 / 0.40 | 0.90 / 0.60 |
| Benchmark | gap between bars | 2.1 | 1.40 | 2.10 |
| Operator | hub ring stroke (rim and spokes 1.25) | 1.1 | 0.73 | 1.10 |
| Showcase | triangle (3.8 × 4.6 overall) | 3.8 | 2.53 | 3.80 |
| Docs | bar thickness / gap between bars, perpendicular | 1.13 / 0.96 | 0.76 / 0.64 | 1.13 / 0.96 |
| Community | gap between a side figure and the center body / head and body | 0.1 / 0.2 | 0.07 / 0.13 | 0.10 / 0.20 |
| ORM | gap between layers, perpendicular | 1.88 | 1.25 | 1.88 |
| Organization mark | seam between faces (the faces also differ in color) | 1.4 | 0.93 | 1.40 |

## Pass/fail by icon and size

Light and dark pages give the same grades except where noted. P = pass, M = marginal, F = fail, with the failing criteria.

| Icon(s) | 16 px | 24 px | 32 px | 48 px | 64 px |
| --- | --- | --- | --- | --- | --- |
| Driver: `pycubrid`, `cubrid-client` | F (C2, C4: a 2 to 3 px smudge in the corner) | M (C4: reads as a short line and dot) | P | P | P |
| Driver: `cubrid-go` | F (C1, C2, C4) | F (C1) | F (C1) | F (C1) | F (C1) |
| Driver: `cubrid-rs` | F (C1, C2, C4) | F (C1) | F (C1) | F (C1) | F (C1) |
| ORM: all four | P | P | P | P | P |
| MCP: `cubrid-mcp-server` | F (C2, C4: a diamond blob) | P | P | P | P |
| Cookbook: `cubrid-cookbook-python` | P (two pages; lines drop out by design) | P | P | P | P |
| Benchmark: `cubrid-benchmark` | P | P | P | P | P |
| Operator: `cubrid-kubernetes-operator` | F (C1, C2, C4: a ring) | F (C1; C4 marginal, spokes merge) | F (C1) | F (C1) | F (C1) |
| Showcase: `showcase` | M (C4: the triangle reads as a dot) | M (C4) | P | P | P |
| Docs: `docs` | F (C2, C3: bars merge into a block) | M (C3, 0.96 px) | P | P | P |
| Community: `community` | F (C3, C4: one blob) | F (C3) | F (C3; the group reads) | F (C3; the group reads) | F (C3; the group reads) |
| Organization mark | P | P | P | P | P |

The C1 failures for Go and Rust are measurements against a guideline threshold. In the renders the Go and Rust marks are still visible at 24 px and up; they are less crisp than the Python and TypeScript variants, most visibly on the Rust cube.

## Proposals

### P1. Darker keyline under the mark for low-contrast tokens (Go, Rust)

Affected approved assets: `cubrid-go`, `cubrid-rs`, `cubrid-kubernetes-operator`.

The seam backing from issue #23 already draws the mark widened by 0.55 units under the face shading, in the cube color, so it is invisible on the faces. P1 paints that backing in a darker shade of the same token instead: the token mixed with black in 5% steps until white on it reaches 3:1 on every face (Go `#0093B8`, Rust `#A67A63`). The language tokens and the cube grammar are unchanged; the result is a thin darker outline around the white mark.

Limits: the keyline is 0.55 units wide, which is 0.37 px at 16 px, 0.55 px at 24 px and 1.47 px at 64 px. It sharpens the mark's edge from about 48 px up, but it does not fix 16 or 24 px. It also introduces a derived shade of the language color, which the maintainer should judge against the "color = implementation language" rule. Leaving Go and Rust as they are is a reasonable alternative, since the marks remain recognizable by shape at 24 px and up.

### P2. Enlarge the Docs and Showcase marks

Affected approved assets: `docs`, `showcase`.

Scale each mark about its own bounding-box center: Docs by 1.25, Showcase by 1.3. Both stay on the right face (at least 0.74 units from its edges) and pass `tests/test_glyph_seams.py`. Docs bars become 1.41 units thick with 1.2-unit gaps, so 24 px passes C2 and C3; 16 px is still below 1 px. The Showcase triangle grows to 4.9 × 6 units. This is the smallest change that addresses the "too small and displaced to the right" note from issue #23 for these two marks without moving them.

### Not proposed here

- Driver and MCP marks: their redesign is in progress in issue #23 (the maintainer selected the MCP "3-Way Router" direction; the Driver direction is still open). The replacements should be checked against C1 to C4, with C2 and C4 at 16 px in particular. This study does not adjust the current marks.
- Community: separating the figures needs at least about 0.75 units between the heads and bodies and between the figures for C3 at 32 px. That is a redraw of a mark approved on 2026-10-25, so it needs the maintainer's design direction first.
- Operator at 16 px: the six-spoke dial cannot resolve in 16 pixels at any stroke weight that still reads as a dial at 64 px. A simplified small-size variant would be a new asset, which is out of scope here.

## Usage guidance from the measurements

- From 32 px every role mark is recognizable (C4), but not every icon passes all four criteria: Go and Rust stay below 3:1 (C1) and Community's figures do not separate (C3) at any size up to 64 px.
- At 24 px, besides those failures, Driver, Showcase and Docs are marginal and the Operator spokes merge.
- At 16 px only the ORM, Cookbook, Benchmark and organization mark keep their role shape. Elsewhere the cube silhouette and language color carry the identity, and the role mark should not be relied on.

## Automated checks

`tests/test_legibility.py` (no extra dependencies, part of `python -m unittest discover -s tests`):

- Computes the white-mark contrast on each face shade parsed from the generated SVG for every repository and surface icon with a white mark, and fails if the set of tokens below 3:1 differs from the reviewed set `{go, rust}`. A self-test shows a JavaScript Driver would be flagged and a JavaScript ORM would not.
- Fails if any white stroke or white dot in a role mark is thinner than 1 viewBox unit (1 px at 24 px), with fill, stroke and stroke width inherited from enclosing groups (the MCP and Community dots inherit their white fill). Self-tests show a 0.6-unit stroke and 0.8-unit dots are flagged, directly set or inherited. Filled shapes such as the Docs bars are not measured by this check; the table above covers them.
