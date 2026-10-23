"""Apply the single verdict rule to every number of the infographic and write ``results.json``.

Each infographic number is reproduced under ONE primary specification per indicator
(declared in :data:`ESPECIFICACAO` and in ``docs/*/METHODOLOGY.md``). Alternatives that were
also tried are written next to it as *sensitivity*; they never change the verdict.

Limitation, stated plainly: the primary specifications were fixed on 2026-10-19 after an
exploratory pass over the data (the area ``RESULTADO.md`` files), so the verdicts describe
how the printed numbers relate to public data; they are not a pre-registered test.
"""

import csv
import json
import math
import re
from pathlib import Path

from govfc.verdict import APROXIMADO, NAO_REPRODUZ, NAO_VERIFICADO, REPRODUZ, SIMBOLO, veredito

#: Rank used only to pick the closest sensitivity alternative (lower = closer).
ORDEM = {REPRODUZ: 0, APROXIMADO: 1, NAO_REPRODUZ: 2, NAO_VERIFICADO: 3}

RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw"
SAIDA = RAIZ / "output"

COLUNAS = ["ditadura", "itamar", "fhc", "lula12", "dilma", "temer", "bolsonaro", "lula3"]

#: Mandate months (start, end) used only by the sensitivity "annualised over the mandate".
#: Source: ``data/raw/historia/RESULTADO.md`` table 1.
MANDATO = {
    "itamar": ((1992, 10), (1994, 12)),
    "fhc": ((1995, 1), (2002, 12)),
    "lula12": ((2003, 1), (2010, 12)),
    "dilma": ((2011, 1), (2016, 8)),
    "temer": ((2016, 9), (2018, 12)),
    "bolsonaro": ((2019, 1), (2022, 12)),
    "lula3": ((2023, 1), (2025, 12)),
}

ESPECIFICACAO = {
    "pib": "Ipeadata SCN10_PIBG10 (IBGE national accounts): arithmetic mean of the annual real "
    "growth rates over the printed calendar-year window.",
    "inflacao": "BCB SGS 433 (IPCA): monthly rates compounded per calendar year, arithmetic mean "
    "of the annual rates over the printed window. IPCA does not exist before 1980.",
    "desemprego": "Series whose coverage includes the whole printed window, never spliced: "
    "PME antiga (<=2002), PME nova (2003-2015), PNAD Continua annual (>=2012). No series -> not "
    "verified. The row label says 'regioes metro.', which is the PME universe.",
    "salmin": "Ipea GAC12_SALMINRE12 (real minimum wage): December of the last window year over "
    "December of the year before the window.",
    "pobreza": "World Bank PIP, US$ 6.85/day (2017 PPP), the single series that covers 1981-2024 "
    "with one method; compared at the printed year. IBGE SIS vintages enter as sensitivity. "
    "No printed year -> not verified.",
    "gini": "World Bank PIP, Gini of household per-capita income, one series for 1981-2024, at "
    "the printed year. IBGE (PNADC) and Ipea (PNAD) enter as sensitivity. No year -> not verified.",
    "expvida": "World Bank WDI SP.DYN.LE00.IN (UN WPP), one vintage for 1960-2024, at the printed "
    "year. IBGE vintages enter as sensitivity. No printed year -> not verified.",
}
UNIDADE = {
    "pib": "pct",
    "inflacao": "pct",
    "desemprego": "pct",
    "salmin": "pct",
    "pobreza": "pct",
    "gini": "indice",
    "expvida": "anos",
}
CAMPO = {
    "pib": ("pib_medio_anual_pct", "pib_janela"),
    "inflacao": ("ipca_medio_anual_pct", "ipca_janela"),
    "desemprego": ("desemprego_pct", "desemprego_janela"),
    "salmin": ("salario_minimo_real_var_pct", "salmin_janela"),
    "pobreza": ("pobreza_pct", "pobreza_ano"),
    "gini": ("gini", "gini_ano"),
    "expectativa": ("expectativa_vida_anos", "expvida_ano"),
}
CAMPO["expvida"] = CAMPO.pop("expectativa")


