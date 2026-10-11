# AGENTS.md

## Purpose

This repository is the source of truth for CUBRID Lab brand geometry, tokens, generated assets, repository mappings, and usage guidance.

## Rules

1. **Shape = technical role; color = implementation language.**
2. Never assign a repository-specific color directly when a language token exists.
3. Do not copy third-party logos into role symbols.
4. Do not describe CUBRID Lab token colors as official CUBRID brand colors.
5. Do not mark a role symbol approved until a maintainer explicitly approves it.
6. Keep experimental concepts out of `dist/`.
7. Generated assets must be reproducible from `src/`, `tokens/`, and `registry/`.
8. Legal/trademark review status must remain separate from design approval.

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
git diff --exit-code -- dist
```

Refs #1.
