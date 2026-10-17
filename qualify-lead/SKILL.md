---
name: qualify-lead
description: Score researched companies against the Verity rubric, separating facts, hypotheses and unknowns. Use after find-prospects or when asked to qualify or prioritise leads.
---

# qualify-lead

1. Read `docs/scoring-rubric.md` and the company's row and sources in `data/companies.csv`.
2. Fetch more public evidence only where it changes a score: decision-maker, manual-workflow signals, trigger.
3. For each company write a `data/scores.csv` row with the six sub-scores within caps, plus `facts` (sourced), `hypotheses` (inferred, labelled), `unknowns`.
4. Unknown scores conservatively. A hypothesis never counts as evidence for the manual-workflow criterion beyond its cap.
5. Add contacts to `data/contacts.csv` only if publicly listed, with source URL and consent note.
6. Run `uv run scripts/engine.py score` then `validate`. Update company `status` to `qualified` (priority) or `nurture`.
7. Reply: ranked list, tier, the single strongest fact per lead, and what must be verified before outreach.
