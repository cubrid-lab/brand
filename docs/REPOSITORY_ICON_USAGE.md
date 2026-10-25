# Applying repository icons

This guide is for repositories owned by the `cubrid-lab` GitHub organization.
Each one embeds its approved role icon from `dist/icons/` by a commit-pinned URL;
it does not copy or modify the SVG. The
[registry](../registry/repositories.json) defines the icon's role, language, and
approval status. Use outside CUBRID Lab is not covered: see
[Repository icon use](../BRAND_USAGE.md#repository-icon-use) for what is
permitted, what is not, and what is still pending legal review.

## README header

Place a centered, 120 px icon before the project title. Use the same header in
each translated README, preserving its translated title and surrounding content.
The marker pair lets future updates locate the icon without replacing other
README content.

This example uses the approved TypeScript Driver icon at an immutable revision:

```html
<!-- CUBRID-LAB-ICON:START -->
<p align="center">
  <a href="https://github.com/cubrid-lab/brand"><img src="https://raw.githubusercontent.com/cubrid-lab/brand/aa62d38b48d165e39f0c56ed706a9dadb090a2bb/dist/icons/cubrid-client.svg" alt="CUBRID Lab Driver icon (TypeScript)" width="120"></a>
</p>
<!-- CUBRID-LAB-ICON:END -->
```

Follow the block with a blank line and the Markdown project title, such as
`# cubrid-client`. When adapting the example, select the repository's own filename
and an immutable commit containing its approved icon, and update the alt text.
Keep an existing revision pin when its SVG is still current; a newer commit alone
is not a reason to change it. Avoid `main` URLs, which can change unexpectedly.

## Documentation sites

For MkDocs Material, set `theme.logo` and `theme.favicon` to the same approved,
commit-pinned SVG used in the README. Preserve the rest of the site's theme and
navigation. This convention is already applied to `pycubrid`, `sqlalchemy-cubrid`,
`cubrid-mcp-server`, and `cubrid-cookbook-python`.

## Rollout inventory

The seven earlier repository integrations retain these revisions. Both revisions contain
byte-identical Driver SVGs; the later revision also contains the newly approved
Python ORM, MCP, and Cookbook icons.

| Repository | Role | Language | Asset revision | README alignment work |
| --- | --- | --- | --- | --- |
| `pycubrid` | Driver | Python | `94e2bf6b915d7ef6a1111e06376f693f70bf6c4e` | Existing standard header |
| `sqlalchemy-cubrid` | ORM | Python | `94e2bf6b915d7ef6a1111e06376f693f70bf6c4e` | Existing standard header |
| `cubrid-mcp-server` | MCP | Python | `94e2bf6b915d7ef6a1111e06376f693f70bf6c4e` | Existing standard header |
| `cubrid-cookbook-python` | Cookbook | Python | `94e2bf6b915d7ef6a1111e06376f693f70bf6c4e` | Existing standard header |
| `cubrid-client` | Driver | TypeScript | `aa62d38b48d165e39f0c56ed706a9dadb090a2bb` | [#65](https://github.com/cubrid-lab/cubrid-client/issues/65) |
| `cubrid-go` | Driver | Go | `aa62d38b48d165e39f0c56ed706a9dadb090a2bb` | [#33](https://github.com/cubrid-lab/cubrid-go/issues/33) |
| `cubrid-rs` | Driver | Rust | `aa62d38b48d165e39f0c56ed706a9dadb090a2bb` | [#14](https://github.com/cubrid-lab/cubrid-rs/issues/14) |
| `cubrid-kubernetes-operator` | Operator | Go | `572addda0f5403a455c27ec742eacd315f9ff929` | [#429](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/429) |
| `drizzle-cubrid` | ORM | TypeScript | `cc9c7b2a50b1b93f96b18902dbf3f029ccdda026` | [#116](https://github.com/cubrid-lab/drizzle-cubrid/issues/116) |
| `gorm-cubrid` | ORM | Go | `cc9c7b2a50b1b93f96b18902dbf3f029ccdda026` | [#22](https://github.com/cubrid-lab/gorm-cubrid/issues/22) |
| `sea-orm-cubrid` | ORM | Rust | `cc9c7b2a50b1b93f96b18902dbf3f029ccdda026` | [#7](https://github.com/cubrid-lab/sea-orm-cubrid/issues/7) |
| `cubrid-benchmark` | Benchmark | Neutral | Promotion commit recorded in [brand #6](https://github.com/cubrid-lab/brand/issues/6) | Pending consumer rollout |
| `showcase` | Showcase | Neutral | Promotion commit recorded in [brand #6](https://github.com/cubrid-lab/brand/issues/6) | Pending consumer rollout |

The Operator icon was selected on 2026-10-15, the TypeScript, Go, and Rust
ORM icons were selected on 2026-10-20, and the Benchmark and Showcase icons were
approved on 2026-10-25. Each repository README must pin the promotion commit
containing its `dist/icons/<repository>.svg` asset; older study URLs are
historical evidence rather than approved integration sources.

The `docs` and `community` concept-surface icons were also approved on
2026-10-25 and are generated as `dist/icons/docs.svg` and
`dist/icons/community.svg`. They are not repository names; a documentation or
community surface that adopts one pins the same promotion commit.

No registry entry is currently marked `pending-symbol`. Record explicit
maintainer approval before promoting or applying any future candidate. The
registry remains authoritative as approvals change.

The organization emblem has separate scoped approval and
[usage guidance](ORGANIZATION_MARK_USAGE.md). Wordmark and broader legal/license
review remain under [issue #3](https://github.com/cubrid-lab/brand/issues/3).
A repository's role icon must not become the organization avatar or
organization-site logo.

## Consumption inventory (2026-10-25)

A search of the default branches of every public `cubrid-lab` repository
(plus the README files of the private `terraform-zadara-k8s` and of the `cubrid`
engine fork) for `cubrid-lab/brand` references and for files byte-identical to
any SVG in this repository's history found:

| Pattern | Where |
| --- | --- |
| README header, pinned `raw.githubusercontent.com` image | `pycubrid`, `sqlalchemy-cubrid`, `cubrid-mcp-server`, `cubrid-cookbook-python`, `cubrid-client`, `cubrid-go`, `cubrid-rs`, `cubrid-kubernetes-operator` |
| Translated README headers, same pinned image | `pycubrid` and `sqlalchemy-cubrid` (de, hi, ko, ru, zh); `cubrid-mcp-server` and `cubrid-cookbook-python` (ko) |
| MkDocs `theme.logo` and `theme.favicon`, same pinned URL | `pycubrid`, `sqlalchemy-cubrid`, `cubrid-mcp-server`, `cubrid-cookbook-python` |
| Organization emblem, pinned URL | `.github` profile README (governed by [Organization mark usage](ORGANIZATION_MARK_USAGE.md)) |
| Copied brand SVG files | None |
| Not yet consuming an icon | `drizzle-cubrid`, `gorm-cubrid`, `sea-orm-cubrid`, `cubrid-benchmark`, `showcase`, `cubrid-lab.github.io` |

`showcase/presentation/public/favicon.svg` is an unrelated letter "C" tile, not
a brand asset. No repository holds an SVG copy that a package could ship; a
registry page that renders one of these READMEs loads the same pinned URL. All observed
use is first-party embedding by pinned URL, which
[Repository icon use](../BRAND_USAGE.md#repository-icon-use) permits. Before an
organization repository departs from that pattern, for example by vendoring a
copy for offline documentation builds, it needs a recorded maintainer decision.

## Verification

Before merging an integration change:

1. Check the registry status, role, and language against the selected filename.
2. Confirm the immutable asset URL returns SVG and matches the current approved
   file byte-for-byte.
3. Render the README through GitHub Markdown and check that exactly one 120 px
   icon is centered above the title, with descriptive alt text and a brand link.
4. Check light and dark backgrounds, and synchronize any translated READMEs.
5. Check active documentation logo/favicon mappings and complete an independent
   post-implementation review.

Design approval remains separate from the rights and visual-asset licensing
status documented in [BRAND_USAGE.md](../BRAND_USAGE.md).

Refs [#8](https://github.com/cubrid-lab/brand/issues/8).
