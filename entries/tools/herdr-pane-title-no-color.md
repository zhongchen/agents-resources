---
title: Herdr pane border title has no color or style support
summary: Herdr pane report-metadata --title is plain text; ANSI codes get stripped
tags: [herdr, terminal-multiplexer]
date: 2026-10-02
confidence: confirmed
---

**Problem:** Wanting per-field color (e.g. branch in blue, dirty flag in red)
in a pane's border title set via `herdr pane report-metadata --title`.

**Cause:** Every text field on a pane (`title`, `display_agent`,
`state_labels`) is typed as plain `string`/`string|null` in Herdr's API
schema (`herdr api schema --json`). There is no style/color object attached
to any of them. Confirmed by sending a title with embedded ANSI escape
codes (`\033[31mred\033[0m`) and reading it back: Herdr stripped the escape
bytes entirely, leaving literal `[31mred[0m` text.

**Fix / Fact:** Per-field color only exists in the **sidebar**, via
`[ui.sidebar.agents].rows` / `[ui.sidebar.spaces].rows` config, which
supports `{ token = "...", fg = "#rrggbb", bold = true }` styling. Pane
borders cannot be colored at all; use shape/icon distinctions (different
unicode glyphs) there instead.

**Applies to:** herdr pane borders, `pane report-metadata --title`.
