---
name: workflow-incident
description: Production bug flow: error report to reproduction, root cause via git history, patch, test, PR. Use when given a stack trace, Sentry issue, or a report that something broke in production.
---

# workflow-incident

Announce "Using workflow-incident to <purpose>".

## Flow
1. Gather the error: stack trace, release, affected tenant or route. Use the error monitor or deploy logs if connected; otherwise ask for the trace.
2. Reproduce locally or write a failing test. No fix without a reproduction or a stated reason it cannot be reproduced.
3. Find the regression: `git log` and `git blame` on the failing path; identify the introducing change.
4. Patch the root cause, not the symptom.
5. Run the failing test, then the surrounding suite.
6. Commit with the incident reference. Open the PR only when asked.

## Report
Root cause, introducing commit, fix, proof, and any data that needs repair.
