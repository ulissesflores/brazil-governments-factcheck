# Economia real: PIB, desemprego e salário mínimo real contra o infográfico

Bloco: PIB, desemprego, salário mínimo real. Colheita de 2026-10-19. Sem opinião política: só reprodução de números.

Legenda: ✅ reproduz (|dif| <= 0,05 p.p., ou 0,1 em salário mínimo) | ⚠️ aproximado (dentro de 0,3 p.p. ou 5% relativo) | ❌ não reproduz | ❓ não consegui verificar.

Tudo aqui sai de `python3 -I recalcula.py` (lê só os brutos desta pasta, sem rede). A saída integral, com as séries anuais completas e as varreduras, está em `saida-recalcula.txt` e nos três `saida-*.csv`. Os brutos têm hash encadeado em `manifest.jsonl` (`python3 ../manifest_tool.py verify .` devolve 43 linhas, OK, cabeça `cd46053901d57a6f8694879e882ca5178c4e3080a4adc80cb336f2638c33470b` no momento da escrita).

> [!IMPORTANT]
> Resumo curto: no PIB, Médici reproduz (✅, só na média geométrica) e FHC, Lula 1-2 e Lula 3 aproximam (⚠️). PIB de Itamar, Dilma, Temer e Bolsonaro não fecha com média anual. Desemprego: só Temer aproxima (⚠️); Itamar, FHC, Lula 1-2, Dilma, Bolsonaro e Lula 3 não reproduzem (❌) e 1968-73 não tem série oficial (❓). Salário mínimo real: nenhum dos oito números fecha com convenção natural, só Lula 1-2 aproxima.

## 1. Fontes (série, código, URL, atualização na fonte, download)

Downloads de 2026-10-19, entre 13:15 e 13:21 (America/Sao_Paulo; no manifest o timestamp é o mtime do arquivo, marcado "metadata reconstruida", porque foram baixados antes do protocolo de hash). Os arquivos baixados depois do protocolo (SGS 24369, SIDRA 4099 e metadados SIDRA) têm timestamp e HTTP 200 reais no manifest. A coluna "atualização" é o `SERATUALIZACAO` do catálogo Ipeadata (`meta/ipeadata-Metadados-catalogo-completo-raw.json`, 4071 séries).

