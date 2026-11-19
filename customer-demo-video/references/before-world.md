# The "before" world: legacy screens that feel real

The "before" half earns the "after". It should look dated, dense and noisy, but plausible: something
the audience has actually sat in front of. Use a different visual language from Fluent so the
contrast is felt before anything is said.

## Visual language
- Fonts: `HMI Sans` (Liberation Sans, an Arial clone) for labels, `HMI Mono` (Liberation Mono) for values,
  tags and tables. Both are installed by `setup_project.sh`.
- Industrial HMI / SCADA: dark navy panels (#0e141b, #151d26), bevelled grey buttons, saturated
  red/amber/cyan rows, flashing borders. Real plants increasingly use grey ISA-101 screens, but the dark
  noisy version reads as "legacy" on video.
- Classic Windows dialogs: #d4d0c8 body, a navy→steel gradient title bar, a square × button, bevel borders.
- Office-of-2010 feel for business processes: dense grids, tiny fonts, modal dialogs stacked on each other.

## Patterns by industry (pick what matches the use case)
| Industry | Before screens | Trigger event | Scramble tools |
|---|---|---|---|
| Discrete manufacturing | SCADA alarm summary, line overview tiles, trend window | Machine fault, line stops | Trend screen, PDF service manual, OEM phone hold |
| Process / chemicals | DCS faceplates, P&ID mimic with valve states, alarm banner | Pressure/temperature excursion | Historian trends, SOP binder PDF, shift log |
| Medtech / regulated | QMS forms, CAPA/deviation records, document control lists | Complaint or nonconformance | Spreadsheet trackers, SOP PDFs, email chains, approval queue |
| Supply chain | ERP green-screen or grid, MRP exception list | Late shipment, stock-out | Excel pivot, email to supplier, carrier portal |
| Field service | Ticket queue, dispatch board | Asset down at a customer site | Phone, paper manuals, parts catalog |
| Back office / finance | ERP grids, approval inbox | Invoice exception or audit request | Excel, email threads, shared drive |

## Reusable components (all in the example file)
- **Alarm list**: about 60 generated rows (`gen_alarm_rows.py` pattern) in a clipped table; scroll new
  rows in with `steps(n)` easing; flash unacknowledged rows with a finite yoyo on an overlay span;
  "ACK ALL" resets the flashing. Hide the important item among identical-looking rows.
- **Status tiles**: 140×96 boxes with name, state and a value; red/amber borders that flash.
- **Fault banner**: full-width red bar with a flashing overlay and a running counter (DOWNTIME hh:mm:ss).
- **Trend window**: black plot, green grid, a dashed red limit line, and a path drawn on with `strokeDashoffset`.
- **PDF reader**: grey toolbar ("Find: …", "Page 187 / 412"), white pages with grey text bars and yellow
  search hits, scrolled in jumps.
- **Softphone / hold**: vendor name, a hold timer that time-lapses, "Position in queue: 7".
- **System report window**: the cost of the "before", told by the legacy system itself (big red
  monospace values in a dialog), replacing a stats slide.
- **Callout annotation** (`.hmi-callout` + `.ring` + `.hmi-dim`): dark glass card with an orange tag line,
  2-line headline and a sub line; dims the screen briefly. Use it for the opening hook.

## Time and money tell the story
Drive every clock and counter from one deterministic `update(t)` function (see the HyperFrames
cookbook). Real time for the first beats, then a visible time-lapse during the scramble (10:42 → 13:27),
so the viewer *feels* hours pass without the video being long.
