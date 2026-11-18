---
title: Setting env.java.opts.all in a Flink chart silently drops forced G1GC
summary: Any env.java.opts.all value stops Flink's taskmanager.sh adding -XX:+UseG1GC, so 1-CPU TaskManagers use SerialGC
tags: [kubernetes, java, config]
date: 2026-11-18
confidence: confirmed
symptoms:
  - "env.java.opts.all"
  - "FLINK_ENV_JAVA_OPTS"
  - "if no other JVM options are set, set the GC to G1"
---

**Problem:** After adding a JVM flag for every Flink job through
`flinkConfiguration` (for example a CVE mitigation such as
`env.java.opts.all: "-XX:-UseBASE64Intrinsics"`), TaskManager GC changes
without any error. Single-CPU TaskManagers start on SerialGC instead of G1.

**Cause:** Flink 1.17 and 2.0 `bin/taskmanager.sh` only adds its default GC
when no JVM options are set at all:

```sh
# if no other JVM options are set, set the GC to G1
if [ -z "${FLINK_ENV_JAVA_OPTS}" ] && [ -z "${FLINK_ENV_JAVA_OPTS_TM}" ]; then
    export JVM_ARGS="$JVM_ARGS -XX:+UseG1GC"
fi
```

`bin/config.sh` fills `FLINK_ENV_JAVA_OPTS` from `env.java.opts.all` in the
YAML config. So any value there, even one unrelated to GC, defeats the
check. The JVM then falls back to its own ergonomic choice, which is
SerialGC with one CPU and G1 with two or more.

**Fix / Fact:** Set `env.java.opts.taskmanager: "-XX:+UseG1GC"` next to
`env.java.opts.all`. TaskManager opts are appended to the same JVM command
line, so G1 is forced again. JobManagers never had G1 forced
(`jobmanager.sh` has no such check), so leave them alone.

**Applies to:** Flink 1.17 and 2.0 on Kubernetes, or anywhere the
FlinkDeployment `flinkConfiguration` carries `env.java.opts.*`.
