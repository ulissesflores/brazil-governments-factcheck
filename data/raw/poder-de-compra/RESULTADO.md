# RESULTADO: poder de compra, excesso monetario e trabalho

Colheita de 2026-10-19. Sem opiniao, sem nota, sem ranking: so numeros, fonte e limite. Tudo sai de `python3 -I scripts/construir.py`, `scripts/quebras_gerar.py`, `scripts/bolsa_familia.py`, `scripts/pnad_microdados.py`, `scripts/escrever_md_*.py` e `scripts/escrever_resultado.py`, que leem so arquivos locais. Os brutos baixados nesta pasta entram na cadeia de hash (`manifest.jsonl`; `python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py verify .` -> 93 lines; head da290c7f12812457498bd006cf44460c7932a8f13983f8e42107b49a6be136a2; OK). Pre-registro: `../preregistro/PREREGISTRATION-EMENDA-01.md`, secao B, linhas "Purchasing power" e "Labour".

Legenda: ACHADO = tem numero e fonte aqui; NAO ACHADO = procurei e nao obtive (com onde procurei).

## 1. Resumo

1. **ACHADO.** Cesta basica DIEESE de Sao Paulo mensal 1959-2026 (Ipeadata, ja hasheada em `../quebras/bruto/`): quantas cestas 1 salario minimo compra caiu de 3,76 (1959) para 0,95 (1994, minimo) e foi a 2,16 (2017, maximo desde 1995) e 1,76 (2025). Em horas de trabalho (220 h/mes, formula do DIEESE), de 59 h (1959) a 231 h (1994) e 125 h (2025). 1964 fica de fora: a fonte so tem janeiro e fevereiro.
2. **ACHADO com ressalva.** O salario minimo real depende muito do deflator antes de 1995: em 1980, R$ 947 (INPC), R$ 1.006 (IPCA), R$ 2.124 (IGP-DI) e R$ 482 (IPC-Fipe), todos em R$ de set/2026; em 2025 as quatro ficam entre R$ 1.566 e R$ 1.600. O ICV-DIEESE so existe de 1997 a 2019 (pesquisa suspensa em 2020-2023) e **nao encadeia**; neste intervalo o salario minimo de dezembro deflacionado por ele e pelo INPC coincide em 2019 por construcao (mesma base) e difere em 1996 (R$ 450,0 contra R$ 445,5).
3. **NAO ACHADO.** IPC-C1 da FGV (renda baixa): a serie historica fica atras de login em `extra-ibre.fgv.br`; nao achei no catalogo do Ipeadata e nao achei codigo no SGS (testei alguns codigos, nao varri o catalogo do SGS). Em seu lugar, e **rotulado como outro indice**, o Indicador Ipea de Inflacao por Faixa de Renda (renda muito baixa e baixa), que so comeca em jul/2006.
4. **ACHADO.** Excesso monetario anual 1948-2025 (crescimento de M0 e de M1 menos crescimento real do PIB, em pontos percentuais), ao lado de IGP-DI e IPCA de dezembro a dezembro. Co-movimento medido, sem causalidade: correlacao de Pearson M1-excesso x IGP-DI de 0,88 em 1948-2025, mas 0,45 em 1995-2025 (secao 4).
5. **ACHADO.** PNAD Continua (2012T1-2026T2): nivel da ocupacao, participacao, desocupacao, subutilizacao e desalento, trimestrais e media anual; quatro quebras de metodo dentro da serie (2015T4, 2016T2, 2020T2, 2021). **PARCIAL**: desocupacao da PNAD de 1981-1990 nao e publicada em tabela digital, mas os microdados existem no FTP do IBGE; **calculei 6 dos 10 anos** (1981, 1982, 1984, 1985, 1986, 1988) de microdados com arquivo de ate 25 MB: 4,26%, 3,93%, 4,26%, 3,37%, 2,43% e 3,80%; 1983, 1987, 1989 e 1990 ficam em branco porque o arquivo passa de 25 MB (29, 79, 100 e 103 MB). **NAO ACHADO**: desocupacao dos Censos de 1970 e 1980 (secao 5).
6. **ACHADO.** Definicoes oficiais (IBGE e OIT, com trecho literal) e resposta: receber beneficio nao muda a classificacao; ninguem cruza beneficio com forca de trabalho em tabela publicada (`definicoes.md`). A linha do Bolsa Familia nao e indexada e tem justificativa escrita minima; contra 1/4 do salario minimo ela vai de 0,77 (2004) a 0,35 (2022) (`bolsa_familia_linhas.md`).

