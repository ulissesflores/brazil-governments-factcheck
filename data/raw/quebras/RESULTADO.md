# Quebras de metodo, de regra e de vintage: o que mudou, quanto moveu o numero e o que fica quando o metodo e mantido

Dossie governos-do-brasil-economia. Colheita e calculo de 2026-10-19. Sem opiniao e sem estimativa no dado bruto: onde ha estimativa (contrafactuais de pesos do IPCA, series harmonizadas pelo Ipea), ela vem rotulada e separada.

Legenda: ✅ medido em dado publicado | ⚠️ medido por contrafactual/estimativa rotulada ou so em parte | ❓ nao encontrei / nao li | ❌ nao reproduz.

## 0. Resumo

1. **51 quebras** catalogadas em `quebras.csv`, cada uma com a razao que a PROPRIA fonte da, o trecho literal (verificado por script contra o arquivo baixado), a direcao e como ela foi determinada. Por tipo: mudanca_de_regra = 16, revisao_de_vintage = 14, metodo_estatistico = 21. Por direcao: desconhecida = 21, ambigua = 10, eleva = 11, reduz = 9.

2. **Desemprego**: a troca PME antiga -> PME nova (2002) soma +3,73 p.p. em media nos 10 meses em que as duas rodaram (de +3,13 a +5,14); so +0,66 p.p. disso sao a troca de 'semana' por '30 dias' (mar/2002). PNAD -> PNADC 2012-2014 tem sinal misto (+0,10 p.p. na media anual, -0,17 no 3o trimestre).
3. **Pobreza**: nao existe 'o' numero. A troca de linha/PPC, no mesmo pais, ano e pesquisa, move a pobreza em +8,0 p.p. (5,50/PPC 2011 -> 6,85/PPC 2017, IBGE SIS 2012-2019) e em +2,1 p.p. (6,85 -> 8,30, PIP, 40 anos); a linha de US$ 2,15 -> 3,00 move +3,8 p.p. em media.
4. **Gini**: PNADC fica +0,008 acima da PNAD nos 3 anos de sobreposicao (2012-2014); Censo 2010 fica +0,069 acima da PNAD 2011.
5. **Expectativa de vida**: o mesmo ano muda de valor com a vintage (2000: 68,62 tabua publicada, 70,46 Rev. 2008, 69,8 Rev. 2013, 69,83 Rev. 2018, 71,1 Rev. 2024); a tabua publicada de 2021 diz 77,03 e a vigente 72,8.
6. **Comparacao a metodo constante** (`comparativo-metodo-constante.csv`, 385 linhas): quais governos cabem INTEIROS num unico segmento depende do indicador. IPCA: Collor, Lula 3, Temer. Desemprego: Bolsonaro, Collor, FHC, Itamar Franco, Lula 1-2, Lula 3, Sarney, Temer. PIB: Bolsonaro, Castelo Branco, Costa e Silva + Medici, Dilma, Figueiredo, Geisel, Itamar Franco, Lula 1-2, Lula 3, Sarney, Temer (FHC atravessa 3 vintages de PIB e so cabe parcialmente na referencia 2010 continua, 7 de 8 anos).

7. **Mistura do proprio infografico** (`mistura-do-infografico.md`): por familia de indicador, Ditadura: consistente: favorece (3 familias com sinal); Itamar: nao ha padrao (4 familias com sinal); FHC: nao ha padrao (3 familias com sinal); Lula 1-2: nao ha padrao (2 familias com sinal); Dilma: nao ha padrao (4 familias com sinal); Temer: consistente: prejudica (3 familias com sinal); Bolsonaro: nao ha padrao (5 familias com sinal); Lula 3: consistente: prejudica (3 familias com sinal). Os 3 vereditos 'consistentes' estao na margem minima (3 familias) e nenhum depende de celula estimada. Onde a direcao muda com a referencia (PIP x SIS, linha de pobreza, WDI x IBGE), a celula fica 'indeterminado'.

> [!IMPORTANT]
> **O que NAO foi achado** (detalhe na secao 8): decomposicao do salto PME 2002 alem do periodo de referencia; razao de o PIP dar 18,8% de pobreza em 2020 contra 31,1% no SIS na mesma linha; serie do PIB ref. 1985 e ref. 2000 ano a ano (a tabela do IBGE e imagem); documento da Rev. 2013 do IBGE; PED, RAIS/CAGED e SIM/SINASC (alternativos sem dado baixado); PIP em PPC 2011 (a API devolve erro).

## 1. Entregas e como reproduzir

Tudo roda com `python3 -I`, so le brutos locais (hash em `manifest.jsonl` de cada pasta) e nao usa rede. Ordem: `extrair.py` (texto dos PDFs), `calc.py`, `gerar_pobreza.py`, `gerar_quebras.py`, `gerar_vintage.py`, `gerar_alternativos.py`, `gerar_mistura.py`, `gerar_resultado.py`. As citacoes sao verificadas por `citacoes.py`: uma frase que nao exista literalmente no arquivo local derruba o script.

| arquivo | o que e | linhas |
|---|---|---|
| `quebras.csv` | uma linha por quebra, com `tipo_de_quebra` (metodo_estatistico, mudanca_de_regra ou revisao_de_vintage) | 51 |
| `comparativo-metodo-constante.csv` | segmentos homogeneos x governos, com coluna `vintage` | 385 |
| `vintage-do-infografico.csv` | onde cada numero impresso de pobreza, Gini e expectativa de vida aparece | 24 |
| `mistura-do-infografico.md` | o que o infografico mistura e a direcao medida por governo | 180 |
| `pobreza-leque-series.csv` | TODAS as linhas de pobreza como series separadas (PIP, SIS por edicao, SIDRA, Ipea, WDI), com `vintage` | 665 |
| `pobreza-linhas-historico.csv` | quando e por que cada linha mudou (US$ 1,01 a 8,30; linhas Ipea e do Atlas), com citacao | 17 |
| `pobreza-efeito-mecanico.csv` | efeito de trocar a linha/PPC no mesmo pais-ano-pesquisa | 144 |
| `pobreza-linhas-em-reais-reais.csv` | cada linha internacional em R$ mensais de set/2026 | 9 |
| `bolsa-familia-linhas-elegibilidade.csv` | linhas de elegibilidade 2004-2023 em valor real e em fracao do salario minimo | 10 |
| `renda-por-decil.csv` | medida SEM linha: renda por decil (PIP, PPC 2017 e 2021) | 960 |
| `renda-por-decil-por-governo.csv` | variacao da renda dos decis por governo, separada por spell | 63 |
| `indicadores-alternativos.csv` | para cada indicador, o alternativo que nao depende da regra que mudou | 17 |
| `alternativos-por-governo.csv` | os alternativos baixados, por governo | 103 |

## 2. As quebras, por indicador

