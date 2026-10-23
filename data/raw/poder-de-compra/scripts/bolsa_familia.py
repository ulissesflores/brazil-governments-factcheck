#!/usr/bin/env python3
"""Linhas de elegibilidade do Bolsa Familia 2004-2025 contra 1/4 e 1/2 do salario minimo, as linhas internacionais e a linha do Atlas (Ipea/PNUD/FJP).

python3 -I bolsa_familia.py   (sem rede). Le: ../../quebras/bolsa-familia-linhas-elegibilidade.csv, ../../quebras/pobreza-linhas-em-reais-reais.csv,
../../economia-real (SM nominal, INPC). Escreve ../series/bolsa_familia_linhas.csv
"""
import csv
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
D = AQUI.parent.parent


def ipea(arq):
    return {(int(x["VALDATA"][:4]), int(x["VALDATA"][5:7])): float(x["VALVALOR"]) for x in json.load(open(arq))["value"] if x["VALVALOR"] is not None}


sm = ipea(D / "economia-real/ipeadata-MTE12_SALMIN12-raw.json")
inpc = {}
v = 100.0
for x in json.load(open(D / "economia-real/bcb-sgs188-raw.json")):
    d, m, a = x["data"].split("/")
    v *= 1 + float(x["valor"]) / 100
    inpc[(int(a), int(m))] = v
ipca = {}
v = 100.0
for x in json.load(open(D / "economia-real/bcb-sgs433-raw.json")):
    d, m, a = x["data"].split("/")
    v *= 1 + float(x["valor"]) / 100
    ipca[(int(a), int(m))] = v
REF = (2026, 9)
# linhas internacionais e do Atlas atualizadas pelo IPCA (mesmo criterio de quebras/pobreza-linhas-em-reais-reais.csv: IPCA medio de 2017);
# salario minimo e linhas do Bolsa Familia em reais de set/2026 pelo INPC (mesmo criterio de quebras/bolsa-familia-linhas-elegibilidade.csv)
f17 = sum(ipca[(2017, m)] for m in range(1, 13)) / 12
intl = {r["linha"]: float(r["R$_mensal_precos_do_ano_base"]) for r in csv.DictReader(open(D / "quebras/pobreza-linhas-em-reais-reais.csv"))}
L215, L365 = intl["US$ 2.15 (PPC 2017)"], intl["US$ 3.65 (PPC 2017)"]
conf = [r for r in csv.DictReader(open(D / "quebras/pobreza-linhas-em-reais-reais.csv")) if r["linha"] == "US$ 2.15 (PPC 2017)"][0]
print("conferencia: US$2,15 PPC2017 = R$", L215, "(2017) x IPCA(set/2026)/IPCA(media 2017) =", round(L215 * ipca[REF] / f17, 2), "| arquivo da pasta quebras diz", conf["R$_mensal_set2026"])
ATLAS_EXTR, ATLAS_POBRE, ATLAS_BASE = 70.0, 140.0, (2010, 8)   # Atlas do Desenvolvimento Humano (PNUD/Ipea/FJP): R$ 70 e R$ 140 mensais, reais de ago/2010
rows = []
for r in csv.DictReader(open(D / "quebras/bolsa-familia-linhas-elegibilidade.csv")):
    ano, mes = int(r["inicio_dos_efeitos"][:4]), int(r["inicio_dos_efeitos"][5:7])
    k = (ano, mes)
    pob = float(r["linha_pobreza_nominal_R$"])
    ext = float(r["linha_extrema_pobreza_nominal_R$"]) if r["linha_extrema_pobreza_nominal_R$"].replace(".", "").isdigit() else None
    S = sm[k]
    fk = inpc[REF] / inpc[k]
    i215, i365 = L215 * ipca[k] / f17, L365 * ipca[k] / f17        # R$ do mes de inicio
    a_ext, a_pob = ATLAS_EXTR * ipca[k] / ipca[ATLAS_BASE], ATLAS_POBRE * ipca[k] / ipca[ATLAS_BASE]
    rows.append({
        "inicio": r["inicio_dos_efeitos"], "instrumento": r["instrumento"], "programa": "Auxilio Brasil" if "Auxilio" in r["instrumento"] else "Bolsa Familia",
        "linha_pobreza_R$": pob, "linha_extrema_R$": ext if ext else "",
        "SM_vigente_R$": S, "um_quarto_SM_R$": round(S / 4, 2), "meio_SM_R$": round(S / 2, 2),
        "pobreza_/_meio_SM": round(pob / (S / 2), 3), "extrema_/_um_quarto_SM": round(ext / (S / 4), 3) if ext else "",
        "pobreza_/_SM": round(pob / S, 3),
        "US$2,15_PPC2017_em_R$_do_mes": round(i215, 2), "US$3,65_PPC2017_em_R$_do_mes": round(i365, 2),
        "extrema_/_US$2,15": round(ext / i215, 3) if ext else "", "pobreza_/_US$3,65": round(pob / i365, 3),
        "Atlas_extrema_R$70_ago2010_em_R$_do_mes": round(a_ext, 2), "Atlas_pobre_R$140_ago2010_em_R$_do_mes": round(a_pob, 2),
        "extrema_/_Atlas_extrema": round(ext / a_ext, 3) if ext else "", "pobreza_/_Atlas_pobre": round(pob / a_pob, 3),
        "pobreza_real_set2026_INPC": round(pob * fk, 2), "extrema_real_set2026_INPC": round(ext * fk, 2) if ext else "",
        "SM_real_set2026_INPC": round(S * fk, 2), "INPC_fator_para_set2026": round(fk, 4),
    })
