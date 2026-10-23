# Monta RESULTADO.md a partir de saida/*.csv (numeros das tabelas vem dos CSV, nao digitados). SEM REDE.
# Rodar na ordem: construir.py, senhoriagem.py, extras.py, agregados.py, hipotese.py, montar_resultado.py   (todos com python3 -I)
import csv, pathlib
AQUI = pathlib.Path(__file__).resolve().parent; S = AQUI / "saida"
def rd(n): return list(csv.DictReader(open(S / n)))
def tab(cabecalho, linhas):
    return "\n".join(["| " + " | ".join(cabecalho) + " |", "|" + "|".join(["---"] * len(cabecalho)) + "|"] + ["| " + " | ".join(str(x) for x in l) + " |" for l in linhas])
def f(x, n=2, vazio="n/d"):
    if x in ("", None, "nan"): return vazio
    x = float(x)
    return f"{x:,.{n}f}".replace(",", "_").replace(".", ",").replace("_", ".") if abs(x) < 1e6 else f"{x:.3g}".replace(".", ",")
def fs(x, n=3):  # notacao curta para numeros muito pequenos/grandes
    return "n/d" if x in ("", None) else f"{float(x):.{n}g}".replace(".", ",")

AN = {int(r["ano"]): r for r in rd("senhoriagem_anual.csv")}
# ---------- tabelas ----------
t_cob = tab(["SGS", "papel", "nome no catálogo do BCB (CKAN)", "nome só por inferência numérica", "início", "fim", "meses"],
            [[r["sgs"], r["papel"], r["nome_no_catalogo_CKAN_BCB"] or "—", r["nome_por_inferencia_numerica"] or "—", r["primeiro_mes"], r["ultimo_mes"], r["n_meses"]] for r in rd("agregados_cobertura.csv")])
t_id = tab(["identidade testada", "meses testados", "meses que fecham (< 0,01%)", "de", "até"], [[r["identidade"], r["meses_testados"], r["meses_com_diferenca_menor_que_0_01pct"], r["de"], r["ate"]] for r in rd("agregados_identidades.csv")])
q = rd("agregados_quebra_2018.csv")
kq = [k for k in q[0] if k.startswith("dez2017")][0]
t_q = tab(["agregado", "dez/2001", "dez/2005", "dez/2010", "dez/2015", "dez/2017", "jun/2018", "mín", "máx"],
          [[r["agregado"], f(r["razao_novo_sobre_antigo_dez2001"], 3), f(r["dez2005"], 3), f(r["dez2010"], 3), f(r["dez2015"], 3), f(r[kq], 3), f(r["jun2018"], 3), f(r["minimo"], 3), f(r["maximo"], 3)] for r in q])
t_ipea = tab(["comparação (Ipeadata x BCB)", "meses", "meses iguais (< 0,01%)", "primeiro igual", "último igual"], [list(r.values()) for r in rd("agregados_ipea_auditoria.csv")])
t_gov_m = tab(["janela (anos civis)", "M0", "M1 (antigo)", "M1 (Novo)", "M2 (2001)", "M3 (2001)", "M4 (2001)", "M2 (Novo)", "M3 (Novo)", "M4 (Novo)"],
              [[r["janela"]] + [f(r[k + "_media_pct_PIB"], 1) for k in ("M0", "M1", "M1novo", "M2_2001", "M3_2001", "M4_2001", "M2_novo", "M3_novo", "M4_novo")] for r in rd("agregados_governos.csv")])
t_rep = tab(["série minha", "contra", "período", "n", "erro abs. médio (p.p.)", "erro abs. máx. (p.p.)", "ano do máx.", "viés (p.p.)", "correlação"],
            [[r["serie_minha"], r["serie_cysne"], r["periodo"], r["n"], f(r["erro_abs_medio_pp"], 3), f(r["erro_abs_max_pp"], 3), r["ano_do_max"], f(r["vies_medio_pp"], 3), f(r["correlacao"], 3)]
             for r in rd("reproducao_cysne.csv") if r["serie_minha"] in ("c_II_mensal_pib", "c_TIT_mensal_pib", "b_anual_igpdi_pib", "a_dM0_pib") and r["periodo"] in ("1947-2003", "1947-1979", "1980-2003", "1980-1994", "1995-2003")])
