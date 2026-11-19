# Storytelling: from a use-case description to a storyboard

The audience is customers and peers who need to *believe* the scenario and see themselves in it.
They are not evaluating the software stack; they react to a recognizable pain, a credible fix, and a
number they care about. Every choice below serves that.

## 1. Read the use case (intake)

Extract these from what the user wrote. Fill gaps with plausible, industry-specific assumptions and note
them in the storyboard rather than stopping to ask, unless something central is truly unknowable
(for example, which Microsoft surface the "after" should live in when nothing hints at it).

| Field | What to capture | Line 3 example |
|---|---|---|
| Industry & site | Sector, plant/site type, a fictional company | Discrete manufacturing, CNC machining, Contoso Plant 2 |
| Persona | Who is on screen, their job, their shift | Line operator, day shift |
| Before pain | What they do today, the tools, why it hurts | 212 alarms, manual digging, manuals, OEM hold queue |
| The trigger event | The concrete moment the pain bites | CNC-07 faults at 10:42, line stops |
| After solution | Which surfaces: Teams app, Copilot/declarative agent, Outlook, web app, mobile | Teams "Line Ops" app + "Line Assist" declarative agent |
| AI mechanics | What the AI actually does, in plain terms | Forecast downtime/scrap risk, rank top 3, re-rank hourly; agent cites manuals and creates/closes work orders |
| Proof numbers | 3-5 metrics with before → after values | 2 h 45 min to root cause → found 6 h early; 4.6 h → 42 min; 340 → 0 scrap |
| Systems of record | What the agent touches | Sensor history, CMMS, OEM manual PDF |

Use fictional names everywhere: Contoso, Fabrikam, Northwind, Woodgrove, Tailspin, or invented OEMs
(e.g. "Hartwell Machine Tools"). Never real customers, real people or real vendor brands. Keep every
number internally consistent across beats (the same failure, the same counts, clocks that add up).

## 2. The arc

Default arc (about 100-120 s total; a short cut is 45-60 s):

1. **Before – establish** (6-10 s): the legacy screen, the persona's normal, the scale of noise.
2. **Before – miss** (6-8 s): the signal that mattered is visibly buried.
3. **Before – the trigger** (6-8 s): the failure lands; a counter starts (downtime, SLA, cost).
4. **Before – the scramble** (12-18 s): the manual hunt across tools (trends, PDFs, email, phone, spreadsheets). Time-lapse clocks sell the pain.
5. **Before – the cost** (5-6 s): the bill, told *by the legacy system itself* (a report window, an email, a ticket).
6. **After – open** (4-5 s): the modern surface loads (skeleton → content) with a teaching popover naming the change.
7. **After – prioritize/insight** (10-15 s): the AI output, with reasons and confidence; show it is *live* (a re-rank, a new event, a notification).
8. **After – act with the agent** (20-30 s): user asks, agent answers with citations, an action card, one click does the work.
9. **After – close the loop** (6-10 s): the outcome confirmed and logged; the item marked resolved.
10. **After – impact** (8-10 s): the before/after numbers, shown *inside the app* (a summary tab, a report card).

Short cut: merge 1-2, 3-4 and 7-8, keep 5 and 10.

## 3. The core rule: no slides. Every word lives on a screen

The first version used full-screen title cards ("Before", a stats slide, "After", a comparison
table). Viewers read them as a slide deck, which broke the illusion that they were watching real
software. Keep the viewer inside the software for the whole video. Put each piece of explanatory
text where it would plausibly appear, or as an annotation drawn over the live UI:

| Need | In-world device (preferred) | Annotation device (when no in-world one fits) |
|---|---|---|
| Opening hook / title | The legacy screen fades in with the problem already visible | A dark callout card on the screen, with a ring around the element it describes |
| "Before" cost summary | A report window, email, ticket or log in the legacy system | A highlight box with a short label beside a value |
| Transition to "after" | Crossfade; the new app loads (skeleton) | A Fluent **teaching popover** naming the change |
| Explaining AI output | Reason line with a sparkle icon, confidence badge, citations | A ring and label pointing at a field |
| Live updates | Toast notification, "Updated 9:00 AM", re-ranked cards | — |
| Final impact | An in-app "Shift impact" or "Summary" tab, a KPI row, a comparison table | — |
| Narration | Bottom caption bar (outside the window frame), plus a small BEFORE/AFTER chip and a "Concept demo · illustrative data" note | — |

The caption bar, the BEFORE/AFTER chip and the disclaimer sit in the band below the app window.
They are always allowed: they read as video chrome, not slides. Do not add full-frame title or
summary cards unless the user explicitly asks for them.

## 4. Narration-first timing

Write narration before animating, then build the animation around the measured audio. Budget about
**2.4 spoken words per second** (Ryan-style narrator at an unhurried pace). A 6 s beat holds about
14 words. Lines are one or two short sentences, written for the ear:

- Spell out what the TTS might mangle: "C-N-C seven" for CNC-07, "ten-thirty" if "10:30" reads oddly.
- Prefer round spoken numbers ("a 400-page manual") and keep the precise number on screen.
- Captions mirror the narration closely but can use the precise form (#2, 10:42 AM).

## 5. Storyboard file

Write `storyboard.md` in the project before building. One row per beat:

```
| # | t (s) | Screen & action | On-screen text (where) | Narration (words) | Audio cue |
| 1 | 0-4.4 | HMI fades in, camera eases out, ring on alarm counter | Callout card on HMI: "212 active alarms. Which one actually matters?" | — | low boom |
| 2 | 4.4-10.9 | Alarm list scrolls, rows flash, counters climb | — | "8 AM on Line 3. The alarm console shows 212 active alarms." (11) | alarm beeps |
...
```

Then a short "Assumptions" list (anything you invented), and the metrics table (before/after values),
so the user can correct facts without re-reading the whole storyboard.

See `assets/example-line3/storyboard.md` for the full worked example.
