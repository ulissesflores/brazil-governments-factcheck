#!/bin/bash
# AQUISICAO (usa rede): Ipeadata (termos de troca, FBCF) com metadado; cadeia propria em mundo/ipea/manifest.jsonl
set -u
D=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mundo/ipea
CH=/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py
for s in FUNCEX_TTR HIST_TROCA PAN_FBKFPIBV SCN10_FBKFN10 SCN10_FBKFP10 SCN10_PIB10 SCN10_FBKFPIBV10 HIST_FBKFGN HIST_FBKFN; do
  python3 -I "$CH" add "$D" "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='$s')" "bruto/ipea_$s.json" --nota "Ipeadata $s" >/dev/null || echo "FALHOU valores $s"
  python3 -I "$CH" add "$D" "http://www.ipeadata.gov.br/api/odata4/Metadados('$s')" "bruto/ipea_meta_$s.json" --nota "metadado Ipeadata $s" >/dev/null || echo "FALHOU meta $s"
done
