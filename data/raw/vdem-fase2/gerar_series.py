#!/usr/bin/env python3
"""Extrai o Brasil dos RData do V-Dem (bruto/) para series/ (CSV longo) e confere contra OWID e entre versoes.
Uso: venv com `rdata` e `pandas`:  python -I gerar_series.py"""
import csv, math, warnings, sys
from pathlib import Path
import rdata
warnings.filterwarnings("ignore")
D = Path(__file__).resolve().parent
B = D / "bruto"

ITENS = {  # variavel: (rotulo, definicao, unidade)
    "v2x_libdem": ("Democracia liberal", "To what extent is the ideal of liberal democracy achieved? (V-Dem v2x_libdem; indice 0-1, mais alto = mais democratico)", "indice 0-1"),
    "v2x_corr": ("Corrupcao politica", "How pervasive is political corruption? (V-Dem v2x_corr; indice 0-1, mais alto = MAIS corrupto)", "indice 0-1"),
    "v2xlg_legcon": ("Restricoes legislativas ao Executivo", "Capacidade do legislativo e de orgaos de controle de questionar, investigar e fiscalizar o Executivo (V-Dem v2xlg_legcon; 0-1, mais alto = mais restricao)", "indice 0-1"),
    "v2x_jucon": ("Restricoes judiciais ao Executivo", "Em que medida o Executivo respeita a Constituicao e as decisoes judiciais e o Judiciario age com independencia (V-Dem v2x_jucon; 0-1, mais alto = mais restricao)", "indice 0-1"),
    "v2clstown": ("Propriedade estatal da economia (escala do modelo de medicao)", "Does the state own or directly control important sectors of the economy? (V-Dem v2clstown; saida intervalar do modelo de medicao; MAIS ALTO = MENOS propriedade estatal; 0 = quase todo o capital e do Estado, 4 = muito pouco)", "escala intervalar do modelo (aprox. 0-4)"),
    "v2clstown_osp": ("Propriedade estatal da economia (escala original)", "v2clstown_osp: estimativa na escala original ordinal 0-4 (mais alto = MENOS propriedade estatal)", "escala original 0-4"),
    "v2x_polyarchy": ("Democracia eleitoral (bonus, conferencia com OWID)", "v2x_polyarchy, Electoral democracy index (0-1, mais alto = mais democratico)", "indice 0-1"),
}
SUF = {"": "estimativa pontual", "_codelow": "limite inferior (codelow, limite inferior da incerteza publicado pelo V-Dem)", "_codehigh": "limite superior (codehigh, limite superior da incerteza publicado pelo V-Dem)"}

def carrega(arq):
    df = rdata.read_rda(B / arq)["vdem"]
    b = df[df.country_text_id == "BRA"].copy()
    b["year"] = b["year"].astype(int)
    return b.set_index("year")

def val(b, v, ano):
    if v not in b.columns or ano not in b.index: return None
    x = b.at[ano, v]
    return None if x is None or (isinstance(x, float) and math.isnan(x)) or str(x) == "<NA>" else float(x)

def main():
    v16 = carrega("vdemdata_v16_vdem.RData")
    v15 = carrega("vdemdata_V15_vdem.RData")
    v12 = carrega("vdemdata_V12_vdem.RData")
    linhas = []
    for var, (rot, defn, un) in ITENS.items():
        for suf, sdesc in SUF.items():
            col = var + suf
            if col not in v16.columns: continue
            for ano in sorted(v16.index):
                x = val(v16, col, ano)
                if x is None: continue
                nota = "v2clstown_osp: sem estimativa de incerteza proprio nesta coluna alem de codelow/codehigh" if var == "v2clstown_osp" and suf == "" else ""
                linhas.append([col, "V-Dem Country-Year Full+Others v16 (pacote oficial vdemdata, tag V16)", f"{rot}: {sdesc}. {defn}", ano, "", repr(x), un, nota, "V-Dem v16, publicada em 2026-03 (commit 2026-03-17)"])
    out = D / "series" / "vdem_brasil_v16.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["indicador","fonte","definicao_linha","ano","mes_ou_trimestre","valor","unidade","nota","vintage"]); w.writerows(linhas)
    print("linhas", len(linhas), out)
    # tabela de valores-chave
    anos = [1994, 2002, 2010, 2016, 2018, 2022]
    print("\nVALORES v16 (estimativa [low, high])")
    for var in ITENS:
        ult = max(a for a in v16.index if val(v16, var, a) is not None)
        cols = []
        for a in anos + [ult]:
            p, lo, hi = (val(v16, var + s, a) for s in SUF)
            cols.append(f"{a}: {p} [{lo}, {hi}]")
        print(var, "| ult", ult, "|", " | ".join(cols))
    # cobertura
    print("\nCOBERTURA")
    for var in ITENS:
        anosv = [a for a in v16.index if val(v16, var, a) is not None]
        print(var, min(anosv), max(anosv), len(anosv), "faltando entre extremos:", [a for a in range(min(anosv), max(anosv)+1) if a not in anosv][:10])
    # vintage
    print("\nVINTAGE (v12, v15, v16)")
    vint = []
    for var in ["v2x_libdem","v2x_corr","v2xlg_legcon","v2x_jucon","v2clstown","v2clstown_osp","v2x_polyarchy"]:
        for a in anos:
            vals = [val(b, var, a) for b in (v12, v15, v16)]
            vint.append([var, a] + vals)
            print(var, a, vals)
    # maior revisao v15->v16 em 1960+
    print("\nMAIOR |v16-v15| 1960+ por item")
    for var in ["v2x_libdem","v2x_corr","v2xlg_legcon","v2x_jucon","v2clstown","v2x_polyarchy"]:
        d = [(abs(val(v16,var,a)-val(v15,var,a)), a) for a in v16.index if a >= 1960 and val(v16,var,a) is not None and val(v15,var,a) is not None]
        print(var, max(d), "mediana", sorted(x for x,_ in d)[len(d)//2])
        d12 = [(abs(val(v16,var,a)-val(v12,var,a)), a) for a in v16.index if 1960 <= a <= 2020 and val(v16,var,a) is not None and val(v12,var,a) is not None]
        print("   v12->v16 (1960-2020)", max(d12), "mediana", sorted(x for x,_ in d12)[len(d12)//2])
    # OWID
    print("\nOWID x vdemdata v16")
    mapa = {"v2x_libdem":"libdem","v2x_corr":"corr","v2xlg_legcon":"legcon","v2x_jucon":"jucon","v2x_polyarchy":"polyarchy"}
    for var, k in mapa.items():
        rows = list(csv.DictReader((B / f"owid_{k}_BRA.csv").open(encoding="utf-8")))
        bra = {int(r["year"]): float(r[[c for c in r if c.endswith("estimate_best")][0]]) for r in rows if r["code"] == "BRA"}
        dif = [(a, bra[a], val(v16, var, a)) for a in bra if abs(bra[a] - (val(v16, var, a) or 1e9)) > 1e-9]
        print(var, "anos OWID", min(bra), max(bra), len(bra), "divergentes", len(dif), dif[:5])
main()
