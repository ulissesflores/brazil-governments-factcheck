# RESULTADO — dimensão monetária (governos-do-brasil-economia)

> Gerado por `montar_resultado.py` a partir de `saida/*.csv`; os números das tabelas não foram digitados. Bruto baixado em 2026-10-19 (BCB SGS, CKAN do BCB, Ipeadata), cadeia de hash em `manifest.jsonl`.
> Legenda: ✅ verificado contra fonte primária ou reproduzido · ⚠️ verificado por via indireta/inferência declarada · ❌ errado/inexistente (com prova) · ❓ não verificado/não achado.

## 0. Resumo

1. Base monetária (M0) existe em série mensal de fev/1946 a 2026 no SGS (código 1788) e M1 de fev/1946 a jun/2018 (1827) mais a série Novo de 2002 em diante (27791); papel-moeda emitido, anual de 1946 a 1979 (Ipeadata HIST_PME) e mensal de 1980 em diante (SGS 1786); M2, M3 e M4 só existem de jul/1988 em diante; **antes disso não achei série oficial digital** ❓.
2. Há **três regimes** de meios de pagamento, não dois (pré-2001, "metodologia de 2001" com séries refeitas desde jul/1988 e descontinuadas em jun/2018, e "Novo" de 2018 com série desde dez/2001). A quebra de 2018 é medida: em dez/2017 o M1 sobe 5,2%, o M3 cai 0,4% e o M4 cai 6,2% frente ao conceito antigo (a Nota Técnica 48 diz +5%, −0,4% e −6%) ✅. Recomendação: **emendar só M0 e M1; M2–M4 por razão ao PIB dentro de cada regime, com a quebra declarada**.
3. Os níveis do SGS estão na **moeda da época** (cinco cortes de zeros entre 1967 e 1994); as razões ao PIB só valem depois de converter, e o fator foi validado contra o Ipeadata (razão exata em cada trecho) ✅. O Ipeadata `BM12_M2NCN12` ("M2") traz, de jan/2002 a dez/2023, **os depósitos à vista, não o M2** ❌ (264 meses idênticos ao SGS 27790).
4. **Senhoriagem com fórmula validada**: a fórmula mensal de Cysne e Coimbra-Lisboa (2004, eq. 2) reproduz a Tabela 1 do próprio artigo (TIT/PIB 1947-2003: erro absoluto médio 0,18 p.p., correlação 0,9986) e foi estendida a 2025. A forma **anual** π/(1+π)·M0/PIB falha na hiperinflação (1980-1994: correlação −0,06, viés −1,1 p.p.), e ΔM0/PIB mistura imposto inflacionário com remonetização.
5. Hipótese "a inflação oficial esconde algo": **medida, não confirmada nem refutada**. O IPCA fecha com seus componentes (livres + monitorados, R² 0,997); os monitorados ficaram 11,2 p.p. abaixo dos livres em 2012-2014 e 9,6 p.p. acima em 2015, e o acumulado 2011-2016 ficou 3,8 p.p. abaixo. No Plano Cruzado, IPCA, INPC e IGP-DI divergem 7,8 p.p. entre mar e out/1986 (18,4% contra 10,6%-11,1%) enquanto M1 crescia 246%; fila e ágio **não são mensuráveis** com esses dados.

## 1. Séries monetárias e a quebra metodológica

### 1.1 Códigos e cobertura

| SGS | papel | nome no catálogo do BCB (CKAN) | nome só por inferência numérica | início | fim | meses |
|---|---|---|---|---|---|---|
| 1788 | M0 base restrita fim | BM - Base monetária restrita (saldo em final de período) | — | 1946-02 | 2026-08 | 967 |
| 1783 | papel-moeda em circulacao media | BM - Papel moeda em circulação (média nos dias úteis do mês) | — | 1980-02 | 2026-08 | 559 |
| 1785 | M0 base restrita media | BM - Base monetária restrita (média nos dias úteis do mês) | — | 1980-02 | 2026-08 | 559 |
| 1786 | papel-moeda em circulacao fim | BM - Papel moeda em circulação (saldo em final de período) | — | 1980-02 | 2026-08 | 559 |
| 1787 | reservas bancarias fim | BM - Reservas bancárias (saldo em final de período) | — | 1980-02 | 2026-08 | 559 |
| 1833 | base ampliada fim | Base Monetária Ampliada (saldo em final de período) | — | 1994-08 | 2026-08 | 385 |
| 1827 | M1 fim (conceito antigo) | — | M1 = 1825 + 1826 | 1946-02 | 2018-06 | 869 |
| 1824 | M1 media (antigo) | — | M1 media = 1822 + 1823 | 1980-02 | 2018-06 | 461 |
| 1835 | poupanca fim | Meios de pagamento amplos - Depósito de Poupança (saldo em final de período) | — | 1988-08 | 2026-08 | 457 |
| 1839 | compromissadas Selic fim | Meios de pagamento amplos - Operações compromissadas/Selic (saldo em final de período) | — | 1988-08 | 2026-08 | 457 |
| 1837 | M2 (reg. 2001) | — | M2 = M1 + 1835 + 1836 (+ dep. especiais remunerados 1991-2000) | 1988-08 | 2018-06 | 359 |
| 1840 | M3 (reg. 2001) | — | M3 = M2 + 1838 + 1839 | 1988-08 | 2018-06 | 359 |
| 1843 | M4 (reg. 2001) | — | M4 = M3 + 1841 + 1842 | 1988-08 | 2018-06 | 359 |
| 27791 | M1 fim Novo | Meios de pagamento - M1 (saldo em final de período) - Novo | — | 2002-01 | 2026-08 | 296 |
| 27810 | M2 fim Novo | Meios de pagamento amplos - M2 (saldo em final de período) - Novo | — | 2001-12 | 2026-08 | 297 |
| 27813 | M3 fim Novo | Meios de pagamento amplos - M3 (saldo em final de período) - Novo | — | 2001-12 | 2026-08 | 297 |
| 27815 | M4 fim Novo | Meios de pagamento amplos - M4 (saldo em final de periodo) - Novo | — | 2001-12 | 2026-08 | 297 |
| 27788 | M1 media Novo | — | — | 2002-01 | 2026-08 | 296 |

- Nomes "no catálogo do BCB" vêm do campo `codigo_sgs` do CKAN (`https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=codigo_sgs:<cod>`, bruto em `bruto/ckan_<cod>.json`) ✅. As séries **descontinuadas** 1822-1827, 1836-1838, 1840-1843 **não estão no catálogo** (1835 = poupança e 1839 = compromissadas Selic estão ✅); a página de metadados do SGS (`https://www3.bcb.gov.br/sgspub/consultarmetadados/consultarMetadadosSeries.do?method=consultarMetadadosSeriesInternet&hdOidSerieSelecionada=1837`) abre, mas responde "System unavailable" ❓. O nome delas é ⚠️ **inferência por igualdade numérica**:

