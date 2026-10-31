---
title: OpenCode live session cost is in the session_v2 SQLite table, not session
summary: opencode.db session table is legacy and near-empty; live per-session cost and token totals are in session_v2
tags: [opencode, agents, cost]
date: 2026-10-31
confidence: confirmed
---

**Problem:** You read per-session cost or token totals from the OpenCode
database (`~/.local/share/opencode/opencode.db`), or a session ID reported by
another tool (for example herdr `agent list`) is missing from your query
results.

**Cause:** OpenCode v2 migrated sessions to a new `session_v2` table. The
old `session` table still exists and its schema has the same cost/token
columns, but it holds only a few stale rows. A query against `session`
returns nothing for live sessions, which looks like a missing session.

**Fix / Fact:**
- Query `session_v2`. It has the aggregates already computed: `cost`,
  `tokens_input`, `tokens_output`, `tokens_reasoning`, `tokens_cache_read`,
  `tokens_cache_write`. No need to sum per-message rows.
- `session` is the pre-v2 schema; keep it only as a fallback.
- OpenCode holds the DB in WAL mode while running. A read-only SQLite open
  (`file:...?mode=ro`) can fail because SQLite needs write access to the
  `-shm` file; fall back to a normal open.

**Applies to:** opencode v2.x, SQLite WAL mode.
