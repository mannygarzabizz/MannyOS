"""Take selection for the Naya reel (studio-mic master: camera picture + OBS voice, OFF=2.504 s).

Last take wins; boundaries scan OUTWARD from the Scribe word edge to the first quiet frame,
then re-pad from the measured speech edge so every sentence break is the same length.
"""
from pathlib import Path
import subprocess, json, math
import numpy as np

P = Path(__file__).resolve().parent
MASTER = str(P / 'edit/master.mkv')
SRC = {'a': MASTER}

# (start, end, beat) -- Scribe word times of the CHOSEN take on the master, before snapping
select = [
 (13.86, 16.92, 'hook'),      # Someone just released a free and open source version of JEV.   (3rd / last)
 (38.58, 40.26, 'faster'),    # And it's actually much faster.                                  (8th / last)
 (45.58, 46.78, 'possible'),  # How is that even possible?                                      (last)
 (51.36, 52.28, 'naya'),      # It's called Naya.                                               (last)
 (54.02, 57.58, 'local'),     # And it's a local system one model that you can run on your own computer.
 (66.62, 68.30, 'nocode'),    # Same as JEV, it cannot write code,   (take runs on into an aborted "but where JEV...")
 (100.16, 105.32, 'speed'),   # But where JEV takes around 250 milliseconds to respond, this model only takes 30 milliseconds. (last)
 (113.12, 116.48, 'cloud'),   # and that's because it's running local, so it doesn't have to go to the cloud and back,
 (116.92, 118.20, 'muchfast'),# which makes it much faster.           (same take; 0.44 s breath removed)
 (128.12, 130.78, 'problem'), # The only problem is that the base model isn't good at everything.  (last)
 (133.66, 136.52, 'tuned'),   # so it needs to be tuned and trained for specific use cases.        (last)
 (148.04, 149.50, 'claude'),  # But we can actually do that with Claude.                            (last)
 (155.82, 158.58, 'cta'),     # if you want the link to the model, just comment "FAST" and I'll send it to you. (last)
]
SPEED = {'hook': 1.12}
# 'nocode' ends inside running speech: "code," decays to -57 dBFS at 68.36-68.38 and "but" starts at 68.39.
# The end is pinned to that 30 ms trough and gets a longer fade-out instead of the outward scan.
FORCE_END = {'nocode': 68.383}
FADE_OUT = {'nocode': 0.014}

# ---- 10 ms RMS scan of the whole master (vectorised) ------------------------------------
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', MASTER, '-ac', '1', '-ar', '16000',
                      '-f', 's16le', '-'], capture_output=True).stdout
a = np.frombuffer(raw, dtype='<i2').astype(np.float32)
W = 160                                            # 10 ms @ 16 kHz
n = len(a) // W
rms = np.sqrt((a[:n * W].reshape(n, W) ** 2).mean(1))
DB = 20 * np.log10(np.maximum(rms, 1.0) / 32768.0)

def db(i):
    return float(DB[min(max(i, 0), len(DB) - 1)])

# Gates calibrated on the studio-mic master: inside a take the quietest 10 ms frame sits at
# -57..-73 dBFS, while the air between takes runs -70..-180 dBFS.  -58 separates them.
QUIET = -58.0
SPEECH = -58.0
PAD_IN, PAD_OUT = 0.30, 0.28
LEAD, TAIL = 0.07, 0.10

def edge(t, side, pad):
    """First frame at or below QUIET, scanning OUTWARD from the word boundary.
    Falls back to the quietest frame in the window when nothing clears QUIET."""
    c = int(round(t * 100)); w = int(round(pad * 100))
    idx = range(c, max(0, c - w) - 1, -1) if side < 0 else range(c, min(len(DB) - 1, c + w) + 1)
    idx = [i for i in idx if 0 <= i < len(DB)]
    for i in idx:
        if db(i) <= QUIET:
            return i / 100.0
    return min(idx, key=db) / 100.0

def speech_edges(a0, b0):
    """First and last frame above SPEECH inside the chosen window."""
    lo, hi = int(round(a0 * 100)), int(round(b0 * 100))
    live = [i for i in range(lo, min(hi, len(DB) - 1) + 1) if db(i) > SPEECH]
    return (live[0] / 100.0, live[-1] / 100.0) if live else (a0, b0)

ranges = []; report = []
for s, e, nm in select:
    a0 = edge(s, -1, PAD_IN); b0 = edge(e, +1, PAD_OUT)
    s0, e0 = speech_edges(a0, b0)
    a0 = max(a0, round(s0 - LEAD, 3))
    b0 = min(b0, round(e0 + (0.20 if nm == 'cta' else TAIL), 3))
    if nm in FORCE_END: b0 = FORCE_END[nm]
    if nm == 'cta': b0 = round(e0 + 0.22, 3)          # let the last word ring out; 158.61-158.85 is clean air
    report.append((nm, s, e, a0, b0, db(int(a0 * 100)), db(int(b0 * 100))))
    sp = SPEED.get(nm, 1)
    # hook keeps exact trough times (no 1/30 snapping) per the skill's hook pacing rule
    st = a0 if nm == 'hook' else math.floor(a0 * 30) / 30
    en = b0 if nm == 'hook' else math.ceil(b0 * 30) / 30
    if nm in FORCE_END: en = st + math.floor((b0 - st) * 30) / 30      # whole frames, never past the trough
    ranges.append({'src': 'a', 'start': round(st, 6), 'end': round(en, 6), '_': nm, 'speed': sp})

print(f"{'beat':10s} {'scribe':>15s}   {'snapped':>15s}   {'dB at joins':>14s}")
for nm, s, e, a0, b0, d1, d2 in report:
    print(f'{nm:10s} {s:7.2f}-{e:7.2f}   {a0:7.2f}-{b0:7.2f}   {d1:6.1f} {d2:6.1f}')
json.dump({'sources': SRC, 'ranges': ranges}, open(P / 'edit/edl.json', 'w'), indent=2)

(P / 'edit/segments').mkdir(exist_ok=True)
time = 0; beats = []
for i, r in enumerate(ranges):
    src_dur = round(r['end'] - r['start'], 8); sp = r['speed']
    dur = round(round(src_dur / sp * 30) / 30, 8)
    beats.append({'name': r['_'], 'start': round(time, 8), 'end': round(time + dur, 8)}); time += dur
    # atempo only where the take is actually retimed. Running atempo=1 on an unretimed take is not a
    # no-op: the WSOLA stretcher steps the audio 4-6 ms part-way through the segment (measured on the
    # v2 cut), which shifts sound against picture inside the take and breaks exact provenance checks.
    tempo = f"atempo={sp}," if sp != 1 else ""
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(r['start']), '-i', SRC[r['src']],
        '-t', str(src_dur),
        '-vf', f"setpts=(PTS-STARTPTS)/{sp},fps=30",
        '-af', f"{tempo}atrim=duration={dur},asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st={dur-FADE_OUT.get(r['_'],.004)}:d={FADE_OUT.get(r['_'],.004)}",
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '1',
        '-t', str(dur), str(P / f'edit/segments/{i:02d}.mkv')], check=True)
    print(f'  cut {i:02d} {r["_"]:10s} -> {dur:5.2f}s  (total {time:6.2f})', flush=True)
json.dump(beats, open(P / 'edit/beats.json', 'w'), indent=2)
(P / 'edit/concat.txt').write_text('\n'.join(f"file 'segments/{i:02d}.mkv'" for i in range(len(ranges))))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(P / 'edit/concat.txt'),
                '-c', 'copy', str(P / 'edit/tight.mkv')], check=True)
print('DURATION', round(time, 3))
