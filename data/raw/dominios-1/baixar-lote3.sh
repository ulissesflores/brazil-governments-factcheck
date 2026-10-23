#!/bin/zsh
# lote 3: metadados SIDRA das tabelas usadas, tabelas auxiliares para medir efeitos de quebra, evidencias de cobertura
D=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1
M=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py
S="https://servicodados.ibge.gov.br/api/v3/agregados"
for t in 179 204 256 1187 1436 1437 1955 1956 3149 3216 3217 4660 4708 6731 6735 6803 6804 6805 7113 7126 7192 9542; do
  python3 -I $M add $D "$S/$t/metadados" bruto/meta/sidra_meta_${t}.json --nota "SIDRA metadados da tabela ${t} (titulo, periodicidade, classificacoes)"
done
python3 -I $M add $D "$S/3149/periodos/2010/variaveis/140|1645|950|2376?localidades=N1[all]&classificacao=1[all]" bruto/sidra_3149_alfab_2010_urbrur.json --nota "SIDRA 3149 Censo 2010 com situacao urbana/rural: para inferir direcao da inclusao do Norte rural na PNAD 2004"
python3 -I $M add $D "$S/6803/periodos/2022/variaveis/381?localidades=N1[all]&classificacao=1821[all]" bruto/sidra_6803_agua_ligacao_2022.json --nota "SIDRA 6803 Censo 2022: ligacao a rede geral x principal forma; mede efeito da definicao 'rede geral'"
python3 -I $M add $D "$S/7126/periodos/all/variaveis/3593?localidades=N1[all]&classificacao=2[6794]|58[2795]" bruto/sidra_7126_anosestudo_pnadc_2016_2025.json --nota "SIDRA 7126 anos de estudo 15+ PNADC (so 2016+): evidencia de 'sem serie de 30 anos'"
python3 -I $M add $D "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='MEDUCA')" bruto/ipea_MEDUCA.json --nota "Ipeadata MEDUCA media de anos de estudo 25+ (so Censos 1991 e 2000 no nivel Brasil)"
python3 -I $M add $D "https://api.worldbank.org/v2/country/BRA/indicator/SE.XPD.TOTL.GD.ZS?format=json&per_page=20000" bruto/wb_SE.XPD.TOTL.GD.ZS.json --nota "Banco Mundial WDI: gasto do governo em educacao, % do PIB (cobertura e vazios)"
python3 -I $M add $D "https://api.worldbank.org/v2/country/BRA/indicator/SE.ADT.LITR.ZS?format=json&per_page=20000" bruto/wb_SE.ADT.LITR.ZS.json --nota "Banco Mundial WDI: alfabetizacao de adultos (UIS), cobertura"
echo FIM-LOTE3
