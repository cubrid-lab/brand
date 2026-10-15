# CUBRID Lab Brand

Canonical brand-system source for CUBRID Lab.

> CUBRID Lab is an independent, community-driven open-source initiative and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project. CUBRID is a trademark of its owner; the name is used here only to identify compatibility with the CUBRID database.

## Design system

- **Shape = technical role.** Nine role symbols share one 24×24 isometric construction grammar and use distinct internal marks.
- **Color = implementation language.** Every repository variant uses a language token; mixed-language repositories and non-repository surfaces use Neutral.

The maintainer selected the [cube-based infographic](docs/studies/repository-icon-system-infographic.png) to replace the former Driver drawing and build out the individual icon family. The [icon gallery](docs/ICON_GALLERY.md) previews all 15 generated variants and the separate organization-mark study. The [numerical construction](docs/GEOMETRY.md) documents the SVG reconstruction. The raster is a visual reference, not a source of generated geometry.

Current language and neutral tokens are defined in [`tokens/colors.json`](tokens/colors.json):

| Token | Color |
| --- | --- |
| Python | `#3776AB` |
| TypeScript | `#3178C6` |
| Go | `#00ADD8` |
| Rust | `#DEA384` |
| JavaScript | `#F7DF1E` |
| OCaml | `#A34CC3` |
| Neutral | `#6B7280` |

These are **CUBRID Lab design tokens**, not official CUBRID brand colors or claims about language brands. JavaScript and OCaml currently have no mapped repositories. The infographic's labels differ from the actual mappings for Drizzle, Benchmark, and Showcase; the registry records the implementation-language decisions.

## Repository and surface mapping

Machine-readable mappings live in [`registry/repositories.json`](registry/repositories.json). `dist/icons/` contains eight approved repository icons: the four Driver variants; the Python ORM (`sqlalchemy-cubrid`), MCP (`cubrid-mcp-server`), and Cookbook (`cubrid-cookbook-python`) icons selected on 2026-10-14; and the Go Operator (`cubrid-kubernetes-operator`) icon selected on 2026-10-15. The maintainer selections are recorded in [issue #6](https://github.com/cubrid-lab/brand/issues/6). The other five repository icons and two concept surfaces are generated under `studies/icons/` pending symbol approval. `docs` and `community` are not asserted to be repository names.

Role geometry is common across repositories with the same role. The six-spoke Operator control dial is an original generic mark and does not copy the Kubernetes logo or any other third-party logo.

See [Applying repository icons](docs/REPOSITORY_ICON_USAGE.md) for the shared README header, immutable asset URLs, documentation-site configuration, and rollout inventory.

## Organization identity

The [three-color organization-mark study](studies/organization/mark.svg) and its [horizontal](studies/organization/lockup-horizontal.svg) and [stacked](studies/organization/lockup-stacked.svg) lockups are separate from role icons. They are review candidates under [issue #3](https://github.com/cubrid-lab/brand/issues/3). The GitHub organization avatar and profile remain unchanged until design and rights review is recorded. The GitHub handle remains `cubrid-lab`.

## Source of truth

```text
tokens/              numeric geometry, language colors, organization study colors
registry/            repository and concept-surface mappings
scripts/             deterministic SVG generation
src/                 generated color-inheriting role templates
dist/icons/           generated approved repository icons
studies/icons/        generated individual symbol candidates (pending review)
studies/organization/ generated organization-identity candidates (pending review)
docs/                construction, gallery, and visual-reference study
provenance/          immutable superseded Connector Study / 02 reference
```

The old Driver SVG and numerical parameters remain under [`provenance/connector-study-02/`](provenance/connector-study-02/) as historical evidence. Do not edit generated SVG geometry directly.

## Build and verify

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
git diff --exit-code -- src dist studies/icons studies/organization
test -z "$(git ls-files --others --exclude-standard -- src dist studies/icons studies/organization)"
```

CI uses `python` on its Python 3.12 runner.

## Licensing and review status

Code in `scripts/` and `tests/` is MIT-licensed. Visual marks and generated brand assets are **not yet licensed for redistribution** while asset licensing and trademark review are pending. See [LICENSE](LICENSE), [BRAND_USAGE.md](BRAND_USAGE.md), and [PROVENANCE.md](PROVENANCE.md).

Design selection for repository icons does **not** mean trademark, non-infringement, or formal legal review is complete. The organization mark is still a candidate and must not be deployed as the organization avatar before its separate review.

Refs #3, #4, #6.