| uso | série (código) | URL do dado bruto | atualização na fonte | arquivo bruto |
|---|---|---|---|---|
| PIB real, var. anual 1901-2025 | Ipeadata `SCN10_PIBG10` (IBGE/SCN anual) | http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='SCN10_PIBG10') | 2026-07-10 | `ipeadata-SCN10_PIBG10-raw.json` |
| PIB real, índice 2010=100 | Ipeadata `SCN10_PIB10` | idem, SERCODIGO='SCN10_PIB10' | 2026-07-10 | `ipeadata-SCN10_PIB10-raw.json` |
| PIB real 1997-2025 (conferência) | Ipeadata `PAN_PIBPMG` | idem | 2026-03-10 | `ipeadata-PAN_PIBPMG-raw.json` |
| PIB trimestral dessazonalizado, base média 1995=100, 1996T1-2026T2 | Ipeadata `SCN104_PIBPMAS104` (IBGE/SCN trimestral) | idem | 2026-09-30 | `ipeadata-SCN104_PIBPMAS104-raw.json` |
| conferência do PIB | BCB SGS 7326 | https://api.bcb.gov.br/dados/serie/bcdata.sgs.7326/dados?formato=json | n/d | `bcb-sgs7326-pib-var-real-anual-raw.json` |
| PIB e PIB per capita, volume, 1996-2023 | IBGE SIDRA tabela 6784, variáveis 9810, 9814, 93, 9808 | https://servicodados.ibge.gov.br/api/v3/agregados/6784/periodos/1996-2023/variaveis/9810\|9814\|93\|9808?localidades=N1[all] | n/d | `sidra-t6784-pib-percapita-raw.json` |
| IBC-Br (proxy de atividade) | BCB SGS 24364 | https://api.bcb.gov.br/dados/serie/bcdata.sgs.24364/dados?formato=json | n/d | `bcb-sgs24364-raw.json` |
| população, censos | Ipeadata `POPTOT` (IBGE, decenal) | idem | 2026-03-05 | `ipeadata-POPTOT-raw.json` |
| população anual 1872-2024 (usada no per capita derivado) | Ipeadata `DEPIS_POP` (IBGE/Pop) | idem | 2025-08-21 | `ipeadata-DEPIS_POP-raw.json` |
| população, projeção 1980-2070 (2025 e sensibilidade) | Ipeadata `POP_PROJE` (IBGE, revisão 2024) | idem | 2024-09-23 | `ipeadata-POP_PROJE-raw.json` |
| baixados e não usados no cálculo | `GAC_PIBCAPN` (PIB per capita em R$ nominais, Ipea, 2025-08-20; não é real); `DEPIS_POPP` (projeção 2022-2070, redundante); `SCN104_PIBPMG104` (trimestral s/ ajuste, redundante com o dessazonalizado) | idem | - | `ipeadata-GAC_PIBCAPN-raw.json`, `ipeadata-DEPIS_POPP-raw.json`, `ipeadata-SCN104_PIBPMG104-raw.json` |
| desemprego, PME antiga | Ipeadata `PME12_TDA12` | idem | 2003-02-18 | `ipeadata-PME12_TDA12-raw.json` |
| desemprego, PME nova | Ipeadata `PAN12_TD12` | idem | 2016-02-02 | `ipeadata-PAN12_TD12-raw.json` |
| desemprego, PNAD anual | Ipeadata `Dese_Pnad` (IBGE) e `DISOC_DESE` (Ipea/Disoc) | idem | 2015-11-17 e 2016-01-06 | `ipeadata-Dese_Pnad-raw.json`, `ipeadata-DISOC_DESE-raw.json` |
| desemprego, PNAD Contínua anual | IBGE SIDRA tabela 4562, variável 4099 | https://servicodados.ibge.gov.br/api/v3/agregados/4562/periodos/2012-2025/variaveis/4099?localidades=N1[all] | n/d | `sidra-pnadc-anual-t4562-raw.json` |
| desemprego, PNAD Contínua trimestral | IBGE SIDRA tabela 4099, variável 4099 | https://servicodados.ibge.gov.br/api/v3/agregados/4099/periodos/201201-202602/variaveis/4099?localidades=N1[all] | n/d | `sidra-pnadc-trimestral-t4099-raw.json` |
| desemprego, trimestre móvel | BCB SGS 24369 | https://api.bcb.gov.br/dados/serie/bcdata.sgs.24369/dados?formato=json | n/d | `bcb-sgs24369-pnadc-trimestre-movel-raw.json` |
| desemprego PNADC, média dos meses | Ipeadata `PAN_TDESOC` | idem | 2026-01-30 | `ipeadata-PAN_TDESOC-raw.json` |
| PME por região metropolitana (não usada no headline) | SIDRA 13, 14 e 2179 | https://servicodados.ibge.gov.br/api/v3/agregados/{13,14,2179}/... | n/d | `sidra-pme-*-raw.json` |
| salário mínimo real | Ipeadata `GAC12_SALMINRE12` (Ipea) | idem | 2026-10-09 | `ipeadata-GAC12_SALMINRE12-raw.json` |
| salário mínimo nominal | Ipeadata `MTE12_SALMIN12` | idem | 2025-06-30 | `ipeadata-MTE12_SALMIN12-raw.json` |
| deflatores alternativos | Ipeadata `IGP12_IGPDI12`; BCB SGS 433 (IPCA); SGS 188 (INPC) | https://api.bcb.gov.br/dados/serie/bcdata.sgs.{433,188}/dados?formato=json | IGP-DI 2026-10-09 | `ipeadata-IGP12_IGPDI12-raw.json`, `bcb-sgs433-raw.json`, `bcb-sgs188-raw.json` |

Os códigos Ipeadata foram confirmados no catálogo oficial da própria API (`/Metadados`, 4071 séries), nome e fonte batendo com o uso. O filtro OData `$filter` foi rejeitado pela API, então o catálogo foi baixado inteiro. O código SGS 7326 **não foi confirmado numa página de catálogo do BCB** (a página do portal de dados abertos devolveu 404 e a API CKAN devolveu não-JSON); a identidade da série foi aferida de outra forma: bate com `SCN10_PIBG10` ano a ano, de 1963 a 2025, sem nenhuma diferença acima de 0,05 p.p. Isso é conferência, não prova de nome.

