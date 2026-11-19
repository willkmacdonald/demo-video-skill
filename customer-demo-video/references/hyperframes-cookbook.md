# HyperFrames cookbook (what worked, and the traps)

HyperFrames renders an HTML page frame by frame in headless Chrome by seeking a paused GSAP timeline.
Everything must be **deterministic and seekable**: the renderer jumps to arbitrary times, sometimes backwards.

## Contents
1. Project and build loop
2. Composition skeleton
3. Timeline patterns
4. Traps (each one hit in practice)
5. QA loop and what lint warnings to ignore
6. Render

## 1. Project and build loop
```
bash <skill>/scripts/setup_project.sh /home/user/demos/<name>
cd /home/user/demos/<name>
cp <skill>/assets/example-line3/index.src.html src/index.html     # starting point
python3 build.py && npx hyperframes lint                           # every edit
npx hyperframes snapshot --at 2,10,25,48,70                        # look at frames (Read the PNGs)
npx hyperframes render -q looks -o renders/raw.mp4                 # about 2.5x real time on CPU
```
Edit `src/index.html`, never `index.html` (it is generated). The CLI docs are offline: `npx hyperframes docs <topic>`.

## 2. Composition skeleton
- Root: `<div id="root" data-composition-id="main" data-start="0" data-duration="T" data-width="1920" data-height="1080">`.
- **Top-level scenes only** get `data-start`/`data-duration` and `class="clip"` (`<section>`s: one per
  world, e.g. `#s-hmi`, `#s-teams`, plus `#captions`). Inside a scene, control visibility with GSAP
  (opacity), not nested clips.
- Scenes that fade in need `opacity: 0` in CSS, otherwise lint fails with "full-frame overlay starts visible".
- Audio: `<audio id=… src=… data-start data-duration data-volume [data-fade-in data-fade-out]>` at root level
  (generated into `src/partials/audio.html` by `audio_cues.py`).
- Load GSAP from `assets/vendor/gsap.min.js`, not a CDN.
- One paused timeline registered as `window.__timelines["main"]`, ending with `tl.seek(0)`.

## 3. Timeline patterns
- **Clock/counter driver**: one proxy tween drives every changing number and text:
  ```js
  const P = { t: 0 };
  tl.to(P, { t: T, duration: T, ease: "none", onUpdate: () => update(P.t) }, 0); update(0);
  function update(t) { el.textContent = t < 22 ? hms(8*3600 + t) : hms(lerp(a, b, 24, 40, t)); ... }
  ```
  Pure functions of `t` are seek-safe. Never use `tl.call()`, `Date.now()` or `Math.random()`.
- **Captions**: `cap(id, start, end)` = fromTo opacity/y in, fade out 0.3 s before end. Timings come from
  the measured narration (see `audio_cues.py` output).
- **Cursor**: an SVG arrow inside the window (logical coords) moved with `power2.inOut`; a click is a
  scale 0.85 dip plus a ripple ring. Place the ripple with `tl.set(rip, {x, y}, at)` just before the click.
- **Camera**: tween `.cam` `{scale, x, y}` (transform-origin 960px 490px) for push-ins on the important
  row or pane, then back out. Keep pushes modest (1.1-1.3) and slow (1-1.4 s).
- **Flashing**: `tl.to(sel, {opacity: .55, duration: .3, repeat: N, yoyo: true, ease: "none"}, t)`. Use a
  finite `repeat` only; follow with `tl.set(sel, {opacity: 0}, tEnd)` to stop cleanly.
- **Scrolling lists**: tween a list's `y` with `ease: steps(n)` for row-by-row arrivals.
- **Drawn lines**: SVG path with `stroke-dasharray`/`stroke-dashoffset` = length, tween offset to 0.
- **Tab switch / class state**: `tl.set(el, { className: "tab sel" }, t)` is seek-safe.
- **Streaming chat**: typing dots (staggered yoyo), then lines fade in with `stagger: 0.35-0.4`.

## 4. Traps
- `fromTo` renders its *from* state immediately at time 0. For effects that should be invisible until
  later (ripples, flashes), pass `immediateRender: false`, or they show as stray artifacts in early frames.
- Text measured by the browser (wrapping, widths) can differ from your guess, so aim the cursor at
  absolutely positioned targets. Use one-line `white-space: nowrap` text where you need exact layout.
- An element animated with GSAP transforms loses any CSS `transform`. That is why the window scale
  lives on `.win` and camera moves on `.cam`.
- Long chat content: give the inner chat container an explicit height and scroll it by `y`; check the
  last card ends above the composer.
- Sound effects that overlap narration mask it. Keep loud effects (klaxons, booms) at 0.4-0.5 volume
  with `data-fade-out`, or start the narration line 0.5 s later.
- The network may block `jsdelivr`/Microsoft font CDNs. Everything the page needs must be local.

## 5. QA loop
- After each change: `python3 build.py && npx hyperframes lint`. Then `snapshot` at the beats you
  touched and **look at the PNGs** before rendering. A passing lint does not mean it looks right.
- `npm run check` also runs layout/contrast checks. These warnings are expected and safe to ignore:
  `content_overlap` / `text_occluded` where dialogs or the agent pane intentionally cover UI,
  `text_below_floor` (real UIs use 12-14 px text), contrast warnings on flashing rows, and
  `nested_structure_needs_subcomposition`. Fix real errors: visible-at-start overlays, missing assets, script errors.
- Add `data-layout-ignore` to intentionally overlapping windows to quiet the checker.

## 6. Render
`npx hyperframes render -q looks -o renders/raw.mp4`. A 2-minute 1080p video takes about 5 minutes on
this CPU-only sandbox (it falls back to screenshot capture). Run it with `run_in_background` and keep
working. Then run `finish.sh` for loudness and a web copy.
