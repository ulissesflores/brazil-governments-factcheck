"""Mede, por SOBREPOSICAO de dados baixados, o efeito das quebras e revisoes das series de mundo/.

Sem rede. Le so bruto. Saidas: mundo/medidas_efeito.csv (uma linha por medida) e mundo/quebras.csv.
Rodar: python3 -I .../mundo/scripts/medir.py
Nao ha escolha depois do resultado: os pares comparados (versoes, fontes) foram fixados pela existencia dos brutos.
"""
import csv
import json
import statistics as st
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
import construir as cn  # noqa: E402
import xlsx_min as xl  # noqa: E402

REFS = ["ARG", "CHL", "COL", "MEX", "PER", "URY", "VEN"]
OUTRAS = REFS + ["WLD", "LCN", "UMC"]
MED = []  # linhas de medidas_efeito.csv


def med(medida, descricao, alvo, estat, valor, n="", nota=""):
    MED.append(dict(medida=medida, descricao=descricao, alvo=alvo, estatistica=estat,
                    valor=(round(valor, 4) if isinstance(valor, float) else valor), n=n, nota=nota))


arquivo = cn.arquivo


def pct(a, b):
    return (b / a - 1) * 100


# ---------- A. troca de base do PPC no WDI (PIB per capita) ----------
def ppc_wdi(v_old, v_new, rotulo):
    old, new = arquivo("NY.GDP.PCAP.PP.KD", v_old), arquivo("NY.GDP.PCAP.PP.KD", v_new)
    anos = sorted({a for (u, a) in old if (u, a) in new and a >= 1990})
    res = {}
    for u in cn.UNIDADES:
        xs = [pct(old[(u, a)], new[(u, a)]) for a in anos if (u, a) in old and (u, a) in new]
        if xs:
            res[u] = xs
            med(rotulo, f"variacao % do nivel do PIB pc PPC: versao {v_new} sobre {v_old}", u, "mediana", st.median(xs), len(xs), f"min {min(xs):.2f} max {max(xs):.2f}")
    # efeito sobre a razao Brasil / referencia (o que importa para 'Brasil menos referencia')
    for u in OUTRAS:
        rs = []
        for a in anos:
            if all(k in d for d in (old, new) for k in ((u, a), ("BRA", a))):
                rs.append(pct(old[("BRA", a)] / old[(u, a)], new[("BRA", a)] / new[(u, a)]))
        if rs:
            med(rotulo, f"variacao % da razao BRA/ref do PIB pc PPC: {v_new} sobre {v_old}", f"BRA/{u}", "mediana", st.median(rs), len(rs), f"min {min(rs):.2f} max {max(rs):.2f}")
    return res


# ---------- B. revisoes WDI dos demais indicadores ----------
INDS = ["NY.GDP.MKTP.KD.ZG", "SP.DYN.LE00.IN", "SP.DYN.IMRT.IN", "VC.IHR.PSRC.P5", "SH.IMM.IDPT", "FP.CPI.TOTL.ZG", "SL.UEM.TOTL.ZS", "TT.PRI.MRCH.XD.WD", "NE.GDI.FTOT.ZS"]


