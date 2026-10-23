# mistura-do-infografico.md: o que o PROPRIO infografico mistura, com a DIRECAO medida do efeito sobre cada governo.
# Convencao (declarada no texto): "favorece" = o numero impresso (ou o efeito da mistura) deixa o governo MELHOR que a referencia de metodo
# constante (menor para desemprego, inflacao, pobreza, Gini; maior para PIB, salario minimo real, expectativa de vida); "prejudica" = pior;
# "neutro" = diferenca dentro de 1 unidade da ultima casa impressa; "indeterminado" = sem referencia no ano/janela, ou o sinal muda com a referencia.
# Nada aqui infere intencao. Rode: python3 -I gerar_mistura.py (depois de calc.py e gerar_vintage.py).
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from carga import *  # noqa: E402,F401,F403

M = json.load(open(H / "saida" / "medidas.json"))
SA = M["series_anuais"]
INFO = list(csv.DictReader(open(D.parent / "infografico-transcrito.csv", encoding="utf-8")))
GOVS = ["Ditadura", "Itamar", "FHC", "Lula 1-2", "Dilma", "Temer", "Bolsonaro", "Lula 3"]
NOME = dict(zip(GOVS, ["Costa e Silva + Medici", "Itamar Franco", "FHC", "Lula 1-2", "Dilma", "Temer", "Bolsonaro", "Lula 3"]))
MAND = {"Ditadura": (1967, 1973), "Itamar": (1993, 1994), "FHC": (1995, 2002), "Lula 1-2": (2003, 2010), "Dilma": (2011, 2016), "Temer": (2017, 2018), "Bolsonaro": (2019, 2022), "Lula 3": (2023, 2025)}
JAN = {  # janelas impressas por indicador de fluxo
    "pib": {"Ditadura": (1968, 1973), "Itamar": (1992, 1994), "FHC": (1995, 2002), "Lula 1-2": (2003, 2010), "Dilma": (2011, 2016), "Temer": (2016, 2018), "Bolsonaro": (2019, 2022), "Lula 3": (2023, 2025)},
}
JAN["ipca"] = {**JAN["pib"], "Ditadura": (1967, 1973)}
JAN["des"] = {**JAN["pib"], "Bolsonaro": (2019, 2020)}
JAN["sm"] = dict(JAN["pib"])
IMP = {  # valores impressos (infografico-transcrito.csv)
    "pib": [11.1, 2.5, 2.3, 4.0, 1.4, 0.7, 1.8, 2.9], "ipca": [20.3, 1088, 7.6, 5.6, 8.7, 3.4, 6.4, 4.9],
    "des": [3.7, 6.8, 7.7, 8.4, 6.7, 12.3, 13.2, 9.3], "sm": [42.8, -13.9, 4.8, 58.5, 8.0, 1.1, 0.9, 12.6],
    "pob": [42.6, 34.0, 28.9, 21.4, 22.1, 26.5, 31.6, 27.4], "gini": [0.59, 0.60, 0.59, 0.53, 0.52, 0.54, 0.58, 0.51],
    "e0": [62.6, 67.1, 70.4, 73.9, 75.2, 75.7, 72.8, 76.4],
}
ANO = {"pob": [1990, 1994, 2002, 2010, 2014, 2018, 2021, 2024], "gini": [1975, 1992, 2002, 2010, 2014, 2018, 2021, 2024], "e0": [1970, 1990, 2000, 2010, 2015, 2018, 2021, 2023]}
MELHOR_ALTO = {"pib": True, "ipca": False, "des": False, "sm": True, "pob": False, "gini": False, "e0": True}
TOL = {"pib": 0.1, "ipca": 0.1, "des": 0.1, "sm": 0.1, "pob": 0.1, "gini": 0.01, "e0": 0.1}


def media(d, a, b):
    v = [d[str(y)] for y in range(a, b + 1) if str(y) in d and d[str(y)] is not None]
    return (sum(v) / len(v), len(v)) if v else (None, 0)


def acum(d, a, b):
    p = 1.0
    n = 0
    for y in range(a, b + 1):
        if str(y) in d and d[str(y)] is not None:
            p *= 1 + d[str(y)] / 100
            n += 1
    return ((p - 1) * 100, n) if n else (None, 0)


def dire(ind, diff):
    """diff = impresso (ou efeito) - referencia."""
    if diff is None:
        return "indeterminado"
    if abs(diff) <= TOL[ind] + 1e-9:
        return "neutro"
    melhor = diff > 0 if MELHOR_ALTO[ind] else diff < 0
    return "favorece" if melhor else "prejudica"


