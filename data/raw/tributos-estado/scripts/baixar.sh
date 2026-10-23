#!/bin/bash
# uso: baixar.sh <url> <destino-relativo-a-tributos-estado> ["nota"]  -- curl + entrada na cadeia de hash
set -u
P=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado
mkdir -p "$(dirname "$P/$2")"
code=$(curl -sS -L -A 'Mozilla/5.0' --max-time 120 --max-filesize 26214400 -o "$P/$2" -w '%{http_code}' "$1")
sz=$(stat -f%z "$P/$2" 2>/dev/null || echo 0)
echo "$code $sz $2"
if [ "$code" = "200" ] && [ "$sz" -gt 0 ]; then
  python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py add-local "$P" "$P/$2" --url "$1" --nota "baixado por curl em $(date -u +%Y-%m-%dT%H:%M:%SZ); ${3:-}" >/dev/null
else
  rm -f "$P/$2"; echo "FALHOU $1" >> "$P/scripts/falhas.log"
fi
