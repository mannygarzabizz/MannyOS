# youtube-clean — setup

A Claude Code skill that edits a long-form talking-head video end to end: it cuts the voice once (last take wins),
builds lip-sync-exact section files, hands each section to its own sub-agent, verifies every clip from frames and
signal checks, and stitches only when you say so.

Drop this folder in `~/.claude/skills/youtube-clean/` and say **"edit this YouTube video"** with your camera file
and your screen recording.

---

## What you need

| | |
|---|---|
| **ffmpeg / ffprobe** | on PATH. Everything is built through pipes. |
| **Python 3.11+** | with `numpy` and `Pillow`. |
| **macOS** | `lib/faces.swift` uses the Vision framework for face tracking, and real Apple emoji are read from `/System/Library/Fonts/Apple Color Emoji.ttc`. The rest is portable; those two parts are not. |
| **A speech-to-text step** | **not bundled** — see below. |
| **A TypeSafe key** | optional, see below. |

## The one thing you must supply: transcription

`cutting.md` refers to `<ui>` — a small set of helpers this skill calls but does **not** ship:

```
transcribe.py   cutjoin.py   edl_check.py   splice_audit.py   speech_map.py   elevenlabs_auth.py
```

The only one the pipeline truly needs is **`transcribe.py`**, which must take an audio/video file and write
word-level timings as:

```json
{ "words": [ { "text": "Hello", "start": 0.12, "end": 0.34, "type": "word" }, ... ] }
```

The skill is built around **ElevenLabs Scribe v2** because word timings have to be accurate to ~20 ms for the cut
points to land. Anything that produces the shape above will work; if the timings are loose, the cuts will be too.

Point `<ui>` at wherever you put it.

## Optional: the Jev said-twice pass

`scripts/said_twice_check.py` asks **TypeSafe Jev** one question over the transcript — *is anything said twice?* —
and can drop the earlier of a duplicated pair (`--decide`), escalating anything it is unsure about to you.
It exists because the 5-gram duplicate check cannot see a paraphrased retake.

Set `TYPESAFE_API_KEY` in `./.env`, `~/.env`, or the environment. **Without a key it skips cleanly** and the rest of
the pipeline runs exactly as before — it is an extra pair of eyes, not a dependency.

## Also referenced but not bundled

`layout.md` and `section-agent.md` point at a sibling skill, **`reel-clean`**, for the shared drawing/type/cursor
and honesty rules, and for the redrawn Apple-emoji example. The YouTube pipeline runs without it; you will just be
missing those cross-references.

---

## Where to start reading

1. **`SKILL.md`** — the pipeline, step 0 to step 9. Read this first.
2. **`cutting.md`** — how the voice cut works: sync, take selection, the triple check, section packages.
3. **`layout.md`** — the visual and sound contract. The accepted/rejected log at the bottom is the real taste.
4. **`section-agent.md`** — the brief each section sub-agent receives.
5. **`examples/`** — two accepted scene files from a finished video, to see the shape of a `scenes.py`.

## A note on the bundled assets

`lib/assets/icons/` contains third-party product marks and `lib/audio/sources/` contains three short SFX. They are
here so the skill runs out of the box. Check they suit your use before you redistribute this folder further —
brand marks belong to their owners, and you should confirm the licence on the audio.
`lib/assets/fonts/Inter.ttf` is Inter, under the SIL Open Font License.