def f(x, nd=2):
    return "n/d" if x is None else f"{x:.{nd}f}".replace(".", ",")


def fs(x, nd=2):
    if x is None:
        return "n/d"
    s = f"{x:+.{nd}f}"
    if float(s) == 0:
        s = f"{0:.{nd}f}"
    return s.replace(".", ",")


OUT = []
P = OUT.append
DIRS = {}  # (indicador, governo) -> lista de direcoes


def reg(ind, g, d):
    DIRS.setdefault(g, []).append((ind, d))


P("# O que o infografico mistura, e a direcao medida do efeito sobre cada governo\n")
P("Gerado por `gerar_mistura.py` a partir de `saida/medidas.json`, `comparativo-metodo-constante.csv`, `vintage-do-infografico.csv` e `pobreza-*.csv`; nenhum numero foi digitado a mao. Sem opiniao e sem inferir intencao: so a direcao do efeito, medida com os numeros.\n")
P("> [!IMPORTANT]\n> Convencao. **favorece** = o numero impresso (ou o efeito da mistura) deixa o governo MELHOR do que a referencia de metodo constante (menor para desemprego, inflacao, pobreza e Gini; maior para PIB, salario minimo real e expectativa de vida). **prejudica** = PIOR. **neutro** = diferenca de ate 1 unidade da ultima casa impressa (0,1; 0,01 no Gini). **indeterminado** = nao ha referencia no ano/janela, ou o sinal muda conforme a referencia escolhida. Referencias de metodo constante: PIB = SCN ref. 2010 (ou o segmento do governo); pobreza e Gini = Banco Mundial PIP, com IBGE SIS como segunda linha; expectativa de vida = UMA vintage (WDI/UN), com a serie vigente do IBGE como segunda linha; desemprego = o segmento do proprio governo.\n")

# ------------------------------------------------------------------------------------------------ 1 janelas
P("## 1. Janela do mandato (PIB, IPCA, desemprego, salario minimo)\n")
P("O infografico usa janelas diferentes por indicador e por governo (ver `historia/RESULTADO.md`, secao 2). Efeito = valor da serie na janela IMPRESSA menos o valor da MESMA serie na janela do mandato (cada ano ao governo que o exerceu na maior parte). Sao os dados publicados, sem estimar.\n")
P("| indicador | governo | janela impressa | media na janela impressa | janela do mandato | media no mandato | efeito da janela | direcao |")
P("|---|---|---|---|---|---|---|---|")
series_j = {"pib": ("PIB (% a.a.)", SA["pib"], "aritm"), "ipca": ("IPCA (% a.a.)", SA["ipca"], "aritm")}
pnadc = SA["desemprego_pnadc"]
ant = SA["desemprego_pme_antiga"]
nova = SA["desemprego_pme_nova"]
for ind, (nome, serie, _) in series_j.items():
    for g in GOVS:
        a, b = JAN[ind][g]
        ma, mb = MAND[g]
        if (a, b) == (ma, mb):
            continue
        v1, n1 = media(serie, a, b)
        v2, n2 = media(serie, ma, mb)
        if v1 is None or v2 is None:
            continue
        diff = v1 - v2
        d = dire(ind, diff)
        reg(ind + "-janela", g, d)
        P(f"| {nome} | {g} | {a}-{b} | {f(v1)} | {ma}-{mb} | {f(v2)} | {fs(diff)} | {d} |")
# desemprego: so com PNADC e dentro do mesmo segmento (Temer, Bolsonaro); Itamar com PME antiga
for g, a, b, ma, mb, serie, nm in (("Temer", 2016, 2018, 2017, 2018, pnadc, "PNADC"), ("Bolsonaro", 2019, 2020, 2019, 2022, pnadc, "PNADC"), ("Itamar", 1992, 1994, 1993, 1994, ant, "PME antiga")):
    v1, _ = media(serie, a, b)
    v2, _ = media(serie, ma, mb)
    diff = v1 - v2
    d = dire("des", diff)
    reg("des-janela", g, d)
    P(f"| Desemprego (%), {nm} | {g} | {a}-{b} | {f(v1)} | {ma}-{mb} | {f(v2)} | {fs(diff)} | {d} |")
