"""Gera mundo/janelas.csv: para cada indicador x governo, media do Brasil, media de cada referencia e diferenca.

Sem rede; le series/*.csv, quebras.csv e mandatos.csv. Regra de atribuicao ano -> governo: o governo que ocupa MAIS DIAS do ano-calendario
(a mesma regra de dominios-2). A media da diferenca usa SO os anos em que Brasil e referencia tem valor (maca com maca).
Variacao anual (`*_var_pct`) = (v_t / v_{t-1} - 1) * 100, so quando t e t-1 existem (sem interpolar).
Rodar: python3 -I .../mundo/scripts/janelas.py
"""
import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MANDATOS = Path("/Users/ulissesflores/Developer/brazil-governments-factcheck/data/curated/mandatos.csv")
REFS = ["WLD", "LCN", "UMC", "ARG", "CHL", "COL", "MEX", "PER", "URY", "VEN"]
# indicadores cuja leitura natural e a VARIACAO (niveis / indices): ganham tambem a linha `<indicador>_var_pct`
NIVEIS = {"mun_pibpc_ppc", "cc_pibpc_pwt", "cc_pibpc_na_pwt", "cc_pibpc_maddison", "cc_estoque_capital_pwt", "cc_pib_real_pwt", "cc_ptf_pwt",
          "tt_funcex", "tt_histtroca", "tt_wdi", "tt_wdi_arq"}
COLS = ["indicador", "fonte", "governo", "inicio", "fim", "referencia", "media_brasil", "media_referencia", "diferenca_brasil_menos_ref", "n_anos", "n_anos_brasil",
        "quebras_na_janela", "vintage"]


def governos():
    return [(r["id"], dt.date.fromisoformat(r["posse"]), dt.date.fromisoformat(r["saida"])) for r in csv.DictReader(open(MANDATOS))]


def governo_do_ano(gs, ano):
    ini, fim = dt.date(ano, 1, 1), dt.date(ano + 1, 1, 1)
    dias = {}
    for gid, p, s in gs:
        d = (min(s, fim) - max(p, ini)).days
        if d > 0:
            dias[gid] = d
    return max(dias.items(), key=lambda kv: kv[1])[0] if dias else None


def carregar():
    S = defaultdict(lambda: defaultdict(dict))  # (indicador, fonte) -> unidade -> ano -> valor
    vint = {}
    for arq in ("mundo", "termos_de_troca", "crescimento_contexto"):
        for r in csv.DictReader(open(RAIZ / f"series/{arq}.csv")):
            S[(r["indicador"], r["fonte"])][r["pais_ou_grupo"]][int(r["ano"])] = float(r["valor"])
            vint[(r["indicador"], r["fonte"])] = r["vintage"]
    return S, vint


def quebras():
    out = []
    p = RAIZ / "quebras.csv"
    if p.exists():
        for r in csv.DictReader(open(p)):
            for ind in r["indicador"].split(";"):
                out.append((ind.strip(), r["data_quebra"], r["tipo_de_quebra"]))
    return out


def data_q(txt):
    """'2012', '2012-05' ou '2012-05-17' -> date (campos faltantes = 1)."""
    k = (txt.split("-") + ["1", "1"])[:3]
    return dt.date(int(k[0]), int(k[1]), int(k[2]))


def variacao(serie):
    return {a: (v / serie[a - 1] - 1) * 100 for a, v in serie.items() if a - 1 in serie and serie[a - 1] != 0}


def media(xs):
    return sum(xs) / len(xs) if xs else None


def f(x):
    return "" if x is None else repr(round(x, 4))


def main():
    gs = governos()
    ano_gov = {a: governo_do_ano(gs, a) for a in range(1940, 2030)}
    S, vint = carregar()
    Q = quebras()
    saida = []
    for (ind, fonte), U in sorted(S.items()):
        variantes = [(ind, U)]
        if ind in NIVEIS:
            variantes.append((ind + "_var_pct", {u: variacao(s) for u, s in U.items()}))
        for nome, D in variantes:
            if "BRA" not in D:
                continue
            refs = [r for r in REFS if r in D] or [""]
            for gid, p, s in gs:
                anos_g = [a for a, g in ano_gov.items() if g == gid]
                qs = ";".join(f"{q[2]}@{q[1]}" for q in Q if q[0] in (ind, nome) and p <= data_q(q[1]) < s)
                bra = {a: D["BRA"][a] for a in anos_g if a in D["BRA"]}
                for ref in refs:
                    if ref:
                        comuns = [a for a in bra if a in D[ref]]
                        mb, mr = media([bra[a] for a in comuns]), media([D[ref][a] for a in comuns])
                        dif = None if mb is None else mb - mr
                        n = len(comuns)
                    else:
                        mb, mr, dif, n = media(list(bra.values())), None, None, len(bra)
                    saida.append(dict(indicador=nome, fonte=fonte, governo=gid, inicio=p.isoformat(), fim=s.isoformat(), referencia=ref,
                                      media_brasil=f(mb), media_referencia=f(mr), diferenca_brasil_menos_ref=f(dif), n_anos=n, n_anos_brasil=len(bra),
                                      quebras_na_janela=qs, vintage=vint[(ind, fonte)]))
    with (RAIZ / "janelas.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(saida)
    print("janelas.csv", len(saida))


if __name__ == "__main__":
    main()
