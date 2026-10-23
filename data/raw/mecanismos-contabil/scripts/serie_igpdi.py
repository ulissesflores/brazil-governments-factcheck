"""IGP-DI (FGV) variacao dezembro/dezembro por ano, calculada do indice mensal do Ipeadata (IGP12_IGPDI12)
coletado em ../inflacao/igpdi-ipeadata-raw.json (bruto com hash em ../inflacao/manifest.jsonl). Sem rede.
Uso: python3 -I serie_igpdi.py <pasta_mecanismos>"""
import csv, json, pathlib, sys
base = pathlib.Path(sys.argv[1])
raw = json.load(open(base.parent / "inflacao/igpdi-ipeadata-raw.json"))["value"]
idx = {r["VALDATA"][:7]: r["VALVALOR"] for r in raw}
VINT = "Ipeadata IGP12_IGPDI12, colhido em 2026-10-19 (../inflacao/igpdi-ipeadata-raw.json)"
w = csv.writer(open(base / "series/igpdi-dez-dez-anual.csv", "w", newline="", encoding="utf8"))
w.writerow(["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"])
for a in range(1945, 2026):
    d1, d0 = idx.get(f"{a}-12"), idx.get(f"{a-1}-12")
    if d1 and d0:
        w.writerow(["igpdi_dez_dez", "FGV via Ipeadata", "IGP-DI, variacao dezembro/dezembro sobre o indice mensal", a, f"{(d1/d0-1)*100:.2f}", "% a.a.",
                    "indice encadeado atraves das trocas de moeda pelo proprio Ipeadata", VINT])
print([ (a, round((idx[f'{a}-12']/idx[f'{a-1}-12']-1)*100,1)) for a in range(1970,1978)])
