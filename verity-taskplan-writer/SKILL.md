---
name: verity-taskplan-writer
description: Use when creating a new file under `taskplans/` in the Verity repo — "write a taskplan for X", "add a task plan", "log this as a new taskplan". Scaffolds the correct number and the established structure (Authority citation, Status, trigger, scope, non-goals) instead of hand-authoring one from a blank file, and updates `00_STATUS_INDEX.md` in the same pass so the new file doesn't start already stale.
license: Apache 2.0
---

Authority: `taskplans/99_verity_custom_skills_plan.md` Skill 4. This
session hand-wrote 25 taskplans (72-99, then 100-104) following the same
shape every time. A skill that scaffolds it removes a class of numbering
and format mistakes rather than just doing the typing faster — the same
reasoning `verity-adr-gate` applies to ADR numbers.

## Procedure

1. **Find the true next number.** `ls taskplans/` and take the highest
   existing number, +1. Do not trust memory of "the last one I wrote" —
   check the directory. Known gap: numbers 61-63 do not exist in this
   repo's sequence (a gap from the original numbering, not a slot to
   reuse). Some numbers carry letter suffixes for closely related
   follow-ups (`17A`, `26A`, `35A`, `46A`/`46B`/`46C`) — use a suffix only
   when the new content is a direct extension of one specific existing
   taskplan, not for an unrelated new topic that happens to be adjacent
   in time.

2. **Match the established structure**, read from any recent taskplan
   before writing (e.g. `93_progressive_setup_capability_readiness.md` for
   a short one, `103_payload_cms_control_plane_adr.md` for a long
   analysis one) rather than inventing a template:
   - `# Task Plan N — <title>` (or `# Task N — <title>` — both forms exist
     in this repo; match whichever the immediately preceding few taskplans
     use)
   - An `Authority:` line citing what grounds this taskplan — a Bible/Spec
     section, an ADR, "User synthesis, <date>, item N," or a prior
     taskplan number. Never leave this uncited; an ungrounded taskplan is
     exactly the "generic engineering knowledge" `CLAUDE.md`'s stop
     conditions warn against.
   - `## Status:` — one of PENDING, BUILT, PARTIALLY BUILT, PROPOSED,
     DRAFT, or COMPLETE, each with enough evidence to justify it (a commit
     hash once built, a file path once designed) — never just the word
     alone.
   - A trigger condition or scope section — what has to be true before
     this is picked up, or what's explicitly in/out of scope. Most
     taskplans in this repo state a non-goal explicitly; do the same
     rather than leaving scope creep for whoever picks it up next.

3. **Update `00_STATUS_INDEX.md` in the same pass** — add a row to
   whichever table (Done/Pending) matches the new file's actual status.
   A taskplan that exists but isn't indexed is exactly the kind of drift
   that index's own header warns about ("re-derive if more than a few
   weeks stale") — don't create day-one drift by skipping this step.

4. If the new taskplan resolves, supersedes, or extends an existing one,
   say so explicitly in both directions: the new file cites the old one,
   and (if the old file is still read for anything) a short note in the
   old file points forward — the way `103` and `104` cross-reference each
   other, and the way ADR-018 states what it supersedes and what it
   doesn't.

## Non-goals

- Not a content-generation tool — it scaffolds structure and numbering;
  the actual analysis, decision, or scope still has to be thought through
  by whoever is writing it.
- Not a replacement for `verity-adr-gate` when the taskplan IS (or
  produces) an ADR — use that skill for the ADR-numbering half of that
  case, this one for the taskplan file itself.