def rev_wdi():
    for ind in INDS:
        v = {"202403": arquivo(ind, "202403"), "202507": arquivo(ind, "202507"), "2026-10-08": cn.wdi(ind)}
        for a_, b_ in [("202403", "202507"), ("202507", "2026-10-08")]:
            A, B = v[a_], v[b_]
            for alvo, us in [("BRA", ["BRA"]), ("demais 10 unidades", OUTRAS)]:
                ch, tot, mx, only_a, only_b = 0, 0, (0.0, None), 0, 0
                for (u, a) in set(A) | set(B):
                    if u not in us:
                        continue
                    if (u, a) in A and (u, a) in B:
                        tot += 1
                        d = abs(A[(u, a)] - B[(u, a)])
                        if d > 1e-6 * max(1.0, abs(A[(u, a)])):
                            ch += 1
                            if d > mx[0]:
                                mx = (d, (u, a))
                    elif (u, a) in A:
                        only_a += 1
                    else:
                        only_b += 1
                sumiram = sorted(a for (u, a) in A if u in us and (u, a) not in B)
                faixa = f"; anos que existiam e sumiram: {sumiram[0]}-{sumiram[-1]} ({len(sumiram)} anos)" if sumiram and alvo == "BRA" else ""
                med("revisao_wdi", f"{ind}: {a_} -> {b_}", alvo, "valores comuns alterados / comuns", f"{ch}/{tot}", tot,
                    faixa.lstrip("; ") + ("; " if faixa else "") + f"maior mudanca absoluta {mx[0]:.4f}" + (f" em {mx[1][0]} {mx[1][1]}" if mx[1] else "") + f"; so na antiga {only_a}; so na nova {only_b}")


# ---------- C. PIP: releases e troca de PPC ----------
def pip(arq, nac_ou_arg=True):
    out = {}
    for r in csv.DictReader(open(RAIZ / arq)):
        if r["country_code"] not in cn.PAISES:
            continue
        if r["reporting_level"] != "national" and r["country_code"] != "ARG":
            continue
        out[(r["country_code"], int(r["reporting_year"]))] = (float(r["headcount"]) * 100, float(r["gini"]) * 100)
    return out


def pip_medidas():
    cur = pip("bruto/pip/pip_685_ppp2017.csv")
    for nome, arq in [("20260324", "bruto/pip/pip_685_ppp2017_rel20260324.csv"), ("20250930", "bruto/pip/pip_685_ppp2017_rel20250930.csv")]:
        o = pip(arq)
        for k, (i, rot) in enumerate([(0, "pobreza 6,85"), (1, "Gini")]):
            difs = {c: [] for c in cn.PAISES}
            for key in set(cur) & set(o):
                difs[key[0]].append(abs(cur[key][i] - o[key][i]))
            for c in ("BRA", "ARG", "VEN"):
                if difs[c]:
                    med("revisao_pip", f"{rot}: release 20260922 vs {nome}", c, "maior diferenca absoluta (pontos)", max(difs[c]), len(difs[c]),
                        f"alteradas (>0,001): {sum(1 for x in difs[c] if x > 1e-3)}; so-na-corrente {sum(1 for kk in cur if kk[0]==c and kk not in o)}; so-na-antiga {sum(1 for kk in o if kk[0]==c and kk not in cur)}")
    n21 = pip("bruto/pip/pip_830_ppp2021.csv")
    for c in cn.PAISES:
        xs = [(n21[k][0] - cur[k][0]) for k in cur if k[0] == c and k in n21]
        if xs:
            med("troca_ppc_pip", "pobreza: linha 8,30 (PPC 2021) menos linha 6,85 (PPC 2017), mesmo release 20260922, pontos percentuais", c, "mediana das diferencas", st.median(xs), len(xs),
                f"min {min(xs):.2f} max {max(xs):.2f}")
    for ref in REFS:
        xs = [((n21[("BRA", a)][0] - n21[(ref, a)][0]) - (cur[("BRA", a)][0] - cur[(ref, a)][0])) for (_, a) in cur if _ == "BRA" and ("BRA", a) in n21 and (ref, a) in cur and (ref, a) in n21]
        if xs:
            med("troca_ppc_pip", "efeito da troca de PPC sobre (Brasil menos referencia) na pobreza, pontos percentuais: (BRA-ref em 8,30/2021) menos (BRA-ref em 6,85/2017)", f"BRA-{ref}", "mediana", st.median(xs), len(xs), f"min {min(xs):.2f} max {max(xs):.2f}")


