#!/bin/bash
# Regera series/, eventos e quebras a partir de bruto/ e derivado/txt/ (sem rede). derivado/txt/ vem de `pdftotext -layout bruto/...pdf`.
set -e
cd "$(dirname "$0")"
for s in eventos burocracia carga_receita tesouro_ctb ipea_td583 ctb_pib_arrec doingbusiness mapa_empresas ibpt pep nfsp_estatais cvm_lucro sest_raeef tesouro_dividendos quebras; do
  echo "== $s"; python3 -I $s.py
done
