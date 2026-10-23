"""The composite index of phase 2 (``PREREGISTRATION-FASE-2.md``): one score per item, one series.

Every rule here is the sealed pre-registration applied literally:

* three doors (declared direction, no composite inside the composite, one concept once);
* two layers: the consensual core (N) and the declared economic premises (P), published as N and N+P;
* polarity first (``menor`` items enter multiplied by -1), then frozen goalposts: 0 = worst and 100 =
  best value observed in the base period 1995-2024, no clipping;
* method breaks chained only through a measured overlap (difference for rates and shares, ratio for
  levels), the effect printed; without overlap only the longest base is kept;
* no imputation: an item missing in a year leaves that year's area mean; the index is not computed
  for a year with less than 70 % of the core items;
* equal nominal weights, then area weights tuned so that each area's effective importance (squared
  Pearson correlation with the index, the linear estimate of the correlation ratio) is equal, within
  [0.5/K, 2/K], at most 100 iterations, falling back to equal nominal weights;
* arithmetic mean across areas by default; geometric and non-compensatory (Mazziotta-Pareto)
  scenarios; percentile goalposts and carry-forward scenarios; 10 000 Dirichlet draws of area weights
  for the robustness of each term's closing value and rank.

Nothing is estimated. Items the pre-registration lists as "coletar" plug in here when their
collection lands; until then they are absent and the coverage says so.
"""

import csv
import json
import math
import random
import re
import statistics
from pathlib import Path

from govfc import terminal
from govfc.explica import EXPLICA_INDICE
from govfc.mandatos import carregar

RAIZ = Path(__file__).resolve().parents[2]
CURADO = RAIZ / "data" / "curated"
BASE = (1995, 2024)  # frozen goalpost period (annual)
BASE_PULSO = ("1996-01", "2024-12")  # frozen goalpost period (monthly pulse)
COBERTURA_MINIMA = 0.7
SORTEIOS = 10_000
SEMENTE = 20261020


