#!/usr/bin/env python3
"""Imprime (markdown) os valores de 1994, 2002, 2010, 2016, 2018, 2022 e do ultimo ano por indicador e por linha (base)."""
import csv
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ITENS = ["ind_transf_sobre_pib_mercado_pct", "ind_transf_sobre_pib_basico_pct", "ind_transf_pib_publicado_ipeadata_pct",
         "consumo_governo_sobre_pib_mercado_pct", "abertura_comercial_sobre_pib_mercado_pct", "internet_domicilios_pct"]
ANOS = [1994, 2002, 2010, 2016, 2018, 2022]
d = {}
for r in csv.DictReader(open(AQUI / "series" / "ibge_fase2_longo.csv", encoding="utf-8")):
    if r["indicador"] in ITENS:
        d.setdefault((r["indicador"], r["definicao_linha"]), {})[int(r["ano"])] = float(r["valor"])
for it in ITENS:
    print(f"\n### {it}\n")
    print("| linha (base) | cobertura | " + " | ".join(map(str, ANOS)) + " | ultimo ano (valor) |")
    print("|---|---|" + "---|" * (len(ANOS) + 1))
    for (i, l), s in sorted(d.items()):
        if i != it:
            continue
        cel = [f"{s[a]:.2f}" if a in s else "n/d" for a in ANOS]
        ult = max(s)
        print(f"| {l} | {min(s)}-{ult} ({len(s)} anos) | " + " | ".join(cel) + f" | {ult} ({s[ult]:.2f}) |")
