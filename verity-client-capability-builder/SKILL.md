---
name: verity-client-capability-builder
description: Use when building, extracting, or auditing a Verity client or platform capability — a new business module (accounting, inventory, selling, buying, payments, billing, HR, payroll, or any future domain) that plugs into the existing Command/Query/State/Event runtime. Triggers include "build a new Verity client module", "extract this client requirement into Verity", "implement a plywood-like module", "add ERP/accounting/inventory/sales/buying/payments capability", "turn this PRD into Verity capability code", "use ERPClaw architecture for Verity", "audit whether this should be platform or client capability". Not for platform-core changes (tenancy, auth, command runtime itself), not for frontend-only work (use impeccable), not generic ERP-building.
license: Apache 2.0
---

Authority: `taskplans/82_erpclaw_client_capability_builder_skill.md` (this
skill's own source spec). Every rule below cites this repo's own authority
docs, never generic ERP or SaaS knowledge — that split is the whole point:
a capability built from this skill should look like it belongs next to
`src/server/capabilities/plywood/` and `src/server/capabilities/asset/`,
not like it was copied from a tutorial.

## Required context-loading order

Read these, in this order, before writing a line of capability code:

1. Root `README.md` — current authority order.
2. `CLAUDE.md` — project rules and the Experience System design authority.
3. `CLAUDE.md` §Build priority — what's actually built vs. planned, so the
   capability doesn't assume infrastructure that doesn't exist yet.
4. The relevant `taskplans/17A`–`22` authority docs for whatever the
   capability touches: platform/capability/entity/state/permission/data
   rules.
5. The existing shipped capability closest to this task. In order of
   maturity: `src/server/capabilities/plywood/` (deepest — catalogue,
   stock, trading, finance, tax, reports), `src/server/capabilities/
   accounting/`, `inventory/`, `hr/`, `billing/` (backend MVP slices; as of
   2026-10-04 only `hr` has a screen — do not copy their missing UI as a norm),
   `src/server/capabilities/asset/` or `location/` (smallest, cleanest
   skeleton to copy the shape of a brand-new capability from).
6. Relevant client design docs (`docs/reference/verticals/plywood.md`,
   `docs/reference/verticals/KentsRestaurant.md`,
   `docs/reference/verticals/clinic.md`, `docs/reference/verticals/salon.md`,
   `docs/reference/verticals/coaching.md`) and `docs/reference/erpclaw-prd/`,
   if the capability traces to one of them. (Moved from repo root
   2026-09-17 — Task 110's cleanup.)

## First, for every client: the reference-parity document (2026-10-05 rule)

**The trigger.** 2026-10-05: clients other than Shree Ganesh Timber said their Verity instance is not
comparable to Odoo or other ERPs — modules incomplete, workflows missing, "not even usable". The
2026-10-04 UI completeness audit (`docs/audits/2026-10-04-ui-completeness-audit.md`) confirmed it:
five capabilities (hr, inventory, accounting, billing, scheduling) had a backend and no screens, and
four sidebar links led to a 404.

**The rule.** For every client, existing or new, before building or extending their modules, write
the per-client reference-parity document using `docs/reference/client-reference-parity-template.md`,
under `clients/<client-slug>/reference-parity/`. It records how Odoo (`D:\Code\R&D\odoo-19.0`) and
ERPNext (`D:\Code\R&D\erpnext`) serve that client's requirements: every module, menu, page, section,
field group, button and workflow, read from their source with evidence paths. Every reference item
ends in a decision row (Include / Defer with owner / Not applicable). The capability's design and
scope come from that document, not from what Verity's code already happens to have.

This sits *before* the V1 completeness gate below, not instead of it: the gate checks a finished v1;
this document defines what v1 must be.

## Before writing code: state the lifecycle, not the commands

Write the capability's business lifecycle first — e.g. plywood's
`Catalogue → Purchase → Receive → Stock → Sale → Reserve → Dispatch →
Deliver → Invoice → Payment → Margin`. The lifecycle is what reveals which
platform primitives are reused, which commands/states/reports are actually
required, and what's missing. "Needs purchase orders" without the lifecycle
skips the step that would have surfaced the gap.

## Rules (non-negotiable, carried from Task 82's source spec)

- Verity's database and code are authority for current behavior — not this
  skill's memory of a previous session, not a training-data ERP pattern.
- Distinguish BUILT / PROVEN / DEMONSTRATED / NOT YET BUILT exactly per
  `CLAUDE.md` §Reporting vocabulary. Never report a hypothetical as shipped.
- Keep client modules capability-private unless at least two real clients
  prove reuse. "One client's need means platform primitive" is the
  anti-pattern, not the default.
- Do not broaden platform core (`src/server/platform/`) to satisfy one
  capability. If the capability seems to need that, stop — that's a
  platform decision, not a capability one.
- Preserve RLS and fail-closed security guards (INV-001, `withTenant()`).
  Every new table gets `ENABLE ROW LEVEL SECURITY` + `FORCE ROW LEVEL
  SECURITY` + a tenant-isolation policy in its migration, no exceptions.
- Register everything through the established patterns — capability
  definitions, entity definitions, commands, queries, workspace
  contributions, migrations — never a bypass. Direct table writes outside
  `executeCommand` are a defect, not a shortcut.
- Money is integer minor units, always — see `prisma/schema.prisma`'s own
  "MONEY IS INTEGER MINOR UNITS" comment block for the convention every
  existing capability already follows.
- Snapshot product names, HSN/tax codes, prices, discounts, tax rates,
  customer/supplier names, and commercial terms onto submitted documents —
  never re-derive them later from a mutable master record.
- Use append-only ledgers for stock/accounting/payment history — see
  `journal_entry`/`journal_line` (accounting) and `inventory_stock_movement`
  for the pattern: `ENABLE ROW LEVEL SECURITY` + a
  `BEFORE UPDATE OR DELETE ... EXECUTE FUNCTION verity.reject_mutation()`
  trigger, SELECT + INSERT-only RLS policies.
- Use lifecycle states instead of deleting historical business records
  (ADR-009). A wrong fact is corrected by a new fact (reversal, decision,
  amendment), never by editing or deleting the old one.
- Hide internal command keys from user-facing UI (Task 81 §3) — a command
  key like `verity.accounting.post_journal_entry` is an implementation
  detail, never product copy.
- Use semantic design tokens for any UI; never hardcode dark-mode-hostile
  text classes (Experience System, ADR-011/012) — load `impeccable` before
  writing any capability UI.
- Keep dense operational tables scrollable and legible.
- Add tests before claiming BUILT/PROVEN.

### Six more, from the 2026-09-03 synthesis

- Every capability declares its own business invariants explicitly (e.g.
  "stock cannot go negative unless the capability opts in," "a settled
  invoice cannot become editable") and enforces them at the command/DB
  layer — never trusted to the UI alone.
- Every externally- or automatically-triggered command (webhook, cron,
  AI-issued, or a user's accidental double-click) needs a safe-retry story
  so it cannot duplicate the business event it represents. Not every
  command needs this — only ones a retry can plausibly reach. See
  `billing`'s `generateInvoiceForMeter`: idempotent by a DATABASE unique
  constraint, not an application check.
- Model data as master (customer, item, warehouse), transactional (order,
  receipt, invoice, payment), or derived (outstanding balance, margin,
  current stock) — treat derived data as computed, never stored as if it
  were a fact of its own.
- State who controls each piece of configuration before adding it:
  platform-controlled, client-controlled, role-controlled, or
  system-derived. A settings screen with no named owner per field is how it
  becomes a dumping ground.
- State the business lifecycle before decomposing into commands (see
  above — promoted to its own section because it's load-bearing).
- Prefer retiring a reference/registry value over deleting it whenever
  historical records depend on it (ADR-009's rule, one layer down: tax
  categories, payment terms, units, status labels).
- When a field can genuinely be "we don't know yet" as a distinct state
  from "the value is empty" (Task 94 — a customer's GSTIN, a delivery
  confirmation, a credit rating), don't overload the value field with a
  sentinel and don't force it required before the business actually knows.
  Add a companion `Select`-type custom field for the status (`Unknown` /
  `Not applicable` / `Verified` / etc.) alongside the value field — the
  existing `CustomFieldSchema`/`CustomFieldType` machinery already covers
  this, no new platform primitive needed.

## V1 completeness gate — before scope is called done

**The trigger.** 2026-09-19: a client noticed Core had no way to manage
team leadership, membership, or team creation — every one of those
commands already existed server-side (`create_team`, `remove_team_member`,
even `set_team_co_leader`), but no page ever reached them for anyone
except a team's own leader. A written requirements doc rarely asks for
"admins can also do the things individual users can do to their own
records" — it's assumed. Nothing in this skill's process would have
caught that gap before a client found it, because nothing required
comparing the finished capability against what a mature ERP treats as
baseline for the same domain.

**The rule.** Before any client capability's v1 is reported DONE (per
`CLAUDE.md`'s reporting vocabulary), two checks run, both required, same
enforcement posture already given to `verity-adr-gate` and
`verity-migration-safety` (Task 121 §3.3 — not just an audit run once,
a standing bar every new capability clears before shipping):

1. Invoke the global `obvious-basics-checklist` skill against every
   entity/screen the capability introduces. It is broader than the
   Odoo cross-check below in one respect (data completeness, list-view
   basics, notifications, accessibility) and narrower in another (it
   doesn't require a reference-system read) — run both, they catch
   different gaps. `taskplans/121_permanent_obvious_basics_enforcement_
   and_priority_order.md` is why this exists: the exact class of bug
   this checklist targets (a hand-rolled `<table>` missing its
   `overflow-x-auto` wrapper in one spot but not another, in the same
   file) already reproduced in this codebase once, on a screen that was
   the strong example elsewhere in the same file.
2. Cross-check its scope against the equivalent module in a reference
   system under `D:\Code\R&D\` — `odoo-19.0` first (broadest domain
   coverage, most actively maintained), `erpnext` second (already has a
   full audit at `taskplans/archive/05_erpnext_audit.md` — read that before
   re-deriving from source). This is narrower than `verity-rd-miner`'s
   full nine-section audit: not "what can Verity learn architecturally
   from this system," but "what would this domain's users consider too
   obvious to write into a requirements doc, and does our v1 actually
   have it." Use `verity-rd-miner`'s own method when the answer needs a
   real architecture audit, not just a feature checklist.

Concretely, for the closest-matching reference module, read its `views/`
(Odoo) directory listing and ask, for each file, "do we have this, and if
not, was that a stated decision or a silent gap":

- **A role/admin management surface for every role-scoped surface a
  regular member gets.** The bug that triggered this gate, generalized:
  if a Senior can manage their own team, Core needs the same power over
  every team, not just visibility into it.
- **A dashboard/landing page shaped for the signed-in role**, not a
  single generic page everyone shares — Odoo's per-app home view and
  `digest_views.xml` (periodic own-work summary) are the concrete
  reference points. A landing page that's the same for a front-line
  worker and for an owner is very likely wrong for one of them.
- **A calendar/timeline view wherever the domain has dated events** —
  `calendar_views.xml` in Odoo's `crm` module is the concrete example:
  Verity Outreach has `OutreachMeeting.scheduledAt` but no calendar view
  of it, only a flat per-lead list.
- **Lost/decline/cancel reasons as a structured field, not free text**,
  wherever a record can end unsuccessfully (`crm_lost_reason_views.xml` —
  Verity Outreach already does this for leads; check whether a newer
  capability replicates the pattern or reverts to a bare text field).
- **Source/campaign attribution** wherever leads/records originate from
  multiple channels (`utm_campaign_views.xml`) — not built into Outreach
  yet; flag as a real, not-yet-built gap rather than silently absent from
  future audits of this same capability.
- **Team/ownership management** (`crm_team_views.xml`,
  `crm_team_member_views.xml`) — the exact shape of 2026-09-19's fix.

**The deliverable.** A short checklist section in the capability's own
taskplan (see `verity-taskplan-writer`), one line per reference-module
file/concept checked: `Included` / `Deferred — <reason, and who owns the
decision to defer>` / `Not applicable — <why this domain doesn't need
it>` — plus `obvious-basics-checklist`'s own per-entity table (`Category
| Status | Evidence | Fix`), run against every entity/screen the
capability introduces, in the same taskplan section. Never silently
absent — the whole point of this gate is that a missing item without a
marked reason is exactly the failure mode it exists to catch. This
checklist is additive to the existing "Skill output
checklist" below, not a replacement for any item in it.

## Every input control uses Verity's own design-system components — never a raw native browser control

Concrete anti-pattern found 2026-09-19, **fixed the same day**:
`TaskPanel.tsx`'s due date used a bare `<input type="date">` and
`MeetingPanel.tsx`'s scheduling field used a bare native datetime picker
(confirmed native by its accessibility tree: separate Day/Month/Year/
Hour/Minute/AM-PM spinbuttons, the OS control's own shape, not a
Verity-themed one) — both bypassing Verity's own `Input`/form primitives
and the Experience System's material/motion rules (ADR-011/012/023/024)
entirely, because a native browser control renders with the OS's own
chrome, never the app's theme, spacing, or interaction pattern.
`src/components/ui/DateTimePicker.tsx` (`DateField`/`DateTimeField`,
plus `Form*` uncontrolled variants matching `Combobox`/`FormCombobox`'s
own pattern) is the themed replacement — use it for every new date or
datetime field; do not reach for the native input again. A `time`-only
variant doesn't exist yet — add it the same way if a capability needs
one, rather than falling back to a native `<input type="time">`. Any
native `<input type="date"|"datetime-local"|"time">`, `window.alert()`,
`window.confirm()`, or `window.prompt()` in new capability code is the
specific, checkable symptom — same class of rule as this skill's existing
"integer autoincrement primary key" and "unprefixed table name" checkable
anti-patterns above.

## Two checkable UI rules from the 2026-10-04/05 audits

- **Every navigation entry resolves to a page.** A `registerContribution` `href` with no
  `src/app/(shell)<href>/page.tsx` is a 404 in the sidebar. `/hr`, `/accounting`, `/billing` and
  `/inventory` all shipped that way. Never register navigation for a page that does not exist; check
  with a grep of every `href` against the route tree before reporting done.
- **No internal identifiers on screen.** Users must never see `verity.capability.x`, `verity.<cap>.<entity>`,
  command keys, raw config keys or snake_case field names. Show the business label (see
  `src/components/ui/business/vocabulary.ts`). The HQ live pass (`docs/audits/2026-10-05-hq-audit.md`)
  found raw keys on Modules, Roles, Settings, Operations and Audit — the single most common reason
  screens read as "built by a developer for a developer".

A capability is "UI complete" only against `docs/reference/module-completeness-bar.md`; a backend
with commands and no screen is reported as **BUILT (backend)**, never complete.

## Skill output checklist, per new capability

Capability status statement; requirement-to-platform-primitive map; scope
boundaries and non-goals; domain model; state machines; commands; queries;
permissions; dashboard contributions; UI routes and page sections; migration
plan; seed/demo plan; test plan; acceptance checklist; open decisions;
implementation summary with exact files changed; **the client's
reference-parity document** (see "First, for every client" above); **V1 completeness
checklist against the closest Odoo/erpnext module** (see the gate above).

Three more, required per the 2026-09-03 synthesis:

- **Source-of-truth map.** For every important number the capability
  surfaces, state exactly where it comes from — "stock reads from the
  movement ledger, never `product.stock`," "receivable is invoices minus
  payments, never a maintained balance field." This is the specific bug
  class where a cached/duplicated number quietly drifts from the ledger
  that's supposed to be authoritative for it.
- **Happy path + exception path, named separately, per workflow.** Not just
  the state machine — the explicit branch. `Purchase → Receive → Stock`
  happy path, then short receipt / damaged goods / rejected goods /
  duplicate receipt as named exceptions, each with its own handling.
- **The business event before the report.** Don't design a report ("profit
  this month") before the domain model settles what exactly counts as
  revenue, cost, settlement, and returns. The report is a read over
  already-agreed facts, not a reason to retroactively decide what the facts
  are.

## Anti-patterns — refuse these outright

"Navigation hiding is authorization." / "One client's need means platform
primitive." / "JSON blob instead of a table for queryable line items." /
"Direct ledger row writes from UI." / "Updating submitted financial facts
in place." / "Assuming a customer/supplier/item exists from chat memory." /
"Using action keys as visible product copy." / "Adding a fake generic pack
name before a real pack exists." / "Calling docs complete because the
worktree is clean." / "Weakening RLS or bypass guards to make tests pass."

Four more, mechanical and checkable:

"Integer autoincrement primary key for a business record" — Verity is
UUID-keyed throughout; an autoincrement id is the specific, checkable
symptom of a capability that wasn't built against the platform's own
primitives. / "A hardcoded CHECK constraint standing in for a value a
registry should own" — the same mistake as a hardcoded enum, one layer
lower, in the schema instead of the code. / "An unprefixed table name that
could collide with a future platform table" — capability-private tables
need a namespace a human reviewer can verify at a glance (`account`,
`inventory_item`, `hr_employee`, `billing_meter` — every table this session
added is prefixed or, for accounting, deliberately scoped to names nothing
else in the schema claims). / "A destructive action shipped without a
confirmation class" — every command that deletes, restores, rolls back, or
generates an external file needs `impact: "destructive"` set on its
`CommandDefinition`, not assumed.

Two more:

"A deprecated write path that just gets hidden from the UI" — a retired
direct-write gateway must actively refuse and name the supported
replacement; an API a UI merely stopped calling is still callable. / "One
giant transaction that either fully succeeds or fully fails for a bulk/
imported/AI-issued batch" — see Task 91's `runCommandBatch`
(`src/server/platform/batch.ts`): a batch of N operations preserves the
ones that succeeded and surfaces the ones that didn't, individually, never
rolling the whole batch back over one bad row.

## Non-goals

- Not a generic ERP-building skill — every rule above cites this repo's own
  authority docs, not generic engineering knowledge.
- Not a replacement for reading the actual authority docs — this skill
  points to them, it doesn't duplicate their content.
- Not a design skill — load `impeccable` separately for any UI this
  capability needs.
