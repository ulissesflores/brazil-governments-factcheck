# Bloco social: pobreza, Gini, expectativa de vida, mortalidade infantil

Dossiê: governos-do-brasil-economia. Coleta e conferência em 2026-10-19. Sem opinião política: só o que os números dizem.

Legenda: ✅ reproduz (fonte primária, mesmo valor no MESMO ano) | ⚠️ aproximado (o valor existe, mas em outro ano/linha/vintage, ou difere até ~1 ponto) | ❌ não reproduz (nada próximo no ano rotulado) | ❓ não consegui verificar.

Como reproduzir: `python3 -I /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/social/recalcula.py` (sem rede; confere o sha256 de cada bruto contra `manifest.jsonl` antes de ler; grava `series/*.csv` e `series/conferencia.md`). Cadeia de hash: `python3 /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py verify /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/social`.

## 0. Achado em 5 linhas

1. Das 8 cifras de pobreza, nenhuma fecha como rotulada. Quatro são valores reais do IBGE com ano ou linha deslocados: 31,6% é 2022 (não 2021) e 27,4% é 2023 (não 2024), ambos na linha US$ 6,85; 26,5% é 2017 (não 2018) na linha US$ 5,50 de edição antiga do SIS; 21,4% é 2009 (série Ipea interrompida, sem PNAD 2010). 2014 = 22,1 não bate (SIS na linha 5,50 dá 22,8). 42,6 e 28,9 não saem de nenhuma série. O infográfico muda de linha no meio: 2014 e 2018 parecem da linha US$ 5,50 (PPC 2011), 2021 e 2024 da US$ 6,85 (PPC 2017); na mesma linha 6,85, 2018 = 33,4%.
2. Gini: 2002 (0,59), 2014 (0,52) e 2018 (0,54) fecham; 1992 (0,60) é o valor de 1993; 0,58 em 2021 não existe (PNADC dá 0,543); 0,51 em 2024 é o valor de 2025 (2024 = 0,504).
3. Expectativa de vida: 2010, 2021 e 2023 fecham. "62,6 em 1970" é o valor de 1980 (1970 = 57,6). 2015 = 75,2 é a tábua de 2014. 67,1 (1990) e 75,7 (2018) não saem de nenhuma série. 72,8 em 2021 só existe depois da revisão pós-pandemia (a tábua como publicada em 2022 dizia 77,03).
4. "Pobreza 1990" não representa governo da ditadura (encerrada em março de 1985). Existe série de pobreza nos anos 1970 (Ipeadata: Censo 1970 e PNAD a partir de 1976), mas com linha diferente da usada nos demais anos do infográfico.
5. O infográfico mistura fontes e linhas sem declarar (Ipea 1976-2014, SIS com 5,50 e SIS com 6,85); em cada caso conferido o número existe numa dessas fontes, mas com o ano deslocado em 1 ano em 4 dos 8 pontos de pobreza, o que distorce a tendência.

## 1. Fontes (URL completa, código, data do download)

Todos os brutos estão em `bruto/` e cada um tem linha em `manifest.jsonl` (110 linhas na última conferência; metadata reconstruída = timestamp é o mtime do arquivo, marcada na `nota`). Download: 2026-10-19.

