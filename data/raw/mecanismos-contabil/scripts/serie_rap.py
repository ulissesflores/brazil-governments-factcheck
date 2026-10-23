"""Estoque de restos a pagar (RAP) inscrito/reinscrito de um exercicio para o seguinte, Tesouro Nacional.
Le derivado/rap-2026.txt (Tabela 2, pdftotext do bruto/tesouro-relatorio-rap-2026.pdf; linhas 'AAAA/AAAA+1') e,
para o par 2007/2008, derivado/rap-2019.txt (Tabela 2 do relatorio de 2019, linha '2008').
PIB = RTN tab 2.2 (serie/rtn-resultado-primario-extraordinarias.csv, indicador pib_nominal_rs_mi), calculo deste dossie.
Uso: python3 -I serie_rap.py <pasta_mecanismos>. Sem rede."""
import csv, re, sys, pathlib
base = pathlib.Path(sys.argv[1])
num = lambda s: float(s.replace(",", "."))
VINT = "Relatorio de Avaliacao dos Restos a Pagar 2026 (Tesouro Nacional, estoque inscrito para 2026) e 2019 (so a linha 2007/2008)"
reg = {}  # ano_fim (ano em que o estoque e apurado: 31/12 de Y) -> (total, proc, nproc, canc, pagos, apagar)
for ln in open(base / "derivado/rap-2026.txt", encoding="utf8"):
    m = re.match(r"\s*(20\d\d)/(20\d\d)\s+(.*)", ln)
    if not m: continue
    campos = re.findall(r"-|\d+(?:,\d+)?", m.group(3))
    if len(campos) != 12: continue
    v = [None if c == "-" else num(c) for c in campos]
    reg[int(m.group(1))] = dict(total=v[0], canc=v[1], pagos=v[2], apagar=v[3], proc=v[4], nproc=v[8])
for ln in open(base / "derivado/rap-2019.txt", encoding="utf8"):
    m = re.match(r"\s*2008\s+(\d+,\d+)\s+(\d+,\d+)\s+(\d+,\d+)\s+(\d+,\d+)\s+(\d+,\d+)\s+(\d+,\d+)\s+(\d+,\d+)\s+(\d+,\d+)\s+(\d+,\d+)", ln)
    if m:
        v = [num(x) for x in m.groups()]
        reg[2007] = dict(total=v[0], canc=v[1], pagos=v[2], apagar=v[3], proc=v[4], nproc=v[7])
pib = {}
for r in csv.DictReader(open(base / "series/rtn-resultado-primario-extraordinarias.csv", encoding="utf8")):
    if r["indicador"] == "pib_nominal_rs_mi": pib[int(r["ano"])] = float(r["valor"])
out = []
def put(ind, fonte, defn, ano, val, un, nota=""):
    out.append([ind, fonte, defn, ano, "" if val is None else f"{val:.4f}".rstrip("0").rstrip("."), un, nota, VINT])
D1 = "Estoque de restos a pagar (processados + nao processados) inscrito e reinscrito em 31/12 do ano para o exercicio seguinte; Orcamentos Fiscal e da Seguridade Social da Uniao, inclui despesas financeiras"
for y in sorted(reg):
    r = reg[y]
    nota = "ano = 31/12 do ano indicado (tabela do Tesouro rotula 'AAAA/AAAA+1')"
    if y == 2025: nota += "; a elevacao de 2025/2026 e concentrada em despesas financeiras (R$ 65,4 bi dos R$ 79,1 bi segundo o proprio relatorio)"
    if y == 2018: nota += "; R$ 34,0 bi da elevacao de 2018/2019 decorrem de mudanca de sistematica de pagamento (ordem bancaria), nao de fluxo, segundo o relatorio de 2019"
    put("rap_estoque_total_rs_bi", "Tesouro RAP Tab 2", D1, y, r["total"], "R$ bilhoes correntes", nota)
    put("rap_estoque_processados_rs_bi", "Tesouro RAP Tab 2", D1 + " (so processados)", y, r["proc"], "R$ bilhoes correntes")
    put("rap_estoque_nao_processados_rs_bi", "Tesouro RAP Tab 2", D1 + " (so nao processados)", y, r["nproc"], "R$ bilhoes correntes")
    if y in pib:
        put("rap_estoque_total_pct_pib", "calculo sobre Tesouro RAP Tab 2 e RTN tab 2.2", D1 + " dividido pelo PIB nominal do ano", y, r["total"] * 1000 / pib[y] * 100, "% do PIB", "PIB do mesmo ano (RTN)")
w = csv.writer(open(base / "series/restos-a-pagar-estoque-fim-de-ano.csv", "w", newline="", encoding="utf8"))
w.writerow(["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]); w.writerows(out)
print(len(reg), "anos", min(reg), max(reg))
for y in sorted(reg): print(y, reg[y]["total"], round(reg[y]["total"]*1000/pib[y]*100,2) if y in pib else None)
