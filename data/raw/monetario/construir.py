# Constroi as series mensais e anuais a partir do BRUTO (bruto/*.json). SEM REDE. Rodar: python3 -I construir.py
# Saidas em saida/: mensal.csv, anual.csv, fatores_de_conversao.csv
# Unidade de saida: R$ milhoes na moeda de hoje (real). O SGS/BCB publica niveis na moeda da epoca ("milhares de unidades
# monetarias correntes"); aqui dividimos pelo fator acumulado dos cortes de zeros (BCB Museu de Valores, ver RESULTADO.md).
import csv, json, pathlib, math
AQUI = pathlib.Path(__file__).resolve().parent
BR = AQUI / "bruto"; OUT = AQUI / "saida"; OUT.mkdir(exist_ok=True)

def bcb(c):
    """SGS -> {'AAAA-MM': float} (ignora nulos)."""
    return {r["data"][6:] + "-" + r["data"][3:5]: float(r["valor"]) for r in json.load(open(BR / f"bcb_sgs_{c}.json")) if r["valor"] not in (None, "")}
def ipea(c, n=7):
    return {r["VALDATA"][:n]: r["VALVALOR"] for r in json.load(open(BR / f"ipea_{c}.json"))["value"] if r["VALVALOR"] is not None}

# Cortes de zeros (BCB Museu de Valores): 13.2.1967 (/1000), 28.2.1986 (/1000), 16.1.1989 (/1000), 1.8.1993 (/1000), 1.7.1994 (/2750).
# Primeiro mes publicado na unidade nova (verificado: razao SGS 1788 / Ipeadata BM12_M0N12 e potencia exata de 10 ou 2750 em cada trecho).
CORTES = [("1967-02", 1000), ("1986-03", 1000), ("1989-01", 1000), ("1993-08", 1000), ("1994-07", 2750)]
def fator(ym):
    """Divisor para levar saldo na moeda da epoca (em milhares) a R$ milhoes de hoje: raw/1000/fator(ym)."""
    f = 1.0
    for m, k in CORTES:
        if ym < m: f *= k
    return f
def conv(d):  # SGS (milhares de moeda da epoca) -> R$ milhoes
    return {m: v / 1e3 / fator(m) for m, v in d.items()}

# --- series monetarias (SGS) ---
M0 = conv(bcb(1788)); M0med = conv(bcb(1785)); PME = conv(bcb(1786)); RB = conv(bcb(1787))
M1 = conv(bcb(1827)); M1med = conv(bcb(1824))
BA = conv(bcb(1833))                      # base ampliada, desde 1994-08
# regime "2001" (BCB reformulou em jul/2001, series refeitas desde jul/1988, descontinuadas em jun/2018)
M2a = conv(bcb(1837)); M3a = conv(bcb(1840)); M4a = conv(bcb(1843))
# regime "2018" ("Novo"; historia revista desde dez/2001)
M1n = conv(bcb(27791)); M1nmed = conv(bcb(27788)); M2n = conv(bcb(27810)); M3n = conv(bcb(27813)); M4n = conv(bcb(27815))
# precos
igp_idx = ipea("IGP12_IGPDI12")          # IGP-DI geral, indice (ago/1994 = 100), FGV via Ipeadata
ipca = bcb(433)                           # IPCA mensal, % a.m. (desde 1980)
# PIB nominal anual, R$ milhoes (IBGE SCN via Ipeadata, ja em moeda de hoje)
PIB = {int(k): v for k, v in ipea("SCN10_PIBN10", 4).items()}

meses = sorted(set(M0) | set(M1) | set(M2a) | set(M2n) | set(igp_idx))
with open(OUT / "mensal.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ym", "igpdi_idx", "ipca_pct_mes", "M0_fim", "M0_med", "PME_fim", "reservas_banc_fim", "base_ampliada_fim", "M1_fim", "M1_med",
                                    "M1_novo", "M1_med_novo", "M2_reg2001", "M3_reg2001", "M4_reg2001", "M2_novo", "M3_novo", "M4_novo"])
    for m in meses:
        g = lambda d: "" if m not in d else repr(d[m])
        w.writerow([m, g(igp_idx), g(ipca), g(M0), g(M0med), g(PME), g(RB), g(BA), g(M1), g(M1med), g(M1n), g(M1nmed), g(M2a), g(M3a), g(M4a), g(M2n), g(M3n), g(M4n)])
with open(OUT / "fatores_de_conversao.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["a_partir_de", "divisor_adicional"]); [w.writerow(c) for c in CORTES]
print("mensal.csv:", len(meses), "meses;", meses[0], "->", meses[-1])

# --- anual: dezembro e media de 12 meses, razoes ao PIB ---
def dez(d, y): return d.get(f"{y}-12")
def med(d, y):
    v = [d[f"{y}-{m:02d}"] for m in range(1, 13) if f"{y}-{m:02d}" in d]
    return sum(v) / len(v) if len(v) == 12 else None
# papel-moeda emitido antes de 1980: Ipeadata HIST_PME (anual, dezembro). Unidade inferida: "mil NCr$" (= milhoes de Cr$ antigos); conferido por
# (i) igualdade exata de 1980 com o SGS 1786 de dez/1980 e (ii) razao PME/M0 suave (0,5-0,8) em 1947-1980. Ver RESULTADO.md (⚠️).
PMEH = {int(k): v / 1e3 / 2.75e12 for k, v in ipea("HIST_PME", 4).items() if 1946 <= int(k) <= 1979}
linhas = []
for y in range(1946, 2026):
    p = PIB.get(y)
    r = {"ano": y, "PIB_RSmi": p}
    for nome, d in (("M0", M0), ("M1", M1), ("PME", PME), ("BA", BA), ("M2_2001", M2a), ("M3_2001", M3a), ("M4_2001", M4a),
                    ("M1_novo", M1n), ("M2_novo", M2n), ("M3_novo", M3n), ("M4_novo", M4n)):
        a, b = dez(d, y), med(d, y)
        r[nome + "_dez"] = a; r[nome + "_dez_pib_pct"] = (100 * a / p) if (a is not None and p) else None
        r[nome + "_med12_pib_pct"] = (100 * b / p) if (b is not None and p) else None
    if y in PMEH:
        r["PME_dez"] = PMEH[y]; r["PME_dez_pib_pct"] = (100 * PMEH[y] / p) if p else None
    linhas.append(r)
cols = list(linhas[0])
with open(OUT / "anual.csv", "w", newline="") as f:
    w = csv.DictWriter(f, cols); w.writeheader()
    for r in linhas: w.writerow({k: ("" if v is None else v) for k, v in r.items()})
print("anual.csv:", len(linhas), "anos")