| Fonte | Código / tabela | URL | Arquivo bruto |
| --- | --- | --- | --- |
| Banco Mundial PIP (pobreza e Gini; 2017 PPC: 2,15/3,65/6,85; 2021 PPC: 3,00/4,20/8,30) | API PIP v1, `year=all`, `fill_gaps=false` | https://api.worldbank.org/pip/v1/pip?country=BRA&year=all&povline=6.85&ppp_version=2017&fill_gaps=false&format=json (idem para cada linha) | `bruto/pip_ppp2017_line*.json`, `bruto/pip_ppp2021_line*.json` |
| Banco Mundial WDI | SI.POV.GINI, SP.DYN.LE00.IN, SP.DYN.IMRT.IN, SI.POV.DDAY/LMIC/UMIC (lastupdated 2026-10-08) | https://api.worldbank.org/v2/country/BRA/indicator/SP.DYN.LE00.IN?format=json&per_page=20000 (idem) | `bruto/wb_*.json` |
| IBGE Síntese de Indicadores Sociais 2025 (pub. 2025-12-03) | Tabelas 2.13 (Gini) e 2.17 (pobreza), pastas por ano 2012-2024 | https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2025/Tabelas/xls/2_Distribuicao_Renda_xls.zip | `bruto/sis2025_2_dist_renda.zip` + `bruto/xlsx2025/` (derivado, `soffice --convert-to xlsx`) |
| IBGE SIS 2018, 2019, 2020 (linhas PPC 2011: 1,90 / 3,20 / 5,50) | 2018: Tabelas 2.28 e 2.28a (anos 2016-2017); 2019: 2.28, 2.28a, 2.28b (2012-2018); 2020: 2.25, 2.25a, 2.25b (2012-2019) | https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2019/xls/2_Rendimento_xls.zip (idem 2018, 2020) | `bruto/sis2018/`, `bruto/sis2019/`, `bruto/sis2020/` + `bruto/xlsx2018..2020/` (derivado) |
| IBGE SIS 2021, 2022, 2023 | baixados (zips e índices em `bruto/sis2021..2023/`), mas NÃO usados nas séries: não extraí as tabelas de pobreza dessas edições | https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2022/xls/ (idem) | `bruto/sis2021..2023/` |
| IBGE SIS 2017 | zip de rendimento baixado; o índice lista classes de rendimento (não linha de US$ 5,50): testado e descartado | https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2017/xls/rendimento_xls.zip | `bruto/sis2017/` |
| IBGE SIS 2024 (pub. 2024-12-04) | idem, anos 2012-2023 | https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2024/Tabelas/xls/2_Distribuicao_Renda_xls.zip | `bruto/sis2024_2_dist_renda.zip` + `bruto/xlsx2024/` |
| IBGE SIDRA / agregados | 5877 (pobreza linha nacional ODS), 5817 (internacional ODS), 7435 (Gini PNADC), 1174 (e0, 2000-2014), 1175 (TMI 1990-2009, série encerrada) | https://servicodados.ibge.gov.br/api/v3/agregados/7435/periodos/2012-2025/variaveis/all?localidades=BR (idem); páginas https://sidra.ibge.gov.br/tabela/7435 etc. | `bruto/sidra/` |
| Ipeadata OData | PGINI (=DISOC_RDCG), DISOC_PPY, PNADS_GINI, PNADS_PERCPOBRE300/420/830, PNADCA_GINIUF, PNADCA_TXPNUF/TXPIUF, DEPIS_ESVIDA, DEPIS_TMI, P0, ADH_GINI, ADH_PMPOB, ADH_PIND, EVNNEW | http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='PGINI') (idem); catálogo http://www.ipeadata.gov.br/api/odata4/Metadados | `bruto/ipea_*.json` |
| IBGE Tábuas Completas de Mortalidade (como publicadas) | folders 2000, 2005, 2010, 2014-2024; linha de idade 0 (e0 e 1000·q0) | https://ftp.ibge.gov.br/Tabuas_Completas_de_Mortalidade/Tabuas_Completas_de_Mortalidade_2024/xlsx/ambos_os_sexos.xlsx (idem por ano) | `bruto/tabuas_ibge/` |
| Agência IBGE, 2025-11-28, "Expectativa de vida chega a 76,6 anos em 2024" | tabelas 1940-2024 de e0 e TMI (série vigente) | https://agenciadenoticias.ibge.gov.br/pt/agencia-noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024.html (lido via proxy https://r.jina.ai/ porque o acesso direto devolve Cloudflare 403) | `bruto/ibge_agencia_tabuas2024_jina.md` |
| IBGE, "Observações sobre a evolução da mortalidade no Brasil" (2010) | Tabela 2: e0 e TMI 1980/1991/2000/2009 (Projeção, Revisão 2008) | https://biblioteca.ibge.gov.br/visualizacao/livros/liv98593.pdf | `bruto/ibge_liv98593.pdf` |
| Bonelli e Ramos, RBE 2/1995 (FGV) | Tabela 1: Gini dos censos 1960/1970/1980 (Langoni 1973; Bonelli e Malan 1984) | https://periodicos.fgv.br/rbe/article/download/642/7993/19921 | `bruto/fgv_rbe_642_gini_censos.pdf` |

