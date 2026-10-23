# Dominios-2: saude, seguranca, alimentacao, ambiente e democracia

Dossie governos-do-brasil-economia. Coleta em 2026-10-19. Sem opiniao politica: so bruto, vintage e quebra.
Reproduzir (sem rede, confere sha256 do bruto contra o manifest de cada subpasta):
`python3 -I /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-2/scripts/construir.py` e depois `.../scripts/montar_resultado.py`.
Aquisicao (COM rede, nao rode por acaso): `scripts/coletar_tabnet.py` e `scripts/tabnet_lib.py`.

## 0. Achado e nao achado

1. Seis series entram como primarias (mortalidade materna, DTP3, taxa de homicidios, subalimentacao, desmatamento PRODES, democracia V-Dem). Duas NAO atingem 30 anos e ficam marcadas: subalimentacao FAO (2001-2024, 24 anos) e gasto publico em saude (2000-2023, 24 anos). Pela regra 4 do pre-registro, sao "sem serie comparavel de 30 anos": os numeros existem em `series/`, mas nao sustentam leitura de longo prazo.
2. Homicidios cruza uma quebra de classificacao no meio de um mandato: o mandato FHC (1995-2002) tem 1995 em CID-9 e 1996-2002 em CID-10. A tabela de janelas traz a linha cheia e uma linha por metodo (`seg_homic_taxa|SIM-CID10`, `|SIM-CID9`).
3. Nao ha ano duplamente codificado CID-9/CID-10 nos brutos: o efeito da troca de 1996 e `sem sobreposicao` (a propria nota do DATASUS diz que nao ha lista que compatibilize as duas). Nao estimei efeito.
4. Sobreposicoes reais encontradas e medidas: (a) WUENIC revisao 2025 x WDI: 2023 = 86 x 90, 2024 = 90 x 91, demais 43 anos iguais; (b) subalimentacao SOFI 2015 x FAOSTAT 2026: 2000-02 = 11,2 x 10,5; (c) PRODES 2024 estimativa x consolidado: 6.288 x 6.518 (+3,66%); (d) populacao Censo x Projecao rev. 2024: de -0,4% a +3,8% no denominador; (e) homicidios Ipeadata x TabNet: igual de 1996 a 2024 (exceto 2022: -1), diferenca de -61 a +120 obitos/ano em 1979-95.
5. Nao encontrei, nem tentei estimar: serie de cobertura do SIM; gasto publico em saude antes de 2000; PRODES antes de 1988 (Castelo a Figueiredo ficam sem dado); V-Dem v15 e Atlas da Violencia como arquivos proprios (so o Ipeadata, que reproduz o SIM).

## 1. Regra de atribuicao ano -> governo (unica, mecanica)

Cada observacao anual e atribuida ao governo que ocupa MAIS DIAS dentro do intervalo da observacao (ano-calendario; para o PRODES, 1 ago do ano anterior a 31 jul). Consequencias: a Junta Militar (2 meses) nunca fica com ano (n=0); anos de transicao (1990, 1992, 1995, 2003, 2011, 2016...) vao ao governo majoritario. Para o PRODES existe tambem a atribuicao alternativa pelo ano-calendario de inicio (ago-dez): linhas `amb_prodes_amz|atribuicao-alternativa:ano-calendario-de-inicio` em `janelas.csv`. Medias sao simples (sem ponderar). Termino do Lula 3 = 2026-10-19 (mandatos.csv).

## 2. Cadeia de hash (resultado de `manifest_tool.py verify`)

