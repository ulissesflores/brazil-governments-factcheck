# Receita Federal, "Carga Tributaria no Brasil": uma serie por EDICAO (nunca emendadas). Le so bruto/. python3 -I carga_receita.py
import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import xl  # noqa: E402

COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]
man = {}
for l in (RAIZ / "manifest.jsonl").read_text().splitlines():
    r = json.loads(l)
    man[r["arquivo"]] = r


def vint(ed, arq):
    r = man.get("bruto/receita-ctb/" + arq)
    return "Receita Federal, Carga Tributaria no Brasil, edicao %s (%s); baixado %s sha256 %s" % (ed, arq, r["timestamp_utc"][:10], r["sha256"][:12])


SKIP = []


def fnum(x, ctx):
    try:
        return float(x)
    except ValueError:
        SKIP.append((ctx, x))
        return None


def num(s):
    return float(s.replace(".", "").replace(",", "."))


TXT = {y: (RAIZ / ("derivado/txt/ctb-%d.txt" % y)).read_text().split("\n") for y in range(1995, 2025)}

# ---------- 1) total da CTB, por edicao ----------
tot = []  # (edicao, ano, valor, definicao, nota)
DEF_CTB = "Carga Tributaria Bruta = arrecadacao tributaria bruta / PIB a precos de mercado, tres esferas"
# 1995-1997: definicoes proprias (nao e a CTB de 1998+)
manual = [
 (1995, 1995, 26.77, "Carga Tributaria Bruta (def. 1995: arrecadacao tributaria bruta menos restituicoes, retificacoes e saques do FGTS)", r"CARGA TRIBUTÁRIA BRUTA\s+: 26,77%"),
 (1995, 1995, 28.56, "Arrecadacao Tributaria Bruta (def. 1995)", r"ARRECADAÇÃO TRIBUTÁRIA BRUTA : 28,56%"),
 (1995, 1994, 27.79, "Carga Tributaria Bruta (def. 1995), ano anterior citado na edicao", r"CTB/94 = 27,79%"),
 (1995, 1994, 28.96, "Arrecadacao Tributaria Bruta (def. 1995), ano anterior citado na edicao", r"ATB/94 = 28,96%"),
 (1996, 1996, 28.17, "Carga Fiscal Bruta (def. 1996-1997, 'CFB')", r"Carga Fiscal Bruta de 28,17%"),
 (1996, 1996, 26.18, "Carga Fiscal Liquida (def. 1996-1997, 'CFL' = CFB menos saques do FGTS, incentivos, restituicoes e retificacoes)", r"Carga Fiscal Líquida de 26,18%"),
 (1997, 1997, 27.81, "Carga Fiscal Bruta (def. 1996-1997, 'CFB')", r"Carga Fiscal Bruta correspondeu a 27,81%"),
 (1997, 1997, 25.79, "Carga Fiscal Liquida (def. 1996-1997, 'CFL')", r"Carga Fiscal Líquida atingiu 25,79%"),
 (1998, 1998, 29.84, DEF_CTB + " (def. 1998: inclui IRRF de estados/municipios e previdencia municipal)", r"Em 1998, a Carga Tributária Bruta foi de 29,84%"),
 (1998, 1997, 29.00, DEF_CTB + " (def. 1998, recalculado para 1997)", r"em\s*$|1997, o valor calculado foi de 29,00%"),
 (2005, 2005, 37.37, DEF_CTB + " (edicao 2005, antes do ajuste de metodologia e do PIB da edicao 2006)", r"foi de 37,37% do PIB"),
]
for ed, ano, v, d, rx in manual:
    achou = [i + 1 for i, l in enumerate(TXT[ed]) if re.search(rx, l)]
    if not achou and ed == 1998 and ano == 1997:
        achou = [i + 1 for i, l in enumerate(TXT[ed]) if "29,00%" in l]
    assert achou, (ed, ano, v)
    tot.append((ed, ano, v, d, "linha %d do texto extraido do PDF" % achou[0]))

# edicoes com quadro 'Componentes ... CTB' de dois anos
for ed in [1999, 2000, 2001, 2002, 2003, 2004, 2007, 2008, 2009, 2010, 2011, 2012, 2013]:
    L = TXT[ed]
    for i, l in enumerate(L):
        m = re.match(r"\s*Carga Tributária Bruta\s+(\d\d,\d\d)%\s+(\d\d,\d\d)%\s*$", l)
        if m:
            tot.append((ed, ed - 1, num(m.group(1)), DEF_CTB, "linha %d do quadro 'Carga Tributaria Bruta' da edicao" % (i + 1)))
            tot.append((ed, ed, num(m.group(2)), DEF_CTB, "linha %d do quadro 'Carga Tributaria Bruta' da edicao" % (i + 1)))
            break
    else:
        raise SystemExit("sem quadro CTB na edicao %d" % ed)

# edicoes 2006-2011: serie de 5 anos (Total da Receita Tributaria, % do PIB)
for ed in [2006, 2007, 2008, 2010, 2011]:
    for i, l in enumerate(TXT[ed]):
        m = re.match(r"\s*Total da Receita Tributária\s+((?:\d\d,\d\d%\s*){5})\s*$", l)
        if m:
            vs = [num(x) for x in re.findall(r"(\d\d,\d\d)%", m.group(1))]
            for k, v in enumerate(vs):
                tot.append((ed, ed - 4 + k, v, "Total da Receita Tributaria / PIB (serie de 5 anos da edicao)" , "linha %d, 'Tabela 01-B' em %% do PIB" % (i + 1)))
            break
    else:
        raise SystemExit("sem serie 5a em %d" % ed)

