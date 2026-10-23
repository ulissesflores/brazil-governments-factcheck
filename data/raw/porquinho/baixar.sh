#!/bin/bash
# Baixa os brutos desta pasta pela cadeia de hash (chain.py add). TEM REDE; os scripts de analise NAO tem.
# Uso: bash baixar.sh   (idempotente por arquivo: pula o que ja existe)
P=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/porquinho
C=/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py
cd "$P" || exit 1
get() { # destino url nota
  if [ -s "$P/$1" ]; then echo "ja existe $1"; return; fi
  python3 -I "$C" add "$P" "$2" "$1" --nota "$3" | python3 -I -c "import json,sys; r=json.loads(sys.stdin.read()); print(r['seq'], r['arquivo'], r['bytes'], r['sha256'][:12])"
}
B=https://api.bcb.gov.br/dados/serie/bcdata.sgs
# BECO (2026-10-20): as janelas 01/01/1995-31/12/2004 (SGS 25) e 04/05/2012-03/05/2022 (SGS 195) devolveram HTML "Requisicao invalida"
# (limite de 10 anos por consulta: 10 anos exatos ja falha). Os dois arquivos de erro ficam na cadeia (bruto/sgs25-poupanca-ate-2004.json,
# bruto/sgs195-poupanca-2012-2022.json); os dados vieram das janelas de 5-6 anos abaixo.
get bruto/sgs25-poupanca-1995-2000.json "$B.25/dados?formato=json&dataInicial=01/01/1995&dataFinal=31/12/2000" "Poupanca ate 03.05.2012, rentabilidade no periodo, % ao mes, serie diaria (SGS 25), janela 1 (limite de 10 anos por consulta)"
get bruto/sgs25-poupanca-2001-2004.json "$B.25/dados?formato=json&dataInicial=01/01/2001&dataFinal=31/12/2004" "Poupanca ate 03.05.2012 (SGS 25), janela 2"
get bruto/sgs25-poupanca-2005-2012.json "$B.25/dados?formato=json&dataInicial=01/01/2005&dataFinal=03/05/2012" "Poupanca ate 03.05.2012 (SGS 25), janela 2"
get bruto/sgs195-poupanca-2012-2017.json "$B.195/dados?formato=json&dataInicial=04/05/2012&dataFinal=31/12/2017" "Poupanca a partir de 04.05.2012, rentabilidade no periodo, % ao mes, diaria (SGS 195), janela 1"
get bruto/sgs195-poupanca-2018-2022.json "$B.195/dados?formato=json&dataInicial=01/01/2018&dataFinal=03/05/2022" "Poupanca a partir de 04.05.2012 (SGS 195), janela 2"
get bruto/sgs195-poupanca-2022-2026.json "$B.195/dados?formato=json&dataInicial=04/05/2022&dataFinal=20/10/2026" "Poupanca a partir de 04.05.2012 (SGS 195), janela 2"
get bruto/sgs4390-selic-mensal.json "$B.4390/dados?formato=json&dataInicial=01/01/1994&dataFinal=20/10/2026" "Selic acumulada no mes, % ao mes (SGS 4390; CKAN bruto/ckan_4390.json)"
get bruto/sgs3698-ptax-venda-media-mensal.json "$B.3698/dados?formato=json&dataInicial=01/12/1994&dataFinal=20/10/2026" "Dolar venda, media do mes, R\$/US\$ (SGS 3698; mapeamento conferido contra Ipeadata BM12_ERV12)"
get bruto/sgs3696-dolar-venda-fim-mes.json "$B.3696/dados?formato=json&dataInicial=01/12/1994&dataFinal=20/10/2026" "Dolar venda, fim do mes (SGS 3696): conferencia"
get bruto/sgs433-ipca-2026.json "$B.433/dados?formato=json&dataInicial=01/01/2026&dataFinal=20/10/2026" "Extensao IPCA mensal 2026 (SGS 433); ate 2025-12 vale ../inflacao/ipca-sgs433-raw.json"
get bruto/sgs188-inpc-2026.json "$B.188/dados?formato=json&dataInicial=01/01/2026&dataFinal=20/10/2026" "Extensao INPC mensal 2026 (SGS 188)"
get bruto/sgs190-igpdi-2026.json "$B.190/dados?formato=json&dataInicial=01/01/2026&dataFinal=20/10/2026" "Extensao IGP-DI mensal 2026 (SGS 190)"
I='http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='"'"
for s in ANBIMA12_TJPOUP12 BM12_RNDPO12 BM12_TJOVER12 BM12_ERV12 BM12_ERVF12; do
  get bruto/ipeadata-$s-raw.json "${I}${s}')" "Ipeadata $s (conferencia/confirmacao de codigo)"
