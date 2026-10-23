#!/bin/bash
# uso: baixar.sh <destino-relativo[.auto]> <url> [ua]   (baixa, detecta extensao se .auto, registra na cadeia de hash)
P=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/estatais-lucro
cd "$P" || exit 1
dest="$1"; url="$2"; ua="${3:-Mozilla/5.0}"
mkdir -p "$(dirname "$dest")"
jar=$(mktemp); curl -sS -L -c "$jar" -b "$jar" -A "$ua" --max-time 120 -o "$dest" "$url" || { echo "FALHA $url" >> scripts/falhas.log; exit 2; }
rm -f "$jar"; sz=$(stat -f%z "$dest")
if [ "$sz" -gt 26214400 ]; then echo "GRANDE $sz $url" >> scripts/falhas.log; rm -f "$dest"; exit 3; fi
case "$dest" in *.auto)
  t=$(file -b "$dest"); case "$t" in
   PDF*) e=pdf;; *Microsoft\ Excel*|*Excel*) e=xls;; *Microsoft\ Word*|*Composite\ Document*) e=doc;; *Zip*|*Microsoft\ OOXML*) e=zip;; *HTML*) e=html;; *) e=bin;; esac
  n="${dest%.auto}.$e"; mv "$dest" "$n"; dest="$n";; esac
python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py add-local "$P" "$dest" --url "$url" --nota "baixado por curl em $(date -u +%F)" >/dev/null && echo "OK $sz $dest"
