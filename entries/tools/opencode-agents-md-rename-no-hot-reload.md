---
title: opencode does not hot-reload replaced files (AGENTS.md, config)
summary: mv or git checkout/commit bypass the file watcher; config reload is unreliable, use /reload or restart
tags: [opencode, agents, config]
date: 2026-10-31
confidence: confirmed
---

**Problem:** Rebuilding a global AGENTS.md with the write-temp-then-rename
pattern (`mv new old`) leaves every running opencode session on the old
instructions. New sessions attached to the same server also see the old
content. The same happens to `opencode.jsonc`: a config edit committed
through git (an editor rename plus commit) stayed inactive; the running
service kept the old MCP server URL and its connection state for hours.

**Cause:** The rename does not trigger the file-watcher rescan, so the
server keeps its cached content. Verified for AGENTS.md on v2.0.25. On
v2.2.3 the config watcher is unreliable even for in-place writes: one
in-place rewrite was followed by a reload with the new content, two
later ones were not. `touch` (mtime change, same content) never triggers
a reload. An MCP server removed from config stays in the live registry
until it is disconnected.

**Fix:** For generated instruction files, write in place (`cat new >
old`), never rename over the target. For config changes made through
git, do not rely on the watcher: run `/reload` in the TUI or restart the
service (`opencode service restart`). To drop a removed MCP server from
the live registry, POST `/api/experimental/mcp/<server>/disconnect` or
run `/reload`.

**Applies to:** opencode v2 (verified on 2.0.25 and 2.2.3).