t_ay = tab(["subperíodo", "Ayres: base real", "Ayres: seigniorage", "Ayres: soma", "meu d2", "meu d1", "minha (a) ΔM0/PIB", "meu (c) II", "meu (c) TIT"],
           [[r["subperiodo"]] + [f(r[k], 2) for k in list(r)[1:]] for r in rd("validacao_ayres.csv")])
anos_pico = list(range(1980, 1995))
t_pico = tab(["ano", "IGP-DI dez/dez %", "Cysne II", "Cysne TIT", "(c) II", "(c) TIT", "(c2) II c/ IPCA", "(b) anual", "(a) ΔM0/PIB", "Ayres seigniorage"],
             [[y, f(AN[y]["infl_igpdi_pct"], 1), f(AN[y]["cysne_II"]), f(AN[y]["cysne_TIT"]), f(AN[y]["c_II_mensal_pib"]), f(AN[y]["c_TIT_mensal_pib"]), f(AN[y]["c2_II_ipca_pib"]),
               f(AN[y]["b_anual_igpdi_pib"]), f(AN[y]["a_dM0_pib"]), f(AN[y]["d1_ayres_seigniorage"])] for y in anos_pico])
J = rd("senhoriagem_janelas.csv")
ordem_gov = ["Castelo Branco", "Costa e Silva+Junta", "Medici", "Geisel", "Figueiredo", "Sarney", "Collor", "Itamar", "FHC", "Lula 1-2", "Dilma (ate afastamento 12/05/2016)", "Temer (de 12/05/2016, interino)",
             "Dilma (ate 31/08/2016)", "Temer (de 31/08/2016)", "Bolsonaro", "Lula 3"]
Jm = {r["janela"]: r for r in J}
def linha_j(r): return [r["janela"], r["meses"], f(r["infl_igpdi_pct"], 1), f(r["a_dM0_pib"]), f(r["b_anual_igpdi_pib"]), f(r["c_II_mensal_pib"]), f(r["c_TIT_mensal_pib"]), f(r["c2_II_ipca_pib"]), f(r["d1_ayres_seigniorage"])]
cab_j = ["janela", "meses", "IGP-DI médio % a.a.", "(a) ΔM0/PIB", "(b) anual", "(c) II mensal", "(c) TIT (M1)", "(c2) II c/ IPCA", "Ayres seign."]
t_gov_s = tab(cab_j, [linha_j(Jm[n]) for n in ordem_gov])
t_info_s = tab(cab_j, [linha_j(r) for r in J if r["tipo"] == "anos civis"])
E = rd("extras_janelas.csv")
def e(r, k, n=1): return f(r.get(k), n)
t_ext1 = tab(["janela", "câmbio: fator fim/início", "Selic over média % a.a.", "juro real médio (IPCA) %", "juro real médio (IGP-DI) %", "primário médio GF+BC % PIB", "primário médio consol. % PIB"],
             [[r["janela"], f(r["cambio_fator"], 2), f(r["selic_media"], 1), f(r["juro_real_ipca_medio"], 1), f(r["juro_real_igpdi_medio"], 1), f(r["primario_gfbc_medio"], 2), f(r["primario_cons_medio"], 2)] for r in E])
