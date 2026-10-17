---
name: engineering-standards
description: Global engineering rules for any code change: understand before editing, reuse existing structure, preserve invariants, verify, review the diff. Use at the start of any implementation, refactor, or bug fix. Project skills and CLAUDE.md override it.
---

# engineering-standards

Announce "Using engineering-standards to <purpose>".

## When
Any change to code, config, or schema.

## How
1. Read the project CLAUDE.md and the nearest existing implementation of the same thing.
2. State the invariants the change touches (tenancy, auth, data loss, public API).
3. Reuse an existing component, helper, or pattern. Add a new abstraction only when none fits.
4. Fix the root cause. No duplicated guards.
5. Do not rewrite working systems without evidence they are broken.

## Verify
Run the smallest sufficient proof: typecheck, the relevant test, and for UI the browser (see qa-loop). Review `git diff` for unrelated changes before committing.

## Stop
When the definition of done (templates/definition-of-done.md) is satisfied. Do not add speculative features.
