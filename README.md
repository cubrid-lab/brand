<p align="center">
  <img src="dist/organization/mark.svg" width="96" alt="CUBRID Lab geometric organization emblem">
</p>

# CUBRID Lab Brand

The visual identity and source of truth for **CUBRID Lab** — a geometric icon family for database drivers, ORMs, developer tools, and community projects.

**[Browse the icon gallery](docs/ICON_GALLERY.md)** · **[Use an icon](docs/REPOSITORY_ICON_USAGE.md)** · **[Brand usage and rights](BRAND_USAGE.md)** · **[How icons are built](docs/GEOMETRY.md)**

> CUBRID Lab is an independent, community-driven open-source initiative and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project. CUBRID is a trademark of its owner; the name is used here only to identify compatibility with the CUBRID database.

## Explore the identity

The **organization emblem** is the approved three-color cube. Repository icons belong to the same geometric family, but each represents a **technical role**, not the organization itself.

| Driver · `pycubrid` | ORM · `sqlalchemy-cubrid` | AI tools · `cubrid-mcp-server` | Examples · `cubrid-cookbook-python` |
|:---:|:---:|:---:|:---:|
| <img src="dist/icons/pycubrid.svg" width="76" alt="Current pycubrid icon"> | <img src="dist/icons/sqlalchemy-cubrid.svg" width="76" alt="Current SQLAlchemy CUBRID icon"> | <img src="dist/icons/cubrid-mcp-server.svg" width="76" alt="Current CUBRID MCP icon"> | <img src="dist/icons/cubrid-cookbook-python.svg" width="76" alt="Current CUBRID Cookbook icon"> |

**[See every approved repository icon and concept-surface icon](docs/ICON_GALLERY.md)**. The gallery also identifies studies and shows small-size previews. Current published artwork is not necessarily the final design: the Driver/ORM directions are being refined in [#30](https://github.com/cubrid-lab/brand/issues/30), and role-glyph visual improvements are tracked in [#23](https://github.com/cubrid-lab/brand/issues/23).

## How the brand system works

- **Shape = technical role.** Icons follow a shared **24 × 24 isometric construction grammar**. A Driver, ORM, MCP server, and Cookbook have different silhouettes.
- **Color = implementation language.** Repositories with the same technical role share geometry, while their language determines the color. Python currently uses **Python Blue `#3776AB`**; other colors are maintained in [`tokens/colors.json`](tokens/colors.json).
- **One generated source of truth.** Approved assets in `dist/` are generated from the [registry](registry/repositories.json), numeric [geometry tokens](tokens/geometry.json), and [build script](scripts/build.py). Edit the generator, not generated SVGs.
- **Organization and role symbols stay separate.** Do not substitute a Driver/ORM icon for the CUBRID Lab emblem.

See the [construction specification](docs/GEOMETRY.md), [original visual-study rationale](docs/REPOSITORY_ICON_SYSTEM_PROPOSAL.md), and [design provenance](PROVENANCE.md) for details.

## Use an approved icon

For **CUBRID Lab-owned repositories**, use only the mapped SVGs and placements authorized under [brand usage and rights](BRAND_USAGE.md), with a **commit-pinned URL** as described in the [icon usage guide](docs/REPOSITORY_ICON_USAGE.md). Icon design approval alone does not authorize every use. For example, a first-party `pycubrid` README header may use:

```html
<p align="center">
  <a href="https://github.com/cubrid-lab/brand">
    <img src="https://raw.githubusercontent.com/cubrid-lab/brand/bfb1871c8856d59dd60eb6276328465a7ab03ac7/dist/icons/pycubrid.svg" alt="pycubrid icon" width="120">
  </a>
</p>
```

This example pins an existing published revision; when integrating newly approved artwork, select its reviewed commit. **Design approval does not grant general rights to reuse, modify, or redistribute icons.** Read [brand usage and rights](BRAND_USAGE.md) before embedding assets on a new surface, especially outside CUBRID Lab. The [organization emblem](dist/organization/mark.svg) has separate approval and usage rules.

## Organization identity

The [three-color organization emblem](dist/organization/mark.svg) is separate from role icons. On 2026-10-15 the maintainer approved its design and use as the CUBRID Lab organization avatar and profile mark, recorded in [issue #3](https://github.com/cubrid-lab/brand/issues/3). On 2026-10-25 the maintainer approved the design and own-organization use of the [horizontal](dist/organization/lockup-horizontal.svg) and [stacked](dist/organization/lockup-stacked.svg) wordmark lockups, which also have [dark-background variants](dist/organization/lockup-horizontal-dark.svg) ([stacked](dist/organization/lockup-stacked-dark.svg)). General redistribution licensing and independent legal/trademark clearance remain pending. See [Organization mark usage](docs/ORGANIZATION_MARK_USAGE.md) for the scoped approval and rollout. The GitHub handle remains `cubrid-lab`.

## Find the source files

| Path | Purpose |
| --- | --- |
| [`dist/icons/`](dist/icons/) | Currently approved repository and concept-surface icons |
| [`dist/organization/`](dist/organization/) | Approved organization emblem and wordmark lockups (light and dark) |
| [`studies/`](studies/) | Candidate artwork and visual review references (not approved for distribution) |
| [`registry/repositories.json`](registry/repositories.json) | Authoritative repository, language, and role mapping |
| [`tokens/`](tokens/) | Geometry, language colors, and organization construction |
| [`scripts/build.py`](scripts/build.py) | Deterministic SVG generation |
| [`docs/ICON_GALLERY.md`](docs/ICON_GALLERY.md) | Complete visual inventory and size previews |
| [`provenance/`](provenance/) | Historical/superseded design references |

## Build and verify

Run from the repository root with Python 3.12 (the version used in CI):

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
git diff --exit-code -- src dist studies/icons studies/organization
test -z "$(git ls-files --others --exclude-standard -- src dist studies/icons studies/organization)"
```

The generator reports unmanaged SVGs rather than silently deleting them. Details, contribution expectations, and approval boundaries are in [AGENTS.md](AGENTS.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Licensing and review status

Code in `scripts/` and `tests/` is MIT-licensed. Visual marks and generated brand assets are **not licensed for redistribution**: on 2026-10-25 the maintainer decided not to offer a visual-asset license for now, and all rights are reserved. Trademark review is still pending. See [LICENSE](LICENSE), [BRAND_USAGE.md](BRAND_USAGE.md), and [PROVENANCE.md](PROVENANCE.md).

CUBRID Lab's own repositories may show their approved icons in the README and on their documentation sites by commit-pinned URL, without copying or modifying them. Forks and mirrors may keep that link in an unmodified README. No other embedding, copying, modification or redistribution is permitted. [Repository icon use](BRAND_USAGE.md#repository-icon-use) lists each case and the reviews still pending.

Design selection for repository icons does **not** mean trademark, non-infringement, or formal legal review is complete. The organization emblem's scoped design and own-organization-use approval and the wordmark lockups' design and own-organization-use approval do not broaden the visual-asset redistribution license.

Related: [organization mark and wordmark #3](https://github.com/cubrid-lab/brand/issues/3), [symbol approvals #6](https://github.com/cubrid-lab/brand/issues/6), [README usability #20](https://github.com/cubrid-lab/brand/issues/20).
