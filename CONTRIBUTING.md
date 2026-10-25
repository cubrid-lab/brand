# Contributing to CUBRID Lab Brand

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


## Issue ownership and agent handoff

Before implementation, check the latest source, open issues and overlapping PRs. Keep each change focused on one independently reviewable brand or asset task. New issues begin with `status: needs triage`; maintainers verify duplicates, scope, type and relative urgency against the local open backlog, then confirm one `priority: critical/high/medium/low` and one `size: XS/S/M/L/XL`. Remove the status only after checking the saved GitHub labels and the actual triage decision.

Human contributors may propose or implement unclaimed work without a required AI tool or pre-approval. Maintainer-operated autonomous agents need explicit authorization and a verified assignee before taking reserved work. Preserve the distinction between design approval, legal/trademark clearance and code review: passing tests or an AI review does not approve a public brand asset.

Keep `tokens/`, `registry/` and `scripts/` as the source of truth and regenerate `dist/` using the existing build process. Do not alter generated assets by hand, claim rights approval without evidence, or add a new approval bot or CI gate. Use the existing validation commands in [AGENTS.md](AGENTS.md#validation) and report checks that were not run.
