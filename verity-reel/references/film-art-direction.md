
# Film art direction (16:9 industry films)

The standard every Verity industry film is held to. It sits on top of the code system in `video/src/film/`
(`layout.ts` grid and materials, `engine.tsx` camera, grade and audio, `props.tsx`) and the content bridge
`video/src/reels/content.ts`. Principles come from studying premium SaaS product films (see
`references/reference-analysis.md`). We take their discipline, never their branding, layouts or scripts.

**premium = better composition + typography + spacing + timing + materials + transitions.**
Not more animation, glow, particles, 3D, UI or text. If a simpler scene says it better, ship the simpler scene.

**Pipeline:** reference library → this skill → industry content → screenplay → composition → animation → audit → render.
Composition is settled on paused frames before any animation is written.

**Provenance:** merged from the archived `verity-motion-design` skill; it is now part of `verity-reel`. Edit it here.

## 0. Before you touch a scene

1. Read the film's screenplay in `video/docs/film-NN-*.md` and the shared grid in `video/src/film/layout.ts`.
2. Pull every product word, number and workflow step from `content/` via `src/reels/content.ts`. Never invent a metric,
   capability or customer. Props (tickets, receipts, shelves) may be invented, product data may not.
3. Write the shot list as one line per shot: *focal point / statement (or none) / what the camera does / how it hands off*.
   If a shot has no single focal point, it is not a shot yet.

## 1. Composition (1920x1080)

**Grid.** Safe margins 120 left/right, 96 top/bottom (`SAFE`). Twelve columns of 120 with 20 gutters inside the safe area.
Two working zones: the **text column** (x 120, width 620, `TEXT`) and the **product zone** (x 840 to 1800, `UI`).
Only full-bleed backgrounds and deliberately cropped hero objects cross the margins.

**Every element is anchored to another element.** Text never goes "where there is room". Before placing type, name what it
aligns to:

- a shared baseline (statement bottom = panel bottom = text baseline, y 984),
- a shared cap line (statement top = top of the workflow title it describes),
- the edge of the object it talks about (statement bottom = bottom of the voice note it refers to),
- the frame centre, for brand moments only.

If you cannot name the anchor, the text is in the wrong place. Write the anchor in a code comment.

**Hierarchy.** One focal point per frame. Second-read element at most 40% of the focal point's visual weight. Everything
else is environment: dimmed, blurred or cropped.

**Object scale.**
- Hero UI (a workflow being read): fills 60-75% of frame width, and may bleed off the right or bottom edge.
- Context UI (an overview being recognised): 50% of frame width, fully inside the product zone.
- Props: large and cropped beats small and complete. A ticket cropped at the frame edge reads as a world. Three tiny
  tickets read as clip art.

**Asymmetry.** Default composition is left text column against right product zone, weighted roughly 1:2. Centre a
composition only when there is exactly one object (logo lockup, single number, end card).

**Negative space** is a decision. It is fine only when it points at the focal point: dark space left of the UI makes the
UI the subject. Space that exists because nothing was placed there means the frame needs a closer crop.

**Cropping.**
- Crop at a deliberate place: through a margin, a gutter or a row boundary, never through a word or a number.
- Crop the trailing edge (right, bottom), so the reading start (top-left) of UI stays intact.
- Once something bleeds in a shot, it keeps bleeding until the shot ends. Do not alternate.

**UI and type relationship.** Statement and UI are two halves of one sentence. The statement names the idea; the UI proves
it. They never say the same words. If a UI title already says "A shortage before it happens", the statement is not a
paraphrase of it. Remove the statement, or make it the consequence ("Caught before service.").

## 2. Typography

Inter (loaded in `engine.tsx`), features `cv02 cv03 cv04 ss03`. Four levels only.

