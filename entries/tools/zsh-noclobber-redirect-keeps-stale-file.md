---
title: zsh noclobber makes > fail and leaves the old file in place
summary: With noclobber, > to an existing file errors, and the next command silently reads stale data
tags: [zsh, shell, redirect]
date: 2026-10-14
confidence: confirmed
---

**Problem:** `cmd > /tmp/out.json; parse /tmp/out.json` gives old results.
The only sign is a `file exists: /tmp/out.json` line that is easy to miss.

**Cause:** With `setopt noclobber`, zsh refuses `>` onto an existing file.
`cmd` does not run into the file, and `;` runs the next command anyway, on
the file from the previous run.

**Fix / Fact:** Use `>|` (or `>!`) when you mean to overwrite. Or use a
fresh file name per run, or chain with `&&` so a failed redirect stops the
chain.

**Applies to:** zsh with `noclobber` set; scripts and agent shell commands
that reuse temp files.
