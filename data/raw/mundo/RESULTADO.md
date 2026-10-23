# Mundo: referencias internacionais, termos de troca e contexto de crescimento

Dossie governos-do-brasil-economia. Coleta em 2026-10-19. Pre-registro: `preregistro/PREREGISTRATION-EMENDA-01.md`, secao A e secao B (linha 'Growth context'). So descricao: sem causalidade, sem nota, sem ranking de merito.

Reproduzir (sem rede; confere o bruto contra o manifest antes): `python3 -I .../mundo/scripts/construir.py`, depois `medir.py`, `quebras.py`, `janelas.py`, `resultado.py`. Aquisicao (COM rede, nao rode por acaso): `scripts/baixar_*.sh` (um por cadeia de hash).

## 0. Achado e NAO achado

**Achado (descricao):**

1. Crescimento real do PIB, anos com dado nos dois lados. Lula 1-2 (2003-2010): Brasil 4.08 % a.a., America Latina e Caribe (LCN) 3.76, diferenca +0.32 pp. Dilma (2011-2016): Brasil 0.43, LCN 1.74, diferenca -1.31 pp. A LCN inclui o proprio Brasil (peso grande no agregado): a media simples dos 7 paises sem o Brasil esta na secao 4.
2. Coincidencia de direcao, sem causalidade: na janela Lula 1-2 a correlacao anual entre o crescimento do Brasil e o da LCN e 0.88 (n=8); na janela Dilma, 0.95 (n=6). Com n tao pequeno, o intervalo e largo; o numero descreve a janela, nao estima uma lei.
3. Termos de troca do Brasil (Funcex via Ipeadata, indice com base 2018=100): variacao do indice do ano anterior ao governo ate o ultimo ano do governo: Lula 1-2 +29.3 %, Dilma -13.6 %. Pela WDI/UNCTAD (versao 202507 do arquivo do WDI, 1980-2023; o WDI corrente de 2026-10-08 so traz o Brasil de 2005 em diante, ou seja, a fonte encurtou a serie em 25 anos): Lula 1-2 +29.3 % (2002-2010), Dilma -13.6 % (2010-2016). Variacao anual media (Funcex): Lula 1-2 +3.41 % a.a., Dilma -2.23 % a.a.
4. Associacao historica (1961 em diante, 65 anos): crescimento do Brasil contra crescimento da LCN, coeficiente 1.15 e R2 0.64; contra a media simples dos 7 paises, coeficiente 0.58 e R2 0.24. Crescimento do Brasil contra variacao anual dos termos de troca (Funcex, 65 anos): correlacao 0.19.
5. As trocas de base do PPC (2011 -> 2017 em 05/2020; 2017 -> 2021 em 05/2024) mudam o NIVEL do PIB per capita em PPC e a razao Brasil/referencia, quase por um fator constante por pais: as taxas de crescimento do pais ficam. Medido por sobreposicao em duas versoes do arquivo do WDI (secao 6).
6. Mesma quebra, pobreza: a troca da linha US$ 6,85 (PPC 2017) para US$ 8,30 (PPC 2021), no mesmo release do PIP, muda o nivel e o sinal do 'Brasil menos referencia' para varias referencias (secao 6).

**NAO achado:**

- Nenhum teste de causalidade. Nenhuma estimativa de quanto 'foi mundo' e quanto 'foi governo': so coincidencia e diferenca. As correlacoes por janela tem n entre 3 e 9.
- PIB per capita em PPC do WDI so existe de 1990 em diante; antes disso, so PWT e Maddison, com outros anos-base de PPC (2017/2021 e 2011) e valores de nivel diferentes entre si (secao 6.3).
- Venezuela: sem PIB per capita PPC no WDI; inflacao so de 2009 a 2016; pobreza e Gini do PIP so ate 2006. Argentina: o WDI so traz inflacao a partir de 2018. Nada foi interpolado nem retirado depois de ver o resultado.
- Investimento publico: nao ha serie oficial unica. A serie longa e uma compilacao da FGV IBRE (IBGE ate 1994; Gobetti/Orair, Tesouro e SEST depois): marcada como LITERATURA/COMPILACAO. O ICSD do FMI (conceito FBCF do governo geral) vai ate 2019 e difere do FGV por +2.88 / +0.91 / +5.50 pp do PIB [mediana / min / max], conceitos diferentes.
- Releases do PIP 20250401 e 20240627 devolveram erro 500 do servidor em 2026-10-19: so tres releases foram comparados. A troca 2011 -> 2017 do PPC no PIP nao pode ser medida.
- A planilha do Banco Mundial de classes de renda (OGHIST) termina em FY25; FY26 e FY27 nao foram lidos como serie (so a classe corrente via API).
- Nao ha, nos brutos, a serie de V-Dem v15 para ver revisao do indice; so a v16 via OWID.

## 1. Regra de atribuicao ano -> governo

Cada ano-calendario pertence ao governo que o ocupa por MAIS DIAS (mesma regra de `dominios-2`; datas de `data/curated/mandatos.csv`, saida exclusiva). Anos com mais de um governo: 1967, 1969, 1974, 1979, 1985, 1990, 1992, 2016; ex.: 2016 fica com Dilma (243 dias contra 123 de Temer). A Junta Militar nunca fica com ano. Medias sao simples. As medias Brasil x referencia usam SO os anos em que os dois lados tem valor (por isso a media do Brasil muda de referencia para referencia em `janelas.csv`).

## 2. Cobertura (anos com valor)

