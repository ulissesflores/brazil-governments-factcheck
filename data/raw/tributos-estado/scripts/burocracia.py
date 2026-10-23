# eventos de burocracia (leis e nota do Banco Mundial) com trecho literal. Le so bruto. python3 -I burocracia.py
import csv, json, re, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import txt
MANDATOS = [(r["posse"], r["saida"], r["nome"]) for r in csv.DictReader(open(RAIZ.parent / "porquinho/bruto/mandatos.csv", encoding="utf-8"))]

def quem(d):
    return next((g for a, b, g in MANDATOS if a <= d < b), "?")
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
P = "https://www.planalto.gov.br/ccivil_03"
E = [
 ("2007-12-03", "Lei 11.598/2007", "cria", "texto do ato", "@2007-12-03", "bruto/planalto/l11598.html", P + "/_ato2007-2010/2007/lei/l11598.htm", r"Art\. 2o Fica criada a Rede Nacional para a Simplificação do Registro e da Legalização de Empresas e Negócios - REDESIM.{0,120}", "base legal da REDESIM, fonte do Mapa de Empresas"),
 ("2019-09-20", "Lei 13.874/2019 (Declaracao de Direitos de Liberdade Economica)", "cria", "texto do ato", "@2019-09-20", "bruto/planalto/l13874.html", P + "/_ato2019-2022/2019/lei/L13874.htm", r"Art\. 1º Fica instituída a Declaração de Direitos de Liberdade Econômica.{0,200}", "conversao da MPv 881/2019; o art. 3º lista direitos (ex.: desenvolver atividade de baixo risco sem ato publico de liberacao); efeito sobre o tempo de abertura nao medido aqui"),
 ("2021-09-16", "Nota oficial do Banco Mundial: World Bank Group to Discontinue Doing Business Report", "extingue", "texto do ato (nota institucional)", "n/a (Banco Mundial)", "bruto/bm-nota-descontinuacao-doing-business-2021-09-16.html", "https://www.worldbank.org/en/news/statement/2021/09/16/world-bank-group-to-discontinue-doing-business-report", r"After data irregularities on Doing Business 2018 and 2020 were reported internally in June 2020, World Bank management paused the next Doing Business report.{0,260}", "a nota atribui a descontinuacao a irregularidades de dados nas edicoes 2018 e 2020 apuradas internamente; a pagina remete a 'Statement on Release of Investigation into Data Irregularities in Doing Business 2018 and 2020' (nao baixada)"),
]
rows = []
for d, inst, sent, base, gov, f, url, rx, nota in E:
    t = re.sub(r"\s+", " ", txt.ler(RAIZ / f))
    m = re.search(rx, t)
    assert m, inst
    r = man[f]
    rows.append({"data": d, "instrumento": inst, "sentido": sent, "base_do_sentido": base, "governo": (quem(gov[1:]) if gov.startswith("@") else gov), "url": url, "trecho_literal": m.group(0).strip(), "arquivo_bruto": f, "sha256_do_bruto": r["sha256"], "nota": nota, "vintage": "lido em %s" % r["timestamp_utc"][:10]})
with open(RAIZ / "eventos_burocracia.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