| identidade testada | meses testados | meses que fecham (< 0,01%) | de | até |
|---|---|---|---|---|
| M1 fim = 1825+1826 | 461 | 461 | 1980-02 | 2018-06 |
| M1 media = 1822+1823 | 461 | 461 | 1980-02 | 2018-06 |
| M2 = 1827+1835+1836 | 359 | 219 | 1988-08 | 2018-06 |
| M3 = 1837+1838+1839 | 359 | 354 | 1988-08 | 2018-06 |
| M4 = 1840+1841+1842 | 242 | 242 | 1988-08 | 2017-10 |

- A única identidade que não fecha em todos os meses é a do M2 (219 de 359): 57 meses entre ago/1991 e dez/2007 têm resíduo de 0,5% a 8,4% do M2 (máximo em jul/1992). A Nota Metodológica de 2001 inclui no M2 os "depósitos especiais remunerados" (`https://www.bcb.gov.br/ftp/infecon/NM-MeiosPagAmplp.pdf`), componente que eu não baixei; atribuo o resíduo a ele, **não verifiquei** ❓.
- Papel-moeda emitido: SGS 1786 ("BM - Papel moeda em circulação (saldo em final de período)", catálogo do BCB ✅) de fev/1980 em diante. Antes, o Ipeadata `HIST_PME` (anual, dez): o valor de 1980 (326.309.000) é **idêntico** ao SGS 1786 de dez/1980 ✅, e a razão PME/M0 fica entre 0,51 e 0,82 de 1947 a 1979; a unidade (mil NCr$ = milhões de Cr$) é inferência minha ⚠️.
- Base ampliada: SGS 1833 só de ago/1994 ✅ (nome no catálogo); **não achei base ampliada anterior** ❓.

### 1.2 Os três regimes (links)

| regime | período das séries | definição | fonte |
|---|---|---|---|
| anterior a 2001 | publicado até jul/2001 | M2 incluía títulos públicos; M3 = M2 + poupança; M4 = M3 + títulos de instituições financeiras | Nota Metodológica de 2001, seção III, `https://www.bcb.gov.br/ftp/infecon/NM-MeiosPagAmplp.pdf` ✅. **Séries não achadas no SGS** ❓ |
| 2001 | jul/1988 a jun/2018 (refeitas pelo BCB desde jul/1988; SGS 1827, 1837, 1840, 1843) | M2 = M1 + especiais + poupança + títulos de depositárias; M3 = M2 + fundos de renda fixa + compromissadas Selic; M4 = M3 + títulos públicos | mesma nota, seções IV-V ✅; Nota Técnica 3 (ago/2001) `https://www.bcb.gov.br/conteudo/depec/NotasTecnicas/2001nt03Meiospgtop.pdf` ✅ |
| 2018 ("Novo") | dez/2001 em diante (SGS 27791, 27810, 27813, 27815) | entram cooperativas de crédito, letras financeiras/de crédito, compromissadas com títulos privados; saem os haveres de não residentes | Nota Técnica 48 (nov/2018) `http://www.ipeadata.gov.br/doc/NT%2048_Dstat_Dimob_novembro_2018.pdf` ✅ |

### 1.3 Tamanho da quebra de 2018 (mesmas datas, Novo ÷ conceito de 2001)

| agregado | dez/2001 | dez/2005 | dez/2010 | dez/2015 | dez/2017 | jun/2018 | mín | máx |
|---|---|---|---|---|---|---|---|---|
| M1 | n/d | 1,014 | 1,021 | 1,038 | 1,052 | 1,074 | 1,012 | 1,080 |
| M2 | 1,008 | 0,997 | 1,019 | 1,021 | 1,039 | 1,052 | 0,993 | 1,052 |
| M3 | 1,004 | 1,000 | 1,052 | 1,020 | 0,996 | 0,988 | 0,968 | 1,066 |
| M4 | 0,995 | 0,990 | 0,979 | 0,956 | 0,938 | 0,931 | 0,927 | 1,006 |

- Conferência com o texto do BCB (NT 48, seção 3): "em dezembro de 2017 ... M1 cresceu 5%", "M3 atual 0,4% menor", "M4 ... redução de 6%" ✅ (minha razão: +5,2%, −0,4%, −6,2%).
- O M1 Novo só começa em jan/2002; M2, M3 e M4 Novos em dez/2001 (os meses ago-nov/2001 vêm nulos no JSON do SGS).

### 1.4 Dá para emendar?

| série | emenda? | motivo |
|---|---|---|
| M0 (1946-2026) | **sim**, uma única série | o BCB publica contínua; **atenção**: o conceito de base mudou em 1980 (e foi retroagido pelo BCB só até 1980; Cysne e Coimbra-Lisboa, 2004, nota técnica a) |
| M1 | **sim, com nota**: 1827 até jun/2018, Novo (27791) a partir de jan/2002 | quebra de nível de +1,2% (mínimo) a +8,0% (máximo) na sobreposição (+5,2% em dez/2017), por causa das cooperativas |
| M2, M3, M4 | **não em nível**; razão ao PIB dentro de cada regime (2001: 1988-2001, ou até 2018 se quiser mostrar a sobreposição; Novo: 2001-2026) | M4 difere até −7,3% e M2 até +5,2%; a composição mudou (haveres de não residentes saem) |
| antes de jul/1988 | **sem série** | ❓ procurei no SGS, Ipeadata (`HIST_M2` termina em 1947) e na nota do BCB |

### 1.5 Auditoria do Ipeadata

| comparação (Ipeadata x BCB) | meses | meses iguais (< 0,01%) | primeiro igual | último igual |
|---|---|---|---|---|
| Ipeadata BM12_M2NCN12 (rotulada M2) vs BCB 27810 (M2 Novo) | 296 | 32 | 2024-01 | 2026-08 |
| Ipeadata BM12_M2NCN12 (rotulada M2) vs BCB 27790 (depositos a vista Novo) | 296 | 264 | 2002-01 | 2023-12 |
| Ipeadata BM12_M3NCN12 (rotulada M3 fim) vs BCB 27813 (M3 Novo) | 297 | 297 | 2001-12 | 2026-08 |
| Ipeadata BM12_M4NCN12 (rotulada M4 fim) vs BCB 27815 (M4 Novo) | 297 | 297 | 2001-12 | 2026-08 |
| Ipeadata BM12_M1N12 (rotulada M1 fim) vs BCB 27791 (M1 fim Novo) | 296 | 34 | 2005-09 | 2026-08 |
| Ipeadata BM12_M1N12 (rotulada M1 fim) vs BCB 27788 (M1 media Novo) | 296 | 264 | 2002-01 | 2023-12 |

- ❌ `BM12_M2NCN12` é os depósitos à vista (27790) de jan/2002 a dez/2023 e só vira o M2 verdadeiro (27810) a partir de jan/2024. Quem usar essa série do Ipeadata para M2 erra o nível em cerca de 90%. M3 e M4 do Ipeadata coincidem com o Novo desde dez/2001 e são seguros. ❌ `BM12_M1N12` (rotulada "fim de período") também erra: de jan/2002 a dez/2023 ela é a **média dos dias úteis** (SGS 27788, 264 meses idênticos), não o saldo de fim de período (27791), que o Ipeadata só passa a trazer a partir de 2024; a diferença mensal entre as duas chega a −8,9% e +6,6%. Usei sempre o SGS.

