# Contributing

This repo takes contributions from both humans and AI agents. See
`AGENTS.md` first for what belongs here and what must never be included.

## Topics

Entries live under `entries/<topic>/`. Use an existing topic when it fits:

- `git` — git and GitHub mechanics
- `tools` — CLI tools, editors, package managers
- `languages` — language and runtime quirks
- `infra` — cloud, containers, CI/CD, networking
- `testing` — test frameworks and practices
- `security` — security gotchas and fixes
- `preferences` — personal conventions: communication style, PR rules,
  workflow habits
- `misc` — anything else

Create a new topic directory only if nothing existing fits.

## Entry template

Save as `entries/<topic>/<short-kebab-slug>.md`:

```
---
title: Short, specific title
summary: One line, about 100 chars, shown in INDEX.md
tags: [tag1, tag2]
date: YYYY-MM-DD
confidence: confirmed   # or: tentative
---

**Problem:** What situation triggers this.

**Cause:** Why it happens, if known.

**Fix / Fact:** The actual lesson.

**Applies to:** Languages, tools, versions, or "general".
```

For a `preferences` entry (a personal convention, not a bug), use this body
shape instead:

```
**Rule:** The convention, stated directly.

**Why:** The reason, if stated.

**Applies to:** When this convention kicks in.
```

The 100-character summary length is a guide, not a hard limit. Keep only
essential info. Exceed 100 when you have to. Never cut essential info just
to fit.

Keep entries under 200 lines. One idea per entry. See
`entries/git/push-default-upstream-lands-on-main.md` for a worked technical
example and `entries/preferences/reporting-style.md` for a worked preference
example.

## Workflow

1. Branch: `knowledge/<topic>-<slug>`, or a batch name for several entries.
2. Add or edit entries. One commit per entry, each running
   `python scripts/build_index.py` and including the updated `INDEX.md`, so
   every commit is self-contained.
3. Several entries ready at once: one PR, not several. Separate PRs opened
   close together both touch `INDEX.md` and conflict.
4. Open a PR with the PR template filled in.
5. CI validates the entries, confirms `INDEX.md` is up to date, and scans
   for secret-shaped strings.
6. On success, the PR auto-merges.

## What CI checks

- Required frontmatter fields are present and well-formed.
- No duplicate titles.
- Entry length limit.
- No secret-shaped strings (API keys, private keys, tokens).
- `INDEX.md` matches what `scripts/build_index.py` would generate.

CI is a backstop, not a substitute for judgment. See `AGENTS.md` for what
should never be submitted in the first place.
