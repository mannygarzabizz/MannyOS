# Brief for a section sub-agent (the mediator fills the {…} fields)

You edit **one section** of Albert's YouTube video: `{NN-name}` ({kind}: intro / explain / screen). Project root `P` = {project}.
Work only inside `P/sections/{NN-name}/`. Never touch `P/lib`, other sections, `voice.mkv`, or Downloads.

Read first: `~/.claude/skills/youtube-clean/layout.md`; `~/.claude/skills/reel-clean/SKILL.md` critical rules + `style.md`;
`P/lib/render_section.py` docstring, `P/lib/camcaps.py`, `P/lib/mix_section.py`, `P/lib/captions.py`, `P/lib/layout.py`;
the examples in `~/.claude/skills/youtube-clean/examples/`; `P/research/*.md` + `P/research/assets/`.

Inputs in your folder: `voice.mkv` (final, lip-sync-exact: camera picture + good-mic audio — never recut, retime or remux it),
`transcript.json` + `beats.json` (Scribe word timings on that cut; time everything with `at(beat, word)`), `script.txt`,
`screen_spans.json`. Surface plan from the mediator: {surface plan — which beats are `cam`, which visuals are needed and why}.

Screen-share sections: `screen.mp4` + `screen_meta.json` are in your folder (chrome-free capture, frame i == voice frame i). Use
`P/lib/screenshare.py` (read its docstring) and the `screen` mode exactly on its grid; read `layout.md` → Screen share. Never open the raw recording.
**Minimal by default** (layout.md → "Minimal by default"): one idea per frame, at most THREE things on the stage at once,
no explanatory sentences (a bare number beside the thing, never `Reply to "…" $0.0020 on …`), labels <= 3 words, one accent
colour, half the stage empty, elements leave when he moves on. Cards/tiles/steps/columns get a HEADLINE ONLY - never a
description line under it ("Choice", not "Choice / Ask a multiple choice question"). Build it, then delete one thing.
**Zoom gently**: 1.2-1.4x is normal, 1.6x is the hard cap, one push per screen stretch, hold >= 4 s, default to no push at all
(an accent ring beats a zoom). Same restraint on recreated `full` visuals (<= 1.4x).
**No captions over `cam`** (Albert, 2026-09-20) and **no text over `screen`** (2026-09-19/20): text can only ever live
on a recreated `full` / `split` stage. `camcap_clicks.py` is retired with CAM_CAPS.
**No text at all while the screen share is on screen**: no title line above the card (`SS.title` is retired), no caption below it,
no number call-outs, nothing over the capture — point with focus push-ins and accent rings only. Text belongs in `cam` and recreated `full` visuals.

Rules
- **Never show Albert's script / Google Doc.** Only `screen_spans.json` rows with `screen_is_not_script: true` may be sampled,
  and look at every frame you use. Prefer recreating the page (light mode, Apple-clean) over using his capture.
- **Calm, ~50 % `cam`.** `cam` = Albert full screen and **NOTHING OVER HIM — no caption at all, ever** (Albert,
  2026-09-20). `CAM_CAPS`, `camcaps.make_overlay()` and `scripts/camcap_clicks.py` are RETIRED — do not use them. A visual exists only where the line needs it: recreated tweets / X posts / real pages (he likes
  these), real numbers landing on the spoken word, the ONE diagram that explains your section. No emoji-only beats, filler
  cards, recap rows, second examples. Fewer surfaces, each held ≥ 3 s, one clear action, then it may rest. Modes in stretches
  of 6–15 s. If your section opens on him talking, `MODES` starts with `(0,'cam')`; if it closes on him talking, `'cam'` is the
  last entry (clean cut into the next chapter). Check a few `cam` frames: head not cropped (FACE_CX).
- **Truth.** Graphics show what he SAYS in this cut; use the precise sourced figure in the UI and his rounded wording in the
  caption. Real copy, real numbers, real logos only — sources in `sources.md`; anything illustrative is listed there as filler.
  Do not caption words the mediator marked uncertain.
- **Sizes.** `full`: composition fills 70–80 % of the frame width, vertically centred with its caption, tiles ≥ 260 px, labels
  ≥ 34 px. `split`: graphics + caption fill ~80 % of the stage (x 70–1180, y 80–1000), windows ≥ 1000 px wide, row text ≥ 30 px.
  Nothing under the presenter card or the full-mode bubble.
- **Sound.** Write `sfx.json` and run `python3 P/lib/mix_section.py P/sections/{NN-name}` — do not write your own mixer.
  No pop/bubbly samples. One whoosh per mode change at −31 dBFS peak, none in the first/last second; `first-click.wav` only where
  a cursor presses; intro only: caption mouse-down clicks on cinematic groups. Music is NOT yours to mix: if `P/stitch.json`
  has a music block covering your section, `mix_section.py` adds the preview at the right track offset by itself.
- Disk: never save full-length frame arrays (.npy) or frame dumps — stream through ffmpeg pipes, keep numbers, small JPGs only;
  delete your scratch before returning (2026-09-19: 7 agents filled a 460 GB disk to 0 bytes).
- No speech-to-text of any kind. No edits to lib (ask the mediator).

Workflow (the machine is shared by up to nine renders — expect ~3 fps; preview often, full-render once or twice)
1. `beatmap.md`: beat → `cam` or visual, and for each visual why the line needs it; target % `cam`.
2. `scenes.py` → `python3 P/lib/render_section.py P/sections/{NN-name} --preview` → READ `review/preview.jpg`; `--strip` for
   every landing; fix cut-offs, overlaps, baselines, late cues (lead the word by 0.13 s).
3. Full render → `mix_section.py` → `python3 P/lib/qa_section.py P/sections/{NN-name}` → READ `review/sheet.jpg`.
   (QA "quiet runs" are natural pauses on the good mic — report, don't fix. "script-doc" flags on your own recreated text
   windows are false positives — look, confirm, report.)
4. Report ≤ 12 lines: modes timeline, % cam vs visuals, what each visual shows and why it survived, captions used, anything
   done differently, frame count, peak, QA result, files. Be literal — the mediator checks your frames.

Revisions: do exactly the notes you are sent, nothing else; keep the previous final as `{NN-name}-vN.mp4`; say per note what
changed and at which timestamps. Audio-only notes never re-render the picture (`mix_section.py` only).
