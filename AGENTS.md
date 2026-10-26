# AGENTS.md

## Organization-wide writing standard

Follow [cubrid-lab's Issue, PR and commit policy](https://github.com/cubrid-lab/.github/blob/main/docs/ISSUE_PR_COMMIT_STANDARD.md). Issue titles use a type-only prefix such as `feat: ...`, `bug: ...`, or `docs: ...` without a required module scope. Describe a human-readable goal/problem and verifiable acceptance criteria. Triage handles validity, scope, duplicates, priority and size; PR and commit titles retain Conventional Commits/local CI requirements. Avoid internal review codes, personal comments and agent execution logs in issue prose.


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
10. Do not grant or broaden a visual-asset license without a recorded maintainer decision. None is offered: on 2026-10-25 the maintainer reserved all rights in the visual assets (see `BRAND_USAGE.md`), and trademark review is pending.
11. The Driver role icon is not the CUBRID Lab organization logo. Keep the three-color organization-mark study separate (issue #3); do not repurpose a role icon or publish an organization avatar before design and rights approval.

## Approval status sources

Current approval status lives only in `registry/repositories.json` (repository and
concept-surface icons) and `tokens/organization.json` (organization emblem and
wordmark lockups). Record the decision history in `PROVENANCE.md`. Guides link to
these files rather than repeating status lists, counts or approval dates. When a
status changes, also update the independent `APPROVED` list in
`tests/test_brand.py`.

## Repository settings

`main` uses classic branch protection, as configured on 2026-10-25 (issue #18):
a pull request is required (0 approving reviews), the `validate` check must pass
on a branch that is up to date with `main`, and force pushes and branch deletion
are blocked. `enforce_admins` is off, so a repository administrator can bypass the
rules; this is a documented exception. Viewing or changing these settings requires
a repository administrator.

## Workflow

Use the shared, tool-neutral PR process: scoped change, implementation
with tests and documentation, applicable required CI, independent review
of relevant design/rights risks, and final maintainer decision. Issue
assignment and existing design/legal approval obligations remain.

## Validation

```bash
python scripts/build.py
python -m unittest discover -s tests -v
git diff --exit-code -- src dist studies/icons studies/organization studies/roles studies/python-yellow
test -z "$(git ls-files --others --exclude-standard -- src dist studies/icons studies/organization studies/roles studies/python-yellow)"
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

## Human-readable communication (all agents)

Use this rule for text authored or edited by Codex, Claude Code, OpenCode,
ChatGPT, Copilot, or any other agent. It applies to issues, PRs, reviews,
comments, checklists, status updates, commit summaries, release notes,
documentation, presentations, and other maintainer-facing writing.

- Write for a reader unfamiliar with the underlying script, storyboard,
  automation run, or agent plan. Name the actual project, component,
  action, evidence, and location in ordinary, clear language.
- Never use unexplained internal identifiers as reader-facing labels or
  checklist instructions (for example, `H1, P1, C1, K1, F2` or `A1/B1/R1/R2`).
  Do not substitute `P1`/`P2` for repository priority labels.
- When an internal identifier is necessary for accurate cross-reference,
  **describe the subject first**, then add the identifier in context:
  `pycubrid introduction (0:20; storyboard shot P1)`. Use descriptive
  names and timestamps, section titles, or paths wherever practical.
- Use natural, actionable wording. Prefer `Listen to the full narration and
  verify the pronunciation of each project name` to `Maintainer full listen`.
  Avoid compressed task fragments, unexplained acronyms, and generated
  process/status jargon.
- Keep legitimate technical identifiers unchanged in code, tests, structured
  data, logs, specifications, and exact evidence references. Issue numbers,
  filenames, command names, APIs, error codes, and hashes are not prohibited.
  Do not break machine-readable references to improve prose.
- Before publishing, reread the text as a first-time maintainer. It should
  state what happened or needs to happen, why, and where without requiring a
  separate lookup table. Edit an existing editable comment to correct unclear
  wording rather than adding redundant follow-up comments.

This is a shared writing convention, not a new CI check, reviewer approval,
or merge gate. Keep existing repository-specific technical and safety rules.