## 2. Poder de compra (`series/poder_de_compra.csv`)

Formato longo: `indicador,fonte,definicao_linha,ano,valor,unidade,nota,vintage`. 19 indicadores, 929 linhas de valor. Anos completos so (12 meses). Reais atuais = moeda convertida pelo Ipeadata (cinco cortes de zeros 1967-1994); a razao salario minimo/cesta nao depende de deflator. Antes de maio/1984 o salario minimo e o MAIOR regional (fonte Ipea/MTE): a serie e um teto, nao a media.

| ano | cestas por SM | horas por cesta | SM real INPC | SM real IPCA | SM real IGP-DI | SM real IPC-Fipe |
|---|---|---|---|---|---|---|
| 1959 | 3,76 | 59 |  |  | 3.264 | 712 |
| 1963 | 2,52 | 87 |  |  | 2.481 | 515 |
| 1970 | 2,27 | 97 |  |  | 2.146 | 402 |
| 1974 | 1,46 | 151 |  |  | 2.085 | 396 |
| 1980 | 1,53 | 143 | 947 | 1.006 | 2.124 | 482 |
| 1985 | 1,40 | 157 | 819 | 876 | 1.524 | 529 |
| 1990 | 1,10 | 201 | 538 | 511 | 971 | 431 |
| 1994 | 0,95 | 231 | 550 | 541 | 864 | 462 |
| 1995 | 1,02 | 217 | 613 | 604 | 924 | 506 |
| 2002 | 1,42 | 155 | 797 | 792 | 1.021 | 710 |
| 2010 | 2,06 | 107 | 1.253 | 1.260 | 1.463 | 1.186 |
| 2014 | 2,10 | 105 | 1.403 | 1.410 | 1.615 | 1.375 |
| 2017 | 2,16 | 102 | 1.475 | 1.487 | 1.757 | 1.460 |
| 2022 | 1,59 | 138 | 1.447 | 1.465 | 1.277 | 1.428 |
| 2025 | 1,76 | 125 | 1.597 | 1.600 | 1.566 | 1.582 |

SM real = media dos 12 meses do salario minimo mensal deflacionado, em R$ de set/2026. Celula vazia = indice nao existe naquele ano (INPC desde abr/1979, IPCA desde 1980).

Pontos de conferencia: (a) a serie INPC coincide com `../economia-real/saida-salmin-real-anual.csv` (Ipea) ate o centavo em 1980, 1990, 2000, 2010, 2020 e 2025, e em 1991-1993 e 1995-1996; em **1994** difere 1,6% (550,39 contra 541,79), por causa da conversao de moeda de julho de 1994 (`quebras.csv`). (b) O indice IGP-DI do Ipeadata tem um salto de nivel de x1,182 em jul/1994 frente as taxas mensais do SGS 190: o indice reproduz a taxa anual de 1994 (1.093,9%) e a cadeia mensal da 909,7%; mantive o do Ipeadata. (c) Nos cinco meses de corte de moeda a cesta convertida varia em linha com o IGP-DI (`series/_conferencias.txt`).

