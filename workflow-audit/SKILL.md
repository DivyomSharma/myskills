---
name: workflow-audit
description: Run a structured audit of a codebase area: tenant isolation, authorization, security, UX, or architecture drift. Use when asked to audit, review security, or check tenancy or permissions.
---

# workflow-audit

Announce "Using workflow-audit to <purpose>".

## Flow (tenancy and data access)
1. Inspect schema and migrations.
2. Inspect row-level security policies.
3. Inspect the tenant wrapper and how queries obtain it.
4. Grep for queries that bypass the wrapper.
5. Inspect the service layer and server actions for authorization checks.
6. Run isolation tests; if none exist, write one that proves user A cannot read tenant B.
7. Report findings.

## Flow (other audits)
Pick the matching project skill (security, ux, architecture). Same shape: inspect, enumerate, test, report.

## Report
One line per finding: `path:line severity problem. fix.` Order by severity. State what was not checked. Do not fix unless asked.