# ---------- D. PWT 10.01 vs 11.0 e Maddison ----------
def pwt(arq):
    rows = xl.ler(RAIZ / "pwt_maddison/bruto" / arq, "Data")
    h = next(rows)
    ix = {k: h.index(k) for k in ("countrycode", "year", "rgdpo", "pop", "rnna", "rtfpna", "rgdpna")}
    out = {}
    for r in rows:
        r = r + [""] * (len(h) - len(r))
        c = r[ix["countrycode"]]
        if c in cn.PAISES:
            out[(c, int(r[ix["year"]]))] = {k: cn.num(r[ix[k]]) for k in ("rgdpo", "pop", "rnna", "rtfpna", "rgdpna")}
    return out


def pwt_medidas():
    a, b = pwt("pwt1001.xlsx"), pwt("pwt110.xlsx")
    anos = sorted({k[1] for k in a if k in b and k[1] >= 1950})
    pc = lambda D, c, y: (D[(c, y)]["rgdpo"] / D[(c, y)]["pop"]) if (c, y) in D and D[(c, y)]["rgdpo"] and D[(c, y)]["pop"] else None
    for c in cn.PAISES:
        xs = [pct(pc(a, c, y), pc(b, c, y)) for y in anos if pc(a, c, y) and pc(b, c, y)]
        if xs:
            med("versao_pwt", "PIB pc (rgdpo/pop): PWT 11.0 (PPC 2021) sobre PWT 10.01 (PPC 2017), variacao % do nivel, 1950-2019", c, "mediana", st.median(xs), len(xs), f"min {min(xs):.2f} max {max(xs):.2f}")
    for ref in REFS:
        xs = [pct(pc(a, "BRA", y) / pc(a, ref, y), pc(b, "BRA", y) / pc(b, ref, y)) for y in anos if all(pc(D, c, y) for D in (a, b) for c in ("BRA", ref))]
        if xs:
            med("versao_pwt", "razao BRA/ref do PIB pc: PWT 11.0 sobre 10.01, variacao %", f"BRA/{ref}", "mediana", st.median(xs), len(xs), f"min {min(xs):.2f} max {max(xs):.2f}")
    # crescimento medio anual do Brasil em janelas fixas (Lula 1-2 = 2003-2010; Dilma = 2011-2016) nas duas versoes
    def cresc(D, c, y0, y1, campo="rgdpo", per_capita=True):
        xs = []
        for y in range(y0, y1 + 1):
            f = (lambda yy: pc(D, c, yy)) if per_capita else (lambda yy: D[(c, yy)][campo] if (c, yy) in D else None)
            if f(y) and f(y - 1):
                xs.append(pct(f(y - 1), f(y)))
        return (sum(xs) / len(xs), len(xs)) if xs else (None, 0)
    for nome, y0, y1 in [("Lula1-2 (2003-2010)", 2003, 2010), ("Dilma (2011-2016; PWT 10.01 so ate 2019)", 2011, 2016)]:
        va, na = cresc(a, "BRA", y0, y1)
        vb, nb = cresc(b, "BRA", y0, y1)
        med("versao_pwt", f"crescimento medio anual do PIB pc de BRA medido por rgdpo/pop (lado da producao, PPC encadeada), {nome}: PWT 10.01 / 11.0 / diferenca (pp/ano)", "BRA", "10.01 / 11.0 / diferenca", f"{va:.3f} / {vb:.3f} / {vb - va:+.3f}", f"{na}/{nb}")
    # estoque de capital e PTF: crescimento acumulado 2003-2010 nas duas versoes
    for campo in ("rnna", "rtfpna"):
        res = []
        for D in (a, b):
            v0, v1 = D[("BRA", 2002)][campo], D[("BRA", 2010)][campo]
            res.append(pct(v0, v1))
        med("versao_pwt", f"{campo}: variacao % acumulada 2002->2010 do Brasil, PWT 10.01 / 11.0", "BRA", "10.01 / 11.0", f"{res[0]:.2f} / {res[1]:.2f}", 8)


