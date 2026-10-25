# Provenance

## Selected repository icon direction

In October 2026 the maintainer supplied the [repository icon-system infographic](docs/studies/repository-icon-system-infographic.png) and directed that its cube-based Driver replace the previous Driver, with individual role icons generated from the same visual direction. The image is retained byte-for-byte as a visual reference. Numeric construction parameters live in [`tokens/geometry.json`](tokens/geometry.json); [`scripts/build.py`](scripts/build.py) reconstructs the family as original vector geometry and produces all checked-in SVGs.

The raster does not contain exact SVG paths or numerical stroke parameters. The generated vectors are an original reconstruction, not a pixel-exact extraction. The source image contains inconsistent language labels and presentation colors. Repository colors follow language tokens and the actual mapping: Drizzle is TypeScript, Benchmark is Neutral because it is multi-language, and Showcase is Neutral pending a stable implementation-language decision.

The prior **Connector Study / 02** Driver SVG and its parameters remain unchanged under [`provenance/connector-study-02/`](provenance/connector-study-02/). That study was previously selected and restored after an incorrect bootstrap polygon. It is now superseded by the maintainer's newer cube-based direction; it is preserved as historical evidence rather than silently overwritten.

The role glyphs were drawn with simple vector primitives. The Operator uses a generic six-spoke control dial, not a Kubernetes logo. No official CUBRID, language, or other third-party logo was copied into the symbols.

## Organization identity

