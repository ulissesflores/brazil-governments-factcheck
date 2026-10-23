#!/usr/bin/env python3
"""Gap anual IPCA livres menos IPCA monitorados (BCB SGS 11428 e 4449). Le so o bruto, sem rede.

Uso: python3 -I calcular-gap.py   (a partir da pasta mecanismos-preco)
Saidas: series/gap-livres-monitorados.csv (formato longo), gap-anual-mandatos.csv (largo),
        gap-por-governo.csv (janela de cada mandato, mes a mes).
Regras (fixas, escritas antes de olhar o resultado):
- acumulado anual = produto das 12 variacoes mensais (2 casas) - 1. Difere do publicado pelo BCB em ate 0,02 p.p.
- gap_pp = livres_acum - monitorados_acum (positivo = monitorados subiram MENOS que livres).
- governo do ano = quem estava no cargo em 31/12 (mandatos.csv). Tambem sai a coluna "governo_seguinte" (proxima linha do csv)
  e os governos que ocupavam o cargo em 31/12 de Y+1..Y+3; a fase 2 escolhe, aqui nao se escolhe.
- 2026 e parcial (jan-set); nao entra em soma de reversao.
- governo do mes (janela do mandato) = quem estava no cargo no dia 15.
"""
import csv, json, datetime as dt
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAND = Path("/Users/ulissesflores/Developer/brazil-governments-factcheck/data/curated/mandatos.csv")
VINTAGE = "2026-10-19 (dados ate 09/2026)"
ELEICAO = {1989, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022}


def ler(arq):
    d = json.loads((HERE / "bruto" / arq).read_text())
    return {(int(x["data"][6:]), int(x["data"][3:5])): float(x["valor"]) for x in d}


L = ler("bcb-sgs11428-livres-raw.json")
M = ler("bcb-sgs4449-raw.json")
assert set(L) == set(M), "meses diferentes entre livres e monitorados"
meses = sorted(L)
ultimo = meses[-1]

mand = list(csv.DictReader(MAND.open()))
for r in mand:
    r["p"] = dt.date.fromisoformat(r["posse"])
    r["s"] = dt.date.fromisoformat(r["saida"])


def gov_em(d):
    """governo no cargo na data d (posse <= d < saida); na troca vale o novo."""
    for r in mand:
        if r["p"] <= d < r["s"]:
            return r["id"]
    return None


def gov_31dez(y):
    return gov_em(dt.date(y, 12, 31)) or ("lula3" if y == 2026 else None)


def acum(serie, y):
    v = 1.0
    for m in range(1, 13):
        if (y, m) in serie:
            v *= 1 + serie[(y, m)] / 100
    return (v - 1) * 100


anos = sorted({y for y, _ in meses})
completos = {y for y in anos if all((y, m) in L for m in range(1, 13))}
ids = [r["id"] for r in mand]
prox = {ids[i]: (ids[i + 1] if i + 1 < len(ids) else "") for i in range(len(ids))}

gap, la, ma, rel = {}, {}, {}, {}
for y in anos:
    la[y], ma[y] = acum(L, y), acum(M, y)
    gap[y] = la[y] - ma[y]
    # preco relativo: quanto os monitorados subiram acima/abaixo dos livres, em %. Comparavel sob qualquer inflacao
    # (o gap em p.p. nao e: em 1993 a inflacao anual passava de 2.000%).
    rel[y] = ((1 + ma[y] / 100) / (1 + la[y] / 100) - 1) * 100

linhas = []  # formato longo
FONTE = "BCB SGS 11428 (IPCA itens livres) e 4449 (IPCA precos monitorados - total)"


def L_(ind, defin, y, v, un, nota=""):
    linhas.append(dict(indicador=ind, fonte=FONTE, definicao_linha=defin, ano=y,
                       valor=("" if v is None else f"{v:.2f}"), unidade=un, nota=nota, vintage=VINTAGE))


