# Tesouro Transparente, "Dividendos Arrecadados pela Uniao" (planilha 2015 a abril/2020): total por ano e por empresa. So le bruto. python3 -I tesouro_dividendos.py
import csv, json, re, sys
from collections import defaultdict
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import xl
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
arq = "bruto/tesouro-dividendos/dividendos-2015-a-abril-de-2020.xlsx"
vint = "Tesouro Transparente CKAN 'Dividendos Arrecadados pela Uniao' (metadata_modified 2020-05-29); baixado %s sha256 %s" % (man[arq]["timestamp_utc"][:10], man[arq]["sha256"][:12])
d = xl.abrir(str(RAIZ / arq))
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]
rows = []
for aba, sh in d.items():
    ano = int(aba)
    tot_planilha, por = None, defaultdict(float)
    cab = ""
    for r in sh:
        r = [c.strip() for c in r]
        r = [c for c in r if c != ""] if r and r[0] == "" else r
        if not r:
            continue
        if r[0] == "EMPRESAS":
            cab = r[1]
        if r[0] == "TOTAL" and len(r) > 1:
            tot_planilha = float(r[1])
        elif len(r) >= 3 and re.fullmatch(r"[\d.]+", r[2]) and re.fullmatch(r"-?[\d.]+(E-?\d+)?", r[1]) and r[0].lower() not in ("total",) and not re.match(r"(?i)(janeiro|fevereiro|mar|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)", r[0]):
            por[r[0].upper()] += float(r[1])
    parcial = ano == 2020
    nota = "planilha %s, aba %s; coluna de valor rotulada '%s' (muda entre abas: 'Valor pago', 'Valor Atualizado', 'Valor recibo (Caixa)'); regime de caixa, na entrada na Conta Unica; inclui dividendos, JCP e premio de debentures" % (arq.split("/")[-1], aba, cab) + ("; ANO PARCIAL: pagamentos ate 30/04/2020" if parcial else "")
    rows.append(("tesouro_dividendos_total_rs", "Tesouro Nacional (Tesouro Transparente)", "Receitas de participacao da Uniao (dividendos, JCP e premio de debentures), total do ano, linha TOTAL da aba", ano, round(tot_planilha, 2), "R$ correntes", nota, vint))
    rows.append(("tesouro_dividendos_total_soma_das_linhas_rs", "calculo desta pasta sobre a planilha do Tesouro", "Soma das linhas de pagamento por empresa da aba (para conferir com a linha TOTAL)", ano, round(sum(por.values()), 2), "R$ correntes", nota, vint))
    for emp in ("PETROBRAS", "PETROBRÁS", "BB", "CAIXA", "ELETROBRAS", "ELETROBRÁS", "CORREIOS", "ECT", "BNDES"):
        if emp in por:
            rows.append(("tesouro_dividendos_%s_rs" % emp.lower().replace("á", "a"), "Tesouro Nacional (Tesouro Transparente)", "Soma dos pagamentos da empresa %s no ano" % emp, ano, round(por[emp], 2), "R$ correntes", nota, vint))
with open(RAIZ / "series/tesouro-dividendos-2015-2020.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(COLS); w.writerows(rows)
for r in rows:
    if r[0].startswith("tesouro_dividendos_total"): print(r[0][-14:], r[3], r[4])
print(sorted({r[0] for r in rows}))
