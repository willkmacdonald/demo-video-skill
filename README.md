# customer-demo-video (Claude skill)

Turns a short business use-case description into a narrated before/after demo video that looks like
real software (Teams apps, Copilot / declarative agents, Fluent 2 web apps, legacy HMI/SCADA screens),
built as HTML with HyperFrames and voiced with ElevenLabs (default narrator: WKM-1).

- **Skill:** [`customer-demo-video/`](customer-demo-video/SKILL.md)
- **Video sources it produces:** `demo-videos` repo, one folder per video
- **Where finished videos are published:** `demos-site` (demos.willmacdonald.com)

## Contents
| Path | What it is |
|---|---|
| `customer-demo-video/SKILL.md` | The workflow: storyboard → narration → screens → frame checks → audio → render → deliver |
| `customer-demo-video/references/storytelling.md` | Use-case intake, the before/after arc, the "no slides, all text on screen" rule, narration timing |
| `customer-demo-video/references/fluent-teams-ui.md` | Fluent 2 tokens, Teams shell, custom-app cards, toasts, teaching popovers, Copilot agent pane |
| `customer-demo-video/references/before-world.md` | Legacy-screen patterns by industry (SCADA, DCS, QMS, ERP, …) |
| `customer-demo-video/references/hyperframes-cookbook.md` | Composition rules, timeline patterns, traps, QA and render |
| `customer-demo-video/references/audio-elevenlabs.md` | Voice, music and SFX generation, downloading, placement and mixing levels |
| `customer-demo-video/scripts/` | `setup_project.sh`, `build.py` (icons + partials), `audio_cues.py` (cue sheet → audio tags + captions), `finish.sh` (loudness + web copy) |
| `customer-demo-video/assets/example-line3/` | The Line 3 demo as a worked example (source, storyboard, cue sheet) |

## Install
- **Claude Code:** copy `customer-demo-video/` to `~/.claude/skills/` (or a project's `.claude/skills/`).
- **Claude.ai:** zip the `customer-demo-video/` folder (or use the `.skill` file from a release) and upload it
  under Settings → Capabilities → Skills.
