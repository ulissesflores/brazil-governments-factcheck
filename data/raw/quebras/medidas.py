# Medidas de sobreposicao (executado dentro do espaco de nomes de calc.py; nao rodar sozinho).
# Cada medida compara dois metodos/vintages no MESMO periodo, com dados ja baixados.

def _d(a, b, anos, nd=3):
    return {str(y): r3(a[y] - b[y]) for y in anos if y in a and y in b}


def _media(d):
    v = [x for x in d.values() if x is not None]
    return r3(sum(v) / len(v)) if v else None


# 1. PME antiga (30 dias, 15+) x PME nova (semana, 10+), mar-dez/2002 --------------------------------
dif = {m: nov[(2002, m)] - ant[(2002, m)] for m in range(3, 13)}
M["pme_sobreposicao"] = {
    "por_mes_pp": {f"2002-{m:02d}": r3(v) for m, v in dif.items()},
    "antiga_30d": {f"2002-{m:02d}": r3(ant[(2002, m)]) for m in range(3, 13)},
    "nova": {f"2002-{m:02d}": r3(nov[(2002, m)]) for m in range(3, 13)},
    "media_pp": r3(sum(dif.values()) / len(dif)), "min_pp": r3(min(dif.values())), "max_pp": r3(max(dif.values())), "n_meses": len(dif),
}
# manchete publicada pelo IBGE na epoca (referencia SEMANA, 15+): mar/2002 = 7,1 (texto da PME de mar/2002); nov/2002 = 7,1 (texto da PME de nov/2002)
M["pme_semana_vs_30d"] = {
    "2002-03": {"antiga_semana_publicada": 7.1, "antiga_30d_ipeadata": r3(ant[(2002, 3)]), "nova": r3(nov[(2002, 3)])},
    "2002-11": {"antiga_semana_publicada": 7.1, "antiga_30d_ipeadata": r3(ant[(2002, 11)]), "nova": r3(nov[(2002, 11)])},
}
for k, v in M["pme_semana_vs_30d"].items():
    v["efeito_periodo_ref_pp"] = r3(v["antiga_30d_ipeadata"] - v["antiga_semana_publicada"])
    v["efeito_total_vs_semana_pp"] = r3(v["nova"] - v["antiga_semana_publicada"])
    v["efeito_resto_vs_30d_pp"] = r3(v["nova"] - v["antiga_30d_ipeadata"])

# 2. PNAD (setembro, 10+) x PNADC (14+), 2012-2014 ------------------------------------------------------
pnadc_tri = {k: v for k, v in sidra_serie(ER / "sidra-pnadc-trimestral-t4099-raw.json", 4099).items()}
pnadc_q3 = {y: pnadc_tri.get(f"{y}03") for y in (2012, 2013, 2014)}
M["pnad_x_pnadc_desemprego"] = {
    str(y): {"pnad_set": r3(pnad[y]), "pnadc_media_4tri": pnadc[y], "pnadc_3tri": pnadc_q3[y],
             "dif_vs_media_pp": r3(pnadc[y] - pnad[y]), "dif_vs_3tri_pp": r3(pnadc_q3[y] - pnad[y])}
    for y in (2012, 2013, 2014)
}
M["pnad_x_pnadc_desemprego"]["media_dif_3tri_pp"] = r3(sum(pnadc_q3[y] - pnad[y] for y in (2012, 2013, 2014)) / 3)
M["pnad_x_pnadc_desemprego"]["media_dif_anual_pp"] = r3(sum(pnadc[y] - pnad[y] for y in (2012, 2013, 2014)) / 3)

