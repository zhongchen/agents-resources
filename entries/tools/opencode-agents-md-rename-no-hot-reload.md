---
title: opencode does not hot-reload AGENTS.md replaced by rename
summary: Rebuilding AGENTS.md with mv leaves live sessions on the old content; write in place
tags: [opencode, agents-md, watcher]
date: 2026-10-11
confidence: confirmed
---

**Problem:** Rebuilding a global AGENTS.md with the write-temp-then-rename
pattern (`mv new old`) leaves every running opencode session on the old
instructions. New sessions attached to the same server also see the old
content.

**Cause:** The rename does not trigger the file-watcher rescan, so the
server keeps its cached instruction content. An in-place write
(`cat new > old`) does trigger it. Verified on v2.0.25; the watcher
mechanism behind the difference was not isolated.

**Fix:** Build scripts that regenerate AGENTS.md must write in place, not
rename over the target.

**Applies to:** opencode v2 (verified on 2.0.25).
