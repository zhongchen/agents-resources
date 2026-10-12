---
title: ClickHouse quota counters are per node behind a load-balanced endpoint
summary: Quota limits never trip through a load-balanced endpoint; counters are per node
tags: [clickhouse, quotas, load-balancing]
date: 2026-10-07
confidence: confirmed
---

**Problem:** A `CREATE QUOTA` with small limits (for example `MAX queries = 3`
per minute) never trips when tested against a multi-node ClickHouse cluster
through its load-balanced HTTP endpoint. Every test query succeeds, far past
the limit. Re-checking `system.quotas_usage` shows zero counters everywhere.

**Cause:** Quota usage counters live on the node that executes the query
("accumulated amounts are stored on the requestor server", per ClickHouse
docs). An endpoint that load balances each new connection spreads queries
across nodes, so each node sees only a fraction of the traffic and no node
exceeds the limit. The effective limit through the endpoint is roughly
limit x node count. Verified side effects: `queries` is checked before
execution, `result_rows` is checked after (an over-limit SELECT still
executes, then the response is rejected), and interval windows align to
wall-clock boundaries, so a "1 minute" interval ends at the next minute
mark, not 60 seconds after the first query.

**Fix / Fact:** To test a quota, pin all test queries to one node: send
several requests over a single HTTP keep-alive connection (curl with one
`--data` body and the same URL repeated reuses the connection), or connect
to one node directly. To inspect counters cluster-wide, query
`clusterAllReplicas('<cluster>', 'system.quotas_usage')`; the per-node
`system.quotas_usage` shows only that node's view. When sizing real limits
behind a load balancer, multiply by node count, or use keyed quotas.

**Applies to:** ClickHouse (verified on 26.3), any load-balanced multi-node
ClickHouse endpoint.
