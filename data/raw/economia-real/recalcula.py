# Recalcula PIB, PIB per capita, desemprego e salario minimo real por janela de governo.
# Le SOMENTE os brutos desta pasta (baixados em 2026-10-19; hash em manifest.jsonl). Sem rede.
# Rode: python3 -I recalcula.py   (grava saida-recalcula.txt ao lado e imprime o mesmo texto)
import csv, json, math, pathlib, sys
from collections import defaultdict

H = pathlib.Path(__file__).resolve().parent
OUT = []


def p(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s)


def ipea(code, nivel=None):
    """Ipeadata ValoresSerie -> dict {(ano, mes): valor}; None descartado."""
    d = json.load(open(H / f"ipeadata-{code}-raw.json"))["value"]
    r = {}
    for x in d:
        if nivel is not None and x["NIVNOME"] != nivel:
            continue
        if x["VALVALOR"] is None:
            continue
        r[(int(x["VALDATA"][:4]), int(x["VALDATA"][5:7]))] = float(x["VALVALOR"])
    return r


def ipea_a(code, nivel=None):
    return {k[0]: v for k, v in ipea(code, nivel).items()}


def sgs(s):
    return {
        (int(r["data"][-4:]), int(r["data"][3:5])): float(r["valor"])
        for r in json.load(open(next(H.glob(f"bcb-sgs{s}-*raw.json"))))
    }


def fmt(x, n=2):
    return "n/d" if x is None else f"{x:.{n}f}"


def tab(cab, linhas):
    p("| " + " | ".join(cab) + " |")
    p("|" + "|".join(["---"] * len(cab)) + "|")
    for l in linhas:
        p("| " + " | ".join(str(c) for c in l) + " |")
    p("")


def status(inf, rep, tol_abs=0.3, tol_rel=0.05, exato=0.05):
    if rep is None:
        return "?"
    d = abs(inf - rep)
    if d <= exato:
        return "OK"
    if d <= tol_abs or d <= tol_rel * abs(inf):
        return "~"
    return "X"


# ============================ 1. PIB =====================================================
g = ipea_a("SCN10_PIBG10")  # var. real anual %, 1901-2025
idx = ipea_a("SCN10_PIB10")  # indice real base 2010=100, 1900-2025
sgs7326 = {k[0]: v for k, v in sgs(7326).items()}
sidra = {
    v["id"]: v["resultados"][0]["series"][0]["serie"]
    for v in json.load(open(H / "sidra-t6784-pib-percapita-raw.json"))
}
s9810 = {int(k): float(v) for k, v in sidra["9810"].items()}
s9814 = {int(k): float(v) for k, v in sidra["9814"].items()}
s93 = {int(k): float(v) * 1000 for k, v in sidra["93"].items()}

p("## 1.1 Consistencia interna e cruzamentos do PIB real anual")
inc = [
    (y, round((idx[y] / idx[y - 1] - 1) * 100, 3), round(g[y], 3))
    for y in range(1948, 2026)
    if abs((idx[y] / idx[y - 1] - 1) * 100 - g[y]) > 0.01
]
p(
    f"Anos 1948-2025 em que a razao do indice SCN10_PIB10 difere da taxa SCN10_PIBG10 em mais de 0,01 p.p.: {inc or 'nenhum'}. O script usa SEMPRE a taxa (SCN10_PIBG10) e compoe a media geometrica por produto das taxas."
)
dif = [(y, g[y], sgs7326[y]) for y in sorted(sgs7326) if y in g and abs(g[y] - sgs7326[y]) > 0.05]
p(f"SGS 7326 vs SCN10_PIBG10 (1963-2025): anos com diferenca > 0,05 p.p.: {dif or 'nenhum'}")
dif = [(y, g[y], s9810[y]) for y in sorted(s9810) if abs(g[y] - s9810[y]) > 0.05]
p(
    f"SIDRA t6784 var 9810 (arredondada a 0,1) vs SCN10_PIBG10 (1996-2023): anos com diferenca > 0,05 p.p.: {[(y, round(a, 2), b) for y, a, b in dif] or 'nenhum'}"
)
p("")

# populacao anual: DEPIS_POP (IBGE/Pop, serie anual 1872-2024, ancorada nos censos) em 1940-2024; 2025 = 2024 x crescimento de POP_PROJE 2025/2024.
# Verificacao: POP_PROJE (projecao rev. 2024, 1980+) e interpolacao log-linear dos censos (POPTOT) so como sensibilidade.
dep = {
    int(r["VALDATA"][:4]): float(r["VALVALOR"])
    for r in json.load(open(H / "ipeadata-DEPIS_POP-raw.json"))["value"]
}
proj = ipea_a("POP_PROJE", "Brasil")
pop = {y: dep[y] for y in range(1940, 2025)}
pop[2025] = dep[2024] * proj[2025] / proj[2024]
cen = {
    r["VALDATA"][:4]: r["VALVALOR"]
    for r in json.load(open(H / "ipeadata-POPTOT-raw.json"))["value"]
    if r["NIVNOME"] == "Brasil"
}
pts = {1940: cen["1940"], 1950: cen["1950"], 1960: cen["1960"], 1970: cen["1970"], 1980: proj[1980]}
anos = sorted(pts)
interp = {}
for y in range(1940, 1980):
    a_ = max(x for x in anos if x <= y)
    b_ = min(x for x in anos if x > y)
    interp[y] = math.exp(
        math.log(pts[a_]) + (math.log(pts[b_]) - math.log(pts[a_])) * (y - a_) / (b_ - a_)
    )