# 3. Gini PNAD x PNADC, 2012-2014 -----------------------------------------------------------------------
pg = serie_csv(GS, "Ipeadata-PGINI", "renda dom. per capita (PNAD antiga, serie interrompida)")
sg = serie_csv(GS, "SIDRA-7435", "renda dom. per capita, precos medios do ano (PNADC)")
M["pnad_x_pnadc_gini"] = {str(y): {"pnad": r3(pg[y]), "pnadc": r3(sg[y]), "dif": r3(sg[y] - pg[y])} for y in (2012, 2013, 2014)}
M["pnad_x_pnadc_gini"]["media_dif"] = r3(sum(sg[y] - pg[y] for y in (2012, 2013, 2014)) / 3)
# Censo 2010 x PNAD vizinha
adh = serie_csv(GS, "Ipeadata-ADH_GINI", "renda dom. per capita, CENSO (Atlas DH)")
M["censo_x_pnad_gini"] = {"censo_2010": adh.get(2010), "pnad_2009": r3(pg.get(2009)), "pnad_2011": r3(pg.get(2011)),
                          "dif_vs_2009": r3(adh.get(2010) - pg.get(2009)), "dif_vs_2011": r3(adh.get(2010) - pg.get(2011)),
                          "censo_1991": adh.get(1991), "censo_2000": adh.get(2000), "pnad_1990": r3(pg.get(1990)), "pnad_1999": r3(pg.get(1999))}
# harmonizacao Ipea (PNAD<=2011 x fator)
hg = serie_csv(GS, "Ipeadata-PNADS_GINI", "harmonizada: PNAD<=2011 multiplicada por fator que iguala 2012")
M["gini_harmonizado_razao"] = {str(y): r3(hg[y] / pg[y]) for y in sorted(hg) if y in pg and y <= 2011}
M["gini_harmonizado_dif"] = {str(y): r3(hg[y] - pg[y]) for y in sorted(hg) if y in pg and y <= 2011}
M["gini_2012_pnad_x_pnadc_razao"] = r3(sg[2012] / pg[2012])

# 4. Pobreza: US$ 5,50 PPC 2011 (SIS 2020) x US$ 6,85 PPC 2017 (SIS 2025), 2012-2019 -----------------------
s550 = serie_csv(PS, "IBGE-SIS2020-PPC2011", "US$ 5,5 PPC2011")
s685 = serie_csv(PS, "IBGE-SIS2025", "US$ 6,85 PPC2017")
s320 = serie_csv(PS, "IBGE-SIS2020-PPC2011", "US$ 3,2 PPC2011")
s365 = serie_csv(PS, "IBGE-SIS2025", "US$ 3,65 PPC2017")
s190 = serie_csv(PS, "IBGE-SIS2020-PPC2011", "US$ 1,9 PPC2011")
s215 = serie_csv(PS, "IBGE-SIS2025", "US$ 2,15 PPC2017")
anos = range(2012, 2020)
M["sis_550_x_685"] = {"por_ano": {str(y): {"5.50_ppc2011": s550[y], "6.85_ppc2017": s685[y], "dif_pp": r3(s685[y] - s550[y])} for y in anos},
                      "media_dif_pp": _media(_d(s685, s550, anos))}
M["sis_320_x_365"] = {"media_dif_pp": _media(_d(s365, s320, anos)), "por_ano": _d(s365, s320, anos)}
M["sis_190_x_215"] = {"media_dif_pp": _media(_d(s215, s190, anos)), "por_ano": _d(s215, s190, anos)}
# edicoes do SIS (mesma linha 5,50 PPC 2011)
e18 = serie_csv(PS, "IBGE-SIS2018-PPC2011", "US$ 5,5 PPC2011")
e19 = serie_csv(PS, "IBGE-SIS2019-PPC2011", "US$ 5,5 PPC2011")
M["sis_edicoes_550"] = {"2016": {"SIS2018": e18.get(2016), "SIS2019": e19.get(2016), "SIS2020": s550.get(2016)},
                        "2017": {"SIS2018": e18.get(2017), "SIS2019": e19.get(2017), "SIS2020": s550.get(2017)}}
e24 = serie_csv(PS, "IBGE-SIS2024", "US$ 6,85 PPC2017")
M["sis_edicoes_685"] = {"max_abs_dif_pp_2012_2023": r3(max(abs(s685[y] - e24[y]) for y in e24 if y in s685)),
                        "2023": {"SIS2024": e24.get(2023), "SIS2025": s685.get(2023)}}

