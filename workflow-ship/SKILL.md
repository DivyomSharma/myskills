---
name: workflow-ship
description: Pre-merge and deploy gate: verifies the definition of done, runs checks, reviews the diff, and prepares the PR or release. Use when asked to ship, release, merge, or prepare a PR.
---

# workflow-ship

Announce "Using workflow-ship to <purpose>".

## Flow
1. `git status` and `git diff` against the base branch. Flag unrelated changes.
2. Run typecheck, lint, unit tests, and e2e if configured.
3. Walk templates/definition-of-done.md; each line needs evidence.
4. Check migrations are reviewed and reversible. Never apply to production without explicit approval.
5. Check env vars the change needs exist in the target environment (names only).
6. Prepare the PR: summary, test evidence, risks, rollback.
7. Open the PR or deploy only when the user says so. After deploy, check deployment logs and error monitor if connected.

## Stop
Report pass or fail per gate. A failed gate blocks shipping.