| pasta | resultado | observacao |
|---|---|---|
| dominios-2/ (raiz) | REPROVADO | seq 1 e o JSON do Ipeadata (AVIOL12_HOMIC) de 64.653.700 bytes, baixado por engano sem filtro (o filtro OData `$filter=NIVNOME` foi ignorado pelo servidor); excede o teto de 25 MB, entao foi APAGADO. A linha (sha256 cd8db235c218c0b79b6435cb22e8f32e723b0f3fb5b3d7dc70354ee1c8cda017) fica na cadeia. Sobrevive so o derivado `Brasil` (46 linhas, 6.440 bytes), registrado na raiz (seq 2) e copiado em seguranca/. Recriar o bruto: URL na linha seq 1. |
| saude/ | OK | |
| alimentacao/ | REPROVADO | seq 5 e um download TRUNCADO do SOFI 2015 (597.999 bytes, timeout); o arquivo foi baixado de novo (seq 6, 2.506.724 bytes) sob o mesmo nome e a ferramenta compara cada linha ao arquivo atual. A linha superada nao pode passar: comportamento da ferramenta, nao editei o manifest. |
| seguranca/ | OK | inclui 2 brutos de qualidade ruim mantidos por rastreabilidade: `portaria_svs_116_2009.pdf` e um HTML de erro do MPBA (a copia correta e `portaria_svs_116_2009_es.pdf`) |
| seguranca_unodc/, democracia/ | OK | |
| ambiente/ | OK | 2 arquivos `inpe_nt_prodes_2021/2022_consolidada.pdf` sao HTML (gov.br nao serviu o PDF); mantidos por rastreabilidade, nao usados |

Brutos grandes NAO baixados: V-Dem zip v16 https://v-dem.net/media/datasets/V-Dem-CY-FullOthers-v16_csv.zip (26.867.425 bytes) e v15 https://v-dem.net/media/datasets/V-Dem-CY-FullOthers-v15_csv.zip (25.953.685 bytes): acima de 25 MB; usei a redistribuicao OWID (CC BY 4.0, v16, DOI 10.23696/vdemds26; o arquivo traz todos os paises). Ipeadata AVIOL12_HOMIC completo (64,65 MB): so o derivado Brasil. Ipeadata AVIOL12_THOMIC (taxa do Ipea) NAO baixado (mesmo problema de tamanho; o comentario do metadado dessa serie descreve codigos de suicidio e esta corrompido): a taxa foi calculada aqui. FAOSTAT zip: 2,2 MB baixado; o CSV de 52 MB extraido foi apagado depois de gerar o derivado Brasil.

## 3. Saude

Fontes: mortalidade materna = estimativa MODELADA (OMS/UNICEF/UNFPA/Banco Mundial/ONU), via WDI 2026-10-08; DTP3 = WUENIC revisao 2025 (export oficial da OMS, 2026-10-19); gasto publico = OMS GHED via WDI. Mortalidade infantil ja existe em `social/series/mortinf.csv` (nao refeita).

| governo | mort. materna modelada (por 100 mil nv) | DTP3 WUENIC 2025 (%) | gasto publico saude (% PIB) |
|---|---|---|---|
| castelo | sem dado | sem dado | sem dado |
| costa_silva | sem dado | sem dado | sem dado |
| junta | sem dado | sem dado | sem dado |
| medici | sem dado | sem dado | sem dado |
| geisel | sem dado | sem dado | sem dado |
| figueiredo | sem dado | 53.6 (n=5) | sem dado |
| sarney | 168 (n=5) | 59.2 (n=5) | sem dado |
| collor | 128.6667 (n=3) | 71.6667 (n=3) | sem dado |
| itamar | 110.5 (n=2) | 74.5 (n=2) | sem dado |
| fhc | 81.625 (n=8) | 89.875 (n=8) | 3.5565 (n=3) |
| lula12 | 69.875 (n=8) | 99 (n=8) | 3.5171 (n=8) |
| dilma | 62.1667 (n=6) | 94.8333 (n=6) | 3.6454 (n=6) |
| temer | 61.5 (n=2) | 85 (n=2) | 3.9212 (n=2) |
| bolsonaro | 95.5 (n=4) | 73 (n=4) | 4.1638 (n=4) |
| lula3 | 67 (n=1) | 87.3333 (n=3) | 4.2939 (n=1) |

