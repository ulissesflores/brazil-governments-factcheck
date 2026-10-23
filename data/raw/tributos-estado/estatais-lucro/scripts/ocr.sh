#!/bin/bash
# uso: ocr.sh <pdf-bruto> <saida.txt> : OCR (pdftoppm 200dpi + tesseract por), paginas separadas por form-feed. Sem rede.
pdf="$1"; out="$2"; t=$(mktemp -d)
n=$(pdfinfo "$pdf" | awk '/^Pages:/{print $2}')
: > "$out"
for p in $(seq 1 $n); do
  pdftoppm -r 200 -gray -f $p -l $p -png "$pdf" "$t/p" >/dev/null 2>&1
  f=$(ls "$t"/p*.png | head -1)
  tesseract "$f" - -l por --psm 6 2>/dev/null >> "$out"
  printf '\f' >> "$out"; rm -f "$t"/p*.png
done
rm -rf "$t"
