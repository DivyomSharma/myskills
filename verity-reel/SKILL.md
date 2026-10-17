---
name: verity-reel
description: The single final skill for making a Verity reel, Meta ad, short film or motion-graphic unit at the quality of the R09 "WhatsApp is not the problem" reel - dark world with light objects, voice-led timing, English-only on-screen text, zero jitter, art-directed keyframes, a measured audit and a beat-synced music bed. Covers brief and truth, direction, script from voiceover word timings, shot plan, the Remotion build recipe, stability and overlap gates, BGM mixing, delivery, and the talking-head variant. It replaces verity-motion-director, verity-motion-design, workflow-reel, reel-edit, reel-captions and reel-style-aevytv. Use before writing any scene of any Verity video, and again when a finished video looks vibrating, overlapping, generic or cheap.
---

# verity-reel

One front door for Verity video. It exists because tooling that passes is not the same as a film that looks premium, and
because the user's rejections were specific: jitter, text colliding, flat layout, Hinglish and subtitles on screen. The laws
below fix those, in the order they matter. The reference film is **R09**: `video/src/ads/R09/` (comp
`Ad-R09-WhatsApp-9x16`), delivered as `video/renders/ads/R09/verity-meta-R09-9x16-v1-bgm.mp4`. Match its quality and style.

`<skill>` below is `.claude/skills/verity-reel`. Scripts run from `video/` (they need its `node_modules`).

