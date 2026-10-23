#!/bin/bash
# baixa series do BCB SGS em janelas de 10 anos (a API limita o intervalo) e registra na cadeia de hash
cd "$(dirname "$0")/../.."
for c in "$@"; do
  while read -r di df tag; do
    ./scripts/baixar.sh "https://api.bcb.gov.br/dados/serie/bcdata.sgs.$c/dados?formato=json&dataInicial=$di&dataFinal=$df" "bruto/bcb-sgs/sgs$c-$tag.json" "BCB SGS $c, janela $di a $df"
  done <<'JANELAS'
01/01/1980 31/12/1989 a
01/01/1990 31/12/1999 b
01/01/2000 31/12/2009 c
01/01/2010 31/12/2019 d
01/01/2020 31/12/2026 e
JANELAS
done
