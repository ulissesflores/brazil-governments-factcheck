#!/bin/zsh
# lote 2: Ipeadata (tbl/pre/ass/pop/PIB/funcoes) + metadados + SIDRA PNAD/PNADC + documentos de quebra
D=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1
M=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py
IP="http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='"
for s in DISOC_INFI BPC_idos BPC_defi FAM_PBF MPAS12_RESPRGPS12 MPAS12_ARRLIQ12 MPAS12_BENPREV12 PAN_PIBPMV DEPIS_POP PNADCA_TXA15MUF PAN_RRPE DFEDUCE DFDELE DFTRAE; do
  python3 -I $M add $D "${IP}${s}')" bruto/ipea_${s}.json --nota "Ipeadata OData ValoresSerie SERCODIGO=${s}"
done
MD="http://www.ipeadata.gov.br/api/odata4/Metadados('"
for s in TXA15M7091 ADH_T_ANALF15M ADH_T_AGUA ADH_T_LUZ PDIAE PDIEREDE DISOC_INFI BPC_idos BPC_defi FAM_PBF MPAS12_RESPRGPS12 MPAS12_ARRLIQ12 MPAS12_BENPREV12 PAN_PIBPMV DEPIS_POP PNADCA_TXA15MUF PAN_RRPE DFEDUCE DFDELE DFTRAE; do
  python3 -I $M add $D "${MD}${s}')" bruto/meta/ipea_meta_${s}.json --nota "Ipeadata Metadados SERCODIGO=${s} (SERATUALIZACAO = vintage; SERCOMENTARIO = definicao)"
done
S="https://servicodados.ibge.gov.br/api/v3/agregados"
python3 -I $M add $D "$S/1187/periodos/all/variaveis/2513?localidades=N1[all]&classificacao=2[all]" bruto/sidra_1187_alfab15_pnad_2004_2015.json --nota "SIDRA 1187 (IDS) taxa de alfabetizacao 15+ PNAD 2004-2015"
python3 -I $M add $D "$S/7113/periodos/all/variaveis/10267?localidades=N1[all]&classificacao=2[6794]|58[2795]" bruto/sidra_7113_analfab15_pnadc_2016_2025.json --nota "SIDRA 7113 taxa de analfabetismo 15+ PNADC anual 2016-2025"
python3 -I $M add $D "$S/1955/periodos/all/variaveis/96?localidades=N1[all]&classificacao=12058[0]|1[0]|61[all]" bruto/sidra_1955_agua_pnad_2001_2015.json --nota "SIDRA 1955 PNAD 2001-2015 domicilios por abastecimento de agua"
python3 -I $M add $D "$S/1956/periodos/all/variaveis/96?localidades=N1[all]&classificacao=12058[0]|1[0]|7173[all]" bruto/sidra_1956_esgoto_pnad_2001_2015.json --nota "SIDRA 1956 PNAD 2001-2015 domicilios por esgotamento sanitario"
python3 -I $M add $D "$S/6731/periodos/all/variaveis/9784?localidades=N1[all]&classificacao=1[6795]|825[all]" bruto/sidra_6731_agua_pnadc_2016_2025.json --nota "SIDRA 6731 PNADC distribuicao % dos domicilios por principal fonte de agua"
python3 -I $M add $D "$S/6735/periodos/all/variaveis/9988?localidades=N1[all]&classificacao=1[6795]|11558[all]" bruto/sidra_6735_esgoto_pnadc_2016_2018.json --nota "SIDRA 6735 PNADC esgotamento 2016-2018 (tabela encerrada em 2018)"
python3 -I $M add $D "$S/7192/periodos/all/variaveis/9988?localidades=N1[all]&classificacao=1[6795]|11558[all]" bruto/sidra_7192_esgoto_pnadc_2019_2025.json --nota "SIDRA 7192 PNADC esgotamento a partir de 2019 (categorias novas)"
python3 -I $M add $D "$S/4708/periodos/all/variaveis/12466?localidades=N1[all]" bruto/sidra_4708_informalidade_pnadc_2016_2025.json --nota "SIDRA 4708 taxa de informalidade 14+ PNADC anual"
python3 -I $M add $D "$S/4660/periodos/all/variaveis/5933?localidades=N1[all]" bruto/sidra_4660_rendimento_real_pnadc_2012_2025.json --nota "SIDRA 4660 rendimento medio mensal real, todos os trabalhos habitual, PNADC anual"
python3 -I $M add $D "$S" bruto/sidra_catalogo_agregados.json --nota "Listagem completa de agregados (tabelas) do SIDRA em 2026-10-19; evidencia de busca para 'sem serie comparavel' (cultura, lazer, transporte, previdencia idosos)"
python3 -I $M add $D "https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2012/notas_tecnicas.pdf" bruto/doc/ibge_sis2012_notas_tecnicas.pdf --nota "doc de quebra: PNAD, area rural da Regiao Norte"
python3 -I $M add $D "http://tabnet.datasus.gov.br/cgi/sinasc/Nascidos_Vivos_1994_2012.pdf" bruto/doc/datasus_sinasc_notas_tecnicas.pdf --nota "doc de quebra: SINASC, DN 2011"
python3 -I $M add $D "http://www.ipeadata.gov.br/doc/AEPS-2018.pdf" bruto/doc/mps_aeps_2018.pdf --nota "doc de quebra: AEPS 2018 (fluxo de caixa da Previdencia); 7,4 MB"
python3 -I $M add $D "https://www.planalto.gov.br/ccivil_03/leis/l8742.htm" bruto/doc/planalto_lei_8742_loas.htm --nota "doc de quebra: BPC, idade (LOAS)"
python3 -I $M add $D "https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm" bruto/doc/planalto_lei_10741_estatuto_idoso.htm --nota "doc de quebra: BPC, art. 34 (65 anos)"
python3 -I $M add $D "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14284.htm" bruto/doc/planalto_lei_14284_auxilio_brasil.htm --nota "doc de quebra: Auxilio Brasil substitui o Bolsa Familia"
python3 -I $M add $D "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14601.htm" bruto/doc/planalto_lei_14601_pbf.htm --nota "doc de quebra: Programa Bolsa Familia reinstituido (2023)"
python3 -I $M add $D "https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/lei/l11457.htm" bruto/doc/planalto_lei_11457_superreceita.htm --nota "doc de quebra: Super-Receita, arrecadacao previdenciaria"
python3 -I $M add $D "https://www.gov.br/planejamento/pt-br/assuntos/orcamento/orcamentos-anuais/1999/portariamog42_1999_atualizada_23jul2012.odt/@@download/file" bruto/doc/portaria_mog_42_1999.odt --nota "doc de quebra/evidencia: classificacao funcional (cultura, desporto e lazer) criada pela Portaria MOG 42/1999"
python3 -I $M add $D "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Nota_Tecnica/2013_12_09_nota_pnad_continua.pdf" bruto/doc/ibge_nota_pnad_continua_2013.pdf --nota "doc de quebra: PNAD Continua substituira PME e PNAD"
echo FIM-LOTE2
