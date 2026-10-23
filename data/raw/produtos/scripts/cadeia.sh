#!/bin/bash
# atalho: cadeia.sh <url> <destino-relativo> [nota]  (baixa e registra na cadeia de hash de produtos/)
exec python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py add /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/produtos "$1" "$2" --nota "${3:-}"
