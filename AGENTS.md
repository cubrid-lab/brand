# AGENTS.md

## Purpose

This repository is the source of truth for CUBRID Lab brand geometry, tokens, generated assets, repository mappings, and usage guidance.

## Rules

1. **Shape = technical role; color = implementation language.**
2. `tokens/geometry.json` defines the selected `repository-icon-cube-01` construction. `scripts/build.py` implements it against the maintainer-supplied visual reference at `docs/studies/repository-icon-system-infographic.png`. The superseded Connector Study / 02 SVG and parameters remain immutable under `provenance/connector-study-02/`. Generated SVGs are outputs, never a second source of truth.
3. Never assign a repository-specific color directly when a language token exists.
4. Do not copy third-party logos into role symbols.
5. Do not describe CUBRID Lab token colors as official CUBRID brand colors.
6. Do not mark a role symbol approved until a maintainer explicitly approves it.
7. Keep experimental concepts out of `dist/`.
8. Generated assets must be reproducible from `tokens/`, `registry/`, and `scripts/`.
9. Legal/trademark review status must remain separate from design approval.
10. Do not broaden the visual-asset license while rights/trademark review is pending.
11. The Driver role icon is not the CUBRID Lab organization logo. Keep the three-color organization-mark study separate (issue #3); do not repurpose a role icon or publish an organization avatar before design and rights approval.

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
git diff --exit-code -- src dist studies/icons studies/organization
test -z "$(git ls-files --others --exclude-standard -- src dist studies/icons studies/organization)"
```

Refs #1.
