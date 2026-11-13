"""Cuts filler phrases from the tightened VO and speeds it up (pitch kept) to fit under 60 s.
Writes assets/vo/voiceover-short.wav and assets/vo/vo-map.json (old VO time -> new VO time breakpoints)."""
import json, subprocess
TEMPO = 1.12
REMOVE = [  # word sequences removed from the VO
    "projek perumahan baru ini menawarkan",
    "Apa yang menarik,",
    "Memang sesuai untuk keluarga yang mahukan ruang lebih selesa.",
    "Dari segi lokasi pula,",
    "Lagi menarik,",
    "Kalau berminat nak tahu lebih lanjut atau",
]
d = json.load(open("assets/vo/voiceover-tight.words.json")); words = d["words"]; dur = d["duration"]
norm = lambda w: w.lower().strip(".,")
toks = [norm(w["w"]) for w in words]
# word timestamps are only roughly right at boundaries, so cut at the quietest 10 ms frame
# in the gap between the kept word and the removed one (and again at the far end).
import numpy as np
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "assets/vo/voiceover-tight.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
pcm = np.frombuffer(raw, dtype=np.float32)
rms = np.sqrt(np.convolve(pcm ** 2, np.ones(160) / 160, mode="same"))
def quietest(t0, t1):
    i0, i1 = int(max(0, t0) * 16000), int(t1 * 16000)
    return (i0 + int(np.argmin(rms[i0:i1]))) / 16000 if i1 > i0 else t0
cuts = []
for ph in REMOVE:
    seq = [norm(x) for x in ph.split()]
    i = next(i for i in range(len(toks)) if toks[i:i + len(seq)] == seq)
    j = i + len(seq)
    a = quietest(words[i - 1]["e"] - 0.08, words[i]["s"] + 0.12)
    b = quietest(words[j - 1]["e"] - 0.08, words[j]["s"] - 0.02) if j < len(words) else dur
    cuts.append((round(a, 3), round(b, 3)))
    print(f"cut {a:6.2f}-{b:6.2f}  {ph}")
cuts.sort()
keep, t = [], 0.0
for a, b in cuts:
    keep.append((t, a)); t = b
keep.append((t, dur))
fc = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={b - a - 0.012:.3f}:d=0.012[p{i}];" for i, (a, b) in enumerate(keep))
fc += "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,atempo={TEMPO}[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/vo/voiceover-tight.wav", "-filter_complex", fc, "-map", "[o]", "-ar", "44100", "assets/vo/voiceover-short.wav"], check=True)
bp, n = [], 0.0   # breakpoints: (old, new) at each kept segment edge; cut spans collapse to a point
for a, b in keep:
    bp += [[round(a, 3), round(n / TEMPO, 3)], [round(b, 3), round((n + b - a) / TEMPO, 3)]]
    n += b - a
json.dump({"tempo": TEMPO, "breakpoints": bp, "new_duration": round(n / TEMPO, 3)}, open("assets/vo/vo-map.json", "w"), indent=0)
print("new VO", round(n / TEMPO, 2), "s")
