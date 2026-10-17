---
name: verity-usage-qa
description: Operate a realistic fictional business through Verity end to end (restaurant chain, plywood trading, manufacturing, outreach team) to find broken state, UX friction, functional gaps and tenant leaks, then fix and re-run. Use for "test the workflow", "audit like a real user", "does this client actually work", or before declaring a client module done. Not for unit tests.
---

# verity-usage-qa

Announce "Using verity-usage-qa to run <workflow>".

You are a **business operator**, not a feature tester. The question for every run:

> Can this business finish its real work in Verity, without a workaround, and is the resulting
> state correct for the next person who reads it?

A page rendering, a 200, a row existing and a toast are **not** a pass. A workflow passes only when
its final business outcome is observable by someone else, in another place, after a reload.

## Ground rules specific to Verity (read first)

1. **Never run against production or a real client tenant.** Use the local test database
   (`.env.test`, port 55432) or a seeded throwaway tenant (`npm run seed:plywood`,
   `seed:audit-tenant`, `seed:scale`). Create what you need; delete what you create.
2. **Workflows come from what Verity actually ships**, not generic ERP lists. Derive them from:
   `clients/*/reference-parity/*.md` (the client's real needs), `src/app/(shell)/` (the screens),
   `src/server/capabilities/*` (the commands). CRM, Sales, Procurement and Finance are out of the
   platform scope *except* where a client capability (dinein, finance, loyalty, inventory,
   trading, outreach, manufacturing) already implements them. Do not invent a "quotation module"
   and then report it missing.
3. **Authority for "correct"**: the client's parity doc and `DECISIONS.md` beat your instinct. A
   behaviour the docs mark Defer is not a gap. A behaviour they mark Include and is absent is a gap.
4. **Fix authority.** You may fix bugs and UX defects. You must stop and write an ADR first
   (CLAUDE.md stop conditions) if a fix needs: a new security boundary, a change to INV-001/ADR-017/
   `enforcePolicy()`, a new platform primitive, or a client-specific fork. Functional gaps are
   *reported with a recommended build*, not silently built, unless they are listed Include in a
   parity doc.
5. **UI standard is ADR-033 (iOS HIG)**: 44pt targets, 17px inputs on phones, large title, inset
   grouped cells, WCAG AA light and dark, `prefers-reduced-motion/transparency`. Judge UX against
   that, not against generic taste.
6. Money is paise (`*Minor`). Check arithmetic yourself, to the paisa, before trusting the screen.
7. Terminology is canonical (Bible/CLAUDE.md): `Organization`, `Party`, `Location`, `Work`,
   `ChecklistItem`. A screen that says "Branch" or "Job card" is a defect.

## Setup

1. Pick one workflow from the matrix below (or the one the user named).
2. Create `docs/qa/runs/<date>-<workflow>/STATE.md` from the template. **Update it after every
   phase.** This is your memory; do not rely on recollection 15 steps later.
3. Seed realistic Indian data in volume: 15–30 guests/parties, 30–80 items, repeated and long
   names (Devanagari and Latin), ₹ amounts from ₹10 to ₹5,00,000, GSTIN-format ids (15 chars),
   +91 numbers, decimals and zero quantities. Two rows proves nothing.
4. Use the dev server on localhost (`npm run dev`) and a browser tool. Take a screenshot at each
   consequential step and at 390px and 1280px. Never screenshot `file://`.

## The run (per workflow)

```
DISCOVER  read parity doc + screens + commands; list actors, entities, statuses, roles
EXECUTE   do the happy path as the real role, through the UI only
VERIFY    after each consequential step check four layers (below)
BREAK     run at least 5 realistic deviations (below)
ANALYSE   classify every finding (below); find root cause
FIX       smallest correct fix in the owning layer; no test-specific hacks
RETEST    the failed step, then the full workflow once from the top
REGRESS   run affected vitest files + `npx tsc --noEmit`; for UI add the Playwright spec
REPORT    verdict + findings; update STATE.md
```

Bound the loop: at most **3 fix-and-rerun cycles per workflow**. If it still fails, stop and
report BLOCKED with the evidence; do not thrash.

### Four-layer verification (after every consequential action)

1. **UI** — what the user sees, after reload.
2. **Command result** — what the command returned / the audit and `domain_event` rows written.
3. **Database** — read the row through a tenant-scoped query (`withTenant`) or the local DB;
   check `tenant_id`, status, amounts, foreign keys.
4. **Downstream** — what the *next* process sees: the kitchen board, the stock level, the
   outstanding balance, the P&L, the HQ client directory, the other role's screen.

### Deviations to run (pick what fits, minimum five)

blank required field; invalid and over-long value; duplicate submit (double-click, two tabs);
refresh and Back mid-flow; edit after creation; cancel/void after a downstream effect; zero,
negative and decimal quantity; wrong role attempting the action; search with no result; a record
in a terminal state (INV-002: closed is read-only); a very long list; offline/slow request.

### Classification

- **BUG** — claims to work, does not.
- **UX defect** — works, but a non-technical user would stall, mistype or distrust it.
- **FUNCTIONAL GAP** — needed to finish the business task, absent (check the parity doc first).
- **PRODUCT GAP** — Verity models the business differently from how it really runs.
- **SECURITY** — any cross-tenant read or write, any client-trusted tenant id, any action allowed
  by the UI but not the server, or the reverse. **Cross-tenant access is CRITICAL and stops the run.**

Severity: CRITICAL (data leak, money wrong, data loss) · HIGH (task cannot finish) ·
MEDIUM (workaround needed) · LOW (polish).

### Tenancy and permission pass (every run)

With two seeded tenants A and B: as A, request B's ids on every detail route and every command;
expect not-found/forbidden, never B's data. As a low role, call each command directly (not
through the UI) and expect `ForbiddenError`. Confirm tenant comes from the session, not a payload.

