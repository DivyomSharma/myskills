---
name: verity-shared-db-hygiene
description: Use when auditing the shared Verity database for leftover test/demo tenants — "clean up fake tenants", "what tenants exist in the DB", "is this test data or real", periodically or after a batch of integration-test runs. Prevents real-vs-fake tenant confusion: automates the classification this project already had to do by hand (16 leftover tenants from tests that ran against the shared DB instead of an isolated local one, per this project's own `setup-env.ts` guard).
license: Apache 2.0
---

Authority: real cleanup, 2026-09-17 (Task 110's companion DB action, not
itself in `taskplans/` but same session). 16 of 21 tenants in the shared
database were leftover fixtures (`Trading Test Distributors`, `Rival
Traders`, `Finance Automation Plywood`, `boundary-*`) from
`capability-plywood-*.test.ts` and `operator-boundary.test.ts` — tests that
should only ever run against an isolated local database per
`src/test/setup-env.ts`'s own remote-URL guard, but evidently ran against
the shared one at some point regardless.

## Procedure

1. List every tenant (bypass connection — see `verity-tenant-query-safety`
   for why): `prisma.tenant.findMany({ orderBy: { createdAt: "asc" } })`.
2. For each tenant name, grep `src/test/**/*.test.ts` and `prisma/seed-*.ts`
   for that exact literal string. A name that appears as a hardcoded
   fixture in a test file is a test artifact; a name that appears only in a
   dedicated `seed-<client>.ts` is a deliberate demo/reference tenant; a
   name that appears in neither and has real associated org/role/data rows
   is presumptively real client data.
3. Classify every tenant into exactly one of: **real** (has a matching
   client relationship, real people, ongoing use), **deliberate demo/fixture**
   (has its own `seed-*.ts`, sometimes a fixed deterministic UUID like
   `b0000000-0000-4000-8000-000000000001` — a strong signal of intentional,
   not accidental), **test debris** (matches a `*.test.ts` fixture name
   exactly, no dedicated seed script, usually appears in duplicate — same
   name, several `createdAt` timestamps close together).
4. Before deleting anything: present the full classified list with the
   evidence for each (which file matched, what data the tenant holds — team
   count, lead count) and get explicit confirmation. `tenant.delete()`
   cascades to every FK'd child row across every capability — irreversible,
   shared-system, exactly the class of action that needs a stop-and-confirm
   even when the classification looks obvious.
5. Delete only the confirmed test-debris list, via `prisma.tenant.delete()`
   per id (not a bulk `deleteMany` on a name match — a bulk match is exactly
   how a real tenant with a coincidentally similar name gets caught).
6. Verify after: re-list tenants, confirm the kept set matches exactly what
   was meant to survive.

## Non-goals

- Not a fix for tests running against the shared DB in the first place —
  that's `setup-env.ts`'s guard (`VERITY_TEST_ALLOW_REMOTE_DATABASE`); if
  this skill is needed repeatedly, the actual bug is upstream of it.
- Not for deciding whether a REAL tenant's data should be deleted — that's
  a business decision this skill has no opinion on.
