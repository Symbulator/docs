#!/bin/sh
# Install IBM Plex for the PDF build.
#
# The PDFs and the website should use the same three faces. The website loads
# them from Google Fonts; XeLaTeX needs them installed on the machine doing the
# build. If they are missing, symbulator.cls falls back to the TeX Gyre clones
# and warns — the build still succeeds, it just looks different.
#
# The simplest route on most systems is the package manager:
#
#   Debian / Ubuntu   sudo apt install fonts-ibm-plex
#   macOS (Homebrew)  brew install --cask font-ibm-plex
#   Windows           download from https://github.com/IBM/plex/releases
#                     and install the Sans, Serif and Mono .ttf files
#
# This script is the fallback for when none of those is available: it pulls the
# web fonts from npm and converts them to TrueType.
#
#   sh tools/install_plex.sh
#
set -e
MISSING=""
command -v npm >/dev/null || MISSING="$MISSING npm"
python3 -c "import fontTools, brotli" 2>/dev/null || pip install fonttools brotli
[ -n "$MISSING" ] && { echo "missing:$MISSING"; exit 1; }

WORK=$(mktemp -d)
cd "$WORK"
npm pack @ibm/plex-sans @ibm/plex-serif @ibm/plex-mono >/dev/null
for f in *.tgz; do tar xzf "$f"; mv package "${f%.tgz}"; done

DEST="${HOME}/.fonts"
mkdir -p "$DEST"
python3 - "$DEST" <<'PY'
import glob, sys
from fontTools.ttLib import TTFont
dest = sys.argv[1]
weights = ["Regular", "Italic", "Bold", "BoldItalic", "SemiBold", "SemiBoldItalic"]
n = 0
for fam in ("IBMPlexSans", "IBMPlexSerif", "IBMPlexMono"):
    for w in weights:
        hits = glob.glob(f"**/{fam}-{w}.woff2", recursive=True)
        if not hits:
            continue
        font = TTFont(hits[0])
        font.flavor = None
        font.save(f"{dest}/{fam}-{w}.ttf")
        n += 1
print(f"installed {n} faces into {dest}")
PY

fc-cache -f >/dev/null 2>&1 || true
fc-list : family | grep -i "plex" | sort -u
echo "Done. Rebuild with: python3 build.py --pdf"