# edicoes 2014-2024: planilhas, serie completa 2002..ano
base_rows, esf_rows = [], []
for ed in range(2014, 2025):
    arq = "ctb-tabelas-%d.xlsx" % ed
    d = xl.abrir(str(RAIZ / "bruto/receita-ctb" / arq))
    # INC02B: bases de incidencia, fracao do PIB
    sh = d["INC02B"]
    hdr = next(r for r in sh if sum(bool(re.fullmatch(r"\d{4}", c)) for c in r) >= 3)
    anos = [(j, int(c)) for j, c in enumerate(hdr) if re.fullmatch(r"\d{4}", c)]
    for r in sh:
        r = r + [""] * (len(hdr) - len(r))
        cod = r[1] or r[2]
        if not cod.isdigit() or r is hdr:
            continue
        nome = (r[3] or "").strip()
        nivel = "agregado" if cod.endswith("000") or cod == "0" else "subitem"
        for j, a in anos:
            if r[j] != "":
                v = fnum(r[j], (ed, "INC02B", cod, a))
                if v is not None:
                    base_rows.append((ed, cod, nome, nivel, a, v * 100, arq))
    # T01B: total e por esfera (fracao do PIB)
    sh = d["T01B"]
    hdr = next(r for r in sh if sum(bool(re.fullmatch(r"\d{4}", c)) for c in r) >= 3)
    anos = [(j, int(c)) for j, c in enumerate(hdr) if re.fullmatch(r"\d{4}", c)]
    for r in sh:
        r = r + [""] * (len(hdr) - len(r))
        nome = r[2].strip()
        if nome in ("Total da Receita Tributária", "Tributos do Governo Federal", "Tributos do Governo Estadual", "Tributos do Governo Municipal"):
            for j, a in anos:
                v = fnum(r[j], (ed, "T01B", nome, a)) if r[j] != "" else None
                if v is not None:
                    esf_rows.append((ed, nome, a, v * 100, arq))
                    if nome.startswith("Total"):
                        tot.append((ed, a, v * 100, "Total da Receita Tributaria / PIB (planilha T01B da edicao; serie 2002..%d)" % ed, "planilha %s, aba T01B" % arq))

# edicoes 2006-2013: esferas (2 anos, % PIB) a partir do texto; 2006-2011 tambem 5 anos
def esferas_pdf(ed):
    out = []
    nomes = ["Total da Receita Tributária", "Tributos do Governo Federal", "Tributos do Governo Estadual", "Tributos do Governo Municipal"]
    for i, l in enumerate(TXT[ed]):
        for n in nomes:
            m = re.match(r"\s*%s\s+((?:[\d.]+,\d\d\s+\d\d,\d\d%%\s+\d+,\d\d%%\s*){2})\s*$" % n, l)
            if m:
                g = re.findall(r"([\d.]+,\d\d)\s+(\d\d,\d\d)%\s+(\d+,\d\d)%", m.group(1))
                if len(g) == 2 and (ed, n) not in {(e, nn) for e, nn, *_ in out}:
                    for k, (rs, pib, ar) in enumerate(g):
                        out.append((ed, n, ed - 1 + k, num(pib), "texto do PDF, linha %d (Tabela 01-A/1)" % (i + 1)))
    return out
for ed in range(2006, 2014):
    for t in esferas_pdf(ed):
        esf_rows.append(t)

# ---------- gravar ----------
def gravar(nome, rows):
    with open(RAIZ / "series" / nome, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        w.writerows(rows)

linhas = []
for ed, ano, v, d, nota in sorted(tot, key=lambda x: (x[0], x[3][:30], x[1])):
    arq = "ctb-tabelas-%d.xlsx" % ed if ed >= 2014 else "ctb-%d.pdf" % ed
    linhas.append(("receita_ctb_total_pct_pib__edicao_%d" % ed, "Receita Federal, Carga Tributaria no Brasil, edicao %d" % ed, d, ano, round(v, 4), "% do PIB", nota, vint(ed, arq)))
gravar("receita-ctb-total-por-edicao.csv", linhas)

linhas = []
for ed, cod, nome, nivel, a, v, arq in sorted(base_rows, key=lambda x: (x[0], x[1], x[4])):
    linhas.append(("receita_ctb_base_%s__edicao_%d" % (cod, ed), "Receita Federal, Carga Tributaria no Brasil, edicao %d" % ed, "Base de incidencia %s '%s' (%s), tabela INC02B, %% do PIB" % (cod, nome, nivel), a, round(v, 4), "% do PIB", "planilha %s aba INC02B; codigos 1000..9000 sao agregados; 4300 'Comercio exterior' e subitem de Bens e Servicos" % arq, vint(ed, arq)))
gravar("receita-ctb-por-base-por-edicao.csv", linhas)

linhas = []
for row in sorted(esf_rows, key=lambda x: (x[0], x[1], x[2])):
    ed, n, a, v, arq = row
    nota = arq if arq.startswith("texto") else "planilha %s aba T01B" % arq
    src = ("ctb-tabelas-%d.xlsx" % ed) if ed >= 2014 else ("ctb-%d.pdf" % ed)
    linhas.append(("receita_ctb_esfera_%s__edicao_%d" % (n.replace("Tributos do Governo ", "").replace("Total da Receita Tributária", "total").lower(), ed), "Receita Federal, Carga Tributaria no Brasil, edicao %d" % ed, "%s / PIB" % n, a, round(v, 4), "% do PIB", nota, vint(ed, src)))
# deduplicar (pdf pode repetir ano)
seen, out = set(), []
for r in linhas:
    k = (r[0], r[3])
    if k in seen:
        continue
    seen.add(k); out.append(r)
gravar("receita-ctb-por-esfera-por-edicao.csv", out)
print("celulas nao numericas puladas:", SKIP)
print("total", len(tot), "bases", len(base_rows), "esferas", len(out))
