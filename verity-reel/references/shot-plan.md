# Shot plan: frame-by-frame design and transition planning

The shot plan is the film. It is engine-neutral: coordinates in canvas pixels, times in seconds (and frames at the film's
fps), eases by name. Write it before code, and keep it next to the render. A copy-paste form is in `templates/shot-plan.md`.

## 1. Per-beat spec

Every beat gets one block. A beat with no single focal point is not a beat yet.

| Field | What to write |
|---|---|
| id and time | `B4  18.0-25.0 s  (1080-1500 f @60)` |
| Purpose | the one thing this beat proves |
| VO / script line | exact words, with start times when narrated |
| Focal point | the one object the eye is on |
| Carrier(s) | the persistent object(s) entering, crossing or leaving this beat |
| Keyframes | **three paused frames** (see section 2) |
| Text | exact copy, size, line breaks, anchor |
| Camera | the leg: start scale and pan, end scale and pan, ease, origin |
| Motion verbs | one verb per moving element, with ease and duration |
| Hold budget | any declared hold, with its length and reason |
| Seam in / seam out | ledger row ids |
| Sound | cue times |

## 2. Keyframes: compose the paused frames first

For each beat define three frames: **in** (just after the entry settles), **payload** (the moment the beat proves its point)
and **out** (just before the exit begins). For each frame list every element with its rectangle `x, y, w, h` and its role
(focal, carrier, support, environment). Check each against the composition rules before writing any animation:

- One focal point; the second-read element at most 40 % of its visual weight.
- Every text block anchored to a named edge, baseline or object.
- Safe areas respected (`verity-look.md` §5); something that bleeds must bleed at least 15 % of its width.
- Negative space points at the focal object; space that exists only because nothing was placed there means crop closer.
- Everything legible at 360 px wide (downscale the paused frame and read it).

Animation is then interpolation between keyframes with named eases. Do not invent geometry while animating.

## 3. Time budget

| Rule | Value |
|---|---|
| Average beat | 5-8 s |
| Event density | at least one visible event every 1.5 s (something arrives, moves, changes state, or a camera leg starts or ends) |
| Max undeclared hold | 1.0 s (the audit flags frames unchanged for 0.6 s; each flag must map to a declared hold) |
| Declared holds | reveal comma 0.3-0.75 s; a belief or claim line up to 1.5 s; end card up to 2 s |
| Camera drift on a beat over 2 s | 3-5 % scale or a 20-60 px travel, eased, bounded, ending before the seam |
| Entry | 0.26-0.38 s for UI and cards, 0.8-0.9 s for a hero statement |
| State change | 0.4-0.7 s, cross-faded or carried, never a one-frame swap |
| Seam | 0.4-0.7 s total |

## 4. Sustained-motion routes

Every second between entry and exit belongs to one of these. Name the route per beat in the plan.

| Route | What it is |
|---|---|
| Staged reveals | Content held back and paid off on narration beats; the frame keeps gaining information |
| Camera with intent | A mapped scale and pan: establish wide, travel, arrive on the subject |
| Sequenced UI life | The product behaves: progress advances, rows highlight in turn, counts tick |
| Animated sequence | Elements act out a beat: a card files into a sidebar, an item is dragged, a result assembles |
| Cursor-led action | An oversized cursor walks the eye to a trigger; its click ignites the next beat |

## 5. Transition planning: the vector ledger

Write the ledger before authoring any seam. One row per seam.

| # | Cut time | Exit vector | Entry vector | Carrier | Technique | Duration | Blur | Cause |
|---|---|---|---|---|---|---|---|---|
| S1 | 6.20 s | x, left, power4.in | x, left, power4.out | the six cards | cut-the-curve | 0.6 s | 0-8 px | the current |

Rules:

1. **Axis, direction, speed and phase must match** across the cut. On Z, direction is the sign of the scale change: a
   receding exit answered by a grow-from-small entry is a mirrored vector, the most common violation.
2. **The current.** Pick one dominant direction for the film (default LEFT). Every ordinary seam uses it. Never run
   consecutive seams in opposing directions.
3. **Reserved vectors** are spent on meaning: upward is a conclusion rising above what came before; Z forward is pushing
   deeper into the same thought; Z backward is an arrival; a scale burst is leaving a world.
4. **Carrier first.** Name the object that crosses the cut (a card that docks into the next layout, a cursor mid-path, a line
   that becomes a graph). With no natural carrier, the heroes carry it by partial travel plus early fade. Never a crossfade.
5. **Vocabulary budget.** At most three seam types per film; default to cut-the-curve in the current's direction.
6. **Causal motion.** An effect starts on the causing frame. A force is the licence for a direction change; an uncaused flip
   is a ping-pong. Reactions scale with implied mass.
7. **Stillness before climax.** 0.3-0.75 s between the major action and its result.
8. **Edits reopen the seam.** Any change to a beat's first or last second, including re-timing to new VO, invalidates the
   adjoining ledger rows.

Engine notes: with HyperFrames, write the ledger as `ledger.json` and stamp and verify it with the `motion-doctrine`
scripts (`seam-stamp.mjs`, `seam-gate.mjs`). With Remotion, implement each row as mirrored exit and entry interpolations
sharing one origin and verify numerically on the delivered file with the audit.

## 6. Hand-off to build

The plan is ready to build when: every beat has keyframes; every seam has a ledger row with a carrier; every hold is
declared; every text block has an anchor; the approved-figures list covers every number on screen; the theme, aspect and
engine are recorded.