| indicador | fonte | Brasil: anos (n) | n de anos por referencia |
|---|---|---|---|
| mun_pibpc_ppc | WDI NY.GDP.PCAP.PP.KD | 1990-2025 (36) | WLD 36, LCN 36, UMC 36, ARG 36, CHL 36, COL 36, MEX 36, PER 36, URY 36 |
| mun_pib_cresc | WDI NY.GDP.MKTP.KD.ZG | 1961-2025 (65) | WLD 65, LCN 65, UMC 65, ARG 65, CHL 65, COL 65, MEX 65, PER 65, URY 65, VEN 65 |
| mun_expvida | WDI SP.DYN.LE00.IN | 1960-2024 (65) | WLD 65, LCN 65, UMC 65, ARG 65, CHL 65, COL 65, MEX 65, PER 65, URY 65, VEN 65 |
| mun_mortinf | WDI SP.DYN.IMRT.IN | 1960-2024 (65) | WLD 35, LCN 35, UMC 35, ARG 56, CHL 65, COL 65, MEX 65, PER 65, URY 65, VEN 65 |
| mun_gini | PIP (Banco Mundial) | 1981-2024 (40) | ARG 36, CHL 17, COL 26, MEX 20, PER 30, URY 19, VEN 13 |
| mun_pobreza_685 | PIP (Banco Mundial) | 1981-2024 (40) | ARG 36, CHL 17, COL 26, MEX 20, PER 30, URY 19, VEN 13 |
| mun_pobreza_830_ppc2021 | PIP (Banco Mundial) | 1981-2024 (40) | ARG 36, CHL 17, COL 26, MEX 20, PER 30, URY 19, VEN 13 |
| mun_homic | WDI VC.IHR.PSRC.P5 | 1990-2023 (34) | WLD 24, LCN 14, UMC 14, ARG 23, CHL 20, COL 34, MEX 34, PER 11, URY 32, VEN 31 |
| mun_dtp3 | WDI SH.IMM.IDPT | 1980-2024 (45) | WLD 45, LCN 45, UMC 45, ARG 45, CHL 45, COL 45, MEX 45, PER 45, URY 45, VEN 45 |
| mun_inflacao | WDI FP.CPI.TOTL.ZG | 1981-2025 (45) | WLD 45, LCN 59, UMC 51, ARG 7, CHL 55, COL 66, MEX 66, PER 66, URY 66, VEN 8 |
| mun_desemprego_oit | WDI SL.UEM.TOTL.ZS | 1991-2025 (35) | WLD 35, LCN 35, UMC 35, ARG 35, CHL 35, COL 35, MEX 35, PER 35, URY 35, VEN 35 |
| mun_polyarchy | V-Dem v16 (via OWID, CC BY 4.0) | 1960-2025 (66) | ARG 66, CHL 66, COL 66, MEX 66, PER 66, URY 66, VEN 66 |
| tt_funcex | Ipeadata FUNCEX_TTR | 1850-2025 (176) | so Brasil |
| tt_histtroca | Ipeadata HIST_TROCA | 1901-1975 (75) | so Brasil |
| tt_wdi | WDI TT.PRI.MRCH.XD.WD (UNCTAD) | 2005-2024 (20) | WLD 20, ARG 20, CHL 20, COL 20, MEX 20, PER 20, URY 20, VEN 14 |
| tt_wdi_arq | WDI arquivo v202507 TT.PRI.MRCH.XD | 1980-2023 (44) | WLD 19, ARG 44, CHL 44, COL 44, MEX 44, PER 44, URY 44, VEN 39 |
| cc_fbcf_pib | FGV IBRE (dados IBGE SCN) | 1947-2025 (79) | so Brasil |
| cc_fbcf_pib | Ipeadata PAN_FBKFPIBV (IPEA) | 1996-2025 (30) | so Brasil |
| cc_fbcf_pib | WDI NE.GDI.FTOT.ZS | 1970-2025 (56) | WLD 55, LCN 56, UMC 65, ARG 66, CHL 66, COL 66, MEX 66, PER 66, URY 66, VEN 66 |
| cc_invpub_pib | FGV IBRE Observatorio de Politica  | 1947-2025 (474) | so Brasil |
| cc_invpub_pib | IMF ICSD 2021 | 1960-2019 (60) | ARG 60, CHL 60, COL 60, MEX 60, PER 60, URY 60, VEN 60 |
| cc_pibpc_na_pwt | PWT 10.01 | 1950-2019 (70) | ARG 70, CHL 69, COL 70, MEX 70, PER 70, URY 70, VEN 70 |
| cc_pibpc_pwt | PWT 10.01 | 1950-2019 (70) | ARG 70, CHL 69, COL 70, MEX 70, PER 70, URY 70, VEN 70 |
| cc_estoque_capital_pwt | PWT 10.01 | 1950-2019 (70) | so Brasil |
| cc_pib_real_pwt | PWT 10.01 | 1950-2019 (70) | so Brasil |
| cc_ptf_pwt | PWT 10.01 | 1954-2019 (66) | so Brasil |
| cc_pibpc_na_pwt | PWT 11.0 | 1950-2023 (74) | ARG 74, CHL 73, COL 74, MEX 74, PER 74, URY 74, VEN 74 |
| cc_pibpc_pwt | PWT 11.0 | 1950-2023 (74) | ARG 74, CHL 73, COL 74, MEX 74, PER 74, URY 74, VEN 74 |
| cc_estoque_capital_pwt | PWT 11.0 | 1950-2023 (74) | so Brasil |
| cc_pib_real_pwt | PWT 11.0 | 1950-2023 (74) | so Brasil |
| cc_ptf_pwt | PWT 11.0 | 1954-2023 (70) | so Brasil |
| cc_pibpc_maddison | Maddison Project Database 2023 | 1900-2022 (123) | ARG 123, CHL 123, COL 123, MEX 123, PER 123, URY 123, VEN 123 |


