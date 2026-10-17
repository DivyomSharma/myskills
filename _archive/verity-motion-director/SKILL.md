---
name: verity-motion-director
description: The single entry point for making any Verity motion video, whether a brand film, industry film, founder film, trailer, promo, explainer, reel or short motion-graphic unit. It decides the engine (Remotion or HyperFrames), then directs the whole job: brief, three directions, truth pass, script and timing, a frame-by-frame shot plan, a transition plan (vector ledger), build, a measured audit of the delivered file, the director loop, and delivery. It merges verity-motion-design, HyperFrames motion-doctrine and cut-the-curve, product-launch-motion, hyperframes-creative and saas-vid. Use it before writing any scene of any Verity video, and again when a finished video looks stuck, glitchy, generic or "AI slop".
---

# verity-motion-director

One front door for every Verity video that has motion. It exists because green tooling is not good film: our own builds have
shipped with a third of the runtime frozen, instant state swaps, faked photorealism and a look that changed with each
brief. The laws below are the fixes, in the order they matter.

**Scope.** Anything animated that we author. Static posts, carousels and ad stills go to `verity-social-design`. Editing
existing talking-head footage goes to the HyperFrames `talking-head-recut` / `embedded-captions` workflows or `reel-edit`.
This skill calls two layers rather than replacing them: `verity-motion-design` (industry-film art direction, 16:9) and
`verity-social-design` (stills). The sources it merges are listed in `references/sources.md`.

**Pipeline.** brief and truth → direction → engine → script and timing → shot plan with vector ledger → build → measured
gates → director loop → ship. Do not skip 2, 5 or 7; they decide whether the film is good.

| # | Phase | Output | Read |
|---|---|---|---|
| 1 | **Brief and truth.** The audience, the one claim, platform and aspect, length, theme, voice or not, real assets, approved figures | `BRIEF.md` | `references/direction.md` §1-2 |
| 2 | **Direction.** Three genuinely different directions, kill two, name the signature move, lock the look | direction block in `BRIEF.md` | `references/direction.md` §3-6 |
| 3 | **Engine.** Remotion or HyperFrames, decided once, recorded in the brief | one line in `BRIEF.md` | `references/engine-decision.md` |
| 4 | **Script and timing.** Written for the ear. VO and word timings first when narrated, otherwise a timing sheet | `SCRIPT.md` | `references/direction.md` §7 |
| 5 | **Shot plan.** Frame-by-frame spec per beat, paused keyframes with coordinates, then the vector ledger for every seam | `SHOTPLAN.md` | `references/shot-plan.md`, `templates/shot-plan.md` |
| 6 | **Build.** Composition before animation; one engine per film | code | `references/motion-law.md`, `references/verity-look.md` |
| 7 | **Gates.** The engine's lint and snapshots, then the measured audit of the delivered file | audit report | `references/gates.md`, `scripts/audit-render.sh` |
| 8 | **Direct.** Watch it, write the defect list yourself, fix, re-render as a new version | v2, v3 | `references/gates.md` §5 |
| 9 | **Ship.** The set, not just the master | `deliverables/` | `references/gates.md` §6 |

## The laws

Break one and the film reads amateur, however good the single frames are.

1. **Truth first.** Every product word, number, panel row and UI element is the product's own (`content/`, the site, real
   components). Props may be invented as props; a number may never be. Write the approved-figures list before animating.
2. **One idea per beat, and beats get room.** Average beat 5-8 s. A 75 s film has 10-12 beats at most. Cramming sixteen
   scenes into 73 s gave each idea four seconds and none landed.
3. **Composition before animation.** Design the paused frames (coordinates, anchors, hierarchy) first. A frame must look
   designed with everything stopped. Effects never rescue weak composition.
4. **Every text block has a named anchor** (margin, baseline, edge of the object it describes). Never place text where
   there is room.
5. **A carrier crosses every seam.** One concrete object persists across the cut at matched position and velocity. No
   crossfade between scenes, no cut to black.
6. **The vector law.** At a seam the exit and entry share axis, direction (Z is the sign of the scale change), speed and
   phase, and the cut lands mid-motion on both sides. One dominant direction per film (the current); other vectors are
   reserved for meaning. Plan it in the ledger before building.
7. **Nothing sits dead.** Inside a beat every move completes; across a seam momentum carries. No frame is unchanged for
   more than 1.0 s unless the shot plan declares that hold (reveal comma 0.3-0.75 s, belief line, end card).
   A slow camera leg (3-5 %) or a sequenced UI event owns every beat longer than 2 s. Idle wobble, breathing and floating
   loops are banned.
