"""find-drop.py <music.mp3> <anchor_seconds_in_video> [search_from] [search_to]

Finds the strongest onset (the drop) in the music between search_from and search_to (default 15-40 s of the track),
snaps it to the nearest detected beat, and prints the trim offset so that drop lands on <anchor_seconds_in_video>.
Use the printed `atrim=start=` value in mix-bgm.sh. Needs: uv run --with librosa --with soundfile python find-drop.py ...
"""
import sys

import librosa
import numpy as np

music, anchor = sys.argv[1], float(sys.argv[2])
lo = float(sys.argv[3]) if len(sys.argv) > 3 else 15.0
hi = float(sys.argv[4]) if len(sys.argv) > 4 else 40.0
y, sr = librosa.load(music, sr=22050, duration=hi + 15)
hop = 256
env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
t = librosa.times_like(env, sr=sr, hop_length=hop)
m = (t > lo) & (t < hi)
drop = t[m][np.argmax(env[m])]
tempo, beats = librosa.beat.beat_track(onset_envelope=env, sr=sr, hop_length=hop, start_bpm=118)
bt = librosa.frames_to_time(beats, sr=sr, hop_length=hop)
near = bt[np.argmin(abs(bt - drop))]
print(f"tempo ~{float(np.atleast_1d(tempo)[0]):.1f} BPM, beat every {60 / float(np.atleast_1d(tempo)[0]):.2f}s")
print(f"drop in track at {drop:.2f}s, nearest beat {near:.2f}s")
print(f"trim start for the drop to land at video t={anchor}: {near - anchor:.2f}  (atrim=start={near - anchor:.2f})")