### 1.6 Razão ao PIB por governo (média de 12 saldos mensais ÷ PIB do ano; % do PIB; média dos anos da janela)

| janela (anos civis) | M0 | M1 (antigo) | M1 (Novo) | M2 (2001) | M3 (2001) | M4 (2001) | M2 (Novo) | M3 (Novo) | M4 (Novo) |
|---|---|---|---|---|---|---|---|---|---|
| Ditadura 1967-1974 (info) | 5,2 | 15,2 | n/d | n/d | n/d | n/d | n/d | n/d | n/d |
| Geisel 1974-1978 | 3,7 | 12,3 | n/d | n/d | n/d | n/d | n/d | n/d | n/d |
| Figueiredo 1979-1984 | 2,9 | 7,1 | n/d | n/d | n/d | n/d | n/d | n/d | n/d |
| Sarney 1985-1989 | 2,1 | 4,6 | n/d | 16,7 | 16,7 | 34,0 | n/d | n/d | n/d |
| Collor 1990-1992 | 1,8 | 3,0 | n/d | 14,8 | 16,4 | 20,4 | n/d | n/d | n/d |
| Itamar 1992-1994 (info) | 1,4 | 2,2 | n/d | 20,9 | 24,6 | 29,0 | n/d | n/d | n/d |
| FHC 1995-2002 (info) | 3,0 | 4,2 | 5,7 | 22,6 | 36,9 | 43,9 | 23,8 | 43,8 | 51,7 |
| Lula 2003-2010 (info) | 4,0 | 5,8 | 6,0 | 26,6 | 53,0 | 61,5 | 26,8 | 53,4 | 60,3 |
| Dilma 2011-2016 (info) | 4,1 | 5,4 | 5,6 | 35,0 | 71,1 | 83,0 | 35,7 | 73,0 | 79,2 |
| Temer 2016-2018 (info) | 3,9 | 4,9 | 5,2 | 36,3 | 82,1 | 95,2 | 37,8 | 83,7 | 90,7 |
| Bolsonaro 2019-2022 (info) | 4,3 | n/d | 6,2 | n/d | n/d | n/d | 44,4 | 92,5 | 99,3 |
| Lula 3 2023-2025 (info) | 3,6 | n/d | 5,3 | n/d | n/d | n/d | 52,4 | 97,3 | 107,5 |

Anos com dado por célula: `saida/agregados_governos.csv` (colunas `*_anos`). Atenção: M2-M4 do regime 2001 em "Sarney" usam **um único ano** (1989, porque as séries começam em ago/1988) e em "Collor" três; "FHC" mistura 7 anos do regime 2001 e 1 ano (2002) do Novo, por isso a coluna Novo de FHC é um ano só.

> [!WARNING]
> Use a média dos 12 saldos mensais, não o saldo de dezembro: com inflação alta o saldo de dezembro está a preços de dezembro e o PIB do ano a preços médios do ano. Em 1989 o M0 de dezembro dá 5,8% do PIB e a média de 12 meses dá 1,5%. As colunas "(2001)" e "(Novo)" **não são comparáveis em nível**.

## 2. Unidades monetárias: como cada série trata os cortes de zeros

| corte (BCB Museu de Valores, `https://www.bcb.gov.br/content/acessoinformacao/museudocs/pub/SintesePadroesMonetariosBrasileiros.pdf`) | data | divisor |
|---|---|---|
| Cruzeiro -> Cruzeiro Novo | 13/02/1967 | 1.000 |
| Cruzeiro -> Cruzado | 28/02/1986 | 1.000 |
| Cruzado -> Cruzado Novo | 16/01/1989 | 1.000 |
| Cruzeiro -> Cruzeiro Real | 01/08/1993 | 1.000 |
| Cruzeiro Real -> Real | 01/07/1994 | 2.750 |

Divisor acumulado até hoje para saldo de antes de fev/1967: 2,75 x 10^15 (1.000^4 x 2.750). O renome Cruzeiro Novo -> Cruzeiro (1970) e Cruzado Novo -> Cruzeiro (1990) é 1:1.

| série | unidade que publica | tratamento | status |
|---|---|---|---|
| SGS monetárias (1788, 1827, 1837, ...) | "milhares de unidades monetárias correntes" = **moeda da época** | divido por 1.000 e pelo divisor acumulado do mês (`construir.py`); o primeiro mês na unidade nova que obtive é fev/1967, mar/1986, jan/1989, ago/1993 e jul/1994 (o saldo de fev/1986 ainda vem em cruzeiros) | ✅ razão SGS/Ipeadata em M0 é potência exata de 10 (ou 2.750) em cada trecho |
| Ipeadata BM12_M0N12 e similares | R$ milhões, já convertido | usado só para validar | ✅ |
| PIB, Ipeadata SCN10_PIBN10 (IBGE) | R$ milhões, já convertido (PIB de 1964 = 9,5 x 10^-9 R$ milhões) | uso direto | ✅ |
| PIB, SGS 1207 | "Reais", já convertido, **arredondado a 2 casas**: 1963 = 0,00; 1970 = 0,07; 1980 = 4,55 | inútil antes de 1990; de 1990 a 2025 coincide com o Ipeadata (desvio máx. 1,6 x 10^-7) | ✅ |
| câmbio SGS 3692 | moeda da época (19,63 em 1943) | não usei; usei Ipeadata BM_ERVF (já convertido) | ✅ |

Base do PIB (metadados do Ipeadata): 1947-1989 Contas Nacionais Consolidadas; 1990-1994 SCN referência 1985; 1995-1999 estimativa a partir das Contas Trimestrais referência 2010; 2000 em diante SCN referência 2010 ✅. **Os níveis de PIB de bases diferentes não são estritamente homogêneos**; a razão M/PIB e o II/PIB herdam esse ruído.

## 3. PIB nominal anual 1947-2025

Série usada: Ipeadata `SCN10_PIBN10` ("PIB - preços de mercado", R$ milhões, IBGE/SCN Anual), 79 anos (1947-2025), `bruto/ipea_SCN10_PIBN10.json`, CSV em `saida/anual.csv`. Não achei série alternativa homogênea de 1947 a 1989 ❓; o PIB de 1947-1989 vem das Contas Nacionais Consolidadas, não do SCN atual.

## 4. Senhoriagem

### 4.1 Fórmulas

| símbolo | fórmula | observação |
|---|---|---|
| (a) | (M0 dez(t) − M0 dez(t−1)) / PIB(t) | emissão da base como % do PIB; **inclui crescimento real da demanda por moeda** |
| (b) | π/(1+π) × (M0 médio do ano / PIB), π = IGP-DI dez/dez | forma anual do imposto inflacionário; (b2) com IPCA dez/dez, só de 1980 |
| (c) | Σ(t=1..12) A(t) × (P(t+1) − P(t)) / P(t+1) / PIB(ano), A = M0 (II) ou M1 (TIT = II + TI) | **fórmula do artigo de Cysne e Coimbra-Lisboa (2004, eq. 2), mensal**; P = IGP-DI; A = saldo de fim de mês até 1979 e média mensal dos saldos diários de 1980 em diante; (c2) idem com a taxa mensal do IPCA |
| (d) | seigniorage(t) = (N(t) − N(t−1))/N(t) × M0(t−1)/N(t−1), N = PIB nominal | Ayres et al. (2019), apêndice C, eq. (2); (d1)+(d2) = (a) por identidade, com (d2) = variação da base real/PIB |

