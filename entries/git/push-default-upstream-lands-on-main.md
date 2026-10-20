---
title: git push can land on main with push.default=upstream
summary: Bare `git push` on a branch checked out from origin/main can push straight to main
tags: [git, github]
date: 2026-09-30
confidence: confirmed
---

**Problem:** Running `git push origin <branch>` (or a bare `git push`) appears
to push to `<branch>`, but silently lands on `main` instead.

**Cause:** When a branch is created with `git checkout -b foo origin/main`, its
upstream is set to `origin/main`. With `push.default=upstream` (or `tracking`),
`git push` pushes to the branch's configured upstream, not to a same-named
remote branch.

**Fix:** Always push new branches with an explicit refspec:
`git push -u origin foo:foo`. This sets `foo`'s upstream to `origin/foo`, so
later bare pushes go to the right place.

**Applies to:** git, any repo using `push.default=upstream` or `tracking`.
