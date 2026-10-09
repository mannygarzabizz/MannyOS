---
name: albert-carousel-ig
description: Generate Albert's signature Instagram carousels in the "hacker-light" style - warm cream background, blurred bright dev desk, 8-bit pixel-art mascot in a bright orange hoodie, bold condensed sans headlines in black + bright orange #E95223, and BIG flat app icons instead of screenshots. Flexible slide count (6 to 15). Can repurpose a YouTube video into a carousel automatically. Use when Albert says "albert carousel", "my carousel style", "carousel from this youtube video", "recreate my winning carousel", or wants an icon-first slide deck. Runs on the Higgsfield MCP, no external API keys.
---

# Albert Carousel IG (Hacker-Light Edition)

Albert's proven carousel formula, refined from his winning tech-stack post. One visual world across every slide: light mode, pixel-art mascot, big app icons, handwritten annotations. Built on the Higgsfield MCP so it runs natively in Claude Code.

This is a sibling of `famous-ig-carousel` but with ONE locked style (hacker-light), Albert's defaults baked in, flexible slide counts, and a YouTube-repurposing path.

## Albert's defaults (do not ask, just use)

- `BRAND_ACCENT` = bright orange `#E95223` (vivid, saturated, Claude-brand orange; NEVER muted terracotta)
- `SOCIAL_HANDLE` = `@albert.olgaard`
- Style = **hacker-light** only (see `references/style-hacker-light.md`)
- Footer on every slide: Instagram glyph + handle bottom-left (handwritten), bookmark glyph + `save for later` bottom-right (handwritten italic)
- CTA pattern: `COMMENT "<WORD>"` for the full guide + a pixel-art video card + handwritten `100% free of course :)`

## Prerequisites

- Higgsfield MCP connected (`generate_image`, `generate_image_batch`, `jobs_wait`).
- Roughly 1 credit per slide (6-15 slides per deck).
- A topic, a winning carousel to recreate, or a YouTube link.

## Process

### Step 1: Get the content

Three input modes:

1. **Free topic** - plan slides from the topic directly.
2. **Recreate a winning carousel** - the user shares slide images. Take ALL the text and the idea of every slide, one for one. Do NOT compress to 6 slides. Replace screenshots with icon-first layouts (below).
3. **YouTube video** - extract content yourself:
   - Title: `curl -s "https://www.youtube.com/oembed?url=<VIDEO_URL>&format=json"` (WebFetch on the YouTube page FAILS, do not bother).
   - Description + transcript: `yt-dlp --skip-download --write-description --write-auto-subs --sub-langs "en" --sub-format vtt -o "<name>" "<VIDEO_URL>"` into the scratchpad, then strip the VTT tags/timestamps with a small python script and read the transcript in chunks.
   - Plan slides from the actual transcript structure (intro hook, numbered steps/tools, use cases, CTA). Show the user the slide plan in the chat before generating.

### Step 2: Plan the slides

Flexible count, driven by content:

- Quick topic: 6-8 slides.
- Numbered tool/step list (like the tech stack post): 1 cover + one slide per item + 1 recap grid + 1 CTA. 13-15 slides is fine and performs well.
- Every deck always has: **cover** (hook + big headline + mascot scene), **content slides** (one idea each), **recap "stack grid"** when 4+ apps/tools appear (all icons in one card), **CTA** last.

NO context slides, NO transition slides, NO filler.

### Step 3: Generate the cover

`generate_image` with `model: nano_banana_2`, `aspect_ratio: 4:5`, `resolution: 2k`, using the cover template in `references/style-hacker-light.md`. (The server may downgrade to `nano_banana_flash`; that is fine, do not fight it.) Then `jobs_wait` on the job to get it terminal. Keep the cover `job_id`: it is the style anchor.

### Step 4: Generate all content slides in parallel batches

Use `generate_image_batch` (max 12 requests per call, so split e.g. 12 + 2). Every request:

- same model/ratio/resolution
- `medias: [{ "role": "image", "value": "<cover-job-id>" }]`
- prompt starts with the exact style-match line from the reference file, then the slide content.

Then `jobs_wait` in groups of up to 12 (a job may still be `in_progress` after 15s; just poll again).

### Step 5: Download + caption + deliver

- Create `outputs/carousels/<slug>/` and `curl` all PNGs **in parallel** (one command, `&` + `wait`).
- Name files by content, not generically: `01_cover.png`, `02_stripe.png`, `03_mongodb.png`, ... `NN_cta.png`.
- Write `caption.txt`: hook line, 2-3 concrete value lines, the comment-word CTA, "Save this", then 5 specific hashtags. Short sentences. No em dashes. No inflated promo words.
- Send all slides to the user with SendUserFile.
- Tell the user WHICH slides to eyeball: any slide with multiple brand icons in one frame, and any less-famous logo (the model nails Stripe/Gmail/Sheets but can fumble GHL, Kit, Fathom, Higgsfield). Offer to regenerate single slides against the same cover reference.
- If asked to "open it", `open "<folder>"` shows it in Finder.

## The icon-first slide formula (replaces screenshots)

Every app/tool slide uses this layout, which is the core lesson from the winning recreate:

1. **Headline**: `'N. APPNAME'` in near-black condensed sans + `'FOR <ROLE>'` in bright orange, hand-drawn orange underline under the app name.
2. **Hero icon**: the app's icon HUGE, flat vector, soft drop shadow, described precisely in the prompt (e.g. "purple-indigo rounded square with a bold white letter S"). Never a screenshot.
3. **Benefit card**: white rounded card, thin bright orange border, exactly 3 short monospace benefit lines (5th-grade reading level).
4. **Mascot gag**: the pixel guy does something on-theme with THAT app (holds a credit card for Stripe, waters the MongoDB leaf, fires envelope cannons for Instantly, sips coffee for morning-brief). One gag per slide, always different.
5. **Annotation**: one handwritten dark-ink line + hand-drawn curved arrow pointing at the icon (e.g. "this handles all the money").

Icon descriptions that worked (reuse verbatim): see the icon library in `references/style-hacker-light.md`.

## Rules

- ONE style per deck: hacker-light. Never dark background, never serif headlines, never 3D voxel mascot.
- Accent is ALWAYS `#E95223` unless Albert names another hex in the request.
- Cover first, every other slide references the cover `job_id`.
- 4:5 portrait, 2k, `nano_banana_2`.
- Same footer on every slide. No carousel dots. No colored emojis in the artwork.
- NEVER em dashes anywhere (slides, caption, chat).
- NEVER auto-post. Posting is out of scope.
- When recreating a user's existing carousel, keep their text verbatim (headlines, numbers, CTA word) and only change the visual system.
- Keep each finished deck in its own folder; regenerating a recolor or variant goes in a NEW folder so the old deck survives.

## When NOT to use this skill

- The user wants the daylight/serif style or the dark hacker-desk style: use `famous-ig-carousel`.
- Single static graphic, video slideshow, or real PowerPoint: other skills.
