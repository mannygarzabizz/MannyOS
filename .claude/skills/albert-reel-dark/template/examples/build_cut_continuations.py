"""Take selection for the "AI killed software" reel (studio-mic master: camera picture + OBS voice, OFF=1.106 s).

Last take wins; boundaries scan OUTWARD from the Scribe word edge to the first quiet frame,
then re-pad from the measured speech edge so every sentence break is the same length.
A range whose name ends in '+' is the continuation of the previous beat (same take, a pause tightened
between them): it becomes a separate segment but is MERGED into the previous beat in beats.json.
"""
from pathlib import Path
import subprocess, json, math
import numpy as np

P = Path(__file__).resolve().parent
MASTER = str(P / 'edit/master.mkv')
SRC = {'a': MASTER}

# (start, end, beat) -- Scribe word times of the CHOSEN take on the master, before snapping
select = [
 (13.92, 15.84, 'hook'),       # AI just killed all software.                        (4th / last; takes 2-4 drop "forever")
 (31.14, 34.48, 'worry'),      # But don't worry because the money was never in software to begin with.  (last)
 (42.36, 44.44, 'hidden'),     # It's actually hidden somewhere else in plain sight.  (last)
 (48.36, 53.84, 'spend'),      # US companies are right now spending around $750 billion every year in software.  (one take; the 52.04-52.60 "pause" is voiced on the RMS profile, kept)
 (56.28, 58.34, 'alot'),       # A lot, but not compared to this.
 (69.54, 75.24, 'six'),        # Because the same companies are spending six times more, $4.6 trillion in services   (last; beat is split at "in" -> 'services' by fix_words.py)
 (78.30, 79.96, 'six+'),       #   every single year.                 (re-said ending 3 s later, spliced on; lands in 'services' after the split)
 (85.10, 87.82, 'jobs'),       # Accountants, lawyers, brokers, agencies.
 (90.88, 91.82, 'why'),        # And why is that?                     (last)
 (102.60, 105.96, 'tool'),     # Well, companies never wanted a software tool to help with accounting.  (last)
 (112.56, 114.92, 'done'),     # what they really want is accounting done for them.  (last)
 (121.74, 124.70, 'humans'),   # And up until now, this needed a lot of humans, but
 (125.18, 125.74, 'humans+'),  #   not anymore.                       (same take, 0.48 s pause tightened)
 (134.30, 137.60, 'next'),     # The next billion-dollar companies won't be AI software companies.  (last)
 (142.52, 146.24, 'service'),  # It will be AI software companies acting as service companies.  (last)
 (149.32, 152.72, 'skills'),   # Which is why you need to learn how to take your skills that you know
 (159.16, 161.64, 'turn'),     # and turn that into an AI-native service business.  (last)
 (171.14, 175.98, 'cta'),      # If you want a completely free guide for how you get started with that, just comment "free" and I'll send it to you.   (v2: "And yes, it's completely free." cut - Albert)
]
SPEED = {'hook': 1.12}
FORCE_END = {}
FADE_OUT = {}

# ---- 10 ms RMS scan of the whole master (vectorised) ------------------------------------
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', MASTER, '-ac', '1', '-ar', '16000',
                      '-f', 's16le', '-'], capture_output=True).stdout
a = np.frombuffer(raw, dtype='<i2').astype(np.float32)
W = 160                                            # 10 ms @ 16 kHz
n = len(a) // W
rms = np.sqrt((a[:n * W].reshape(n, W) ** 2).mean(1))
DB = 20 * np.log10(np.maximum(rms, 1.0) / 32768.0)
np.save(P / 'edit/db10ms.npy', DB)

def db(i):
    return float(DB[min(max(i, 0), len(DB) - 1)])

# Gates calibrated on the studio-mic master (floor -98 dBFS, speech p95 -27): inside a take the quietest
# 10 ms frame sits well above the between-take air.
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

