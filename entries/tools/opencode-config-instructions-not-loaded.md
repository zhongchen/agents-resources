---
title: opencode v2 accepts an instructions array in config but never loads it
summary: The config schema documents the instructions field, but no code reads those files
tags: [opencode, config]
date: 2026-10-11
confidence: confirmed
---

**Problem:** Adding `"instructions": ["/abs/path/rule.md"]` to opencode.json
looks like it loads rule files into every session, and the schema and docs
describe the field, but the rules never reach the model.

**Cause:** opencode v2 validates the field, then drops it. Verified against
the v2 source and on v2.0.25: the only instruction sources are AGENTS.md
discovery, built-in date and environment, skills, MCP, references, and API
session entries.

**Fix:** Put global rules in `~/.config/opencode/AGENTS.md`. To keep one
shared source, build that file by concatenating the rule files.

**Applies to:** opencode v2 (verified on 2.0.25).