| indicador | quebras | tipos | direcoes | apresentada como aprimoramento |
|---|---|---|---|---|
| PIB | 5 | mudanca_de_regra:4, revisao_de_vintage:1 | desconhecida:3, ambigua:1, eleva:1 | sim:4, nao_declarado:1 |
| IPCA | 10 | mudanca_de_regra:2, metodo_estatistico:8 | desconhecida:5, reduz:3, eleva:1, ambigua:1 | nao_declarado:6, sim:4 |
| Desemprego | 7 | metodo_estatistico:7 | desconhecida:3, eleva:3, ambigua:1 | nao_declarado:3, sim:4 |
| Desemprego e Gini | 2 | metodo_estatistico:1, revisao_de_vintage:1 | desconhecida:2 | sim:2 |
| Desemprego, Gini e pobreza | 1 | revisao_de_vintage:1 | desconhecida:1 | sim:1 |
| Salario minimo real | 3 | mudanca_de_regra:3 | desconhecida:1, ambigua:2 | nao_declarado:3 |
| Pobreza | 6 | mudanca_de_regra:4, revisao_de_vintage:2 | eleva:3, reduz:1, ambigua:1, desconhecida:1 | sim:2, nao_declarado:4 |
| Pobreza e Gini | 4 | metodo_estatistico:3, revisao_de_vintage:1 | desconhecida:1, reduz:1, eleva:1, ambigua:1 | sim:2, nao_declarado:2 |
| Gini | 2 | revisao_de_vintage:1, metodo_estatistico:1 | reduz:1, eleva:1 | nao_declarado:2 |
| Expectativa de vida | 6 | revisao_de_vintage:6 | reduz:3, desconhecida:1, ambigua:1, eleva:1 | sim:4, nao_declarado:2 |
| Agregados monetarios | 4 | mudanca_de_regra:2, metodo_estatistico:1, revisao_de_vintage:1 | desconhecida:2, ambigua:2 | nao_declarado:1, sim:2, nao:1 |
| Agregados monetarios e salario minimo | 1 | mudanca_de_regra:1 | desconhecida:1 | nao_declarado:1 |

A fonte apresenta 25 das 51 quebras como aprimoramento (recomendacao da OIT na PME, manual da ONU no PIB, novos PPCs do ICP na pobreza); 25 nao declaram se e aprimoramento e 1 diz expressamente que nao (rotulagem do Ipeadata). A propria fonte so mede o efeito em poucos casos (PIB 2007 e 2015, NT 48 do BCB, contrafactuais do BCB para o IPCA).

## 3. O que foi MEDIDO na sobreposicao, e a direcao

Direcao = efeito do metodo/linha/vintage NOVO sobre o valor medido (eleva = o novo valor e maior).

| quebra | onde sobrepoe | efeito | direcao | status |
|---|---|---|---|---|
| PME antiga (30 dias, 15+) -> PME nova | mar-dez/2002, 6 RMs | +3,73 p.p. (de +3,13 a +5,14); decomposicao: periodo de referencia +0,66 / +0,67 (mar e nov), resto +5,14 / +3,13 | eleva | ✅ |
| PNAD (set., 10+) -> PNADC (14+) | 2012-2014 | +0,10 p.p. (media anual) e -0,17 p.p. (3o tri); por ano: +0,38, -0,15, -0,74 | ambigua | ✅ |
| Gini PNAD -> PNADC | 2012-2014 | +0,008 (os 3 anos positivos) | eleva | ✅ |
| Gini PNAD -> Censo | 2009-2011 | +0,057 (vs 2009) e +0,069 (vs 2011) | eleva | ✅ (so 1 Censo na janela) |
| Linha 5,50 (PPC 2011) -> 6,85 (PPC 2017) | 2012-2019, IBGE SIS | +8,01 p.p. (de 7,59 a 8,27) | eleva | ✅ (mistura edicoes SIS 2020 x 2025) |
| US$ 2.15 (PPC 2017) -> US$ 3.00 (PPC 2021) | 1981-2024, PIP | +3,76 p.p. em media (de +0,82 a +7,15; 40 anos) | eleva | ✅ |
| US$ 3.65 (PPC 2017) -> US$ 4.20 (PPC 2021) | 1981-2024, PIP | +0,20 p.p. em media (de +0,06 a +0,55; 40 anos) | eleva | ✅ |
| US$ 6.85 (PPC 2017) -> US$ 8.30 (PPC 2021) | 1981-2024, PIP | +2,09 p.p. em media (de +1,68 a +2,53; 40 anos) | eleva | ✅ |
| PIP x IBGE SIS, mesma linha 6,85 | 2012-2024 | -7,00 p.p. (-6,57 sem 2020); 2020: PIP 18,8 contra SIS 31,1 | reduz | ✅ causa ❓ |
| SIS edicoes (5,50, ano 2017) | SIS 2018 x 2019/2020 | 26,47 -> 26,00 (-0,47 p.p.) | reduz | ✅ |
| Rev. 2013 -> Rev. 2018 (e0) | 2000-2014 | maximo 0,05 ano | neutro | ✅ |
| Tabua publicada -> serie vigente (e0) | 2000, 2010, 2019-2024 | 2000 +2,48, 2010 +0,92, 2019 -0,35, 2020 -1,99, 2021 -4,23, 2022 -0,05, 2023 +0,01, 2024 -0,01 anos | ambigua | ✅ |
| M1-M4 metodologia 2001 -> Novo (2018) | 2002-2018 | dez/2017: M1 +5,2%, M2 +3,9%, M3 -0,4%, M4 -6,2% | ambigua | ✅ |
| PIB ref. 2000 -> ref. 2010 | 2000-2011, IBGE | media anual 3,5% -> 3,7% (+0,2 p.p. ao ano); nivel +2,1% | eleva | ✅ (media; tabela ano a ano e imagem) |
| PIB ref. 1985 -> ref. 2000 | 2000 e 2005, IBGE | 2000: 4,4 -> 4,3; 2005: 2,3 -> 2,9 | ambigua | ⚠️ (2 pontos em texto) |
| IPCA, troca de POF (1999, 2006, 2012, 2020) | Banco Central EE70 | 1999 +0,71 antes / +0,06 depois; 2006 +0,40 / -0,34; 2012 -0,49 / -0,56; 2017-2019 -0,09 p.p. ao ano | ambigua | ⚠️ contrafactual do BCB |
| IPCA, cesta POF 2017-18 (2020-2025) | reconstrucao por 9 grupos (SIDRA 1419/7060) | por ano: -0,62, -0,01, -0,68, +0,32, -0,17, +0,01 p.p.; acumulado 2020-2025: 40,6% (cesta antiga) contra 39,1% (nova) | reduz em media, sinal nao se repete | ⚠️ estimativa deste dossie (reproduz o publicado: 2018 em 3,744 contra 3,745) |
| Salario minimo: fator 1,2225 de jul/1994 | serie Ipea x nominal/INPC | Itamar -1,8% contra -0,3%; FHC +47,0% contra +44,7% | ambigua | ✅ |

Sem sobreposicao nos dados baixados (e portanto sem efeito medido): FGV -> IBGE em 1990; ref. 1985 -> ref. 2010 em 1995/1996; estruturas do IPCA de 1989, 1991, formula geometrica de 1994 e cobertura de 2014/2018; PME 1982/1988/1993; conceito de trabalho da PNAD em 1992; area rural do Norte em 2004; reponderacao da PNAD 2001-2009; telefone da PNADC (2020-21); reponderacao de nov/2021; quintas visitas 2020-2022; M0 de 1980; faixas regionais do salario minimo.

