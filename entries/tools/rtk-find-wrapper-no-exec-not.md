---
title: rtk rewrites `find` to `rtk find`, which rejects `-not` and `-exec`
summary: rtk rewrites find to `rtk find`; -not/-exec fail, and command find does not help; use /usr/bin/find
tags: [rtk, shell]
date: 2026-10-05
confidence: confirmed
symptoms:
  - "does not support compound predicates"
  - "/usr/bin/find"
  - "-exec"
---

**Problem:** Running `find . -not -path ...` or `find . -exec ...` in a
session with rtk's bash rewrite fails with: `rtk: rtk find does not support
compound predicates or actions (e.g. -not, -exec). Use `find` directly.`
Prefixing with `command find` does not help: rtk rewrites that to
`command rtk find`, which fails the same way.

**Cause:** The rewrite hook replaces `find` with `rtk find` before the shell
runs it. There is no shell function: `whence -w find` reports `command`.
`rtk find` handles a simple subset of flags and refuses compound predicates
and actions. The rewriter skips a command it does not read as a single
`find`, so `find ... | head -3` runs unchanged, which makes the failure
look intermittent.

**Fix / Fact:** Call the real binary by absolute path:
`/usr/bin/find . -iname '*.hcl' -not -path '*cache*'`. rtk leaves an
absolute path alone. Check the behavior with
`echo '{"tool_name":"Bash","tool_input":{"command":"find . -not -name x"}}' | rtk hook claude`.

**Applies to:** rtk 0.42.3 with the opencode bash rewrite shim. Reproduce
with `rtk find . -not -name x`.
