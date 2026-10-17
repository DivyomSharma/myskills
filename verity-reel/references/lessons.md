
## From the Meta ad films R08 and R09 (2026-10-08)

| What went wrong | Cause | Fix, and where it lives |
|---|---|---|
| Phone "vibrated" and the user called it awful | Per-frame sine shake at ~14 Hz aliases against 30 fps | One damped 3 Hz sway per event (`build-recipe.md` §5) |
| Diagram labels (Orders, Accounts...) kept moving after they landed | Whole-scene scale 1.0 to 1.07 resampled all text; depth reveal (scale + blur) on text sheets; `outX` sub-pixel tail | No whole-scene zoom over text, fade-and-rise sheets, `glide` ease, integer `translateY`; verify with `region-stability.sh` |
| "YOU" node text pulsed | Animated `fontSize` and radius | Animate one group `scale()` |
| Hinglish on screen and a subtitle layer | Copied the VO language into the visuals | English-only on-screen text, no subtitles unless the brief asks |
| Text overlapping the phone, a headline under a caption, a grey ghost of a sheet | Next layer started before the previous was gone; object too big for the text column | Ghost-overlap sweep at transitions; shrink or move the object; hide the caption when a headline says the words |
| IIT and IIM white plates looked like keyboard keys | Frosted-acrylic plates for plain type | Large thin type between hairline rules |
| Dark background requested after a light film | Theme left open in the brief | Dark world, light objects is the ad style now; theme is still a brief input |
| Every render failed with "Duplicate identifier" | Two imports of `FILM_DURATION` in `Root.tsx` from unrelated films | Alias on import; run `tsc --noEmit` first |
| Whisper printed the prompt back as the transcript; Devanagari crashed the shell | `initial_prompt` echo; Windows codepage | No prompt; `PYTHONIOENCODING=utf8` |
| First BGM mix raised the voice by about 1 dB | `alimiter` auto-level on by default | `alimiter level=0`, `amix normalize=0`; compare VO-only and mix loudness |
| A shell one-liner that edited the TSX broke on quotes and `$'` replacement patterns | Inline `node -e` with apostrophes | Write the patch to a temp `.cjs` file; use `split/join` or a function replacement |

## From R10 (landscape, 2026-10-10)

| What went wrong | Cause | Fix, and where it lives |
|---|---|---|
| Stray blue arcs appeared before the cards they led to | `strokeDasharray` shorter than the path: the dash pattern repeats, so the tail shows when the offset hides only the first dash | Dash length must be at least the path length; hide a zero-progress path with `opacity 0` (round caps also leave a dot at zero) |
| Every render failed with a JSON error after a scripted edit | PowerShell `Set-Content -Encoding UTF8` writes a BOM; `package.json` and the skill frontmatter then fail to parse | Write with `[System.IO.File]::WriteAllText(path, text, New-Object System.Text.UTF8Encoding($false))`, or check and strip the 3-byte BOM after any scripted edit |
| A grey slab showed when the end card arrived | The closing sheet's fade overlapped the end card | Sheets and headlines finish leaving at least 0.2 s before the next layer lands |
| Landscape reuse of portrait components | R07 to R09 parts are sized for 1080 wide | Landscape grid: text x 120 to 840, product zone x 880 to 1800, cap line y 250, objects 920 wide; see `video/src/ads/R10/parts.tsx` |
## From the industry series (2026-10-12)

| What went wrong | Cause | Fix, and where it lives |
|---|---|---|
| The recording's closing "Limited time offer." was missing from the transcript, and a 6 s offer section was missing from another | Whisper drops speech after pauses and at the file end | Check for audible sound after the last transcribed word (`volumedetect` on the tail), then re-transcribe just that stretch |
| The music drop check reported a hit 2 s late | A wide search window picks the strongest onset, not the drop | Check a narrow window (+/- 0.8 s) around the intended moment |
| A shared tail built on fixed offsets drifted from the real recordings | Each recording's pauses differ | Anchor every tail beat to that recording's own word times (`Anchors` in `video/src/ads/series/engine.tsx`) |
| Dim ghost of the last cards under the end card | Layers exited as the end card faded in | Finish the last layers leaving at least 0.4 s before the end card starts |