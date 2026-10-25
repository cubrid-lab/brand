# Provenance

## Selected repository icon direction

In October 2026 the maintainer supplied the [repository icon-system infographic](docs/studies/repository-icon-system-infographic.png) and directed that its cube-based Driver replace the previous Driver, with individual role icons generated from the same visual direction. The image is retained byte-for-byte as a visual reference. Numeric construction parameters live in [`tokens/geometry.json`](tokens/geometry.json); [`scripts/build.py`](scripts/build.py) reconstructs the family as original vector geometry and produces all checked-in SVGs.

The raster does not contain exact SVG paths or numerical stroke parameters. The generated vectors are an original reconstruction, not a pixel-exact extraction. The source image contains inconsistent language labels and presentation colors. Repository colors follow language tokens and the actual mapping: Drizzle is TypeScript, Benchmark is Neutral because it is multi-language, and Showcase is Neutral pending a stable implementation-language decision.

The prior **Connector Study / 02** Driver SVG and its parameters remain unchanged under [`provenance/connector-study-02/`](provenance/connector-study-02/). That study was previously selected and restored after an incorrect bootstrap polygon. It is now superseded by the maintainer's newer cube-based direction; it is preserved as historical evidence rather than silently overwritten.

The role glyphs were drawn with simple vector primitives. The Operator uses a generic six-spoke control dial, not a Kubernetes logo. No official CUBRID, language, or other third-party logo was copied into the symbols.

## Organization identity

The infographic also depicts a separate three-color CUBRID Lab cube and wordmark. Numeric face colors, comparison candidates, and scoped emblem approvals are recorded in [`tokens/organization.json`](tokens/organization.json). The approved emblem is generated under `dist/organization/`; two alternative mark candidates (`candidate-monochrome-cube.svg`, `candidate-hex-frame.svg`) and two wordmark lockups remain candidates under `studies/organization/`. They are separate from the Driver and ORM role symbols and tracked in [issue #3](https://github.com/cubrid-lab/brand/issues/3). System font fallbacks are used for the text; no font file is bundled. The original emblem study remains available at [the pre-approval revision](https://github.com/cubrid-lab/brand/blob/572addda0f5403a455c27ec742eacd315f9ff929/studies/organization/mark.svg).

## Review state

- Driver icon: the maintainer selected the cube-based direction, and its four variants are generated in `dist/icons/`.
- Python ORM, MCP, and Cookbook icons (`sqlalchemy-cubrid`, `cubrid-mcp-server`, `cubrid-cookbook-python`): explicitly approved by the maintainer on 2026-10-14 ([issue #6](https://github.com/cubrid-lab/brand/issues/6)) and generated in `dist/icons/`. This is a design approval only.
- Go Operator icon (`cubrid-kubernetes-operator`): selected for repository use by the maintainer on 2026-10-15 ([issue #6](https://github.com/cubrid-lab/brand/issues/6)) and generated in `dist/icons/`. The existing geometry and Go color token are unchanged. Legal review and the general visual-asset license remain pending.
- TypeScript, Go, and Rust ORM icons (`drizzle-cubrid`, `gorm-cubrid`, `sea-orm-cubrid`): explicitly approved by the maintainer on 2026-10-20 ([issue #6](https://github.com/cubrid-lab/brand/issues/6)) and generated in `dist/icons/` using the shared ORM role geometry and their respective language tokens. Legal review and the general visual-asset license remain pending.
- Other role symbols (`cubrid-benchmark`, `showcase`, `docs`, `community`): individual candidates are generated in `studies/icons/` and await explicit approval before release.
- Organization emblem: on 2026-10-15 the maintainer reviewed the three-color cube and answered “ㅇㅇ” (“yes”) to approval of both its design and organization-use rights. This authorizes its use as the CUBRID Lab organization avatar and profile mark only (issue #3). Deployment is verified separately from approval.
- Organization wordmark lockups: design and rights review pending (issue #3).
- Visual-asset redistribution license: pending.
- Trademark and legal clearance: pending.

## Seam backing change (issue #23)

On 2026-10-25 the generator gained a cube-colored backing under each role mark, clipped to the cube silhouette, so marks no longer cross transparent seams ([issue #23](https://github.com/cubrid-lab/brand/issues/23); construction in [`docs/GEOMETRY.md`](docs/GEOMETRY.md)). Glyph paths, colors and review statuses are unchanged. Approved assets whose rendering changes: the four Driver variants (`pycubrid`, `cubrid-client`, `cubrid-go`, `cubrid-rs`), `cubrid-mcp-server`, `cubrid-cookbook-python` and `cubrid-kubernetes-operator`; pending candidates `cubrid-benchmark` and `community` also change. `showcase` and `docs` gain the same markup but render identically, and the ORM icons are untouched. This replacement of approved `dist/` geometry requires the maintainer's design review on the pull request before merge; it does not approve or promote anything. Consumer READMEs pin immutable revisions and keep their current artwork until updated in their own repositories. The before/after review sheet is [`docs/studies/glyph-seams-before-after.png`](docs/studies/glyph-seams-before-after.png).

AI assistance was used to reconstruct the SVGs and prepare this documentation. Publication in this repository is not a grant of rights to use the visual assets.