gpc_d = {
    y: ((1 + g[y] / 100) / (pop[y] / pop[y - 1]) - 1) * 100 for y in range(1941, 2026)
}  # derivado puro: (1+g)/(1+crescimento populacional)-1
gpc = {
    y: (s9814[y] if y in s9814 else gpc_d[y]) for y in gpc_d
}  # final: oficial SIDRA 9814 onde existe (1996-2023)
p("## 1.2 PIB per capita real")
p(
    "Oficial (IBGE SIDRA t6784 var 9814, 1996-2023, arredondado a 0,1). Fora disso, derivado: (1+PIB real)/(1+crescimento da populacao)-1, com populacao = Ipeadata DEPIS_POP (IBGE/Pop, anual, ancorada nos censos) em 1948-1995 e 2024, e 2025 = 2024 x crescimento de POP_PROJE. 'per capita final' usa o oficial onde existe e o derivado nos demais anos (1948-1995 e 2024-2025)."
)
gpc_i = {y: ((1 + g[y] / 100) / (interp[y] / interp[y - 1]) - 1) * 100 for y in range(1949, 1980)}
gpc_p = {y: ((1 + g[y] / 100) / (proj[y] / proj[y - 1]) - 1) * 100 for y in range(1981, 2026)}
p(
    f"Sensibilidade pre-1980: interpolacao log-linear dos censos (POPTOT) em vez de DEPIS_POP muda o crescimento per capita anual em no maximo {max(abs(gpc_i[y] - ((1 + g[y] / 100) / (pop[y] / pop[y - 1]) - 1) * 100) for y in gpc_i):.2f} p.p. e o nivel da populacao em no maximo {max(abs(interp[y] / pop[y] - 1) * 100 for y in range(1948, 1980)):.2f}%."
)
p(
    f"Sensibilidade 1981-2025: POP_PROJE (rev. 2024) em vez de DEPIS_POP muda o crescimento per capita anual em no maximo {max(abs(gpc_p[y] - ((1 + g[y] / 100) / (pop[y] / pop[y - 1]) - 1) * 100) for y in gpc_p if y <= 2024):.2f} p.p. (salto de {(proj[2000] / proj[1999] - 1) * 100:.2f}% em POP_PROJE 1999->2000; DEPIS_POP: {(pop[2000] / pop[1999] - 1) * 100:.2f}%)."
)
p(
    f"Derivado com DEPIS_POP vs oficial SIDRA 9814 em 1996-2023: maior diferenca {max(abs(gpc_d[y] - s9814[y]) for y in s9814):.2f} p.p. (SIDRA usa a populacao de revisao anterior); anos acima de 0,3 p.p.: {[(y, round(gpc_d[y], 2), s9814[y]) for y in sorted(s9814) if abs(gpc_d[y] - s9814[y]) > 0.3]}"
)
p("")


def pib_win(a, b):
    v = [g[y] for y in range(a, b + 1)]
    pr = 1.0
    for x in v:
        pr *= 1 + x / 100
    return sum(v) / len(v), (pr ** (1 / len(v)) - 1) * 100


def pc_win(a, b, x=None):
    x = x or gpc
    v = [x[y] for y in range(a, b + 1)]
    pr = 1.0
    for z in v:
        pr *= 1 + z / 100
    return sum(v) / len(v), (pr ** (1 / len(v)) - 1) * 100


INF_PIB = {  # nome: (a, b, valor do infografico)
    "Ditadura (Costa e Silva e Medici) 1968-1973": (1968, 1973, 11.1),
    "Itamar 1992-1994": (1992, 1994, 2.5),
    "FHC 1995-2002": (1995, 2002, 2.3),
    "Lula 1-2 2003-2010": (2003, 2010, 4.0),
    "Dilma 2011-2016": (2011, 2016, 1.4),
    "Temer 2016-2018": (2016, 2018, 0.7),
    "Bolsonaro 2019-2022": (2019, 2022, 1.8),
    "Lula 3 2023-2025*": (2023, 2025, 2.9),
}
p(
    "## 1.3 PIB real: janelas do infografico (anos-calendario inclusivos), media aritmetica e geometrica, PIB e PIB per capita"
)
L = []
for n, (a, b, v) in INF_PIB.items():
    ar, ge = pib_win(a, b)
    par, pge = pc_win(a, b)
    L.append([n, v, fmt(ar), fmt(ge), status(v, ar), status(v, ge), fmt(par), fmt(pge)])
tab(
    [
        "janela",
        "infografico",
        "PIB aritm.",
        "PIB geom.",
        "status aritm.",
        "status geom.",
        "per capita aritm.",
        "per capita geom.",
    ],
    L,
)
p("Per capita = final (oficial 9814 onde existe, derivado com DEPIS_POP nos demais anos).")

p(
    "## 1.4 PIB real: variantes de janela para cada coluna (qual recorte chega no valor do infografico?)"
)
L = []
for n, (a, b, v) in INF_PIB.items():
    best = []
    for aa in range(a - 1, a + 3):
        for bb in range(b - 2, b + 2):
            if bb < aa:
                continue
            if bb > 2025:
                continue
            ar, ge = pib_win(aa, bb)
            for tipo, val in (("aritm.", ar), ("geom.", ge)):
                if abs(val - v) <= 0.05:
                    best.append(f"{aa}-{bb} {tipo}={val:.2f}")
    L.append([n, v, "; ".join(best) or "nenhuma variante (+-1 a 2 anos nas pontas) fecha em 0,05"])
tab(["janela", "infografico", "variantes que reproduzem (|dif|<=0,05)"], L)

OMIT = [
    ("Castelo Branco 1964-1966", 1964, 1966),
    ("Costa e Silva+Medici 1967-1973", 1967, 1973),
    ("Costa e Silva+Medici 1967-1974 (periodo declarado)", 1967, 1974),
    ("Geisel 1974-1978", 1974, 1978),
    ("Figueiredo 1979-1984", 1979, 1984),
    ("Geisel+Figueiredo 1974-1985 (como pedido)", 1974, 1985),
    ("Sarney 1985-1989 (anos-calendario do mandato mar/85-mar/90)", 1985, 1989),
    ("Sarney 1985-1990 (como pedido)", 1985, 1990),
    ("Collor 1990-1992 (como pedido)", 1990, 1992),
    ("Collor+Itamar 1990-1994", 1990, 1994),
    ("Itamar 1993-1994 (anos plenos)", 1993, 1994),
    ("Ditadura inteira 1964-1985", 1964, 1985),
]
p("## 1.5 PIB real: o que o infografico omitiu (e recortes alternativos)")
L = []
for n, a, b in OMIT:
    ar, ge = pib_win(a, b)
    par, pge = pc_win(a, b)
    L.append(
        [
            n,
            fmt(ar),
            fmt(ge),
            fmt(par),
            fmt(pge),
            " ".join(f"{y}:{g[y]:.1f}" for y in range(a, b + 1)),
        ]
    )
