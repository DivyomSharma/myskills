#!/usr/bin/env bash
# contact-sheet.sh <out.png> <img1> <img2> ...   Tile 9:16 stills into a sheet, 6 per row, 300 px wide each.
# Read the sheet for content and overlaps; judge scale from full-size frames.
set -eu
out="$1"; shift
args=(); fc=""; lay=""; i=0
for f in "$@"; do
  args+=(-i "$f"); fc+="[$i]scale=300:-1[s$i];"
  lay+="${lay:+|}$(( (i % 6) * 300 ))_$(( (i / 6) * 533 ))"; i=$((i + 1))
done
ins=""; for k in $(seq 0 $((i - 1))); do ins+="[s$k]"; done
ffmpeg -y -loglevel error "${args[@]}" -filter_complex "${fc}${ins}xstack=inputs=$i:layout=${lay}" "$out"
