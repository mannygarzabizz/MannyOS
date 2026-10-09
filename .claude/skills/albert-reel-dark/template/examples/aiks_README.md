# "AI just killed all software" reel — 22 Sep 2026 (v8)

`renders/FINAL-ai-killed-software.mp4` — **54.63 s**, 1080×1920, 30 fps, H.264 / AAC 48 kHz.
`renders/clean-voice.mp4` — same picture, recorded voice only (no music, no SFX).

Sources (neither file was modified):

| file | role |
|---|---|
| `~/Desktop/C1334.MP4` | camera, portrait via rotation metadata — **picture** |
| `~/Desktop/2026-09-22 09-22-22.mov` | OBS recording of the teleprompter — **voice** (studio mic) |

## v8 — smooth shell game with both arms, Shiney.ai

| note | what changed |
|---|---|
| "the cups animation cuts, not smooth, flickers; make it smooth and use both arms" | the shell game is now **one continuous choreography** (`cupsgame`) that both beats draw from (the second beat continues at `t + worry duration` and no longer re-enters the card, so the cut is invisible). Cups and both hands are position tracks with smooth blends between phases: left hand takes the left cup, right hand the right one, they cross on both shuffles; the right hand lifts the Salesforce cup on "never" and throws it on "in", the left hand throws the middle cup on "begin" and the last one on "actually"; the right hand rests on the wiggling hat and takes it off after "else" while the left hand does a ta-da |
| "instead of site.com always use Shiney.ai" | the accounting tool's tabs are `shiney.ai/…`, the Google local-pack row is **Shiney.ai Accounting**; skill rule updated |

## v7 — the throws start on "was never", spread out

| note | what changed |
|---|---|
| "start the throwing much earlier, when I say 'was never', so it doesn't feel rushed" | the cups now go across both beats, ≈0.9 s apart: on "never" the Salesforce cup lifts (empty), on "in" it is hurled away, on "begin" the second cup goes, on "actually" (next beat) the last one; the hat wiggles under his hand while he says "hidden somewhere", comes off right after "else", money on his head, pulse on "sight" |

## v6 — throw the cups, taller bar card, no sub-lines, the 🤔

| note | what changed |
|---|---|
| "when I say 'it's actually somewhere else' take each cup and throw it away, until it opens the hat at the end; faster" | `hidden`: Claude grabs a cup on "actually", "hidden" and "somewhere" and hurls each off the table (spin, gravity); right after "else" the hat flips off and the money is on his head, green pulse on "sight" |
| "'not compared to this' goes out of frame — make the frame taller" | `alot`: 940×620 card; the grey "?" bar shoots up to 60 px below the card top and bounces off it, always in frame |
| "remove these under-headlines" | grey sub-lines removed under "Software" / "Services" (`six`), "US companies" (`spend`) and "September books" (`done`); skill rule 24 |
| "'and why is that' — the thinking emoji we used in other reels" | `why`: the 4K-keyed Apple 🤔 from the 19 Sep reel pops in, rocks, hops on "why", shakes on "that?", question marks spring in around it |

## v5 — the cups, polished

| note | what changed |
|---|---|
| "Give Claude orange arms instead" | curved terracotta arms with darker hands, same colour as the tile |
| "trigger the money under the hat quicker" | the arm is on the hat during "else / in", the hat comes off in 0.18 s right after "plain", the money springs out at once, so it is already showing when he says "sight" (green pulse on the word) |
| "make it look more premium" | shaded cups (gradient body, rim band, specular, darker foot) on a table board with a soft shadow, soft shadows under the cups, a shadow under the hat brim, a green glow behind the money, the moving cup arcs while the other slides flat |

## v4 — Albert's third round of notes, applied