def maddison():
    rows = xl.ler(RAIZ / "pwt_maddison/bruto/mpd2023_web.xlsx", "Full data")
    h = next(rows)
    ix = {k: h.index(k) for k in ("countrycode", "year", "gdppc")}
    M = {}
    for r in rows:
        r = r + [""] * (len(h) - len(r))
        if r[ix["countrycode"]] in cn.PAISES and cn.num(r[ix["gdppc"]]):
            M[(r[ix["countrycode"]], int(r[ix["year"]]))] = float(r[ix["gdppc"]])
    return M


def fontes_cruzadas():
    """BRA / mediana dos 7 paises, nas tres fontes de nivel (nao e revisao: sao fontes diferentes)."""
    M = maddison()
    a, b = pwt("pwt1001.xlsx"), pwt("pwt110.xlsx")
    W = {k: v for k, v in cn.wdi("NY.GDP.PCAP.PP.KD").items() if k[0] in cn.PAISES}
    pc = lambda D, c, y: (D[(c, y)]["rgdpo"] / D[(c, y)]["pop"]) if (c, y) in D and D[(c, y)]["rgdpo"] and D[(c, y)]["pop"] else None
    fontes = {"Maddison 2023 (PPC 2011)": lambda c, y: M.get((c, y)), "PWT 10.01 (PPC 2017)": lambda c, y: pc(a, c, y),
              "PWT 11.0 (PPC 2021)": lambda c, y: pc(b, c, y), "WDI corrente (PPC 2021)": lambda c, y: W.get((c, y))}
    for y in (1970, 1980, 1990, 2002, 2010, 2016, 2019):
        for nome, f in fontes.items():
            refs = [f(c, y) for c in ("ARG", "CHL", "COL", "MEX", "PER", "URY") if f(c, y)]  # sem VEN: PWT/WDI nao cobrem todos os anos
            if f("BRA", y) and len(refs) >= 5:
                med("fontes_cruzadas", f"PIB pc: Brasil / mediana de ARG,CHL,COL,MEX,PER,URY em {y}", nome, "razao", f("BRA", y) / st.median(refs), len(refs), f"BRA={f('BRA', y):.0f}")


# ---------- E. FGV: vintages ----------
def fgv_vintages():
    V = {a: cn.ler_fgv(RAIZ / f"invpub/bruto/fgv_investimentos_publicos_1947-{a}.xlsx") for a in (2023, 2024, 2025)}
    for chave, nome in [("SP (GG+EPU)", "investimento do setor publico"), ("FBCF", "FBCF")]:
        for a_, b_ in [(2023, 2024), (2024, 2025)]:
            A, B = V[a_][("Em % do PIB", chave)], V[b_][("Em % do PIB", chave)]
            dif = {y: B[y] - A[y] for y in A if y in B}
            ch = {y: d for y, d in dif.items() if abs(d) > 1e-6}
            mx = max(ch.items(), key=lambda kv: abs(kv[1])) if ch else (None, 0.0)
            med("revisao_fgv", f"{nome} (% do PIB): vintage {a_} -> {b_}", "BRA", "anos alterados / comuns", f"{len(ch)}/{len(dif)}", len(dif),
                f"maior mudanca {mx[1]:+.3f} pp em {mx[0]}; mediana das mudancas absolutas entre os alterados {st.median([abs(x) for x in ch.values()]) if ch else 0:.3f} pp; anos novos {len(set(B) - set(A))}")
    # conceito: FGV (aquisicao de ativos, setor publico) vs ICSD (FBCF governo geral) em anos comuns
    L = list(csv.DictReader(open(RAIZ / "series/crescimento_contexto.csv")))
    g = {int(r["ano"]): float(r["valor"]) for r in L if r["indicador"] == "cc_invpub_pib" and r["pais_ou_grupo"] == "BRA" and r["definicao_linha"].endswith("governo geral (central + estados + municipios)")}
    s = {int(r["ano"]): float(r["valor"]) for r in L if r["indicador"] == "cc_invpub_pib" and r["fonte"] == "IMF ICSD 2021" and r["pais_ou_grupo"] == "BRA"}
    xs = [(y, s[y] - g[y]) for y in sorted(set(g) & set(s))]
    if xs:
        vs = [d for _, d in xs]
        med("conceito_invpub", "ICSD (FBCF governo geral) menos FGV (governo geral) em pp do PIB, anos comuns 1960-2019", "BRA", "mediana / min / max", f"{st.median(vs):+.2f} / {min(vs):+.2f} / {max(vs):+.2f}", len(vs),
            "conceitos e deflatores diferentes (ICSD: PIB e FBCF em US$ PPC de 2017); nao e revisao")
    return V


