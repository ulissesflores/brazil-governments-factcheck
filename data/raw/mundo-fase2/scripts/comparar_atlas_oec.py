#!/usr/bin/env python3
"""Compara ECI do Brasil: Atlas v12 x OEC (hs92 hs6/hs4, legado SITC). Somente stdlib.
Saida: derivado/eci_atlas_v12_vs_oec.csv e resumo (correlacao de Pearson e diferenca media) impresso."""
import csv
import statistics as st
from pathlib import Path

R = Path(__file__).resolve().parent.parent
def ler(f):
    d = {}
    for r in csv.DictReader(open(R / "series" / f)):
        d.setdefault(r["indicador"], {})[int(r["ano"])] = float(r["valor"])
    return d
A, O = ler("eci_atlas_brasil.csv"), ler("eci_oec_brasil.csv")
# versoes antigas do Atlas (v3/v4 = SITC/HS 1995-2017 ~ mesma janela do legado)
V = {}
for r in csv.DictReader(open(R / "derivado" / "eci_atlas_revisoes_entre_versoes.csv")):
    V.setdefault((r["versao"], r["serie"]), {})[int(r["ano"])] = float(r["valor"])
pares = [
    ("atlas_v12_eci_hs92", A["atlas_eci_hs92"], "oec_eci_hs92_hs6", O["oec_eci_hs92_hs6"]),
    ("atlas_v12_eci_hs92", A["atlas_eci_hs92"], "oec_eci_hs92_hs4", O["oec_eci_hs92_hs4"]),
    ("atlas_v12_eci_sitc", A["atlas_eci_sitc"], "oec_eci_legado", O["oec_eci_legado"]),
    ("atlas_v4_eci_sitc", V[("v4", "eci_sitc")], "oec_eci_legado", O["oec_eci_legado"]),
    ("atlas_v11_eci_sitc", V[("v11", "eci_sitc")], "oec_eci_legado", O["oec_eci_legado"]),
    ("atlas_v11_eci_hs92", V[("v11", "eci_hs92")], "oec_eci_hs92_hs6", O["oec_eci_hs92_hs6"]),
]
linhas = []
for na, a, no, o in pares:
    anos = sorted(set(a) & set(o))
    xs, ys = [a[y] for y in anos], [o[y] for y in anos]
    cor = st.correlation(xs, ys)
    dif = st.mean(x - y for x, y in zip(xs, ys))
    print("%-20s x %-18s anos %d-%d n=%d  pearson=%.3f  dif_media(atlas-oec)=%.3f" % (na, no, anos[0], anos[-1], len(anos), cor, dif))
    for y in anos:
        linhas.append([na, no, y, a[y], o[y], a[y] - o[y]])
with (R / "derivado" / "eci_atlas_v12_vs_oec.csv").open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["base_a", "base_b", "ano", "valor_a", "valor_b", "a_menos_b"])
    w.writerows(linhas)
