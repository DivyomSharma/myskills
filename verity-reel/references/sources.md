# Sources: what was merged, archived and left alone

Taken 2026-10-09 when `verity-reel` replaced the earlier Verity video skills. The quality bar is the R09 reel; the
rules were rewritten from the defects the user rejected in R08 and R09, not inherited unchanged.

## Archived and merged in (restorable)

Archive: `~/.claude/skills-archive/` (global and project copies) and `D:\Code\myskills\_archive\` (repo mirrors). Each folder
is the untouched original. `~/.claude/skills-archive/README.md` has the restore commands.

| Archived skill | What `verity-reel` took |
|---|---|
| `verity-motion-director` | The pipeline, the engine decision, direction, shot plan with the vector ledger, motion law, Verity look, gates, the audit script, lessons (all carried as `references/` and `scripts/`). Its laws were rewritten: the "no frame unchanged over 1.0 s" law became "stillness" plus declared holds, because the accepted R08/R09 films measure 23 % and 42 % held text and every complaint was about wobble, overlap and layout |
| `verity-motion-design` | Verbatim as `references/film-art-direction.md` and `film-reference-analysis.md`: the 16:9 grid, anchors, type table, camera language, material, restraint, pre-render audit |
| `workflow-reel` | Folded into the pipeline table. Free-first rule (real UI in motion first) is law 9 |
| `reel-edit` | `references/talking-head.md` pipeline; `scripts/transcribe.py` |
| `reel-captions` | The caption behaviour in `references/talking-head.md` (the animated ads carry no captions) |
| `reel-style-aevytv` | Pace and structure notes in `references/talking-head.md`, minus its terracotta palette |

## New in this skill (from R08 and R09)

`references/build-recipe.md`, `references/audio.md`, `gates.md` §2b, the R08/R09 rows in `lessons.md`, and the scripts
`stills.mjs`, `contact-sheet.sh`, `region-stability.sh`, `find-drop.py`, `mix-bgm.sh`. Code: `video/src/ads/stage.tsx`,
`video/src/ads/R08/`, `video/src/ads/R09/`.

## Left alone on purpose

| Skill | Why it stays |
|---|---|
| `verity-social-design` | Static posts, carousels and ad stills; this skill routes to it |
| `promo-video`, `saas-vid`, `remotion-saas`, `remotion-best-practices` | Generic Remotion and promo foundations other skills call; `promo-video` is AI-voiceover based |
| `product-ui-motion`, `still-to-motion`, `ai-video-shotlist`, `hero-imagery`, `scroll-storyline`, `motion-kit`, `visual-budget-audit`, `motion-safety-qa` | Website motion and imagery; the global CLAUDE.md visual pipeline still routes site work to them |
| `captions-overlay`, `motion-doctrine`, `cut-the-curve`, `seam-craft`, `oversized-cursor`, HyperFrames skills | The HyperFrames engine's own skills |
| `promo-creator-skills` | Third-party Chinese promo pack, symlinked |
| `ad-creative`, `ads` | Paid-media copy and strategy, not video production |

## Keeping it fresh

Edit the project copy in `.claude/skills/verity-reel/` and the mirror in `D:\Code\myskills\verity-reel` together. When a
film is accepted, add what it taught to `lessons.md` and `build-recipe.md`, not to a new skill.