tab(["janela", "PIB aritm.", "PIB geom.", "per capita aritm.", "per capita geom.", "anual %"], L)

p(
    "## 1.6 Serie anual completa 1948-2025 (PIB real var. %, per capita derivado %, SIDRA 9810/9814 quando existe, SGS 7326)"
)
L = []
for y in range(1948, 2026):
    L.append(
        [
            y,
            fmt(g[y]),
            fmt(gpc[y]) + ("" if y in s9814 else " (deriv.)"),
            s9810.get(y, "n/d"),
            s9814.get(y, "n/d"),
            fmt(sgs7326.get(y)),
        ]
    )
tab(["ano", "PIB SCN10_PIBG10", "per capita final", "SIDRA 9810", "SIDRA 9814", "SGS 7326"], L)

# janela exata via indice trimestral dessazonalizado (SCN104_PIBPMAS104, base media 1995=100, 1996T1+)
q = ipea("SCN104_PIBPMAS104")
import datetime


def mid(y, m):
    return datetime.date(y, m + 1, 15).toordinal()  # m = 1,4,7,10 -> meio do trimestre


pts_q = sorted((mid(y, m), math.log(v)) for (y, m), v in q.items())


def nivel_q(d):
    t = d.toordinal()
    for (t0, l0), (t1, l1) in zip(pts_q, pts_q[1:]):
        if t0 <= t <= t1:
            return l0 + (l1 - l0) * (t - t0) / (t1 - t0)
    return None


ibc = sgs(24364)


def exata(nome, d0, d1, m0, m1):
    anos = (d1.toordinal() - d0.toordinal() + 1) / 365.25
    lq = nivel_q(d1)
    rq = math.exp((lq - nivel_q(d0)) / anos) - 1
    # IBC-Br mensal (SGS 24364, proxy do BCB, nao e PIB): dezembro anterior -> mes final
    rm = (ibc[m1] / ibc[m0]) ** (12 / ((m1[0] - m0[0]) * 12 + m1[1] - m0[1])) - 1
    return [nome, d0.isoformat(), d1.isoformat(), fmt(anos), fmt(rq * 100), fmt(rm * 100)]


p("## 1.7 Janela exata do mandato (so 1996+; antes disso nao ha PIB trimestral nesta serie)")
p(
    "Metodo trimestral: nivel do indice dessazonalizado SCN104_PIBPMAS104 (media do trimestre tratada como o dia 15 do mes central), interpolacao log-linear no tempo; taxa anualizada = (N_fim/N_inicio)^(1/anos)-1. Metodo IBC-Br: SGS 24364 (indice mensal de atividade do BCB, proxy, nao e PIB), do mes anterior ao inicio ao mes final. Fronteiras: Dilma ate 31/08/2016, Temer de 01/09/2016, ambos como definido no briefing (o afastamento provisorio de 12/05/2016 nao e usado)."
)
L = [
    exata(
        "Dilma 01/01/2011-31/08/2016",
        datetime.date(2011, 1, 1),
        datetime.date(2016, 8, 31),
        (2010, 12),
        (2016, 8),
    ),
    exata(
        "Temer 01/09/2016-31/12/2018",
        datetime.date(2016, 9, 1),
        datetime.date(2018, 12, 31),
        (2016, 8),
        (2018, 12),
    ),
    exata(
        "Bolsonaro 01/01/2019-31/12/2022",
        datetime.date(2019, 1, 1),
        datetime.date(2022, 12, 31),
        (2018, 12),
        (2022, 12),
    ),
    exata(
        "FHC 01/01/1996-31/12/2002 (so 1996+; mandato comecou em 1995)",
        datetime.date(1996, 1, 1),
        datetime.date(2002, 12, 31),
        (2003, 1),
        (2003, 1),
    )
    if False
    else [
        "FHC",
        "-",
        "-",
        "-",
        "n/d (indice trimestral so a partir de 1996T1; mandato comeca 1995)",
        "n/d",
    ],
    exata(
        "Lula 1-2 01/01/2003-31/12/2010",
        datetime.date(2003, 1, 1),
        datetime.date(2010, 12, 31),
        (2003, 1),
        (2010, 12),
    )
    if False
    else ["Lula 1-2", "-", "-", "-", "ver nota", "ver nota"],
]
# Lula 1-2 e FHC: calculo direto no nivel trimestral (nao ha dezembro anterior no IBC-Br para 2003)
dl = (datetime.date(2010, 12, 31).toordinal() - datetime.date(2003, 1, 1).toordinal() + 1) / 365.25
L[4] = [
    "Lula 1-2 01/01/2003-31/12/2010",
    "2003-01-01",
    "2010-12-31",
    fmt(dl),
    fmt(
        (
            math.exp(
                (nivel_q(datetime.date(2010, 12, 31)) - nivel_q(datetime.date(2003, 1, 1))) / dl
            )
            - 1
        )
        * 100
    ),
    "n/d (IBC-Br comeca em jan/2003)",
]
L = [L[0], L[1], L[2], L[4]]
for nome, d0, d1 in (
    (
        "Dilma, janela civil 01/01/2011-31/12/2016",
        datetime.date(2011, 1, 1),
        datetime.date(2016, 12, 31),
    ),
    (
        "Temer, janela civil 01/01/2016-31/12/2018",
        datetime.date(2016, 1, 1),
        datetime.date(2018, 12, 31),
    ),
    (
        "FHC, so 15/02/1996-31/12/2002 (indice comeca no meio de 1996T1)",
        datetime.date(1996, 2, 15),
        datetime.date(2002, 12, 31),
    ),
    (
        "Lula 3, janela civil 01/01/2023-31/12/2025",
        datetime.date(2023, 1, 1),
        datetime.date(2025, 12, 31),
    ),
):
    an = (d1.toordinal() - d0.toordinal() + 1) / 365.25
    L.append(
        [
            nome,
            d0.isoformat(),
            d1.isoformat(),
            fmt(an),
            fmt((math.exp((nivel_q(d1) - nivel_q(d0)) / an) - 1) * 100),
            "-",
        ]
    )
