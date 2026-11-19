---
name: customer-demo-video
description: Turn a business use-case description into a polished, narrated before/after demo video that looks like real software (Microsoft Teams apps, Copilot and declarative agents, Fluent 2 web apps, legacy HMI/SCADA, ERP or QMS screens), built as HTML with HyperFrames and voiced with ElevenLabs. Use this whenever someone describes a scenario they want to show customers or peers ("show an operator getting alarm overload and then an AI agent fixing it", "demo for a medtech CAPA process with Copilot", "make a video of a Teams app for supply chain exceptions"), asks for a demo, concept video, explainer, or "realistic mock" of an AI/Copilot/Industry 4.0 solution, or wants an earlier demo video re-made for a new customer, even if they never say "video" or "HyperFrames".
---

# Customer demo video

Make a believable demo video from a short description of a use case. The user's time should go into
the scenario. Everything else is your job: storyboard, screens, motion, narration, music, sound, render
and a link to watch.

What "good" means here, learned from a real customer-facing build:
- **It looks like real software the whole time.** No slides. Every word appears on a screen: in the UI
  itself, in a system report or popover, or as an annotation drawn over the live UI. Full-frame title
  or summary cards read as a slide deck and break the illusion. Viewers asked for them to go.
- **It is pixel-faithful to the platform.** Fluent 2 tokens, official Fluent System Icons, a
  Segoe-compatible font, the real Teams shell and Copilot pane conventions.
- **The story carries the business point.** A recognizable pain, a visible trigger, a credible AI
  mechanism, a closed loop, and 3-5 consistent numbers.
- **It is clearly a concept.** Fictional companies and people, "Concept demo · illustrative data"
  on screen, no Microsoft product logos.

## Workflow

Work through these in order. Steps 3-6 loop on screenshots, so look at frames before rendering.

### 1. Storyboard from the description
Read `references/storytelling.md`. Do the intake table, pick surfaces for "before" and "after", choose
the beats, write the narration lines (about 2.4 words per second), set the in-world text devices,
and fix the numbers. Write it all to `storyboard.md` in the project. Make sensible industry assumptions
instead of interviewing the user. Ask only if the "after" surface or the core AI mechanism is
genuinely unclear. Show the user a 5-line summary of the storyboard (beats, surfaces, the
numbers) and continue unless they object, so they keep control without being blocked.

### 2. Set up the project
```
bash <skill-dir>/scripts/setup_project.sh <demo-videos-checkout>/<kebab-slug>
```
Each video is a folder in the user's `demo-videos` repo (source only; renders, `node_modules` and the
generated `index.html` are git-ignored there). If that repo isn't available, use any working folder and
offer to add the result to `demo-videos` at the end.

This scaffolds HyperFrames and installs Fluent icons, Selawik (Segoe UI stand-in), Liberation fonts
(legacy UIs) and GSAP, all local, because the sandbox often blocks font CDNs. It also copies
`build.py`, `audio_cues.py` and `finish.sh` into the project.

### 3. Narration first
Generate the narration lines now, before animating (read `references/audio-elevenlabs.md`), and
measure them. Lay the beat timings around the real durations. This avoids re-timing animation after
the voice comes back longer than planned. Music and effects can be generated in the same batch.

### 4. Build the screens
Start from `assets/example-line3/index.src.html` (copy it to `src/index.html`). It contains, ready to
adapt: the stage and caption band, a legacy SCADA HMI with alarm list, fault banner, trend, PDF reader,
softphone and report windows; the Teams shell with a custom app, priority cards, side panels, toast,
skeleton, teaching popover and an in-app impact view; and the Copilot agent pane with streaming chat,
adaptive cards, citations and a composer. Keep the scaffolding (camera, cursor, `update(t)` driver,
caption helper) and replace the content to fit the new scenario. Reference material:
- `references/fluent-teams-ui.md`: tokens, layout grid, every Teams, Copilot and Fluent component used, other M365 surfaces.
- `references/before-world.md`: legacy-screen language and per-industry "before" patterns.
- `references/hyperframes-cookbook.md`: composition rules, timeline patterns, and the traps that cost time.

Generate long repetitive UI content (alarm rows, inbox items, logs) with a small deterministic script
into `src/partials/` (pattern: `assets/example-line3/gen_alarm_rows.py`) and include it with
`{{include:partials/<file>.html}}`. Icons are `{{ic:<fluent_icon_name>}}`.

### 5. Check frames
`python3 build.py && npx hyperframes lint`, then `npx hyperframes snapshot --at <beat times>` and read
the PNGs. Check: nothing clipped or overlapping by accident, text readable at video size, cursor on
its targets, camera zooms keeping the subject above the caption band, numbers consistent between
beats. Fix and re-snapshot only the beats you changed.

### 6. Place audio and render
Write `cues.json` and run `python3 audio_cues.py cues.json` (writes `src/partials/audio.html`, prints
caption windows, flags overlapping narration). Paste the caption windows into the timeline. Rebuild,
then render in the background (about 5 minutes for 2 minutes of video):
```
npx hyperframes render -q looks -o renders/raw.mp4
bash finish.sh renders/raw.mp4 renders/<name>-final.mp4 <scratchpad>/<name>-web.mp4
```

### 7. Deliver
- Send the full-quality MP4 with the file-sending tool.
- Give the user a link to watch: publish a small HTML page with the Artifact tool that holds a
  `<video controls>` of the web copy (published via `files`; each file must be under 15 MB, which
  `finish.sh` guarantees). Tell the user the page is private until they share it.
- Publish to the user's Demo Library (demos.willmacdonald.com), if they want it there: from their
  `demos-site` checkout run `python scripts/add_demo.py --video <final.mp4> --slug <kebab-name> --title ...
  --industry ... --tags ... --summary <2 sentences: the pain, then the outcome with one number>`, then commit
  and push `data/demos.json`. The script uploads to private Azure Blob, cuts a poster at 58 s (pass `--poster-at`
  for a better frame), and measures the duration. It needs AZURE_STORAGE_ACCOUNT/KEY in the environment.
- Narration voice: WKM-1 unless the user names another (see the audio reference).
- Summarize: what the video shows (beat list), assumptions you made, ElevenLabs credits used, the
  flow name in ElevenLabs, and the paths to `src/index.html`, `storyboard.md` and `cues.json`.
- Commit and push the video folder to `demo-videos` (source, cues, storyboard, audio, poster; no renders),
  and add a row for it to that repo's README table. In a cloud session this is the only way the source survives.

## Adapting rather than rebuilding
For a follow-up ("same demo for a pharma plant", "make a 45-second cut", "change the agent's name"),
change the storyboard, then only the affected beats, narration lines and cues. Regenerate only the
narration lines whose words changed: each costs credits, and the others stay valid.

## Environment notes
- The ElevenLabs connector tools load via ToolSearch (`+ElevenLabs`). Audio downloads come from
  `elevenlabsusercontent.com`. If the proxy blocks it, add that host with the environment tools (the
  user approves a card) rather than giving up.
- Chromium is preinstalled. Do not install Playwright browsers. `ffmpeg`/`ffprobe` are available.
- Rendering is CPU-only. Use draft quality (`-q draft`) for quick motion checks, `looks` for delivery.
