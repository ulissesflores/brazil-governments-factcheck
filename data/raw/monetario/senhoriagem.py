# Senhoriagem / imposto inflacionario por ano e por governo. LE so saida/*.csv e referencias/*.csv (gerados a partir do bruto). SEM REDE.
# Rodar: python3 -I construir.py && python3 -I senhoriagem.py
#
# Formulas (todas em % do PIB nominal anual; base = M0, base monetaria restrita):
#  (a) variacao da base:        a_y   = (M0_dez_y - M0_dez_{y-1}) / PIB_y
#  (b) imposto inflacionario    b_y   = pi_y/(1+pi_y) * M0_medio_y / PIB_y          pi_y = IGP-DI dez/dez  (b2: IPCA dez/dez, so 1980+)
#      (forma ANUAL; M0_medio = media dos 12 saldos mensais - ver A_M0)
#  (c) Cysne e Coimbra-Lisboa (2004) eq. (2), forma MENSAL:
#      II_y  = sum_{t=1..12} A_t * (P_{t+1}-P_t)/P_{t+1} / PIB_y,  A=M0 (II) ; A=M1 (TIT) ; TI = TIT - II ; P = IGP-DI (indice mensal)
#      A_t = saldo de fim de mes ate 1979; media mensal dos saldos diarios de 1980 em diante (como no artigo; jan/1980 sem media -> fim de mes).
#  (d) Ayres et al. (2018/19) apendice C eq. (2): seigniorage_y = (N_y - N_{y-1})/N_y * M0_dez_{y-1}/N_{y-1}  (N = PIB nominal)
#      real_base_y = M0_dez_y/N_y - M0_dez_{y-1}/N_{y-1};   (d1)+(d2) = (a) por identidade algebrica.
import csv, math, pathlib, collections, datetime
AQUI = pathlib.Path(__file__).resolve().parent; S = AQUI / "saida"

def fl(x): return float(x) if x not in ("", None) else None
M = {r["ym"]: {k: fl(v) for k, v in r.items() if k != "ym"} for r in csv.DictReader(open(S / "mensal.csv"))}
PIB = {int(r["ano"]): fl(r["PIB_RSmi"]) for r in csv.DictReader(open(S / "anual.csv"))}
CY = {int(r["ano"]): {k: float(v) for k, v in r.items() if k != "ano"} for r in csv.DictReader(open(AQUI / "referencias" / "cysne_coimbra_lisboa_2004_tabela1_transcrita.csv"))}
ym = lambda y, m: f"{y}-{m:02d}"
def nxt(y, m): return (y + 1, 1) if m == 12 else (y, m + 1)

def A_M0(t):
    r = M.get(t)
    if not r: return None
    return r["M0_med"] if (t >= "1980-02" and r["M0_med"] is not None) else r["M0_fim"]
def A_M1(t):
    r = M.get(t)
    if not r: return None
    if t >= "1980-02":
        v = r.get("M1_med_novo") if t >= "2002-01" else r["M1_med"]
        if v is not None: return v
    return r["M1_fim"] if r["M1_fim"] is not None else r["M1_novo"]
P = lambda t: M[t]["igpdi_idx"] if t in M else None

def inflacao_dez_dez(y):
    a, b = P(ym(y, 12)), P(ym(y - 1, 12))
    return a / b - 1 if a and b else None
def ipca_dez_dez(y):
    f = 1.0
    for m in range(1, 13):
        v = (M.get(ym(y, m)) or {}).get("ipca_pct_mes")
        if v is None: return None
        f *= 1 + v / 100
    return f - 1
def soma_mensal(A, y):
    s = 0.0
    for m in range(1, 13):
        y2, m2 = nxt(y, m); a, p0, p1 = A(ym(y, m)), P(ym(y, m)), P(ym(y2, m2))
        if None in (a, p0, p1): return None
        s += a * (p1 - p0) / p1
    return s
def soma_mensal_ipca(A, y):
    """Variante (c2): mesma formula de Cysne, mas com a taxa mensal do IPCA (SGS 433, desde 1980) no lugar do IGP-DI: A_t * r/(1+r), r = IPCA do mes t+1."""
    s = 0.0
    for m in range(1, 13):
        y2, m2 = nxt(y, m); a, r = A(ym(y, m)), (M.get(ym(y2, m2)) or {}).get("ipca_pct_mes")
        if a is None or r is None: return None
        s += a * (r / 100) / (1 + r / 100)
    return s
def media12(A, y):
    v = [A(ym(y, m)) for m in range(1, 13)]
    return None if None in v else sum(v) / 12
def dez(y): return (M.get(ym(y, 12)) or {}).get("M0_fim")

