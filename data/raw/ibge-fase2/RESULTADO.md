# RESULTADO: coleta IBGE fase 2 (contas nacionais e TIC)

Pasta: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/ibge-fase2/`
Coleta em 2026-10-20. Bruto em `bruto/` (cadeia de hash em `manifest.jsonl`), serie longa em `series/ibge_fase2_longo.csv`
(indicador,fonte,definicao_linha,ano,mes_ou_trimestre,valor,unidade,nota,vintage; uma linha de base por `definicao_linha`, nenhuma base emendada),
sobreposicoes medidas em `series/sobreposicoes.csv`, quebras em `quebras.csv` (9 linhas, cabecalho igual ao de `moeda-fiscal/quebras.csv`).
Reconstrucao: `construir_series.py` e `tabela_anos_chave.py` (leem so `bruto/`; precisam de `xlrd`).

## Bases (definicao_linha)

| linha | o que e | cobertura |
|---|---|---|
| `ipeadata_concatenada` | series SCN10_* do Ipeadata; o PROPRIO Ipeadata concatena: 1947-1989 SCN Consolidadas, 1990-1994 ref. 1985, 1995-1999 CNT ref. 2010, 2000+ ref. 2010 (metadado SERCOMENTARIO). Nao foi emendada por nos | 1947-2025 |
| `ibge_scn_consolidadas_1947-1989` | IBGE SCN Consolidadas (edicao 2009 do FTP, quadros 1 e 7). Valor adicionado da transformacao e PIB "a custo de fatores", em moeda da epoca | 1947-1989 |
| `ibge_scn_ref2000_ed2009` | SCN ref. 2000, edicao 2009 (1995-1999 retropolados pelo IBGE). Transformacao = soma das classes (derivada por nos, conferida pelo residuo) | 1995-2009 |
| `ibge_scn_ref2010_ed2023` | SCN ref. 2010, edicao 2023 (tab05, tab06, tab10_1); PIB 1996-1999 so da tab06 | 2000-2023 (PIB desde 1996) |
| `ibge_cnt_ref2010_soma4tri` | SIDRA 1846 (CNT, ref. 2010): soma aritmetica dos 4 trimestres correntes (derivada por nos) | 1996-2025 |
| `pnad_microcomputador_com_internet_2003-2015` | SIDRA 2387, domicilios com microcomputador COM acesso a Internet | 2003-2015 (sem 2010) |
| `pnad_utilizacao_internet_2013-2015` | SIDRA 5144, domicilios com UTILIZACAO da Internet (qualquer equipamento) | 2013-2015 |
| `pnadc_tic_utilizacao_internet_2016+` | SIDRA 7307, PNAD Continua TIC | 2016-2025 (sem 2020) |

Indicadores em `series/`: razoes `ind_transf_sobre_pib_mercado_pct`, `ind_transf_sobre_pib_basico_pct`, `consumo_governo_sobre_pib_mercado_pct`,
`abertura_comercial_sobre_pib_mercado_pct`, `internet_domicilios_pct`, `ind_transf_pib_publicado_ipeadata_pct` (razao como publicada pelo Ipeadata), e os
componentes em nivel (`va_industria_transformacao`, `pib_mercado`, `pib_precos_basicos`, `consumo_final_governo`, `exportacoes_bens_servicos`,
`importacoes_bens_servicos`, `internet_domicilios_mil`, `domicilios_total_mil`) para reproduzir qualquer razao so com o CSV.
As razoes sao calculadas por nos, componente a componente, no mesmo ano e na mesma base; nada estimado, nada interpolado.

## Valores por item e por base (1994, 2002, 2010, 2016, 2018, 2022 e ultimo ano)

`n/d` = a base nao cobre o ano. Valores em %.

### ind_transf_sobre_pib_mercado_pct

| linha (base) | cobertura | 1994 | 2002 | 2010 | 2016 | 2018 | 2022 | ultimo ano (valor) |
|---|---|---|---|---|---|---|---|---|
| ibge_cnt_ref2010_soma4tri | 1996-2025 (30 anos) | n/d | 12.36 | 12.72 | 10.79 | 10.53 | 13.07 | 2025 (11.77) |
| ibge_scn_consolidadas_1947-1989 | 1947-1989 (43 anos) | n/d | n/d | n/d | n/d | n/d | n/d | 1989 (29.29) |
| ibge_scn_consolidadas_1947-1989_1980_duplicado_tab70_80 | 1980-1980 (1 anos) | n/d | n/d | n/d | n/d | n/d | n/d | 1980 (30.21) |
| ibge_scn_ref2000_ed2009 | 1995-2009 (15 anos) | n/d | 14.52 | n/d | n/d | n/d | n/d | 2009 (14.36) |
| ibge_scn_ref2010_ed2023 | 2000-2023 (24 anos) | n/d | 12.36 | 12.72 | 10.79 | 10.53 | 13.07 | 2023 (13.25) |
| ipeadata_concatenada | 1947-2025 (79 anos) | 23.72 | 12.36 | 12.72 | 10.79 | 10.53 | 13.07 | 2025 (11.77) |

### ind_transf_sobre_pib_basico_pct

| linha (base) | cobertura | 1994 | 2002 | 2010 | 2016 | 2018 | 2022 | ultimo ano (valor) |
|---|---|---|---|---|---|---|---|---|
| ibge_cnt_ref2010_soma4tri | 1996-2025 (30 anos) | n/d | 14.48 | 14.97 | 12.48 | 12.27 | 15.08 | 2025 (13.69) |
| ibge_scn_consolidadas_1947-1989 | 1947-1989 (43 anos) | n/d | n/d | n/d | n/d | n/d | n/d | 1989 (32.39) |
| ibge_scn_consolidadas_1947-1989_1980_duplicado_tab70_80 | 1980-1980 (1 anos) | n/d | n/d | n/d | n/d | n/d | n/d | 1980 (33.49) |
| ibge_scn_ref2000_ed2009 | 1995-2009 (15 anos) | n/d | 16.85 | n/d | n/d | n/d | n/d | 2009 (16.65) |
| ibge_scn_ref2010_ed2023 | 2000-2023 (24 anos) | n/d | 14.48 | 14.97 | 12.48 | 12.27 | 15.08 | 2023 (15.17) |
| ipeadata_concatenada | 1947-2025 (79 anos) | 26.79 | 14.48 | 14.97 | 12.48 | 12.27 | 15.08 | 2025 (13.69) |

### ind_transf_pib_publicado_ipeadata_pct

| linha (base) | cobertura | 1994 | 2002 | 2010 | 2016 | 2018 | 2022 | ultimo ano (valor) |
|---|---|---|---|---|---|---|---|---|
| ipeadata_concatenada | 1947-2025 (79 anos) | 26.79 | 14.48 | 14.97 | 12.48 | 12.27 | 13.07 | 2025 (11.77) |

### consumo_governo_sobre_pib_mercado_pct

| linha (base) | cobertura | 1994 | 2002 | 2010 | 2016 | 2018 | 2022 | ultimo ano (valor) |
|---|---|---|---|---|---|---|---|---|
| ibge_cnt_ref2010_soma4tri | 1996-2025 (30 anos) | n/d | 19.81 | 19.02 | 20.38 | 19.90 | 18.40 | 2025 (19.13) |
| ibge_scn_consolidadas_1947-1989 | 1947-1989 (43 anos) | n/d | n/d | n/d | n/d | n/d | n/d | 1989 (15.50) |
| ibge_scn_consolidadas_1947-1989_1980_duplicado_tab70_80 | 1980-1980 (1 anos) | n/d | n/d | n/d | n/d | n/d | n/d | 1980 (9.19) |
| ibge_scn_ref2000_ed2009 | 1995-2009 (15 anos) | n/d | 20.57 | n/d | n/d | n/d | n/d | 2009 (21.21) |
| ibge_scn_ref2010_ed2023 | 2000-2023 (24 anos) | n/d | 19.81 | 19.02 | 20.38 | 19.90 | 18.40 | 2023 (19.04) |
| ipeadata_concatenada | 1947-2025 (79 anos) | 17.87 | 19.81 | 19.02 | 20.38 | 19.90 | 18.40 | 2025 (19.13) |

### abertura_comercial_sobre_pib_mercado_pct

| linha (base) | cobertura | 1994 | 2002 | 2010 | 2016 | 2018 | 2022 | ultimo ano (valor) |
|---|---|---|---|---|---|---|---|---|
| ibge_cnt_ref2010_soma4tri | 1996-2025 (30 anos) | n/d | 27.62 | 22.77 | 24.53 | 28.88 | 38.82 | 2025 (35.29) |
| ibge_scn_consolidadas_1947-1989 | 1947-1989 (43 anos) | n/d | n/d | n/d | n/d | n/d | n/d | 1989 (14.39) |
| ibge_scn_consolidadas_1947-1989_1980_duplicado_tab70_80 | 1980-1980 (1 anos) | n/d | n/d | n/d | n/d | n/d | n/d | 1980 (20.33) |
| ibge_scn_ref2000_ed2009 | 1995-2009 (15 anos) | n/d | 26.68 | n/d | n/d | n/d | n/d | 2009 (22.12) |
| ibge_scn_ref2010_ed2023 | 2000-2023 (24 anos) | n/d | 27.62 | 22.77 | 24.53 | 28.88 | 38.82 | 2023 (33.67) |
| ipeadata_concatenada | 1947-2025 (79 anos) | 18.67 | 27.62 | 22.77 | 24.53 | 28.88 | 38.82 | 2025 (35.29) |

### internet_domicilios_pct

| linha (base) | cobertura | 1994 | 2002 | 2010 | 2016 | 2018 | 2022 | ultimo ano (valor) |
|---|---|---|---|---|---|---|---|---|
| pnad_microcomputador_com_internet_2003-2015 | 2003-2015 (12 anos) | n/d | n/d | n/d | n/d | n/d | n/d | 2015 (40.47) |
| pnad_utilizacao_internet_2013-2015 | 2013-2015 (3 anos) | n/d | n/d | n/d | n/d | n/d | n/d | 2015 (57.80) |
| pnadc_tic_utilizacao_internet_2016+ | 2016-2025 (9 anos) | n/d | n/d | n/d | 70.80 | 80.50 | 91.60 | 2025 (95.00) |


## Denominador: decisao NAO tomada por nos, declarada

O pre-registro pede "valor adicionado da transformacao / PIB a precos correntes". Ha dois denominadores legitimos e eles diferem em ~2 pontos percentuais
(2010: 12.72% sobre PIB a precos de mercado, 14.97% sobre o valor adicionado total / PIB a precos basicos). Publicamos AMBOS
(`ind_transf_sobre_pib_mercado_pct` e `ind_transf_sobre_pib_basico_pct`) e quem usar deve escolher um e manter.
Fato descoberto: a razao publicada pelo Ipeadata (SCN10_VAITY10) usa PIB a precos basicos ate 2019 e PIB a precos de mercado de 2020 em diante
(coincide com a nossa razao a 0.00 pp em cada regime), com media de -1.915 pp entre os dois denominadores em 2020-2025 (min -2.010, max -1.645),
embora o metadado continue dizendo "PIB a precos basicos". Por isso NAO usamos a razao publicada do Ipeadata como item; usamos as razoes calculadas.
Antes de 1995 o "PIB a precos basicos" e o PIB a custo de fatores; o Ipeadata avisa que ate 1994 os tres grandes setores somam mais de 100% do PIB a precos basicos
(setor ficticio "dummy financeiro" negativo).

## Sobreposicoes medidas (`series/sobreposicoes.csv`; diferenca B menos A, em pontos percentuais)

| indicador | A -> B | anos | diferenca media (min a max) |
|---|---|---|---|
| industria de transformacao / PIB mercado | ref. 2000 (ed. 2009) -> ref. 2010 (ed. 2023) | 2000-2009 | -1.167 (-2.162 a -0.195) |
| industria de transformacao / VAB (basico) | ref. 2000 -> ref. 2010 | 2000-2009 | -1.207 (-2.370 a -0.104) |
| consumo do governo / PIB | ref. 2000 -> ref. 2010 | 2000-2009 | -0.894 (-1.557 a -0.311) |
| abertura comercial (X+M)/PIB | ref. 2000 -> ref. 2010 | 2000-2009 | +0.574 (-0.012 a +1.258) |
| industria de transformacao / PIB mercado | ref. 2000 (ed. 2009) -> CNT soma 4 tri (ref. 2010) | 1996-2009 | +1.328 (+0.195 a +2.162) |
| internet: microcomputador com internet -> utilizacao da Internet | SIDRA 2387 -> 5144 | 2013-2015 | +11.910 (+5.590 a +17.330), crescente |
| qualquer razao do SCN | CNT soma 4 tri <-> ref. 2010 ed. 2023 | 2000-2023 | 0.000 (as duas coincidem) |
| qualquer razao do SCN | Ipeadata <-> CNT / ref. 2010 ed. 2023 | 1996-2025 / 2000-2023 | 0.000 (o Ipeadata 1996+ e a propria CNT/ref. 2010) |
| qualquer razao do SCN | Ipeadata <-> IBGE Consolidadas | 1947-1989 | 0.000 (max 0.01 pp; o Ipeadata copia as Consolidadas, 1980 de tab80_89) |
| qualquer razao do SCN | Ipeadata <-> ref. 2000 (ed. 2009) | 1995-2009 | ver CSV; ex.: transformacao/PIB mercado -1.353 (-2.162 a -0.195) |

Sem sobreposicao (nao medido): Consolidadas -> ref. 1985 (1989/1990); ref. 1985 -> ref. 2000 (1994/1995); PNAD (5144, 2015) -> PNAD Continua (7307, 2016).
Descontinuidades observadas (nao sao medida de efeito de metodo): transformacao/PIB mercado na linha Ipeadata 29.29% (1989) -> 22.83% (1990) e
23.72% (1994) -> 14.54% (1995). Por regra do pre-registro (§8) esses trechos nao se encadeiam; cada base cobre so o seu trecho.
Tratar 1947-1989, 1990-1994 e 1995-2025 como trechos separados.

## O que nao foi achado / desvios declarados

1. SCN ref. 1985 (1990-1994) NAO foi obtido como arquivo IBGE: as edicoes do FTP comecam em 2005 e ja sao ref. 2000. O trecho 1990-1994 so existe aqui via Ipeadata (copia), sem conferencia contra o IBGE.
2. 1995 no Ipeadata: a CNT (SIDRA 1846) so comeca em 1996; a origem do valor de 1995 do Ipeadata nao foi verificada (nao coincide com a ref. 2000: 14.54% contra 16.25%).
3. Ipeadata baixou como serie concatenada; "uma linha por base" foi respeitada marcando a base no `definicao_linha` e preservando a nota de concatenacao; a base de cada ano segue o metadado, nao uma checagem por ano (exceto Consolidadas e ref. 2010/CNT, cujo casamento a 0.00 pp foi medido).
4. Transformacao na ref. 2000 e SOMA de classes publicadas (2000-2009: 0301-0334; 1995-1999: codigos 04-32), derivada por nos; conferida contra o residuo "Industria menos extrativas, utilidades e construcao" (assert no script, tolerancia 1.5 milhoes de R$).
5. CNT anual = soma de 4 trimestres correntes (derivada por nos); 2026 incompleto (so 2 trimestres), fora.
6. Consolidadas: 1980 aparece em tab70_80 e tab80_89 com valores diferentes (unidade e revisao; PIB 12 399 841 contra 12 507.8); a linha principal usa tab80_89 (coincide com o Ipeadata) e o outro valor esta em `ibge_scn_consolidadas_1947-1989_1980_duplicado_tab70_80`. Valores em nivel das Consolidadas ficam em moeda da epoca (sem conversao); so as razoes sao comparaveis.
7. Metadados do SIDRA (`sidra-*-metadados.json`) vieram comprimidos (gzip) do servidor; o hash na cadeia e do byte bruto; o parser descomprime. Datas de modificacao do SIDRA estao em `sidra-*-periodos.json`.
8. Internet: o conceito muda duas vezes (2387 e "microcomputador com internet"; 5144/7307 e "utilizacao da Internet por qualquer equipamento"); 2387 cai de 2014 para 2015 (42.09 -> 40.47) enquanto 5144 sobe (54.9 -> 57.8), e a diferenca entre as duas cresce de 5.59 a 17.33 pp, entao encadeamento por diferenca media seria inseguro. Lacunas: sem 2010 (2387) e sem 2020 (7307). O resumo de uma busca citou 69,3% para a PNAD Continua 2016; o SIDRA hoje traz 70.8% (modificacao 02/07/2026): nao verificado o motivo (possivel reponderacao); usamos o valor do SIDRA.
9. Nao ha serie pre-2003 de internet em domicilios nas tabelas coletadas (2387 comeca em 2003).
10. A edicao 2005 do FTP (`scn-vint2005-*`) foi baixada e guardada no bruto, mas nao entra nas series (e a mesma ref. 2000 em edicao mais antiga; serviria so para medir revisao de edicao).
11. Ultimo ano: SCN anual ref. 2010 vai a 2023; CNT e Ipeadata chegam a 2025; PNADC TIC a 2025.

## Cadeia de hash

Saida de `PYTHONPATH=code python3 -m govfc.chain verify /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/ibge-fase2`:

```
41 lines; head d1845a9a6667d27d9531ee964a777a859aed7d522cf713c663b92063a919b27e; 3 superseded (same path re-downloaded); OK
```
(3 linhas superseded: arquivos baixados duas vezes no mesmo caminho por reinicio do lote; o historico permanece na cadeia.)
