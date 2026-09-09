# The Scroll-Film Playbook (Lane B — cinematic footage)

Hard-won rules for making the whole page one continuous Higgsfield film. These are a
floor, not a ceiling — break them knowingly, never by accident.

## 1. Footage-first law
The film is the source of truth; the website is a player. Design the camera arc first
(one continuous journey, ~5 chapters), then build the page around whatever footage
actually comes back. Never storyboard the site and force footage to match — footage
drifts, copy is cheap to move.

## 1b. The default shape — 5 clips × 5s. Start here, then confirm with the user.

Measured off PULP, the best film this skill has produced (`Website Builds/pulp-cinema`,
14 Jul 2026), with `ffprobe`:

| | PULP (worked) | the 25 Jul builds (rejected) |
|---|---|---|
| clips | **5** | 9 |
| per clip | **5.04s** | 8s |
| total | **25.04s** | 72s |
| frames @24fps | **601** | 1,729 |
| frames shipped | **601 — all of them** | ~300 |
| effective scrub rate | **24fps** | ~4fps |
| resolution | 1920×1080 | 1920×1080 |
| cost | ~227 credits | — |

**Propose 5 × 5s = 25s as the default and confirm it with the user before generating.**
Say the number of clips, the seconds each, the total runtime and the credit cost, and
get a yes. Never generate a film shape nobody agreed to.

Why short wins, and it is not taste:

- **A 25s film is 601 frames. A 72s film is 1,729.** The page must ship *every* frame or
  the scrub degrades in exact proportion. 601 JPEGs at 1024px is a sane payload; 1,729 is
  not, so someone always "optimises" it down to ~300 — and 300 frames across 72 seconds
  is a **4fps slideshow**. That is the whole of "why does it feel janky". The engine is
  fine; it has nothing to draw.
- **Distance per clip is the thing that breaks continuity.** Five seconds of camera travel
  is a hop the model can actually make. Eight seconds asks it to cross a location, a scale
  and a lighting change at once, so it teleports mid-clip and you get the jump-cut.
- **It is cheaper.** 5 × 5s = 225 credits at Seedance 1080p. 9 × 8s = 648.

Go longer only when the user asks for it *and* accepts the frame payload. If they want a
longer journey, add **clips**, not seconds per clip — 7 × 5s beats 5 × 7s every time.

---

## 2. Chaining law (flawless joins)

**Use `seedance_2_0`, or the newest Seedance the account exposes.** Run
`higgsfield model list` first and take the highest version. Never silently drop to an
older or non-Seedance model because a call errored — retry, or stop and say the engine
is down.

**THE ONE LAW, TRUE FOR EVERY ENGINE (Higgsfield, Kie, fal, Replicate — all of them):
clip N's start image is clip N−1's ffmpeg-extracted LITERAL LAST FRAME — the actual
rendered pixels — never the keyframe.** Only the far end (`end_image` / `last_frame_url`)
is the next keyframe. The opening keyframe starts clip 1 and nothing else.

### 2a. FIRST — check whether the whole film fits in ONE generation

**If the engine's max duration covers your film, generate it as a single clip and skip this
entire section.** A single generation has no junctions, so there is nothing to gate, nothing
to repair, and no seam can exist. Seedance 2.0 accepts `duration` 4–15s; 15s at 24fps is
**361 frames**, which is a perfectly respectable scrub payload (PULP is 601 over 25s).

Measured 26 Jul 2026: after four failed chaining attempts on the same brief, one 15-second
single-take generation — `duration: 15`, start pinned to the opening keyframe, end pinned to
the final keyframe, and the WHOLE journey written as one continuous move — produced the
first genuinely continuous film of the session, first time, and the owner approved it on
sight. Cost ~615 Kie credits versus ~820 wasted on seamed 4-clip attempts.

