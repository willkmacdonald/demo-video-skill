#!/usr/bin/env bash
# Scaffold a HyperFrames demo-video project with Fluent icons, a Segoe UI stand-in font, local GSAP,
# and the skill's build script. Usage: setup_project.sh <project-dir> [hyperframes-version]
set -euo pipefail
DIR="${1:?project dir required}"
HF_VER="${2:-0.9.69}"   # last version this skill was verified against; pass "latest" to try newer
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PARENT="$(dirname "$DIR")"; NAME="$(basename "$DIR")"
mkdir -p "$PARENT" && cd "$PARENT"
npx -y "hyperframes@${HF_VER}" telemetry disable >/dev/null 2>&1 || true
npx -y "hyperframes@${HF_VER}" init "$NAME" --example blank --non-interactive --skip-skills >/dev/null
cd "$NAME"
# Fluent System Icons (official SVGs), Selawik (Microsoft's OFL metric-compatible Segoe UI stand-in,
# plus Liberation fonts for legacy/industrial UIs), and GSAP served locally (CDNs may be blocked at render).
npm install --no-save --silent @fluentui/svg-icons @reductoai/portable-fonts gsap@3.13.0
mkdir -p assets/fonts assets/vendor assets/audio src/partials renders
F=node_modules/@reductoai/portable-fonts
cp $F/files/Selawik-{Light,Regular,Bold}.ttf $F/OFL-Selawik.txt assets/fonts/
cp $F/files/Liberation{Sans,Mono}-{Regular,Bold}.ttf assets/fonts/
cp node_modules/gsap/dist/gsap.min.js assets/vendor/
cp "$SKILL_DIR/scripts/build.py" "$SKILL_DIR/scripts/audio_cues.py" "$SKILL_DIR/scripts/finish.sh" .
echo "Project ready: $(pwd)"
echo "Next: write src/index.html (start from $SKILL_DIR/assets/example-line3/index.src.html), then: python3 build.py && npx hyperframes lint"