NOTA_ARR = "acumulado de 12 variacoes mensais com 2 casas; difere do publicado pelo BCB em ate 0,02 p.p."
cum = 0.0
wide = []
for y in anos:
    parcial = y not in completos
    np_ = "parcial: jan-set/2026, nao anualizado. " if parcial else ""
    cum += gap[y]
    L_("livres_acum_ano", "IPCA itens livres, acumulado no ano", y, la[y], "% no ano", np_ + NOTA_ARR)
    L_("monitorados_acum_ano", "IPCA precos monitorados, acumulado no ano", y, ma[y], "% no ano", np_ + NOTA_ARR)
    L_("gap_pp", "livres menos monitorados; positivo = monitorados subiram menos", y, gap[y], "p.p.",
       np_ + "diferenca de acumulados anuais")
    L_("gap_soma_desde_1991", "soma simples dos gap_pp de 1991 ate o ano (nao e composto)", y, cum, "p.p. (soma)", np_)
    L_("preco_relativo_monit_vs_livres", "(1+monitorados)/(1+livres)-1 no ano; negativo = monitorados subiram menos", y, rel[y], "%", np_)
    q1 = rel.get(y + 1) if (y + 1) in completos else None
    q3 = sum(rel[k] for k in (y + 1, y + 2, y + 3)) if all(k in completos for k in (y + 1, y + 2, y + 3)) else None
    if y in completos:
        L_("reversao_relativa_t1", "preco_relativo do ano seguinte", y, q1, "%", "" if q1 is not None else "janela incompleta")
        L_("reversao_relativa_soma_3", "soma simples do preco_relativo de Y+1 a Y+3", y, q3, "% (soma)", "" if q3 is not None else "janela incompleta")
    r1 = gap.get(y + 1) if (y + 1) in completos else None
    s3 = sum(gap[k] for k in (y + 1, y + 2, y + 3)) if all(k in completos for k in (y + 1, y + 2, y + 3)) else None
    if y in completos:
        L_("reversao_t1", "gap_pp do ano seguinte (sem inverter sinal)", y, r1, "p.p.",
           "" if r1 is not None else "janela incompleta (ano seguinte nao fechado)")
        L_("reversao_soma_3", "soma dos gap_pp de Y+1 a Y+3", y, s3, "p.p. (soma)",
           "" if s3 is not None else "janela incompleta (algum dos 3 anos seguintes nao fechado)")
    wide.append(dict(
        ano=y, eleicao_federal="SIM" if y in ELEICAO else "NAO",
        governo_no_cargo_31dez=gov_31dez(y) or "", governo_seguinte_no_csv=prox.get(gov_31dez(y) or "", ""),
        governo_31dez_Y1=gov_31dez(y + 1) or "", governo_31dez_Y2=gov_31dez(y + 2) or "",
        governo_31dez_Y3=gov_31dez(y + 3) or "",
        livres_acum=f"{la[y]:.2f}", monitorados_acum=f"{ma[y]:.2f}", gap_pp=f"{gap[y]:.2f}",
        reversao_t1="" if r1 is None else f"{r1:.2f}", reversao_soma_3="" if s3 is None else f"{s3:.2f}",
        preco_relativo_pct=f"{rel[y]:.2f}", rel_reversao_t1="" if q1 is None else f"{q1:.2f}",
        rel_reversao_soma_3="" if q3 is None else f"{q3:.2f}",
        nota="parcial jan-set" if parcial else ""))

(HERE / "series").mkdir(exist_ok=True)
with (HERE / "series/gap-livres-monitorados.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"])
    w.writeheader(); w.writerows(linhas)
with (HERE / "gap-anual-mandatos.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(wide[0])); w.writeheader(); w.writerows(wide)


def mes_gov(y, m):
    return gov_em(dt.date(y, m, 15))


def comp(serie, ms):
    v = 1.0
    for k in ms:
        v *= 1 + serie[k] / 100
    return (v - 1) * 100


por = []
for r in mand:
    ms = [k for k in meses if mes_gov(*k) == r["id"]]
    if not ms:
        por.append(dict(governo=r["id"], meses_com_dado=0,
                        nota="sem dado: mandato inteiro antes de jan/1991 (SGS comeca em 1991-01)"))
        continue
    lv, mn = comp(L, ms), comp(M, ms)
    rel = ((1 + mn / 100) / (1 + lv / 100) - 1) * 100  # preco relativo acumulado dos monitorados vs livres
    ult = ms[-1]
    pos = [k for k in meses if k > ult][:12]
    pos_txt = ""
    if len(pos) == 12:
        pos_txt = f"{((1 + comp(M, pos) / 100) / (1 + comp(L, pos) / 100) - 1) * 100:.2f}"
    notas = []
    if ms[0] == (1991, 1) and r["p"] < dt.date(1991, 1, 1):
        notas.append("inicio da serie (jan/1991) corta o mandato")
    if ult == ultimo and r["s"] > dt.date(2026, 9, 30):
        notas.append("janela termina em set/2026 (fim dos dados), mandato em curso")
    anos_gov = [y for y in anos if gov_31dez(y) == r["id"] and y in completos]
    por.append(dict(
        governo=r["id"], meses_com_dado=len(ms), janela=f"{ms[0][0]}-{ms[0][1]:02d} a {ult[0]}-{ult[1]:02d}",
        livres_composto_pct=f"{lv:.2f}", monitorados_composto_pct=f"{mn:.2f}", gap_composto_pp=f"{lv - mn:.2f}",
        preco_relativo_monitorados_vs_livres_pct=f"{rel:.2f}", preco_relativo_12m_seguintes_pct=pos_txt,
        soma_gap_anos_31dez_pp=(f"{sum(gap[y] for y in anos_gov):.2f}" if anos_gov else ""),
        nota="; ".join(notas)))
with (HERE / "gap-por-governo.csv").open("w", newline="") as f:
    cols = ["governo", "meses_com_dado", "janela", "livres_composto_pct", "monitorados_composto_pct", "gap_composto_pp",
            "preco_relativo_monitorados_vs_livres_pct", "preco_relativo_12m_seguintes_pct", "soma_gap_anos_31dez_pp", "nota"]
    w = csv.DictWriter(f, fieldnames=cols, restval=""); w.writeheader(); w.writerows(por)
print("ok", len(linhas), "linhas longas;", len(wide), "anos;", len(por), "governos")