| Level | Size @1080p | Weight | Line-height | Tracking | Max line | Max lines |
|---|---|---|---|---|---|---|
| Hero statement | 72-84 (`TYPE.statement`) | 300 | 1.04-1.08 | -0.035em | ~18 characters (620px column at 72px) | 3 |
| Supporting | 0.38-0.42 x hero (28-32) | 300-400 | 1.3 | -0.01em | ~42 characters | 2 |
| Data (UI numbers) | 44-140, tabular figures | 300-400 | 1.0-1.1 | -0.03 to -0.05em | n/a | 1 |
| Micro / UI | 17-25 on screen, never under 16 at final scale | 400-500; labels 500 uppercase | 1.3 | labels +0.14em | n/a | 1 |

"At final scale" means after camera push. A 15px label shown at 1.3x is 19.5px, which is fine.

**Line breaks are written, not wrapped.** Break at phrase boundaries ("A shortage, / caught before it happens."). Never
leave one short word alone on the last line. Use `textWrap: 'balance'` only as a safety net.

**Alignment.** Left-aligned, ragged right, by default; all left text in a film shares x 120. Centre only a single-object
frame (brand lockup, one number). Never centre multi-line body text.

**Spacing.** Statement to support gap is 0.38 x hero size (about 28). The label above a UI title gets 14. Keep one rhythm per film.

**Say it once.** Each concept appears once per film. Do not repeat "one record", "one system", "one Verity" or the
industry name across shots. If the visual communicates the idea, delete the text. A shot with no statement is often the
strongest shot. Typical films carry 4-6 statements in 35 seconds.

**Editorial, not webpage.** No marketing adjectives ("seamless", "powerful"), no feature lists, no CTA verbs except on the
end card. Statements are observations in plain present tense.

## 3. Motion language

**Preferred:** camera moves that create depth, controlled parallax (background at 0.3-0.5x), continuous transformation of
one object into the next, scale transitions, mask reveals, coordinated movement where 2-3 elements share one curve and
start within 0.1s.

**Easing** (defined in each film file):
- `glide` = `bezier(0.22, 1, 0.36, 1)` for arrivals and camera settles.
- `smooth` = `bezier(0.45, 0, 0.15, 1)` for exits, pushes and handoffs.
- Linear only for slow ambient drift (no more than 2% scale or 20px over a whole shot).
- No springs with visible overshoot. No bounce.

**Durations at 60fps:** text in 0.8-0.9s, text out 0.5-0.6s, camera pushes 1.2-2.0s, UI state changes 0.5-0.7s.

**Budget:** at most 2 things moving with intent at once, plus ambient drift. Text is still once it lands. No per-letter
animation. No looping wobble on UI.

**Banned:** generic slide-ins from off-frame, bounce, spring overshoot, random floating, particles, light streaks, lens
flares, constant text animation, gratuitous zooms, neon SaaS effects, rainbow rings, gradient-text, glowing orbs.

**Transitions transform, they do not cut.** Find the shared shape between scenes (a barcode that becomes a barcode, a
ticket that becomes a page, a list row that opens into a workflow). Use a hard cut only on a deliberate beat, at most once
per film. A cross-dissolve is a fallback.

## 4. Camera language

The camera lives on the product or the prop, not on the canvas. Implement it as one transform on a scene group
(scale + translate around a named origin), or with `Stage`/`Obj` from `engine.tsx` for real depth.

| Move | Use | Spec |
|---|---|---|
| Macro / detail | prove one fact (a number, a check) | 1.6-2.4x on a UI region, the rest cropped |
| Hero | introduce the product surface | panel 50% of frame width, 3-6 degree Y tilt, settles flat |
| Slow push-in | from overview to the thing being read | 1.0 to 1.25-1.4x over 1.5-2s, origin at the region's top-left |
| Slow pull-back | from detail back to context, or to scale/breadth | reverse of push, `smooth` |
| Lateral | move along a row of props (shelf, pass, rack) | 40-160px over the shot, linear or `smooth` |
| Orbit | reveal that a surface is physical | 4-8 degrees rotateY, never a full turn |
| Depth reveal | new scene arrives from behind | from scale 0.92, blur 10px, opacity 0 to 1, 0, 1 |
| Environmental | establish the industry world | wide prop shot, slow drift, no UI |
| UI fly-through | only when the workflow spans screens | camera travels along the step line, max once per film |

