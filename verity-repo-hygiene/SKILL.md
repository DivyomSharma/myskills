---
name: verity-repo-hygiene
description: Use when the repo root or a top-level directory has accumulated loose files — "clean up the repo", "organize these files", "where should this doc live", or noticing several unrelated `.md`/asset files at repo root with no clear home. Automates the classification/move this project already did once as Task 110 — a repeatable audit, not a one-time cleanup.
license: Apache 2.0
---

Authority: `taskplans/110_repo_root_cleanup.md`, 2026-09-17 — 13 loose root
files sorted into `docs/reference/`, `docs/archive/`, `business/`, one
deleted, with `CLAUDE.md`-cited paths left untouched. Loose files will
reaccumulate (new client PRDs, new one-off audit docs) — this skill is the
canned version of that same audit for next time.

## Procedure

1. **List root-level (and any other suspect directory's) loose files** —
   anything not matched by an established pattern (`clients/<slug>/`,
   `docs/<topic>/`, standard project config).
2. **For each file, check if `CLAUDE.md` cites it by exact path** (grep
   `CLAUDE.md` for the filename). If yes: **leave it exactly where it is** —
   moving it means editing the citation in the same change, which is a
   larger, separate decision than a hygiene pass. Do not silently break an
   authority reference.
3. **For each remaining file, check if a skill or `taskplans/*.md` cites it
   by path** (grep `.claude/skills/**/*.md` and `taskplans/*.md`). If a
   skill cites it: moving is fine, but update the skill's citation in the
   same change (see Task 110's `verity-client-capability-builder` update).
   If only a taskplan cites it: taskplans are historical record, a stale
   path reference there is expected and fine, no update needed.
4. **Classify what's left**: client-specific → `clients/<slug>/`;
   cross-client reference material → `docs/reference/<topic>/`; business/
   sales collateral → `business/<topic>/`; dated, superseded-in-substance,
   or no longer live → `docs/archive/<yyyy-mm>-<topic>/` (archive, don't
   delete, unless truly zero-reference — see step 5); anonymous/unreferenced
   binary assets (screenshots with no descriptive name, zero content
   references) → delete candidate.
5. **Before deleting anything**: confirm zero references found (content
   grep across `.md`/`.ts`/`.tsx`, not just filename). When in doubt,
   archive instead of delete — archiving is reversible in spirit (still
   there, just out of the way), deletion is not.
6. **Execute with `git mv`**, never `mv`+`add`+`rm`, so history follows the
   file.
7. **Verify**: `git status --short` shows only intended renames/deletes, no
   untracked leftovers; `npx tsc --noEmit` confirms no `src/` import broke
   (unlikely for docs, cheap to check).
8. **Record it** — this is exactly the kind of change `verity-taskplan-writer`
   scaffolds: file-by-file disposition, what was explicitly left alone and
   why, verification performed.

## Non-goals

- Not a general `taskplans/` reorganizer. The only sanctioned subdirectories are `handoffs/` (live
  work) and `archive/` (closed plans, added 2026-10-04 at the product owner's request — see
  `taskplans/archive/README.md`). Archiving a closed plan is in scope: `git mv` it to `archive/` and
  rewrite live citations (src, skills, deploy, spec) in the same commit; never edit applied
  migrations' comments. Do not invent other subfolders. (`CLAUDE.md`'s "Do not assume a
  directory-based corpus exists" is about the V2 authority documents, which stay at the top level.)
- Not a decision-maker on `verity-bible/`/`verity-spec/`/`implementation/`
  placement — those are fixed authority tiers, not hygiene targets.
