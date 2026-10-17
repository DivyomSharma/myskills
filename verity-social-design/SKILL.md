---
name: verity-social-design
description: Visual and design system for every Verity Instagram and Meta creative - static posts (1:1, 4:5), carousels, Meta ads, stories, reel covers, announcements and industry, product, educational, comparison, workflow, proof and POV posts. Use before designing, writing or reviewing any Verity social graphic. Static counterpart to verity-motion-design; overrides generic design-skill advice.
---

# verity-social-design

Films are cinematic motion (`verity-motion-design`). Social is editorial product communication. Both are the same brand:
a dark world, light product UI, refined glass, Inter, and restraint. This skill is the visual authority for Verity
social. Copy and marketing skills (`copywriting`, `social`, `ad-creative`, `ads`, `content-strategy`) may shape
*what* is said. They never override *how it looks*. Where any generic design skill asks for a distinctive or unusual
font, a new palette or "bold" aesthetics, Verity's locked system wins.

Code lives in `video/src/social/` (Remotion stills). Renders go to `video/renders/social/`. Reference study:
`references/reference-analysis.md`. Carousel grammar: `references/carousel-system.md`. Paid creative:
`references/meta-ads.md`.

**Pipeline:** reference library → this skill → content idea → copy → creative format → composition → design →
quality audit → export. Composition is decided in grayscale boxes before glass, shadow or colour is added. A creative
has to work before effects.

## 0. Source of truth (read before designing)

- Words, numbers, panels, workflows: `content/` (`industries.js`, `businesses/*.js`, `capabilities.js`) and `index.html`.
  Use the site's own sentences wherever they fit. Never invent a metric, customer, result or capability. Proof posts
  need real evidence; if none exists, do not make a proof post.
- Tokens: `css/verity.css` (dark set for the world, light set for the UI), `design-system.md`.
- Material: `GLASS_LIGHT` and `CARD_LIGHT` in `video/src/film/layout.ts`.

## 1. Locked visual language

| | Rule |
|---|---|
| World | Dark: `#0b0f17` base, `#0f141d` alt, one soft radial lift (at most +4% luminance) behind the focal object. No gradients that read as colour. |
| Product | Verity UI in the **light** theme: `#ffffff` surface, `#0f1115` ink, `#6b7078` muted, `#e6eaee` line. |
| Glass | 93% white, 30px blur, 1px rim at 55% white, inset specular top edge, contact shadow plus soft long shadow at most 0.5 alpha. One sheen, upper left. |
| Accent | `#0a84ff` only for state and data: the live dot, an active row dot, a check, a progress line, the CTA. Never a glow, never a headline colour, never a border over 2px. |
| Type | Inter only, features `cv02 cv03 cv04 ss03`. Statements at weight 300. |
| Signature | **The two-tone statement** from the site hero: the statement in ink, its completion in muted ink, in one paragraph ("Your business is already running. *Verity makes it run as one.*"). |
| Never | Neon or blue glow, gradient text, stock photos of people at laptops, 3D blobs, emoji, icon grids, illustrated mascots, feature-card grids, more than one CTA, Canva-style badges and stickers. |

## 2. Canvas and grid

| Format | Size | Margin | Notes |
|---|---|---|---|
| Feed / Meta 4:5 (default) | 1080 x 1350 | 80 | Profile grid crops to 1080 x 1080 centred, so the hook must sit inside y 135-1215. |
| Square 1:1 | 1080 x 1080 | 80 | Only when the placement demands it. |
| Story / reel cover 9:16 | 1080 x 1920 | 80 sides | Keep y 0-250 and y 1580-1920 free of type (platform UI). Reel covers: put the hook in the centre 1080 x 1350. |

- Six columns inside the margins: content width 920, gutter 24, column 133.3.
- Baseline unit 8. Every y position and gap is a multiple of 8.
- **Fixed furniture.** The Verity mark (logomark plus wordmark, 30px tall, ink-white) always sits at the top-left
  margin corner (x 80, y 80). Micro text (URL, page number, slide count) always sits on the bottom margin line
  (bottom 80). Furniture never moves between posts; that consistency is half the brand.

## 3. Composition

**Text is never placed where there is room.** Every element states its anchor, in a code comment:

- a margin line (left x 80; top cap line y 200 for the hero; bottom line y 1270 on 4:5),
- an edge of the hero object (the headline's left edge = the UI panel's left edge; a caption's top = a row's top),
- a shared baseline across slides (the carousel hero cap line never moves),
- the canvas centre, for a single-object frame only.

**One focal point.** Size the hero at least 2.5x the next element by visual weight. A post has at most three text
blocks: hero, support and micro.

**Negative space must point at the focal point.** If a region is empty because nothing was put there, crop closer or
scale the subject up. Never fill it with a second message.

**Asymmetric by default.** Left-aligned type on the left margin. The object (UI, number, diagram) either bleeds off the
right or bottom edge or sits on the column grid. Centre only a single-object frame (one number, one lockup).

**Cropping.** Crop UI on the trailing edges (right, bottom), so its reading start (top-left chrome) stays visible.
Crop through padding or between rows, never through a word or a number. Something that bleeds must bleed at least 15% of
its width; a 2% overlap reads as a mistake.

### Composition archetypes (rotate them, never use one twice in a row on the grid)

