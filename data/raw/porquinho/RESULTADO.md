# RESULTADO: o porquinho (R$ 100.000 em dinheiro desde 1 de janeiro de 1995)

Colheita de 2026-10-20. Sem opiniao, sem nota, sem ranking: so numeros, fonte e limite. Pre-registro: `../preregistro/PREREGISTRATION-EMENDA-03.md`, secao E (mapa linha -> item registrado na secao 1.1). Tudo sai de `python3 -I scripts/construir.py`, `scripts/quebras_gerar.py` e `scripts/escrever_resultado.py`, que leem so arquivos locais; as formulas estao no cabecalho de `scripts/construir.py`. Os brutos entram na cadeia de hash (`manifest.jsonl`; `python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py verify .` -> 43 lines; head 2f41ca54a9e2b700c238c8c8d7eb4536cd4c188f7ccbfcd2c3051b9298a75fe5; OK). O imposto inflacionario nunca e somado a inflacao: nao e calculado em lugar nenhum.

Legenda: ACHADO = tem numero e fonte aqui; NAO ACHADO = procurei e nao obtive (com onde procurei).

## 1. Resumo

1. **ACHADO.** R$ 100.000 em dinheiro vivo em 1 jan 1995 compram, em set/2026, o que R$ 13.208 compravam em dez/1994 pelo IPCA (13.072 pelo INPC, 8.868 pelo IGP-DI, 15.701 pelo IPC-Fipe).
2. **ACHADO.** A mesma quantia na poupanca (SGS 25, regra de deposito ate 03/05/2012, aniversario no dia 1) vale em set/2026 R$ 231.405 (reais de dez/1994, IPCA) e na Selic R$ 1.131.005; diferenca caixa menos poupanca = R$ -218.197. Se a regra nova (SGS 195) valesse desde jun/2012 o saldo nominal de set/2026 seria R$ 1.563.850 em vez de R$ 1.752.040 (`series/_conferencias.txt`).
3. **ACHADO.** Em unidades relativas: R$ 100.000 eram 1.429 salarios minimos em dez/1994 e 61,7 em set/2026; 1.144 cestas DIEESE-SP e 111,0 em ago/2026; 43,6 anos de PIB per capita nominal (1994) e 1,74 (2024, ultimo ano publicado).
4. **ACHADO.** Quatro referencias externas, cada uma deflacionada pelo CPI da propria referencia (EUA para dolar, DES e ouro; Suica para o franco): US$ de dez/1994 117.633 -> 8.676 (2026-09); CHF de dez/1994 156.323 -> 12.749 (2026-08); DES de dez/1994 81.014 -> 6.369 (2026-08); onças de ouro (sem deflator) 310 -> 5 (2026-09).
5. **ACHADO com ressalva.** Ouro: a LBMA (preco PM diario) esta bloqueada para este IP (HTTP 403, Cloudflare, tambem no Chrome real) e o FRED retirou a serie (404). Usei a media mensal do Pink Sheet do Banco Mundial; a partir de jun/2025 o proprio Banco Mundial passa a usar o preco a vista medio em vez do fixing da tarde de Londres (`quebras.csv`, Q06 e Q07).
6. **ACHADO com ressalva.** ICV-DIEESE e Ipea renda muito baixa nao cobrem 1995-2026 (ICV: so taxa anual de 1997 a 2019; Ipea: jul/2006 a jul/2026). A parte sem fonte nao e preenchida: as linhas comecam com emenda no IPCA (dez/1996 e dez/2006) e o por-governo so mostra os mandatos com as duas pontas.

### 1.1 Mapa das linhas emitidas para os itens do pre-registro (secao E)

| item registrado | linhas em `series/porquinho.csv` | intermediarios (so para montar a linha registrada) |
|---|---|---|
| E.1 poder de compra por IPCA, INPC, IGP-DI, IPC-Fipe, ICV-DIEESE, Ipea renda muito baixa | `caixa_real_ipca`, `caixa_real_inpc`, `caixa_real_igpdi`, `caixa_real_ipcfipe`, `caixa_real_icv_dieese`, `caixa_real_ipea_renda_muito_baixa` | |
| E.2 poupanca e Selic deflacionadas pelo IPCA; caixa menos poupanca | `poupanca_real_ipca`, `selic_real_ipca`, `caixa_menos_poupanca_real_ipca` | `poupanca_nominal`, `selic_nominal` |
| E.3 anos de PIB per capita, salarios minimos, cestas DIEESE | `caixa_em_anos_pib_per_capita_nominal`, `caixa_em_salarios_minimos`, `caixa_em_cestas_dieese_sp` | |
| E.4 dolar, franco suico, DES, ouro, cada um deflacionado pela referencia | `usd_poder_compra_ref`, `chf_poder_compra_ref`, `sdr_poder_compra_ref`, `ouro_preco_real_usd_oz` | `usd_nominal`, `chf_nominal`, `sdr_nominal`, `ouro_oncas` (quantidade) |

