# The Verity look: tokens, type, glass, grids

The theme is a brief input; lock it before building. Default light. Use dark only when the brief or the industry-film
series asks for it. Source of truth: `css/verity.css` and `design-system.md`; film materials in `video/src/film/layout.ts`.

## 1. Tokens

| Token | Light (default) | Dark |
|---|---|---|
| base | `#F7F8FA` | `#0B0F17` (site) / `#0B0C0E` (cinematic briefs) |
| base-alt | `#F1F3F7` | `#0F141D` |
| surface | `#FFFFFF` | `#141A25` |
| ink | `#0F1115` | `#F4F7FB` |
| ink-muted | `#6B7078` | `#8E9AAE` |
| line | `#E6EAEE` | `rgba(244,247,251,0.14)` |
| line-hair | `#EDEFF3` | `rgba(244,247,251,0.08)` |
| accent | `#0A84FF` | `#0A84FF` (site) |
| accent-text | `#0050A8` | `#80BBFF` |

Always read tokens through the CSS variables in Remotion (`src/index.ts` imports `css/verity.css`) and in HyperFrames (copy
the `:root` block). Never hardcode a hex that has a token. If a brief gives its own palette (for example `#6E8FFF` accent),
use it only if the user explicitly set it and note the deviation from the site.

Backdrop: a soft radial lift (light: white centre to base at the edges; dark: surface centre to base) and nothing else. No
gradient that reads as colour, no texture beyond optional grain at 5 %.

## 2. Type

Inter only, features `cv02 cv03 cv04 ss03`. Four levels:

| Level | At 1080 wide | At 1920 wide | Weight | Tracking |
|---|---|---|---|---|
| Hero statement | 72-96 px | 72-84 px | 300 | -0.03 to -0.04 em |
| Support | 28-40 px | 28-32 px | 300-400 | -0.01 em |
| Data / numbers | 44-140 px, tabular | same | 300-400 | -0.03 to -0.05 em |
| Micro / UI | 16-26 px, never under 16 on screen | 17-25 px | 400-500, labels 500 uppercase +0.14 em | |

Two-tone statement (the site hero): ink for the statement, muted for its completion. Sentence case; uppercase only for micro
labels. UI text inside panels must read at 20 px or more on a 1080-wide canvas: crop or push in rather than shrink the
product. The founder film "adapt" used 13-14 px labels and they were unreadable on a phone crop.

## 3. Material

- **Glass (light):** about 74-93 % white, 24-30 px blur, 1 px rim at 6-7 % ink, inset white specular top edge, one soft long
  shadow at most 9 % ink. One diagonal sheen, upper left.
- **Glass (dark):** 93 % white panel with 30 px blur, rim at 55 % white, long shadow at most 0.5 alpha. The UI stays light on a
  dark world.
- **Cards on glass:** near-opaque white, 1 px hairline, 1-2 px shadow. Cards do not carry their own glass.
- **Accent:** state and data only (live dot, selected row, approval, path being followed, CTA). No glow, no border over 2 px.
- **Drawn objects, not faked ones:** wireframe or flat-drawn objects are honest; CSS "photographs" of paper, laptops and
  handwriting are not.

## 4. Real UI

Use the real Verity structure and words: panel title and meta, metrics, attention rows, workflow steps, terminology, capability
names (`content/` via `src/reels/content.ts`). One product surface per film that changes state, not a new floating card per
idea. Callouts attach to the element they describe. Perspective tilt (3-7 degrees) settles flat as the camera arrives; a UI that
never moves in depth reads as a screenshot. It must be legible at final scale.

## 5. Grids and safe areas

| Aspect | Canvas | Margins | Notes |
|---|---|---|---|
| 16:9 | 1920 x 1080 | 120 left/right, 96 top/bottom | Text column x 120 width 620; product zone x 840-1800 |
| 9:16 | 1080 x 1920 | 80 sides, keep top 250 and bottom 420 free | Reels, Stories and ad overlays cover those bands |
| 9:8 | 1080 x 960 | 80 sides, 72 top/bottom | Hero cap line at y 96; product zone below or right of the statement |
| 4:5 | 1080 x 1350 | 80 | Hook inside y 135-1215 for the grid crop |
| 1:1 | 1080 x 1080 | 80 | |

Design each aspect separately; never scale a 16:9 layout. Baseline unit 8.

## 6. Outros and series

- **Industry-film series:** the master outro is `src/film/components/VerityOutro.tsx` with locked copy ("Run your business.
  Clearly.", "Enterprise operations, simplified.", theverityai.xyz) and 16:9 and 9:16 layouts. Do not vary the copy per industry.
- **Founder or script-led films** may close with the script's own copy, built with the same material and timing language
  (`GlassTile` and `reveal` are exported from `VerityOutro.tsx`). Flag the deviation from the locked copy in the brief and the
  report, and flag a differing URL for the user to confirm.
- **Handoff chain:** each film's last object becomes the next film's first object; see
  `video/docs/industry-films-screenplays.md`.
- The wordmark is the lowercase `verity` logo with the hourglass mark, not typed capitals.

## 7. Verity dark industry films

`verity-motion-design` remains the art-direction layer for the dark, 16:9, cinematic industry films (grid 120/96, text
column and product zone, cream paper props, camera language table, pre-render audit). Apply it when the brief says
"industry film", then add this skill's gates and ledger on top.
