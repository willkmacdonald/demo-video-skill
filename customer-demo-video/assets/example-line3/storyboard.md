# Worked example: Line 3 – from alarm overload to guided resolution (1:54)

**Use case as the user gave it:** operators on a manufacturing line drown in alarms, ignore most of
them, and investigate the critical one by hand (manuals, OEM calls). After: ML ranks the top 3 issues by
forecast downtime and scrap risk, re-ranks every hour, and a declarative Copilot agent guides the
resolution and closes the ticket.

**Surfaces:** Before: legacy SCADA "FactoryView" HMI. After: a Teams app "Line Ops" plus the
declarative agent "Line Assist". Company: Contoso Precision Components, Plant 2. OEM: Hartwell Machine Tools (fictional).

| # | t (s) | Screen & action | On-screen text (where) | Narration | Audio |
|---|---|---|---|---|---|
| 1 | 0-4.4 | HMI fades in, camera eases out, ring on the alarm counter, screen dims | Callout card on HMI: "212 active alarms. Which one actually matters?" | — | low boom |
| 2 | 4.4-10.9 | Alarm rows scroll in, rows and tiles flash, counters climb | — | "8 AM on Line 3. The alarm console shows 212 active alarms." | alarm beeps |
| 3 | 10.9-16.2 | Cursor clicks ACK ALL twice; new alarms keep arriving | — | "Most are nuisance alarms, so operators acknowledge them in bulk and move on." | 2 clicks, quieter beeps |
| 4 | 16.2-22.4 | Camera pushes to the alarm table; orange box on the CNC-07 vibration row | Label on HMI: "The alarm that actually matters" | "The one that matters, spindle vibration on C-N-C seven, looks just like the rest." | — |
| 5 | 22-30.5 | Red banner LINE 3 STOPPED, CNC-07 tile turns FAULT, downtime counter starts; cursor opens TRENDS | Banner text | "10:42. C-N-C seven faults, and the line stops. Now the investigation starts." | grind + klaxon, click |
| 6 | 25-35 | Trend window draws the rising vibration; PDF manual opens and jumps pages; clock time-lapses | Window content | "First the trend screens, then a 400-page service manual..." | — |
| 7 | 33.6-40 | Softphone: OEM support, on hold, timer racing | Window content | "...then on hold with the equipment maker's support line." | ring + hold music |
| 8 | 40.2-46 | SHIFT DOWNTIME REPORT window on the HMI (2:45 to root cause, 4.6 h, 340 parts, 212 alarms, 47 min hold); camera pushes in | Report window | "Nearly three hours to find the cause. Four and a half hours of unplanned downtime." | — |
| 9 | 46-51 | Crossfade to Teams; Line Ops loads (skeleton) | Teaching popover: "Same shift. Same 212 alarms. ..." | "Now, the same shift... with AI." | soft boom |
| 10 | 51-61 | Top 3 cards (CNC-07 bearing, coolant drift, sealer variance) plus funnel and risk panels | Card reasons, badges | "Same 212 alarms, but machine learning forecasts which ones will cost the most." / "The shift starts with three priorities, ranked by predicted downtime and scrap." | — |
| 11 | 61-68 | 9:00 AM: toast, sealer drops off, coolant moves to #3, hydraulic decay enters at #2 (New) | Toast; "Updated 9:00 AM" | "At nine, new sensor data re-ranks the list. A hydraulic pressure issue jumps to number two." | chime |
| 12 | 68-80 | Click "Resolve with Line Assist"; agent pane slides in; camera zooms to pane; cause with citations; repair-steps card; sources | Agent chat | "From priority one, the operator opens Line Assist, a declarative Copilot agent." / "It explains the likely cause, cites its sources, and lays out the repair steps." | click, whoosh |
| 13 | 80-86 | Click "Schedule at 10:30 changeover" → success bar WO-48213 | Card | "One click schedules the work order for the 10:30 planned changeover." | click, success |
| 14 | 84-94 | Chat scrolls; "10:30-11:12 Repair completed"; user reports 1.9 mm/s; close-out card; click Close ticket | Card | "After the repair, the agent confirms the result and closes out the ticket." | click, success |
| 15 | 94.5-100 | Camera out; card #1 dims with a Resolved badge | Badge | "Found before it failed. Fixed during planned downtime." | — |
| 16 | 100.4-114 | Pane closes; cursor clicks the Shift log tab; Shift impact view: KPI tiles plus comparison table | In-app impact view | "From alarm overload... to fast, guided resolution." | whoosh, click |

**Metrics (keep consistent everywhere):** root cause after 2 h 45 min → found about 6 h before failure;
4.6 h unplanned downtime → 42 min planned; 340 scrapped parts → 0; 212 alarms → top 3; 47 min OEM hold
→ cited steps; WO-48213 scheduled 10:30, closed 11:14.

**Narrator:** WKM-1 (user's own ElevenLabs voice).

**Assumptions made:** HX-500 machine, bearing kit HX-SB-220 in Crib B-14, technician R. Patel,
operator "JL", CMMS as the system of record.

Build files: `index.src.html` (copy to `src/index.html`), `gen_alarm_rows.py` (run first, writes
`src/partials/alarm_rows.html`), `cues.json` (audio placement for `audio_cues.py`). Audio files are not
bundled: regenerate them with ElevenLabs for a new project.
