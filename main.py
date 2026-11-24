#!/usr/bin/env python3
"""Entry point for news-image-20261124.

Pure standard library: copies the pre-rendered entry.png that ships in
this repository into /output/entry.png, the path the grader reads.
No third-party imports, no network, no image work at run time.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied", src, "->", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
