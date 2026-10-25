# Driver and ORM — one cube, two layer directions

Maintainer design direction: 2026-10-25. Issues [#41](https://github.com/cubrid-lab/brand/issues/41) and [#43](https://github.com/cubrid-lab/brand/issues/43).

**The cube stays.** Both roles now share the three-face, 24×24 isometric cube already used by MCP and the organization emblem. Each has two equally spaced interior grooves defining three parts. The sole role difference is the axis: top-to-bottom for Driver, side-to-side for ORM.

The earlier detached Driver/ORM shapes were selected during [#30](role-redesign-30.md) but did not read clearly as a cube. They are preserved in `studies/roles/`, and the 2026 Python Yellow candidates remain preserved in `studies/python-yellow/`.

## Current proposal — compare side by side

| Language | Driver: vertical divisions | ORM: lateral divisions |
| --- | :---: | :---: |
| Python Yellow | <img src="../../dist/icons/pycubrid.svg" width="110" alt="yellow cube with horizontal divisions"> | <img src="../../dist/icons/sqlalchemy-cubrid.svg" width="110" alt="yellow cube with lateral divisions"> |
| TypeScript Blue | <img src="../../dist/icons/cubrid-client.svg" width="110" alt="blue cube with horizontal divisions"> | <img src="../../dist/icons/drizzle-cubrid.svg" width="110" alt="blue cube with lateral divisions"> |
| Go Cyan | <img src="../../dist/icons/cubrid-go.svg" width="110" alt="cyan cube with horizontal divisions"> | <img src="../../dist/icons/gorm-cubrid.svg" width="110" alt="cyan cube with lateral divisions"> |
| Rust | <img src="../../dist/icons/cubrid-rs.svg" width="110" alt="rust cube with horizontal divisions"> | <img src="../../dist/icons/sea-orm-cubrid.svg" width="110" alt="rust cube with lateral divisions"> |

Compare the earlier [Driver icon](https://github.com/cubrid-lab/brand/blob/8aa81b79f00ae936b03a9546f14f514c5e2554a7/dist/icons/pycubrid.svg) and [ORM icon](https://github.com/cubrid-lab/brand/blob/8aa81b79f00ae936b03a9546f14f514c5e2554a7/dist/icons/sqlalchemy-cubrid.svg) to the new cube-based candidates.

## Verification before merge

- The outer silhouette is a genuine cube in both roles.
- Groove fractions are identical (one third and two thirds), so the layer weight is consistent.
- Each groove terminates inside its face to avoid breaking the white/transparent seam and the cube's perimeter.
- Python retains its yellow token and dark-groove/ochre-outline treatment.
- At 16/24/32/48/64/128 px, review the SVGs on **white and dark** backgrounds. Automated 3:1 contrast checks are guides for the non-text symbol, not a claim of WCAG logo conformance; Go and Rust white marks need particular attention.

This page is for visual review of a PR. It does not independently certify that the final design has been approved.
