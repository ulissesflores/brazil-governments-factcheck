# Dominios-1: educacao, moradia, previdencia, assistencia, trabalho (alem de 2 linhas), maternidade, e o que nao tem serie

Dossie: governos-do-brasil-economia. Coleta e conferencia em 2026-10-19. Sem opiniao politica: so bruto como publicado, vintage e quebra. Nenhum numero daqui foi comparado com o infografico (estes dominios nao estao nele), por isso nao ha marcas de conferencia (certo/aproximado/errado/nao verificado).

Como reproduzir: `python3 -I /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1/recalcula.py` (sem rede; confere o sha256 de cada bruto e a cadeia do `manifest.jsonl`; grava `series/*.csv`, `janelas.csv`, `quebras.csv`, `busca-sem-serie.csv`) e depois `python3 -I resultado.py` (grava este arquivo). Verificacao da cadeia: `python3 /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py verify /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1`.

## 0. Achado e nao achado

1. **Achado.** 752 linhas em 6 arquivos de serie, 35 indicadores, cada linha com `vintage` e `dependente_de_regra`. Tem extensao de 30 anos ou mais (ultimo - primeiro ano + 1), entre os indicadores de dados: edu_alfabetizacao_adultos_wdi, edu_analfab15, edu_persistencia_ultima_serie_primario, edu_repetentes_primario_pct, mat_prenatal7, mat_prenatal_ignorado, mat_prenatal_nenhuma, mor_agua_rede_geral, mor_esgoto_adequado. Cumprem tambem a regra de fonte homogenea (uma so fonte/metodo para o primario) apenas os de Censo e SINASC: edu_analfab15, mor_agua_rede_geral, mor_esgoto_adequado e mat_prenatal*; os tres do WDI/UIS ficam como 'nao verificada'. A extensao nao e densidade: os Censos dao 4 pontos em 32 anos (1991-2022; mais 1970 e 1980 pelo Atlas 1998), o WDI/UIS 20 a 30 pontos esparsos, o SINASC 30 anos completos. Na maior parte dos governos de 1964-1989 so ha 1970 e 1980 (analfabetismo e esgoto) e, para repetencia e persistencia, os pontos do WDI.
2. **Quase passam.** Saeb (proficiencia media, 1995-2023, escala equalizada pela TRI) tem 29 anos de cobertura e o BPC por mil habitantes (1996-2024) tem 29: ficam a um ano do corte e entram marcados como `NAO` na tabela 2, nao omitidos.
3. **Nao achado (sem serie comparavel):** cultura, lazer, transporte; Ideb e Pisa (cobertura <30 anos, arquivo do INEP nao localizado); deficit habitacional da Fundacao Joao Pinheiro; proporcao de 65+ com aposentadoria/pensao; gasto federal em assistencia; **taxas de aprovacao, reprovacao, abandono e distorcao idade-serie (nao coletadas: planilhas do INEP nao localizadas)**. Evidencia da busca: `busca-sem-serie.csv` e secao 5.
4. **Quebras:** 34 linhas em `quebras.csv` (16 de metodo estatistico, 14 de mudanca de regra, 4 de revisao de vintage). So em 9 ha efeito medido (sobreposicao real nos dados baixados); nas demais a coluna diz `sem sobreposicao`. Maiores efeitos medidos: costura PDIAE em 1991 (+9,07 p.p. contra o recalculo do SIDRA), PNADC contra Censo no esgoto de 2022 (+8,00 p.p. no mesmo universo), 'ligacao a rede' contra 'rede como principal forma' em 2022 (+7,10 p.p.), PNADC contra Censo no analfabetismo de 2022 (-1,40 p.p.).
5. **Regra que move o indicador:** a linha de pobreza do Bolsa Familia/Auxilio Brasil em R$ de dez/2025 vai de 309 (2004) a 218 (2025), com duas linhas ate 2022 e uma so (R$ 218) desde a Lei 14.601/2023; a idade minima do BPC por idade cai de 70 para 67 (1998) e 65 (2004). Esses limiares estao em `series/ass.csv` e `series/limiares_eventos.csv`.
6. **Saeb:** as duas vintages (Press Kit 2019 e Relatorio 2023) coincidem em 30 de 30 pontos de 2011-2019; o INEP declara que a escala 'permaneceu a mesma'. Mesmo assim ha quebras de desenho (Aneb + Prova Brasil em 2005; ensino fundamental de 9 anos desde a Lei 11.274/2006), sem sobreposicao para medir.

## 1. Fontes e cadeia de hash

`manifest.jsonl`: 149 arquivos, cabeca da cadeia = sha256 da ultima linha (conferida por `recalcula.py`). Fontes principais (URL completa, tipo):

| Fonte | URL / consulta | Onde esta o bruto | Observacao |
| --- | --- | --- | --- |
| Ipeadata OData (series e metadados) | http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='X') e .../Metadados('X') | bruto/ipea_*.json, bruto/meta/ipea_meta_*.json | a vintage de cada serie = SERATUALIZACAO do metadado |
| IBGE SIDRA (API agregados v3) | https://servicodados.ibge.gov.br/api/v3/agregados/{tabela}/periodos/.../variaveis/...?localidades=N1[all]&classificacao=... | bruto/sidra_*.json, bruto/meta/sidra_meta_*.json | o servidor devolve gzip mesmo sem pedir; o arquivo guardado e exatamente o que veio (gzip), o leitor descompacta |
| DATASUS TabNet (SINASC) | http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinasc/cnv/nvuf.def (POST; parametros em scripts/baixar_sinasc.py) | bruto/tabnet_sinasc_prenatal_ano_1994_2025.html | registrado com `add-local` (POST nao e coberto pelo `add`); dados finais ate 2024, 2025 preliminar |
| INEP (Saeb) | https://download.inep.gov.br/educacao_basica/saeb/2019/presskit/PressKit_Saeb_2019.pdf; https://download.inep.gov.br/saeb/resultados/relatorio-saeb_volume_1_2023.pdf | bruto/doc/inep_*.pdf | baixados com curl e registrados com `add-local` (urllib falhou na verificacao do certificado); valores lidos dos rotulos dos graficos com `pdftotext -bbox` |
| Banco Mundial WDI | https://api.worldbank.org/v2/country/BRA/indicator/{codigo}?format=json&per_page=20000 | bruto/wb_*.json | repetentes, persistencia, gasto em educacao, alfabetizacao de adultos |
| MPS (AEPS 2018) e fluxo de caixa | http://www.ipeadata.gov.br/doc/AEPS-2018.pdf | bruto/doc/mps_aeps_2018.pdf | documento de quebra (7,4 MB) |
| Planalto (leis, decretos, emendas) | https://www.planalto.gov.br/ccivil_03/... | bruto/doc/*.htm, bruto/doc/leg/*.htm | texto compilado; datas de vigencia lidas do proprio texto |
| BCB SGS 433 (IPCA) | https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json | bruto/bcb_sgs433_ipca_mensal.json | deflator dos limiares (R$ de dez/2025) |

