# Applying repository icons

This guide is for repositories owned by the `cubrid-lab` GitHub organization.
Each one embeds its approved role icon from `dist/icons/` by a commit-pinned URL;
it does not copy or modify the SVG. The
[registry](../registry/repositories.json) is the authoritative record of the
icon's role, language, and approval status. Every approved icon may be used this
way, in the README and as the documentation-site logo and favicon. See [Repository icon use](../BRAND_USAGE.md#repository-icon-use) for
the full decision, use outside CUBRID Lab, and the reviews still pending.

## README header

Place a centered, 120 px icon before the project title. Use the same header in
each translated README, preserving its translated title and surrounding content.
The marker pair lets future updates locate the icon without replacing other
README content.

This example uses the approved TypeScript Driver icon at an immutable revision:

```html
<!-- CUBRID-LAB-ICON:START -->
<p align="center">
  <a href="https://github.com/cubrid-lab/brand"><img src="https://raw.githubusercontent.com/cubrid-lab/brand/38b46469a1e18c7e9f7270f0b3d286ab45c3b376/dist/icons/cubrid-client.svg" alt="CUBRID Lab Driver icon (TypeScript)" width="120"></a>
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

Mind the [known small-size limits](ICON_GALLERY.md#known-small-size-limits): favicons
render at 16 px, where the Operator dial does not resolve, and the Community figures
need 48 px or more to separate.

## Rollout inventory

On 2026-10-25 every repository README (and, where present, translated READMEs and the
documentation-site logo and favicon) was pinned to `8aa81b7`, the revision that contains
the #37 Driver/ORM/MCP redesign and the #38 Python Yellow treatment. After #45 restored
the complete cube for the Driver and ORM roles, their eight repositories moved to `38b4646`. `showcase` pins
`bfb1871`, whose `showcase.svg` is byte-identical to `8aa81b7`.

| Repository | Role | Language | Asset revision | Rollout PR |
| --- | --- | --- | --- | --- |
| `pycubrid` | Driver | Python | `38b46469a1e18c7e9f7270f0b3d286ab45c3b376` | [#1061](https://github.com/cubrid-lab/pycubrid/pull/1061) |
| `sqlalchemy-cubrid` | ORM | Python | `38b46469a1e18c7e9f7270f0b3d286ab45c3b376` | [#1055](https://github.com/cubrid-lab/sqlalchemy-cubrid/pull/1055) |
| `cubrid-mcp-server` | MCP | Python | `8aa81b79f00ae936b03a9546f14f514c5e2554a7` | [#457](https://github.com/cubrid-lab/cubrid-mcp-server/pull/457) |
| `cubrid-cookbook-python` | Cookbook | Python | `8aa81b79f00ae936b03a9546f14f514c5e2554a7` | [#500](https://github.com/cubrid-lab/cubrid-cookbook-python/pull/500) |
| `cubrid-client` | Driver | TypeScript | `38b46469a1e18c7e9f7270f0b3d286ab45c3b376` | [#75](https://github.com/cubrid-lab/cubrid-client/pull/75) |
| `cubrid-go` | Driver | Go | `38b46469a1e18c7e9f7270f0b3d286ab45c3b376` | [#50](https://github.com/cubrid-lab/cubrid-go/pull/50) |
| `cubrid-rs` | Driver | Rust | `38b46469a1e18c7e9f7270f0b3d286ab45c3b376` | [#23](https://github.com/cubrid-lab/cubrid-rs/pull/23) |
| `cubrid-kubernetes-operator` | Operator | Go | `8aa81b79f00ae936b03a9546f14f514c5e2554a7` | [#582](https://github.com/cubrid-lab/cubrid-kubernetes-operator/pull/582) |
| `drizzle-cubrid` | ORM | TypeScript | `38b46469a1e18c7e9f7270f0b3d286ab45c3b376` | [#139](https://github.com/cubrid-lab/drizzle-cubrid/pull/139) |
| `gorm-cubrid` | ORM | Go | `38b46469a1e18c7e9f7270f0b3d286ab45c3b376` | [#33](https://github.com/cubrid-lab/gorm-cubrid/pull/33) |
| `sea-orm-cubrid` | ORM | Rust | `38b46469a1e18c7e9f7270f0b3d286ab45c3b376` | [#16](https://github.com/cubrid-lab/sea-orm-cubrid/pull/16) |
| `cubrid-benchmark` | Benchmark | Neutral | `8aa81b79f00ae936b03a9546f14f514c5e2554a7` | [#65](https://github.com/cubrid-lab/cubrid-benchmark/pull/65) |
| `showcase` | Showcase | Neutral | `bfb1871c8856d59dd60eb6276328465a7ab03ac7` | [#49](https://github.com/cubrid-lab/showcase/pull/49) |

Each repository README must pin a commit containing its approved
`dist/icons/<repository>.svg` asset; older study URLs are historical evidence
rather than approved integration sources. The `docs` and `community` icons are
concept surfaces, not repository names; a documentation or community surface
that adopts one pins a commit the same way.

Check the [registry](../registry/repositories.json) for the current approval
status before applying an icon; an entry marked `pending-symbol` is a candidate
and must not be applied. Approval dates and decisions are recorded in
[PROVENANCE.md](../PROVENANCE.md#review-state), and the permitted uses in
[Repository icon use](../BRAND_USAGE.md#repository-icon-use).

The organization emblem has separate scoped approval and
[usage guidance](ORGANIZATION_MARK_USAGE.md), as do the approved wordmark
lockups. Their legal/trademark review remains under
[issue #3](https://github.com/cubrid-lab/brand/issues/3).
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
[Repository icon use](../BRAND_USAGE.md#repository-icon-use) permits. Copying an
SVG into a repository, for example for offline documentation builds, is not
permitted.

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