## 3. Lula 1-2 e Dilma: Brasil menos referencia, por indicador

Media anual dos anos em comum; diferenca = media do Brasil menos media da referencia. Colunas: LCN, UMC (renda media alta, definicao do Banco Mundial), WLD, e o menor e o maior da diferenca entre os 7 paises (ARG, CHL, COL, MEX, PER, URY, VEN). `n de anos comuns` = anos em comum com a LCN e com os 7 paises (min-max). Todas as combinacoes (14 governos, 11 referencias) estao em `janelas.csv`.

### Lula 1-2 (2003-2010)

| indicador | Brasil (anos comuns com LCN) | LCN | Brasil menos LCN | Brasil menos UMC | Brasil menos WLD | Brasil menos cada um dos 7 paises (min a max) | n de anos comuns |
|---|---|---|---|---|---|---|---|
| PIB real, % a.a. | 4.08 | 3.76 | +0.32 | -3.11 | +0.85 | -2.43 a +2.41 | LCN 8; 7 paises 8-8 |
| PIB pc PPC, variacao % a.a. | 3.02 | 2.54 | +0.48 | -2.77 | +0.44 | -2.39 a +2.77 | LCN 8; 7 paises 8-8 |
| expectativa de vida, anos | 72.43 | 72.83 | -0.40 | -0.15 | +2.84 | -6.14 a +0.17 | LCN 8; 7 paises 8-8 |
| mortalidade infantil, por mil | 19.50 | 20.49 | -0.99 | -1.68 | -22.41 | -0.41 a +11.82 | LCN 8; 7 paises 8-8 |
| homicidios, por 100 mil | 26.99 | 23.90 | +3.09 | +20.59 | +20.30 | -18.10 a +23.07 | LCN 1; 7 paises 0-8 |
| DTP3, % | 99.00 | 93.08 | +5.92 | +8.66 | +19.91 | +2.00 a +25.75 | LCN 8; 7 paises 8-8 |
| inflacao, % a.a. | 6.45 | 4.44 | +2.02 | +1.43 | +2.09 | -22.67 a +3.76 | LCN 8; 7 paises 0-8 |
| desemprego OIT (MODELO), % | 9.61 | 7.87 | +1.74 | +3.72 | +3.45 | -2.24 a +5.52 | LCN 8; 7 paises 8-8 |
| pobreza US$ 6,85 PPC 2017, % | 41.58 * | - | - | - | - | -12.40 a +22.27 | LCN -; 7 paises 3-7 |
| Gini, 0-100 | 55.52 * | - | - | - | - | +1.31 a +9.18 | LCN -; 7 paises 3-7 |
| polyarchy V-Dem, 0-1 | 0.86 * | - | - | - | - | -0.03 a +0.41 | LCN -; 7 paises 8-8 |

`*` = media de todos os anos do Brasil na janela (nao ha agregado LCN para este indicador).


### Dilma (2011-2016)

| indicador | Brasil (anos comuns com LCN) | LCN | Brasil menos LCN | Brasil menos UMC | Brasil menos WLD | Brasil menos cada um dos 7 paises (min a max) | n de anos comuns |
|---|---|---|---|---|---|---|---|
| PIB real, % a.a. | 0.43 | 1.74 | -1.31 | -4.99 | -2.58 | -4.22 a +3.11 | LCN 6; 7 paises 6-6 |
| PIB pc PPC, variacao % a.a. | -0.37 | 0.94 | -1.31 | -4.51 | -2.52 | -3.99 a -0.26 | LCN 6; 7 paises 6-6 |
| expectativa de vida, anos | 74.67 | 74.41 | +0.26 | +0.12 | +3.05 | -5.00 a +1.82 | LCN 6; 7 paises 6-6 |
| mortalidade infantil, por mil | 14.47 | 16.35 | -1.88 | +0.07 | -18.40 | -2.00 a +7.43 | LCN 6; 7 paises 6-6 |
| homicidios, por 100 mil | 28.81 | 23.72 | +5.09 | +22.68 | +22.73 | -25.83 a +25.90 | LCN 6; 7 paises 5-6 |
| DTP3, % | 94.83 | 90.70 | +4.13 | +1.85 | +10.19 | -0.17 a +13.17 | LCN 6; 7 paises 6-6 |
| inflacao, % a.a. | 7.06 | 3.01 | +4.04 | +3.91 | +4.30 | -80.72 a +3.70 | LCN 6; 7 paises 0-6 |
| desemprego OIT (MODELO), % | 8.13 | 6.69 | +1.44 | +2.66 | +2.07 | -1.17 a +4.71 | LCN 6; 7 paises 6-6 |
| pobreza US$ 6,85 PPC 2017, % | 26.77 * | - | - | - | - | -11.60 a +19.83 | LCN -; 7 paises 0-6 |
| Gini, 0-100 | 52.74 * | - | - | - | - | -0.21 a +12.33 | LCN -; 7 paises 0-6 |
| polyarchy V-Dem, 0-1 | 0.86 * | - | - | - | - | -0.05 a +0.51 | LCN -; 7 paises 6-6 |

`*` = media de todos os anos do Brasil na janela (nao ha agregado LCN para este indicador).


Leitura: onde LCN/UMC/WLD estao vazios (homicidios nos agregados, pobreza, Gini, polyarchy) a referencia e so o conjunto de paises. Desemprego OIT e estimativa modelada; DTP3, expectativa de vida e mortalidade infantil sao estimativas de agencias da ONU, nao registros. Os 'Brasil menos' em niveis de PIB per capita PPC estao em `janelas.csv` mas dependem da base do PPC (secao 6); as variacoes anuais nao.

