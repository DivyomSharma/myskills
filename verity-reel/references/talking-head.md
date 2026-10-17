# Variant: a reel built from talking-head footage

Carried over from the archived `reel-edit`, `reel-captions` and `reel-style-aevytv` skills. Use this only when the reel
starts from real footage of a person; an animation-only ad (R08, R09) never needs it. Everything else in this skill
(truth, stability, audit, music) still applies.

## Pipeline

1. **Ingest.** Raw clip in `public/raw/`. Probe, then normalise to 1080x1920 at a constant 30 fps:
   `ffmpeg -i in.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" -c:v libx264 -crf 16 -c:a aac -ar 48000 public/raw/clip.mp4`
2. **Tighten.** Remove dead air before anything else:
   `auto-editor public/raw/clip.mp4 --edit audio:threshold=0.04 --margin 0.12sec -o public/raw/clip.tight.mp4`
   Review it; back off `threshold` if speech clips.
3. **Transcribe** the tightened file: `uv run --with faster-whisper python scripts/transcribe.py clip.tight.mp4 src/data/words.json medium`.
   Fix names and brand terms by hand. This file drives captions and b-roll timing. (Script output is `[{text,start,end}]`.)
4. **Cut plan** in `src/data/plan.json`: ordered beats `{start, end, kind: talk|broll|card|title, comp?, punch?}`.
   A new visual every 2-4 s; a b-roll beat opens on the word that names the thing; never cover a punchline; open with a
   1-2 s hook and the first spoken word before 0.5 s.
5. **Build b-roll** as one Remotion composition per beat (doc highlight, numbered card, UI mockup, kinetic type). One idea
   per composition, designed when paused. Real Verity UI, light objects (`Light`) as in `build-recipe.md`.
6. **Assemble** in one master composition: `<Sequence from>` per beat, the talking head as `<OffthreadVideo startFrom
   endBefore>` of the tightened clip, voice playing continuously under b-roll (never restart audio per beat).
7. **Punch-ins.** On talk beats alternate scale 1.0 and 1.08-1.12 with a hard cut, no easing, so one camera reads as two.
   Keep faces above the caption zone.
8. **Audio.** Voice is master; music per `audio.md`. SFX only on b-roll entries.
9. **QA and finish.** Stills at each cut for safe zones and caption collisions; `audit-render.sh`; colour and final
   loudness in DaVinci Resolve (human step) if the `resolve` MCP is available.

## Captions (only for footage reels, or when the brief asks)

The animated Meta ads carry no captions. For footage reels:

- One to three words at a time, centred, about 62-70 % down the frame. Small bold sans, white on a dark rounded pill
  (about 60 % black), not full width.
- A word appears at its `start` and leaves at the next word's `start` (no gaps, no overlaps); sentence ends clear the screen.
- At most one accent-coloured keyword per caption. Hide captions where a beat's own on-screen text would collide.
- Safe zone: 120 px from the bottom, 60 px from the sides. Prefer `@remotion/captions` `createTikTokStyleCaptions` for
  pages and highlighting. Check five random cuts: the caption equals the speech at that frame, never covers the mouth,
  never wraps to three lines.
- If the HyperFrames embedded-captions workflow is the engine instead, its overlay model (`captions-overlay`) owns this.

## Pace and structure (the AevyTV reference)

Hook 0-3 s as a bold graphic, then talking head about 60 % of the runtime with hard cuts every 2-4 s; source-proof cutaways
(a real doc screenshot with the key phrase highlighted, speaker as a small inset below); one numbered card per tip, 2-3 s;
close on the face with a direct CTA. Palette and type come from Verity's tokens, not the reference's terracotta. Do not use
stock footage, emoji spam, a second accent colour, or transitions between talking-head cuts. Budget: about 60 % real
footage, 30 % real-UI motion graphics, 10 % brand stings.