# 5. PIP x IBGE SIS na MESMA linha (6,85 PPC 2017), 2012-2024 ----------------------------------------------
p685 = pipd[(2017, "6.85")]
anos = range(2012, 2025)
M["pip_x_sis_685"] = {"por_ano": {str(y): {"pip": r3(p685[y]), "sis": s685[y], "dif_pp": r3(p685[y] - s685[y]), "razao": r3(p685[y] / s685[y])} for y in anos if y in p685 and y in s685},
                      "media_dif_pp": _media(_d(p685, s685, anos)), "media_dif_pp_sem_2020": _media({y: v for y, v in _d(p685, s685, anos).items() if y != "2020"})}
for l, sd in (("2.15", s215), ("3.65", s365)):
    pl = pipd[(2017, l)]
    M[f"pip_x_sis_{l}"] = {"media_dif_pp": _media(_d(pl, sd, anos)), "por_ano": _d(pl, sd, anos)}
# visita: PIP usa quinta visita so em 2020-2021; SIS usa 2020-2022
M["visitas_pnadc"] = {"pip": {str(a): r["survey_acronym"] for a, r in pip(SO / "bruto" / "pip_ppp2017_line6.85.json").items() if a >= 2019},
                      "sis_e_ipeadata": "quintas visitas em 2020-2022 (nota da PNADC; ver quebras.csv)"}

# 6. PIP: linhas PPC 2017 x PPC 2021 (a mudanca de PPC), por ano e por governo --------------------------------
par = (("2.15", "3.00"), ("3.65", "4.20"), ("6.85", "8.30"))
M["pip_ppc"] = {}
for a_, b_ in par:
    d17, d21 = pipd[(2017, a_)], pipd[(2021, b_)]
    difs = {y: d21[y] - d17[y] for y in d17 if y in d21}
    por_gov = {}
    for gname, y0, y1 in GOV:
        v = [difs[y] for y in range(y0, y1 + 1) if y in difs]
        if v:
            por_gov[gname] = {"media_dif_pp": r3(sum(v) / len(v)), "n": len(v)}
    M["pip_ppc"][f"{a_}->{b_}"] = {"dif_pp_por_ano": {str(y): r3(v) for y, v in sorted(difs.items())}, "por_governo": por_gov,
                                    "media_geral_pp": r3(sum(difs.values()) / len(difs))}

# 7. Expectativa de vida: vintages sobre o mesmo ano -------------------------------------------------------
e = M
anosv = [y for y in (2000, 2010, 2019, 2020, 2021, 2022, 2023, 2024) if str(y) in M["e0_vigente"]]
M["e0_publicada_x_vigente"] = {str(y): {"publicada": M["e0_publicada"].get(str(y)), "vigente": M["e0_vigente"][str(y)],
                                        "dif": r3(M["e0_vigente"][str(y)] - M["e0_publicada"][str(y)])}
                               for y in anosv if str(y) in M["e0_publicada"]}
M["e0_wdi_x_vigente"] = {str(y): {"wdi": r3(M["e0_wdi"][str(y)]), "vigente": M["e0_vigente"][str(y)], "dif": r3(M["e0_wdi"][str(y)] - M["e0_vigente"][str(y)])}
                         for y in sorted(map(int, M["e0_vigente"])) if str(y) in M["e0_wdi"]}
M["e0_revisoes_ano2000"] = {"tabua_2000_publicada": M["e0_publicada"].get("2000"), "rev2008": M["e0_rev08"].get("2000"),
                            "rev2013": M["e0_rev13"].get("2000"), "rev2018": M["e0_rev18"].get("2000"),
                            "vigente_rev2024": M["e0_vigente"].get("2000"), "wdi": r3(M["e0_wdi"].get("2000"))}
M["e0_revisoes_ano2010"] = {"tabua_2010_publicada": M["e0_publicada"].get("2010"), "rev2013": M["e0_rev13"].get("2010"),
                            "rev2018": M["e0_rev18"].get("2010"), "vigente_rev2024": M["e0_vigente"].get("2010"), "wdi": r3(M["e0_wdi"].get("2010"))}
comuns = [y for y in M["e0_rev13"] if y in M["e0_rev18"]]
M["e0_rev13_x_rev18"] = {"max_abs_dif": r3(max(abs(M["e0_rev18"][y] - M["e0_rev13"][y]) for y in comuns)), "n_anos": len(comuns)}
comuns = [y for y in M["e0_publicada"] if y in M["e0_rev18"]]
M["e0_publicada_x_rev18"] = {y: r3(M["e0_publicada"][y] - M["e0_rev18"][y]) for y in sorted(comuns)}

