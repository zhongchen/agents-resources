---
title: Herdr split naming is inverted from tmux; no native pane rotate
summary: Herdr's split_vertical/split_horizontal are swapped vs tmux; no built-in rotate action
tags: [herdr, tmux, terminal-multiplexer]
date: 2026-10-01
confidence: confirmed
symptoms:
  - "split_vertical"
  - "split_horizontal"
  - "prefix+shift+h/j/k/l"
---

**Problem:** Herdr's `split_vertical`/`split_horizontal` config keys look
backwards compared to tmux, and there is no "rotate pane" command.

**Cause:** Herdr names splits like Vim: `split_vertical` = side-by-side,
`split_horizontal` = stacked. tmux uses the opposite. Rotate/cycle-layout is
not implemented.

**Fix / Fact:**
- Default prefix: `ctrl+b`.
- `split_vertical` (side by side): `prefix+v`.
- `split_horizontal` (stacked): `prefix+minus`.
- Move between panes: `prefix+h/j/k/l`. Swap panes (closest built-in
  equivalent to rotate): `prefix+shift+h/j/k/l`.
- No native rotate. Use swap, or the `pane.move` CLI/socket API.
- Reference: `herdr.dev/docs/keyboard/`, `herdr.dev/docs/config-reference/`.

**Applies to:** herdr config `[keys]` split/swap bindings.