Vintage do PIB, segundo o comentário da própria série `SCN10_PIBG10`: 1948-1990 Contas Nacionais Consolidadas; 1991-1995 SCN referência 1985; 1996-2000 estimado a partir das Contas Trimestrais referência 2010; 2001 em diante SCN referência 2010. Costura de metodologias dentro da mesma série.

## 2. PIB

### 2.1 Método

- Média aritmética = média das taxas anuais de `SCN10_PIBG10` na janela, anos-calendário inclusivos. Geométrica = produto das taxas elevado a 1/n. (O índice `SCN10_PIB10` difere da taxa só em 2024, 3,396% contra 3,419%; o script usa sempre a taxa.)
- Conferências: SGS 7326 contra `SCN10_PIBG10` sem diferença acima de 0,05 p.p. (1963-2025); SIDRA 9810 (arredondada a 0,1) difere de `SCN10_PIBG10` só em 2018 (1,78 contra 1,7) e 2019 (1,22 contra 1,3), efeito de vintage.
- PIB per capita real: **oficial** (SIDRA 6784, variável 9814, 1996-2023, arredondado a 0,1); fora disso **derivado** como (1+PIB real)/(1+crescimento da população)-1, vale para 1948-1995 e 2024-2025. População = Ipeadata `DEPIS_POP` (IBGE/Pop, série anual 1872-2024, ancorada nos censos), e 2025 = 2024 multiplicado pelo crescimento 2024-25 de `POP_PROJE`. Sensibilidades medidas pelo script: trocar `DEPIS_POP` por interpolação log-linear dos censos (`POPTOT`) antes de 1980 muda o crescimento per capita anual em no máximo 0,46 p.p. (nível da população até 0,8%); trocar por `POP_PROJE` (projeção rev. 2024, 1980+) muda em até 1,65 p.p., por causa de um salto de 3,5% em 1999-2000 que só a projeção tem. O derivado com `DEPIS_POP` fica a no máximo 0,77 p.p. do oficial 9814 em 1996-2023 (o SIDRA usa população de revisão anterior).
- Janela exata do mandato (posse-saída): só de 1996 em diante, com o índice trimestral dessazonalizado. Cada trimestre vira o dia 15 do mês central, interpolação log-linear no tempo, taxa anualizada ponta a ponta. Dilma até 31/08/2016, Temer a partir de 01/09/2016 (como no briefing; o afastamento provisório de 12/05/2016 não é usado). Antes de 1996 não há PIB trimestral nesta série: só anos-calendário. Não reconstruí as datas de posse de 1964-1990, o recorte anual não as resolve.

### 2.2 Infográfico contra reproduzido (janela do infográfico, anos-calendário)

| coluna | infográfico | aritmética | geométrica | status | observação |
|---|---|---|---|---|---|
| Médici (1968-1973) | 11,1 | 11,159 | 11,148 | ✅ | geométrica 11,148 (dif 0,048); a aritmética, 11,159, já daria ⚠️; o rótulo "1967-1974" não corresponde à janela usada (1967-1974 daria 9,9) |
| Itamar (1992-1994) | 2,5 | 3,41 | 3,37 | ❌ | 1992 = -0,54, 1993 = 4,92, 1994 = 5,85; nenhuma variante de ±1-2 anos nas pontas fecha |
| FHC (1995-2002) | 2,3 | 2,43 | 2,42 | ⚠️ | dif 0,13; 1995-2001 daria 2,34 |
| Lula 1-2 (2003-2010) | 4,0 | 4,079 | 4,051 | ⚠️ | geométrica 4,051 (dif 0,051): passa raspando do limite de ✅ |
| Dilma (2011-2016) | 1,4 | 0,43 | 0,39 | ❌ | 2011-2015 = 1,17; só uma janela 2010-2016 chega a 1,44 (aritmética), hipótese de recorte, não achado |
| Temer (2016-2018) | 0,7 | -0,06 | -0,08 | ❌ | 2017-2018 = 1,55 |
| Bolsonaro (2019-2022) | 1,8 | 1,43 | 1,39 | ❌ | por média anual; ponta a ponta trimestral dá 1,77 (tabela 2.3), ver nota |
| Lula 3* (2023-2025) | 2,9 | 2,98 | 2,98 | ⚠️ | 2025 vem de estimativa preliminar do IBGE; dif 0,08 |

