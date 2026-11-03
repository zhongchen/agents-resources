---
title: Herdr has no event-subscription API; poll for state changes
summary: herdr api only offers snapshot/schema, no watch/subscribe; live tooling must poll
tags: [herdr, terminal-multiplexer]
date: 2026-10-02
confidence: confirmed
symptoms:
  - "herdr api"
  - "herdr pane list --workspace <id>"
---

**Problem:** Building external tooling that reacts to Herdr state changes
(pane cwd, agent status, revision) in near-real-time.

**Cause:** `herdr api` only exposes `snapshot` (point-in-time state) and
`schema` (type definitions). There is no subscribe/watch/event-stream
command in the CLI.

**Fix / Fact:** Any live-updating external tool (e.g. a status-bar script)
has to poll `herdr workspace list` / `herdr pane list --workspace <id>` on
an interval and diff against previously seen state, rather than reacting to
pushed events. A 2-3 second poll interval is cheap enough for per-pane
metadata updates (title, custom tokens) without noticeable lag.

**Applies to:** external scripts/automation built against the herdr CLI or
socket API.