t_ext2 = tab(["janela", "DLSP GF+BC %PIB (início -> fim)", "DLSP consolidado %PIB (início -> fim)", "DBGG método até 2007 (início -> fim)", "DBGG método desde 2008 (início -> fim)", "reservas US$ mi (início -> fim)"],
             [[r["janela"], f"{e(r,'dlsp_gfbc_pib_ini')} -> {e(r,'dlsp_gfbc_pib_fim')}", f"{e(r,'dlsp_cons_pib_ini')} -> {e(r,'dlsp_cons_pib_fim')}", f"{e(r,'dbgg_ate2007_ini')} -> {e(r,'dbgg_ate2007_fim')}",
               f"{e(r,'dbgg_desde2008_ini')} -> {e(r,'dbgg_desde2008_fim')}", f"{e(r,'reservas_USDmi_ini',0)} -> {e(r,'reservas_USDmi_fim',0)}"] for r in E])
H = rd("hipotese_livres_monitorados.csv")
t_h1 = tab(["ano", "IPCA", "livres (11428)", "monitorados (4449)", "monitorados − livres (p.p.)", "IGP-DI", "INPC"],
           [[r["ano"], f(r["ipca"]), f(r["ipca_livres_11428"]), f(r["ipca_monitorados_4449"]), f(r["monitorados_menos_livres_pp"]), f(r["igp_di"]), f(r["inpc"])] for r in H if 2010 <= int(r["ano"]) <= 2017])
t_h2 = tab(["janela", "IPCA", "livres", "monitorados", "IGP-DI", "INPC", "monitorados − livres (p.p.)"], [[r["janela"]] + [f(r[k]) for k in list(r)[1:]] for r in rd("hipotese_acumulados.csv")])
t_h3 = tab(["janela", "peso implícito dos monitorados", "R2", "meses"], [[r["janela"], f(r["peso_implicito_monitorados"], 3), f(r["R2"], 4), r["meses"]] for r in rd("hipotese_peso_implicito.csv")])
t_c1 = tab(["mês", "IPCA", "INPC", "IGP-DI", "máx − mín (p.p.)", "M0 var. no mês %", "M1 var. no mês %"], [[r["mes"]] + [f(r[k]) for k in list(r)[1:]] for r in rd("hipotese_cruzado_mensal.csv") if "1985-12" <= r["mes"] <= "1987-03"])
t_c2 = tab(["janela", "IPCA %", "INPC %", "IGP-DI %", "M0 fim %", "M1 fim %", "M1 real (M1/IGP-DI) %"], [[r["janela"]] + [f(r[k], 1) for k in list(r)[1:]] for r in rd("hipotese_cruzado_acumulados.csv")])