## 4. Quanto do movimento do Brasil coincide com a America Latina e com os termos de troca

Descricao de coincidencia, nao de causa. Crescimento anual real do PIB (WDI NY.GDP.MKTP.KD.ZG). Termos de troca: Funcex (Ipeadata FUNCEX_TTR, anual desde 1850, encadeada em 1974; ver secao 6) e WDI/UNCTAD (TT.PRI.MRCH.XD.WD, versao 202507 do arquivo, 1980-2023; a versao corrente tem so 2005-2024). A LCN inclui o Brasil; por isso ha tambem a media simples dos 7 paises sem o Brasil.

| janela | anos | n (com LCN) | PIB Brasil, % a.a. | PIB LCN, % a.a. | Brasil menos LCN, pp | media 7 paises: Brasil / 7 paises (anos comuns) | correlacao anual Brasil x LCN | correlacao anual Brasil x media dos 7 | anos em que a mudanca de crescimento teve o mesmo sinal |
|---|---|---|---|---|---|---|---|---|---|
| Lula 1-2 | 2003-2010 | 8 | 4.08 | 3.76 | +0.32 | 4.08 / 4.85 | 0.88 | 0.79 | 7/8 |
| Dilma | 2011-2016 | 6 | 0.43 | 1.74 | -1.31 | 0.43 / 2.33 | 0.95 | 0.89 | 5/6 |


| janela | termos de troca Funcex: variacao % do ano anterior ao governo ate o ultimo ano | Funcex: variacao anual media, % | correlacao crescimento do Brasil x variacao anual do indice (Funcex) | termos de troca WDI: variacao % | correlacao com WDI |
|---|---|---|---|---|---|
| Lula 1-2 | +29.3 | +3.41 | 0.79 (n=8) | +29.3 (2002-2010) | 0.80 (n=8) |
| Dilma | -13.6 | -2.23 | 0.46 (n=6) | -13.6 (2010-2016) | 0.46 (n=6) |


Associacao historica para comparar com as janelas (todos os anos disponiveis, 1961 em diante; n=65): crescimento do Brasil = -0.01 + 1.15 x crescimento da LCN (R2 0.64); contra a media dos 7 paises: 2.17 + 0.58 x media (R2 0.24). Aplicada sem ajuste as medias das janelas, a relacao historica com a LCN daria Brasil de 4.33 % a.a. em Lula 1-2 (observado 4.08) e 2.00 % a.a. em Dilma (observado 0.43). Isto e uma descricao dentro da amostra, nao uma previsao nem uma decomposicao causal.

Todos os governos com pelo menos 3 anos de dados de crescimento, na mesma metrica:

| governo | anos | n | Brasil, % a.a. | LCN, % a.a. | Brasil menos LCN, pp | correlacao Brasil x LCN | termos de troca Funcex, variacao anual media % | correlacao Brasil x termos de troca |
|---|---|---|---|---|---|---|---|---|
| castelo | 1964-1966 | 3 | 4.17 | 5.94 | -1.78 | -0.56 | +5.22 | -0.56 |
| costa_silva | 1967-1969 | 3 | 7.83 | 5.99 | +1.84 | 0.99 | -0.84 | 0.21 |
| medici | 1970-1973 | 4 | 11.91 | 7.03 | +4.88 | 0.97 | +4.12 | 0.34 |
| geisel | 1974-1978 | 5 | 6.70 | 4.91 | +1.79 | 0.72 | -2.77 | 0.05 |
| figueiredo | 1979-1984 | 6 | 2.50 | 2.65 | -0.14 | 0.87 | -6.17 | -0.23 |
| sarney | 1985-1989 | 5 | 4.39 | 2.39 | +2.01 | 0.80 | +3.08 | 0.25 |
| collor | 1990-1992 | 3 | -1.29 | 1.89 | -3.18 | 0.99 | -0.58 | 1.00 |
| fhc | 1995-2002 | 8 | 2.43 | 2.27 | +0.16 | 0.25 | +0.32 | 0.77 |
| lula12 | 2003-2010 | 8 | 4.08 | 3.76 | +0.32 | 0.88 | +3.41 | 0.79 |
| dilma | 2011-2016 | 6 | 0.43 | 1.74 | -1.31 | 0.95 | -2.23 | 0.46 |
| bolsonaro | 2019-2022 | 4 | 1.43 | 1.16 | +0.27 | 1.00 | +2.02 | 0.36 |
| lula3 | 2023-2025 | 3 | 2.98 | 2.26 | +0.72 | -0.84 | +1.21 | 1.00 |


## 5. Contexto de crescimento (pre-registro, secao B)

Media por governo (anos atribuidos pela regra da secao 1). FBCF e investimento publico em % do PIB; estoque de capital (rnna) e PTF (rtfpna) do PWT em variacao % a.a. calculada aqui (10.01 ate 2019; 11.0 ate 2023). `-` = sem dado.