Catalogos de busca: listagem de tabelas do SIDRA em `bruto/sidra_catalogo_agregados.json` (nesta cadeia) e catalogo Ipeadata de 4.071 series em `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/social/bruto/ipea_metadados_all.json` (cadeia da pasta social; `recalcula.py` confere o sha256 contra o manifest de la).

## 2. Indicadores, cobertura e corte de 30 anos

Regra pre-registrada: fonte oficial, cobertura nacional, frequencia anual (decenal aceita para Censo), pelo menos 30 anos de cobertura ou sobreposicao medida em cada quebra, e uma serie homogenea para o primario (regra 3). 'Cobertura' = ultimo ano - primeiro ano + 1 da serie primaria; pontos = anos com valor.

| Dominio | Indicador (primario) | Fonte | Primeiro-ultimo ano | Pontos | Cobertura (anos) | Extensao >= 30 anos | Fonte homogenea (regra 3) | dependente_de_regra |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ass | ass_bpc_idade_minima | Planalto(Lei 8.742/1993 art. 20 e 38; Lei 9.720/ | 1996-2025 | 30 | 30 | sim | sim (uma so fonte/metodo) | n/a (e a propria regra) |
| ass | ass_bpc_limiar_meio_sm_real | Planalto(Lei 13.981/2020; Lei 14.176/2021)+MTE+B | 2020-2025 | 6 | 6 | NAO | sim (uma so fonte/metodo) | n/a (e a propria regra) |
| ass | ass_bpc_limiar_quarto_sm_real | Planalto(Lei 8.742/1993 art. 20 par.3)+MTE(salar | 1996-2025 | 30 | 30 | sim | sim (uma so fonte/metodo) | n/a (e a propria regra) |
| ass | ass_bpc_por_mil_hab | MDS-BPC(Ipeadata BPC_idos+BPC_defi) / IBGE-Pop(D | 1996-2024 | 29 | 29 | NAO | sim (uma so fonte/metodo) | sim |
| ass | ass_pbf_familias_por_mil_hab | MDS-PBF(Ipeadata FAM_PBF) / IBGE-Pop(DEPIS_POP) | 2004-2024 | 21 | 21 | NAO | sim (uma so fonte/metodo) | sim |
| ass | ass_pbf_limiar_extrema_pobreza_real | Planalto(decretos/leis do PBF)+BCB-IPCA(SGS433) | 2004-2022 | 19 | 19 | NAO | sim (uma so fonte/metodo) | n/a (e a propria regra) |
| ass | ass_pbf_limiar_pobreza_real | Planalto(decretos/leis do PBF)+BCB-IPCA(SGS433) | 2004-2025 | 22 | 22 | NAO | sim (uma so fonte/metodo) | n/a (e a propria regra) |
| edu | edu_alfabetizacao_adultos_wdi | Banco Mundial WDI(SE.ADT.LITR.ZS) | 1980-2024 | 22 | 45 | sim | nao verificada (compilacao UIS de fontes nacionais) | nao |
| edu | edu_analfab15 | Atlas-DH-Censo(ADH_T_ANALF15M) | 1991-2022 | 4 | 32 | sim | sim (uma so fonte/metodo) | nao |
| edu | edu_anos_estudo_15mais | IBGE-PNADC(SIDRA7126) | 2016-2025 | 8 | 10 | NAO | sim (uma so fonte/metodo) | nao |
| edu | edu_anos_estudo_25mais | Ipea-Atlas(MEDUCA) | 1991-2000 | 2 | 10 | NAO | sim (uma so fonte/metodo) | nao |
| edu | edu_gasto_publico_pib | Banco Mundial WDI(SE.XPD.TOTL.GD.ZS) | 1995-2022 | 25 | 28 | NAO | nao verificada (compilacao UIS de fontes nacionais) | sim |
| edu | edu_persistencia_ultima_serie_primario | Banco Mundial WDI(SE.PRM.PRSL.ZS) | 1971-2003 | 20 | 33 | sim | nao verificada (compilacao UIS de fontes nacionais) | sim |
| edu | edu_repetentes_primario_pct | Banco Mundial WDI(SE.PRM.REPT.ZS) | 1970-2011 | 30 | 42 | sim | nao verificada (compilacao UIS de fontes nacionais) | sim |
| edu | edu_saeb_LP_EF_5ano_4serie | INEP-Saeb(PressKit2019) | 1995-2023 | 15 | 29 | NAO | sim (uma so fonte/metodo) | nao |
| edu | edu_saeb_LP_EF_9ano_8serie | INEP-Saeb(PressKit2019) | 1995-2023 | 15 | 29 | NAO | sim (uma so fonte/metodo) | nao |
| edu | edu_saeb_LP_EM_3serie | INEP-Saeb(PressKit2019) | 1995-2023 | 15 | 29 | NAO | sim (uma so fonte/metodo) | nao |
| edu | edu_saeb_MT_EF_5ano_4serie | INEP-Saeb(PressKit2019) | 1995-2023 | 15 | 29 | NAO | sim (uma so fonte/metodo) | nao |
| edu | edu_saeb_MT_EF_9ano_8serie | INEP-Saeb(PressKit2019) | 1995-2023 | 15 | 29 | NAO | sim (uma so fonte/metodo) | nao |
| edu | edu_saeb_MT_EM_3serie | INEP-Saeb(PressKit2019) | 1995-2023 | 15 | 29 | NAO | sim (uma so fonte/metodo) | nao |
| mat | mat_prenatal7 | MS-SINASC(TabNet) | 1995-2024 | 30 | 30 | sim | sim (uma so fonte/metodo) | nao |
| mat | mat_prenatal_ignorado | MS-SINASC(TabNet) | 1995-2024 | 30 | 30 | sim | sim (uma so fonte/metodo) | nao |
| mat | mat_prenatal_nenhuma | MS-SINASC(TabNet) | 1995-2024 | 30 | 30 | sim | sim (uma so fonte/metodo) | nao |
| mor | mor_agua_encanada_pop | Atlas-DH-Censo(ADH_T_AGUA) | 1991-2010 | 3 | 20 | NAO | sim (uma so fonte/metodo) | nao |
| mor | mor_agua_rede_geral | IBGE-Censo(SIDRA) | 1991-2022 | 4 | 32 | sim | sim (uma so fonte/metodo) | nao |
| mor | mor_esgoto_adequado | IBGE-Censo(SIDRA) | 1991-2022 | 4 | 32 | sim | sim (uma so fonte/metodo) | nao |
| mor | mor_esgoto_rede | IBGE-Censo(Ipeadata PDIEREDE) | 2000-2022 | 3 | 23 | NAO | sim (uma so fonte/metodo) | nao |
| mor | mor_esgoto_rede_ou_fossa_ligada | IBGE-PNADC(SIDRA6735) | 2016-2018 | 3 | 3 | NAO | sim (uma so fonte/metodo) | nao |
| mor | mor_esgoto_rede_ou_fossa_ligada | IBGE-PNADC(SIDRA7192) | 2019-2025 | 5 | 7 | NAO | sim (uma so fonte/metodo) | nao |
| mor | mor_luz | Atlas-DH-Censo(ADH_T_LUZ) | 1991-2010 | 3 | 20 | NAO | sim (uma so fonte/metodo) | nao |
| pre | pre_rgps_arrecadacao_liquida_pib | MPS-fluxo-de-caixa(Ipeadata MPAS12_*) / IBGE-PIB | 2004-2025 | 22 | 22 | NAO | sim (uma so fonte/metodo) | sim |
| pre | pre_rgps_beneficios_pib | MPS-fluxo-de-caixa(Ipeadata MPAS12_*) / IBGE-PIB | 2004-2025 | 22 | 22 | NAO | sim (uma so fonte/metodo) | sim |
| pre | pre_rgps_resultado_pib | MPS-fluxo-de-caixa(Ipeadata MPAS12_*) / IBGE-PIB | 2004-2025 | 22 | 22 | NAO | sim (uma so fonte/metodo) | sim |
| tbl | tbl_informalidade | Ipea-PNAD(DISOC_INFI) | 1992-2014 | 20 | 23 | NAO | sim (uma so fonte/metodo) | sim |
| tbl | tbl_informalidade_ibge | IBGE-PNADC(SIDRA4708) | 2016-2025 | 10 | 10 | NAO | sim (uma so fonte/metodo) | sim |
| tbl | tbl_renda_trabalho_real | IBGE-PNAD(SIDRA1871 deflacionado) | 2001-2015 | 14 | 15 | NAO | sim (uma so fonte/metodo) | nao |

Series de sensibilidade (outras fontes, nunca emendadas na primaria) ficam em `series/*.csv` com `fonte` diferente e em `janelas.csv` com o sufixo `__<fonte>` no identificador.

## 3. Resultado por governo (media na janela do mandato, entre parenteses o numero de anos com dado)

Regra fixa de atribuicao: o ano pertence ao governo que ocupa o cargo em 1o de julho. Datas de `brazil-governments-factcheck/data/curated/mandatos.csv` (inclui os cinco governos que o infografico omite: Castelo Branco, Geisel, Figueiredo, Sarney, Collor; a Junta Militar de 1969 nao contem 1o de julho e sempre fica sem dado). `-` = nenhum ano com dado na janela; nao ha interpolacao. Anos sinalizados `ANOMALIA`, `PRELIMINAR` ou `FORA_DA_JANELA` ficam na serie e fora das janelas (secao 8). Cada indicador esta nos dois sentidos: nenhum foi retirado depois de ver o resultado.

### 3.1 Educacao: alfabetizacao

| Governo | Analfabetismo 15+ %, Atlas DH (primaria) | idem, Atlas 1998 (1970-1991) | idem, PNAD 2004-2015 | idem, PNADC 2016+ |
| --- | --- | --- | --- | --- |
| Medici | - | 32.97 (1) | - | - |
| Figueiredo | - | 25.34 (1) | - | - |
| Collor | 20.07 (1) | 19.40 (1) | - | - |
| Fernando Henrique Cardoso | 13.63 (1) | - | - | - |
| Lula (1o e 2o mandatos) | 9.61 (1) | - | 10.50 (6) | - |
| Dilma Rousseff | - | - | 8.42 (5) | 6.70 (1) |
| Michel Temer | - | - | - | 6.40 (2) |
| Jair Bolsonaro | 7.00 (1) | - | - | 5.85 (2) |
| Lula (3o mandato) | - | - | - | 5.20 (3) |

### 3.2 Educacao: Saeb, proficiencia media (pontos, escala 0-500; Press Kit 2019 ate 2009, Relatorio 2023 de 2011 em diante)

| Governo | LP 5o ano | LP 9o ano | LP 3a EM | MT 5o ano | MT 9o ano | MT 3a EM |
| --- | --- | --- | --- | --- | --- | --- |
| Fernando Henrique Cardoso | 177.8 (4) | 243.5 (4) | 275.8 (4) | 184.8 (4) | 248.0 (4) | 282.0 (4) |
| Lula (1o e 2o mandatos) | 175.2 (4) | 235.8 (4) | 263.8 (4) | 189.0 (4) | 245.2 (4) | 274.5 (4) |
| Dilma Rousseff | 198.3 (3) | 247.7 (3) | 266.7 (3) | 213.3 (3) | 253.7 (3) | 270.7 (3) |
| Michel Temer | 215.0 (1) | 258.0 (1) | 268.0 (1) | 224.0 (1) | 258.0 (1) | 270.0 (1) |
| Jair Bolsonaro | 211.5 (2) | 259.0 (2) | 276.5 (2) | 222.5 (2) | 259.5 (2) | 273.5 (2) |
| Lula (3o mandato) | 214.0 (1) | 259.0 (1) | 276.0 (1) | 225.0 (1) | 257.0 (1) | 272.0 (1) |

### 3.3 Educacao: indicadores que dependem de regra (`dependente_de_regra=sim`) e outros

| Governo | Repetentes, primario, % (WDI) | Persistencia ate a ultima serie, % (WDI) | Gasto em educacao, % PIB (WDI) | Alfabetizacao de adultos % (WDI) | Anos de estudo 25+ (Censo) | Anos de estudo 15+ (PNADC) |
| --- | --- | --- | --- | --- | --- | --- |
| Medici | 17.87 (4) | 40.59 (3) | - | - | - | - |
| Geisel | 19.38 (5) | 45.29 (5) | - | - | - | - |
| Figueiredo | 20.73 (5) | 48.25 (5) | - | 74.59 (1) | - | - |
| Sarney | 19.71 (2) | - | - | - | - | - |
| Collor | 18.15 (1) | 71.32 (2) | - | - | 4.87 (1) | - |
| Itamar Franco | 18.75 (2) | 74.01 (1) | - | - | - | - |
| Fernando Henrique Cardoso | 22.78 (4) | 82.82 (3) | 4.11 (6) | 86.37 (1) | 5.87 (1) | - |
| Lula (1o e 2o mandatos) | 15.14 (6) | 80.62 (1) | 4.95 (7) | 89.83 (6) | - | - |
| Dilma Rousseff | 8.75 (1) | - | 5.99 (6) | 91.80 (6) | - | 9.30 (1) |
| Michel Temer | - | - | 6.20 (2) | 93.16 (2) | - | 9.55 (2) |
| Jair Bolsonaro | - | - | 5.71 (4) | 94.45 (4) | - | 9.90 (2) |
| Lula (3o mandato) | - | - | - | 94.66 (2) | - | 10.23 (3) |

### 3.4 Moradia

| Governo | Agua por rede geral %, Censo IBGE | Esgoto adequado %, Censo IBGE | Esgoto adequado %, Ipea PDIAE (1970+; ver quebra 17) | Agua encanada %, Atlas DH | Luz eletrica %, Atlas DH |
| --- | --- | --- | --- | --- | --- |
| Medici | - | - | 42.28 (1) | - | - |
| Figueiredo | - | - | 52.86 (1) | - | - |
| Collor | 70.71 (1) | 49.78 (1) | 58.85 (1) | 71.31 (1) | 84.84 (1) |
| Fernando Henrique Cardoso | 77.82 (1) | 62.20 (1) | 62.20 (1) | 81.79 (1) | 93.46 (1) |
| Lula (1o e 2o mandatos) | 82.85 (1) | 67.06 (1) | 67.06 (1) | 92.72 (1) | 98.58 (1) |
| Jair Bolsonaro | 83.88 (1) | 77.41 (1) | 77.42 (1) | - | - |

### 3.5 Trabalho (alem de desemprego e salario minimo, que ja estao na pasta economia-real)

| Governo | Informalidade % (Ipea, PNAD 1992-2014) | Informalidade % (IBGE, PNADC 2016+) | Renda real do trabalho, R$ dez/2025 (PNAD 2001-2015) | idem, PNADC 2012-2025 (nominal deflacionado) | idem, PNAD 1996-2006 como publicado (base de precos nao declarada) |
| --- | --- | --- | --- | --- | --- |
| Collor | 56.38 (1) | - | - | - | - |
| Itamar Franco | 57.20 (1) | - | - | - | - |
| Fernando Henrique Cardoso | 58.33 (7) | - | 2180.65 (2) | - | 797.33 (6) |
| Lula (1o e 2o mandatos) | 54.26 (7) | - | 2236.69 (7) | - | 734.50 (4) |
| Dilma Rousseff | 47.06 (4) | 39.10 (1) | 2922.33 (5) | 3219.20 (5) | - |
| Michel Temer | - | 40.75 (2) | - | 3229.30 (2) | - |
| Jair Bolsonaro | - | 39.45 (4) | - | 3207.47 (4) | - |
| Lula (3o mandato) | - | 38.77 (3) | - | 3439.17 (3) | - |

### 3.6 Previdencia (RGPS, % do PIB nominal; 2004-2025)

| Governo | Arrecadacao liquida | Beneficios previdenciarios | Resultado primario (negativo = deficit) |
| --- | --- | --- | --- |
| Lula (1o e 2o mandatos) | 5.18 (7) | 6.65 (7) | -1.47 (7) |
| Dilma Rousseff | 5.75 (6) | 6.99 (6) | -1.23 (6) |
| Michel Temer | 5.64 (2) | 8.47 (2) | -2.78 (2) |
| Jair Bolsonaro | 5.34 (4) | 8.30 (4) | -2.91 (4) |
| Lula (3o mandato) | 5.48 (3) | 8.12 (3) | -2.60 (3) |

### 3.7 Assistencia: cobertura e limiares de elegibilidade

| Governo | BPC (idosos+deficiencia) por mil hab., dez | Bolsa Familia/Auxilio Brasil por mil hab., dez | Idade minima do BPC idoso | 1/4 do SM em R$ dez/2025 | Linha de pobreza do PBF, R$ dez/2025 | Linha de extrema pobreza do PBF, R$ dez/2025 |
| --- | --- | --- | --- | --- | --- | --- |
| Fernando Henrique Cardoso | 5.92 (7) | - | 67.86 (7) | 165.95 (7) | - | - |
| Lula (1o e 2o mandatos) | 14.05 (8) | 56.38 (7) | 65.25 (8) | 246.26 (8) | 320.06 (7) | 160.03 (7) |
| Dilma Rousseff | 20.00 (5) | 69.93 (6) | 65.00 (6) | 323.42 (6) | 276.99 (6) | 138.50 (6) |
| Michel Temer | 22.64 (2) | 69.15 (2) | 65.00 (2) | 349.45 (2) | 257.17 (2) | 128.59 (2) |
| Jair Bolsonaro | 23.47 (4) | 76.93 (4) | 65.00 (4) | 343.54 (4) | 241.69 (4) | 120.84 (4) |
| Lula (3o mandato) | 29.36 (2) | 101.09 (2) | 65.00 (3) | 369.42 (3) | 227.86 (3) | - |

### 3.8 Maternidade e infancia (mortalidade infantil ja existe em `social/series/mortinf.csv`, nao refeita)

| Governo | 7+ consultas, % dos informados | Numero de consultas ignorado, % dos nascimentos | Nenhuma consulta, % dos informados |
| --- | --- | --- | --- |
| Fernando Henrique Cardoso | 48.28 (4) | 17.47 (8) | 4.76 (4) |
| Lula (1o e 2o mandatos) | 55.87 (8) | 1.47 (8) | 2.29 (8) |
| Dilma Rousseff | 64.58 (6) | 0.84 (6) | 2.55 (6) |
| Michel Temer | 70.39 (2) | 0.45 (2) | 1.80 (2) |
| Jair Bolsonaro | 73.22 (4) | 0.52 (4) | 1.65 (4) |
| Lula (3o mandato) | 78.45 (2) | 0.42 (2) | 1.37 (2) |

## 4. Regras de politica que mudam o que o indicador mede (educacao)

| Data | Regra | Fonte primaria (URL) | Indicador afetado |
| --- | --- | --- | --- |
| 1996-12-20 | LDB (Lei 9.394): ciclos e progressao continuada permitidos (art. 23; art. 32, par. 2) | https://www.planalto.gov.br/ccivil_03/leis/l9394.htm | repetentes, persistencia (dependente_de_regra=sim) |
| 1998 (SP) | Progressao continuada em ciclos na rede estadual de Sao Paulo (Deliberacao CEE 9/97; Resolucao SE 4/98). Texto oficial nao localizado; citado por artigo (fonte SECUNDARIA) | https://www.scielo.br/pdf/pp/v21n3/v21n3a12.pdf | repetentes |
| 1998-01-01 | Fundef (EC 14/1996; Lei 9.424/1996) | https://www.planalto.gov.br/ccivil_03/leis/l9424.htm | gasto em educacao |
| 2005-03-21 | Portaria MEC 931/2005: Saeb = Aneb (amostral) + Anresc/Prova Brasil (censitaria nas escolas publicas) | https://download.inep.gov.br/educacao_basica/saeb/documentos_edicoes_antigas/coletanea_de_documentos_de_edicoes_antigas.pdf | Saeb |
| 2006-02-06 | Lei 11.274: ensino fundamental de 9 anos, matricula aos 6 anos (implantacao ate 2010) | https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11274.htm | Saeb 5o e 9o anos (rotulo 4a/8a serie ate entao) |
| 2007-01-01 | Fundeb (EC 53/2006; Lei 11.494/2007) | https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/lei/l11494.htm | gasto em educacao |
| 2009-11-11 | EC 59/2009: educacao basica obrigatoria dos 4 aos 17 anos | https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc59.htm | gasto, anos de estudo, Saeb EM |
| 2020-08-26 | Fundeb permanente (EC 108/2020; Lei 14.113/2020) | https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc108.htm | gasto em educacao |

Os valores brutos de repetentes (WDI/UIS) foram publicados assim e nao foram atribuidos a regra nenhuma: 1992=18.1, 2000=25.0, 2004=20.1, 2008=11.8, 2011=8.7 (% da matricula; anos ausentes na fonte nao foram preenchidos).

### Definicao de 'alfabetizado' em cada fonte (o que cada metadado diz)

| Fonte | O que a fonte diz | Onde |
| --- | --- | --- |
| Atlas DH (ADH_T_ANALF15M, Censos 1991-2022) | razao entre a populacao de 15+ que 'nao sabe ler nem escrever um bilhete simples' e o total de 15+ | `bruto/meta/ipea_meta_ADH_T_ANALF15M.json` |
| Atlas 1998 (TXA15M7091, Censos 1970-1991) | 'pessoas de 15 ou mais anos de idade que nao sabem ler nem escrever um bilhete simples' | `bruto/meta/ipea_meta_TXA15M7091.json` |
| IBGE SIDRA (Censo 2022, tab. 9542; PNAD IDS 1187; PNADC 7113) | os metadados baixados trazem so o titulo da tabela ('taxa de alfabetizacao/analfabetismo das pessoas de 15 anos ou mais'); a pergunta do questionario nao esta nos arquivos baixados | `bruto/meta/sidra_meta_*.json` |

A diferenca de -1,40 p.p. entre PNADC e Censo em 2022 (quebra 2) e a unica medida, no mesmo ano, de quanto a pesquisa amostral se afasta do recenseamento nesta pergunta; a definicao de 'alfabetizado' do IBGE nao foi lida em documento do questionario, entao nao atribuo a diferenca a ela.

## 5. O que nao tem serie comparavel (evidencia da busca)

| Dominio | Candidato | Onde procurei | O que apareceu | Conclusao |
| --- | --- | --- | --- | --- |
| cul | gasto federal na funcao cultura, % do orcamento | catalogo Ipeadata (4071 series; sha256 0927071bf904, pasta social) (cultur) | 5 series: DFEDUCE, DFEDUCM, BPAG12_SERCULT12, BPAG12_SERCULTD12, BPAG12_SERCULTR12; todas de outro tipo (estaduais combinadas 'educacao e cultura' ou balanco de pagamentos) | sem serie comparavel: o Ipeadata so tem a funcao Educacao+Cultura somada e so estadual/municipal; a funcao Cultura separada nasce na Portaria MOG 42/1999 (bruto/doc/portaria_mog_42_1999.odt) |
| cul | acesso a cultura (equipamentos/participacao) | listagem de tabelas do SIDRA (bruto/sidra_catalogo_agregados.json) (cultur/bibliotec/museu/cinema/teatro) | 807 tabelas; ids: 1101, 1109, 1110, 1111, 1112, 1113, 1115, 1116, 1117, 1118, 1119, 1224... | tabelas pontuais (MUNIC/POF/suplementos), sem serie anual nacional de 30 anos com metodo unico |
| laz | gasto publico em desporto e lazer / acesso a lazer | catalogo Ipeadata (4071 series; sha256 0927071bf904, pasta social) (lazer/desport/esporte) | 2 series: DFDELE, DFDELM | so DFDELE/DFDELM (despesa estadual/municipal na funcao Desporto e Lazer); DFDELE comeca em 2002 (24 anos, ver ipea_DFDELE.json): nao qualifica (<30 anos) e e despesa, nao acesso |
| laz | acesso a lazer | listagem de tabelas do SIDRA (lazer/esporte/desporto/turismo/viag) | 59 tabelas; ids: 5885, 6812, 6984, 7282, 7402, 7403, 7405, 8495, 9347, 4250, 4251, 4252 | suplementos pontuais (ex.: turismo/viagens PNADC a partir de 2019, tabelas 6411/7229/7234/7251), sem serie de 30 anos |
| tra | acesso/qualidade do transporte publico (nacional) | catalogo Ipeadata (4071 series; sha256 0927071bf904, pasta social) (transport) | 64 series; as que medem politica publica sao despesas estaduais/municipais por funcao: DFTRAE, DFTRAM; o resto e producao/venda de veiculos, receitas de servicos e cambio | sem serie comparavel de acesso: DFTRAE (despesa estadual, 1965-2025) e despesa, nao acesso, e a funcao Transporte inclui rodovias/infraestrutura; nao e uma medida do direito a transporte |
| tra | tempo de deslocamento casa-trabalho / mobilidade | listagem de tabelas do SIDRA (deslocamento/transporte/mobilidade/casa-trabalho) | 111 tabelas; ids: 2039, 3643, 4160, 862, 10330, 10331, 10332, 10333, 10335, 10336, 10337, 10338 | tabelas pontuais; sem serie nacional anual de 30 anos com metodo unico |
| pre | % de 65+ com aposentadoria/pensao (PNAD) | listagem de tabelas do SIDRA (aposentad/beneficio previd/pensionista) | 55 tabelas relevantes (ex.: PD 1866/4022: aposentados 10+/15+ 2001-2015; CD 2964/3580: Censo); nenhuma com recorte 65+ e serie 1992-2025 de metodo unico | sem serie comparavel; exigiria microdados PNAD 1981-2015 e PNADC (que nao pergunta igual) - nao coletado |
| pre | saldo da previdencia, % do PIB | catalogo Ipeadata (4071 series; sha256 0927071bf904, pasta social) (previd/aposent) | 10 series: DFASPRE, DFASPRM, MPAS12_ARRBT12, MPAS12_ARRLIQ12, MPAS12_BENPREV12, MPAS12_RESPRGPS12, PNADC12_OCUPCONT12, PNADC12_PEROCUPCONT12, DISOC_QCONTRIBPF, DISOC_VARREC | MPAS12_* (fluxo de caixa mensal) comeca em 2003-02: 22 anos completos (2004-2025). Usado, mas nao qualifica pela regra de cobertura de 30 anos |
| ass | gasto em assistencia social, % do PIB | catalogo Ipeadata (4071 series; sha256 0927071bf904, pasta social) (assistencia/bolsa/BPC/gasto social) | 11 series; com 'assistencia social' como funcao: DFASPRE/DFASPRM (somada com previdencia, so estadual/municipal); nenhuma federal | sem serie comparavel de gasto federal em assistencia; usadas apenas as series de cobertura (BPC 1996+, PBF 2004+) |
| edu | taxas de aprovacao, reprovacao, abandono e distorcao idade-serie (INEP; dependente_de_regra=sim) | download.inep.gov.br (URLs de planilhas testadas: .../portal_ideb/planilhas_para_download/{2019,2021,2023}/divulgacao_brasil_*.xlsx, .../indicadores_educacionais/taxas_de_rendimento_escolar/2023/tx_rend_brasil_regioes_ufs_2023.zip, .../informacoes_estatisticas/indicadores_educacionais/2023/TAXA_RENDIMENTO/...) e paginas gov.br/inep de Ideb/Saeb/Resultados (taxas de rendimento escolar) | 404 em todas as URLs testadas; as paginas de resultados do gov.br/inep carregam o conteudo por JavaScript (o WebFetch devolve 'Aguarde. Carregando conteudo da aba...'); duas buscas na web nao devolveram o link da planilha | nao coletadas; a repetencia ficou so na serie WDI/UIS (1970-2011), marcada dependente_de_regra=sim |
| tbl | rendimento do trabalho: PME (6 regioes metropolitanas) | listagem de tabelas do SIDRA (pesquisa PE) (pme rendimento) | tabela 16 (PME antiga, rendimento NOMINAL, serie encerrada, moedas anteriores ao Real) e 2181-2187 (PME nova 2002-2016, real) | nao coletada: cobre so 6 regioes metropolitanas, nao o Brasil; a serie nacional usada e a PNAD (1996-2015) + PNADC |
| edu | IDEB (INEP) | conhecimento do desenho da fonte + tentativa de achar a planilha no INEP (paginas dinamicas; URLs de download.inep.gov.br testadas deram 404) (ideb) | o Ideb e calculado desde 2005 (primeira edicao) | nao qualifica pela cobertura (2005-2023 = 19 anos); planilha nao localizada; nao coletado |
| edu | PISA (OCDE) | pre-registro e documentos do INEP (pisa) | participacao do Brasil desde a edicao de 2000 | nao qualifica pela cobertura (2000-2022 = 22 anos, 8 pontos); nao coletado |
| mor | deficit habitacional (Fundacao Joao Pinheiro) | WebSearch 2026-10-19 (artigos sobre a metodologia FJP) (deficit habitacional serie historica) | estudos desde 1995 com Censo 1991; desde 2016 a PNADC e a unica fonte e variaveis foram excluidas | sem serie de metodo unico de 30 anos; relatorios FJP nao baixados |

Fora dessas linhas: a lista de 'cultura' do Ipeadata so tem a funcao 'educacao e cultura' somada (DFEDUCE/DFEDUCM) e so estadual/municipal; a funcao Cultura separada nasce na Portaria MOG 42/1999 (funcoes 13 Cultura e 27 Desporto e Lazer, `bruto/doc/portaria_mog_42_1999.odt`); DFDELE (desporto e lazer, estadual) comeca em 2002. Parei ai: nao forcei uma serie.

## 6. Limiares de elegibilidade em valor real (R$ de dez/2025, IPCA)

| Vigencia | Instrumento | Pobreza nominal | Extrema pobreza nominal | Pobreza real | Extrema real |
| --- | --- | --- | --- | --- | --- |
| 2004-09-17 | Decreto 5.209/2004, art. 18 | 100 | 50 | 315 | 157 |
| 2006-04-11 | Decreto 5.749/2006 | 120 | 60 | 345 | 172 |
| 2009-04-16 | Decreto 6.824/2009 | 137 | 69 | 345 | 174 |
| 2009-09-01 | Decreto 6.917/2009 (efeitos financeiros desde 1/9/2009) | 140 | 70 | 347 | 174 |
| 2014-04-30 | Decreto 8.232/2014 | 154 | 77 | 291 | 145 |
| 2016-06-29 | Decreto 8.794/2016 | 170 | 85 | 268 | 134 |
| 2018-05-30 | Decreto 9.396/2018 | 178 | 89 | 265 | 132 |
| 2021-11-08 | Decreto 10.852/2021 (Auxilio Brasil substitui o Bolsa Familia) | 200 | 100 | 244 | 122 |
| 2022-03-29 | Decreto 11.013/2022 | 210 | 105 | 246 | 123 |
| 2023-06-16 | Decreto 11.566/2023 e Lei 14.601/2023 (linha unica) | 218 | - | 242 | - |

BPC: idade minima do idoso 70 anos (texto original, 1996), 67 desde 1/1/1998 (Lei 9.720/1998, art. 38), 65 desde o Estatuto do Idoso (Lei 10.741/2003, art. 34, vigencia 2004). Renda familiar per capita: 1/4 do salario minimo no texto original (art. 20, par. 3); Lei 13.981/2020 traz 1/2; Lei 14.176/2021 volta a 1/4 com possibilidade de ampliar ate 1/2 por regulamento; o texto compilado remete a ADPF 662 (aplicacao efetiva nao verificada). Valores reais anuais em `series/ass.csv` (`ass_bpc_limiar_quarto_sm_real`, `ass_bpc_limiar_meio_sm_real`).

## 7. Quebras (resumo; texto completo em `quebras.csv`)

| # | Indicador | Quebra | Tipo | Direcao | Efeito medido |
| --- | --- | --- | --- | --- | --- |
| 1 | edu_analfab15 | 1991 (mesmo Censo, duas vintages) | revisao_de_vintage | eleva | +0,67 p.p. em 1991 (20.07 contra 19.40) |
| 2 | edu_analfab15 | 2022 (Censo x pesquisa domiciliar amostral no mesmo ano) | metodo_estatistico | reduz | -1,40 p.p. em 2022 (PNADC 5.6 contra Censo 7.00); Censo 2010 9.61 contra PNAD 2009 9.8 e PNAD 2011 8.6 (anos diferentes, so indicativo) |
| 3 | edu_analfab15 | 2016 (PNAD encerrada em 2015; PNADC anual desde 2016) | metodo_estatistico | desconhecida | sem sobreposicao |
| 4 | edu_analfab15 (e tbl_renda_trabalho_real, mor_agua_rede_geral, mor_esgoto_adequado) | 2020-03 a 2021-06 | metodo_estatistico | desconhecida | sem sobreposicao |
| 5 | edu_repetentes_primario_pct | 1996-12-20 | mudanca_de_regra | reduz | sem sobreposicao (nao ha serie com e sem a regra); valores publicados: 1992=18.1, 1993=18.4, 1994=19.1, 1999=24.0, 2000=25.0, 2001=21.5, 2002=20.6, 20 |
| 6 | edu_repetentes_primario_pct | 1998 (Sao Paulo) | mudanca_de_regra | reduz | sem sobreposicao |
| 7 | edu_saeb_* (5o ano e 9o ano) | 2006-02-06 (Lei 11.274); implantacao ate 2010 | mudanca_de_regra | desconhecida | sem sobreposicao |
| 8 | edu_saeb_* (todas as etapas) | 2005 (Portaria MEC 931/2005; Prova Brasil) | metodo_estatistico | desconhecida | sem sobreposicao |
| 9 | edu_saeb_* (todas as etapas) | 2011-2019 (mesmas edicoes em duas vintages) | revisao_de_vintage | ambigua | 0 em 30 de 30 pontos (valores arredondados identicos) |
| 10 | edu_gasto_publico_pib | 1998-01-01 | mudanca_de_regra | desconhecida | sem sobreposicao |
| 11 | edu_gasto_publico_pib | 2007-01-01 | mudanca_de_regra | desconhecida | sem sobreposicao |
| 12 | edu_gasto_publico_pib | 2009-11-11 | mudanca_de_regra | desconhecida | sem sobreposicao |
| 13 | edu_gasto_publico_pib | 2020-08-26 | mudanca_de_regra | desconhecida | sem sobreposicao |
| 14 | mor_agua_rede_geral | 2022 (mesmo Censo, duas definicoes de 'rede geral') | metodo_estatistico | eleva | +7,10 p.p. (90.98% com ligacao contra 83.88% com rede como principal forma) |
| 15 | mor_agua_rede_geral | 2022 (Censo contra PNADC no mesmo ano) | metodo_estatistico | eleva | +1,62 p.p. (PNADC 85.5 contra Censo 83.88) |
| 16 | mor_esgoto_adequado | 1991 contra 2000-2022 | metodo_estatistico | eleva | +2,71 p.p. em 1991 (49.78% so exclusivas contra 52.49% incluindo as compartilhadas com rede ou fossa septica) |
| 17 | mor_esgoto_adequado | 1991 (costura de fontes: Atlas 1998 ate 1991, SIDRA desde 2000) | revisao_de_vintage | eleva | +9,07 p.p. em 1991 (PDIAE 58.85 contra 49.78); em 2000/2010/2022 a diferenca e +0.00/+0.00/+0.01 |
| 18 | mor_esgoto_adequado | 2022 (Censo contra PNADC no mesmo ano) | metodo_estatistico | eleva | +8,00 p.p. no mesmo universo (PNADC 85.8 contra Censo 77.80); +8,39 p.p. contra o Censo no universo de todos os domicilios |
| 19 | mor_esgoto_rede_ou_fossa_ligada | 2019 | metodo_estatistico | desconhecida | sem sobreposicao |
| 20 | mor_agua_rede_geral / mor_esgoto_adequado (series PNAD) | 2003 -> 2004 | metodo_estatistico | desconhecida | sem sobreposicao |
| 21 | tbl_informalidade | 2014 -> 2016 | metodo_estatistico | desconhecida | sem sobreposicao |
| 22 | tbl_informalidade | 2017-11-11 (Lei 13.467/2017, vigencia apos 120 dias) | mudanca_de_regra | desconhecida | sem sobreposicao |
| 23 | tbl_renda_trabalho_real | 2012-2015 (sobreposicao) e 2016 | metodo_estatistico | eleva | +8.5% em media (PNADC acima da PNAD, 10+): 2012: +7.8% (10+) / +7.0% (15+), 2013: +6.9% (10+) / +6.1% (15+), 2014: +10.0% (10+) / +9.1% (15+), 2015: + |
| 24 | pre_rgps_* | 2007-03-16 (Lei 11.457/2007) | mudanca_de_regra | desconhecida | sem sobreposicao |
| 25 | pre_rgps_arrecadacao_liquida_pib | 2015 | metodo_estatistico | desconhecida | sem sobreposicao |
| 26 | pre_rgps_* | 2019-11-13 (EC 103/2019) | mudanca_de_regra | desconhecida | sem sobreposicao |
| 27 | ass_bpc_por_mil_hab / ass_bpc_idade_minima | 1998-01-01 (70 -> 67 anos) | mudanca_de_regra | eleva | sem sobreposicao (benefícios de idosos em dezembro: 1997=88806, 1998=207031, 2003=664875, 2004=933164, valores brutos, nao atribuiveis a regra isolada |
| 28 | ass_bpc_por_mil_hab / ass_bpc_limiar_* | 2020-03-23 (Lei 13.981/2020) e 2021-06-22 (Lei 14.176/2021) | mudanca_de_regra | eleva | sem sobreposicao |
| 29 | ass_bpc_por_mil_hab | 2016 (vintage) | revisao_de_vintage | reduz | sem sobreposicao; valor mantido como publicado (74) e ano excluido das janelas |
| 30 | ass_pbf_familias_por_mil_hab | 2021-11-08 (Auxilio Brasil) e 2023-06-16 (volta do Bolsa Familia) | mudanca_de_regra | eleva | sem sobreposicao |
| 31 | ass_pbf_limiar_pobreza_real / ass_pbf_limiar_extrema_pobreza_real | 2023-06-16 | mudanca_de_regra | ambigua | sem sobreposicao; linha de pobreza em R$ de dez/2025 (vigente em 31/dez): 2004=309, 2009=343, 2014=281, 2018=258, 2022=240, 2023=238, 2025=218 |
| 32 | mat_prenatal7 | 1995-1999 (categorias) e 2000 | metodo_estatistico | desconhecida | sem sobreposicao; observado: 7+ entre os informados: 50.7% (1999, ignorado 8.5%) contra 46.0% (2000, ignorado 4.9%) |
| 33 | mat_prenatal7 | 2011 | metodo_estatistico | desconhecida | sem sobreposicao |
| 34 | mat_prenatal7 | 1994-2000 (implantacao gradual) | metodo_estatistico | desconhecida | sem sobreposicao; observado: ignorado 54.5% (1995), 12.9% (1998), 2.7% (2002) |

## 8. Decisoes fixas e anomalias (para o leitor poder refazer)

- **BPC_defi 2016 = 74** no Ipeadata (2015 = 2.323.808; 2017 = 2.527.257). Mantido na serie como publicado, marcado `ANOMALIA`, fora das janelas. Nao corrigi.
- **SINASC:** 1994 tem 100% de 'ignorado' (fora). Anos com mais de 10% de nascimentos com numero de consultas ignorado (1995 a 1998) ficam na serie e fora das janelas; 2025 e preliminar e tambem fica fora. Limite de 10% fixado antes de ver o efeito nas medias.
- **Saeb:** os valores sao rotulos de grafico, arredondados a inteiro; o proprio INEP informa o erro amostral da media nacional de 2023 na 3a serie do ensino medio: 1,0 ponto em Lingua Portuguesa e 1,3 em Matematica (Relatorio Saeb 2023 vol. 1). Diferencas de 1-2 pontos entre edicoes nao sao distinguiveis de ruido de amostra.
- **PNADC:** os indicadores anuais de educacao, agua e esgoto nao existem para 2020 e 2021 nas tabelas baixadas (coleta por telefone).
- **PDIAE (Ipea):** os pontos de 2000, 2010 e 2022 batem com o meu recalculo a partir do SIDRA (diferenca <= 0,01 p.p.); o ponto de 1991 (Atlas 1998) nao bate (quebra 17). Por isso a serie primaria de esgoto e o recalculo do SIDRA e o PDIAE entra como extensao 1970-1991.
- **Censos 1970/1980 de agua e luz** nao foram achados em tabela nacional comparavel (so contagens de domicilios 1940-1960 no Ipeadata, baixadas e nao usadas por cairem antes de 1964).
- **Anos de estudo:** so ha Censos 1991 e 2000 (Ipea/PNUD, 25+) e PNADC 2016+ (15+): sem serie de 30 anos. Conclusao por idade (por exemplo, 19 anos com ensino medio) nao foi coletada: nao localizei tabela agregada nacional com metodo unico.

## 9. Becos (evidencia negativa, para ninguem repetir)

- `seriesestatisticas.ibge.gov.br` devolve a tela de verificacao do Cloudflare (403); `agenciadenoticias.ibge.gov.br` barra a leitura direta e as URLs de noticia testadas deram 404 (pagina do Censo 2022 sobre analfabetismo nao lida).
- `download.inep.gov.br`: o `urllib` do manifest_tool falha na verificacao do certificado; resolvido com `curl` + `add-local` (nota na linha do manifest). Planilhas do Ideb e das taxas de rendimento: 404 em todas as URLs tentadas; paginas gov.br/inep carregam o conteudo por JavaScript.
- `.odt` do gov.br so baixa com `/@@download/file` no fim da URL; a URL sem isso devolve HTML.
- SIDRA devolve gzip sem ser pedido (o bruto guardado e o gzip exato); o filtro `$filter` do Ipeadata e ignorado (o arquivo vem inteiro, com todos os niveis territoriais; filtro de nivel Brasil e feito no codigo).
- TabNet/DATASUS so por POST (fora do `add`); `old.scielo.br` falha no certificado, `www.scielo.br` serve o mesmo PDF.
- Nao localizados: texto oficial da Deliberacao CEE 9/97 e da Resolucao SE 4/98 (SP); documento 'Consolidacao do SINASC 2011'; relatorios da FJP; microdados PNAD 1981-1999 (rendimento nacional so 1996-2006, tabela 427, sem 2000).
- O catalogo Ipeadata local nao lista a PNAD antiga de rendimento (ela esta no SIDRA); busca so por palavra no catalogo perdeu essa serie na primeira passada.

## 10. Inventario do que foi entregue

| Arquivo | Conteudo |
| --- | --- |
| `series/edu.csv, mor.csv, tbl.csv, pre.csv, ass.csv, mat.csv` | formato longo: indicador, fonte, definicao_linha, ano, valor, unidade, nota, vintage, dependente_de_regra |
| `series/limiares_eventos.csv` | cada decreto/lei dos limiares do PBF com valor nominal e real |
| `janelas.csv` | indicador, governo, inicio, fim, media, valor_inicial, valor_final, n_anos, segmento_metodo |
| `quebras.csv` | uma linha por quebra, com tipo_de_quebra, trecho citado e fonte primaria |
| `busca-sem-serie.csv` | evidencia da busca onde nao ha serie comparavel |
| `manifest.jsonl, bruto/, recalcula.py, resultado.py, scripts/, baixar-lote*.sh` | cadeia de hash, brutos, codigo e roteiros de download |
