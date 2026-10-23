# Extras fiscal-monetarios por ano e por janela de governo (anos civis). LE so bruto/ e saida/anual.csv. SEM REDE. Rodar: python3 -I extras.py
# Convencoes: cambio = R$/US$ comercial venda fim de periodo, em R$ de hoje (Ipeadata BM_ERVF, origem BCB; ja convertido dos cortes de zeros).
#  Selic anual = produto das taxas Over/Selic mensais acumuladas (Ipeadata BM12_TJOVER12, % a.m., desde 1974; antes de 1986 a comparabilidade da taxa "over" nao foi verificada;
#  de outro mercado - ver RESULTADO.md). Juro real ex-post = (1+Selic)/(1+inflacao)-1 (inflacao: IPCA SGS 433 desde 1980; IGP-DI antes).
#  Resultado primario: o BCB publica como NFSP (necessidade de financiamento): NEGATIVO = SUPERAVIT. Aqui: primario = -NFSP (positivo = superavit).
import csv, json, pathlib, collections
AQUI = pathlib.Path(__file__).resolve().parent; BR = AQUI / "bruto"; S = AQUI / "saida"

def ipea(c, n=7): return {r["VALDATA"][:n]: r["VALVALOR"] for r in json.load(open(BR / f"ipea_{c}.json"))["value"] if r["VALVALOR"] is not None}
def bcb(c): return {r["data"][6:] + "-" + r["data"][3:5]: float(r["valor"]) for r in json.load(open(BR / f"bcb_sgs_{c}.json")) if r["valor"] not in (None, "")}
PIB = {int(r["ano"]): float(r["PIB_RSmi"]) for r in csv.DictReader(open(S / "anual.csv")) if r["PIB_RSmi"]}
mensal = {r["ym"]: r for r in csv.DictReader(open(S / "mensal.csv"))}

cambio = {int(k): v for k, v in ipea("BM_ERVF", 4).items()}
over = ipea("BM12_TJOVER12"); ipca = bcb(433)
dlsp_gfbc = {int(k): v for k, v in ipea("BM_DTGFN", 4).items()}          # R$ milhoes, DLSP governo federal + Banco Central (inclui base monetaria como passivo)
dlsp_cons = bcb(4513); dbgg_old = bcb(4537); dbgg_new = bcb(13762); dlgg = bcb(4536)
nfsp_gfbc = ipea("BM12_NFGFPYS12"); nfsp_cons = bcb(5793)                 # % PIB, fluxo acumulado em 12 meses, sem desvalorizacao cambial
reservas = {int(k): v for k, v in ipea("BM_RES", 4).items()}
igp = {k: float(v["igpdi_idx"]) for k, v in mensal.items() if v["igpdi_idx"]}

def anual_acum_mensal(d, y):  # produto de (1+x/100) dos 12 meses
    f = 1.0
    for m in range(1, 13):
        v = d.get(f"{y}-{m:02d}")
        if v is None: return None
        f *= 1 + v / 100
    return 100 * (f - 1)
def igp_ano(y):
    a, b = igp.get(f"{y}-12"), igp.get(f"{y-1}-12"); return 100 * (a / b - 1) if a and b else None

rows = []
for y in range(1947, 2026):
    r = {"ano": y}
    r["cambio_fim_RS_por_USD"] = cambio.get(y)
    r["cambio_var_pct"] = 100 * (cambio[y] / cambio[y - 1] - 1) if y in cambio and y - 1 in cambio else None
    r["selic_over_ano_pct"] = anual_acum_mensal(over, y)
    r["ipca_ano_pct"] = anual_acum_mensal(ipca, y)
    r["igpdi_ano_pct"] = igp_ano(y)
    for nome, infl in (("ipca", r["ipca_ano_pct"]), ("igpdi", r["igpdi_ano_pct"])):
        s = r["selic_over_ano_pct"]
        r[f"juro_real_{nome}_pct"] = 100 * ((1 + s / 100) / (1 + infl / 100) - 1) if (s is not None and infl is not None) else None
    r["dlsp_gf_bc_pib_pct"] = 100 * dlsp_gfbc[y] / PIB[y] if y in dlsp_gfbc and y in PIB else None
    r["dlsp_consolidado_pib_pct_dez"] = dlsp_cons.get(f"{y}-12")
    r["dlgg_pib_pct_dez"] = dlgg.get(f"{y}-12")
    r["dbgg_pib_pct_dez_metodo_ate_2007"] = dbgg_old.get(f"{y}-12")
    r["dbgg_pib_pct_dez_metodo_desde_2008"] = dbgg_new.get(f"{y}-12")
    v = nfsp_gfbc.get(f"{y}-12"); r["primario_gf_bc_pib_pct"] = None if v is None else -v
    v = nfsp_cons.get(f"{y}-12"); r["primario_consolidado_pib_pct"] = None if v is None else -v
    r["reservas_USDmi_dez"] = reservas.get(y)
    rows.append(r)
