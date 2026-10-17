# Build recipe: the R09 reel, step by step

R09 ("WhatsApp is not the problem", `video/src/ads/R09/`, render `video/renders/ads/R09/verity-meta-R09-9x16-v1-bgm.mp4`)
is the accepted quality bar for a Verity Meta ad. R08 (`video/src/ads/R08/`) is the sibling that taught most of the
rules. This file is how to make the next one the same way. Commands run from `video/` unless noted.

## 0. Inputs

- A script with beats and a recorded voiceover (mp3/wav). Nothing is timed until the VO exists.
- `video/ads/00-strategy/*` for approved claims, offer wording and brand rules. If a claim is not in
  `offer-and-claims.md` it is not approved.
- The VO may be Hinglish. **On-screen text is English only and there are no subtitles** unless the brief says otherwise
  (the user rejected Roman-Hinglish captions and a caption layer on this film).

## 1. Word timings from the voiceover

```bash
cp "<vo>.mp3" public/ads/<ID>/vo.mp3
PYTHONIOENCODING=utf8 uv run --with faster-whisper python <skill>/scripts/transcribe.py public/ads/<ID>/vo.mp3 words.json medium
```

- Whisper returns Devanagari for Hinglish and mis-hears loanwords. Use the timestamps, ignore the spelling. Do not pass an
  `initial_prompt`: it gets echoed back as the transcript.
- On Windows set `PYTHONIOENCODING=utf8` or the Devanagari print crashes the run.
- Write the anchors you will use as one `const V = {...}` object (seconds) at the top of `Film.tsx`. Every beat reads
  from `V`, so a re-recorded VO is a one-place retime.

## 2. Stage, theme, tokens

`video/src/ads/stage.tsx` is the shared stage for dark-world ads:

| Export | Use |
|---|---|
| `DarkStudio` | The room: near-black wall and floor, one faint light shaft, dark tokens on the root |
| `Light` | Re-scopes the light tokens for any physical object (phone, paper, cards, sheets, workspace) |
| `Layer` | One information layer: rises in at `a`, out at `b`, `light` prop wraps children in `Light` |
| `glide`, `tk`, `lin`, `LABEL` | The settle ease, eased and linear tracks, the uppercase micro-label style |

**Dark world, light objects.** Headlines, the offer and the end card are text on the dark room (ink = near-white).
Everything you could touch is a light object lit against it. Put objects inside `<Light>` or `<Layer light>`; never put
`color: #fff` on dark text by hand, use `var(--ink)`.

Shared props live in `video/src/ads/R08/props.tsx` (`Phone`, `Artifact` card, `BigLockup`, `Person`, `PHONE`) and the
R09-specific ones in `video/src/ads/R09/props.tsx` (chat list and thread screens, the four tool cards, `Glyph`).

## 3. Beat map (R09, 51 s)

| Time | Beat | Device |
|---|---|---|
| 0-5 | Hook: "Quick question? / Still running your business on WhatsApp?" | Small phone, chat list fills with unread rows |
| 5-11 | Pain | Camera pushes the phone to fill the frame; thread stacks "Sir, ..." messages with attachments; 99+ badge |
| 11-15 | Montage then freeze | Five fast cuts (chat, sheet, call log, notebook, chat), then hold on "Business system?" with a drawn cross |
| 15-21 | Reframe: "WhatsApp isn't the problem." | Scattered fragments morph into an ordered list (Orders, Customers, Payments, Approvals, Reporting) |
| 21-31 | Verity | Mark draws itself on a hard cut; four mapped cards around "Your business"; Business > Understanding > System chips; workspace builds module by module |
| 31-36 | Offer | Limited-time tag, giant ₹5,000, accent bar sweeps through it, FREE revealed by a clip-path wipe. Cleanest frame in the ad |
| 36-47 | Credibility and payoff | Analysis sheet traced with callouts ("IIT & IIM selected professionals"), then three Blueprint step cards ticking |
| 47-51 | End card | Lockup, line, struck ₹5,000 + FREE, one button, URL |

The arc is: relatable pain, reframe (the problem is the missing system, not the tool), Verity understands first and builds
around it, free offer, proof, one action. The offer frame is the cleanest in the film by design.

## 4. Pass the art-direction gate before the full render

1. `npx tsc --noEmit` after every structural edit (a stale import in `Root.tsx` blocks every render).
2. Render a stills sweep through one bundle, 20-25 times across the whole film, including +/- 0.2 s around every
   transition, then tile and read it:

```bash
node <skill>/scripts/stills.mjs Ad-R09-WhatsApp-9x16 0.9,3.5,5.5,... out/r09a
bash <skill>/scripts/contact-sheet.sh out/r09a/A.png out/r09a/t0_9.png out/r09a/t3_5.png ...
```

3. Score each keyframe 1-10 (composition, type, depth, material, brand, product integration, originality). Under 8 is
   rebuilt before animating further. R09 took three passes. Typical first-pass failures: object too small to be the
   environment, text colliding with the object, two headlines visible at once, a grey ghost of a fading sheet.
4. Look for **ghost overlaps** at transitions: the outgoing layer must be gone before the next lands at the same spot.

## 5. Motion rules that fixed "vibrating"

These came from real defects the user saw; the measurement for each is in `gates.md` §2b.

| Defect | Cause | Rule |
|---|---|---|
| Phone shaking randomly | A per-frame `sin(frame * k)` shake at ~14 Hz aliases against 30 fps | One damped sway per event: `amp * exp(-dt*4.5) * sin(dt*19)`, 3 Hz, 1.2 s tail |
| Diagram labels swimming | Whole-scene `scale(1.0 -> 1.07)` resamples every text layer each frame | **No whole-scene zoom over text.** Move the camera by moving objects, not a transform on the text parent |
| Labels swimming on entry | Depth reveal (scale 0.95 -> 1 plus blur) on text-heavy sheets | Depth reveal only for objects without small text; sheets fade and rise |
| Text creeping for a second | `outX` (0.16,1,0.3,1) has a very long tail of sub-pixel movement | Settle with `glide` bezier(0.22,1,0.36,1), under 0.9 s, and `Math.round` every `translateY` |
| "YOU" node text pulsing | Animating `fontSize` and `r` each frame | Animate one `scale()` on a group; never animate font size |
| Idle ripples on a held node | Looping ambient animation | Banned; hold means hold |

Also: do not slow-zoom the offer or end card. A 2% drift there measured as visible wobble on the big numerals.

## 6. Render, audit, then music

```bash
npm run render:ad-r09                      # master with VO, crf 16
bash <skill>/scripts/audit-render.sh renders/ads/R09/<file>.mp4
bash <skill>/scripts/region-stability.sh <file> 49.6 0.9 900:700:90:420   # offer/end-card text must read < 0.05
```

Then the BGM (`audio.md`). Deliver the music version as a separate file next to the master; never overwrite.

## 7. Registering a new ad

1. Folder `video/src/ads/R<NN>/` with `Film.tsx` and `props.tsx`; the VO copied to `video/public/ads/R<NN>/vo.mp3`.
2. `Root.tsx`: import the film and add one `<Composition id="Ad-R<NN>-<Name>-9x16" ... width={ADW} height={ADH} />`
   (`ADW`/`ADH`/`ADFPS` come from `src/ads/tokens.ts`).
3. `package.json`: a `render:ad-r<nn>` script with `--crf=16`.
4. If `Root.tsx` already imports a name (for example `FILM_DURATION`) alias the new one; duplicate identifiers block
   every render, not just the new one.
