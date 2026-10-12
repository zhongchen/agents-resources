---
title: Herdr config edits need server reload; pane-status.sh edits need daemon kickstart
summary: UI config (sidebar rows, keybinds) is not picked up until reload-config; the pane-status bash loop holds old code until launchctl kickstart
tags: [herdr, terminal-multiplexer, launchd]
date: 2026-10-11
confidence: confirmed
---

**Problem:** Edited `config.toml` (e.g. new sidebar token rows) or
`~/scripts/herdr/pane-status.sh`, but nothing changes in the running Herdr UI.
This caused a "sidebar still not showing $pane_id" report even though the token
was reported on every pane.

**Cause:** Two separate staleness sources.
1. Herdr does not re-read `config.toml` automatically. UI settings need an
   explicit client reload.
2. `pane-status.sh` runs `while true` in a single long-lived bash process
   under launchd (`com.herdr.pane-status`). Bash parsed the whole script at
   startup, so on-disk edits never take effect in the running loop.

**Fix / Fact:**
- After editing `config.toml`: `herdr config check`. Reload sidebar and
  layout settings with the client reload `prefix+shift+r` (prefix is
  `ctrl+k`), not `herdr server reload-config`. See
  `herdr-pane-token-name-not-id.md`.
- After editing `pane-status.sh` (or any launchd-managed loop script):
  `launchctl kickstart -k gui/$(id -u)/com.herdr.pane-status`.

**Applies to:** herdr `config.toml`, `~/scripts/herdr/*`, launchd jobs
`com.herdr.pane-status` / `com.herdr.agent-cost`.