| governo | FBCF % PIB (FGV/IBGE) | inv. publico % PIB: setor publico (FGV) | inv. publico: governo geral (FGV) | inv. publico governo geral (ICSD/FMI, ate 2019) | estoque de capital, var. % a.a. (PWT 10.01) | idem (PWT 11.0) | PTF, var. % a.a. (PWT 10.01) | idem (PWT 11.0) |
|---|---|---|---|---|---|---|---|---|
| castelo | 15.21 | 5.97 | 4.15 | 8.16 | 5.54 | 5.51 | 0.71 | 0.62 |
| costa_silva | 18.00 | 6.74 | 4.79 | 7.55 | 6.83 | 6.80 | 2.49 | 2.41 |
| medici | 19.86 | 6.79 | 4.08 | 6.64 | 9.56 | 9.53 | 3.99 | 3.93 |
| geisel | 22.24 | 8.95 | 3.66 | 7.93 | 9.99 | 9.97 | 0.09 | -0.05 |
| figueiredo | 22.18 | 6.51 | 2.31 | 5.45 | 5.42 | 5.41 | -1.19 | -1.27 |
| sarney | 22.48 | 5.83 | 3.09 | 5.93 | 4.10 | 4.10 | 0.16 | 0.13 |
| collor | 19.07 | 4.85 | 3.16 | 7.48 | 2.83 | 2.81 | -3.41 | -3.94 |
| itamar | 20.02 | 4.58 | 3.13 | 7.09 | 3.23 | 3.24 | 2.34 | 2.44 |
| fhc | 18.53 | 3.21 | 2.09 | 4.94 | 3.03 | 3.03 | -1.06 | -1.01 |
| lula12 | 18.15 | 3.23 | 1.95 | 4.04 | 2.70 | 2.94 | 0.42 | 0.33 |
| dilma | 19.25 | 3.55 | 2.07 | 4.07 | 3.06 | 3.21 | -2.52 | -2.59 |
| temer | 14.83 | 2.26 | 1.31 | 2.41 | 1.07 | 1.18 | -0.69 | -0.19 |
| bolsonaro | 16.94 | 2.30 | 1.53 | 2.20 | 1.32 | 1.85 | -1.92 | -1.54 |
| lula3 | 16.72 | 2.80 | 2.02 | - | - | 1.80 | - | 0.72 |


Nota: PTF e residuo estimado pelo PWT, nao observado; o estoque de capital e construido por acumulacao do investimento (PWT), nao medido. Investimento publico FGV e compilacao (LITERATURA), com trocas de fonte em 1995, 2011 e 2015 (secao 6.7).

PIB per capita, variacao anual media (%) por governo, em cinco medidas: WDI (PPC 2021, 1991+), PWT 10.01 e 11.0 com rgdpna/pop (precos nacionais constantes, crescimento das contas nacionais), PWT 10.01 e 11.0 com rgdpo/pop (lado da producao a PPC encadeada, a medida que o PWT usa para comparar paises) e Maddison 2023 (PPC 2011). As duas familias de PWT dao taxas muito diferentes para o mesmo pais e periodo. Legenda do PWT, literal: rgdpo = 'Output-side real GDP at chained PPPs (in mil. 2017US$)' (2021US$ na 11.0); rgdpna = 'Real GDP at constant 2017 national prices (in mil. 2017US$)'. Sao medidas diferentes; esta pasta nao interpreta a diferenca (a documentacao do PWT sobre ela nao foi lida para este ponto), so a mostra.

| governo | WDI | PWT 10.01 (rgdpna/pop) | PWT 11.0 (rgdpna/pop) | PWT 10.01 (rgdpo/pop) | PWT 11.0 (rgdpo/pop) | Maddison 2023 |
|---|---|---|---|---|---|---|
| castelo | - | 1.98 | 1.98 | 2.21 | 2.27 | 1.14 |
| costa_silva | - | 4.78 | 4.78 | 3.97 | 3.92 | 4.83 |
| medici | - | 9.29 | 9.27 | 10.20 | 10.00 | 9.00 |
| geisel | - | 4.20 | 4.18 | 3.11 | 3.23 | 4.08 |
| figueiredo | - | 0.15 | 0.18 | 0.06 | 0.27 | 0.15 |
| sarney | - | 2.32 | 2.34 | 3.08 | 2.90 | 2.34 |
| collor | -1.44 | -3.14 | -3.31 | 1.38 | 0.96 | -2.09 |
| itamar | 3.72 | 3.62 | 3.35 | 8.39 | 8.09 | 5.01 |
| fhc | 0.98 | 0.78 | 0.94 | 1.91 | 2.41 | 2.20 |
| lula12 | 3.02 | 2.95 | 3.02 | 6.38 | 6.33 | 4.21 |
| dilma | -0.37 | -0.44 | -0.37 | -0.74 | -0.61 | -0.22 |
| temer | 0.84 | 0.52 | 0.84 | 1.06 | 1.81 | 0.74 |
| bolsonaro | 0.92 | 0.38 | 0.92 | 0.49 | 2.29 | 0.82 |
| lula3 | 2.58 | - | 2.83 | - | 3.18 | - |


## 6. Quebras, revisoes e luzes de confianca dos dados

`quebras.csv` tem uma linha por quebra, no formato das outras pastas (tipo_de_quebra: metodo_estatistico, mudanca_de_regra, revisao_de_vintage). `medidas_efeito.csv` guarda cada numero medido. `quebras_na_janela` em `janelas.csv` lista as quebras que caem dentro de cada governo.

Total: 73 linhas (metodo_estatistico 29, mudanca_de_regra 22, revisao_de_vintage 22).

### 6.1 Troca da base do PPC no WDI (PIB per capita), por sobreposicao de versoes

Cada coluna: variacao % mediana (anos comuns) do nivel do PIB per capita PPC entre a versao antiga e a nova do arquivo WDI (fonte 57, baixado em 2026-10-19). O rotulo de unidade do proprio arquivo diz 'constant 2011 international $' em todas as versoes (rotulo desatualizado); as trocas foram identificadas pelo salto de nivel entre versoes consecutivas e pelas datas de divulgacao do ICP (19/05/2020 e 30/05/2024).