Ouro: deflacionar a quantia em ouro pelo CPI dos EUA da exatamente a linha do dolar (numerador e denominador levam o mesmo deflator), portanto seria redundante; a referencia ouro deflacionada pelo CPI dos EUA e o preco, emitido como `ouro_preco_real_usd_oz`; `ouro_oncas` e a quantidade fisica, sem deflator. Total: 22 indicadores = 16 linhas registradas + 6 intermediarios (a quantidade `ouro_oncas` entra entre os intermediarios).

## 2. Tabela por governo (variacao de dez 1994 / inicio do mandato ate o fim, % e % ao ano)

Valores em `series/porquinho_por_governo.csv` (inicio e fim usados, valores, variacao absoluta, n_meses). Fronteira do mandato = fim do mes anterior (dia 1) ou do proprio mes (31/08/2016); Lula (3o mandato) termina no ultimo mes da linha (set/2026 ou antes, conforme a fonte; o mandato esta registrado ate 2026-10-19). Linha anual (PIB per capita): ano completo mais recente antes da fronteira. Variacao % = fim/inicio - 1; % a.a. = composta sobre n_meses.

| linha | FHC | Lula 1-2 | Dilma | Temer | Bolsonaro | Lula 3 |
|---|---|---|---|---|---|---|
| `caixa_real_ipca` | -50,2% (-8,3% a.a.) | -36,2% (-5,5% a.a.) | -32,5% (-6,7% a.a.) | -7,1% (-3,1% a.a.) | -21,2% (-5,8% a.a.) | -15,9% (-4,5% a.a.) |
| `caixa_real_inpc` | -51,0% (-8,5% a.a.) | -36,3% (-5,5% a.a.) | -32,9% (-6,8% a.a.) | -5,7% (-2,5% a.a.) | -22,2% (-6,1% a.a.) | -14,8% (-4,2% a.a.) |
| `caixa_real_igpdi` | -60,4% (-10,9% a.a.) | -39,0% (-6,0% a.a.) | -31,5% (-6,5% a.a.) | -7,2% (-3,2% a.a.) | -39,0% (-11,6% a.a.) | -5,6% (-1,5% a.a.) |
| `caixa_real_ipcfipe` | -46,3% (-7,5% a.a.) | -33,8% (-5,0% a.a.) | -29,8% (-6,1% a.a.) | -6,0% (-2,6% a.a.) | -23,0% (-6,3% a.a.) | -13,1% (-3,7% a.a.) |
| `caixa_real_ipea_renda_muito_baixa` | sem dado | sem dado | -34,2% (-7,1% a.a.) | -5,7% (-2,5% a.a.) | -23,0% (-6,3% a.a.) | -14,1% (-4,2% a.a.) |
| `caixa_real_icv_dieese` | sem dado | -36,1% (-5,5% a.a.) | sem dado | sem dado | sem dado | sem dado |
| `poupanca_nominal` | 212,7% (15,3% a.a.) | 88,7% (8,3% a.a.) | 48,6% (7,2% a.a.) | 16,4% (6,7% a.a.) | 29,2% (6,6% a.a.) | 32,9% (7,9% a.a.) |
| `poupanca_real_ipca` | 55,8% (5,7% a.a.) | 20,4% (2,4% a.a.) | 0,2% (0,0% a.a.) | 8,1% (3,4% a.a.) | 1,8% (0,4% a.a.) | 11,8% (3,0% a.a.) |
| `caixa_menos_poupanca_real_ipca` | -106.013 R$ | -49.854 R$ | -10.778 R$ | -16.799 R$ | -7.844 R$ | -26.909 R$ |
| `selic_nominal` | 546,2% (26,3% a.a.) | 198,2% (14,6% a.a.) | 79,8% (10,9% a.a.) | 22,2% (9,0% a.a.) | 27,8% (6,3% a.a.) | 58,3% (13,0% a.a.) |
| `selic_real_ipca` | 222,0% (15,7% a.a.) | 90,3% (8,4% a.a.) | 21,3% (3,5% a.a.) | 13,4% (5,6% a.a.) | 0,7% (0,2% a.a.) | 33,2% (7,9% a.a.) |
| `caixa_em_anos_pib_per_capita_nominal` | -73,1% (-15,1% a.a.) | -58,2% (-10,3% a.a.) | -31,9% (-7,4% a.a.) | -13,0% (-4,6% a.a.) | -30,7% (-8,8% a.a.) | -13,4% (-7,0% a.a.) |
| `caixa_em_salarios_minimos` | -65,0% (-12,3% a.a.) | -60,8% (-11,0% a.a.) | -42,0% (-9,2% a.a.) | -7,8% (-3,4% a.a.) | -21,3% (-5,8% a.a.) | -25,2% (-7,5% a.a.) |
| `caixa_em_cestas_dieese_sp` | -44,9% (-7,2% a.a.) | -40,1% (-6,2% a.a.) | -44,2% (-9,8% a.a.) | 0,8% (0,3% a.a.) | -40,4% (-12,1% a.a.) | -12,1% (-3,5% a.a.) |
| `usd_nominal` | -76,6% (-16,6% a.a.) | 114,1% (10,0% a.a.) | -47,2% (-10,7% a.a.) | -17,4% (-7,9% a.a.) | -25,9% (-7,2% a.a.) | 1,9% (0,5% a.a.) |
| `usd_poder_compra_ref` | -80,6% (-18,6% a.a.) | 76,6% (7,4% a.a.) | -51,6% (-12,0% a.a.) | -21,4% (-9,8% a.a.) | -37,3% (-11,0% a.a.) | -9,5% (-2,6% a.a.) |
| `chf_nominal` | -74,6% (-15,7% a.a.) | 44,2% (4,7% a.a.) | -47,1% (-10,6% a.a.) | -15,6% (-7,0% a.a.) | -30,4% (-8,7% a.a.) | -10,3% (-2,9% a.a.) |
| `chf_poder_compra_ref` | -76,4% (-16,5% a.a.) | 34,4% (3,8% a.a.) | -45,7% (-10,2% a.a.) | -16,8% (-7,6% a.a.) | -32,9% (-9,5% a.a.) | -15,2% (-4,4% a.a.) |
| `sdr_nominal` | -74,6% (-15,7% a.a.) | 86,8% (8,1% a.a.) | -42,1% (-9,2% a.a.) | -16,5% (-7,5% a.a.) | -22,7% (-6,2% a.a.) | -1,2% (-0,3% a.a.) |
| `sdr_poder_compra_ref` | -79,0% (-17,7% a.a.) | 54,1% (5,6% a.a.) | -46,9% (-10,6% a.a.) | -20,6% (-9,4% a.a.) | -34,7% (-10,1% a.a.) | -11,7% (-3,3% a.a.) |
| `ouro_oncas` | -73,2% (-15,2% a.a.) | -48,9% (-8,0% a.a.) | -45,2% (-10,1% a.a.) | -11,4% (-5,1% a.a.) | -48,5% (-15,3% a.a.) | -57,6% (-20,4% a.a.) |
| `ouro_preco_real_usd_oz` | -27,7% (-4,0% a.a.) | 245,5% (16,8% a.a.) | -11,7% (-2,2% a.a.) | -11,2% (-5,0% a.a.) | 21,7% (5,0% a.a.) | 113,5% (22,4% a.a.) |