### 4.2 Fontes lidas (texto integral guardado no manifest)

| fonte | DOI conferido no Crossref (JSON bruto em `referencias/`) | URL | o que diz |
|---|---|---|---|
| Cysne, R. P.; Coimbra-Lisboa, P. C. (2004). Imposto inflacionário e transferências inflacionárias no Brasil: 1947-2003. Revista de Economia Política 24(4): 632-637 | 10.1590/0101-35172004-1602 ✅ | `https://doi.org/10.1590/0101-35172004-1602` (PDF: `https://www.scielo.br/j/rep/a/fFLPSd4bLmm45CZYQYQbQ4R/?format=pdf&lang=pt`) | define o imposto inflacionário como transferência por juros reais negativos pagos pela base (eq. 1, contínua) e dá a aproximação mensal (eq. 2); usa IGP-DI; Tabela 1 (1947-2003) |
| Ayres, J.; Garcia, M.; Guillén, D.; Kehoe, P. (2019). The Monetary and Fiscal History of Brazil, 1960-2016. NBER WP 25421 | 10.3386/w25421 ✅ | `https://www.nber.org/system/files/working_papers/w25421/w25421.pdf` | restrição orçamentária do governo, apêndice C eq. (2): seigniorage = ((πg − 1)/(πg)) × m(t−1), m = M/(PY); IGP-DI; Tabela 1 por subperíodo |
| Cysne (1994), Rev. Economia Política 14(3) | 10.1590/0101-31571994-0784 ✅ (só o Crossref; não li o texto) | `https://doi.org/10.1590/0101-31571994-0784` | origem da série; citada por Cysne e Coimbra-Lisboa |

**A fórmula bate com a minha?** ✅ em essência: a eq. (2) de Cysne e Coimbra-Lisboa é `J(t) = A(t) × (P(t) − P(t+1)) / P(t+1)`, mensal, somada em 12 meses e dividida pelo PIB, que é exatamente a minha (c). A minha (b) anual é a mesma ideia com um único passo por ano. A forma de Ayres et al. difere: usa o crescimento do PIB **nominal** (inflação e crescimento real) no lugar da inflação, e por isso (d1) é maior que o imposto inflacionário estrito. Observação do próprio Cysne: por causa da mudança do conceito de base em 1980 (o BB passa a ser tratado como os demais bancos), "a variável mais adequada a uma análise histórica é o total das transferências inflacionárias, TIT" (M1).

### 4.3 Reprodução da Tabela 1 de Cysne e Coimbra-Lisboa (1947-2003)

Transcrição da tabela: `referencias/cysne_coimbra_lisboa_2004_tabela1_transcrita.csv` (médias conferidas com o texto: II 1,96; TI 1,63; TIT 3,59 ✅; coluna "Inflação" bate com meu IGP-DI dez/dez: erro médio 0,15 p.p., correlação 1,000).

| série minha | contra | período | n | erro abs. médio (p.p.) | erro abs. máx. (p.p.) | ano do máx. | viés (p.p.) | correlação |
|---|---|---|---|---|---|---|---|---|
| c_II_mensal_pib | cysne_II | 1947-2003 | 57 | 0,287 | 0,998 | 1963 | -0,230 | 0,967 |
| c_II_mensal_pib | cysne_II | 1947-1979 | 33 | 0,434 | 0,998 | 1963 | -0,434 | 0,990 |
| c_II_mensal_pib | cysne_II | 1980-2003 | 24 | 0,084 | 0,352 | 1989 | 0,051 | 0,999 |
| c_II_mensal_pib | cysne_II | 1980-1994 | 15 | 0,110 | 0,352 | 1989 | 0,105 | 0,996 |
| c_II_mensal_pib | cysne_II | 1995-2003 | 9 | 0,040 | 0,104 | 2002 | -0,040 | 0,999 |
| c_TIT_mensal_pib | cysne_TIT | 1947-2003 | 57 | 0,181 | 0,554 | 1989 | 0,156 | 0,999 |
| c_TIT_mensal_pib | cysne_TIT | 1947-1979 | 33 | 0,202 | 0,415 | 1958 | 0,192 | 0,999 |
| c_TIT_mensal_pib | cysne_TIT | 1980-2003 | 24 | 0,152 | 0,554 | 1989 | 0,107 | 0,999 |
| c_TIT_mensal_pib | cysne_TIT | 1980-1994 | 15 | 0,212 | 0,554 | 1989 | 0,203 | 0,993 |
| c_TIT_mensal_pib | cysne_TIT | 1995-2003 | 9 | 0,053 | 0,116 | 2002 | -0,053 | 0,999 |
| b_anual_igpdi_pib | cysne_II | 1947-2003 | 57 | 0,726 | 3,129 | 1989 | -0,695 | 0,868 |
| b_anual_igpdi_pib | cysne_II | 1947-1979 | 33 | 0,681 | 2,270 | 1963 | -0,671 | 0,959 |
| b_anual_igpdi_pib | cysne_II | 1980-2003 | 24 | 0,789 | 3,129 | 1989 | -0,728 | 0,764 |
| b_anual_igpdi_pib | cysne_II | 1980-1994 | 15 | 1,224 | 3,129 | 1989 | -1,126 | -0,058 |
| b_anual_igpdi_pib | cysne_II | 1995-2003 | 9 | 0,065 | 0,297 | 2002 | -0,065 | 0,991 |
| a_dM0_pib | cysne_II | 1947-2003 | 57 | 0,633 | 3,916 | 1994 | 0,135 | 0,744 |
| a_dM0_pib | cysne_II | 1947-1979 | 33 | 0,544 | 2,290 | 1957 | -0,087 | 0,786 |
| a_dM0_pib | cysne_II | 1980-2003 | 24 | 0,756 | 3,916 | 1994 | 0,440 | 0,766 |
| a_dM0_pib | cysne_II | 1980-1994 | 15 | 0,975 | 3,916 | 1994 | 0,614 | 0,318 |
| a_dM0_pib | cysne_II | 1995-2003 | 9 | 0,391 | 1,074 | 1997 | 0,150 | 0,498 |

- ✅ (c) **reproduz o artigo**: TIT 1947-2003 com erro médio de 0,18 p.p.; II de 1980 em diante com 0,08 p.p. Diferenças restantes: PIB (o artigo usa PIB da FGV Dados; usei o do IBGE/SCN) e, antes de 1980, o conceito de base (base com depósitos do público no BB).
- ❌ (b) **anual falha de 1980 a 1994** (correlação −0,06, viés −1,1 p.p.): com inflação mensal de 5% a 30%, a forma anual comprime a erosão num único passo. De 1995 em diante, com inflação baixa, funciona (erro 0,065 p.p., correlação 0,99).
- ⚠️ (a) ΔM0/PIB **não é** imposto inflacionário (correlação 0,74 com o II de Cysne): em 1994 vale 4,9% do PIB contra 1,0% de II, porque o Plano Real remonetizou a economia.

