# Visual and sound contract — YouTube Clean (16:9)

Everything in `reel-clean/style.md` about type, chrome, icons, cursors, product fidelity and "nothing static
for more than ~0.6 s" applies. Differences for long-form:

## Canvas
- 1920×1080, 30 fps (camera is 25 fps → `fps=30` on the presenter layer only; never retime the voice).
- Ground pure white `#FFFFFF`. Ink `#1D1D1F`, secondary `#6E6E73`, hairline `#E3E3E6`, accent blue `#0071E3`,
  green `#1E8E3E`, red `#FF3B30`, highlighter (255,214,10,95).
- **Presenter card (right):** x=1250, y=80, 610×920, corner radius 48, soft shadow (offset y 18, blur 28,
  black α≈70), mask antialiased (draw at 2× and downscale). Crop the camera 716×1080 **centred on his face**
  (detect or eyeball from a frame; for C1327-style framing the face centre is x≈1040 of 1920) and check a
  frame at the start, middle and end of each section — he moves. Rounded rectangle, not a background-removed
  silhouette. No border line.
- **Graphics stage (left):** x=70…1180, y=80…1000 (1110×920). Windows, pages and diagrams live here.
  Nothing important within 60 px of any frame edge.
- **Modes per beat** (alternate at meaningful lines, like the reels):
  - `split` — stage left + presenter card right. For visuals he talks alongside.
  - `full` — graphics use the full 1920×1080; the presenter card springs down to a 300×300 r=40 bubble at
    bottom-right (x=1560,y=720) or leaves entirely for the intro. Use for page zooms, big numbers, diagrams.
  - `cam` — **Albert full screen**: the camera fills the frame (cover-fit on his face, no card) and **NOTHING ELSE.**
    **NO CAPTION, ever** (Albert, 2026-09-20: "remove the captions on the full screen of me as well, everywhere in the
    video"). No lower-third, no key phrase, no emoji, no scrim — just him. `CAM_CAPS` and `camcaps.make_overlay()` are
    RETIRED; so is `scripts/camcap_clicks.py` (there is no caption left to click under). This is the DEFAULT when a line
    does not need a visual. Stretches of 6–15 s per mode; do not flip modes every sentence.
  - `face` — presenter card eases to centre-right and grows (900×920 at x=510) for opinion lines with only a
    caption. Use sparingly, ≤ 6 s.
  Card moves are 0.35 s `smooth()`; never cut the card position between two frames.

## Minimal by default — every recreated visual (Albert, 2026-09-20: "there is a little too much going on… keep it super simple and minimalistic so it doesn't get overwhelmed")

A frame should read in ONE glance. Build the simplest frame that carries the line he is saying, then delete something.

- **ONE idea per frame.** The visual answers exactly the sentence he is on. If it needs two ideas, it is two frames in sequence.
- **THREE THINGS MAX on the stage at once**, counting anything the eye lands on: a window/diagram, a label, a number, a
  caption. The subject counts as one. When a fourth wants in, remove one first — or split it across time.
- **NO EXPLANATORY SENTENCES anywhere on the stage.** The reject that made this rule: `Reply to "Hey, how are you?"
  $0.0020 on Claude Opus 5` under the routing diagram. His voice already said it. If the NUMBER is the point, show the
  number alone, next to the thing it belongs to (`$0.0020`, one accent colour), and nothing else.
- **Labels are ≤ 3 words** and name a thing ("Customer service agent", "hard · expensive"). Never a sentence, never a
  restatement of the caption, never a description of what just happened.
- **Cards and tiles carry a HEADLINE ONLY — no description line under it** (Albert, 2026-09-20: "this would ideally also just
  be headline, not 'Ask a multiple choice question'"). The little picture inside the card already shows what the thing is:
  `Choice` / `True / false %` / `Score`, and nothing else. Same for list items, steps and comparison columns — a name, not a
  name plus an explanation. If the name alone does not land, the name is wrong; fix the name instead of adding a sub-line.
- **Never say the same thing twice on screen.** Caption OR number OR label — pick the one that lands, drop the rest. If
  the caption says it, the stage stays silent.
- **One accent colour per frame** (the number or the active path), everything else ink/grey. No second highlight.
- **Empty space is the design.** Roughly half the stage stays empty; a smaller, calmer frame beats a full one.
- **Nothing accumulates.** An element leaves when he stops talking about it — a diagram must not end the beat carrying
  every label it collected along the way.
- **Reviewer check (on a frame, not from the code):** count the things on the stage; more than 3, or any sentence-shaped
  text outside the caption line, or a second accent colour = major. Ask "could this frame lose one element and still say
  the line?" — if yes, it is not done.

## Captions
**Captions exist only on the white stage (`split` / `full`), never over the camera.** `cam` is always bare
(Albert, 2026-09-20) and `screen` carries no text at all (Albert, 2026-09-19/20) — so a caption can only ever sit
on a recreated visual.
- Body: not every word. Key phrases only, 1–4 words, SF Pro Semibold 64–84 px, sentence case, ink on white,
  word-by-word entrance (8 px rise + fade, 0.18 s), inside the stage's negative space, never over the card.
  Emphasis word may be New York italic or coloured (green payoff, red problem).
- **Real Apple emoji**: render from `/System/Library/Fonts/Apple Color Emoji.ttc` at its native 160 px strike
  (`ImageFont.truetype(path, 160)` + `embedded_color=True`) and scale; for anything larger than ~200 px
  redraw it (see `reel-clean/template/examples/eyes_hook.py`). Never a non-Apple emoji font, never tofu —
  check the frame.
- Intro: full-screen cinematic captions as in the reels (editorial_caption.py), bigger (120–170 px), with the
  mouse-down click on first and last word of each group.

## Intro (section 00) — edited differently
- Pace: a new visual every 1.5–3 s, mostly `full` mode, hard number payoffs (count-ups landing on the spoken
  word), recreated viral post with the view counter ticking, quick push-ins. Presenter appears for the
  "in this video I'll show you…" promise, then a clean title/transition into section 01.
- Voice may be tightened harder than the body (no air between list items; hook ~1.08–1.12× only if there is
  no face on screen for that stretch).
- **Music: tense, non-copyrighted.** Sources in order: a track Albert supplies → YouTube Audio Library /
  Pixabay Music / Uppbeat free tier (keep the licence URL + track page in `audio/LICENSES.md`) → generated
  (ElevenLabs Music or the Higgsfield/Topview music tools; ask before spending credits). Tense = minor key,
  pulsing low synth / ticking, 100–125 BPM, a riser into the first number and a drop-out or hit on
  "let's get into it". about −30 LUFS under the voice (−26 was too loud for Albert) with gentle sidechain, 1.5 s tail into section 01.
  Never chart music.
- Body sections: no music by default, or a very low neutral bed (−34 LUFS) if Albert asks. SFX: one click per UI press, whoosh only on mode
  changes (−31). **No pop / bubbly sounds anywhere** (Albert, 2026-09-18) — arrivals are silent.

## Screen share (`screen` mode) — the clean layout (Albert, 2026-09-19: "needs to look clean always… cut off the top browser… align everything")
Screen-share-heavy videos (demos, walkthroughs; he records with Screen Studio, auto zoom baked in) use the REAL capture, cleaned:
- **Never the raw recording.** `scripts/build_screen.py <project>` makes `sections/<sec>/screen.mp4` on the section's exact timeline:
  browser/OS chrome (menu bar, tabs, URL bar, bookmarks ≈ top 150 px of 1080) detected per frame and cropped — also while Screen
  Studio zooms in/out — fixed 1920×930 output so the card never changes shape, and a 5-frame cross-dissolve on every voice cut
  (a hard jump cut inside a moving zoom looks broken; the camera keeps its hard cut). The mediator reads `review/screen_sheet.jpg`
  and writes script / private spans into `screen_spans.json` — those are forbidden.
- **One grid** (`lib/layout.py` SCREEN / SCREEN_CARD, drawn by `lib/screenshare.py`): capture card 1480×716 r28 at (60,182), 40 px gutter,
  slim presenter card 280×716 r36 at (1580,182). Same top, same bottom, 60 px frame margins, white ground, soft shadow, 2 px
  hairline, **no fake browser chrome**.
  **NO TEXT AT ALL while the screen share is on screen** (Albert, 2026-09-19/20: "I don't like it above the screenshare, and I
  don't like it below the screenshare"): no title line above the card (`SS.title` is retired — do not call it), no key-phrase
  caption below it, no number call-outs, nothing over the capture. Just the capture card, the presenter card and white ground.
  The screen and his voice carry the meaning; point at things with a focus push-in or an accent ring on the value itself.
  Text stays only in `cam` (him full screen) and in recreated `full` visuals. Tune FACE_CX so his face is centred in the slim card.
- **Zoom — GENTLE (Albert, 2026-09-20: "we zoom in a little too much too often… zoom out a little, but still make it look good"):**
  Screen Studio's own zooms are kept and usually enough. Add a `FocusTrack` push-in only when the thing he is talking about is
  genuinely unreadable at 1× on a phone, and then **1.2–1.4× is the normal amount, 1.6× the hard cap** (was 2.2×, too much).
  At most ONE push per screen stretch, moves ≥ 0.8 s, hold ≥ 4 s, and back to 1× when he moves on. Default to no push at all;
  an accent ring on the value reads better than a big zoom. Never chase the cursor, never zoom while Screen Studio is already
  moving (`SCR.zoomed(T)` changes), never push onto content Screen Studio just zoomed out of.
  Recreated `full` visuals (a tweet, a page, a card): the same restraint — ≤ 1.4×, one slow move, no pumping.
- **Face in the slim card:** his head (430-500 camera px) is wider than the card's 422 px crop. Centre on the EYES/NOSE
  (Vision landmarks), keep the path per camera shot, and crop the back of the head / ear — never the brow or face side.
  Face box / jaw-contour centres drift when he turns to his screen and put the face against the edge (03 went 3 rounds).
- **Pacing:** slow. Screen-share sections are mostly `screen` (60–80 %), with `cam` for lines where nothing happens on screen and
  `full` for the ONE explainer animation of the section (e.g. how routing works: question → Jev score → cheap / expensive model).
  The ~50 % cam rule applies to talking sections, not to demos. Stretches ≥ 8 s; enter/leave `screen` on a sentence start.
- Highlights are allowed on top of the capture (rounded 3 px accent ring or highlighter sweep on the value he reads — NOT a
  caption / number call-out) — placed from a frame you LOOKED at, faded in/out, removed before the next cut/zoom.
- Private stuff: bookmarks and tabs are gone with the chrome; still check every used stretch for inbox lists, chat sidebars,
  account e-mails, API keys → blur (Gaussian 18) or focus away.

## Intro revisions Albert asked for (2026-09-19)
- Cold open on a real moment (coffee sip) with a slow eased push-in (`scenes.cam_zoom`) = "fun hook"; music starts after it
  (`stitch.json` music `start_at`) so the natural sound plays.
- When he says something happened on his screen ("you are in", "join the waitlist"), show his REAL screenshare there, even in
  the intro — cut it from any moment of the recording with `scripts/build_screen_clip.py` (clean, chrome-free) instead of recreating it.

## Section boundaries
- First and last 8 frames of every section: white ground + presenter card in the `split` position, no
  graphics mid-animation, so any two sections butt-join cleanly. Audio has 4 ms fades, no music tails
  except intro → 01.

## Pacing for the WHOLE video — intro and body (Albert, 2026-09-18 — the first cut felt "almost stressful to watch")
- Roughly **50 % Albert full screen (`cam` mode: camera fills the frame, lower-third caption only) / 50 % visuals**.
  A visual appears only when the line actually needs one; otherwise it is him, full screen, with a key-phrase caption.
- He likes the recreated tweets / X posts — keep those. Keep the number hook. Drop gag windows, charts, chips and anything
  that is "animation after animation". No visual shorter than ~2.5 s; fewer, longer-held surfaces.
- Music: if Albert supplies a track, use it (first two sections, continuous across the join, identical fixed chain in both:
  volume so the bed is ≈ −30 LUFS pre-duck → sidechain 0.03 / 2 / 15 / 250; fade-in 0.5 s at the start of 00, 3 s fade-out
  at the end of 01; no ending hit between them).

## Words and emoji (Albert, 2026-09-18)
- **Never use the ninja emoji 🥷** ("could be seen as racist"). More generally: no emoji depicting a person in a role that
  stands in for an ethnicity, culture or stereotype; when unsure, use an object emoji or none.
- **Censor swear words in on-screen text with an asterisk**: "sh*t", "f*ck" — the audio stays as spoken.

## Accepted / Rejected (append with dates)
- 2026-09-20 rejected: recreated tiles/animations standing in for something he actually has on tape. When his capture
  shows the thing, show the capture (`screen` = his face in the slim card + the real screen) — he asked for exactly
  that in place of a recreated editor window, the Remotion/HyperFrames logo tiles and the eyes-emoji beat.
- 2026-09-20: swear words are BLEEPED in the audio (1 kHz tone over the word), as well as censored in on-screen text.
- 2026-09-20 rejected: sub-lines under card headlines ("Choice / Ask a multiple choice question"). Headline only.
- 2026-09-20 rejected: the cost line under the routing diagram — `Reply to "Hey, how are you?" $0.0020 on Claude Opus 5`
  ("a little too much going on"). A bare `$0.0020` beside the model node would have been right. See "Minimal by default".
- 2026-09-20 REJECTED and reversed: captions over `cam` (him full screen) anywhere in the video — "remove the captions
  on the full screen of me as well". CAM_CAPS / camcaps.py / camcap_clicks.py are retired. (This supersedes the earlier
  2026-09-20 note that accepted the caption click under full-screen captions — there are no full-screen captions now.)
- 2026-09-20 rejected: strong push-ins. Zoom less often and less far: 1.2–1.4× normal, 1.6× cap, one per stretch.
- 2026-09-20 rejected: ALL text while the screen share is on screen — the caption line under the card ("< 100 ms", "$0.0007",
  "Saved 80%", "Passed ✅") AND the title line above it ("Playground · Multiple choice"). "I don't like it above the screenshare,
  and I don't like it below the screenshare." Capture card + presenter card + white ground only; point with zoom / accent ring.
- 2026-09-19: Albert liked the coffee-sip cold open + real screenshare intro ("really good") and REMOVED the intro music on this
  screen-share video — ask before adding music to a demo-style video; the natural cold-open sound carries it.
- 2026-09-19: screen-share layout introduced (chrome-free capture card + slim presenter card on one grid, dissolved cuts). Sent, not yet accepted.
- 2026-09-18: layout requested by Albert — white ground, rounded presenter card on the right, Apple-style
  animation, recreated UI, real Apple emoji, tense intro music. (No section accepted yet.)
- 2026-09-18 rejected: the pop / bubbly arrival sound (`pop.mp3`) in every section; intro music at −26 LUFS was a little too loud → start the bed around −30 LUFS pre-duck.
- Carry over from reels — rejected: command bars over icons, "FREE" badges, empty outlines, white podiums,
  card-shake + no-entry sign, chart pop songs as background.
