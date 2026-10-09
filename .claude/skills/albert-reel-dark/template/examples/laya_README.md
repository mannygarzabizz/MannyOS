# Laya ("Naya") reel — 21 Sep 2026 (v1)

`renders/FINAL-laya.mp4` — **32.73 s**, 1080×1920, 30 fps, H.264 / AAC 48 kHz.
`renders/clean-voice.mp4` — same picture, recorded voice only (no music, no SFX).

Sources (neither file was modified):

| file | role |
|---|---|
| `~/Downloads/C1332.MP4` | camera, portrait via rotation metadata — **picture** |
| `~/Downloads/2026-09-21 08-31-49.mov` | OBS recording of the teleprompter — **voice** (studio mic) |

## ⚠ The model is called **Laya**, not "Naya"

The teleprompter says "Naya" and that is what is spoken. The project the script describes — free, open
source, local System-One model, ~30 ms vs Jev's ~250 ms, base model needs fine-tuning — is
**Laya** by Convai Innovations: <https://github.com/NandhaKishorM/laya> (5.2k★, Apache-2.0, `pip install laya`,
logo lockup "laya — DECISIONS, NOT TEXT"). Searching "Naya" + Jev / System One returns nothing.

What I did: the **voice is untouched** (he says "Naya"), but every on-screen surface and the caption show the
real name **Laya**, because that is what viewers have to search for and what the DM link will open. N/L are
close enough that it does not read as a mismatch at speed. To caption it as spoken instead, change the one
`'Naya,':'Laya,'` entry in `fix_words.py` and re-run. The clean fix is re-recording the 1-second line
"It's called Laya".

## Audio source and sync

`edit/master.mkv` = camera picture + OBS mic. Offset measured by brute-force envelope correlation (estimator
validated on a synthetic +1234 ms shift first): **OFF = 2.504 s** (camera time T ↔ mic time T + 2.504),
0.81–0.86 correlation on 9/9 windows, drift 49 ppm (8 ms over the take → constant offset). Residual of the
built master against the camera's own audio: **+1 ms**. Noise floor: camera −39.6 dBFS vs mic **−87.8 dBFS**.

## The cut — 13 beats, last take wins (`build_cut.py`)

| # | beat | line | master range |
|---|---|---|---|
| 1 | hook (1.12×) | Someone just released a free and open source version of Jev, | 13.75–16.92 |
| 2 | faster | and it's actually much faster. | 38.57–40.30 |
| 3 | possible | How is that even possible? | 45.54–46.81 |
| 4 | naya | It's called Naya, | 51.33–52.34 |
| 5 | local | and it's a local System One model that you can run on your own computer. | 54.00–57.62 |
| 6 | nocode | Same as Jev, it cannot write code, | 66.51–68.38 |
| 7 | speed | but where Jev takes around 250 milliseconds to respond, this model only takes 30 milliseconds, | 100.15–105.36 |
| 8 | cloud | and that's because it's running local, so it doesn't have to go to the cloud and back, | 113.10–116.52 |
| 9 | muchfast | which makes it much faster. | 116.91–118.23 |
| 10 | problem | The only problem is that the base model isn't good at everything, | 128.11–130.79 |
| 11 | tuned | so it needs to be tuned and trained for specific use cases. | 133.59–136.55 |
| 12 | claude | But we can actually do that with Claude. | 148.04–149.51 |
| 13 | cta | If you want the link to the model, just comment "FAST" and I will send it to you. | 155.76–158.83 |

- `nocode` ends inside running speech (the take continues into an aborted "but where Jev takes around 200…").
  "code," decays to −57 dBFS at 68.36–68.38 s and "but" starts at 68.39 s, so the end is pinned to that 30 ms
  trough (whole frames, never past it) with a 14 ms fade. Scribe reads the join as "it cannot write code, but
  where Jev takes around…".
- `cloud` / `muchfast` are one take with the 0.44 s breath before "which" removed.
- "F*ck JEV" (first teleprompter line) was never recorded, so it is not in the reel.

## Scenes (all recreated with Pillow, no screenshots)