Linhas de pobreza usadas por cada série (a definição é parte do dado):

| Série | Linha | Observação |
| --- | --- | --- |
| IBGE SIS 2024/2025, Tabela 2.17 | US$ 2,15 / 3,65 / 6,85 por dia, PPC 2017; e 50% da mediana | renda domiciliar per capita, PNADC, série 2012+ |
| IBGE SIS 2018/2019/2020 | US$ 1,90 / 3,20 / 5,50 por dia, PPC 2011 (R$ 1,66 por US$ PPC 2011, inflacionado pelo IPCA) | PNADC; edições anteriores à troca para PPC 2017 |
| IBGE SIDRA 5877 / Ipeadata PNADCA_TXPNUF | US$ 8,30 PPC 2021 ("linha nacional" ODS) | vintage nova (2026); NÃO é a de 6,85 |
| IBGE SIDRA 5817 / PNADCA_TXPIUF | US$ 3,00 PPC 2021 | idem |
| Ipeadata PNADS_PERCPOBRE300/420/830 | US$ 3,00 / 4,20 / 8,30 PPC 2021 | PNAD 1995-2011 harmonizada à PNADC (Souza e Hecksher 2025) |
| Ipeadata DISOC_PPY (INATIVA) | linha própria Ipea = 2 x linha de indigência (cesta FAO), 24 regiões | PNAD 1976-2014, sem anos de Censo; série interrompida |
| Ipeadata P0 (Atlas 1998) | renda familiar per capita < 50% do salário mínimo de set/1991 | Censos 1970, 1980, 1991 |
| Ipeadata ADH_PMPOB / ADH_PIND | <= R$ 140 / <= R$ 70 de ago/2010 | Censos 1991, 2000, 2010 |
| Banco Mundial PIP | 2,15 / 3,65 / 6,85 (PPC 2017) e 3,00 / 4,20 / 8,30 (PPC 2021) | PNAD até 2011, PNADC de 2012 |

## 2. Pobreza: as 8 cifras do infográfico

O infográfico não declara a linha. Coluna "no ano rotulado" = o que as séries dizem naquele ano; "mesmo valor aparece em" = onde o número bate.

| Ano rotulado | Infográfico (%) | No ano rotulado | Mesmo valor aparece em | Status |
| --- | --- | --- | --- | --- |
| 1990 ("referência") | 42,6 | Ipeadata PPY 41,9; PIP 3,65 (2017) 41,6; PIP 4,20 (2021) 41,8; PIP 6,85 63,7 | nenhuma série | ⚠️ (nenhuma linha dá 42,6; 41,6 a 41,9 só por coincidência de linhas diferentes) |
| 1994 | ~34 | não há PNAD em 1994, nenhuma série tem o ano | PPY 1998 = 34,0 (PPY 1993 = 43,0; 1995 = 35,1) | ❌ |
| 2002 | 28,9 | PPY 34,4; PIP 3,65 25,3; PIP 6,85 47,3; PNADS 4,20 35,3 | PIP 3,65 em 1998 (28,87) | ❌ |
| 2010 | 21,4 | não há PNAD 2010; Censo (Atlas) R$ 140 = 15,2 | Ipeadata PPY 2009 = 21,41 | ⚠️ (valor de 2009) |
| 2014 | 22,1 | IBGE SIS 5,50 (PPC 2011) = 22,8 (SIS 2019 e 2020; menor valor da série 2012-2019); SIS 6,85 = 30,9; PPY 13,3; PIP 6,85 24,4; ODS 8,30 33,2 | PIP 2,15 em 1993 (22,1) | ⚠️ (formato certo, 2014 é o piso da série 5,50, mas 22,8 não é 22,1) |
| 2018 | 26,5 | IBGE SIS 5,50 (PPC 2011) = 25,28 (SIS 2019/2020); SIS 6,85 = 33,4; ODS 8,30 35,5; PIP 6,85 26,8 | SIS 2018 (linha 5,50), ano 2017 = 26,47; SIS 2019/2020, ano 2012 = 26,46; ODS 8,30 em 2024 = 26,5 | ⚠️ (valor de 2017 como publicado no SIS 2018; as edições seguintes revisaram 2017 para 26,0) |
| 2021 | 31,6 | IBGE SIS 6,85 = 36,7 (SIS 2024) / 36,8 (SIS 2025); PIP 6,85 28,4 | IBGE SIS 6,85 em 2022 = 31,6 (31,62 / 31,65) | ⚠️ (valor de 2022) |
| 2024 | 27,4 | IBGE SIS 2025 6,85 = 23,1 | IBGE SIS 2024 6,85 em 2023 = 27,37; SIS 2025 revisou 2023 para 27,30 | ⚠️ (valor de 2023) |