Indicadores separados no CSV: `salario_minimo_nominal`, `cesta_basica_dieese_sp_nominal`, `cestas_por_salario_minimo`, `horas_de_trabalho_por_cesta`, `salario_minimo_real_{inpc,igpdi,ipcfipe,ipca,ipea_renda_muito_baixa,ipea_renda_baixa}`, `inflacao_dez_dez_*` (dos mesmos seis indices e do ICV-DIEESE), `salario_minimo_dezembro_real_icv_dieese` e `..._inpc_mesma_base_do_icv` (R$ de dez/2019, 1996-2019).

Horas: formula do DIEESE (`bruto/dieese-metodologia-cesta-basica-2016.pdf`, secao 4): custo da cesta x 220 / salario minimo vigente, 220 h/mes "desde outubro de 1988". Aqui 220 h em todos os anos e a cesta de Sao Paulo (o DIEESE publica por capital). A cesta e a "Racao Essencial Minima" do Decreto-Lei 399/1938, com a quantidade de cada produto fixa; o DIEESE atualizou a pesquisa em jan/2016 (27 capitais, coleta, ponderacao).

## 3. ICV-DIEESE e IPC-C1

* **ICV-DIEESE**: taxas anuais de 1997-2004 (relatorio do DIEESE, tabela 2) e 2004-2019 (notas anuais), 23 anos, todas conferidas por programa contra o texto do PDF. A pagina antiga do DIEESE diz que o "Banco de Dados" do ICV esta "ainda nao disponivel"; a nova diz "há um hiato na série histórica do ICV" (suspensa em mar/2020, retomada em ago/2023 com ponderacao da POF 2017/18, "impossível voltar com o índice no tempo"). Resultado: **sem serie mensal, sem ICV antes de 1997, sem ICV depois de 2019**. 2005: 4,54% na nota de 2005 e 4,55% na de 2006 (revisao de 0,01 p.p.). A tabela de 1997-2004 vem arredondada a 0,1.
* **IPC-C1 (FGV)**: definicao da propria FGV, "mede a variação do custo de vida para famílias com renda entre 1 e 2,5 salários-mínimos mensais", serie desde 2004; a "Série Histórica" leva a uma pagina de autenticacao para produtos licenciados. Procurei no catalogo do Ipeadata (4.071 series, busca por "c1", "baixa renda", "1 a 2,5"), em alguns codigos do SGS do BCB e na edicao de julho/2025 de "Conjuntura Estatistica" da FGV (sem texto de IPC-C1): **nao achei serie aberta**. Nao usei noticias de jornal como fonte.

## 4. Excesso monetario (`series/excesso_monetario.csv`)

Formula (declarada): `M_cresc(t) = (M_dez(t) / M_dez(t-1) - 1) x 100` com M em saldo de fim de dezembro, na mesma moeda (`../monetario/saida/anual.csv`); `excesso(t) = M_cresc(t) - PIB_real_cresc(t)`, em pontos percentuais, sem deflator. M0 = base monetaria restrita (SGS 1788); M1 = SGS 1827 (conceito antigo) ate 2017 e SGS 27791 ("Novo") de 2018 em diante; coluna `M1_novo_cresc_pct` traz o Novo tambem em 2003-2017. PIB real: `../economia-real/saida-pib-anual-1948-2025.csv`. IGP-DI e IPCA: variacao de dezembro a dezembro (IPCA desde 1981). Coincidencia sem importancia: o crescimento de M0 em 2018 (1,784%) e o do PIB (1,784%) tem o mesmo valor ate a terceira casa.

