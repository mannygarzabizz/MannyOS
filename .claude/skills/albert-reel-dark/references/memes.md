# Memes in a reel (added 23 Sep 2026, Opus 5.5 / CLAUDE.md reel)

Albert: "update the skill to be able to find good memes 1 or 2 times in the videos as well."
A meme is a reaction shot for a line that is about a *feeling* the viewer shares. It replaces the recreated UI for
that beat; it never replaces a proof beat (numbers, real pages, the product).

## Where a meme belongs (one to three per reel)

| line type | example from the script | meme job |
|---|---|---|
| "if you're like me…" / shared pain | "you run into your usage limit one day after reset" | grimace / cringe (The Office, Michael Scott wince) |
| the payoff / "and boom" / "just saved you…" | "And boom, that one change means…" | celebration (Wolf of Wall Street dance, Leo cheers) |
| "how the f*ck" / disbelief | "How is that even possible?" | jaw-drop, blinking-guy, confused math lady |
| "if you do this" / "think about it" | "can solve it if you do this" | Tenor "think about it, use your brain" (head tap) - Albert sent it; it replaces the whole panel |
| a rival's failure | "…and it just died" | Homer into the bush, Drake no/yes |

Rules that came out of the 23 Sep reel:
- The meme lands on the *feeling word* ("like me" / "boom"), not on the first word of the beat, and something else
  must already be moving on frame 0 (a card sliding in, the previous prop wobbling).
- One meme card per beat, the full 940 px wide, in a rounded 26 px card with the usual soft shadow, on the off-white
  ground. No border, no caption inside the card. **Crop the platform watermark out** (Peacock, Giphy, Tenor) - Albert asked
  for the Peacock mark to go; `gif_card(name,t,w,crop)` takes the crop as fractions of the frame width.
- When he names a GIF for a line ("show this only"), the GIF is the whole panel: cover-crop to 940×560, nothing else on it.
- Play the GIF at its own pace (30 fps resample of the GIF's frame durations), loop if the beat is longer than the GIF.
- A meme beat can still carry one product element under it (the usage-limit banner under the Michael Scott card);
  the celebration meme flies out on the next spoken clause so the explanation can start.
- Full-screen for the "like me" moment (face-less, caption underneath); a split panel is fine for a celebration.

## Finding one

1. **Albert's links first.** He usually pastes a Giphy or Pinterest URL. `curl -sL <url> -o assets/gif/<name>.gif`;
   a Giphy page URL becomes the file at `https://media.giphy.com/media/<id>/giphy.gif` (any `media0-4` host works).
2. **Otherwise search Giphy/Tenor in the built-in browser** (no API key needed): open
   `https://giphy.com/search/<two-word feeling>` (e.g. `awkward-grimace`, `celebration-dance`, `mind-blown`), pick a
   result from a known show/film (The Office, Parks and Rec, Wolf of Wall Street, Succession, SpongeBob) - recognisable
   beats obscure. Read the GIF id from the result URL (`/gifs/<slug>-<id>`) and download `media.giphy.com/media/<id>/giphy.gif`.
   Tenor: `https://tenor.com/search/<phrase>-gifs`, the media URL is in the page's `og:image` / `contentUrl`.
3. **Check it before drawing:** open frame ~10 (`python3 helpers/gif_frames.py assets/gif/x.gif --peek`) and read it.
   It must be a face reaction that reads at 760 px wide in 0.5 s. Reject text-heavy memes, low-res (< 400 px) GIFs
   and anything with a burned-in caption that fights the cinematic words.
4. **Convert:** `python3 helpers/gif_frames.py assets/gif/x.gif assets/gif/<name> 900` writes 30 fps JPEG frames
   sized for the card; `scenes.gif_card(name, t, width)` draws frame `int(t*30)` with rounded corners.
5. Say in the README which meme, from which URL, and on which word it lands. Memes are third-party footage: fine for
   Albert's own reels, never for client work without asking.