md = f"""# RESULTADO — dimensão monetária (governos-do-brasil-economia)

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

{t_cob}

- Nomes "no catálogo do BCB" vêm do campo `codigo_sgs` do CKAN (`https://dadosabertos.bcb.gov.br/api/3/action/package_search?q=codigo_sgs:<cod>`, bruto em `bruto/ckan_<cod>.json`) ✅. As séries **descontinuadas** 1822-1827, 1836-1838, 1840-1843 **não estão no catálogo** (1835 = poupança e 1839 = compromissadas Selic estão ✅); a página de metadados do SGS (`https://www3.bcb.gov.br/sgspub/consultarmetadados/consultarMetadadosSeries.do?method=consultarMetadadosSeriesInternet&hdOidSerieSelecionada=1837`) abre, mas responde "System unavailable" ❓. O nome delas é ⚠️ **inferência por igualdade numérica**:

{t_id}

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

{t_q}

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

{t_ipea}

- ❌ `BM12_M2NCN12` é os depósitos à vista (27790) de jan/2002 a dez/2023 e só vira o M2 verdadeiro (27810) a partir de jan/2024. Quem usar essa série do Ipeadata para M2 erra o nível em cerca de 90%. M3 e M4 do Ipeadata coincidem com o Novo desde dez/2001 e são seguros. ❌ `BM12_M1N12` (rotulada "fim de período") também erra: de jan/2002 a dez/2023 ela é a **média dos dias úteis** (SGS 27788, 264 meses idênticos), não o saldo de fim de período (27791), que o Ipeadata só passa a trazer a partir de 2024; a diferença mensal entre as duas chega a −8,9% e +6,6%. Usei sempre o SGS.

### 1.6 Razão ao PIB por governo (média de 12 saldos mensais ÷ PIB do ano; % do PIB; média dos anos da janela)

{t_gov_m}

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

{t_rep}

- ✅ (c) **reproduz o artigo**: TIT 1947-2003 com erro médio de 0,18 p.p.; II de 1980 em diante com 0,08 p.p. Diferenças restantes: PIB (o artigo usa PIB da FGV Dados; usei o do IBGE/SCN) e, antes de 1980, o conceito de base (base com depósitos do público no BB).
- ❌ (b) **anual falha de 1980 a 1994** (correlação −0,06, viés −1,1 p.p.): com inflação mensal de 5% a 30%, a forma anual comprime a erosão num único passo. De 1995 em diante, com inflação baixa, funciona (erro 0,065 p.p., correlação 0,99).
- ⚠️ (a) ΔM0/PIB **não é** imposto inflacionário (correlação 0,74 com o II de Cysne): em 1994 vale 4,9% do PIB contra 1,0% de II, porque o Plano Real remonetizou a economia.

Validação cruzada de (d) com Ayres et al. (Tabela 1, médias por subperíodo, % do PIB):

{t_ay}

✅ minha (a) = soma de (3)+(4) de Ayres dentro de 0,42 p.p. nos sete subperíodos (maior desvio em 1973-1980: 1,78 contra 2,2); minha (d1) fica dentro de 0,5 p.p. da linha (4) deles.

### 4.4 Anos de pico (1980-1994), % do PIB

{t_pico}

### 4.5 Por governo (posse-saída, mês pertence a quem ocupa a presidência no dia 16)

> [!NOTE]
> As datas de posse e saída são constantes minhas no script (`senhoriagem.py`), ⚠️ **a conferir contra `fontes/dados/historia/`** (pasta vazia quando fechei esta colheita). Dilma/Temer aparecem nas duas variantes (afastamento em 12/05/2016 e impeachment em 31/08/2016). Valor da janela = média dos valores anuais ponderada pelos meses do mandato em cada ano (aproximação; anos incompletos entram com peso proporcional). A coluna de inflação é a média aritmética das taxas anuais do IGP-DI dez/dez.

{t_gov_s}

Janelas do infográfico (anos civis, como no CSV transcrito):

{t_info_s}

### 4.6 Quatro ressalvas de leitura

1. O IGP-DI é índice de atacado e câmbio: em 2002 (26,4%) e 2020 (23,1%) infla o imposto inflacionário frente ao IPCA (12,5% e 4,5%). Em 2020 o (c) dá II = 1,19% do PIB e o (c2) com IPCA dá 0,24%. Para o período do IPCA-alvo (pós-1999), prefira (c2) ou mostre os dois.
2. O imposto inflacionário (c) usa a base **real** perdida; ele não é "receita do governo" no mesmo sentido do déficit primário (Ayres et al. documentam que boa parte da senhoriagem financiou o Banco do Brasil).
3. Antes de 1980 o II (base) tem quebra de conceito; use o TIT (M1).
4. O PIB de 1947-1989 vem de outra base do IBGE que o de 2000 em diante (seção 2).

## 5. Extras fiscais e monetários por governo (anos civis)

Convenções: câmbio = R$/US$ comercial venda, fim de período (Ipeadata BM_ERVF); Selic = produto das taxas "over" mensais (Ipeadata BM12_TJOVER12, cobre desde 1974; **não verifiquei a comparabilidade da taxa "over" antes de 1986** ❓; o juro real anual com inflação alta é muito ruidoso); juro real ex-post = (1+Selic)/(1+inflação)−1; resultado primário = −NFSP (positivo = superávit). CSV anual: `saida/extras_anual.csv`.

{t_ext1}

{t_ext2}

- ✅ Dívida bruta (DBGG): o BCB publica **duas** séries em paralelo, "metodologia até 2007" (SGS 4537, desde jan/2002) e "desde 2008" (SGS 13762, desde dez/2006); o nível difere em cerca de 8 a 15 p.p. do PIB. Nunca misture. A DLSP consolidada (SGS 4513) e a dívida líquida do governo geral (SGS 4536) começam em 2001-2002; para 1981-2000 só tenho a DLSP de governo federal + Banco Central (Ipeadata BM_DTGFN, "inclui a base monetária" como passivo ✅ pelo metadado).
- ⚠️ Razão estoque de dezembro / PIB do ano fica inflada em anos de inflação alta (1989: DLSP GF+BC = 73% do PIB, 1990: 10%): não compare Sarney com os demais por esse número.
- Primário: GF+BC desde 1991 (Ipeadata BM12_NFGFPYS12); consolidado desde nov/2002 (SGS 5793). ❓ **Antes de 1991 não achei série oficial** (Ayres et al. usam o IBGE, Estatísticas do Século XX, que não baixei).
- Reservas internacionais: Ipeadata BM_RES (estoque de dezembro, US$ milhões) ✅; não confirmei o conceito (liquidez internacional) ⚠️.

## 6. Teste da hipótese "a inflação oficial esconde algo" (medida, sem endosso)

> [!IMPORTANT]
> O SGS **11427 não é "preços administrados"**: o catálogo do BCB o chama "IPCA - Núcleo por exclusão - Sem monitorados e alimentos no domicílio" ✅. O par correto é **11428 (itens livres)** e **4449 (preços monitorados - total)**, ambos desde jan/1991. "Administrados" é o nome antigo de "monitorados".

Códigos: 11428 = "IPCA - Itens livres" (catálogo do BCB ✅); 4449 = "IPCA - Preços monitorados - Total" (catálogo ✅); 433 = IPCA geral. Cada um bate com a série homônima do Ipeadata (`PRECOS12_IPCAG12`: 561 de 561 meses iguais; `BM12_IPCAPL12` e `BM12_IPCAPM12`: iguais até o arredondamento de 0,01) ✅.

### 6.1 Livres x monitorados, 2010-2017 (variação anual do IPCA, %)

{t_h1}

Acumulados:

{t_h2}

Peso implícito dos monitorados no IPCA (regressão de IPCA − livres sobre monitorados − livres, mensal, sem intercepto): o IPCA fecha com seus componentes.

{t_h3}

**O que se mede:** (i) o IPCA é aritmeticamente coerente com livres + monitorados (peso de cerca de 24%, R² > 0,997); (ii) em 2012-2014 os monitorados subiram 10,8% contra 22,0% dos livres (−11,2 p.p.) e em 2015 subiram 18,1% contra 8,5% (+9,6 p.p.); (iii) em 2013-2015 o saldo é de +2,0 p.p. a favor dos monitorados; em 2011-2016 fecha em −3,8 p.p.; (iv) IGP-DI e INPC ficam na mesma ordem de grandeza do IPCA nos acumulados de 2013-2015 (IGP-DI 21,2%, INPC 24,8%, IPCA 24,7%). **O que não se mede:** se o preço do item monitorado foi "represado" por decisão administrativa (a série só mostra o preço que foi coletado) nem o efeito sobre expectativas. Diferença cumulativa 2011-2016 de 3,8 p.p. nos monitorados corresponde a cerca de 0,9 p.p. no IPCA acumulado (peso 24%), contra IPCA acumulado de 49,4% no período.

### 6.2 Plano Cruzado (congelamento de 28/02/1986)

{t_c1}

{t_c2}

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
"""
(AQUI / "RESULTADO.md").write_text(md)
print("RESULTADO.md:", len(md), "bytes")
