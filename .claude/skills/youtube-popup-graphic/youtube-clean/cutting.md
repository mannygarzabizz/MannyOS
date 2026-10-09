# Cutting rules — YouTube Clean

`<ui>` = wherever your transcription helpers live (transcribe.py, cutjoin.py, edl_check.py, splice_audit.py,
speech_map.py, elevenlabs_auth.py) — see SETUP.md, they are NOT bundled. ElevenLabs Scribe v2 only.

## 1. Sync camera and screen recording
Extract both audios to 16 kHz mono wav. Cross-correlate 30 s windows at ~1 min, the middle and ~1 min before the
end. Report `screen_time − cam_time` at each; expect a constant offset plus a few ms/min drift (OBS vs camera
clock). Use the offset local to each section; peak correlation < 0.15 means the window was silence — move it.
**Voice = the screen recording's audio track (his good mic, via OBS). Picture = the camera file.** (Albert, 2026-09-18.)
Transcribe and pick takes on either track, but every section's `voice.mkv` carries camera video + screen-recording audio,
cut at `cam_time + local offset` with one median offset per section (per-range cross-correlation on short ranges can lock
±10 ms off). Loudness-match nothing to the camera track; the camera audio is only the sync reference. The good mic has a
lower noise floor, so natural pauses show up as 'quiet runs' in QA — judge them against the 0.25–0.45 s pause rule instead.

## 2. Find the script in the screen recording (so it is never shown)
Sample the screen recording at 1 frame / 5 s. A frame is `script` when the document area is a bright page of text
(Google Docs / Notion / Word: mean luma of the page region > 225) or the tab/URL is a docs editor. Write
`review/non_script_spans.json` (screen times) and a contact sheet of the non-script spans; read it. Spans
shorter than 5 s around a script span are treated as script. The same frames are useful for one thing only:
reading what he actually scripted (OCR by eye into `sections.md`).

## 3. Take selection — the last take wins
1. Scribe the full camera audio once (`transcribe.py edit/cam.wav --edit-dir edit/raw --language en`).
2. Align transcript to script sentence by sentence (fuzzy match on content words). For each script sentence list
   every attempt with start/end and whether it is complete (reaches the sentence end without restart, filler
   trail-off or a laugh/"sorry"/"again").
3. Keep the **last complete** attempt. If he restarts mid-sentence, the kept range starts at the restart that
   leads into the last complete ending. If he retakes a whole section later in the recording, the later block
   replaces the earlier one entirely — do not mix sentences from both unless the later block skipped one.
4. Improvised stretches (no script match, usually over a screen share) are kept in order, minus restarts,
   fillers ("uh", "so yeah", repeated openers) and dead air while he scrolls.
5. **No micro-fragments.** A kept range shorter than ~0.8 s that sits between two cuts ("So", "But", "And it") flashes as a
   double jump cut when he is full screen. Either keep it attached to a neighbour (same take, natural pause left in) or drop
   the word if the sentence still reads. `build_edl.py` prints every range < 0.8 s — resolve each before building.
6. Cut points: trough after the previous word end → ~30 ms before the next onset, fine RMS scan (5–10 ms).
   Body joins keep 60–120 ms of natural air; intro joins 10–40 ms. No gap > 0.25 s inside a section unless it is
   a deliberate beat before a reveal (≤ 0.45 s).

7. **Near-duplicates across sentences count as retakes too** (Albert, 2026-09-19): "We have some API key stuff going on" …
   "Then we have some API keys, some documentation"; "No idea what this is." … "No idea what the answer would be to this."
   When two kept sentences say the same thing, keep the LAST (usually the fuller one). Note that neither example above
   shares a 5-gram, so the Pass B slide cannot see them — that is what the said-twice check in §4 is for. **Take
   selection itself is yours**: you read, you choose, last take wins. Nothing is automated here.

## 4. Triple check (all three must pass before graphics start)
- **Pass A — coverage:** Scribe the cut. Every script sentence appears exactly once (or is knowingly dropped
  because he never finished it — list those for Albert).
- **Pass B — duplicates:** slide a 5-word window over the final-cut transcript; any 5-gram appearing twice is
  inspected. Also compare section ends with the next section's start (retakes often re-say the subhook).
