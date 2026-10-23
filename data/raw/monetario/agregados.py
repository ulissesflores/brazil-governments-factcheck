# Cobertura, identidades, quebras de regime e auditoria do Ipeadata para M0/M1/M2/M3/M4. LE so bruto/ e saida/. SEM REDE.
# Rodar: python3 -I construir.py && python3 -I agregados.py
import csv, json, pathlib, statistics as st, math
AQUI = pathlib.Path(__file__).resolve().parent; BR = AQUI / "bruto"; S = AQUI / "saida"

def bcb(c): return {r["data"][6:] + "-" + r["data"][3:5]: float(r["valor"]) for r in json.load(open(BR / f"bcb_sgs_{c}.json")) if r["valor"] not in (None, "")}
def ipea(c): return {r["VALDATA"][:7]: r["VALVALOR"] for r in json.load(open(BR / f"ipea_{c}.json"))["value"] if r["VALVALOR"] is not None}
def ckan_nome(c):
    try:
        j = json.load(open(BR / f"ckan_{c}.json"))["result"]
        if "results" not in j: return j["title"]          # formato package_show (primeira versao do baixador)
        return next(r["title"] for r in j["results"] if str(r.get("codigo_sgs")) == str(c))
    except Exception: return None

# --- 1. cobertura ---
# (codigo, papel, nome por inferencia se nao ha pagina no catalogo)
SERIES = [(1788, "M0 base restrita fim", None), (1783, "papel-moeda em circulacao media", None), (1785, "M0 base restrita media", None), (1786, "papel-moeda em circulacao fim", None), (1787, "reservas bancarias fim", None),
          (1833, "base ampliada fim", None), (1827, "M1 fim (conceito antigo)", "M1 = 1825 + 1826"), (1824, "M1 media (antigo)", "M1 media = 1822 + 1823"),
          (1835, "poupanca fim", None), (1839, "compromissadas Selic fim", None),
          (1837, "M2 (reg. 2001)", "M2 = M1 + 1835 + 1836 (+ dep. especiais remunerados 1991-2000)"), (1840, "M3 (reg. 2001)", "M3 = M2 + 1838 + 1839"),
          (1843, "M4 (reg. 2001)", "M4 = M3 + 1841 + 1842"), (27791, "M1 fim Novo", None), (27810, "M2 fim Novo", None), (27813, "M3 fim Novo", None), (27815, "M4 fim Novo", None),
          (27788, "M1 media Novo", None)]
