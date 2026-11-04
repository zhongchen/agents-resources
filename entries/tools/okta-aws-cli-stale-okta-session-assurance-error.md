---
title: okta-aws-cli web device grant fails assurance check until the browser Okta session is refreshed
summary: Stale or weaker Okta web session makes the device grant fail; log out of Okta in the browser, sign in, retry
tags: [aws, security]
date: 2026-11-04
confidence: confirmed
symptoms:
  - "The application's assurance requirements are not met by the 'subject_token'"
  - "okta-aws-cli web"
guard: none - the CLI cannot force a fresh Okta authentication; the fix needs a browser logout
---

**Problem:** `okta-aws-cli web` prints the device activation URL, then exits with:

```
Error: Okta API returned an error: The application's assurance requirements are not met by the 'subject_token'.
```

The same command works for other AWS profiles, so the profile, role ARN, and IdP ARN look correct.

**Cause:** The device grant reuses the existing Okta web session. Okta compares the assurance level of the token from that session against the assurance policy of the OIDC app. A stale session, a session created through a different app tile, or a session authenticated with a weaker factor does not satisfy the policy, so the token exchange fails. Retrying the command does not help, because it reuses the same session.

**Fix:** Log out of Okta in the web browser, then sign in again and complete MFA. Retry the command and finish the device activation. If a cached access token is present, delete it before the retry and do not set `OKTA_AWSCLI_CACHE_ACCESS_TOKEN=true`. Removing a leftover `~/.saml2aws` file from an older tool is also worth checking.

**Applies to:** okta-aws-cli 2.x with the `web` command and device authorization, Okta Identity Engine orgs.
