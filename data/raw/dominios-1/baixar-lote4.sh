#!/bin/zsh
# lote 4: aditivo do coordenador (2026-10-19): SAEB, regras de educacao (leis), limiares de elegibilidade (PBF, BPC), deflator e salario minimo
D=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1
M=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py
add() { python3 -I $M add $D "$1" "$2" --nota "$3"; }
# SAEB (INEP)
add "https://download.inep.gov.br/educacao_basica/saeb/2019/presskit/PressKit_Saeb_2019.pdf" bruto/doc/inep_presskit_saeb_2019.pdf "INEP, Press Kit Saeb 2019 (divulgado 2020-09-15): proficiencia media Brasil 1995-2019, LP e MT, 5o/9o ano EF e 3a serie EM (rotulos dos graficos); historico das edicoes"
add "https://download.inep.gov.br/saeb/resultados/relatorio-saeb_volume_1_2023.pdf" bruto/doc/inep_relatorio_saeb_2023_vol1.pdf "INEP, Relatorio Saeb 2023 vol. 1: proficiencia media Brasil 2011-2023 (rotulos dos graficos); declara manter a matriz antiga para comparabilidade"
add "https://download.inep.gov.br/educacao_basica/saeb/documentos_edicoes_antigas/coletanea_de_documentos_de_edicoes_antigas.pdf" bruto/doc/inep_saeb_coletanea_edicoes_antigas.pdf "INEP, coletanea de documentos de edicoes antigas do Saeb: abrangencia amostral/censitaria por edicao, Portaria MEC 931/2005 (Aneb + Anresc/Prova Brasil)"
add "https://download.inep.gov.br/publicacoes/institucionais/avaliacoes_e_exames_da_educacao_basica/escalas_de_proficiencia_do_saeb.pdf" bruto/doc/inep_escalas_proficiencia_saeb.pdf "INEP, Escalas de proficiencia do Saeb (escala 0-500, media 250/DP 50 no 9o ano EF de 1997)"
# indicadores de fluxo (dependentes de regra) via Banco Mundial/UIS
add "https://api.worldbank.org/v2/country/BRA/indicator/SE.PRM.REPT.ZS?format=json&per_page=20000" bruto/wb_SE.PRM.REPT.ZS.json "Banco Mundial WDI (UIS): repetentes no ensino primario, % da matricula; dependente de regra (promocao automatica / ciclos)"
add "https://api.worldbank.org/v2/country/BRA/indicator/SE.PRM.PRSL.ZS?format=json&per_page=20000" bruto/wb_SE.PRM.PRSL.ZS.json "Banco Mundial WDI (UIS): persistencia ate a ultima serie do primario, % da coorte; dependente de regra"
# regras da educacao (Planalto)
P=https://www.planalto.gov.br/ccivil_03
add "$P/leis/l9394.htm" bruto/doc/leg/lei_9394_ldb.htm "LDB, arts. 23 e 32 (ciclos, progressao regular por serie, ensino fundamental)"
add "$P/_ato2004-2006/2006/lei/l11274.htm" bruto/doc/leg/lei_11274_ef9anos.htm "Lei 11.274/2006: ensino fundamental de 9 anos"
add "$P/constituicao/emendas/emc/emc59.htm" bruto/doc/leg/ec_59_2009.htm "EC 59/2009: obrigatoriedade 4 a 17 anos, fim da DRU na educacao"
add "$P/constituicao/emendas/emc/emc14.htm" bruto/doc/leg/ec_14_1996_fundef.htm "EC 14/1996: Fundef"
add "$P/constituicao/emendas/emc/emc53.htm" bruto/doc/leg/ec_53_2006_fundeb.htm "EC 53/2006: Fundeb"
add "$P/leis/l9424.htm" bruto/doc/leg/lei_9424_fundef.htm "Lei 9.424/1996: Fundef"
add "$P/_ato2007-2010/2007/lei/l11494.htm" bruto/doc/leg/lei_11494_fundeb.htm "Lei 11.494/2007: Fundeb"
add "$P/_ato2019-2022/2020/lei/L14113.htm" bruto/doc/leg/lei_14113_fundeb_permanente.htm "Lei 14.113/2020: Fundeb permanente"
add "$P/constituicao/emendas/emc/emc108.htm" bruto/doc/leg/ec_108_2020.htm "EC 108/2020: Fundeb permanente"
add "https://old.scielo.br/pdf/pp/v21n3/v21n3a12.pdf" bruto/doc/leg/scielo_pp_progressao_continuada_sp.pdf "SECUNDARIA: artigo (Pro-Posicoes) que cita Deliberacao CEE 9/97 e Resolucao SE 4/98 (progressao continuada em SP); texto oficial nao localizado"
# limiares de elegibilidade: Bolsa Familia / Auxilio Brasil
add "$P/_ato2004-2006/2004/lei/l10.836.htm" bruto/doc/leg/lei_10836_pbf.htm "Lei 10.836/2004 (PBF), compilada"
add "$P/_ato2004-2006/2004/decreto/d5209.htm" bruto/doc/leg/dec_5209_2004.htm "Decreto 5.209/2004, compilado (art. 18: linhas 100/50 e alteracoes posteriores)"
add "$P/_ato2004-2006/2006/decreto/d5749.htm" bruto/doc/leg/dec_5749_2006.htm "Decreto 5.749/2006: 120/60"
add "$P/_ato2007-2010/2009/decreto/d6824.htm" bruto/doc/leg/dec_6824_2009.htm "Decreto 6.824/2009: 137/69"
add "$P/_ato2007-2010/2009/decreto/d6917.htm" bruto/doc/leg/dec_6917_2009.htm "Decreto 6.917/2009: 140/70, efeitos financeiros desde 1/9/2009"
add "$P/_ato2011-2014/2014/decreto/d8232.htm" bruto/doc/leg/dec_8232_2014.htm "Decreto 8.232/2014: 154/77"
add "$P/_ato2015-2018/2016/decreto/d8794.htm" bruto/doc/leg/dec_8794_2016.htm "Decreto 8.794/2016: 170/85"
add "$P/_ato2015-2018/2018/decreto/D9396.htm" bruto/doc/leg/dec_9396_2018.htm "Decreto 9.396/2018: 178/89"
add "$P/_ato2019-2022/2021/decreto/D10852.htm" bruto/doc/leg/dec_10852_2021_auxilio_brasil.htm "Decreto 10.852/2021 (Auxilio Brasil): 200/100, compilado"
add "$P/_ato2019-2022/2022/decreto/D11013.htm" bruto/doc/leg/dec_11013_2022.htm "Decreto 11.013/2022: 210/105"
add "$P/_ato2023-2026/2023/decreto/D11566.htm" bruto/doc/leg/dec_11566_2023.htm "Decreto 11.566/2023: linha unica R$ 218"
add "$P/_ato2023-2026/2023/lei/L14601.htm" bruto/doc/leg/lei_14601_2023_pbf.htm "Lei 14.601/2023 (PBF): renda per capita ate R$ 218"
add "$P/_ato2019-2022/2021/lei/L14284.htm" bruto/doc/leg/lei_14284_2021_auxilio_brasil_cp.htm "Lei 14.284/2021 (Auxilio Brasil)"
# BPC
add "$P/_ato2019-2022/2020/lei/L13981.htm" bruto/doc/leg/lei_13981_2020_bpc.htm "Lei 13.981/2020: BPC, renda per capita inferior a 1/2 salario minimo (texto)"
add "$P/_ato2019-2022/2021/lei/L14176.htm" bruto/doc/leg/lei_14176_2021_bpc.htm "Lei 14.176/2021: BPC, 1/4 SM com possibilidade de ampliar ate 1/2 SM"
# deflator e salario minimo
add "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json" bruto/bcb_sgs433_ipca_mensal.json "BCB SGS 433: IPCA, variacao mensal % (deflator dos limiares)"
add "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='MTE12_SALMIN12')" bruto/ipea_MTE12_SALMIN12.json "Ipeadata MTE12_SALMIN12: salario minimo vigente (mensal), para o limiar de 1/4 e 1/2 SM do BPC"
echo FIM-LOTE4
