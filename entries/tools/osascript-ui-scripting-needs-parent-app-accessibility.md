---
title: osascript UI scripting fails with -1728 because the agent's parent app lacks Accessibility
summary: The responsible process for TCC is the ancestor app (herdr), not osascript; adhoc signing breaks the grant
tags: [macos, herdr, agents]
date: 2026-11-09
confidence: confirmed
symptoms:
  - "System Events got an error: osascript is not allowed assistive access. (-1728)"
  - "osascript is not allowed assistive access"
  - "AXIsProcessTrusted()"
---

**Problem:** In an agent session, `osascript -e 'tell application "System
Events" to tell process "X" to get name of every window'` fails with:
`execution error: System Events got an error: osascript is not allowed
assistive access. (-1728)`. The error names `osascript`, so it looks like
osascript is misconfigured. Plain AppleScript
such as `tell application "Finder" to get name of home` keeps working in the
same shell, which makes the failure look random.

**Cause:** Two separate permissions are involved.

1. Reading process names (`get name of every process`) is allowed by Apple
   Events. Reading **windows and UI elements** needs Accessibility
   (`kTCCServiceAccessibility`), a different grant.
2. TCC attributes the request to the **responsible process**, which is the
   app at the top of the process tree, not `osascript`. In a herdr session
   the chain is `herdr server` -> `zsh` -> `opencode` -> `zsh` -> `osascript`.
   The grant must exist for `herdr`.

`herdr` is adhoc-signed with no bundle: `Signature=adhoc`,
`Info.plist=not bound`, `designated => cdhash H"..."`. TCC stores an adhoc
grant against the **CDHash**, so every rebuild of the binary silently voids
the grant and `-1728` comes back with no prompt and no log entry.

**Fix / Fact:**
- Confirm the grant: `osascript -e 'tell application "System Events" to get
  UI elements enabled'` returns `true` when Accessibility is held.
- Check attribution: compare `AXIsProcessTrusted()` in a compiled helper
  against the failing call.
- Grant Accessibility to the **stable ancestor app**, not to osascript: add
  the terminal app or herdr under System Settings > Privacy & Security >
  Accessibility.
- To make it durable, give herdr a bundle, an `Info.plist`, and a stable
  signature so the grant is not keyed to a CDHash. Otherwise re-grant after
  every rebuild.
- Avoid Accessibility entirely when a target has a real API. For a browser,
  the DevTools protocol needs no TCC grant and gives better data than UI
  scripting.

Do not expect the log to explain it: `TCC.db` is SIP-protected
(`authorization denied` on read and on copy) and unified-log TCC decisions
are redacted, so there is often no evidence trail of when or why the grant
changed.

**Applies to:** macOS 26 with any agent harness whose shell is a child of an
adhoc-signed or unbundled app. `-1728` here is a permission error, not a
missing-application error.