# ---------- F. termos de troca: encadeamento ----------
def splice_tt():
    f, h = cn.ipea("FUNCEX_TTR"), cn.ipea("HIST_TROCA")
    razoes = {y: f[y] / h[y] for y in sorted(set(f) & set(h))}
    ys = [y for y in razoes if y <= 1973]
    base = st.median([razoes[y] for y in ys])
    desv = {y: (razoes[y] / base - 1) * 100 for y in razoes}
    med("encadeamento_tt", "FUNCEX_TTR / HIST_TROCA: razao mediana 1901-1973 (mesma fonte IBGE, bases diferentes)", "BRA", "mediana", base, len(ys),
        f"desvio maximo absoluto em relacao a mediana, 1901-1973: {max(abs(desv[y]) for y in ys):.2f}%")
    for y in (1972, 1973, 1974, 1975):
        if y in desv:
            med("encadeamento_tt", f"desvio % da razao FUNCEX_TTR/HIST_TROCA em {y} em relacao a mediana 1901-1973", "BRA", "desvio %", desv[y], 1, f"FUNCEX={f[y]:.2f} HIST={h[y]:.2f}")
    # variacao anual 1973->1974 e 1974->1975 em cada serie (a de Funcex incorpora a transicao)
    for y in (1974, 1975):
        if all(k in d for d in (f, h) for k in (y, y - 1)):
            med("encadeamento_tt", f"variacao % do indice em {y} sobre {y - 1}: FUNCEX_TTR / HIST_TROCA", "BRA", "FUNCEX / HIST", f"{pct(f[y-1], f[y]):.2f} / {pct(h[y-1], h[y]):.2f}", 1)


# ---------- G. FBCF: FGV vs Ipeadata ----------
def fbcf():
    L = list(csv.DictReader(open(RAIZ / "series/crescimento_contexto.csv")))
    g = {int(r["ano"]): float(r["valor"]) for r in L if r["indicador"] == "cc_fbcf_pib" and r["fonte"].startswith("FGV")}
    p = {int(r["ano"]): float(r["valor"]) for r in L if r["indicador"] == "cc_fbcf_pib" and r["fonte"].startswith("Ipeadata")}
    w = {int(r["ano"]): float(r["valor"]) for r in L if r["indicador"] == "cc_fbcf_pib" and r["fonte"].startswith("WDI") and r["pais_ou_grupo"] == "BRA"}
    for nome, o in [("Ipeadata PAN_FBKFPIBV", p), ("WDI NE.GDI.FTOT.ZS", w)]:
        ys = sorted(set(g) & set(o))
        if ys:
            d = [o[y] - g[y] for y in ys]
            med("fbcf_fontes", f"{nome} menos FGV/IBGE, FBCF % do PIB, anos comuns {ys[0]}-{ys[-1]} (pp)", "BRA", "mediana / min / max", f"{st.median(d):+.2f} / {min(d):+.2f} / {max(d):+.2f}", len(ys),
                f"anos com |dif|>0,5 pp: {sum(1 for x in d if abs(x) > 0.5)}")
    # SCN10 nominal / PIB nominal, quando existir
    try:
        fb, pib = cn.ipea("SCN10_FBKFN10"), cn.ipea("SCN10_PIBN10")
        ys = sorted(set(fb) & set(pib))
        r = {y: fb[y] / pib[y] * 100 for y in ys}
        d = [(y, r[y] - g[y]) for y in ys if y in g]
        if d:
            med("fbcf_fontes", f"Ipeadata SCN10 (FBKFN10/PIBN10 nominais) menos FGV, anos comuns {d[0][0]}-{d[-1][0]} (pp)", "BRA", "mediana / min / max",
                f"{st.median([x for _, x in d]):+.2f} / {min(x for _, x in d):+.2f} / {max(x for _, x in d):+.2f}", len(d), f"anos de |dif|>0,5 pp: {[y for y, x in d if abs(x) > 0.5][:12]}")
    except FileNotFoundError:
        pass


