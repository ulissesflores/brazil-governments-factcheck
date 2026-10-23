# Pobreza: leque de linhas como series separadas, historico das linhas (quando e por que mudaram), efeito mecanico da troca
# de linha/PPC no mesmo pais-ano, linhas de elegibilidade do Bolsa Familia em valor real e renda por decil (medida SEM linha).
# Dado como publicado; nada e estimado aqui, exceto a conversao de valores nominais para reais de set/2026 (indice oficial, declarado).
# Rode: python3 -I gerar_pobreza.py
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from carga import *  # noqa: E402,F401,F403
import citacoes  # noqa: E402

SAIDA = H / "saida"
SAIDA.mkdir(exist_ok=True)
PS = SO / "series" / "pobreza.csv"
V_PIP = "PIP API v1, versao corrente em 2026-10-19 (mais recente listada no pip-info: 20260922); baixado 2026-10-19"
V_WDI = "Banco Mundial WDI, lastupdated 2026-10-08; baixado 2026-10-19"


def w(nome, cab, linhas):
    with open(H / nome, "w", newline="", encoding="utf-8") as f:
        x = csv.DictWriter(f, fieldnames=cab)
        x.writeheader()
        for l in linhas:
            x.writerow({k: ("" if l.get(k) is None else l.get(k)) for k in cab})
    print(nome, len(linhas), "linhas")


# ---------------------------------------------------------------------------------------------------
# 1. LEQUE: cada linha como serie separada (nada e emendado; cada edicao do SIS fica como serie propria)
# ---------------------------------------------------------------------------------------------------
serie = []
for ppp, ls in ((2017, ("2.15", "3.65", "6.85")), (2021, ("3.00", "4.20", "8.30"))):
    for l in ls:
        for ano, r in sorted(pip(SO / "bruto" / f"pip_ppp{ppp}_line{l}.json").items()):
            serie.append({"linha_id": f"PIP-{l}-PPC{ppp}", "linha_usd_dia": l, "ppc": ppp, "tipo_de_linha": "internacional absoluta (Banco Mundial)",
                          "fonte": "Banco Mundial PIP", "pesquisa": r["survey_acronym"], "ano": ano, "valor_pct": round(r["headcount"] * 100, 3),
                          "comparable_spell_segundo_a_fonte": r["comparable_spell"], "vintage": V_PIP, "nota": f"welfare={r['welfare_type']}"})
for arq, nome, linha_id, ppc in (("wb_SI.POV.DDAY.json", "SI.POV.DDAY", "WDI-DDAY", "2021 (hoje US$ 3,00)"),
                                 ("wb_SI.POV.LMIC.json", "SI.POV.LMIC", "WDI-LMIC", "2021 (hoje US$ 4,20)"),
                                 ("wb_SI.POV.UMIC.json", "SI.POV.UMIC", "WDI-UMIC", "2021 (hoje US$ 8,30)")):
    d = json.load(open(SO / "bruto" / arq))
    rot = d[1][0]["indicator"]["value"]
    for x in d[1]:
        if x["value"] is not None:
            serie.append({"linha_id": linha_id, "linha_usd_dia": rot, "ppc": ppc, "tipo_de_linha": "internacional absoluta (WDI; o MESMO codigo de indicador ja designou outras linhas)",
                          "fonte": f"Banco Mundial WDI {nome}", "pesquisa": "via PIP", "ano": int(x["date"]), "valor_pct": round(x["value"], 3),
                          "vintage": V_WDI, "nota": f"rotulo atual do codigo: {rot}"})
LIN = {  # (fonte, linha) -> (id, usd, ppc, tipo, vintage)
    ("IBGE-SIS2018-PPC2011", "US$ 1,9 PPC2011"): ("SIS2018-1.90-PPC2011", "1.90", 2011, "internacional absoluta", "IBGE SIS edicao 2018 (Tabela 2.28a)"),
    ("IBGE-SIS2018-PPC2011", "US$ 5,5 PPC2011"): ("SIS2018-5.50-PPC2011", "5.50", 2011, "internacional absoluta", "IBGE SIS edicao 2018 (Tabela 2.28)"),
    ("IBGE-SIS2019-PPC2011", "US$ 1,9 PPC2011"): ("SIS2019-1.90-PPC2011", "1.90", 2011, "internacional absoluta", "IBGE SIS edicao 2019"),
    ("IBGE-SIS2019-PPC2011", "US$ 3,2 PPC2011"): ("SIS2019-3.20-PPC2011", "3.20", 2011, "internacional absoluta", "IBGE SIS edicao 2019"),
    ("IBGE-SIS2019-PPC2011", "US$ 5,5 PPC2011"): ("SIS2019-5.50-PPC2011", "5.50", 2011, "internacional absoluta", "IBGE SIS edicao 2019"),
    ("IBGE-SIS2020-PPC2011", "US$ 1,9 PPC2011"): ("SIS2020-1.90-PPC2011", "1.90", 2011, "internacional absoluta", "IBGE SIS edicao 2020"),
    ("IBGE-SIS2020-PPC2011", "US$ 3,2 PPC2011"): ("SIS2020-3.20-PPC2011", "3.20", 2011, "internacional absoluta", "IBGE SIS edicao 2020"),
    ("IBGE-SIS2020-PPC2011", "US$ 5,5 PPC2011"): ("SIS2020-5.50-PPC2011", "5.50", 2011, "internacional absoluta", "IBGE SIS edicao 2020"),
}
for ed in ("2024", "2025"):
    for l, usd in (("US$ 2,15 PPC2017", "2.15"), ("US$ 3,65 PPC2017", "3.65"), ("US$ 6,85 PPC2017", "6.85")):
        LIN[(f"IBGE-SIS{ed}", l)] = (f"SIS{ed}-{usd}-PPC2017", usd, 2017, "internacional absoluta", f"IBGE SIS edicao {ed}" + (" (publ. 2024-12-04)" if ed == "2024" else " (publ. 2025-12-03)"))
    LIN[(f"IBGE-SIS{ed}", "50% da mediana")] = (f"SIS{ed}-50pct-mediana", "50% da mediana", "n/a", "relativa", f"IBGE SIS edicao {ed}")
