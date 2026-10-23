#!/usr/bin/env python3
"""derivado/conferencia_mesmo_ano.csv: SIM x IBGE RC x ONU WPP (obitos) e SINASC x IBGE RC x WPP (nascimentos), mesmos anos; razoes = base / WPP."""
import csv, glob
P = "/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/populacao-fase2/"
D = {}
for f in glob.glob(P + "series/*.csv") + glob.glob(P + "derivado/wdi_*.csv"):
    for r in csv.DictReader(open(f, encoding="utf-8")):
        if r["mes_ou_trimestre"] == "":
            D.setdefault(r["indicador"], {})[int(r["ano"])] = float(r["valor"])
g = lambda k, a: D.get(k, {}).get(a)
rc_obt_oc = lambda a: g("obitos_ocorridos_no_ano", a) or g("obitos_ocorridos_e_registrados_no_ano", a)
rc_nasc_reg = lambda a: g("nascidos_vivos_registrados_no_ano_lugar_registro", a) or g("nascidos_vivos_registrados_no_ano", a)
rc_obt_reg = lambda a: g("obitos_registrados_no_ano_lugar_registro", a) or g("obitos_registrados_no_ano", a)
H = ["ano", "sim_obitos_ocorrencia", "ibge_rc_obitos_ocorridos", "ibge_rc_obitos_registrados", "onu_wpp_obitos", "wdi_obitos_estimados", "sim/wpp", "rc_ocorridos/wpp", "rc_registrados/wpp",
     "sinasc_nascidos_ocorrencia", "ibge_rc_nascidos_ocorridos", "ibge_rc_nascidos_registrados", "onu_wpp_nascimentos", "wdi_nascimentos_estimados", "sinasc/wpp", "rc_ocorridos/wpp ", "rc_registrados/wpp "]
rows = []
rt = lambda x, y: "" if x is None or not y else round(x / y, 4)
for a in range(1979, 2026):
    ob = [g("obitos_total_por_ocorrencia", a), rc_obt_oc(a), rc_obt_reg(a), g("obitos_wpp", a), g("obitos_estimados_wdi", a)]
    nb = [g("nascidos_vivos_por_ocorrencia", a), g("nascidos_vivos_ocorridos_no_ano", a), rc_nasc_reg(a), g("nascimentos_wpp", a), g("nascimentos_estimados_wdi", a)]
    rows.append([a] + [("" if v is None else int(v)) for v in ob] + [rt(ob[0], ob[3]), rt(ob[1], ob[3]), rt(ob[2], ob[3])]
                + [("" if v is None else int(v)) for v in nb] + [rt(nb[0], nb[3]), rt(nb[1], nb[3]), rt(nb[2], nb[3])])
with open(P + "derivado/conferencia_mesmo_ano.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(H); w.writerows(rows)
for r in rows:
    if r[0] in (1980, 1990, 1995, 2000, 2010, 2016, 2020, 2021, 2022, 2024, 2025): print(r)
