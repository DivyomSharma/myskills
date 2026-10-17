#!/usr/bin/env bash
# audit-render.sh <video.mp4> [outdir]
# Measured motion audit of a delivered video: stuck holds, hard jumps, loudness and a contact sheet.
# Needs ffmpeg and ffprobe on PATH. Writes <outdir>/sheet.jpg and prints a report.
set -u
f="${1:?usage: audit-render.sh <video> [outdir]}"
[ -f "$f" ] || { echo "no such file: $f" >&2; exit 2; }
name="$(basename "${f%.*}")"
out="${2:-$(dirname "$f")/audit-$name}"
mkdir -p "$out"

dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
dim=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$f")
echo "file      $f"
echo "video     $dim"
echo "duration  ${dur}s"

echo
echo "== HOLDS  (frame unchanged for >= 0.6 s). Each must be a hold declared in the shot plan."
holds=$(ffmpeg -v info -i "$f" -vf "freezedetect=n=0.0008:d=0.6" -map 0:v -f null - 2>&1 |
  grep -oE "freeze_(start|duration): [0-9.]+" | paste - - | awk '{printf "%s %s\n", $2, $4}')
if [ -z "$holds" ]; then
  echo "  none"
  frozen=0
else
  echo "$holds" | awk '{printf "  %7.2fs  for %.2fs%s\n", $1, $2, ($2>1.0 ? "   <-- over 1.0 s" : "")}'
  frozen=$(echo "$holds" | awk '{s+=$2} END {printf "%.2f", s}')
fi
awk -v z="$frozen" -v d="$dur" 'BEGIN {printf "  total frozen %.1fs of %.1fs = %.0f%% (target: under 10%%)\n", z, d, 100*z/d}'

echo
echo "== JUMPS  (scene change > 0.18). Each must be a declared hard cut."
jumps=$(ffmpeg -v info -i "$f" -vf "select='gt(scene,0.18)',showinfo" -an -f null - 2>&1 | grep -oE "pts_time:[0-9.]+" | cut -d: -f2)
if [ -z "$jumps" ]; then
  echo "  none"
else
  echo "$jumps" | awk '{printf "  %7.2fs\n", $1}'
fi

if ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of csv=p=0 "$f" | grep -q audio; then
  echo
  echo "== LOUDNESS  (narrated target: -14 LUFS +/- 0.5, true peak <= -1 dBTP; ambient SFX-only films are quieter by design)"
  ffmpeg -nostats -i "$f" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2 | sed 's/^/  /'
fi

echo
echo "== CONTACT SHEET"
ffmpeg -v error -y -i "$f" -vf "fps=20/${dur},scale=360:-1,tile=5x4:padding=4:color=gray" -frames:v 1 "$out/sheet.jpg" &&
  echo "  $out/sheet.jpg  (read it for missing content; judge scale and legibility from full-size frames)"
echo
echo "Next: sample frames at every changed beat and at each seam +/- 0.1 s, view them full size, write the defect list."
