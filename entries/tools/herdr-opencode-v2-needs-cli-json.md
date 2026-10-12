---
title: Herdr never resumes OpenCode v2 panes without cli.json
summary: Stale tui.json makes herdr skip cli.json; no session ID is reported, so no resume
tags: [herdr, opencode]
date: 2026-10-12
confidence: confirmed
---

**Problem:** After a Herdr server restart, Claude Code panes resume but
OpenCode panes come back as plain shells. `herdr integration status` shows
OpenCode as current. `agent_session` is missing for the OpenCode pane in
`herdr pane list` and `~/.config/herdr/session.json`.

**Cause:** Herdr resumes a pane only if the agent reported a session ID. For
OpenCode, only the TUI plugin reports it. OpenCode v2 ignores `tui.json` and
`tui.jsonc`. It loads TUI plugins from `~/.config/opencode/cli.json`. The
installer skips creating `cli.json` when a v1 `tui.json` exists, so the v2
registration is never written. The status command only checks that files exist.

**Fix / Fact:** Move `~/.config/opencode/tui.json` aside, run
`herdr integration install opencode`, then confirm `cli.json` contains
`"plugins": ["./herdr-opencode"]`. Restart each OpenCode TUI. Only sessions
the restarted TUI reports are resumed; panes open before the fix are not.
Check with `herdr pane list`: the pane must show `agent_session` with
`source: herdr:opencode`.

**Applies to:** Herdr 0.9.x, OpenCode 2.x.
