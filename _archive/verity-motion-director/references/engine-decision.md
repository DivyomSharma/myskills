# Engine decision: Remotion or HyperFrames

Decide once, from the brief, before any code. Record the choice and the reason in `BRIEF.md`. The shot plan is
engine-neutral (coordinates, times, eases, ledger), so a wrong choice costs only the build, never the direction.

## 1. Hard overrides (apply first, stop at the first match)

| Situation | Engine | Why |
|---|---|---|
| Output is a still: post, carousel, ad, cover | Remotion stills (`npx remotion still`, `src/social`) | The kit and tokens already exist there. HyperFrames snapshots are for QA, not delivery |
| Must embed in the site (`<Player>`) or share components with site React | Remotion | Same components render the site and the video |
| Part of the industry-film series and reuses `src/film/engine.tsx`, `layout.ts`, `props.tsx`, `components/VerityOutro.tsx` or the `content.ts` bridge | Remotion | Reuse beats rebuild; the handoff objects between films live there |
| Voice-led with word-locked reveals, captions, ducking, loudness mastering | HyperFrames | It ships `/hyperframes-audio`, caption workflows and `media-use`; Remotion has captions but no audio chain |
| Needs shader (WebGL) transitions or a named CSS transition from the registry | HyperFrames | 14 shader and 30+ CSS transitions with tested parameters, plus `seam-gate` |
| Talking-head footage with designed overlays | HyperFrames `talking-head-recut` (or `reel-edit` on Remotion if the repo already has the footage pipeline) | Purpose-built workflows |
| Real 3D scene, models, orbit cameras | Remotion `@remotion/three` | Established in our repo; HyperFrames has a three adapter, so use it only if already committed to HyperFrames |

## 2. Scoring (when no override matches)

Answer each question for this film. Count the column that wins; the larger count is the engine.

| Question | Remotion if... | HyperFrames if... |
|---|---|---|
| Do persistent objects morph and travel across many scenes (cards becoming sidebar items, a line becoming a graph)? | Few, simple | Many. GSAP tweens DOM attributes and transforms directly, so carriers need no per-frame geometry code |
| Is the film built from real Verity React components or data (many industries from one code path)? | Yes | No |
| How many seams, and do they need tested velocity matching? | Few | Many; use the ledger plus `seam-stamp` / `seam-gate` |
| Is first-draft speed with built-in guard rails important? | No | Yes: `lint`, `check`, `snapshot` contact sheets, `timeline`, animation map |
| Is voice, captions or an audio chain involved? | No | Yes |
| Does the team need to hand-edit in a Studio timeline afterwards? | Remotion Studio is fine | HyperFrames Studio edits clips and tracks |

If it is a tie, narrative motion graphics go to HyperFrames and series, stills and embeds go to Remotion.

## 3. Evidence we have (treat as a prior, not a law)

One A/B on one film (the 73 s founder film "software ko adapt karna chahiye"):

- **Remotion build:** about 900 lines of hand-computed geometry across tokens, desk, graph and modules. It rendered clean but
  audited badly: about 24 s of 73 s frozen, instant state swaps and a hard cut. A second rebuild with a 3D desk looked
  worse, not better, because faked realism and 16 scenes were the real problem, not the engine.
- **HyperFrames build:** one HTML file and one GSAP timeline, with the site's own light tokens and carriers that persist
  across scenes. `lint` and `snapshot` caught a layout-property tween and a z-order bug before rendering. The delivered file
  audited with zero jump frames but 18 flagged holds (16.9 s of 73 s, 23 %), so it still fails the under-10 % hold gate and needs a hold pass.

Much of the difference came from direction (a carrier object, fewer ideas, the real product doing something), not the
engine. Do not credit HyperFrames with what the shot plan did.

## 4. Rules

- One engine per film. Never port mid-film. If the first build proves the choice wrong, restart the build from the same
  shot plan.
- Do not mix renders from both engines inside one timeline. A finished MP4 from one engine may be cut into another
  film's edit, but not composited scene by scene.
- Both engines render 1080-wide, 60 fps, 70-75 s films in minutes on this machine, so render speed does not decide.
- Remotion: `npx tsc --noEmit` is the lint. HyperFrames: `npx hyperframes lint`, then `check`, then `snapshot`.
- If the choice is unclear after the table, ask the user one question: "reuse the site's React components, or build a
  choreographed film from HTML?" Then record the answer.