- **Pass B+ — said-twice, decided by Jev:**

      python3 scripts/said_twice_check.py <project>        # -> review/said_twice.json

  An extra pair of eyes over the finished cut, asking one thing: *is anything said twice?* It exists because Pass B
  is string overlap and a paraphrased repeat shares no 5-gram (see §3.7 for two real examples). The judgment is
  semantic, so it goes to **Jev** (TypeSafe System One): state carries the sentences once, every neighbouring pair
  inside a 30 s / 6-sentence window is one Noul, and Jev reads the state once and answers them all in parallel —
  ~3.5k tokens for a 22-minute recording, fractions of a cent at $0.042/M.
  Because the answer is a calibrated probability the report is three-way, never a coin flip at 0.5:
  `p >= 0.85` said twice · `p <= 0.35` clear · in between → **you read those few**.
  **What it decides and what it never touches.** With `--decide` the clear cases become `edit/jev_drops.json` and
  the EARLIER of a duplicated pair is dropped — the existing last-take-wins rule of §3, applied by Jev instead of
  by eye. The uncertain band is never decided automatically: it is escalated to you. Jev judges CONTENT (is this
  line already said?); code keeps the TIMELINE (cut points on RMS troughs, word indices, ordering) and Jev never
  writes a word of the transcript — that comes from speech-to-text, which Jev cannot do, being text-only.
  With no `TYPESAFE_API_KEY` it skips cleanly and the pipeline runs exactly as before.
- **Pass C — read-through:** read the whole final-cut text top to bottom as a viewer. Flag sentences that start
  mid-thought, dangling "and…"/"but…" with nothing after, pronouns whose referent was cut, and numbers that
  contradict an earlier line.
- `splice_audit.py` on every join; quote the join text in the report. Signal checks only — say so.

## 5. Per-section packages — ALWAYS built with `scripts/build_sections.py`, then proven with `scripts/verify_sync.py`
**Never cut each range to its own file and concatenate them.** That is how the first video went out of lip-sync: every cut's
video is padded to a whole frame (0–45 ms) and the joins carry timestamp gaps, so the presenter ends a section up to 0.5 s
late while the audio (and therefore all graphics) stay right. Also never build the picture with the concat demuxer, and
never mux with `-shortest`.

1. Write `edit/edl.json` = `{"sources":{"cam":…,"screen":…},"ranges":[{"sec","start","end"}…]}` (camera seconds, playback order).
2. `python3 ~/.claude/skills/youtube-clean/scripts/build_sections.py <project>` → per section `voice.mkv`
   (camera PICTURE + screen-recording AUDIO on one exact timeline: gapless audio buffer, ONE video encoder on a constant
   30 fps clock, one median screen-mic offset per section), `timeline.json`, `_cam.wav`, `_voice.wav`.
3. `python3 …/scripts/verify_sync.py <project>` must print `ok` for every section (≤ 40 ms at start / middle / end; the
   camera is 25 fps so 40 ms is the floor). **Do not run Scribe on the sections or brief any agent before this passes.**
4. Then per section: `transcript.json` (Scribe on `voice.mkv`), `beats.json`, `screen_spans.json`, `script.txt`.
5. After the agents render: `python3 …/scripts/verify_final_sync.py <project>` (exact: re-creates sampled output frames with the
   camera shifted −6…+6 frames and finds the matching shift; must be 0 ± 1 frame everywhere). The older
   `verify_sync.py <project> --final` (which voice frame the presenter card really
   shows, at many moments, only where he is clearly moving) is only a rough check — it reads ±500 ms whenever the card is not in the split position; do not rely on it. `lib/render_section.py` carries a
   SYNC GUARD that refuses to render when a voice file's picture and sound differ by more than 1.5 frames — keep it.

## 6. Stitch (only after every section is accepted)
Concat the accepted `NN-name.mp4` files with the concat demuxer after re-encoding each to identical params
(libx264 high, yuv420p, 30 fps, 48 kHz stereo AAC 320k or PCM in mkv for the master). 4 ms audio fades at
joins; intro music tail may overlap 1.5 s into section 01 via an audio-only crossfade. Then: loudness to
−14 LUFS integrated, true peak ≤ −1 dBTP, a contact sheet around every join (±0.5 s), a final script-doc scan
over the whole file, chapters list (`00:00 Intro` …) from the section durations.