| note | what changed |
|---|---|
| "plain sight: have the cups, with Claude in the background doing the shuffling, with a hat on; the money under the hat, so the hat is lifted" | `worry` + `hidden` share one table: the Claude tile stands behind it in a top hat (🎩), two ink arms follow the cup being moved. `worry`: two shuffles, the Salesforce cup lifts on "never" — empty. `hidden`: two more shuffles on "hidden / somewhere", all three cups lift on "else" (nothing), the arm goes to the hat on "plain", the hat comes off on "sight" and the money (💵) is on his head, green frame |
| "US companies: show the US country figure, engaging; find it on the internet; skill should usually work like that" | `spend`: the contiguous US drawn from real geodata (PublicaMundi `us-states.json`, ink with white state lines) wipes in on "US", ten Fluent 3D office buildings pop on real city coordinates on "companies", then the flap counter. Skill rule 22 added |
| "acting as service companies doesn't work, come up with a better animation" | `service`: a recreated Google search for **accountant near me**: query types, tabs, "Businesses" with two firms; on "acting" the AI company (Claude tile, "AI · Accounting service · Open now") slides in at the top of the local pack, the row highlights on "as", the chip goes green on "service", the cursor presses **Book** → **Booked ✓** on "companies" |
| "the click on the skills is messed up, slower clicks" | `skills`: picks on "skills / that / know" (≈0.4 s apart), adjacent chips, the cursor glides between them |
| "remove the free guide popup" | `cta`: the cover card is gone |
| "don't make your own person figures; find icons online; update the skill" | no drawn figures remain anywhere; skill rules 21–23 + style notes added (Apple emoji, Fluent 3D emoji, App Store icons via the iTunes API, GeoJSON outlines) |

## v3 — Albert's second round of notes, applied (superseded where v4 says so)

