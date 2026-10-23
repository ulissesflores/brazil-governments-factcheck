# Tesouro Nacional, "Estimativa da CTB do Governo Geral": Tabela 1 (2 anos) e rotulos do Grafico 1 (serie por esfera).
# So le derivado/txt (pdftotext -layout do bruto). python3 -I tesouro_ctb.py
import csv, json, re
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
rows, avisos = [], []
ESF = [("central", 17, 24), ("estadual", 6, 11), ("municipal", 1, 3.5)]
for ed in (2018, 2020, 2022, 2025):
    arq = "bruto/tesouro-ctb/Boletim_CTB_%d.pdf" % ed
    vint = "Tesouro Nacional, Estimativa da CTB do Governo Geral, boletim %d; baixado %s sha256 %s" % (ed, man[arq]["timestamp_utc"][:10], man[arq]["sha256"][:12])
    L = (RAIZ / ("derivado/txt/tesouro-Boletim_CTB_%d.txt" % ed)).read_text().split("\n")
    # Tabela 1
    for i, l in enumerate(L):
        m = re.match(r"\s*(Governo Central|Governos? Estaduais?|Governos? Municipais?|Governo Geral)\s+[\d.]+\s+[\d.]+\s+(\d+,\d\d)%\s+(\d+,\d\d)%", l)
        if m:
            nome = m.group(1)
            e = {"Governo Central": "central", "Governo Geral": "geral"}.get(nome, "estadual" if "Estadu" in nome else "municipal")
            anos = re.search(r"(20\d\d)\s+(20\d\d)\s+(20\d\d)\s+(20\d\d)", "\n".join(L[max(0, i - 6):i]))
            a1, a2 = (int(anos.group(3)), int(anos.group(4))) if anos else (ed - 1, ed)
            for a, v in ((a1, m.group(2)), (a2, m.group(3))):
                rows.append(("tesouro_ctb_%s_pct_pib__boletim_%d" % (e, ed), "Tesouro Nacional, boletim CTB %d (Tabela 1)" % ed, "Carga tributaria bruta, %s, %% do PIB (GFSM 2014)" % nome.lower(), a, float(v.replace(",", ".")), "% do PIB", "linha %d do texto; dado preliminar no ano mais recente" % (i + 1), vint))
            if "Geral" in nome and nome == "Governo Geral":
                pass
    # Grafico 1: rotulos por coluna
    ax = [i for i, l in enumerate(L) if len(re.findall(r"\b20\d\d\b", l)) >= 8 and re.match(r"^\s*(20\d\d\s+)+20\d\d\s*$", l)]
    if not ax:
        avisos.append((ed, "sem eixo do Grafico 1"))
        continue
    iax = ax[0]
    cols = {int(m.group(0)): m.start() + 2 for m in re.finditer(r"20\d\d", L[iax])}
    toks = []
    for i in range(max(0, iax - 30), iax):
        for m in re.finditer(r"(\d+),(\d)%", L[i]):
            toks.append((float(m.group(1) + "." + m.group(2)), m.start() + len(m.group(0)) / 2, i))
    ini = min(cols)
    for a, c in cols.items():
        cand = [t for t in toks if abs(t[1] - c) <= 4.5]
        tot = [t for t in cand if t[0] >= 25]
        if len(tot) == 1:
            rows.append(("tesouro_ctb_geral_pct_pib__boletim_%d" % ed, "Tesouro Nacional, boletim CTB %d (Grafico 1, rotulo do total)" % ed, "Carga tributaria bruta, governo geral, %% do PIB, lido do rotulo (1 casa) do grafico", a, tot[0][0], "% do PIB", "rotulo do grafico (1 casa decimal); posicao por coluna do texto extraido", vint))
        else:
            avisos.append((ed, a, "total ambiguo", [t[0] for t in cand]))
        for nome, lo, hi in ESF:
            e = [t for t in cand if lo <= t[0] <= hi]
            if len(e) == 1:
                rows.append(("tesouro_ctb_%s_pct_pib__boletim_%d" % (nome, ed), "Tesouro Nacional, boletim CTB %d (Grafico 1, rotulo)" % ed, "Carga tributaria bruta, governo %s, %% do PIB, rotulo (1 casa) do grafico" % nome, a, e[0][0], "% do PIB", "rotulo do grafico; faixa de valor usada para distinguir a serie: %s-%s" % (lo, hi), vint))
            else:
                avisos.append((ed, a, nome, [t[0] for t in cand]))
vistos, unicas = set(), []
for r in rows:  # a Tabela 1 aparece em mais de um quadro: fica a primeira ocorrencia por (indicador, ano, fonte)
    k = (r[0], r[3], r[1])
    if k not in vistos:
        vistos.add(k); unicas.append(r)
rows = unicas
with open(RAIZ / "series/tesouro-ctb-governo-geral-por-boletim.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(COLS); w.writerows(sorted(rows, key=lambda r: (r[0], r[3])))
print(len(rows), "linhas; avisos:", len(avisos), "(graficos de 2018-2022 sao imagens: so Tabela 1)")