LIN[("SIDRA-5877", "linha nacional ODS US$ 8,30 PPC2021")] = ("SIDRA5877-8.30-PPC2021", "8.30", 2021, "nacional ODS (IBGE) = US$ 8,30 PPC 2021", "IBGE SIDRA tabela 5877, baixado 2026-10-19")
LIN[("SIDRA-5817", "linha internacional ODS US$ 3,00 PPC2021")] = ("SIDRA5817-3.00-PPC2021", "3.00", 2021, "internacional ODS (IBGE) = US$ 3,00 PPC 2021", "IBGE SIDRA tabela 5817, baixado 2026-10-19")
for (fonte, linha), (lid, usd, ppc, tipo, vint) in LIN.items():
    for ano, v in sorted(serie_csv(PS, fonte, linha).items()):
        serie.append({"linha_id": lid, "linha_usd_dia": usd, "ppc": ppc, "tipo_de_linha": tipo, "fonte": fonte, "pesquisa": "PNADC", "ano": ano,
                      "valor_pct": v, "vintage": vint + "; tabelas baixadas 2026-10-19", "nota": "2020-2022 em quintas visitas (SIS 2024/2025, SIDRA)" if usd != "n/a" and ppc in (2017, 2021) else ""})
EXTRA = [
    ("Ipeadata-DISOC_PPY", "linha propria Ipea = 2x indigencia (cesta FAO), 24 regioes; serie INTERROMPIDA", "IPEA-PPY", "linha Ipea: 2 x indigencia (cesta FAO)", "n/a", "nacional Ipea (24 regioes)", "PNAD", "Ipeadata DISOC_PPY (inativa, atualizada 2016-01-06)"),
    ("Ipeadata-P0", "renda fam. per capita < 50% do SM de set/1991 (Atlas 1998)", "IPEA-P0", "50% do SM de set/1991", "n/a", "relativa ao salario minimo de 1991", "Censo", "Ipeadata P0 (inativa, atualizada 2009-04-20)"),
    ("Ipeadata-ADH_PMPOB", "renda dom. per capita <= R$140 (ago/2010)", "ADH-140", "R$ 140 de ago/2010", "n/a", "nacional (Atlas DH) = linha do Bolsa Familia de 2009", "Censo", "Ipeadata ADH_PMPOB (Atlas DH)"),
    ("Ipeadata-ADH_PIND", "renda dom. per capita <= R$70 (ago/2010)", "ADH-70", "R$ 70 de ago/2010", "n/a", "nacional (Atlas DH) = linha de extrema pobreza do Bolsa Familia de 2009", "Censo", "Ipeadata ADH_PIND (Atlas DH)"),
    ("Ipeadata-PNADS_PERCPOBRE300", "PPC$3,00 (2021)", "IPEA-PNADS-3.00", "3.00", 2021, "internacional harmonizada pelo Ipea (PNAD<=2011 x fator que iguala 2012)", "PNAD ate 2011 / PNADC desde 2012", "Ipeadata PNADS_PERCPOBRE300 (atual. 2026-05-25); SERIE HARMONIZADA PELO IPEA, nao e o dado bruto do IBGE"),
    ("Ipeadata-PNADS_PERCPOBRE420", "PPC$4,20 (2021)", "IPEA-PNADS-4.20", "4.20", 2021, "internacional harmonizada pelo Ipea", "PNAD ate 2011 / PNADC desde 2012", "Ipeadata PNADS_PERCPOBRE420 (atual. 2026-05-25); SERIE HARMONIZADA PELO IPEA"),
    ("Ipeadata-PNADS_PERCPOBRE830", "PPC$8,30 (2021)", "IPEA-PNADS-8.30", "8.30", 2021, "internacional harmonizada pelo Ipea", "PNAD ate 2011 / PNADC desde 2012", "Ipeadata PNADS_PERCPOBRE830 (atual. 2026-05-25); SERIE HARMONIZADA PELO IPEA"),
]
for fonte, linha, lid, desc, ppc, tipo, pesq, vint in EXTRA:
    for ano, v in sorted(serie_csv(PS, fonte, linha).items()):
        serie.append({"linha_id": lid, "linha_usd_dia": desc, "ppc": ppc, "tipo_de_linha": tipo, "fonte": fonte, "pesquisa": pesq, "ano": ano,
                      "valor_pct": v, "vintage": vint + "; baixado 2026-10-19", "nota": ""})
