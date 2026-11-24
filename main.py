#!/usr/bin/env python3
"""Entry point for the news-image-20261124 submission.

The poster itself was drawn by draw.py (kept in this repository as the
provenance of the artwork). At run time nothing needs to be redrawn:
this program simply copies the shipped entry.png next to it into
/output/entry.png, the path the grader reads.

Pure Python standard library only - no third-party imports, no network.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Read back and compare, so a truncated copy can never pass silently.
    with open(src, "rb") as fh:
        want = fh.read()
    with open(dst, "rb") as fh:
        got = fh.read()
    if want != got:
        print("copy verification failed", file=sys.stderr)
        return 1
    print("entry.png copied to /output (%d bytes)" % len(got))
    return 0


if __name__ == "__main__":
    sys.exit(main())