| ano | M0 cresc. % | M1 cresc. % | PIB real % | excesso M0 (p.p.) | excesso M1 (p.p.) | IGP-DI dez/dez % | IPCA dez/dez % |
|---|---|---|---|---|---|---|---|
| 1948 | 7,9 | 7,5 | 9,7 | -1,8 | -2,2 | 8,0 |  |
| 1955 | 18,6 | 17,4 | 8,8 | 9,8 | 8,6 | 12,1 |  |
| 1964 | 69,0 | 84,6 | 3,4 | 65,6 | 81,2 | 92,1 |  |
| 1975 | 35,4 | 43,5 | 5,2 | 30,2 | 38,4 | 29,4 |  |
| 1980 | 58,5 | 77,4 | 9,2 | 49,3 | 68,2 | 110,2 |  |
| 1985 | 257,3 | 304,3 | 7,8 | 249,5 | 296,4 | 235,1 | 242,2 |
| 1990 | 2.304,2 | 2.335,7 | -4,3 | 2.308,5 | 2.340,1 | 1.476,7 | 1.621,0 |
| 1993 | 1.953,2 | 2.129,4 | 4,9 | 1.948,2 | 2.124,5 | 2.708,2 | 2.477,1 |
| 1994 | 3.322,4 | 2.586,2 | 5,9 | 3.316,6 | 2.580,3 | 1.093,9 | 916,4 |
| 1995 | 22,6 | 25,1 | 4,2 | 18,4 | 20,9 | 14,8 | 22,4 |
| 2000 | -1,5 | 18,5 | 4,4 | -5,9 | 14,1 | 9,8 | 6,0 |
| 2008 | 0,6 | -3,5 | 5,1 | -4,5 | -8,5 | 9,1 | 5,9 |
| 2015 | -3,1 | -4,9 | -3,5 | 0,4 | -1,3 | 10,7 | 10,7 |
| 2020 | 36,3 | 43,2 | -3,3 | 39,6 | 46,5 | 23,1 | 4,5 |
| 2021 | -5,2 | 1,9 | 4,8 | -9,9 | -2,8 | 17,7 | 10,1 |
| 2025 | -0,9 | -1,7 | 2,3 | -3,2 | -4,0 | -1,2 | 4,3 |

Co-movimento entre o excesso e a inflacao do ano (so descricao; correlacao nao e causa; os anos de hiperinflacao dominam as medias; 78 anos de dados, nao 78 observacoes independentes):

| periodo | excesso M1 x IGP-DI (Pearson / Spearman) | excesso M0 x IGP-DI | excesso M1 x IPCA | n (IGP-DI) |
|---|---|---|---|---|
| 1948-2025 | 0,88 / 0,85 | 0,84 / 0,82 | 0,87 / 0,65 | 78 |
| 1948-1979 | 0,79 / 0,70 | 0,84 / 0,77 | n/d (IPCA so desde 1981) | 32 |
| 1980-1994 | 0,81 / 0,83 | 0,74 / 0,82 | 0,79 / 0,81 | 15 |
| 1995-2025 | 0,45 / 0,38 | 0,36 / 0,22 | 0,08 / -0,05 | 31 |

Anos com excesso de M1 negativo (M1 cresceu menos que o PIB real): 1948, 2008, 2011, 2015, 2021, 2022, 2023, 2025. Os maiores: 1994 (2.580 p.p.), 1990 (2.340 p.p.), 1993 (2.124 p.p.), 1989 (1.381 p.p.). Limite: a mudanca de conceito do M1 em 2018 (dez/2017: +5,2% so pelo conceito, ver `../monetario/RESULTADO.md`) cai dentro do periodo, e o crescimento em 1980-1994 e nominal em hiperinflacao.

## 5. Trabalho (`series/trabalho.csv`)

Colunas: `indicador,fonte,definicao_linha,ano,trimestre,valor,unidade,nota,vintage` (`trimestre` = T1-T4 ou `ano` para a media simples dos quatro trimestres; 2026 so tem T1 e T2, sem media). Tabelas SIDRA conferidas na pagina de metadados: 4093 (variaveis 1641 pessoas de 14+, 4088 forca de trabalho, 4090 ocupadas, 4092 desocupadas, 4094 fora da forca, 4096 participacao, 4097 nivel da ocupacao, 4099 desocupacao), 4099 (4116, 4118 subutilizacao composta, 4114) e 6813 (9869 percentual de desalentados na forca de trabalho ou desalentada). Trimestre fixo, nao movel.

