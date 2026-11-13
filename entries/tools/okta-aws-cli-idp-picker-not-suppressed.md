---
title: okta-aws-cli web keeps prompting "Choose an IdP" after a successful Okta login
summary: IdP picker means the AWS federation app choice; pin aws-acct-fed-app-id per profile in okta.yaml
tags: [aws, security, config, tui]
date: 2026-11-12
confidence: confirmed
symptoms:
  - "Choose an IdP:"
  - "error asking for IdP selection: error running picker: could not open a new TTY"
  - "okta-aws-cli web --profile"
guard: none - the fix is a per-profile aws-acct-fed-app-id key in the okta.yaml profiles map
---

**Problem:** `okta-aws-cli web --profile <name>` finishes the browser device authorization, then shows a `Choose an IdP:` picker. The profile already sets `aws-iam-role` and `aws-iam-idp` in the `profiles` map of `~/.okta/okta.yaml`, so it should not ask for anything.

**Cause:** The picker title is misleading. It is the AWS federation app list, not the SAML IdP list. The CLI calls `/api/v1/users/me/appLinks` with the OIDC client and keeps the entries whose app name is the AWS federation app type. When the client is assigned to two or more of them, the CLI always prompts. `aws-iam-idp` cannot suppress this prompt: the app-link objects carry no `identityProviderArn`, so the comparison that would skip the picker never matches.

A second, separate picker can appear after the app is chosen, when the SAML assertion offers more than one IdP ARN. That one does become a single choice once `aws-acct-fed-app-id` and `aws-iam-idp` are both pinned.

**Fix:** Add `aws-acct-fed-app-id` to the profile in `~/.okta/okta.yaml`:

```yaml
awscli:
  profiles:
    my-profile:
      org-domain: "example.okta.com"
      oidc-client-id: "..."
      aws-acct-fed-app-id: "<app instance id>"
      aws-iam-role: "arn:aws:iam::111111111111:role/admin"
      aws-iam-idp: "arn:aws:iam::111111111111:saml-provider/okta"
      write-aws-credentials: true
      open-browser: true
```

Find the app instance id from the appLinks body `appInstanceId` field. To capture it without a second login, run `okta-aws-cli web --profile <name> --debug-api-calls 2>&1 | tee out.log`, then parse the appLinks JSON array out of `out.log`. The OIDC access token in that log is a live bearer token: delete the log after use.

Without a TTY the picker fails instead of waiting:

```
Error: error asking for IdP selection: error running picker: could not open a new TTY: open /dev/tty: device not configured
```

That error means the pins are incomplete, not that the command needs a terminal.

**Applies to:** okta-aws-cli 2.6.x with the `web` command, `~/.okta/okta.yaml` profiles, Okta Identity Engine orgs.