with open(S / "agregados_cobertura.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["sgs", "papel", "nome_no_catalogo_CKAN_BCB", "nome_por_inferencia_numerica", "primeiro_mes", "ultimo_mes", "n_meses"])
    for c, papel, inf in SERIES:
        d = bcb(c); k = sorted(d)
        w.writerow([c, papel, ckan_nome(c) or "", inf or "", k[0], k[-1], len(k)])

# --- 2. identidades dos codigos antigos (prova numerica) ---
def ident(alvo, partes):
    A = bcb(alvo); P = [bcb(p) for p in partes]
    ks = [m for m in sorted(A) if all(m in p for p in P)]
    ok = [m for m in ks if abs(sum(p[m] for p in P) - A[m]) / abs(A[m]) < 1e-4 if A[m]]
    return len(ks), len(ok), (ks[0] if ks else ""), (ks[-1] if ks else "")
with open(S / "agregados_identidades.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["identidade", "meses_testados", "meses_com_diferenca_menor_que_0_01pct", "de", "ate"])
    for nome, alvo, partes in (("M1 fim = 1825+1826", 1827, (1825, 1826)), ("M1 media = 1822+1823", 1824, (1822, 1823)), ("M2 = 1827+1835+1836", 1837, (1827, 1835, 1836)),
                               ("M3 = 1837+1838+1839", 1840, (1837, 1838, 1839)), ("M4 = 1840+1841+1842", 1843, (1840, 1841, 1842))):
        w.writerow([nome] + list(ident(alvo, partes)))

# --- 3. tamanho da quebra de 2018: mesmas datas, conceito 2001 (antigo) x conceito 2018 (Novo) ---
PAR = (("M1", 1827, 27791), ("M2", 1837, 27810), ("M3", 1840, 27813), ("M4", 1843, 27815))
with open(S / "agregados_quebra_2018.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["agregado", "razao_novo_sobre_antigo_dez2001", "dez2005", "dez2010", "dez2015", "dez2017 (NT48: M1 +5%, M3 -0,4%, M4 -6%)", "jun2018", "minimo", "maximo", "n_meses"])
    for nome, a, n in PAR:
        A, N = bcb(a), bcb(n)
        # 1827 esta em milhares da moeda da epoca; apos jul/1994 a unidade e o real: comparar so de 2001 em diante
        ks = [m for m in sorted(set(A) & set(N)) if m >= "2001-12"]
        r = {m: N[m] / A[m] for m in ks}
        w.writerow([nome] + [round(r.get(m, float("nan")), 4) for m in ("2001-12", "2005-12", "2010-12", "2015-12", "2017-12", "2018-06")] + [round(min(r.values()), 4), round(max(r.values()), 4), len(r)])

# --- 4. auditoria do Ipeadata contra o BCB ---
rows = []
i2 = ipea("BM12_M2NCN12"); n2 = bcb(27810); dv = bcb(27790)
ks = [m for m in sorted(i2) if m >= "2001-12" and m in n2 and m in dv]
eq_m2 = [m for m in ks if abs(i2[m] * 1e3 - n2[m]) / n2[m] < 1e-4]; eq_dv = [m for m in ks if abs(i2[m] * 1e3 - dv[m]) / dv[m] < 1e-4]
rows.append(["Ipeadata BM12_M2NCN12 (rotulada M2) vs BCB 27810 (M2 Novo)", len(ks), len(eq_m2), eq_m2[0] if eq_m2 else "", eq_m2[-1] if eq_m2 else ""])
rows.append(["Ipeadata BM12_M2NCN12 (rotulada M2) vs BCB 27790 (depositos a vista Novo)", len(ks), len(eq_dv), eq_dv[0] if eq_dv else "", eq_dv[-1] if eq_dv else ""])
for c, s, nome in (("BM12_M3NCN12", 27813, "M3"), ("BM12_M4NCN12", 27815, "M4"), ("BM12_M1N12", 27791, "M1 fim"), ("BM12_M1N12", 27788, "M1 media")):
    I, B = ipea(c), bcb(s); ks = [m for m in sorted(I) if m >= "2001-12" and m in B]
    eq = [m for m in ks if abs(I[m] * 1e3 - B[m]) / B[m] < 1e-4]
    rows.append([f"Ipeadata {c} (rotulada {nome.split()[0]} fim) vs BCB {s} ({nome} Novo)", len(ks), len(eq), eq[0] if eq else "", eq[-1] if eq else ""])
with open(S / "agregados_ipea_auditoria.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["comparacao", "meses_comparados", "meses_iguais_(<0,01%)", "primeiro_igual", "ultimo_igual"])
    for r in rows: w.writerow(r)

# --- 5. M/PIB anual por regime (media dos 12 saldos / PIB e saldo de dezembro / PIB) ja em anual.csv; resumo por governo (anos civis) ---
A = {int(r["ano"]): r for r in csv.DictReader(open(S / "anual.csv"))}
JAN = [("Ditadura 1967-1974 (info)", 1967, 1974), ("Geisel 1974-1978", 1974, 1978), ("Figueiredo 1979-1984", 1979, 1984), ("Sarney 1985-1989", 1985, 1989), ("Collor 1990-1992", 1990, 1992),
       ("Itamar 1992-1994 (info)", 1992, 1994), ("FHC 1995-2002 (info)", 1995, 2002), ("Lula 2003-2010 (info)", 2003, 2010), ("Dilma 2011-2016 (info)", 2011, 2016),
       ("Temer 2016-2018 (info)", 2016, 2018), ("Bolsonaro 2019-2022 (info)", 2019, 2022), ("Lula 3 2023-2025 (info)", 2023, 2025)]
CAMPOS = [("M0", "M0_med12_pib_pct"), ("M1", "M1_med12_pib_pct"), ("M1novo", "M1_novo_med12_pib_pct"), ("M2_2001", "M2_2001_med12_pib_pct"), ("M3_2001", "M3_2001_med12_pib_pct"), ("M4_2001", "M4_2001_med12_pib_pct"),
          ("M2_novo", "M2_novo_med12_pib_pct"), ("M3_novo", "M3_novo_med12_pib_pct"), ("M4_novo", "M4_novo_med12_pib_pct")]
def mm(k, a, b):
    v = [float(A[y][k]) for y in range(a, b + 1) if y in A and A[y][k] != ""]
    return (round(sum(v) / len(v), 2), len(v)) if v else ("", 0)
with open(S / "agregados_governos.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["janela"] + [x for n, _ in CAMPOS for x in (n + "_media_pct_PIB", n + "_anos")])
    for nome, a, b in JAN:
        w.writerow([nome] + [x for _, k in CAMPOS for x in mm(k, a, b)])
for fn in ("agregados_cobertura", "agregados_identidades", "agregados_quebra_2018", "agregados_ipea_auditoria"):
    print("##", fn); print(open(S / (fn + ".csv")).read())