Nota Bolsonaro: o infográfico diz "médio anual". Com média das taxas anuais (que é a definição de média anual) o resultado é 1,43/1,39. Com a taxa anualizada ponta a ponta do índice dessazonalizado (4T2018 a 4T2022) sai 1,77, que coincide com 1,8. Isso é coincidência numérica de método diferente; não prova que esse foi o método usado, e o mesmo método não reproduz Dilma nem Temer.

### 2.3 Janela exata do mandato (taxa anualizada ponta a ponta, índice trimestral dessazonalizado; IBC-Br como proxy)

| mandato | início | fim | anos | PIB trimestral % a.a. | IBC-Br % a.a. (proxy, não é PIB) |
|---|---|---|---|---|---|
| Dilma | 2011-01-01 | 2016-08-31 | 5,67 | -0,10 | -0,65 |
| Temer | 2016-09-01 | 2018-12-31 | 2,33 | 1,68 | 1,71 |
| Bolsonaro | 2019-01-01 | 2022-12-31 | 4,00 | 1,77 | 0,87 |
| Lula 1-2 | 2003-01-01 | 2010-12-31 | 8,00 | 4,21 | n/d |
| Dilma, janela civil | 2011-01-01 | 2016-12-31 | 6,00 | -0,02 | - |
| Temer, janela civil | 2016-01-01 | 2018-12-31 | 3,00 | 0,97 | - |
| FHC, só 15/02/1996-31/12/2002 | 1996-02-15 | 2002-12-31 | 6,88 | 2,49 | - |
| Lula 3, janela civil | 2023-01-01 | 2025-12-31 | 3,00 | 2,62 | - |

Para a média aritmética de janela exata (fração de ano), não há definição única; só reporto a taxa anualizada. A fronteira de 31/08/2016 cai no meio do 3T2016, por isso a interpolação é aproximação.

### 2.4 PIB per capita real e o que o infográfico omitiu

PIB per capita não aparece no infográfico; entrego como pedido. "final" = oficial 9814 onde existe, derivado com `DEPIS_POP` nos demais anos.

| janela | PIB aritm. | PIB geom. | per capita aritm. | per capita geom. | anuais (PIB %) |
|---|---|---|---|---|---|
| Castelo Branco 1964-1966 | 4,17 | 4,15 | 1,24 | 1,22 | 3,4; 2,4; 6,7 |
| Costa e Silva+Médici 1967-1973 | 10,16 | 10,13 | 7,29 | 7,25 | 4,2; 9,8; 9,5; 10,4; 11,3; 11,9; 14,0 |
| Costa e Silva+Médici 1967-1974 (período declarado) | 9,91 | 9,88 | 7,06 | 7,03 | idem + 8,2 |
| Geisel 1974-1978 | 6,70 | 6,67 | 4,14 | 4,11 | 8,2; 5,2; 10,3; 4,9; 5,0 |
| Figueiredo 1979-1984 | 2,50 | 2,38 | 0,22 | 0,10 | 6,8; 9,2; -4,2; 0,8; -2,9; 5,4 |
| Geisel+Figueiredo 1974-1985 (como pedido) | 4,70 | 4,60 | 2,30 | 2,21 | inclui 1985 = 7,8 |
| Sarney 1985-1989 (anos-calendário do mandato mar/85-mar/90) | 4,39 | 4,35 | 2,47 | 2,44 | 7,8; 7,5; 3,5; -0,1; 3,2 |
| Sarney 1985-1990 (como pedido) | 2,94 | 2,85 | 1,10 | 1,02 | inclui 1990 = -4,3 |
| Collor 1990-1992 (como pedido) | -1,29 | -1,31 | -2,63 | -2,66 | -4,3; 1,0; -0,5 |
| Collor+Itamar 1990-1994 | 1,38 | 1,31 | 0,06 | -0,01 | |
| Itamar 1993-1994 (anos plenos) | 5,39 | 5,39 | 4,10 | 4,10 | 4,9; 5,9 |
| 1964-1985 inteiro | 6,36 | 6,27 | 3,74 | 3,65 | |

Per capita das janelas do infográfico (aritm./geom.): Médici 8,28/8,26; Itamar 2,14/2,10; FHC 0,92/0,91; Lula 1-2 3,01/2,98; Dilma -0,35/-0,39; Temer -0,80/-0,83; Bolsonaro 0,90/0,85; Lula 3 2,56/2,55.

### 2.5 Série anual 1948-2025

Em `saida-pib-anual-1948-2025.csv`: PIB real (`SCN10_PIBG10`), PIB per capita final e derivado puro, SIDRA 9810/9814 e SGS 7326 lado a lado, com a origem de cada ano de per capita marcada.