# 8. Monetario: quebra de 2018 ------------------------------------------------------------------------------
M["monetario_quebra_2018"] = [dict(r) for r in csv.DictReader(open(MO / "saida" / "agregados_quebra_2018.csv"))]

# 9. IPCA: contrafactual de pesos por grupo (IBGE SIDRA 1419/7060; BCB Estudo Especial 70) ---------------------
def _grupos(arq):
    d = json.load(open(arq))
    out = {"63": {}, "66": {}}
    for v in d:
        for r in v["resultados"]:
            cat = list(r["classificacoes"][0]["categoria"].items())[0]
            out[v["id"]][cat[0]] = {k: float(x) for k, x in r["series"][0]["serie"].items()}
    return out


G1 = _grupos(D / "quebras" / "bruto" / "sidra-1419-ipca-grupos-2012-2019.json")
G2 = _grupos(D / "quebras" / "bruto" / "sidra-7060-ipca-grupos-2020-2026.json")
GRP = ["7170", "7445", "7486", "7558", "7625", "7660", "7712", "7766", "7786"]


def cadeia(var, w0, meses):
    """IPCA acumulado (%) por Laspeyres mensal com pesos iniciais w0 (soma 100), atualizados pelos relativos de grupo."""
    w = dict(zip(GRP, [x / sum(w0) for x in w0]))
    p = 1.0
    for m in meses:
        r = {g_: var[g_][m] / 100 for g_ in GRP}
        R = sum(w[g_] * r[g_] for g_ in GRP)
        p *= 1 + R
        w = {g_: w[g_] * (1 + r[g_]) / (1 + R) for g_ in GRP}
    return (p - 1) * 100


var1 = G1["63"]
var2 = G2["63"]
# (a) 2018, pesos de jan/2018 das duas estruturas (BCB, Relatorio de Inflacao dez/2019, Tabela 2)
w_old18 = [24.58, 15.72, 3.98, 5.96, 18.28, 12.04, 10.96, 4.83, 3.65]
w_new18 = [18.99, 15.16, 4.02, 4.80, 20.84, 13.46, 10.60, 5.95, 6.19]
m18 = [f"2018{m:02d}" for m in range(1, 13)]
vg = {g_: var1[g_] for g_ in GRP}
M["ipca_cf_2018"] = {"pesos_POF0809_jan2018": w_old18, "pesos_POF1718_jan2018": w_new18,
                     "ipca_publicado_2018": r3(ipca_a[2018]), "reconstrucao_pesos_antigos": r3(cadeia(vg, w_old18, m18)),
                     "reconstrucao_pesos_novos": r3(cadeia(vg, w_new18, m18))}
M["ipca_cf_2018"]["efeito_pp"] = r3(M["ipca_cf_2018"]["reconstrucao_pesos_novos"] - M["ipca_cf_2018"]["reconstrucao_pesos_antigos"])
# (b) 2020-2025: pesos de dez/2019 (estrutura antiga, ja evoluida) x pesos de jan/2020 (estrutura nova)
w_old20 = [G1["66"][g_]["201912"] for g_ in GRP]
w_new20 = [G2["66"][g_]["202001"] for g_ in GRP]
M["ipca_cf_2020_2025"] = {"pesos_dez2019_estrutura_antiga": w_old20, "pesos_jan2020_estrutura_nova": w_new20, "por_ano": {}}
for y in range(2020, 2026):
    meses = [f"{y}{m:02d}" for m in range(1, 13)]
    vg2 = {g_: var2[g_] for g_ in GRP}
    # cada ano reinicia com os pesos do mes anterior segundo a propria estrutura: usa pesos mensais publicados de dezembro anterior (nova) e
    # para a antiga evolui os pesos dez/2019 ate o inicio do ano
    if y == 2020:
        wa, wn = w_old20, w_new20
    else:
        wn = [G2["66"][g_][f"{y - 1}12"] for g_ in GRP]
        # evolui a estrutura antiga ate dez do ano anterior
        w = dict(zip(GRP, [x / sum(w_old20) for x in w_old20]))
        for yy in range(2020, y):
            for m in range(1, 13):
                k = f"{yy}{m:02d}"
                r = {g_: var2[g_][k] / 100 for g_ in GRP}
                R = sum(w[g_] * r[g_] for g_ in GRP)
                w = {g_: w[g_] * (1 + r[g_]) / (1 + R) for g_ in GRP}
        wa = [w[g_] * 100 for g_ in GRP]
    ca, cn = cadeia(vg2, wa, meses), cadeia(vg2, wn, meses)
    M["ipca_cf_2020_2025"]["por_ano"][str(y)] = {"publicado": r3(ipca_a[y]), "recons_pesos_antigos": r3(ca), "recons_pesos_novos": r3(cn), "efeito_pp": r3(cn - ca)}
