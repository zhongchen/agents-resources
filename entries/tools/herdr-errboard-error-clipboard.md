---
title: Herdr errboard — shared error-code clipboard between panes
summary: prefix+shift+e captures the last error line; prefix+shift+v types it into another pane; sidebar shows $errboard in red
tags: [herdr, terminal-multiplexer, workflow]
date: 2026-10-11
confidence: confirmed
---

**Problem:** Quickly moving an error code seen in one Herdr panel into
another panel (e.g. pasting a ClickHouse `Code: 60` exception into a
different agent's prompt) without mouse copy/paste.

**Fix / Fact:** `~/scripts/herdr/errboard.sh` (symlinked into
`~/.config/herdr/scripts/errboard.sh`), bound in `config.toml` as
`[[keys.command]]` shell commands (prefix is `ctrl+k`):
- `prefix+shift+e` → `errboard.sh push`: with no args, greps the focused
  pane's last 250 output lines for error-looking text (error, exception,
  failed, fatal, refused, denied, timeout, cannot connect, exit status,
  `code: N`) and stores the last match. With args, stores the given text.
  Broadcasts a 60-char short form to every pane's `$errboard` custom
  metadata token with a 10-minute TTL; the full text persists in
  `~/.config/herdr/errboard`.
- `prefix+shift+v` → `errboard.sh pull`: types the stored text into the
  focused pane via `herdr pane send-text` (no Enter — review before
  submitting). CLI: `errboard.sh pull [--enter] [PANE_ID]`.
- `errboard.sh show` / `clear` — print / clear (clear also removes the
  `$errboard` token from all panes, per the merge-not-replace metadata
  behavior).

The sidebar config `[ui.sidebar.agents].rows` has a red
`{ token = "$errboard", fg = "#f38ba8" }` row so all agent panels show the
last shared error. Border titles now start with `[pane_id]` (set by
`pane-status.sh`) so panels are easy to reference.

**Applies to:** herdr multi-agent workflows; `herdr pane read/send-text/
report-metadata`.