## 3. Desemprego

### 3.1 Séries oficiais e metodologia (nunca emendadas numa linha só)

| série | código | período | abrangência e definição | primeira observação |
|---|---|---|---|---|
| PME antiga | Ipeadata `PME12_TDA12` (IBGE) | 1980-01 a 2002-12, mensal | 6 regiões metropolitanas (Recife, Salvador, Belo Horizonte, Rio, São Paulo, Porto Alegre); 15+ anos; desemprego aberto, referência de 30 dias. Comentário da série: 1982-1989 vêm da publicação "PME: estatísticas básicas, séries retrospectivas, n. 1", IBGE 1990 | 1980-01 |
| PME nova | Ipeadata `PAN12_TD12` (IBGE) | 2002-03 a 2015-12, mensal | mesmas 6 RMs; 10+ anos; desocupação na semana de referência. PME encerrada em março de 2016 | 2002-03 |
| PNAD anual | Ipeadata `Dese_Pnad` (IBGE) e `DISOC_DESE` (Ipea/Disoc, microdados), Brasil | 1992-2014 | 10+ anos; semana de referência (setembro). Lacunas: 1994, 2000, 2010 (e antes de 1992 não há nada no Ipeadata). Tem diferença de 0,01-0,02 p.p. entre as duas séries | 1992 |
| PNAD Contínua anual | SIDRA 4562 (var. 4099) | 2012-2025 | 14+ anos; semana de referência; média dos 4 trimestres | 2012 |
| PNAD Contínua, média dos meses | Ipeadata `PAN_TDESOC` | 2013-2025 | média anual da série mensal de trimestres móveis; difere do SIDRA em até 0,4 p.p. | 2013 |

Nota sobre a PNAD anual: cobertura nacional sem a zona rural da região Norte (exceto Tocantins) até 2003 é fato metodológico conhecido do IBGE, **não verificado nesta colheita**.

O catálogo SIDRA tem as tabelas 13 e 14 (PME antiga, 1991-2002) e 2179 (PME nova, 2002-2016), mas só por região metropolitana; não há agregado das 6 RMs no SIDRA. O headline usa o agregado do Ipeadata.

### 3.2 A quebra de metodologia PME antiga para PME nova, medida

Meses em que as duas séries coexistem (2002-03 a 2002-12):

| mês | PME antiga % | PME nova % | diferença p.p. |
|---|---|---|---|
| 2002-03 | 7,76 | 12,9 | 5,1 |
| 2002-06 | 8,27 | 11,6 | 3,3 |
| 2002-09 | 8,26 | 11,5 | 3,2 |
| 2002-12 | 6,17 | 10,5 | 4,3 |

Média da diferença nos 10 meses: cerca de 3,6 p.p. Qualquer linha que passe de 2002 para 2003 sem marcar a quebra mistura um salto metodológico de ~3-4 p.p. com variação real.

### 3.3 1968-1973: existe série oficial?

**Não encontrei, e a evidência é negativa.** A observação mais antiga de qualquer série de desemprego baixada é 1980-01 (PME antiga). Nenhuma das cinco séries cobre 1968-1973. Revisei o catálogo Ipeadata inteiro (4071 séries) pelos nomes "desemprego", "desocupação", "PME", "PNAD": nada antes de 1980 em nível nacional, e a PNAD anual só começa em 1992 no Ipeadata. O SIDRA lista PME desde 1991. Isto prova ausência *nas fontes que consultei*, não que o IBGE nunca tenha tabulado. A PME nasceu em 1980 em seis RMs. A PNAD nacional existe desde 1981 (1980 foi substituída pelo Censo, segundo a busca web que fiz, não verificada em fonte primária); eu **não** tenho os números de 1981-1990 da PNAD, e o IBGE publica tabelas desses anos nos volumes da PNAD, que não localizei em formato legível.