Leitura do que existe: mortalidade materna modelada comeca em 1985 e DTP3 em 1980; antes disso, sem dado. Gasto publico: so 2000-2023 (FHC n=3, Lula 3 n=1). `sau_mortmat_nacional` (1995-2022) esta em `series/sau.csv` como sensibilidade; em 2022 a estimativa nacional (57,7) e a modelada (104) divergem (razao 0,55); em 1999 a razao e 1,23 e em 2000, 1,06. Esses saltos nao tem explicacao declarada nos arquivos baixados e nao sao tratados como quebra.
DTP3: a cobertura administrativa menos a WUENIC tem media absoluta de 1,4 pp (1980-94), 1,6 pp (1995-2011) e 0,1 pp (2012-2025).

## 4. Seguranca (homicidios)

Definicao primaria: homicidios (Ipeadata AVIOL12_HOMIC, obitos por residencia, MS/SIM): CID-9 E960-E978 e E990-E999 (1979-95); CID-10 X85-Y09 e Y35 (1996-). Taxa = contagem / populacao projetada IBGE rev. 2024 (1o jul), um unico vintage de denominador 1980-2024 (1979 so tem contagem). Dado final do SIM ate 2024 (extracao DATASUS 02/12/2025). Sensibilidades: UNODC via WDI (1990-2023; diferenca media de -0,83 por 100 mil, em modulo 0,84), homicidios + intencao indeterminada.

| governo | taxa por 100 mil (primaria) | homic. + intencao indeterminada | UNODC/WDI |
|---|---|---|---|
| castelo | sem dado | sem dado | sem dado |
| costa_silva | sem dado | sem dado | sem dado |
| junta | sem dado | sem dado | sem dado |
| medici | sem dado | sem dado | sem dado |
| geisel | sem dado | sem dado | sem dado |
| figueiredo | 13.1003 (n=5) | 23.2021 (n=5) | sem dado |
| sarney | 16.591 (n=5) | 27.0297 (n=5) | sem dado |
| collor | 20.4359 (n=3) | 27.6156 (n=3) | 18.3434 (n=3) |
| itamar | 20.3717 (n=2) | 28.9444 (n=2) | 18.3045 (n=2) |
| fhc | 25.4871 (n=8) | 32.0765 (n=8) | 24.9923 (n=8) |
| lula12 | 26.7015 (n=8) | 32.6436 (n=8) | 26.5386 (n=8) |
| dilma | 29.0929 (n=6) | 34.0723 (n=6) | 28.8087 (n=6) |
| temer | 30.0149 (n=2) | 35.3827 (n=2) | 29.1609 (n=2) |
| bolsonaro | 22.6275 (n=4) | 29.7961 (n=4) | 20.9109 (n=4) |
| lula3 | 20.8222 (n=2) | 28.1514 (n=2) | 19.2753 (n=1) |

Comparacao dentro de um unico metodo para o mandato que cruza a quebra:

| segmento | media (n) | inicial | final |
|---|---|---|---|
| FHC, linha cheia (CRUZA CID-9/CID-10) | 25.4871 (n=8) | 23.3844 (1995) | 27.7947 (2002) |
| FHC so CID-10 (1996-2002) | 25.7875 (n=7) | 24.1311 (1996) | 27.7947 (2002) |
| FHC so CID-9 (1995) | 23.3844 (n=1) | 23.3844 (1995) | 23.3844 (1995) |

### 4.1 O que mudou no SIM (cada item em `quebras.csv`, com data, trecho e URL)

