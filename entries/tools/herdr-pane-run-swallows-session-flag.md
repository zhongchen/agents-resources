---
title: herdr pane run swallows --session as the global CLI session flag
summary: pane run never delivers opencode/kimi/pi/kilo resume commands; their --session flag selects a herdr session instead; use pane send-text plus send-keys
tags: [herdr, cli]
date: 2026-11-02
confidence: confirmed
---

**Problem:** `herdr pane run <pane_id> opencode --session ses_x` fails with
`server_not_running` and nothing reaches the pane. The same call with a
leading `--` types a literal `--` into the shell.

**Cause:** `--session` is a global herdr CLI flag (`herdr --session <name>`
selects a named persistent session). The clap parser claims it before
`pane run` sees the command, so the resume argv is cut and herdr tries to
connect to a session named `ses_x`. Any resume command that starts with
`--session` or another herdr global flag is affected. `claude --resume`
worked only because `--resume` is not a herdr flag.

**Fix:** Type the command instead of running it:
`herdr pane send-text <pane_id> 'opencode --session ses_x'` followed by
`herdr pane send-keys <pane_id> enter`. `pane send-text` takes the whole
command as one argument, so no flag parsing happens.

**Applies to:** herdr 0.9.3 `pane run`, and any command text that begins
with a herdr global flag.