| # | Archetype | Structure |
|---|---|---|
| A | **Editorial statement** | Hero type only, 3-6 lines, top-left. One small anchored detail (a row dot, a hairline). Large negative space below. |
| B | **UI hero bleed** | Hero on the top cap line. A light glass panel starts on the left margin under the hero and bleeds off the right and bottom edges. The panel is 60-75% of the canvas area. |
| C | **Macro crop** | One UI row, check or metric at 2-3x scale fills the frame; hero type sits above it on the margin. |
| D | **Data-led** | One number at 220-320px, weight 200-300, tabular figures; its label sits on the number's baseline or directly above its cap line. |
| E | **Workflow line** | A vertical or horizontal record line with 3-5 nodes; node labels anchored to their nodes; the hero names the outcome. |
| F | **Before / after** | Split on the vertical centre or the 3:3 columns; "before" muted and scattered, "after" ink and aligned. Same objects on both sides. |
| G | **Industry world** | A physical prop of that industry (ticket, shelf label, invoice, job card), drawn not photographed, meeting a piece of real UI. |
| H | **Carousel narrative** | See `references/carousel-system.md`. |

## 4. Typography (4:5 and 1:1 at 1080 wide; 9:16 uses the same sizes)

An Instagram post shows at roughly 0.36x on a phone, so the canvas sizes below are tuned to on-phone sizes.

| Level | Size | Weight | Line-height | Tracking | Measure | Use |
|---|---|---|---|---|---|---|
| Hero | 88-112 (default 96) | 300 | 1.04 | -0.035em | 10-18 characters per line (18 is about 860px at 96px); max 5 ink lines plus 2 muted | One statement. Ink, completion in muted. |
| Support | 36-40 | 300 | 1.3 | -0.01em | max 30 characters per line, max 3 lines | Optional. Muted. At most 0.42x the hero. |
| Data | 200-320 | 200-300 | 1.0 | -0.05em | 1 line | Numbers only, tabular figures. |
| Micro | 24-26 | 400-500 | 1.3 | 0 (labels +0.12em, uppercase) | 1 line | URL, slide count, a single UI-style label. Never under 24. |
| UI text inside panels | at least 22 on canvas | per UI | per UI | per UI | n/a | If the real UI would be smaller, crop closer or scale the panel. |

- **Line breaks are written by hand** at phrase boundaries, using `\n` and `white-space: pre-line`. Never leave a
  single word alone on a line. Check with `textWrap: 'balance'` only as a fallback.
- Hero top: the cap line sits on y 200 (4:5) unless the archetype anchors it to an object.
- Hero to support gap: 40. Support to object: at least 64. Everything else: multiples of 8.
- All-caps only for micro labels, at most one per creative.
- One dominant message per frame. No paragraph copy. No competing headlines. No label above the headline unless it
  carries information (an industry or a date).
- Copy test: if the caption is needed to understand the graphic, the graphic is wrong.

## 5. UI treatment

- Use the real Verity UI structure and words (`content/` panels: title, meta, metrics, attention rows).
- Light theme on light glass; chrome bar reads `VERITY / <TITLE>` with the meta and a live dot.
- UI is the hero visual: at least 60% of the canvas in archetype B, 2-3x scale in C. A full panel shrunk to fit is a
  thumbnail; crop instead.
- No screenshot-in-a-box (a hard rectangle with a heavy drop shadow and no material). No neon outlines, no floating-card
  collages: one surface per creative, plus at most one callout attached to the row it explains.
- Highlight state with the accent (one active dot or one row tint at 8% accent), never with arrows or circles drawn on top.

## 6. Content frameworks

The system stays fixed while the format changes. Recommended archetype per type:

| Type | Job | Archetype | Notes |
|---|---|---|---|
| Problem | Name a pain the reader recognises | A or F | Use the site's challenge copy. Two-tone statement. |
| Industry | "This was made for my business" | G or B with that industry's panel | Use the industry's own words, numbers and props. |
| Product | Show what Verity does | B or C | Real panel, real rows. |
| Educational | Teach one operational concept | E or carousel | One concept per post. |
| Comparison | Before and after | F | The same facts on both sides; only the connection changes. |
| Workflow | How information moves | E | Use real workflow steps from `content/`. |
| Proof | Result or implementation | D | Only with real, attributable evidence. |
| Founder / POV | A strong opinion | A | First person allowed; no portrait unless one is supplied. |
| Announcement | Feature, update, news | B or C | Date or version as the one micro label. |

## 7. Organic vs paid

Organic posts can be quiet and assume a follower. Paid creatives must work cold in under 2 seconds on a phone. Their
rules are in `references/meta-ads.md`: problem in the first read, product visible, CTA visible, hero at least 88px,
nothing under 24px.

## 8. Variety without drift

Across any 9 consecutive grid posts: at least 4 archetypes, no archetype twice in a row, and at most 3 posts where UI is
the hero. Variety comes from archetype, crop and scale, never from new colours, fonts or effects.

## 9. Quality gate (run on every creative before export)

Render the PNG and look at it at 100% and at 360px wide (phone scale).

- **Composition:** one focal point? Balanced? Negative space pointing at the subject? Anything placed at random?
  Every text block has a named anchor?
- **Typography:** hero 88px or more and reading first? Line breaks intentional? Lines within measure? Any unnecessary
  copy? Support clearly subordinate? Nothing under 24px?
- **Brand:** recognisably Verity in one second? Dark world, light UI, refined glass, Inter, accent only for state?
  Furniture in its fixed place?
- **Ad readability** (paid only): idea understood in 2 seconds at 360px? Value obvious? CTA clear?
- **Static quality:** it looks intentionally designed with nothing moving.
- **Subtraction test:** would removing an element, or adding whitespace, make it stronger? Then do it.
- Effects never compensate for weak composition.

Record the gate result in `video/docs/social-*.md` next to the creative.
