#!/usr/bin/env python3
"""Turn an audio cue sheet into <audio> tags, using each file's *measured* duration.

Usage: python3 audio_cues.py cues.json   (run from the project root)
Writes src/partials/audio.html (include it in src/index.html with {{include:partials/audio.html}})
and prints caption windows to paste into the timeline's cap(...) list.

cues.json:
{
  "voice": [ {"id": "vo01", "file": "assets/audio/vo01.mp3", "start": 4.4, "caption": "c1"} , ...],
  "music": [ {"id": "mus-before", "file": "assets/audio/music-before.mp3", "start": 0, "end": 46.4,
              "volume": 0.28, "fade_in": 1, "fade_out": 2.5}, ...],
  "sfx":   [ {"file": "assets/audio/sfx-click.mp3", "start": 12.33, "volume": 2.0}, ...],
  "voice_volume": 1.6
}
Voice lines that overlap are reported (exit code 1) so you can move them.
"""
import json
import subprocess
import sys
from pathlib import Path


def dur(path: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip()
    return round(float(out), 2)


def main() -> None:
    cues = json.loads(Path(sys.argv[1] if len(sys.argv) > 1 else "cues.json").read_text())
    tags, caps, problems = [], [], []
    for m in cues.get("music", []):
        d = round(m["end"] - m["start"], 2)
        tags.append(f'<audio id="{m["id"]}" src="{m["file"]}" data-start="{m["start"]}" data-duration="{d}" '
                    f'data-volume="{m.get("volume", 0.2)}" data-fade-in="{m.get("fade_in", 1)}" data-fade-out="{m.get("fade_out", 2)}"></audio>')
    vv = cues.get("voice_volume", 1.6)
    voice = sorted(cues.get("voice", []), key=lambda v: v["start"])
    for i, v in enumerate(voice):
        d = dur(v["file"])
        end = round(v["start"] + d, 2)
        tags.append(f'<audio id="{v["id"]}" src="{v["file"]}" data-start="{v["start"]}" data-duration="{d}" data-volume="{v.get("volume", vv)}"></audio>')
        nxt = voice[i + 1]["start"] if i + 1 < len(voice) else None
        # Rendered TTS files carry ~0.1-0.2 s of trailing silence, so only a real overlap is a problem.
        if nxt is not None and end > nxt + 0.05:
            problems.append(f'{v["id"]} ends at {end}s but {voice[i + 1]["id"]} starts at {nxt}s (move it to >= {end + 0.2:.1f})')
        if v.get("caption"):
            # Hold the caption ~1 s past the line, but hand over cleanly to the next line's caption.
            cap_end = end + 1.0 if nxt is None else min(end + 1.0, nxt)
            caps.append(f'["#{v["caption"]}",{v["start"]},{round(cap_end, 1)}]')
        print(f'{v["id"]:8s} {v["start"]:7.2f} → {end:7.2f}  ({d:.2f}s)')
    for i, s in enumerate(cues.get("sfx", [])):
        d = dur(s["file"])
        fo = f' data-fade-out="{s["fade_out"]}"' if "fade_out" in s else ""
        tags.append(f'<audio id="fx{i:02d}" src="{s["file"]}" data-start="{s["start"]}" data-duration="{d}" data-volume="{s.get("volume", 1)}"{fo}></audio>')
    out = Path("src/partials/audio.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(tags) + "\n")
    print(f"\nwrote {out} ({len(tags)} clips)")
    if caps:
        print("\ncaption windows for the timeline:\n[" + ",".join(caps) + "]")
    if problems:
        print("\nOVERLAPS:\n  " + "\n  ".join(problems))
        sys.exit(1)


if __name__ == "__main__":
    main()