8. **No instant state swaps.** Text, labels, numbers and status never flip in one frame. Cross-stack them, mask them, tween
   them or let a carrier move them.
9. **Honest material.** No CSS imitation of photography (paper, laptops, handwriting, 3D desks). Use real UI built from the
   real components, drawn objects that look drawn, or real captured assets.
10. **Ration the accent.** Verity blue marks state and data only: a live dot, an approval, a selected row, a path being
    followed. Never a glow, never decoration.
11. **Type is large, short and written.** Hero statement 72-96 px at 1080 wide, nothing under 16 px on screen, line breaks
    written by hand, each concept said once.
12. **Cursor is a stage prop.** At least 44 x 54 px, heavy stroke and shadow, enters from off-frame, its click ignites the
    next beat on the same frame, zoom origin on the control it clicks.
13. **Easing is a family.** Arrivals expo/power4 out, exits and camera moves in-out, no bounce, overshoot only on a
    confirmation. Similar elements share one ease and duration.
14. **Determinism.** No render-time clocks or random values; every value derives from the frame or an index.
15. **Lock the look before building.** Theme, direction and aspect are decided in the brief. Flipping them mid-build costs a
    rebuild; the shot plan is engine-neutral so only the build is redone.
16. **Verify the delivered file, not the source.** Run `scripts/audit-render.sh` on the rendered MP4, look at frames at
    full size, write the defect list yourself, and version every render (`name-v3.mp4`, never overwritten).
17. **No clones.** Take the discipline of a reference, never its branding, layouts, animations or scripts.

## Engine decision (details in `references/engine-decision.md`)

Decide once, from the brief, before any code.

| If the film is... | Engine |
|---|---|
| A still (post, carousel, ad) | Remotion stills (`src/social`) |
| Embedded in the site with `<Player>`, or must share React components with the site | Remotion |
| Part of a series that reuses `src/film/*` (engine, VerityOutro, props) or the content bridge for many industries | Remotion |
| A choreographed narrative or explainer built from persistent objects, many seams, morphs, cursor beats | **HyperFrames** |
| Voice-led with word-locked sync, captions, audio mixing | **HyperFrames** |
| Needing WebGL or shader transitions, or the 30+ CSS transition registry | **HyperFrames** |
| Real 3D scene work | Remotion (`@remotion/three`) unless the HyperFrames three adapter is already in use |

When the answers split, default to HyperFrames for narrative motion graphics and Remotion for series, stills and embeds. One
engine per film. Never port mid-film.

## Verity look in one paragraph

The theme is a brief input. Default **light**, from the site's own tokens (`css/verity.css`), because that is the system
behind the main trailer. **Dark** only when the brief or the industry-film series asks for it. Either way: Inter,
real Verity UI in the light theme, glass kept subtle, one accent. Tokens, type scale, safe areas per aspect and the outro
rules are in `references/verity-look.md`.

## Reference map

| File | What it holds |
|---|---|
| `references/direction.md` | Intake, fixed vs free, direction dials, three directions, signature move, story arc, beat budget |
| `references/engine-decision.md` | Overrides, scoring table, evidence, hybrid rule |
| `references/shot-plan.md` | The frame-by-frame spec, keyframes, hold budget, event density, the vector ledger and transition plan |
| `references/motion-law.md` | Merged motion rules and numbers: seams, easing, entrances, stagger, camera, cursor, type, sound cues |
| `references/verity-look.md` | Tokens (light and dark), type, glass, UI, aspect grids, outros, series handoffs |
| `references/gates.md` | Per-engine gates, the measured audit, direct loop, delivery set |
| `references/lessons.md` | Failures from our own builds, each with cause and fix |
| `references/sources.md` | What each merged skill contributed, what was skipped, credits |
| `templates/shot-plan.md` | Copy-paste shot plan and ledger |
| `scripts/audit-render.sh` | Freeze, jump, loudness and contact-sheet audit of a rendered MP4 |

## Definition of done

- [ ] Brief records audience, claim, aspect, length, theme, voice, engine and the approved-figures list
- [ ] Three directions written, two killed, signature move named in one sentence
- [ ] Shot plan has keyframes with coordinates and a ledger row for every seam
- [ ] `audit-render.sh` shows no undeclared hold over 1.0 s and no undeclared jump
- [ ] Frames sampled from the delivered file at every changed beat, looked at full size, defect list written
- [ ] Nothing under 16 px on screen; every number on the approved list
- [ ] Loudness measured on the delivered file when there is audio
- [ ] Render versioned; sources, shot plan and audit report kept next to it
- [ ] You have written down what you would fix next
