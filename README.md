# CUBRID Lab Brand

Canonical brand-system source for CUBRID Lab.

> CUBRID Lab is an independent, community-driven open-source initiative and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project. CUBRID is a trademark of its owner; the name is used here only to identify compatibility with the CUBRID database.

## Design system

The system follows two rules:

- **Shape = technical role**
- **Color = implementation language**

The first approved role symbol is **Driver**: two mirrored geometric modules joined around a central channel. It represents a driver bridging an application runtime and CUBRID while remaining visually distinct from the vertically layered ORM concept.

Current language tokens:

| Language | Token | Color |
|---|---|---|
| Python | `python` | `#3776AB` |
| TypeScript | `typescript` | `#3178C6` |
| Go | `go` | `#00ADD8` |
| Rust | `rust` | `#CE422B` |

These colors are **CUBRID Lab design tokens**, not claims about official CUBRID brand colors.

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

`tokens/geometry.json` is the canonical numeric geometry. `scripts/build.py` deterministically generates the neutral Driver template and all approved repository variants from that geometry, the language-color tokens, and the repository registry.

```text
tokens/              canonical geometry and language colors
registry/            repository -> role/language mapping
scripts/             deterministic asset generation
src/                 generated neutral role template
dist/                generated approved repository assets
tests/               geometry, mapping, and generation invariants
docs/                design rationale and Korean guide
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
