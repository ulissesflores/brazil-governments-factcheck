"""Emendas parlamentares pagas por tipo e ano, a partir do zip hasheado do Portal da Transparencia (sem rede).

Fonte: ``bruto/emendas/EmendasParlamentares.zip`` (CGU, base unica, cadeia de hash). Le ``EmendasParlamentares.csv``
(latin-1, ';', uma linha por emenda e ano orcamentario) e soma, por 'Ano da Emenda' e 'Tipo de Emenda', duas
colunas que a propria fonte traz: 'Valor Pago' (pago no exercicio da emenda) e 'Valor Restos A Pagar Pagos'
(pago em exercicios seguintes, inscrito em restos a pagar). Nada e estimado; o tipo e o rotulo da CGU.
Saida: ``series/emendas_pagas_por_tipo_e_ano.csv`` (CSV longo, R$ milhoes correntes).
"""
import csv, io, json, re, zipfile
from pathlib import Path

P = Path(__file__).resolve().parent.parent
ZIP = P / "bruto" / "emendas" / "EmendasParlamentares.zip"
man = {Path(json.loads(l)["arquivo"]).name: json.loads(l) for l in (P / "manifest.jsonl").read_text().splitlines() if l.strip()}
m = man["EmendasParlamentares.zip"]
VINT = f"bruto/emendas/EmendasParlamentares.zip adquirido {m['timestamp_utc']} sha256 {m['sha256'][:12]} (Portal da Transparencia, CGU)"


def num(s):
    return float(s.replace(".", "").replace(",", ".")) if s else 0.0


def slug(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "_", t.replace("ê", "e").replace("ç", "c").replace("ã", "a").replace("í", "i").replace("é", "e"))
    return t.strip("_")


tot = {}
with zipfile.ZipFile(ZIP) as z:
    with z.open("EmendasParlamentares.csv") as fh:
        for x in csv.DictReader(io.TextIOWrapper(fh, encoding="latin-1", newline=""), delimiter=";"):
            k = (int(x["Ano da Emenda"]), x["Tipo de Emenda"])
            t = tot.setdefault(k, [0.0, 0.0, 0])
            t[0] += num(x["Valor Pago"]); t[1] += num(x["Valor Restos A Pagar Pagos"]); t[2] += 1
(P / "series").mkdir(exist_ok=True)
CAB = "indicador,fonte,definicao_linha,ano,mes_ou_trimestre,valor,unidade,nota,vintage".split(",")
with open(P / "series" / "emendas_pagas_por_tipo_e_ano.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(CAB)
    for (ano, tipo), (pago, rap, n) in sorted(tot.items()):
        s = slug(tipo)
        w.writerow([f"emendas_pago_exercicio__{s}", "Portal da Transparencia (CGU), EmendasParlamentares.csv", f"'{tipo}': soma de 'Valor Pago' das emendas do ano orcamentario (pago no proprio exercicio)", ano, "", round(pago / 1e6, 3), "R$ milhoes correntes", f"{n} linhas da base no ano", VINT])
        w.writerow([f"emendas_rap_pagos__{s}", "Portal da Transparencia (CGU), EmendasParlamentares.csv", f"'{tipo}': soma de 'Valor Restos A Pagar Pagos' das emendas do ano orcamentario (pago em exercicios seguintes)", ano, "", round(rap / 1e6, 3), "R$ milhoes correntes", f"{n} linhas da base no ano; atribuido ao ano da emenda, nao ao ano do pagamento", VINT])
    # total por ano (soma dos tipos), as duas colunas
    for ano in sorted({k[0] for k in tot}):
        pago = sum(v[0] for k, v in tot.items() if k[0] == ano); rap = sum(v[1] for k, v in tot.items() if k[0] == ano)
        w.writerow(["emendas_pago_exercicio__total", "Portal da Transparencia (CGU), EmendasParlamentares.csv", "todos os tipos: soma de 'Valor Pago' no exercicio da emenda", ano, "", round(pago / 1e6, 3), "R$ milhoes correntes", "", VINT])
        w.writerow(["emendas_rap_pagos__total", "Portal da Transparencia (CGU), EmendasParlamentares.csv", "todos os tipos: soma de 'Valor Restos A Pagar Pagos'", ano, "", round(rap / 1e6, 3), "R$ milhoes correntes", "atribuido ao ano da emenda", VINT])
print({k: round(v[0] / 1e9, 2) for k, v in sorted(tot.items()) if k[0] in (2019, 2024)})
