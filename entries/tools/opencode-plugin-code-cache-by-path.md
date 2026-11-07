---
title: opencode keeps old compiled code for an edited local plugin
summary: Editing a local plugin does not reload it; re-adding the path, touch, and /api/location/reload keep the old module; restart the service
tags: [opencode, config]
date: 2026-11-06
confidence: confirmed
symptoms:
  - "/api/location/reload"
  - "opencode service restart"
  - "Unknown tool"
  - "plugin reconciliation completed"
---

**Problem:** A local plugin under `~/.config/opencode/plugins/` was
rewritten. The running opencode server kept executing the previous
version. The plugin's tool descriptions, tool set, and behaviour all
stayed old, so a tool name added in the edit answered `Unknown tool` for
hours.

**Cause:** opencode compiles a local plugin into a module cache keyed by
its resolved file path, so the cache survives every reload path. Confirmed
on v2.2.5:

- An in-place rewrite of the file: old code still ran.
- `touch` on the file: old code still ran.
- Deleting the plugin and re-creating it at the same path (symlink or
  copy): old code still ran, even though the server logged
  `plugin reconciliation completed` and a fresh `loading plugin` line.
- `POST /api/location/reload`: re-read config, but old plugin code still
  ran.
- Copying the file to a new name in the same directory: the new code ran
  immediately, which proves the cache is keyed by path, not by directory
  scan.
- `opencode service restart`: new code ran.

**Fix:** After changing a local plugin, run `opencode service restart` and
then check the new behaviour, not just the log. A log line that says the
plugin loaded does not prove the current code is running. To confirm fast,
include a unique marker string in a tool description and search for it.

For a temporary check, copy the plugin to a new file name in the same
directory. A new path gets a fresh compile.

**Applies to:** opencode v2 (verified on 2.2.5), local plugins loaded from
`plugins/` or the `plugins` config array.
