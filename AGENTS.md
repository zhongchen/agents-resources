# AGENTS.md

This is Zhong's personal knowledge bank for AI coding agents. Any agent, on
any model, working in any of his projects, reads it for reusable lessons and
personal conventions, and contributes new ones back. The repo is public on
GitHub so auto-merge and branch protection work, but it is not meant for
outside contributors. Treat it as personal, not a community project.

## Read before you write

1. Read `INDEX.md` first. It is a short, one-line-per-entry summary of
   everything in the bank, grouped by topic.
2. Open only the specific entry files under `entries/` that are relevant to
   your current task. Do not read the whole repo into context.
3. If nothing in the index covers your situation, proceed with your task as
   normal. Only come back here to contribute if you learn something worth
   keeping (see below).

## When to contribute

Add an entry when you confirm something that:

- Took real effort to figure out: a non-obvious gotcha, a tool quirk, a
  version-specific bug, a subtle failure mode.
- Is a personal convention or preference Zhong has stated and wants applied
  consistently across projects: communication style, PR rules, tooling
  defaults, workflow habits.
- Generalizes beyond the one project you were in. Project-specific business
  logic does not belong here.
- Is not already covered by an existing entry. Check `INDEX.md` first. If a
  close match exists, update that entry instead of adding a near-duplicate.

Do not add: speculation, one-off trivia, anything that depends on internal
business context, or anything that just duplicates public documentation you
could instead link to.

## What must never go in this repo

- Credentials, tokens, API keys, connection strings.
- Customer names, internal hostnames, internal URLs, internal ticket or
  project codenames.
- Proprietary business logic, pricing, or architecture specific to one
  company's systems.
- Anything confidential or under NDA.

If you are unsure whether something is safe to share, leave it out.

## How to contribute

1. Branch: `knowledge/<topic>-<short-slug>`, or a batch name for several
   entries at once.
2. Add or edit entries under `entries/<topic>/`, using the template in
   `CONTRIBUTING.md`. One commit per entry; each commit runs
   `python scripts/build_index.py` and includes the updated `INDEX.md`, so
   every commit is self-contained. Never hand-edit `INDEX.md`.
3. Have several entries ready at once? Put them in one PR, not several.
   Separate PRs opened close together both touch `INDEX.md` and conflict.
4. Open a pull request using the PR template.
5. CI validates the entries (schema, secret-pattern scan) and confirms
   `INDEX.md` matches what the script would generate. Once checks pass, the
   PR auto-merges. No need to wait for a human.

## Style

Write in plain, direct language any model can parse: state the fact and what
it applies to. Technical entries use Problem/Cause/Fix/Applies-to. Preference
entries use Rule/Why/Applies-to. No narrative, no chain-of-thought, no
tool-specific jargon unless the entry is specifically about that tool. Cut
anything not essential: the bank will grow large, and every token here is
paid by every future reader.

The 100-character guide for `summary` is soft. Keep only essential info, and
exceed 100 rather than drop something essential.
