# O que o infografico mistura, e a direcao medida do efeito sobre cada governo

Gerado por `gerar_mistura.py` a partir de `saida/medidas.json`, `comparativo-metodo-constante.csv`, `vintage-do-infografico.csv` e `pobreza-*.csv`; nenhum numero foi digitado a mao. Sem opiniao e sem inferir intencao: so a direcao do efeito, medida com os numeros.

> [!IMPORTANT]
> Convencao. **favorece** = o numero impresso (ou o efeito da mistura) deixa o governo MELHOR do que a referencia de metodo constante (menor para desemprego, inflacao, pobreza e Gini; maior para PIB, salario minimo real e expectativa de vida). **prejudica** = PIOR. **neutro** = diferenca de ate 1 unidade da ultima casa impressa (0,1; 0,01 no Gini). **indeterminado** = nao ha referencia no ano/janela, ou o sinal muda conforme a referencia escolhida. Referencias de metodo constante: PIB = SCN ref. 2010 (ou o segmento do governo); pobreza e Gini = Banco Mundial PIP, com IBGE SIS como segunda linha; expectativa de vida = UMA vintage (WDI/UN), com a serie vigente do IBGE como segunda linha; desemprego = o segmento do proprio governo.

## 1. Janela do mandato (PIB, IPCA, desemprego, salario minimo)

O infografico usa janelas diferentes por indicador e por governo (ver `historia/RESULTADO.md`, secao 2). Efeito = valor da serie na janela IMPRESSA menos o valor da MESMA serie na janela do mandato (cada ano ao governo que o exerceu na maior parte). Sao os dados publicados, sem estimar.

| indicador | governo | janela impressa | media na janela impressa | janela do mandato | media no mandato | efeito da janela | direcao |
|---|---|---|---|---|---|---|---|
| PIB (% a.a.) | Ditadura | 1968-1973 | 11,16 | 1967-1973 | 10,16 | +0,99 | favorece |
| PIB (% a.a.) | Itamar | 1992-1994 | 3,41 | 1993-1994 | 5,39 | -1,98 | prejudica |
| PIB (% a.a.) | Temer | 2016-2018 | -0,06 | 2017-2018 | 1,55 | -1,61 | prejudica |
| IPCA (% a.a.) | Itamar | 1992-1994 | 1504,22 | 1993-1994 | 1696,79 | -192,57 | favorece |
| IPCA (% a.a.) | Temer | 2016-2018 | 4,33 | 2017-2018 | 3,35 | +0,98 | prejudica |
| Desemprego (%), PNADC | Temer | 2016-2018 | 12,10 | 2017-2018 | 12,35 | -0,25 | favorece |
| Desemprego (%), PNADC | Bolsonaro | 2019-2020 | 12,75 | 2019-2022 | 12,28 | +0,47 | prejudica |
| Desemprego (%), PME antiga | Itamar | 1992-1994 | 5,78 | 1993-1994 | 5,59 | +0,18 | prejudica |
| Salario minimo real (acumulado %, serie Ipea) | Ditadura | 1968-1973 | -3,3 | 1967-1973 | -10,2 | +6,9 | favorece |
| Salario minimo real (acumulado %, serie Ipea) | Itamar | 1992-1994 | 6,1 | 1993-1994 | -1,8 | +7,9 | favorece |
| Salario minimo real (acumulado %, serie Ipea) | Temer | 2016-2018 | 4,5 | 2017-2018 | 2,3 | +2,2 | favorece |

Dilma (2011-2016) e Temer (2016-2018) contam 2016 nas duas colunas (Dilma governou 8 dos 12 meses). Itamar (1992-1994) inclui 9 meses de Collor. A coluna 'Ditadura' tem cabecalho 1967-1974 e janelas de 1968-1973 ou 1967-1973 conforme o indicador. 'Lula 3' tem janela 2023-2025 marcada com asterisco no infografico (2026 incompleto): sem referencia para comparar.

## 2. Pobreza: linha que muda, janela de ano e fonte

