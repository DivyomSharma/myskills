---
name: proposal-builder
description: Convert verified discovery notes into a phased Verity implementation proposal. Use after discovery or Blueprint, with real notes supplied.
---

# proposal-builder

Refuse to start without the user's discovery or Blueprint notes. Do not invent requirements.

Sections: context in the client's own words; phased scope; deliverables per phase; integrations; explicit exclusions; assumptions; timeline; pricing and payment milestones (ask the user for numbers, do not invent); acceptance criteria; ongoing support; risks and open items.

Rules:
- Every in-scope workflow is marked `supported`, `configurable`, or `needs feasibility` against actual Verity state in `D:\Code\verity`. `needs feasibility` items go to a discovery phase, not a fixed price.
- Phase 1 should be small and demonstrable. Later phases are gated on Phase 1 acceptance.
- Output as a draft for human review. Log `proposal` with `value_inr` in `data/outcomes.csv` only after the user confirms it was sent.
