"""Gastos tributarios federais (Receita Federal, DGT) em % do PIB. Le os CSVs derivados dos .xlsx brutos
(derivado/dgtbe-*/05-Q_VI.csv = bases efetivas 2019-2023; derivado/dgt2024|2025|2026/05-Q_VI.csv = projecoes PLOA)
e, para 2007-2013, a nota tecnica Ipea n.19 (derivado/ipea-nt19.txt, rotulos do Grafico 2, citando RFB Bases Efetivas).
Uso: python3 -I serie_gt.py <pasta_mecanismos>. Sem rede."""
import csv, glob, pathlib, re, sys
base = pathlib.Path(sys.argv[1]); out = []
def put(ind, fonte, defn, ano, val, un, nota, vint):
    out.append([ind, fonte, defn, ano, f"{val:.4f}".rstrip("0").rstrip("."), un, nota, vint])
DEF = "Gasto tributario federal total (perda de arrecadacao estimada pela RFB; metodo de perda de arrecadacao), tributos administrados pela RFB; % do PIB"
def q6(path):
    tot = pib = None
    for r in csv.reader(open(path, encoding="utf8")):
        if r and r[0] == "TOTAL": tot = (float(r[1]), float(r[2]))
        if r and r[0] == "PIB": pib = float(r[1])
    return tot, pib
for d in sorted(glob.glob(str(base / "derivado/dgtbe-*"))):
    ano = int(re.search(r"dgtbe-(\d{4})-", d).group(1)); (rs, pct), pib = q6(d + "/05-Q_VI.csv")
    v = f"DGT Bases Efetivas {ano} (Receita Federal)"
    put("gasto_tributario_federal_pct_pib", "RFB DGT Bases Efetivas", DEF, ano, pct, "% do PIB", "base efetiva (arrecadacao do proprio ano)", v)
    put("gasto_tributario_federal_rs_mi", "RFB DGT Bases Efetivas", DEF, ano, rs / 1e6, "R$ milhoes correntes", "base efetiva", v)
for ano in (2024, 2025, 2026):
    (rs, pct), pib = q6(str(base / f"derivado/dgt{ano}/05-Q_VI.csv"))
    v = f"DGT Previsao PLOA {ano} (Receita Federal)"
    put("gasto_tributario_federal_pct_pib", "RFB DGT PLOA", DEF, ano, pct, "% do PIB", "PROJECAO (previsao PLOA), nao base efetiva", v)
    put("gasto_tributario_federal_rs_mi", "RFB DGT PLOA", DEF, ano, rs / 1e6, "R$ milhoes correntes", "PROJECAO (previsao PLOA)", v)
txt = open(base / "derivado/ipea-nt19.txt", encoding="utf8").read()
for ano, val in zip(range(2007, 2014), ["3,95", "3,78", "3,65", "3,60", "3,68", "4,15", "4,66"]):
    assert val in txt, val  # transcricao dos rotulos do Grafico 2 (conferida contra o texto extraido)
    put("gasto_tributario_federal_pct_pib", "Ipea NT 19 (2016) citando RFB DGT Bases Efetivas", DEF, ano, float(val.replace(",", ".")), "% do PIB",
        "transcrito dos rotulos do Grafico 2 da nota (derivado/ipea-nt19.txt); fonte primaria RFB nao baixada para estes anos; camada literatura", "Ipea Nota Tecnica 19, 2016 (RFB Bases Efetivas 2013)")
out.sort(key=lambda r: (r[0], int(r[3])))
w = csv.writer(open(base / "series/gastos-tributarios-federais.csv", "w", newline="", encoding="utf8"))
w.writerow(["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]); w.writerows(out)
print([(r[3], r[4]) for r in out if r[0].endswith("pct_pib")])
