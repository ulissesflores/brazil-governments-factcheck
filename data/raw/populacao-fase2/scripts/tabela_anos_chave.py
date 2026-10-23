#!/usr/bin/env python3
"""Imprime a tabela de anos-chave (markdown) a partir de series/ e derivado/."""
import csv, glob
P = "/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/populacao-fase2/"
D = {}
for f in glob.glob(P + "series/*.csv") + glob.glob(P + "derivado/wdi_*.csv"):
    for r in csv.DictReader(open(f, encoding="utf-8")):
        if r["mes_ou_trimestre"] == "":
            D.setdefault(r["indicador"], {})[int(r["ano"])] = r["valor"]
ROWS = [("SIM obitos (ocorrencia)", "obitos_total_por_ocorrencia", 2025), ("SINASC nascidos (ocorrencia)", "nascidos_vivos_por_ocorrencia", 2025),
        ("IBGE RC nascidos registrados no ano", "nascidos_vivos_registrados_no_ano", 2024), ("IBGE RC nascidos ocorridos no ano", "nascidos_vivos_ocorridos_no_ano", 2024),
        ("IBGE RC obitos registrados no ano", "obitos_registrados_no_ano", 2024), ("IBGE RC obitos ocorridos (1984-2002: ocorr.+reg. no ano)", None, 2024),
        ("WDI nascimentos estimados", "nascimentos_estimados_wdi", 2024), ("WDI obitos estimados", "obitos_estimados_wdi", 2024),
        ("ONU WPP nascimentos", "nascimentos_wpp", 2025), ("ONU WPP obitos", "obitos_wpp", 2025)]
YRS = [1964, 1970, 1980, 1990, 1994, 2000, 2010, 2016, 2020, 2021, 2024]
def get(ind, a):
    if ind is None:
        return (D.get("obitos_ocorridos_e_registrados_no_ano", {}).get(a) or D.get("obitos_ocorridos_no_ano", {}).get(a))
    if ind in ("nascidos_vivos_registrados_no_ano", "obitos_registrados_no_ano"):
        return D.get(ind + "_lugar_registro", {}).get(a) or D.get(ind, {}).get(a)
    return D.get(ind, {}).get(a)
fmt = lambda v: "-" if v is None else f"{int(float(v)):,}".replace(",", ".")
print("| Base | " + " | ".join(map(str, YRS)) + " | ultimo ano |")
print("|---|" + "---|" * (len(YRS) + 1))
for nome, ind, _ in ROWS:
    keys = [ind] if ind else ["obitos_ocorridos_no_ano"]
    anos = sorted(set(a for k in ([ind] if ind else ["obitos_ocorridos_e_registrados_no_ano", "obitos_ocorridos_no_ano"]) for a in D.get(k, {}) ) )
    if ind in ("nascidos_vivos_registrados_no_ano", "obitos_registrados_no_ano"):
        anos = sorted(set(anos) | set(D.get(ind + "_lugar_registro", {})))
    last = [a for a in anos if a <= {"obitos_total_por_ocorrencia": 2025, "nascidos_vivos_por_ocorrencia": 2025, "nascimentos_wpp": 2025, "obitos_wpp": 2025}.get(ind, 2024)]
    la = max(last)
    print(f"| {nome} | " + " | ".join(fmt(get(ind, a)) for a in YRS) + f" | {la}: {fmt(get(ind, la))} |")