# linha vigente em 19/10/2026 segundo o texto consolidado da Lei 14.601 (art. 5, II: R$ 218,00): linha nominal inalterada desde 06/2023
def comp(inicio, instr, prog, pob, ext, k):
    S = sm[k]
    fk = inpc[REF] / inpc[k]
    i215, i365 = L215 * ipca[k] / f17, L365 * ipca[k] / f17
    a_ext, a_pob = ATLAS_EXTR * ipca[k] / ipca[ATLAS_BASE], ATLAS_POBRE * ipca[k] / ipca[ATLAS_BASE]
    return {
        "inicio": inicio, "instrumento": instr, "programa": prog,
        "linha_pobreza_R$": pob, "linha_extrema_R$": ext if ext else "",
        "SM_vigente_R$": S, "um_quarto_SM_R$": round(S / 4, 2), "meio_SM_R$": round(S / 2, 2),
        "pobreza_/_meio_SM": round(pob / (S / 2), 3), "extrema_/_um_quarto_SM": round(ext / (S / 4), 3) if ext else "",
        "pobreza_/_SM": round(pob / S, 3),
        "US$2,15_PPC2017_em_R$_do_mes": round(i215, 2), "US$3,65_PPC2017_em_R$_do_mes": round(i365, 2),
        "extrema_/_US$2,15": round(ext / i215, 3) if ext else "", "pobreza_/_US$3,65": round(pob / i365, 3),
        "Atlas_extrema_R$70_ago2010_em_R$_do_mes": round(a_ext, 2), "Atlas_pobre_R$140_ago2010_em_R$_do_mes": round(a_pob, 2),
        "extrema_/_Atlas_extrema": round(ext / a_ext, 3) if ext else "", "pobreza_/_Atlas_pobre": round(pob / a_pob, 3),
        "pobreza_real_set2026_INPC": round(pob * fk, 2), "extrema_real_set2026_INPC": round(ext * fk, 2) if ext else "",
        "SM_real_set2026_INPC": round(S * fk, 2), "INPC_fator_para_set2026": round(fk, 4),
    }


rows.append(comp("2026-09", "Lei 14.601/2023, art. 5, II, texto consolidado lido em 2026-10-19 (linha nominal sem reajuste desde 2023-06)", "Bolsa Familia", 218.0, None, (2026, 9)))
# anual: linha em vigor em dezembro de cada ano, 2004-2025
vig = [(tuple(map(int, r["inicio"].split("-"))), r) for r in rows[:-1]]
anual = []
for y in range(2004, 2026):
    ativo = [(k, r) for k, r in vig if k <= (y, 12)]
    k, r = ativo[-1]
    anual.append({"ano_dezembro": y, **comp(r["inicio"], r["instrumento"], r["programa"], r["linha_pobreza_R$"], r["linha_extrema_R$"] if r["linha_extrema_R$"] != "" else None, (y, 12))})
with open(AQUI.parent / "series/bolsa_familia_linhas_anual.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(anual[0]))
    w.writeheader()
    w.writerows(anual)
for a in anual:
    print(a["ano_dezembro"], a["programa"][:3], "vigente desde", a["inicio"], "pob", a["linha_pobreza_R$"], "ext", a["linha_extrema_R$"], "SM", a["SM_vigente_R$"], "pob/SM", a["pobreza_/_SM"], "pob real set26", a["pobreza_real_set2026_INPC"], "ext real", a["extrema_real_set2026_INPC"], "| pob/US3.65", a["pobreza_/_US$3,65"], "ext/US2.15", a["extrema_/_US$2,15"], "ext/Atlas", a["extrema_/_Atlas_extrema"])
cab = list(rows[0])
with open(AQUI.parent / "series/bolsa_familia_linhas.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, cab)
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r["inicio"], r["programa"][:3], r["linha_pobreza_R$"], r["linha_extrema_R$"], "SM", r["SM_vigente_R$"], "| pob/SM", r["pobreza_/_SM"], "pob/(1/2 SM)", r["pobreza_/_meio_SM"], "ext/(1/4 SM)", r["extrema_/_um_quarto_SM"], "| ext/US2.15", r["extrema_/_US$2,15"], "pob/US3.65", r["pobreza_/_US$3,65"], "| ext/Atlas", r["extrema_/_Atlas_extrema"], "pob/Atlas", r["pobreza_/_Atlas_pobre"], "| real set26 pob", r["pobreza_real_set2026_INPC"], "ext", r["extrema_real_set2026_INPC"])
