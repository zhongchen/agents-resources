---
title: Herdr sidebar `pane` token shows the pane name, not the pane ID
summary: no built-in token renders the w1:p2 ID; use a custom $pane_id token; sidebar layout is client config, server reload-config does not refresh it
tags: [herdr, terminal-multiplexer]
date: 2026-10-11
confidence: confirmed
---

**Problem:** Show a pane's public ID (`w1:p2`) in the Herdr sidebar, and get
an edited `ui.sidebar.*.rows` layout to take effect.

**Cause:** Two separate traps. The built-in `pane` sidebar token renders the
pane *name* (the label set by `herdr pane rename`), which is usually unset,
so it renders nothing. No built-in token renders the pane ID. And sidebar
layout is client-local config: `herdr server reload-config` applies server
config only and does not refresh a running client's sidebar.

**Fix / Fact:** Report the ID as a custom token from each pane's shell and
reference it with the `$` prefix:

```zsh
# .zshrc
if [[ -n "${HERDR_ENV:-}" && -n "${HERDR_PANE_ID:-}" ]]; then
  herdr pane report-metadata "$HERDR_PANE_ID" --source shell --token "pane_id=${HERDR_PANE_ID}" &>/dev/null
fi
```

```toml
[ui.sidebar.agents]
rows = [
  ["state_icon", "machine", "workspace", "tab", { token = "$pane_id", fg = "#6c7086" }],
  ["agent"],
]
```

Backfill live panes by looping
`herdr pane report-metadata <id> --source shell --token pane_id=<id>`; a
pane keeps its token until a new shell runs in it. Apply the new layout with
the client reload action `prefix+shift+r` (`keys.reload_config`), not
`herdr server reload-config`.

Related trap: `herdr config check` on a config with an unknown token prints
a TOML parse error and then an interactive auto-fix prompt (`overwrite
config.toml? (y/n)`). In a non-interactive script it hangs forever. Reject
candidate token names with a timeout, or accept `config: ok` as proof the
token exists.

**Applies to:** herdr `config.toml` `[ui.sidebar.*].rows`, herdr 0.9.x.
