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

Use the shared, tool-neutral PR process: scoped change, implementation
with tests and documentation, applicable required CI, independent review
of relevant design/rights risks, and final maintainer decision. Issue
assignment and existing design/legal approval obligations remain.

## Validation

```bash
python scripts/build.py
python -m unittest discover -s tests -v
git diff --exit-code -- src dist studies/icons studies/organization studies/roles
test -z "$(git ls-files --others --exclude-standard -- src dist studies/icons studies/organization studies/roles)"
```

The build deletes only stale generator-owned outputs. Any other SVG in an
output directory is never deleted: the build still writes outputs and removes
stale owned copies, then reports the unmanaged SVG and exits with status 1.

Refs #1.

## Unified PR Review and Merge Policy

Use the **same criteria** for every contribution, whether human-written or
implemented with OpenCode, Codex, Claude Code, ChatGPT, Copilot or another
agent. No tool-specific AI review or Oracle pre/post review is required.
Oracle, Copilot and other AI findings are optional advisory context.

Keep the existing design, generated-asset, rights and trademark constraints
in every review. Required GitHub CI checks (where configured) are the
authoritative automated result at the final head; local validation commands
above are recommended and do not replace CI. The responsible maintainer
verifies reproducibility, intellectual-property and publication impact
and makes the final merge decision. Visual/brand/legal sign-off, where
required, remains an independent approval, **not** an AI-code-review stage.

## Issue triage lifecycle

Every new issue in this repository starts with `status: needs triage`.
The `issues: opened` workflow (`.github/workflows/issue-triage.yml`) adds it
to every opened issue; this repository has no issue forms. Automation that
files issues with `GITHUB_TOKEN` must attach the label at creation, since
`GITHUB_TOKEN` issue events do not trigger another workflow.

1. Check evidence and impact, unknowns, duplicate/open-PR overlap, repository
   scope, issue type, non-goals, acceptance and dependencies. Close duplicate
   or invalid issues with a reason.
2. Review **all other open issues in this repository**, using pagination,
   before assigning relative priority, considering current risks, work
   already in progress, and blockers rather than creation order.
3. Choose exactly one `priority: critical/high/medium/low` and one existing
   `size: XS/S/M/L/XL` (effort, not importance). Split oversized independent
   implementation tasks, preserving accepted scope and contributor history.
4. Read back GitHub's actual saved issue labels and classification. Only
   remove `status: needs triage` after reviewing type, priority, size,
   evidence, duplicates and backlog position. Keep the status if unresolved.

Do not auto-rank priorities or auto-close triage in CI. This introduces
no new PR merge gate and preserves existing design and release standards.
