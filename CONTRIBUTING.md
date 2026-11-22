# Contributing to CUBRID Lab Brand

**Title policy:** Use type-only issue titles (`feat:`, `bug:`, `docs:`) without module scopes. Keep Conventional Commits for PRs/commits and verifiable acceptance criteria for issues; triage and PR CI have separate responsibilities. See [AGENTS.md](AGENTS.md).

This repository uses a tool-neutral PR review policy for people and coding
agents (OpenCode, Codex, Claude Code, ChatGPT, Copilot, etc.).

Keep proposed changes in one focused PR with reproducible generated assets,
tests, documentation and any necessary rights provenance. Use the validation
commands in [AGENTS.md](AGENTS.md#validation), and treat required GitHub CI
checks at the final head as authoritative. Local runs are recommended.
AI review output is advisory, never a required tool-specific approval.
The responsible maintainer determines merge readiness; material brand,
trademark, licensing and public asset changes retain explicit independent
design/rights assessment. Do not treat green CI as asset publication approval.



## PR review outcomes

Use the same decision labels for every PR, whether human-authored or AI-assisted:

- **`APPROVE`** a reviewed, non-blocking change; optional suggestions can accompany approval instead of delaying it.
- **`REQUEST_CHANGES`** for an actionable must-fix defect, with the affected code and required correction clearly identified.
- **`COMMENT`** when asking a question or when a review is not yet decisive. The author cannot approve their own PR; never imply an AI review is an independent human approval.
- Code approval and GitHub Actions **run approval** are separate. `action_required`, pending, failed or stale required CI checks do not permit merge, even if a code review is approved. Confirm final-head CI, resolved blocking findings, applicable independent/security/integration requirements and the maintainer's merge decision before merging.

See [AGENTS.md — PR review outcomes](AGENTS.md#pr-review-outcomes-common-decision-rules). Existing repository-specific branch, release, security and required-review safeguards continue to apply.

## Suggest improvements and credit problem discovery

You are welcome to report a confusing page, missing documentation,
unexpected result, workflow friction or any other useful observation even
if you do not have a fix. Open **Improvement Idea** through
[New issue](https://github.com/cubrid-lab/brand/issues/new/choose).
One short description is sufficient to propose an issue; providing code,
a complete reproduction, a design or acceptance criteria is **optional at
intake**. The maintainers check duplicates, scope, evidence, priority,
ownership and actionable acceptance criteria before scheduling work.

Keep credentials, personal information, private infrastructure logs and
security reports out of public issues. A new idea does not grant permission
to change infrastructure, release controls, security configuration or
architecture, or skip required review. Where existing repository rules
permit direct small PRs, no preliminary issue is required solely for
ceremony. Check overlapping work and coordinate before coding.

When the work originates from an external report, link the issue in the PR
and acknowledge the verified **reporter** as distinct from the
implementation author. Follow this repository's existing verified
contributor and release-note rules; a separately labeled
`reported by @handle` credit may be appropriate, but attribution should
never be fabricated or imposed as repetitive boilerplate.

## Issue ownership and agent handoff

Before implementation, check the latest source, open issues and overlapping PRs. Keep each change focused on one independently reviewable brand or asset task. New issues begin with `status: needs triage`; maintainers verify duplicates, scope, type and relative urgency against the local open backlog, then confirm one `priority: critical/high/medium/low` and one `size: XS/S/M/L/XL`. Remove the status only after checking the saved GitHub labels and the actual triage decision.

Human contributors may propose or implement unclaimed work without a required AI tool or pre-approval. Maintainer-operated autonomous agents need explicit authorization and a verified assignee before taking reserved work. Preserve the distinction between design approval, legal/trademark clearance and code review: passing tests or an AI review does not approve a public brand asset.

Keep `tokens/`, `registry/` and `scripts/` as the source of truth and regenerate `dist/` using the existing build process. Do not alter generated assets by hand, claim rights approval without evidence, or add a new approval bot or CI gate. Use the existing validation commands in [AGENTS.md](AGENTS.md#validation) and report checks that were not run.


## Issue handoff and development progress

Use the issue and PR's actual state as evidence. Classification, authorization,
implementation, review and completion are **different decisions**:

1. **Intake / triage:** A newly filed issue starts with `status: needs triage`.
   Check evidence or reproduction, duplicate open/closed issues and overlapping
   PRs, repository scope, type, priority, size, dependencies, and verifiable
   acceptance criteria. A maintainer removes the intake label only after
   confirming the saved GitHub metadata. Do not infer priority, size, or triage
   completion automatically from the title or an AI suggestion.
2. **Ready:** Triage completion alone does not authorize development. Record
   the Ready decision in the issue only when the intended outcome and non-goals are bounded, blockers
   have been resolved, and any repository-specific product, architecture,
   safety or compatibility decisions have been accepted. Unresolved research
   remains investigation; blocked work records its dependency and next action.
3. **In Progress:** Before maintainer-directed or autonomous implementation,
   identify the actual implementer in the GitHub Assignee field, check whether
   another open PR already owns the change, and link the implementation PR to
   its issue. Human-led outside contributors may propose a change on an
   unclaimed issue without prior assignment or an AI-tool-specific approval;
   coordinate with existing assignees and follow the local contribution rules.
4. **In Review:** A PR is in review only when its scoped change and verification
   evidence are available. Check the required CI on the final PR head, test
   coverage appropriate to the risk, unresolved review findings and any
   repository-specific independent review or live-system validation. A bot
   review or passing CI cannot replace an outstanding product/safety decision.
5. **Done:** Record the actual disposition: a merged and validated change,
   a completed investigation with evidence, or an explained duplicate/not-
   planned closure. Use an issue-closing PR keyword only if merging actually
   satisfies its acceptance criteria. A merged PR is not proof that any
   deferred integration, fault, security or release verification has passed.

**Tracking without boards:** GitHub Issues and pull requests are the only
workflow tracker. The sole lifecycle label is `status: needs triage` for
unreviewed intake. Once triage is completed, remove that label after checking
the actual saved issue metadata; do not create `status: ready`, `status: in
progress`, or other duplicate workflow labels. Record the **Ready** decision,
remaining dependencies, and next action in the issue. For **In Progress**,
identify the actual implementer using Assignees and add a concise start/handoff
comment; link the working PR when it exists. **In Review** is visible from the
linked open, non-draft PR and its actual review/check status. A **Blocked**
issue records the blocker, responsible party, and unblock condition in a
comment. **Done** is the issue's Closed state with the recorded validated
outcome or explained disposition, not merely the existence of a merged PR.
Do not configure or depend on GitHub Projects/boards. Priority measures impact,
and size estimates effort; neither represents work-in-progress.
This guidance introduces no new automated merge gate and does not supersede
this repository's design, testing, security, or release requirements.
