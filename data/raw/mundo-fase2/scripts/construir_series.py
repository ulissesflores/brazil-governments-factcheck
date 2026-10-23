#!/usr/bin/env python3
"""Constroi series/*.csv e derivado/*.csv a partir de bruto/ (somente stdlib; nada estimado).

Uso: python3 -I construir_series.py   (a pasta mundo-fase2 e deduzida do caminho do script)
Linhas com valor ausente na fonte NAO sao escritas (cobertura medida no RESULTADO.md).
"""
import csv
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BRUTO, SERIES, DERIVADO = RAIZ / "bruto", RAIZ / "series", RAIZ / "derivado"
CAB = ["indicador", "fonte", "definicao_linha", "ano", "mes_ou_trimestre", "valor", "unidade", "nota", "vintage"]
SERIES.mkdir(exist_ok=True)
DERIVADO.mkdir(exist_ok=True)


def gravar(caminho, linhas):
    with caminho.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(CAB)
        w.writerows(linhas)
    print(caminho.name, len(linhas))


# ---------- WDI ----------
WDI = {
    "GB.XPD.RSDV.GD.ZS": ("wdi_pd_pib", "% do PIB", "P&D (GERD) % PIB; origem UNESCO UIS"),
    "SP.POP.SCIE.RD.P6": ("wdi_pesquisadores_por_milhao", "por milhao de habitantes", "pesquisadores em P&D (FTE) por milhao; origem UNESCO UIS"),
    "IP.PAT.RESD": ("wdi_patentes_residentes", "pedidos", "pedidos de patente de residentes (escritorio nacional, direto + entrada PCT); origem WIPO"),
    "NY.GDP.MKTP.CD": ("wdi_pib_usd_correntes", "US$ correntes", "PIB em US$ correntes"),
    "SP.POP.TOTL": ("wdi_populacao", "habitantes", "populacao total (meio do ano)"),
    "NE.TRD.GNFS.ZS": ("wdi_comercio_pib", "% do PIB", "comercio (X+M de bens e servicos) % PIB; conferencia com IBGE"),
    "NV.IND.MANF.ZS": ("wdi_industria_transformacao_pib", "% do PIB", "valor adicionado da industria de transformacao % PIB; conferencia"),
    "NE.CON.GOVT.ZS": ("wdi_consumo_governo_pib", "% do PIB", "despesa de consumo final do governo geral % PIB; conferencia"),
    "FI.RES.TOTL.CD": ("wdi_reservas_usd", "US$ correntes", "reservas totais incluindo ouro; conferencia com BCB"),
}
linhas, wdi_val = [], {}
for cod, (nome, un, defn) in WDI.items():
    d = json.load(open(BRUTO / f"wdi_BRA_{cod}.json"))
    vint = "WDI lastupdated " + d[0]["lastupdated"]
    for r in sorted(d[1], key=lambda r: int(r["date"])):
        if r["value"] is None:
            continue
        a = int(r["date"])
        wdi_val[(cod, a)] = r["value"]
        linhas.append([nome, "Banco Mundial WDI " + cod, defn, a, "", repr(float(r["value"])) if cod not in ("IP.PAT.RESD", "SP.POP.TOTL") else str(int(r["value"])), un, "", vint])
gravar(SERIES / "wdi_brasil.csv", linhas)

