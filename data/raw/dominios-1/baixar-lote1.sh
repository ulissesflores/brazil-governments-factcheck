#!/bin/zsh
# lote 1: Ipeadata (series decenais Censo) + SIDRA Censo 1991/2000/2010/2022 (alfabetizacao, agua, esgoto, luz)
D=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1
M=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py
IP="http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='"
for s in TXA15M7091 ADH_T_ANALF15M ADH_T_AGUA ADH_T_LUZ PDIAE PDIEREDE DOMAGE DOMELE DOMISE NDOME; do
  python3 -I $M add $D "${IP}${s}')" bruto/ipea_${s}.json --nota "Ipeadata OData ValoresSerie SERCODIGO=${s}; catalogo em social/bruto/ipea_metadados_all.json"
done
S="https://servicodados.ibge.gov.br/api/v3/agregados"
python3 -I $M add $D "$S/204/periodos/1991|2000/variaveis/157?localidades=N1[all]&classificacao=59[all]|58[all]" bruto/sidra_204_alfab_1991_2000.json --nota "SIDRA 204 Censo 1991/2000 pop 5+ por alfabetizacao e idade"
python3 -I $M add $D "$S/3149/periodos/2010/variaveis/140|1645|950|2376?localidades=N1[all]&classificacao=1[0]" bruto/sidra_3149_alfab_2010.json --nota "SIDRA 3149 Censo 2010 universo: 10+ e 15+ total e alfabetizadas"
python3 -I $M add $D "$S/9542/periodos/2022/variaveis/950?localidades=N1[all]&classificacao=59[all]|2[6794]|86[95251]|287[100362]" bruto/sidra_9542_alfab_2022.json --nota "SIDRA 9542 Censo 2022 15+ total e alfabetizadas"
python3 -I $M add $D "$S/179/periodos/1991/variaveis/96?localidades=N1[all]&classificacao=1[0]|61[all]" bruto/sidra_179_agua_1991.json --nota "SIDRA 179 Censo 1991 domicilios por abastecimento de agua"
python3 -I $M add $D "$S/1436/periodos/2000/variaveis/96?localidades=N1[all]&classificacao=1[0]|61[all]" bruto/sidra_1436_agua_2000.json --nota "SIDRA 1436 Censo 2000"
python3 -I $M add $D "$S/3217/periodos/2010/variaveis/96?localidades=N1[all]&classificacao=1[0]|61[all]|67[0]|309[0]" bruto/sidra_3217_agua_2010.json --nota "SIDRA 3217 Censo 2010"
python3 -I $M add $D "$S/6804/periodos/2022/variaveis/381?localidades=N1[all]&classificacao=301[all]|1817[72125]" bruto/sidra_6804_agua_2022.json --nota "SIDRA 6804 Censo 2022"
python3 -I $M add $D "$S/1437/periodos/2000/variaveis/96?localidades=N1[all]&classificacao=1[0]|11558[all]" bruto/sidra_1437_esgoto_2000.json --nota "SIDRA 1437 Censo 2000 esgotamento"
python3 -I $M add $D "$S/3216/periodos/2010/variaveis/96?localidades=N1[all]&classificacao=1[0]|125[0]|63[0]|299[all]|300[0]" bruto/sidra_3216_esgoto_2010.json --nota "SIDRA 3216 Censo 2010 banheiro/esgotamento"
python3 -I $M add $D "$S/6805/periodos/2022/variaveis/381?localidades=N1[all]&classificacao=11558[all]" bruto/sidra_6805_esgoto_2022.json --nota "SIDRA 6805 Censo 2022 esgotamento"
python3 -I $M add $D "$S/256/periodos/1991/variaveis/96?localidades=N1[all]&classificacao=1[0]|61[0]|60[0]|182[0]|181[0]|1612[all]" bruto/sidra_256_esgoto_1991.json --nota "SIDRA 256 Censo 1991 instalacao sanitaria"
echo FIM-LOTE1
