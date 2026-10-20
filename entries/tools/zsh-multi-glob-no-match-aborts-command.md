---
title: zsh aborts the whole command when one glob has no match
summary: one unmatched glob cancels the whole command, so files other globs match are never listed
tags: [zsh, shell]
date: 2026-10-05
confidence: confirmed
---

**Problem:** Checking for a file that may use either casing, e.g.
`ls .github/PULL_REQUEST_TEMPLATE* .github/pull_request_template*`, prints
`zsh: no matches found` and runs nothing. A file that matches only one of the
globs (here lowercase `pull_request_template.md`) is never listed, so the
check falsely reports the file absent.

**Cause:** By default (the `NOMATCH` option), zsh fails the entire command
at expansion time if any glob argument matches nothing. bash instead passes
the unmatched pattern through as a literal and still runs the command.

**Fix / Fact:** Use a single glob that covers the variants: a character
class (`.github/[Pp][Uu][Ll][Ll]_request_template*`), a case-insensitive
`find .github -iname '*pull_request_template*'`, or `setopt null_glob` in
the session.

**Applies to:** zsh generally; any command with multiple glob arguments.
bash is not affected.
