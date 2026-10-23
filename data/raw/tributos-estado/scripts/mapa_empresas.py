# Mapa de Empresas (Redesim), tempo medio de abertura de empresas, Brasil, por quadrimestre. So le derivado/txt. python3 -I mapa_empresas.py
import csv, json, re
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]

def horas(s):
    d = re.search(r"(\d+) dias?", s); h = re.search(r"(\d+) horas?", s)
    return (int(d.group(1)) * 24 if d else 0) + (int(h.group(1)) if h else 0)

rows = []
for arq in sorted((RAIZ / "bruto/mapa-empresas").glob("*.pdf")):
    t = re.sub(r"\s+", " ", (RAIZ / ("derivado/txt/mapa-%s.txt" % arq.stem)).read_text())
    ano, q = arq.stem.split("-")[1], arq.stem.split("-")[2]
    m = re.search(r"O tempo médio ?\d* registrado (?:ao final d\w+ |n\w+ )?\w+ quadrimestre de (\d{4}) para abertura de empresas no Brasil é de (.+?)(?:, o que| apresent)", t)
    if m:
        txt, ano_b = m.group(2), int(m.group(1))
    else:
        m = re.search(r"Brasil \((\d)º quadrimestre/(\d{4})\): ➤ (.+?) em média", t)
        assert m, arq
        txt, ano_b = m.group(3), int(m.group(2))
    assert ano_b == int(ano), (arq, ano_b)
    h = horas(txt)
    metodo = "media baseada apenas no ultimo mes do quadrimestre" if (int(ano), q) < (2024, "2o") else "media baseada na soma dos dados de todos os meses do quadrimestre (nova abordagem declarada no boletim do 2o quadrimestre de 2024)"
    r = man["bruto/mapa-empresas/" + arq.name]
    rows.append(("mapa_empresas_tempo_medio_abertura_horas", "Mapa de Empresas / Redesim (Governo Federal), boletim quadrimestral", "Tempo medio de abertura de empresas no Brasil (inclui a etapa de viabilidade), fim do %s quadrimestre de %s; texto do boletim: '%s'" % (q.replace("o", "º"), ano, txt), "%s-Q%s" % (ano, q[0]), h, "horas", metodo, "boletim %s-%s.pdf baixado %s sha256 %s" % (ano, q, r["timestamp_utc"][:10], r["sha256"][:12])))
r3 = man["bruto/mapa-empresas/boletim-2020-3o.pdf"]
rows.insert(0, ("mapa_empresas_tempo_medio_abertura_horas", "Mapa de Empresas / Redesim (Governo Federal), boletim quadrimestral", "Tempo medio de abertura de empresas no Brasil em janeiro de 2019 (primeiro ponto do 'Destaque 3' do boletim do 3o quadrimestre de 2020): '5 dias e 9 horas'", "2019-01", 129, "horas", "ponto MENSAL lido do rotulo do grafico (Destaque 3), nao quadrimestral; metodo: ultimo mes", "boletim 2020-3o.pdf baixado %s sha256 %s" % (r3["timestamp_utc"][:10], r3["sha256"][:12])))
with open(RAIZ / "series/mapa-empresas-tempo-abertura-por-quadrimestre.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(COLS); w.writerows(rows)
for r in rows: print(r[3], r[4], r[5])
