#!/bin/bash
# AQUISICAO (usa rede): PWT 10.01 e 11.0, Maddison 2023, historico de classes de renda do Banco Mundial, V-Dem via OWID.
# Cadeias proprias por subpasta. Todos os arquivos < 25 MB (medido por content-range antes).
set -u
B=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mundo
CH=/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py
add() { python3 -I "$CH" add "$1" "$2" "$3" --nota "$4" >/dev/null || echo "FALHOU $3"; }
P=$B/pwt_maddison
add $P https://dataverse.nl/api/access/datafile/354095 bruto/pwt1001.xlsx "Penn World Table 10.01 (xlsx, dataverse.nl datafile 354095; release de 2023-02-09)"
add $P https://dataverse.nl/api/access/datafile/554105 bruto/pwt110.xlsx "Penn World Table 11.0 (xlsx, dataverse.nl datafile 554105; release de 2025-10-07; cobre ate 2023)"
add $P https://dataverse.nl/api/access/datafile/554031 bruto/pwt110_whatsnew.pdf "PWT 11.0 what's new (o que mudou vs 10.01)"
add $P https://dataverse.nl/api/access/datafile/421302 bruto/mpd2023_web.xlsx "Maddison Project Database 2023 (xlsx, dataverse.nl datafile 421302)"
add $P https://www.rug.nl/ggdc/productivity/pwt/news bruto/pwt_news.html "pagina de noticias do PWT: datas de release 10.0, 10.01, 11.0"
add $P https://www.rug.nl/ggdc/productivity/pwt/pwt-releases/pwt1001 bruto/pwt1001_release.html "pagina do release PWT 10.01"
add $P https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023 bruto/mpd2023_release.html "pagina do release Maddison 2023"
O=$B/oghist
add $O "https://datacatalogfiles.worldbank.org/ddh-published/0037712/DR0090754/OGHIST.xlsx" bruto/OGHIST.xlsx "Banco Mundial: historico das classificacoes de renda por pais (OGHIST), FY1988 em diante"
V=$B/vdem_owid
add $V "https://ourworldindata.org/grapher/electoral-democracy-index.csv?v=1&csvType=full&useColumnShortNames=true&country=BRA~ARG~CHL~COL~MEX~PER~URY~VEN" bruto/owid_electoral_democracy_index_8paises.csv "V-Dem v2x_polyarchy via OWID, 8 paises (mesma redistribuicao ja usada em dominios-2/democracia)"
