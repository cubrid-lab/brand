# Brand usage and legal status

## Independence

CUBRID Lab is independently maintained and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project.

CUBRID is a trademark of its owner. References to CUBRID identify compatibility with the CUBRID database.

## Current status

The repository role icons in this repository are original CUBRID Lab geometric reconstructions based on a maintainer-supplied visual study. Design selection does **not** constitute:

- trademark clearance,
- a non-infringement opinion,
- permission to imply endorsement,
- permission to modify or redistribute any official CUBRID trademark asset.

On 2026-10-15 the maintainer explicitly approved the three-color organization emblem's design and rights for use as the CUBRID Lab organization avatar and profile mark, recorded in [issue #3](https://github.com/cubrid-lab/brand/issues/3). This authorization covers that emblem and those organization surfaces only. The horizontal and stacked wordmark lockups remain review candidates.

## Visual-asset license status

The MIT license in this repository covers only `scripts/` and `tests/`. The names, marks, generated SVGs, and other visual brand assets are **not yet licensed for redistribution** while the maintainers review asset licensing and trademark implications.

Publication in this public repository should not be interpreted as a grant of trademark rights or a general license to reuse the visual marks. A public URL, a merged pull request or a symbol approval does not grant one either.

CUBRID Lab's own repositories may embed their approved repository icons by commit-pinned URL, within the limits described in [Repository icon use](#repository-icon-use). That is an internal authorization, not a license, and it does not extend to anyone else.

The emblem's recorded own-organization-use authorization is separate from this pending general redistribution license. It is not a statement that independent legal or trademark clearance has been completed.

## Repository icon use

This section covers the approved repository-role and concept-surface icons in
`dist/icons/` (the classes are listed in the
[registry](registry/repositories.json)). The organization emblem follows
[Organization mark usage](docs/ORGANIZATION_MARK_USAGE.md). Files under
`studies/`, `src/` and `provenance/` are not approved for use anywhere.

Symbol approval (issue #6) is a design decision: it chooses which drawing
represents a role. It does not grant a license, clear trademarks or settle
creator rights. Only the uses marked **Permitted** below are authorized; they
are an internal maintainer decision for CUBRID Lab's own repositories, not a
license. Everything else stays unlicensed until the maintainers record a
decision.

### Inside CUBRID Lab organization repositories

A CUBRID Lab repository is one owned by the `cubrid-lab` GitHub organization.

| Use | Status |
| --- | --- |
| Embed the repository's own mapped icon, by its commit-pinned `raw.githubusercontent.com` URL, in that repository's README and translated READMEs: the four Driver variants, `sqlalchemy-cubrid`, `cubrid-mcp-server`, `cubrid-cookbook-python`, `cubrid-kubernetes-operator`, `drizzle-cubrid`, `gorm-cubrid` and `sea-orm-cubrid` | **Permitted** (rollout scope agreed in [issue #8](https://github.com/cubrid-lab/brand/issues/8) and its per-repository rollout issues listed in [Applying repository icons](docs/REPOSITORY_ICON_USAGE.md#rollout-inventory); consumer pin instructions recorded in [issue #6](https://github.com/cubrid-lab/brand/issues/6)) |
| Use the same pinned URL as that repository's documentation-site logo and favicon: `pycubrid`, `sqlalchemy-cubrid`, `cubrid-mcp-server`, `cubrid-cookbook-python`, `drizzle-cubrid`, `gorm-cubrid` and `sea-orm-cubrid` | **Permitted** (the Python mappings were kept under issue #8; the 2026-10-20 pin instruction in issue #6 names documentation surfaces for the three ORM repositories) |
| The same documentation-site use for `cubrid-client`, `cubrid-go`, `cubrid-rs` and `cubrid-kubernetes-operator` | **Pending maintainer confirmation.** Their recorded rollout covers the README only. |
| Embed `cubrid-benchmark` or `showcase` in its repository, or `docs` or `community` on a CUBRID Lab documentation or community surface | **Pending maintainer confirmation.** The 2026-10-25 record in issue #6 approves these symbols only and leaves usage to issue #19. |
| CUBRID Lab's own package pages (for example PyPI) rendering a permitted README with its pinned image link | **Permitted**; the image is still loaded from this repository |
| Commit a copy of an SVG into another repository, package or build output | **Not authorized yet.** Link the pinned URL. Ask in this repository first if a copy is needed. |
| Modify, recolor, crop, combine with text, or rasterize a role icon | **Not authorized.** Change the generator here so the result goes through design review. |
| Use another repository's icon, or a role icon as the organization avatar or site logo | **Not permitted** |
| Link a `main` branch, study or candidate URL | **Not permitted** |

Follow [Applying repository icons](docs/REPOSITORY_ICON_USAGE.md) for layout,
alt text and pinning. The README image links to
`https://github.com/cubrid-lab/brand`; that link is the attribution for
first-party use.

### Outside CUBRID Lab

This covers everyone else, including forks, mirrors, articles, talks, other
projects and other organizations.

| Use | Status |
| --- | --- |
| Link to this repository or to a CUBRID Lab project page in text | Allowed; a hyperlink does not use the icon |
| Embed (hotlink) an icon in your own page, README or slides | **No permission granted.** Pending the review below. |
| Copy or redistribute an SVG, alone or in a package, theme or icon set | **Not licensed** |
| Modify an icon or make derivative artwork | **Not licensed** |
| Keep the pinned image link of an unmodified CUBRID Lab README in a fork or mirror | **Undecided.** No permission is recorded; this is a pending decision below. |

This policy grants nothing beyond the table above, and it does not decide what
the law allows without permission in any jurisdiction. To ask for a use, open
an issue in [cubrid-lab/brand](https://github.com/cubrid-lab/brand/issues).
Only a maintainer decision recorded there authorizes it. Any such decision
sets its own attribution terms.

### Never permitted

- Implying that CUBRID Corporation or the official CUBRID project endorses,
  sponsors or is affiliated with anything that uses an icon.
- Implying that CUBRID Lab maintains or endorses a project it does not
  maintain, for example by showing a role icon on that project.
- Combining a role icon with an official CUBRID logo or wordmark.
- Using a role icon as the CUBRID Lab organization logo or avatar.

### Pending decisions

The rules above are the maintainers' position while these items remain open:

1. confirmation of first-party use for `cubrid-benchmark`, `showcase`, `docs`
   and `community`, and of documentation-site use for `cubrid-client`,
   `cubrid-go`, `cubrid-rs` and `cubrid-kubernetes-operator`,
2. whether forks and mirrors may keep the pinned image link of an unmodified
   CUBRID Lab README,
3. a visual-asset license (or a decision not to offer one) for third-party
   embedding, copying, modification and redistribution,
4. creator-rights confirmation for the AI-assisted reconstruction recorded in
   [PROVENANCE.md](PROVENANCE.md),
5. the confusing-similarity and trademark items listed below.

Until those are recorded, third-party uses stay unlicensed and first-party
use stays limited to the permitted rows above.

## Third-party marks and language identifiers

Language colors are internal visual tokens. The generated icons do not include Python, TypeScript, Go, Rust, Kubernetes, or other third-party logos. The Operator's six-spoke control dial is not the Kubernetes logo.

## Broader use and remaining review

The scoped emblem authorization above does not claim that independent similarity or trademark searches were performed. Before broader use or granting a general visual-asset license, maintainers should complete and record:

1. confusing-similarity review,
2. relevant trademark searches,
3. confirmation of the intended use of the CUBRID name,
4. asset-license and creator-rights approval,
5. final human design review of any additional identity assets, including the pending wordmark lockups.

This document is project governance, not legal advice.