acum = {"antigos": 1.0, "novos": 1.0, "publicado": 1.0}
for y in range(2020, 2026):
    d_ = M["ipca_cf_2020_2025"]["por_ano"][str(y)]
    acum["antigos"] *= 1 + d_["recons_pesos_antigos"] / 100
    acum["novos"] *= 1 + d_["recons_pesos_novos"] / 100
    acum["publicado"] *= 1 + d_["publicado"] / 100
M["ipca_cf_2020_2025"]["acumulado_2020_2025"] = {k: r3((v - 1) * 100) for k, v in acum.items()}
M["ipca_cf_2020_2025"]["efeito_medio_anual_pp"] = r3(sum(M["ipca_cf_2020_2025"]["por_ano"][str(y)]["efeito_pp"] for y in range(2020, 2026)) / 6)

# 10. Pobreza: Ipea PNADS_PERCPOBRE830 x SIDRA 5877 (mesma linha 8,30 PPC 2021) ---------------------------------
i830 = serie_csv(PS, "Ipeadata-PNADS_PERCPOBRE830", "PPC$8,30 (2021)")
sd830 = serie_csv(PS, "SIDRA-5877", "linha nacional ODS US$ 8,30 PPC2021")
M["ipea_x_sidra_830"] = {"max_abs_dif_2012_2024": r3(max(abs(i830[y] - sd830[y]) for y in range(2012, 2025) if y in i830 and y in sd830))}

# 11. PIB: vintages anuais (SIDRA 9810 x Ipeadata SCN10_PIBG10 x indice SCN10_PIB10) ---------------------------------
_s9810 = {int(k): float(v) for k, v in sidra_serie(ER / "sidra-t6784-pib-percapita-raw.json", 9810).items()}
M["pib_sidra9810_x_ipeadata"] = {str(y): {"sidra_9810": _s9810[y], "ipeadata": r3(g[y]), "dif": r3(_s9810[y] - g[y])} for y in sorted(_s9810) if abs(_s9810[y] - g[y]) > 0.05}
_idx = ipea_a("SCN10_PIB10")
M["pib_indice_x_taxa_2024"] = {"taxa_SCN10_PIBG10": r3(g[2024]), "razao_do_indice_SCN10_PIB10": r3((_idx[2024] / _idx[2023] - 1) * 100)}

# 12. Salario minimo: efeito do fator 1,2225 de jul/1994 (serie Ipea x nominal/INPC sem fator) ---------------------------
M["salmin_fator_1994"] = {gname: {"ipea": M["salmin_por_governo"][f"{gname}|mandato|{a}-{b}"]["Ipea composto"], "inpc_puro": M["salmin_por_governo"][f"{gname}|mandato|{a}-{b}"]["INPC"]}
                         for gname, a, b in GOV if gname in ("Collor", "Itamar Franco", "FHC", "Lula 1-2")}

# 13. Pobreza: linha propria do Ipea (PPY, PNAD) x linhas internacionais do SIS, 2012-2014 ------------------------------
_ppy = serie_csv(PS, "Ipeadata-DISOC_PPY", "linha propria Ipea = 2x indigencia (cesta FAO), 24 regioes; serie INTERROMPIDA")
M["ppy_x_sis"] = {str(y): {"ipea_ppy_pnad": _ppy.get(y), "sis_3.20_ppc2011": s320.get(y), "sis_5.50_ppc2011": s550.get(y)} for y in (2012, 2013, 2014)}
