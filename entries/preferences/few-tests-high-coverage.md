---
title: Few tests, high coverage
summary: Small test budget; table-driven tests, one mock round trip, UI snapshots; add a case before a test
tags: [testing]
date: 2026-10-14
confidence: confirmed
---

**Rule:**
- Set a small test budget for the whole project (about 10-15 test
  functions). Add a case to an existing table or snapshot before adding a
  new test function.
- Pure logic: table-driven tests, many cases per function.
- I/O: one round trip against a local mock server per external boundary.
- UI: snapshot tests of rendered screens.
- Test behavior through public functions, not internals. No test-only
  production code except named injection points.
- Coverage target: about 80% lines, excluding entry points and the event
  loop.

**Why:** Keeps the suite cheap to maintain and to run, while coverage stays
high.

**Applies to:** all projects unless the repo states its own test policy.
