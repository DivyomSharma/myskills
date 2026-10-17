---
name: verity-tenant-query-safety
description: Use before running any ad-hoc read/write script against the Verity database outside the normal app request path — "check how many X exist", "query the DB directly", "verify the seed landed", "is this tenant empty", debugging a query result that looks surprisingly empty, or any one-off Node/Prisma script touching `prisma.<model>` outside `withTenant()`. Prevents a real incident this project already hit: reading with the RLS-enforced app-role client and no tenant scope set, getting zero rows for everything, and wrongly concluding a tenant/table was empty.
license: Apache 2.0
---

Authority: this project's own `src/server/platform/tenancy.ts` design
("With no scope set, queries return nothing and writes are rejected —
isolation fails closed") plus a real incident, 2026-09-17: a session ran a
plain `new PrismaClient()` (the `DATABASE_URL` / `verity_app` role, RLS
enforced, `verity.tenant_id` never set) to check whether the PA-OMS tenant
had any roles or teams. It returned zero for everything. That was read as
"the tenant was never seeded," which led to running a one-time seed script
a second time, creating a duplicate tenant and 5 duplicate identities that
then had to be found and repaired by hand. The database was never empty —
the query was structurally incapable of seeing rows without a tenant scope,
by design (INV-001 fails closed), and the zero read was mistaken for a fact
about the data instead of a fact about the query.

## The rule

**A zero-row result from the app-role connection with no tenant context set
proves nothing about whether data exists.** It is the expected, correct
result of RLS working — not evidence of an empty table.

Before trusting any "this doesn't exist" read against the shared database:

1. Which connection is this script using? `DATABASE_URL` (→ `verity_app`,
   `NOBYPASSRLS`) needs `verity.tenant_id` set via `set_config` (what
   `withTenant()` does) before it can see any tenant-scoped row. `DIRECT_URL`
   (→ `postgres`, `BYPASSRLS`) sees everything unconditionally and is the
   right choice for an exploratory/diagnostic script that doesn't yet know
   which tenant it's looking for.
2. If using `DATABASE_URL`: is `verity.tenant_id` actually set for this
   query? A bare `new PrismaClient()` with no `$transaction` +
   `set_config('verity.tenant_id', ..., true)` around it is NOT scoped —
   every tenant-scoped table reads as empty, unconditionally, regardless of
   real contents.
3. If a read comes back empty and the plan is to act on that (seed, migrate,
   provision, delete) — re-run the same read via the bypass (`DIRECT_URL`)
   connection first, un-scoped, across every tenant, before treating "empty"
   as true. One extra query is cheaper than repairing a duplicate tenant.
4. Never chain "empty read" → "destructive/provisioning action" without this
   check in between, especially for one-time/non-idempotent scripts (see
   `verity-identity-provisioning-safety`).

## Quick reference

```js
// WRONG — silently scoped to nothing, always reads empty for tenant tables
const prisma = new PrismaClient();
await prisma.role.count(); // 0, even if roles exist

// RIGHT for a known tenant — matches app request-path behavior
await prisma.$transaction(async (tx) => {
  await tx.$executeRaw`SELECT set_config('verity.tenant_id', ${tenantId}, true)`;
  return tx.role.count();
});

// RIGHT for "does this exist anywhere, across all tenants" — bypass, read-only
const admin = new PrismaClient({ datasourceUrl: process.env.DIRECT_URL });
await admin.role.findMany({ select: { tenantId: true, name: true } });
```

## Non-goals

- Not a case for routing application code through `DIRECT_URL` — the running
  app must never hold that connection (VCA-002; see
  `deploy/compose/docker-compose.yml`'s own separation). This skill is for
  one-off diagnostic/seed/migration scripts run by a human or agent outside
  the app process, where the choice of connection is a live decision every
  time.
- Not a migration-authoring or seed-safety guide — see
  `verity-migration-safety` and `verity-identity-provisioning-safety` for
  those, adjacent but distinct failure modes.