Referencia de linha constante: US$ 6,85 (PPC 2017), mesma linha em todos os anos (e, SO para as celulas anteriores a 2012, cuja linha e desconhecida, tambem US$ 3,65 para mostrar que o sinal muda com a linha), PIP (1981-2024) e IBGE SIS (2012-2024). Efeito = numero impresso menos o valor da referencia NO ANO ROTULADO. Onde o PIP nao tem o ano (1994, 2010), nao ha referencia (indeterminado).

| governo | impresso (%) | ano rotulado | PIP 6,85 no ano | dif. vs PIP 6,85 | PIP 3,65 no ano | dif. vs PIP 3,65 | SIS 6,85 no ano | dif. vs SIS | direcao (6,85) | direcao (3,65) | direcao (SIS) | veredito |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ditadura | 42,6 | 1990 | 63,7 | -21,1 | 41,6 | +1,0 | n/d | n/d | favorece | prejudica | indeterminado | indeterminado |
| Itamar | 34,0 | 1994 | n/d | n/d | n/d | n/d | n/d | n/d | indeterminado | indeterminado | indeterminado | indeterminado |
| FHC | 28,9 | 2002 | 47,3 | -18,4 | 25,3 | +3,6 | n/d | n/d | favorece | prejudica | indeterminado | indeterminado |
| Lula 1-2 | 21,4 | 2010 | n/d | n/d | n/d | n/d | n/d | n/d | indeterminado | indeterminado | indeterminado | indeterminado |
| Dilma | 22,1 | 2014 | 24,4 | -2,3 | 8,6 | +13,5 | 30,9 | -8,8 | favorece | prejudica | favorece | favorece |
| Temer | 26,5 | 2018 | 26,8 | -0,3 | 10,9 | +15,6 | 33,4 | -6,9 | favorece | prejudica | favorece | favorece |
| Bolsonaro | 31,6 | 2021 | 28,4 | +3,2 | 11,2 | +20,4 | 36,8 | -5,2 | prejudica | prejudica | favorece | indeterminado |
| Lula 3 | 27,4 | 2024 | 18,9 | +8,5 | 6,1 | +21,3 | 23,1 | +4,3 | prejudica | prejudica | prejudica | prejudica |

Nas celulas anteriores a 2012 (Ditadura/1990, Itamar/1994, FHC/2002, Lula 1-2/2010) a linha usada no infografico e desconhecida (nenhuma serie baixada reproduz o numero); a comparacao com US$ 6,85 mede, portanto, linha + ano juntos.

O infografico NAO mantem a linha: pela reproducao do bloco social (`vintage-do-infografico.csv`), 2014 e 2018 casam com a faixa de US$ 5,50 (PPC 2011) e 2021 e 2024 com a de US$ 6,85 (PPC 2017). O efeito dessa troca, medido nos mesmos microdados 2012-2019 (IBGE SIS, edicoes 2020 e 2025):

| ano | SIS 5,50 (PPC 2011) | SIS 6,85 (PPC 2017) | diferenca (pp) |
|---|---|---|---|
| 2012 | 26,46 | 34,73 | +8,27 |
| 2013 | 24,89 | 32,48 | +7,59 |
| 2014 | 22,80 | 30,88 | +8,08 |
| 2015 | 23,69 | 31,72 | +8,03 |
| 2016 | 25,51 | 33,75 | +8,24 |
| 2017 | 26,00 | 33,79 | +7,79 |
| 2018 | 25,28 | 33,44 | +8,16 |
| 2019 | 24,71 | 32,61 | +7,90 |

Media +8,01 pp. Leitura medida: as celulas de Dilma (2014) e Temer (2018), que usam a linha de 5,50, ficam ~8 pp abaixo do que a linha de 6,85 daria no mesmo ano; as de Bolsonaro (2021) e Lula 3 (2024) ja estao em 6,85. Direcao sobre a comparacao entre governos: **favorece Dilma e Temer** em relacao a Bolsonaro e Lula 3 (a diferenca de linha por si so e de cerca de 8 pp). Isso e dito sem inferir como a linha foi escolhida.