| item | data | fonte primaria | efeito medido |
|---|---|---|---|
| CID-9 -> CID-10 | 1996-01-01 | nota DATASUS Mortalidade_Geral_1996_2012.pdf | sem sobreposicao (nenhum ano em duas revisoes). Contagens vizinhas, so descritivas: 1994 32631, 1995 37152, 1996 38929, 1997 40531 |
| causa de intencao indeterminada (E980-E989 -> Y10-Y34) | 1996 | tabelas TabNet | sem sobreposicao |
| intervencao legal dentro de "homicidios" (rotulo do Ipeadata) | 1996 | metadado Ipeadata | sem sobreposicao; intervencoes legais no CID-10: 35 (1996), 121 (2002), 491 (2003), 2.644 (2024) |
| causa mal definida (cap. XVI -> XVIII) | 1996 | nota DATASUS | sem sobreposicao; proporcao de mal definidas: 1979 20.1%, 1995 16.2%, 1996 15.1%, 2010 7.0%, 2024 4.5% |
| fluxo/periodicidade de envio (cobertura) | 2009-02-11 | Portaria SVS 116/2009 | sem sobreposicao; serie de cobertura do SIM nao baixada |
| formulario da DO | 2011 | nota DATASUS | sem sobreposicao |
| CID-10 v2019 no SIM | 2025-01 | nota DATASUS | fora da serie (final ate 2024) |
| denominador (Censo x projecao) | 2022 | Ipeadata POPTOT x POP_PROJE | ver quebras.csv (taxa com projecao x taxa com Censo: -0,4% em 1980, +1,5% em 1991, +2,8% em 2000, +2,1% em 2010, +3,8% em 2022 no denominador) |

### 4.2 Descontinuidades vistas nos dados SEM quebra declarada pela fonte (nao entram em quebras.csv: a tabela exige quebra declarada ou de vintage)

- 1989 -> 1990 (CID-9): homicidios 28757 -> 31989 (+3232); "lesoes em que se ignora acidente ou intencao" 13716 -> 8966 (-4750); soma 42473 -> 40955. Os brutos nao separam reclassificacao de mudanca real.
- 2018 -> 2019 (CID-10): agressoes 55914 -> 44033 (-11881); intencao indeterminada 12310 -> 16648 (+4338); soma 68224 -> 60681. Mesma limitacao.
- 2002 -> 2003: intervencoes legais 121 -> 491 (+306%).

## 5. Alimentacao

FAO, prevalencia de subalimentacao, media trienal atribuida ao ano central (2000-02 -> 2001). Vintage FAOSTAT 2026-07-10. Valores publicados como "<2,5" (9 de 24 medias trienais) entram como 2,5 (teto): as medias de Dilma e Temer sao, portanto, limite superior. SOFI 2015 (1990-92: 14,8; 2000-02: 11,2; demais "<5,0") fica como outra vintage em `series/ali.csv`.

| governo | subalimentacao % (FAOSTAT 2026) | SOFI 2015 (teto 5,0 nos censurados) |
|---|---|---|
| castelo | sem dado | sem dado |
| costa_silva | sem dado | sem dado |
| junta | sem dado | sem dado |
| medici | sem dado | sem dado |
| geisel | sem dado | sem dado |
| figueiredo | sem dado | sem dado |
| sarney | sem dado | sem dado |
| collor | sem dado | 14.8 (n=1) |
| itamar | sem dado | sem dado |
| fhc | 9.8 (n=2) | 11.2 (n=1) |
| lula12 | 4.9625 (n=8) | 5 (n=1) |
| dilma | 2.5333 (n=6) | 5 (n=2) |
| temer | 2.5 (n=2) | sem dado |
| bolsonaro | 3.05 (n=4) | sem dado |
| lula3 | 2.6 (n=2) | sem dado |

Governos ate 1999: sem dado na vintage atual (a unica cifra anterior, 14,8% em 1990-92, e do SOFI 2015).

## 6. Ambiente (desmatamento da Amazonia Legal, PRODES)

Taxa consolidada, soma dos 9 estados, 1988-2025 (testes: 1988 = 21.050; 2022 = 11.594; 2024 = 6.518; 2025 = 5.731). A estimativa de 2026 (3.335 km2, 271 de 516 tiles, nota de 2026-10-16) e linha a parte e nao entra na media. 1993 e 1994 tem valor identico (14.896). Quebras de metodo do PRODES (analogico, digital, TerraAmazon, ajuste de mascara 2015, poligonos 2008-12 em 2017) estao em `quebras.csv` sem efeito mensurado.