Notas da tabela: `caixa_menos_poupanca_real_ipca` e uma diferenca em R$ (comeca em zero em dez/1994), por isso mostra a variacao absoluta; "sem dado" = a fonte nao tem observacao em uma das pontas (ICV so em dezembros de 1996 a 2019; Ipea so desde dez/2006).

## 3. Estado das linhas na data-base e no ultimo mes

| linha | dez/1994 | ultimo mes | valor no ultimo mes | unidade |
|---|---|---|---|---|
| `caixa_real_ipca` | 100.000,00 | 2026-09 | 13.207,73 | R$ de dez/1994 |
| `caixa_real_inpc` | 100.000,00 | 2026-09 | 13.071,74 | R$ de dez/1994 |
| `caixa_real_igpdi` | 100.000,00 | 2026-09 | 8.867,58 | R$ de dez/1994 |
| `caixa_real_ipcfipe` | 100.000,00 | 2026-09 | 15.700,91 | R$ de dez/1994 |
| `caixa_real_ipea_renda_muito_baixa` |  | 2026-07 | 12.510,07 | R$ de dez/1994 |
| `caixa_real_icv_dieese` |  | 2019-12 | 18.556,79 | R$ de dez/1994 |
| `poupanca_nominal` | 100.000,00 | 2026-09 | 1.752.040,39 | R$ correntes |
| `poupanca_real_ipca` | 100.000,00 | 2026-09 | 231.404,79 | R$ de dez/1994 |
| `caixa_menos_poupanca_real_ipca` | 0,00 | 2026-09 | -218.197,06 | R$ de dez/1994 |
| `selic_nominal` | 100.000,00 | 2026-09 | 8.563.202,59 | R$ correntes |
| `selic_real_ipca` | 100.000,00 | 2026-09 | 1.131.004,81 | R$ de dez/1994 |
| `caixa_em_anos_pib_per_capita_nominal` | | anual | | anos de PIB per capita nominal |
| `caixa_em_salarios_minimos` | 1.428,57 | 2026-09 | 61,69 | salarios minimos |
| `caixa_em_cestas_dieese_sp` | 1.143,90 | 2026-08 | 111,04 | cestas DIEESE Sao Paulo |
| `usd_nominal` | 117.633,22 | 2026-09 | 19.437,48 | US$ correntes |
| `usd_poder_compra_ref` | 117.633,22 | 2026-09 | 8.675,54 | US$ de dez/1994 |
| `chf_nominal` | 156.322,79 | 2026-09 | 15.936,79 | CHF correntes |
| `chf_poder_compra_ref` | 156.322,79 | 2026-08 | 12.749,32 | CHF de dez/1994 |
| `sdr_nominal` | 81.014,22 | 2026-08 | 14.177,45 | DES correntes |
| `sdr_poder_compra_ref` | 81.014,22 | 2026-08 | 6.368,86 | DES de dez/1994 |
| `ouro_oncas` | 310,38 | 2026-09 | 4,50 | onças troy |
| `ouro_preco_real_usd_oz` | 379,00 | 2026-09 | 1.927,70 | US$ de dez/1994 por onça |