### 2.1 Ano deslocado

Em 4 das 8 celulas o numero impresso e o da fonte em OUTRO ano (reproducao em `vintage-do-infografico.csv`). Efeito = valor da fonte no ano rotulado menos o impresso (positivo = a fonte, no ano certo, diria mais pobreza).

| governo | impresso | ano rotulado | valor da MESMA fonte/linha no ano rotulado | ano em que o impresso aparece | efeito do deslocamento (pp) | direcao |
|---|---|---|---|---|---|---|
| Lula 1-2 | 21,4 | 2010 | n/d (Ipea PPY (sem PNAD em 2010)) | 2009 | n/d | indeterminado |
| Temer | 26,5 | 2018 | 25,28 (SIS ed. 2020, 5,50) | 2017 | -1,22 | prejudica |
| Bolsonaro | 31,6 | 2021 | 36,77 (SIS 2025, 6,85) | 2022 | +5,17 | favorece |
| Lula 3 | 27,4 | 2024 | 23,11 (SIS 2025, 6,85) | 2023 | -4,29 | prejudica |

## 3. Gini: pesquisa, vintage e ano deslocado

Referencia: PIP (renda domiciliar per capita; PNAD 1981-2011, PNADC 2012-2024 como spells do proprio PIP). Segunda linha: IBGE SIS (PNADC, 2012+) e PNAD antiga (Ipeadata PGINI). 'anos 1970' do infografico e tratado como 1975 so para a consulta (sem dado PIP anterior a 1981: indeterminado).

| governo | impresso | ano rotulado | PIP no ano | dif. vs PIP | SIS (PNADC) no ano | PNAD antiga no ano | direcao (PIP) | direcao (2a fonte) | sinal igual? |
|---|---|---|---|---|---|---|---|---|---|
| Ditadura | 0,59 | anos 1970 | n/d | n/d | n/d | n/d | indeterminado | indeterminado | n/d |
| Itamar | 0,60 | 1992 | 0,531 | +0,069 | n/d | 0,583 | prejudica | prejudica | sim |
| FHC | 0,59 | 2002 | 0,581 | +0,009 | n/d | 0,589 | neutro | neutro | sim |
| Lula 1-2 | 0,53 | 2010 | n/d | n/d | n/d | n/d | indeterminado | indeterminado | n/d |
| Dilma | 0,52 | 2014 | 0,520 | 0,000 | 0,526 | 0,518 | neutro | neutro | sim |
| Temer | 0,54 | 2018 | 0,539 | +0,001 | 0,545 | n/d | neutro | neutro | sim |
| Bolsonaro | 0,58 | 2021 | 0,528 | +0,051 | 0,543 | n/d | prejudica | prejudica | sim |
| Lula 3 | 0,51 | 2024 | 0,503 | +0,007 | 0,504 | n/d | neutro | neutro | sim |

Mistura de pesquisa: do PNAD para o PNADC (2012) o Gini sobe +0,008 na sobreposicao 2012-2014 (PNADC maior em todos os 3 anos). As celulas de FHC, Lula 1-2 e Dilma 2014 usam PNAD antiga; Temer, Bolsonaro e Lula 3 usam PNADC (e 2020-2022 em quintas visitas). Direcao sobre a comparacao FHC/Lula 1-2 contra Temer/Bolsonaro/Lula 3: **favorece os primeiros** (PNAD antiga mede ~0,008 menos que PNADC no mesmo ano). Censo 2010 = 0,600 contra PNAD 2011 = 0,531: a celula de Lula 1-2 usa PNAD, nao o Censo (diferenca de +0,069).

## 4. Expectativa de vida: vintages coladas na mesma linha

Referencia 1: UMA vintage (UN WPP via Banco Mundial, 1960-2024). Referencia 2: serie vigente do IBGE (marcos). Efeito = impresso menos referencia no ano rotulado. A linha do infografico mistura Projecao Rev. 2008 (1970/2000, por deslocamento), Rev. 2013 (2010), tabua publicada de 2014 (2015), Rev. 2018 (2018, deslocado) e a serie vigente pos-pandemia (2021, 2023): ver `vintage-do-infografico.csv`.

