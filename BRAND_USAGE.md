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

On 2026-10-15 the maintainer explicitly approved the three-color organization emblem's design and rights for use as the CUBRID Lab organization avatar and profile mark, recorded in [issue #3](https://github.com/cubrid-lab/brand/issues/3). This authorization covers that emblem and those organization surfaces only.

On 2026-10-25 the maintainer approved the design and CUBRID Lab's own organization use of the horizontal and stacked wordmark lockups, with light- and dark-background variants, recorded in [issue #3](https://github.com/cubrid-lab/brand/issues/3). Own organization use means showing an unmodified lockup by commit-pinned URL on CUBRID Lab surfaces, as described in [Organization mark usage](docs/ORGANIZATION_MARK_USAGE.md#wordmark-lockups). It is not a license, and it is not a legal or trademark clearance.

## Visual-asset license status

The MIT license in this repository covers only `scripts/` and `tests/`. The names, marks, generated SVGs, and other visual brand assets are **not licensed for redistribution**. On 2026-10-25 the maintainer decided not to offer a visual-asset license for now; all rights in them are reserved (see [Maintainer decisions](#maintainer-decisions-2026-10-25)). Trademark review is still pending.

Publication in this public repository should not be interpreted as a grant of trademark rights or a general license to reuse the visual marks. A public URL, a merged pull request or a symbol approval does not grant one either.

CUBRID Lab's own repositories may show their approved repository icons by commit-pinned URL, and forks and mirrors may keep that link in an unmodified README, within the limits described in [Repository icon use](#repository-icon-use). These are recorded permissions, not a license.

The emblem's and the wordmark lockups' recorded own-organization-use authorizations are separate from the repository icon decisions and do not create a redistribution license. They are not a statement that independent legal or trademark clearance has been completed.

## Repository icon use

This section covers the approved repository-role and concept-surface icons in
`dist/icons/` (the classes are listed in the
[registry](registry/repositories.json)). The organization emblem follows
[Organization mark usage](docs/ORGANIZATION_MARK_USAGE.md). Files under
`studies/`, `src/` and `provenance/` are not approved for use anywhere.

Symbol approval (issue #6) is a design decision: it chooses which drawing
represents a role. It does not grant a license or clear trademarks.

### Maintainer decisions (2026-10-25)

On 2026-10-25 the maintainer (@yeongseon) decided the following for issue #19:

1. Every approved icon in `dist/icons/` may be shown by its own CUBRID Lab
   repository, in its README and as its documentation-site logo and favicon,
   only through a commit-pinned `raw.githubusercontent.com` URL. The `docs` and
   `community` icons follow the same rule on CUBRID Lab documentation and
   community surfaces. Copying, modifying, rasterizing and using another
   repository's icon stay not permitted.
2. Forks and mirrors may keep the pinned image link in an unmodified CUBRID Lab
   README. Modification and redistribution remain unlicensed.
3. No visual-asset license is offered for now. All rights in the icons are
   reserved; the pinned-link uses in this section are the only permitted uses.
   [LICENSE](LICENSE) is unchanged.
4. The maintainer confirmed that the AI-assisted icon reconstruction is the
   maintainer's original work; see [PROVENANCE.md](PROVENANCE.md#creator-rights).

These are permissions recorded by the maintainer, not a license, and not a
legal or trademark clearance.

### Inside CUBRID Lab organization repositories

A CUBRID Lab repository is one owned by the `cubrid-lab` GitHub organization.

| Use | Status |
| --- | --- |
| Show the repository's own approved icon, by its commit-pinned `raw.githubusercontent.com` URL, in that repository's README and translated READMEs (all 13 repository icons) | **Permitted** (decision 1) |
| Use the same pinned URL as that repository's documentation-site logo and favicon | **Permitted** (decision 1) |
| Show the `docs` or `community` icon by its pinned URL on a CUBRID Lab documentation or community surface | **Permitted** (decision 1) |
| CUBRID Lab's own package pages (for example PyPI) rendering a README with its pinned image link | **Permitted**; the image is still loaded from this repository |
| Commit a copy of an SVG into another repository, package or build output | **Not permitted** (decision 1). Link the pinned URL. |
| Modify, recolor, crop, combine with text, or rasterize an icon | **Not permitted** (decision 1). Change the generator here so the result goes through design review. |
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
| Keep the pinned image link of an unmodified CUBRID Lab README in a fork or mirror | **Permitted** (decision 2) |
| Embed (hotlink) an icon in your own page, README or slides | **Not permitted**; no license is offered (decision 3) |
| Copy or redistribute an SVG, alone or in a package, theme or icon set | **Not licensed** (decisions 2 and 3) |
| Modify an icon or make derivative artwork | **Not licensed** (decisions 2 and 3) |

This policy grants nothing beyond the tables above, and it does not decide
what the law allows without permission in any jurisdiction. To ask for a use,
open an issue in [cubrid-lab/brand](https://github.com/cubrid-lab/brand/issues).
Only a maintainer decision recorded there authorizes it. Any such decision
sets its own attribution terms.

### Never permitted

- Implying that CUBRID Corporation or the official CUBRID project endorses,
  sponsors or is affiliated with anything that uses an icon.
- Implying that CUBRID Lab maintains or endorses a project it does not
  maintain, for example by showing a role icon on that project.
- Combining a role icon with an official CUBRID logo or wordmark.
- Using a role icon as the CUBRID Lab organization logo or avatar.

### Still pending

A person still has to carry out and record two checks; no clearance is
claimed until then:

1. a confusing-similarity review of the icons,
2. relevant trademark searches.

Both are also listed under [Broader use and remaining review](#broader-use-and-remaining-review).

## Third-party marks and language identifiers

Language colors are internal visual tokens. The generated icons do not include Python, TypeScript, Go, Rust, Kubernetes, or other third-party logos. The Operator's six-spoke control dial is not the Kubernetes logo.

## Broader use and remaining review

The scoped emblem authorization above does not claim that independent similarity or trademark searches were performed. Before broader use or granting a general visual-asset license, maintainers should complete and record:

1. confusing-similarity review,
2. relevant trademark searches,
3. confirmation of the intended use of the CUBRID name,
4. asset-license and creator-rights approval (decided for the repository icons on 2026-10-25: no license is offered and the maintainer confirmed creator rights; the wordmark lockups' design and own-organization use were approved on 2026-10-25, but their creator rights and any license remain open under issue #3),
5. final human design review of any additional identity assets.

This document is project governance, not legal advice.
