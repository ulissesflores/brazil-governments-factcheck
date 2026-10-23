# Por edicao da CTB da Receita: PIB, arrecadacao tributaria bruta e CTB do(s) ano(s) do quadro de abertura. So le bruto/derivado. python3 -I ctb_pib_arrec.py
import csv, json, re, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import xl
def n(s):
    return float(s.replace(".", "").replace(",", "."))
out = []
for ed in list(range(1999, 2005)) + list(range(2007, 2015)):
    L = (RAIZ / ("derivado/txt/ctb-%d.txt" % ed)).read_text().split("\n")
    for i, l in enumerate(L):
        m = re.match(r"\s*Carga Tributária Bruta\s+(\d\d,\d\d)%\s+(\d\d,\d\d)%\s*$", l)
        if m:
            blk = "\n".join(L[max(0, i - 8): i])
            F = r"(?:\(\d\)|\d\s*/)?"
            pib = re.search(r"Produto\s*I?\s*nterno Bruto\s*" + F + r"\s+([\d.]+,\d\d)\s*" + F + r"\s+([\d.]+,\d\d)", blk)
            arr = re.search(r"Arrecadação Tributária Bruta\s+([\d.]+,\d\d)\s+([\d.]+,\d\d)", blk)
            assert pib and arr, (ed, blk)
            for k, a in enumerate((ed - 1, ed)):
                out.append((ed, a, n(pib.group(k + 1)), n(arr.group(k + 1)), n(m.group(k + 1))))
            break
for ed in range(2015, 2025):
    d = xl.abrir(str(RAIZ / ("bruto/receita-ctb/ctb-tabelas-%d.xlsx" % ed)))
    sh = d["Tab_01"]
    hdr = next(r for r in sh if sum(bool(re.fullmatch(r"\d{4}", c)) for c in r) >= 2)
    anos = [(j, int(c)) for j, c in enumerate(hdr) if re.fullmatch(r"\d{4}", c)]
    def linha(nome):
        return next(r for r in sh if len(r) > 1 and r[1].strip().startswith(nome)) + [""] * len(hdr)
    p, a, c = linha("Produto Interno Bruto"), linha("Arrecadação Tributária Bruta"), linha("Carga Tributária Bruta")
    for j, y in anos:
        if y >= ed - 1 and p[j] != "" and c[j] != "":
            out.append((ed, y, float(p[j]) * 1000, float(a[j]) * 1000, float(c[j]) * 100))
out.sort()
with open(RAIZ / "derivado/ctb-pib-arrecadacao-por-edicao.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["edicao", "ano", "pib_rs_milhoes", "arrecadacao_rs_milhoes", "ctb_pct_pib"]); w.writerows([(e, a, round(p, 1), round(r, 1), round(c, 2)) for e, a, p, r, c in out])
print(len(out))
