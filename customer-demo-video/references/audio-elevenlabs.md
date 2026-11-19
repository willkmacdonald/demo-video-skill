# Audio with ElevenLabs: narration, music, sound effects

Narration and sound turn a screen recording into a demo. All three come from the ElevenLabs MCP
connector (tools named `mcp__ElevenLabs__creative_*`; load them with ToolSearch). Generations spend the
user's credits: one take per line (`generations_count: 1`), never re-run a generation as a "retry",
and report the credit total at the end. A 2-minute demo cost about 3,800 credits (≈$0.70): narration
~1,200, two music tracks 1,800, ten effects ~170, plus optional checks.

## 1. One flow for everything
`creative_create_flow` once (name it after the demo), then pass its `flow_id` to every call, so the user
can audition alternatives in one place.

## 2. Narration
- Voice: the default is the user's own workspace voice **WKM-1** (`Z66yHzLXMXdP7a6gNgR9`, middle-aged
  male, Canadian English, made for their videos). Confirm the id still resolves with
  `creative_list_voices(search="WKM-1")` before generating. Use another voice only when the user asks.
  Fallback if WKM-1 is unavailable: **Ryan – American Documentary Narrator** (`GQQpeRnV5mCWTgxKhGo5`);
  British/Canadian alternatives (Becky, Marcus) come up with search "professional narrator", languages ["en"].
- Voices differ in pace: WKM-1 ran up to 1 s longer than Ryan on the same line, so always place lines
  from measured durations (`audio_cues.py`), never from the script's word count alone.
- Model `eleven_v4`, one call per line (each line is its own clip, so any single line can be redone and re-timed).
- Inline direction tags work with v4, sparingly: `[slightly weary] ...then on hold with the support line.`
- Respell for speech: "C-N-C seven", "ten-thirty", "four and a half hours".
- Poll `creative_get_flow_run_status` (all session ids at once) until `all_completed`.

## 3. Music
`creative_generate_in_flow` with `node_type: "music"`, `model_id: "eleven_music_v2_5"`. Two cues,
matching the arc, with the duration in the prompt:
- Before (≈50 s): "Instrumental only, no vocals. Tense, low-key industrial underscore... dark ambient
  synth pads, steady muted pulse at 90 BPM, subtle metallic textures and ticking clock-like percussion...
  sits under a voiceover, sparse mid-range, ends with a soft fade."
- After (≈70 s): "Instrumental only, no vocals. Optimistic, modern corporate technology underscore: clean
  plucked synths, soft piano, light electronic drums at 110 BPM, warm pads... sits under a voiceover,
  gentle build, clean resolved ending."
The node reports `Instrumental: False` even when the prompt asks for none. If in doubt, transcribe the
track with `creative_transcribe_audio` (connect_from = the music node id). An empty transcript means no vocals.

## 4. Sound effects
`node_type: "sfx"`, `model_id: "eleven_text_to_sound_v3"`, durations in the prompt. A kit that covered a
whole demo: low riser-boom (scene open), alarm annunciator beeps, machine fault plus klaxon, single mouse
click, phone ring into tinny hold music, soft two-note notification chime (generic, not a real product
sound), quick UI whoosh (pane open), bright success chime. Adapt the "before" sounds to the industry (a
printer, an email ping, a ringing desk phone, keyboard clatter).

## 5. Getting the files
Results come from `elevenlabsusercontent.com`. If curl gets a 403 from the proxy, that host is not
allowed in this cloud environment: call `get_environment`, then propose `update_environment` adding
exactly that host (the user approves a card), and retry. URLs in the status result are signed and expire
after a few hours, so download right after generation into `assets/audio/` with stable names
(`vo01.mp3`…, `music-before.mp3`, `sfx-click.mp3`).

## 6. Placing and mixing
1. Measure everything: `npx hyperframes audio assets/audio/*.mp3` (duration, loudness, silences).
2. Write `cues.json` (voice starts, music ranges, effect hits) and run `python3 audio_cues.py cues.json`.
   It writes `src/partials/audio.html`, prints caption windows, and fails on overlapping narration.
3. Levels that worked (narration about −24 LUFS raw):
   - voice `1.6`; music `0.28` (a quiet track around −17 LUFS) or `0.16` (a loud one around −13 LUFS), giving music ≈8 dB under the voice.
   - clicks `2.0`; whoosh `2.2`; chimes `0.55-0.8`; alarm beeps `0.18-0.32`; booms `0.4-0.45`; klaxon `0.45` with `fade_out 1.6`; tinny phone `2.4`.
4. Sync effects to the visual frame: click sounds 0.15 s before the cursor's click time (the transient
   sits about 0.17 s into the file).
5. After rendering, `finish.sh` normalizes to about −14 to −16 LUFS integrated with a −1.5 dBTP ceiling.