rows = []
for y in range(1947, 2026):
    N = PIB.get(y); N0 = PIB.get(y - 1); d1, d0 = dez(y), dez(y - 1)
    pi = inflacao_dez_dez(y); pi2 = ipca_dez_dez(y)
    r = {"ano": y, "infl_igpdi_pct": None if pi is None else 100 * pi}
    r["a_dM0_pib"] = 100 * (d1 - d0) / N if (N and d1 is not None and d0 is not None) else None
    m0 = media12(A_M0, y)
    r["b_anual_igpdi_pib"] = 100 * pi / (1 + pi) * m0 / N if (pi is not None and m0 is not None and N) else None
    r["b2_anual_ipca_pib"] = 100 * pi2 / (1 + pi2) * m0 / N if (pi2 is not None and m0 is not None and N) else None
    s0, s1 = soma_mensal(A_M0, y), soma_mensal(A_M1, y)
    r["c_II_mensal_pib"] = 100 * s0 / N if (s0 is not None and N) else None
    r["c_TIT_mensal_pib"] = 100 * s1 / N if (s1 is not None and N) else None
    s2, s3 = soma_mensal_ipca(A_M0, y), soma_mensal_ipca(A_M1, y)
    r["c2_II_ipca_pib"] = 100 * s2 / N if (s2 is not None and N) else None
    r["c2_TIT_ipca_pib"] = 100 * s3 / N if (s3 is not None and N) else None
    r["c_TI_mensal_pib"] = None if r["c_II_mensal_pib"] is None or r["c_TIT_mensal_pib"] is None else r["c_TIT_mensal_pib"] - r["c_II_mensal_pib"]
    if N and N0 and d0 is not None and d1 is not None:
        r["d1_ayres_seigniorage"] = 100 * (N - N0) / N * d0 / N0
        r["d2_ayres_base_real"] = 100 * (d1 / N - d0 / N0)
    else: r["d1_ayres_seigniorage"] = r["d2_ayres_base_real"] = None
    c = CY.get(y)
    r["cysne_infl"], r["cysne_II"], r["cysne_TI"], r["cysne_TIT"] = (c["inflacao_igpdi_pct"], c["II_pib_pct"], c["TI_pib_pct"], c["TIT_pib_pct"]) if c else (None,) * 4
    rows.append(r)
cols = list(rows[0])
with open(S / "senhoriagem_anual.csv", "w", newline="") as f:
    w = csv.DictWriter(f, cols); w.writeheader()
    for r in rows: w.writerow({k: ("" if v is None else round(v, 4)) for k, v in r.items()})

# --- reproducao da Tabela 1 de Cysne e Coimbra-Lisboa (1947-2003) ---
def cmp(a, b, anos):
    d = [(y, R[a] - R[b]) for R in rows for y in [R["ano"]] if y in anos and R[a] is not None and R[b] is not None]
    if not d: return None
    ab = [abs(x) for _, x in d]
    return {"n": len(d), "erro_abs_medio_pp": round(sum(ab) / len(ab), 3), "erro_abs_max_pp": round(max(ab), 3), "ano_max": max(d, key=lambda t: abs(t[1]))[0],
            "vies_medio_pp": round(sum(x for _, x in d) / len(d), 3),
            "corr": round(corr([R[a] for R in rows if R["ano"] in anos and R[a] is not None and R[b] is not None], [R[b] for R in rows if R["ano"] in anos and R[a] is not None and R[b] is not None]), 4)}
