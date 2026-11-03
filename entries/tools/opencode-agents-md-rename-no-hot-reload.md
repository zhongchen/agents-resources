---
title: opencode does not hot-reload replaced files (AGENTS.md, config)
summary: mv or git checkout/commit bypass the file watcher; a symlinked config never reloads on target edits; use /reload or POST /api/location/reload
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
When `~/.config/opencode/opencode.jsonc` is a symlink into another repo
(for example a dotfiles repo), an edit committed on the target file never
reaches the server at all, even hours later, and sessions started after
the edit still get the old default model.

**Cause:** The rename does not trigger the file-watcher rescan, so the
server keeps its cached content. Verified for AGENTS.md on v2.0.25. On
v2.2.3 the config watcher is unreliable even for in-place writes: one
in-place rewrite was followed by a reload with the new content, two
later ones were not. `touch` (mtime change, same content) never triggers
a reload. For a symlinked config the reason is stronger: the watcher
subscribes to the path under `~/.config/opencode`, while file events
carry the real target path; the symlink entry itself never changes, so
no event ever matches. Verified on v2.2.5: a git commit on the target
file and a `touch` on the symlink path both left `GET /api/config`
showing the old model. An MCP server removed from config stays in the
live registry until it is disconnected.

**Fix:** For generated instruction files, write in place (`cat new >
old`), never rename over the target. For config changes made through
git or through a symlinked target, do not rely on the watcher: run
`/reload` in the TUI, or headless with `opencode api post
/api/location/reload`, or restart the service
(`opencode service restart`). On v2.2.5 the `location/reload` POST
re-read the config at once where the touch had done nothing. To drop a
removed MCP server from the live registry, POST
`/api/experimental/mcp/<server>/disconnect` or run `/reload`.

**Applies to:** opencode v2 (verified on 2.0.25, 2.2.3 and 2.2.5).
