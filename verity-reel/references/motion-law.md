# Motion law: the merged rules and numbers

Merged from HyperFrames `motion-doctrine` and `cut-the-curve` (seams), `product-launch-motion` (grammar, camera, cursor),
`film-art-direction.md` (camera language, restraint) and `oversized-cursor`. Numbers are working starts measured on real
builds; widths scale with the canvas (a 12 % partial travel is about 230 px at 1920 wide and 130 px at 1080 wide).

## 1. Two failure modes

- **Slideshow:** everything arrives at once, then nothing happens. Fix by cueing each piece to the thing that earns it and
  giving every beat more than one event.
- **Screensaver:** everything drifts independently, forever, and the frame is still moving when it cuts. Fix by bounding
  every move and ending the last tween before the seam.

They are opposites and easy to fix one into the other. The target: several cued events, each completes, then a still read of
no more than 1.0 s.

## 2. Seams (cut-the-curve catalogue)

| Seam | Use for | Exit | Entry | Notes |
|---|---|---|---|---|
| **Cut-the-curve** (default) | Ordinary scene boundary | 0.2-0.4 s `power4.in`, partial travel about 12 % of the frame in the current's direction, opacity out by 25-30 % of the travel | Same travel and duration, `power4.out`, ignites at about 0.35 opacity mid-path | Mirrored eases so velocity matches at the cut. Total about 0.6 s |
| **Zoom-through** | Pushing deeper into the same thought | scale 1 to 1.2, blur 0 to 10 px, `power3.in`, 0.2 s | scale 0.75 to 1, blur 10 to 0, `expo.out`, 0.5 s | Headlines and short phrases. Exit opacity is its own linear tween |
| **Inverse zoom-through** | Arrival: something bigger lands | scale 1 to 0.8, blur to 10 px, 0.2 s | scale 1.25 to 1, blur to 0, `expo.out`, 0.5 s | Z sign rule: scale velocity keeps the same sign on both sides |
| **Waterfall cut** | Text to text | words exit ±12 % of the frame, 0.34 s `power4.in`, +0.022 s stagger | 0.3 s `power4.out`, entry gaps 0.05 s x 0.84 decay | The line peels instead of sliding as a block |
| **Rack-focus blur-cut** | A deliberate visible cut | blur up, `power2.in` | swap at peak blur 8-12 px (never over 18), `power2.out` | Soft optics, not momentum |

Blur scale: 10 px for text-scale subjects, 18-20 px only when both sides are full-bleed surfaces. 20 px on text smears the
letters and reads as a glitch.

Z is a sign: push (growing) answered by pull (shrinking) is a mirrored vector. The incoming scene's own pop-in intro must not
fight the handoff sign; hold its opening frame composed instead.

**Scale-burst** (leaving a world): the old surface scales up past the camera while fading (about 1.9x over 0.55 s, `power4.in`);
the arrival lands on the same Z sign.

## 3. In-scene techniques

- **Waterfall entry** (title cards, segment openers): per-word `power4.out`, never `.inOut`; offsets 60-80 px for a hero line
  and 30-48 px for small text; per-word duration 0.10-0.20 s; gaps 0.05 s with 0.84 decay.
- **Nudge curve** (group slide with no cut): three phases of about 10 % / 65 % / 25 % of the time carrying about 20 % /
  18 % / 62 % of the distance: `power3.in`, linear, `power4.out`. A single `power4.inOut` is not a substitute.
- **Counters and progress:** numbers tween with tabular figures; progress bars and lines draw, they do not snap.
- **Path draw:** an SVG stroke with `pathLength=1` and `strokeDashoffset` from 1 to 0. Morph shapes by interpolating matching
  points of two polylines rather than swapping.

## 4. Entrances and easing

