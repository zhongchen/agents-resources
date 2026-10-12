---
title: Only one quota per user is ever consumed; execution_time bills inter-chunk elapsed only
summary: Attaching multiple quotas to a user silently does nothing; execution_time skips single-block queries
tags: [clickhouse, quotas]
date: 2026-10-07
confidence: confirmed
---

**Problem:** Two traps make ClickHouse quotas look broken when they are not.
First: attaching several quotas to one user (e.g. one quota limiting
execution_time, another limiting written_bytes) silently does nothing for all
but one of them — usage is billed to a single arbitrary quota and the others
never enforce or even appear in `system.quotas_usage`. Second: an
`execution_time` limit never trips for queries whose result arrives in one
block (scalars, `LIMIT n` results, `sleep()`, small aggregations), so testing
it with `SELECT sleep(2)` or a single-row result reports "not enforced" while
a streaming query enforces fine.

**Cause:** `QuotaCache::chooseQuotaToConsumeFor` (src/Access/QuotaCache.cpp)
iterates the user's quotas, takes the first match, and breaks — exactly one
quota object consumes all usage; the rest are dead objects. There is no
unioning of limits across quotas. For execution_time,
`LimitsCheckingTransform::checkQuota` bills only the elapsed time between
output chunks, with the stopwatch starting when the first output chunk
reaches the transform — a one-block result bills ~zero. Upstream issue #993
(closed as minor, "not intended to work" as a true query-time limit)
documents the same behavior.

**Fix / Fact:** Give a user exactly ONE quota and put every needed limit
inside it (one quota can hold multiple intervals, each with its own limits).
Verify resource limits one at a time: `read_bytes` and `written_bytes` are
checked during execution and interrupt the query mid-flight;
`result_rows` is checked after execution; `queries` is checked before. To
test execution_time, use a streaming query (`SETTINGS max_block_size = 2`
forces many chunks) so time accrues between chunks. Verified on
26.3.33.10001.altinitystable: with a single quota per user, read_bytes,
written_bytes, and execution_time all count and enforce correctly —
including MergeTree reads and INSERT SELECT writes.

**Applies to:** ClickHouse (mechanism confirmed in 26.3 source; observed
behavior on 26.3.33.10001.altinitystable).