## 4. Comparativo a metodo constante (media / variacao no segmento, n anos)

Cada coluna e UM metodo e UM intervalo de anos. 'media / variacao (n)': media das taxas ou dos niveis anuais; variacao = crescimento acumulado (PIB, IPCA, salario) ou ultimo menos primeiro ano (demais, em pp, pontos ou anos); n = anos usados; `*` = governo so parcialmente dentro do segmento ou com lacunas. So a janela do mandato (cada ano ao governo que o exerceu na maior parte); as janelas impressas estao no CSV.

### 4.1 PIB real (% a.a.; acumulado %)

| governo | FGV 1948-90 | ref.1985 1991-95 | ref.2010 retrop. 1996-2000 | ref.2010 2001-25 | ref.2010 continua 1996-2025 |
|---|---|---|---|---|---|
| Castelo Branco | 4,17 / +12,98 (n=3) | - | - | - | - |
| Costa e Silva + Medici | 10,16 / +96,47 (n=7) | - | - | - | - |
| Geisel | 6,70 / +38,14 (n=5) | - | - | - | - |
| Figueiredo | 2,50 / +15,15 (n=6) | - | - | - | - |
| Sarney | 4,39 / +23,74 (n=5) | - | - | - | - |
| Collor | - | 0,24 / +0,48 (n=2)* | - | - | - |
| Itamar Franco | - | 5,39 / +11,07 (n=2) | - | - | - |
| FHC | - | - | 2,16 / +11,21 (n=5)* | 2,22 / +4,49 (n=2)* | 2,18 / +16,20 (n=7)* |
| Lula 1-2 | - | - | - | 4,08 / +37,39 (n=8) | 4,08 / +37,39 (n=8) |
| Dilma | - | - | - | 0,43 / +2,35 (n=6) | 0,43 / +2,35 (n=6) |
| Temer | - | - | - | 1,55 / +3,13 (n=2) | 1,55 / +3,13 (n=2) |
| Bolsonaro | - | - | - | 1,43 / +5,66 (n=4) | 1,43 / +5,66 (n=4) |
| Lula 3 | - | - | - | 2,98 / +9,21 (n=3) | 2,98 / +9,21 (n=3) |

### 4.2 IPCA (% a.a.; acumulado %)

| governo | 81-85 Endef | 87-88 base mar/86 | 90-93 POF87 | 94-98 geom. | 00-05 POF95 | 07-11 POF02 | 12-19 POF08 | 20-25 POF17 |
|---|---|---|---|---|---|---|---|---|
| Figueiredo | 144,94 / +3235,25 (n=4)* | - | - | - | - | - | - | - |
| Sarney | - | 671,82 / +4905,89 (n=2)* | - | - | - | - | - | - |
| Collor | - | - | 1070,91 / +120050,35 (n=3) | - | - | - | - | - |
| FHC | - | - | - | 9,71 / +43,46 (n=4)* | 8,73 / +28,40 (n=3)* | - | - | - |
| Lula 1-2 | - | - | - | - | 7,53 / +24,30 (n=3)* | 5,14 / +22,21 (n=4)* | - | - |
| Dilma | - | - | - | - | - | - | 7,02 / +40,31 (n=5)* | - |
| Temer | - | - | - | - | - | - | 3,35 / +6,80 (n=2) | - |
| Bolsonaro | - | - | - | - | - | - | - | 6,79 / +21,69 (n=3)* |
| Lula 3 | - | - | - | - | - | - | - | 4,57 / +14,35 (n=3) |

### 4.3 Desemprego (%; variacao em pp)

| governo | PME antiga 80-02 | PME nova 03-15 | PNAD 92-03 | PNAD 04-14 | PNADC 12-25 |
|---|---|---|---|---|---|
| Figueiredo | 7,41 / +1,65 (n=5)* | - | - | - | - |
| Sarney | 4,36 / -2,27 (n=5) | - | - | - | - |
| Collor | 5,35 / +1,49 (n=3) | - | - | - | - |
| Itamar Franco | 5,59 / -0,31 (n=2) | - | 6,80 (n=1)* | - | - |
| FHC | 7,01 / +2,92 (n=8) | - | 8,97 / +3,19 (n=7)* | - | - |
| Lula 1-2 | - | 9,46 / -5,61 (n=8) | - | 9,14 / -0,67 (n=6)* | - |
| Dilma | - | 5,70 / +0,89 (n=5)* | - | 7,17 / +0,25 (n=4)* | 8,44 / +4,20 (n=5)* |
| Temer | - | - | - | - | 12,35 / -0,50 (n=2) |
| Bolsonaro | - | - | - | - | 12,28 / -2,20 (n=4) |
| Lula 3 | - | - | - | - | 6,63 / -2,10 (n=3) |

### 4.4 Salario minimo real (var. % a.a. da media anual; acumulado %)

| governo | Ipea IGPC-Mtb 48-78 | Ipea INPC 80-25 | IGP-DI unico 44-25 | INPC unico 80-25 | IPCA unico 81-25 |
|---|---|---|---|---|---|
| Castelo Branco | -4,94 / -16,09 (n=3) | - | -3,05 / -8,92 (n=3) | - | - |
| Costa e Silva + Medici | -1,49 / -10,24 (n=7) | - | -0,19 / -1,45 (n=7) | - | - |
| Geisel | 0,74 / +3,59 (n=5) | - | 0,63 / +2,67 (n=5) | - | - |
| Figueiredo | - | -4,34 / -16,69 (n=4)* | -6,51 / -34,24 (n=6) | -4,33 / -16,68 (n=4)* | -5,08 / -14,63 (n=3)* |
| Sarney | - | -1,49 / -9,11 (n=5) | -3,01 / -15,57 (n=5) | -1,50 / -9,11 (n=5) | -3,51 / -18,27 (n=5) |
| Collor | - | -7,34 / -23,06 (n=3) | -5,65 / -18,52 (n=3) | -7,34 / -23,06 (n=3) | -7,68 / -24,70 (n=3) |
| Itamar Franco | - | -0,34 / -1,81 (n=2) | -7,88 / -16,48 (n=2) | 0,36 / -0,26 (n=2) | 1,52 / +2,19 (n=2) |
| FHC | - | 5,00 / +47,03 (n=8) | 2,22 / +18,21 (n=8) | 4,78 / +44,74 (n=8) | 4,93 / +46,25 (n=8) |
| Lula 1-2 | - | 5,89 / +57,27 (n=8) | 4,77 / +43,30 (n=8) | 5,89 / +57,26 (n=8) | 6,03 / +59,18 (n=8) |
| Dilma | - | 2,23 / +13,88 (n=6) | 2,23 / +13,88 (n=6) | 2,23 / +13,88 (n=6) | 2,35 / +14,67 (n=6) |
| Temer | - | 1,18 / +2,33 (n=2) | 0,86 / +1,52 (n=2) | 1,18 / +2,33 (n=2) | 0,57 / +1,09 (n=2) |
| Bolsonaro | - | -0,21 / -0,91 (n=4) | -6,54 / -24,55 (n=4) | -0,21 / -0,91 (n=4) | 0,08 / +0,27 (n=4) |
| Lula 3 | - | 3,34 / +10,36 (n=3) | 7,11 / +22,64 (n=3) | 3,34 / +10,36 (n=3) | 2,99 / +9,24 (n=3) |

