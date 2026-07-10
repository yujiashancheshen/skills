#!/usr/bin/env python3
"""Flag large images in a PPTX that may be text-bearing cards.

This is a heuristic helper. It does not replace visual inspection or OCR.

Usage:
  python scripts/check_large_text_images.py deck.pptx
"""

from __future__ import annotations

import sys
import zipfile
from io import BytesIO
from pathlib import Path

from PIL import Image


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_large_text_images.py deck.pptx", file=sys.stderr)
        return 2

    pptx = Path(sys.argv[1])
    if not pptx.exists():
        print(f"not found: {pptx}", file=sys.stderr)
        return 1

    flagged = 0
    with zipfile.ZipFile(pptx) as zf:
        for name in sorted(n for n in zf.namelist() if n.startswith("ppt/media/") and not n.endswith("/")):
            data = zf.read(name)
            try:
                im = Image.open(BytesIO(data))
            except Exception:
                continue
            pixels = im.width * im.height
            aspect = im.width / max(1, im.height)
            is_card_like = pixels >= 250_000 and 0.5 <= aspect <= 4.0
            if is_card_like:
                flagged += 1
                print(f"FLAG\t{name}\t{im.width}x{im.height}\tcheck for embedded text")

    if flagged == 0:
        print("No large card-like images flagged. Still perform visual QA.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
