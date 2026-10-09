# Fish Audio transcription (replaces ElevenLabs Scribe, 27 Sep 2026)

Albert switched this skill from ElevenLabs Scribe to the Fish Audio API. The scripts live in `scripts/`:

| script | job |
|---|---|
| `fish_audio.py` | loads the key, sends one ASR request; run it alone for a free auth check |
| `align_words.py` | Fish segments → timed words: Fish's own word times, punctuation restored, local aligner as fallback |
| `transcribe.py` | Fish + timing → `<edit-dir>/transcripts/<stem>.json` (same `words` shape Scribe produced) |
| `splice_audit.py` | the per-join doubled-speech audit, Fish windows instead of Scribe windows |

## Word timing
Fish's ASR is `POST https://api.fish.audio/v1/asr` with a `model: transcribe-1` header, multipart `audio` and
`ignore_timestamps=false`. It returns `{text, duration, segments:[{text,start,end}]}`. The docs only promise
phrase segments, but in practice (tested 27 Sep 2026) **every segment is one word** on a 40 ms grid.
- Tested against measured silence edges on a synthetic clip, Fish's word times were off by about 30 ms on
  average. The local MMS_FA aligner was off by about 42 ms, and its CTC word ends ran up to 125 ms early. So
  one-word segments keep Fish's times (`"timing": "fish"`).
- One-word segments lose their punctuation ("month" vs "month."). `restore_punctuation()` takes each token's
  spelling from Fish's full `text`, because captions break on `. ! ? :` and `fix_words.py` keys on tokens like
  `'Naya,'`.
- If Fish ever returns multi-word segments, those words are force-aligned locally with torchaudio's MMS_FA
  wav2vec2 model (`"timing": "aligner"`, CPU, nothing uploaded). Segments are grouped into chunks of 30 s or
  less, cut at gap midpoints. A failed chunk retries segment by segment, then shares the segment's time by
  letter count (`"timing": "estimated"`). `--force-align` re-times everything with the aligner.
- Aligner model: `model.pt`, 1.2 GB, from Meta (dl.fbaipublicfiles.com). It is already downloaded to
  `~/.cache/torch/hub/checkpoints` (27 Sep 2026) and is only loaded when a segment actually needs aligning.
- Numbers, `$`, `%` and `k/m/b` are spelled out *for alignment only* (`$20M` → "twenty million dollars"). The
  caption text stays as Fish wrote it.
- Never land a graphic on an `"timing": "estimated"` word without checking it on the 10 ms RMS profile. The outward
  RMS edge scan in `build_cut_*.py` still decides cut points; the transcript never does that alone.

## Key
`FISH_API_KEY` is read, never executed, from the first of: the environment (or `FISH_AUDIO_API_KEY`) →
`FISH_ENV_FILE` → `.env` in the reel folder → `ReelCreator/.env` → `~/Desktop/ContentHouse/.env` (where it lives
today). Never print it, copy it into a project, or put it in the skill.
`python3 scripts/fish_audio.py` checks it against `GET /wallet/self/api-credit`. HTTP 200 means the key is good,
401 means a bad key, and 402 means no API credit.

## Cost and caching
- Full files: the raw Fish response is cached as `<stem>.fish.json` next to the transcript, keyed on path, size,
  mtime, language and model. Re-running `transcribe.py` on the same file never re-uploads.
- Splice windows: `~/.cache/fish_asr_windows/` holds raw responses and timed words, cached separately.
- Uploads are 16 kHz mono WAV. Over about 19 MB (about 10 min) they go as 64 kbps MP3. Over about 60 min the
  script stops: split the file first.
- 429/503 retry up to 3 times with backoff; any other error stops the step with its HTTP code. There is no
  silent fallback to Whisper or Scribe, and an unavailable transcript means a failed splice audit.

## What changed vs Scribe
- Scribe's `no_verbatim=false` kept false starts and stutters. Fish has no such switch and may tidy a stutter,
  so the splice audit's RMS fragment check (a speech blob under 180 ms at the join) matters more now. In the
  test it still caught a doubled "model costs … model costs" join.
- Fish mishears brand names like any ASR: "Shiney" came back as "Shiny" and "Shinny". Keep the `fix_words.py`
  `FIX` map.
- `--num-speakers` is accepted and ignored. `--model transcribe-1-pro` is for multi-speaker audio. It adds
  `<|speaker:N|>` markers, which are stripped, and `[emotion]` cues, which become `audio_event` tokens. Its segment
  shape is untested.
