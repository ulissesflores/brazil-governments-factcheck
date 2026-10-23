#!/bin/bash
# AQUISICAO (usa rede). WDI + PIP + metadados. Cada arquivo entra na cadeia de hash de mundo/manifest.jsonl.
# Sequencial de proposito: o manifest e append-only e nao admite escritores concorrentes.
set -u
D=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mundo
CH=/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py
C="BRA;ARG;CHL;COL;MEX;PER;URY;VEN;WLD;LCN;UMC"
add() { python3 -I "$CH" add "$D" "$1" "$2" --nota "$3" >/dev/null || echo "FALHOU $2"; }
add "https://api.worldbank.org/v2/sources/2?format=json" bruto/wdi/_fonte_wdi.json "metadado da fonte WDI (lastupdated)"
for i in NY.GDP.PCAP.PP.KD NY.GDP.MKTP.KD.ZG SP.DYN.LE00.IN SP.DYN.IMRT.IN VC.IHR.PSRC.P5 SH.IMM.IDPT FP.CPI.TOTL.ZG SL.UEM.TOTL.ZS TT.PRI.MRCH.XD.WD NE.GDI.FTOT.ZS; do
  add "https://api.worldbank.org/v2/country/$C/indicator/$i?format=json&per_page=20000&date=1960:2026" "bruto/wdi/$i.json" "WDI $i, 11 unidades (BRA, 7 refs, WLD, LCN, UMC)"
  add "https://api.worldbank.org/v2/indicator/$i?format=json" "bruto/wdi/_meta_$i.json" "metadado do indicador WDI $i (nome, unidade, fonte, nota)"
done
# PIP: pobreza 6,85/dia PPC 2017 e Gini, so paises (survey years, sem interpolacao: fill_gaps=false)
P="country=BRA,ARG,CHL,COL,MEX,PER,URY,VEN&year=all&fill_gaps=false&format=csv"
add "https://api.worldbank.org/pip/v1/pip?$P&povline=6.85&ppp_version=2017" bruto/pip/pip_685_ppp2017.csv "PIP linha US\$ 6,85/dia PPC 2017, versao de dados corrente"
add "https://api.worldbank.org/pip/v1/pip?$P&povline=8.3&ppp_version=2021" bruto/pip/pip_830_ppp2021.csv "PIP linha US\$ 8,30/dia PPC 2021 (equivalente da 6,85 de 2017 na base 2021), mesma versao: mede o efeito da troca de base do PPC"
add "https://api.worldbank.org/pip/v1/pip?$P&povline=6.85&ppp_version=2017&version=20260324_2017_01_02_PROD" bruto/pip/pip_685_ppp2017_rel20260324.csv "PIP 6,85 PPC 2017, release 2026-03-24: mede revisao entre releases"
add "https://api.worldbank.org/pip/v1/pip?$P&povline=6.85&ppp_version=2017&version=20250401_2017_01_02_PROD" bruto/pip/pip_685_ppp2017_rel20250401.csv "PIP 6,85 PPC 2017, release 2025-04-01: mede revisao entre releases"
add "https://api.worldbank.org/pip/v1/pip?$P&povline=6.85&ppp_version=2011&version=20240627_2011_02_02_PROD" bruto/pip/pip_685_ppp2011_rel20240627.csv "PIP 6,85 com PPC 2011 (release 2024-06-27): so para medir a troca de base; 6,85 e a linha da base 2017"
add "https://api.worldbank.org/pip/v1/versions" bruto/pip/_versions.json "lista de versoes/releases do PIP"