# ---------- WIPO ----------
VINT_WIPO = "WIPO IPSDC 'Last updated: May 2026' (baixado 2026-10-20)"
WIPO = [
    ("wipo_ind10_rt15_off-BR_ori-BR.json", "wipo_pedidos_residentes_inpi", "WIPO ind.1 pedidos totais (diretos + entrada nacional PCT), escritorio BR x origem BR = residentes no INPI", "pedidos"),
    ("wipo_ind11_rt15_off-BR_ori-BR.json", "wipo_pedidos_diretos_residentes_inpi", "WIPO ind.1a pedidos diretos, escritorio BR x origem BR", "pedidos"),
    # rt13 ind.1 (origem, todos os escritorios) NAO e parseado: o export traz 5 subvalores sem rotulo e fora de ordem (ver RESULTADO)
    ("wipo_ind101_rt13_ori-BR.json", "wipo_residentes_por_milhao_oficial", "WIPO ind.10 pedidos de residentes por milhao de habitantes (calculo da propria WIPO)", "pedidos por milhao"),
    ("wipo_ind100_rt13_ori-BR.json", "wipo_residentes_por_100bi_pib_ppc", "WIPO ind.9 pedidos de residentes por 100 bi US$ de PIB (PPC 2017)", "pedidos por 100 bi US$ PPC 2017"),
]
linhas, wipo_val = [], {}
for arq, nome, defn, un in WIPO:
    d = json.load(open(BRUTO / arq))
    rec = d["records"][0]
    assert len(d["records"]) == 1, arq
    for k, v in sorted(rec.items()):
        if re.fullmatch(r"\d{4}", k) and v not in (None, ""):
            val = float(v.replace(",", ""))
            wipo_val[(nome, int(k))] = val
            linhas.append([nome, "WIPO IP Statistics Data Center", defn, int(k), "", v, un, "", VINT_WIPO])
gravar(SERIES / "wipo_brasil.csv", linhas)

# ---------- UNESCO UIS ----------
d = json.load(open(BRUTO / "unesco_uis_BRA_EXPGDP_RESDEN.json"))
UIS = {"EXPGDP.TOT": ("uis_pd_pib", "% do PIB", "GERD % PIB"), "RESDEN.INHAB.TFTE": ("uis_pesquisadores_por_milhao_fte", "por milhao de habitantes (FTE)", "pesquisadores por milhao de habitantes (FTE)")}
linhas = []
for r in sorted(d["records"], key=lambda r: (r["indicatorId"], r["year"])):
    nome, un, defn = UIS[r["indicatorId"]]
    if r["value"] is None:
        continue
    linhas.append([nome, "UNESCO UIS API " + r["indicatorId"], defn, r["year"], "", repr(r["value"]), un, "qualifier=%s magnitude=%s" % (r["qualifier"], r["magnitude"]), "UIS versao 20260507-91260335 (release fev/2026)"])
gravar(SERIES / "unesco_uis_brasil.csv", linhas)

# ---------- ECI Atlas (Growth Lab) ----------
linhas = []
with open(BRUTO / "atlas_growth_proj_eci_rankings_v12.csv", newline="") as f:
    for r in csv.DictReader(f):
        if r["country_iso3_code"] != "BRA":
            continue
        for col, un, tipo in [("eci_sitc", "indice", "SITC"), ("eci_rank_sitc", "posicao", "SITC"), ("eci_hs92", "indice", "HS92"), ("eci_rank_hs92", "posicao", "HS92"), ("eci_hs12", "indice", "HS12"), ("eci_rank_hs12", "posicao", "HS12")]:
            if r[col] != "":
                linhas.append(["atlas_" + col, "Harvard Growth Lab Atlas (Dataverse doi:10.7910/DVN/XTAQMC)", "ECI %s (%s); in_rankings=%s" % (tipo, "valor" if un == "indice" else "ranking entre pares incluidos", r["in_rankings"]), int(r["year"]), "", r[col], un, "", "dataset v12.0, 2026-02-08"])
gravar(SERIES / "eci_atlas_brasil.csv", linhas)

# ---------- ECI OEC ----------
linhas = []
legado = json.load(open(BRUTO / "oec_legacy_complexity_eci_a_todos_paises.json"))["data"]
for r in sorted((r for r in legado if r["Country Official ID"] == "bra"), key=lambda r: r["Year"]):
    linhas.append(["oec_eci_legado", "OEC API-v2 tesseract cubo legacy_complexity_eci_a", "ECI legado 1964-2017: SITC-4 rev.2, Feenstra et al. (2005) + Comtrade pos-2000; descontinuado (pagina OEC /rankings/legacy/eci)", r["Year"], "", repr(r["ECI"]), "indice", "", "OEC API baixada em 2026-10-20 (sem versao declarada)"])