| Role | Duration | Ease |
|---|---|---|
| Card or UI element in | 0.26-0.38 s | `power3.out` or `expo.out` |
| Hero statement in (word cascade) | 0.8-0.9 s total | `power4.out` |
| Statement out | 0.5-0.6 s | in-out |
| UI state change | 0.4-0.7 s | `power3.inOut` |
| Camera leg | 1.2-2.0 s for a push, 3-6 s for a drift | `power3.inOut` / `sine.inOut` |
| Hairline or path draw | 0.5-0.9 s | `power2.inOut` |

House curves: **glide** = `cubic-bezier(0.22, 1, 0.36, 1)` for arrivals and settles; **smooth** = `cubic-bezier(0.45, 0, 0.15, 1)`
for exits, pushes and handoffs. Opacity plus a 10-28 px translate, never opacity alone. Use `fromTo` so a seek reproduces any
frame. `back.out` only for a cursor press recovering, a state confirmation, or one punctuation mark on a hero beat. Forbidden:
`bounce`, `elastic`, uncaused overshoot, springs with visible wobble.

Stagger: at most 6 items, 60 ms apart; total stagger under 500 ms. Similar elements share one ease and duration.

## 5. Carriers and causal motion

The eye follows objects, not abstractions. The strongest seams hand a concrete carrier across the cut at matched position and
velocity: a cursor mid-path, a card that shrinks and docks into the next layout, a mark that flies into its exact slot, a line
that becomes the graph. Chain motion so each move is launched by the last (click, press, release, flight, impact, recoil,
reveal) and start effects on the causing frame, not after it.

## 6. Camera

The camera lives on the product or the prop. Rotation and scale must live on separate nodes (outer dolly, inner turn),
otherwise they fight one transform matrix and the move judders. Put the zoom origin on the control being clicked or read.

| Move | Use | Spec |
|---|---|---|
| Drift | any beat over 2 s | 3-5 % scale or 20-60 px, eased, ends before the seam |
| Slow push-in | overview to the thing being read | 1.0 to 1.25-1.4, 1.5-2 s, origin on the target |
| Pull-back | detail to context, or to scale | reverse of push |
| Lateral | along a row of objects | 40-160 px, `smooth` |
| Hero | introducing the product surface | panel 3-6 degrees Y tilt settling flat |
| Depth reveal | a new scene arrives from behind | scale 0.92 to 1, blur 10 px to 0 |
| Macro | proving one fact | 1.6-2.4x on a region |
| Rack focus | depth emphasis | only in true 3D; blur on 3D children is applied per face so it never flattens them |

Never: whip pans, shake, aggressive zooms, constant movement on every beat.

## 7. Cursor

Draw it at least 44 x 54 px (a life-size pointer disappears into any saturated control), heavy stroke, deep shadow, inside the
node the camera moves. It enters from off-frame, takes a purposeful path, targets the tip not the centre, and clicks with an
0.08 s press (scale 0.86 and back). The click ignites the next beat on the same frame. It exits off-frame or hands off across
the seam. Without a cause, do not draw one.

## 8. Type in motion

- Statements 72-96 px at 1080 wide, weight 300, tracking -0.03 to -0.04 em, line-height 1.04-1.08, about 18 characters per
  line, 3 lines max, breaks written by hand.
- Support 0.38-0.42 x the hero; labels and UI text never under 16 px on screen (check after any camera push).
- No per-letter animation, no gradient text, no constant text motion. Text is still once it lands.
- Swapping two words (for example "Business to Software" becoming "Software to Business") crosses them on separate arcs
  with the arrow fading, so they never overprint.

## 9. Sound cues (when the film has audio)

Sparse and quiet. A continuous bed at most, a soft hit on the logo, a tick per list step, one glass sound when the product
arrives, nothing on every transition. A cue's volume cannot rescue a quiet source file: level the asset, then verify the cue
is audible in the delivered file. Narrated films: master to -14 LUFS plus or minus 0.5, true peak at or below -1 dBTP.

## 10. Banned

Idle sine loops, particles, light streaks, lens flares, glow, gradient text, rainbow rings, orbs, floating-card collages,
bounce, whip pans, per-letter text effects, stock photography, CSS imitations of real objects, cutting to black between
scenes, crossfading between scenes.
