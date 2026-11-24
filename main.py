"""news-23 b59 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir = os.path.abspath(out_dir)
    if out_dir == HERE or out_dir.startswith(HERE + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must be outside the repo")
    os.makedirs(out_dir, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > 1024 * 1024:
        fail("entry.png is over 1 MiB")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("entry.png is not a PNG")
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (1024, 1024):
        fail("entry.png is not 1024x1024, got %dx%d" % (w, h))
    # IEND chunk: 4-byte length (0) + "IEND" + 4-byte CRC (0xAE426082)
    if (len(data) < 12 or struct.unpack(">I", data[-12:-8])[0] != 0
            or data[-8:-4] != b"IEND"
            or struct.unpack(">I", data[-4:])[0] != 0xAE426082):
        fail("entry.png has a malformed IEND trailer")
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        fail("output differs from source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), hashlib.sha256(data).hexdigest()))
    print("source %s is %dx%d, %d bytes" % (SRC, w, h, len(data)))


if __name__ == "__main__":
    main()
