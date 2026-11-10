---
title: rtk rewrites `ps` and returns only the 30 lowest-pid rows with truncated args
summary: Piped ps silently misses high-pid processes; rtk ps returns only pids 1-587 and cuts each args field
tags: [rtk, shell, macos]
date: 2026-11-09
confidence: confirmed
symptoms:
  - "type=renderer"
  - "/bin/ps -Ao pid,rss,args"
  - "rtk ps -Ao pid,rss,args"
---

**Problem:** In a session with rtk's bash rewrite, `ps -Ao pid,rss,args | awk
'/type=renderer/ {print $1}'` returns nothing, and `ps -Ao pid,rss,args |
wc -l` reports 31 lines on a machine running 742 processes. Piping `ps`
through `grep` or `awk` silently misses most of the system.

**Cause:** The rewrite hook replaces `ps` with `rtk ps`, so a command such as
`rtk ps -Ao pid,rss,args` runs instead of the real binary. That form is not a
filtered view: it returns only the 30 lowest-pid rows and truncates each
row's args field. On booted-forever machines pid 587 is roughly the cut-off,
so every GUI app started since login is absent. Chrome renderers, editors,
and agents never appear. `whence -w ps` reports `command` and
`type ps` reports `/bin/ps`, so nothing looks wrong. The failure reads as
"the process does not exist" rather than "the output is incomplete".

`rtk df` is safe: it returns the same row count as `/bin/df`. The problem is
specific to `ps`.

**Fix / Fact:** Call the real binary by absolute path in any script or
pipeline where the process set matters:
`/bin/ps -Ao pid,rss,args | awk '/type=renderer/ {print $1}'`.
rtk leaves an absolute path alone. Verify the rewrite with:
`echo '{"tool_name":"Bash","tool_input":{"command":"ps aux"}}' | rtk hook claude`.
Interactive one-off `ps` calls are fine; only parsed output is affected.

**Applies to:** rtk 0.42.3 with the opencode bash rewrite shim, macOS. `ps`
is a single-word command, so the rewriter always catches it.
