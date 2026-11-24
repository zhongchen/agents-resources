---
title: ClickHouse `MODIFY TTL` also rewrites every existing part
summary: MODIFY TTL also schedules a MATERIALIZE TTL rewrite of every part, so a big table blows the DDL timeout
tags: [clickhouse, ci]
date: 2026-11-24
confidence: confirmed
symptoms:
  - "Distributed DDL task /clickhouse/*/task_queue/ddl/query-* is not finished on N of M hosts"
  - "distributed_ddl_task_timeout"
  - "Dirty database version"
  - "MATERIALIZE TTL"
guard: none - fix is the inline SETTINGS clause on the statement; a migration linter can enforce it
---

**Problem:** A migration runs `ALTER TABLE t ON CLUSTER c MODIFY TTL <expr>`
on a table with hundreds of parts and tens of TB. The client waits, then
fails with: `Code: 159 ... Distributed DDL task ... is not finished on 6 of
6 hosts (0 of them are currently executing the task, 0 are inactive). They
are going to execute the query in background. Was waiting for 180.69s,
which is longer than distributed_ddl_task_timeout`. A golang-migrate based
runner then marks its stream `dirty=1`, so every later `up` and `goto`
refuses to run. Meanwhile `system.mutations` shows `MATERIALIZE TTL` still
running with `parts_to_do` in the hundreds, and `system.part_log`
`MutatePart` rows keep growing.

**Cause:** `MODIFY TTL` is two steps. It updates the table metadata, then,
because the session setting `materialize_ttl_after_modify` defaults to `1`,
it schedules a `MATERIALIZE TTL` mutation that reads and rewrites every part
to apply the expression. The metadata step is instant; the mutation is a
full table rewrite. ClickHouse stops *waiting* at
`distributed_ddl_task_timeout` (default 180 s) but does not cancel the work,
so the error reports a timeout while the rewrite carries on. The TTL
expression itself is already in place on every host, which makes the failure
look like bad SQL when it is not.

**Fix:** Make the change metadata only by putting the setting on the
statement that needs it:

```sql
ALTER TABLE db.events_local ON CLUSTER '{cluster}'
    MODIFY TTL toDate(ts) + INTERVAL 15 DAY
    SETTINGS materialize_ttl_after_modify = 0, distributed_ddl_task_timeout = 3600;
```

Existing parts then convert as they merge, and a retry is nearly free:
`AlterCommand::isTTLAlter` compares the formatted expression, so an
unchanged TTL text schedules no second mutation. To convert old parts
deliberately, run `MATERIALIZE TTL IN PARTITION ...` by hand, one partition
at a time, off-peak. Never in a migration.

Do not write a standalone `SET materialize_ttl_after_modify = 0;` above the
`ALTER`. golang-migrate sends each statement as its own `Exec` on a pooled
connection, so the `SET` can land on a different connection, and it would
only affect the initiating host anyway. A linter can reject both forms.

**Recovery when it already failed:** read
`system.distributed_ddl_queue` (per host, via
`clusterAllReplicas('<cluster>', system.distributed_ddl_queue)`) to see
whether the task Finished or is still Active, and `system.tables.engine_full`
to confirm the metadata changed. If the whole file applied, stamp that
version. If only the first statement applied, stamp the version before it,
so the fixed file runs again from the top, and never stamp a version whose
second statement never ran.

**Applies to:** ClickHouse 24.x through 26.x. `distributed_ddl_task_timeout`
default is 180 s; `0` means async, a negative value means wait forever, but
keep it bounded so a stuck host returns an error instead of hanging a sync.