CAB1 = ["linha_id", "linha_usd_dia", "ppc", "tipo_de_linha", "fonte", "pesquisa", "ano", "valor_pct", "comparable_spell_segundo_a_fonte", "vintage", "nota"]
w("pobreza-leque-series.csv", CAB1, serie)

# ---------------------------------------------------------------------------------------------------
# 2. HISTORICO DAS LINHAS (quando e por que cada uma mudou), com citacao verificada
# ---------------------------------------------------------------------------------------------------
HIST = []


def h(lid, valor, base, tipo, ini, fim, subst, por, razao, efeito, url, chave, trecho, vint):
    citacoes.verifica(chave, trecho)
    HIST.append({"linha_id": lid, "valor": valor, "ppc_ou_base": base, "tipo_de_linha": tipo, "vigencia_inicio": ini, "vigencia_fim": fim,
                 "substituiu": subst, "substituida_por": por, "razao_declarada_pela_fonte": razao, "efeito_declarado_pela_fonte": efeito,
                 "fonte_primaria_url": url, "trecho_citado": trecho, "tipo_de_quebra": "mudanca_de_regra", "vintage": vint})


U7432 = "https://openknowledge.worldbank.org/bitstreams/2cc05502-3bf7-5c6c-bd4c-213e714013ee/download"
h("WB-1.01-1985", "US$ 1,01/dia (conhecida como 'um dolar por dia')", "PPC 1985", "internacional absoluta", "1990 (World Development Report 1990)", "1996-2000 (atualizada p/ 1,08)", "", "WB-1.08-1993",
  "linha baseada em amostra de linhas nacionais de pobreza (Ravallion, Datt e van de Walle, 1991)", "n/d na fonte lida", U7432, "wb_prwp7432",
  "was set at $1.01 using 1985 PPPs, by Ravallion, Datt and van de Walle (RDW, 1991) and used in the 1990 World Development Report (World Bank, 1990)", "PRWP 7432 (out/2015), baixado 2026-10-19")
h("WB-1.08-1993", "US$ 1,08/dia", "PPC 1993", "internacional absoluta", "Chen e Ravallion (2001)", "ate a adocao da linha de 1,25 (2009)", "WB-1.01-1985", "WB-1.25-2005",
  "atualizacao com os PPCs de 1993 (mediana das 10 menores linhas nacionais da amostra RDW)", "contagem global de 1993: 1,3 bilhao (linha 1,08/PPC 1993) contra 1,8 bilhao (linha 1,25/PPC 2005)", U7432, "wb_prwp7432",
  "Chen and Ravallion (2001) later updated this to $1.08 per day, using the 1993 PPPs. [...] The $1.08 poverty line and 1993 PPPs suggested that 1.3 billion people were poor all over the world. However, the new $1.25 poverty line at 2005 PPPs resulted in an estimated count of 1.8 billion people who were poor in revised estimates for 1993.",
  "PRWP 7432 (out/2015), baixado 2026-10-19")
h("WB-1.25-2005", "US$ 1,25/dia", "PPC 2005", "internacional absoluta", "2009", "2015 (adocao da linha de 1,90)", "WB-1.08-1993", "WB-1.90-2011",
  "novos PPCs de 2005 e novo conjunto de linhas nacionais (Ravallion, Chen e Sangraula, 2009)", "ver linha anterior (1,3 -> 1,8 bilhao em 1993)", U7432, "wb_prwp7432",
  "Ravallion, Chen and Sangraula (RCS, 2009) proposed a new poverty line of $1.25 per day, which is the line that has been used by the World Bank to measure poverty since 2009.", "PRWP 7432 (out/2015), baixado 2026-10-19")
h("WB-1.90-2011", "US$ 1,90/dia", "PPC 2011", "internacional absoluta", "2015 (PRWP 7432 e de out/2015; data exata de adocao nao lida)", "set/2022", "WB-1.25-2005", "WB-2.15-2017",
  "novos PPCs de 2011; mesma definicao das 15 linhas nacionais de Ravallion et al. (2009), preservando o poder de compra da linha anterior nos paises pobres",
  "o nivel de pobreza com a nova linha e os novos PPCs e semelhante ao estimado com PPC 2005 e linha de 1,25", U7432, "wb_prwp7432",
  "The new line is still derived from the same fifteen national poverty lines that Ravallion et al. (2009) used to define the $1.25 poverty line in 2005 PPPs. [...] The level of poverty using the new line and PPPs is similar to estimates based on the 2005 PPPs and the $1.25 line.",
  "PRWP 7432 (out/2015), baixado 2026-10-19")
h("WB-2.00-2005", "US$ 2,00/dia ('dois dolares por dia')", "PPC 2005", "internacional absoluta (renda media baixa)", "c. 2008-2009", "substituida pela linha de 3,10 (PPC 2011), depois 3,20", "", "WB-3.20-2011",
  "linha 'comumente usada para paises de renda media'; seu equivalente em PPC 2011 foi proposto como US$ 3,10", "n/d", U7432, "wb_prwp7432",
  "A second poverty line of $3.10 in 2011 PPPs has also been proposed as the comparable equivalent to the $2 dollar-a-day poverty line in 2005 PPPs, commonly used as a poverty line for middle-income countries.", "PRWP 7432 (out/2015), baixado 2026-10-19")