| note | what changed |
|---|---|
| "plain sight: do a street lamp that is not wide, and a cash bill hidden behind it" | `hidden`: a narrow drawn street lamp in the centre; the bill slides in **behind the post** on "hidden" (most of it showing — that's the gag), the lamp switches on and lights it on "somewhere else", the bill jumps out in front, bigger, with a green frame on "sight" |
| "redo the next billion-dollar companies: have Claude shoot again, on a bunch of SaaS icons like Salesforce, Notion" | `next`: Claude with the SMG again (`parts/shootout.py`); six official App Store icons — Salesforce, Notion, Slack, HubSpot, Zoom, Dropbox — stack into a 3×2 wall on "billion-dollar companies"; full auto from "won't", three rounds per tile sweeping the wall, each tile shatters on its third round, the last on "companies" |
| "acting part: an email that says 'Accounting is all done' from Jeff, an arrow pointing to Jeff who is an AI sitting at a MacBook" | `service`: an Apple-Mail message from **Jeff** ("Accounting is all done", body types in) on the left; Jeff — the AI-headed figure — sits typing at a drawn MacBook on the right; on "acting" a terracotta arrow draws from the sender name to him; "Jeff · AI" tag on "service"; his screen shows **Sent ✓** on "companies" |

## v2 — Albert's first revision notes, applied

| note | what changed |
|---|---|
| "hidden… should be a bush it is searching, then find the money; in the middle" | `hidden`: a drawn bush centred in the card, the magnifier searches it (the glass sees the cash inside), the cash pops out of the bush on "sight" and the lens moves aside |
| "750 billion: include all the 0, redo the animation so it's cooler" | `spend`: a split-flap counter, **$750,000,000,000** — tiles flip in already spinning on "right now", lock left→right across "seven hundred and fifty", the last zero on "billion" with the ink frame |
| "this looks weird, show better icons / emoji figures" | `jobs` + `why`: Microsoft Fluent 3D emoji figures (office worker, judge, man in suit, artist) in white tiles — Apple's profession emoji are ZWJ sequences Pillow cannot shape here |
| "never wanted a tool… show it closing down a lot of tabs" | `tool`: a browser with ten `shiney.ai` accounting tabs; the cursor closes them one after another from "never" to "accounting", pages swap each time, the empty window collapses |
| "accounting done for them: a button it clicks, then a popup Complete with checkmark, inside the computer, not the terminal" | `done`: on the MacBook an Accounting app with a terracotta **Do my accounting** button — cursor presses it on "accounting", spinner, three tasks tick, a **Complete ✓** sheet drops on "done", OK pressed on "them" |
| "won't be AI software companies: a figure that dies; acting as: a mask it takes off; more engaging" | `next`: a drawn figure (white head with an AI badge, ink body) walks in, keels over on "won't" with ✕ eyes, a headstone rises on "software". `service`: the same figure walks in wearing a smiling service-company mask; on "acting" its arm lifts the mask off, revealing the AI head; tags swap |
| "cut the 'yes, it's completely free' at the end" | `cta` take ends after "to you" (+0.22 s ring-out); the previous cut is kept as `edit/tight-v1.mkv` |

## ⚠ Two things to know first

1. **The hook target is Salesforce.** The brief said "the most well known software logo… not Google, one of the
   software companies everyone knows". I picked Salesforce: it is the poster child of business software, the script is
   about what companies spend on software, and its cloud takes bullet holes well. The tile is the official Salesforce
   iOS app icon (App Store artwork, `assets/icons/Salesforce.png`). Swapping the target is one line: `tile_salesforce`
   in `brand.py` + the label string in `parts/hook.py`.
2. **"forever" is not in the reel.** The first hook take says "AI just killed all software forever"; the next three
   (the last one wins) say "AI just killed all software." — so the tile breaks on **software**. If you want "forever",
   change the first `select` row in `build_cut.py` to `(2.92, 5.38, 'hook')` and rebuild (the burst then runs through
   "forever" automatically).

## Fact-check (before drawing)

- **$4.6 trillion in services** — real, and sourced: Foundation Capital, *AI leads a service as software paradigm
  shift* (Joanne Chen & Jaya Gupta, 19 Apr 2024, also run by Forbes): "The push towards services represents a
  $4.6 trillion opportunity" ($2.3T of salaries + $2.3T of outsourced IT and business-process services, global).
  The article is recreated in the `services` beat and the highlighter lands on that exact sentence.
- **$750 billion a year on software (US companies)** — spoken, no single public source found. Nearest published
  figures: Gartner worldwide software spend $1.23T (2025) / $1.43T (2026); US-only estimates range $390–540B.
  It stays on screen because it is spoken (rule 17), but if you want it bullet-proof, "$1.2 trillion worldwide"
  is the Gartner line.
- **6×** — internally consistent ($4.6T / $750B = 6.1×); shown as a chip on the shared-axis chart.
- No other number is on screen except spoken ones ($1B for "billion-dollar"). The accounting table uses skeleton bars
  where amounts would be; the terminal prints check-lines with no counts.

## Audio source and sync

`edit/master.mkv` = camera picture + OBS mic. Offset measured by brute-force envelope correlation (estimator
validated on a synthetic +1234 ms shift first): **OFF = 1.106 s** (camera time T ↔ mic time T + 1.106),
0.89–0.93 correlation on 10/10 windows, drift −90 ppm (−16 ms over the 3-minute take → under half a frame at the
last take, constant offset kept). Residual of the built master against the camera's own audio: **0 ms**.
Noise floor: camera −66.7 dBFS vs mic **−98.5 dBFS**.

## The cut — 17 beats, last take wins (`build_cut.py`)

| # | beat | line | master range |
|---|---|---|---|
| 1 | hook (1.12×) | AI just killed all software. | 13.85–15.84 |
| 2 | worry | split | Shell game, both arms: two shuffles with the hands crossing, the right hand lifts the Salesforce cup on "never" (nothing under it) and throws it off on "in", the left hand throws the middle cup on "begin" |
| 3 | hidden | split | Same choreography continued (no cut): the left hand throws the last cup on "actually", the right hand waits on the wiggling hat, takes it off right after "else" — the money is on his head — and the left hand does a ta-da; green pulse on "sight" |
| 4 | spend | **full** | The contiguous US (real GeoJSON) wipes in on "US", ten office buildings pop on real cities on "companies", then the **split-flap counter** locks **$750,000,000,000** across "seven hundred and fifty", last zero on "billion"; "/ year" pill; software row on "software" |
| 5 | alot | split | Vertical bars in a taller card: the $750B bar stands tall on "a lot", shrinks on "not compared", the grey "?" bar creeps up and shoots to the top of the card on "this", bouncing off the ceiling |
| 6 | six | **full** | Shared-axis card (0–$5T): Software row; the card **grows** for the Services row on "companies"; **6×** chip on "six" as the green bar stretches; the number counts up and lands **4.6** on the word, **T** + green frame on "trillion"; the software row fades back; axis ticks arrive one by one; "source: Foundation Capital, 2024" on "dollars" |
| 7 | services | in services every single year. | (same take) + 78.20–79.97 |
| 8 | jobs | **full** | Four figure tiles (Fluent 3D emoji: office worker, judge, man in suit, artist) land on their words and re-centre as each arrives |
| 9 | why | split | The Apple 🤔 (4K keyed) pops in, rocks, hops on "why", shakes on "that?"; seven question marks spring in around it |
| 10 | tool | split | Browser with ten `shiney.ai` accounting tabs: the cursor closes them one by one from "never" to "accounting" (page swaps each time), then the empty window collapses |
| 11 | done | **full** | **MacBook**: Accounting app, Claude bounces into the Dock on "want"; the cursor presses **Do my accounting** on "accounting" → spinner → the three tasks tick → a **Complete ✓** sheet drops on "done" → OK on "them" and a Claude notification |
| 12 | humans | And up until now, this needed a lot of humans, but not anymore. | 121.72–124.74 + 125.13–125.74 |
| 13 | next | **full** | **Claude shoots the SaaS wall** (`parts/shootout.py`): Salesforce · Notion · Slack · HubSpot · Zoom · Dropbox (official App Store icons) stack up on "billion-dollar companies"; full auto from "won't", the gun aims tile by tile, three rounds each, every tile shatters on its third round, the last on "companies" |
| 14 | service | split | Google search "accountant near me" recreated: two firms in the local pack; on "acting" **Shiney.ai Accounting** (Claude tile, "AI · Accounting service · Open now") slides in at the top, highlights on "as", chip green on "service", **Book → Booked ✓** on "companies" |
| 15 | skills | split | "Skills you already have": nine chips pop in, the cursor glides and picks three adjacent ones on "skills / that / know" (green check) |
| 16 | turn | and turn that into an AI-native service business. | 159.12–161.69 |
| 17 | cta | split | Instagram comments: the guide chip writes itself, **FREE** typed on "comment", posted on "and", the chip goes blue and the plane flies on "send", the comment gets liked on "you" — *link/guide chip rejected 25 Sep 2026: copy the comment UI only, no link pill* |

- Two "pauses" I planned to tighten were not air on the 10 ms RMS profile (Scribe's word edges lag the sound): the
  0.56 s after "billion" and the 0.5 s after "trillion" are voiced, so those takes stay continuous. The `six | services`
  beat boundary is a split at the measured onset of "in" (`fix_words.py`), not a cut.
- The only tightened gap is "but | not anymore" (0.48 s → 0.12 s). "every single year" is his re-said ending, spliced on.
- Scribe spelled the numbers out ("seven hundred and fifty"); `fix_words.py` merges them to `750` / `4.6` for the captions.

## Scenes (all recreated with Pillow, no screenshots)

| # | beat | mode | surface |
|---|---|---|---|
| 1 | hook | **full** | **Claude empties a machine gun into the Salesforce tile** (`parts/hook.py`). SMG silhouette, levels during "AI just", **full auto from "killed" (13 rounds/s)**: 2-frame muzzle flash + tracer + recoil shudder + brass + a hole punched in the tile + blue chips + camera kick per round; the last round on "software" breaks the tile into three shards and the name tumbles off |
| 2 | worry | split | Shell game, both arms: two shuffles with the hands crossing, the right hand lifts the Salesforce cup on "never" (nothing under it) and throws it off on "in", the left hand throws the middle cup on "begin" |
| 3 | hidden | split | Same choreography continued (no cut): the left hand throws the last cup on "actually", the right hand waits on the wiggling hat, takes it off right after "else" — the money is on his head — and the left hand does a ta-da; green pulse on "sight" |
| 4 | spend | **full** | The contiguous US (real GeoJSON) wipes in on "US", ten office buildings pop on real cities on "companies", then the **split-flap counter** locks **$750,000,000,000** across "seven hundred and fifty", last zero on "billion"; "/ year" pill; software row on "software" |
| 5 | alot | split | Vertical bars in a taller card: the $750B bar stands tall on "a lot", shrinks on "not compared", the grey "?" bar creeps up and shoots to the top of the card on "this", bouncing off the ceiling |
| 6 | six | **full** | Shared-axis card (0–$5T): Software row; the card **grows** for the Services row on "companies"; **6×** chip on "six" as the green bar stretches; the number counts up and lands **4.6** on the word, **T** + green frame on "trillion"; the software row fades back; axis ticks arrive one by one; "source: Foundation Capital, 2024" on "dollars" |
| 7 | services | split | **Favourite move** (`parts/fcpage.py`): the Foundation Capital article recreated in Safari with the real URL, camera push-in, highlighter sweeps "services" on the word and "$4.6 trillion opportunity" across "every single year", cursor riding the tip |
| 8 | jobs | **full** | Four figure tiles (Fluent 3D emoji: office worker, judge, man in suit, artist) land on their words and re-centre as each arrives |
| 9 | why | split | The Apple 🤔 (4K keyed) pops in, rocks, hops on "why", shakes on "that?"; seven question marks spring in around it |
| 10 | tool | split | Browser with ten `shiney.ai` accounting tabs: the cursor closes them one by one from "never" to "accounting" (page swaps each time), then the empty window collapses |
| 11 | done | **full** | **MacBook**: Accounting app, Claude bounces into the Dock on "want"; the cursor presses **Do my accounting** on "accounting" → spinner → the three tasks tick → a **Complete ✓** sheet drops on "done" → OK on "them" and a Claude notification |
| 12 | humans | split | "until … now" timeline fills to "now"; twelve avatars pop in across "a lot of humans"; they grey and drop on "not", the Claude tile lands on "anymore" |
| 13 | next | **full** | **Claude shoots the SaaS wall** (`parts/shootout.py`): Salesforce · Notion · Slack · HubSpot · Zoom · Dropbox (official App Store icons) stack up on "billion-dollar companies"; full auto from "won't", the gun aims tile by tile, three rounds each, every tile shatters on its third round, the last on "companies" |
| 14 | service | split | Google search "accountant near me" recreated: two firms in the local pack; on "acting" **Shiney.ai Accounting** (Claude tile, "AI · Accounting service · Open now") slides in at the top, highlights on "as", chip green on "service", **Book → Booked ✓** on "companies" |
| 15 | skills | split | "Skills you already have": nine chips pop in, the cursor glides and picks three adjacent ones on "skills / that / know" (green check) |
| 16 | turn | **full** | Storefront drawn from scratch: the picked skills fly in through the door on "turn", windows light on "into", the Claude mark glows on "AI-native", the awning unrolls on "service", **OPEN** flips on "business" |
| 17 | cta | split | Instagram comments: the guide chip writes itself, **FREE** typed on "comment", posted on "and", the chip goes blue and the plane flies on "send", the comment gets liked on "you" — *link/guide chip rejected 25 Sep 2026: copy the comment UI only, no link pill* |

Rhythm: F S S F S F S F S S F S F S S F S — 7 full / 10 split.

## Sound

`audio/cue-sheet.json`. Twelve quiet ticks as the flaps lock, ten clicks as the tabs close, a thud when the figure lands, a whoosh when the mask comes off. The machine-gun round is synthesised (`audio/sources/mg-round.wav`: 10 ms crack + 40 ms body
+ pitch-dropping thump, tighter than the pistol so 13 rounds/s stay separate), −19 dB in the burst, −16 dB first
round, the pistol crack −15 dB + whoosh −23 on the break. Caption mouse-down on the first and last word of every
full-screen group; one click per UI press; quiet pops for landings; whooshes on flips, sweeps, camera moves and card
growth. Music: the approved *Timeless (Instrumental)* excerpt, −29 LUFS pre-duck, sidechained under the voice
(no song was picked for this reel).

## Verification — signal and frame checks only; I cannot listen

- 54.633 s, 1080×1920, 30/1 fps (ffprobe), 1639 frames. Integrated **−17.1 LUFS**, LRA 2.1, **true peak −1.5 dBFS**.
- **Provenance:** all 17 unretimed segments correlate **1.0000** with the master at |lag| ≤ 0.5 ms (48 kHz, lag-searched).
  Hook is 1.12×, excluded.
- **Air:** 0 quiet runs ≥ 0.30 s (`check_air.py`); the four ≥ 0.15 s are word gaps inside takes and the 0.22 s ring-out
  after "to you".
- **Motion:** 0 beats hold still > 0.60 s (`check_motion.py`); longest 0.60 s in `humans`, 0.50 s in `jobs`.
- **Frames** (`check_frames.py`, all 1639): min frame std 10.4 (no blank frame), **0 frames with ink in the top 180 px**,
  nothing under the captions in any full-screen beat. Dense 2-frame strips across every shell-game transition (swap ends,
  lift→throw, the worry|hidden cut, the hat) show continuous motion — no snaps, no re-entrance.
- Captions cover all 170 words; the last group ("you") runs to the final frame.
- **Scribe splice audit** (v2 cut, unchanged since): every join reads as the intended sentence; the flags are the
  sped-up hook syllables, two consonant tails and two legitimate repeats.

## Rebuild

```bash
python3 build_cut.py && python3 fix_words.py && python3 render.py && python3 mix.py && python3 qa.py
python3 check_air.py && python3 check_motion.py && python3 check_frames.py
```

`python3 render.py --preview` → contact sheet; `python3 gridstrip.py <tag> beat1,beat2 6` → several beats in one
sheet; `parts/hook.py`, `parts/shootout.py`, `parts/fcpage.py`, `parts/macbook.py`, `brand.py` each run standalone.

## Not done

- Comment-to-DM automation is **not** wired (no link was given for the guide). Keyword would be **FREE**.
- Music is the default approved excerpt; no new song was picked for this reel.