Push-ins change where the eye reads. Every push must land on something worth reading at its new scale.

## 5. Material and lighting

- **World:** deep dark (`DK.base #080b11` / `DK.baseAlt #0e131c`), one soft warm key from top-left (`Grade`), vignette
  0.25-0.35, grain 0.07. No coloured light sources.
- **Product UI:** always the light theme.
- **Glass** (`GLASS_LIGHT`): about 93% white, 30px blur with saturation, 1px rim at 55% white, inset specular top edge,
  short contact shadow plus long soft shadow at most 0.5 alpha. One diagonal sheen on the upper left at most 0.5 alpha.
- **Cards on glass** (`CARD_LIGHT`): near-opaque white, 7% ink hairline, 1-2px shadow. Cards do not have their own glass.
- **Accent:** `#0A84FF` only for state and data (checks, progress, live dot, selected row). Never as glow, never on borders
  thicker than 2px.
- **Banned:** neon glass, blue glow, thick glowing borders, HUD styling, gradient fills on UI, more than one sheen.
- Paper props use `CREAM` / `PAPER_INK` with a warm shadow. Paper is the analogue world and the UI is the resolved world.

## 6. Verity UI on screen

- Use the real Verity UI structure and words from `content/` (panel metrics, attention rows, workflow steps).
- Light theme, always.
- It must be readable at final scale. If micro text is under 16px on screen, push the camera in or cut the element.
- Integrate the UI into the world: a slight perspective tilt (3-6 degrees) that settles flat as the camera arrives, a contact
  shadow, and dimming or blur when it is not the focal point. A UI that never moves in depth reads as a screenshot.
- One surface per film. The same panel changes state (overview, workflow, roster). Do not spawn new floating cards per
  concept.
- Callouts, if any, attach to the UI element they describe (same top edge or same row), never floating in empty space.

## 7. Visual storytelling

Arc: **problem, tension, transformation, product, workflow, resolution, scale, brand.** The metaphor is industry-specific:

- **Retail & Commerce:** shelves, stock counts, barcodes, receipts, the till.
- **Food & Hospitality:** the pass, order tickets, covers, the clock of service, rosters, reservations.
- **Other industries** get their own physical world (the clinic: appointment slips and charts; manufacturing: the job card
  and the line; education: the register and the timetable). Decide the world before writing any statement.

Never reuse one industry's prop or animation in another film. Shared across the series: the grid, the panel material, the
type scale and the handoff device (each film's last frame becomes the next film's first object).

## 8. Restraint

Before adding anything, ask: "does the shot fail without it?" If not, cut it. Prefer a closer crop to an extra element,
a held frame to an extra animation, no text to redundant text.

- **A frame must look intentionally designed even when all animation is paused.** Any frame you pause on must have a clear
  focal point, anchored text and balanced space. Motion reveals a good composition; it never rescues a bad one.
- **Do not use visual effects to compensate for weak composition.** If a shot feels flat, fix the crop, scale, anchor or
  copy first. Glow, blur, particles and extra movement are not fixes.
- **Once a film passes the audit, stop.** Further polish goes into the next film in the series, not into extra animation
  on this one.

## 9. Pre-render visual audit (mandatory)

Render stills at the midpoint of every shot (`npx remotion still src/index.ts <Comp> out.png --frame=N`), or tile frames
from the draft render with ffmpeg. Check each shot and fix every failure before the final render.

- **Composition:** one clear focal point? Frame balanced? Negative space pointing at the subject? Objects scaled to their
  role? Anything competing?
- **Typography:** obvious hierarchy? Headline large enough? Intentional line breaks? Redundant text (against the UI or an
  earlier shot)? Consistent spacing? Text anchored to something you can name?
- **Motion:** purposeful? Refined easing? More than 2 intentional movers? Transition connected to the previous shot?
- **Material:** UI physical (tilt, shadow, depth)? Glass subtle? Shadows believable? Lighting controlled?
- **Brand:** dark world, light UI, refined glass, accent only for state, no banned effects?

Record the audit results in the film's doc under "Audit".
