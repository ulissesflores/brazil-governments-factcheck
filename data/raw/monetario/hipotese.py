# Teste de hipotese "a inflacao oficial esconde algo": MEDE, nao endossa. LE so bruto/ e saida/. SEM REDE. Rodar: python3 -I hipotese.py
# (1) IPCA livres (SGS 11428) x monitorados (SGS 4449) x IPCA cheio (433), 1991-2025, foco 2011-2016.
#     ATENCAO: o SGS 11427 NAO e "administrados": o catalogo do BCB o nomeia "IPCA - Nucleo por exclusao - Sem monitorados e alimentos no domicilio".
# (2) Plano Cruzado (congelamento de 28/02/1986): 4 indices x moeda (M0/M1) em 1986-87.
import csv, json, math, pathlib
AQUI = pathlib.Path(__file__).resolve().parent; BR = AQUI / "bruto"; S = AQUI / "saida"
def bcb(c): return {r["data"][6:] + "-" + r["data"][3:5]: float(r["valor"]) for r in json.load(open(BR / f"bcb_sgs_{c}.json")) if r["valor"] not in (None, "")}
IPCA, LIV, MON, INPC, IGPM, IGPDI = bcb(433), bcb(11428), bcb(4449), bcb(188), bcb(189), bcb(190)
mensal = {r["ym"]: r for r in csv.DictReader(open(S / "mensal.csv"))}

def acum(d, ini, fim):
    """Variacao acumulada (%) de ini ('AAAA-MM') a fim ('AAAA-MM') inclusive; None se faltar mes."""
    f = 1.0; y, m = int(ini[:4]), int(ini[5:])
    while f"{y}-{m:02d}" <= fim:
        v = d.get(f"{y}-{m:02d}")
        if v is None: return None
        f *= 1 + v / 100
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return 100 * (f - 1)
ano = lambda d, y: acum(d, f"{y}-01", f"{y}-12")

# --- (1) ---
linhas = []
for y in range(1991, 2026):
    i, l, m = ano(IPCA, y), ano(LIV, y), ano(MON, y)
    linhas.append([y, i, l, m, None if (l is None or m is None) else m - l, ano(IGPDI, y), ano(INPC, y), ano(IGPM, y)])
with open(S / "hipotese_livres_monitorados.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ano", "ipca", "ipca_livres_11428", "ipca_monitorados_4449", "monitorados_menos_livres_pp", "igp_di", "inpc", "igp_m"])
    for r in linhas: w.writerow([r[0]] + [("" if x is None else round(x, 3)) for x in r[1:]])

# peso implicito dos monitorados: IPCA - livres = k * (monitorados - livres)  (k = peso dos monitorados), OLS sem intercepto, mensal
def peso(ini, fim):
    xs, ys = [], []
    y, m = int(ini[:4]), int(ini[5:])
    while f"{y}-{m:02d}" <= fim:
        k = f"{y}-{m:02d}"
        if k in IPCA and k in LIV and k in MON: xs.append(MON[k] - LIV[k]); ys.append(IPCA[k] - LIV[k])
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    b = sum(a * c for a, c in zip(xs, ys)) / sum(a * a for a in xs)
    ss = sum((c - b * a) ** 2 for a, c in zip(xs, ys)); tot = sum(c * c for c in ys)
    return b, 1 - ss / tot, len(xs)
with open(S / "hipotese_peso_implicito.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["janela", "peso_implicito_monitorados", "R2", "meses"])
    for a, b in (("2011-01", "2016-12"), ("2012-01", "2014-12"), ("2015-01", "2015-12"), ("2017-01", "2025-12")):
        k, r2, n = peso(a, b); w.writerow([f"{a}..{b}", round(k, 3), round(r2, 4), n])
# acumulados de janelas
with open(S / "hipotese_acumulados.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["janela", "ipca", "livres", "monitorados", "igp_di", "inpc", "monitorados_menos_livres_pp"])
    for a, b in (("2013-01", "2015-12"), ("2012-01", "2014-12"), ("2012-01", "2016-12"), ("2011-01", "2016-12"), ("2015-01", "2015-12"), ("2003-01", "2010-12"), ("2017-01", "2022-12")):
        v = [acum(d, a, b) for d in (IPCA, LIV, MON, IGPDI, INPC)]
        w.writerow([f"{a}..{b}"] + [round(x, 2) for x in v] + [round(v[2] - v[1], 2)])

# --- (2) Plano Cruzado ---
IDX = (("IPCA(433)", IPCA), ("INPC(188)", INPC), ("IGP-DI(190)", IGPDI))
with open(S / "hipotese_cruzado_mensal.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["mes", "IPCA", "INPC", "IGP_DI", "max_menos_min_pp", "M0_var_mes_pct", "M1_var_mes_pct"])
    y, m = 1985, 10
    while (y, m) <= (1987, 12):
        k, kp = f"{y}-{m:02d}", (f"{y}-{m-1:02d}" if m > 1 else f"{y-1}-12")
        v = [d.get(k) for _, d in IDX]
        g = lambda c: (float(mensal[k][c]) / float(mensal[kp][c]) - 1) * 100 if (k in mensal and kp in mensal and mensal[k][c] and mensal[kp][c]) else None
        w.writerow([k] + [("" if x is None else x) for x in v] + [("" if None in v else round(max(v) - min(v), 2))] + [("" if (z := g(c)) is None else round(z, 2)) for c in ("M0_fim", "M1_fim")])
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
with open(S / "hipotese_cruzado_acumulados.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["janela", "IPCA", "INPC", "IGP_DI", "M0_fim_var_pct", "M1_fim_var_pct", "M1_real_var_pct(M1/IGP-DI)"])
    for nome, a, b in (("pre-congelamento 1985-03..1986-02 (12m)", "1985-03", "1986-02"), ("congelamento 1986-03..1986-10", "1986-03", "1986-10"), ("1986-03..1986-11", "1986-03", "1986-11"),
                       ("ano 1986", "1986-01", "1986-12"), ("pos-congelamento 1987-01..1987-12", "1987-01", "1987-12"), ("1986-03..1987-12", "1986-03", "1987-12")):
        v = [acum(d, a, b) for _, d in IDX]
        ka = f"{int(a[:4])}-{int(a[5:])-1:02d}" if int(a[5:]) > 1 else f"{int(a[:4])-1}-12"
        gM = lambda c: 100 * (float(mensal[b][c]) / float(mensal[ka][c]) - 1)
        real = 100 * ((float(mensal[b]["M1_fim"]) / float(mensal[b]["igpdi_idx"])) / (float(mensal[ka]["M1_fim"]) / float(mensal[ka]["igpdi_idx"])) - 1)
        w.writerow([nome] + [round(x, 2) for x in v] + [round(gM("M0_fim"), 1), round(gM("M1_fim"), 1), round(real, 1)])
for fn in ("hipotese_livres_monitorados", "hipotese_peso_implicito", "hipotese_acumulados", "hipotese_cruzado_mensal", "hipotese_cruzado_acumulados"):
    print("##", fn); print(open(S / (fn + ".csv")).read())