**Scope.** Anything animated that we author, for any Verity platform. Static posts, carousels and ad stills go to
`verity-social-design`. Generic Remotion API questions go to `remotion-best-practices`. Product-wide promo with AI voiceover
is `promo-video` (not used for Verity ads: we use the founder's own voice).

## Pipeline

brief and truth > direction > script from the voiceover > shot plan > build > gates > music > deliver. Do not skip the
gates; they are where R08 and R09 were actually fixed.

| # | Phase | Output | Read |
|---|---|---|---|
| 1 | **Brief and truth.** Audience, the one claim, aspect, length, theme, voice, approved offer wording and figures | `BRIEF.md` | `references/direction.md` §1-2, `video/ads/00-strategy/*` |
| 2 | **Direction.** Three directions, kill two, name the signature move | brief block | `references/direction.md` §3-6 |
| 3 | **Script from the VO.** Transcribe the recording, anchor every beat to word timings in one `V` object | `V` in `Film.tsx` | `references/build-recipe.md` §1, `references/audio.md` |
| 4 | **Shot plan.** Keyframes with coordinates, seams planned | `SHOTPLAN.md` | `references/shot-plan.md`, `templates/shot-plan.md` |
| 5 | **Build.** Composition before animation, dark world and light objects | code | `references/build-recipe.md` §2-3, §7 |
| 6 | **Gates.** Typecheck, stills sweep scored 1-10, overlap sweep, stability, measured audit | defect list | `references/build-recipe.md` §4-6, `references/gates.md` |
| 7 | **Music.** Drop synced to a story anchor, ducked bed, loudness unchanged | `...-bgm.mp4` | `references/audio.md`, `scripts/mix-bgm.sh` |
| 8 | **Deliver.** Versioned files, truthful report | `deliverables/` | `references/gates.md` §6 |

## The laws

1. **Truth first.** Every product word, number and UI element comes from the product or `video/ads/00-strategy/`. Props
   (names, amounts, messages) may be invented as props and are labelled so. A claim not in `offer-and-claims.md` is not approved.
2. **Voice leads.** Time from the recorded VO; never squeeze the voice. The VO may be Hinglish; **on-screen text is English
   only and there are no subtitles** until the founder specifically asks for them (decision 2026-10-10).
3. **Dark world, light objects** is the Meta-ad style: near-black room, headlines in near-white, every touchable object
   (phone, paper, cards, sheets, workspace) is a light Verity object. Theme remains a brief input for other work; never
   flip it mid-build.
4. **One idea per beat, one focal point per frame.** Beats get room (about 5-8 s). Each concept is said once; if the visual
   carries it, delete the text. There are no captions, so headlines carry the key line for sound-off viewers.
5. **Composition before animation.** Paused frames must look designed: named anchor for every text block, objects large and
   cropped rather than small and complete, negative space that points at the subject.
6. **Stillness.** Settled text does not move. No whole-scene zoom over text, no looping ambient motion, no per-frame shake,
   no animated font size, no depth-reveal scale/blur on text-heavy sheets. Settle with `glide`, round translates to whole
   pixels. A hold means hold. (Fixes and numbers: `references/build-recipe.md` §5.)
7. **One layer at a time.** The outgoing headline or sheet is gone before the next lands in the same place. Check ghosts
   at every transition +/- 0.2 s.
8. **Carriers cross seams** (an object or the camera persists across a cut) and **no instant state swaps**: tween, mask or
   cross-stack. A hard cut is allowed on a deliberate beat, like the Verity mark entering. (`references/motion-law.md`.)
9. **Honest material.** Drawn objects look drawn; UI is the real Verity UI. No CSS faked photography, no glow, no neon,
   no gradient text. Accent `#0A84FF` marks state and data only.
10. **Type is large, short and written.** 72-104 px headlines at 1080 wide, nothing under 16 px on screen (the UI floor
    is 20 px on canvas), line breaks written by hand. Meta safe band: keep hook, offer and CTA inside y 250-1500.
11. **The offer frame is the cleanest frame**: struck ₹5,000 very large, accent bar sweeping through it, then FREE; held still.
12. **Verify the delivered file, not the source.** Stills sweep, `audit-render.sh`, `region-stability.sh` on every settled
    text block. Version every render; never overwrite. Stop after one more round; open-ended polish makes it worse.
13. **Say what you did not verify.** Audio is measured, not heard; a render is sampled, not watched. Report both.

## Verity look in one paragraph

Inter (300 headlines, 500 labels, uppercase labels +0.14em), Verity UI in the light theme, glass subtle, one accent.
Tokens, type scale, safe areas and outro rules: `references/verity-look.md` (its default-light note is for site and
industry films; Meta ads use law 3 above). Shared dark stage and token scoping: `video/src/ads/stage.tsx`. Props:
`video/src/ads/R08/props.tsx`, `video/src/ads/R09/props.tsx`.

## Engine

Meta ads, reels and stills: **Remotion** (proven by R08 and R09; one comp, `Root.tsx`, `render:ad-r<nn>` script).
Narrative motion graphics with many seams, cursor beats or WebGL transitions can use HyperFrames; decide once per film
(`references/engine-decision.md`). Never port mid-film.

## Reference map

| File | What it holds |
|---|---|
| `references/build-recipe.md` | The R09 step by step: VO timings, stage, beat map, gates, stability fixes, registering an ad |
| `references/audio.md` | VO leads; music placement by drop, level, ducking, loudness verification and its honest limits |
| `references/direction.md` | Intake, truth pass, dials, three directions, signature move, story arc, beat budget |
| `references/shot-plan.md`, `templates/shot-plan.md` | Frame-by-frame spec, keyframes, hold budget, the vector ledger |
| `references/motion-law.md` | Seams, easing, entrances, camera, cursor, type in motion, sound cues, banned list |
| `references/verity-look.md` | Tokens (light and dark), type, glass, real UI, grids, outros |
| `references/film-art-direction.md`, `film-reference-analysis.md` | 16:9 industry-film art direction (grid, anchors, camera language, material) from the archived `verity-motion-design` |
| `references/gates.md` | Engine gates, measured audit, stability and overlap checks (§2b), the director loop, delivery set |
| `references/lessons.md` | Failures from our own builds, with cause and fix, including R08/R09 |
| `references/talking-head.md` | The footage-based variant: tighten, transcribe, cut plan, punch-ins, captions |
| `references/engine-decision.md` | Remotion or HyperFrames |
| `references/sources.md` | What was merged, what was archived, what was left alone |
| `scripts/stills.mjs`, `contact-sheet.sh` | Render a stills sweep through one bundle, tile it |
| `scripts/audit-render.sh` | Holds, jumps, loudness and contact sheet of the delivered file |
| `scripts/region-stability.sh` | Proves settled text is not moving |
| `scripts/transcribe.py`, `find-drop.py`, `mix-bgm.sh` | Word timings; music drop and beat; the BGM mix |

## Definition of done

- [ ] Brief records audience, claim, aspect, length, theme, voice, offer wording and the approved-figures list
- [ ] Beats keyed to word timings in one `V` object; on-screen text English only; no captions unless asked
- [ ] `tsc --noEmit` clean; every keyframe scored 8 or above in a stills sweep, ghost overlaps checked at each transition
- [ ] `region-stability.sh` under 0.05 on every settled headline, the offer and the end card
- [ ] `audit-render.sh` run; any frozen span over 1.0 s is a declared hold (settled text under the voice, offer, end card)
- [ ] Music bed: drop lands on the story anchor, mix loudness equals the voice-only file, original left untouched
- [ ] Offer wording matches `offer-and-claims.md`; any deviation from the script is stated
- [ ] Renders versioned; the report says what was measured and what was not heard or watched

