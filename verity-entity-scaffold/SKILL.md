---
name: verity-entity-scaffold
description: Use when adding ONE new entity/table to an EXISTING capability — "add an X table to the outreach capability", "give this capability an append-only log", "I need a new entity for tracking Y" where the capability itself already exists. Not for building a whole new capability from scratch (use `verity-client-capability-builder` for that). Encodes the exact 6-step shape (schema + migration + capability code) done five times in one session (Task 106 Phases A-E) with the same structure every time — turns a repeatable, error-prone multi-file pattern into a checklist instead of re-deriving it from scratch each time.
license: Apache 2.0
---

Authority: `src/server/capabilities/outreach/index.ts` and its five
migrations `20260917100000`-`140000` (Task 106 Phases A-E, 2026-09-17) —
five new entities added to one existing capability in one session, each
following the identical shape. Also `taskplans/82_erpclaw_client_capability_
builder_skill.md`'s rules, one level down: that skill designs a whole
capability's lifecycle; this one is the mechanical unit inside it — one
more table.

## Before scaffolding: decide the entity's write discipline

Every entity in this codebase is one of two shapes. Pick before writing
anything (mixing them in one table is the specific mistake to avoid):

- **Mutable, tenant-isolated** — a record that can be renamed/edited/its
  status changed in place (`OutreachTeam`, `OutreachAssignment`,
  `OutreachEscalation`'s `status` field). RLS: one `FOR ALL`-style
  `USING (...) WITH CHECK (...)` isolation policy.
- **Append-only** — a historical/audit fact that must never be edited or
  deleted once written (`OutreachActivity`, `OutreachAttributionRecord`,
  `OutreachOpportunity`/`OutreachClosedClient` when they represent a
  fired-once event). RLS: separate `FOR SELECT` + `FOR INSERT` policies,
  plus a `BEFORE UPDATE OR DELETE ... EXECUTE FUNCTION verity.reject_
  mutation()` trigger. ADR-009's rule one layer down: a wrong fact gets
  corrected by a NEW row, never an edit to the old one.

## The 6 steps, every time

1. **`prisma/schema.prisma`** — new model, tenant-scoped (`tenantId String
   @map("tenant_id") @db.Uuid` + `tenant Tenant @relation(...)`), FK to
   whatever it belongs to (usually the capability's root entity, e.g.
   `OutreachLead`). Add the matching back-relation list field on BOTH sides
   of every relation — Prisma's validator catches a missing one immediately
   (`npx prisma generate` will refuse to run), so this is self-checking.
2. **Migration file** (hand-authored SQL, not `prisma migrate diff` —
   every capability migration in this tree does this because `diff` bundles
   in unrelated live-DB drift): `CREATE TABLE` with the exact column shape
   from step 1, indexes matching the query patterns you'll actually run,
   FK constraints, then RLS per the write-discipline decision above, then
   `INSERT INTO entity_definition (...)`, then `UPDATE capability_definition
   SET entity_types = array_append(entity_types, '<key>') WHERE ... AND NOT
   ('<key>' = ANY(entity_types))`, then a `DO $$ ... $$` permission-grant
   loop over the capability's existing roles (copy the shape from the most
   recent migration in the same capability — the verb set differs per role
   by design, don't grant uniformly without checking who should actually
   have Create/Edit).
3. **`npx prisma generate`** — before writing any capability code; confirms
   the schema is valid and gives you the typed client to write against.
4. **Capability code** — entity-key constant (`ENTITY_<NAME> =
   "verity.<capability>.<name>"`), `CommandDefinition`/`QueryDefinition`
   exports following the existing file's exact shape (input `z.object`,
   `entity`, `verb`, `handler: async (ctx, input) => ...`), registered via
   `registerCommand`/`registerQuery` in the capability's
   `register<Capability>Capability()` function.
5. **Wire it into whatever already-existing command should write to it** —
   a new entity rarely stands alone; it's usually materialized from an
   existing state transition (see `OutreachOpportunity` created inside
   `advanceLeadStage`) or written alongside an existing field change (see
   `OutreachAttributionRecord` written alongside `opportunityOwnerId`
   updates). Decide the source-of-truth question explicitly: does this new
   table REPLACE an existing field, or sit ALONGSIDE it as a queryable
   history? (Almost always alongside, for a live system — replacing risks
   breaking every existing reader of the old field.)
6. **Verify**: `npx tsc --noEmit`, `npx eslint <file>`, then apply the
   migration (`npx prisma migrate deploy` after checking `migrate status`
   shows no drift — see `verity-migration-safety`).

## Non-goals

- Not for a brand-new capability — that needs the full lifecycle/scope
  design `verity-client-capability-builder` covers (state machine, non-goals,
  permission model from scratch). This skill assumes the capability, its
  roles, and its permission conventions already exist.
- Not a substitute for deciding whether the new table should exist at all —
  that's still a real design question (does this duplicate an existing
  entity? should it be a field instead of a table?), this skill only makes
  the mechanical part of "yes, build it" consistent.
