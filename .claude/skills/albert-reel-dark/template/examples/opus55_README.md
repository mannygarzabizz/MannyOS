# Opus 5.5 / CLAUDE.md reel — 23 Sep 2026 (v8)

`renders/FINAL-opus55.mp4` — **38.63 s**, 1080×1920, 30 fps, H.264 / AAC 48 kHz (v2).
`renders/clean-voice.mp4` — same picture, recorded voice only (no music, no SFX). `renders/FINAL-opus55-v1.mp4` … `-v7.mp4` — earlier cuts.

## v8 — "the line on the arm, make it not as thick"

Arm outline 1.5 px (was 4), matching the hand's outline.

## v7 — "make the middle finger a little longer and move the hand down, so it's on top of the arm"

Finger length up by a third (two knuckle creases now); the wrist stub is gone and the fist is seated on the arm's end
disc, so it reads as a hand on an arm.

## v6 — "it's pretty terrible the finger; make the middle finger smaller, and the arm not as long"

The fist is redrawn (`scenes.fist()`): a rounder fist with four folded knuckles, a short thick middle finger rising from the
second knuckle (about ¾ of the fist's height), the thumb wrapped in front, the wrist merged into the arm. The arm is half
the length (≈ 120 px out from the tile) and drawn as a tube of overlapping discs, so no seams. Pumps are smaller.

## v4/v5 — your notes → what changed (voice untouched)

| you said | what changed |
|---|---|
| make the fuck finger smaller and him hold it out to the right of him with an arm | hand at 0.6×, fully below the meme card; a terracotta arm (outlined like the hand) extends from the tile's right side on "usage" with a closed fist, the finger flicks up on "limit", the arm pumps on "one"/"day", pumps higher and wags on "reset" |
| "if you do this" → show only the Tenor "think about it, use your brain" GIF | the brain is gone; on "if" the whole 940×560 panel becomes that GIF (square source cover-cropped to the face and the tapping finger, rounded corners), nothing else on it |


## v3 — your notes → what changed (voice untouched)

| you said | what changed |
|---|---|
| make the finger animation better; no emoji, an orange fuck finger, bigger | a drawn terracotta hand (`scenes.fist()`, 4× with a dark outline, creases, knuckles, highlight): a closed fist rises out of the Claude tile on "usage", the middle finger flicks up with a spring on "limit", the hand pumps on "one" and "day", pumps higher and wags on "reset"; ~300 px tall |
| remove "Usage limit reached" | pill gone |
| move the Claude icon and finger to the middle | tile and hand centred under the meme card |


## v2 — your notes → what changed (voice untouched)

| you said | what changed |
|---|---|
| make him actually hold the bazooka, look better, higher res, more engaging | boxes 380 px; the launcher redrawn at 4× with shading (cylinder gradient, wooden guards, olive warhead + ochre nose, optical sight with a glint, sling swivels) and held: two navy sleeves out of Dario's box, a hand on the pistol grip and one on the forward grip, the tube across his chest below the chin; badge moved to the box's top corner |
| make the drop faster, there is a delay after the transition | the smoke clears in 0.43 s (was 0.7) and the tile is already falling through it: it lands on **"Opus"** (squash, dust, kick, thud) and that landing writes the wordmark; "5.5" pops; on "just" it jumps and lands again on **"dropped"** |
| remove the things under Claude Opus 5.5 | pills gone |
| cut the meme so Peacock isn't included, make it wider/larger | Office GIF cropped to its 16:9 face window (mark cut), card now 940 px wide |
| under the meme show Claude pull up a fuck finger instead of the week schedule | (v2: emoji + pill; replaced in v3 by the drawn hand, see above) |
| "if you do this" → a high-res giga brain, not the claude.md clicky thing | file icon + cursor removed; the Microsoft Fluent 3D brain (256 px source, shown at native size) pops on "do" and goes giga on "this": grows, warm glow bursts, sparks fly |
| make the routing lines curvy | the three dispatch connectors are cubic S-curves that draw progressively |


Sources (neither file was modified):

| file | role |
|---|---|
| `~/Downloads/C1335.MP4` | camera, portrait via rotation metadata — **picture** |
| `~/Movies/2026-09-23 08-53-58.mov` | OBS recording — **voice** (studio mic). The picture in it is a static Claude Code window, not a prompter, so the script is the Scribe transcript. |

## ⚠ Three things to know first

1. **"Claude just killed Astra" checks out.** Astra is OpenAI's GPT-6 Astra (launched 3 Sep 2026 — TechCrunch, CNBC),
   and Claude Opus 5.5 was announced yesterday, 22 Sep 2026 (anthropic.com/claude-opus-5-5). Every number on screen is
   from that page: "40% cheaper than Opus 5", "30% faster output", the date.
2. **You did not record a "just saved your usage limit" line.** The brief asked for the celebration GIF on it; the
   takes go "And boom, that one change means that Claude is now not always gonna use Fable now." The Wolf of Wall
   Street dance bursts in on **"And boom"** instead (with confetti) and flies out on "means". If you want the literal
   line, re-record "And boom, that just saved your usage limit." and it drops in as its own beat.
3. **The DM keyword is SAVE.** Scribe heard "just come and save" — the caption reads "just comment SAVE" (one merge in
   `fix_words.py`). `CLAUDE-md-prompt.md` in this folder is the file the reel promises; wire the Blotato automation when
   you want it (keyword SAVE, one link, account-wide trigger).

## What you asked for → what shipped

| you said | what it became |
|---|---|
| Dario left, Sam right, square boxes, Claude icon on Dario, ChatGPT icon on Sam | two 360 px square photo boxes (Wikimedia Commons, CC BY 2.0: Dario Amodei 2023 / Sam Altman TechCrunch 2019, cropped to face each other), names under them, the Claude tile and the official ChatGPT App Store icon as corner badges |
| a bazooka instead of the gun, Dario shoots Sam | RPG-style launcher shouldered along the top of Dario's box, levels on "Claude just", fires on "killed" (backblast + muzzle flash + recoil + launch sound), rocket with a smoke trail, impact on "Astra": Sam's box shatters into four photo shards |
| explosion that takes the entire screen, clean transition | fireball grows from the impact to cover the whole 1080×1920 by the last frame of the hook, then cools to grey smoke and clears over the first 0.7 s of the next beat (`parts/bazooka.py::explosion`) |
| clean animation for "Opus 5.5 just dropped" | "Claude Opus 5.5" writes on "Opus", "5.5" pops terracotta, a shadow grows on the ground, the tile plummets from off-frame on "just" and lands on "dropped" (squash, dust, camera kick, thud), three sourced pills stagger in |
| "if you are like me" → the Office GIF | full-screen meme card (Giphy 6f15PceJUw8WGlj4uu at 30 fps), the Claude usage-limit banner slides under it on "usage limit", the week strip marks reset (green ↻) and the next day (red ✕) |
| mimic the UI of Claude for the CLAUDE.md | the Claude Code desktop app recreated (`parts/claudeapp.py`): sidebar, project groups, "Albert · Max", prompt field, the "Fable 5.1 · Medium" chip. Create → the tab pops; write → lines typed on your words; "Use Opus 5.5" → the model picker opens and the cursor picks Opus 5.5, the chip swaps; "the rest of this prompt" → the remaining lines stream in and the file saves |
| clean animation when I explain how it works | "And boom": Claude tile + CLAUDE.md chip dispatches three sub-agent cards; on "Fable" two chips flip Fable 5.1 → Opus 5.5 (green), "not always". "It's gonna determine itself": a sub-agent list whose chips spin like a split-flap until each locks on its word (Opus 5.5 / Fable 5.1 / Opus 5.5), checks on "use" |
| celebration GIF | Wolf of Wall Street dance (the Pinterest GIF) on "And boom" — see ⚠ 2 |
| memes 1–2 times per video, in the skill | done: `reel-clean/references/memes.md` (where a meme belongs, how to find one, size/card rules), rule 29 in SKILL.md, `helpers/gif_frames.py` |

## Audio source and sync

`edit/master.mkv` = camera picture + OBS mic. Offset by brute-force envelope correlation (estimator validated on a
synthetic +1234 ms shift first): **OFF = 5.695 s**, 0.87–0.94 correlation on 9/9 windows, drift −27 ppm (−4 ms over the
take → constant offset). Residual of the built master against the camera's own audio: **0 ms**. Noise floor: camera
−60.0 dBFS vs mic **−98.2 dBFS**.

## The cut — 12 beats, last take wins (`build_cut.py`)

| # | beat | mode | line | master range |
|---|---|---|---|---|
| 1 | hook | full, 1.12× | Claude just killed Astra. | 10.66–12.16 |
| 2 | opus | full | Because the brand-new Opus 5.5 just dropped, | 23.99–27.08 |
| 3 | solves | split | and it solves a massive issue within these frontier models. | 39.23–42.06 |
| 4 | likeme | full | Because if you're like me, you run into your usage limit one day after reset. | 55.87–59.64 |
| 5 | but | split | But Opus 5.5 can solve it if you do this. | 73.07–75.88 |
| 6 | create | split | Create a CLAUDE.md file | 78.10–79.84 |
| 7 | write1 | full | and write, "Never do the work yourself. Always dispatch a sub-agent." | 91.27–94.69 |
| 8 | write2 | split | And then also write, "Don't always use Fable. Use Opus 5.5 for easier tasks." | 103.20–108.00 |
| 9 | rest | split | And then you want to include the rest of this prompt in the CLAUDE.md as well. | 113.04–116.27 |
| 10 | boom | full | And boom, that one change means that Claude is now not always gonna use Fable now. | 134.54–138.59 (pinned to the trough before the aborted "It's") |
| 11 | determine | split | It's gonna determine itself what model to use. | 144.56–146.88 |
| 12 | cta | split | If you want to know exactly what to write in the CLAUDE.md, just comment SAVE, and I'll send it over to you completely for free | 155.28–160.25 |

Takes dropped: three stumbled "Create a claude.md file and write, and tell it…", the "Use 5.5" take without "Opus",
five aborted "And boom…" starts, "It's gonna, it's gonna" and "It's gonna determine, it's gonna" restarts, the
"if you want the prompt, if you want the, if you want the claude.md" run-up to the CTA.

## Scene table

| beat | surface | on the word |
|---|---|---|
| hook | photo boxes + held bazooka | boxes half-in on frame 0 · launcher levels "Claude just" · fires "killed" · impact + shards + fireball "Astra" · full frame by the last frame |
| opus | smoke clears → tile lands, wordmark, second drop | tile falls through the smoke, lands "Opus" (writes the wordmark) · "5.5" pops · jumps "just" · lands again "dropped" |
| solves | Claude / ChatGPT / Gemini tiles with usage bars | tiles land 0–0.3 s · bars fill red "massive" · red frame "issue" · tiles hop "frontier"/"models" |
| likeme | The Office meme card (940 px) + Claude holds the finger out on an arm | card 0 s · arm extends right "usage" · finger flicks up "limit" · pumps "one"/"day" · big pump + wag "reset" |
| but | Opus 5.5 tile + red bar → green, then the "use your brain" meme | tile "Opus" · bounce "5.5" · hop "can" · drains "solve" · check "it" · meme takes the panel "if" |
| create | Claude Code window | "+ New" click 0.26 s · CLAUDE.md tab "CLAUDE.md" · caret + click "file" |
| write1 | Claude Code window, big | line 1 typed "Never…yourself." · line 2 "Always…sub-agent." · sub-agent chip "sub-agent" |
| write2 | Claude Code window + model picker | line 3 "Don't…Fable." · picker opens "Use" · cursor walks Fable → Opus 5.5 · picked on "5.5" · line 4 · "Model changed" banner "easier" |
| rest | Claude Code window, lines stream | 9 lines from "include" (one per 0.11 s, paste flash) · save wash + tab check "CLAUDE.md" · scrolls back to the top "as" |
| boom | celebration meme → dispatch diagram | GIF + confetti "boom" · flies out "means" · Claude tile + CLAUDE.md chip · cards "now"/"not"/"always" · chips flip "Fable" · green pulse "now." |
| determine | sub-agent list | rows in 0–0.3 s · chips spin · lock "determine"/"itself"/"model" · checks "use" |
| cta | Instagram comments + chip | chip slides in "exactly", writes to "CLAUDE.md" · field focused · "SAVE" typed "comment" · posted "and" · chip blue + plane "send" · liked "free" — *link/guide chip rejected 25 Sep 2026: copy the comment UI only, no link pill* |

## Sound (`mix.py`, 97 cues)

Caption clicks on the first/last word of every full-screen group (−25 hook, −27 later). Bazooka launch −13 dB on the
fire, rocket hiss −24, explosion −9 + whoosh −20 on the impact. Thud −15 on both tile landings ("Opus", "dropped"), whoosh on the jump; whoosh −29 on the fist rising and −28 on the big pump, pop −25 on the finger flick, −24 whoosh on the giga brain; pops −27…−32 on every
landing (pills, tiles, chips, checks, day squares); first-click −26 on every UI press (file, "+ New", picker open, pick,
post, like); whoosh −29…−31 on fills, drains, streams, flips and the card fly-out. Music: the approved Timeless excerpt
at −29 LUFS with sidechain ducking. Synth SFX are made by `make_sfx.py` (bazooka-launch, rocket-flight, explosion, thud).

## Verification (signal-based — no perceptual listening available)

- Scribe on the final cut reads the whole script as intended; the splice audit reads every join as one sentence
  (the only flag is the intended repeat "gonna use Fable now. It's gonna determine").
- `check_provenance.py`: every unretimed take correlates 1.0000 with the master at ≤ 0.5 ms lag (hook is 1.12×, excluded).
- `check_air.py`: no quiet run ≥ 0.30 s (one 0.23 s ring-out inside the CTA take).
- `check_motion.py`: no beat held still over 0.60 s (v2 longest runs: create 0.60, opus 0.57, write1/rest 0.53, but 0.47, solves 0.40, cta 0.27, write2 0.23, boom/determine 0.17, likeme/hook 0.07).
- `check_frames.py`: no blank frame (min frame std 4.08); 0 frames with ink in the top 180 px outside the declared `fx`
  windows (the full-frame fireball 0.89–2.08 s, the tile falling in 1.33–2.33 s, the meme card flying out 28.61–29.04 s);
  nothing under the cinematic words on any full-screen beat.
- The final caption group ("for free") runs to the last frame; 1159 frames decode with no errors.
- Loudness of the mix: **−17.1 LUFS integrated, true peak −1.5 dBFS.**
- Presenter crop `CROP_Y=490`: hair clears the caption chip, face centred in the 1080×1062 panel.

## Not done / decisions

- No Blotato automation yet (not asked this time). Keyword SAVE, deliverable `CLAUDE-md-prompt.md`.
- Portraits are CC BY 2.0 (UK Prime Minister's Office; TechCrunch) — fine for your own reel; credit lives here.
- The picker lists Fable 5.1 / Opus 5.5 / Sonnet 5 / Haiku 4.5 — the current model line-up; the "40% cheaper" descriptor
  under Opus 5.5 is the announcement's number.