## 4. Conferencias (todas em `series/_conferencias.txt`)

* SGS 25 (dia 1) vs Ipeadata ANBIMA12_TJPOUP12: 382 meses comparados, 0 divergencias > 0,0051
* SGS 195 (dia 1) vs Ipeadata BM12_RNDPO12: 173 meses comparados, 0 divergencias > 0,0051
* SGS 3698 vs Ipeadata BM12_ERV12 (venda, media): 382 meses, 91 diferem; maior diferenca relativa 0.582% em (1998, 2) (1.1271 vs 1.1337)
* SGS 3696 vs Ipeadata BM12_ERVF12 (venda, fim): 1 divergencias: [((1998, 2), 1.1304, 1.1374)]
* SGS 4390 vs Ipeadata BM12_TJOVER12: 394 meses, 0 divergencias > 0,0051
* IGP-DI dez/1994->dez/2025: cadeia SGS 190 = 10.875077; indice Ipeadata IGP12_IGPDI12 = 10.875742; razao 0.999939
* IPC-Fipe dez/1994->ago/2026: cadeia da taxa = 6.336872; indice Ipeadata FIPE12_IPCFIPE12 = 6.334152
* IPCA acumulado 12 meses a dez/2025 (cadeia SGS 433): 4.2644%
* IPC suico FRED CHECPIALLMINMEI ate (2025, 4) vs SNB LD2010100: 352 meses no overlap, maior diferenca na variacao de 12 meses = 0.0002% relativo
* poupanca com a regra nova (SGS 195) a partir de jun/2012, em (2026, 9): R$ 1,563,850.17 nominais contra R$ 1,752,040.39 pela regra antiga (SGS 25); real IPCA 206,549.13 contra 231,404.79
* meses (dia 1) em que SGS 25 e SGS 195 diferem: 66, de (2012, 6) a (2021, 12)
* US$ por R$ 100.000 em (2002, 12): media do mes 27,579 ; fim do mes 28,302
* US$ por R$ 100.000 em (2010, 12): media do mes 59,053 ; fim do mes 60,017
* US$ por R$ 100.000 em (2022, 12): media do mes 19,075 ; fim do mes 19,166