def _lido(nome):
    """Read a curated CSV into a list of dicts."""
    with open(CURADO / nome, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _serie(obs, ind, trecho, anos=None):
    """Annual ``{year: v}`` of one curated indicator whose series label contains ``trecho``."""
    out = {}
    for r in obs:
        if r["indicador"] == ind and trecho in r["serie"] and re.fullmatch(r"\d{4}", r["periodo"]):
            a = int(r["periodo"])
            if anos is None or anos[0] <= a <= anos[1]:
                out.setdefault(a, float(r["valor"]))
    return out


def _longo_pasta(colecao, pasta, nome, indicador, linha=None):
    """Annual ``{year: v}`` of one indicator (and optionally one ``definicao_linha``) in a long CSV."""
    out = {}
    with open(terminal.RAW / colecao / pasta / nome, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            ok = r["indicador"] == indicador and re.fullmatch(r"\d{4}", r["ano"])
            if not ok or r["valor"] in ("", "NA"):
                continue
            if linha is not None and linha not in r["definicao_linha"]:
                continue
            out[int(r["ano"])] = float(r["valor"])
    return out


def razao_anual(num, den):
    """``100 x num / den`` on the common years (a share in percent)."""
    return {a: 100 * num[a] / den[a] for a in num if a in den and den[a]}


def encadear(bases, modo):
    """Chain bases through their measured overlap (pre-registration §8).

    Parameters
    ----------
    bases : list of (str, dict)
        ``(label, {year: value})`` from the oldest to the newest base.
    modo : str
        ``"diferenca"`` (rates, shares) or ``"razao"`` (levels).

    Returns
    -------
    tuple
        ``(serie, efeitos)``: the chained ``{year: value}`` on the newest base's level and a list
        of printed effects, one per link; a base without overlap is dropped unless it is the
        longest one.
    """
    if not bases:
        return {}, []
    atual_rotulo, atual = bases[0]
    atual = dict(atual)
    efeitos = []
    for rotulo, nova in bases[1:]:
        comum = sorted(set(atual) & set(nova))
        if not comum:
            # no overlap: keep the longer of the two, declare it
            if len(nova) > len(atual):
                efeitos.append(
                    {
                        "de": atual_rotulo,
                        "para": rotulo,
                        "sobreposicao": 0,
                        "efeito": None,
                        "mantida": rotulo,
                    }
                )
                atual_rotulo, atual = rotulo, dict(nova)
            else:
                efeitos.append(
                    {
                        "de": atual_rotulo,
                        "para": rotulo,
                        "sobreposicao": 0,
                        "efeito": None,
                        "mantida": atual_rotulo,
                    }
                )
            continue
        if modo == "razao":
            fator = statistics.mean(nova[a] / atual[a] for a in comum if atual[a])
            ajustada = {a: v * fator for a, v in atual.items()}
            efeito = {"fator": round(fator, 6)}
        else:
            difs = [nova[a] - atual[a] for a in comum]
            delta = statistics.mean(difs)
            ajustada = {a: v + delta for a, v in atual.items()}
            efeito = {"diferenca": round(delta, 6)}
            if len(difs) > 1:  # the overlap is rarely constant: say how much it moves
                efeito["desvio_padrao"] = round(statistics.pstdev(difs), 6)
                efeito["minimo"], efeito["maximo"] = round(min(difs), 6), round(max(difs), 6)
        efeitos.append(
            {
                "de": atual_rotulo,
                "para": rotulo,
                "sobreposicao": len(comum),
                "anos": [comum[0], comum[-1]],
                "efeito": efeito,
            }
        )
        atual = {**ajustada, **nova}  # the newer base wins where both exist
        atual_rotulo = rotulo
    return atual, efeitos


def balizas(serie, direcao, janela):
    """Frozen goalposts after polarity: ``(pior, melhor)`` observed inside ``janela``."""
    sinal = -1 if direcao == "menor" else 1
    vals = [sinal * v for k, v in serie.items() if janela[0] <= k <= janela[1]]
    if len(vals) < 2:
        return None
    return min(vals), max(vals)


def pontuar(serie, direcao, bal):
    """Score 0-100 (no clipping): 100 x (value - worst) / (best - worst), on the polarised value."""
    sinal = -1 if direcao == "menor" else 1
    pior, melhor = bal
    if melhor == pior:
        return {}
    return {k: 100 * (sinal * v - pior) / (melhor - pior) for k, v in serie.items()}


def media(vals):
    """Arithmetic mean or ``None`` when empty."""
    return math.fsum(vals) / len(vals) if vals else None


def media_geometrica(vals):
    """Geometric mean; undefined (``None``) when any value is not positive."""
    if not vals or any(v <= 0 for v in vals):
        return None
    return math.exp(math.fsum(math.log(v) for v in vals) / len(vals))


def ampi(vals):
    """Mazziotta-Pareto adjusted mean: mean minus standard deviation times coefficient of variation."""
    if len(vals) < 2:
        return media(vals)
    m = media(vals)
    s = statistics.pstdev(vals)
    return m - s * (s / m) if m else None


def correlacao(xs, ys):
    """Pearson correlation of two equally long lists (``0`` when degenerate)."""
    if len(xs) < 3:
        return 0.0
    mx, my = media(xs), media(ys)
    sx = math.sqrt(math.fsum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(math.fsum((y - my) ** 2 for y in ys))
    if not sx or not sy:
        return 0.0
    return math.fsum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True)) / (sx * sy)


def agregar(areas_por_ano, pesos, forma="aritmetica"):
    """Aggregate area scores into the index, year by year, with the given area weights.

    Parameters
    ----------
    areas_por_ano : dict
        ``{year: {area: score}}`` (areas missing in a year are skipped, weights renormalised).
    pesos : dict
        ``{area: weight}``.
    forma : str
        ``"aritmetica"``, ``"geometrica"`` or ``"ampi"``.
    """
    out = {}
    for ano, sc in areas_por_ano.items():
        presentes = [a for a in sc if a in pesos and sc[a] is not None]
        if not presentes:
            continue
        w = {a: pesos[a] for a in presentes}
        tot = math.fsum(w.values())
        if forma == "aritmetica":
            out[ano] = math.fsum(sc[a] * w[a] / tot for a in presentes)
        elif forma == "geometrica":
            out[ano] = (
                None
                if any(sc[a] <= 0 for a in presentes)
                else math.exp(math.fsum(w[a] / tot * math.log(sc[a]) for a in presentes))
            )
        else:
            out[ano] = ampi([sc[a] for a in presentes])
    return {k: v for k, v in out.items() if v is not None}


def importancia_efetiva(areas_por_ano, indice):
    """Squared Pearson correlation between each area and the index on the common years."""
    out = {}
    areas = sorted({a for sc in areas_por_ano.values() for a in sc})
    for a in areas:
        anos = [y for y in indice if y in areas_por_ano and areas_por_ano[y].get(a) is not None]
        out[a] = correlacao([areas_por_ano[y][a] for y in anos], [indice[y] for y in anos]) ** 2
    return out


def ajustar_pesos(areas_por_ano, areas, tol=0.02, max_iter=100):
    """Tune area weights so that effective importances are equal (pre-registration §5.2).

    Returns
    -------
    tuple
        ``(pesos, convergiu, iteracoes)``; on failure the weights are the equal nominal ones.
    """
    k = len(areas)
    nominal = {a: 1 / k for a in areas}
    pesos = dict(nominal)
    lo, hi = 0.5 / k, 2 / k
    for it in range(1, max_iter + 1):
        idx = agregar(areas_por_ano, pesos)
        s = importancia_efetiva(areas_por_ano, idx)
        alvo = media([s[a] for a in areas])
        if max(abs(s[a] - alvo) for a in areas) <= tol:
            return pesos, True, it
        for a in areas:
            if s[a] > 0:
                pesos[a] = min(hi, max(lo, pesos[a] * math.sqrt(alvo / s[a])))
        tot = math.fsum(pesos.values())
        pesos = {a: w / tot for a, w in pesos.items()}
    return nominal, False, max_iter


def trimestre_para_meses(trimestral):
    """Attribute a quarterly ``{"YYYY-MM": v}`` (keyed by the quarter's last month) to its three months."""
    out = {}
    for k, v in trimestral.items():
        a, m = int(k[:4]), int(k[5:7])
        for mm in (m - 2, m - 1, m):
            out[f"{a}-{mm:02d}"] = v
    return out


def _mensais(obs, efeitos):
    """Monthly series (on the newest base's level) of the items that have intra-year data (amendment 06).

    Parameters
    ----------
    obs : list of dict
        Curated observations.
    efeitos : dict
        ``{item_id: [link effects]}`` measured by the annual chaining; the same deltas are applied
        to the older monthly bases so that December equals the annual item.
    """
    ipca12 = terminal.taxa_12m(terminal._bcb_mensal("ipca-sgs433-raw.json"))
    salmin = terminal._ipea("ipeadata-GAC12_SALMINRE12-raw.json")
    pme_a = terminal._ipea("ipeadata-PME12_TDA12-raw.json")
    pme_n = terminal._ipea("ipeadata-PAN12_TD12-raw.json")
    pnadc_q = {}
    for r in obs:
        if r["indicador"] == "taxa_de_desocupacao" and "-T" in r["periodo"]:
            a, t = r["periodo"].split("-T")
            pnadc_q[f"{a}-{int(t) * 3:02d}"] = float(r["valor"])
    d_des = [
        e["efeito"].get("diferenca", 0.0) for e in efeitos.get("desemprego", []) if e.get("efeito")
    ]
    d1, d2 = (d_des + [0.0, 0.0])[:2]
    desemprego = {}
    desemprego.update({k: v + d1 + d2 for k, v in pme_a.items()})
    desemprego.update({k: v + d2 for k, v in pme_n.items()})
    desemprego.update(trimestre_para_meses(pnadc_q))
    d_div = [
        e["efeito"].get("diferenca", 0.0) for e in efeitos.get("divida", []) if e.get("efeito")
    ]
    divida = {}
    divida.update(
        {
            k: v + (d_div[0] if d_div else 0.0)
            for k, v in terminal._longo(
                "bcb-fase2", "dbgg_pib_metodologia_ate_2007_sgs4537.csv"
            ).items()
        }
    )
    divida.update(terminal._longo("bcb-fase2", "dbgg_pib_metodologia_2008_sgs13762.csv"))
    return {
        "inflacao": ipca12,
        "salmin": salmin,
        "desemprego": desemprego,
        "familias": terminal._longo("bcb-fase2", "endividamento_familias_renda_total_sgs29037.csv"),
        "divida": divida,
    }


def candles_do_indice(mensal):
    """Yearly candles on the monthly index: open = previous December (else the first month), close = December (else the last month), extremes = the months."""
    por_ano = {}
    for k, v in sorted(mensal.items()):
        por_ano.setdefault(int(k[:4]), []).append((k, v))
    out = []
    for ano in sorted(por_ano):
        meses = por_ano[ano]
        prev = mensal.get(f"{ano - 1}-12")
        nota = []
        if prev is None:
            prev = meses[0][1]
            nota.append(f"abre no primeiro mês calculado ({meses[0][0]})")
        if meses[-1][0] != f"{ano}-12":
            nota.append(f"fecha em {meses[-1][0]} (ano incompleto)")
        vals = [v for _, v in meses] + [prev]
        out.append(
            {
                "t": f"{ano}-01-01",
                "o": prev,
                "c": meses[-1][1],
                "h": max(vals),
                "l": min(vals),
                "n": len(meses),
                "nota": "; ".join(nota),
            }
        )
    return out


def mandato_candles(indice, govs):
    """Term candles on the index: open = year before inauguration (or the first value), close = last year."""
    out = []
    anos = sorted(indice)
    for g in govs:
        y0, y1 = (
            g["posse"].year - 1,
            (g["saida"].year if g["saida"].month > 6 or g.get("corrente") else g["saida"].year - 1),
        )
        dentro = [y for y in anos if g["posse"].year <= y <= y1]
        if not dentro:
            continue
        abre = indice.get(y0)
        nota = ""
        if abre is None:
            abre, nota = (
                indice[dentro[0]],
                f"abre no primeiro valor calculado ({dentro[0]}): nao ha {y0}",
            )
        vals = [indice[y] for y in dentro] + [abre]
        out.append(
            {
                "gov": g["id"],
                "o": abre,
                "c": indice[dentro[-1]],
                "h": max(vals),
                "l": min(vals),
                "anos": [dentro[0], dentro[-1]],
                "nota": nota,
            }
        )
    return out


def _itens(obs):
    """The pre-registered items available today (``temos``), as bases in declared order."""
    ipca = terminal.taxa_12m(terminal._bcb_mensal("ipca-sgs433-raw.json"))
    ipca_dez = {int(k[:4]): v for k, v in ipca.items() if k.endswith("-12")}
    salmin = terminal._ipea("ipeadata-GAC12_SALMINRE12-raw.json")
    salmin_dez = {int(k[:4]): v for k, v in salmin.items() if k.endswith("-12")}
    S = _serie

    def L(colecao, nome, indicador, pasta="series", linha=None):
        """Annual rows of one indicator in a long CSV of a phase-2 collection."""
        return _longo_pasta(colecao, pasta, nome, indicador, linha)

    def IB(indicador):
        """IBGE ratio (% of GDP at market prices) as two bases: ref. 2000, then the quarterly accounts (ref. 2010), chained on 2000-2009."""
        return [
            (
                "IBGE SCN referência 2000 (1995-2009)",
                L("ibge-fase2", "ibge_fase2_longo.csv", indicador, linha="ibge_scn_ref2000_ed2009"),
            ),
            (
                "IBGE contas trimestrais, referência 2010 (1996-2025)",
                L(
                    "ibge-fase2",
                    "ibge_fase2_longo.csv",
                    indicador,
                    linha="ibge_cnt_ref2010_soma4tri",
                ),
            ),
        ]

    def DEZ(mensal):
        """December value of a monthly ``{"YYYY-MM": v}`` dict, keyed by year."""
        return {int(k[:4]): v for k, v in mensal.items() if k.endswith("-12")}

    pme_a = terminal._ipea("ipeadata-PME12_TDA12-raw.json")
    pme_n = terminal._ipea("ipeadata-PAN12_TD12-raw.json")
    pnadc_q = {}
    for r in obs:
        if r["indicador"] == "taxa_de_desocupacao" and "-T" in r["periodo"]:
            a, t = r["periodo"].split("-T")
            pnadc_q[f"{a}-{int(t) * 3:02d}"] = float(r["valor"])
    pnadc_m = trimestre_para_meses(pnadc_q)

    def V(var):
        """Annual point estimate of one V-Dem variable for Brazil (collection ``vdem-fase2``)."""
        return terminal._longo_ind("vdem-fase2", "vdem_brasil_v16.csv", var)

    return [
        # id, area, nome, direcao, camada, modo de encadeamento, bases (da mais antiga para a mais nova)
        (
            "inflacao",
            "Preços",
            "Inflação IPCA, dez/dez",
            "menor",
            "N",
            "diferenca",
            [("IPCA 12 meses em dezembro (BCB SGS 433)", ipca_dez)],
        ),
        (
            "pibpc",
            "Atividade e renda",
            "PIB per capita, US$ PPC de 2021",
            "maior",
            "N",
            "razao",
            [("WDI NY.GDP.PCAP.PP.KD", S(obs, "mun_pibpc_ppc", "| BRA"))],
        ),
        (
            "fbcf",
            "Atividade e renda",
            "Investimento (FBCF), % do PIB",
            "maior",
            "N",
            "diferenca",
            [("FGV IBRE / IBGE SCN", S(obs, "cc_fbcf_pib", "FGV IBRE"))],
        ),
        (
            "ptf",
            "Atividade e renda",
            "Produtividade total dos fatores (PWT)",
            "maior",
            "N",
            "razao",
            [("PWT 11.0", S(obs, "cc_ptf_pwt", "PWT 11.0"))],
        ),
        (
            "salmin",
            "Atividade e renda",
            "Salário mínimo real, dezembro",
            "maior",
            "N",
            "razao",
            [("Ipea GAC12_SALMINRE12", salmin_dez)],
        ),
        (
            "renda_trab",
            "Atividade e renda",
            "Renda real do trabalho",
            "maior",
            "N",
            "razao",
            [
                ("PNAD (SIDRA 1871)", S(obs, "tbl_renda_trabalho_real", "SIDRA1871")),
                (
                    "PNADC (SIDRA 4660 deflacionado)",
                    S(obs, "tbl_renda_trabalho_real", "SIDRA4660 nominal"),
                ),
            ],
        ),
        (
            "desemprego",
            "Trabalho",
            "Taxa de desemprego",
            "menor",
            "N",
            "diferenca",
            [
                ("PME antiga, dezembro", DEZ(pme_a)),
                ("PME nova, dezembro", DEZ(pme_n)),
                ("PNAD Contínua, 4º trimestre", DEZ(pnadc_m)),
            ],
        ),
        (
            "informalidade",
            "Trabalho",
            "Informalidade",
            "menor",
            "N",
            "diferenca",
            [
                ("PNAD (Ipea DISOC_INFI)", S(obs, "tbl_informalidade", "DISOC")),
                ("PNADC (SIDRA 4708)", S(obs, "tbl_informalidade_ibge", "SIDRA4708")),
            ],
        ),
        (
            "divida",
            "Fiscal e vulnerabilidade",
            "Dívida bruta do governo geral, % do PIB",
            "menor",
            "N",
            "diferenca",
            [
                ("BCB, metodologia até 2007", S(obs, "divida_pib", "metodologia até 2007")),
                ("BCB, metodologia desde 2008", S(obs, "divida_pib", "metodologia desde 2008")),
            ],
        ),
        (
            "primario",
            "Fiscal e vulnerabilidade",
            "Resultado primário, % do PIB",
            "maior",
            "N",
            "diferenca",
            [
                (
                    "Governo federal e BC (NFSP)",
                    S(obs, "primario_pib", "governo federal e Banco Central"),
                ),
                ("Setor público consolidado (NFSP)", S(obs, "primario_pib", "consolidado")),
            ],
        ),
        (
            "pobreza",
            "Pobreza e desigualdade",
            "Pobreza, US$ 6,85/dia (PPC 2017)",
            "menor",
            "N",
            "diferenca",
            [("Banco Mundial PIP", S(obs, "pobreza", "PIP | US$ 6.85/dia PPC2017"))],
        ),
        (
            "gini",
            "Pobreza e desigualdade",
            "Gini",
            "menor",
            "N",
            "diferenca",
            [("Banco Mundial PIP", S(obs, "gini", "PIP | renda dom"))],
        ),
        (
            "subalimentacao",
            "Pobreza e desigualdade",
            "Subalimentação, % da população",
            "menor",
            "N",
            "diferenca",
            [("FAO SOFI 2026", S(obs, "ali_pou", "SOFI-2026"))],
        ),
        (
            "expvida",
            "Saúde",
            "Expectativa de vida ao nascer",
            "maior",
            "N",
            "diferenca",
            [("ONU via WDI", S(obs, "expvida", "WB-WDI"))],
        ),
        (
            "mortinf",
            "Saúde",
            "Mortalidade infantil, por mil",
            "menor",
            "N",
            "diferenca",
            [("UN IGME via WDI", S(obs, "mortinf", "WB-WDI"))],
        ),
        (
            "mortmat",
            "Saúde",
            "Mortalidade materna, por 100 mil",
            "menor",
            "N",
            "diferenca",
            [("Estatística nacional via WDI", S(obs, "sau_mortmat_nacional", "WB-WDI"))],
        ),
        (
            "dtp3",
            "Saúde",
            "Cobertura vacinal DTP3, %",
            "maior",
            "N",
            "diferenca",
            [("OMS/UNICEF WUENIC 2025", S(obs, "sau_dtp3", "WUENIC-rev2025"))],
        ),
        (
            "prenatal",
            "Saúde",
            "Pré-natal com 7+ consultas, %",
            "maior",
            "N",
            "diferenca",
            [("SINASC", S(obs, "mat_prenatal7", "SINASC"))],
        ),
        (
            "saeb",
            "Educação",
            "Saeb matemática, média das três etapas",
            "maior",
            "N",
            "diferenca",
            [
                ("Press kit 2019", _saeb(obs, "PressKit2019")),
                ("Relatório 2023", _saeb(obs, "Relatorio2023")),
            ],
        ),
        (
            "analfabetismo",
            "Educação",
            "Analfabetismo 15+, %",
            "menor",
            "N",
            "diferenca",
            [
                ("PNAD (IDS 1187)", S(obs, "edu_analfab15", "IDS1187")),
                ("PNADC (SIDRA 7113)", S(obs, "edu_analfab15", "SIDRA7113")),
            ],
        ),
        (
            "homicidios",
            "Segurança",
            "Homicídios por 100 mil",
            "menor",
            "N",
            "diferenca",
            [("SIM / Ipeadata", S(obs, "seg_homic_taxa", "AVIOL12"))],
        ),
        (
            "agua",
            "Moradia e infraestrutura",
            "Água por rede geral, % dos domicílios",
            "maior",
            "N",
            "diferenca",
            [
                ("PNAD (SIDRA 1955)", S(obs, "mor_agua_rede_geral", "SIDRA1955")),
                ("PNADC (SIDRA 6731)", S(obs, "mor_agua_rede_geral", "SIDRA6731")),
            ],
        ),
        (
            "esgoto",
            "Moradia e infraestrutura",
            "Esgoto adequado, % dos domicílios",
            "maior",
            "N",
            "diferenca",
            [
                ("PNAD (SIDRA 1956)", S(obs, "mor_esgoto_adequado", "SIDRA1956")),
                ("PNADC (SIDRA 7192)", S(obs, "mor_esgoto_adequado", "SIDRA7192")),
            ],
        ),
        (
            "desmatamento",
            "Ambiente",
            "Desmatamento da Amazônia, km²/ano",
            "menor",
            "N",
            "diferenca",
            [("INPE PRODES", S(obs, "amb_prodes_amz", "TerraBrasilis"))],
        ),
        (
            "familias",
            "Fiscal e vulnerabilidade",
            "Endividamento das famílias, % da renda de 12 meses (dezembro)",
            "menor",
            "N",
            "diferenca",
            [
                (
                    "BCB SGS 29037 (2005+)",
                    DEZ(
                        terminal._longo(
                            "bcb-fase2", "endividamento_familias_renda_total_sgs29037.csv"
                        )
                    ),
                )
            ],
        ),
        (
            "reservas",
            "Fiscal e vulnerabilidade",
            "Reservas internacionais, % do PIB",
            "maior",
            "N",
            "diferenca",
            [
                (
                    "BCB reservas (dezembro) / WDI PIB em US$ correntes",
                    razao_anual(
                        S(obs, "reservas_usd", "dezembro"),
                        {
                            a: v / 1e6
                            for a, v in L(
                                "mundo-fase2", "wdi_brasil.csv", "wdi_pib_usd_correntes"
                            ).items()
                        },
                    ),
                )
            ],
        ),
        (
            "pd",
            "Ciência e tecnologia",
            "Gasto em P&D, % do PIB",
            "maior",
            "N",
            "diferenca",
            [("UNESCO via WDI", L("mundo-fase2", "wdi_brasil.csv", "wdi_pd_pib"))],
        ),
        (
            "pesquisadores",
            "Ciência e tecnologia",
            "Pesquisadores por milhão de habitantes",
            "maior",
            "N",
            "diferenca",
            [
                (
                    "UNESCO via WDI (até 2014)",
                    L("mundo-fase2", "wdi_brasil.csv", "wdi_pesquisadores_por_milhao"),
                )
            ],
        ),
        (
            "patentes",
            "Ciência e tecnologia",
            "Pedidos de patente de residentes por milhão",
            "maior",
            "N",
            "diferenca",
            [
                (
                    "WIPO via WDI / população WDI",
                    L(
                        "mundo-fase2",
                        "patentes_por_milhao.csv",
                        "patentes_residentes_por_milhao",
                        pasta="derivado",
                    ),
                )
            ],
        ),
        (
            "eci",
            "Ciência e tecnologia",
            "Índice de complexidade econômica (Atlas, HS92)",
            "maior",
            "N",
            "diferenca",
            [
                (
                    "Harvard Growth Lab Atlas v12",
                    L("mundo-fase2", "eci_atlas_brasil.csv", "atlas_eci_hs92"),
                )
            ],
        ),
        (
            "internet",
            "Moradia e infraestrutura",
            "Acesso à internet, % dos domicílios",
            "maior",
            "N",
            "diferenca",
            [
                (
                    "PNAD 2003-2015, microcomputador com internet",
                    L(
                        "ibge-fase2",
                        "ibge_fase2_longo.csv",
                        "internet_domicilios_pct",
                        linha="pnad_microcomputador",
                    ),
                ),
                (
                    "PNAD 2013-2015, internet por qualquer equipamento",
                    L(
                        "ibge-fase2",
                        "ibge_fase2_longo.csv",
                        "internet_domicilios_pct",
                        linha="pnad_utilizacao",
                    ),
                ),
                (
                    "PNAD Contínua TIC 2016+",
                    L(
                        "ibge-fase2",
                        "ibge_fase2_longo.csv",
                        "internet_domicilios_pct",
                        linha="pnadc_tic",
                    ),
                ),
            ],
        ),
        # premise block (declared by the author): denominator = GDP at market prices, the usual "% do PIB"
        (
            "industria",
            "Premissas econômicas",
            "Indústria de transformação, % do PIB a preços de mercado",
            "maior",
            "P",
            "diferenca",
            IB("ind_transf_sobre_pib_mercado_pct"),
        ),
        (
            "governo",
            "Premissas econômicas",
            "Consumo final do governo, % do PIB a preços de mercado",
            "menor",
            "P",
            "diferenca",
            IB("consumo_governo_sobre_pib_mercado_pct"),
        ),
        (
            "abertura",
            "Premissas econômicas",
            "Abertura comercial (X+M), % do PIB a preços de mercado",
            "maior",
            "P",
            "diferenca",
            IB("abertura_comercial_sobre_pib_mercado_pct"),
        ),
        (
            "libdem",
            "Instituições",
            "Democracia liberal (V-Dem v2x_libdem)",
            "maior",
            "N",
            "diferenca",
            [("V-Dem v16", V("v2x_libdem"))],
        ),
        (
            "corrupcao",
            "Instituições",
            "Corrupção política (V-Dem v2x_corr)",
            "menor",
            "N",
            "diferenca",
            [("V-Dem v16", V("v2x_corr"))],
        ),
        (
            "legcon",
            "Instituições",
            "Restrições legislativas ao Executivo (V-Dem v2xlg_legcon)",
            "maior",
            "N",
            "diferenca",
            [("V-Dem v16", V("v2xlg_legcon"))],
        ),
        (
            "jucon",
            "Instituições",
            "Restrições judiciais ao Executivo (V-Dem v2x_jucon)",
            "maior",
            "N",
            "diferenca",
            [("V-Dem v16", V("v2x_jucon"))],
        ),
        # premise block: the pre-registration says "less state ownership is better"; in the V-Dem
        # codebook (v2clstown) a HIGHER value means LESS state ownership, so the item enters as "maior"
        (
            "estatal",
            "Premissas econômicas",
            "Propriedade estatal da economia (V-Dem v2clstown; valor alto = menos Estado)",
            "maior",
            "P",
            "diferenca",
            [("V-Dem v16", V("v2clstown"))],
        ),
    ]


def _saeb(obs, trecho):
    """Mean of the three Saeb mathematics stages in the years when all three exist (one item)."""
    etapas = [
        _serie(obs, f"edu_saeb_MT_{e}", trecho)
        for e in ("EF_5ano_4serie", "EF_9ano_8serie", "EM_3serie")
    ]
    anos = set(etapas[0]) & set(etapas[1]) & set(etapas[2])
    return {a: media([e[a] for e in etapas]) for a in sorted(anos)}


def _meses(ate):
    """All months from jan/1996 to ``ate`` (``"YYYY-MM"``)."""
    out, a, m = [], 1996, 1
    while f"{a}-{m:02d}" <= ate:
        out.append(f"{a}-{m:02d}")
        a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    return out


def _mensal(itens, pesos, mensais, carry=False):
    """Monthly index (amendment 06): monthly items by their month, annual items as steps, same weights.

    With ``carry=True`` this is the pre-registered carry-forward scenario (§9): a missing month of a
    monthly item, or a missing year of an annual item, takes the last published value; the series
    then runs to the last month any monthly item has, and the result is labelled as a scenario.
    """
    por_mes = {}
    n_itens = len(itens)
    ultimo = max((max(d) for d in mensais.values() if d), default="2024-12")
    for i in itens:
        sinal = -1 if i["direcao"] == "menor" else 1
        pior, melhor = sinal * i["balizas"]["pior"], sinal * i["balizas"]["melhor"]
        if i["id"] in mensais:
            serie = {
                k: 100 * (sinal * v - pior) / (melhor - pior)
                for k, v in mensais[i["id"]].items()
                if k >= "1996-01"
            }
            if carry:
                atual = None
                for k in _meses(ultimo):
                    atual = serie.get(k, atual)
                    if atual is not None:
                        serie[k] = atual
        else:
            serie, atual = {}, None
            for k in _meses(ultimo):
                a = int(k[:4])
                if a in i["_pontos"]:
                    atual = i["_pontos"][a]
                elif not carry:
                    continue
                if atual is not None:
                    serie[k] = atual
        for k, v in serie.items():
            por_mes.setdefault(k, {}).setdefault(i["area"], {})[i["id"]] = v
    scores = {}
    for k, por_area in por_mes.items():
        if sum(len(v) for v in por_area.values()) / n_itens >= COBERTURA_MINIMA:
            scores[k] = {ar: media(list(v.values())) for ar, v in por_area.items()}
    return agregar(scores, pesos)


def leitura_mandatos(itens, candles):
    """Per term, which scored items moved most (§10 description, not a score).

    Same window as the term candle: open = points of the year before the inauguration (or the
    first scored year), close = points of the last year of the term. Only points inside the
    frozen goalposts (0-100, base period) are read; a point outside them (1994 inflation) is
    off-scale and skipped. A split year (2016) belongs to both terms, as in the candles.
    """
    out = []
    for c in candles:
        a0, a1 = c["anos"]
        ini = a0 - 1 if a0 > BASE[0] else a0
        fim = min(a1, BASE[1])
        movs = []
        for i in itens:
            p = i["_pontos"]
            s = next((y for y in (ini, ini + 1) if y in p), None)
            e = next((y for y in (fim, fim - 1) if y in p), None)
            if s is None or e is None or e <= s:
                continue
            if not (0 <= p[s] <= 100 and 0 <= p[e] <= 100):
                continue
            movs.append(
                {
                    "id": i["id"],
                    "nome": i["nome"],
                    "area": i["area"],
                    "de": s,
                    "ate": e,
                    "pontos": round(p[e] - p[s], 1),
                }
            )
        movs.sort(key=lambda m: -m["pontos"])
        out.append(
            {
                "gov": c["gov"],
                "anos": [ini, fim],
                "abertura": round(c["o"], 2),
                "fechamento": round(c["c"], 2),
                "n_itens": len(movs),
                "subiram": sum(1 for m in movs if m["pontos"] > 1),
                "cairam": sum(1 for m in movs if m["pontos"] < -1),
                "mais_subiram": movs[:5],
                "mais_cairam": movs[-5:][::-1],
                "nota": c["nota"],
            }
        )
    return out


def _versao(itens, govs, rotulo, mensais=None):
    """Build one version of the index (``N`` or ``N+P``) from scored items: areas, weights, scenarios, robustness."""
    areas_por_ano = {}
    for i in itens:
        for a, v in i["_pontos"].items():
            areas_por_ano.setdefault(a, {}).setdefault(i["area"], {})[i["id"]] = v
    areas = sorted({i["area"] for i in itens})
    n_itens = len(itens)
    scores, cobertura = {}, {}
    for a, por_area in sorted(areas_por_ano.items()):
        presentes = sum(len(v) for v in por_area.values())
        cobertura[a] = presentes / n_itens
        if cobertura[a] >= COBERTURA_MINIMA and a >= BASE[0]:
            scores[a] = {ar: media(list(v.values())) for ar, v in por_area.items()}
    pesos, convergiu, it = ajustar_pesos(scores, areas)
    indice = agregar(scores, pesos)
    nominal = {a: 1 / len(areas) for a in areas}
    cenarios = {
        "S1_pesos_nominais_iguais": agregar(scores, nominal),
        "geometrica": agregar(scores, pesos, "geometrica"),
        "nao_compensatoria_ampi": agregar(scores, pesos, "ampi"),
    }
    rnd = random.Random(SEMENTE)
    fechamentos = {g["id"]: [] for g in govs}
    ranks = {g["id"]: [] for g in govs}
    for _ in range(SORTEIOS):
        draw = [rnd.gammavariate(1.0, 1.0) for _ in areas]
        tot = math.fsum(draw)
        w = {a: d / tot for a, d in zip(areas, draw, strict=True)}
        cs = {c["gov"]: c["c"] for c in mandato_candles(agregar(scores, w), govs)}
        ordem = sorted(cs, key=lambda g: -cs[g])
        for g, v in cs.items():
            fechamentos[g].append(v)
            ranks[g].append(ordem.index(g) + 1)
    candles = mandato_candles(indice, govs)
    mensal = _mensal(itens, pesos, mensais or {})
    mensal_cf = _mensal(itens, pesos, mensais or {}, carry=True)
    base_rank = {c["gov"]: r + 1 for r, c in enumerate(sorted(candles, key=lambda c: -c["c"]))}
    robustez = []
    for g in govs:
        f = sorted(fechamentos[g["id"]])
        if not f:
            continue
        r = ranks[g["id"]]
        robustez.append(
            {
                "gov": g["id"],
                "fechamento": next(c["c"] for c in candles if c["gov"] == g["id"]),
                "p5": f[int(0.05 * len(f))],
                "p95": f[int(0.95 * len(f)) - 1],
                "posicao": base_rank[g["id"]],
                "fracao_mantem_posicao": sum(1 for x in r if x == base_rank[g["id"]]) / len(r),
            }
        )
    return {
        "versao": rotulo,
        "itens": [i["id"] for i in itens],
        "areas": areas,
        "pesos": {"nominal": nominal, "ajustados": pesos, "convergiu": convergiu, "iteracoes": it},
        "importancia_efetiva": importancia_efetiva(scores, indice),
        "cobertura": {str(a): round(c, 4) for a, c in sorted(cobertura.items()) if a >= 1980},
        "scores_areas": {
            str(a): {ar: round(v, 4) for ar, v in sc.items()} for a, sc in sorted(scores.items())
        },
        "serie": {str(a): round(v, 4) for a, v in sorted(indice.items())},
        "cenarios": {
            k: {str(a): round(v, 4) for a, v in sorted(v_.items())} for k, v_ in cenarios.items()
        },
        "candles_mandato": candles,
        "leitura_mandatos": leitura_mandatos(itens, candles),
        "mensal": {k: round(v, 4) for k, v in sorted(mensal.items())},
        "candles_ano": candles_do_indice(mensal),
        "cenario_carry_forward": {
            "nota": "cenário pré-registrado (§9): item sem dado no mês ou no ano toma o último valor publicado; não é o índice padrão",
            "mensal": {k: round(v, 4) for k, v in sorted(mensal_cf.items())},
            "candles_ano": candles_do_indice(mensal_cf),
        },
        "robustez": robustez,
    }


def construir():
    """Compute the scored items and the two versions of the index, N and N+P (pre-registration §3-§10)."""
    obs = _lido("observations.csv")
    govs = [g for g in carregar() if g["posse"].year >= 1995]
    for g in govs:
        g["corrente"] = "data de referencia" in g["fonte"]
    itens_out, excluidos = [], []
    for id_, area, nome, direcao, camada, modo, bases in _itens(obs):
        serie, efeitos = encadear([(r, d) for r, d in bases if d], modo)
        bal = balizas(serie, direcao, BASE)
        n_base = sum(1 for a in serie if BASE[0] <= a <= BASE[1])
        if bal is None or n_base < 10:
            excluidos.append({"id": id_, "motivo": f"{n_base} anos no periodo-base (minimo 10)"})
            continue
        pontos = pontuar(serie, direcao, bal)
        sinal = -1 if direcao == "menor" else 1
        itens_out.append(
            {
                "id": id_,
                "area": area,
                "nome": nome,
                "direcao": direcao,
                "camada": camada,
                "bases": [r for r, d in bases if d],
                "encadeamento": efeitos,
                "balizas": {
                    "pior": sinal * bal[0],
                    "melhor": sinal * bal[1],
                    "periodo": list(BASE),
                },
                "valores": {str(a): round(v, 6) for a, v in sorted(serie.items())},
                "pontos": {str(a): round(v, 4) for a, v in sorted(pontos.items())},
                "_pontos": pontos,
            }
        )
    mensais = _mensais(obs, {i["id"]: i["encadeamento"] for i in itens_out})
    nucleo = [i for i in itens_out if i["camada"] == "N"]
    versoes = {"N": _versao(nucleo, govs, "N", mensais)}
    if len(nucleo) < len(itens_out):
        versoes["N+P"] = _versao(itens_out, govs, "N+P", mensais)
    for i in itens_out:
        del i["_pontos"]
    return {
        "schema": 4,
        "definicoes": __doc__,
        "explica": EXPLICA_INDICE,
        "preregistro": "data/raw/preregistro/PREREGISTRATION-FASE-2.md",
        "periodo_base": list(BASE),
        "itens": itens_out,
        "excluidos": excluidos,
        "versoes": versoes,
        "sorteios": SORTEIOS,
        "semente": SEMENTE,
    }


def gravar():
    """Write ``output/indice.json``; return the number of scored items."""
    d = construir()
    (RAIZ / "output").mkdir(exist_ok=True)
    (RAIZ / "output" / "indice.json").write_text(
        json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    return len(d["itens"])


if __name__ == "__main__":
    print(f"items: {gravar()}")