### Line-list basics pass (every screen that builds a list of lines)

Order pad, purchase order, bill of materials, stock count, bill split, invoice, journal. A
missing item here is HIGH, not polish — staff work around it with duplicate lines and voids.

1. Adding an item already on the list raises its quantity; it does not stack a second line
   (unless the lines are genuinely different: another portion, note, price or kitchen round).
2. Quantity is adjustable in place with `QuantityStepper` (`src/components/ui/QuantityStepper.tsx`):
   minus, a typed number, plus. 44pt targets; Enter or blur commits.
3. A line can be removed before it is committed (minus at 1 becomes remove). After commit,
   removing is the module's reversal (void, credit note, reversal) with a reason.
4. Picking an item that is already on another line folds the two (`assignLineItem` in
   `src/lib/line-list.ts`), never a "duplicate item" error the user must fix by hand.
5. The running total updates as lines change, and the line's status says what has really
   happened ("Not sent yet" before the kitchen has it, not "With kitchen").

## Workflow matrix (Verity-real)

| Client / area | Workflow | Roles |
|---|---|---|
| Colonel Kebabz | Dine-in: table → order → kitchen → bill → settle, with note, void, split later | waiter, kitchen, manager |
| Colonel Kebabz | Takeaway / delivery / Zomato order → kitchen → settle (no table) | counter, manager |
| Colonel Kebabz | Receive stock → sale depletes by recipe → wastage → count → low-stock | storekeeper, manager |
| Colonel Kebabz | Purchase order → goods receipt → stock up → vendor payable | manager, owner |
| Colonel Kebabz | Guest → points earned → offer → redeem → complaint | counter, manager |
| Colonel Kebabz | Shift attendance → leave → payroll input; day cash reconcile → outlet P&L | manager, accountant, owner |
| Colonel Kebabz | Owner 9 AM: what needs my attention across all outlets | owner |
| Plywood | Order → goods issue → invoice → payment → outstanding; purchase side | sales, accounts |
| Carxen | Route → order → stage checkpoints → dispatch → passport | production, QC |
| PlotArmour | Lead → outreach → check-in → proposal → close | founder, senior, member |
| HQ | Onboard client → enter with reason → health → suspend (ADR-034) | operator |
| Platform | Tenant A attempts tenant B (all of the above) | any |
| First-time user | Complete one task with zero prior knowledge (no source reading first) | role of the task |

## First-time-user mode

Run once per client, **before** reading source for that screen. Record each hesitation as:
DISCOVERY (can't tell what to do), COMPREHENSION (don't understand a label), ACTION (can't do
it), RECOVERY (can't undo a mistake), CONFIDENCE (can't tell if it saved). Output a friction map
ordered by severity. Needing Excel, WhatsApp, a calculator, or a copied id is a defect.

## Owner mode

Open the owner view cold: can they see cash and outstanding, sales by outlet, what is pending
approval, what failed, and exceptions, without opening more than two screens?

## Persisting what you found

A finding fixed once regresses silently. For every fixed BUG add a vitest (pure or DB lane) that
fails without the fix; for every fixed UX flow add or extend a Playwright spec under `e2e/`.
Then run `npx vitest run <affected>` and `npx tsc --noEmit`. Do not mark done on a green UI alone.

## Report (write to `docs/qa/runs/<date>-<workflow>/REPORT.md`)

```
Workflow · Business objective · Actors · Starting state
Happy path: what happened, per phase, with the four-layer check results
Findings: id, class, severity, step, expected, actual, repro, root cause, fix or recommendation
UX friction (functional but poor) · Functional/product gaps (with the parity-doc row)
Deviations run · Tenancy/permission results
Evidence: screenshots (390 and 1280), commands run, test files added
Verdict: PASS | PASS WITH ISSUES | FAIL | BLOCKED
```

PASS only if the final business outcome was independently observed. If any step was not actually
executed, say so; never infer a pass from code reading.

## STATE.md template

```
Workflow:            Tenant (throwaway):        Role(s):        Run date:
Phase:               Entities created (ids):    Expected vs actual:
Defects open:        Unverified assumptions:    Blocked by:     Next action:
Fix cycles used: 0/3
```