Série IBGE SIS na linha US$ 5,50 PPC 2011 (% da população; edições 2018 / 2019 / 2020): 2012 -/26,46/26,46; 2013 -/24,89/24,89; 2014 -/22,80/22,80; 2015 -/23,69/23,69; 2016 25,72/25,51/25,51; 2017 26,47/26,00/26,00; 2018 -/25,28/25,28; 2019 -/-/24,71. Duas coisas a notar: (a) o infográfico tem 2014 como mínimo e 2018 acima dele, o que a série 5,50 também mostra (22,8 -> 25,3); (b) a mesma tendência na linha 6,85 dá 30,9 (2014) e 33,4 (2018), um nível 8 pontos acima.

Série IBGE SIS, US$ 6,85 PPC 2017 (% da população), para a conferência de tendência:

| Ano | SIS 2024 | SIS 2025 | | Ano | SIS 2024 | SIS 2025 |
| --- | --- | --- | --- | --- | --- | --- |
| 2012 | 34,71 | 34,73 | | 2019 | 32,51 | 32,61 |
| 2013 | 32,44 | 32,48 | | 2020 | 30,96 | 31,06 |
| 2014 | 30,82 | 30,88 | | 2021 | 36,69 | 36,77 |
| 2015 | 31,65 | 31,72 | | 2022 | 31,62 | 31,65 |
| 2016 | 33,67 | 33,75 | | 2023 | 27,37 | 27,30 |
| 2017 | 33,69 | 33,79 | | 2024 | - | 23,11 |
| 2018 | 33,34 | 33,44 | | | | |

Leitura sobre a ordem de grandeza: o Banco Mundial PIP com a mesma linha (6,85, PPC 2017) dá níveis bem menores que o IBGE na era PNADC (2021: 28,4 contra 36,8; 2024: 18,9 contra 23,1). O motivo da diferença (tratamento de renda/benefícios, fator de conversão, vintage) não foi investigado: ❓. Misturar IBGE e PIP na mesma coluna distorce a tendência.

### 2.1 Existe série de pobreza para os anos 1970?

Sim, mas com linha diferente e sem comparabilidade direta com os anos seguintes:

| Série | Anos 1970 | Valor | Linha |
| --- | --- | --- | --- |
| Ipeadata P0 (Atlas 1998, Censo) | 1970 / 1980 / 1991 | 67,9% / 39,5% / 45,5% | renda familiar per capita < 50% do SM de set/1991 |
| Ipeadata DISOC_PPY (PNAD) | 1976 a 1979 | 42,1 / 39,1 / 42,7 / 38,7 | linha própria Ipea (2 x indigência); a série começa em 1976 e não tem 1980 (ano de Censo) |
| Banco Mundial PIP | começa em 1981 | - | - |

Para o intervalo 1967-1974 da linha "Ditadura" só o Censo 1970 (67,9%, linha P0) existe; não há valor PNAD nacional nesses anos nas fontes baixadas. Observação metodológica: o 67,9% de 1970 e o 42,1% de 1976 usam linhas diferentes e não formam uma série contínua.

### 2.2 "Pobreza 1990" pode representar o governo da ditadura?

Não. A ditadura militar terminou em 15 de março de 1985; 1990 é a PNAD de setembro de 1990, cinco anos depois e sob outro mandato. O infográfico rotula a célula "1990 (referência)", ou seja, admite que o ano não é o do período. Série de pobreza que cobre o fim do período militar existe só na linha Ipea (PPY: 1981 40,8; 1983 48,7; 1984 48,3; 1985 42,0) e no PIP a partir de 1981 (3,65: 1981 42,9; 1985 45,2).