tab(["mandato", "inicio", "fim", "anos", "PIB trimestral anualizado %", "IBC-Br anualizado %"], L)
dd = g
ar = [dd[y] for y in (2011, 2012, 2013, 2014, 2015)]
p(
    f"Contraste para Dilma: anos-calendario 2011-2016 = media aritmetica {pib_win(2011, 2016)[0]:.2f}, geometrica {pib_win(2011, 2016)[1]:.2f}; 2011-2015 = {pib_win(2011, 2015)[0]:.2f} / {pib_win(2011, 2015)[1]:.2f}. Temer: 2016-2018 = {pib_win(2016, 2018)[0]:.2f} / {pib_win(2016, 2018)[1]:.2f}; 2017-2018 = {pib_win(2017, 2018)[0]:.2f} / {pib_win(2017, 2018)[1]:.2f}."
)
p("")

# ============================ 2. DESEMPREGO ==============================================
pme_a = ipea("PME12_TDA12")  # PME antiga 1980-01..2002-12 (6 RMs, 15+, 30 dias)
pme_n = ipea("PAN12_TD12")  # PME nova 2002-03..2015-12 (6 RMs, 10+, semana de referencia)
pnad_ipea = ipea_a("Dese_Pnad", "Brasil")
pnad_disoc = ipea_a("DISOC_DESE")
pnadc = {
    int(k): float(v)
    for k, v in json.load(open(H / "sidra-pnadc-anual-t4562-raw.json"))[0]["resultados"][0][
        "series"
    ][0]["serie"].items()
}
pnadc_ipea = ipea_a("PAN_TDESOC")


def anual(m):
    t = defaultdict(list)
    for (y, mo), v in m.items():
        t[y].append(v)
    return {y: (sum(v) / len(v), len(v)) for y, v in t.items()}


A_a, A_n = anual(pme_a), anual(pme_n)
p("## 2.1 Primeira observacao de cada serie de desemprego baixada")
tab(
    ["serie", "codigo", "primeira obs.", "ultima obs.", "metodologia"],
    [
        [
            "PME antiga (6 RMs)",
            "Ipeadata PME12_TDA12",
            f"{min(pme_a)[0]}-{min(pme_a)[1]:02d}",
            f"{max(pme_a)[0]}-{max(pme_a)[1]:02d}",
            "15+ anos, desemprego aberto, ref. 30 dias, Recife/Salvador/BH/Rio/SP/POA",
        ],
        [
            "PME nova (6 RMs)",
            "Ipeadata PAN12_TD12",
            f"{min(pme_n)[0]}-{min(pme_n)[1]:02d}",
            f"{max(pme_n)[0]}-{max(pme_n)[1]:02d}",
            "10+ anos, desocupacao na semana de ref., mesmas 6 RMs",
        ],
        [
            "PNAD anual (Brasil)",
            "Ipeadata Dese_Pnad / DISOC_DESE",
            f"{min(pnad_ipea)}",
            f"{max(pnad_ipea)}",
            "10+ anos, semana de ref. (set.), cobertura nacional com exclusao da zona rural da regiao Norte (exceto TO) ate 2003 [fato metodologico do IBGE, nao verificado nesta colheita]; sem 1994, 2000, 2010 (PNAD nao realizada em ano de censo/1994)",
        ],
        [
            "PNAD Continua anual",
            "SIDRA t4562 var 4099",
            f"{min(pnadc)}",
            f"{max(pnadc)}",
            "14+ anos, semana de ref., media dos 4 trimestres",
        ],
        [
            "PNAD Continua (media dos meses)",
            "Ipeadata PAN_TDESOC",
            f"{min(pnadc_ipea)}",
            f"{max(pnadc_ipea)}",
            "14+ anos; media anual da serie mensal (trimestres moveis)",
        ],
    ],
)
p(
    f"Menor ano com qualquer observacao entre as 5 series acima: {min(min(pme_a)[0], min(pme_n)[0], min(pnad_ipea), min(pnadc))}. Nenhuma cobre 1968-1973."
)
p("")
p("## 2.2 Quebra metodologica PME antiga -> PME nova: meses em que as duas series existem")
L = []
for k in sorted(set(pme_a) & set(pme_n)):
    L.append([f"{k[0]}-{k[1]:02d}", pme_a[k], pme_n[k], fmt(pme_n[k] - pme_a[k], 1)])
tab(["mes", "PME antiga %", "PME nova %", "diferenca p.p."], L)

p(
    "## 2.3 Series anuais lado a lado (media simples dos meses; cada coluna e uma metodologia distinta, NAO emendar)"
)
L = []
for y in range(1980, 2026):
    L.append(
        [
            y,
            fmt(A_a[y][0]) + (f" ({A_a[y][1]}m)" if y in A_a and A_a[y][1] < 12 else "")
            if y in A_a
            else "-",
            fmt(A_n[y][0]) + (f" ({A_n[y][1]}m)" if A_n[y][1] < 12 else "") if y in A_n else "-",
            fmt(pnad_ipea.get(y)) if y in pnad_ipea else "-",
            fmt(pnad_disoc.get(y)) if pnad_disoc.get(y) is not None else "-",
            pnadc.get(y, "-"),
            fmt(pnadc_ipea.get(y)) if y in pnadc_ipea else "-",
        ]
    )
tab(
    [
        "ano",
        "PME antiga (15+, 30d)",
        "PME nova (10+, sem.)",
        "PNAD Ipeadata Dese_Pnad",
        "PNAD DISOC_DESE (Ipea)",
        "PNADC SIDRA 4562",
        "PNADC media Ipeadata",
    ],
    L,
)

