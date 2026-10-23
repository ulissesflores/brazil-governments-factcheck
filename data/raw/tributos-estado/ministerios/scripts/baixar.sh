#!/bin/bash
# uso: baixar.sh <nome-local.html> <url>  -- baixa por curl para ministerios/bruto/ e registra na cadeia de hash da pasta ministerios/
P=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/ministerios
CH=/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py
n="$1"; u="$2"
dest="$P/bruto/$n"
if [ -f "$dest" ]; then echo "JA TEM $n"; exit 0; fi
code=$(curl -sS -L -A 'Mozilla/5.0' --max-time 120 -o "$dest" -w "%{http_code}" "$u" 2>/dev/null) 
sz=$(stat -f%z "$dest" 2>/dev/null)
if [ "$code" != "200" ] || [ "${sz:-0}" -lt 3000 ]; then echo "FALHA $n $code $sz $u" | tee -a "$P/scripts/falhas.log"; rm -f "$dest"; exit 1; fi
d=$(date -u +%Y-%m-%dT%H:%MZ)
python3 -I "$CH" add-local "$P" "$dest" --url "$u" --nota "baixado por curl em $d UTC" >/dev/null && echo "OK $n $sz"