| ano (media de 4 trimestres) | nivel da ocupacao % | participacao % | desocupacao % | subutilizacao composta % | desalentados % |
|---|---|---|---|---|---|
| 2012 | 58,0 | 62,7 | 7,4 | 18,3 | 1,9 |
| 2013 | 58,1 | 62,6 | 7,2 | 16,4 | 1,8 |
| 2014 | 58,0 | 62,4 | 6,9 | 15,0 | 1,4 |
| 2015 | 57,3 | 62,7 | 8,6 | 17,3 | 1,9 |
| 2016 | 55,4 | 62,7 | 11,6 | 21,0 | 3,1 |
| 2017 | 54,9 | 63,0 | 12,8 | 23,9 | 3,8 |
| 2018 | 55,2 | 63,0 | 12,4 | 24,4 | 4,3 |
| 2019 | 55,8 | 63,5 | 12,0 | 24,2 | 4,2 |
| 2020 | 51,0 | 59,1 | 13,8 | 28,2 | 5,2 |
| 2021 | 53,1 | 61,1 | 13,2 | 27,2 | 4,8 |
| 2022 | 56,5 | 62,3 | 9,2 | 20,8 | 3,8 |
| 2023 | 56,8 | 61,8 | 8,0 | 17,9 | 3,3 |
| 2024 | 58,0 | 62,2 | 6,8 | 16,3 | 2,9 |
| 2025 | 58,5 | 62,2 | 5,9 | 14,4 | 2,5 |

Glosas: **nivel da ocupacao** = ocupados / pessoas de 14 anos ou mais (todas, inclusive quem esta fora da forca de trabalho); **desocupacao** = desocupados / forca de trabalho; **subutilizacao composta** = (desocupados + subocupados por insuficiencia de horas + forca de trabalho potencial) / (forca de trabalho + forca de trabalho potencial); **desalentados** = quem quer trabalhar e esta disponivel mas nao procura por achar que nao vai achar.

Quebras dentro da PNAD Continua (`quebras.csv`): 2015T4 (conceito de ocupada ajustado a OIT), 2016T2 (conceito de desocupada: quem ja arranjou trabalho para comecar so conta se comeca em menos de 4 meses), 2020T2 (coleta so por telefone) e 2021 (reponderacao). Entre a PNAD anual e a PNAD Continua ha sobreposicao 2012-2014: PNADC menos PNAD = +0,67, +0,15 e -0,54 p.p. (quebra de sinal, ver `quebras.csv`).

### 5.1 Desocupacao da PNAD 1981-1990 calculada de microdados (`series/pnad_1981_1990_microdados.csv`)

Metodo (igual em todos os anos; posicoes e codigos lidos no dicionario `Documentacao.zip` de cada ano): registro de pessoa = tipo de registro `3`; variavel V501 "que fez na semana de referencia?": 1 trabalhou, 2 tinha trabalho mas nao trabalhou, 3 procurou trabalho, 4 a 7 fora da forca de trabalho, em branco menor de 10 anos; PEA = V501 em {1,2,3}; desocupado = V501 = 3; taxa = soma do peso da pessoa (V9991 ou equivalente) dos desocupados sobre a soma da PEA. Idade minima 10 anos (V501 em branco abaixo disso). **NAO e numero publicado pelo IBGE**; sem validacao contra um numero publicado do mesmo ano (as PNAD de 1992 e 1993, unicas com tabela publicada para comparar, tem Dados.zip de 27 MB, acima do limite). Checagens de plausibilidade: a PEA ponderada cresce de 47,5 milhoes (1981) a 61,0 milhoes (1988); a queda de 1984 para 1985 e 1986 vai no mesmo sentido da PME (6 regioes metropolitanas); o nivel nacional (2,4% a 4,3%) e menor que o da PME (4,0% a 8,1%); as duas pesquisas medem populacoes e janelas de procura diferentes (a PNAD inclui areas rurais; a PME so 6 regioes metropolitanas), entao os niveis nao sao comparaveis, so o sentido.