SER = {
    "PME antiga": {y: v[0] for y, v in A_a.items() if v[1] == 12},
    "PME nova": {y: v[0] for y, v in A_n.items() if v[1] == 12},
    "PNAD Dese_Pnad": pnad_ipea,
    "PNAD DISOC_DESE": {y: v for y, v in pnad_disoc.items() if v is not None},
    "PNADC SIDRA": pnadc,
}
INF_DES = [
    ("Itamar 1992-1994", 1992, 1994, 6.8),
    ("FHC 1995-2002", 1995, 2002, 7.7),
    ("Lula 2003-2010 (8,4->6,5: media)", 2003, 2010, 7.45),
    ("Dilma 2011-2016", 2011, 2016, 6.7),
    ("Temer 2016-2018", 2016, 2018, 12.3),
    ("Bolsonaro 2019-2022", 2019, 2022, 13.2),
    ("Lula 3 2023-2025*", 2023, 2025, 9.3),
    ("Ditadura 1968-1973", 1968, 1973, 3.7),
]
p(
    "## 2.4 Media da janela do infografico em cada metodologia (so quando todos os anos da janela existem)"
)
L = []
for n, a, b, v in INF_DES:
    row = [n, v]
    for s, d in SER.items():
        ys = range(a, b + 1)
        if all(y in d for y in ys):
            m = sum(d[y] for y in ys) / len(ys)
            row.append(f"{m:.2f} [{status(v, m)}]")
        else:
            ok = [y for y in ys if y in d]
            if len(ok) * 2 < len(list(ys)):
                row.append("n/d" if not ok else f"so {len(ok)} de {len(list(ys))} anos")
            else:
                m = sum(d[y] for y in ok) / len(ok)
                row.append(
                    f"{m:.2f} [{status(v, m)}] (so {len(ok)} de {len(list(ys))} anos; faltam {[y for y in ys if y not in d]})"
                )
    L.append(row)
tab(["janela", "infografico"] + list(SER), L)
p(
    "Legenda: [OK] |dif|<=0,05; [~] dentro de 0,3 p.p. ou 5% relativo; [X] fora. 'Lula' compara a media dos dois extremos 8,4 e 6,5 (7,45) apenas como referencia; o infografico mostra um par inicio->fim."
)
p("")

p("## 2.5 Testes especificos por coluna")
p("### Lula 1-2 '8,4 -> 6,5' como par inicio->fim (anos de ponta em cada serie)")
L = []
for s, d in SER.items():
    for a, b in ((2003, 2010), (2002, 2009), (2003, 2009), (2002, 2010), (2004, 2010)):
        if a in d and b in d:
            L.append(
                [
                    s,
                    f"{a}->{b}",
                    f"{d[a]:.2f} -> {d[b]:.2f}",
                    status(8.4, d[a]) + "/" + status(6.5, d[b]),
                ]
            )
tab(["serie", "pontas", "valores", "status (inicio/fim)"], L)
p("### Pares (inicio -> fim) em dezembro/janeiro mensal da PME nova e PME antiga")
for lab, k0, k1 in (
    ("PME nova dez/2003->dez/2010", (2003, 12), (2010, 12)),
    ("PME nova jan/2003->dez/2010", (2003, 1), (2010, 12)),
):
    if k0 in pme_n and k1 in pme_n:
        p(f"- {lab}: {pme_n[k0]} -> {pme_n[k1]}")
p("")
pc_m = sgs(24369) if any(H.glob("bcb-sgs24369-*raw.json")) else None
p("### Bolsonaro '13,2 (2019-2020 pico)'")
p(
    f"- PNADC SIDRA anual 2019: {pnadc[2019]}, 2020: {pnadc[2020]}, 2021: {pnadc[2021]}, 2022: {pnadc[2022]}. Media 2019-2022 = {sum(pnadc[y] for y in range(2019, 2023)) / 4:.2f}; media 2019-2020 = {(pnadc[2019] + pnadc[2020]) / 2:.2f}; maximo anual = {max(pnadc[y] for y in range(2019, 2023))} (2021)."
)
if pc_m:
    mx = max((v, k) for k, v in pc_m.items() if 2019 <= k[0] <= 2022)
    mx2 = max((v, k) for k, v in pc_m.items() if 2019 <= k[0] <= 2020)
    p(
        f"- PNADC trimestre movel (SGS 24369), maximo em 2019-2022: {mx[0]} (trimestre movel terminado em {mx[1][0]}-{mx[1][1]:02d}); maximo em 2019-2020: {mx2[0]} ({mx2[1][0]}-{mx2[1][1]:02d}). Valores mensais de 13,2 em qualquer trimestre movel: {[k for k, v in pc_m.items() if abs(v - 13.2) < 0.051]}"
    )
p("")
qf = next(H.glob("sidra-pnadc-trimestral-t4099-*raw.json"), None)
if qf:
    qd = {
        k: float(v)
        for k, v in json.load(open(qf))[0]["resultados"][0]["series"][0]["serie"].items()
    }

    def qs(a, b):
        return {k: v for k, v in qd.items() if a <= int(k[:4]) <= b}

    for lab, a, b in (
        ("2019-2022", 2019, 2022),
        ("2019-2020", 2019, 2020),
        ("2023-2025", 2023, 2025),
    ):
        s = qs(a, b)
        mk = max(s, key=s.get)
        p(
            f"- PNADC trimestral (SIDRA t4099), {lab}: maximo {s[mk]} no trimestre {mk[:4]}T{int(mk[4:])}; media dos {len(s)} trimestres {sum(s.values()) / len(s):.2f}; trimestres com valor entre 13,15 e 13,25: {[k for k, x in s.items() if 13.15 <= x <= 13.25]}; entre 9,25 e 9,35: {[k for k, x in s.items() if 9.25 <= x <= 9.35]}"
        )
    p(
        "- PNADC trimestral 2019-2021 completo: "
        + ", ".join(f"{k[:4]}T{int(k[4:])}={v}" for k, v in qs(2019, 2021).items())
    )