| unidade | nivel: 2011->2017 (v202004->v202005), % | nivel: 2017->2021 (v202403->v202405), % | nivel: revisao 202405->202412, % | razao Brasil/unidade: 2011->2017, % | razao Brasil/unidade: 2017->2021, % |
|---|---|---|---|---|---|
| BRA | +1.70 | +18.42 | +2.67 | - | - |
| ARG | +24.37 | +20.77 | -0.40 | -18.23 | -1.95 |
| CHL | +6.40 | +14.70 | -0.86 | -4.42 | +3.25 |
| COL | +8.54 | +19.95 | +0.45 | -6.30 | -1.27 |
| MEX | +10.25 | +7.68 | -0.87 | -7.75 | +9.98 |
| PER | -0.09 | +18.51 | +1.74 | +1.79 | -0.07 |
| URY | +3.23 | +26.84 | +0.55 | -1.48 | -6.64 |
| WLD | +6.13 | +14.92 | -0.17 | -4.17 | +3.05 |
| LCN | +9.13 | +15.66 | +0.59 | -6.81 | +2.39 |
| UMC | +0.21 | +17.39 | -7.35 | +1.49 | +0.88 |


Efeito: a troca altera o nivel e a razao entre paises (ex.: Brasil/Argentina cai 18% na primeira troca), mas o fator e quase o mesmo em todos os anos de cada pais (min e max proximos em `medidas_efeito.csv`), de modo que a taxa de crescimento do pais fica. Luz de dados pela regra D: vermelha para qualquer comparacao de NIVEL entre paises que atravesse uma troca nao medida; aqui a troca foi medida por sobreposicao, entao a luz seria amarela para niveis e nenhuma para variacoes anuais.

### 6.2 Pobreza (PIP): linha 6,85 PPC 2017 contra 8,30 PPC 2021, mesmo release

| pais | mediana de (8,30/2021 menos 6,85/2017), pp | n | efeito sobre Brasil menos pais, pp (mediana) | min a max |
|---|---|---|---|---|
| BRA | +2.11 | 40 | - |  |
| ARG | +2.94 | 36 | -0.86 | min -2.19 max 0.97 |
| CHL | +2.55 | 17 | -0.15 | min -0.99 max 1.00 |
| COL | +5.20 | 26 | -3.11 | min -3.65 max -2.15 |
| MEX | +5.83 | 20 | -3.76 | min -4.70 max -2.89 |
| PER | +4.70 | 30 | -2.55 | min -3.91 max -1.65 |
| URY | -0.11 | 19 | +2.18 | min 1.74 max 2.66 |
| VEN | +4.16 | 13 | -1.97 | min -2.94 max -1.37 |


### 6.3 PWT 10.01 contra 11.0 e fontes de nivel (nao sao revisoes da mesma serie quando as fontes diferem)

| medida (PWT 10.01 / 11.0) | valores |
|---|---|
| crescimento medio anual do PIB pc de BRA medido por rgdpo/pop (lado da producao, PPC encadeada), Lula1-2 (2003-2010): PWT 10.01 / 11.0 / diferenca (pp/ano) | 6.385 / 6.327 / -0.058 |
| crescimento medio anual do PIB pc de BRA medido por rgdpo/pop (lado da producao, PPC encadeada), Dilma (2011-2016; PWT 10.01 so ate 2019): PWT 10.01 / 11.0 / diferenca (pp/ano) | -0.739 / -0.614 / +0.125 |
| rnna: variacao % acumulada 2002->2010 do Brasil, PWT 10.01 / 11.0 | 23.73 / 26.03 |
| rtfpna: variacao % acumulada 2002->2010 do Brasil, PWT 10.01 / 11.0 | 3.27 / 2.57 |


Razao PIB per capita do Brasil / mediana de ARG, CHL, COL, MEX, PER, URY (VEN fora por falta de cobertura em PWT/WDI), por fonte:

| fonte | 1980 | 1990 | 2002 | 2010 | 2016 | 2019 |
|---|---|---|---|---|---|---|
| Maddison 2023 (PPC 2011) | 0.871 | 0.788 | 0.872 | 0.914 | 0.788 | 0.821 |
| PWT 10.01 (PPC 2017) | 0.778 | 0.819 | 0.853 | 0.868 | 0.723 | 0.743 |
| PWT 11.0 (PPC 2021) | 0.700 | 0.833 | 0.858 | 0.856 | 0.714 | 0.750 |
| WDI corrente (PPC 2021) | - | 1.010 | 0.820 | 0.818 | 0.714 | 0.746 |


O nivel relativo do Brasil entre as quatro fontes varia ate dezenas de pontos percentuais no mesmo ano (ex.: 1980); o WDI corrente nao existe antes de 1990. Nada aqui diz qual fonte esta certa.

### 6.4 Termos de troca: encadeamento da serie Funcex em 1974

| medida | valor | nota |
|---|---|---|
| FUNCEX_TTR / HIST_TROCA: razao mediana 1901-1973 (mesma fonte IBGE, bases diferentes) | 1.0361 | desvio maximo absoluto em relacao a mediana, 1901-1973: 0.00% |
| desvio % da razao FUNCEX_TTR/HIST_TROCA em 1972 em relacao a mediana 1901-1973 | 0.0 | FUNCEX=110.59 HIST=106.74 |
| desvio % da razao FUNCEX_TTR/HIST_TROCA em 1973 em relacao a mediana 1901-1973 | -0.0 | FUNCEX=123.70 HIST=119.40 |
| desvio % da razao FUNCEX_TTR/HIST_TROCA em 1974 em relacao a mediana 1901-1973 | -8.4902 | FUNCEX=94.31 HIST=99.47 |
| desvio % da razao FUNCEX_TTR/HIST_TROCA em 1975 em relacao a mediana 1901-1973 | -8.6073 | FUNCEX=89.97 HIST=95.01 |
| variacao % do indice em 1974 sobre 1973: FUNCEX_TTR / HIST_TROCA | -23.76 / -16.69 |  |
| variacao % do indice em 1975 sobre 1974: FUNCEX_TTR / HIST_TROCA | -4.60 / -4.48 |  |


