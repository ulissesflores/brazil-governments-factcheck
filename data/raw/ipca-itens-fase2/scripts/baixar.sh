#!/bin/bash
# Baixa tudo pela cadeia de hash (govfc.chain add baixa e registra no mesmo ato).
P=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/ipca-itens-fase2
cd /Users/ulissesflores/Developer/brazil-governments-factcheck || exit 1
add() { PYTHONPATH=code python3 -m govfc.chain add "$P" "$1" "$P/$2" --nota "$3" | tail -1 | cut -c1-200; }
A=https://servicodados.ibge.gov.br/api/v3/agregados
S=https://apisidra.ibge.gov.br/values
for t in 58 655 656 2938 1419 7060; do add $A/$t/metadados bruto/ibge/agregado-$t-metadados.json "metadados SIDRA tabela $t (variaveis, classificacao, periodo)"; done
add "$S/t/58/n1/all/v/63/p/all/c72/2640,1935" bruto/ibge/sidra-58-v63.json "IPCA variacao mensal %, tabela 58 (1991-01 a 1999-07), c72: 2640 geral, 1935 aluguel residencial"
add "$S/t/655/n1/all/v/63/p/all/c315/7169,7448,7696" bruto/ibge/sidra-655-v63.json "IPCA variacao mensal %, tabela 655 (1999-08 a 2006-06), c315: 7169 geral, 7448 aluguel residencial, 7696 plano de saude"
add "$S/t/656/n1/all/v/66/p/all/c315/7169,7448,7696" bruto/ibge/sidra-656-v66.json "IPCA peso mensal %, tabela 656 (1999-08 a 2006-06), mesmos c315"
add "$S/t/2938/n1/all/v/63,66/p/all/c315/7169,7448,7696" bruto/ibge/sidra-2938-v63-66.json "IPCA variacao mensal e peso mensal %, tabela 2938 (2006-07 a 2011-12), mesmos c315"
add "$S/t/1419/n1/all/v/63,66,2265/p/all/c315/7169,7448,7696" bruto/ibge/sidra-1419-v63-66-2265.json "IPCA variacao mensal, peso mensal e acumulada 12 meses %, tabela 1419 (2012-01 a 2019-12), mesmos c315"
add "$S/t/7060/n1/all/v/63,66,2265/p/all/c315/7169,7448,7696" bruto/ibge/sidra-7060-v63-66-2265.json "IPCA variacao mensal, peso mensal e acumulada 12 meses %, tabela 7060 (2020-01 em diante), mesmos c315"
add "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json" bruto/bcb/sgs_433.json "BCB SGS 433 IPCA variacao mensal % (conferencia do IPCA geral)"
for q in "IPCA%20aluguel" "plano%20de%20sa%C3%BAde" "IPCA"; do add "https://dadosabertos.bcb.gov.br/api/3/action/package_search?rows=100&q=$q" "bruto/bcb/ckan_busca_$q.json" "busca no catalogo CKAN do BCB (SGS) por '$q' para localizar serie pronta de subitem do IPCA"; done
# --- rodadas posteriores (executadas a mao, na ordem do manifest.jsonl) ---
# CKAN: buscas com espaco como '+' (a forma %20 e 'de' foram rejeitadas pelo servidor); PDFs de ftp.ibge.gov.br (Notas_Tecnicas, Metodos_de_calculo);
# agregados/58/periodos. Ver manifest.jsonl para URL e hash de cada um.