cols = list(rows[0])
with open(S / "extras_anual.csv", "w", newline="") as f:
    w = csv.DictWriter(f, cols); w.writeheader()
    for r in rows: w.writerow({k: ("" if v is None else (float(f"{v:.6g}") if isinstance(v, float) else v)) for k, v in r.items()})

# janelas (anos civis): estoque = dez do ano anterior ao inicio -> dez do ultimo ano; fluxo = media dos anos
JAN = [("Medici 1970-1973", 1970, 1973), ("Geisel 1974-1978", 1974, 1978), ("Figueiredo 1979-1984", 1979, 1984), ("Sarney 1985-1989", 1985, 1989),
       ("Collor 1990-1992", 1990, 1992), ("Itamar 1992-1994 (info)", 1992, 1994), ("FHC 1995-2002", 1995, 2002), ("Lula 2003-2010", 2003, 2010),
       ("Dilma 2011-2016 (info)", 2011, 2016), ("Temer 2016-2018 (info)", 2016, 2018), ("Bolsonaro 2019-2022", 2019, 2022), ("Lula 3 2023-2025", 2023, 2025)]
AR = {r["ano"]: r for r in rows}
def mean(v):
    v = [x for x in v if x is not None]; return (sum(v) / len(v), len(v)) if v else (None, 0)
def stock(k, a, b):
    i, f = AR.get(a - 1, {}).get(k), AR.get(b, {}).get(k)
    return i, f
out = []
for nome, a, b in JAN:
    r = {"janela": nome}
    ci, cf = stock("cambio_fim_RS_por_USD", a, b); r["cambio_ini"], r["cambio_fim"] = ci, cf
    r["cambio_fator"] = cf / ci if ci and cf else None
    for k, lab in (("selic_over_ano_pct", "selic_media"), ("juro_real_ipca_pct", "juro_real_ipca_medio"), ("juro_real_igpdi_pct", "juro_real_igpdi_medio"),
                   ("primario_gf_bc_pib_pct", "primario_gfbc_medio"), ("primario_consolidado_pib_pct", "primario_cons_medio")):
        m, n = mean([AR[y][k] for y in range(a, b + 1)]); r[lab] = m; r[lab + "_n_anos"] = n
    for k, lab in (("dlsp_gf_bc_pib_pct", "dlsp_gfbc_pib"), ("dlsp_consolidado_pib_pct_dez", "dlsp_cons_pib"), ("reservas_USDmi_dez", "reservas_USDmi")):
        i, f = stock(k, a, b); r[lab + "_ini"], r[lab + "_fim"] = i, f
    i, f = stock("dbgg_pib_pct_dez_metodo_ate_2007", a, b); r["dbgg_ate2007_ini"], r["dbgg_ate2007_fim"] = i, f
    i, f = stock("dbgg_pib_pct_dez_metodo_desde_2008", a, b); r["dbgg_desde2008_ini"], r["dbgg_desde2008_fim"] = i, f
    out.append(r)
c2 = list(out[0])
with open(S / "extras_janelas.csv", "w", newline="") as f:
    w = csv.DictWriter(f, c2); w.writeheader()
    for r in out: w.writerow({k: ("" if v is None else (float(f"{v:.6g}") if isinstance(v, float) else v)) for k, v in r.items()})
print("extras ok;", len(rows), "anos;", len(out), "janelas")