### 4.5 Pobreza (% da populacao; variacao em pp), PIP, uma coluna por linha e spell

**Spell PNAD (1981-2011)**

| governo | 2,15/PPC17 | 3,65/PPC17 | 6,85/PPC17 | 3,00/PPC21 | 4,20/PPC21 | 8,30/PPC21 |
|---|---|---|---|---|---|---|
| Figueiredo | 27,2 / +6,0 (n=4)* | 46,7 / +7,3 (n=4)* | 69,4 / +5,2 (n=4)* | 34,1 / +6,2 (n=4)* | 46,9 / +7,3 (n=4)* | 71,3 / +5,1 (n=4)* |
| Sarney | 20,2 / -5,3 (n=5) | 36,7 / -8,8 (n=5) | 59,3 / -9,6 (n=5) | 25,7 / -6,8 (n=5) | 37,0 / -8,9 (n=5) | 61,3 / -9,7 (n=5) |
| Collor | 23,6 / -0,7 (n=2)* | 41,2 / -0,9 (n=2)* | 64,6 / +1,7 (n=2)* | 29,9 / -0,9 (n=2)* | 41,4 / -0,9 (n=2)* | 66,8 / +2,1 (n=2)* |
| Itamar Franco | 22,1 (n=1)* | 39,6 (n=1)* | 64,3 (n=1)* | 28,2 (n=1)* | 39,9 (n=1)* | 66,0 (n=1)* |
| FHC | 14,4 / -3,0 (n=7)* | 28,6 / -4,3 (n=7)* | 51,3 / -5,3 (n=7)* | 19,1 / -3,3 (n=7)* | 28,9 / -4,2 (n=7)* | 53,6 / -5,0 (n=7)* |
| Lula 1-2 | 8,9 / -6,5 (n=7)* | 20,1 / -11,5 (n=7)* | 41,6 / -14,8 (n=7)* | 12,3 / -8,7 (n=7)* | 20,3 / -11,4 (n=7)* | 43,9 / -14,6 (n=7)* |

**Spell PNADC (2012-2024)**

| governo | 2,15/PPC17 | 3,65/PPC17 | 6,85/PPC17 | 3,00/PPC21 | 4,20/PPC21 | 8,30/PPC21 |
|---|---|---|---|---|---|---|
| Dilma | 4,0 / +0,3 (n=5)* | 9,7 / +0,0 (n=5)* | 26,1 / -1,1 (n=5)* | 5,7 / +0,1 (n=5)* | 9,9 / +0,1 (n=5)* | 28,2 / -1,3 (n=5)* |
| Temer | 5,3 / +0,0 (n=2) | 11,0 / -0,1 (n=2) | 27,0 / -0,4 (n=2) | 6,9 / -0,1 (n=2) | 11,1 / -0,1 (n=2) | 29,0 / -0,6 (n=2) |
| Bolsonaro | 4,2 / -1,9 (n=4) | 8,9 / -2,4 (n=4) | 24,2 / -2,9 (n=4) | 5,5 / -2,2 (n=4) | 9,1 / -2,4 (n=4) | 26,2 / -2,7 (n=4) |
| Lula 3 | 2,3 / -0,7 (n=2)* | 6,7 / -1,2 (n=2)* | 20,3 / -2,7 (n=2)* | 3,4 / -0,8 (n=2)* | 6,8 / -1,2 (n=2)* | 22,0 / -2,6 (n=2)* |

**Segunda linha: IBGE SIS (PNADC)** e Ipea (PNAD, linha propria)

| governo | SIS 5,50/PPC11 | SIS 6,85/PPC17 | SIS 3,65/PPC17 | ODS 8,30/PPC21 | Ipea PPY (PNAD) |
|---|---|---|---|---|---|
| Geisel | - | - | - | - | 41,3 / +0,6 (n=3)* |
| Figueiredo | - | - | - | - | 43,5 / +9,6 (n=5)* |
| Sarney | - | - | - | - | 38,4 / -0,7 (n=5) |
| Collor | - | - | - | - | 42,0 / +0,2 (n=2)* |
| Itamar Franco | - | - | - | - | 43,0 (n=1)* |
| FHC | - | - | - | - | 34,8 / -0,7 (n=7)* |
| Lula 1-2 | - | - | - | - | 28,1 / -14,3 (n=7)* |
| Dilma | 24,7 / -0,9 (n=5)* | 32,7 / -1,0 (n=5)* | 13,4 / +0,0 (n=5)* | 34,9 / -0,7 (n=5)* | 15,7 / -5,1 (n=4)* |
| Temer | 25,6 / -0,7 (n=2) | 33,6 / -0,3 (n=2) | 14,7 / -0,3 (n=2) | 36,0 / -1,1 (n=2) | - |
| Bolsonaro | - | 33,0 / -1,0 (n=4) | 13,9 / -1,8 (n=4) | 35,1 / -0,8 (n=4) | - |
| Lula 3 | - | 25,2 / -4,2 (n=2)* | 9,4 / -1,7 (n=2)* | 28,1 / -3,3 (n=2)* | - |

### 4.6 Gini

| governo | PIP PNAD 81-11 | PIP PNADC 12-24 | PIP unica 81-24 | SIS PNADC | Ipea PGINI (PNAD) | Ipea harmonizada |
|---|---|---|---|---|---|---|
| Geisel | - | - | - | - | 0,617 / -0,019 (n=3)* | - |
| Figueiredo | 0,584 / +0,004 (n=4)* | - | 0,584 / +0,004 (n=4)* | - | 0,591 / -0,004 (n=5)* | - |
| Sarney | 0,596 / +0,077 (n=5) | - | 0,596 / +0,077 (n=5) | - | 0,608 / +0,038 (n=5) | - |
| Collor | 0,568 / -0,074 (n=2)* | - | 0,568 / -0,074 (n=2)* | - | 0,598 / -0,031 (n=2)* | - |
| Itamar Franco | 0,601 (n=1)* | - | 0,601 (n=1)* | - | 0,604 (n=1)* | - |
| FHC | 0,592 / -0,014 (n=7)* | - | 0,592 / -0,014 (n=7)* | - | 0,598 / -0,011 (n=7)* | 0,612 / -0,012 (n=7)* |
| Lula 1-2 | 0,555 / -0,039 (n=7)* | - | 0,555 / -0,039 (n=7)* | - | 0,562 / -0,040 (n=7)* | 0,574 / -0,042 (n=7)* |
| Dilma | - | 0,527 / -0,001 (n=5)* | 0,527 / +0,004 (n=6) | 0,532 / -0,002 (n=5)* | - | 0,534 / -0,006 (n=6) |
| Temer | - | 0,536 / +0,006 (n=2) | 0,536 / +0,006 (n=2) | 0,542 / +0,007 (n=2) | - | 0,542 / +0,007 (n=2) |
| Bolsonaro | - | 0,518 / -0,016 (n=4) | 0,518 / -0,016 (n=4) | 0,532 / -0,026 (n=4) | - | 0,532 / -0,026 (n=4) |
| Lula 3 | - | 0,509 / -0,012 (n=2)* | 0,509 / -0,012 (n=2)* | 0,510 / -0,012 (n=2)* | - | 0,511 / -0,005 (n=3) |

