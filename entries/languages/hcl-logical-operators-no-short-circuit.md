---
title: HCL logical operators do not short-circuit
summary: "a == null || length(a) errors on null; guard with a ternary instead of ||"
tags: [hcl, terraform, validation]
date: 2026-10-12
confidence: confirmed
---

**Problem:** A variable validation like
`group.node_types == null || length(group.node_types) > 0` fails with
"Invalid function argument ... argument must not be null" when
`group.node_types` is null. Under `terraform console` the same expression
crashes the CLI with a stack trace.

**Cause:** HCL evaluates both operands of `&&` and `||` eagerly. There is no
short-circuit, so `length(null)` runs even when the left side of `||` is
true.

**Fix / Fact:** Guard with a lazy ternary, since a conditional expression
evaluates only the taken branch:
`group.node_types != null ? length(group.node_types) > 0 : true`.

**Applies to:** HCL2 expressions in Terraform and OpenTofu, general.
