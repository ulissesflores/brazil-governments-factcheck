# IBPT (FONTE SECUNDARIA: copia do Poder360 do release de nov/2022). Tabela da p.2 do PDF e IMAGEM: valores transcritos por leitura visual.
# A ancora legivel no texto do PDF (7.129.074 em 2022) e conferida abaixo. python3 -I ibpt.py
import csv, json, re
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
ARQ = "bruto/ibpt-normas-editadas-brasil-2022-copia-poder360.pdf"
GER = """1989 543998|1990 641917|1991 751043|1992 889986|1993 1060864|1994 1259776|1995 1498564|1996 1787127|1997 2126681|1998 2479285|1999 2782984|2000 2896208|2001 3014739|2002 3139908|2003 3267654|2004 3315947|2005 3434805|2006 3510804|2007 3628013|2008 3776364|2009 3989765|2010 4155915|2011 4353665|2012 4614449|2013 4785194|2014 4960610|2015 5241914|2016 5471980|2017 5679157|2018 5876143|2019 6087473|2020 6475682|2021 6782002|2022 7129074"""
TRI = """1989 118922|1990 123893|1991 129072|1992 134467|1993 140087|1994 145943|1995 152043|1996 158398|1997 165019|1998 171916|1999 179102|2000 186588|2001 194388|2002 202513|2003 210977|2004 219796|2005 225626|2006 229616|2007 235900|2008 240210|2009 244148|2010 249124|2011 275094|2012 290932|2013 309147|2014 320343|2015 352366|2016 363779|2017 377566|2018 390726|2019 403322|2020 419387|2021 443236|2022 466561"""
g = {int(a): int(b) for a, b in (x.split() for x in GER.split("|"))}
t = {int(a): int(b) for a, b in (x.split() for x in TRI.split("|"))}
txt = (RAIZ / "derivado/txt/ibpt-2022.txt").read_text()
assert "7.129.074" in txt and g[2022] == 7129074  # ancora no texto
assert all(g[a] < g[a + 1] and t[a] < t[a + 1] for a in range(1989, 2022))  # acumulados crescentes
r = man[ARQ]
vint = "FONTE SECUNDARIA: copia do Poder360 do release do IBPT (nov/2022), baixada %s sha256 %s; acumulado ate 30/09/2022" % (r["timestamp_utc"][:10], r["sha256"][:12])
nota = "transcrito da tabela-imagem da p.2 do PDF; 2022 vai ate 30/09/2022 (ano incompleto); acumulado desde 05/10/1988"
rows = []
for a in range(1989, 2023):
    rows.append(("ibpt_normas_gerais_acumuladas", "IBPT, Quantidade de Normas Editadas no Brasil (secundaria)", "Normas gerais editadas (federais, estaduais, municipais) desde 5/10/1988, acumulado no fim do ano", a, g[a], "normas (acumulado)", nota, vint))
    rows.append(("ibpt_normas_tributarias_acumuladas", "IBPT, Quantidade de Normas Editadas no Brasil (secundaria)", "Normas tributarias editadas (tres esferas) desde 5/10/1988, acumulado no fim do ano", a, t[a], "normas (acumulado)", nota + "; a linha '1985 a 04/10/1988' do quadro mostra 29.713 e o salto para 118.922 em 1989 nao e explicado no release", vint))
    if a > 1989:
        rows.append(("ibpt_normas_tributarias_no_ano_derivado", "calculo desta pasta sobre IBPT (secundaria)", "Normas tributarias editadas no ano = diferenca entre acumulados consecutivos", a, t[a] - t[a - 1], "normas no ano", "DERIVADO por subtracao; " + nota, vint))
        rows.append(("ibpt_normas_gerais_no_ano_derivado", "calculo desta pasta sobre IBPT (secundaria)", "Normas gerais editadas no ano = diferenca entre acumulados consecutivos", a, g[a] - g[a - 1], "normas no ano", "DERIVADO por subtracao; " + nota, vint))
with open(RAIZ / "series/ibpt-normas-tributarias.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["indicador","fonte","definicao_linha","ano","valor","unidade","nota","vintage"]); w.writerows(rows)
print(len(rows), "linhas; 2010-2011 salto:", t[2011] - t[2010], "; 1989 vs 1988:", t[1989])