### 4.7 Expectativa de vida (anos; variacao em anos)

| governo | UMA vintage (WDI/UN) 1960-2024 | tabua como publicada | Rev. 2018 (Ipea) | Rev. 2013 (SIDRA) |
|---|---|---|---|---|
| Castelo Branco | 55,24 / +0,78 (n=3) | - | - | - |
| Costa e Silva + Medici | 57,35 / +2,67 (n=7) | - | - | - |
| Geisel | 60,01 / +1,84 (n=5) | - | - | - |
| Figueiredo | 62,47 / +2,19 (n=6) | - | - | - |
| Sarney | 64,77 / +1,53 (n=5) | - | - | - |
| Collor | 66,20 / +0,68 (n=3) | - | - | - |
| Itamar Franco | 67,09 / +0,40 (n=2) | - | - | - |
| FHC | 69,04 / +2,69 (n=8) | - | 70,28 / +0,90 (n=3)* | 70,27 / +0,90 (n=3)* |
| Lula 1-2 | 72,43 / +2,90 (n=8) | 72,72 / +1,53 (n=2)* | 72,55 / +2,70 (n=8) | 72,56 / +2,70 (n=8) |
| Dilma | 74,67 / +1,03 (n=6) | 75,49 / +0,57 (n=3)* | 74,98 / +1,52 (n=6) | 74,65 / +0,90 (n=4)* |
| Temer | 75,51 / +0,25 (n=2) | 76,18 / +0,26 (n=2) | 76,12 / +0,26 (n=2) | - |
| Bolsonaro | 74,56 / -0,94 (n=4) | 76,45 / -1,10 (n=4) | 76,85 / +0,69 (n=4) | - |
| Lula 3 | 75,94 / +0,17 (n=2)* | 76,50 / +0,22 (n=2)* | - | - |

### 4.8 Agregados monetarios (% do PIB)

| governo | M0 47-79 | M0 80-25 | M1 antigo | M1 Novo | M2 2001 | M2 Novo | M3 2001 | M3 Novo | M4 2001 | M4 Novo |
|---|---|---|---|---|---|---|---|---|---|---|
| Castelo Branco | 6,6 / -0,2 (n=3) | - | 15,0 / +0,7 (n=3) | - | - | - | - | - | - | - |
| Costa e Silva + Medici | 5,4 / -1,9 (n=7) | - | 15,4 / -0,5 (n=7) | - | - | - | - | - | - | - |
| Geisel | 3,7 / +0,2 (n=5) | - | 12,3 / -3,4 (n=5) | - | - | - | - | - | - | - |
| Figueiredo | - | 2,6 / -1,5 (n=5)* | 7,1 / -5,5 (n=6) | - | - | - | - | - | - | - |
| Sarney | - | 2,1 / -0,2 (n=5) | 4,6 / -1,7 (n=5) | - | - | - | - | - | - | - |
| Collor | - | 1,8 / -1,1 (n=3) | 3,0 / -1,6 (n=3) | - | 14,8 / +7,0 (n=3) | - | 16,4 / +10,3 (n=3) | - | 20,4 / +8,2 (n=3) | - |
| Itamar Franco | - | 1,5 / +1,0 (n=2) | 2,2 / +1,1 (n=2) | - | 21,9 / +1,9 (n=2) | - | 25,7 / +2,4 (n=2) | - | 30,4 / +3,7 (n=2) | - |
| FHC | - | 3,0 / +1,5 (n=8) | 4,3 / +2,8 (n=8) | - | 22,6 / +1,4 (n=8) | - | 36,9 / +17,3 (n=8) | - | 43,9 / +21,3 (n=8) | - |
| Lula 1-2 | - | 4,0 / +0,6 (n=8) | 5,8 / +1,0 (n=8) | 6,0 / +1,0 (n=8) | 26,6 / +8,6 (n=8) | 26,8 / +9,0 (n=8) | 53,0 / +16,5 (n=8) | 53,4 / +20,0 (n=8) | 61,5 / +21,4 (n=8) | 60,3 / +21,5 (n=8) |
| Dilma | - | 4,1 / -0,3 (n=6) | 5,4 / -0,9 (n=6) | 5,6 / -0,9 (n=6) | 35,0 / +2,7 (n=6) | 35,7 / +3,1 (n=6) | 71,1 / +16,4 (n=6) | 73,0 / +14,8 (n=6) | 83,0 / +18,4 (n=6) | 79,2 / +14,9 (n=6) |
| Temer | - | 3,9 / -0,0 (n=2) | - | 5,2 / +0,1 (n=2) | - | 38,0 / +0,6 (n=2) | - | 85,0 / +0,8 (n=2) | - | 91,8 / +1,1 (n=2) |
| Bolsonaro | - | 4,3 / +0,1 (n=4) | - | 6,2 / +0,8 (n=4) | - | 44,4 / +6,8 (n=4) | - | 92,4 / +4,0 (n=4) | - | 99,3 / +6,9 (n=4) |
| Lula 3 | - | 3,6 / -0,2 (n=3) | - | 5,3 / -0,5 (n=3) | - | 52,4 / +4,9 (n=3) | - | 97,3 / +6,2 (n=3) | - | 107,5 / +7,2 (n=3) |

## 5. Pobreza: o leque de linhas, quando e por que cada uma mudou, e a medida sem linha

### 5.1 Linhas e datas

