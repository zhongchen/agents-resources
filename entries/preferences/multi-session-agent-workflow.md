---
title: Build apps in small agent sessions from a shared plan
summary: Short AGENTS.md + per-session PLAN.md sections, one branch per session, owner merges
tags: [agents, workflow, cost, planning]
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
- Each session: new branch `sN-<slug>`, commit there, do not push or
  merge. The owner tests and merges, then the next session starts.
- End of session: tick status, add one-line decisions to PLAN.md, so the
  next session needs no chat history.
- One feature per session. A session with several features costs much
  more than the sum of small ones, because context grows with each step.
- Before an agent runs with auto-approval, stash the owner's uncommitted
  edits so the agent cannot commit them.
- Verify each session yourself (checks, coverage, a real run) before you
  report; cheap models can leave placeholder code or miss input bugs.

**Why:** Saves tokens and keeps each change small enough to test by hand.

**Applies to:** multi-step app builds driven by AI agents.
