---
title: Smoke-test a TUI app headlessly with tmux
summary: Drive a TUI with tmux send-keys and read the screen with capture-pane; -e keeps colors
tags: [tmux, tui, testing, agents]
date: 2026-10-14
confidence: confirmed
---

**Problem:** An agent cannot see a TUI app, so it cannot check key flows
end to end. Unit and snapshot tests miss real terminal input bugs.

**Fix / Fact:**
- Start: `tmux new-session -d -s t -x 120 -y 30 "./app; sleep 5"`. The
  `sleep` keeps the pane open so a crash message stays readable.
- Wait about 1 s before sending keys. Keys sent before the app enters raw
  mode get line-buffered and translated (`\r` becomes `\n`, which crossterm
  reads as Ctrl+J).
- Keys: `tmux send-keys -t t j Tab Enter`. Literal text:
  `tmux send-keys -t t -l "X-Test"`.
- Read: `tmux capture-pane -t t -p`. Add `-e` to keep ANSI color codes, to
  check syntax highlighting or focus colors.
- Run against a copy of any data file the app saves to.
- In zsh, `tmux` can be an alias; call `$(whence -p tmux)` in scripts.

**Applies to:** any terminal UI (ratatui, Bubble Tea, Textual) on macOS or
Linux.
