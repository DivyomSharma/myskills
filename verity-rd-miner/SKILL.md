---
name: verity-rd-miner
description: Use when auditing a reference system under `D:\Code\R&D\` (or any external open-source repo) for lessons applicable to Verity — "audit n8n for Verity", "mine frappe for reusable patterns", "what can we learn from odoo/Zam/calcom". Also the client UX parity audit: "how do Odoo and ERPNext serve this client", "audit Odoo pages/buttons for <client>'s modules", "prepare the client reference document". Encodes the method the twelve `taskplans/02-13_*_audit.md` files already used, not their specific findings, so the next repo's mining session takes hours instead of a full multi-turn session.
license: Apache 2.0
---

Authority: `taskplans/99_verity_custom_skills_plan.md` Skill 5. The
erpclaw extraction (Tasks 72-95) and the twelve R&D audits
(`taskplans/archive/02_digit_works_audit.md` through `13_seaweedfs_audit.md`) were
each a genuinely valuable but entirely manual process. This skill encodes
the *method*, so a session mining a new repo (`n8n`, `frappe`, `odoo-19.0`,
`Zam`, a second `calcom` clone, `liquid-glass-react`, or anything not yet
audited) reuses the discipline instead of re-deriving it.

## Two modes — pick one before starting

- **Architecture audit** (the original mode, below): what Verity can learn from how a reference
  system is *built*. Nine sections, ADOPT/ADAPT/INSPIRE/REJECT/DEFER.
- **Client UX parity audit** (added 2026-10-05): how Odoo and ERPNext *serve a specific client's
  requirements* — every menu, page, section, field group, button and workflow of the modules that
  client needs — so Verity's modules for that client can be specified to the same completeness.
  Product-owner rule: done for every client, existing and new. Use
  `docs/reference/client-reference-parity-template.md`; output goes to
  `clients/<client-slug>/reference-parity/`. Read the source, not memory: Odoo `addons/<module>/views/*.xml`
  (menus, actions, view types, `<button>` elements, statusbar states) and `models/*.py` (`state`
  selections, `action_*` methods); ERPNext `erpnext/<module>/doctype/<doctype>/<doctype>.json` (fields,
  sections) and `<doctype>.js` (`add_custom_button`). Every claim carries a source path. Every
  reference item ends with an Include / Defer / Not applicable decision.

## Architecture mode: read `taskplans/archive/03_payload_audit.md` first, then follow its shape

Every completed audit under `taskplans/archive/02-13` uses the same nine-section
shape. Read the most recently written one before starting a new audit —
don't invent a new structure:

1. **Product Model & Objectives** — target users, buyers, problems solved,
   major use cases. Understand what the reference system is FOR before
   judging how it's built.
2. **Repository Map & Codebase Anatomy** — the actual directory structure
   and what each top-level piece owns. Read the real `package.json`/repo
   layout, not the README's marketing description of it.
3. **Technical Architecture & Dataflow** — a request-lifecycle diagram
   (ASCII, matching this repo's style), not prose alone.
4. **Domain & Data Architecture** — how the reference system models its
   core entities, including any schema/versioning tricks worth noting.
5. **Identity & RBAC Model** — auth and authorization approach, concretely
   (code snippets of the actual access-check shape, not a description).
6. **Workflow Engine** (or the closest equivalent the system has).
7. **Storage, Search & Auditing** — file handling, search indexing, audit
   trail approach, whichever of these the system actually has.
8. **Verity Relevance & Verdict** — the five-way classification, applied
   to SPECIFIC features, not the system as a whole:
   - **ADOPT** — implement Verity's own version of this concept.
   - **ADAPT** — the concept is right, the specific mechanism needs a
     Verity-specific change (cite what and why).
   - **INSPIRE** — a design pattern worth reusing even though the concrete
     feature doesn't map directly.
   - **REJECT** — explicitly wrong for Verity, with the reason (cite the
     conflicting Verity invariant/ADR/decision).
   - **DEFER** — plausible later, not now, with the reason it's not now.
9. **Proposed Verity Changes** — concrete code/interface sketches for
   anything marked ADOPT or ADAPT, matching Verity's own naming
   conventions (canonical terminology table in `CLAUDE.md`) from the
   first sketch, not translated later.

## Cross-reference discipline (the part that stops duplicate work)

Before marking anything ADOPT or ADAPT, check whether Verity already has
it: `00_STATUS_INDEX.md`'s Done table, `14_capability_matrix.md`'s
existing directives, and a `Grep` of `src/server/platform/` for the
concept by name. `taskplans/104`'s correction (Payload's sketched
configuration tables turned out to already exist as `CustomFieldSchema`/
`WorkflowDefinition`/`TenantActivation`) is the concrete lesson: an audit
that skips this check re-proposes something already built.

After a single-repo audit, if two or more completed audits recommend the
same directive for the same capability (e.g. multiple systems all point
to "shared DB + RLS" for multi-tenancy), that pattern belongs in
`14_capability_matrix.md` as a cross-repo synthesis row, not left
duplicated across individual audit files — that file's own structure
already does this for the twelve existing audits.

## Non-goals

- Not a mandate to re-audit anything already covered by `taskplans/archive/02-13`
  — check `taskplans/archive/00_research_program_ledger.md` and
  `taskplans/archive/01_rd_clone_and_freeze.md` first for what's already frozen and audited.
  (An architecture audit of Odoo does not replace a client UX parity audit; they answer different
  questions.)
- Not a license to copy code verbatim from a reference repo regardless of
  its license — note the license in the audit's header (as
  `03_payload_audit.md` does) and treat findings as "lessons," never as
  a source to paste from.
- Not a build step — an audit's ADOPT/ADAPT items still need their own
  taskplan (see `verity-taskplan-writer`) and, if they touch a platform
  invariant, their own ADR (see `verity-adr-gate`) before implementation.
