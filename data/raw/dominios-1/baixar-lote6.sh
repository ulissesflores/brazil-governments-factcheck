#!/bin/zsh
# lote 6 (apos revisao do advisor): rendimento do trabalho na PNAD antiga (1996-2015), para a serie mais longa e sobreposicao 2012-2015 com a PNADC
D=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1
M=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py
S="https://servicodados.ibge.gov.br/api/v3/agregados"
python3 -I $M add $D "$S/1871/periodos/all/variaveis/778?localidades=N1[all]&classificacao=2[6794]|12025[99149]" bruto/sidra_1871_rendimento_nominal_pnad_2001_2015.json --nota "SIDRA 1871 PNAD 2001-2015: rendimento medio mensal NOMINAL de todos os trabalhos, ocupados 10+ (mes de referencia: setembro)"
python3 -I $M add $D "$S/4027/periodos/all/variaveis/4015?localidades=N1[all]&classificacao=2[6794]|12025[99149]" bruto/sidra_4027_rendimento_nominal_pnad15mais_2012_2015.json --nota "SIDRA 4027 PNAD 2012-2015: mesma variavel, ocupados 15+"
python3 -I $M add $D "$S/427/periodos/all/variaveis/1906?localidades=N1[all]&classificacao=2[6794]" bruto/sidra_427_rendimento_real_pnad_1996_2006.json --nota "SIDRA 427 PNAD 1996-2006: rendimento medio mensal REAL de todos os trabalhos, ocupados 10+ (base de precos nao declarada nos metadados)"
python3 -I $M add $D "$S/4660/periodos/all/variaveis/5929?localidades=N1[all]" bruto/sidra_4660_rendimento_nominal_pnadc_2012_2025.json --nota "SIDRA 4660 PNADC anual: rendimento medio mensal NOMINAL, todos os trabalhos, habitual, ocupados 14+"
for t in 427 1871 4027; do python3 -I $M add $D "$S/$t/metadados" bruto/meta/sidra_meta_${t}.json --nota "SIDRA metadados da tabela ${t}"; done
echo FIM-LOTE6