done
F=https://fred.stlouisfed.org/graph/fredgraph.csv?id
# (FRED: ver getcurl no fim; chain.py add/urllib estoura timeout contra o FRED)
get bruto/snb-plkopr-ipc-suica.csv "https://data.snb.ch/api/cube/plkopr/data/csv/en" "SNB cubo plkopr: IPC suico (indice dez/2010=100 e variacao), monthly"
get bruto/imf-er-usa-xdr_usd-pa-m.xml "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,ER/USA.XDR_USD.PA_RT.M?startPeriod=1994-01" "IMF ER (SDMX): USA XDR_USD media do periodo mensal"
get bruto/imf-er-usa-usd_xdr-pa-m.xml "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,ER/USA.USD_XDR.PA_RT.M?startPeriod=1994-01" "IMF ER (SDMX): USA USD_XDR media do periodo mensal"
get bruto/imf-er-dsd.xml "https://api.imf.org/external/sdmx/2.1/datastructure/IMF.STA/DSD_ER_PUB/4.0.0" "IMF ER: estrutura (DSD_ER_PUB)"
get bruto/wb-pinksheet-monthly.xlsx "https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx" "Banco Mundial Pink Sheet mensal (ouro: Gold UK 99.5%, London PM fixing, media do mes, US\$/toz)"

# --- Rodada 2 (2026-10-20) ---
# SGS 25 continua depois de 03/05/2012 (depositos anteriores mantem a regra antiga): janelas < 10 anos.
get bruto/sgs25-poupanca-2012-2017.json "$B.25/dados?formato=json&dataInicial=04/05/2012&dataFinal=31/12/2017" "Poupanca (SGS 25, depositos ate 03.05.2012) segue publicada depois de 04/05/2012: janela 3"
get bruto/sgs25-poupanca-2018-2026.json "$B.25/dados?formato=json&dataInicial=01/01/2018&dataFinal=20/10/2026" "SGS 25: janela 4"
# FRED: chain.py add (urllib) estoura timeout 4x; curl responde. Baixa por curl e registra com add-local --url.
getcurl() { # destino url nota
  if [ -s "$P/$1" ]; then echo "ja existe $1"; return; fi
  curl -sS -m 90 -o "$P/$1" "$2" || { echo "curl falhou $2"; rm -f "$P/$1"; return; }
  python3 -I "$C" add-local "$P" "$P/$1" --url "$2" --nota "$3; baixado por curl em $(date -u +%H:%MZ) porque chain.py add estourou timeout 4x contra o FRED" | python3 -I -c "import json,sys; r=json.loads(sys.stdin.read()); print(r['seq'], r['arquivo'], r['bytes'], r['sha256'][:12])"
}
for s in CPIAUCSL EXSZUS DEXSZUS CHECPIALLMINMEI; do
  getcurl bruto/fred-$s.csv "$F=$s" "FRED $s"
done
# BECO: bruto/sgs25-poupanca-2018-2026.json voltou HTML "Requisicao invalida" (erro transitorio: a mesma consulta funcionou minutos depois); fica na cadeia. Refeito abaixo.
get bruto/sgs25-poupanca-2018-2026-refeito.json "$B.25/dados?formato=json&dataInicial=01/01/2018&dataFinal=20/10/2026" "SGS 25: janela 4, refeita (a primeira tentativa devolveu pagina de erro)"
# Rodada 3: documentos de quebra de metodo da PTAX
get bruto/bcb-circ-3506-ptax.pdf "https://www.bcb.gov.br/pre/normativos/circ/2010/pdf/circ_3506_v3_p.pdf" "Circular BCB 3.506/2010 (PTAX por consulta a dealers)"
get bruto/okai-comunicado-6815-1999-ptax.html "https://okai.com.br/documento/1999-06-28/comunicado-n-006815" "Comunicado BCB 6.815 de 28/06/1999 (PTAX800), copia de terceiro (okai.com.br); original do BCB nao localizado"