| ano | desocupacao PNAD derivada % | sem peso % | peso reponderado Censo 91 % | registros de pessoa | PME 6 RMs % (publicada, outra pesquisa) |
|---|---|---|---|---|---|
| 1981 | 4,26 | 4,59 |  | 482.611 | 7,90 |
| 1982 | 3,93 | 4,19 |  | 507.030 | 6,91 |
| 1983 | nao calculado (arquivo acima de 25 MB) | | | | 7,57 |
| 1984 | 4,26 | 4,57 |  | 514.866 | 8,15 |
| 1985 | 3,37 | 3,51 | 3,37 | 523.632 | 5,90 |
| 1986 | 2,43 | 2,57 | 2,42 | 289.783 | 3,99 |
| 1987 | nao calculado (arquivo acima de 25 MB) | | | | 4,08 |
| 1988 | 3,80 | 4,08 |  | 298.368 | 4,18 |
| 1989 | nao calculado (arquivo acima de 25 MB) | | | | 3,64 |
| 1990 | nao calculado (arquivo acima de 25 MB) | | | | 4,65 |

Avisos: (a) 1986 e 1988 tem cerca de 290 mil e 298 mil registros de pessoa contra 523 mil em 1985 (a amostra e menor; nao investiguei o motivo; as taxas usam os pesos de cada ano). (b) De 1981 a 1990 a PNAD cobre o pais menos a area rural da antiga Regiao Norte (nota do IBGE em `bruto/wayback-series-estatisticas/FDT222.html`). (c) O IBGE reponderou 1984-1990 pela projecao do Censo 91 (mesma pagina): para 1985 e 1986 o arquivo traz as duas ponderacoes e a diferenca e de 0,002 e 0,012 p.p.; para 1984 e 1988 so ha uma e usei a do arquivo. (d) Antes de 1992 a PNAD nao contava como ocupados quem produzia para o proprio consumo (ver `../quebras/quebras.csv`).

**NAO ACHADO, com onde procurei:**

* **PNAD 1981-1990 publicada em tabela**: o SIDRA e o FTP de tabelas do IBGE (`Pesquisa_Nacional_por_Amostra_de_Domicilios_anual`) comecam em 1992; o Ipeadata `Dese_Pnad` e `DISOC_DESE` comecam em 1992; no "Series Estatisticas" do IBGE (via Wayback, 21 paginas de series de trabalho conferidas) a PNAD de desocupacao cobre 1992-2007 e 2001-2011; o Anuario Estatistico do Brasil (1983 a 1992) esta em PDF escaneado acima de 25 MB; a API da OIT (ILOSTAT) devolveu resposta vazia. **O que existe**: microdados da PNAD de 1976 a 1990 em `.../PNAD_anual/microdados/<ano>/` (`bruto/ibge-ftp-pnad-microdados-listagem.html`), e o que foi calculado esta na secao 5.1.
* **Desocupacao nos Censos 1970 e 1980**: nenhuma tabela digital achada; das 17 tabelas do SIDRA com condicao de atividade dos Censos cujo metadado conferi, a mais antiga comeca em 1991 (tabela 616; as outras, 2000 e 2010); o Ipeadata tem so a PEA por setor (`PEA_*`, sem desocupados). Nao verifiquei microdados dos Censos de 1970 e 1980.
* **Cruzamento beneficio x forca de trabalho**: nao existe em tabela oficial (`definicoes.md`, secao 4).
* **ICV-DIEESE** antes de 1997 e depois de 2019; **IPC-C1** (acima).
* **Justificativa escrita do R$ 218** (Lei 14.601/2023): a Exposicao de Motivos da MP 1.164/2023 nao cita o valor (`bolsa_familia_linhas.md`).

## 6. Quebras (`quebras.csv`)

