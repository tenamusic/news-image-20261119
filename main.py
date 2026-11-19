#!/usr/bin/env python3
"""Entrypoint for the news-image-20261119 make.fun entry.

The repository bundles a finished image, entry.png, which summarises
the world news of 19 November 2026 on a single 1024x1024 page. The
judge runs this program in a sandbox with no network and afterwards
reads one file from the output directory, so this program copies the
bundled image there and proves the copy is intact before exiting.
"""

import hashlib
import os
import shutil
import sys

IMAGE_NAME = "entry.png"


def digest_of(path):
    """Return the sha256 hex digest of the file at path."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def deliver():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    if not os.path.isfile(source):
        print(f"bundled image not found: {source}", file=sys.stderr)
        return 1

    # The bounty caps the entry image at 1 MiB; an empty or oversized
    # bundle can never score, so refuse it here instead of copying it.
    source_size = os.path.getsize(source)
    if source_size == 0 or source_size > 1024 * 1024:
        print(f"bundled image size out of bounds: {source_size} bytes", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, IMAGE_NAME)

    shutil.copyfile(source, destination)

    if digest_of(destination) != digest_of(source):
        print("copied image failed the integrity check", file=sys.stderr)
        return 1

    size = os.path.getsize(destination)
    print(f"delivered {destination} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(deliver())