## 3. Gini (renda domiciliar per capita)

Quebras metodológicas marcadas:

| Marco | O que acontece | Evidência |
| --- | --- | --- |
| Sem PNAD em 1991, 1994, 2000, 2010 | anos de Censo (1991, 2000, 2010) e PNAD não realizada em 1994; Ipeadata registra "dados não calculados para os anos de Censo" | `ipea_PGINI.json` não tem esses anos |
| PNAD -> PNADC em 2012 | nível sobe ao trocar a pesquisa. Sobreposição 2012-2014 (PNAD antiga, Ipeadata PGINI / PNADC, SIDRA 7435): 0,5297 / 0,540; 0,5275 / 0,532; 0,5179 / 0,526 | `series/gini.csv` |
| Censo x PNAD | o Gini do Censo 2010 (Atlas DH) é 0,600; os Gini de PNAD em torno de 2010 são ~0,53 a 0,54 | `ipea_ADH_GINI.json` (1991 0,63; 2000 0,64; 2010 0,60) |
| Harmonização Ipea (PNADS_GINI) | multiplica a PNAD <= 2011 por um fator que iguala 2012; 2002 vira 0,603, não 0,589 | metadado da série (Souza e Hecksher 2025) |
| Pandemia | 2020 cai (0,523) e 2021 sobe (0,543); causa não investigada | SIDRA 7435 |
| Anomalia | PIP/WDI 1992 = 0,531 destoa de 1990 (0,605) e 1993 (0,601), enquanto a PNAD de 1992 pelo Ipeadata dá 0,583. Causa não verificada: ❓ | `pip_*`, `wb_SI.POV.GINI.json` |

Série anual por fonte (0 a 1). PGINI = PNAD antiga (Ipeadata, série interrompida em 2014); PNADC = SIDRA 7435 / IBGE SIS; WB = Banco Mundial.

| Ano | PGINI (PNAD) | PNADC (IBGE) | Harmonizada Ipea | WB/PIP | Censo (Atlas) |
| --- | --- | --- | --- | --- | --- |
| 1976 | 0,623 | - | - | - | - |
| 1979 | 0,593 | - | - | - | - |
| 1981 | 0,584 | - | - | 0,579 | - |
| 1985 | 0,598 | - | - | 0,555 | - |
| 1989 | 0,636 | - | - | 0,632 | - |
| 1990 | 0,614 | - | - | 0,605 | - |
| 1992 | 0,583 | - | - | 0,531 | - |
| 1993 | 0,604 | - | - | 0,601 | - |
| 1995 | 0,601 | - | 0,615 | 0,595 | - |
| 2001 | 0,596 | - | 0,610 | 0,584 | - |
| 2002 | 0,589 | - | 0,603 | 0,581 | - |
| 2003 | 0,583 | - | 0,596 | 0,576 | - |
| 2009 | 0,543 | - | 0,554 | 0,537 | - |
| 2010 | sem PNAD | - | - | sem dado | 0,600 |
| 2011 | 0,531 | - | 0,543 | 0,529 | - |
| 2012 | 0,530 | 0,540 | 0,540 | 0,534 | - |
| 2013 | 0,528 | 0,532 | 0,532 | 0,527 | - |
| 2014 | 0,518 | 0,526 | 0,526 | 0,521 | - |
| 2015 | - | 0,524 | 0,524 | 0,519 | - |
| 2018 | - | 0,545 | 0,545 | 0,539 | - |
| 2020 | - | 0,523 | 0,523 | 0,488 | - |
| 2021 | - | 0,543 | 0,544 | 0,529 | - |
| 2022 | - | 0,517 | 0,517 | 0,519 | - |
| 2023 | - | 0,517 | 0,517 | 0,515 | - |
| 2024 | - | 0,504 | 0,505 | 0,503 | - |
| 2025 | - | 0,511 | 0,511 | - | - |

Os Gini dos Censos 1960/1970/1980 (população economicamente ativa com rendimento não nulo, não é per capita domiciliar): 0,500 / 0,568 / 0,590 (Bonelli e Ramos, RBE 2/1995, Tabela 1, citando Langoni 1973 e Bonelli e Malan 1984); PNAD 1979 da mesma tabela: 0,580 (PEA).

