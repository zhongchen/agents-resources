---
title: crossterm sends uppercase letters with SHIFT and a raw \n as Ctrl+J
summary: A modifiers.is_empty() guard drops uppercase letters; raw-mode \n arrives as Char('j') + CONTROL
tags: [rust, crossterm, ratatui, tui, keyboard]
date: 2026-10-14
confidence: confirmed
---

**Problem:** In a crossterm/ratatui text input, typing `X-Test` gives
`-est`. Separately, a `j` key binding fires on Ctrl+J, or on a stray `\n`
that reaches the app.

**Cause:** crossterm reports an uppercase letter as `KeyCode::Char('X')`
with `KeyModifiers::SHIFT`, so a `key.modifiers.is_empty()` guard rejects
it. In raw mode the byte `\n` is decoded as `Char('j')` with `CONTROL`, so
a binding that matches `Char('j')` without checking modifiers fires.

**Fix / Fact:**
- Text input: accept a char when only SHIFT is set:
  `KeyCode::Char(c) if (key.modifiers - KeyModifiers::SHIFT).is_empty()`.
- Shortcuts: match plain keys with `key.modifiers.is_empty()`, or check the
  exact modifier set.

**Applies to:** crossterm 0.28/0.29 legacy keyboard decoding, ratatui apps.