Validação cruzada de (d) com Ayres et al. (Tabela 1, médias por subperíodo, % do PIB):

| subperíodo | Ayres: base real | Ayres: seigniorage | Ayres: soma | meu d2 | meu d1 | minha (a) ΔM0/PIB | meu (c) II | meu (c) TIT |
|---|---|---|---|---|---|---|---|---|
| 1960-1964 | -0,40 | 4,10 | 3,70 | -0,16 | 3,77 | 3,61 | 3,40 | 7,56 |
| 1965-1972 | -0,20 | 1,90 | 1,70 | -0,38 | 2,09 | 1,71 | 1,27 | 3,28 |
| 1973-1980 | -0,20 | 2,40 | 2,20 | -0,14 | 1,92 | 1,78 | 1,43 | 4,20 |
| 1981-1994 | -0,10 | 3,20 | 3,10 | 0,03 | 3,25 | 3,28 | 2,69 | 5,07 |
| 1995-2002 | 0,10 | 0,40 | 0,50 | -0,02 | 0,63 | 0,61 | 0,37 | 0,52 |
| 2003-2011 | 0,10 | 0,40 | 0,50 | -0,00 | 0,55 | 0,55 | 0,24 | 0,35 |
| 2012-2016 | -0,10 | 0,30 | 0,20 | -0,12 | 0,33 | 0,21 | 0,27 | 0,38 |

✅ minha (a) = soma de (3)+(4) de Ayres dentro de 0,42 p.p. nos sete subperíodos (maior desvio em 1973-1980: 1,78 contra 2,2); minha (d1) fica dentro de 0,5 p.p. da linha (4) deles.

### 4.4 Anos de pico (1980-1994), % do PIB

| ano | IGP-DI dez/dez % | Cysne II | Cysne TIT | (c) II | (c) TIT | (c2) II c/ IPCA | (b) anual | (a) ΔM0/PIB | Ayres seigniorage |
|---|---|---|---|---|---|---|---|---|---|
| 1980 | 110,2 | 2,46 | 6,27 | 2,43 | 6,21 | 2,27 | 1,75 | 1,71 | 3,22 |
| 1981 | 95,2 | 1,84 | 4,48 | 1,90 | 4,57 | 1,95 | 1,45 | 1,62 | 2,22 |
| 1982 | 99,7 | 1,97 | 4,45 | 2,04 | 4,63 | 2,10 | 1,46 | 2,00 | 2,05 |
| 1983 | 211,0 | 2,58 | 5,47 | 2,77 | 5,86 | 2,42 | 1,73 | 1,42 | 2,22 |
| 1984 | 223,8 | 2,03 | 4,26 | 2,25 | 4,73 | 2,21 | 1,34 | 2,65 | 2,19 |
| 1985 | 235,1 | 2,11 | 4,56 | 2,23 | 4,82 | 2,20 | 1,23 | 2,50 | 2,68 |
| 1986 | 65,0 | 1,34 | 3,22 | 1,40 | 3,36 | 1,91 | 1,27 | 3,81 | 2,18 |
| 1987 | 415,8 | 3,27 | 6,69 | 3,39 | 6,95 | 3,22 | 1,75 | 2,92 | 3,50 |
| 1988 | 1.037,6 | 3,45 | 6,50 | 3,68 | 6,94 | 3,66 | 1,31 | 3,88 | 3,91 |
| 1989 | 1.782,9 | 4,35 | 6,70 | 4,70 | 7,25 | 4,68 | 1,22 | 5,45 | 4,19 |
| 1990 | 1.476,7 | 3,39 | 5,28 | 3,46 | 5,38 | 3,62 | 2,02 | 4,89 | 5,55 |
| 1991 | 480,2 | 3,08 | 5,20 | 3,13 | 5,27 | 3,06 | 1,40 | 2,85 | 4,13 |
| 1992 | 1.157,8 | 2,69 | 4,59 | 2,76 | 4,75 | 2,77 | 1,06 | 3,57 | 3,47 |
| 1993 | 2.708,2 | 2,91 | 4,89 | 2,90 | 4,89 | 2,85 | 0,86 | 3,49 | 3,75 |
| 1994 | 1.093,9 | 1,00 | 1,56 | 1,00 | 1,56 | 0,94 | 1,73 | 4,92 | 3,52 |

### 4.5 Por governo (posse-saída, mês pertence a quem ocupa a presidência no dia 16)

> [!NOTE]
> As datas de posse e saída são constantes minhas no script (`senhoriagem.py`), ⚠️ **a conferir contra `fontes/dados/historia/`** (pasta vazia quando fechei esta colheita). Dilma/Temer aparecem nas duas variantes (afastamento em 12/05/2016 e impeachment em 31/08/2016). Valor da janela = média dos valores anuais ponderada pelos meses do mandato em cada ano (aproximação; anos incompletos entram com peso proporcional). A coluna de inflação é a média aritmética das taxas anuais do IGP-DI dez/dez.

| janela | meses | IGP-DI médio % a.a. | (a) ΔM0/PIB | (b) anual | (c) II mensal | (c) TIT (M1) | (c2) II c/ IPCA | Ayres seign. |
|---|---|---|---|---|---|---|---|---|
| Castelo Branco | 35 | 50,3 | 2,75 | 2,11 | 2,45 | 5,54 | n/d | 3,55 |
| Costa e Silva+Junta | 32 | 23,4 | 1,74 | 1,15 | 1,19 | 3,05 | n/d | 1,91 |
| Medici | 52 | 18,2 | 1,28 | 0,75 | 0,83 | 2,56 | n/d | 1,67 |
| Geisel | 60 | 39,4 | 1,66 | 1,05 | 1,22 | 3,90 | n/d | 1,65 |
| Figueiredo | 72 | 140,6 | 2,04 | 1,56 | 2,29 | 5,28 | 2,19 | 2,35 |
| Sarney | 60 | 748,7 | 3,79 | 1,38 | 3,12 | 5,88 | 3,18 | 3,39 |
| Collor | 31 | 998,4 | 3,72 | 1,50 | 3,13 | 5,15 | 3,16 | 4,39 |
| Itamar | 27 | 1.818,5 | 4,13 | 1,27 | 2,04 | 3,39 | 2,00 | 3,61 |
| FHC | 96 | 12,5 | 0,61 | 0,34 | 0,37 | 0,52 | 0,26 | 0,63 |
| Lula 1-2 | 96 | 6,5 | 0,59 | 0,24 | 0,25 | 0,36 | 0,22 | 0,55 |
| Dilma (ate afastamento 12/05/2016) | 64 | 6,7 | 0,20 | 0,25 | 0,26 | 0,36 | 0,28 | 0,39 |
| Temer (de 12/05/2016, interino) | 32 | 4,3 | 0,24 | 0,15 | 0,14 | 0,19 | 0,14 | 0,23 |
| Dilma (ate 31/08/2016) | 68 | 6,7 | 0,20 | 0,25 | 0,26 | 0,36 | 0,27 | 0,38 |
| Temer (de 31/08/2016) | 28 | 3,9 | 0,24 | 0,14 | 0,13 | 0,18 | 0,14 | 0,23 |
| Bolsonaro | 48 | 13,4 | 0,39 | 0,51 | 0,57 | 0,80 | 0,27 | 0,43 |
| Lula 3 | 36 | 0,8 | 0,08 | 0,02 | 0,03 | 0,04 | 0,16 | 0,30 |

