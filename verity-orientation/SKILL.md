---
name: verity-orientation
description: Use at the start of a fresh session or when a new developer needs to get oriented on the Verity repo without reading 900+ lines of CLAUDE.md cold — "orient me on Verity", "what's the current state of the platform", "cold-start briefing", "what's built vs pending right now". Generates a short, regenerated-not-static briefing from the actual current state of the repo, not a memorized snapshot.
license: Apache 2.0
---

Authority: `taskplans/99_verity_custom_skills_plan.md` Skill 7. A fresh
developer or a fresh agent session currently has to read all of
`CLAUDE.md` plus whichever taskplans are relevant before doing useful
work. This skill compresses that ramp-up — and regenerates itself from
current files each time, rather than staying a static document that
drifts the way `CLAUDE.md`'s own ADR-count note already drifted once
(the exact failure `verity-adr-gate` exists to catch).

## Procedure — read these four things, in this order, then synthesize

1. **`CLAUDE.md`'s "Current objective" and "Build priority" sections** —
   what phase the platform is in (FOUNDATION READY, not a client build),
   and which numbered build-priority items are actually done vs. still
   open. Check for a "Correction" note near the build-priority list (one
   exists as of 2026-09-08) before trusting the list's face value — a
   build-priority item can be substantially built without the list saying
   so yet.
1a. **`taskplans/handoffs/README.md`** — the live work order; read it before the index below. Closed
   plans are in `taskplans/archive/` (moved 2026-10-04). Recent audits that frame current priorities
   live in `docs/audits/` — as of 2026-10-05: the UI completeness audit (five backend-only
   capabilities) and the HQ audit. Per-client Odoo/ERPNext parity documents live under
   `clients/<slug>/reference-parity/` (template `docs/reference/client-reference-parity-template.md`).
2. **`taskplans/00_STATUS_INDEX.md`** — the Done table (what's actually
   shipped, with commit evidence) and the Pending table (what's blocked
   and why: real trigger unfired vs. needs an ADR vs. needs an explicit
   decision vs. low-priority deferral). Read its own header first — it
   states its own regeneration date and staleness warning.
3. **`taskplans/101_remaining_work_master_plan.md`** (or its successor,
   if a later master-plan taskplan supersedes it — check
   `00_STATUS_INDEX.md` for that) — the sequencing and categorization
   logic for everything still open, so a fresh session doesn't re-derive
   triage that's already been done.
4. **`CLAUDE.md`'s "Authority order"** — which documents actually govern
   (V2-ADRs, Bible v2, Spec v2, PRD, consistency audit, roadmap) versus
   which are historical-only (`verity-bible/`, `verity-spec/` legacy
   folders, ADR-001 through ADR-016 in the OLD numbering — not to be
   confused with the accepted `verity-spec/17_decisions/adr/adr-016.md`).

## Output shape

A short briefing (aim for something a person reads in 2-3 minutes, not
another 900-line document): current objective and phase; the 3-5 most
recently completed pieces of work with their evidence; the top few
genuinely-actionable-now items (not blocked by a trigger, ADR, or
decision) if any exist; a one-line pointer to where the full detail lives
for anything summarized. Do not restate `CLAUDE.md`'s constitutional
invariants or terminology table in full — point to them, since they
don't change often enough to need repeating in a briefing that's
regenerated every time.

## Non-goals

- Not a replacement for reading `CLAUDE.md` in full before any
  significant architectural decision — this is a ramp-up aid, not a
  substitute for the authority documents themselves.
- Not a cached/saved document — regenerate from the current state of the
  four sources above every time this is invoked, since a stale cached
  briefing is worse than no briefing (it's `CLAUDE.md`'s own ADR-count
  drift, repeated in a new form).
