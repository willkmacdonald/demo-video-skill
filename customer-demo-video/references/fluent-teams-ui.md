# Fluent 2 / Microsoft 365 UI kit for demo videos

Goal: a frame that a Microsoft 365 user instantly reads as "Teams" or "Copilot", built from Fluent 2
tokens, the official Fluent System Icons, and a Segoe-compatible font. Every class named here exists
in `assets/example-line3/index.src.html`. Copy from that file rather than rewriting.

## Contents
1. Fonts and icons
2. Tokens
3. Window framing and scale
4. Teams shell (title bar, app rail, content)
5. Custom Teams app (header, tabs, cards, badges, buttons, side panels)
6. Live and system feedback (toast, skeleton, teaching popover)
7. Copilot / declarative agent pane (chat, adaptive cards, citations)
8. Branding boundaries
9. Other Microsoft surfaces

## 1. Fonts and icons
- **Font**: Segoe UI is not redistributable, and Microsoft's font CDN is usually unreachable from the
  sandbox. Use **Selawik** (Microsoft's open-source, metric-compatible Segoe UI stand-in) from the npm
  package `@reductoai/portable-fonts`; `scripts/setup_project.sh` copies it into `assets/fonts`.
  Declare `font-family: "Selawik", "Segoe UI", sans-serif` so a Windows machine that re-renders gets real Segoe.
  Selawik has 300/400/700 only; weight 600 maps to Bold.
- **Icons**: `@fluentui/svg-icons` (about 21k official SVGs). Write `{{ic:name}}` in `src/index.html` and
  `build.py` inlines it. Names are `<name>_<size>_<regular|filled>`, e.g. `chat_24_regular`,
  `sparkle_20_filled`, `checkmark_circle_16_filled`, `people_team_24_regular`, `calendar_24_regular`,
  `call_24_regular`, `apps_24_regular`, `alert_24_regular`, `data_trending_24_filled`,
  `wrench_20_filled`, `document_pdf_16_regular`, `clipboard_task_20_regular`, `send_20_filled`,
  `attach_20_regular`, `arrow_sync_20_regular`, `warning_16_filled`, `arrow_up_16_filled`.
  Look up names with `ls node_modules/@fluentui/svg-icons/icons | grep <word>`.
  There is no Copilot logo in the package. Use a gradient agent avatar instead (see section 7).

## 2. Tokens (Teams light theme)
```
--brand #5B5FC7  --brand-hover #4F52B2  --brand-fg #444791  --brand-bg2 #E8EBFA  --brand-bg3 #DCE0FA
--n-bg1 #FFFFFF  --n-bg2 #FAFAFA  --n-bg3 #F5F5F5  --n-bg4 #F0F0F0  --n-frame #EBEBEB
--n-fg1 #242424  --n-fg2 #424242  --n-fg3 #616161  --n-fg4 #707070
--n-stroke1 #D1D1D1  --n-stroke2 #E0E0E0  --n-stroke3 #F0F0F0
danger  fg #B10E1C bg #FDF3F4 border #EEACB2   (sparkline stroke #C50F1F)
warning fg #8A3707 bg #FFF9F5 border #FDCFB4   (stroke #DA3B01)
success fg #0E700E bg #F1FAF1 border #9FD89F   (dot #13A10E)
shadow4  0 0 2px rgba(0,0,0,.12), 0 2px 4px rgba(0,0,0,.14)    cards
shadow16 0 0 2px rgba(0,0,0,.12), 0 8px 16px rgba(0,0,0,.14)   toasts, popovers
shadow28 0 0 8px rgba(0,0,0,.12), 0 14px 28px rgba(0,0,0,.14)  side panes, teaching popover
radius 4 (controls), 6 (bubbles), 8 (cards, panes)
type: 12 caption · 14 body · 16 subtitle2/semibold · 18-20 subtitle1 · 24 title3
```
For a non-Teams Microsoft-style app (web portal, Power App), keep the neutrals and semantic colors
and swap `--brand` (e.g. #0F6CBD for the generic Fluent web blue).

## 3. Window framing and scale
- The stage is 1920×1080. The app window is designed at **1440×792 logical px** and scaled by
  `transform: scale(1.166667)`, so it fills 1680×924 at left 120, top 28. Real-size UI (14 px body) then
  reads well on video. The band from y≈968 to 1060 holds the captions, the BEFORE/AFTER chip and the disclaimer.
- Wrap the window in a `.cam` div and animate the camera (scale/x/y) on `.cam`, never on `.win`
  (whose CSS transform would be overwritten).
- Place everything inside the window in **logical coordinates with absolute positioning**. Cursor
  targets and camera moves then stay exact, independent of font metrics.

## 4. Teams shell
- `.teams` frame: background `--n-frame`, radius 10, a soft large shadow on a pale lavender/blue gradient stage.
- `.t-titlebar` (48 px): back/forward icons at left 82, a centered search box (560×32, white, 1 px stroke,
  "Search"), and at right a "…" icon plus an avatar with initials and a green presence dot.
- `.t-rail` (68 px wide): items 56 px tall, a 24 px icon over a 10 px label: Activity (with a red count
  badge), Chat, Teams, Calendar, Calls, *your app* (selected: brand color, semibold, 3 px left
  indicator), "…", and Apps at the bottom.
- `.t-content`: starts at x 68, y 48, top-left radius 8, background `--n-bg2`.

## 5. Custom Teams app (the "after" surface)
- `.app-h` header (56 px, white): app icon tile (28 px, brand→blue gradient, white glyph), app name 18/600,
  tabs (`.tab`, selected gets a 3 px brand underline and semibold weight), and right-side status:
  `.live` pill (success colors with a dot) and "Updated 8:00 AM" plus a sync icon.
- Body: `.body-h` heading 24/600 at (24, 20), `.body-sub` 14 fg3 with a sparkle icon (the AI hint).
- `.pcard` priority card 820×172: rank circle (filled brand for #1), title 18/600, meta 13 fg3,
  badges top-right (`.fbadge` + `.fb-danger|warn|ok|neutral|brand`), a 4-column `.metrics` row
  (label 12 fg3 / value 16/600, red or amber for the headline risk), a `.spark` SVG sparkline at
  right with a dashed limit line, a `.reason` line (sparkle icon + one plain sentence), and buttons at
  the bottom right: secondary "Details" + primary "{{ic:sparkle_20_filled}}Resolve with <Agent>".
- `.side-card` panels (480 wide): a "How this list was built" funnel (bars that narrow:
  212 alarms → 37 conditions → 9 forecast → 3), "If left unaddressed" stat rows, "Continuously re-ranked".
- Impact view (ending): `.kpis` row of 3 `.kpi-t` tiles (green value plus "was …" in fg3), an `.itable`
  comparison (header row `.irow.hd`, before column in danger red, after column with green checks on a
  faint green background), and a `.close-note`.

## 6. Live and system feedback
- **Toast** (`.toast`, 380 wide, top right, shadow16): app icon, app name, time, a one-line message with
  the key noun in bold. Slide in from x+40, hold about 5 s.
- **Skeleton** (`#skeleton .skel`): grey bars in card shapes, pulsed with a finite yoyo while the app "loads".
- **Teaching popover** (`.teach`, brand background, white text, beak at top-left, shadow28): title with a
  sparkle icon, a 1-2 sentence body, and a footer with a small label and a white "Got it" button.
  This is the in-world replacement for an "After" title slide.
- Re-rank: fade/slide the dropped card out, tween the moved card's `y`, swap rank numerals by
  crossfading two spans, fade the new card in with a pulsing brand outline and a "New" badge.

## 7. Copilot / declarative agent pane
- `.pane` (512 wide, right side, full height under the title bar, shadow28) slides in from x+520.
- Header: `.agent-av` (rounded square with a gradient #6B5BE6 → #2F8FD8 → #18B9A4 and a white glyph),
  the agent name 16/600, and "Agent · <Company>" 12 fg3. Icons at right: "…" and dismiss.
- Chat: user bubbles `.ubub` (brand-bg2, radius 6, right-aligned, timestamp above). Agent turns:
  `.a-head` (small avatar + **Name** + time), then typing dots (`.typing`) before lines appear, then text
  lines `.ln2` revealed in sequence (opacity/y stagger ≈0.35 s reads as streaming).
- Citations: inline `.cite` superscript squares (1, 2, 3) and a "Sources" row of `.chip`s with an icon
  and source name (sensor history, CMMS records, a manual PDF).
- Adaptive cards `.acard` (1 px stroke, radius 8): a header with an icon, numbered `.step`s, a divider, a
  parts/status line with a green check, and action buttons (`.btn-s primary|secondary`). On click,
  replace the buttons with an `.okbar` success bar ("WO-48213 scheduled · 10:30 AM · Assigned to …").
- Composer at the bottom: "Message <Agent>" placeholder, attach and send icons, a 2 px brand bottom
  border. Under it: "AI-generated content may be incorrect" (real Copilot UIs carry this).
- Scroll the chat by tweening the inner container's `y`, to make room for a second turn.
- When zooming the camera into the pane, keep the whole pane above the caption band
  (≈ scale 1.1, x −170, y −25 for a right-side pane).

## 8. Branding boundaries
Recreate the *design language* faithfully, but do not paste Microsoft product logos (Teams, Copilot,
Office), real customer logos or real people. Mark every video "Concept demo · illustrative data".
Agents get their own name and gradient avatar, which is how custom/declarative agents appear anyway.

## 9. Other Microsoft surfaces (same tokens, different chrome)
- **Outlook**: three columns (folder pane, message list with unread bold and a brand left bar, reading
  pane), Copilot "Summarize" banner at the top of the message, brand "Reply" split button.
- **Copilot Chat (full page)**: centered conversation column (max 760), a large composer with prompt
  chips above it, response cards with citations, the same agent avatar approach.
- **Power BI / dashboards inside Teams**: white tiles, shadow4, a titled tile header, simple SVG
  charts with token colors, a slicer row.
- **Web app (non-Microsoft)**: when the customer's own portal is the surface, keep Fluent neutrals but
  use the customer's fictional brand color and logo wordmark.