| # | beat | mode | surface |
|---|---|---|---|
| 1 | hook | **full** | **The "?" model shoots up Jev** (`parts/hook.py`). Official TypeSafe/Jev tile on the right; the ink "?" tile slides in with a pistol. One round per stressed word (released / free / open / source), a three-round burst on "version of", and the last round on "Jev" breaks the tile into three shards that fall under gravity. Each round: 2-frame muzzle flash + tracer + recoil + ejected brass + a hole punched **in** the tile + a 2-frame camera kick |
| 2 | faster | split | Two-lane drag strip: Jev crawls, the "?" tile accelerates with speed streaks and crosses the checkered line on "faster" |
| 3 | possible | split | Magnifying glass sweeps onto the "?" tile; inside the glass you glimpse the real Laya mark. Question marks drift up around it |
| 4 | naya | split | The "?" tile flips over on the name → Laya tile, their own wordmark + tagline "DECISIONS, NOT TEXT", pills: `NandhaKishorM/laya` · ★ 5.2k · Apache-2.0 |
| 5 | local | **full** | **MacBook Pro** (`parts/macbook.py`, drawn from scratch: notch, bezel, aluminium base). Lid opens and is up by "local"; Laya drops into the Dock and bounces; Terminal types `pip install laya` → `python triage.py` → the README's real example output (billing 0.94 / 1.84 / 0.892); the menu-bar Wi-Fi gets struck through on "own" and "ran on this Mac – no cloud call" lands on "computer" |
| 6 | nocode | split | Dark editor: five lines of Python type in, then a red strike-through sweeps each line left→right on "cannot"; Jev tile pops next to Laya in the title bar on "Same as Jev" |
| 7 | speed | **full** | Latency card: Jev row counts up and lands on **250 ms** exactly on the word (red frame), a dot crosses the bar once every real 250 ms; the card **grows** for the Laya row, which counts to **30 ms** on the word (green frame) on the same 0–250 axis |
| 8 | cloud | split | MacBook + cloud diagram: a pink packet does the slow round trip; the green loop starts on the laptop on "local"; on "doesn't" the route un-draws and the cloud drifts off; check lands on "back" |
| 9 | muchfast | split | Speedometer: needle accelerates past the little Jev marker and hits the top on "faster" |
| 10 | problem | **full** | **Favourite move** (`parts/readme_zoom.py`): the real GitHub README recreated in Safari (`github.com/NandhaKishorM/laya`), camera pushes in to **Honest limits**, yellow highlighter sweeps the bold lead on "base model" and "Laya is a fast base to specialise, not a zero-shot decision engine." on "isn't good" |
| 11 | tuned | split | Fine-tune run: accuracy counts **0.362 → 0.766** with the curve (README's typed-decisions numbers), epoch ticker, then the four real presets (Support triage / Prompt guardrails / Moderation / Model routing) get picked across "specific use cases" |
| 12 | claude | **full** | Laya tile centred; cream Claude Code prompt types "Fine-tune Laya on my support tickets"; on "Claude" the Laya tile slides left, "+" spins in and the Claude tile lands; send presses |
| 13 | cta | split | Instagram comments: **FAST** typed + posted; the real repo link writes itself underneath on "link" and goes blue on "send" — *link/guide chip rejected 25 Sep 2026: copy the comment UI only, no link pill* |

Brand assets: **official TypeSafe icon** = their own `apple-touch-icon` from typesafe.ai (400 px, magenta
#E551BA, saved as `assets/icons/TypeSafe.png`; the older 115 px mark from the 16 Sep reel is retired). Laya mark
is redrawn from the repo's `logo-mark.svg` so it is sharp at any size; the lockup PNG in the README scene is
theirs. Every number on screen is either spoken (250 ms, 30 ms) or from the Laya README as scraped today.

## Sound

91 cues in `audio/cue-sheet.json`. Gunshots are **synthesised** (`audio/sources/gunshot.wav`: noise crack +
low-passed body + pitch-dropping thump — there was no shot in the kit), −15 dB first/last, −17/−19 in between;
whoosh on the break. Caption mouse-down on the first and last word of every full-screen group; one click per
UI press; quiet pops for things that land. Music: the approved *Timeless (Instrumental)* excerpt, −29 LUFS
pre-duck, sidechained under the voice.

## Verification — signal and frame checks only; I cannot listen

- 32.733 s, 1080×1920, 30/1 fps (ffprobe). Integrated **−17.4 LUFS**, LRA 1.9, **true peak −1.4 dBFS**, sample peak −4.45.
- **Provenance:** all 12 unretimed takes correlate **1.0** with the master at |lag| ≤ 0.5 ms (48 kHz). Hook is 1.12×, excluded.
- **Air:** 0 quiet runs ≥ 0.30 s (`check_air.py`); the only one ≥ 0.15 s is the 0.23 s ring-out after the last word.
- **Motion:** 0 beats hold still > 0.60 s (`check_motion.py`); longest 0.60 s in `cta`, 0.57 s in `nocode`/`speed`.
- **Frames** (`check_frames.py`, all 982): min frame std 12.1 (no blank frame), **0 frames with ink in the top 180 px**,
  nothing under the captions in any full-screen beat.
- Captions cover all 133 words; the last group ("to you") runs to the final frame.
- **Scribe splice audit:** every join reads as the intended sentence; the single flag is the legitimate
  "the link to **the** model".

## Rebuild

```bash
python3 build_cut.py && python3 fix_words.py && python3 render.py && python3 mix.py && python3 qa.py
python3 check_air.py && python3 check_motion.py && python3 check_frames.py
```

`python3 render.py --preview` → contact sheet; `python3 render.py --strip <beat> t1,t2,…` → motion strip;
`python3 gridstrip.py <tag> beat1,beat2 6` → several beats in one sheet. `parts/hook.py`, `parts/macbook.py`
and `parts/readme_zoom.py` each run standalone.

## Not done

- Comment-to-DM automation is **not** wired. Keyword would be **FAST**, link `https://github.com/NandhaKishorM/laya`.
- Music is the default approved excerpt; no new song was picked for this reel.
