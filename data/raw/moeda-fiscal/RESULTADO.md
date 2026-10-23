# RESULTADO: moeda e fiscal (blocos A e B da Emenda 03)

> Gerado por `scripts/montar_resultado.py` a partir dos arquivos da pasta; as cifras vem dos CSV, nao foram digitadas. Aquisicao em 2026-10-20 com cadeia de hash em `manifest.jsonl` (231 linhas). Sem nota, sem ranking, sem atribuicao de causa. Legenda: [OK] verificado contra fonte ou reproduzido; [PARCIAL] feito com limite declarado; [NAO ACHADO] nao obtido, com o motivo.

## 0. Resumo

1. [OK] Bloco A: Selic over mensal 1974+ em tres fontes (1974-01 a 2026-09 (630 linhas)), meta Copom diaria desde 1999-03 (161 mudancas registradas), juro real ex-post mensal e anual (IPCA e IGP-DI), credito/PIB em duas bases do BCB, compulsorios, multiplicadores e velocidade derivados de `monetario/saida/`.
2. [OK] Bloco B: RTN Governo Central 1997-2025 em R$ e % do PIB (tabela 2.1 caixa, tabela 2.5 valor pago 2008+), mensal 1997-01 a 2026-07 em R$; NFSP por nivel (66 series SGS confirmadas no CKAN), anual e mensal.
3. [NAO ACHADO] Emendas parlamentares pagas por tipo (RP 6/7/8/9) e por ano: as tres fontes abertas encontradas pesam mais de 25 MB ou exigem chave (ver secao 2.3). Em disco: as regras (13 linhas, `regras_emendas.csv`) e a definicao legal de cada RP nas LDOs (`rp_identificadores.csv`).
4. [NAO ACHADO] SIOP para discricionarias: nao tentado (nao identifiquei endpoint aberto); a linha de discricionarias vem do RTN (caixa desde 2008 e valor pago desde 2008).
5. [OK] `eventos_fiscais.csv` (41 linhas), `marcos.csv` (12 linhas), `quebras.csv` (45 linhas) com trechos copiados do texto baixado. Ancoras nao localizadas: nenhuma.
6. [PARCIAL] Downloads que falharam (3; `sgs_432_2016-2026` foi substituido pelas janelas 2016-2025 e 2026): bruto/bcb/sgs_432_2016-2026.json <- falhou apos 4 tentativas: https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json&dataInicial=01/01/2016&dataFinal=20/10/2026 (<HTTPError 406: 'Not; bruto/marcos/imf-pr02-40-brasil-2002.html <- falhou apos 4 tentativas: https://www.imf.org/en/news/articles/2015/09/14/01/49/pr0240 (<HTTPError 403: 'Forbidden'>); bruto/marcos/sec-lehman-8k-2008-09-15.html <- falhou apos 4 tentativas: https://www.sec.gov/Archives/edgar/data/806085/000110465908059632/a08-22764_48k.htm (<HTTPError 403: 'Forbidden'>).

## 1. Bloco A: moeda

### 1.1 Selic over mensal e meta Copom

| arquivo | cobertura |
|---|---|
| `series/selic_over_mensal_ipeadata_BM12_TJOVER12.csv` | 1974-01 a 2026-09 (630 linhas) |
| `series/selic_over_mensal_ipeadata_PAN12_TJOVER12.csv` | 1974-01 a 2026-09 (633 linhas) |
| `series/selic_over_mensal_sgs4390.csv` | 1986-08 a 2026-09 (482 linhas) |
| `series/selic_meta_copom_fim_de_mes_sgs432.csv` | 1999-03 a 2026-10 (332 linhas) |
| `series/selic_meta_copom_fim_de_mes_ipeadata_BM366.csv` | 1996-07 a 2026-10 (364 linhas) |
| `series/selic_meta_copom_mudancas_sgs432.csv` | 1999-03 a 2026-09 (161 linhas) |

- [OK] **`PAN12_TJOVER12` e a mesma serie de `BM12_TJOVER12` anualizada, nao outra serie.** O metadado do Ipeadata marca `PAN12` como % a.a. ("Percentagem anualizada: elaboracao IPEA") e `BM12` como % a.m.; 630 meses em comum, 0 diferem mais de 0,005 pp de (1+BM12/100)^12-1 (maior diferenca 0). Quem tratar `PAN12` como mensal erra por um fator ~12.
- [OK] `BM12_TJOVER12` contra o SGS 4390 (confirmado no CKAN como "Taxa de juros - Selic acumulada no mes"): 482 meses em comum (1986-08 a 2026-09); 0 diferem mais de 0,005 pp (maior 0 pp). Exemplos: nenhum.
- [OK] `BM12_TJOVER12` e nulo em 1986-03, 1986-04 e 1986-05 (3 meses sem valor no JSON); `PAN12_TJOVER12` tem valor nesses meses. Nas series de juro real esses 3 meses usam a Selic mensal de-anualizada de PAN12, com aviso na coluna `nota`; `selic_over_mensal_ipeadata_BM12_TJOVER12.csv` tem 3 linhas a menos que `..._PAN12_...` por isso.
- O mes de outubro de 2026 (mes do download) foi excluido: o metadado do Ipeadata diz que o mes corrente e parcial, e o SGS 4390 trazia 0,61% para 2026-10 com o mes em curso.
- [OK] Meta Copom: o SGS 432 (confirmado no CKAN: "Taxa de juros - Meta Selic definida pelo Copom") so devolve dados a partir de 1999-03; a serie do Ipeadata `BM366_TJOVER366` esta em `selic_meta_copom_fim_de_mes_ipeadata_BM366` (1996-07 a 2026-10 (364 linhas)). O pedido citava 1996+: o que ha antes de 1999, se houver, esta so na serie do Ipeadata.
- A API do SGS recusa janela diaria maior que 10 anos (HTTP 406): por isso 4 janelas (1996-2005, 2006-2015, 2016-2025, 2026 ate 2026-10-20). Uma consulta exploratoria `ultimos/1` (nao gravada) devolveu o SGS 432 com data 04/11/2026, posterior ao dia da consulta; as janelas gravadas terminam em 2026-10-20 e nao contem essa linha.

### 1.2 Juro real ex-post

| arquivo | cobertura |
|---|---|
| `series/juro_real_ex_post_mensal_ipca.csv` | 1980-01 a 2026-09 (561 linhas) |
| `series/juro_real_ex_post_mensal_igpdi.csv` | 1974-01 a 2026-09 (633 linhas) |
| `series/juro_real_ex_post_anual_ipca.csv` | 1980 a 2025 (46 linhas) |
| `series/juro_real_ex_post_anual_igpdi.csv` | 1974 a 2025 (52 linhas) |

Formula: ((1+Selic over do mes)/(1+inflacao do mes)-1)*100; anual = composicao de 12 meses de cada lado (ano civil completo). Anos incompletos nao foram calculados (2026).
- [OK] SGS 433 vs Ipeadata (IPCA): 561 meses em comum, 0 diferem mais de 0,005 pp (maior 0 pp).
- [PARCIAL] SGS 190 vs Ipeadata (IGP-DI): 992 meses em comum, 12 diferem mais de 0,005 pp (maior 19.24 pp).
- Os codigos SGS 433 (IPCA) e 190 (IGP-DI) **nao estao no catalogo CKAN** (`package_search?q=codigo_sgs:433` e `:190` devolvem 0 resultados) e a pagina de metadados do SGS responde "System unavailable". Por isso o deflator usado nas series e o do Ipeadata (`PRECOS12_IPCAG12`, `IGP12_IGPDIG12`, com nome no metadado); o SGS entra so como conferencia.

### 1.3 Credito, compulsorios, multiplicadores, velocidade

| arquivo | cobertura |
|---|---|
| `series/base_ampliada_depositos_compulsorios_em_especie_sgs1828.csv` | 1994-07 a 2026-08 (386 linhas) |
| `series/compulsorios_depositos_a_prazo_em_especie_sgs1850.csv` | 1995-07 a 2026-08 (374 linhas) |
| `series/compulsorios_exigibilidade_adicional_em_especie_sgs1797.csv` | 2002-09 a 2017-06 (167 linhas) |
| `series/compulsorios_poupanca_em_especie_sgs1848.csv` | 1994-07 a 2026-08 (386 linhas) |
| `series/compulsorios_recursos_a_vista_em_especie_sgs1849.csv` | 1994-07 a 2026-08 (386 linhas) |
| `series/compulsorios_saldo_total_sgs17633.csv` | 1994-08 a 2026-08 (385 linhas) |
| `series/credito_ampliado_empresas_e_familias_pib_sgs28217.csv` | 2013-01 a 2026-08 (164 linhas) |
| `series/credito_ampliado_empresas_pib_sgs28867.csv` | 2013-01 a 2026-08 (164 linhas) |
| `series/credito_ampliado_familias_pib_sgs28868.csv` | 2013-01 a 2026-08 (164 linhas) |
| `series/credito_ampliado_total_pib_sgs28215.csv` | 2013-01 a 2026-08 (164 linhas) |
| `series/credito_sfn_recursos_direcionados_pib_sgs20628.csv` | 2007-03 a 2026-08 (234 linhas) |
| `series/credito_sfn_recursos_livres_pib_sgs20625.csv` | 2007-03 a 2026-08 (234 linhas) |
| `series/credito_sfn_setor_privado_total_rs_mi_sgs22052.csv` | 2012-01 a 2026-08 (176 linhas) |
| `series/credito_sfn_setor_publico_total_rs_mi_sgs22051.csv` | 2012-01 a 2026-08 (176 linhas) |
| `series/credito_sfn_total_pib_sgs20622.csv` | 1995-07 a 2026-08 (374 linhas) |
| `series/insuficiencia_direcionamento_credito_total_sgs17624.csv` | 2003-10 a 2026-08 (275 linhas) |
| `series/multiplicador_M1_M0_conceito_antigo.csv` | 1946-02 a 2018-06 (869 linhas) |
| `series/multiplicador_M1_M0_novo.csv` | 2002-01 a 2026-08 (296 linhas) |
| `series/multiplicador_M3_M0_novo.csv` | 2001-12 a 2026-08 (297 linhas) |
| `series/multiplicador_M3_M0_regime2001.csv` | 1988-08 a 2018-06 (359 linhas) |
| `series/outros_recolhimentos_total_sgs17625.csv` | 2003-10 a 2026-08 (275 linhas) |
| `series/velocidade_PIB_M1_dezembro_conceito_antigo.csv` | 1946 a 2017 (72 linhas) |
| `series/velocidade_PIB_M1_dezembro_novo.csv` | 2002 a 2025 (24 linhas) |
| `series/velocidade_PIB_M1_media12_conceito_antigo.csv` | 1947 a 2017 (71 linhas) |
| `series/velocidade_PIB_M1_media12_novo.csv` | 2002 a 2025 (24 linhas) |

- [PARCIAL] Credito/PIB: as "duas metodologias do BCB" foram tratadas como duas bases em arquivos separados, nunca emendadas: **SFN** (SGS 20622 e abertura livres/direcionados) e **credito ampliado** (SGS 28215 e aberturas). O SGS 20622 tem dados desde 1995-07, mas o catalogo CKAN declara `inicio_periodo` = 01-03-2007; as linhas anteriores a 2007-03 levam a flag na coluna `nota`. Nao achei, no CKAN nem no Ipeadata, uma serie de credito/PIB da decada de 1990 separada.
- [PARCIAL] **Setor privado.** O pre-registro pede "credito ao setor privado, % do PIB". O SGS 20622 e o credito total do SFN (setor publico incluido: o CKAN tem a serie irma 22051, setor publico). Cortes privados obtidos: SGS 22052 "Saldo das operacoes de credito por tipo de cliente - Setor privado - Total" em **R$ milhoes, desde 2012-01** (`credito_sfn_setor_privado_total_rs_mi_sgs22052.csv`), sem versao em % do PIB no catalogo que consultei; e SGS 28217/28867/28868 (credito ampliado a empresas e familias, ja sem governo geral) em % do PIB desde 2013-01. **Nao existe aqui o % do PIB do credito privado do SFN antes de 2012**; calcula-lo exigiria o PIB acumulado em 12 meses do BCB, que nao esta nesta pasta.
- [PARCIAL] Compulsorios: 87 de 167 meses fecham a soma de 1849+1848+1850+1797 com o total 17633 (tolerancia max(1; 0,01%)); detalhe em `derivado/compulsorios_identidade.csv`. A busca do CKAN por "compuls" nao retornou titulo; os codigos vieram de "Recolhimentos obrigatorios de instituicoes financeiras" (17633, 1797, 1848-1850) e "Base monetaria ampliada - Depositos compulsorios em especie" (1828).
- Multiplicadores M1/M0 e M3/M0 e velocidade PIB/M1 saem de `monetario/saida/mensal.csv` e `anual.csv` (nao refeitos); cada regime (M1 antigo, M1 Novo, M3 regime 2001, M3 Novo) e um arquivo, nunca emendado. Velocidade: media de 12 saldos (primaria) e saldo de dezembro (variante), conforme o aviso de `monetario/RESULTADO.md` 1.6.

## 2. Bloco B: fiscal

### 2.1 RTN (Tesouro Nacional)

Fonte: planilha `seriehistoricajul26.xlsx` ja hasheada em `mecanismos-contabil/manifest.jsonl` (sha256 35899d771fc4...), lida pelos CSV de aba de `mecanismos-contabil/derivado/rtn/`; nao foi baixada de novo.

| arquivo | cobertura |
|---|---|
| `series/rtn_gc_caixa_receita_total_rs_mi.csv` | 1997 a 2025 (29 linhas) |
| `series/rtn_gc_caixa_receita_total_pct_pib.csv` | 1997 a 2025 (29 linhas) |
| `series/rtn_gc_caixa_despesa_total_rs_mi.csv` | 1997 a 2025 (29 linhas) |
| `series/rtn_gc_caixa_despesa_total_pct_pib.csv` | 1997 a 2025 (29 linhas) |
| `series/rtn_gc_caixa_despesa_discricionarias_rs_mi.csv` | 2008 a 2025 (18 linhas) |
| `series/rtn_gc_caixa_despesa_discricionarias_pct_pib.csv` | 2008 a 2025 (18 linhas) |
| `series/rtn_gc_valor_pago_discricionarias_valor_pago_rs_mi.csv` | 2008 a 2025 (18 linhas) |
| `series/rtn_gc_valor_pago_discricionarias_valor_pago_pct_pib.csv` | 2008 a 2025 (18 linhas) |
| `series/rtn_gc_caixa_receita_total_mensal_rs_mi.csv` | 1997-01 a 2026-07 (355 linhas) |
| `series/rtn_gc_caixa_despesa_total_mensal_rs_mi.csv` | 1997-01 a 2026-07 (355 linhas) |

- 51 arquivos RTN no total (ver `series/INDICE.csv`). Discricionarias: linha 4.4.2 da tabela 2.1 vale 0 de 1997 a 2007 na planilha; foi tratada como linha nao publicada (sem valor), nao como gasto zero. Tabela 2.5 (valor pago) so existe a partir de 2008.
- Discricionarias em 2025: 204918.387047 R$ mi (caixa) e 204444.43044 R$ mi (valor pago); em % do PIB, 1.60864569261 e 1.60492504915.

### 2.2 NFSP por nivel (BCB)

Codigos confirmados no CKAN (titulo, unidade e primeiro mes na API):

| SGS | titulo no CKAN | unidade | primeiro mes | ultimo mes completo |
|---|---|---|---|---|
| 5717 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Governo Federal e Banco Central | Percentual | 1991-12 | 2026-08 |
| 5718 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Governo Federal | Percentual | 1999-12 | 2026-08 |
| 5719 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Banco Central | Percentual | 1999-12 | 2026-08 |
| 5720 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Governos estaduais e municipais | Percentual | 1991-12 | 2026-08 |
| 5721 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Governos estaduais | Percentual | 1998-12 | 2026-08 |
| 5722 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Governos municipais | Percentual | 1998-12 | 2026-08 |
| 5723 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Empresas estatais | Percentual | 2002-11 | 2026-08 |
| 5724 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Empresas estatais federais | Percentual | 2002-11 | 2026-08 |
| 5725 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Empresas estatais estaduais | Percentual | 1998-12 | 2026-08 |
| 5726 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Empresas estatais municipais | Percentual | 1998-12 | 2026-08 |
| 5727 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado nominal - Total - Setor público consolidado | Percentual | 2002-11 | 2026-08 |
| 5750 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Governo Federal e Banco Central | Percentual | 1991-12 | 2026-08 |
| 5751 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Governo Federal | Percentual | 1999-12 | 2026-08 |
| 5752 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Banco Central | Percentual | 1999-12 | 2026-08 |
| 5753 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Governos estaduais e municipais | Percentual | 1991-12 | 2026-08 |
| 5754 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Governos estaduais | Percentual | 1998-12 | 2026-08 |
| 5755 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Governos municipais | Percentual | 1998-12 | 2026-08 |
| 5756 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Empresas estatais | Percentual | 2002-11 | 2026-08 |
| 5757 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Empresas estatais federais | Percentual | 2002-11 | 2026-08 |
| 5758 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Empresas estatais estaduais | Percentual | 1998-12 | 2026-08 |
| 5759 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Empresas estatais municipais | Percentual | 1998-12 | 2026-08 |
| 5760 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Juros nominais - Total - Setor público consolidado | Percentual | 2002-11 | 2026-08 |
| 5783 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Governo Federal e Banco Central | Percentual | 1991-12 | 2026-08 |
| 5784 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Governo Federal | Percentual | 1999-12 | 2026-08 |
| 5785 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Banco Central | Percentual | 1999-12 | 2026-08 |
| 5786 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Governos estaduais e municipais | Percentual | 1991-12 | 2026-08 |
| 5787 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Governos estaduais | Percentual | 1998-12 | 2026-08 |
| 5788 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Governos municipais | Percentual | 1998-12 | 2026-08 |
| 5789 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Empresas estatais | Percentual | 2002-11 | 2026-08 |
| 5790 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Empresas estatais federais | Percentual | 2002-11 | 2026-08 |
| 5791 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Empresas estatais estaduais | Percentual | 1998-12 | 2026-08 |
| 5792 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Empresas estatais municipais | Percentual | 1998-12 | 2026-08 |
| 5793 | NFSP s/ desv. cambial (% PIB) - Fluxo acumulado em 12 meses - Resultado primário - Total - Setor público consolidado | Percentual | 2002-11 | 2026-08 |
| 4573 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Governo Federal e Banco Central | Milhões de reais | 1991-02 | 2026-08 |
| 4574 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Governo Federal | Milhões de reais | 1999-01 | 2026-08 |
| 4575 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Banco Central | Milhões de reais | 1999-01 | 2026-08 |
| 4576 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Governos estaduais e municipais | Milhões de reais | 1991-02 | 2026-08 |
| 4577 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Governos estaduais | Milhões de reais | 1998-01 | 2026-08 |
| 4578 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Governos municipais | Milhões de reais | 1998-01 | 2026-08 |
| 4579 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Empresas estatais | Milhões de reais | 2001-12 | 2026-08 |
| 4580 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Empresas estatais federais | Milhões de reais | 2001-12 | 2026-08 |
| 4581 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Empresas estatais estaduais | Milhões de reais | 1998-01 | 2026-08 |
| 4582 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Empresas estatais municipais | Milhões de reais | 1998-01 | 2026-08 |
| 4583 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado nominal - Total - Setor público consolidado | Milhões de reais | 2001-12 | 2026-08 |
| 4606 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Governo Federal e Banco Central | Milhões de reais | 1991-02 | 2026-08 |
| 4607 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Governo Federal | Milhões de reais | 1999-01 | 2026-08 |
| 4608 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Banco Central | Milhões de reais | 1999-01 | 2026-08 |
| 4609 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Governos estaduais e municipais | Milhões de reais | 1991-02 | 2026-08 |
| 4610 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Governos estaduais | Milhões de reais | 1998-01 | 2026-08 |
| 4611 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Governos municipais | Milhões de reais | 1998-01 | 2026-08 |
| 4612 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Empresas estatais | Milhões de reais | 2001-12 | 2026-08 |
| 4613 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Empresas estatais federais | Milhões de reais | 2001-12 | 2026-08 |
| 4614 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Empresas estatais estaduais | Milhões de reais | 1998-01 | 2026-08 |
| 4615 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Empresas estatais municipais | Milhões de reais | 1998-01 | 2026-08 |
| 4616 | NFSP s/ desv. cambial - Fluxo mensal corrente - Juros nominais - Total - Setor público consolidado | Milhões de reais | 2001-12 | 2026-08 |
| 4639 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Governo Federal e Banco Central | Milhões de reais | 1991-02 | 2026-08 |
| 4640 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Governo Federal | Milhões de reais | 1999-01 | 2026-08 |
| 4641 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Banco Central | Milhões de reais | 1999-01 | 2026-08 |
| 4642 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Governos estaduais e municipais | Milhões de reais | 1991-02 | 2026-08 |
| 4643 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Governos estaduais | Milhões de reais | 1998-01 | 2026-08 |
| 4644 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Governos municipais | Milhões de reais | 1998-01 | 2026-08 |
| 4645 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Empresas estatais | Milhões de reais | 2001-12 | 2026-08 |
| 4646 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Empresas estatais federais | Milhões de reais | 2001-12 | 2026-08 |
| 4647 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Empresas estatais estaduais | Milhões de reais | 1996-01 | 2026-08 |
| 4648 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Empresas estatais municipais | Milhões de reais | 1996-01 | 2026-08 |
| 4649 | NFSP s/ desv. cambial - Fluxo mensal corrente - Resultado primário - Total - Setor público consolidado | Milhões de reais | 2001-12 | 2026-08 |

- Sinal: conforme a fonte. Leitura do sinal (inferencia, a pagina do CKAN nao a declara): valor positivo = deficit (necessidade de financiamento), negativo = superavit; no consolidado, resultado primario 12 meses em dez/2008 = -3.33; dez/2015 = 1.86; dez/2020 = 9.24 (% do PIB).
- Anual = valor de dezembro do fluxo acumulado em 12 meses em % do PIB (selecao, nao soma). Fluxos mensais em R$ milhoes vem em arquivo proprio; soma anual em R$ nao foi gerada.
- O catalogo do BCB descreve a abrangencia: sem Petrobras (dados de maio/2009 em diante) e sem Eletrobras (novembro/2010 em diante), recalculado so ate dez/2001; ver `quebras.csv`.

### 2.3 Emendas parlamentares

- [OK] `regras_emendas.csv`: EC 86/2015, EC 100/2019, EC 105/2019, EC 126/2022 e LC 210/2024, data e trecho copiados do texto do Planalto, com a vigencia lida do proprio texto.
- [OK] `rp_identificadores.csv`: a definicao legal de RP 6 (individuais), RP 7 (bancada estadual), RP 8 (comissoes) e RP 9 (relator-geral) nas LDOs 2020 a 2025 baixadas.
- [NAO ACHADO] **Valores pagos por tipo e ano.** Nao baixei: (a) Portal da Transparencia, `EmendasParlamentares.zip`, 32.490.844 bytes (cabecalho HTTP `content-length`); o site em HTML devolve verificacao humana e a API exige chave; (b) Tesouro Transparente, "Emendas Parlamentares Individuais e de bancada", CSV de 67,1 MiB segundo a pagina (so individuais e bancada, desde 2015); (c) Tesouro, "Despesas e Transferencias Totais da Uniao", um XLSX por ano; tamanhos lidos da pagina do CKAN em 2026-10-20: 2010 a 2025 entre 28,2 e 38,5 MiB (2020: 35,7; 2021: 36; 2022: 34,9; 2023: 30,3; 2024: 28,2; 2025: 32,9), 2008 e 2009 "0 bytes"; so o de 2026 (22 MiB, ano em curso) cabe no teto e nao foi baixado (um ano parcial nao entrega a serie pedida). Nao sondei se essas bases trazem o identificador RP. Todos os demais acima do teto de 25 MB. Metadados do Tesouro: `bruto/tesouro/metadados-emendas-individuais-bancada.pdf`.
- Caminho para completar, se o teto for liberado: a coluna de tipo de emenda do CSV do Portal da Transparencia ou o identificador RP das bases do Tesouro, somando o valor pago por ano; o mapeamento tipo -> RP esta em `rp_identificadores.csv`.

### 2.4 Eventos fiscais, marcos e quebras

- `eventos_fiscais.csv`: LRF (LC 101/2000), EC 95/2016, EC 103/2019, LC 200/2023, DLG 6/2020, EC 126/2022 art. 3 e uma linha por LDO de 2001 a 2025 e por lei que alterou LDO (41 no total). A coluna `trecho` traz a primeira ocorrencia da clausula da meta de resultado primario; a pagina do Planalto pode mostrar tambem a redacao alterada por lei posterior (aviso na coluna `nota`). A meta citada e a do ato, nao o resultado apurado. LDO 2026 nao foi baixada.
- `marcos.csv` (12 linhas): Real (Lei 8.880/1994, Lei 9.069/1995), cambio flutuante 1999 (BCB, duas datas no mesmo documento: 15.01 e 18.01), Decreto 3.088/1999, 2002 (Relatorio de Inflacao set/2002), 2008 (MP 442 e Relatorio de Inflacao dez/2008), recessao 2014-2016 (CODACE, copia hospedada pelo Poder360), OMS 11/03/2020, DLG 6/2020, LC 179/2021. Nao obtidos (HTTP 403 ao servidor com o agente de usuario da cadeia): comunicado do FMI de 06/09/2002 e o 8-K da Lehman na SEC.
- `quebras.csv` (45 linhas, colunas de `quebras/quebras.csv`): linhas proprias (abrangencia da NFSP, RTN, Selic, deflatores, credito, compulsorios) e linhas herdadas de `quebras/quebras.csv` (PIB e agregados monetarios) para as series que usam esses dados.

## 3. Estado da cadeia de hash

`manifest.jsonl`: 231 linhas. Verificacao: `python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py verify <pasta>` (resultado registrado em `STATE.md`).

## 4. NAO ACHADO e desvios

| item | situacao |
|---|---|
| Emendas pagas por RP e ano | bloqueado pelo teto de 25 MB (secao 2.3) |
| SIOP (discricionarias) | nao tentado; o RTN cobre a linha |
| Siga Brasil (emendas) | nao tentado |
| Credito privado do SFN em % do PIB | so R$ (SGS 22052, desde 2012); ver 1.3 |
| Selic meta Copom antes de 1999-03 no SGS | 432 comeca em 1999-03; ver Ipeadata BM366 |
| Credito/PIB dos anos 1990 em base separada | nao achado no CKAN nem no Ipeadata |
| IPCA/IGP-DI no CKAN | codigos 433 e 190 ausentes; usado o Ipeadata |
| Vintage anterior das series | um unico vintage em disco; revisoes nao medidas |
| Comunicado FMI 2002 e 8-K Lehman | HTTP 403 |
| LDO 2026 e LOA | nao baixadas |
| Aplicacao do ato a cada ano para emendas | so a vigencia lida do texto; sem tabela ano a ano alem de `regras_emendas.csv` |

**Desvios que o agente cometeu e corrigiu ou deixou registrado:**

- Uma chamada `curl -r -2000-` baixou o `EmendasParlamentares.zip` inteiro (32,5 MB) para o scratchpad por engano (o formato de faixa estava errado); o arquivo foi apagado, nao entrou na cadeia e nenhum dado dele foi usado. Uma sonda de tamanho (`-r 0-0`) de duas bases do Tesouro transferiu o corpo para `/dev/null` sem gravar nada.
- Duas filas de download rodaram por um instante em paralelo contra o mesmo `manifest.jsonl`; a verificacao da cadeia depois disso deu OK. Arquivos que o servidor respondeu com pagina HTML de erro foram rebaixados (linha nova na cadeia; a antiga fica).

## 5. Becos

- IPCA/IGP-DI no CKAN: volta se o BCB indexar os codigos 433/190.
- Portal da Transparencia em HTML: volta se alguem fornecer chave de API.
- Pagina de metadados do SGS: "System unavailable"; volta se o servico voltar.

## 5. Adendo 2026-10-23: emendas pagas (CGU) e bases do Tesouro

- [OK] `bruto/emendas/EmendasParlamentares.zip` (Portal da Transparencia, CGU, 32,5 MB, hash na cadeia): `scripts/emendas_pagas.py` -> `series/emendas_pagas_por_tipo_e_ano.csv` (valor pago no exercicio e restos a pagar pagos, por tipo e ano, 2014-2026). Na pagina: `emendas_pagas` e `emendas_pib`.
- [OK] `bruto/tesouro-despesas/despesas-transferencias-uniao-<ano>.xlsx`, 2008-2025 (Tesouro Transparente, CKAN 8675a0a4..., 30-40 MB cada, so o hash no repositorio): `scripts/baixar_tesouro_despesas.py`.
- [NAO EXISTE] Emendas pagas antes de 2014: o identificador de resultado primario das bases do Tesouro (`ID_IN_RESULTADO_EOF`) so traz o codigo 6 (despesa discricionaria decorrente de emenda individual) a partir de 2014; em 2013 ha apenas 0 (financeiro), 1 (primario obrigatorio), 2 (primario discricionario) e 3 (sem impacto fiscal). Antes da LDO 2014 a emenda nao era marcada no orcamento. Nada foi estimado.