p("### Lula 3 '9,3*' (2023-2025)")
p(
    f"- PNADC SIDRA anual 2023: {pnadc[2023]}, 2024: {pnadc[2024]}, 2025: {pnadc[2025]}; media = {sum(pnadc[y] for y in (2023, 2024, 2025)) / 3:.2f}."
)
if pc_m:
    mx = max((v, k) for k, v in pc_m.items() if k[0] >= 2023)
    p(
        f"- PNADC trimestre movel (SGS 24369), maximo desde jan/2023: {mx[0]} (terminado em {mx[1][0]}-{mx[1][1]:02d}); meses com 9,3: {[k for k, v in pc_m.items() if k[0] >= 2022 and abs(v - 9.3) < 0.051]}; valores dez/2022-mar/2023: {[(k, pc_m[k]) for k in sorted(pc_m) if (2022, 10) <= k <= (2023, 6)]}"
    )
p("")

p(
    "## 2.6 Caca ao valor: qual (serie, recorte) reproduz cada numero de desemprego do infografico (|dif|<=0,05)?"
)
p(
    "Recortes testados: valor de um ano isolado em [a-1, b+1], ou media anual de [a', b'] com a' em a-1..a+1 e b' em b-1..b+1. Coincidencia numerica nao e prova de origem: lista candidatos, nao fonte."
)
ALVOS = [
    ("Itamar 6,8", 1992, 1994, 6.8),
    ("FHC 7,7", 1995, 2002, 7.7),
    ("Lula inicio 8,4", 2003, 2003, 8.4),
    ("Lula fim 6,5", 2010, 2010, 6.5),
    ("Dilma 6,7", 2011, 2016, 6.7),
    ("Temer 12,3", 2016, 2018, 12.3),
    ("Bolsonaro 13,2", 2019, 2022, 13.2),
    ("Lula 3 9,3", 2023, 2025, 9.3),
    ("Ditadura 3,7", 1968, 1973, 3.7),
]
L = []
for n, a, b, v in ALVOS:
    hits = []
    for s, d in SER.items():
        for y in range(a - 1, b + 2):
            if y in d and abs(d[y] - v) <= 0.05:
                hits.append(f"{s}: ano {y} = {d[y]:.2f}")
        for aa in range(a - 1, a + 2):
            for bb in range(max(aa + 1, b - 1), b + 2):
                ys = range(aa, bb + 1)
                if all(y in d for y in ys):
                    m = sum(d[y] for y in ys) / len(ys)
                    if abs(m - v) <= 0.05:
                        hits.append(f"{s}: media {aa}-{bb} = {m:.2f}")
    L.append([n, "; ".join(hits) or "nenhum"])
tab(["numero", "candidatos que coincidem (anual)"], L)

# ============================ 3. SALARIO MINIMO REAL ======================================
sr = ipea(
    "GAC12_SALMINRE12"
)  # R$ do ultimo mes (set/2026), Ipea; deflator IGPC-Mtb ate mar/1979, INPC depois
sn = ipea("MTE12_SALMIN12")  # nominal vigente (R$)


def mean_y(m, y):
    v = [m[(y, mo)] for mo in range(1, 13) if (y, mo) in m]
    return sum(v) / len(v) if len(v) == 12 else None


def var_(a, b):
    return (b / a - 1) * 100


def metodos(m, a, b):
    r = {}
    r["dez(a-1)->dez(b)"] = var_(m[(a - 1, 12)], m[(b, 12)]) if (a - 1, 12) in m else None
    r["dez(a)->dez(b)"] = var_(m[(a, 12)], m[(b, 12)])
    ma, mb, mp = mean_y(m, a), mean_y(m, b), mean_y(m, a - 1)
    r["media(a-1)->media(b)"] = var_(mp, mb) if mp else None
    r["media(a)->media(b)"] = var_(ma, mb)
    r["jan(a)->dez(b)"] = var_(m[(a, 1)], m[(b, 12)])
    return r


INF_SM = [
    ("Ditadura 1968-1973", 1968, 1973, 42.8),
    ("Itamar 1992-1994", 1992, 1994, -13.9),
    ("FHC 1995-2002", 1995, 2002, 4.8),
    ("Lula 2003-2010", 2003, 2010, 58.5),
    ("Dilma 2011-2016", 2011, 2016, 8.0),
    ("Temer 2016-2018", 2016, 2018, 1.1),
    ("Bolsonaro 2019-2022", 2019, 2022, 0.9),
    ("Lula 3 2023-2025*", 2023, 2025, 12.6),
]
p(
    "## 3.1 Salario minimo real (Ipeadata GAC12_SALMINRE12, R$ de set/2026): variacao por janela, 5 convencoes de ponta"
)
p(
    "Mes mais recente da serie real: "
    + f"{max(sr)} = {sr[max(sr)]}. Variacao '%' entre as pontas indicadas (a = ano inicial da janela, b = ano final)."
)
L = []
for n, a, b, v in INF_SM:
    mt = metodos(sr, a, b)
    L.append(
        [n, v]
        + [
            f"{x:.1f} [{status(v, x, tol_abs=0.3, tol_rel=0.05, exato=0.1)}]"
            if x is not None
            else "n/d"
            for x in mt.values()
        ]
    )
tab(["janela", "infografico"] + list(metodos(sr, 2003, 2010)), L)
p(
    "Para salario minimo: [OK] = |dif|<=0,1; [~] = dentro de 0,3 p.p. ou 5% relativo (regra do briefing)."
)
p("")
p("## 3.2 Salario minimo real: o que o infografico omitiu")
OM_SM = [
    ("Castelo Branco 1964-1966", 1964, 1966),
    ("Ditadura 1964-1985", 1964, 1985),
    ("Geisel 1974-1978", 1974, 1978),
    ("Figueiredo 1979-1984", 1979, 1984),
    ("Sarney 1985-1989", 1985, 1989),
    ("Sarney 1985-1990 (como pedido)", 1985, 1990),
    ("1985-1992 (como pedido)", 1985, 1992),
    ("Collor 1990-1992", 1990, 1992),
    ("Costa e Silva+Medici 1967-1973", 1967, 1973),
    ("Costa e Silva+Medici 1968-1973", 1968, 1973),
]
L = []
for n, a, b in OM_SM:
    L.append([n] + [fmt(x, 1) for x in metodos(sr, a, b).values()])
