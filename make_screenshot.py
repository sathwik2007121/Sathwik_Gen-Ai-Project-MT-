"""
make_screenshot.py — Render outputs/results.txt as a PNG image.

Uses Pillow to draw monospace text on a dark background, simulating a
terminal screenshot. No browser or OS screenshot tools required.

Usage:
    python make_screenshot.py
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("[ERROR] Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(1)

# ─── Configuration ────────────────────────────────────────────────────────────
INPUT_TXT: Path = Path("outputs/results.txt")
OUTPUT_PNG: Path = Path("outputs/execution_output.png")

BG_COLOR: tuple = (18, 18, 18)        # near-black background
FG_COLOR: tuple = (220, 220, 220)      # light grey text
ACCENT_COLOR: tuple = (97, 214, 214)   # cyan for headers
BORDER_COLOR: tuple = (60, 60, 60)     # subtle border

FONT_SIZE: int = 15
H_PADDING: int = 32
V_PADDING: int = 32
LINE_HEIGHT_MULT: float = 1.55         # spacing multiplier


def _get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """
    Try system monospace fonts in order; fall back to PIL default.
    """
    candidates = [
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/Library/Fonts/Courier New.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "cour.ttf",
        "DejaVuSansMono.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    # PIL default bitmap font (always available)
    print("[screenshot] Using PIL default font (no TTF found).")
    return ImageFont.load_default()


def render(input_path: Path, output_path: Path) -> None:
    """Render a text file into a dark-themed PNG."""
    if not input_path.exists():
        print(f"[ERROR] Text file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    font = _get_font(FONT_SIZE)

    # Measure: use a temporary 1x1 image to get text metrics
    tmp_img = Image.new("RGB", (1, 1))
    tmp_draw = ImageDraw.Draw(tmp_img)

    max_width = 0
    for line in lines:
        bbox = tmp_draw.textbbox((0, 0), line or " ", font=font)
        w = bbox[2] - bbox[0]
        max_width = max(max_width, w)

    # Estimate line height from a sample character
    bbox_h = tmp_draw.textbbox((0, 0), "Ag", font=font)
    char_height = bbox_h[3] - bbox_h[1]
    line_height = int(char_height * LINE_HEIGHT_MULT)

    img_width = max_width + 2 * H_PADDING + 4   # +4 for border
    img_height = line_height * len(lines) + 2 * V_PADDING + 4

    # Draw the image
    img = Image.new("RGB", (img_width, img_height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw subtle border
    draw.rectangle(
        [(1, 1), (img_width - 2, img_height - 2)],
        outline=BORDER_COLOR,
        width=1,
    )

    # Render lines
    y = V_PADDING
    for line in lines:
        # Accent colour for header/separator lines
        color = ACCENT_COLOR if line.startswith("=") or line.startswith("┌") or line.startswith("└") else FG_COLOR
        draw.text((H_PADDING, y), line, font=font, fill=color)
        y += line_height

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "PNG")
    print(f"[screenshot] ✓ Saved → {output_path} ({img_width}×{img_height}px)")


if __name__ == "__main__":
    render(INPUT_TXT, OUTPUT_PNG)