| governo | impresso | ano rotulado | WDI no ano | dif. vs WDI | IBGE vigente no ano | dif. vs vigente | direcao (WDI) | direcao (vigente) | sinal igual? |
|---|---|---|---|---|---|---|---|---|---|
| Ditadura | 62,6 | 1970 | 57,34 | +5,26 | 57,6 | +5,00 | favorece | favorece | sim |
| Itamar | 67,1 | 1990 | 65,86 | +1,24 | n/d | n/d | favorece | indeterminado | n/d |
| FHC | 70,4 | 2000 | 69,58 | +0,82 | 71,1 | -0,70 | favorece | prejudica | NAO |
| Lula 1-2 | 73,9 | 2010 | 73,78 | +0,12 | 74,4 | -0,50 | favorece | prejudica | NAO |
| Dilma | 75,2 | 2015 | 75,11 | +0,09 | n/d | n/d | neutro | indeterminado | n/d |
| Temer | 75,7 | 2018 | 75,63 | +0,07 | n/d | n/d | neutro | indeterminado | n/d |
| Bolsonaro | 72,8 | 2021 | 73,04 | -0,24 | 72,8 | 0,00 | prejudica | neutro | NAO |
| Lula 3 | 76,4 | 2023 | 75,85 | +0,55 | 76,4 | 0,00 | favorece | neutro | NAO |

Efeito da vintage da 'tabua como publicada' sobre 2020-2022 (Bolsonaro): a tabua de 2021 diz 77,03; a serie vigente diz 72,8. Quem comparasse a tabua publicada de 2021 com a vigente de 2019 (76,2) leria um GANHO de 0,8 ano; na mesma vintage, a queda e de 3,4 anos. Direcao sobre Bolsonaro da mistura de vintages: **depende de qual vintage entra**; o impresso (72,8, vigente) e coerente com a serie vigente.

## 5. Desemprego cruza metodologias

Cada celula versus os metodos disponiveis NA SUA JANELA (nenhum metodo cobre todas as janelas). 'Referencia' so existe quando a janela cabe num unico segmento; do contrario o intervalo entre metodos e mostrado e a direcao e 'indeterminado'.

| governo | impresso | janela | PME antiga | PME nova | PNAD | PNADC | leitura |
|---|---|---|---|---|---|---|---|
| Ditadura | 3,7 | 1968-1973 | n/d | n/d | n/d | n/d | sem serie oficial 1968-1973; **indeterminado** |
| Itamar | 6,8 | 1992-1994 | 5,78 | n/d | 7,00 (2 de 3 anos) | n/d | sinais por metodo: prejudica, favorece; **indeterminado** |
| FHC | 7,7 | 1995-2002 | 7,01 | n/d | 8,97 (7 de 8 anos) | n/d | sinais por metodo: prejudica, favorece; **indeterminado** |
| Lula 1-2 | 8,4 | 2003-2010 | n/d | 9,46 | 9,33 (7 de 8 anos) | n/d | impresso '8,4 -> 6,5' contra media PME nova 9,46 e PNAD 9,33: abaixo dos dois; **favorece** |
| Dilma | 6,7 | 2011-2016 | n/d | 5,70 (5 de 6 anos) | 7,18 (4 de 6 anos) | 8,44 (5 de 6 anos) | sinais por metodo: prejudica, favorece, favorece; **indeterminado** |
| Temer | 12,3 | 2016-2018 | n/d | n/d | n/d | 12,10 | sinais por metodo: prejudica; **prejudica** |
| Bolsonaro | 13,2 | 2019-2020 | n/d | n/d | n/d | 12,75 | sinais por metodo: prejudica; **prejudica** |
| Lula 3 | 9,3 | 2023-2025 | n/d | n/d | n/d | 6,63 | sinais por metodo: prejudica; **prejudica** |

