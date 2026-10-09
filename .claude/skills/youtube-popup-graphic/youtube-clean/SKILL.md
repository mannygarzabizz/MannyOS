---
name: youtube-clean
description: Edit Albert's long-form YouTube recordings (camera file + screen recording + the script he read) into a clean, calm 16:9 video in one pass — a mediator cuts the voice once (last take wins, ElevenLabs Scribe only), builds lip-sync-exact section files, delegates each script section to its own sub-agent, verifies every clip from frames and signal checks, routes Albert's notes back to the right agent, and stitches only after every section is accepted. Look — about half Albert full screen, half Apple-style recreated UI on a white ground (tweets, real pages, real numbers), rounded presenter card, real Apple emoji, tense quiet intro music, no pop sounds. Use when Albert says "/youtube-clean", "edit this YouTube video", "clean YouTube edit", "edit the long-form", gives a script plus a camera/screen recording, sends notes on a section ("section 3 make the pricing bigger", "intro music quieter"), or says "stitch it".
argument-hint: [script path/text + camera file + screen recording, or revision notes for one or more sections, or "stitch"]
---

# YouTube Clean

You are the **mediator**. You cut, package, delegate, verify, report and stitch; sub-agents edit the sections. Read
`cutting.md` (voice cut, sync-exact build, stitch), `layout.md` (look, pacing, sound), `section-agent.md` (the brief you send),
and skim `~/.claude/skills/reel-clean/SKILL.md` + `style.md` (drawing/cursor/honesty rules still apply). Everything in
`lib/` and `scripts/` works — **copy and run it, never rebuild it.** `examples/` holds scene files from the first video.

## Hard rules (Albert's, non-negotiable)
1. **Never show his script.** The screen recording shows his Google Doc most of the time; map script / non-script spans first.
2. **ElevenLabs Scribe only**, never Whisper or another STT. On 401/quota: stop the cut, report credits, do transcript-free prep.
3. **Last take wins.** Earlier takes, restarts and abandoned sentences go.
4. **Nothing twice, nothing missing, no breaks** — triple check (`cutting.md` §4) before any graphics.
5. **Voice = the screen recording's audio (good mic). Picture = the camera.**
6. **Picture and sound 1:1.** Build section files only with `scripts/build_sections.py`, prove with `scripts/verify_sync.py`,
   prove finals with `scripts/verify_final_sync.py`, stitch only with `scripts/stitch.py`. Never concat per-cut files, never
   the concat demuxer for picture, never `-shortest`. (First video drifted 0.5 s per section before this existed.)
7. **Calm, ~50/50** (talking sections; demo sections are mostly the clean `screen` layout — `layout.md` → Screen share). About half of every section is Albert full screen (`cam`), a visual only where the line needs one. Keep
   recreated tweets/pages, real numbers landing on the word, one mechanism diagram per section. `layout.md`.
8. **Sound:** soft caption click under EVERY caption, including his full-screen ones (`scripts/camcap_clicks.py` writes the cues); no pop/bubbly samples; one quiet whoosh per mode change; music quiet (bed ≈ −30 LUFS); if Albert supplies a
   track use it; music is laid in ONE pass at the stitch (per-section previews use the same offsets via `lib/mix_section.py`).
9. **Deliver sections one by one; stitch only when he says so.** Graphics follow what he SAYS; flag misspoken facts.
10. Report honestly: checks are frame/signal based — say so; never claim to have listened.

## One-shot pipeline (run in this order; do not improvise the plumbing)
**0 Intake (5 min).** Project `<your content root>/YYYY-MM-DD-<topic>-youtube/` with `edit/ sections/ review/
audio/ renders/`. Probe both files. Copy `~/.claude/skills/youtube-clean/lib/` → `<project>/lib/`. Check Scribe credits
(`/v1/user/subscription`; a 25-min recording ≈ 1,600 credits per pass, budget ~5k). `TYPESAFE_API_KEY` (in `./.env`, `~/.env`, or the environment) enables the Jev said-twice pass —
optional, the pipeline runs without it.

**1 Script + screen map.** Sample the screen recording (1 frame / 5 s) → `review/non_script_spans.json`; read the doc frames
to get the script he actually read (he rewrites in Google Docs) → `sections.md` with one row per heading (intro = 00).

**2 Voice cut.** Scribe the full camera audio once → phrase lines with times → write `edit/targets.py` (section, window,
exact kept text, last take — your judgment, nothing automated) → match to word indices
(last occurrence in window) → refine cut points on RMS troughs, split at inner pauses > 0.40 s, fix stretched word-ends →
`edit/edl.json` with `sources.cam` / `sources.screen` and ordered `ranges`.