tab(["janela"] + list(metodos(sr, 2003, 2010)), L)
p("### Serie anual do salario minimo real (media dos 12 meses; R$ de set/2026) e variacao anual")
L = []
for y in range(1960, 2026):
    ma, mp = mean_y(sr, y), mean_y(sr, y - 1)
    L.append([y, f"{ma:.0f}", f"{sr[(y, 12)]:.0f}", fmt(var_(mp, ma), 1)])
tab(["ano", "media anual", "dezembro", "var. media anual %"], L)

# deflatores alternativos (pos-1980): nominal MTE12_SALMIN12 / IPCA, INPC; pre-1980: nominal / IGP-DI
igpdi = ipea("IGP12_IGPDI12")


def acum(serie_pct, de, ate):
    f = 1.0
    for y in range(de[0], ate[0] + 1):
        for mo in range(1, 13):
            if de < (y, mo) <= ate:
                f *= 1 + serie_pct[(y, mo)] / 100
    return f


ipca, inpc = sgs(433), sgs(188)


def real_alt(defl_fn, a, b, tipo):
    """variacao do nominal deflacionado entre pontas (dez/dez a-1->b se tipo=='dd')."""
    if tipo == "dd":
        k0, k1 = (a - 1, 12), (b, 12)
    r = (sn[k1] / sn[k0]) / defl_fn(k0, k1)
    return (r - 1) * 100


def defl_idx(ix):
    return lambda k0, k1: ix[k1] / ix[k0]


def defl_pct(s):
    return lambda k0, k1: acum(s, k0, k1)


p(
    "## 3.3 Robustez ao deflator: nominal (MTE12_SALMIN12) deflacionado por outros indices, dez(a-1)->dez(b)"
)
L = []
for n, a, b, v in INF_SM:
    row = [n, v, fmt(var_(sr[(a - 1, 12)], sr[(b, 12)]), 1)]
    for nome, fn, ini in (
        ("IGP-DI", defl_idx(igpdi), 1944),
        ("IPCA", defl_pct(ipca), 1980),
        ("INPC", defl_pct(inpc), 1979),
    ):
        row.append(fmt(real_alt(fn, a, b, "dd"), 1) if a - 1 >= ini + 1 else "n/d")
    L.append(row)
tab(
    [
        "janela",
        "infografico",
        "Ipeadata real",
        "nominal/IGP-DI",
        "nominal/IPCA (SGS 433)",
        "nominal/INPC (SGS 188)",
    ],
    L,
)
p("### 1964-1985, 1985-1992, 1974-1985 e 1967-1973 com IGP-DI como deflator alternativo (dez/dez)")
for n, a, b in (
    ("1964-1985", 1964, 1985),
    ("1985-1992", 1985, 1992),
    ("1967-1973", 1967, 1973),
    ("1968-1973", 1968, 1973),
):
    p(
        f"- {n}: Ipeadata real {var_(sr[(a - 1, 12)], sr[(b, 12)]):.1f}%; nominal/IGP-DI {real_alt(defl_idx(igpdi), a, b, 'dd'):.1f}%"
    )
p("")
# verificacao: Ipeadata real reproduzido por nominal / INPC a partir de abr/1979
p(
    "## 3.4 Verificacao do deflator do Ipeadata: razao real(t)/real(s) vs nominal(t)/nominal(s)/INPC acumulado (mensal, de abr/1979)"
)
L = []
for s, t in (
    ((1980, 12), (1989, 12)),
    ((1995, 1), (2002, 12)),
    ((2003, 1), (2010, 12)),
    ((2018, 12), (2025, 12)),
):
    r_ip = sr[t] / sr[s]
    r_in = (sn[t] / sn[s]) / acum(inpc, s, t)
    L.append(
        [
            f"{s[0]}-{s[1]:02d} -> {t[0]}-{t[1]:02d}",
            f"{r_ip:.4f}",
            f"{r_in:.4f}",
            f"{(r_in / r_ip - 1) * 100:+.2f}%",
        ]
    )
tab(["intervalo", "Ipeadata real (razao)", "nominal/INPC (razao)", "diferenca"], L)
s, t = (1994, 1), (1995, 1)
p(
    f"Cruzando jul/1994 (troca de unidade): Ipeadata real {sr[t] / sr[s]:.4f}; nominal/INPC {(sn[t] / sn[s]) / acum(inpc, s, t):.4f}; com fator 1,2225 sobre o deflator de jul/1994: {(sn[t] / sn[s]) / (acum(inpc, s, t) * 1.2225):.4f}"
)
p("")

# caca ao valor do salario minimo
ix_ipca = {}
acc = 1.0
for y in range(1980, 2027):
    for mo in range(1, 13):
        if (y, mo) in ipca:
            acc *= 1 + ipca[(y, mo)] / 100
            ix_ipca[(y, mo)] = acc
REAIS = {
    "Ipeadata real (INPC desde abr/1979)": sr,
    "nominal/IGP-DI": {k: sn[k] / igpdi[k] for k in sn if k in igpdi},
    "nominal/IPCA (1980+)": {k: sn[k] / ix_ipca[k] for k in sn if k in ix_ipca},
}


def pontos(m, y):
    r = {}
    if (y, 1) in m:
        r[f"jan/{y}"] = m[(y, 1)]
    if (y, 12) in m:
        r[f"dez/{y}"] = m[(y, 12)]
    mm = mean_y(m, y)
    if mm:
        r[f"media {y}"] = mm
    return r