def janela(texto):
    """Parse a printed window such as ``"1968-1973"``, ``"1994"`` or ``"1990 (referencia)"``.

    Parameters
    ----------
    texto : str
        Window as printed on the infographic.

    Returns
    -------
    tuple of int or None
        ``(first_year, last_year)``; ``None`` when the text does not start with a year
        (for instance ``"anos 1970"``).
    """
    m = re.match(r"\s*(\d{4})(?:\s*-\s*(\d{4}))?", texto)
    return None if not m else (int(m[1]), int(m[2] or m[1]))


def _csv(caminho):
    """Read a CSV file into a list of dicts."""
    with open(caminho, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _media(valores):
    """Arithmetic mean, or ``None`` if any value is missing or the list is empty."""
    if not valores or any(v is None for v in valores):
        return None
    return math.fsum(valores) / len(valores)


def _geo(valores):
    """Geometric mean of percentage rates, or ``None`` if any value is missing."""
    if not valores or any(v is None for v in valores):
        return None
    return (math.prod(1 + v / 100 for v in valores) ** (1 / len(valores)) - 1) * 100


def _num(txt):
    """Float from a CSV cell, or ``None`` when empty."""
    return float(txt) if txt not in ("", None) else None


def _mensal(arquivo):
    """Load a BCB SGS monthly JSON into ``{(year, month): percent}``."""
    dados = json.loads((RAW / "inflacao" / arquivo).read_text())
    return {(int(r["data"][-4:]), int(r["data"][3:5])): float(r["valor"]) for r in dados}


def _anual_composto(mensal):
    """Compound monthly rates into calendar-year rates (complete years only)."""
    anos = {}
    for ano in sorted({a for a, _ in mensal}):
        meses = [mensal.get((ano, m)) for m in range(1, 13)]
        if None not in meses:
            anos[ano] = (math.prod(1 + x / 100 for x in meses) - 1) * 100
    return anos


def _anualizada(mensal, inicio, fim):
    """Annualised compound rate between two ``(year, month)`` limits, inclusive."""
    p, n = 1.0, 0
    for (a, m), x in mensal.items():
        if inicio <= (a, m) <= fim:
            p *= 1 + x / 100
            n += 1
    return (p ** (12 / n) - 1) * 100 if n else None


def _igpdi_dez():
    """IGP-DI December-over-December (Ipeadata IGP12_IGPDI12 index), by year."""
    j = json.loads((RAW / "inflacao" / "igpdi-ipeadata-raw.json").read_text())["value"]
    ix = {(int(r["VALDATA"][:4]), int(r["VALDATA"][5:7])): r["VALVALOR"] for r in j}
    return {
        a: (ix[(a, 12)] / ix[(a - 1, 12)] - 1) * 100
        for a in range(1945, 2026)
        if (a, 12) in ix and (a - 1, 12) in ix
    }


def _alt(rotulo, valor, impresso, unidade):
    """Build one sensitivity entry (label, value, verdict under the same rule)."""
    return {
        "rotulo": rotulo,
        "valor": None if valor is None else round(valor, 4),
        "veredito": veredito(impresso, valor, unidade),
    }


def _deslocadas(rotulo, serie, a, b, impresso):
    """Sensitivity: the same series over the window minus its first / last year."""
    alts = []
    for nome, (x, y) in (("without first year", (a + 1, b)), ("without last year", (a, b - 1))):
        if x <= y:
            alts.append(
                _alt(
                    f"{rotulo}, window {x}-{y} ({nome})",
                    _media([serie.get(k) for k in range(x, y + 1)]),
                    impresso,
                    "pct",
                )
            )
    return alts


def linha_pib(col, impresso, win, tab):
    """Reproduce a GDP-growth cell.

    Parameters
    ----------
    col : str
        Column slug (unused here, kept for a uniform signature).
    impresso : str
        Printed value.
    win : tuple of int or None
        Printed window.
    tab : dict
        Preloaded tables (see :func:`construir`).

    Returns
    -------
    tuple
        ``(primary_value, sensitivity_list, note)``.
    """
    if win is None:
        return None, [], "no printed window"
    serie = [tab["pib"].get(a) for a in range(win[0], win[1] + 1)]
    alts = [_alt("geometric mean of the same annual rates", _geo(serie), impresso, "pct")]
    alts += _deslocadas("arithmetic mean", tab["pib"], win[0], win[1], impresso)
    return _media(serie), alts, ""


def linha_inflacao(col, impresso, win, tab):
    """Reproduce an inflation cell (see :func:`linha_pib` for parameters and return)."""
    if win is None:
        return None, [], "no printed window"
    a, b = win
    alts = []
    ipca = tab["ipca"]
    prim = _media([ipca.get(x) for x in range(a, b + 1)])
    note = "" if prim is not None else "IPCA does not exist for this window (starts in 1980)"
    alts.append(
        _alt("IPCA, geometric mean", _geo([ipca.get(x) for x in range(a, b + 1)]), impresso, "pct")
    )
    for nome, chave in (("INPC", "inpc"), ("IGP-M", "igpm"), ("IGP-DI (BCB)", "igpdi")):
        alts.append(
            _alt(
                f"{nome}, arithmetic mean of calendar years",
                _media([tab[chave].get(x) for x in range(a, b + 1)]),
                impresso,
                "pct",
            )
        )
    alts.append(
        _alt(
            "IGP-DI December/December (Ipeadata), arithmetic mean",
            _media([tab["igpdi_dez"].get(x) for x in range(a, b + 1)]),
            impresso,
            "pct",
        )
    )
    alts += _deslocadas("IPCA arithmetic mean", ipca, a, b, impresso)
    if col in MANDATO:
        ini, fim = MANDATO[col]
        alts.append(
            _alt(
                "IPCA annualised over the mandate months",
                _anualizada(tab["ipca_mensal"], ini, fim),
                impresso,
                "pct",
            )
        )
    return prim, alts, note


def _serie_desemprego(a, b):
    """Choose the unemployment column whose coverage includes ``[a, b]`` (or ``None``)."""
    if a >= 1980 and b <= 2002:
        return "PME_antiga_15mais_30d_6RMs"
    if a >= 2003 and b <= 2015:
        return "PME_nova_10mais_semana_6RMs"
    if a >= 2012:
        return "PNADC_SIDRA_4562"
    return None


def linha_desemprego(col, impresso, win, tab):
    """Reproduce an unemployment cell; ``"x->y"`` prints compare start and end years."""
    if win is None:
        return None, [], "no printed window"
    a, b = win
    colname = _serie_desemprego(a, b)
    alts = []
    for nome in tab["desemprego_cols"]:
        v = [tab["desemprego"].get(x, {}).get(nome) for x in range(a, b + 1)]
        if nome != colname and None not in v:
            alts.append(_alt(f"{nome}, arithmetic mean", _media(v), impresso, "pct"))
    if colname is None:
        return None, alts, "no official series covers the whole printed window"
    v = [tab["desemprego"].get(x, {}).get(colname) for x in range(a, b + 1)]
    return _media(v), alts, f"series {colname}"


def linha_salmin(col, impresso, win, tab):
    """Reproduce a real-minimum-wage cell (December over December)."""
    if win is None:
        return None, [], "no printed window"
    a, b = win
    sal = tab["salmin"]
    dez = lambda y: sal.get(y, {}).get("dez")  # noqa: E731
    med = lambda y: sal.get(y, {}).get("med")  # noqa: E731

    def razao(f):
        """Percent change of ``f`` from year ``a-1`` to year ``b``."""
        x0, x1 = f(a - 1), f(b)
        return None if x0 is None or x1 is None else (x1 / x0 - 1) * 100

    alts = [
        _alt("annual average over annual average", razao(med), impresso, "pct"),
        _alt(
            "mean of the yearly changes of the annual average",
            _media([sal.get(y, {}).get("var") for y in range(a, b + 1)]),
            impresso,
            "pct",
        ),
    ]
    return razao(dez), alts, ""


def _social(tab, indicador, ano, preferidos, impresso, unidade):
    """Reproduce a social-indicator cell: first preferred (source, line) with that year."""
    if ano is None:
        return None, [], "no printed year"
    linhas = [r for r in tab[indicador] if int(r["ano"]) == ano]
    prim, nota = None, "no source has this year"
    usados = None
    for fonte, linha in preferidos:
        for r in linhas:
            if r["fonte"] == fonte and (linha is None or r["definicao_linha"] == linha):
                prim, nota, usados = float(r["valor"]), f"{fonte} / {r['definicao_linha']}", r
                break
        if prim is not None:
            break
    alts = [
        _alt(f"{r['fonte']} / {r['definicao_linha']}", float(r["valor"]), impresso, unidade)
        for r in linhas
        if r is not usados
    ]
    return prim, alts, nota


def linha_pobreza(col, impresso, win, tab):
    """Reproduce a poverty cell (World Bank PIP, one series, US$ 6.85/day)."""
    return _social(
        tab,
        "pobreza",
        None if win is None else win[0],
        [("PIP", "US$ 6.85/dia PPC2017")],
        impresso,
        "pct",
    )


def linha_gini(col, impresso, win, tab):
    """Reproduce a Gini cell (World Bank PIP, one series)."""
    return _social(
        tab,
        "gini",
        None if win is None else win[0],
        [("PIP", None)],
        impresso,
        "indice",
    )


def linha_expvida(col, impresso, win, tab):
    """Reproduce a life-expectancy cell (World Bank WDI / UN WPP, one vintage)."""
    return _social(
        tab,
        "expvida",
        None if win is None else win[0],
        [("WB-WDI-SP.DYN.LE00.IN", None)],
        impresso,
        "anos",
    )


FUNCOES = {
    "pib": linha_pib,
    "inflacao": linha_inflacao,
    "desemprego": linha_desemprego,
    "salmin": linha_salmin,
    "pobreza": linha_pobreza,
    "gini": linha_gini,
    "expvida": linha_expvida,
}


def carregar():
    """Load every sealed input table the engine needs.

    Returns
    -------
    dict
        Annual series and long-format social tables, all read from ``data/raw``.
    """
    er = RAW / "economia-real"
    des = {
        int(r["ano"]): {k: _num(v) for k, v in r.items() if k != "ano"}
        for r in _csv(er / "saida-desemprego-anual.csv")
    }
    # a PME year only counts when all 12 months exist (the column "meses_*" says so)
    for r in des.values():
        for nome, meses in (
            ("PME_antiga_15mais_30d_6RMs", "meses_PME_antiga"),
            ("PME_nova_10mais_semana_6RMs", "meses_PME_nova"),
        ):
            if r.get(meses) != 12:
                r[nome] = None
    sal = {
        int(r["ano"]): {
            "med": _num(r["media_anual_real_R$_set2026"]),
            "dez": _num(r["dezembro_real_R$_set2026"]),
            "var": _num(r["var_media_anual_pct"]),
        }
        for r in _csv(er / "saida-salmin-real-anual.csv")
    }
    mensal = {
        "ipca": _mensal("ipca-sgs433-raw.json"),
        "inpc": _mensal("inpc-sgs188-raw.json"),
        "igpm": _mensal("igpm-sgs189-raw.json"),
        "igpdi": _mensal("igpdi-sgs190-raw.json"),
    }
    tab = {k: _anual_composto(v) for k, v in mensal.items()}
    tab.update(
        ipca_mensal=mensal["ipca"],
        igpdi_dez=_igpdi_dez(),
        desemprego=des,
        salmin=sal,
        desemprego_cols=[c for c in next(iter(des.values())) if not c.startswith("meses_")],
        pib={
            int(r["ano"]): _num(r["pib_real_var_pct_SCN10_PIBG10"])
            for r in _csv(er / "saida-pib-anual-1948-2025.csv")
        },
    )
    for nome in ("pobreza", "gini", "expvida"):
        tab[nome] = _csv(RAW / "social" / "series" / f"{nome}.csv")
    return tab


def construir():
    """Build the full list of rows (infographic number x primary reproduction x verdict).

    Returns
    -------
    list of dict
        One dict per printed number, in column order then indicator order.
    """
    tab = carregar()
    celulas = _csv(RAIZ / "data" / "infographic" / "infografico-transcrito.csv")
    linhas = []
    for slug, cel in zip(COLUNAS, celulas, strict=True):
        for ind, (campo, campo_janela) in CAMPO.items():
            bruto = cel[campo].strip()
            win = janela(cel[campo_janela])
            partes = [p.strip() for p in bruto.split("->")] if "->" in bruto else [bruto]
            for i, impresso in enumerate(partes):
                w = win
                sufixo = ""
                if len(partes) == 2 and win:
                    w = (win[0], win[0]) if i == 0 else (win[1], win[1])
                    sufixo = ".inicio" if i == 0 else ".fim"
                limpo = impresso.split(" ")[0]
                prim, alts, nota = FUNCOES[ind](slug, limpo, w, tab)
                ver = veredito(limpo, prim, UNIDADE[ind])
                melhor = min((a for a in alts), key=lambda a: ORDEM[a["veredito"]], default=None)
                if melhor is not None and ORDEM[melhor["veredito"]] >= ORDEM[ver]:
                    melhor = None
                linhas.append(
                    {
                        "id": f"{slug}.{ind}{sufixo}",
                        "coluna": cel["coluna"],
                        "indicador": ind,
                        "impresso": impresso,
                        "janela": cel[campo_janela],
                        "unidade": UNIDADE[ind],
                        "especificacao_primaria": ESPECIFICACAO[ind],
                        "valor_reproduzido": None if prim is None else round(prim, 4),
                        "veredito": ver,
                        "nota": nota,
                        "n_alternativas": len(alts),
                        "melhor_alternativa": melhor,
                        "sensibilidade": alts,
                    }
                )
    return linhas


def _csv_num(caminho):
    """Read a CSV and convert every numeric-looking cell to ``float`` (empty -> ``None``)."""
    out = []
    for r in _csv(caminho):
        linha = {}
        for k, v in r.items():
            try:
                linha[k] = None if v == "" else round(float(v), 4)
            except ValueError:
                linha[k] = v
        out.append(linha)
    return out


def construir_monetario():
    """Collect the monetary block (derived CSVs of ``data/raw/monetario/saida``).

    Returns
    -------
    dict
        ``senhoriagem`` (seigniorage and inflation tax by term), ``agregados`` (money aggregates
        as % of GDP by term) and ``extras`` (exchange rate, Selic, real interest, primary
        balance, debt, reserves by term). Values are passed through unchanged (rounded to 4
        decimals); the derivation scripts and their raw inputs are sealed with the repository.
    """
    base = RAW / "monetario" / "saida"
    return {
        "senhoriagem": _csv_num(base / "senhoriagem_janelas.csv"),
        "agregados": _csv_num(base / "agregados_governos.csv"),
        "extras": _csv_num(base / "extras_janelas.csv"),
    }


def resumo(linhas):
    """Count verdicts overall and per indicator.

    Parameters
    ----------
    linhas : list of dict
        Output of :func:`construir`.

    Returns
    -------
    dict
        ``{"total": {...}, "por_indicador": {...}}`` with verdict counts.
    """

    def cont(sub):
        """Count verdict labels in ``sub``."""
        out = {}
        for r in sub:
            out[r["veredito"]] = out.get(r["veredito"], 0) + 1
        return dict(sorted(out.items()))

    return {
        "total": cont(linhas),
        "por_indicador": {i: cont([r for r in linhas if r["indicador"] == i]) for i in FUNCOES},
    }


def main():
    """Write ``output/results.json`` and print a one-line summary per verdict."""
    linhas = construir()
    doc = {
        "schema": 1,
        "infografico": "data/infographic/infografico-original-whatsapp-2026-10-19.jpeg",
        "regra_veredito": "src: code/govfc/verdict.py; tolerance 0.3 pp (pct) or 5 % relative",
        "linhas": linhas,
        "resumo": resumo(linhas),
        "monetario": construir_monetario(),
    }
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / "results.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    for k, n in doc["resumo"]["total"].items():
        print(f"{SIMBOLO[k]} {k}: {n}")


if __name__ == "__main__":
    main()