B17 = "https://blogs.worldbank.org/en/opendata/updating-international-poverty-line-2017-ppps"
h("WB-3.20-2011", "US$ 3,20/dia (renda media baixa)", "PPC 2011", "internacional absoluta", "data de adocao nao lida (a metodologia e de Jolliffe e Prydz, 2016)", "set/2022", "WB-2.00-2005", "WB-3.65-2017",
  "mesma metodologia da linha extrema (mediana das linhas nacionais harmonizadas), aplicada a paises de renda media baixa", "n/d", B17, "wb_blog_2017ppp",
  "define two higher lines — $3.20 (2011 PPP) and $5.50 (2011 PPP) — based on national poverty lines for lower- and upper-middle-income countries, respectively", "blog WB (2022), baixado 2026-10-19")
h("WB-5.50-2011", "US$ 5,50/dia (renda media alta)", "PPC 2011", "internacional absoluta", "data de adocao nao lida", "set/2022", "", "WB-6.85-2017",
  "idem, para paises de renda media alta", "n/d", B17, "wb_blog_2017ppp",
  "define two higher lines — $3.20 (2011 PPP) and $5.50 (2011 PPP) — based on national poverty lines for lower- and upper-middle-income countries, respectively", "blog WB (2022), baixado 2026-10-19")
h("WB-2.15-2017", "US$ 2,15/dia", "PPC 2017", "internacional absoluta", "set/2022 ('fall 2022'; versao 20220909 do PIP)", "jun/2025", "WB-1.90-2011", "WB-3.00-2021",
  "lancamento dos PPCs de 2017 (ICP, 2020) e nova metodologia: mediana das linhas nacionais harmonizadas dos paises de renda baixa",
  "US$ 2,17 seria a linha que mantem constante a pobreza GLOBAL em 2017; o 2,15 arredonda isso. 'In nominal terms, it is a quarter of a dollar higher'", B17, "wb_blog_2017ppp",
  "The World Bank will start using new poverty lines in fall 2022. The decision follows the release in 2020 of new purchasing power parities (PPPs) by the International Comparison Program (ICP). [...] $2.17 is the line that holds constant global poverty in 2017, the year of the PPP data.",
  "blog WB (2022), baixado 2026-10-19")
h("WB-3.65-2017", "US$ 3,65/dia", "PPC 2017", "internacional absoluta (renda media baixa)", "set/2022", "jun/2025", "WB-3.20-2011", "WB-4.20-2021",
  "dados atualizados das linhas nacionais; arredondamento a 5 centavos", "n/d", B17, "wb_blog_2017ppp",
  "With updated data, these higher lines are now being updated to $3.65 (2017 PPP) and $6.85 (2017 PPP), rounding to the nearest five cents", "blog WB (2022), baixado 2026-10-19")
h("WB-6.85-2017", "US$ 6,85/dia", "PPC 2017", "internacional absoluta (renda media alta)", "set/2022", "jun/2025", "WB-5.50-2011", "WB-8.30-2021",
  "idem", "n/d", B17, "wb_blog_2017ppp",
  "With updated data, these higher lines are now being updated to $3.65 (2017 PPP) and $6.85 (2017 PPP), rounding to the nearest five cents", "blog WB (2022), baixado 2026-10-19")
B25 = "https://blogs.worldbank.org/en/opendata/the-world-bank-s-new-global-poverty-lines-in-2021-prices"
h("WB-3.00-2021", "US$ 3,00/dia", "PPC 2021", "internacional absoluta", "2025-06-09 (data do blog; PIP de jun/2025)", "vigente", "WB-2.15-2017", "",
  "novos PPCs de 2021 (ICP, 2024) e base maior de linhas nacionais (1.747 linhas em 163 paises, contra 1.381 em 157)",
  "+125 milhoes de pessoas na pobreza extrema global em 2022 so pela redefinicao; a fonte diz que a mudanca nao reflete 'ambicoes crescentes' e sim custo de necessidades basicas melhor medido", B25, "wb_blog_2021prices",
  "The international poverty line of $2.15 (in 2017 prices) has been updated to $3.00 (in 2021 prices), leading to an upward revision of the population in extreme poverty by 125 million people in 2022. [...] these revised lines do not reflect rising ambitions of what it means to be non-poor but largely reflect better measured cost of basic needs in the poorest countries of the world.",
  "blog WB (jun/2025), baixado 2026-10-19")
h("WB-4.20-2021", "US$ 4,20/dia", "PPC 2021", "internacional absoluta (renda media baixa)", "2025-06-09", "vigente", "WB-3.65-2017", "",
  "idem", "n/d", B25, "wb_blog_2021prices",
  "The poverty lines more relevant for middle income countries have been updated from $3.65 (in 2017 prices) to $4.20 (in 2021 prices) in the case of lower-middle-income countries and from $6.85 (in 2017 prices) to $8.30 (in 2021 prices) in the case of upper-middle-income countries.",
  "blog WB (jun/2025), baixado 2026-10-19")
