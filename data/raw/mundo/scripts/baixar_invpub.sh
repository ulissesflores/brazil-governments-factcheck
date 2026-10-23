#!/bin/bash
# AQUISICAO (usa rede): investimento publico (FGV IBRE Observatorio de Politica Fiscal, 3 vintages) e IMF ICSD 2021.
set -u
P=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mundo/invpub
CH=/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py
add() { python3 -I "$CH" add "$P" "$1" "$2" --nota "$3" >/dev/null || echo "FALHOU $2"; }
F=https://observatorio-politica-fiscal.ibre.fgv.br
add $F/sites/observatorio-politica-fiscal.ibre.fgv.br/files/u49/investimentos_publicos_1947-2025.xlsx bruto/fgv_investimentos_publicos_1947-2025.xlsx "FGV IBRE Observatorio de Politica Fiscal, serie atualizada em 2026-04-10"
add $F/sites/observatorio-politica-fiscal.ibre.fgv.br/files/u49/investimentos_publicos_1947-2024.xlsx bruto/fgv_investimentos_publicos_1947-2024.xlsx "FGV IBRE, vintage de 2025-04-22: serve para medir revisao da serie"
add $F/sites/observatorio-politica-fiscal.ibre.fgv.br/files/u49/investimentos_publicos_1947-2023.xlsx bruto/fgv_investimentos_publicos_1947-2023.xlsx "FGV IBRE, vintage anterior (2024): serve para medir revisao da serie"
add $F/series-historicas/investimentos-publicos/investimentos-publicos-serie-historica-1947-2025 bruto/fgv_pagina_1947-2025.html "pagina de descricao da serie 1947-2025"
add $F/series-historicas/investimentos-publicos/investimentos-publicos-1947-2024 bruto/fgv_pagina_1947-2024.html "pagina de descricao da serie 1947-2024 (nota [1] sobre diferencas)"
I=https://infrastructuregovern.imf.org/content/dam/PIMA/Knowledge-Hub/dataset
add $I/IMFInvestmentandCapitalStockDataset2021.xlsx bruto/IMFInvestmentandCapitalStockDataset2021.xlsx "IMF ICSD 2021 (investimento do governo geral, % PIB; ate 2019)"
add $I/WhatsNewinIMFInvestmentandCapitalStockDatabase_May2021.pdf bruto/ICSD_whatsnew_May2021.pdf "nota de atualizacao do ICSD maio/2021"
