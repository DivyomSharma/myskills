---
name: verity-adr-gate
description: Use before writing, numbering, or citing any Verity ADR (Architecture Decision Record) — "write an ADR for X", "what's the next ADR number", "is there already a decision about Y", "accept this architecture decision". Also use when a taskplan or CLAUDE.md says a capability "requires ADR before generalizing". Prevents a real mistake this project already made once: writing an ADR under a number already taken in a different register.
license: Apache 2.0
---

Authority: `taskplans/99_verity_custom_skills_plan.md` Skill 2. Traces to a
real mistake, same project: an ADR got written into `CLAUDE.md` as
"ADR-013" without checking `verity-spec/17_decisions/adr/`, which already
had an *accepted* ADR-013 (Global HQ Operator Security Model). The wrong
number shipped, had to be found by accident while scanning for something
unrelated, and corrected across five files. This skill exists so that
never happens twice.

## The three registers — check ALL of them, every time

Verity has **three separate places** that number architecture decisions.
They are not one list:

1. **`verity-spec/17_decisions/adr/adr-NNN.md`** — the canonical,
   accepted-decision register. This is the one that actually matters; a
   number "used" here is used, full stop.
2. **`CLAUDE.md`'s own "Accepted decisions currently in force" section** —
   a curated highlight reel, explicitly flagged in the file itself as
   **stale past ADR-012** ("This list stops at ADR-012 and is stale... check
   the register before assuming an ADR number is unused"). Never trust
   this list alone for the next free number — it undercounts.
3. **`taskplans/17A_verity_architecture_decisions.md`** — a *separate*
   `V2-ADR-*` namespace. Different prefix, different sequence, do not
   confuse a `V2-ADR-N` slot with a plain `ADR-N` slot or vice versa.

## Procedure

1. `ls verity-spec/17_decisions/adr/` — this is ground truth for the next
   plain `ADR-NNN` number. Take the highest existing number and add one.
2. Grep `CLAUDE.md` for `ADR-` to see what it currently claims — if it
   disagrees with step 1 (i.e. shows a lower "stops at" number), that's
   expected staleness, not a signal to use its number. Register 1 wins.
3. If the decision is in the `V2-ADR-*` series specifically (platform-
   architecture decisions per `taskplans/17A`), check that file's own
   sequence separately — it does not share numbers with plain `ADR-N`.
4. Write the canonical file at `verity-spec/17_decisions/adr/adr-NNN.md`
   (or the `V2-ADR` equivalent in `17A`), following the format of the
   most recent existing ADR in that same register — read one before
   writing, don't invent a new template.
5. Update **every** citing location in one pass: `CLAUDE.md`'s "Accepted
   decisions" section (add the new entry; if it changes what the "stale
   past ADR-N" line should say, update that line too — don't let it drift
   further), any taskplan whose "requires ADR" note this decision resolves,
   and any code comment that names the decision it's implementing.
6. Grep the whole repo for the number you just assigned before finishing,
   to catch a collision this checklist itself might have missed (a
   half-written draft ADR left in `implementation/`, for instance — see
   `implementation/adr-013-hq-operator-security-proposal.md`, which is
   exactly a superseded draft with the old wrong number, renamed and
   marked superseded rather than deleted, precisely so a future search
   doesn't repeat the original mistake by finding it first).

## Non-goals

- Not a spec for what makes a good ADR — that's a judgment call per
  decision. This skill only prevents the numbering/register mistake.
- Not a replacement for actually reading the existing ADRs before writing
  a new one that might conflict with or duplicate an accepted decision.
