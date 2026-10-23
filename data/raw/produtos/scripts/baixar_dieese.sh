#!/bin/bash
# Baixa, por POST no banco publico do DIEESE, os precos medios (tipoDado=4) de cada item da cesta de Sao Paulo
# (cidade 8) de 01/1959 a 09/2026, mais o gasto mensal (5) e o tempo de trabalho (3) do total da cesta (produto 1).
# Cada arquivo entra na cadeia de hash logo apos o download (add-local: timestamp = mtime do arquivo recem-baixado).
set -u
P=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/produtos
CH=/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py
mkdir -p "$P/bruto/dieese"
baixa() { # produto tipo nome
  local f="bruto/dieese/dieese-sp-$3-tipo$2.html"
  local body="farinha=true&cidades=8&tipoDado=$2&produtos=$1&dataInicial=011959&dataFinal=092026"
  curl -s -m 120 -A "Mozilla/5.0 (compatible; brazil-governments-factcheck/0.1)" -X POST https://www.dieese.org.br/cesta/cidade -d "$body" -o "$P/$f" -w "$3 tipo$2 http=%{http_code} bytes=%{size_download}\n"
  python3 -I "$CH" add-local "$P" "$P/$f" --url "POST https://www.dieese.org.br/cesta/cidade $body" --nota "banco de dados da Pesquisa Nacional da Cesta Basica (DIEESE), consulta por cidade; produto=$1 tipoDado=$2" >/dev/null
  sleep 2
}
for par in 2:carne 3:leite 4:feijao 5:arroz 9:pao 10:cafe 12:acucar 13:oleo 6:farinha 7:batata 8:tomate 11:banana 14:manteiga; do
  baixa "${par%%:*}" 4 "${par##*:}"
done
baixa 1 5 total
baixa 1 3 total