| governo | PRODES km2/ano (atribuicao: maioria dos dias do ano ago-jul) | atribuicao alternativa (ano-calendario de inicio) |
|---|---|---|
| castelo | sem dado | sem dado |
| costa_silva | sem dado | sem dado |
| junta | sem dado | sem dado |
| medici | sem dado | sem dado |
| geisel | sem dado | sem dado |
| figueiredo | sem dado | sem dado |
| sarney | 17516.6667 (n=3) | 17516.6667 (n=3) |
| collor | 12408 (n=2) | 13237.3333 (n=3) |
| itamar | 14896 (n=2) | 21977.5 (n=2) |
| fhc | 19141.25 (n=8) | 18683.375 (n=8) |
| lula12 | 15686.75 (n=8) | 13314.5 (n=8) |
| dilma | 5998.6667 (n=6) | 6086.8333 (n=6) |
| temer | 7241.5 (n=2) | 8832.5 (n=2) |
| bolsonaro | 11403 (n=4) | 11136.75 (n=4) |
| lula3 | 7104.3333 (n=3) | 6124.5 (n=2) |

Lula 3 inclui a estimativa de 2026 como linha separada: 3.335 km2 (n=1, vintage "PRODES 2026 estimativa"); a estimativa de 2024 (6.288) e a consolidada (6.518) estao guardadas como duas vintages do mesmo ano.

## 7. Democracia

V-Dem v2x_polyarchy (v16, via OWID). Sensibilidades: Polity5 polity2 (ate 2018) e Freedom House (direitos politicos e liberdades civis, escala 1 = melhor; 1981-89 usam periodos nao-calendario e ficaram fora; edicao 2024; licenca nao verificada, so notas de Brasil).

| governo | V-Dem polyarchy 0-1 | Polity5 polity2 (-10..10) | FH direitos politicos (1 melhor) |
|---|---|---|---|
| castelo | 0.166 (n=3) | -7 (n=3) | sem dado |
| costa_silva | 0.179 (n=3) | -9 (n=3) | sem dado |
| junta | sem dado | sem dado | sem dado |
| medici | 0.175 (n=4) | -9 (n=4) | 5 (n=2) |
| geisel | 0.184 (n=5) | -4 (n=5) | 4 (n=5) |
| figueiredo | 0.2575 (n=6) | -3.5 (n=6) | 4 (n=2) |
| sarney | 0.5656 (n=5) | 7.4 (n=5) | sem dado |
| collor | 0.826 (n=3) | 8 (n=3) | 2 (n=3) |
| itamar | 0.843 (n=2) | 8 (n=2) | 2.5 (n=2) |
| fhc | 0.8508 (n=8) | 8 (n=8) | 2.625 (n=8) |
| lula12 | 0.8642 (n=8) | 8 (n=8) | 2 (n=8) |
| dilma | 0.8557 (n=6) | 8 (n=6) | 2 (n=6) |
| temer | 0.7615 (n=2) | 8 (n=2) | 2 (n=2) |
| bolsonaro | 0.6947 (n=4) | sem dado | 2 (n=4) |
| lula3 | 0.791 (n=3) | sem dado | 2 (n=1) |

## 8. Quebras (resumo; `quebras.csv` tem trecho citado, URL e como a direcao foi determinada)

