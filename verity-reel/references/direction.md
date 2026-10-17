# Direction: brief, three directions, signature move

Merged from `product-launch-motion` (three directions, kill two; dials; signature move), `hyperframes-creative`
(story spine, house style, beat direction) and `film-art-direction.md` (arc, restraint). Do all of this before opening an editor.

## 1. Intake (ask once, batch the questions, pre-fill from the repo)

| Ask | Why it matters |
|---|---|
| Audience and the **one claim** the viewer should believe afterwards | Everything else is cut against this |
| Platform and **aspect** (16:9, 9:16, 9:8, 4:5, 1:1) | Fixes grid, type and safe areas; never crop one aspect into another |
| **Length** | Sets the beat budget (section 7) |
| **Theme**: light or dark | Locks the whole look; see `verity-look.md` |
| **Voice**: recorded VO, TTS, or silent with captions | Decides whether timing comes from word timestamps |
| **Real assets**: product screens, components, data in `content/` | Truth pass |
| Series continuity: must it hand off to or from another film? | The handoff object is planned in the shot plan |
| Business or industry shown | Props and copy come from `content/businesses/<slug>.js` |

Write the answers into `BRIEF.md`. If theme, aspect or voice are missing, ask; do not guess. They are the three choices
that cost a rebuild.

## 2. Truth pass

- List every number, name and claim that may appear (the approved-figures list). Source each from `content/`, the site or a
  real capture. Anything not on the list does not appear.
- Props (a quotation, a chat) may be invented as props; mark them as props in the shot plan. Prop numbers never contradict
  panel numbers.
- Never fake a product feature. If the product cannot do it, the film does not show it.
- Never use third-party logos, real customers or stock faces.

## 3. Fixed and free

| Fixed (the Verity layer) | Free (what a viewer would actually describe) |
|---|---|
| Inter; the site's tokens for the chosen theme | Which beats, how many, in what order |
| Real Verity UI, light theme, subtle glass | Camera personality: locked, drifting, continuous |
| One accent with a written budget | The carrier object and the signature move |
| Truth; determinism; verified delivered file | Pacing and rhythm, within the beat budget |
| Anchored type, written line breaks | Metaphor: drawn objects, graphs, tools, props that suit the industry |

If two Verity films cannot be told apart, the free column was skipped.

## 4. The direction dials

Place the film on each dial in writing before building.

| Dial | One pole | Other pole |
|---|---|---|
| Energy | contemplative, long holds | relentless, cut on every beat |
| Density | one idea, vast negative space | layered, many things true at once |
| Depth | flat 2D | real perspective |
| Camera | locked, cuts do the work | continuous move across the film |
| Product | literal reconstructed UI | abstracted or metaphorical |
| Texture | clinical | grain, print, glitch |
| Sound | silence and UI ticks | sound-design-led |
| Voice | narrated throughout | title cards only |

Two films in the same series should differ on at least three dials. Extremes read as a point of view; centres read as the
default look.

## 5. Three directions, kill two

Write each direction in five lines: **world** (what the viewer is looking at), **carrier** (the object that persists),
**camera**, **type and material**, **sound**. Each must sit inside the Verity layer. Judge them against the one claim, kill
two, and record the survivor plus why the other two lost. Reaching for the last film's look because it exists is the failure
this step prevents.

## 6. Signature move

One sentence naming the thing only this film does, for example "a line that is forced into a grid and set free" or "a
discovery card that grows into the app". If you cannot name it, the film has no direction yet. The signature move is
usually the carrier's journey.

## 7. Story arc and beat budget

Arc, adapted per industry (film-art-direction.md): problem, tension, transformation, product, workflow, resolution, scale, brand.
Name the industry's own physical metaphor first (a till, a pass, a matter folder, a job card, a timetable) and never reuse
another film's prop. For a founder or belief film the arc is observation, friction, the different approach, how it works,
the belief, the product at work, the brand.

| Film length | Beats | Notes |
|---|---|---|
| 15 s | 3 | hook, proof, brand |
| 30 s | 4-5 | one carrier, one product moment |
| 45 s | 6-7 | trailer length; the main trailer is 44 s and works |
| 75 s | 10-12 max | average 6-7 s per beat |

Each beat proves one thing. Cut any beat that decorates. Say each concept once; if the visual already says it, delete the
text. Statements are plain present-tense observations, not marketing adjectives. Hook in the first 2-3 s with motion and a
claim, never a logo intro.

## 8. Script and timing

- Narrated: record or generate the VO first. Frame durations come from the real VO length; cue every reveal to the measured
  start of the word it illustrates (word-level transcript). Never estimate timings and fix them later.
- Silent: write a timing sheet (second-by-second) from the script's own timestamps. Where the script's header and timestamps
  disagree, follow the timestamps and say so.
- Reveals land on the word. 200 ms late reads as lag.