Conferência:

| Ano rotulado | Infográfico | Fontes no ano | Onde o valor aparece | Status |
| --- | --- | --- | --- | --- |
| "anos 1970" | 0,59 | 1970 (Censo, PEA): 0,568; PNAD per capita 1976: 0,623, 1977: 0,625, 1978: 0,604, 1979: 0,593 | PNAD per capita 1979 = 0,593 (ainda dentro da década); Censo 1980 (PEA) = 0,590 | ✅ para o rótulo "anos 1970" lido como a década (reproduz em 1979; a década vai de 0,59 a 0,62); ⚠️ se for lido como 1970, que é 0,568 (PEA, Censo) |
| 1992 | 0,60 | PNAD 1992 = 0,583; PIP 0,531 | PNAD 1993 = 0,604 (PIP 0,601); 1990 = 0,614 | ⚠️ (valor de 1993; 1992 = 0,58) |
| 2002 | 0,59 | PGINI 0,589; PIP/WDI 0,581 | - | ✅ (PNAD Ipeadata; PIP daria 0,58) |
| 2010 | 0,53 | sem PNAD; Censo 0,600 | PNAD 2011 = 0,531; PIP 2011 = 0,529 | ⚠️ (valor de 2011; 2009 = 0,543) |
| 2014 | 0,52 | PGINI 0,518; PIP 0,521; PNADC 0,526 (= 0,53) | - | ✅ (com PNAD antiga ou PIP; PNADC arredonda para 0,53) |
| 2018 | 0,54 | PIP 0,539; PNADC 0,545 / IBGE SIS 0,5454 (= 0,55 se arredondar) | - | ✅ (PIP; IBGE no limite do arredondamento) |
| 2021 | 0,58 | PNADC 0,543; PIP 0,529 | nenhum ano recente (0,58 só em 1981-1992) | ❌ |
| 2024 | 0,51 | PNADC 0,504; PIP 0,503 | PNADC 2025 = 0,511 | ⚠️ (valor de 2025; 2024 = 0,50) |

## 4. Expectativa de vida ao nascer (anos)

Duas camadas de revisão precisam estar marcadas:

1. Revisão pós-pandemia. A tábua de 2021 como publicada em 2022 dava 77,03 (ainda sem o excesso de mortes da Covid); a tábua de 2020 como publicada dava 76,79. Depois, a série vigente (Tábua 2024, divulgada em 2025-11-28) passou a dar 74,8 (2020) e 72,8 (2021); a data exata da revisão não foi verificada (❓). O 72,8 do infográfico só existe depois dessa revisão. Evidência: `series/expvida.csv`, fonte `IBGE-Tabua-como-publicada` (2020 = 76,79; 2021 = 77,03) contra `IBGE-Tabuas2024-serie-vigente` (74,8; 72,8).
2. Revisão das projeções. O mesmo ano muda de valor conforme a Projeção da População em uso. Exemplo, ano 2000: tábua de 2000 como publicada 68,62; Projeção Revisão 2008 = 70,46; Revisão 2013 (SIDRA 1174) = 69,8; série vigente (Tábua 2024) = 71,1. Exemplo, ano 2010: 73,48 (tábua publicada), 73,9 (SIDRA 1174), 74,4 (vigente).