h("WB-8.30-2021", "US$ 8,30/dia", "PPC 2021", "internacional absoluta (renda media alta); IBGE a usa como 'linha nacional' dos ODS", "2025-06-09", "vigente", "WB-6.85-2017", "",
  "idem", "n/d", B25, "wb_blog_2021prices",
  "The poverty lines more relevant for middle income countries have been updated from $3.65 (in 2017 prices) to $4.20 (in 2021 prices) in the case of lower-middle-income countries and from $6.85 (in 2017 prices) to $8.30 (in 2021 prices) in the case of upper-middle-income countries.",
  "blog WB (jun/2025), baixado 2026-10-19")
IPEA = "http://www.ipeadata.gov.br/api/odata4/Metadados"
h("IPEA-PPY", "linha propria: 2 x linha de extrema pobreza (cesta FAO), 24 regioes", "reais de cada regiao/epoca", "nacional Ipea (absoluta, regionalizada)", "1976", "2014 (serie interrompida)", "", "",
  "linha de pobreza = dobro da linha de extrema pobreza, que e o valor de uma cesta de alimentos com o minimo de calorias (FAO/OMS)", "n/d", IPEA, "ipeadata",
  "A linha de pobreza aqui considerada é o dobro da linha de extrema pobreza, uma estimativa do valor de uma cesta de alimentos com o mínimo de calorias necessárias para suprir adequadamente uma pessoa", "Ipeadata DISOC_PPY (atual. 2016-01-06), baixado 2026-10-19")
h("IPEA-P0", "50% do salario minimo de 1/set/1991", "reais de set/1991", "relativa ao SM de 1991", "Censos 1970, 1980, 1991", "serie parada em 1991", "", "",
  "Atlas do Desenvolvimento Humano no Brasil 1998", "n/d", IPEA, "ipeadata",
  "Percentual de pessoas com renda familiar per capita inferior a 50% do salário mínimo de 1º de setembro de 1991.", "Ipeadata P0 (atual. 2009-04-20), baixado 2026-10-19")
h("ADH-140-70", "R$ 140 (pobreza) e R$ 70 (extrema pobreza), valores de ago/2010", "reais de ago/2010", "nacional (Atlas DH/Censos 1991, 2000, 2010)", "Censo 1991", "Censo 2010", "", "",
  "linhas do Atlas do Desenvolvimento Humano, ancoradas nos valores do Bolsa Familia de 2009-2010 (mesmos R$ 140 e R$ 70 do Decreto 6.917/2009)", "n/d", IPEA, "ipeadata",
  "renda per capita", "Ipeadata ADH_PMPOB/ADH_PIND, baixado 2026-10-19")
h("IBGE-ODS-8.30", "US$ 8,30/dia (PPC 2021), chamada 'linha nacional' dos ODS", "R$ 2,44983620 por US$ PPC 2021 (consumo final)", "nacional ODS (IBGE)", "serie 2012-2024 na revisao de 2026", "vigente", "", "",
  "acompanhamento dos Objetivos de Desenvolvimento Sustentavel; consolidado das primeiras entrevistas de 2012-2019 e 2023-2024 e das quintas entrevistas de 2020-2022", "n/d", IPEA, "ipeadata",
  "Consolidado das primeiras entrevistas de 2012-2019, 2023-2024 e das quintas entrevistas de 2020-2022", "Ipeadata PNADCA_TXPNUF (atual. 2026-05-12), baixado 2026-10-19")
CAB2 = ["linha_id", "valor", "ppc_ou_base", "tipo_de_linha", "vigencia_inicio", "vigencia_fim", "substituiu", "substituida_por", "razao_declarada_pela_fonte",
        "efeito_declarado_pela_fonte", "fonte_primaria_url", "trecho_citado", "tipo_de_quebra", "vintage"]
# ADH-140-70: trecho generico demais; troca por frase real do metadado
for x in HIST:
    if x["linha_id"] == "ADH-140-70":
        for hit in citacoes.corpus("ipeadata").split("\n"):
            if hit.startswith("[ADH_PMPOB]"):
                x["trecho_citado"] = hit[hit.index("::") + 3: hit.index("::") + 3 + 230].strip()
                break
w("pobreza-linhas-historico.csv", CAB2, HIST)

