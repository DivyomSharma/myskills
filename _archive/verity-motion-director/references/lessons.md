# Lessons from our own builds

Each row is a failure we shipped or nearly shipped, with its cause and the rule that now prevents it. Read this before
debugging a film, and before agreeing to a brief that repeats one of them.

| What went wrong | Cause | Fix, and where it lives |
|---|---|---|
| About a third of a 73 s film was frozen (18 flagged holds, 24 s) | Each animation finished and then nothing happened until the next one started | Law 7, hold budget and routes (`shot-plan.md` §3-4), `audit-render.sh` |
| Text and labels snapped between states (QUOTATION to QUOTAT...), nodes dimmed instantly, a status pill changed in one frame | State changed by swapping content, not animating it | Law 8; cross-stack, mask or tween |
| A hard cut to black between scenes | The scene ended and the next began with no carrier | Law 5 and ledger; carrier crosses every seam |
| 16 scenes in 73 s; no idea got more than about 4 s | The brief listed 30 sections and each became a scene | Law 2 and the beat budget (`direction.md` §7) |
| Faked photoreal desk, laptop, paper, handwriting and stamp looked like "AI slop" | CSS imitating photography | Law 9; draw honestly or use real UI |
| Theme and direction flipped four times (light, dark, light, dark) | Each new brief re-decided the look | Law 15 and intake (`direction.md` §1); lock the look first |
| The film felt generic next to the main trailer | The film reinvented its look; the trailer uses the site's own system | Law 1 and `verity-look.md`; start from the site tokens and real UI |
| Dashboards and graphs of tiny labels | 13-15 px micro text in a 1080 frame | Law 11; 16 px floor, UI text 20 px on canvas |
| Words overprinted mid-swap | Two words crossing on the same line | `motion-law.md` §8; separate arcs, fade the arrow |
| A stage crossfade-blurred layer hid parts of a scene | Z-order was not planned; cards sat under the suite | Declare layers in keyframes; check the snapshot at each beat |
| A render passed lint and looked fine in stills but dragged | Judged from stills, never audited the motion | Law 16; audit the delivered file |
| A third-party plugin claimed the HyperFrames compose tool was usable | The compose and render tools are disabled from CLI agents | `engine-decision.md`; use the local skills and `npx hyperframes` |
| A deleted component left a stale import and a TypeScript error | Removed files without updating `Root.tsx` | Run `npx tsc --noEmit` after every structural edit |
| Reviewed the audit then kept polishing | No stop rule | Law 16 and the director loop: at most one more round |
| A script's header said 40-50 s but its timestamps ran to 1:13 | Inconsistent source | Follow the timestamps and say so in the brief |
| A scene's blurred 3D child flattened its 3D | CSS blur on a 3D container | Apply blur per face, not to the container (`motion-law.md` §6) |
| The locked outro copy conflicted with the script's own outro | Two sources of truth | Flag the deviation in the brief and the report (`verity-look.md` §6) |

## HyperFrames-specific

- Layout properties (`left`, `top`) in tweens are rejected; use transforms.
- A tween on an element that is also a carrier must not set the same property from CSS.
- Overlapping tweens on one property warn; leave a 0.01 s gap rather than butt-joining.
- `snapshot` writes contact sheets, but judge scale from full-size PNGs.
- Pass `-f 60 -q delivery` for a final render; check the render summary line for capture mode.

## Remotion-specific

- Keep scene components pure functions of the frame so the same scene can also run in a `<Player>`.
- Register compositions in `src/Root.tsx`; removing a file requires removing its import and composition.
- Use `track` and `seg` helpers rather than hand-writing interpolation chains; sample polylines per frame for morphs.