Janelas do infográfico (anos civis, como no CSV transcrito):

| janela | meses | IGP-DI médio % a.a. | (a) ΔM0/PIB | (b) anual | (c) II mensal | (c) TIT (M1) | (c2) II c/ IPCA | Ayres seign. |
|---|---|---|---|---|---|---|---|---|
| Ditadura 1967-1974 (info) | 96 | 21,8 | 1,43 | 0,92 | 0,99 | 2,88 | n/d | 1,76 |
| Itamar 1992-1994 (info) | 36 | 1.653,3 | 3,99 | 1,22 | 2,22 | 3,73 | 2,19 | 3,58 |
| FHC 1995-2002 (info) | 96 | 12,5 | 0,61 | 0,34 | 0,37 | 0,52 | 0,26 | 0,63 |
| Lula 2003-2010 (info) | 96 | 6,5 | 0,59 | 0,24 | 0,25 | 0,36 | 0,22 | 0,55 |
| Dilma 2011-2016 (info) | 72 | 6,7 | 0,20 | 0,25 | 0,26 | 0,36 | 0,27 | 0,37 |
| Temer 2016-2018 (info) | 36 | 4,6 | 0,24 | 0,17 | 0,15 | 0,20 | 0,15 | 0,22 |
| Bolsonaro 2019-2022 (info) | 48 | 13,4 | 0,39 | 0,51 | 0,57 | 0,80 | 0,27 | 0,43 |
| Lula 3 2023-2025 (info) | 36 | 0,8 | 0,08 | 0,02 | 0,03 | 0,04 | 0,16 | 0,30 |
| Pico 1980-1994 | 180 | 746,2 | 3,18 | 1,44 | 2,67 | 5,14 | 2,66 | 3,25 |
| Pos-Real 1995-2003 | 108 | 12,0 | 0,54 | 0,33 | 0,35 | 0,50 | 0,26 | 0,63 |

### 4.6 Quatro ressalvas de leitura

1. O IGP-DI é índice de atacado e câmbio: em 2002 (26,4%) e 2020 (23,1%) infla o imposto inflacionário frente ao IPCA (12,5% e 4,5%). Em 2020 o (c) dá II = 1,19% do PIB e o (c2) com IPCA dá 0,24%. Para o período do IPCA-alvo (pós-1999), prefira (c2) ou mostre os dois.
2. O imposto inflacionário (c) usa a base **real** perdida; ele não é "receita do governo" no mesmo sentido do déficit primário (Ayres et al. documentam que boa parte da senhoriagem financiou o Banco do Brasil).
3. Antes de 1980 o II (base) tem quebra de conceito; use o TIT (M1).
4. O PIB de 1947-1989 vem de outra base do IBGE que o de 2000 em diante (seção 2).

## 5. Extras fiscais e monetários por governo (anos civis)

Convenções: câmbio = R$/US$ comercial venda, fim de período (Ipeadata BM_ERVF); Selic = produto das taxas "over" mensais (Ipeadata BM12_TJOVER12, cobre desde 1974; **não verifiquei a comparabilidade da taxa "over" antes de 1986** ❓; o juro real anual com inflação alta é muito ruidoso); juro real ex-post = (1+Selic)/(1+inflação)−1; resultado primário = −NFSP (positivo = superávit). CSV anual: `saida/extras_anual.csv`.

| janela | câmbio: fator fim/início | Selic over média % a.a. | juro real médio (IPCA) % | juro real médio (IGP-DI) % | primário médio GF+BC % PIB | primário médio consol. % PIB |
|---|---|---|---|---|---|---|
| Medici 1970-1973 | 1,43 | n/d | n/d | n/d | n/d | n/d |
| Geisel 1974-1978 | 3,36 | 33,7 | n/d | -3,2 | n/d | n/d |
| Figueiredo 1979-1984 | 152,20 | 125,5 | 0,7 | -6,2 | n/d | n/d |
| Sarney 1985-1989 | 3.567,21 | 1.023,6 | 9,0 | 8,8 | n/d | n/d |
| Collor 1990-1992 | 1.090,64 | 1.079,8 | 6,4 | 6,8 | 1,04 | n/d |
| Itamar 1992-1994 (info) | 2.176,74 | 1.921,0 | 27,1 | 16,2 | 1,72 | n/d |
| FHC 1995-2002 | 4,18 | 26,7 | 15,9 | 13,1 | 1,08 | 3,19 |
| Lula 2003-2010 | 0,47 | 14,7 | 8,4 | 8,0 | 2,18 | 3,12 |
| Dilma 2011-2016 (info) | 1,96 | 11,1 | 3,9 | 4,1 | 0,08 | 0,32 |
| Temer 2016-2018 (info) | 0,99 | 10,1 | 5,6 | 5,4 | -2,00 | -1,90 |
| Bolsonaro 2019-2022 | 1,35 | 6,4 | 0,3 | -5,6 | -2,71 | -2,03 |
| Lula 3 2023-2025 | 1,05 | 12,7 | 7,8 | 12,1 | -1,09 | -1,04 |

| janela | DLSP GF+BC %PIB (início -> fim) | DLSP consolidado %PIB (início -> fim) | DBGG método até 2007 (início -> fim) | DBGG método desde 2008 (início -> fim) | reservas US$ mi (início -> fim) |
|---|---|---|---|---|---|
| Medici 1970-1973 | n/d -> n/d | n/d -> n/d | n/d -> n/d | n/d -> n/d | n/d -> 6.416 |
| Geisel 1974-1978 | n/d -> n/d | n/d -> n/d | n/d -> n/d | n/d -> n/d | 6.416 -> 11.895 |
| Figueiredo 1979-1984 | n/d -> 27,5 | n/d -> n/d | n/d -> n/d | n/d -> n/d | 11.895 -> 11.995 |
| Sarney 1985-1989 | 27,5 -> 73,2 | n/d -> n/d | n/d -> n/d | n/d -> n/d | 11.995 -> 9.679 |
| Collor 1990-1992 | 73,2 -> 34,6 | n/d -> n/d | n/d -> n/d | n/d -> n/d | 9.679 -> 23.754 |
| Itamar 1992-1994 (info) | 31,2 -> 18,9 | n/d -> n/d | n/d -> n/d | n/d -> n/d | 9.406 -> 38.806 |
| FHC 1995-2002 | 18,9 -> 37,7 | n/d -> 59,9 | n/d -> 76,1 | n/d -> n/d | 38.806 -> 37.823 |
| Lula 2003-2010 | 37,7 -> 25,8 | 59,9 -> 38,0 | 76,1 -> 62,4 | n/d -> 51,8 | 37.823 -> 288.575 |
| Dilma 2011-2016 (info) | 25,8 -> 33,3 | 38,0 -> 46,1 | 62,4 -> 77,4 | 51,8 -> 69,8 | 288.575 -> 365.016 |
| Temer 2016-2018 (info) | 21,9 -> 39,5 | 35,6 -> 52,8 | 71,7 -> 84,8 | 65,5 -> 75,3 | 356.464 -> 374.715 |
| Bolsonaro 2019-2022 | 39,5 -> 47,0 | 52,8 -> 56,1 | 84,8 -> 83,9 | 75,3 -> 71,7 | 374.715 -> 324.703 |
| Lula 3 2023-2025 | 47,0 -> 56,5 | 56,1 -> 65,2 | 83,9 -> 93,3 | 71,7 -> 78,6 | 324.703 -> 358.234 |