def corr(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
with open(S / "reproducao_cysne.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["serie_minha", "serie_cysne", "periodo", "n", "erro_abs_medio_pp", "erro_abs_max_pp", "ano_do_max", "vies_medio_pp", "correlacao"])
    for a, b in (("c_II_mensal_pib", "cysne_II"), ("c_TIT_mensal_pib", "cysne_TIT"), ("c_TI_mensal_pib", "cysne_TI"), ("b_anual_igpdi_pib", "cysne_II"), ("a_dM0_pib", "cysne_II"), ("infl_igpdi_pct", "cysne_infl")):
        for nome, anos in (("1947-2003", range(1947, 2004)), ("1947-1979", range(1947, 1980)), ("1980-2003", range(1980, 2004)), ("1980-1994", range(1980, 1995)), ("1995-2003", range(1995, 2004))):
            c = cmp(a, b, set(anos))
            if c: w.writerow([a, b, nome, c["n"], c["erro_abs_medio_pp"], c["erro_abs_max_pp"], c["ano_max"], c["vies_medio_pp"], c["corr"]])

# --- governos ---
# Datas de posse/saida: ⚠️ constantes minhas (conferir contra fontes/dados/historia/). Regra do mes: o mes pertence a quem ocupa a presidencia no dia 16.
GOV = [("Dutra", "1946-01-31", "1951-01-31"), ("Vargas+Cafe Filho+Carlos Luz+Nereu Ramos", "1951-01-31", "1956-01-31"), ("JK", "1956-01-31", "1961-01-31"),
       ("Janio+Jango", "1961-01-31", "1964-04-01"), ("Castelo Branco", "1964-04-15", "1967-03-15"), ("Costa e Silva+Junta", "1967-03-15", "1969-10-30"),
       ("Medici", "1969-10-30", "1974-03-15"), ("Geisel", "1974-03-15", "1979-03-15"), ("Figueiredo", "1979-03-15", "1985-03-15"),
       ("Sarney", "1985-03-15", "1990-03-15"), ("Collor", "1990-03-15", "1992-10-02"), ("Itamar", "1992-10-02", "1995-01-01"),
       ("FHC", "1995-01-01", "2003-01-01"), ("Lula 1-2", "2003-01-01", "2011-01-01"), ("Dilma (ate afastamento 12/05/2016)", "2011-01-01", "2016-05-12"),
       ("Temer (de 12/05/2016, interino)", "2016-05-12", "2019-01-01"), ("Bolsonaro", "2019-01-01", "2023-01-01"), ("Lula 3", "2023-01-01", "2027-01-01")]
GOV_ALT = [("Dilma (ate 31/08/2016)", "2011-01-01", "2016-08-31"), ("Temer (de 31/08/2016)", "2016-08-31", "2019-01-01")]
# Janelas do infografico (anos civis)
INFO = [("Ditadura 1967-1974 (info)", 1967, 1974), ("Itamar 1992-1994 (info)", 1992, 1994), ("FHC 1995-2002 (info)", 1995, 2002), ("Lula 2003-2010 (info)", 2003, 2010),
        ("Dilma 2011-2016 (info)", 2011, 2016), ("Temer 2016-2018 (info)", 2016, 2018), ("Bolsonaro 2019-2022 (info)", 2019, 2022), ("Lula 3 2023-2025 (info)", 2023, 2025),
        ("Pico 1980-1994", 1980, 1994), ("Pos-Real 1995-2003", 1995, 2003)]
def meses_do(ini, fim):
    a, b = datetime.date.fromisoformat(ini), datetime.date.fromisoformat(fim)
    res = []
    y, m = a.year, a.month
    while True:
        meio = datetime.date(y, m, 16)
        if a <= meio < b: res.append((y, m))
        if (y, m) >= (b.year, b.month): break
        y, m = nxt(y, m)
    return res
AR = {r["ano"]: r for r in rows}
vars_ = ["a_dM0_pib", "b_anual_igpdi_pib", "c_II_mensal_pib", "c_TIT_mensal_pib", "c2_II_ipca_pib", "c2_TIT_ipca_pib", "d1_ayres_seigniorage", "infl_igpdi_pct"]
def media_pond(ms, v):
    peso = collections.Counter(y for y, _ in ms)
    num = den = 0.0
    for y, w in peso.items():
        x = AR.get(y, {}).get(v)
        if x is None: continue
        num += w * x; den += w
    return num / den if den else None
with open(S / "senhoriagem_janelas.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["janela", "tipo", "meses", "primeiro_ano_dados", ] + vars_)
    for nome, i, fi in GOV + GOV_ALT:
        ms = [(y, m) for y, m in meses_do(i, fi) if y <= 2025]
        if not ms: continue
        w.writerow([nome, "mandato posse-saida (media de anos ponderada por meses)", len(ms), min(y for y, _ in ms)] + [("" if (x := media_pond(ms, v)) is None else round(x, 3)) for v in vars_])
    for nome, a, b in INFO:
        ms = [(y, m) for y in range(a, b + 1) for m in range(1, 13)]
        w.writerow([nome, "anos civis", len(ms), a] + [("" if (x := media_pond(ms, v)) is None else round(x, 3)) for v in vars_])


# --- validacao contra Ayres et al. (2018/19), Tabela 1 (medias por subperiodo, % do PIB): linhas (3) base monetaria real e (4) seigniorage ---
AYRES = [((1960, 1964), -0.4, 4.1), ((1965, 1972), -0.2, 1.9), ((1973, 1980), -0.2, 2.4), ((1981, 1994), -0.1, 3.2), ((1995, 2002), 0.1, 0.4), ((2003, 2011), 0.1, 0.4), ((2012, 2016), -0.1, 0.3)]
with open(S / "validacao_ayres.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["subperiodo", "ayres_base_real", "ayres_seigniorage", "ayres_soma", "meu_d2_base_real", "meu_d1_seigniorage", "minha_soma_(a)", "meu_c_II_mensal", "meu_c_TIT_mensal"])
    for (a, b), r3, r4 in AYRES:
        mm = lambda k: sum(AR[y][k] for y in range(a, b + 1)) / (b - a + 1)
        w.writerow([f"{a}-{b}", r3, r4, round(r3 + r4, 1), round(mm("d2_ayres_base_real"), 2), round(mm("d1_ayres_seigniorage"), 2), round(mm("a_dM0_pib"), 2), round(mm("c_II_mensal_pib"), 2), round(mm("c_TIT_mensal_pib"), 2)])
print("validacao Ayres:"); print(open(S / "validacao_ayres.csv").read())

# --- resumo para o terminal ---
print("reproducao Cysne:"); [print(" ", l.strip()) for l in open(S / "reproducao_cysne.csv")]