(As conferencias acima sao copia literal de `_conferencias.txt`: a formatacao de numeros e a de la.)

Arquivos de erro na cadeia (nao sao dados): `bruto/sgs25-poupanca-ate-2004.json`, `bruto/sgs195-poupanca-2012-2022.json` e `bruto/sgs25-poupanca-2018-2026.json` contem a pagina HTML "Requisicao invalida" do SGS (janela de 10 anos exatos, e uma consulta que falhou e funcionou minutos depois); os dados vieram das janelas refeitas (`sgs25-poupanca-1995-2000/2001-2004/2012-2017/2018-2026-refeito`, `sgs195-poupanca-2012-2017/2018-2022/2022-2026`). Os pacotes CKAN `ckan_1.json` e `ckan_3696.json` tambem sao pagina de erro.

Codigos SGS: a pagina de metadados do SGS respondeu "System unavailable" (3698). SGS 25, 195 e 4390: nome e periodicidade lidos no CKAN do BCB (`bruto/ckan_25.json`, `ckan_195.json`, `ckan_4390.json`; a SGS 25 e 195 sao diarias, "percentual ao mes"). SGS 3698 = dolar venda, media do mes e SGS 3696 = dolar venda, fim do mes: confirmados por igualdade com o Ipeadata BM12_ERV12 e BM12_ERVF12 (91 meses diferem na 4a ou 5a casa na media; so fev/1998 difere no fim do mes), nao pela pagina do SGS. Os pacotes CKAN de 3695, 3697, 3698 e 3694 voltaram vazios (`bruto/ckan_36*.json`); 3696 e 1 voltaram pagina de erro (ficam na cadeia).

## 5. NAO ACHADO e limites

* **LBMA PM diario** (pre-registro): HTTP 403 por curl e pelo Chrome real; FRED GOLDPMGBD228NLBM, 404. Nao contornei o bloqueio. Fonte usada no lugar: Banco Mundial Pink Sheet, media mensal (Q06).
* **ICV-DIEESE mensal, antes de 1997 ou depois de 2019**: nao existe em tabela aberta (`../poder-de-compra/RESULTADO.md` secao 3). Linha de dezembros 1996-2019, sem interpolacao.
* **Ipea renda muito baixa antes de jul/2006** e depois de jul/2026: a serie nao existe; emenda no IPCA em dez/2006 (o pre-registro diz 2007+).
* **PIB per capita nominal de 2025 e 2026**: o Ipeadata GAC_PIBCAPN termina em 2024 (atualizada em 2025-08-20); Lula (3o mandato) usa 2024.
* **IPC suico e DES de set/2026**: SNB e IMF ainda nao publicaram; as linhas deflacionadas em franco e em DES terminam em ago/2026 (o franco nominal vai a set/2026 e o DES nominal a ago/2026).
* **CPI dos EUA de out/2025**: vazio no FRED; sem linha nesse mes (causa nao verificada).
* **Efeito das mudancas de metodo da PTAX, do ouro (jun/2025) e da cesta do DES sobre o nivel das linhas**: nao medi (sem serie sobreposta).
* **Cesta do DES antes de 2016**: nao verifiquei as trocas (euro no lugar de marco e franco, revisoes de 2006 e 2011).
* **Poupanca**: a linha e bruta de imposto e tarifa, na regra antiga (SGS 25); a regra nova esta so como conferencia.
* **Imposto inflacionario**: por pre-registro nao e somado a inflacao e nao e calculado.

## 6. Arquivos

* `series/porquinho.csv` (formato longo linha,ano,mes,valor,unidade,nota,vintage), `series/porquinho_por_governo.csv`, `series/_conferencias.txt`, `quebras.csv` (24 quebras), `manifest.jsonl` e `bruto/`, `baixar.sh` (downloads pela cadeia), `scripts/`.
* Reuso, sem copia: `../inflacao/{ipca-sgs433,inpc-sgs188,igpdi-sgs190}-raw.json` (ate 2025-12), `../inflacao/igpdi-ipeadata-raw.json`, `../poder-de-compra/bruto/ipeadata-{FIPE12_FIPE0001,FIPE12_IPCFIPE12,DIMAC12_INF1}-raw.json`, `../poder-de-compra/series/poder_de_compra.csv` (ICV), `../economia-real/ipeadata-{MTE12_SALMIN12,GAC_PIBCAPN}-raw.json`, `../quebras/bruto/ipeadata-DIEESE12_CBSP12-raw.json`.
