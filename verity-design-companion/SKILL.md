---
name: verity-design-companion
description: Use alongside `impeccable` for any Verity frontend work — before or during writing/changing UI, pass this skill's Verity-specific iOS design constraints (ADR-033) as structured input rather than relying on memory of CLAUDE.md prose. Trigger whenever `impeccable` is invoked in this repo, or whenever a change touches colour, tint, cards/panels/chrome, typography, controls, navigation, motion, or the monochrome mark.
license: Apache 2.0
---

Authority: `verity-spec/17_decisions/adr/adr-033.md` (2026-10-05) — **Verity's interface follows
Apple's iOS Human Interface Guidelines on every surface, client workspaces and HQ alike.** ADR-033
supersedes the visual parts of ADR-011/012/023/024/025/026; if you remember gold accents, glass cards,
an atmospheric background or light-weight headings, that is the old system. This file is a static
checklist: hand-edit it whenever ADR-033 changes.

## The constraints, as structured input

**Where to change things.** Tokens: `src/app/globals.css`. Shapes: `src/components/ui/primitives.tsx`,
`Modal.tsx`, `DataTable.tsx`, `src/components/shell/ShellChrome.tsx`, `HqChrome.tsx`. Fix the shared
piece; do not restyle one page by hand.

**Colour.** iOS system colours only, via tokens:
- `bg-canvas` systemGroupedBackground; `glass-card`/`Surface`/`Panel` the white/`#1C1C1E` cell;
  `bg-surface-sunken` a cell inside a cell; `bg-[var(--color-control)]` system fill (fields, gray
  buttons, chips); `border-line` iOS separator.
- `text-text` label, `text-text-secondary` secondaryLabel, `text-text-tertiary` tertiaryLabel
  (increased-contrast values, AA).
- Tint: `bg-accent` + `text-accent-on` for filled controls, `text-accent-ink` for tint text and glyphs,
  `bg-accent-subtle` for tinted fills and selected rows. Default systemBlue `#0A84FF`; never hard-code a
  tint; contrast is computed in `src/server/platform/accent.ts`.
- Semantic: `text-success|warning|danger|info` and `-subtle` fills — iOS green/orange/red/blue,
  accessible variants, independent of the tint.

**Materials.** Translucency only on bars (`.glass-shell`: sidebar, nav bar, tab bar) and overlays
(`.glass-overlay`: menus, popovers, sheets). Content cells are opaque, 12px corners, no border, no
shadow, no gradient. Never blur a card, row, badge or status dot.

**Typography.** Keep the existing system font stack (SF Pro on Apple devices; never embed SF Pro).
iOS text styles: h1 Large Title 34/41 bold (`PageHeader`); card titles Headline 17 semibold (`Panel`);
section headers footnote 13 uppercase secondary (`SectionHeading`); body 15 wide / 17 phone; secondary
text 13. Numbers are bold or semibold — never `font-light`/`font-thin`. Inputs at least 16px on phones.

**Controls.** `Button` variants: `primary` iOS filled, `secondary` iOS gray (tint label), `ghost` iOS
plain, `danger` destructive tinted; 10px corners, semibold, press dims (`active:opacity-70`). Fields are
rounded system-fill text fields (`Input`, `Textarea`, `Select`). Chips are capsules. Checkboxes are
selection circles. Touch targets 44pt.

**Navigation.** Large title per page. Wide screens: iPadOS sidebar — selected row tint fill + white
label, other rows label text with tinted glyphs, plain section headers. Phones: iOS tab bar (client
shell and HQ). Dialogs (`Modal`): bottom sheet on phones, centred form sheet wider; centred Headline
title; gray circular close button; iOS 40% dimming.

**Motion.** iOS curves (`--ease-out`, `--ease-slide`), springs from `src/lib/motion.ts`;
`prefers-reduced-motion` cross-fades; `prefers-reduced-transparency` makes materials opaque.

**Kept from earlier ADRs.** WCAG AA in both themes (ADR-011 constraint 1); the Verity mark is
monochrome and never tinted (ADR-012); light and dark are one system.

## Procedure

1. Before writing or changing any Verity UI, check the surface against the constraints above: right
   token, opaque content, tint only on interactive things, iOS text style, iOS control shape.
2. Hand `impeccable` this as explicit input when invoking it for Verity work.
3. Anti-regression before finishing: no translucency on content; no gradients or glows on surfaces; no
   light numerals; no hard-coded colour outside tokens; no semantic colour equal to the tint; mark not
   tinted.
4. **Before shipping any new collection/detail/form screen** (or reviewing one a client called
   unfinished), run the `obvious-basics-checklist` skill: per-row actions, drill-in, ledger/statement
   for counterparties, print/export, mobile table safety (`DataTable` only), search/filter, empty and
   error states.
5. **No internal identifiers on screen, and no dead navigation.** Never render
   `verity.<capability>.<entity>`, command keys, raw config keys, snake_case field names or
   `Verb entity @ Scope` strings; map to business labels (`src/components/ui/business/vocabulary.ts`).
   No developer commentary as UI copy. Every sidebar `href` resolves to a page.
6. **Judge completeness against the client's reference-parity document**
   (`clients/<slug>/reference-parity/`, template `docs/reference/client-reference-parity-template.md`)
   and `docs/reference/module-completeness-bar.md`, not against what the code already has.

## Non-goals

- Not a replacement for `impeccable` — this supplies Verity's iOS specifics; `impeccable` supplies
  general craft.
- Not a mandate to re-litigate ADR-033 — propose a new ADR if a change genuinely improves on it.
