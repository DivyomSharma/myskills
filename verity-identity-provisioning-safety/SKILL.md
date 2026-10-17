---
name: verity-identity-provisioning-safety
description: Use before running any one-time identity/tenant bootstrap or seed script against a real Supabase project — "run seed-pa-oms.ts", "seed the new client tenant", "provision these real people's logins", "the seed script says run once, is it safe to run". Also use whenever a seed script's `createUser`/`provisionIdentity` call fails with an "already registered" or unique-constraint error. Prevents a real incident this project already hit: assuming a "run once" seed had never run, re-running it, and getting a duplicate tenant plus 5 duplicate Party/User identities that had to be found and repaired by hand.
license: Apache 2.0
---

Authority: real incident, 2026-09-17, `prisma/seed-pa-oms.ts` (a
`"Idempotency: NONE. Run once"` script). A tenant-emptiness check using the
wrong connection (see `verity-tenant-query-safety`) led to re-running this
script. Supabase Auth already had real accounts for 14 of 19 people
(created by an earlier, partially-completed attempt); Postgres had none of
the matching tenant/role/Party/User rows for the new tenant, because that
earlier attempt's transaction had rolled back after creating some Auth
accounts but before finishing. The re-run then created a second tenant with
fresh duplicate Party/User rows for people who already had real identities.
Two more incidents inside the same fix: (a) the script's hardcoded emails
for two Team Leaders were stale placeholders (`@plotarmour.verity.app`) that
no longer matched the real registered addresses (`@plotarmour.in`); (b) the
`auth_user_id` unique constraint surfaced a THIRD layer — some people
already had a global `Party`/`User` (Party/User have no `tenantId`, so they
persist across a tenant's entire lifecycle) with no matching Supabase Auth
row (deleted at some earlier point), so even after linking the Auth side
correctly, `provisionIdentity` still failed on the Postgres side.

## The rule

**"Run once" on a script's own comment is a promise about intent, not a
guarantee about the current state of the target project.** Supabase Auth,
global `Party`/`User` rows, and tenant-scoped rows are three independent
systems that can each be in a different state of completion after a prior
attempt — check all three before assuming any one of them is empty.

## Procedure, before running any such script

1. **Read the script's own idempotency claim, then verify it independently**
   — don't trust "Idempotency: NONE" to mean "definitely never run"; a prior
   attempt can have partially succeeded and left real state behind.
2. **Check Supabase Auth for existing accounts by email first**, read-only,
   before calling any `createUser`. If found, do not create a duplicate —
   link to the existing account (query its `id`, use that as `authUserId`).
   Never invent a new account for a real person's real email if one exists.
3. **Check for an existing global `Party`/`User` by `authUserId`** (or by
   email on `Party`, cross-referenced) before calling `provisionIdentity` —
   it has no de-duplication by design (see its own doc comment: "do not
   paper over it here" — that rule is about not GUESSING whether two
   different logins are the same human, not about refusing to reuse a
   *known-identical* one). If the same auth account already has a Party/User,
   add a new `TenantMembership` to it, never a second `provisionIdentity`
   call — the unique constraint on `auth_user_id` will refuse it anyway, but
   catching it before the call avoids a half-completed transaction.
4. **Verify hardcoded emails/names in the script against current reality**
   before trusting them — a script's constants can go stale (a real person's
   assigned address can change between when the script was written and when
   it's run again).
5. **After any run that mixes "linked existing" and "created new,"
   independently verify** every affected identity has exactly one `Party`
   row, a working `authUserId` (resolves to a real Auth account), and the
   correct role/team membership — don't assume success from the absence of
   a thrown error.
6. If a run partially fails: check what it already committed (Auth accounts
   are NOT rolled back by a failed Postgres transaction — they're a separate
   system) before re-running blindly.

## Non-goals

- Not a general seed-script-authoring guide — this is specifically about
  safety before/during a run against a project with unknown prior state.
- Not a replacement for `verity-tenant-query-safety` — that skill is about
  the read that decides whether to run the script at all; this one is about
  running it correctly once you've decided to.