# ---------------------------------------------------------------------------------------------------
# 3. EFEITO MECANICO: mesmo pais-ano, so a linha/PPC muda (positivo = mais pessoas contadas como pobres)
# ---------------------------------------------------------------------------------------------------
EF = []
pipd = {(p, l): {a: r["headcount"] * 100 for a, r in pip(SO / "bruto" / f"pip_ppp{p}_line{l}.json").items()} for p, ls in ((2017, ("2.15", "3.65", "6.85")), (2021, ("3.00", "4.20", "8.30"))) for l in ls}
surv = {a: r["survey_acronym"] for a, r in pip(SO / "bruto" / "pip_ppp2017_line6.85.json").items()}
for (l1, l2) in (("2.15", "3.00"), ("3.65", "4.20"), ("6.85", "8.30")):
    for a in sorted(pipd[(2017, l1)]):
        if a in pipd[(2021, l2)]:
            EF.append({"troca": f"US$ {l1} (PPC 2017) -> US$ {l2} (PPC 2021)", "fonte": "Banco Mundial PIP (mesmo pais, ano e pesquisa)", "ano": a, "pesquisa": surv[a],
                       "pct_linha_antiga": round(pipd[(2017, l1)][a], 3), "pct_linha_nova": round(pipd[(2021, l2)][a], 3),
                       "efeito_pp": round(pipd[(2021, l2)][a] - pipd[(2017, l1)][a], 3), "efeito_relativo_pct": round((pipd[(2021, l2)][a] / pipd[(2017, l1)][a] - 1) * 100, 1),
                       "vintage": V_PIP, "nota": "so a linha/PPC mudam; renda, pesos e pesquisa sao os mesmos"})
for (f1, l1n, f2, l2n, nome) in (("IBGE-SIS2020-PPC2011", "US$ 1,9 PPC2011", "IBGE-SIS2025", "US$ 2,15 PPC2017", "US$ 1,90 (PPC 2011) -> US$ 2,15 (PPC 2017)"),
                                 ("IBGE-SIS2020-PPC2011", "US$ 3,2 PPC2011", "IBGE-SIS2025", "US$ 3,65 PPC2017", "US$ 3,20 (PPC 2011) -> US$ 3,65 (PPC 2017)"),
                                 ("IBGE-SIS2020-PPC2011", "US$ 5,5 PPC2011", "IBGE-SIS2025", "US$ 6,85 PPC2017", "US$ 5,50 (PPC 2011) -> US$ 6,85 (PPC 2017)")):
    a1, a2 = serie_csv(PS, f1, l1n), serie_csv(PS, f2, l2n)
    for a in sorted(a1):
        if a in a2:
            EF.append({"troca": nome, "fonte": "IBGE SIS (PNADC): edicao 2020 x edicao 2025", "ano": a, "pesquisa": "PNADC",
                       "pct_linha_antiga": a1[a], "pct_linha_nova": a2[a], "efeito_pp": round(a2[a] - a1[a], 3), "efeito_relativo_pct": round((a2[a] / a1[a] - 1) * 100, 1),
                       "vintage": "IBGE SIS edicoes 2020 e 2025, baixadas 2026-10-19",
                       "nota": "mistura a troca de linha/PPC com a revisao entre edicoes do SIS (a revisao medida em 2016-2017 do SIS e <=0,5 pp; ver quebras.csv)"})
CAB3 = ["troca", "fonte", "ano", "pesquisa", "pct_linha_antiga", "pct_linha_nova", "efeito_pp", "efeito_relativo_pct", "vintage", "nota"]
w("pobreza-efeito-mecanico.csv", CAB3, EF)
resumo = {}
for x in EF:
    resumo.setdefault(x["troca"], []).append(x["efeito_pp"])
