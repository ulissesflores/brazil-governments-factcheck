# Doing Business (Banco Mundial), Brasil (linha BRA = media ponderada Sao Paulo/Rio). Le so o xlsx baixado. python3 -I doingbusiness.py
import csv, json, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import xl
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
arq = "bruto/doingbusiness-historical-DB04-DB20.xlsx"
d = xl.abrir(str(RAIZ / arq))
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]
SEL = {5: ("db_score_metodologia_DB17_21", "pontos 0-100", "Ease of doing business score (DB17-21 methodology)"),
       6: ("db_score_metodologia_DB15", "pontos 0-100", "Ease of doing business score (DB15 methodology)"),
       7: ("db_score_metodologia_DB10_14", "pontos 0-100", "Ease of doing business score (DB10-14 methodology)"),
       9: ("db_abrir_empresa_procedimentos_homens", "numero", "Starting a business: Procedures - Men"),
       10: ("db_abrir_empresa_tempo_homens", "dias", "Starting a business: Time - Men"),
       11: ("db_abrir_empresa_custo_homens", "% da renda per capita", "Starting a business: Cost - Men"),
       15: ("db_abrir_empresa_capital_minimo", "% da renda per capita", "Starting a business: Paid-in minimum capital"),
       53: ("db_impostos_pagamentos_por_ano", "numero por ano", "Paying taxes: Payments (number per year)"),
       54: ("db_impostos_tempo_horas_por_ano", "horas por ano", "Paying taxes: Time (hours per year)"),
       55: ("db_impostos_taxa_total_pct_lucro", "% do lucro", "Paying taxes: Total tax and contribution rate (% of profit)")}
rows = []
for sheet in ("DB21 Data", "DB20 Data"):
    sh = d[sheet]
    h = sh[4]
    for r in sh[5:]:
        if r and r[0] == "BRA":
            r = r + [""] * (60 - len(r))
            for j, (ind, un, desc) in SEL.items():
                if r[j] != "":
                    ano = int(r[4])
                    rows.append((ind, "Banco Mundial, Doing Business (arquivo historico DB04-DB20)", "%s; economia 'Brazil' (BRA, cidade-modelo ponderada); 'DB year' %d reflete dados de maio/junho do ano anterior" % (desc, ano), ano, round(float(r[j]), 4), un, "ano = edicao do relatorio (DB year), nao ano-calendario do dado", "aba '%s' de Historical-Data--DB04-DB20-.xlsx; baixado %s sha256 %s; relatorio descontinuado em 2021 (ver nota oficial)" % (sheet, man[arq]["timestamp_utc"][:10], man[arq]["sha256"][:12])))
rows.sort(key=lambda x: (x[7], x[0], x[3]))
with open(RAIZ / "series/doing-business-brasil.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(COLS); w.writerows(rows)
print(len(rows))
