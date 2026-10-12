---
title: Never commit sensitive information to GitHub repositories
summary: No secrets or confidential data in any repo, private or public; check the staged diff first
tags: [security, git, github]
date: 2026-10-11
confidence: confirmed
---

**Rule:** Never commit sensitive information to any GitHub repository, whether the repo is private or public. This covers credentials, API keys, tokens, passwords, private keys, certificates, connection strings, and internal confidential data. Review the staged diff for these before every commit. Keep secrets out of the tree with .gitignore, sops, or a secret manager such as 1Password. Never add secrets to make a build or test pass.

**Why:** A private repo can change visibility, get cloned, or leak through integrations. A secret committed to git is permanent once pushed.

**Applies to:** git commits and pushes, all repositories.
