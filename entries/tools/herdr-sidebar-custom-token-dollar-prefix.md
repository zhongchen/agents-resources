---
title: Herdr sidebar custom tokens need a $ prefix in config
summary: { token = "branch" } fails; must be { token = "$branch" } to show custom metadata
tags: [herdr, terminal-multiplexer, toml]
date: 2026-10-02
confidence: confirmed
---

**Problem:** `config.toml` fails to parse (or `herdr config check` reports
`unknown sidebar token`) when referencing a custom pane metadata token in
`[ui.sidebar.agents].rows` or `[ui.sidebar.spaces].rows`.

**Cause:** Built-in tokens (`state_icon`, `state_text`, `machine`,
`workspace`, `tab`, `pane`, `agent`, `terminal_title`, ...) are referenced
by bare name. Custom values reported through
`pane report-metadata --token NAME=VALUE` must be referenced with a `$`
prefix: `$NAME`. Writing `{ token = "branch" }` instead of
`{ token = "$branch" }` is rejected with
`unknown sidebar token \`branch\`; custom tokens must start with \`$\``.

**Fix / Fact:** Always prefix custom token references with `$` in row
config, e.g.:
```toml
[ui.sidebar.agents]
rows = [
  ["state_icon", "agent", "workspace", "tab"],
  [{ token = "$branch", fg = "#89b4fa" }],
]
```
Run `herdr config check` after editing to catch this before
`server reload-config`.

**Applies to:** herdr `config.toml`, `[ui.sidebar.*].rows`.
