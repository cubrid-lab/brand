# Provenance

## Selected repository icon direction

In October 2026 the maintainer supplied the [repository icon-system infographic](docs/studies/repository-icon-system-infographic.png) and directed that its cube-based Driver replace the previous Driver, with individual role icons generated from the same visual direction. The image is retained byte-for-byte as a visual reference. Numeric construction parameters live in [`tokens/geometry.json`](tokens/geometry.json); [`scripts/build.py`](scripts/build.py) reconstructs the family as original vector geometry and produces all checked-in SVGs.

The raster does not contain exact SVG paths or numerical stroke parameters. The generated vectors are an original reconstruction, not a pixel-exact extraction. The source image contains inconsistent language labels and presentation colors. Repository colors follow language tokens and the actual mapping: Drizzle is TypeScript, Benchmark is Neutral because it is multi-language, and Showcase is Neutral pending a stable implementation-language decision.

The prior **Connector Study / 02** Driver SVG and its parameters remain unchanged under [`provenance/connector-study-02/`](provenance/connector-study-02/). That study was previously selected and restored after an incorrect bootstrap polygon. It is now superseded by the maintainer's newer cube-based direction; it is preserved as historical evidence rather than silently overwritten.

The role glyphs were drawn with simple vector primitives. The Operator uses a generic six-spoke control dial, not a Kubernetes logo. No official CUBRID, language, or other third-party logo was copied into the symbols.

## Organization identity

The infographic also depicts a separate three-color CUBRID Lab cube and wordmark. Numeric face colors are recorded in [`tokens/organization.json`](tokens/organization.json), and the emblem plus two lockups are generated under `studies/organization/`. They are identity candidates for [issue #3](https://github.com/cubrid-lab/brand/issues/3), separate from the Driver role symbol. System font fallbacks are used for the text; no font file is bundled.

## Review state

- Driver icon: the maintainer selected the cube-based direction, and its four variants are generated in `dist/icons/`.
- Python ORM, MCP, and Cookbook icons (`sqlalchemy-cubrid`, `cubrid-mcp-server`, `cubrid-cookbook-python`): explicitly approved by the maintainer on 2026-10-14 ([issue #6](https://github.com/cubrid-lab/brand/issues/6)) and generated in `dist/icons/`. This is a design approval only.
- Other role symbols: individual candidates are generated in `studies/icons/` and await explicit approval before release.
- Organization emblem and wordmark: design and rights review pending (issue #3); no organization avatar or profile change has been made.
- Visual-asset redistribution license: pending.
- Trademark and legal clearance: pending.

AI assistance was used to reconstruct the SVGs and prepare this documentation. Publication in this repository is not a grant of rights to use the visual assets.
