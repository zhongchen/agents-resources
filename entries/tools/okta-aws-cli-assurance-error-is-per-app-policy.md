---
title: okta-aws-cli web assurance check fails per AWS federation app, not per Okta session
summary: The assurance error is often per-app policy, not a stale session; open the app tile
tags: [aws, security]
date: 2026-11-04
confidence: confirmed
symptoms:
  - "The application's assurance requirements are not met by the 'subject_token'"
  - "okta-aws-cli web"
  - "invalid_grant"
guard: none - per-app Okta assurance policy; no local setting can satisfy it
---

**Problem:** `okta-aws-cli web` prints the device activation URL, then exits with:

```
Error: Okta API returned an error: The application's assurance requirements are not met by the 'subject_token'.
```

**Cause:** There are two distinct causes with the same error text. Tell them apart before you try a fix, because the fixes differ.

1. **Per-app assurance policy.** Each AWS federation app carries its own assurance requirement. One app accepts the current session and another rejects it, from the same browser and the same minute. The Okta access token can carry identical claims in both cases (`amr` with `mfa`, `otp`, `pwd`, same IdP, same user), and the failing profile still fails. The rejection is on the app SSO exchange: `POST /login/token/sso` returns HTTP 400 with `invalid_grant` and the assurance description.
2. **Stale or weak session.** The device grant reuses the existing Okta web session. If Okta raised the requirement for the whole org, every profile fails and a browser logout plus re-login fixes it.

**Triage:** refresh a profile pinned to a different federation app, in the same minute.

```
okta-aws-cli web --profile <other-app-profile> --open-browser=false
```

- If the other app succeeds and yours fails, it is cause 1. Do not log out. The session is fine.
- If every profile fails, it is cause 2. Log out of Okta in the browser, sign in, complete MFA, retry.

`--debug-api-calls` shows which cause it is. Check the `amr` claim in the ID token and compare it with the HTTP 400 on the app SSO exchange. Identical claims plus a 400 means the app policy is the difference, not the factors.

**Fix for cause 1:** open the AWS federation app tile for that account in the browser, then retry the CLI. If the tile loads, the app policy passes and the very next `okta-aws-cli web` succeeds with no other change. If the tile also fails, the policy needs an Okta admin: relax it, or enroll the user in the factor it demands.

**Do not** assume a browser logout is the fix. It costs a full MFA round trip and does nothing for cause 1. A re-login that "fixes" it can also just be the tile-open side effect.

**Applies to:** okta-aws-cli 2.x with the `web` command and device authorization, Okta Identity Engine orgs with more than one AWS federation app. Profile to federation app mapping lives in `~/.okta/okta.yaml` under `aws-acct-fed-app-id`.
