# Ipea TD 583 (Varsano et al. 1998), Tabela A.1: carga tributaria global 1947-1996 (literatura). So le derivado/txt. python3 -I ipea_td583.py
import csv, json, re
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
r = man["bruto/ipea-td583-varsano-1998.pdf"]
vint = "Ipea TD 583 (agosto de 1998), Tabela A.1; baixado %s sha256 %s" % (r["timestamp_utc"][:10], r["sha256"][:12])
L = (RAIZ / "derivado/txt/ipea-td583.txt").read_text().split("\n")
i0 = next(i for i, l in enumerate(L) if l.strip() == "Tabela A.1")
rows, vistos = [], {}
for i in range(i0, i0 + 30):
    for m in re.finditer(r"(19\d\d)(\*?)\s+(\d\d,\d\d)", L[i]):
        a = int(m.group(1)); vistos[a] = (float(m.group(3).replace(",", ".")), bool(m.group(2)), i + 1)
assert sorted(vistos) == list(range(1947, 1997)), sorted(vistos)
for a in sorted(vistos):
    v, est, ln = vistos[a]
    nota = "linha %d do texto extraido; " % ln + ("estimativa (asterisco da tabela). " if est else "") + "ate 1979 direto das contas nacionais; de 1980 a 1989 metodologia das contas nacionais com ajustes (previdencia/FEF); de 1990 PIB IBGE ref. 1997"
    rows.append(("ipea_td583_carga_tributaria_global_pct_pib", "Ipea TD 583 (Varsano et al. 1998), literatura", "Carga tributaria global (tres esferas) / PIB, compilacao de Contas Nacionais (FGV/IBGE) com ajustes dos autores", a, v, "% do PIB", nota, vint))
with open(RAIZ / "series/ipea-td583-carga-tributaria-1947-1996.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["indicador","fonte","definicao_linha","ano","valor","unidade","nota","vintage"]); w.writerows(rows)
print(len(rows), "anos 1947-1996")