**3 Build + prove.** `python3 scripts/build_sections.py <project>` then `python3 scripts/verify_sync.py <project>` (all `ok`,
≤ 40 ms). Scribe each `voice.mkv` → `transcript.json`; run the triple check (coverage, repeated 5-grams, read-through, no pause
> 0.45 s); normalise product-name spellings; write `beats.json` (one beat per sentence), `script.txt`, `screen_spans.json`.
Then the said-twice pass: `python3 scripts/said_twice_check.py <project>` — **Jev** decides whether a line is
already said (`--decide` on the raw transcript writes `edit/jev_drops.json`, last-take-wins, and escalates the
uncertain band to you). Jev judges content; code keeps the timeline. Skips cleanly without a key.

**3b Screen share (when the body uses the real capture).** `python3 scripts/build_screen.py <project>` → per section `screen.mp4`
(chrome-free, zoom-safe, cuts dissolved, frame-exact with `voice.mkv`) + `screen_meta.json` + `review/screen_sheet.jpg`. READ every
sheet; write script/private spans to `screen_spans.json`. Agents use `lib/screenshare.py` + the `screen` mode (`layout.md` → Screen share).
In screen-share stretches do NOT close inner pauses where the screen shows the result arriving — the viewer needs to see it land.

**4 Research once.** One agent gathers real copy/numbers/assets for everything that will be recreated → `research/`.
Flag every number the script gets wrong.

**5 Delegate.** (Ultracode / big edits: a Workflow — editor → adversarial reviewer → fix → re-verify per section — beats bare
agents; the reviewer's checklist is the verify list in step 6 plus chrome/grid/truth/timing.) Write `stitch.json` now (section order + music block if any) so previews carry music at the right offsets.
One background agent per section, all launched in one message, each with `section-agent.md` filled in + a surface plan that
already says which beats are `cam` and which visuals are needed. Tell them the machine is shared (≈3 fps when 8 render).

**6 Verify each return yourself** (an agent's "done" is not evidence): ffprobe; contact sheet you READ; first/last frames;
`scripts/verify_final_sync.py <project> <section>` = 0 ± 1 frame; script-doc flags looked at; sourced numbers spot-checked in
`sources.md`; % cam; peak. Failures go back to the same agent via `SendMessage`. Then `SendUserFile` + status row in `STATUS.md`.

**7 Notes loop.** Split Albert's batch per section → `SendMessage` to each agent → tell him who is on what → verify each note
on frames/audio at the exact times → re-send with done / not done / done differently. Global notes (a sound he dislikes, a
pacing change) go to every agent through one shared brief file in `sections/`. Voice-cut notes are the mediator's job
(edit the EDL → rebuild that section with `build_sections.py <project> <section>` → agent re-times graphics).

**8 Stitch** only on his word: `python3 scripts/stitch.py <project>` (one encoder, one audio grid, music in one pass,
−14 LUFS, verification built in) → master + `chapters.txt` + `stitch_report.json`. Read the join frames. Deliver.

**9 Learn.** Append what he accepted/rejected to `layout.md`; keep accepted scene files in `examples/`; update memory.

## Efficiency notes from the first video
- The voice cut + build + checks take ~30 min of mediator time; do them carefully once — every later fix is a re-render.
- Decide `cam` vs visual in the surface plan up front; the first video was rendered three times because it started too busy.
- Picture re-renders are the cost (8 parallel ≈ 8–10 min each); audio-only fixes are seconds — keep mixes scriptable
  (`lib/mix_section.py` + `sfx.json`), never hand-rolled per agent.
- Screen-share lessons (2026-09-19): detect chrome by the bookmarks bar's flat 59-grey band, never by "a bright page row below"
  (dark pages exist); smooth detections with a MAX, never a median; scan every OUTPUT frame for teal / 59-grey rows at the top
  and read each flag. Section agents that render must background their renders (Bash times out at 10 min).
- Never `SendMessage` an agent that is running inside a Workflow: it resumes a SECOND copy of that agent next to the running
  one, and both edit the same section (happened 2026-09-19, 02 fix round). Put shared answers in `sections/BRIEF-COMMON.md`
  and fix lib yourself; for per-section changes wait for the workflow to return, then use a fresh agent.
- Face in the slim presenter card: `python3 lib/faces.py sections/<s>` (macOS Vision) gives FACE_CX keyframes — the skin-tone
  estimate in layout.py is not good enough for a 280 px card.
- Adversarial reviewers after each section editor caught ~20 real issues on the first video with screen share (zoom pumping
  against Screen Studio, captions over whip-pans, numbers he never said, one-frame pops, strobing thumbnails) — keep them.
- QA "quiet runs" on the good mic are natural pauses; QA "script-doc" flags on recreated text windows are false positives —
  look once, then move on.

Use `$ARGUMENTS` as inputs or notes. If the project exists, resume from `STATUS.md`.
