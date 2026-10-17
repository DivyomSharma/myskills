# Gates: measure the delivered file, then direct

Green tooling is necessary, not sufficient: a composition can lint clean, render without error and still be a slideshow with
a stuck middle. This file defines the gates, with the measurement that proves each. Merged from `product-launch-motion`
(delivered-file verification, director loop), HyperFrames `hyperframes-cli` (lint, check, snapshot) and our own audit.

## 1. Engine gates (before the full render)

**HyperFrames** (from the project folder):

```bash
npx hyperframes lint                     # must be 0 errors; clear errors before trusting layout or contrast numbers
npx hyperframes check                    # lint, runtime, layout, motion, contrast
npx hyperframes snapshot --no-end --at 2.5,5.5,8.5,... -o snaps .   # contact sheets: opening, payload, resolve per beat
npx hyperframes timeline [--json]        # what is on each track
```

Known catches: tweening `left` or `top` is rejected (use `x` and `y`); never pair a CSS initial transform with a GSAP tween of
the same property (set initial state with `fromTo`); never tween a `.clip` with `autoAlpha`; media needs ids; a composition file
over about 350 lines should be split into sub-compositions.

**Remotion:**

```bash
npx tsc --noEmit
npx remotion still src/index.ts <Comp> out.png --frame=N     # one still per beat midpoint; or render a --scale=0.5 draft and extract frames
```

## 2. The measured audit (mandatory, on the rendered MP4)

```bash
bash <SKILL_DIR>/scripts/audit-render.sh path/to/render.mp4
```

It reports, from the delivered file:

| Measure | Method | Pass |
|---|---|---|
| **Holds** | `freezedetect` (noise 0.0008, 0.6 s) | Every flagged span is a hold declared in the shot plan; total frozen time under 10 % of the runtime |
| **Jumps** | scene-change detection above 0.18 | None, except declared hard cuts |
| **Loudness** (audio present) | `ebur128` | -14 LUFS plus or minus 0.5, true peak at or below -1 dBTP |
| **Contact sheet** | 20 frames tiled | Read it: missing content, empty zones, clipped text, wrong order |

A slow camera drift of 3-5 % is detected as motion, so it removes a flagged hold; a one-frame text swap shows up as a jump or
an instantly changed hold boundary. In our measured history: the rejected Remotion film had 18 flagged holds (about 24 s of 73 s)
and one hard jump; the HyperFrames rebuild (measured 2026-10-07) had zero jumps but still 18 flagged holds (16.9 s, 23 %), 7 of them over 1.0 s, so neither build passed the hold gate and the rebuild needs a hold pass.

## 3. Look at frames

Automatic gates do not see composition. After the audit:

1. Extract frames from the **delivered file** at the middle of every beat and at every seam plus or minus 0.1 s.
2. View contact sheets for content, then **full-size frames** for scale, weight, and legibility. Contact sheets mislead about
   size.
3. Downscale a frame to 360 px wide and read the text.
4. Check each beat against the shot plan's keyframes: focal point, anchors, safe areas, accent budget.

## 4. Checklist per beat

**Composition:** one focal point? Balanced? Negative space pointing at the subject? Anything placed at random?
**Typography:** hierarchy obvious? Breaks intentional? Redundant text? Nothing under 16 px? Anchored?
**Motion:** purposeful? Easing in the family? More than two things moving with intent? Any one-frame swaps? Does the seam
carry a carrier at matched velocity?
**Material:** real UI, drawn objects, glass subtle, shadows believable, no faked photography?
**Brand:** theme locked, tokens only, accent only for state, no banned effects?

## 5. The director loop

1. Watch the render once at speed, then scrub. Write the defect list yourself, in plain words with timestamps, before anyone
   else does. Prioritise: broken, then stuck, then glitchy, then ugly.
2. Fix everything in one batch. Re-render as a **new version** (`name-v2.mp4`), never overwriting.
3. Re-run the audit and look at the changed beats. Stop after at most one more round. Open-ended polishing makes a film worse.
4. Write down what you would fix next and put it in the report.

If the defect list is mostly about the idea (too many scenes, faked realism, no carrier) rather than the polish, go back to
the shot plan, not to the tweens.

## 6. Delivery set

The master MP4 at the brief's aspect; the sources; the shot plan; the audit report and contact sheet; a poster frame; the
captions file when there is voice; alternate aspect cuts only if the brief asked (re-layout, never scale). Record fonts,
music and any third-party assets with their licences. Report truthfully: what is real versus invented, what was not
verified (for example, "audio not listened to"), and what is not committed.
