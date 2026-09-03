"""Extract readable text from Word 97-2003 .doc files (best effort).

Reads the WordDocument stream via olefile and uses the FIB to find the
text range. Handles both the simple case (contiguous text) and the
piece-table case (fast-saved documents) by falling back to a printable-
run scan when the structured read looks wrong. Output: a .txt beside
each .doc, UTF-8.
"""
import os
import re
import struct
import sys

import olefile

REF = r"C:\Users\perez\Claude Code\Documentation\paper\references\2000_thesis"


def fib_text(data):
    """Try the structured route: FIB fcMin/fcMac + piece table flags."""
    if len(data) < 0x60:
        return None
    magic = struct.unpack_from("<H", data, 0)[0]
    if magic != 0xA5EC:
        return None
    fcMin, fcMac = struct.unpack_from("<II", data, 0x18)
    if not (0 < fcMin < fcMac <= len(data)):
        return None
    raw = data[fcMin:fcMac]
    # Heuristic decode: if every other byte is 0, it's UTF-16.
    sample = raw[: min(len(raw), 400)]
    zeros = sample[1::2].count(0)
    if zeros > len(sample) // 4:
        try:
            return raw.decode("utf-16-le", errors="replace")
        except Exception:
            return None
    return raw.decode("cp1252", errors="replace")


RUN_RE = re.compile(r"[\x20-\x7E\xA1-\xFF\r\n\t]{40,}")


def scan_text(data):
    """Fallback: printable cp1252 runs of reasonable length."""
    text = data.decode("cp1252", errors="replace")
    return "\n".join(m.group(0) for m in RUN_RE.finditer(text))


def clean(text):
    text = text.replace("\r", "\n").replace("\x07", "\n").replace("\x0b", "\n")
    text = re.sub(r"[\x00-\x08\x0c-\x1f]", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def convert(path):
    ole = olefile.OleFileIO(path)
    try:
        data = ole.openstream("WordDocument").read()
    finally:
        ole.close()
    text = fib_text(data)
    if not text or len(text) < 200:
        text = scan_text(data)
    return clean(text)


def main():
    for name in sorted(os.listdir(REF)):
        if not name.endswith(".doc"):
            continue
        out = os.path.join(REF, name[:-4] + ".txt")
        if os.path.exists(out):
            continue
        text = convert(os.path.join(REF, name))
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"{name}: {len(text)} chars")


if __name__ == "__main__":
    main()
