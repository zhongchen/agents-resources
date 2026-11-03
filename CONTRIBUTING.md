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

## Allowed tags

Tags are for grouping, not keywords. Put specific keywords (for example
`irsa`, `globbing`) in the title and summary. Agents search `INDEX.md`,
which shows titles and summaries, not tags.

Pick tags from the bullet list below. Entry shape:

1. The folder is the main category. Do not add a tag that only repeats
   the folder name.
2. Use subject tags for what the entry is about. They come from the
   Tools, Platforms, and Languages and builds groups.
3. Use 0 to 2 concern tags. They come from the Concerns group.
4. Use at most 4 tags per entry. CI fails an entry with more than 4 tags.

The Preferences group is for `preferences/` entries only.

Use flat names, one name per idea. Do not build a hierarchy like
`aws/sts`. For known aliases, CI suggests the canonical name. The alias
map is `TAG_ALIASES` in `scripts/validate_entries.py`.

Add a tag only when at least 2 entries need it and no listed tag fits.
Remove a tag when no entry uses it. Edit the list in its own
PR. That PR touches a file outside `entries/`, so it does not auto-merge
and a human reviews it. Retag the affected entries in the same PR.

Review tags with `python scripts/tag_report.py`. The same report lists
entries older than 90 days and entries with `confidence: tentative`. A
monthly workflow opens an issue with the report.

CI reads the bullet lines below. A tag not on the list gives a warning,
not a failure, so the entry still merges.

- Tools: `git`, `github`, `github-actions`, `herdr`, `opencode`, `tmux`, `zsh`, `direnv`, `launchd`, `rtk`
- Platforms: `aws`, `clickhouse`, `kubernetes`, `terraform`, `macos`
- Languages and builds: `java`, `rust`, `hcl`
- Concerns: `agents`, `ci`, `config`, `cost`, `quotas`, `security`, `shell`, `testing`, `tui`, `terminal-multiplexer`
- Preferences: `communication`, `style`, `workflow`

## Entry template

Save as `entries/<topic>/<short-kebab-slug>.md`:

```
---
title: Short, specific title
summary: One line, about 100 chars, shown in INDEX.md
tags: [tag1, tag2]
date: YYYY-MM-DD
confidence: confirmed   # or: tentative
symptoms:              # optional, see below
  - "exact error text or command"
guard: none            # optional, see below
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

## Symptoms

`symptoms` is optional. Use it on any entry whose trigger is text a session
will actually see: an error message, an exception class, a failing command,
a config key. Copy the text verbatim from the entry body. Do not paraphrase
and do not invent text that the entry does not show. Short forms are fine
when they are an exact substring (`NoClassDefFoundError`, not
`class not found error`).

Agents search the bank with `scripts/kb.py search "<error text>"`. A
symptom hit ranks above a body hit, so a good list puts the right entry in
the top result when the agent has no idea where the problem lives.

Keep 1 to 4 items. Leave the field out for a preference entry or for a
lesson with no distinctive text. A symptom must be an exact substring of
the entry; CI does not check that, so check it yourself.

## Guards

`guard` is optional. It answers one question for the next reader: is this
already prevented on this machine, and by what?

A setting that prevents it:

```
guard: git config --global push.default=current (set 2026-11-02) - a bare push follows the branch name
```

A protection that is on purpose:

```
guard: none - noclobber is deliberate; the fix stays "use >| or a fresh file name"
```

Apply the setting before you record it. Name the exact key, value, and
file or command. `grep -rn '^guard:' entries/` lists every live guard, and
serves as the checklist after a machine rebuild.

Record `none` with a reason when a reader might otherwise disable a
protection to silence the problem. Leave the field out when there is
nothing to prevent.

Keep entries under 200 lines. One idea per entry. See
`entries/git/push-default-upstream-lands-on-main.md` for a worked technical
example and `entries/preferences/reporting-style.md` for a worked preference
example.

## Workflow

1. Branch: `knowledge/<topic>-<slug>`, or a batch name for several entries.
2. Enable the hook once per clone: `git config core.hooksPath .githooks`.
   It rebuilds `INDEX.md` before each commit that touches `entries/` and
   runs the validator, so the index is never stale.
3. Add or edit entries. One commit per entry, so every commit is
   self-contained.
4. Several entries ready at once: one PR, not several. Separate PRs opened
   close together both touch `INDEX.md` and conflict.
5. Open a PR with the PR template filled in.
6. CI validates the entries, confirms `INDEX.md` is up to date, and scans
   for secret-shaped strings.
7. On success, the PR auto-merges.

## What CI checks

- Required frontmatter fields are present and well-formed.
- No duplicate titles.
- Tags not in the allowed list (warning, with a suggested name for known aliases).
- At most 4 tags per entry.
- Entry length limit.
- No secret-shaped strings (API keys, private keys, tokens).
- `INDEX.md` matches what `scripts/build_index.py` would generate.

CI is a backstop, not a substitute for judgment. See `AGENTS.md` for what
should never be submitted in the first place.