| Ano | Banco Mundial (UN WPP) | IBGE série vigente (Tábua 2024) | IBGE tábua como publicada | IBGE Proj. Rev. 2008 | SIDRA 1174 (Rev. 2013) | Ipeadata DEPIS (Rev. 2018) |
| --- | --- | --- | --- | --- | --- | --- |
| 1960 | 53,16 | 52,5 | - | - | - | - |
| 1970 | 57,34 | 57,6 | - | - | - | - |
| 1980 | 61,82 | 62,5 | - | 62,57 | - | - |
| 1990 | 65,86 | - | - | - | - | - |
| 1991 | 66,20 | 66,9 | - | 66,93 | - | - |
| 2000 | 69,58 | 71,1 | 68,62 | 70,46 | 69,8 | 69,83 |
| 2005 | 71,83 | - | 71,95 | - | 72,0 | 71,99 |
| 2010 | 73,78 | 74,4 | 73,48 | - | 73,9 | 73,86 |
| 2014 | 74,82 | - | 75,20 | - | 75,1 | 75,14 |
| 2015 | 75,11 | - | 75,49 | - | - | 75,44 |
| 2016 | 75,08 | - | 75,77 | - | - | 75,72 |
| 2018 | 75,63 | - | 76,31 | - | - | 76,25 |
| 2019 | 75,81 | 76,2 | 76,55 | - | - | 76,50 |
| 2020 | 74,51 | 74,8 | 76,79 | - | - | 76,74 |
| 2021 | 73,04 | 72,8 | 77,03 | - | - | 76,97 |
| 2022 | 74,87 | 75,4 | 75,45 | - | - | 77,19 |
| 2023 | 75,85 | 76,4 | 76,39 | - | - | - |
| 2024 | 76,02 | 76,6 | 76,61 | - | - | - |

A série anual completa 1960-2024 do Banco Mundial está em `series/expvida.csv` (fonte `WB-WDI-SP.DYN.LE00.IN`); a série vigente IBGE só tem os marcos 1940, 1950, 1960, 1970, 1980, 1991, 2000, 2010 e 2019-2024 (é o que a Agência IBGE publica); a anual 2000-2022 do Ipeadata é a Revisão 2018.

Efeito da pandemia (série vigente IBGE): 2019 76,2 -> 2020 74,8 -> 2021 72,8 -> 2022 75,4 -> 2023 76,4 -> 2024 76,6. Banco Mundial: 75,8 -> 74,5 -> 73,0 -> 74,9 -> 75,8 -> 76,0.

Conferência:

| Ano rotulado | Infográfico | No ano rotulado | Onde o valor aparece | Status |
| --- | --- | --- | --- | --- |
| 1970 | 62,6 | IBGE 57,6; UN/WB 57,3 | 1980: 62,57 (Rev. 2008), 62,5 (vigente) | ⚠️ (valor de 1980; 1970 = 57,6) |
| 1990 | 67,1 | WB 65,9; IBGE 1991 = 66,9 | nenhum | ⚠️ (nada dá 67,1; mais perto é IBGE 1991 66,93) |
| 2000 | 70,4 | IBGE Rev. 2008 70,46; Rev. 2013 69,8; vigente 71,1; WB 69,6 | 70,46 truncado a 70,4; WB 2002 = 70,4 | ⚠️ (vintage 2008, superada) |
| 2010 | 73,9 | SIDRA 1174 73,9; DEPIS 73,86; vigente 74,4; tábua publicada 73,48 | - | ✅ (IBGE Rev. 2013; a série vigente hoje dá 74,4) |
| 2015 | 75,2 | tábua 2015 75,49; DEPIS 75,44; WB 75,11; SIDRA 2014 75,1 | Tábua 2014 como publicada = 75,20 | ⚠️ (valor de 2014) |
| 2018 | 75,7 | tábua 76,31; DEPIS 76,25; WB 75,63 | DEPIS/tábua de 2016 = 75,72/75,77 | ❌ |
| 2021 | 72,8 | vigente IBGE 72,8; WB 73,04; tábua como publicada 77,03 | - | ✅ (só na série revisada) |
| 2023 | 76,4 | vigente 76,4; tábua 76,39 | - | ✅ |

## 5. Mortalidade infantil (por mil nascidos vivos), indicador extra