10 linhas, mesmas colunas de `../quebras/quebras.csv`. Todo trecho citado foi conferido por programa contra o arquivo hasheado. Uma categoria nova de `tipo_de_quebra`, `mudanca_de_unidade` (conversao de moeda de 1994), alem de `metodo_estatistico` e `mudanca_de_regra`: se o consumidor das tres categorias antigas for estrito, mapear para `mudanca_de_regra`.

| quebra | data | tipo | efeito medido |
|---|---|---|---|
| PNAD Continua, pessoas ocupadas (SIDRA 4093, 4099) | 2015T4 | metodo_estatistico | sem sobreposicao nos dados baixados |
| PNAD Continua, taxa de desocupacao (SIDRA 4099) | 2016T2 | metodo_estatistico | sem sobreposicao nos dados baixados |
| PNAD anual (Ipeadata DISOC_DESE) -> PNAD Continua (SIDRA 4562/4099) | 2012 (inicio da PNAD Continua; PNAD anual termina em 2015) | metodo_estatistico | PNADC menos PNAD: +0,67 p.p. em 2012 (7,4 contra 6,728), +0,15 p.p. em 2013 (7,3 contra 7,148), -0,54 p.p. em 2014 (7,0 contra 7,538) |
| PNAD Continua, todos os indicadores (SIDRA 4093, 4099, 6813) | 2020T2 (coleta so por telefone) e 2021 (reponderacao) | metodo_estatistico | sem sobreposicao nos dados baixados |
| Cesta basica DIEESE, Sao Paulo (Ipeadata DIEESE12_CBSP12) | 2016-01 | metodo_estatistico | sem sobreposicao nos dados baixados |
| ICV-DIEESE, Sao Paulo (notas anuais do DIEESE) | 2020-03 a 2023-07 (pesquisa suspensa; retomada com resultados de julho/2023) | metodo_estatistico | nao encadeia |
| Salario minimo nominal (Ipeadata MTE12_SALMIN12) | 1984-05 (unificacao nacional do salario minimo) | mudanca_de_regra | sem sobreposicao nos dados baixados |
| Salario minimo real (Ipeadata GAC12_SALMINRE12) e deflacionamento em geral | 1994-07 (cruzeiro real -> real; divisor 2.750) | mudanca_de_unidade | IGP-DI de 1994 dez/dez: 1.093,9% no indice do Ipeadata contra 909,7% na cadeia das taxas mensais do SGS 190; SM real 1994 por INPC: 550,39 aqui contra |
| IPC-Fipe, Sao Paulo (Ipeadata FIPE12_IPCFIPE12) | 1939 (inicio), 1968 (para o IPE-USP) e 1973 (Fipe) | metodo_estatistico | sem sobreposicao nos dados baixados |
| linha de elegibilidade do Bolsa Familia (Lei 14.601/2023, art. 5, II) | 2023-06 | mudanca_de_regra | -1,3% na linha de pobreza em termos reais; extrema pobreza sem linha propria |

## 7. Arquivos desta pasta

* `series/poder_de_compra.csv`, `series/excesso_monetario.csv`, `series/trabalho.csv`, `series/pnad_1981_1990_microdados.csv`, `series/bolsa_familia_linhas.csv`, `series/bolsa_familia_linhas_anual.csv`, `series/_conferencias.txt`
* `definicoes.md`, `bolsa_familia_linhas.md`, `quebras.csv`, `RESULTADO.md`
* `bruto/` (93 arquivos hasheados em `manifest.jsonl`: Ipeadata, SIDRA, DIEESE, OIT, IBGE incl. microdados da PNAD 1981-1988 de ate 25 MB em `bruto/pnad-microdados` (~125 MB), Planalto, FGV, Wayback), `scripts/`
* Reutilizados sem copiar (ja hasheados em suas pastas): `../economia-real` (salario minimo nominal, IGP-DI, INPC, IPCA, PIB, desemprego, catalogo Ipeadata), `../quebras/bruto` (cesta DIEESE e notas do IBGE), `../monetario/saida` (M0 e M1), `../dominios-1/bruto/doc/leg` (leis e decretos).
