"""Word-level transcript for a talking-head clip.

Usage: python transcribe.py <video_or_audio> [out.json] [model]
Output: [{"text": "word", "start": 0.12, "end": 0.40}, ...]  (seconds)
Model default "small" (CPU ok). Use "large-v3" if a GPU is available.
"""
import json
import sys

from faster_whisper import WhisperModel

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else src.rsplit(".", 1)[0] + ".words.json"
model_name = sys.argv[3] if len(sys.argv) > 3 else "small"

model = WhisperModel(model_name, compute_type="int8")
segments, _ = model.transcribe(src, word_timestamps=True, vad_filter=True)
words = [
    {"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
    for s in segments
    for w in s.words
]
with open(out, "w", encoding="utf-8") as f:
    json.dump(words, f, ensure_ascii=False, indent=1)
print(f"{len(words)} words -> {out}")
