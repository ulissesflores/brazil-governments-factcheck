#!/usr/bin/env python3
"""Compara o ECI do Brasil entre as versoes do dataset Atlas/Growth Lab (Dataverse XTAQMC). Somente stdlib.

Saida: derivado/eci_atlas_revisoes_entre_versoes.csv (formato longo: versao,data,serie,ano,valor).
Identificacao do Brasil: v3/v4 location_id=32 (ids do Atlas antigo; confirmado pelo code=BRA);
v5/v6 country_id=76 (arquivo sem iso3; 76 = codigo M49 do Brasil); v7+ country_iso3_code=BRA.
"""
import csv
import io
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
B = RAIZ / "bruto"
VERS = [
    ("v3", "2022-07-28", "atlas_rankings_v3_2022-07-28.tab"),
    ("v4", "2023-07-28", "atlas_rankings_v4_2023-07-28.tab"),
    ("v5-v6", "2024-09-17", "atlas_rankings_v5-v6_2024-09-17.tab"),
    ("v7", "2025-03-31", "atlas_rankings_v7_2025-03-31.csv"),
    ("v8", "2025-06-10", "atlas_rankings_v8_2025-06-10.csv"),
    ("v9", "2025-06-10", "atlas_rankings_v9_2025-06-10.csv"),
    ("v10", "2025-08-21", "atlas_rankings_v10_2025-08-21.tab"),
    ("v11", "2025-08-21", "atlas_rankings_v11_2025-08-21.csv"),
    ("v12", "2026-02-08", "atlas_growth_proj_eci_rankings_v12.csv"),
]
# nome canonico -> candidatos de coluna
COLS = {
    "eci_sitc": ["sitc_eci", "eci_sitc"],
    "eci_hs92": ["hs_eci", "eci_hs92"],
    "rank_sitc": ["sitc_eci_rank", "eci_rank_sitc"],
    "rank_hs92": ["hs_eci_rank", "eci_rank_hs92"],
}
saida, n_pais = [], []
for v, data, arq in VERS:
    txt = (B / arq).read_text(encoding="utf-8")
    delim = "\t" if arq.endswith(".tab") else ","
    rd = list(csv.DictReader(io.StringIO(txt), delimiter=delim))
    cols = rd[0].keys()
    def eh_br(r):
        if "country_iso3_code" in r:
            return r["country_iso3_code"].strip('"') == "BRA"
        if "code" in r:
            return r["code"].strip('"') == "BRA"
        return r["country_id"] == "76"
    br = [r for r in rd if eh_br(r)]
    ano_col = "year"
    paises_1995 = {r.get("country_id") or r.get("location_id") for r in rd if r[ano_col] == "1995"}
    n_pais.append((v, data, len(paises_1995)))
    for r in br:
        for nome, cands in COLS.items():
            c = next((c for c in cands if c in cols), None)
            val = r[c].strip('"') if c else ""
            if val != "":
                if nome.startswith("rank"):
                    val = str(int(float(val)))
                else:
                    val = repr(round(float(val), 6))
                saida.append([v, data, nome, r[ano_col], val])
with (RAIZ / "derivado" / "eci_atlas_revisoes_entre_versoes.csv").open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["versao", "data_versao", "serie", "ano", "valor"])
    w.writerows(saida)
print(len(saida), n_pais)

# media e desvio-padrao do ECI entre TODOS os paises, v11 x v12 (testa se v12 e um deslocamento global de nivel)
import statistics as st
def _tudo(arq):
    d = {}
    for r in csv.DictReader(open(B / arq)):
        d[(r["country_iso3_code"], r["year"])] = r
    return d
_a, _b = _tudo("atlas_rankings_v11_2025-08-21.csv"), _tudo("atlas_growth_proj_eci_rankings_v12.csv")
with (RAIZ / "derivado" / "eci_atlas_v11_v12_todos_paises_media_dp.csv").open("w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["ano", "coluna", "n_paises_comuns", "dif_media_v12_menos_v11", "dif_dp", "media_v11", "dp_v11", "media_v12", "dp_v12"])
    for ano in ("1995", "2010", "2022"):
        for col in ("eci_hs92", "eci_sitc"):
            dif = [float(_b[k][col]) - float(_a[k][col]) for k in _b if k[1] == ano and k in _a and _b[k][col] and _a[k][col]]
            va = [float(_a[k][col]) for k in _a if k[1] == ano and _a[k][col]]
            vb = [float(_b[k][col]) for k in _b if k[1] == ano and _b[k][col]]
            w.writerow([ano, col, len(dif), round(st.mean(dif), 3), round(st.pstdev(dif), 3), round(st.mean(va), 3), round(st.pstdev(va), 3), round(st.mean(vb), 3), round(st.pstdev(vb), 3)])
