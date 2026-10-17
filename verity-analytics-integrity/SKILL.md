---
name: verity-analytics-integrity
description: Use when building or reviewing ANY metric/dashboard/report page in Verity — a conversion funnel, a performance table, a rate, a "top X" list, a domain/channel/team comparison. Not specific to one capability. Prevents the analytics anti-patterns this project's own outreach capability doc explicitly names — a rate shown without its denominator, activity/engagement/progression/conversion/revenue blended into one number, an unsupported "best X" claim, a number nobody can click into.
license: Apache 2.0
---

Authority: `taskplans/106_pa_oms_deep_operations_prd.md`'s master prompt
§78-81 (written for outreach specifically) generalized as a cross-capability
rule — the same discipline applies to any Verity reporting surface
(plywood margins, finance aging, HR attendance), not just outreach.

## The four rules

1. **Never show a rate without its denominator.** `"66.7% close rate"` alone
   is a claim with no way to judge it; `"2 closed / 3 opportunities"` is
   the same fact, honestly sized. Flag (don't hide) a small sample — this
   codebase's own `thinSample`/`THIN_SAMPLE_BELOW` pattern
   (`src/server/capabilities/outreach/index.ts`) is the reference
   implementation: compute the flag, let the UI render it visibly, never
   silently suppress a thin number.
2. **Don't blend activity, engagement, progression, conversion, and revenue
   into one number.** They answer different questions and collapsing them
   hides which stage is actually the problem. Report them as separate rows/
   columns: effort (count of things done), engagement (response), progression
   (meeting/proposal), outcome (closed), commercial (value), efficiency
   (rate/velocity/revenue-per-unit) — same shape as `IntelligenceRow` in the
   outreach capability.
3. **No unsupported superlative language.** "Best domain," "winning
   channel," "guaranteed high-conversion X" are claims that imply a defined
   ranking criterion and statistical confidence neither this codebase nor
   most sample sizes actually have. Show the observed metric, the sample
   size, and let the reader draw the conclusion — don't draw it for them
   in the label.
4. **Every number on a report links to its underlying records.** A stat
   with no drill-down is a number nobody can verify or act on. If the query
   backing a displayed count can't cheaply be re-run with a narrower filter
   to show the actual rows, that's a sign the aggregate itself might be
   wrong — building the drill-down first is a good way to catch that before
   shipping the summary.

## Source-of-truth check (borrowed from `verity-client-capability-builder`,
worth repeating here specifically for analytics)

State, for every number on the page, exactly which table/query it comes
from and whether it's a live read or a cached/stored aggregate. A derived
number (margin, current stock, response rate) should almost always be
computed at read time over the ledger/log tables, never maintained as a
separately-updated field that can drift from what it's summarizing.

## Non-goals

- Not a charting/visual-design skill — see `dataviz` for chart mechanics,
  color, layout. This skill is about what the NUMBERS are allowed to claim,
  not how they're drawn.
- Not specific to outreach — written from that capability's rules but
  intended to generalize to every capability's reporting surface.
