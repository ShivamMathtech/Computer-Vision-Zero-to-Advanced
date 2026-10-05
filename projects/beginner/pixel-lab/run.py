"""Run the packaged Pixel Lab demo from this project folder or the repo root."""

import sys

from cvzero.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["demo", *sys.argv[1:]]))