Origem do "3,7%": **❓ não encontrada**. Hipóteses que NÃO verifiquei como origem:
- um resultado de PME do fim dos anos 1980 em outra definição: uma busca web trouxe, de um trecho do relatório PME de dez/1991 do IBGE (PDF escaneado, que não consegui ler: https://biblioteca.ibge.gov.br/visualizacao/periodicos/231/pme_1991_dez.pdf), médias anuais de 3,59 (1986), 3,73 (1987), 3,85 (1988), 3,35 (1989), 4,28 (1990). 3,73 existe, mas é de 1987 e vem de um trecho de busca, não do documento aberto. A série do Ipeadata (30 dias) dá 3,99, 4,08, 4,18, 3,64, 4,65 para esses anos, ou seja, definição e vintage mudam o número em 0,3-0,5 p.p.;
- uma taxa de Censo 1970, uma rodada piloto de PNAD ou uma compilação secundária: possibilidades listadas, nenhuma checada.

### 3.4 Médias da janela do infográfico em cada metodologia

Colunas lado a lado, cada uma é uma metodologia distinta (marcadas para o leitor; não são comparáveis entre si):

| janela | infográfico | PME antiga | PME nova | PNAD (Dese_Pnad) | PNADC SIDRA |
|---|---|---|---|---|---|
| Itamar 1992-1994 | 6,8 | 5,78 | n/d | 7,00 (só 1992-93; falta 1994) | n/d |
| FHC 1995-2002 | 7,7 | 7,01 | n/d | 8,97 (falta 2000) | n/d |
| Lula 2003-2010 | 8,4 -> 6,5 | n/d | 9,46 (média) | 9,33 (média sem 2010) | n/d |
| Dilma 2011-2016 | 6,7 | n/d | 5,70 (só 2011-15) | 7,18 (só 2011-14) | 8,44 (só 2012-16) |
| Temer 2016-2018 | 12,3 | n/d | n/d | n/d | 12,10 |
| Bolsonaro 2019-2022 | 13,2 | n/d | n/d | n/d | 12,28 |
| Lula 3* 2023-2025 | 9,3 | n/d | n/d | n/d | 6,63 |
| Ditadura 1968-1973 | 3,7 | n/d | n/d | n/d | n/d |

### 3.5 Infográfico contra reproduzido

| coluna | infográfico | melhor reprodução | status | observação |
|---|---|---|---|---|
| Itamar 1992-1994 | 6,8 | PME antiga 1992-94: 5,78 (janela completa) | ❌ | PNAD só tem 1992 e 1993 (média 7,00, dif 0,2, mas janela incompleta: falta 1994); 6,80 é o valor isolado da PNAD de 1993, coincidência de ano único |
| FHC 1995-2002 | 7,7 | PME antiga 7,01 | ❌ | PNAD (sem 2000) dá 8,97; nenhuma recorte de ±1 ano dá 7,7 |
| Lula 8,4 -> 6,5 | 8,4 e 6,5 | ponta final: PME nova 2010 = 6,73 | ❌ | 8,4 não aparece em nenhuma série; PME nova 2003 = 12,33, PNAD 2003 = 10,47, mensal PME nova dez/2003 = 10,9 e dez/2010 = 5,3 |
| Dilma 2011-2016 | 6,7 | nenhuma média de janela | ❌ | PNAD 2012 = 6,72 e PME nova 2010 = 6,73 são anos isolados que coincidem; média PNADC 2012-2016 = 8,44 |
| Temer 2016-2018 | 12,3 | PNADC 2016-18: 12,10; 2017-18: 12,35 | ⚠️ | dif 0,2 na janela do mandato |
| Bolsonaro 2019-2022 | 13,2 "(pico 2019-2020)" | PNADC 2019-2022: 12,28 | ❌ | pico trimestral é 14,9 (3T2020 e 1T2021), anual 2020 = 13,7, 2021 = 14,0; 13,17 aparece só como média 2019-2021 (janela fora do mandato); 13,2 existe como trimestre móvel jun-ago/2021 (SGS 24369) |
| Lula 3* 2023-2025 | 9,3 | PNADC 2023-25: 6,63 | ❌ | pico trimestral do período é 8,8 (1T2023); 9,3 aparece como trimestre móvel de abr-jun/2022 (SGS 24369), ou seja, antes do mandato: hipótese de origem, não achado |
| Ditadura 1968-1973 | 3,7 | sem série | ❓ | ver 3.3 |

## 4. Salário mínimo real

### 4.1 Série e deflator

`GAC12_SALMINRE12` (Ipea), mensal, R$ constantes do último mês (hoje set/2026 = R$ 1.621,00). Deflator, conforme o comentário da própria série: IPC-SP/Fipe até jan/1944; IPC-RJ/FGV jan/1944-jan/1948; IGPC-Mtb jan/1948-mar/1979; INPC de abr/1979 em diante; a variação do deflator de jul/1994 multiplicada por 1,2225 por causa da troca de moeda. Antes de 1984, o valor é o maior mínimo vigente no país (havia faixas por região). Verifiquei o deflator de 1979 em diante: nominal `MTE12_SALMIN12` dividido pelo INPC acumulado (SGS 188) reproduz a razão da série do Ipeadata dentro de 0,01% em todos os intervalos testados fora de jul/1994 (o cruzamento de jan/1994 a jan/1995, que atravessa jul/1994, dá 0,7924 no Ipeadata e 0,7923 com o INPC do SGS 188 sem nenhum fator; aplicando o 1,2225 do comentário sobre esse INPC sai 0,6481, que não fecha. Não investiguei a razão; hipótese: o SGS 188 já traz a variação de jul/1994 compatível com a série do Ipea).

O infográfico não diz que convenção de pontas usa. Testei cinco: dez(a-1)->dez(b), dez(a)->dez(b), média(a-1)->média(b), média(a)->média(b), jan(a)->dez(b). Em alta inflação (1992-94) a série mensal oscila muito (1993: mínimo 482, máximo 734 no mesmo ano), então as pontas decidem o sinal.

### 4.2 Infográfico contra reproduzido (variação % real; Ipeadata `GAC12_SALMINRE12`)

| janela | infográfico | dez(a-1)->dez(b) | dez(a)->dez(b) | média(a-1)->média(b) | média(a)->média(b) | jan(a)->dez(b) | status |
|---|---|---|---|---|---|---|---|
| Ditadura 1968-1973 | 42,8 | 0,3 | 1,4 | -3,3 | -3,4 | 3,1 | ❌ |
| Itamar 1992-1994 | -13,9 | 37,7 | 38,3 | 6,1 | -1,8 | -24,2 | ❌ |
| FHC 1995-2002 | 4,8 | 40,0 | 19,6 | 47,0 | 29,9 | 42,1 | ❌ |
| Lula 2003-2010 | 58,5 | 62,4 | 49,4 | 57,3 | 56,2 | 66,4 | ⚠️ |
| Dilma 2011-2016 | 8,0 | 15,2 | 14,3 | 13,9 | 13,8 | 9,8 | ❌ |
| Temer 2016-2018 | 1,1 | 7,6 | 2,7 | 4,5 | 2,3 | -2,2 | ❌ |
| Bolsonaro 2019-2022 | 0,9 | -1,2 | -1,3 | -0,9 | -1,7 | -5,2 | ❌ |
| Lula 3* 2023-2025 | 12,6 | 10,9 | 5,6 | 10,4 | 6,0 | 3,8 | ❌ |

⚠️ de Lula 1-2 só nas convenções de média anual (57,3 e 56,2 contra 58,5, 2%-4% relativos). Tolerância: ⚠️ = 0,3 p.p. ou 5% relativo (regra do briefing); ✅ = 0,1 p.p. Nenhum veredito muda se a tolerância absoluta fosse 1,0 p.p.: o caso mais próximo (Temer, 2,3 contra 1,1) fica a 1,2 p.p.

Robustez ao deflator (nominal `MTE12_SALMIN12` deflacionado por outros índices, dez(a-1)->dez(b)): IGP-DI dá 4,2 (Médici), 8,7 (Itamar), 13,3 (FHC), 55,7 (Lula 1-2), 17,0 (Dilma), 5,9 (Temer), -22,5 (Bolsonaro; IGP-DI disparou em 2020-21), 22,7 (Lula 3). IPCA dá 43,5, 42,4, 62,8, 15,5, 6,6, 0,1 e 9,5 de Itamar a Lula 3. Troca de deflator mexe nos números por vários pontos e não fecha os do infográfico (a coincidência mais próxima, Bolsonaro com IPCA, dá +0,1 contra 0,9, ainda ❌).

Varredura de coincidência (mensal exaustiva, Ipeadata real, início em a-1..a, fim em b..b+1; 576 pares por janela): Médici 0 acertos, FHC 0, Lula 1-2 0, Dilma 0, Itamar 2 (1991-02 a 1995-04; 1992-10 a 1995-03, ambos com ponta final fora do mandato), Temer 13, Bolsonaro 13, Lula 3 9. Para as janelas com mais de uma dezena de acertos o número de pares testados é alto e as pontas não são as do mandato; leio como ruído, não como método encontrado.

Se a coluna fosse a média aritmética das variações anuais da média anual (em vez de variação acumulada): 1995-2002 daria 5,0 (infográfico 4,8, ⚠️), mas as outras colunas, como 2003-2010 (5,9 contra 58,5), mostram que o infográfico não usa esse critério de modo consistente.

### 4.3 O que o infográfico omitiu (variação % real)

| janela | dez(a-1)->dez(b) | dez(a)->dez(b) | média(a-1)->média(b) | média(a)->média(b) | jan(a)->dez(b) |
|---|---|---|---|---|---|
| Castelo Branco 1964-1966 | -8,6 | -20,9 | -16,1 | -25,2 | -1,3 |
| Ditadura 1964-1985 | -6,9 | -19,4 | -32,1 | -39,5 | 0,5 |
| Geisel 1974-1978 | 0,1 | -1,1 | 3,6 | 6,0 | 1,5 |
| Figueiredo 1979-1984 | -5,0 | -14,6 | -16,1 | -15,7 | 0,5 |
| Sarney 1985-1989 | -17,4 | -22,3 | -9,1 | -12,4 | -7,7 |
| Sarney 1985-1990 (como pedido) | -45,1 | -48,3 | -31,8 | -34,2 | -38,6 |
| 1985-1992 (como pedido) | -54,8 | -57,5 | -30,1 | -32,6 | -49,5 |
| Collor 1990-1992 | -45,3 | -17,7 | -23,1 | 2,5 | -43,5 |
| Costa e Silva+Médici 1967-1973 | 0,8 | 0,3 | -10,2 | -3,3 | 3,7 |

Com IGP-DI como deflator alternativo (dez/dez): 1964-1985 = -8,4 (Ipeadata real -6,9); 1985-1992 = -55,4 (-54,8); 1967-1973 = 4,2 (0,8); 1968-1973 = 4,2 (0,3). Sinal e ordem de grandeza se mantêm; nenhuma convenção testada leva 1968-1973 a perto de +42,8%. A série anual completa da média e do dezembro está em `saida-salmin-real-anual.csv`.

## 5. Não encontrado, não verificado, limites

- Série oficial de desemprego para 1968-1973: não encontrada em nenhuma fonte consultada (primeira observação 1980-01). Origem do 3,7%: ❓.
- PNAD 1981-1991: existe na publicação do IBGE; não obtive em formato legível. O Ipeadata só tem PNAD anual de 1992 em diante, sem 1994, 2000 e 2010.
- Taxas de desemprego de 1980-81 e 1990-91 na PME antiga vêm de fonte não identificada na série (comentário só cita 1982-1989).
- Código SGS 7326 não confirmado em página de catálogo do BCB (404 no dados abertos, CKAN não-JSON).
- Média aritmética de "janela exata" com fração de ano não definida; reporto só taxa anualizada. Não reconstruí datas de posse de 1964-1990.
- Cobertura territorial da PNAD até 2003 e definição exata da PNAD (10+, setembro) por fato metodológico do IBGE, não verificado nesta colheita.
- Não abri o PDF escaneado da PME de dez/1991 (sem OCR); os números de 1986-1990 daquele relatório vêm de um trecho de busca web, sem checagem.
- O PIB de 2024 e 2025 e o per capita de 2024-2025 são preliminares do IBGE e derivados, respectivamente.
- SCN10_PIB10 e SCN10_PIBG10 divergem em 2024 (3,396% contra 3,419%).
- Coincidências numéricas listadas (PNAD 1993 = 6,80; PNAD 2012 = 6,72; PNADC 2019-2021 = 13,17; PNADC 2017-18 = 12,35) não são prova de origem do número do infográfico.

## 6. Reprodutibilidade

- Script: `recalcula.py` (sha256 `95fb478579e72bb65565e7292ec0bc4966d535b34a84b1c9cf3d7442aea68ba7` na versão final; confira com `shasum -a 256`). Rode `python3 -I recalcula.py`.
- Saída integral: `saida-recalcula.txt`; CSVs: `saida-pib-anual-1948-2025.csv`, `saida-desemprego-anual.csv`, `saida-salmin-real-anual.csv`.
- Brutos e metadados: todos os `*-raw.json` e `meta/`. Cadeia de hash: `manifest.jsonl`; verificação: `python3 ../manifest_tool.py verify <esta pasta>`.
