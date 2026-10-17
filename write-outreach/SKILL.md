---
name: write-outreach
description: Draft one personalised email, LinkedIn message or call opener per qualified Verity prospect using only supported claims. Drafts only; never sends.
---

# write-outreach

1. Only for companies with tier `priority` and a sourced contact in `data/contacts.csv`.
2. Open with one real public fact about the company (cite the source in a note below the draft, not in the message).
3. Name the operational area in general terms ("keeping attendance, replacements and payroll aligned across sites"). Never assert that this company has the problem unless they said so or evidence is cited. Phrase as a question or common pattern.
4. Describe Verity honestly: a platform configured to how the business operates. Name no module as shipped; check `D:\Code\verity` CLAUDE.md if unsure.
5. Offer a short operational conversation, and the Business Analysis Blueprint (Rs 5,000 value, limited-time free) as scoped discovery, not a consulting giveaway. Confirm the offer is still live with the user.
6. Under 90 words for email, under 50 for call opener. One ask. No hype, no fake urgency.
7. Output: draft, source note, and `HUMAN APPROVAL REQUIRED`. Do not send. Respect DND/opt-outs in `consent_note`.
8. After the user sends, log `contacted` in `data/outcomes.csv`.
