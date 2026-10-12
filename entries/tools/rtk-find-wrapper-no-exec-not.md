---
title: rtk's `find` shell wrapper rejects `-not` and `-exec`
summary: rtk shadows `find` as a shell function; -not/-exec fail, call /usr/bin/find by absolute path
tags: [rtk, find, shell]
date: 2026-10-05
confidence: confirmed
---

**Problem:** Running `find . -not -path ...` or `find . -exec ...` in a
session with rtk's hook-based command rewriting fails with: `rtk: rtk find
does not support compound predicates or actions (e.g. -not, -exec). Use
`find` directly.` Prefixing with `command find` does not help, since `find`
is a shell function (not a binary on PATH), so `command` still resolves to
the same wrapper.

**Cause:** rtk replaces `find` with a token-optimized proxy via a shell
function, not a PATH binary. Its parser only handles a simple subset of
`find`'s flags and refuses anything with `-not`, `-exec`, or other compound
predicates/actions, even though real GNU/BSD `find` supports them.

**Fix / Fact:** Call the real binary directly by absolute path, e.g.
`/usr/bin/find . -iname '*.hcl' -not -path '*cache*'`. This bypasses the
shell function entirely and behaves like standard `find`.

**Applies to:** Any shell session with the rtk Claude Code hook installed,
when using `-not`, `-exec`, or other predicates/actions rtk's `find` proxy
doesn't support.
