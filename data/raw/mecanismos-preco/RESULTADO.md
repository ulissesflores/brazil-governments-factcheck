# Mecanismos de preço e tarifa: o mesmo instrumento medido em todos os governos

Colheita de 2026-10-19 (dados BCB até 09/2026). Pasta: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mecanismos-preco/`. Sem opinião, sem nota, sem ranking: o que segue é mecanismo, magnitude medida e evidência. A pontuação é fase 2.

## 0. O que mudou o mapa

- A única medida aplicável aos 15 mandatos de 1964-2026 é a diferença entre preços monitorados e livres do IPCA, e ela só existe desde jan/1991 (BCB SGS 11428 e 4449). Sete mandatos inteiros (Castelo Branco, Costa e Silva, Junta, Médici, Geisel, Figueiredo e Sarney) ficam `sem dado` nessa medida. Não reconstruí.
- Nessa medida, a diferença entre anos de monitorados abaixo dos livres e anos de monitorados acima dos livres aparece em governos diferentes. Em 4 dos 8 anos eleitorais federais com série (1994, 2010, 2014, 2022) os monitorados subiram menos que os livres; em 4 (1998, 2002, 2006, 2018) subiram mais. Nos quatro anos eleitorais com monitorados abaixo dos livres, o preço relativo do ano seguinte foi: 1994 para 1995 +5,40%; 2010 para 2011 -0,42% (sem reversão); 2014 para 2015 +8,83%; 2022 para 2023 +5,82%.
- A amostra de mecanismos além dessa medida é **assimétrica por esforço de busca, não por ocorrência**: fui atrás dos casos que o pedido nomeou (2011-2015, combustíveis, energia) e dos congelamentos já colhidos em `historia/`. Os governos de 1964-1985 e de 1990-2010 estão `sem dado` ou `sem achado` em quase todas as classes porque a busca não os cobriu, não porque nada tenha acontecido. A tabela da seção 4 mostra a cobertura.
- O TCU **não julgou o mérito** da política de preços da Petrobras em 2011-2015: o processo foi baixado em diligência para reinstrução e itens do acórdão de 2023 foram declarados insubsistentes. Não existe medida oficial da perda. A única cifra com fonte oficial de dados é o resultado do segmento de derivados da Petrobras, lido pelo Ipea: soma de US$ -41,0 bi em 2011-2014 (resultado contábil, não "subsídio").
- Em 2022 a LC 194 reduziu o ICMS dos estados e o PIS/Cofins/CIDE federal sobre combustíveis; **a conta dos estados foi paga em lei pelo governo seguinte**: LC 201/2023, art. 2º, fixa R$ 27.014.900.000,00 de compensação. Esse é o caso mais limpo de "quem aplica / quem paga" com número e texto legal na mão.

## 1. Entregas

| Arquivo | O que é |
|---|---|
| `mecanismos.csv` | 36 linhas, 17 colunas exatas do pedido. **Desvio de esquema**: `tipo = renuncia_temporaria` em 3 linhas (IPI-AUTO-2009, DESON-IPI-IR-2008-2012, FOLHA-2011-2015) está fora da lista do pedido (ver seção 6). Linhas: 8 de monitorados x livres em ano eleitoral, 6 de congelamento/controle legal, 4 de índice de preços, 5 de Petrobras/CIDE/IPCA administrado/TCU, 3 de energia, 7 de tributo sobre combustível e diesel (inclui a estimativa da Comsefaz como `alegacao`), 3 de renúncia tributária |
| `simetria-por-governo.csv` | 8 classes x 15 governos (120 linhas). `status` só com o vocabulário do pedido: `medido` (24 células) ou `sem dado` (96); `nao_aplicavel` não ocorre (zero células). A distinção fina fica na coluna extra `detalhe`: `instrumento_achado_sem_medida` (9), `nada_achado_nesta_colheita` (20), `nao_colhido` (67) |
| `gap-anual-mandatos.csv` | 36 anos (1991-2026): livres, monitorados, gap em p.p., preço relativo, reversão, ano eleitoral, governo em 31/12 e governos de Y+1 a Y+3 |
| `gap-por-governo.csv` | janela de cada mandato, mês a mês, e os 12 meses seguintes |
| `series/*.csv` | formato longo: gap livres/monitorados (320 linhas), receita da CIDE-combustíveis, gasto tributário da folha, estimativas da Receita por ato, receitas da CDE, resultado de derivados da Petrobras, IPCA de itens administrados |
| `manifest.jsonl` | cadeia de hash (31 linhas; `chain.py verify .` limpo) |
| `calcular-gap.py`, `extrair-series.py`, `montar-tabelas.py`, `ler-xlsx.py` | `python3 -I`, só leem `bruto/` e arquivos locais, sem rede. Ordem: `calcular-gap.py`, `extrair-series.py`, `montar-tabelas.py` |

Nota sobre o manifest: a linha `seq 1` (`bruto/bcb-sgs11428-raw.json`) é uma página HTML de erro do BCB (a consulta sem datas foi recusada). Foi superada pela `seq 3` (`bruto/bcb-sgs11428-livres-raw.json`, com `dataInicial=01/01/1991`). O arquivo antigo fica na cadeia por regra; nada o lê. Os arquivos da Receita têm extensão `.bin` mas são `.xlsx` ou PDF (nome dado no download).

## 2. Diferença entre monitorados e livres (BCB SGS 11428 e 4449)

**Definições**: SGS 11428 = "IPCA - Itens livres"; SGS 4449 = "IPCA - Preços monitorados - Total" (títulos conferidos no catálogo de dados abertos do BCB: `bruto/bcb-dadosabertos-metadados-*.json`). O BCB define monitorados como "aqueles que são direta ou indiretamente determinados pelos governos federal, estadual ou municipal" (Relatório Anual 2015, nota 3). Portanto o grupo inclui decisões de estados, municípios e agências, não só do governo federal.

**Cálculo**: acumulado de 12 variações mensais com 2 casas. Confere com o publicado pelo BCB em até 0,02 p.p. (computado 7,31/1,54, 6,74/5,32, 8,49/18,07 contra publicado 7,29/1,54, 6,72/5,32, 8,51/18,07 para livres/monitorados em 2013-2015). Onde cito o número do BCB uso o publicado; na série uso o computado.

**Regra do ano para governo**: quem estava no cargo em 31/12 (`mandatos.csv`). Duas leituras mecânicas de "quem paga" estão lado a lado (próxima linha do `mandatos.csv` e quem estava no cargo em 31/12 de Y+1, Y+2, Y+3); não escolhi.

**Preço relativo** = (1+monitorados)/(1+livres) − 1. Usei esta medida além do gap em p.p. porque o gap em p.p. não é comparável quando a inflação anual passava de 900% (1991-1994). Negativo = monitorados subiram menos que livres.

### 2.1 Anos eleitorais federais com série

| Ano | Governo em 31/12 | Livres (%) | Monitorados (%) | Gap (p.p.) | Preço relativo (%) | Preço relativo Y+1 (%) | Soma dos 3 anos seguintes (%) |
|---|---|---|---|---|---|---|---|
| 1989 | Sarney | sem dado | sem dado | sem dado | sem dado | sem dado | sem dado |
| 1994 | Itamar | 948,64 | 737,99 | 210,66 | -20,09 | 5,40 | 31,65 |
| 1998 | FHC | 1,33 | 3,24 | -1,91 | 1,89 | 13,66 | 26,47 |
| 2002 | FHC | 11,51 | 15,32 | -3,80 | 3,41 | 5,01 | 12,96 |
| 2006 | Lula 1-2 | 2,56 | 4,28 | -1,72 | 1,68 | -3,85 | -6,80 |
| 2010 | Lula 1-2 | 7,08 | 3,13 | 3,95 | -3,69 | -0,42 | -8,52 |
| 2014 | Dilma | 6,74 | 5,32 | 1,42 | -1,33 | 8,83 | 14,40 |
| 2018 | Temer | 2,90 | 6,18 | -3,28 | 3,18 | 1,61 | 7,73 |
| 2022 | Bolsonaro | 9,37 | -3,83 | 13,20 | -12,07 | 5,82 | 6,92 |

Anos adjacentes de interesse: 2013 (Dilma) gap 5,77 e preço relativo -5,38; 2015 (Dilma) gap -9,58 e preço relativo +8,83; 2021 (Bolsonaro) gap -9,23 e preço relativo +8,57, seguido de 2022 com -12,07.

Leitura mecânica, sem causa: a série não separa o que é decisão do governo federal do que é decisão de estado, município ou agência, nem o que é choque externo. O ano de 1994 mistura hiperinflação e Plano Real (junho a dezembro) e não é comparável aos demais em p.p.

### 2.2 Janela de cada mandato (mês a mês, mês atribuído a quem estava no cargo no dia 15)

| Governo | Janela | Meses | Preço relativo monitorados/livres no mandato (%) | Preço relativo nos 12 meses seguintes (%) |
|---|---|---|---|---|
| Castelo Branco, Costa e Silva, Junta, Médici, Geisel, Figueiredo, Sarney | antes de 1991 | 0 | sem dado | sem dado |
| Collor | 1991-01 a 1992-09 | 21 | 12,22 (início da série corta o mandato) | 3,87 |
| Itamar | 1992-10 a 1994-12 | 27 | -17,04 | 5,40 |
| FHC | 1995-01 a 2002-12 | 96 | 82,74 | 5,01 |
| Lula 1-2 | 2003-01 a 2010-12 | 96 | 3,71 | -0,42 |
| Dilma | 2011-01 a 2016-08 | 68 | -2,92 | 4,94 |
| Temer | 2016-09 a 2018-12 | 28 | 10,37 | 1,61 |
| Bolsonaro | 2019-01 a 2022-12 | 48 | -5,37 | 5,82 |
| Lula 3 | 2023-01 a 2026-09 | 45 | 7,51 | sem dado (mandato em curso) |

## 3. Episódios com instrumento, data, quem aplica, quem paga e magnitude

Camada: `dado` = número ou texto legal de fonte primária; `decisao_de_orgao_de_controle` = TCU, CGU, Aneel; `literatura` = Ipea, CPDOC; `alegacao` = parte interessada. Lista completa e trechos citados em `mecanismos.csv`.

| Id | Instrumento e data | Aplica | Paga | Magnitude e fonte | Camada |
|---|---|---|---|---|---|
| CTL-CIP-1968 | CIP, Decreto 63.196 de 29/08/1968 (data citada no Decreto 91.240/1985; o 63.196 em si não foi baixado) | Costa e Silva | sem dado | sem medida oficial | dado |
| CTL-CRUZADO-1986 | DL 2.283/2.284, congelamento a partir de 27/02/1986 | Sarney | Sarney | sem medida oficial; IPCA mensal nov/86 5,45 e dez/86 11,65 | dado |
| CTL-BRESSER-1987 | DL 2.335, 12/06/1987, 90 dias | Sarney | Sarney | sem medida oficial | dado |
| CTL-VERAO-1989 | Lei 7.730, art. 8º, 14/01/1989, prazo indeterminado | Sarney | Sarney; sucessor Collor (leitura mecânica) | sem medida oficial | dado |
| CTL-COLLOR1-1990 | Lei 8.030 (MP 154, 15/03/1990) vedou reajuste sem autorização | Collor | Collor | sem medida oficial | dado |
| CTL-COLLOR2-1991 | Lei 8.178, art. 1º, preços de 30/01/1991 | Collor | Collor; sucessor Itamar (leitura mecânica) | sem medida oficial | dado |
| IDX-IPC-1987 | IBGE: inflação até 15/06 "represada" no IPC de junho | Sarney | Sarney | IPC de junho captou 35 dias, o de julho 12 | dado |
| IDX-IPC-1989 | IBGE: inflação até 15/01 "represada" no IPC de janeiro | Sarney | Sarney | 51 dias em janeiro, 11 em fevereiro | dado |
| IDX-IPC-1986 | expurgo de supérfluos e do empréstimo compulsório (CPDOC) | Sarney | Sarney | sem medida oficial | literatura |
| IDX-1973 | tabelamento e índice de 1973 (CPDOC) | Médici | sem dado | ICV-FGV 12,6% contra DIEESE 26,1% (citação) | literatura |
| PETRO-2011-2014 | preços de gasolina e diesel na Petrobras | Dilma | Dilma, Temer (reversão 2015-16) | segmento derivados: -5,7; -11,7; -8,2; -15,4 US$ bi (soma -41,0); +5,7 em 2015 e 2016 | literatura (Ipea sobre DFP) |
| PETRO-TCU | TC 030.033/2016-0 | Dilma | sem medida | mérito não julgado | decisão de controle |
| CIDE-2012-2015 | Decreto 7.764 (22/06/2012) zera CIDE; Decreto 8.395 (28/01/2015) restabelece | Dilma | Dilma | receita: 8.924 (2011), 2.736 (2012), 35 (2013), 14 (2014), 3.312 (2015), 5.700 (2016) R$ mi | dado |
| IPCA-ADM-2013-2015 | energia, gasolina, ônibus | Dilma | Dilma | energia residencial -15,65%, +17,06%, +50,99%; gasolina 6,51%, 2,89%, 20,10% | dado |
| ENER-MP579-2012 | MP 579, 11/09/2012 (Lei 12.783/2013); CDE | Dilma | Dilma, consumidores | Uniao na CDE 8.460 (2013) e 11.805 (2014), zero depois; quotas dos consumidores 1.700 (2014) e 18.920 (2015) R$ mi, orçado | controle (CGU) |
| ENER-RTE-2002 | Lei 10.438/2002 art. 4º | FHC | consumidores nos anos seguintes | teto legal 2,9% e 7,9% da tarifa; total em R$ sem medida | dado (texto legal) |
| ENER-COVID-2020 | Conta Covid | Bolsonaro | Bolsonaro e Lula 3 (amortização 2021-2025) | R$ 15,3 bi | controle (Aneel) |
| DIESEL-2018 | Lei 13.723/2018 | Temer | Temer | teto de R$ 9,5 bi; valor pago sem medida | dado (texto legal) |
| DIESEL-2021, LC192-2022, LC194-2022 | Decreto 10.638/2021; LC 192 (11/03/2022); LC 194 (23/06/2022) | Bolsonaro | Bolsonaro; Lula 3 | Receita: 3.001,99; 14.932,41; 16.511,22 R$ mi (ex-ante) | dado |
| LC201-2023 | LC 201, art. 2º | Bolsonaro (LC 194) | Lula 3 | R$ 27.014,9 mi, fixado em lei | dado |
| MP1157-2023 | MP 1.157 e MP 1.163 | Lula 3 | Lula 3 | 25.000 e 6.610 R$ mi (ex-ante, podem se sobrepor) | dado |
| IPI-AUTO-2009 | IPI de automóveis | Lula 1-2 | Lula 1-2 | 1.817 desonerado e 559 de custo no 1º semestre de 2009, R$ mi (Ipea via TCU) | controle |
| FOLHA-2011-2015 | Lei 12.546/2011 | Dilma | Dilma e seguintes | gasto tributário: 22.107,3 (2014), 25.199,1 (2015), 14.546,6 (2016 proj.) R$ mi | dado (Receita) |

## 4. Cobertura da simetria (classe por governo)

`M` = `status` medido. As demais células são `status` = `sem dado`, e a coluna `detalhe` as separa: `I` = `instrumento_achado_sem_medida`; `0?` = `nada_achado_nesta_colheita` (**não é prova de ausência**); `-` = `nao_colhido`. `nao_aplicavel` ficou com zero células: a CIDE só existe desde 2001, mas a classe K6 junta vários tributos, então os governos anteriores ficam `sem dado`.

| Classe | Castelo | C. e Silva | Junta | Médici | Geisel | Figueiredo | Sarney | Collor | Itamar | FHC | Lula 1-2 | Dilma | Temer | Bolsonaro | Lula 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1/K2 monitorados x livres | - | - | - | - | - | - | - | M | M | M | M | M | M | M | M |
| K3 controle legal geral de preços | - | I | - | I | - | - | I | I | 0? | 0? | 0? | 0? | 0? | 0? | 0? |
| K4 represamento ou regra no índice | 0? | 0? | 0? | I | 0? | 0? | I | 0? | 0? | 0? | 0? | 0? | 0? | 0? | 0? |
| K5 preço de combustível na Petrobras | - | - | - | - | - | - | - | - | - | - | - | M | - | - | I |
| K6 redução temporária de tributo sobre combustíveis | - | - | - | - | - | - | - | - | - | - | - | M | I | M | M |
| K7 tarifa de energia diferida ou subsidiada | - | - | - | - | - | - | - | - | - | I | - | M | - | M | - |
| K8 desoneração setorial temporária | - | - | - | - | - | - | - | - | - | - | M | M | - | - | - |

Como ler: só K1/K2 é aplicável com a mesma regra a todos os governos a partir de 1991. As demais classes foram colhidas onde a pergunta apontou, então uma coluna cheia de `-` não diz que o governo não fez; diz que a colheita não chegou lá. Qualquer pontuação que conte `M` por governo mede o esforço de busca e não o comportamento.

## 5. O que NÃO achei

- Decomposição livres/monitorados antes de jan/1991. O IPCA começa em 1980 e o BCB não publica os dois grupos antes de 1991 nas séries usadas. O catálogo do Ipeadata lista séries espelho (BM12_IPCAPL12 e BM12_IPCAPM12); o início delas não foi verificado e não foram usadas. Nenhum IPC/IGP de antes do Real foi decomposto.
- Número oficial da perda da Petrobras com preços 2011-2014 (TCU sem mérito; sem linha de "subsídio" nas demonstrações). Estimativas de analistas e da imprensa (US$ 41 bi do Ipea é segmento contábil; R$ 55 bi do CBIE e R$ 104 bi do estudo da UFRJ apareceram só em resultados de busca, não foram lidos nas fontes) **não estão na tabela**.
- Estimativa de órgão oficial (STN, Receita, TCU, Congresso, IFI) da perda de ICMS dos estados com a LC 194. Só há (a) a compensação fixada em lei, R$ 27,0 bi, e (b) a estimativa da Comsefaz (R$ 102 a 109 bi em 12 meses; R$ 45 bi de perda observada no período), que é parte interessada e está como `alegacao`.
- Custo realizado da subvenção ao diesel de 2018 (só o teto de R$ 9,5 bi) e a estimativa da Receita para a redução de CIDE/PIS/Cofins do mesmo pacote: a série "Desonerações Instituídas" da Receita começa em 2019.
- IPI de automóveis em 2012-2014 (Regime Automotivo/Inovar-Auto) com valor próprio; o DGT da Receita disponível começa em 2014 e a série 2012-2013 não está na página. O número do Dilma que existe é o agregado de IR+IPI do TCU (2011: R$ 77,2 bi; 2012: R$ 85,2 bi de desoneração bruta), que mistura renúncias permanentes e temporárias.
- Compensação do Tesouro à Previdência pela desoneração da folha; reoneração de 2015 (Leis 13.161 e 13.202 só citadas pela Receita).
- Revisão tarifária extraordinária da Aneel em 2015 (média de 23,4% em imprensa); não li o ato.
- Conselho Interministerial de Preços: nenhum dado de preço tabelado ou custo. CONEP de 1965 só apareceu em resumo de busca.
- Atos da gestão Lula 3 além de 2023 (fim da redução de PIS/Cofins sobre combustíveis, tributação de combustíveis em 2024-2026): o BCB e o Ipeadata trazem a série até set/2026, mas não li o texto legal de nada depois de 2023.
- Petrobras 2016-2022 (política de paridade): resultado de derivados 2017 em diante só tem o 1º semestre de 2017 na tabela do Ipea; o resto não foi colhido.

## 6. Pontos de método e riscos

- Tipo `renuncia_temporaria` em 3 linhas (IPI automóveis 2009, desoneração IR+IPI 2008-2012, folha 2011-2015): a lista de tipos do pedido não tem rótulo para renúncia tributária; preferi um rótulo fora da lista a encaixar errado em "antecipação de receita".
- ENER-RTE-2002 e ENER-COVID-2020 não são represamento de preço no sentido estrito: são diferimento de custo para tarifas futuras, por choque de oferta (2001) e pandemia (2020). Estão marcados `adiamento_de_despesa` e com nota.
- As estimativas da Receita nas planilhas "Desonerações Instituídas" são ex-ante, por ato, por ano de vigência; não são arrecadação observada e se sobrepõem entre atos. Em LC194-2022 a planilha traz R$ 18.616 mi para 2023 com prazo até 31/12/2022 e não explica.
- Valores de CDE (CGU, Tabela 1) são orçados, não executados.
- O "preço relativo" de 1991-1994 usa acumulados anuais com milhares de por cento; é aritmeticamente correto e pouco informativo como magnitude.
- Cópias de acórdãos do TCU e do voto da Aneel foram baixadas de hospedagem do Poder360 e do MPC-ES (as páginas oficiais não deram link direto estável). Conferir no portal do TCU e da Aneel antes de citar o número do acórdão.
- A busca (WebSearch) foi usada para achar a fonte primária, nunca como fonte do número. Onde só o resumo da busca existia, o item foi para `NAO achei` ou para `alegacao`.
