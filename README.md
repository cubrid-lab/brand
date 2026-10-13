# CUBRID Lab Brand

Canonical brand-system source for CUBRID Lab.

> CUBRID Lab is an independent, community-driven open-source initiative and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project. CUBRID is a trademark of its owner; the name is used here only to identify compatibility with the CUBRID database.

## Design system

The system follows two rules:

- **Shape = technical role**
- **Color = implementation language**

The [repository icon-system study](docs/REPOSITORY_ICON_SYSTEM_PROPOSAL.md) records a broader infographic as a **design review proposal**. Its additional symbols, palette entries, organization mark, and copy are not approved assets or mappings.

The first design-approved role symbol is **Driver**, restored to the original **Connector Study / 02** geometry: two congruent modules rotated 180° about the 24×24 canvas center, with 0°/60°/120° edges and a 1.5-unit mitered seam. See [the numerical construction](docs/GEOMETRY.md) and the preserved [approved prototype](provenance/connector-study-02/driver-python.svg).

Current language tokens:

| Language | Token | Color |
|---|---|---|
| Python | `python` | `#3776AB` |
| TypeScript | `typescript` | `#3178C6` |
| Go | `go` | `#00ADD8` |
| Rust | `rust` | `#DEA384` |

These colors are **CUBRID Lab design tokens**, not claims about official CUBRID brand colors. The Python, Go, and Rust variants preserve the selected Connector Study / 02 colors; TypeScript remains an extension proposal.

## Organization identity

**CUBRID Lab** is the organization name and future wordmark. The Driver connector is a repository **role symbol**, **not** the organization logo. A separate organization-level emblem, wordmark, and profile/avatar rollout require design and rights review; see [issue #3](https://github.com/cubrid-lab/brand/issues/3). The GitHub handle remains `cubrid-lab`.

## Repository mapping

Machine-readable mappings live in `registry/repositories.json`.

Approved today:

- `pycubrid` — Driver / Python
- `cubrid-client` — Driver / TypeScript
- `cubrid-go` — Driver / Go
- `cubrid-rs` — Driver / Rust

Pending role-symbol approval:

- `sqlalchemy-cubrid`, `drizzle-cubrid`, `gorm-cubrid`, `sea-orm-cubrid` — ORM/Dialect
- `cubrid-mcp-server` — MCP / Python
- `cubrid-cookbook-python` — Cookbook / Python
- `cubrid-benchmark` — Benchmark / neutral/multi-language
- `cubrid-kubernetes-operator` — Operator / Go

## Source of truth

`tokens/geometry.json` is the canonical numerical parameters of accepted Connector Study / 02. `scripts/build.py` deterministically generates the neutral Driver template and all approved repository variants from that geometry, the language-color tokens, and the repository registry.

```text
tokens/              canonical geometry and language colors
registry/            repository -> role/language mapping
scripts/             deterministic asset generation
src/                 generated neutral role template
dist/                generated approved repository assets
tests/               geometry, mapping, and generation invariants
docs/                exact construction and Korean guide
provenance/          immutable accepted visual reference
```

Do not edit generated SVG geometry directly.

## Build and verify

```bash
python scripts/build.py
python -m unittest discover -s tests -v
git diff --exit-code -- src/driver.svg dist
```

## Licensing and status

Code in `scripts/` and `tests/` is MIT-licensed. Visual marks and generated brand assets are **not yet licensed for redistribution** while asset licensing and trademark review are pending. See [LICENSE](LICENSE), [BRAND_USAGE.md](BRAND_USAGE.md), and [PROVENANCE.md](PROVENANCE.md).

The Driver symbol is **design-approved** for continued development. This does **not** mean trademark, non-infringement, or formal legal review is complete.

Refs #1.
