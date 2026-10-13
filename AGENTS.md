# AGENTS.md

## Purpose

This repository is the source of truth for CUBRID Lab brand geometry, tokens, generated assets, repository mappings, and usage guidance.

## Rules

1. **Shape = technical role; color = implementation language.**
2. `tokens/geometry.json` defines the accepted `connector-study-02` parameters. `scripts/build.py` implements its closed-form geometry; both must agree with the immutable source at `provenance/connector-study-02/driver-python.svg`. Generated SVG geometry must never become a second source of truth.
3. Never assign a repository-specific color directly when a language token exists.
4. Do not copy third-party logos into role symbols.
5. Do not describe CUBRID Lab token colors as official CUBRID brand colors.
6. Do not mark a role symbol approved until a maintainer explicitly approves it.
7. Keep experimental concepts out of `dist/`.
8. Generated assets must be reproducible from `tokens/`, `registry/`, and `scripts/`.
9. Legal/trademark review status must remain separate from design approval.
10. Do not broaden the visual-asset license while rights/trademark review is pending.
11. The Driver role icon is not the CUBRID Lab organization logo. Design the organization mark separately (issue #3), and do not silently repurpose role icons.

## Workflow

Follow the cubrid-lab organization workflow:

1. design review,
2. implementation + tests,
3. documentation,
4. independent post-implementation review.

Issue assignment is mandatory before implementation.

## Validation

```bash
python scripts/build.py
python -m unittest discover -s tests -v
git diff --exit-code -- src/driver.svg dist
```

Refs #1.
