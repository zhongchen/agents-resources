---
title: launchd agents run with a minimal environment
summary: Homebrew and user-local bin dirs aren't in PATH by default; set PATH/HOME in the plist
tags: [launchd, macos]
date: 2026-10-02
confidence: confirmed
symptoms:
  - "EnvironmentVariables"
  - "launchctl bootstrap gui/"
  - "/opt/homebrew/bin"
guard: the herdr LaunchAgents set EnvironmentVariables PATH and HOME in ~/Library/LaunchAgents/com.herdr.*.plist
---

**Problem:** A script that works fine run by hand fails silently (or can't
find a command) when run as a `launchd` user agent (LaunchAgent).

**Cause:** launchd does not source the user's shell profile. Its default
`PATH` is just `/usr/bin:/bin:/usr/sbin:/sbin`. Tools installed via
Homebrew (`/opt/homebrew/bin`) or into a user-local bin dir
(`~/.local/bin`) are not found unless the script hardcodes their full path
or the plist sets `PATH` explicitly.

**Fix / Fact:** Add an `EnvironmentVariables` dict to the `.plist` with an
explicit `PATH` (and `HOME`, if the script relies on it):
```xml
<key>EnvironmentVariables</key>
<dict>
    <key>PATH</key>
    <string>/Users/you/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    <key>HOME</key>
    <string>/Users/you</string>
</dict>
```
Also point `StandardOutPath`/`StandardErrorPath` at log files so failures
are visible, and load with
`launchctl bootstrap gui/$(id -u) <plist>` + `launchctl enable gui/$(id -u)/<label>`
(the modern replacement for `launchctl load -w` on current macOS).

**pyenv shims need more than `PATH`:** adding `~/.pyenv/shims` to `PATH`
is not enough to fix a pyenv-managed `python3`. The shim still needs to
resolve a version (via `PYENV_ROOT`, `PYENV_SHELL`, and `.python-version`
lookups) that launchd's bare environment doesn't provide. Skip the shim
entirely: point `ProgramArguments` at the concrete interpreter, e.g.
`~/.pyenv/versions/3.12.4/bin/python3`, instead of `python3`.

**Applies to:** macOS LaunchAgents/LaunchDaemons running scripts that
depend on Homebrew or user-local tools, including pyenv-managed
interpreters.
