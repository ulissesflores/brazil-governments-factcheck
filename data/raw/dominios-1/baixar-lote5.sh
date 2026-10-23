#!/bin/zsh
D=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1
M=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py
python3 -I $M add $D "https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/42a50edf01ee9b102e4c892fa5b03a7a.pdf" bruto/doc/ibge_pnadc_coleta_nao_presencial_2020.pdf --nota "doc de quebra: PNAD Continua, coleta nao presencial (telefone) a partir de marco/2020"
python3 -I $M add $D "https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc103.htm" bruto/doc/leg/ec_103_2019_previdencia.htm --nota "doc de quebra: EC 103/2019, reforma da previdencia (RGPS)"
for s in MEDUCA MTE12_SALMIN12; do
  python3 -I $M add $D "http://www.ipeadata.gov.br/api/odata4/Metadados('${s}')" bruto/meta/ipea_meta_${s}.json --nota "Ipeadata Metadados SERCODIGO=${s} (vintage e definicao)"
done
echo FIM-LOTE5
