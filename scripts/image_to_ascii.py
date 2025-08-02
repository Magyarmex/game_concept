#!/usr/bin/env python3
"""Convert images to ASCII art sprites.

This script loads an input image, resizes it to a small square (default 32×32),
performs edge detection, binarizes the result, optionally thins the lines, and
outputs an ASCII representation. "On" pixels are mapped to characters from a
custom set (``_/\\|-oO!U``), while "off" pixels become spaces.

Example:
    python scripts/image_to_ascii.py source.png --output sprite.txt
"""

from __future__ import annotations

import argparse
from itertools import cycle
from pathlib import Path

from PIL import Image, ImageFilter


CHARSET = "_/\\|-oO!U"


def image_to_ascii(
    image_path: Path,
    output_path: Path | None,
    size: int = 32,
    thin: bool = False,
) -> None:
    """Convert ``image_path`` to ASCII art and save or print the result."""
    img = Image.open(image_path).convert("L")
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # Edge detection and binarization
    img = img.filter(ImageFilter.FIND_EDGES)
    img = img.point(lambda p: 255 if p > 50 else 0).convert("1")

    if thin:
        # Morphological erosion to thin lines
        img = img.filter(ImageFilter.MinFilter(3))

    width, height = img.size
    pixels = img.load()
    charset_cycle = cycle(CHARSET)

    lines: list[str] = []
    for y in range(height):
        line_chars = []
        for x in range(width):
            if pixels[x, y]:
                line_chars.append(next(charset_cycle))
            else:
                line_chars.append(" ")
        lines.append("".join(line_chars))

    ascii_art = "\n".join(lines)
    if output_path:
        output_path.write_text(ascii_art, encoding="utf-8")
    else:
        print(ascii_art)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Path to the source image")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional path to write the ASCII art. Prints to stdout if omitted.",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=32,
        help="Resize the image to this square size (default: 32)",
    )
    parser.add_argument(
        "--thin",
        action="store_true",
        help="Apply simple morphological thinning to the binary image",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    image_to_ascii(args.image, args.output, size=args.size, thin=args.thin)
