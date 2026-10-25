# CUBRID Lab Brand

Canonical brand-system source for CUBRID Lab.

> CUBRID Lab is an independent, community-driven open-source initiative and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project. CUBRID is a trademark of its owner; the name is used here only to identify compatibility with the CUBRID database.

## Design system

- **Shape = technical role.** Nine role symbols share one 24×24 isometric construction grammar and use distinct internal marks.
- **Color = implementation language.** Every repository variant uses a language token; mixed-language repositories and non-repository surfaces use Neutral.

The maintainer selected the [cube-based infographic](docs/studies/repository-icon-system-infographic.png) recorded in the [design review proposal](docs/REPOSITORY_ICON_SYSTEM_PROPOSAL.md) to replace the former Driver drawing and build out the individual icon family. The [icon gallery](docs/ICON_GALLERY.md) previews all 15 generated variants, the separate organization emblem, and wordmark studies. The [numerical construction](docs/GEOMETRY.md) documents the SVG reconstruction. The raster is a visual reference, not a source of generated geometry.

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

Machine-readable mappings live in [`registry/repositories.json`](registry/repositories.json). `dist/icons/` contains all fifteen approved icons: the four Driver variants; the Python ORM (`sqlalchemy-cubrid`), MCP (`cubrid-mcp-server`), and Cookbook (`cubrid-cookbook-python`) icons selected on 2026-10-14; the Go Operator (`cubrid-kubernetes-operator`) icon selected on 2026-10-15; the TypeScript, Go, and Rust ORM (`drizzle-cubrid`, `gorm-cubrid`, `sea-orm-cubrid`) icons selected on 2026-10-20; and the Benchmark (`cubrid-benchmark`) and Showcase (`showcase`) repository icons and the Docs (`docs`) and Community (`community`) concept-surface icons approved on 2026-10-25. The maintainer selections are recorded in [issue #6](https://github.com/cubrid-lab/brand/issues/6). No repository or surface icon is currently pending symbol approval, so `studies/icons/` is empty. `docs` and `community` are not asserted to be repository names.

Role geometry is common across repositories with the same role. The six-spoke Operator control dial is an original generic mark and does not copy the Kubernetes logo or any other third-party logo.

See [Applying repository icons](docs/REPOSITORY_ICON_USAGE.md) for the shared README header, immutable asset URLs, documentation-site configuration, and rollout inventory.

## Organization identity

The [three-color organization emblem](dist/organization/mark.svg) is separate from role icons. On 2026-10-15 the maintainer approved its design and use as the CUBRID Lab organization avatar and profile mark, recorded in [issue #3](https://github.com/cubrid-lab/brand/issues/3). The [horizontal](studies/organization/lockup-horizontal.svg) and [stacked](studies/organization/lockup-stacked.svg) wordmark lockups remain review candidates. General redistribution licensing and independent legal/trademark clearance remain pending. See [Organization mark usage](docs/ORGANIZATION_MARK_USAGE.md) for the scoped approval and rollout. The GitHub handle remains `cubrid-lab`.

## Source of truth

```text
tokens/              numeric geometry, language colors, scoped organization approval
registry/            repository and concept-surface mappings
scripts/             deterministic SVG generation
src/                 generated color-inheriting role templates
dist/icons/           generated approved repository icons
dist/organization/    generated organization emblem approved for own-organization use
studies/icons/        generated individual symbol candidates (pending review; currently none)
studies/organization/ generated organization mark and wordmark candidates (pending review)
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

The build removes only stale copies of its own outputs: the SVG names derived from `registry/repositories.json` (repositories and surfaces, in both `dist/icons/` and `studies/icons/`) and from the organization emblem, candidates, and lockups. When an asset changes review status, its copy in the previous location is removed. Any other SVG in `dist/icons/`, `studies/icons/`, `dist/organization/`, or `studies/organization/` is never deleted: the build reports it as unmanaged and exits with status 1, so CI fails until it is removed or moved elsewhere. A repository dropped from the registry leaves an unmanaged SVG to delete by hand.

## Licensing and review status

Code in `scripts/` and `tests/` is MIT-licensed. Visual marks and generated brand assets are **not yet licensed for redistribution** while asset licensing and trademark review are pending. See [LICENSE](LICENSE), [BRAND_USAGE.md](BRAND_USAGE.md), and [PROVENANCE.md](PROVENANCE.md).

Design selection for repository icons does **not** mean trademark, non-infringement, or formal legal review is complete. The organization emblem's scoped design and own-organization-use approval does not broaden the visual-asset redistribution license or approve the wordmark candidates.

Refs #3, #4, #6.
