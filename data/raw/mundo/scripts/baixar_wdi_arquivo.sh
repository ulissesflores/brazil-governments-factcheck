#!/bin/bash
# AQUISICAO (usa rede): versoes antigas do WDI (fonte 57 "WDI Database Archives") para medir revisoes e as trocas de base do PPC.
set -u
P=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mundo/wdi_arquivo
CH=/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py
C="BRA;ARG;CHL;COL;MEX;PER;URY;VEN;WLD;LCN;UMC"
add() { python3 -I "$CH" add "$P" "$1" "$2" --nota "$3" >/dev/null || echo "FALHOU $2"; }
# PIB per capita PPC: pares de versoes em torno das duas trocas de base (jump de nivel medido em 2026-10-19: 202004->202005 e 202403->202405) + intermediarias
for v in 201904 202004 202005 202403 202405 202407 202412 202507; do
  add "https://api.worldbank.org/v2/sources/57/country/$C/series/NY.GDP.PCAP.PP.KD/time/all/version/$v?format=json&per_page=20000" "bruto/NY.GDP.PCAP.PP.KD_v$v.json" "WDI arquivo versao $v: PIB pc PPC (o rotulo de unidade no arquivo diz 2011 em todas as versoes; base real inferida por salto de nivel)"
done
for i in NY.GDP.MKTP.KD.ZG SP.DYN.LE00.IN SP.DYN.IMRT.IN VC.IHR.PSRC.P5 SH.IMM.IDPT FP.CPI.TOTL.ZG SL.UEM.TOTL.ZS TT.PRI.MRCH.XD.WD NE.GDI.FTOT.ZS; do
  for v in 202403 202507; do
    add "https://api.worldbank.org/v2/sources/57/country/$C/series/$i/time/all/version/$v?format=json&per_page=20000" "bruto/${i}_v$v.json" "WDI arquivo versao $v: $i (para medir revisao contra a versao corrente de 2026-10-08)"
  done
done
add "https://api.worldbank.org/v2/sources/57/version?format=json&page=2" bruto/_versoes_p2.json "lista de versoes do arquivo WDI (pag. 2)"
add "https://api.worldbank.org/v2/sources/57/version?format=json&page=3" bruto/_versoes_p3.json "lista de versoes do arquivo WDI (pag. 3)"
