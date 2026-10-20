---
title: AWS SDK v2 old sts module silently drops IRSA and uses the node role
summary: Mixed AWS SDK v2 versions break web identity; default chain falls back to instance profile
tags: [aws, java, kubernetes]
date: 2026-10-14
confidence: confirmed
---

**Problem:** After an AWS SDK v2 version bump, a JVM app on EKS gets
`AccessDenied` / `not authorized` errors. The error names the node
instance role (for example `assumed-role/<karpenter-node-role>/i-...`)
and not the IRSA role. The service account, `AWS_ROLE_ARN`, and
`AWS_WEB_IDENTITY_TOKEN_FILE` are all correct. The `sts` module is on the
classpath.

**Cause:** A transitive dependency (for example `flink-connector-aws-base`)
pins `sts` (and `aws-query-protocol`, `apache-client`) to an older SDK
version, while `sdk-core` is the newer version. Old `sts` with new
`sdk-core` throws `NullPointerException: No CLIENT_ENDPOINT_PROVIDER was
configured`. `DefaultCredentialsProvider` catches it, skips
`WebIdentityTokenFileCredentialsProvider`, and resolves credentials from
`InstanceProfileCredentialsProvider` (IMDS). The app logs no error unless
the chain logs at DEBUG. A smaller version gap can work by chance and hide
the mismatch until a later bump.

**Fix / Fact:**
- Check the resolved versions of all `software.amazon.awssdk` modules,
  not only the ones you declare. Every module must use the same version.
  - sbt: `sbt "export <project>/Runtime/managedClasspath"` (resolves
    only, no compile).
  - Maven: `mvn dependency:tree -Dincludes=software.amazon.awssdk`.
- Pin every SDK module to one version: use the AWS SDK BOM in Maven or
  Gradle. In sbt, add `dependencyOverrides` for the modules that drift
  (`sts`, `aws-query-protocol`, `apache-client`).
- To confirm in the pod, call
  `WebIdentityTokenFileCredentialsProvider.create().resolveCredentials()`
  with the app classpath. The exception shows the real cause.
- In a fat jar, read the bundled module version from
  `software/amazon/awssdk/core/util/VersionInfo.class`
  (`unzip -p app.jar <path> | strings`).

**Applies to:** AWS SDK for Java v2, seen with sdk-core 2.55.x and sts
2.20.x. Any build tool, any workload that uses IRSA or web identity.