| Ano | Banco Mundial (UN IGME) | IBGE série vigente | IBGE tábua como publicada (1000 x q0) | IBGE Proj. Rev. 2008 | SIDRA 1175 (série encerrada) | Ipeadata DEPIS |
| --- | --- | --- | --- | --- | --- | --- |
| 1960 | 127,2 | 117,7 | - | - | - | - |
| 1970 | 102,2 | 97,6 | - | - | - | - |
| 1980 | 76,7 | 69,1 | - | 69,12 | - | - |
| 1990 | 51,9 | - | - | - | 47,0 | - |
| 1991 | 49,8 | 45,1 | - | 45,14 | 45,1 | - |
| 2000 | 29,1 | 28,1 | 33,74 | 30,07 | 30,1 | 29,02 |
| 2005 | 21,0 | - | 25,77 | - | 25,8 | 22,18 |
| 2010 | 16,0 | 15,0 | 21,64 | - | - | 17,22 |
| 2014 | 14,0 | - | 14,40 | - | - | 14,40 |
| 2015 | 13,7 | - | 13,82 | - | - | 13,82 |
| 2018 | 13,1 | - | 12,36 | - | - | 12,35 |
| 2019 | 12,9 | 12,1 | 11,94 | - | - | 11,94 |
| 2020 | 12,8 | 11,4 | 11,56 | - | - | 11,56 |
| 2021 | 12,7 | 12,2 | 11,20 | - | - | 11,20 |
| 2022 | 12,6 | 12,4 | 12,84 | - | - | 10,88 |
| 2023 | 12,4 | 12,5 | 12,47 | - | - | - |
| 2024 | 12,3 | 12,3 | 12,26 | - | - | - |

Notas: (1) Os valores de tábua como publicada em 2000, 2005 e 2010 (33,7; 25,8; 21,6) são muito maiores que os da série vigente (28,1; -; 15,0): é o mesmo efeito de revisão de vintage (método/projeção; causa específica não verificada). (2) A série vigente do IBGE mostra TMI subindo de 11,4 (2020) para 12,2 (2021), 12,4 (2022) e 12,5 (2023) e voltando a 12,3 em 2024; o Banco Mundial não mostra essa alta (12,8 -> 12,3 em queda contínua). Divergência entre as duas fontes, causa não investigada: ❓. (3) A Agência IBGE de 2025-11-28 traz 12,3 para 2024; a imprensa citou 12,5 (que é o valor de 2023). (4) O WDI tem salto em 2016 (14,6, entre 13,7 em 2015 e 13,3 em 2017) que parece artefato da fonte; não verificado: ❓.

O infográfico não traz mortalidade infantil; os números acima são o indicador extra pedido.

## 6. O que NÃO foi achado

- Nenhuma série baixada reproduz: pobreza 42,6 (1990, exato), 28,9 (2002), 22,1 (2014, o mais perto é 22,8 na linha 5,50); expectativa de vida 67,1 (1990) e 75,7 (2018); Gini 0,58 (2021).
- `bruto/ibge_liv98586.pdf` (IBGE, mortalidade 1980-2004) foi baixado por engano, achado em busca como se fosse a fonte de e0; não é usado em nenhum número. Fica no manifest porque a cadeia é append-only. A fonte correta é `bruto/ibge_liv98593.pdf`.
- Pobreza em 1994: não existe PNAD em 1994, nenhuma fonte tem o ano.
- Gini domiciliar per capita para 1970: só existe Gini de PEA (0,568, Censo). A série per capita (Ipeadata PGINI) começa em 1976.
- Pobreza nacional por PNAD para 1967-1974: não há; só o Censo 1970 (67,9%, linha diferente).
- Explicação da diferença de nível entre IBGE e Banco Mundial na pobreza com a mesma linha (6,85): não investigada (❓).
- Edições do SIS 2021, 2022 e 2023 (anos de referência 2020-2022): zips baixados, mas as tabelas de pobreza dessas edições não foram extraídas; edições SIS 2016 e anteriores não têm a linha de US$ 5,50 (testei só o índice da de 2017). 28,9 (2002) e 42,6 (1990) não podem vir do SIS, que começa em 2012 (PNADC); a origem desses dois ficou ❓.
- A página da Agência IBGE de 2025-11-28 só foi lida por proxy (r.jina.ai), porque o acesso direto dá Cloudflare 403; a tabela 1940-2024 não foi conferida contra a página original no navegador (❓ parcial). Os valores de 2019 a 2024 batem com as Tábuas baixadas diretamente do FTP do IBGE (2023 = 76,39; 2024 = 76,61).
- As páginas web do Ipeadata não foram abertas; os códigos de série foram confirmados no catálogo `Metadados` da API OData (campos SERCODIGO, SERNOME, FNTNOME, SERCOMENTARIO), com a definição de linha lida do próprio campo SERCOMENTARIO.
- UN WPP não foi baixado diretamente; entrou via espelho do Banco Mundial (WDI, lastupdated 2026-10-08).
