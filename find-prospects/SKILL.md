---
name: find-prospects
description: Research a segment and city for Verity prospects; return a sourced shortlist into data/companies.csv. Use for "find distributors in Pune", "find facility-management companies in Hyderabad".
---

# find-prospects

Input: segment (`distributor` | `facility_staffing` | `manufacturer`) and city. Default shortlist size 20, never a directory dump.

1. Read `CLAUDE.md` hard rules and `docs/schema.md`.
2. Search public sources only: company sites, Google Maps listings viewed manually, industry associations, public tender portals, job pages. Respect robots/terms.
3. For each company capture: name, website, city/state, branches, service lines, observable size signals, source URLs, today's date.
4. Dedupe against existing `data/companies.csv` by domain, else normalized name + city.
5. Append rows with `status=researched`. Leave unknowns empty. Never estimate revenue or headcount.
6. Run `uv run scripts/engine.py validate`. Fix every problem.
7. Reply with the shortlist (name, why it fits, source) and what to qualify next.
