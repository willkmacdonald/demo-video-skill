#!/usr/bin/env python3
"""Build index.html from src/index.html.

Replaces, in order:
  {{include:relative/path.html}}  -> contents of src/relative/path.html (for generated partials)
  {{ic:fluent_icon_name}}          -> inline Fluent System Icon SVG (fill=currentColor, sized 1em)

Icon names are file stems in node_modules/@fluentui/svg-icons/icons, e.g. chat_24_regular,
sparkle_20_filled, checkmark_circle_16_filled. A missing icon fails loudly so typos are caught.

Usage: python3 build.py            (run from the HyperFrames project root)
"""
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
SRC = ROOT / "src" / "index.html"
ICONS = ROOT / "node_modules/@fluentui/svg-icons/icons"


def icon(name: str) -> str:
    f = ICONS / f"{name}.svg"
    if not f.exists():
        near = sorted(p.stem for p in ICONS.glob(name.split("_")[0] + "*"))[:12]
        sys.exit(f"Missing Fluent icon '{name}'. Similar: {', '.join(near) or 'none'}")
    svg = f.read_text()
    svg = re.sub(r'\s(width|height)="\d+"', "", svg, count=2)
    return svg.replace("<svg ", '<svg class="ic" fill="currentColor" aria-hidden="true" ', 1)


def main() -> None:
    html = SRC.read_text()
    html = re.sub(r"\{\{include:([^}]+)\}\}", lambda m: (SRC.parent / m.group(1).strip()).read_text(), html)
    html = re.sub(r"\{\{ic:([a-z0-9_]+)\}\}", lambda m: icon(m.group(1)), html)
    leftover = re.findall(r"\{\{[^}]+\}\}", html)
    if leftover:
        sys.exit(f"Unresolved placeholders: {leftover[:5]}")
    (ROOT / "index.html").write_text(html)
    print(f"built index.html ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
