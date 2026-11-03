---
title: Herdr plugin state directory lives under ~/.local/state, not ~/.config
summary: HERDR_PLUGIN_STATE_DIR is ~/.local/state/herdr/plugins/<id>; plugin config dir is under ~/.config, so manual script runs guess wrong
tags: [herdr, config]
date: 2026-11-02
confidence: confirmed
symptoms:
  - "HERDR_PLUGIN_STATE_DIR"
  - "~/.local/state/herdr/plugins/"
  - "~/.config/herdr/plugins/"
---

**Problem:** A plugin script run manually, without the `HERDR_PLUGIN_STATE_DIR`
variable that herdr injects, needs a fallback path for its state files. The
obvious guess `~/.config/herdr/plugins/...` is wrong: the script reads empty
or missing state while the plugin's own hooks use a different directory.

**Cause:** Herdr splits the two plugin directories across XDG roots:
plugin config lives at `~/.config/herdr/plugins/config/<plugin-id>`, but
plugin state lives at `~/.local/state/herdr/plugins/<plugin-id>`.
`herdr plugin config-dir <id>` prints only the config path.

**Fix:** Default the manual-run fallback to
`$HOME/.local/state/herdr/plugins/$HERDR_PLUGIN_ID` and keep
`HERDR_PLUGIN_STATE_DIR` first when herdr invokes the script. Never store
plugin state by hand next to the config dir.

**Applies to:** herdr 0.9.3 plugin scripts that persist state.