Quebra PME antiga -> PME nova (mar-dez/2002): nova menos antiga +3,73 pp em media. PNAD -> PNADC (2012-2014): +0,10 pp (media anual) e -0,17 pp (3o trimestre): sinal misto. Efeito sobre a transicao FHC -> Lula 1-2: a media de FHC vem da PME antiga/PNAD e a de Lula da PME nova; o salto de ~+3,7 pp na troca de metodo eleva a media de Lula 1-2 em relacao a de FHC. Direcao: **prejudica Lula 1-2 na comparacao com FHC** (o numero de Lula esta numa escala que mede mais desemprego); mas o impresso de Lula (8,4 -> 6,5) esta abaixo da media reproduzida em PME nova, o que o **favorece** em termos absolutos. As duas leituras coexistem; nao ha um unico sinal.

## 6. Salario minimo real: troca de deflator

Acumulado real do mandato (media anual a media anual, ano anterior como base) sob quatro deflatores, em %. 'Ipea composto' = IGPC-Mtb ate mar/1979 e INPC depois, com fator 1,2225 em jul/1994. Os campos vazios nao tem o deflator (INPC so desde abr/1979; IPCA desde 1980).

| governo | janela | Ipea composto | IGP-DI unico | INPC unico | IPCA unico | amplitude entre deflatores (pp) | impresso (%) | posicao do impresso |
|---|---|---|---|---|---|---|---|---|
| Ditadura | 1968-1973 | -3,3 | 1,3 | n/d | n/d | 4,7 | 42,8 | acima de todos; **favorece** |
| Itamar | 1992-1994 | 6,1 | -10,6 | 7,8 | 13,0 | 23,6 | -13,9 | abaixo de todos; **prejudica** |
| FHC | 1995-2002 | 47,0 | 18,2 | 44,7 | 46,2 | 28,8 | 4,8 | abaixo de todos; **prejudica** |
| Lula 1-2 | 2003-2010 | 57,3 | 43,3 | 57,3 | 59,2 | 15,9 | 58,5 | dentro da faixa; **indeterminado** |
| Dilma | 2011-2016 | 13,9 | 13,9 | 13,9 | 14,7 | 0,8 | 8,0 | abaixo de todos; **prejudica** |
| Temer | 2016-2018 | 4,5 | 2,8 | 4,5 | 3,8 | 1,7 | 1,1 | abaixo de todos; **prejudica** |
| Bolsonaro | 2019-2022 | -0,9 | -24,6 | -0,9 | 0,3 | 24,8 | 0,9 | acima de todos; **favorece** |
| Lula 3 | 2023-2025 | 10,4 | 22,6 | 10,4 | 9,2 | 13,4 | 12,6 | dentro da faixa; **indeterminado** |

O numero impresso nao reproduz com nenhum deflator em varias janelas (ver `economia-real/RESULTADO.md`, secao 4). A troca de deflator por si so (comparar a serie Ipea composta com o IGP-DI unico) tem sinais diferentes por governo: Ditadura -8,8 pp; Itamar +14,7 pp; FHC +28,8 pp; Bolsonaro +23,6 pp (serie Ipea menos IGP-DI). Nao ha padrao unico.

## 7. IPCA: troca de pesos (estimativas, separadas do dado bruto)

Contrafactuais publicados pelo Banco Central (EE70/2019) e reconstrucao deste dossie por 9 grupos (validada: reproduz o IPCA publicado). **Sao estimativas**; ficam aqui apenas para dar direcao. Efeito = IPCA com a cesta NOVA menos com a cesta ANTERIOR, no mesmo periodo (negativo = inflacao menor com a cesta nova).