| linha | PPC | vigencia | razao declarada | efeito declarado pela fonte |
|---|---|---|---|---|
| US$ 1,01/dia (conhecida como 'um dolar por dia') | PPC 1985 | 1990 (World Development Report 1990) a 1996-2000 (atualizada p/ 1,08) | linha baseada em amostra de linhas nacionais de pobreza (Ravallion, Datt e van de Walle, 1991) | n/d na fonte lida |
| US$ 1,08/dia | PPC 1993 | Chen e Ravallion (2001) a ate a adocao da linha de 1,25 (2009) | atualizacao com os PPCs de 1993 (mediana das 10 menores linhas nacionais da amostra RDW) | contagem global de 1993: 1,3 bilhao (linha 1,08/PPC 1993) contra 1,8 bilhao (linha 1,25/PPC 2005) |
| US$ 1,25/dia | PPC 2005 | 2009 a 2015 (adocao da linha de 1,90) | novos PPCs de 2005 e novo conjunto de linhas nacionais (Ravallion, Chen e Sangraula, 2009) | ver linha anterior (1,3 -> 1,8 bilhao em 1993) |
| US$ 1,90/dia | PPC 2011 | 2015 (PRWP 7432 e de out/2015; data exata de adocao nao lida) a set/2022 | novos PPCs de 2011; mesma definicao das 15 linhas nacionais de Ravallion et al. (2009), preservando o poder de compra da linha anterior nos paises pobres | o nivel de pobreza com a nova linha e os novos PPCs e semelhante ao estimado com PPC 2005 e linha de 1,25 |
| US$ 2,00/dia ('dois dolares por dia') | PPC 2005 | c. 2008-2009 a substituida pela linha de 3,10 (PPC 2011), depois 3,20 | linha 'comumente usada para paises de renda media'; seu equivalente em PPC 2011 foi proposto como US$ 3,10 | n/d |
| US$ 3,20/dia (renda media baixa) | PPC 2011 | data de adocao nao lida (a metodologia e de Jolliffe e Prydz, 2016) a set/2022 | mesma metodologia da linha extrema (mediana das linhas nacionais harmonizadas), aplicada a paises de renda media baixa | n/d |
| US$ 5,50/dia (renda media alta) | PPC 2011 | data de adocao nao lida a set/2022 | idem, para paises de renda media alta | n/d |
| US$ 2,15/dia | PPC 2017 | set/2022 ('fall 2022'; versao 20220909 do PIP) a jun/2025 | lancamento dos PPCs de 2017 (ICP, 2020) e nova metodologia: mediana das linhas nacionais harmonizadas dos paises de renda baixa | US$ 2,17 seria a linha que mantem constante a pobreza GLOBAL em 2017; o 2,15 arredonda isso. 'In nominal terms, it is a quarter of a dollar higher' |
| US$ 3,65/dia | PPC 2017 | set/2022 a jun/2025 | dados atualizados das linhas nacionais; arredondamento a 5 centavos | n/d |
| US$ 6,85/dia | PPC 2017 | set/2022 a jun/2025 | idem | n/d |
| US$ 3,00/dia | PPC 2021 | 2025-06-09 (data do blog; PIP de jun/2025) a vigente | novos PPCs de 2021 (ICP, 2024) e base maior de linhas nacionais (1.747 linhas em 163 paises, contra 1.381 em 157) | +125 milhoes de pessoas na pobreza extrema global em 2022 so pela redefinicao; a fonte diz que a mudanca nao reflete 'ambicoes crescentes' e sim custo |
| US$ 4,20/dia | PPC 2021 | 2025-06-09 a vigente | idem | n/d |
| US$ 8,30/dia | PPC 2021 | 2025-06-09 a vigente | idem | n/d |
| linha propria: 2 x linha de extrema pobreza (cesta FAO), 24 regioes | reais de cada regiao/epoca | 1976 a 2014 (serie interrompida) | linha de pobreza = dobro da linha de extrema pobreza, que e o valor de uma cesta de alimentos com o minimo de calorias (FAO/OMS) | n/d |
| 50% do salario minimo de 1/set/1991 | reais de set/1991 | Censos 1970, 1980, 1991 a serie parada em 1991 | Atlas do Desenvolvimento Humano no Brasil 1998 | n/d |
| R$ 140 (pobreza) e R$ 70 (extrema pobreza), valores de ago/2010 | reais de ago/2010 | Censo 1991 a Censo 2010 | linhas do Atlas do Desenvolvimento Humano, ancoradas nos valores do Bolsa Familia de 2009-2010 (mesmos R$ 140 e R$ 70 do Decreto 6.917/2009) | n/d |
| US$ 8,30/dia (PPC 2021), chamada 'linha nacional' dos ODS | R$ 2,44983620 por US$ PPC 2021 (consumo final) | serie 2012-2024 na revisao de 2026 a vigente | acompanhamento dos Objetivos de Desenvolvimento Sustentavel; consolidado das primeiras entrevistas de 2012-2019 e 2023-2024 e das quintas entrevistas de 2020-2022 | n/d |

### 5.2 O valor REAL das linhas internacionais (R$ mensais de set/2026, IPCA)

| linha | fator R$ por US$ PPC | R$/mes no ano-base | R$/mes em set/2026 |
|---|---|---|---|
| US$ 1.90 (PPC 2011) | 1.66 | 95.93 | 222.3 |
| US$ 3.20 (PPC 2011) | 1.66 | 161.57 | 374.4 |
| US$ 5.50 (PPC 2011) | 1.66 | 277.7 | 643.49 |
| US$ 2.15 (PPC 2017) | 2.3273771 | 152.2 | 241.59 |
| US$ 3.65 (PPC 2017) | 2.3273771 | 258.39 | 410.14 |
| US$ 6.85 (PPC 2017) | 2.3273771 | 484.92 | 769.72 |
| US$ 3.00 (PPC 2021) | 2.4498362 | 223.55 | 295.2 |
| US$ 4.20 (PPC 2021) | 2.4498362 | 312.97 | 413.28 |
| US$ 8.30 (PPC 2021) | 2.4498362 | 618.48 | 816.73 |

Em termos reais a troca 5,50 (PPC 2011) -> 6,85 (PPC 2017) eleva a linha em reais de R$ 643 para R$ 770 (+20%) e a troca 6,85 -> 8,30 (PPC 2021), de R$ 770 para R$ 817 (+6%): a linha em dolares sobe mais do que o valor real em reais porque os PPCs mudam junto.

### 5.3 Efeito mecanico da troca de linha/PPC (mesmo pais, ano e pesquisa)

| troca | fonte | media (pp) | minimo | maximo | anos |
|---|---|---|---|---|---|
| US$ 2.15 (PPC 2017) -> US$ 3.00 (PPC 2021) | PIP | +3,76 | +0,82 | +7,15 | 40 |
| US$ 3.65 (PPC 2017) -> US$ 4.20 (PPC 2021) | PIP | +0,20 | +0,06 | +0,55 | 40 |
| US$ 6.85 (PPC 2017) -> US$ 8.30 (PPC 2021) | PIP | +2,09 | +1,68 | +2,53 | 40 |
| US$ 1,90 (PPC 2011) -> US$ 2,15 (PPC 2017) | IBGE SIS | +0,81 | +0,70 | +0,90 | 8 |
| US$ 3,20 (PPC 2011) -> US$ 3,65 (PPC 2017) | IBGE SIS | +2,16 | +1,90 | +2,48 | 8 |
| US$ 5,50 (PPC 2011) -> US$ 6,85 (PPC 2017) | IBGE SIS | +8,01 | +7,59 | +8,27 | 8 |

Positivo = pessoas que PASSAM a ser contadas como pobres so pela redefinicao. Por governo (6,85 -> 8,30, PIP): Bolsonaro +1,94 pp; Collor +2,27 pp; Dilma +2,11 pp; FHC +2,23 pp; Figueiredo +1,85 pp; Itamar Franco +1,70 pp; Lula 1-2 +2,34 pp; Lula 3 +1,70 pp; Sarney +2,00 pp; Temer +2,00 pp.

### 5.4 Linha de elegibilidade do Bolsa Familia / Auxilio Brasil, em valor real

