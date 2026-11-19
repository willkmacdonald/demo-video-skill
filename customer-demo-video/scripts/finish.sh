#!/usr/bin/env bash
# Loudness-normalize a rendered MP4 to -14 LUFS and make a web copy under the 15 MB Artifact file limit.
# Usage: finish.sh <rendered.mp4> <final.mp4> <web.mp4>
set -euo pipefail
IN="$1"; FINAL="$2"; WEB="$3"
ffmpeg -hide_banner -nostats -y -i "$IN" -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 "$FINAL"
for CRF in 27 30 33; do
  ffmpeg -hide_banner -nostats -y -i "$FINAL" -c:v libx264 -preset slow -crf $CRF -tune stillimage -pix_fmt yuv420p \
    -movflags +faststart -c:a aac -b:a 128k "$WEB"
  SIZE=$(stat -c %s "$WEB"); [ "$SIZE" -lt 14500000 ] && break
done
ffmpeg -hide_banner -nostats -i "$FINAL" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" || true
ls -la "$FINAL" "$WEB"
