---
title: Personal pull request and commit writing style
summary: PR and commit rules - STE100, Conventional Commits, squash merge, no AI footer
tags: [git, github, communication, style, preferences, commits]
date: 2026-10-14
confidence: confirmed
---

**Rule:**
- Use ASD-STE100 Simplified Technical English. Go straight to the point.
- Follow the repo's pull request template.
- Less is more: no filler, no nice-to-have context, nothing the diff
  already shows.
- No em dashes.
- No "it's not Y, it's Z" phrasing.
- No emojis.
- No "Test plan" section.
- No AI attribution anywhere: no "Generated with Claude Code" footer in
  the PR body, no Co-Authored-By trailer in commit messages.
- Commit subject: Conventional Commits, `type(scope): subject`. Types:
  feat, fix, docs, test, refactor, perf, ci, chore. Imperative, <= 50
  chars, no period. Follow the repo's own commit convention if it has one.
- Commit body: blank line after the subject, wrap at 72, say what changed
  and why. Skip the body only when the subject says it all.
- One commit per logical change. Keep tracking references (plan step,
  ticket) out of the subject.
- Merge PRs by squash. The PR title becomes the commit subject on the
  main branch, so write it like a commit subject; the PR body becomes the
  commit body. The PR keeps the individual commits.

**Why:** Personal preference for PR readability, tone, and minimal token
footprint. GitHub lists show only the commit subject, so a subject that
names a task or session instead of the change says nothing.

**Applies to:** Pull request descriptions and commit messages.