M = {k: {"media_pp": round(sum(v) / len(v), 3), "min_pp": min(v), "max_pp": max(v), "n_anos": len(v)} for k, v in resumo.items()}
json.dump(M, open(SAIDA / "efeito_mecanico_resumo.json", "w"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------------------------------------------
# 4. Valor REAL das linhas em R$ mensais de set/2026 (IPCA, indice oficial); fator PPC de cada rodada
# ---------------------------------------------------------------------------------------------------
ipca = sgs(str(ER / "bcb-sgs433-raw.json"))
inpc = sgs(str(ER / "bcb-sgs188-raw.json"))


def idx(var):
    v, out = 1.0, {}
    for k in sorted(var):
        v *= 1 + var[k] / 100
        out[k] = v
    return out


Ia, In = idx(ipca), idx(inpc)
fim_ipca = Ia[(2026, 9)]
media_ano = lambda I, y: sum(I[(y, m)] for m in range(1, 13)) / 12  # noqa: E731
FATOR = {2011: 1.66, 2017: 2.3273771, 2021: 2.44983620}
REAL = []
for ppc, linhas in ((2011, ("1.90", "3.20", "5.50")), (2017, ("2.15", "3.65", "6.85")), (2021, ("3.00", "4.20", "8.30"))):
    for l in linhas:
        nominal = float(l) * FATOR[ppc] * 365 / 12
        real = nominal * fim_ipca / media_ano(Ia, ppc)
        REAL.append({"linha": f"US$ {l} (PPC {ppc})", "fator_R$_por_US$_PPC": FATOR[ppc], "R$_mensal_precos_do_ano_base": round(nominal, 2),
                     "R$_mensal_set2026": round(real, 2),
                     "fonte_do_fator": {2011: "IBGE SIS 2018-2020: R$ 1,66 (consumo privado)", 2017: "IBGE SIS 2024/2025: R$ 2,3273771 (consumo privado)", 2021: "Ipeadata PNADCA_TXPNUF: R$ 2,44983620 (consumo final)"}[ppc],
                     "vintage": "fatores como publicados; IPCA SGS 433 baixado 2026-10-19", "nota": "multiplicador 365/12 dias e escolha deste script (o IBGE nao declara 30 ou 365/12)"})
w("pobreza-linhas-em-reais-reais.csv", ["linha", "fator_R$_por_US$_PPC", "R$_mensal_precos_do_ano_base", "R$_mensal_set2026", "fonte_do_fator", "vintage", "nota"], REAL)

# ---------------------------------------------------------------------------------------------------
# 5. Linhas de elegibilidade do Bolsa Familia / Auxilio Brasil, em valor real (INPC) e em fracao do salario minimo
# ---------------------------------------------------------------------------------------------------
nom = ipea("MTE12_SALMIN12")
BF = [  # (data de inicio dos efeitos, pobreza, extrema pobreza, instrumento, chave, url, trecho)
    ((2004, 9), 100, 50, "Decreto 5.209, de 17/09/2004 (art. 18, redacao original)", "plan_d5209-2004", "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/decreto/d5209.htm",
     "caracterizadas pela renda familiar mensal per capita de até R$ 100,00 e R$ 50,00, respectivamente."),
    ((2006, 4), 120, 60, "Decreto 5.749, de 11/04/2006 (em vigor na publicacao, DOU 12/04/2006)", "plan_d5749-2006", "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/decreto/d5749.htm",
     "caracterizadas pela renda familiar mensal per capita de até R$ 120,00 (cento e vinte reais) e R$ 60,00 (sessenta reais), respectivamente."),
    ((2009, 4), 137, 69, "Decreto 6.824, de 16/04/2009 (em vigor na publicacao)", "plan_d6824-2009", "https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/decreto/D6824.htm",
     "caracterizadas pela renda familiar mensal per capita de até R$ 137,00 (cento e trinta e sete reais) e R$ 69,00 (sessenta e nove reais)."),
    ((2009, 9), 140, 70, "Decreto 6.917, de 30/07/2009 (efeitos financeiros desde 01/09/2009)", "plan_d6917-2009", "https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/decreto/d6917.htm",
     "caracterizadas pela renda familiar mensal per capita de até R$ 140,00 (cento e quarenta reais) e R$ 70,00 (setenta reais), respectivamente."),
    ((2014, 6), 154, 77, "Decreto 8.232, de 30/04/2014 (efeitos financeiros desde 01/06/2014)", "plan_d8232-2014", "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/decreto/d8232.htm",
     "caracterizadas pela renda familiar mensal per capita de até R$ 154,00 (cento e cinquenta e quatro reais) e R$ 77,00 (setenta e sete reais), respectivamente."),
    ((2016, 7), 170, 85, "Decreto 8.794, de 29/06/2016 (efeitos financeiros desde 01/07/2016)", "plan_d8794-2016", "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/decreto/D8794.htm",
     "caracterizadas pela renda familiar mensal per capita de até R$ 170,00 (cento e setenta reais) e de R$ 85,00 (oitenta e cinco reais), respectivamente."),
    ((2018, 7), 178, 89, "Decreto 9.396, de 30/05/2018 (em vigor em 01/07/2018)", "plan_d9396-2018", "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/decreto/D9396.htm",
     "caracterizadas pela renda familiar mensal per capita de até R$ 178,00 (cento e setenta e oito reais) e R$ 89,00 (oitenta e nove reais), respectivamente."),
    ((2021, 11), 200, 100, "Auxilio Brasil: Decreto 10.852, de 08/11/2021 (art. 20) - OUTRO PROGRAMA (substitui o Bolsa Familia)", "plan_d10852-2021", "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/decreto/D10852.htm",
     "extrema pobreza, caracterizada pela renda familiar mensal per capita no valor de até R$ 100,00 (cem reais)"),
    ((2022, 3), 210, 105, "Auxilio Brasil: Decreto 11.013, de 29/03/2022 (em vigor na publicacao)", "plan_d11013-2022", "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/decreto/D11013.htm",
     "extrema pobreza, caracterizada pela renda familiar mensal per capita no valor de até R$ 105,00 (cento e cinco reais)"),
    ((2023, 6), 218, 218, "Bolsa Familia reinstituido: Lei 14.601, de 19/06/2023 (conversao da MP 1.164/2023); linha UNICA", "plan_l14601-2023", "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/L14601.htm",
     "cuja renda familiar per capita mensal seja igual ou inferior a R$ 218,00 (duzentos e dezoito reais)."),
]
BFL = []
for (a, m), pob, ext, inst, chave, url, trecho in BF:
    citacoes.verifica(chave, trecho)
    real = lambda v: round(v * In[(2026, 9)] / In[(a, m)], 2)  # noqa: E731
    sm = nom.get((a, m))
    BFL.append({"inicio_dos_efeitos": f"{a}-{m:02d}", "linha_pobreza_nominal_R$": pob, "linha_extrema_pobreza_nominal_R$": ext if ext != pob else "(linha unica)",
                "pobreza_R$_set2026_INPC": real(pob), "extrema_R$_set2026_INPC": real(ext), "pobreza_em_fracao_do_SM_vigente": round(pob / sm, 3) if sm else "",
                "extrema_em_fracao_do_SM_vigente": round(ext / sm, 3) if sm else "", "instrumento": inst, "fonte_primaria_url": url, "trecho_citado": trecho,
                "tipo_de_quebra": "mudanca_de_regra", "vintage": "texto consolidado do Planalto lido em 2026-10-19 (atos posteriores podem constar como revogados); INPC SGS 188 baixado 2026-10-19"})
w("bolsa-familia-linhas-elegibilidade.csv", ["inicio_dos_efeitos", "linha_pobreza_nominal_R$", "linha_extrema_pobreza_nominal_R$", "pobreza_R$_set2026_INPC", "extrema_R$_set2026_INPC",
                                             "pobreza_em_fracao_do_SM_vigente", "extrema_em_fracao_do_SM_vigente", "instrumento", "fonte_primaria_url", "trecho_citado", "tipo_de_quebra", "vintage"], BFL)

# ---------------------------------------------------------------------------------------------------
# 6. RENDA POR DECIL (medida sem linha): participacao do decil x media = renda per capita diaria em PPC$ (precos do ano-base do PPC)
# ---------------------------------------------------------------------------------------------------
DEC = []
for ppp, arq in ((2017, "pip_ppp2017_line6.85.json"), (2021, "pip_ppp2021_line8.30.json")):
    for ano, r in sorted(pip(SO / "bruto" / arq).items()):
        for d in range(1, 11):
            DEC.append({"ano": ano, "decil": d, "renda_per_capita_ppc_dolar_dia": round(r[f"decile{d}"] * 10 * r["mean"], 3), "participacao_na_renda": r[f"decile{d}"],
                        "ppc_base": ppp, "pesquisa": r["survey_acronym"], "welfare_type": r["welfare_type"],
                        "comparable_spell_segundo_a_fonte": r["comparable_spell"], "vintage": V_PIP,
                        "nota": "real (precos do ano-base do PPC); PIP: media e participacoes declaradas pela fonte; renda = participacao x 10 x media"})
        DEC.append({"ano": ano, "decil": "media", "renda_per_capita_ppc_dolar_dia": r["mean"], "participacao_na_renda": 1.0, "ppc_base": ppp, "pesquisa": r["survey_acronym"],
                    "welfare_type": r["welfare_type"], "comparable_spell_segundo_a_fonte": r["comparable_spell"], "vintage": V_PIP, "nota": "media declarada pelo PIP"})
        DEC.append({"ano": ano, "decil": "mediana", "renda_per_capita_ppc_dolar_dia": r["median"], "participacao_na_renda": "", "ppc_base": ppp, "pesquisa": r["survey_acronym"],
                    "welfare_type": r["welfare_type"], "comparable_spell_segundo_a_fonte": r["comparable_spell"], "vintage": V_PIP, "nota": "mediana declarada pelo PIP"})
w("renda-por-decil.csv", ["ano", "decil", "renda_per_capita_ppc_dolar_dia", "participacao_na_renda", "ppc_base", "pesquisa", "welfare_type", "comparable_spell_segundo_a_fonte", "vintage", "nota"], DEC)

# resumo por governo (PPC 2017), SEPARADO por spell da propria fonte (PNAD 1981-2011 | PNADC 2012-2024): primeiro e ultimo ano disponiveis na janela
GOV = [("Castelo Branco", 1964, 1966), ("Costa e Silva + Medici", 1967, 1973), ("Geisel", 1974, 1978), ("Figueiredo", 1979, 1984), ("Sarney", 1985, 1989),
       ("Collor", 1990, 1992), ("Itamar Franco", 1993, 1994), ("FHC", 1995, 2002), ("Lula 1-2", 2003, 2010), ("Dilma", 2011, 2016), ("Temer", 2017, 2018),
       ("Bolsonaro", 2019, 2022), ("Lula 3", 2023, 2025)]
base = {(r["ano"], str(r["decil"])): r["renda_per_capita_ppc_dolar_dia"] for r in DEC if r["ppc_base"] == 2017}
anos_pip = sorted({a for a, _ in base})
RD = []
for spell, s0, s1 in (("PNAD (spell 1981-2011)", 1981, 2011), ("PNADC (spell 2012-2024)", 2012, 2024)):
    for g_, a, b in GOV:
        ys = [y for y in anos_pip if max(a, s0) <= y <= min(b, s1)]
        if len(ys) < 2:
            continue
        for dec in ("1", "2", "5", "9", "10", "mediana", "media"):
            v0, v1 = base[(ys[0], dec)], base[(ys[-1], dec)]
            RD.append({"governo": g_, "janela_do_mandato": f"{a}-{b}", "spell": spell, "ano_inicial_disponivel": ys[0], "ano_final_disponivel": ys[-1],
                       "cobertura": "inteira" if (s0 <= a and b <= s1) else "PARCIAL (cruza a quebra PNAD->PNADC ou o limite da serie)", "decil": dec,
                       "renda_inicial_ppc_dia": v0, "renda_final_ppc_dia": v1, "variacao_pct": round((v1 / v0 - 1) * 100, 1), "vintage": V_PIP})
w("renda-por-decil-por-governo.csv", ["governo", "janela_do_mandato", "spell", "ano_inicial_disponivel", "ano_final_disponivel", "cobertura", "decil", "renda_inicial_ppc_dia",
                                      "renda_final_ppc_dia", "variacao_pct", "vintage"], RD)