- ✅ Dívida bruta (DBGG): o BCB publica **duas** séries em paralelo, "metodologia até 2007" (SGS 4537, desde jan/2002) e "desde 2008" (SGS 13762, desde dez/2006); o nível difere em cerca de 8 a 15 p.p. do PIB. Nunca misture. A DLSP consolidada (SGS 4513) e a dívida líquida do governo geral (SGS 4536) começam em 2001-2002; para 1981-2000 só tenho a DLSP de governo federal + Banco Central (Ipeadata BM_DTGFN, "inclui a base monetária" como passivo ✅ pelo metadado).
- ⚠️ Razão estoque de dezembro / PIB do ano fica inflada em anos de inflação alta (1989: DLSP GF+BC = 73% do PIB, 1990: 10%): não compare Sarney com os demais por esse número.
- Primário: GF+BC desde 1991 (Ipeadata BM12_NFGFPYS12); consolidado desde nov/2002 (SGS 5793). ❓ **Antes de 1991 não achei série oficial** (Ayres et al. usam o IBGE, Estatísticas do Século XX, que não baixei).
- Reservas internacionais: Ipeadata BM_RES (estoque de dezembro, US$ milhões) ✅; não confirmei o conceito (liquidez internacional) ⚠️.

## 6. Teste da hipótese "a inflação oficial esconde algo" (medida, sem endosso)

> [!IMPORTANT]
> O SGS **11427 não é "preços administrados"**: o catálogo do BCB o chama "IPCA - Núcleo por exclusão - Sem monitorados e alimentos no domicílio" ✅. O par correto é **11428 (itens livres)** e **4449 (preços monitorados - total)**, ambos desde jan/1991. "Administrados" é o nome antigo de "monitorados".

Códigos: 11428 = "IPCA - Itens livres" (catálogo do BCB ✅); 4449 = "IPCA - Preços monitorados - Total" (catálogo ✅); 433 = IPCA geral. Cada um bate com a série homônima do Ipeadata (`PRECOS12_IPCAG12`: 561 de 561 meses iguais; `BM12_IPCAPL12` e `BM12_IPCAPM12`: iguais até o arredondamento de 0,01) ✅.

### 6.1 Livres x monitorados, 2010-2017 (variação anual do IPCA, %)

| ano | IPCA | livres (11428) | monitorados (4449) | monitorados − livres (p.p.) | IGP-DI | INPC |
|---|---|---|---|---|---|---|
| 2010 | 5,91 | 7,08 | 3,13 | -3,95 | 11,31 | 6,46 |
| 2011 | 6,50 | 6,65 | 6,20 | -0,45 | 5,01 | 6,08 |
| 2012 | 5,84 | 6,55 | 3,65 | -2,90 | 8,11 | 6,20 |
| 2013 | 5,91 | 7,31 | 1,54 | -5,77 | 5,53 | 5,56 |
| 2014 | 6,41 | 6,74 | 5,32 | -1,42 | 3,78 | 6,23 |
| 2015 | 10,67 | 8,49 | 18,07 | 9,58 | 10,68 | 11,28 |
| 2016 | 6,29 | 6,55 | 5,50 | -1,05 | 7,15 | 6,58 |
| 2017 | 2,95 | 1,35 | 7,99 | 6,64 | -0,42 | 2,07 |

Acumulados:

| janela | IPCA | livres | monitorados | IGP-DI | INPC | monitorados − livres (p.p.) |
|---|---|---|---|---|---|---|
| 2013-01..2015-12 | 24,73 | 24,27 | 26,27 | 21,21 | 24,78 | 2,00 |
| 2012-01..2014-12 | 19,28 | 22,04 | 10,84 | 18,40 | 19,09 | -11,20 |
| 2012-01..2016-12 | 40,31 | 41,08 | 38,08 | 40,42 | 41,24 | -3,00 |
| 2011-01..2016-12 | 49,43 | 50,46 | 46,64 | 47,46 | 49,82 | -3,82 |
| 2015-01..2015-12 | 10,67 | 8,49 | 18,07 | 10,68 | 11,28 | 9,58 |
| 2003-01..2010-12 | 56,68 | 54,99 | 60,74 | 63,83 | 57,04 | 5,75 |
| 2017-01..2022-12 | 35,56 | 34,20 | 39,62 | 74,74 | 35,73 | 5,42 |

Peso implícito dos monitorados no IPCA (regressão de IPCA − livres sobre monitorados − livres, mensal, sem intercepto): o IPCA fecha com seus componentes.

| janela | peso implícito dos monitorados | R2 | meses |
|---|---|---|---|
| 2011-01..2016-12 | 0,238 | 0,9972 | 72 |
| 2012-01..2014-12 | 0,237 | 0,9989 | 36 |
| 2015-01..2015-12 | 0,233 | 0,9994 | 12 |
| 2017-01..2025-12 | 0,259 | 0,9990 | 108 |

**O que se mede:** (i) o IPCA é aritmeticamente coerente com livres + monitorados (peso de cerca de 24%, R² > 0,997); (ii) em 2012-2014 os monitorados subiram 10,8% contra 22,0% dos livres (−11,2 p.p.) e em 2015 subiram 18,1% contra 8,5% (+9,6 p.p.); (iii) em 2013-2015 o saldo é de +2,0 p.p. a favor dos monitorados; em 2011-2016 fecha em −3,8 p.p.; (iv) IGP-DI e INPC ficam na mesma ordem de grandeza do IPCA nos acumulados de 2013-2015 (IGP-DI 21,2%, INPC 24,8%, IPCA 24,7%). **O que não se mede:** se o preço do item monitorado foi "represado" por decisão administrativa (a série só mostra o preço que foi coletado) nem o efeito sobre expectativas. Diferença cumulativa 2011-2016 de 3,8 p.p. nos monitorados corresponde a cerca de 0,9 p.p. no IPCA acumulado (peso 24%), contra IPCA acumulado de 49,4% no período.

### 6.2 Plano Cruzado (congelamento de 28/02/1986)