for rev in ["hs92", "hs96", "hs02", "hs07", "hs12", "hs17", "hs22"]:
    for niv in ["hs4", "hs6"]:
        cubo = "complexity_eci_a_%s_%s" % (rev, niv)
        dados = json.load(open(BRUTO / f"oec_{cubo}.json"))["data"]
        for r in sorted((r for r in dados if r["Country Official ID"] == "bra"), key=lambda r: r["Year"]):
            defn = "ECI %s %s (cubo %s)" % (rev.upper(), niv.upper(), cubo)
            linhas.append(["oec_eci_%s_%s" % (rev, niv), "OEC API-v2 tesseract " + cubo, defn, r["Year"], "", repr(r["ECI"]), "indice", "", "OEC API baixada em 2026-10-20 (sem versao declarada)"])
            if r.get("ECI Rank") is not None:
                linhas.append(["oec_eci_rank_%s_%s" % (rev, niv), "OEC API-v2 tesseract " + cubo, defn + " ranking", r["Year"], "", str(r["ECI Rank"]), "posicao", "", "OEC API baixada em 2026-10-20 (sem versao declarada)"])
gravar(SERIES / "eci_oec_brasil.csv", linhas)

# ---------- derivado: patentes por milhao ----------
FORM = "patentes_por_milhao = IP.PAT.RESD / SP.POP.TOTL x 1e6 (ambos WDI, mesmo ano)"
linhas, comp = [], []
for (cod, a), v in sorted(wdi_val.items(), key=lambda kv: kv[0][1]):
    if cod == "IP.PAT.RESD" and ("SP.POP.TOTL", a) in wdi_val:
        pm = v / wdi_val[("SP.POP.TOTL", a)] * 1e6
        linhas.append(["patentes_residentes_por_milhao", "derivado: WDI IP.PAT.RESD (WIPO) / WDI SP.POP.TOTL", FORM, a, "", repr(pm), "pedidos por milhao de habitantes", "", "WDI lastupdated 2026-10-08"])
        # conferencia: IP.PAT.RESD (WDI) x pedidos de residentes no INPI (WIPO IPSDC); e WIPO por milhao oficial
        w = wipo_val.get(("wipo_pedidos_residentes_inpi", a))
        o = wipo_val.get(("wipo_residentes_por_milhao_oficial", a))
        comp.append([a, v, w, "" if w is None else int(v == w), repr(pm), o, "" if o is None else repr(pm - o)])
gravar(DERIVADO / "patentes_por_milhao.csv", linhas)
with (DERIVADO / "conferencia_patentes.csv").open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["ano", "wdi_ip_pat_resd", "wipo_residentes_inpi", "iguais", "derivado_por_milhao", "wipo_por_milhao_oficial", "diferenca_derivado_menos_oficial"])
    w.writerows(comp)
print("conferencia_patentes.csv", len(comp))

# reservas / PIB (WDI, so conferencia do denominador; nada alem da divisao declarada)
linhas = []
for (cod, a), v in sorted(wdi_val.items(), key=lambda kv: kv[0][1]):
    if cod == "FI.RES.TOTL.CD" and ("NY.GDP.MKTP.CD", a) in wdi_val:
        linhas.append(["reservas_wdi_sobre_pib_wdi", "derivado: WDI FI.RES.TOTL.CD / WDI NY.GDP.MKTP.CD x 100", "reservas_pib_pct = FI.RES.TOTL.CD / NY.GDP.MKTP.CD x 100 (so conferencia; o item do indice usa reservas do BCB / PIB US$ do WDI)", a, "", repr(v / wdi_val[("NY.GDP.MKTP.CD", a)] * 100), "% do PIB", "", "WDI lastupdated 2026-10-08"])
gravar(DERIVADO / "reservas_wdi_pct_pib_wdi.csv", linhas)
