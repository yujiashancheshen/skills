#!/usr/bin/env python3
"""List embedded PPTX media files and image dimensions.

Usage:
  python scripts/list_pptx_media.py deck.pptx
"""

from __future__ import annotations

import sys
import zipfile
from io import BytesIO
from pathlib import Path

from PIL import Image


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: list_pptx_media.py deck.pptx", file=sys.stderr)
        return 2

    pptx = Path(sys.argv[1])
    if not pptx.exists():
        print(f"not found: {pptx}", file=sys.stderr)
        return 1

    with zipfile.ZipFile(pptx) as zf:
        names = sorted(n for n in zf.namelist() if n.startswith("ppt/media/") and not n.endswith("/"))
        for name in names:
            data = zf.read(name)
            try:
                im = Image.open(BytesIO(data))
                print(f"{name}\t{im.width}x{im.height}\t{im.mode}\t{len(data)} bytes")
            except Exception:
                print(f"{name}\tunknown\tunknown\t{len(data)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
