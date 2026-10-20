---
title: No decorative comments in code
summary: Never write banner dividers or comments that restate code; only short comments for non-obvious WHY
tags: [style]
date: 2026-10-01
confidence: confirmed
---

**Rule:** Write no decorative comments in code: no banner dividers
(`#####` lines), no section header comments, no comment that restates
what the code already says. Add a comment only when the WHY is
non-obvious: a hidden constraint, a subtle invariant, a workaround for a
specific bug. Keep such comments short.

**Why:** Default model rules already say to avoid unnecessary comments;
decorative ones were added anyway, so this entry makes the rule explicit.

**Applies to:** general.