The infographic also depicts a separate three-color CUBRID Lab cube and wordmark. Numeric face colors, comparison candidates, wordmark text colors, and the scoped emblem and wordmark approvals are recorded in [`tokens/organization.json`](tokens/organization.json). The approved emblem and the approved wordmark lockups (horizontal and stacked, each with a dark-background variant) are generated under `dist/organization/`; two alternative mark candidates (`candidate-monochrome-cube.svg`, `candidate-hex-frame.svg`) remain candidates under `studies/organization/`. They are separate from the Driver and ORM role symbols and tracked in [issue #3](https://github.com/cubrid-lab/brand/issues/3). System font fallbacks are used for the text; no font file is bundled. The original emblem study remains available at [the pre-approval revision](https://github.com/cubrid-lab/brand/blob/572addda0f5403a455c27ec742eacd315f9ff929/studies/organization/mark.svg).

## Review state

This section is the history of approval decisions. The current status of each asset is in [`registry/repositories.json`](registry/repositories.json) and [`tokens/organization.json`](tokens/organization.json).

- Driver icon: the maintainer selected the cube-based direction, and its four variants are generated in `dist/icons/`.
- Python ORM, MCP, and Cookbook icons (`sqlalchemy-cubrid`, `cubrid-mcp-server`, `cubrid-cookbook-python`): explicitly approved by the maintainer on 2026-10-14 ([issue #6](https://github.com/cubrid-lab/brand/issues/6)) and generated in `dist/icons/`. This is a design approval only.
- Go Operator icon (`cubrid-kubernetes-operator`): selected for repository use by the maintainer on 2026-10-15 ([issue #6](https://github.com/cubrid-lab/brand/issues/6)) and generated in `dist/icons/`. The existing geometry and Go color token are unchanged. Legal review remains pending; no visual-asset license is offered.
- TypeScript, Go, and Rust ORM icons (`drizzle-cubrid`, `gorm-cubrid`, `sea-orm-cubrid`): explicitly approved by the maintainer on 2026-10-20 ([issue #6](https://github.com/cubrid-lab/brand/issues/6)) and generated in `dist/icons/` using the shared ORM role geometry and their respective language tokens. Legal review remains pending; no visual-asset license is offered.
- Benchmark and Showcase repository icons (`cubrid-benchmark`, `showcase`) and Docs and Community concept-surface icons (`docs`, `community`): explicitly approved by the maintainer on 2026-10-25 after reviewing the seam contact sheet [`docs/studies/glyph-seams-before-after.png`](docs/studies/glyph-seams-before-after.png) at commit [`9dcb65d`](https://github.com/cubrid-lab/brand/commit/9dcb65d19a2311a3593bcfc366fa091c2ad22e9f) ([issue #6](https://github.com/cubrid-lab/brand/issues/6)), and generated in `dist/icons/` with the reviewed geometry and the Neutral token. This is a symbol (design) approval only. The usage policy was decided by the maintainer on 2026-10-25 in [issue #19](https://github.com/cubrid-lab/brand/issues/19) and is recorded in [Repository icon use](BRAND_USAGE.md#repository-icon-use); similarity and trademark searches remain pending.
- Driver, ORM and MCP role redesign: on 2026-10-25 the maintainer (@yeongseon) reviewed the [family](docs/studies/role-redesign-30/family.png) and [contact](docs/studies/role-redesign-30/contact-sheet.png) sheets at [`1c344fb`](https://github.com/cubrid-lab/brand/commit/1c344fb283fc29284fb543a4e8f1109c620c1b17) and selected `driver-vertical-stack`, `orm-lateral-plates` and `mcp-router-hub` ([issue #30](https://github.com/cubrid-lab/brand/issues/30), [issue #23](https://github.com/cubrid-lab/brand/issues/23), [PR #37](https://github.com/cubrid-lab/brand/pull/37)). See [Driver, ORM and MCP role redesign](#driver-orm-and-mcp-role-redesign-issues-30-and-23).
- No role symbol is currently pending; `studies/icons/` is empty.
- Organization emblem: on 2026-10-15 the maintainer reviewed the three-color cube and answered “ㅇㅇ” (“yes”) to approval of both its design and organization-use rights. This authorizes its use as the CUBRID Lab organization avatar and profile mark only (issue #3). Deployment is verified separately from approval.
- Organization wordmark lockups: on 2026-10-25 the maintainer (@yeongseon) reviewed renders of `lockup-horizontal.svg` on a light background and `lockup-stacked.svg` on a dark background at [`5229cf4`](https://github.com/cubrid-lab/brand/commit/5229cf4387218f640636e8ba3ac208067bdc7fe6) and approved the horizontal and stacked lockup design, with the tagline “Open Source for a More Connected World”, as-is on light backgrounds, for CUBRID Lab's own organization use (issue #3). The same decision asked for dark-background variants because the fixed navy text nearly vanished on the dark render; `lockup-horizontal-dark.svg` and `lockup-stacked-dark.svg` keep the emblem, layout and font stack and change only the text colors (`#F0F6FC` and `#A8C1E8`, recorded in `tokens/organization.json`). Their renders and text contrast are in [`docs/studies/wordmark-lockups.md`](docs/studies/wordmark-lockups.md) for the maintainer's review on the pull request. This is a design and own-organization-use approval only: no license is offered, and it is not a confusing-similarity review, trademark search or legal clearance. Creator rights of the lockups have not been confirmed separately.
- Visual-asset redistribution license: not offered for now; all rights reserved (maintainer decision, 2026-10-25, [issue #19](https://github.com/cubrid-lab/brand/issues/19)).
- Creator rights of the repository icons: confirmed by the maintainer on 2026-10-25 (see [Creator rights](#creator-rights)).
- Confusing-similarity review, trademark searches, and legal clearance: pending.

## Creator rights

On 2026-10-25 the maintainer (@yeongseon) confirmed, for [issue #19](https://github.com/cubrid-lab/brand/issues/19), that the AI-assisted reconstruction of the repository icons is the maintainer's original work. The confirmation covers the role geometry in `src/` and the generated repository and concept-surface icons in `dist/icons/`, built from the maintainer-supplied infographic as described above. It does not cover the organization emblem or wordmark lockups (issue #3), and it is not a confusing-similarity review, trademark search, or legal clearance; those remain pending.

## Seam backing change (issue #23)

On 2026-10-25 the generator gained a cube-colored backing under each role mark, clipped to the cube silhouette, so marks no longer cross transparent seams ([issue #23](https://github.com/cubrid-lab/brand/issues/23); construction in [`docs/GEOMETRY.md`](docs/GEOMETRY.md)). Glyph paths, colors and review statuses are unchanged. Approved assets whose rendering changes: the four Driver variants (`pycubrid`, `cubrid-client`, `cubrid-go`, `cubrid-rs`), `cubrid-mcp-server`, `cubrid-cookbook-python` and `cubrid-kubernetes-operator`; pending candidates `cubrid-benchmark` and `community` also change. `showcase` and `docs` gain the same markup but render identically, and the ORM icons are untouched. This replacement of approved `dist/` geometry requires the maintainer's design review on the pull request before merge; it does not approve or promote anything. Consumer READMEs pin immutable revisions and keep their current artwork until updated in their own repositories. The before/after review sheet is [`docs/studies/glyph-seams-before-after.png`](docs/studies/glyph-seams-before-after.png).

## Small-size enlargement of Docs and Showcase (issue #21)

On 2026-10-25 the maintainer reviewed the small-size legibility study ([`docs/studies/small-size-legibility.md`](docs/studies/small-size-legibility.md), review sheet [`proposal-before-after.png`](docs/studies/small-size-legibility/proposal-before-after.png), study at commit [`c3f2936`](https://github.com/cubrid-lab/brand/commit/c3f2936)) and approved proposal P2: the Docs mark is enlarged ×1.25 and the Showcase mark ×1.3 about their own centers, exactly as rendered in the study ([issue #21](https://github.com/cubrid-lab/brand/issues/21)). `scripts/build.py` now draws these marks, and the changed approved assets are `docs` and `showcase` (`dist/icons/` and `src/`); position, color token and review status are unchanged. Proposal P1, a darker keyline under the Go and Rust marks, was declined because it darkens the Operator dial for a small gain. This is a design decision only; legal review remains pending and no visual-asset license is offered. Consumers that pin an earlier revision of these icons keep the previous artwork until they repin.

## Driver, ORM and MCP role redesign (issues #30 and #23)

On 2026-10-25 the maintainer (@yeongseon) reviewed [`docs/studies/role-redesign-30/family.png`](docs/studies/role-redesign-30/family.png) and [`contact-sheet.png`](docs/studies/role-redesign-30/contact-sheet.png), generated at [`1c344fb`](https://github.com/cubrid-lab/brand/commit/1c344fb283fc29284fb543a4e8f1109c620c1b17) on [PR #37](https://github.com/cubrid-lab/brand/pull/37). From the candidates in [`tokens/role-candidates.json`](tokens/role-candidates.json), the maintainer selected:

- **Driver:** `driver-vertical-stack`. This is the previous ORM layered geometry, reassigned to the Driver role ([issue #30](https://github.com/cubrid-lab/brand/issues/30)).
- **ORM:** `orm-lateral-plates`, the same stack turned on its side ([issue #30](https://github.com/cubrid-lab/brand/issues/30)).
- **MCP:** `mcp-router-hub`, the "3-Way Router" ([issue #23](https://github.com/cubrid-lab/brand/issues/23)). No vector source for the earlier candidate A was found, so this drawing is a reconstruction from its written description, and the maintainer approved the reconstruction itself.

`scripts/build.py` now draws these roles. The changed approved assets are:

- Driver: `pycubrid`, `cubrid-client`, `cubrid-go` and `cubrid-rs`.
- ORM: `sqlalchemy-cubrid`, `drizzle-cubrid`, `gorm-cubrid` and `sea-orm-cubrid`.
- MCP: `cubrid-mcp-server`.

In `dist/icons/` and in `src/driver.svg`, `src/orm.svg` and `src/mcp.svg`, each is generated in its unchanged language token. Language colors, the registry role mapping, review statuses, the organization emblem and lockups, and every other role are byte-identical.

The promoted SVGs draw exactly what the reviewed candidates drew. `tests/test_role_candidates.py` checks this, and the Python, TypeScript and Go renders match pixel for pixel at 16 to 128 px. The before/after sheet is [`docs/studies/role-redesign-30/promoted-before-after.png`](docs/studies/role-redesign-30/promoted-before-after.png). All six reviewed candidates, including the unselected ones, remain in `studies/roles/` as the review record.

This is a symbol design decision only. Creator rights, the all-rights-reserved status, and the pending similarity, trademark and legal reviews are unchanged. Consumers that pin an earlier revision keep the previous artwork until they repin in their own repositories.

AI assistance was used to reconstruct the SVGs and prepare this documentation. Publication in this repository is not a grant of rights to use the visual assets.

## Python Yellow with an ochre keyline (issue #38)

On 2026-10-25 the maintainer (@yeongseon) changed the Python language token from Python Blue `#3776AB` to Python Yellow `#FFD43B` ([issue #38](https://github.com/cubrid-lab/brand/issues/38)), superseding the issue #30 color decision, because Python Blue was too close to TypeScript blue and Go cyan. After reviewing [`docs/studies/python-yellow-38/family.png`](docs/studies/python-yellow-38/family.png) and [`checks.md`](docs/studies/python-yellow-38/checks.md) on [PR #40](https://github.com/cubrid-lab/brand/pull/40), the maintainer selected treatment `t3-ochre-keyline`: dark role marks `#40350F` and a 0.6-unit ochre keyline `#8C7520` outside every Python icon ([study](docs/studies/python-yellow-38.md); construction in [`docs/GEOMETRY.md`](docs/GEOMETRY.md#light-token-treatment-issue-38)).

`tokens/colors.json` now holds the new token and its treatment, and `scripts/build.py` applies it. The changed approved assets are `pycubrid`, `sqlalchemy-cubrid`, `cubrid-mcp-server` and `cubrid-cookbook-python` in `dist/icons/`. They draw exactly what the reviewed `t3-ochre-keyline` candidates drew: `tests/test_python_yellow_candidates.py` checks this, and the renders match pixel for pixel at 16 to 128 px. The before/after sheet is [`docs/studies/python-yellow-38/promoted-before-after.png`](docs/studies/python-yellow-38/promoted-before-after.png). `src/`, the TypeScript, Go, Rust and Neutral icons, the reserved JavaScript token, the organization emblem and lockups, the registry and the role geometry are byte-identical. The Python SVGs in `studies/roles/` follow the token; the issue #30 review sheets keep Python Blue as reviewed.

This is a design decision only. Creator rights, the all-rights-reserved status and the pending legal reviews are unchanged. Consumers that pin an earlier revision keep the Python Blue artwork until they repin in their own repositories.

## Driver/ORM cube restoration (issues #41 and #43)

On 2026-10-25 the maintainer requested that both shared role marks keep the recognizable CUBRID Lab **cube**, with the same three equal-thickness layers turned along different axes. The new Driver is divided top-to-bottom inside the cube; the new ORM is divided side-to-side inside the same cube. The #30 floating constructions and #38 Python Yellow experiments remain under `studies/` as historical review records. The change is to role geometry only; the brand colors, organization emblem, registry and rights status remain separate and unchanged. Final SVG promotion remains subject to PR visual review.
