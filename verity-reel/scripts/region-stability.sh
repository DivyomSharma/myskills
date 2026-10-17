#!/usr/bin/env bash
# region-stability.sh <video> <start_s> <duration_s> <w:h:x:y>
# Measures frame-to-frame pixel change inside one crop of the DELIVERED file. A region that should be dead still
# (settled text, a held card) must read ~0.00-0.05; a visible wobble reads 0.3 or more.
# Why it exists: "vibrating text" is invisible in stills and in the freeze audit. This is the proof that it is gone.
set -eu
f="${1:?video}"; ss="${2:?start}"; d="${3:?duration}"; crop="${4:?w:h:x:y}"
ffmpeg -hide_banner -ss "$ss" -t "$d" -i "$f" \
  -vf "crop=$crop,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG" -an -f null - 2>&1 |
  grep -o "YAVG=[0-9.e-]*" | cut -d= -f2 |
  awk -v s="$ss" '{ if (NR > 1 && $1 > m) m = $1; n++ } END { printf "t=%s frames=%d max_diff=%.4f  (settled text should be < 0.05)\n", s, n, m }'