O nome da serie no Ipeadata diz 'media 2018 = 100'; a nota diz 'Ate 1973, serie encadeada e convertida para a base 2006=100'. Outra incoerencia: a nota cita fonte IBGE a partir de 1879, mas a serie traz valores desde 1850. Incoerencias na propria fonte; nao resolvidas aqui.

### 6.5 Revisoes do WDI nos demais indicadores (Brasil), versao 202403 do arquivo -> 202507 -> corrente 2026-10-08

| indicador: versoes | valores comuns alterados / comuns (Brasil) | nota |
|---|---|---|
| NY.GDP.MKTP.KD.ZG: 202403 -> 202507 | 2/62 | maior mudanca absoluta 0.2262 em BRA 2021; so na antiga 0; so na nova 2 |
| NY.GDP.MKTP.KD.ZG: 202507 -> 2026-10-08 | 1/64 | maior mudanca absoluta 0.0234 em BRA 2024; so na antiga 0; so na nova 1 |
| SP.DYN.LE00.IN: 202403 -> 202507 | 62/62 | maior mudanca absoluta 0.7830 em BRA 2012; so na antiga 0; so na nova 2 |
| SP.DYN.LE00.IN: 202507 -> 2026-10-08 | 0/64 | maior mudanca absoluta 0.0000; so na antiga 0; so na nova 1 |
| SP.DYN.IMRT.IN: 202403 -> 202507 | 61/62 | maior mudanca absoluta 1.3000 em BRA 1996; so na antiga 0; so na nova 2 |
| SP.DYN.IMRT.IN: 202507 -> 2026-10-08 | 34/64 | maior mudanca absoluta 0.8000 em BRA 1960; so na antiga 0; so na nova 1 |
| VC.IHR.PSRC.P5: 202403 -> 202507 | 0/31 | maior mudanca absoluta 0.0000; so na antiga 0; so na nova 0 |
| VC.IHR.PSRC.P5: 202507 -> 2026-10-08 | 31/31 | maior mudanca absoluta 0.5712 em BRA 2020; so na antiga 0; so na nova 3 |
| SH.IMM.IDPT: 202403 -> 202507 | 0/43 | maior mudanca absoluta 0.0000; so na antiga 0; so na nova 1 |
| SH.IMM.IDPT: 202507 -> 2026-10-08 | 0/44 | maior mudanca absoluta 0.0000; so na antiga 0; so na nova 1 |
| FP.CPI.TOTL.ZG: 202403 -> 202507 | 0/42 | maior mudanca absoluta 0.0000; so na antiga 0; so na nova 2 |
| FP.CPI.TOTL.ZG: 202507 -> 2026-10-08 | 0/44 | maior mudanca absoluta 0.0000; so na antiga 0; so na nova 1 |
| SL.UEM.TOTL.ZS: 202403 -> 202507 | 29/33 | maior mudanca absoluta 0.6660 em BRA 1992; so na antiga 0; so na nova 1 |
| SL.UEM.TOTL.ZS: 202507 -> 2026-10-08 | 4/34 | maior mudanca absoluta 0.8330 em BRA 2024; so na antiga 0; so na nova 1 |
| TT.PRI.MRCH.XD.WD: 202403 -> 202507 | 16/42 | maior mudanca absoluta 0.0482 em BRA 2008; so na antiga 0; so na nova 2 |
| TT.PRI.MRCH.XD.WD: 202507 -> 2026-10-08 | 1/19 | anos que existiam e sumiram: 1980-2004 (25 anos); maior mudanca absoluta 0.1000 em BRA 2008; so na antiga 25; so na nova 1 |
| NE.GDI.FTOT.ZS: 202403 -> 202507 | 2/53 | maior mudanca absoluta 1.0222 em BRA 2022; so na antiga 0; so na nova 2 |
| NE.GDI.FTOT.ZS: 202507 -> 2026-10-08 | 1/55 | maior mudanca absoluta 0.1235 em BRA 2024; so na antiga 0; so na nova 1 |


### 6.6 Classes de renda do Banco Mundial

| pais | mudancas FY89-FY25 | transicoes |
|---|---|---|
| BRA | 4 | FY89->FY90: UM -> LM; FY90->FY91: LM -> UM; FY03->FY04: UM -> LM; FY07->FY08: LM -> UM |
| ARG | 6 | FY90->FY91: UM -> LM; FY92->FY93: LM -> UM; FY15->FY16: UM -> H; FY16->FY17: H -> UM; FY18->FY19: UM -> H; FY19->FY20: H -> UM |
| CHL | 2 | FY94->FY95: LM -> UM; FY13->FY14: UM -> H |
| COL | 1 | FY09->FY10: LM -> UM |
| MEX | 1 | FY91->FY92: LM -> UM |
| PER | 1 | FY09->FY10: LM -> UM |
| URY | 1 | FY13->FY14: UM -> H |
| VEN | 5 | FY95->FY96: UM -> LM; FY98->FY99: LM -> UM; FY15->FY16: UM -> H; FY16->FY17: H -> UM; FY21->FY22: UM -> (vazio) |


Economias na classe UM (renda media alta): primeiro FY89=29; menor FY91=23; maior FY20=60; ultimo FY25=54. Se o agregado UMC do WDI recalcula o passado com a classificacao corrente NAO foi verificado; se recalcula, a serie historica do agregado mistura paises de epocas diferentes. Pela API do WDI hoje: ARG, BRA, COL, MEX, PER = renda media alta; CHL e URY = alta; VEN = media baixa (classe corrente lida em 2026-10-19). Nota do Banco Mundial sobre a Argentina: 'Due to the limitations of the Atlas method in classifying countries experiencing persistent high inflation, Argentina and Türkiye remain classified as upper-middle-income.'