def quiet_runs(a0, b0, th=QUIET, minlen=0.25):
    """Quiet runs >= minlen inside [a0,b0] (to know which pauses inside a take still need tightening)."""
    lo, hi = int(round(a0 * 100)), int(round(b0 * 100)); out = []; st = None
    for i in range(lo, hi + 1):
        q = db(i) <= th
        if q and st is None: st = i
        if (not q or i == hi) and st is not None:
            if (i - st) / 100 >= minlen: out.append((st / 100, i / 100))
            st = None
    return out

ranges = []; report = []
for s, e, nm in select:
    a0 = edge(s, -1, PAD_IN); b0 = edge(e, +1, PAD_OUT)
    s0, e0 = speech_edges(a0, b0)
    a0 = max(a0, round(s0 - LEAD, 3))
    b0 = min(b0, round(e0 + (0.20 if nm == 'cta' else TAIL), 3))
    if nm in FORCE_END: b0 = FORCE_END[nm]
    if nm == 'cta': b0 = round(e0 + 0.22, 3)          # let the last word ring out
    report.append((nm, s, e, a0, b0, db(int(a0 * 100)), db(int(b0 * 100)), quiet_runs(a0 + .05, b0 - .05)))
    sp = SPEED.get(nm, 1)
    # hook keeps exact trough times (no 1/30 snapping) per the skill's hook pacing rule
    st = a0 if nm == 'hook' else math.floor(a0 * 30) / 30
    en = b0 if nm == 'hook' else math.ceil(b0 * 30) / 30
    if nm in FORCE_END: en = st + math.floor((b0 - st) * 30) / 30      # whole frames, never past the trough
    ranges.append({'src': 'a', 'start': round(st, 6), 'end': round(en, 6), '_': nm, 'speed': sp})

print(f"{'beat':10s} {'scribe':>15s}   {'snapped':>15s}   {'dB at joins':>14s}   quiet runs >= .25 s inside")
for nm, s, e, a0, b0, d1, d2, qr in report:
    print(f'{nm:10s} {s:7.2f}-{e:7.2f}   {a0:7.2f}-{b0:7.2f}   {d1:6.1f} {d2:6.1f}   ' + (', '.join(f'{x:.2f}-{y:.2f}' for x, y in qr) or '-'))
json.dump({'sources': SRC, 'ranges': ranges}, open(P / 'edit/edl.json', 'w'), indent=2)

(P / 'edit/segments').mkdir(exist_ok=True)
time = 0; beats = []
for i, r in enumerate(ranges):
    src_dur = round(r['end'] - r['start'], 8); sp = r['speed']
    dur = round(round(src_dur / sp * 30) / 30, 8)
    nm = r['_']
    if nm.endswith('+') and beats and beats[-1]['name'] == nm[:-1]:
        beats[-1]['end'] = round(time + dur, 8)               # continuation: same beat, one more segment
    else:
        beats.append({'name': nm, 'start': round(time, 8), 'end': round(time + dur, 8)})
    time += dur
    tempo = f"atempo={sp}," if sp != 1 else ""
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(r['start']), '-i', SRC[r['src']],
        '-t', str(src_dur),
        '-vf', f"setpts=(PTS-STARTPTS)/{sp},fps=30",
        '-af', f"{tempo}atrim=duration={dur},asetpts=PTS-STARTPTS,afade=t=in:d=0.004,afade=t=out:st={dur-FADE_OUT.get(nm,.004)}:d={FADE_OUT.get(nm,.004)}",
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '1',
        '-t', str(dur), str(P / f'edit/segments/{i:02d}.mkv')], check=True)
    print(f'  cut {i:02d} {nm:10s} -> {dur:5.2f}s  (total {time:6.2f})', flush=True)
json.dump(beats, open(P / 'edit/beats.json', 'w'), indent=2)
(P / 'edit/concat.txt').write_text('\n'.join(f"file 'segments/{i:02d}.mkv'" for i in range(len(ranges))))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(P / 'edit/concat.txt'),
                '-c', 'copy', str(P / 'edit/tight.mkv')], check=True)
print('DURATION', round(time, 3))
