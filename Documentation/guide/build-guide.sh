#!/bin/sh
# Rebuild how-to-use.pdf. Run from the project root:  sh guide/build-guide.sh
cd "$(dirname "$0")" || exit 1
cp ../tex/symbulator.cls .
for pass in 1 2 3; do
  xelatex -interaction=nonstopmode -halt-on-error how-to-use.tex >/dev/null || {
    echo "xelatex failed; see guide/how-to-use.log"; exit 1; }
done
rm -f *.aux *.log *.out *.toc *.idx *.ilg *.ind symbulator.cls
echo "wrote guide/how-to-use.pdf"