| governo | quebra de pesos no mandato | efeito (pp ao ano) | fonte | direcao (inflacao menor = favorece) |
|---|---|---|---|---|
| FHC | POF 1995-96 (ago/1999), 3 anos depois | +0,06 | BCB EE70 | neutro |
| Lula 1-2 | POF 2002-03 (jul/2006), 3 anos depois | -0,34 | BCB EE70 | favorece |
| Dilma | POF 2008-09 (jan/2012), 3 anos depois | -0,56 | BCB EE70 | favorece |
| Itamar | media geometrica no subitem (jan/1994): nao medida (inferencia de composicao: reduz) | n/d | sem contrafactual publicado | indeterminado (nao medido) |
| Temer | so a ampliacao de areas (mai/2018): sem efeito publicado | n/d | sem contrafactual publicado | indeterminado (nao medido) |
| Bolsonaro | POF 2017-18 desde 2020 (2020, 2021, 2022: -0,62, -0,01, -0,68) | -0,44 | reconstrucao deste dossie | favorece |
| Lula 3 | POF 2017-18 (2023, 2024, 2025: +0,32, -0,17, +0,01) | +0,05 | reconstrucao deste dossie | indeterminado (sinais mistos) |

Nao ha sinal consistente: a troca de cesta reduziu a inflacao medida em Lula 1-2, Dilma e Bolsonaro, e fica ambigua em Lula 3 e FHC; Itamar e Temer nao tem efeito medido.

## 8. Resumo por governo: a direcao se repete?

As entradas das secoes 1 a 7 foram agrupadas por FAMILIA de indicador (PIB, IPCA, desemprego, salario minimo, pobreza, Gini, expectativa de vida) para nao contar a mesma familia varias vezes. Dentro da familia, o sinal e o das entradas nao neutras e nao indeterminadas; se ha sinais opostos, a familia e 'misto'. So se diz **consistente** quando o governo tem pelo menos 3 familias com sinal e todas iguais.

| governo | PIB | IPCA | desemprego | salario minimo | pobreza | Gini | expectativa de vida | familias com sinal | leitura |
|---|---|---|---|---|---|---|---|---|---|
| Ditadura | favorece | - | neutro/indeterminado | favorece | neutro/indeterminado | neutro/indeterminado | favorece | 3 | consistente: favorece |
| Itamar | prejudica | favorece | prejudica | misto | neutro/indeterminado | misto | favorece | 4 | nao ha padrao |
| FHC | - | neutro/indeterminado | favorece | prejudica | neutro/indeterminado | favorece | neutro/indeterminado | 3 | nao ha padrao |
| Lula 1-2 | - | favorece | misto | neutro/indeterminado | neutro/indeterminado | favorece | neutro/indeterminado | 2 | nao ha padrao |
| Dilma | - | favorece | neutro/indeterminado | prejudica | favorece | favorece | neutro/indeterminado | 4 | nao ha padrao |
| Temer | prejudica | prejudica | misto | misto | misto | prejudica | neutro/indeterminado | 3 | consistente: prejudica |
| Bolsonaro | - | favorece | prejudica | favorece | favorece | prejudica | neutro/indeterminado | 5 | nao ha padrao |
| Lula 3 | - | neutro/indeterminado | prejudica | neutro/indeterminado | prejudica | prejudica | neutro/indeterminado | 3 | consistente: prejudica |

Sem as celulas ESTIMADAS (secao 7, IPCA por pesos) o veredito de cada governo nao muda. Os vereditos 'consistente' dependem so de dado publicado.

Margem dos vereditos consistentes (numero de familias com sinal): Ditadura = 3, Temer = 3, Lula 3 = 3. O minimo exigido e 3; qualquer celula que mude de sinal desfaz o veredito.

Esta tabela mistura dois tipos de celula: (i) efeito de uma mistura medida (janela, linha, pesquisa, vintage) e (ii) diferenca entre o impresso e a referencia, que inclui numeros que nao reproduzem em nenhuma fonte. A lista por governo e indicador esta em `saida/mistura_direcoes.json`.

## 9. O que este documento nao afirma

- Nao afirma que a mistura foi escolhida para favorecer ou prejudicar ninguem: so mede para que lado ela empurra o numero.
- Onde a direcao muda com a referencia (PIP x SIS, WDI x IBGE vigente, PME antiga x PNAD), a celula fica 'indeterminado'.
- As secoes 7 (IPCA) usam estimativas contrafactuais; as demais usam dado publicado.