### 6.7 Investimento publico e FBCF

| medida | valor | nota |
|---|---|---|
| investimento do setor publico (% do PIB): vintage 2023 -> 2024 | 1/77 | maior mudanca +0.025 pp em 2023; mediana das mudancas absolutas entre os alterados 0.025 pp; anos novos 1 |
| investimento do setor publico (% do PIB): vintage 2024 -> 2025 | 2/78 | maior mudanca +0.011 pp em 2024; mediana das mudancas absolutas entre os alterados 0.006 pp; anos novos 1 |
| FBCF (% do PIB): vintage 2023 -> 2024 | 1/77 | maior mudanca -0.128 pp em 2023; mediana das mudancas absolutas entre os alterados 0.128 pp; anos novos 1 |
| FBCF (% do PIB): vintage 2024 -> 2025 | 1/78 | maior mudanca -0.124 pp em 2024; mediana das mudancas absolutas entre os alterados 0.124 pp; anos novos 1 |
| ICSD (FBCF governo geral) menos FGV (governo geral) em pp do PIB, anos comuns 1960-2019 | +2.88 / +0.91 / +5.50 | conceitos e deflatores diferentes (ICSD: PIB e FBCF em US$ PPC de 2017); nao e revisao |
| Ipeadata PAN_FBKFPIBV menos FGV/IBGE, FBCF % do PIB, anos comuns 1996-2025 (pp) | +0.00 / +0.00 / +0.00 | anos com /dif/>0,5 pp: 0 |
| WDI NE.GDI.FTOT.ZS menos FGV/IBGE, FBCF % do PIB, anos comuns 1970-2025 (pp) | +0.00 / -0.89 / +0.04 | anos com /dif/>0,5 pp: 4 |
| Ipeadata SCN10 (FBKFN10/PIBN10 nominais) menos FGV, anos comuns 1947-2025 (pp) | -0.00 / -0.00 / +0.00 | anos de /dif/>0,5 pp: [] |


## 7. Cadeia de hash (resultado de `chain.py verify` por pasta)

| pasta | resultado |
|---|---|
| mundo/ (raiz: WDI e PIP) | 27 lines; head 4dc7d8bc097b5ad86d02863cbcc3e44d9bcde64e7f1d1542b3831e4514fe86eb; OK |
| mundo/wdi_arquivo | 28 lines; head 0bb0eb6a2c140dd83b044ad0f0c0c0d7a08fe394d6437b943473d25d796935ab; OK |
| mundo/ipea | 21 lines; head fabca4acdd6e5f29ef9bf7267b3686dab6075c3757167003220bf9da2dd404e9; OK |
| mundo/invpub | 7 lines; head 73c222971e009035a2efd80519899f13698abb4b5cc6508152f52e3a71ecbf24; OK |
| mundo/pwt_maddison | 7 lines; head fd3b8049d88c005a7353946f9797953dba9d90e58ec0134202bc7e3326829ca7; OK |
| mundo/oghist | 2 lines; head db262d936d9c6d0db762280927bc1d9a2b12ac50454b144310e8c8b9b8266752; OK |
| mundo/vdem_owid | 1 lines; head 0e13e910e6b9d805d527a34264f13a21ff4fba21c05167d4a09e6bfecf7e917d; OK |
| mundo/docs | 6 lines; head 0b4b7db6994356fe914779712904ec8359d9647688b5f9c7df496cac1d470f3f; OK |


Descoberta fora da cadeia: as buscas exploratorias que escolheram as series (catalogo de metadados do Ipeadata, paginas do rug.nl e do FGV, varredura de 54 versoes do arquivo WDI com 3 unidades e 1 ano, testes do PIP) foram feitas no scratchpad da sessao; tudo o que sustenta um numero foi re-adquirido pela cadeia (inclusive o catalogo, `ipea/bruto/ipea_catalogo_Metadados.json`). A varredura das 54 versoes nao esta na cadeia: o que entrou foram as 8 versoes do PIB pc PPC usadas nas medidas (201904, 202004, 202005, 202403, 202405, 202407, 202412, 202507).

Falhas de aquisicao registradas (nada foi omitido): PIP releases 20250401 e 20240627 (erro 500 do servidor, 4 tentativas, no log `scripts/baixar_wdi_pip.log`); uma tentativa de URL do blog 2017-ppp-poverty-lines (404, adivinhada, nao entrou no manifest). O bruto do OWID veio com todos os paises (o filtro da URL foi ignorado, 1,1 MB). Ipeadata SCN10_PIB10 e um indice real, nao o PIB nominal (baixado por engano, mantido na cadeia, nao usado); o nominal e SCN10_PIBN10. Nenhum arquivo passou de 25 MB (maior: PWT 10.01 xlsx, 6,5 MB).

## 8. Arquivos

- `series/mundo.csv`, `series/termos_de_troca.csv`, `series/crescimento_contexto.csv`: formato longo `indicador,fonte,definicao_linha,pais_ou_grupo,ano,valor,unidade,nota,vintage`.
- `janelas.csv`: indicador x governo x referencia (media Brasil, media referencia, diferenca, n_anos, quebras na janela). Para niveis/indices ha tambem a linha `<indicador>_var_pct`.
- `quebras.csv`, `medidas_efeito.csv`, `scripts/` (construir, medir, quebras, janelas, resultado; `baixar_*.sh` so com rede), `manifest.jsonl` por subpasta.
