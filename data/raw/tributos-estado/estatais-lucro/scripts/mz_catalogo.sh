#!/bin/bash
# uso: mz_catalogo.sh <empresa> <fmId> <categoria>  -> bruto/<empresa>-mz-catalogo-<categoria>.json (+ cadeia de hash)
P=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/estatais-lucro
cd "$P" || exit 1
d="bruto/$1-mz-catalogo-$3.json"
curl -sS -A Mozilla/5.0 -m 60 -X POST -H 'Content-Type: application/json' \
  -d "{\"categoryInternalNames\":[\"$3\"],\"language\":\"pt_BR\",\"published\":true}" \
  "https://apicatalog.mziq.com/filemanager/company/$2/filter/categories/meta" -o "$d" || exit 2
python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py add-local "$P" "$d" \
  --url "https://apicatalog.mziq.com/filemanager/company/$2/filter/categories/meta" \
  --nota "catalogo MZ (POST categoryInternalNames=$3 language=pt_BR), baixado por curl em $(date -u +%F)" >/dev/null && echo "OK $d"
