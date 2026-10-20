---
title: Build apps in small agent sessions from a shared plan
summary: Short AGENTS.md + per-session PLAN.md sections, one PR per session, owner squash-merges
tags: [agents, workflow, cost]
date: 2026-10-14
confidence: confirmed
---

**Rule:**
- Keep a short `AGENTS.md` (purpose, goals, non-goals, code map,
  conventions, test rules, commands, session protocol). Every session
  loads it, so every line costs tokens on every session.
- Keep `docs/PLAN.md` with one section per session: files to open, scope,
  tests to add, done criteria. A session reads only its own section.
- Start each session fresh with `Do session N from docs/PLAN.md.`
- Each session: new branch `sN-<slug>`, commit there, push, open a PR,
  do not merge. The owner tests and squash-merges, then the next session
  starts. CI runs on the PR before the merge.
- Pin the toolchain (e.g. `rust-toolchain.toml`) so local checks and CI
  run the same linter version; a newer CI linter fails code that passes
  locally.
- End of session: tick status, add one-line decisions to PLAN.md, so the
  next session needs no chat history.
- One feature per session. A session with several features costs much
  more than the sum of small ones, because context grows with each step.
- Before an agent runs with auto-approval, stash the owner's uncommitted
  edits so the agent cannot commit them.
- Verify each session yourself (checks, coverage, a real run) before you
  report; cheap models can leave placeholder code or miss input bugs.
- When a plan section changes existing behavior, name what must not
  change and require a test for it. Agents build exactly what the plan
  says and test only its example; an unstated invariant breaks silently.
  When you verify, run the cases next to the planned one (the opposite
  type, the old behavior, edit-save-edit-save in one run) with real data.

**Why:** Saves tokens and keeps each change small enough to test by hand.

**Applies to:** multi-step app builds driven by AI agents.