| inicio dos efeitos | pobreza nominal (R$) | extrema nominal (R$) | pobreza em R$ de set/2026 (INPC) | % do salario minimo | instrumento |
|---|---|---|---|---|---|
| 2004-09 | 100 | 50 | 324,79 | 38,5 | Decreto 5.209, de 17/09/2004 (art. 18, redacao original) |
| 2006-04 | 120 | 60 | 361,99 | 34,3 | Decreto 5.749, de 11/04/2006 (em vigor na publicacao, DOU 12/04/2006) |
| 2009-04 | 137 | 69 | 356,50 | 29,5 | Decreto 6.824, de 16/04/2009 (em vigor na publicacao) |
| 2009-09 | 140 | 70 | 358,93 | 30,1 | Decreto 6.917, de 30/07/2009 (efeitos financeiros desde 01/09/2009) |
| 2014-06 | 154 | 77 | 297,92 | 21,3 | Decreto 8.232, de 30/04/2014 (efeitos financeiros desde 01/06/2014) |
| 2016-07 | 170 | 85 | 273,02 | 19,3 | Decreto 8.794, de 29/06/2016 (efeitos financeiros desde 01/07/2016) |
| 2018-07 | 178 | 89 | 270,29 | 18,7 | Decreto 9.396, de 30/05/2018 (em vigor em 01/07/2018) |
| 2021-11 | 200 | 100 | 250,58 | 18,2 | Auxilio Brasil: Decreto 10.852, de 08/11/2021 (art. 20) - OUTRO PROGRAMA |
| 2022-03 | 210 | 105 | 252,58 | 17,3 | Auxilio Brasil: Decreto 11.013, de 29/03/2022 (em vigor na publicacao) |
| 2023-06 | 218 | (linha unica) | 249,27 | 16,5 | Bolsa Familia reinstituido: Lei 14.601, de 19/06/2023 (conversao da MP 1 |

O Auxilio Brasil (nov/2021 a 2023) e outro programa, e a linha de 2023 (R$ 218) e unica. Os valores reais saem do deflator INPC (SGS 188); a norma foi lida no Planalto em 2026-10-19.

### 5.5 Medida SEM linha: renda domiciliar per capita real por decil (PIP, PPC 2017), variacao dentro de cada spell

| governo | spell | anos usados | decil 1 | mediana | media | decil 10 | cobertura |
|---|---|---|---|---|---|---|---|
| Figueiredo | PNAD | 1981-1984 | -10,6% | -16,8% | -14,5% | -13,3% | PARCIAL ( |
| Sarney | PNAD | 1985-1989 | +4,5% | +29,1% | +60,7% | +93,2% | inteira |
| Collor | PNAD | 1990-1992 | -12,1% | +0,6% | -20,4% | -34,3% | inteira |
| FHC | PNAD | 1995-2002 | +21,9% | +15,4% | +9,2% | +6,0% | inteira |
| Lula 1-2 | PNAD | 2003-2009 | +57,3% | +42,2% | +27,4% | +18,3% | inteira |
| Dilma | PNADC | 2012-2016 | -1,7% | +2,9% | +3,0% | +2,2% | PARCIAL ( |
| Temer | PNADC | 2017-2018 | +0,4% | +2,3% | +3,5% | +4,9% | inteira |
| Bolsonaro | PNADC | 2019-2022 | +27,4% | +1,2% | +0,9% | -1,7% | inteira |
| Lula 3 | PNADC | 2023-2024 | +11,7% | +7,2% | +4,3% | +0,9% | PARCIAL ( |

Variacao % da renda real (PPC$/dia) entre o primeiro e o ultimo ano de pesquisa do PIP dentro da janela do mandato. Cruza nunca o spell. Os niveis anuais por decil, em PPC 2017 e 2021, estao em `renda-por-decil.csv`.

## 6. Que indicador alternativo NAO depende da regra que mudou?

| indicador | regra/definicao que mudou | alternativo | depende? | baixado |
|---|---|---|---|---|
| PIB | ano-base e Sistema de Contas Nacionais (FGV ate 1989; ref. 1985; 2000; 2010) | consumo de energia eletrica (quantidade fisica) | nao | sim |
| PIB | idem | consumo final de energia eletrica do Balanco Energetico Nacional | nao | sim |
| PIB | idem | IBC-Br (BCB) | parcialmente | sim |
| IPCA | pesos POF (1989, 1999, 2006, 2012, 2020), formula do subitem (1994), cobertura de areas (1 | IPC-Fipe (Sao Paulo) | nao (as regras do IBGE) | sim |
| IPCA | idem | IGP-DI (FGV) | nao (as regras do IBGE) | sim (em outra pasta) |
| IPCA | idem | custo da cesta basica (DIEESE, Sao Paulo) | nao | sim |
| Desemprego | PME 2002 (15+ -> 10+, definicao de desocupado), PNAD -> PNADC (10+ -> 14+, procura na sema | Pesquisa de Emprego e Desemprego (PED, Seade/Dieese) | nao (a PED nao mudou em 2002, segundo o Ipea) | nao |
| Desemprego | idem | emprego formal por registro administrativo (RAIS/CAGED do Ministerio do Trabalho) | nao (nao e pesquisa domiciliar) | nao |
| Salario minimo real | deflator (IPC-SP, IPC-RJ, IGPC-Mtb, INPC; fator 1,2225 em jul/1994), faixas regionais ate  | salario minimo em cestas basicas DIEESE | nao | sim |
| Salario minimo real | idem | salario minimo nominal / UM indice unico (IGP-DI, INPC ou IPCA) em todos os anos | nao (nao ha troca de deflator) | sim (series de entrada) |
| Pobreza | linha (US$ 1,00/1,08/1,25/1,90/2,15/3,00; 3,20/3,65/4,20; 5,50/6,85/8,30), PPC (1985/1993/ | renda domiciliar per capita real por decil e mediana | nao (nao tem linha) | sim |
| Pobreza | idem | renda domiciliar per capita mediana, media e dos 40% mais pobres (SIS/IBGE) | nao | sim |
| Gini | PNAD -> PNADC (2012), Censo x PNAD, quintas visitas 2020-2022, harmonizacao Ipea | Palma e participacao do 10o decil (PIP) | parcialmente | sim |
| Gini | idem | razao entre a renda dos 10% mais ricos e dos 40% mais pobres (Ipea PPA) | parcialmente | sim |
| Expectativa de vida | projecoes IBGE (Rev. 2000, 2008, 2013, 2018, 2024), tabuas como publicadas x reconstruidas | obitos e nascidos vivos REGISTRADOS (SIM/SINASC, Ministerio da Saude) e mortalidade infantil registrada | nao (contagem direta) | nao |
| Expectativa de vida | idem | UMA vintage unica para todos os anos (UN WPP via Banco Mundial) | parcialmente | sim |
| Agregados monetarios M1-M4 | conceito de base (1980), reformulacao de 2001, NT 48 de 2018 | papel-moeda emitido / em circulacao | nao | sim (em outra pasta) |

Resultados por governo dos alternativos baixados: `alternativos-por-governo.csv` (consumo de energia, IBC-Br, IPC-Fipe, salario minimo em cestas basicas, renda mediana/media/40% mais pobres do SIS, razao 10/40 do Ipea, Palma e participacao do decil 10 do PIP).

## 7. Mistura do infografico (resumo)

Ver `mistura-do-infografico.md`. Resumo: a linha de pobreza muda de 5,50 para 6,85 no meio da fileira (~8 pp); 4 de 8 pontos de pobreza e 3 de 8 de Gini estao em outro ano; a linha de expectativa de vida mistura 5 vintages; o desemprego cruza PME antiga, PME nova, PNAD e PNADC; 2016 entra em duas colunas; o 'IPCA 1967-73' nao existe. Direcao por familia e governo na tabela 8 daquele arquivo.

## 8. O que NAO foi achado, limites e becos

- IPCA, Sarney (1985-1989): nenhum segmento homogeneo cobre o mandato (serie encerrada em fev/1986, base mar/1986; pesos da POF 87-88 desde jun/1989). So 1987-1988 (2 de 5 anos) entram no comparativo, como linha PARCIAL; Figueiredo (1980-1984) tambem so entra em parte, porque a serie SGS 433 comeca em jan/1980 e a cobertura de areas so fecha em out/1980.
- A PME 2002 so tem decomposicao parcial: o periodo de referencia explica ~0,6 p.p.; os outros 3,1 a 5,1 p.p. (idade 10+, questionario, procura, malha) nao sao separaveis em fonte primaria lida. O IBGE nao publica essa decomposicao nos documentos baixados.
- Contradicao entre fontes: o metadado Ipeadata de `PAN12_TD12` diz 'periodo de referencia: 30 dias' e o relatorio metodologico do IBGE define desocupado pela semana; e o Ipea (Reis, 2004) e o IBGE (jul/2003) falam em serie nova desde out/2001, enquanto Ipeadata/SIDRA comecam em mar/2002. Nao resolvido.
- PIB: as tabelas ano a ano dos releases do IBGE (2007, 2015) sao imagens GIF. So os pontos em texto foram usados (2000, 2005; media 2000-2011). A serie ref. 1985 para 1996-2000 e a ref. 2000 nao foram obtidas. Fonte secundaria (nota academica) usada so para a direcao dos demais anos e rotulada.
- IPCA: nao ha contrafactual publicado para 1989, 1991, 1994 (media geometrica), 2014/2018 (areas). A direcao 'reduz' de 1994 e inferencia matematica (media geometrica <= aritmetica), nao medida. A reconstrucao 2020-2025 usa 9 grupos (nao 377 subitens): reproduz o publicado (3,744 contra 3,745 em 2018; 4,518 contra 4,517 em 2020), mas e estimativa.
- Pobreza: o PIP nao serve mais a versao PPC 2011 (a API devolve erro 500 para `ppp_version=2011` e para versoes antigas), entao a troca PPC 2011 -> 2017 so e medida no IBGE SIS (mistura edicoes). O PIP e o IBGE SIS divergem na MESMA linha (6,85) em 7,0 p.p. em media e em 12,3 p.p. em 2020; a causa nao esta nas fontes lidas (o fator PPC e identico).
- Pobreza em 1994 e 2010: o PIP nao tem os anos (sem PNAD em 1994 e 2010); celulas ficam 'indeterminado'. Linhas Ipea 1976-2014 e Atlas (R$ 70/140 de ago/2010) estao no leque como series proprias, sem conversao para dolar.
- Expectativa de vida: o documento da Rev. 2013 e a Rev. 2000 do IBGE nao foram lidos; o WDI nao informa a revisao do WPP usada. DATASUS (SIM/SINASC), RAIS/CAGED e PED (Seade/Dieese) estao listados como alternativos mas NAO foram baixados (URLs nao verificadas).
- A serie Ipea de salario minimo nao se reproduz com nenhum dos deflatores unicos nas janelas de Itamar e FHC por causa do fator 1,2225 de jul/1994; a razao do fator nao esta documentada.
- O Censo de 2022 e a reponderacao da PNADC: o IBGE diz que os indicadores serao recalculados apos o Censo; nao li se isso ja ocorreu (a serie baixada e a reponderada de nov/2021).
- Bolsa Familia: valores lidos nos decretos consolidados do Planalto (atos revogados aparecem no texto); o inicio de 2004-09 e a data do Decreto 5.209, nao a da Lei 10.836 (jan/2004) nem da MP 132 (out/2003), que nao li.

**Becos:** (1) `ibge.gov.br` e `agenciadenoticias.ibge.gov.br` devolvem 403 a curl: usei o proxy r.jina.ai (declarado em cada linha do manifest); (2) tabelas dos releases do IBGE de 2007 e 2015 sao imagens GIF; (3) PIP com `ppp_version=2011` e `release_version` devolvem erro 500; (4) PME por regiao metropolitana (SIDRA 2179) e de 'principais responsaveis pela familia', nao serve; (5) WebFetch de PDF devolveu binario (arquivo fora da cadeia de hash, nao usado); (6) a pagina da PME antiga e as paginas do IBGE nao trazem a decomposicao do salto de 2002; (7) tres entradas do manifest desta pasta tem rotulo imperfeito e, por a cadeia ser append-only, ficam: `bruto/ravallion-0509005.pdf` (a nota diz Ravallion, o conteudo e Reddy e Minoiu, 2005; nao citado em CSV), `bruto/wb-pw4620-dollar-a-day-revisited-jina.md` (267 bytes: a pagina 403 Forbidden do proxy) e `bruto/wb-pw7432-global-count-2012.pdf` (e texto UTF-8, nao PDF; as citacoes o leem como texto).

## 9. Reprodutibilidade

| script | sha256 |
|---|---|
| `carga.py` | `f252c76e9a995b4c447239ce7c07e4264e36fa089178e7cccea4d086a81cc320` |
| `citacoes.py` | `629f3708adf8d0dac0778008683ec95c0de4c2fd51de78401e06b43715410d72` |
| `extrair.py` | `c3b7b98676e88be52802fcf56829893e77d35ede2282dc200c1df436b123baaf` |
| `calc.py` | `95e4f4dd36bf5f452d22cda4247c97f33c8c560d13b8f2dd3e6ddfe640e37bd0` |
| `medidas.py` | `f13df3510e29550441d3443337766c76270a526d4ec43be3fbc5bf5cd07b2ca3` |
| `gerar_pobreza.py` | `beb2a3d0a0fcfde72dbb8a9165c3268a24481ba4f61951f0266b7b50b5b7e61d` |
| `gerar_quebras.py` | `2f9ec284ac9d56594056afc3920fd6a93e77a23d47e9bf6ce80d828f20982f78` |
| `gerar_vintage.py` | `ffcb49b9b0a4483fe8a62fa4a69d332d6a912e6592ce6cfa893e20b5c73a301c` |
| `gerar_alternativos.py` | `86d0fd8dde0697e836b670fcdb1e48e05721455a782e421da11842a2ce84f7b2` |
| `gerar_mistura.py` | `0c9667444d61c5a2247310d1850b2839e8d9a9f34122fbbe4f51a322ca7d479f` |
| `gerar_resultado.py` | `71c570b36226a5f2b41ecb183450b1bedc48e2c21dc40a549e2770321f4e726f` |

Cadeia de hash dos brutos desta pasta: `python3 -I ../manifest_tool.py verify .` (63 linhas; cabeca no momento da escrita: `f8c25d615b7ceaba47bb977ed1833fba63fd2a194ec2090cd991e48714851365`). Os arquivos de `derivado/` (texto de PDFs, HTML e planilhas) sao recriaveis por `extrair.py` e nao entram na cadeia. Fontes de outros blocos usadas como estao: `economia-real/`, `social/series/*.csv`, `monetario/saida/*.csv`, `historia/bruto/ibge-ipca/` (todas com hash no manifest da respectiva pasta).
