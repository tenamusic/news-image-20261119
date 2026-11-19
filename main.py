#!/usr/bin/env python3
"""Deliver the bundled news image for the 19 November 2026 entry.

The repository carries one finished picture, entry.png: a 1024x1024
single-page summary of the day's world news. The judge runs this file
with no network access and afterwards reads a single file, so the
program places the picture where the judge looks for it and reports
its size and checksum.
"""

import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"
TARGET = Path("/output/entry.png")


def main() -> int:
    if not IMAGE.is_file():
        print(f"missing bundled image: {IMAGE}", file=sys.stderr)
        return 1
    data = IMAGE.read_bytes()
    if not 0 < len(data) <= 1024 * 1024:
        print(f"bundled image has unexpected size: {len(data)} bytes", file=sys.stderr)
        return 1
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    staging = TARGET.with_name("entry.png.tmp")
    staging.write_bytes(data)
    staging.replace(TARGET)
    digest = hashlib.sha256(TARGET.read_bytes()).hexdigest()
    expected = hashlib.sha256(data).hexdigest()
    if digest != expected:
        print("output image does not match the bundled image", file=sys.stderr)
        return 1
    print(f"delivered {TARGET} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