| indicador | data | tipo | direcao | efeito medido |
|---|---|---|---|---|
| seg_homic_taxa | 1996-01-01 | mudanca_de_regra | desconhecida | sem sobreposicao |
| seg_indet_pct | 1996-01-01 | mudanca_de_regra | desconhecida | sem sobreposicao |
| seg_homic_taxa | 1996-01-01 | mudanca_de_regra | ambigua | sem sobreposicao |
| seg_maldef_pct | 1996-01-01 | mudanca_de_regra | desconhecida | sem sobreposicao |
| seg_homic_taxa | 2009-02-11 | mudanca_de_regra | desconhecida | sem sobreposicao |
| seg_homic_taxa | 2011-01-01 | mudanca_de_regra | desconhecida | sem sobreposicao |
| seg_homic_taxa | 2025-01-01 | mudanca_de_regra | desconhecida | sem sobreposicao |
| seg_homic_taxa | 2022-08-01 | revisao_de_vintage | reduz | taxa(projecao)/taxa(censo)-1: 1980 +0,4%; 1991 -1,5%; 2000 -2,8%; 2010 -2,1%; 2022 -3,7% |
| sau_dtp3 | 2025 (revisao de julho de 2026) | revisao_de_vintage | reduz | dif. rev.2025 menos WDI: 2023: -4 pp; 2024: -1 pp; nos outros 43 dos 45 anos comuns a diferenca e zero |
| sau_mortmat_nacional | 2008-06-05 | mudanca_de_regra | ambigua | sem sobreposicao |
| ali_pou | 2015 -> 2026 (SOFI 2015 vs FAOSTAT 2026-07-10) | revisao_de_vintage | ambigua | 2000-02: 10.5 - 11.2 = -0.7 pp; 2005-07: 5,1 vs '<5,0' (novo acima do teto antigo); 2010-12: 2,7 vs '<5,0' (compativel) |
| ali_pou | 2012 (media 2011-13) a 2020 e 2024 (media 2023-25) | metodo_estatistico | eleva | sem sobreposicao |
| amb_prodes_amz | 1988 a 2000 | metodo_estatistico | desconhecida | sem sobreposicao |
| amb_prodes_amz | 2000 a 2005 | metodo_estatistico | desconhecida | sem sobreposicao |
| amb_prodes_amz | apos 2005 | metodo_estatistico | desconhecida | sem sobreposicao |
| amb_prodes_amz | 2015 | metodo_estatistico | desconhecida | sem sobreposicao |
| amb_prodes_amz | 2017 | revisao_de_vintage | desconhecida | sem sobreposicao |
| amb_prodes_amz | 1993-1994 | metodo_estatistico | desconhecida | sem sobreposicao |
| amb_prodes_amz | anual (2024 medido) | revisao_de_vintage | eleva | 2024: 6288 -> 6518 km2 (+3,66%); 2026 e apenas estimativa (3.335 km2, 271 tiles) e fica fora da media consolidada |
| amb_prodes_amz | ate 2024 (data exata nao verificada) | metodo_estatistico | desconhecida | sem sobreposicao |
| dem_polyarchy | v15 (mar/2025) -> v16 (2026-03-17) | revisao_de_vintage | desconhecida | sem sobreposicao |
| dem_fh_direitos_politicos | 1981-1989 | metodo_estatistico | desconhecida | sem sobreposicao |

Tipos: `mudanca_de_regra` = a norma/classificacao alterou o que se mede; `metodo_estatistico` = mudanca de metodo de medir/estimar; `revisao_de_vintage` = a mesma coisa medida de novo e publicada com outro valor. A direcao so e "eleva"/"reduz" quando segue de aritmetica sobre dados baixados; nas demais e "desconhecida" ou "ambigua".

## 9. Limites desta entrega

- Nao medi cobertura do SIM, nem subnotificacao de homicidios; so proxies descritivos (mal definidas, intencao indeterminada).
- `janelas.csv` usa mandatos (mandatos.csv); as janelas impressas no infografico nao foram tratadas aqui.
- Nao ha dado de saude/seguranca/alimentacao/ambiente para Castelo, Costa e Silva, Junta, Medici e Geisel (Figueiredo so tem homicidios e DTP3; mortalidade materna comeca no Sarney; PRODES comeca no Sarney). Democracia (V-Dem, Polity) cobre todos exceto a Junta.
- Atlas da Violencia e Freedom House/Polity: licenca/uso nao auditados; nada foi reproduzido alem de series de Brasil.
