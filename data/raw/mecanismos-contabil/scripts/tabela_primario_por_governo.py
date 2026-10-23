"""Tabela GFM do resultado primario do Governo Central por governo: reportado, sem concessoes+ativos, sem concessoes+ativos+dividendos.
Le series/rtn-resultado-primario-extraordinarias.csv e mandatos.csv; sem rede. Uso: python3 -I tabela_primario_por_governo.py <pasta> <mandatos.csv>"""
import csv, datetime as dt, pathlib, statistics as st, sys
base = pathlib.Path(sys.argv[1]); man = list(csv.DictReader(open(sys.argv[2], encoding="utf8")))
G = [(m["id"], m["nome"], dt.date.fromisoformat(m["posse"]), dt.date.fromisoformat(m["saida"])) for m in man]
def gov(y):
    return max(G, key=lambda g: (min(g[3], dt.date(y + 1, 1, 1)) - max(g[2], dt.date(y, 1, 1))).days)[0]
d = {}
for r in csv.DictReader(open(base / "series/rtn-resultado-primario-extraordinarias.csv", encoding="utf8")):
    if r["valor"] != "": d.setdefault(r["indicador"], {})[int(r["ano"])] = float(r["valor"])
rows = []
for gid, nome, _, _ in G:
    ys = sorted(y for y in d["resultado_primario_acima_da_linha_pct_pib"] if gov(y) == gid)
    if not ys: continue
    m = lambda k: st.mean(d[k][y] for y in ys)
    rows.append(f"| {nome} | {ys[0]}-{ys[-1]} ({len(ys)}) | {m('resultado_primario_acima_da_linha_pct_pib'):.2f} | {m('primario_sem_concessoes_e_ativos_pct_pib'):.2f} | {m('primario_sem_concessoes_ativos_dividendos_pct_pib'):.2f} | {m('concessoes_permissoes_pct_pib')+m('operacoes_com_ativos_pct_pib'):.2f} | {m('dividendos_participacoes_pct_pib'):.2f} |")
print("| governo | anos (n) | primario reportado | sem concessoes e ativos | sem concessoes, ativos e dividendos | peso concessoes+ativos | peso dividendos |")
print("|---|---|---|---|---|---|---|")
print("\n".join(rows))