Write the prompt as one unbroken sentence-chain through every chapter ("begins on X… falls
past Y… continues down to Z… lands in W"), and say *"one single unbroken shot, no cuts, no
edits, continuous camera move throughout"* explicitly.

Only chain multiple clips when the journey genuinely cannot fit the duration cap. **Chaining
is the compromise, not the default.**

### 2b. Chaining — and the trap that makes it fail

**Do not assume an engine lands exactly on the frames you pin.** Whether you chain
keyframe→keyframe in parallel, or sequentially off each clip's real extracted last frame,
both strategies rest on the same premise: that `first_frame_url` / `start_image` means
*"begin on exactly these pixels."* **On Seedance 2.0 via Kie it does not.**

Proven 26 Jul 2026, in the order the theories were killed:

| attempt | junction SSIMs |
|---|---|
| parallel, clip prompts = keyframe descriptions | 0.686 / **0.179** / 0.942 |
| parallel, corrected motion prompts | 0.606 / 0.549 / 0.698 |
| **sequential, start = previous clip's literal last frame** | **0.266** |

The decisive test: clip 1's last frame was extracted, confirmed **byte-identical** to the
file uploaded, and the upload URL confirmed publicly fetchable (HTTP 200, exact size). Clip
2 was then generated with that URL as `first_frame_url` — and still opened on a visibly
different image. The engine had the exact frame, could read it, and re-imagined it anyway.

So on this engine a pin is a *suggestion*. Two clips pinned to the same keyframe are two
independent ~0.7-fidelity renderings of one idea, which match each other far worse than
either matches the target. **No prompt, ordering, or upload trick fixes that** — it is why
2a exists. If you must chain, verify on the FIRST junction before paying for the rest.

Sequential chaining off literal last frames remains correct on engines that *do* honour the
start pin (the Higgsfield path PULP was built on). Verify which kind you have — one clip,
one junction measurement — before committing a film's budget to it.

**The thing that actually breaks the join is a prompt that disagrees with the end pin.**
Measured 26 Jul 2026 on a honey-drop film: 4 clips, correctly pinned
`first_frame_url = kf_N`, `last_frame_url = kf_N+1`, and the junctions still came back
0.686 / 0.179 / 0.942. The cause was not the engine. Each clip had been handed **the
description of its own start keyframe** as its prompt — the storyboard's `clips` array was
really a list of keyframe descriptions, ids and all (`"id": "kf2"`). Clip 2 was told to
arrive at *"a bead swelling, about to release"* — which is exactly where it started — so it
sat there for five seconds and never travelled to kf3's dark falling world. The model obeyed
the words over the image, every time.

> **A clip's prompt describes the JOURNEY from its start pin to its end pin — never the
> state of either end.** *"Continuing the same descent, the bead releases and falls away
> into the dark"* travels. *"A bead of honey swells at the comb edge"* does not.

Two cheap checks before spending, both free:

- **Off-by-one audit.** If the storyboard has N keyframes it has N−1 clips. If your clip
  array is N long, or its entries are named `kf*`, you are about to send keyframe
  descriptions as motion prompts. Print `clip[i].prompt` next to `kf[i] -> kf[i+1]` and
  read them as a sentence: *does this text get me from the first image to the second?*
- **Destination words.** Every clip prompt must name something visible in its END keyframe
  that is absent from its start. Clip 2 above never mentioned darkness or open air, and it
  never went there.

For URL-based engines (Kie et al.) the extracted last frame is a **local** PNG, so it must
be uploaded to get a URL before it can be a `first_frame_url` — keyframes already live on a
CDN, but real last frames do not. Kie's uploader is
`https://kieai.redpandaai.co/api/file-base64-upload` (see `scripts/kie-chain.py:upload`).

Each clip's `--start-image` is the **ffmpeg-extracted literal last frame** of the previous
clip — not a lookalike keyframe, the actual pixels. And **pin the far end too**:

```bash
ffmpeg -sseof -0.05 -i clipN.mp4 -update 1 -q:v 1 clipN-last.png
higgsfield generate create seedance_2_0 --prompt "..." \
  --start-image clipN-last.png --end-image kf(N+1).png \
  --duration 5 --resolution 1080p --mode std --generate-audio false
```

**Both ends, always.** Seedance 2.0 takes `end_image` — verified against the live CLI on
25 Jul 2026 (`higgsfield model get seedance_2_0` lists `start_image` AND `end_image`). An
earlier version of this playbook chained on the start image alone, on the false belief
that was all Seedance supported. A clip pinned at one end only is free to wander and then
cut back to wherever it needs to be, and that cut is the jump the viewer sees. Pinning
both ends removes the freedom structurally instead of asking the prompt nicely.

Only the opening keyframe (Nano Banana Pro) starts the chain; every later start-image is a
real last frame. Keep one continuous camera direction (always descending / always pushing
in) — reversals read as cuts. Uniform clip length = constant scrub speed.

**Cost at 1080p, measured 25 Jul 2026:** 5s = 45 credits · 8s = 72 · 10s = 90. A
four-clip 8-second film ≈ 288 credits. Audio off — a scroll-film is silent.

## 2c. Reading SSIM without crying wolf

A low score between two frames means **look**, not **fail**. Fast camera motion drops
consecutive-frame SSIM to ~0.3–0.5 legitimately: on the 15s honey take, frames 1/3 second
apart during the fast approach to the jar scored 0.28, and the pixels showed a perfectly
smooth continuous move — the rim simply grew a lot in a third of a second. Sampling every
8th frame exaggerates this further.

Distinguish the two cases by looking at three consecutive samples:

- **Fast motion** — same objects, same light, same world, progressively transformed. Fine.
- **Teleport / cut** — different composition, different lighting state, or an object that
  appears or vanishes. Real failure.

Inside a single generation a true cut is rare by construction; between two separately
generated clips it is the default. Judge junction scores strictly and within-clip scores
generously.

## 3. The junction gate (measured, never eyeballed)
```bash
ffmpeg -i A-last.png -i B-first.png -lavfi ssim -f null - 2>&1 | grep All
```
- **≥ 0.88 pass** · 0.80–0.88 watch it in motion · a true fail is **structural**.
- SSIM under-reads on stochastic texture (clouds ~0.66, embers ~0.72, liquid caustics
  ~0.60 can all be seamless). The number says *where* to look; the side-by-side decides.
- The #1 real failure is **grade/geometry drift** (an invented sunrise, a new horizon).
  Fix by regenerating with: *"Continue the exact same shot from the reference frame,
  identical framing, identical colour grade. Do not change the colour grade."*
- **Dissolves/crossfades over a bad junction are forbidden** — the scrub lets the user
  park on the seam, which exposes the mask instantly. Fix the join, don't hide it.

## 4. Billing truths (verify by balance delta, not docs)
- `--generate-audio false` is *the* cost lever — audio ON silently ~3×'s the bill.
- Measured price ladder per 5s clip (confirm with `higgsfield generate cost`):
  1080p/std ≈ 45 · 720p/std ≈ 22.5 · 720p/fast ≈ 17.5 · 480p/fast ≈ 7.5. 10s = 2×5s.
- **Draft the whole chain at 480p/fast to validate, then re-run approved prompts at
  1080p.** A regen at draft tier costs a fraction of a full one.
- ~15% of jobs fail server-side with no reason and don't bill — just retry the same call.

## 5. Assembly
- Concat dropping the duplicate junction frame (`select='gte(n,1)'` on clips 2+), and
  **always `-fps_mode vfr`** on the master encode — default CFR sync pads ~5 dup frames per
  junction = frozen scrub zones.
- Extract every 2nd frame to ~300 JPEGs at ~1280px, `-q:v 4`. (Dark, grainy footage nearly
  doubles JPEG bytes — 1280/q4 keeps the payload light without visible loss at cover-fit.)
- Sample the final frame's edge colour → the seam hex for the film→content handoff.

`scripts/chain-step.sh` and `scripts/assemble.sh` do all of this.

## 6. The scrub engine (why it's jank-free)
- **Canvas + pre-extracted JPEGs**, never `<video currentTime>` scrubbing (seek stutter).
- **ImageBitmap sliding window**: `drawImage(HTMLImageElement)` forces a *synchronous* JPEG
  decode on first paint (and after cache eviction) — that decode spike *is* the frame-by-
  frame jank. `createImageBitmap` decodes off-thread; keep a window of decoded bitmaps
  around the playhead (±18 ahead, evict/close beyond ±28) so every draw is a pure GPU blit.
- Lerp the frame index (`current += (target-current)*0.14`) for butter. Cap DPR at ~1.5.
- Lenis smooth scroll; a concurrency-capped image pump; `nearestFrame()` fallback so a
  missing frame never blanks the canvas.
- **Measure jank with rAF deltas (p95/max), not average fps.** Target max < 50ms.

## 7. Chrome, seam, and the ambient layer
- **Adaptive header**: sample the drawn frame's top strip luminance (~every 180ms) → toggle
  a `.on-light` class. Fixed chrome over changing film can't be one hard-coded colour.
- **Seamless handoff**: start the next section's background gradient at the *sampled* final-
  frame colour. No visible line between film and content.
- **Ambient hero layer** (optional, free): sprite-based canvas particles themed to the world
  (snow glisten, gold pollen) over the static first frame, fading out across the first ~7%
  of scroll — the hero feels alive before the scrub starts. Use one offscreen radial-gradient
  sprite + `drawImage` per particle (never `shadowBlur`); stop rendering entirely at alpha 0.
- Film grain + vignette sell the "one shot" feel; fade both out with the handoff.

## 8. Verification harness
Host preview panes throttle hidden tabs (rAF freezes → stale screenshots). The reliable path:
puppeteer-core + system Chrome + a page dev-contract:
- `?jump=<scrollY>` → land pre-scrolled and force-settle all scroll state.
- `window.__ready = true` only after frames are decoded and settled.
- Capture: `goto → waitForFunction(__ready) → wait ~1200ms → screenshot`. Shoot every beat
  position *and* every junction. Hide any cursor-follower until first real mousemove or it
  photobombs captures at 0,0.

`scripts/verify.js` does capture + jank-test.

## 9. Governance
Design taste and design code are done by the Claude model only. Mechanical steps (ffmpeg,
SSIM, puppeteer, vercel) are pure code — no model. Quote credits before spending; show the
receipt after. One continuous shot, one world per brand.