| mês | IPCA | INPC | IGP-DI | máx − mín (p.p.) | M0 var. no mês % | M1 var. no mês % |
|---|---|---|---|---|---|---|
| 1985-12 | 15,07 | 15,75 | 13,20 | 2,55 | 41,62 | 33,44 |
| 1986-01 | 14,37 | 15,01 | 17,79 | 3,42 | 1,04 | -8,79 |
| 1986-02 | 12,72 | 12,46 | 14,98 | 2,52 | 12,18 | 14,10 |
| 1986-03 | 4,77 | 3,18 | 5,52 | 2,34 | 35,89 | 80,21 |
| 1986-04 | 0,78 | 0,43 | -0,58 | 1,36 | 35,35 | 19,27 |
| 1986-05 | 1,40 | 1,08 | 0,32 | 1,08 | 15,03 | 15,34 |
| 1986-06 | 1,27 | 0,97 | 0,53 | 0,74 | 10,57 | 15,64 |
| 1986-07 | 1,71 | 0,91 | 0,63 | 1,08 | 14,11 | -0,23 |
| 1986-08 | 3,55 | 1,43 | 1,33 | 2,22 | 5,99 | 6,87 |
| 1986-09 | 1,72 | 1,19 | 1,09 | 0,63 | 2,78 | 5,53 |
| 1986-10 | 1,90 | 1,43 | 1,39 | 0,51 | 5,17 | 7,27 |
| 1986-11 | 5,45 | 3,29 | 2,46 | 2,99 | 9,42 | 4,63 |
| 1986-12 | 11,65 | 7,27 | 7,56 | 4,38 | 3,73 | 7,95 |
| 1987-01 | 13,21 | 16,82 | 12,04 | 4,78 | -3,61 | -21,83 |
| 1987-02 | 12,64 | 13,94 | 14,11 | 1,47 | -4,72 | 6,02 |
| 1987-03 | 16,37 | 14,40 | 15,00 | 1,97 | 2,98 | 12,59 |

| janela | IPCA % | INPC % | IGP-DI % | M0 fim % | M1 fim % | M1 real (M1/IGP-DI) % |
|---|---|---|---|---|---|---|
| pre-congelamento 1985-03..1986-02 (12m) | 256,1 | 253,4 | 265,8 | 242,0 | 314,3 | 13,3 |
| congelamento 1986-03..1986-10 | 18,4 | 11,1 | 10,6 | 205,8 | 246,0 | 212,9 |
| 1986-03..1986-11 | 24,8 | 14,8 | 13,3 | 234,6 | 262,0 | 219,6 |
| ano 1986 | 79,7 | 59,2 | 65,0 | 293,5 | 306,8 | 146,5 |
| pos-congelamento 1987-01..1987-12 | 363,4 | 394,6 | 415,9 | 181,5 | 127,4 | -55,9 |
| 1986-03..1987-12 | 545,8 | 508,9 | 528,7 | 877,1 | 788,9 | 41,4 |

**O que se mede:** (i) os três índices mostram queda forte da inflação em mar-out/1986 e concordam no sentido, mas **não no tamanho**: IPCA acumula 18,4% e INPC 11,1% e IGP-DI 10,6% em mar-out (7,8 p.p. de diferença), com picos de divergência em mar (2,3 p.p.), ago (2,2 p.p.), nov (3,0 p.p.) e dez/1986 (4,4 p.p.); (ii) no mesmo período a base (M0) cresceu 206% e o M1 246%, e o M1 em termos reais (M1/IGP-DI) cresceu 213%; (iii) em 1987 a inflação volta (IGP-DI 415,9%, IPCA 363,4%) e o M1 real cai 56%. **O que não se mede:** fila, ágio e desabastecimento (preço pago acima da tabela), que são o núcleo da hipótese de inflação reprimida; nenhuma série de preços oficial os captura ❓. O período de coleta difere entre índices (o IGP-DI mede do dia 1 ao 30 do mês, pelo metadado do Ipeadata; o do IPCA não verifiquei ❓), o que explica parte da divergência de março.

## 7. O que NÃO achei

| item | situação |
|---|---|
| M2, M3, M4 antes de jul/1988 | ❓ nenhuma série oficial digital; a nota do BCB reconstrói só desde jul/1988 |
| M2, M3, M4 do conceito anterior a 2001 (como publicados) | ❓ não achei no SGS |
| base ampliada antes de ago/1994 | ❓ SGS 1833 começa em ago/1994 |
| nomes dos SGS 1822-1827, 1836-1838, 1840-1843 no catálogo | ❓ descontinuados; nome só por inferência numérica (⚠️); página do SGS indisponível |
| resultado primário antes de 1991 | ❓ |
| SGS 4380 e 4382 (PIB mensal) | baixados; **não aparecem no catálogo CKAN** pelo campo `codigo_sgs`, por isso não usei |
| artigo de Cysne (1994) e Simonsen e Cysne (1995) | ❓ só o Crossref; texto não lido |
| fila, ágio e desabastecimento no Cruzado | ❓ não mensurável com índices |
| revisão humana das datas de mandato | ⚠️ pendente (`historia/`) |

## 8. Fórmula final recomendada para o artigo

1. **Dizer duas coisas distintas**, com nomes distintos: (i) *emissão primária* = ΔM0/PIB (fórmula a); (ii) *imposto inflacionário* = fórmula (c) de Cysne e Coimbra-Lisboa (2004). A primeira inclui a remonetização (1994: 4,9% do PIB); a segunda é o que a inflação cobrou de quem segurava moeda.
2. **Série principal:** `II/PIB = Σ(12 meses) M0(t) × (P(t+1) − P(t)) / P(t+1) ÷ PIB(ano)`, P = IGP-DI, M0 = média mensal dos saldos diários (1980 em diante) e saldo de fim de mês antes; e `TIT/PIB` com M1 no lugar de M0 para comparar 1947-2025 sem a quebra do conceito de base. Fonte: `saida/senhoriagem_anual.csv`, colunas `c_II_mensal_pib` e `c_TIT_mensal_pib`; de 1999 em diante, mostrar também `c2_II_ipca_pib` (IPCA).
3. **Não usar** a forma anual π/(1+π)·M0/PIB para 1980-1994 (✅ medido: falha). Pode servir de intuição didática com inflação baixa.
4. **Razão M/PIB:** M0 e M1 em série única; M2-M4 em duas séries (2001 até 2018; Novo de dez/2001 em diante) com a quebra de 2018 declarada; sempre média de 12 saldos ÷ PIB.
5. Por governo: usar as janelas posse-saída da seção 4.5 depois de conferir as datas, ou as janelas do infográfico se o artigo quiser comparar diretamente.

## 9. Reprodução

- Tudo o que foi baixado está em `bruto/` e `referencias/`, com `manifest.jsonl` (cadeia de hash; `python3 -I /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py verify /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/monetario`). Os arquivos baixados antes do protocolo entram como "metadata reconstruida" com timestamp = mtime; os `.txt` derivados do `pdftotext` e a transcrição da Tabela 1 estão marcados "DERIVADO".
- Scripts sem rede, na ordem: `python3 -I construir.py`, `senhoriagem.py`, `extras.py`, `agregados.py`, `hipotese.py`, `montar_resultado.py`. Os baixadores com rede são `baixar.py` e `baixar_ckan.py`; `registrar_pendentes.py` (sem rede) registra no manifest o que eles salvaram. Linhas 69, 70 e 74 do manifest trazem URL errada (conteúdo é `package_show`); a correção está nas linhas seguintes, sem editar as antigas.
- Saídas: `saida/` (CSV regeneráveis; não entram no manifest).