p(
    "## 3.5 Caca ao valor: qual par de pontas (jan/dez/media anual) reproduz cada variacao do infografico (|dif|<=0,1)?"
)
p(
    "Pontas iniciais em a-2..a+1; finais em b-1..b+1 (b+1 so ate 2025). Coincidencia numerica nao e prova de origem."
)
L = []
for n, a, b, v in INF_SM:
    hits = []
    for rn, m in REAIS.items():
        for y0 in range(a - 2, a + 2):
            for y1 in range(max(b - 1, y0 + 1), min(b + 1, 2025) + 1):
                p0, p1 = pontos(m, y0), pontos(m, y1)
                for k0, x0 in p0.items():
                    for k1, x1 in p1.items():
                        if abs(var_(x0, x1) - v) <= 0.1:
                            hits.append(f"{rn}: {k0}->{k1} = {var_(x0, x1):.1f}")
    L.append([n, v, "; ".join(hits[:6]) or "nenhum", len(hits)])
tab(["janela", "infografico", "primeiros candidatos", "total de coincidencias"], L)
v = [(var_(mean_y(sr, y - 1), mean_y(sr, y)), y) for y in range(1960, 2026)]
ar = lambda a, b: sum(x for x, y in v if a <= y <= b) / (b - a + 1)
p(
    f"Media aritmetica das variacoes anuais da media anual (Ipeadata real): 1968-1973 = {ar(1968, 1973):.1f}; 1992-1994 = {ar(1992, 1994):.1f}; 1995-2002 = {ar(1995, 2002):.1f}; 2003-2010 = {ar(2003, 2010):.1f}; 2011-2016 = {ar(2011, 2016):.1f}; 2016-2018 = {ar(2016, 2018):.1f}; 2019-2022 = {ar(2019, 2022):.1f}; 2023-2025 = {ar(2023, 2025):.1f}"
)
mx = max((sr[(y, m)], (y, m)) for y in range(1960, 1976) for m in range(1, 13) if (y, m) in sr)
p(
    f"Maior alta pico-vale possivel em 1964-1975 (Ipeadata real): max {max(sr[(y, m)] for y in range(1964, 1976) for m in range(1, 13) if (y, m) in sr):.0f} / min {min(sr[(y, m)] for y in range(1964, 1976) for m in range(1, 13) if (y, m) in sr):.0f}"
)
p("")

p(
    "### Varredura mensal exaustiva (Ipeadata real): inicio em qualquer mes de a-1..a, fim em qualquer mes de b..b+1"
)
for n, a, b, v in INF_SM:
    ini = [k for k in sorted(sr) if a - 1 <= k[0] <= a]
    fim = [k for k in sorted(sr) if b <= k[0] <= min(b + 1, 2026)]
    hits = [(k0, k1) for k0 in ini for k1 in fim if abs(var_(sr[k0], sr[k1]) - v) <= 0.1]
    p(
        f"- {n} ({v}): {len(hits)} pares de {len(ini) * len(fim)}; "
        + (
            "; ".join(f"{k0[0]}-{k0[1]:02d}->{k1[0]}-{k1[1]:02d}" for k0, k1 in hits[:6])
            or "nenhum"
        )
    )
p(
    f"- Nota FHC: o minimo foi a R$ 100 em mai/1995; mai/1995->dez/2002 (Ipeadata real) = {var_(sr[(1995, 5)], sr[(2002, 12)]):.1f}%; jun/1995->dez/2002 = {var_(sr[(1995, 6)], sr[(2002, 12)]):.1f}%"
)
p(
    f"- Nota Itamar: serie mensal em alta inflacao oscila (1993: min {min(sr[(1993, m)] for m in range(1, 13)):.0f}, max {max(sr[(1993, m)] for m in range(1, 13)):.0f}); dez/1992->dez/1994 = {var_(sr[(1992, 12)], sr[(1994, 12)]):.1f}%; out/1992->dez/1994 = {var_(sr[(1992, 10)], sr[(1994, 12)]):.1f}%; jan/1993->dez/1994 = {var_(sr[(1993, 1)], sr[(1994, 12)]):.1f}%"
)
p("")

with open(H / "saida-pib-anual-1948-2025.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(
        [
            "ano",
            "pib_real_var_pct_SCN10_PIBG10",
            "pib_percapita_var_pct_final",
            "percapita_origem",
            "pib_percapita_derivado_puro",
            "sidra_9810",
            "sidra_9814",
            "sgs_7326",
        ]
    )
    for y in range(1948, 2026):
        w.writerow(
            [
                y,
                round(g[y], 4),
                round(gpc[y], 4),
                "oficial_sidra_9814" if y in s9814 else "derivado",
                round(gpc_d[y], 4),
                s9810.get(y, ""),
                s9814.get(y, ""),
                sgs7326.get(y, ""),
            ]
        )
with open(H / "saida-desemprego-anual.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(
        [
            "ano",
            "PME_antiga_15mais_30d_6RMs",
            "meses_PME_antiga",
            "PME_nova_10mais_semana_6RMs",
            "meses_PME_nova",
            "PNAD_Dese_Pnad_Brasil",
            "PNAD_DISOC_DESE_Brasil",
            "PNADC_SIDRA_4562",
            "PNADC_media_Ipeadata_PAN_TDESOC",
        ]
    )
    for y in range(1980, 2026):
        w.writerow(
            [
                y,
                round(A_a[y][0], 3) if y in A_a else "",
                A_a[y][1] if y in A_a else "",
                round(A_n[y][0], 3) if y in A_n else "",
                A_n[y][1] if y in A_n else "",
                round(pnad_ipea[y], 3) if y in pnad_ipea else "",
                round(pnad_disoc[y], 3) if pnad_disoc.get(y) is not None else "",
                pnadc.get(y, ""),
                round(pnadc_ipea[y], 3) if y in pnadc_ipea else "",
            ]
        )
with open(H / "saida-salmin-real-anual.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(
        ["ano", "media_anual_real_R$_set2026", "dezembro_real_R$_set2026", "var_media_anual_pct"]
    )
    for y in range(1948, 2026):
        w.writerow(
            [
                y,
                round(mean_y(sr, y), 2),
                round(sr[(y, 12)], 2),
                round(var_(mean_y(sr, y - 1), mean_y(sr, y)), 3),
            ]
        )
open(H / "saida-recalcula.txt", "w").write("\n".join(OUT) + "\n")
