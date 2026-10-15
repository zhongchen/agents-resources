---
title: Run opencode headless and read the cost of one session
summary: opencode run --auto -m runs without prompts; per-session cost comes only from session export
tags: [opencode, agents, cost]
date: 2026-10-14
confidence: confirmed
---

**Problem:** You want another agent to run a scoped task on a cheaper model
without approval prompts, then report what that one session cost.
`opencode stats` shows only totals across all sessions.

**Fix / Fact:**
- Run: `opencode run --auto -m <provider>/<model> --title "<name>" "<prompt>"`
  from the repo dir. `--auto` approves all permissions not explicitly
  denied. `opencode models` lists valid model IDs.
- Find the session: `opencode session list` (scoped to the current
  project dir; columns: id, title, time).
- Cost: `opencode session export <id> >| /tmp/s.json`, then sum every
  `cost` field on objects that also have a `tokens` object. Redirect to a
  file; piping the export straight into a parser gave truncated JSON.
- The cost uses opencode's price table. A gateway can bill a different
  rate; check the gateway for the real amount.

**Applies to:** opencode v2.0.x.