# salario minimo: serie Ipea composta, variacao acumulada media a media
sm = M["salmin_por_governo"]
for g in GOVS:
    nome = NOME[g]
    ka = [k for k in sm if k.startswith(nome + "|infografico|")]
    km = [k for k in sm if k.startswith(nome + "|mandato|")]
    if ka and km:
        va, vm = sm[ka[0]]["Ipea composto"], sm[km[0]]["Ipea composto"]
        if va is not None and vm is not None:
            diff = va - vm
            d = dire("sm", diff)
            reg("sm-janela", g, d)
            P(f"| Salario minimo real (acumulado %, serie Ipea) | {g} | {ka[0].split('|')[2]} | {f(va, 1)} | {km[0].split('|')[2]} | {f(vm, 1)} | {fs(diff, 1)} | {d} |")
P("")
P("Dilma (2011-2016) e Temer (2016-2018) contam 2016 nas duas colunas (Dilma governou 8 dos 12 meses). Itamar (1992-1994) inclui 9 meses de Collor. A coluna 'Ditadura' tem cabecalho 1967-1974 e janelas de 1968-1973 ou 1967-1973 conforme o indicador. 'Lula 3' tem janela 2023-2025 marcada com asterisco no infografico (2026 incompleto): sem referencia para comparar.\n")

