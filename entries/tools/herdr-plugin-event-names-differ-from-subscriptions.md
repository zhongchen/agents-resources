---
title: Herdr plugin event hook names differ from API subscription events
summary: On herdr 0.9.3 a plugin [[events]] hook accepts fewer event names than events.subscribe; pane.updated silently never fires as a hook
tags: [herdr, tui]
date: 2026-11-02
confidence: confirmed
symptoms:
  - "unknown event 'pane.updated'"
  - "herdr plugin link"
  - "pane.updated"
---

**Problem:** A plugin declares an `[[events]]` hook with `on = "pane.updated"`.
The hook never fires. `herdr plugin link` succeeds anyway.

**Cause:** On herdr 0.9.3, plugin event hooks accept a smaller event set than
the socket API `events.subscribe`. `pane.updated` exists as a subscription
event but is not a valid plugin hook name. Linking only records a warning
(`unknown event 'pane.updated'`) in the link response and
`herdr plugin list`; it does not block the link.

**Fix:** Use hook names from the running server's schema
(`herdr api schema`, `EventMatch` entries). Valid plugin hook events on
0.9.3 include: `pane.created`, `pane.exited`, `pane.closed`, `pane.focused`,
`pane.moved`, `pane.agent_detected`, `pane.agent_status_changed`,
`pane.output_changed`, plus `tab.*` and `workspace.*` lifecycle events.
`pane.agent_status_changed` covers the agent session and state reporting
that `pane.updated` would carry as a subscription. Always check the
`warnings` field after `herdr plugin link`.

**Applies to:** herdr 0.9.3 plugin manifests.
