# Sources: what was merged, what was left out

Inventory taken 2026-10-07 of every motion-related skill on this machine plus open-source candidates.

## Merged

| Source | Origin | What this skill took |
|---|---|---|
| `motion-doctrine` | HyperFrames repo (installed to `~/.claude/skills`) | Vector law, the current, reserved vectors, carriers, causal motion, no idle wobble, stillness before climax, the ledger and the seam gate (scripts kept in place) |
| `cut-the-curve` | HyperFrames repo | The five seams with parameters, partial travel, mirrored eases, blur scale, waterfall entry, nudge curve |
| `seam-craft`, `oversized-cursor` | HyperFrames repo | White-flash guard and render mechanics (use when authoring in HyperFrames), cursor spec |
| `hyperframes`, `-core`, `-animation`, `-creative`, `-keyframes`, `-audio`, `-cli` | HyperFrames plugin v0.8.138 | The engine contract and CLI gates, beat direction, story spine, house style, runtime adapters |
| `motion-graphics`, `product-launch-video`, `general-video` | HyperFrames plugin | Workflow routing for short units and product films (use when the HyperFrames workflow is the better owner) |
| `product-launch-motion` | github.com/AbubakrChan/product-launch-motion (MIT, 73 stars) | Ten laws, three directions and kill two, direction dials, signature move, word-locked sync, delivered-file verification, the director loop, the traps catalogue |
| `verity-motion-design` | our repo | Verity composition grid, type table, material, camera language, arc, restraint, the pre-render audit |
| `verity-social-design` | our repo | Aspect grids, type for 1080-wide frames, anchors |
| `saas-vid`, `remotion-saas`, `remotion-best-practices` | our skills | Remotion structure, one scene set for several aspects, reel safe zones |
| `product-ui-motion`, `still-to-motion`, `visual-budget-audit`, `motion-safety-qa` | our skills | Real-UI-first rule, honest stills, slop flags, reduced-motion and contrast QA for embedded web video |
| Our own failures | this repo's history | `lessons.md` |

## Not merged (and why)

| Skill | Reason |
|---|---|
| `promo-video` | Built on AI voiceover and AI video generation, which our brief excludes |
| `apple-design`, `emil-design-eng`, `liquid-glass`, `animate`, `improve-animations` | Web UI interaction craft, not film direction. Still the right tools for site motion |
| `ai-video-shotlist`, `hero-imagery`, `scroll-storyline`, `motion-kit` | Website motion and AI-video prompting; outside the video pipeline |
| `reel-edit`, `reel-captions`, `reel-style-aevytv` | Talking-head reels; use for footage-based edits |
| `registry/blocks/*` | HyperFrames components, installed with the CLI when needed |
| `bykaranmrn/hyperframes-motion-graphics`, `bykaranmrn/claude-motion-director` | Do not exist on GitHub under those names |
| `abdullatif06/claude-motion-director` (3 stars), `Sibhimanyu/rasanai`, `Hosseinamiri850/motion-graphics-skill` | Found by search; not vetted, small or unmaintained; not installed |

## Vetting note

`product-launch-motion` was cloned and read before use: MIT licensed; the only scripts that execute (`assemble.mjs`,
`level-sfx.mjs`) call local `ffmpeg` and `ffprobe` through `spawnSync`; no network, no credentials. Its ideas are paraphrased
here, not copied, with credit to Abubakr Chan. The HyperFrames skills are the upstream `heygen-com/hyperframes` repo, installed
with `claude plugin install hyperframes@hyperframes`.

## Keeping it fresh

When a source updates, re-read its changed sections and revise the matching file here; the engine rules and CLI flags change
fastest. Record the date and version in this file. The canonical copy lives at `D:\Code\myskills\verity-motion-director`; the
project copy in `.claude/skills/` is the one sessions load. Edit both together.
