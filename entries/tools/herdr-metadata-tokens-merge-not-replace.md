---
title: Herdr custom metadata tokens merge, not replace
summary: pane report-metadata --token values persist across calls until explicitly cleared
tags: [herdr, terminal-multiplexer]
date: 2026-10-02
confidence: confirmed
symptoms:
  - "herdr pane report-metadata"
  - "--token NAME=VALUE"
  - "--clear-token"
---

**Problem:** A pane shows a stale custom token (e.g. a branch name or
status flag) after the condition that set it no longer applies.

**Cause:** `herdr pane report-metadata <pane_id> --token NAME=VALUE` adds
or updates that token but does not clear tokens from earlier calls.
Confirmed by setting `branch` and `dirty` in one call, then a second call
setting only `stale`: both `branch` and `dirty` were still present
afterward. Tokens accumulate per pane until removed.

**Fix / Fact:** Explicitly pass `--clear-token NAME` in the same or a later
call whenever a token no longer applies. A polling script that derives
tokens from live state each cycle must clear every token it owns on every
iteration where that token's condition is false, not just stop setting it.

**Applies to:** `herdr pane report-metadata --token` / `--clear-token`.
