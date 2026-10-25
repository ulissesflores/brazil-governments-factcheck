# RESULTADO - coleta externo-fase3 (divida externa e custo da divida publica), 2026-10-23 (SGS 3685 acrescentada e errata em 2026-10-24)

Pasta: `fontes/dados/externo-fase3/`. Cadeia: `manifest.jsonl` (todo download por `govfc.chain add`). Scripts: `scripts/baixar.py` (rede) e `scripts/construir.py` (sem rede).
Dimensao `ext` do pre-registro original (PREREGISTRATION.md, 'External position: ... external debt'): camada descritiva da fase 1, sem emenda. Codigos do SGS nomeados pela Nota Explicativa do BCB de 24/02/2026 (`bruto/202602_Texto_de_estatisticas_do_setor_externo.pdf`).

## Os dois conceitos de divida externa bruta do BCB (US$ milhoes, fim de trimestre)

| Serie | Inicio | dez/2002 | dez/2010 | dez/2016 | dez/2022 | dez/2025 | Ultimo |
|---|---|---|---|---|---|---|---|
| divida_externa_bruta_restrita_usd_mi (SGS 3684) | 1972-12 | 210.711,3 | 256.910,0 | 326.297,4 | 319.634,3 | 386.147,9 | 407.102,8 (2026-06) |
| divida_externa_bruta_bpm6_usd_mi (SGS 25563) | 2002-03 | 230.068,0 | 452.780,0 | 675.841,0 | 679.413,0 | 819.546,0 | 869.522,0 (2026-06) |
| divida_externa_setor_publico_restrita_usd_mi (SGS 21521) | 1990-03 | 125.245,1 | 104.046,3 | 131.739,8 | 120.433,8 | 138.955,2 | 143.810,6 (2026-06) |
| intercompanhia_usd_mi (SGS 7941) | 1993-12 | 16.978,1 | 95.137,1 | 222.344,1 | 256.809,6 | 274.323,9 | 287.006,8 (2026-06) |
| titulos_mercado_domestico_nao_residentes_usd_mi (SGS 22160) | 2002-03 | 2.378,0 | 100.733,0 | 127.199,0 | 102.969,0 | 159.074,0 | 175.412,0 (2026-06) |

## Razoes publicadas pelo BCB (%, descontinuadas em fev/2026; publicadas como estao)

| Serie | Inicio | 1984T4 | 1999T4 | 2002T4 | 2007T4 | 2010T4 | 2016T4 | 2022T4 | Ultimo |
|---|---|---|---|---|---|---|---|---|---|
| divida_externa_restrita_pib_pct (SGS 11407) | 1971-12 | 53,8 | 41,2 | 41,8 | 14,1 | 12,0 | 18,2 | 16,4 | 17,3 (2025-09) |
| divida_externa_liquida_pib_pct (SGS 11409) | 1971-12 | 46,3 | 32,4 | 32,7 | -0,9 | -2,4 | -3,8 | -1,4 | -0,9 (2025-09) |
| divida_externa_setor_publico_pct (SGS 11408) | 1971-12 | 69,1 | 46,5 | 59,4 | 44,5 | 40,5 | 39,9 | 37,7 | 36,4 (2025-09) |
| pii_liquida_pib_pct (SGS 12506) | 2002-03 | sem dado | sem dado | -45,4 | -39,2 | -41,1 | -32,4 | -42,2 | -51,6 (2025-09) |

## Custo da divida publica (NFSP, 12 meses, % do PIB, convencao do BCB: positivo = deficit)

| Serie | Inicio | dez/2003 | dez/2010 | dez/2015 | dez/2016 | dez/2019 | dez/2022 | Ultimo |
|---|---|---|---|---|---|---|---|---|
| nfsp_juros_nominais_12m_pib_pct (SGS 5760) | 2002-11 | 8,4 | 5,0 | 8,4 | 6,5 | 5,0 | 5,8 | 8,9 (2026-08) |
| nfsp_resultado_nominal_12m_pib_pct (SGS 5727) | 2002-11 | 5,2 | 2,4 | 10,2 | 9,0 | 5,8 | 4,6 | 9,5 (2026-08) |
| nfsp_resultado_primario_12m_pib_pct (SGS 5793) | 2002-11 | -3,2 | -2,6 | 1,9 | 2,5 | 0,8 | -1,2 | 0,6 (2026-08) |

## Divida externa liquida em US$ (SGS 3685, AINDA PUBLICADA; a Tabela 31 foi descontinuada em fev/2026)

Definicao do BCB (coluna M da Tabela 31): liquida = bruta (restrita) - reservas internacionais - creditos brasileiros no exterior - haveres de bancos comerciais. Negativo = credor externo liquido. Tabela 31 da Nota de jan/2026 em `series/tabela31_nota_jan2026.csv`; a serie SGS 3685 coincide com ela em todos os trimestres comuns (jun/2024-set/2025) e traz dez/2025 revisado.

| Serie | Inicio | mar/1990 | dez/2002 | set/2007 | dez/2007 | dez/2010 | dez/2016 | dez/2022 | dez/2024 | dez/2025 | Ultimo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| divida_externa_liquida_usd_mi (SGS 3685) | 1987-06 | 100.656,5 | 164.999,1 | 16.952,5 | -11.947,6 | -50.627,8 | -67.413,4 | -27.483,0 | -13.510,0 | -8.701,6 | 5.083,5 (2026-06) |

ERRATA (2026-10-24). A primeira versao deste RESULTADO (2026-10-23) dizia que a noticia que motivou o pedido (BP Money, 21/10/2026; `bruto/noticia_bpmoney_2026-10-21.html`) calculava 'bruta - reservas' e que nao existia valor oficial de 2026 em nenhum conceito. As duas afirmacoes estavam erradas: o nivel da divida externa liquida continua publicado pelo BCB (SGS 3685) e e exatamente o numero da manchete (+5.083,49 em jun/2026, primeiro valor positivo desde set/2007); os 'US$ 402 bi de reservas' da manchete sao as reservas mais os creditos brasileiros no exterior e os haveres de bancos, o conjunto de ativos que o BCB subtrai (a propria noticia diz que os creditos ja estao contabilizados). O que foi descontinuado em fev/2026 e a RAZAO sobre o PIB (SGS 11409) e a Tabela 31. Nada foi calculado nem prolongado aqui.

## Leitura

'Sem dado' = a serie nao existe naquele ponto; nada estimado nem interpolado. As duas medidas de divida bruta nunca sao somadas nem emendadas: 25563 = 3684 + 7941 + 22160 por construcao do BCB, e a pagina mostra cada uma com o proprio nome. O WDI/IDS (DT.DOD.DECT.CD, GN.ZS) e um TERCEIRO conceito (Banco Mundial), usado so na comparacao com vizinhos na mesma fonte (colecao `mundo`).