# ---------- H. classes de renda do Banco Mundial ----------
def classes():
    rows = list(xl.ler(RAIZ / "oghist/bruto/OGHIST.xlsx", "Country Analytical History"))
    fy = [c for c in rows[3][2:] if c]
    dados = {}
    for r in rows[9:]:
        if r and len(r[0]) == 3 and r[0].isupper():
            dados[r[0]] = (r[1], r[2:2 + len(fy)] + [""] * (len(fy) - len(r[2:2 + len(fy)])))
    saida = {}
    for c in cn.PAISES:
        nome, seq = dados[c]
        trans = []
        for i in range(1, len(fy)):
            if seq[i] != seq[i - 1]:
                trans.append(f"{fy[i-1]}->{fy[i]}: {seq[i-1] or '(vazio)'} -> {seq[i] or '(vazio)'}")
        saida[c] = (seq, trans)
        med("classe_renda", f"mudancas de classe de renda do Banco Mundial FY89-FY25 ({nome})", c, "n. de mudancas", len(trans), len(fy), "; ".join(trans) if trans else "sem mudanca")
    # membros do grupo 'UM' (renda media alta) por ano fiscal, todos os paises da tabela
    cont = []
    for i, f in enumerate(fy):
        n = sum(1 for _, (_, seq) in dados.items() if seq[i] == "UM")
        cont.append((f, n))
    med("classe_renda", "numero de economias na classe UM (renda media alta) por ano fiscal, FY89..FY25 ", "UMC (membros)", "contagem",
        f"primeiro {cont[0][0]}={cont[0][1]}; menor {min(cont, key=lambda x: x[1])[0]}={min(x[1] for x in cont)}; maior {max(cont, key=lambda x: x[1])[0]}={max(x[1] for x in cont)}; ultimo {cont[-1][0]}={cont[-1][1]}", len(fy),
        "lista completa: " + ", ".join(f"{f}={n}" for f, n in cont))
    # saidas e entradas entre FY24 e FY25 (maior ano) : composicao muda
    ent, sai = [], []
    for k, (nome, seq) in dados.items():
        for i in range(1, len(fy)):
            if seq[i] == "UM" and seq[i - 1] != "UM":
                ent.append(1)
            if seq[i - 1] == "UM" and seq[i] != "UM" and seq[i]:
                sai.append(1)
    med("classe_renda", "entradas e saidas de economias na classe UM, FY89..FY25 (soma de todas as transicoes)", "UMC (membros)", "entradas / saidas", f"{len(ent)} / {len(sai)}", len(fy))
    return saida, fy, cont, dados


def main():
    ppc1 = ppc_wdi("202004", "202005", "troca_ppc_wdi_2011_2017")
    ppc2 = ppc_wdi("202403", "202405", "troca_ppc_wdi_2017_2021")
    ppc_wdi("202405", "202412", "revisao_wdi_apos_2021")
    rev_wdi()
    pip_medidas()
    pwt_medidas()
    fontes_cruzadas()
    fgv_vintages()
    splice_tt()
    fbcf()
    classes()
    with (RAIZ / "medidas_efeito.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["medida", "descricao", "alvo", "estatistica", "valor", "n", "nota"], lineterminator="\n")
        w.writeheader()
        w.writerows(MED)
    print("medidas_efeito.csv", len(MED))


if __name__ == "__main__":
    main()
