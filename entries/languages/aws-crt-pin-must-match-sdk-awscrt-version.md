---
title: Pinned aws-crt must match the AWS SDK v2 awscrt.version
summary: Old pinned aws-crt with newer aws-crt-client fails at runtime with NoClassDefFoundError
tags: [aws, java, aws-sdk, aws-crt, sbt, maven]
date: 2026-10-14
confidence: confirmed
---

**Problem:** After an AWS SDK v2 bump, code that uses `aws-crt-client`
(for example an OpenSearch Serverless or S3 CRT client) fails at runtime
with `NoClassDefFoundError: software/amazon/awssdk/crt/...` (for example
`crt/http/HttpStreamManager`). The build compiles without errors.

**Cause:** `aws-crt` (group `software.amazon.awssdk.crt`) has its own
version line, separate from the SDK version. Builds often pin it with a
platform classifier and exclude the transitive version. The pin then stays
old while `aws-crt-client` moves to a newer SDK version that calls new CRT
classes.

**Fix / Fact:**
- Each SDK release needs a specific `aws-crt` version. Find it as
  `<awscrt.version>` in
  `https://repo1.maven.org/maven2/software/amazon/awssdk/aws-sdk-java-pom/<sdk>/aws-sdk-java-pom-<sdk>.pom`.
- Update the pinned `aws-crt` version at the same time as every SDK bump.
  Example: SDK 2.55.16 needs aws-crt 0.48.5.
- A check that "all `software.amazon.awssdk` modules have the same
  version" does not cover `aws-crt`. Check it separately.

**Applies to:** AWS SDK for Java v2 with `aws-crt-client`, any build tool.
