---
name: workflow-feature
description: End-to-end flow for building a new feature from a one-line request to a reviewed PR: requirements, architecture, design, implementation, tests, docs. Use when asked to build, add, or implement a feature or module.
---

# workflow-feature

Announce "Using workflow-feature to <purpose>".

## Flow
1. Read project CLAUDE.md and load the relevant project skills (architecture, tenancy, database, ui).
2. Restate the problem and acceptance criteria. Ask only if a material product, security, or data choice is unresolved.
3. Inspect existing models, components, and patterns for reuse.
4. Propose the approach in a few lines. Wait only if the choice is hard to reverse.
5. If UI is involved, use workflow-new-screen for the screen work.
6. Implement. Typecheck and run tests as you go.
7. Run qa-loop for any user-facing change.
8. Security pass if data access or authorization changed (workflow-audit).
9. Update docs or write an ADR if architecture changed.
10. Check templates/definition-of-done.md, review the diff, commit per git-workflow.

## Stop
When done-list is satisfied with evidence. Report what changed, proof, and unresolved risks.
