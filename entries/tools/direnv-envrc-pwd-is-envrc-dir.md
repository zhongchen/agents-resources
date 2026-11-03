---
title: direnv runs .envrc with PWD set to the .envrc's own directory
summary: direnv runs .envrc with PWD at the .envrc's dir, not the dir you cd'd into; use $OLDPWD
tags: [direnv, git]
date: 2026-10-01
confidence: confirmed
symptoms:
  - "${OLDPWD:-$PWD}"
  - "$OLDPWD"
  - "remote.origin.url"
---

**Problem:** An `.envrc` placed at a parent directory (e.g. `~/.envrc` or
`~/kong/.envrc`) runs for every repo under it, but must read something from the
repo you actually cd'd into, such as `git config --get remote.origin.url` to
pick a token by remote org. With a bare `git config` call the lookup returns
nothing, because the parent directory is not a git repo. The script silently
never fires.

**Cause:** direnv walks up to the nearest `.envrc` and executes it with `$PWD`
set to the directory that contains the `.envrc`, not the directory you cd'd
into. Any command in the script that relies on the current directory reads the
wrong location.

**Fix:** direnv exposes the real directory in `$OLDPWD`. Run commands against
it explicitly:

```bash
git_url="$(git -C "${OLDPWD:-$PWD}" config --get remote.origin.url 2>/dev/null)"
```

The `${OLDPWD:-$PWD}` fallback keeps the script correct when it is sourced
outside direnv, where `$PWD` is the real directory.

**Applies to:** direnv, any `.envrc` that inspects the cd'd-into directory
(git config, files in the repo, and similar). Confirmed with direnv on macOS.