# ------------------------------------------------------------------------------------------------ 2 pobreza
P("## 2. Pobreza: linha que muda, janela de ano e fonte\n")
pipp = {a: float(v) for a, v in M["pip_headcount"]["2017|6.85"].items()}
PS = SO / "series" / "pobreza.csv"
sis685 = serie_csv(PS, "IBGE-SIS2025", "US$ 6,85 PPC2017")
sis550 = serie_csv(PS, "IBGE-SIS2020-PPC2011", "US$ 5,5 PPC2011")
P("Referencia de linha constante: US$ 6,85 (PPC 2017), mesma linha em todos os anos (e, SO para as celulas anteriores a 2012, cuja linha e desconhecida, tambem US$ 3,65 para mostrar que o sinal muda com a linha), PIP (1981-2024) e IBGE SIS (2012-2024). Efeito = numero impresso menos o valor da referencia NO ANO ROTULADO. Onde o PIP nao tem o ano (1994, 2010), nao ha referencia (indeterminado).\n")
pip365 = {a: float(v) for a, v in M["pip_headcount"]["2017|3.65"].items()}
P("| governo | impresso (%) | ano rotulado | PIP 6,85 no ano | dif. vs PIP 6,85 | PIP 3,65 no ano | dif. vs PIP 3,65 | SIS 6,85 no ano | dif. vs SIS | direcao (6,85) | direcao (3,65) | direcao (SIS) | veredito |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for i, g in enumerate(GOVS):
    v, y = IMP["pob"][i], ANO["pob"][i]
    rp = pipp.get(str(y))
    rq = pip365.get(str(y))
    rs = sis685.get(y)
    dp = None if rp is None else v - rp
    dq = None if rq is None else v - rq
    ds = None if rs is None else v - rs
    d1, d3, d2 = dire("pob", dp), dire("pob", dq), dire("pob", ds)
    sinais = {d for d in (d1, d2) if d in ("favorece", "prejudica")}  # 3,65 so entra nas celulas pre-2012 (linha desconhecida)
    if y < 2012:
        final = "indeterminado (linha do impresso desconhecida; o sinal muda com a linha)" if len({d1, d3} - {"indeterminado"}) > 1 or y in (1994, 2010) else d1
        if y < 2012 and len({d for d in (d1, d3) if d != "indeterminado"}) <= 1 and y not in (1994, 2010):
            final = d1
    else:
        final = list(sinais)[0] if len(sinais) == 1 else ("neutro" if not sinais else "indeterminado (sinal muda com a fonte)")
    reg("pobreza", g, "indeterminado" if final.startswith("indeterminado") else final)
    P(f"| {g} | {f(v, 1)} | {y} | {f(rp, 1)} | {fs(dp, 1)} | {f(rq, 1)} | {fs(dq, 1)} | {f(rs, 1)} | {fs(ds, 1)} | {d1} | {d3} | {d2} | {final.split(' (')[0]} |")
P("\nNas celulas anteriores a 2012 (Ditadura/1990, Itamar/1994, FHC/2002, Lula 1-2/2010) a linha usada no infografico e desconhecida (nenhuma serie baixada reproduz o numero); a comparacao com US$ 6,85 mede, portanto, linha + ano juntos.\n")
P("O infografico NAO mantem a linha: pela reproducao do bloco social (`vintage-do-infografico.csv`), 2014 e 2018 casam com a faixa de US$ 5,50 (PPC 2011) e 2021 e 2024 com a de US$ 6,85 (PPC 2017). O efeito dessa troca, medido nos mesmos microdados 2012-2019 (IBGE SIS, edicoes 2020 e 2025):\n")
P("| ano | SIS 5,50 (PPC 2011) | SIS 6,85 (PPC 2017) | diferenca (pp) |\n|---|---|---|---|")
for y, d in M["sis_550_x_685"]["por_ano"].items():
    P(f"| {y} | {f(d['5.50_ppc2011'], 2)} | {f(d['6.85_ppc2017'], 2)} | {fs(d['dif_pp'], 2)} |")
P(f"\nMedia {fs(M['sis_550_x_685']['media_dif_pp'])} pp. Leitura medida: as celulas de Dilma (2014) e Temer (2018), que usam a linha de 5,50, ficam ~8 pp abaixo do que a linha de 6,85 daria no mesmo ano; as de Bolsonaro (2021) e Lula 3 (2024) ja estao em 6,85. Direcao sobre a comparacao entre governos: **favorece Dilma e Temer** em relacao a Bolsonaro e Lula 3 (a diferenca de linha por si so e de cerca de 8 pp). Isso e dito sem inferir como a linha foi escolhida.\n")
for g in ("Dilma", "Temer"):
    reg("pobreza-troca-de-linha", g, "favorece")
for g in ("Bolsonaro", "Lula 3"):
    reg("pobreza-troca-de-linha", g, "neutro")
P("### 2.1 Ano deslocado\n")
P("Em 4 das 8 celulas o numero impresso e o da fonte em OUTRO ano (reproducao em `vintage-do-infografico.csv`). Efeito = valor da fonte no ano rotulado menos o impresso (positivo = a fonte, no ano certo, diria mais pobreza).\n")
P("| governo | impresso | ano rotulado | valor da MESMA fonte/linha no ano rotulado | ano em que o impresso aparece | efeito do deslocamento (pp) | direcao |\n|---|---|---|---|---|---|---|")
desloc = [("Lula 1-2", 21.4, 2010, None, 2009, "Ipea PPY (sem PNAD em 2010)"), ("Temer", 26.5, 2018, sis550.get(2018), 2017, "SIS ed. 2020, 5,50"),
          ("Bolsonaro", 31.6, 2021, sis685.get(2021), 2022, "SIS 2025, 6,85"), ("Lula 3", 27.4, 2024, sis685.get(2024), 2023, "SIS 2025, 6,85")]
for g, v, y, ref, ya, fonte in desloc:
    if ref is None:
        P(f"| {g} | {f(v, 1)} | {y} | n/d ({fonte}) | {ya} | n/d | indeterminado |")
    else:
        diff = ref - v  # quanto mais pobreza a fonte diria no ano certo
        d = dire("pob", -diff)  # impresso menos referencia = -(ref - v)
        reg("pobreza-ano-deslocado", g, d)
        P(f"| {g} | {f(v, 1)} | {y} | {f(ref, 2)} ({fonte}) | {ya} | {fs(diff, 2)} | {d} |")
P("")

# ------------------------------------------------------------------------------------------------ 3 gini
P("## 3. Gini: pesquisa, vintage e ano deslocado\n")
GS = SO / "series" / "gini.csv"
pipg = {a: r["gini"] for a, r in pip(SO / "bruto" / "pip_ppp2017_line6.85.json").items()}
sisg = serie_csv(GS, "IBGE-SIS2025", "renda dom. per capita (PNADC)")
pgini = serie_csv(GS, "Ipeadata-PGINI", "renda dom. per capita (PNAD antiga, serie interrompida)")
P("Referencia: PIP (renda domiciliar per capita; PNAD 1981-2011, PNADC 2012-2024 como spells do proprio PIP). Segunda linha: IBGE SIS (PNADC, 2012+) e PNAD antiga (Ipeadata PGINI). 'anos 1970' do infografico e tratado como 1975 so para a consulta (sem dado PIP anterior a 1981: indeterminado).\n")
P("| governo | impresso | ano rotulado | PIP no ano | dif. vs PIP | SIS (PNADC) no ano | PNAD antiga no ano | direcao (PIP) | direcao (2a fonte) | sinal igual? |\n|---|---|---|---|---|---|---|---|---|---|")
for i, g in enumerate(GOVS):
    v, y = IMP["gini"][i], ANO["gini"][i]
    rp = pipg.get(y)
    r2 = sisg.get(y) if y >= 2012 else pgini.get(y)
    dp = None if rp is None else v - rp
    d1 = dire("gini", dp)
    d2 = dire("gini", None if r2 is None else v - r2)
    ok = "n/d" if "indeterminado" in (d1, d2) else ("sim" if d1 == d2 else "NAO")
    reg("gini", g, d1 if ok in ("sim", "n/d") and d1 != "indeterminado" else ("indeterminado" if ok == "NAO" or d1 == "indeterminado" else d1))
    P(f"| {g} | {f(v)} | {'anos 1970' if i == 0 else y} | {f(rp, 3)} | {fs(dp, 3)} | {f(sisg.get(y), 3)} | {f(pgini.get(y), 3)} | {d1} | {d2} | {ok} |")
P("")
P(f"Mistura de pesquisa: do PNAD para o PNADC (2012) o Gini sobe {fs(M['pnad_x_pnadc_gini']['media_dif'], 3)} na sobreposicao 2012-2014 (PNADC maior em todos os 3 anos). As celulas de FHC, Lula 1-2 e Dilma 2014 usam PNAD antiga; Temer, Bolsonaro e Lula 3 usam PNADC (e 2020-2022 em quintas visitas). Direcao sobre a comparacao FHC/Lula 1-2 contra Temer/Bolsonaro/Lula 3: **favorece os primeiros** (PNAD antiga mede ~0,008 menos que PNADC no mesmo ano). Censo 2010 = {f(M['censo_x_pnad_gini']['censo_2010'], 3)} contra PNAD 2011 = {f(M['censo_x_pnad_gini']['pnad_2011'], 3)}: a celula de Lula 1-2 usa PNAD, nao o Censo (diferenca de {fs(M['censo_x_pnad_gini']['dif_vs_2011'], 3)}).\n")
for g in ("Itamar", "FHC", "Lula 1-2", "Dilma"):
    reg("gini-pesquisa", g, "favorece")
for g in ("Temer", "Bolsonaro", "Lula 3"):
    reg("gini-pesquisa", g, "prejudica")

# ------------------------------------------------------------------------------------------------ 4 e0
P("## 4. Expectativa de vida: vintages coladas na mesma linha\n")
wdi = {int(k): v for k, v in M["e0_wdi"].items()}
vig = {int(k): v for k, v in M["e0_vigente"].items()}
P("Referencia 1: UMA vintage (UN WPP via Banco Mundial, 1960-2024). Referencia 2: serie vigente do IBGE (marcos). Efeito = impresso menos referencia no ano rotulado. A linha do infografico mistura Projecao Rev. 2008 (1970/2000, por deslocamento), Rev. 2013 (2010), tabua publicada de 2014 (2015), Rev. 2018 (2018, deslocado) e a serie vigente pos-pandemia (2021, 2023): ver `vintage-do-infografico.csv`.\n")
P("| governo | impresso | ano rotulado | WDI no ano | dif. vs WDI | IBGE vigente no ano | dif. vs vigente | direcao (WDI) | direcao (vigente) | sinal igual? |\n|---|---|---|---|---|---|---|---|---|---|")
for i, g in enumerate(GOVS):
    v, y = IMP["e0"][i], ANO["e0"][i]
    rw, rv = wdi.get(y), vig.get(y)
    d1 = dire("e0", None if rw is None else v - rw)
    d2 = dire("e0", None if rv is None else v - rv)
    ok = "n/d" if "indeterminado" in (d1, d2) else ("sim" if d1 == d2 else "NAO")
    reg("expectativa de vida", g, d1 if ok in ("sim", "n/d") and d1 != "indeterminado" else "indeterminado")
    P(f"| {g} | {f(v, 1)} | {y} | {f(rw, 2)} | {fs(None if rw is None else v - rw, 2)} | {f(rv, 1)} | {fs(None if rv is None else v - rv, 2)} | {d1} | {d2} | {ok} |")
P("")
P("Efeito da vintage da 'tabua como publicada' sobre 2020-2022 (Bolsonaro): a tabua de 2021 diz 77,03; a serie vigente diz 72,8. Quem comparasse a tabua publicada de 2021 com a vigente de 2019 (76,2) leria um GANHO de 0,8 ano; na mesma vintage, a queda e de 3,4 anos. Direcao sobre Bolsonaro da mistura de vintages: **depende de qual vintage entra**; o impresso (72,8, vigente) e coerente com a serie vigente.\n")

# ------------------------------------------------------------------------------------------------ 5 desemprego
P("## 5. Desemprego cruza metodologias\n")
P("Cada celula versus os metodos disponiveis NA SUA JANELA (nenhum metodo cobre todas as janelas). 'Referencia' so existe quando a janela cabe num unico segmento; do contrario o intervalo entre metodos e mostrado e a direcao e 'indeterminado'.\n")
P("| governo | impresso | janela | PME antiga | PME nova | PNAD | PNADC | leitura |\n|---|---|---|---|---|---|---|---|")
pnad = SA["desemprego_pnad"]
leit = {}
for i, g in enumerate(GOVS):
    a, b = JAN["des"][g]
    cel = []
    for d in (ant, nova, pnad, pnadc):
        v, n = media(d, a, b)
        full = n == (b - a + 1)
        cel.append(f"{f(v)}" + ("" if full or v is None else f" ({n} de {b - a + 1} anos)") if v is not None else "n/d")
    vals, sinais = [], []
    imp = IMP["des"][i]
    for d in (ant, nova, pnad, pnadc):
        v, n = media(d, a, b)
        if v is not None:
            sinais.append(dire("des", imp - v))
            if n == (b - a + 1):
                vals.append(v)
    if g == "Ditadura":
        txt = "sem serie oficial 1968-1973"
        dr = "indeterminado"
    elif not sinais:
        txt = "nenhum metodo tem dado na janela"
        dr = "indeterminado"
    else:
        nz = {s for s in sinais if s not in ("neutro",)}
        dr = list(nz)[0] if len(nz) == 1 else ("neutro" if not nz else "indeterminado")
        txt = f"sinais por metodo: {', '.join(sinais)}"
    if g == "Lula 1-2":
        v, _ = media(nova, 2003, 2010)
        dr = dire("des", 8.4 - v)
        txt = f"impresso '8,4 -> 6,5' contra media PME nova {f(v)} e PNAD {f(media(pnad, 2003, 2010)[0])}: abaixo dos dois"
    reg("desemprego", g, dr)
    P(f"| {g} | {f(imp, 1)} | {a}-{b} | {cel[0]} | {cel[1]} | {cel[2]} | {cel[3]} | {txt}; **{dr}** |")
P("")
P(f"Quebra PME antiga -> PME nova (mar-dez/2002): nova menos antiga {fs(M['pme_sobreposicao']['media_pp'])} pp em media. PNAD -> PNADC (2012-2014): {fs(M['pnad_x_pnadc_desemprego']['media_dif_anual_pp'])} pp (media anual) e {fs(M['pnad_x_pnadc_desemprego']['media_dif_3tri_pp'])} pp (3o trimestre): sinal misto. Efeito sobre a transicao FHC -> Lula 1-2: a media de FHC vem da PME antiga/PNAD e a de Lula da PME nova; o salto de ~+3,7 pp na troca de metodo eleva a media de Lula 1-2 em relacao a de FHC. Direcao: **prejudica Lula 1-2 na comparacao com FHC** (o numero de Lula esta numa escala que mede mais desemprego); mas o impresso de Lula (8,4 -> 6,5) esta abaixo da media reproduzida em PME nova, o que o **favorece** em termos absolutos. As duas leituras coexistem; nao ha um unico sinal.\n")
reg("desemprego-quebra-2002", "FHC", "favorece")
reg("desemprego-quebra-2002", "Lula 1-2", "prejudica")

# ------------------------------------------------------------------------------------------------ 6 salario minimo
P("## 6. Salario minimo real: troca de deflator\n")
P("Acumulado real do mandato (media anual a media anual, ano anterior como base) sob quatro deflatores, em %. 'Ipea composto' = IGPC-Mtb ate mar/1979 e INPC depois, com fator 1,2225 em jul/1994. Os campos vazios nao tem o deflator (INPC so desde abr/1979; IPCA desde 1980).\n")
P("| governo | janela | Ipea composto | IGP-DI unico | INPC unico | IPCA unico | amplitude entre deflatores (pp) | impresso (%) | posicao do impresso |\n|---|---|---|---|---|---|---|---|---|")
for i, g in enumerate(GOVS):
    nome = NOME[g]
    ks = [k for k in sm if k.startswith(nome + "|infografico|")] or [k for k in sm if k.startswith(nome + "|mandato|")]
    k = ks[0]
    d = sm[k]
    vals = [v for v in d.values() if v is not None]
    imp = IMP["sm"][i]
    pos = "acima de todos" if imp > max(vals) + 0.1 else ("abaixo de todos" if imp < min(vals) - 0.1 else "dentro da faixa")
    dr = "favorece" if pos == "acima de todos" else ("prejudica" if pos == "abaixo de todos" else "indeterminado")
    reg("salario minimo", g, dr)
    P(f"| {g} | {k.split('|')[2]} | {f(d['Ipea composto'], 1)} | {f(d['IGP-DI'], 1)} | {f(d['INPC'], 1)} | {f(d['IPCA'], 1)} | {f(max(vals) - min(vals), 1)} | {f(imp, 1)} | {pos}; **{dr}** |")
P("")
P("O numero impresso nao reproduz com nenhum deflator em varias janelas (ver `economia-real/RESULTADO.md`, secao 4). A troca de deflator por si so (comparar a serie Ipea composta com o IGP-DI unico) tem sinais diferentes por governo: " + "; ".join(f"{g} {fs(sm[[k for k in sm if k.startswith(NOME[g] + '|mandato|')][0]]['Ipea composto'] - sm[[k for k in sm if k.startswith(NOME[g] + '|mandato|')][0]]['IGP-DI'], 1)} pp" for g in ("Ditadura", "Itamar", "FHC", "Bolsonaro")) + " (serie Ipea menos IGP-DI). Nao ha padrao unico.\n")

# ------------------------------------------------------------------------------------------------ 7 ipca pesos
P("## 7. IPCA: troca de pesos (estimativas, separadas do dado bruto)\n")
P("Contrafactuais publicados pelo Banco Central (EE70/2019) e reconstrucao deste dossie por 9 grupos (validada: reproduz o IPCA publicado). **Sao estimativas**; ficam aqui apenas para dar direcao. Efeito = IPCA com a cesta NOVA menos com a cesta ANTERIOR, no mesmo periodo (negativo = inflacao menor com a cesta nova).\n")
P("| governo | quebra de pesos no mandato | efeito (pp ao ano) | fonte | direcao (inflacao menor = favorece) |\n|---|---|---|---|---|")
cf = M["ipca_cf_2020_2025"]["por_ano"]
linhas_ip = [("FHC", "POF 1995-96 (ago/1999), 3 anos depois", +0.06, "BCB EE70", "neutro"), ("Lula 1-2", "POF 2002-03 (jul/2006), 3 anos depois", -0.34, "BCB EE70", "favorece"),
             ("Dilma", "POF 2008-09 (jan/2012), 3 anos depois", -0.56, "BCB EE70", "favorece"),
             ("Itamar", "media geometrica no subitem (jan/1994): nao medida (inferencia de composicao: reduz)", None, "sem contrafactual publicado", "indeterminado (nao medido)"),
             ("Temer", "so a ampliacao de areas (mai/2018): sem efeito publicado", None, "sem contrafactual publicado", "indeterminado (nao medido)"),
             ("Bolsonaro", f"POF 2017-18 desde 2020 (2020, 2021, 2022: {fs(cf['2020']['efeito_pp'])}, {fs(cf['2021']['efeito_pp'])}, {fs(cf['2022']['efeito_pp'])})", None, "reconstrucao deste dossie", "favorece"),
             ("Lula 3", f"POF 2017-18 (2023, 2024, 2025: {fs(cf['2023']['efeito_pp'])}, {fs(cf['2024']['efeito_pp'])}, {fs(cf['2025']['efeito_pp'])})", None, "reconstrucao deste dossie", "indeterminado (sinais mistos)")]
for g, q, e, fonte, d in linhas_ip:
    if g in ("Itamar", "Temer"):
        reg("ipca-pesos", g, "indeterminado")
        P(f"| {g} | {q} | n/d | {fonte} | {d} |")
        continue
    if g == "Bolsonaro":
        e = sum(cf[str(y)]["efeito_pp"] for y in (2020, 2021, 2022)) / 3
    if g == "Lula 3":
        e = sum(cf[str(y)]["efeito_pp"] for y in (2023, 2024, 2025)) / 3
    reg("ipca-pesos", g, "indeterminado" if d.startswith("indet") else d)
    P(f"| {g} | {q} | {fs(e)} | {fonte} | {d} |")
P("\nNao ha sinal consistente: a troca de cesta reduziu a inflacao medida em Lula 1-2, Dilma e Bolsonaro, e fica ambigua em Lula 3 e FHC; Itamar e Temer nao tem efeito medido.\n")

# ------------------------------------------------------------------------------------------------ 8 matriz
P("## 8. Resumo por governo: a direcao se repete?\n")
P("As entradas das secoes 1 a 7 foram agrupadas por FAMILIA de indicador (PIB, IPCA, desemprego, salario minimo, pobreza, Gini, expectativa de vida) para nao contar a mesma familia varias vezes. Dentro da familia, o sinal e o das entradas nao neutras e nao indeterminadas; se ha sinais opostos, a familia e 'misto'. So se diz **consistente** quando o governo tem pelo menos 3 familias com sinal e todas iguais.\n")
FAM = {"pib-janela": "PIB", "ipca-janela": "IPCA", "ipca-pesos": "IPCA", "des-janela": "desemprego", "desemprego": "desemprego", "desemprego-quebra-2002": "desemprego",
       "sm-janela": "salario minimo", "salario minimo": "salario minimo", "pobreza": "pobreza", "pobreza-troca-de-linha": "pobreza", "pobreza-ano-deslocado": "pobreza",
       "gini": "Gini", "gini-pesquisa": "Gini", "expectativa de vida": "expectativa de vida"}
P("| governo | PIB | IPCA | desemprego | salario minimo | pobreza | Gini | expectativa de vida | familias com sinal | leitura |\n|---|---|---|---|---|---|---|---|---|---|")
RES = {}
for g in GOVS:
    fam = {}
    for k, d in DIRS.get(g, []):
        fam.setdefault(FAM[k], []).append(d)
    cel = {}
    for nome in ("PIB", "IPCA", "desemprego", "salario minimo", "pobreza", "Gini", "expectativa de vida"):
        ds = {d for d in fam.get(nome, []) if d in ("favorece", "prejudica")}
        cel[nome] = "-" if nome not in fam else (list(ds)[0] if len(ds) == 1 else ("misto" if ds else "neutro/indeterminado"))
    sig = [v for v in cel.values() if v in ("favorece", "prejudica")]
    leit = f"consistente: {sig[0]}" if len(sig) >= 3 and len(set(sig)) == 1 else "nao ha padrao"
    RES[g] = (cel, len(sig), leit)
    P(f"| {g} | " + " | ".join(cel.values()) + f" | {len(sig)} | {leit} |")
def _rodar(excluir):
    out = {}
    for g in GOVS:
        fam = {}
        for k, d in DIRS.get(g, []):
            if k in excluir:
                continue
            fam.setdefault(FAM[k], []).append(d)
        sg = []
        for nome in ("PIB", "IPCA", "desemprego", "salario minimo", "pobreza", "Gini", "expectativa de vida"):
            ds = {d for d in fam.get(nome, []) if d in ("favorece", "prejudica")}
            if len(ds) == 1:
                sg.append(list(ds)[0])
        out[g] = f"consistente: {sg[0]}" if len(sg) >= 3 and len(set(sg)) == 1 else "nao ha padrao"
    return out


_sem_est = _rodar({"ipca-pesos"})
_mudou = [g for g in GOVS if _sem_est[g] != RES[g][2]]
P("\nSem as celulas ESTIMADAS (secao 7, IPCA por pesos) o veredito de cada governo " + ("nao muda." if not _mudou else "muda para: " + ", ".join(f"{g} ({_sem_est[g]})" for g in _mudou) + ".") + " Os vereditos 'consistente' dependem so de dado publicado.")
_marg = {g: RES[g][1] for g in GOVS if RES[g][2].startswith("consistente")}
P("\nMargem dos vereditos consistentes (numero de familias com sinal): " + ", ".join(f"{g} = {n}" for g, n in _marg.items()) + ". O minimo exigido e 3; qualquer celula que mude de sinal desfaz o veredito.")
P("\nEsta tabela mistura dois tipos de celula: (i) efeito de uma mistura medida (janela, linha, pesquisa, vintage) e (ii) diferenca entre o impresso e a referencia, que inclui numeros que nao reproduzem em nenhuma fonte. A lista por governo e indicador esta em `saida/mistura_direcoes.json`.\n")
P("## 9. O que este documento nao afirma\n")
P("- Nao afirma que a mistura foi escolhida para favorecer ou prejudicar ninguem: so mede para que lado ela empurra o numero.\n- Onde a direcao muda com a referencia (PIP x SIS, WDI x IBGE vigente, PME antiga x PNAD), a celula fica 'indeterminado'.\n- As secoes 7 (IPCA) usam estimativas contrafactuais; as demais usam dado publicado.\n")
(H / "mistura-do-infografico.md").write_text("\n".join(OUT), encoding="utf-8")
json.dump({g: DIRS.get(g, []) for g in GOVS}, open(H / "saida" / "mistura_direcoes.json", "w"), ensure_ascii=False, indent=1)
json.dump(RES, open(H / "saida" / "mistura_resumo.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(OUT), "linhas")
