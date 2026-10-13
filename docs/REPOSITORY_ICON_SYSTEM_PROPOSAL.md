# Repository icon system — design review proposal

**Status:** Proposal for design review ([issue #4](https://github.com/cubrid-lab/brand/issues/4)). No new role symbol, organization mark, repository mapping, or language token is approved by this document. Legal and trademark review remains separate.

This document records the content of a maintainer-supplied repository-icon infographic (October 2026). The original image is preserved below as an **unapproved design reference**, outside `dist/`. It is not a generated asset or a second source of truth for any icon or organization mark, and its inclusion does not expand the visual-asset license. The accepted Driver construction remains in [`tokens/geometry.json`](../tokens/geometry.json) and its immutable reference remains in [`provenance/connector-study-02/driver-python.svg`](../provenance/connector-study-02/driver-python.svg).

![CUBRID Lab repository icon-system infographic, unapproved design study](studies/repository-icon-system-infographic.png)

## System concept

- **Shape = technical role; color = implementation language.** Repositories with the same role share a recognizable symbol; repositories with the same language use the same color token.
- Share a 24×24 construction grid, a 1:1 icon proportion, 60°/120° angles, and clear negative space. “Same geometry” means a shared construction grammar, not an identical silhouette for different roles.
- The four presentation groups are **Drivers** (connect to CUBRID), **ORMs / Dialects** (map and abstract), **Tools & AI** (build and extend), and **Infrastructure** (run and operate). Their blue, green, orange, and red panel accents are presentation aids, not repository color assignments.

The study describes the system as “a consistent and meaningful icon system for the CUBRID ecosystem.” Its group copy proposes stable, high-performance connectivity for Drivers; more productive framework integration for ORMs / Dialects; AI, examples, and performance insights for Tools & AI; and real-world operation, deployment, and community exploration for Infrastructure.

## Repository examples shown in the study

| Group | Repository or surface | Proposed meaning | Language label in study | Current canonical state |
| --- | --- | --- | --- | --- |
| Drivers | `pycubrid` | Python Driver | Python | Driver / Python, approved |
| Drivers | `cubrid-go` | Go Driver | Go | Driver / Go, approved |
| Drivers | `cubrid-rs` | Rust Driver | Rust | Driver / Rust, approved |
| ORMs / Dialects | `sqlalchemy-cubrid` | SQLAlchemy Dialect | Python | ORM / Python, symbol pending |
| ORMs / Dialects | `gorm-cubrid` | GORM Dialect | Go | ORM / Go, symbol pending |
| ORMs / Dialects | `drizzle-cubrid` | Drizzle ORM | Rust | ORM / **TypeScript**, symbol pending; study label conflicts |
| ORMs / Dialects | `sea-orm-cubrid` | SeaORM Dialect | Rust | ORM / Rust, symbol pending |
| Tools & AI | `cubrid-mcp-server` | Model Context Protocol | Python | MCP / Python, symbol pending |
| Tools & AI | `cubrid-cookbook-python` | Examples and Guides | Python | Cookbook / Python, symbol pending |
| Tools & AI | `cubrid-benchmark` | Performance Tools | Rust | Benchmark / **neutral**, symbol pending; study label conflicts |
| Infrastructure | `cubrid-kubernetes-operator` | Kubernetes Operator | Go | Operator / Go, symbol pending |
| Infrastructure | `showcase` | Project Showcase | TypeScript | No registry mapping; [current language statistics](https://api.github.com/repos/cubrid-lab/showcase/languages) list Python, Shell, and Vue, but no TypeScript (October 2026) |
| Infrastructure | `docs` | Documentation | Markdown | Presented as a surface; repository identity is unspecified |
| Infrastructure | `community` | Discussions & Support | Markdown | Presented as a surface; repository identity is unspecified |

The study omits `cubrid-client`, whose **Driver / TypeScript** mapping is already approved. Omission from the illustration does not change that mapping. `showcase` exists as a repository, but the study's TypeScript label conflicts with its current language statistics and is not an approved mapping. `docs` and `community` must not be added to the registry as repository names without identifying actual repositories.

## Role meanings proposed for future symbols

| Study label | Meaning | Current registry role |
| --- | --- | --- |
| Driver | Connect | `driver` — approved geometry; the illustrated cube/plug is only a candidate |
| ORM | Layer | `orm` — pending |
| MCP | Network | `mcp` — pending |
| Guide | Book | `cookbook` — pending |
| Tool | Analytics | `benchmark` — pending |
| Operator | Control | `operator` — pending |
| Showcase | Play | No mapping |
| Docs | Document | No mapping |
| Community | People | No mapping |

These are silhouette briefs, not approved drawings. The accepted Driver is **Connector Study / 02**; the Driver pictured in the infographic must not replace it without a separate design decision and geometry review. Other roles need distinct, original shapes. Do not incorporate third-party logos.

## Language palette in the study

| Language or use | Study swatch | Current token |
| --- | --- | --- |
| Python | `#3776AB` | `#3776AB` |
| Go | `#00ADD8` | `#00ADD8` |
| Rust | `#DEA384` | `#DEA384` |
| JavaScript | `#F7DF1E` | Not defined |
| OCaml | `#A34CC3` | Not defined |
| TypeScript | `#3178C6` | `#3178C6` |
| Neutral | `#6B7280` | `#5B6573`; study swatch differs |

The study's additional swatches are proposals only. No repository-specific color should be hard-coded where a language token exists. These colors are CUBRID Lab internal design tokens, not official CUBRID brand colors or claims about language brands.

## Construction and preview checks

- Draw and review on a 24×24 grid with consistent 60°/120° angles and open negative space. Preserve the exact accepted Driver parameters rather than approximating them from the infographic.
- Preview proposed symbols at **16, 24, 32, 48, and 64 px**. Check legibility at 16 px and consistency at each size.
- Preview a monochrome version at **100%, 70%, 40%, and 20%** opacity. The study shows these examples; their contrast and accessibility are not yet validated.
- Test each role in its language colors only after its geometry is approved. Experimental concepts stay outside `dist/`.

## Organization identity and copy

The study depicts a separate cube-like **CUBRID Lab** emblem and wordmark, plus these proposed lines:

> Open Source for a More Connected World
>
> Database · Developers · Open Community · A Better Tomorrow
>
> More connections, a better tomorrow (English rendering of the study's Korean line)
>
> Build Beyond Boundaries. Open for What's Next.

It also uses **“Same geometry · Clear roles · Language colors · One CUBRID”**, **“Open source · Real world · Growing together”**, and **“Est. 2024.”** These are unapproved copy proposals. “One CUBRID” requires particular care because CUBRID Lab is independent of CUBRID Corporation and the official CUBRID project; keep the [independence notice](../BRAND_USAGE.md) prominent and review the wording before publication.

The organization emblem and wordmark belong to [issue #3](https://github.com/cubrid-lab/brand/issues/3). The Driver role symbol is not the organization logo. No organization avatar, profile, or identity asset changes follow from this study.

## Decisions before implementation

1. Review each pending role's silhouette against the approved Driver and other roles; record explicit maintainer design approval per role.
2. Resolve the study's `drizzle-cubrid`, `cubrid-benchmark`, and Neutral mismatches against the canonical registry and tokens. Confirm whether JavaScript and OCaml tokens are needed.
3. Resolve Showcase's TypeScript label against the repository's current languages, and identify the intended repositories and implementation languages for Docs and Community before adding mappings.
4. Review the organization emblem and copy under issue #3, including rights, similarity, and trademark work separately from design approval.
5. After approval, implement numeric geometry in tokens and the generator, add regression tests, update guidance, and obtain independent post-implementation review before publishing generated assets.
