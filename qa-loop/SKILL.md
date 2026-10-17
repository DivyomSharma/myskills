---
name: qa-loop
description: Drive the running app in a browser to verify a change: functional, permissions and tenant isolation, UX states, responsive, visual match. Use after implementing UI or a user flow, or when asked to test, QA, or screenshot the app.
---

# qa-loop

Announce "Using qa-loop to <purpose>".

## Flow
1. Start the app with the project dev command. Confirm it responds.
2. Open a browser (Playwright or claude-in-chrome). Log in as the relevant role.
3. Exercise the changed flow end to end.
4. Check, as applicable:
   - Functional: create, edit, delete, search, filter, pagination, import and export.
   - Security: user A cannot reach tenant B data by URL or API; each role sees only what it should.
   - UX: loading, empty, error, validation, keyboard.
   - Responsive: mobile width.
   - Visual: screenshot, compare with Figma or the design system for spacing, type, alignment.
5. Read console and network errors.
6. Fix, then re-test the failing step. Repeat until clean.

## Evidence
Report each check with a screenshot path or observed output. A skipped check is reported as skipped.

## Stop
When every applicable check passes. For animated pages, finish with motion-safety-qa.
