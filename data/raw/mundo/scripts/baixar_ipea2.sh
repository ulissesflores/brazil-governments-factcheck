#!/bin/bash
# AQUISICAO (usa rede): complemento da cadeia ipea/: PIB nominal (SCN10_PIBN10; o SCN10_PIB10 baixado antes e um indice real) e o catalogo de metadados
# que justificou a escolha das series (descoberta).
set -u
D=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mundo/ipea
CH=/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py
python3 -I "$CH" add "$D" "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='SCN10_PIBN10')" bruto/ipea_SCN10_PIBN10.json --nota "Ipeadata SCN10_PIBN10 (PIB nominal, R\$)" >/dev/null || echo "FALHOU PIBN10"
python3 -I "$CH" add "$D" "http://www.ipeadata.gov.br/api/odata4/Metadados('SCN10_PIBN10')" bruto/ipea_meta_SCN10_PIBN10.json --nota "metadado Ipeadata SCN10_PIBN10" >/dev/null || echo "FALHOU meta PIBN10"
python3 -I "$CH" add "$D" "http://www.ipeadata.gov.br/api/odata4/Metadados" bruto/ipea_catalogo_Metadados.json --nota "catalogo completo de metadados do Ipeadata (4071 series): usado para ESCOLHER as series (busca por nome); re-adquirido pela cadeia, a copia exploratoria foi para o scratchpad" >/dev/null || echo "FALHOU catalogo"
