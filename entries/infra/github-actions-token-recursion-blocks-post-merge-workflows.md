---
title: GITHUB_TOKEN merges don't trigger other push-triggered workflows
summary: Auto-merge via GITHUB_TOKEN skips downstream push workflows on the same branch
tags: [github, github-actions, ci]
date: 2026-09-30
confidence: confirmed
---

**Problem:** A workflow that rebuilds a generated file on `push` to `main`
(for example, regenerating an index from source files) never runs after a
PR is merged through GitHub's auto-merge feature, even though the merge
commit clearly changes the watched paths.

**Cause:** GitHub Actions does not start a new workflow run for events
produced using the default `GITHUB_TOKEN`, to prevent infinite recursive
runs. A squash merge performed by `gh pr merge --auto` (or GitHub's
auto-merge backend) inside a workflow using `secrets.GITHUB_TOKEN` counts
as a GITHUB_TOKEN-driven event, so the resulting push to the base branch
does not fire other `on: push` workflows.

**Fix:** Do not rely on a post-merge, push-triggered workflow to keep a
generated file in sync. Generate the file as part of the PR itself (commit
it alongside the source change) and add a CI check on the PR that fails if
the generated file is out of date. This avoids the token-recursion gap
entirely, since the file is already correct by the time the PR merges.

**Applies to:** GitHub Actions, any repo using `gh pr merge --auto` or
GitHub's native auto-merge feature with a `push`-triggered downstream
workflow.
