# Audio: voiceover timing and the music bed

## Voice leads, picture retimes to it

Never squeeze or stretch the voice to fit the animation. Record or receive the VO first, transcribe it for word timings
(`build-recipe.md` §1), and build every beat from those numbers. Gaps in the VO (0.4-0.8 s) are where a visual lands;
the word that names a thing is when the thing arrives.

## Music bed

Script: `scripts/mix-bgm.sh <video> <music> <out> <music_start_s> [level_db]`. The reel's own audio (the VO) is the
master; the music is a bed.

### Placement: sync the drop, not every beat

1. Find the drop and the beat grid: `uv run --with librosa --with soundfile python scripts/find-drop.py <music> <anchor_s>`
   where `<anchor_s>` is the film moment the groove should arrive on (R09: 20.9 s, when the Verity mark draws itself,
   the turn from problem to solution). It prints the `atrim=start=` value.
2. The track's quiet intro plays under the hook and pain beats; the full groove arrives with the solution. A 256 s track
   is trimmed to the film's length, not looped.
3. Only the drop is locked to a visual event. The VO phrases are fixed by the recording, so they will not sit on the beat
   grid; do not try to force them. Offset the drop by a whole beat if a better anchor exists.
4. Verify the placement by trimming the music stem with the same filter and checking the strongest onset lands on the
   anchor (R09: 20.9 s). Do this with a stem, not by ear.

### Level

- Bed at about -23 dB gain on a hot track (the R09 music measured -9.6 LUFS and +5.6 dBTP raw), about 12 dB under the VO.
- Sidechain duck keyed by the VO: threshold 0.015, ratio 5, attack 15 ms, release 450 ms. The bed breathes up in gaps.
- EQ cut of 3 dB at 2 kHz leaves the speech band to the voice. Fade in 2 s, fade out 2.6 s.
- `amix normalize=0` and `alimiter level=0`. The default `alimiter` auto-levelling raised the voice by about 1 dB on the
  first R09 mix; a "subtle bed" that changes the voice is not subtle.

### Verify

The integrated loudness and true peak of the mix must equal the voice-only file (R09: -20.8 LUFS, -3.9 dBTP). The script
prints both. If the mix is louder, the bed is too loud or the limiter is levelling.

## Loudness target honesty

The ad rules ask for about -14 LUFS integrated, true peak at or below -1 dBTP. The R09 voice file is -20.8 LUFS, so the
delivered mix is quiet against that target. This is the VO's level, left untouched on purpose. Say so in the report and
offer a gain lift (`loudnorm=I=-14:TP=-1.5:LRA=11` on the whole mix) rather than doing it silently.

## What was not verified

Nobody can listen from the terminal. Every audio claim above is measured (loudness, onset position, level difference),
not heard. State that in the delivery note.
