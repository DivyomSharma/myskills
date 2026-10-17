---
name: verity-migration-safety
description: Use before starting any debugging session that touches the database, before writing new Prisma schema, and after any schema.prisma change or migration — "add a table", "why is this query 500ing", "the Receive button doesn't work", "migrate dev is refusing to run", "add a field to X model". Also use whenever prisma migrate dev proposes a destructive reset. Prevents two real bugs this project already hit: a stale generated Prisma Client causing mysterious query failures, and unresolved migration-checksum drift blocking all future schema changes.
license: Apache 2.0
---

Authority: `taskplans/99_verity_custom_skills_plan.md` Skill 3, plus a
second, later incident from the same project not yet folded into that
taskplan's text: a genuine migration-checksum drift on the shared Supabase
database that `prisma migrate dev` refused to run past, with its only
offered automated fix being a full destructive `prisma migrate reset`.

## Incident 1 — stale client (Task 99's own citation)

A migration existed and was already applied to the live database, but the
generated Prisma Client was stale (generated before the migration), so
every query touching the changed table 500'd — including the actual
reported bug, which turned out to be a red herring layered on top of this.
**Symptom**: a query against a column/table that definitely exists in the
database fails as if it doesn't.

**Fix reflex**: run `npx prisma generate` after ANY schema change, and as
the first troubleshooting step whenever a query fails in a way that looks
like the database disagrees with the code — before assuming the bug is in
application logic.

## Incident 2 — migration-checksum drift (2026-09-04, this project)

`prisma migrate dev --create-only` refused to run with: *"The migration
`<name>` was modified after it was applied. We need to reset the 'public'
schema... You may use `prisma migrate reset` to drop the development
database. All data will be lost."*

**Do not run `prisma migrate reset` on a shared/production database.**
That is not "the fix," it is the tool's last resort offered to a
throwaway local dev database — Verity's actual database is shared
(Shree Ganesh's real tenant data lives there). Diagnose instead:

1. `npx prisma migrate status` — this is a DIFFERENT, more targeted check
   than `migrate dev`'s shadow-database replay. It can say "Database
   schema is up to date!" even while `migrate dev` still refuses — that
   combination means the *checksum bookkeeping* is wrong, not the actual
   schema.
2. Query `_prisma_migrations` directly for the named migration (raw SQL,
   read-only, via a Prisma script — see below) to see every row for that
   `migration_name`. Two rows for one name (a failed attempt plus a later
   successful one) is a real, previously-seen pattern.
3. Compute the CURRENT file's real checksum (`sha256` of the migration.sql
   bytes) and compare it against what `_prisma_migrations.checksum` holds
   for the row that actually succeeded (`rolled_back_at IS NULL`,
   `finished_at IS NOT NULL`). If they don't match, that's genuine drift —
   the file was edited after being applied.
4. Fix in this order, non-destructively, each a separate reviewable step:
   - A dead failed-attempt row (`rolled_back_at` set, `applied_steps_count`
     0): `prisma migrate resolve --rolled-back <name>` first; if the row
     persists (it can, if already marked), delete it directly — it
     represents zero applied DDL, deleting it loses nothing real.
   - A checksum mismatch on the row that DID succeed: re-stamp the
     `checksum` column to the current file's real SHA-256 via a direct,
     reviewed `UPDATE` — only after `migrate status` already confirms the
     live schema matches that file's content. This edits Prisma's own
     bookkeeping table, never business data.
5. Only after both are clean does `prisma migrate dev`/`db execute`
   proceed normally.

**Never hand-edit `_prisma_migrations` or run a destructive reset without
explicit, informed authorization from whoever owns the database** — show
the exact SQL before running it, every time. This is a schema-changing,
production-adjacent operation and the auto-mode permission classifier will
(correctly) block it regardless of in-chat approval; the product owner
may need to run it themselves from an unrestricted session, or explicitly
loosen the permission for one command.

## Standard reflex, every schema change

```
npx prisma migrate status      # confirm no drift before touching anything
npx prisma generate            # regenerate client to match schema.prisma
npx tsc --noEmit -p .          # confirm the new types actually compile
```

Run this sequence after writing new Prisma models, after applying a
migration, and as the FIRST step (not the last) when a query fails in a
way that smells like schema drift rather than application logic.

## Non-goals

- Not a migration-authoring guide — see `verity-client-capability-builder`
  for the RLS/append-only/capability-registration pattern new tables need.
- Not a substitute for reading `prisma migrate dev`'s actual error output
  — the two incidents above are the two patterns seen so far, not an
  exhaustive list of everything that can go wrong.
