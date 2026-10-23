"""Descriptive dynamics of every indicator inside every term, on ONE homogeneous base per cell.

Definitions are those of ``data/raw/preregistro/PREREGISTRATION-EMENDA-01.md`` (sections C and D),
written before the numbers were seen:

* A **base** is one homogeneous series segment (one source, one method). A term is evaluated
  only inside the base that covers it; a term that crosses two bases gets no principal value,
  and the value under each base is kept as a small secondary number. Cells are compared
  (shaded) only inside the same base.
* **Start** = value of the year before the term (or the first year with data); **end** = last
  year of the term with data. **Change** = end minus start for a level; for a flow (a rate such as
  GDP growth or inflation) = mean of the term minus mean of the previous term inside the same base.
* **Trend** = ordinary-least-squares slope over the term's years, with its standard error;
  "too short" below 4 annual values. **Acceleration** = slope of the second half minus slope of the
  first half. **Volatility** = standard deviation of the annual changes (levels) or of the annual
  values (flows). **End-of-term deviation** = (last value minus term mean) / term standard
  deviation. **Reversal** = value of the first year after the term minus the last value.
* **Direction** uses the indicator's polarity (which sign is the usual "better" reading):
  ``melhorou`` / ``piorou`` when the change exceeds one unit of the displayed precision,
  ``estavel`` otherwise, ``sem_base`` when there is no principal value. It is a description of
  the number, not a judgement of the government.
* **Light** (data confidence, not merit): ``vermelho``, ``amarelo`` or none, from the
  method-break catalogue and the coverage, exactly as section D states.
"""

import csv
import json
import math
import re
from datetime import date
from pathlib import Path

from govfc.mandatos import carregar

RAIZ = Path(__file__).resolve().parents[2]
CURADO = RAIZ / "data" / "curated"

#: Indicator shown -> display, polarity, kind, decimals, and the ordered list of bases.
#: A base is (label, substring that identifies the curated ``serie``, first year, last year).
INDICADORES = {
    "pib_pc_var_real": {
        "nome": "PIB per capita, crescimento real",
        "un": "% a.a.",
        "pol": "mais",
        "tipo": "fluxo",
        "dec": 1,
        "dom": "Economia",
        "quebras": ["PIB"],
        "bases": [
            ("IBGE, contas nacionais (via Ipeadata)", "IBGE (oficial 1996-2023)", 1948, 2025)
        ],
    },
    "inflacao_igpdi": {
        "nome": "Inflação anual (IGP-DI, dez/dez)",
        "un": "% a.a.",
        "pol": "menos",
        "tipo": "fluxo",
        "dec": 1,
        "dom": "Economia",
        "quebras": ["IPCA"],
        "log": True,
        "bases": [("IGP-DI, FGV, índice contínuo desde 1944", "IGP-DI dez/dez", 1945, 2025)],
    },
    "inflacao_ipca": {
        "nome": "Inflação anual (IPCA)",
        "un": "% a.a.",
        "pol": "menos",
        "tipo": "fluxo",
        "dec": 1,
        "dom": "Economia",
        "quebras": ["IPCA"],
        "log": True,
        "bases": [("IPCA, IBGE, composto no ano", "IPCA composto", 1980, 2025)],
    },
    "salmin_real": {
        "nome": "Salário mínimo real (dezembro)",
        "un": "R$ de set/2026",
        "pol": "mais",
        "tipo": "nivel",
        "dec": 0,
        "dom": "Trabalho",
        "quebras": ["Salario"],
        "bases": [
            ("Ipea, deflator emendado (IGPC-Mtb até 1979, INPC depois)", "dezembro", 1948, 2025)
        ],
    },
    "desemprego": {
        "nome": "Taxa de desemprego",
        "un": "%",
        "pol": "menos",
        "tipo": "nivel",
        "dec": 1,
        "dom": "Trabalho",
        "quebras": ["Desemprego"],
        "bases": [
            ("PME antiga, 6 regiões metropolitanas", "PME antiga", 1980, 2002),
            ("PME nova, 6 regiões metropolitanas", "PME nova", 2003, 2015),
            ("PNAD Contínua, Brasil", "PNAD Contínua anual", 2012, 2025),
        ],
    },
    "expvida": {
        "nome": "Expectativa de vida ao nascer",
        "un": "anos",
        "pol": "mais",
        "tipo": "nivel",
        "dec": 1,
        "dom": "Saúde",
        "quebras": ["Expectativa"],
        "bases": [("ONU via Banco Mundial, um vintage", "WB-WDI-SP.DYN.LE00.IN", 1960, 2024)],
        "secundarias": [("IBGE, série vigente 2025", "IBGE-Tabuas2024-serie-vigente")],
    },
    "mortinf": {
        "nome": "Mortalidade infantil",
        "un": "por mil nascidos vivos",
        "pol": "menos",
        "tipo": "nivel",
        "dec": 1,
        "dom": "Saúde",
        "quebras": ["mortinf", "Mortalidade infantil"],
        "bases": [("ONU IGME via Banco Mundial", "WB-WDI-SP.DYN.IMRT.IN", 1960, 2024)],
    },
    "sau_dtp3": {
        "nome": "Cobertura vacinal DTP3",
        "un": "%",
        "pol": "mais",
        "tipo": "nivel",
        "dec": 0,
        "dom": "Saúde",
        "quebras": ["sau_dtp3"],
        "bases": [("OMS/UNICEF WUENIC, revisão 2025", "rev2025", 1980, 2025)],
    },
    "seg_homic_taxa": {
        "nome": "Homicídios por 100 mil habitantes",
        "un": "por 100 mil",
        "pol": "menos",
        "tipo": "nivel",
        "dec": 1,
        "dom": "Segurança",
        "quebras": ["seg_homic", "Homic"],
        "bases": [
            ("SIM, CID-9", "AVIOL12_HOMIC", 1980, 1995),
            ("SIM, CID-10", "AVIOL12_HOMIC", 1996, 2024),
        ],
    },
    "pobreza": {
        "nome": "Pobreza, linha de US$ 6,85/dia (PPC 2017)",
        "un": "% da população",
        "pol": "menos",
        "tipo": "nivel",
        "dec": 1,
        "dom": "Renda",
        "quebras": ["Pobreza"],
        "bases": [
            ("Banco Mundial PIP, PNAD", "PIP | US$ 6.85/dia PPC2017", 1981, 2011),
            ("Banco Mundial PIP, PNAD Contínua", "PIP | US$ 6.85/dia PPC2017", 2012, 2024),
        ],
        "secundarias": [("IBGE SIS 2025", "IBGE-SIS2025 | US$ 6,85 PPC2017")],
    },
    "gini": {
        "nome": "Desigualdade (índice de Gini)",
        "un": "0 a 1",
        "pol": "menos",
        "tipo": "nivel",
        "dec": 3,
        "dom": "Renda",
        "quebras": ["Gini"],
        "bases": [
            ("Banco Mundial PIP, PNAD", "PIP | renda dom. per capita", 1981, 2011),
            ("Banco Mundial PIP, PNAD Contínua", "PIP | renda dom. per capita", 2012, 2024),
        ],
    },
    "amb_prodes_amz": {
        "nome": "Desmatamento da Amazônia (PRODES)",
        "un": "km² por ano",
        "pol": "menos",
        "tipo": "fluxo",
        "dec": 0,
        "dom": "Ambiente",
        "quebras": ["amb_"],
        "bases": [("INPE PRODES, taxa consolidada", "consolidados", 1988, 2025)],
    },
    "dem_polyarchy": {
        "nome": "Democracia eleitoral (V-Dem)",
        "un": "índice 0 a 1",
        "pol": "mais",
        "tipo": "nivel",
        "dec": 2,
        "dom": "Democracia",
        "quebras": ["dem_"],
        "bases": [("V-Dem v16, codificação de especialistas", "V-Dem", 1940, 2025)],
    },
    "senhoriagem_pib": {
        "nome": "Imposto inflacionário (transferências totais)",
        "un": "% do PIB",
        "pol": "menos",
        "tipo": "fluxo",
        "dec": 2,
        "dom": "Moeda",
        "quebras": [],
        "bases": [
            (
                "Cysne e Coimbra-Lisboa (2004), fórmula mensal, base M1",
                "TIT, fórmula mensal",
                1947,
                2025,
            )
        ],
    },
}

#: Purchasing-power block (collection ``poder-de-compra``): the minimum wage under several
#: deflators, the DIEESE basket, and the monetary overhang. Each deflator is its own base.
INDICADORES.update(
    {
        "cestas_por_salario_minimo": {
            "nome": "Cestas básicas por salário mínimo",
            "un": "cestas (DIEESE-SP)",
            "pol": "mais",
            "tipo": "nivel",
            "dec": 2,
            "dom": "Poder de compra",
            "quebras": ["Salario", "cesta"],
            "bases": [
                (
                    "DIEESE, cesta de São Paulo, e salário mínimo nominal",
                    "MTE12_SALMIN12 / DIEESE12_CBSP12",
                    1959,
                    2025,
                )
            ],
        },
        "horas_de_trabalho_por_cesta": {
            "nome": "Horas de trabalho para comprar uma cesta",
            "un": "horas (220 h/mês)",
            "pol": "menos",
            "tipo": "nivel",
            "dec": 0,
            "dom": "Poder de compra",
            "quebras": ["Salario", "cesta"],
            "bases": [("DIEESE-SP e salário mínimo, 220 horas por mês", "horas", 1959, 2025)],
        },
        "salario_minimo_real_igpdi": {
            "nome": "Salário mínimo real pelo IGP-DI",
            "un": "R$ de set/2026",
            "pol": "mais",
            "tipo": "nivel",
            "dec": 0,
            "dom": "Poder de compra",
            "quebras": ["Salario"],
            "bases": [("Deflator IGP-DI (FGV), índice contínuo", "IGP-DI", 1948, 2025)],
        },
        "salario_minimo_real_ipcfipe": {
            "nome": "Salário mínimo real pelo IPC-Fipe",
            "un": "R$ de set/2026",
            "pol": "mais",
            "tipo": "nivel",
            "dec": 0,
            "dom": "Poder de compra",
            "quebras": ["Salario"],
            "bases": [("Deflator IPC-Fipe (São Paulo)", "IPC-Fipe", 1948, 2025)],
        },
        "excesso_monetario": {
            "nome": "Excesso monetário (M1 menos PIB real)",
            "un": "pontos percentuais ao ano",
            "pol": "menos",
            "tipo": "fluxo",
            "dec": 1,
            "dom": "Moeda",
            "quebras": ["Agregados"],
            "bases": [
                (
                    "Crescimento de M1 (conceito antigo) menos crescimento real do PIB",
                    "Excesso monetário de M1",
                    1948,
                    2025,
                )
            ],
        },
        "bf_linha_relativa": {
            "nome": "Linha do Bolsa Família em fração do salário mínimo",
            "un": "fração",
            "pol": "mais",
            "tipo": "nivel",
            "dec": 3,
            "dom": "Assistência",
            "quebras": ["Bolsa"],
            "bases": [
                (
                    "Decretos do Bolsa Família e salário mínimo vigente em dezembro",
                    "fração do salário mínimo",
                    2004,
                    2025,
                )
            ],
        },
    }
)

#: Education block: flow rates (rule-dependent) beside Saeb proficiency (rule-independent).
INDICADORES.update(
    {
        "edu_reprovacao_ef_ai__total": {
            "nome": "Reprovação, ensino fundamental anos iniciais (todas as redes)",
            "un": "% dos matriculados",
            "pol": "menos",
            "tipo": "nivel",
            "dec": 1,
            "dom": "Educação",
            "quebras": ["edu_", "Reprov", "rendimento"],
            "bases": [
                (
                    "INEP, Censo Escolar: sinopses até 2005 e planilhas desde 2007",
                    "| BR",
                    1996,
                    2025,
                )
            ],
        },
        "edu_abandono_ef_ai__total": {
            "nome": "Abandono, ensino fundamental anos iniciais (todas as redes)",
            "un": "% dos matriculados",
            "pol": "menos",
            "tipo": "nivel",
            "dec": 1,
            "dom": "Educação",
            "quebras": ["edu_", "Abandono", "rendimento"],
            "bases": [
                (
                    "INEP, Censo Escolar; sinopses até 2005 e planilhas desde 2007",
                    "| BR",
                    1996,
                    2025,
                )
            ],
        },
        "edu_saeb_MT_EF_5ano_4serie": {
            "nome": "Saeb, matemática, 5º ano (4ª série)",
            "un": "pontos na escala Saeb",
            "pol": "mais",
            "tipo": "nivel",
            "dec": 0,
            "dom": "Educação",
            "quebras": ["Saeb", "edu_saeb"],
            "bases": [
                ("INEP, Saeb, escala equalizada (edições 2019 e 2023 coincidem)", "", 1995, 2023)
            ],
        },
        "edu_saeb_LP_EF_5ano_4serie": {
            "nome": "Saeb, português, 5º ano (4ª série)",
            "un": "pontos na escala Saeb",
            "pol": "mais",
            "tipo": "nivel",
            "dec": 0,
            "dom": "Educação",
            "quebras": ["Saeb", "edu_saeb"],
            "bases": [
                ("INEP, Saeb, escala equalizada (edições 2019 e 2023 coincidem)", "", 1995, 2023)
            ],
        },
    }
)

MES = 30.4375


def _lido(nome):
    """Read a curated CSV."""
    with open(CURADO / nome, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _serie(obs, ind, trecho):
    """Annual values ``{year: value}`` of the curated series of ``ind`` whose label has ``trecho``.

    Only four-digit periods count (monthly series are skipped). The IGP-DI and IPCA annual
    rates are derived here from the monthly rows, because the curated layer stores them monthly.
    """
    if ind == "inflacao_igpdi":
        idx = {r["periodo"]: float(r["valor"]) for r in obs if r["indicador"] == "igpdi_indice"}
        return {
            y: (idx[f"{y}-12"] / idx[f"{y - 1}-12"] - 1) * 100
            for y in range(1945, 2026)
            if f"{y}-12" in idx and f"{y - 1}-12" in idx
        }
    if ind == "inflacao_ipca":
        meses = {}
        for r in obs:
            if r["indicador"] == "inflacao_mensal" and r["serie"].startswith("IPCA"):
                meses.setdefault(int(r["periodo"][:4]), []).append(float(r["valor"]))
        return {
            y: (math.prod(1 + x / 100 for x in v) - 1) * 100
            for y, v in meses.items()
            if len(v) == 12
        }
    out = {}
    for r in obs:
        if r["indicador"] == ind and trecho in r["serie"] and re.fullmatch(r"\d{4}", r["periodo"]):
            out.setdefault(int(r["periodo"]), float(r["valor"]))
    return out


def classe_unidade(cfg):
    """Per-year rule of amendment 02, section B, from the indicator's kind and unit.

    Returns
    -------
    str
        ``"media"`` (flow: the term mean is already annual), ``"pp"`` (percentage points per
        year), ``"pct_geom"`` (geometric % per year, for monetary levels and indices) or
        ``"unid"`` (units per year).
    """
    if cfg["tipo"] == "fluxo":
        return "media"
    un = cfg["un"]
    if "%" in un or "fração" in un:
        return "pp"
    if "R$" in un or "US$" in un or "cestas" in un or "horas" in un:
        return "pct_geom"
    return "unid"


def anos_do_mandato(g):
    """Years that belong to a term: the government held office for at least 183 days of the year."""
    saida = []
    for y in range(g["posse"].year, g["saida"].year + 1):
        a, b = max(g["posse"], date(y, 1, 1)), min(g["saida"], date(y + 1, 1, 1))
        if (b - a).days >= 183:
            saida.append(y)
    return saida


def ols(xs, ys):
    """Slope and its standard error by ordinary least squares; ``(None, None)`` below 3 points."""
    n = len(xs)
    if n < 3:
        return None, None
    mx, my = math.fsum(xs) / n, math.fsum(ys) / n
    sxx = math.fsum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return None, None
    b = math.fsum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True)) / sxx
    res = math.fsum((y - (my + b * (x - mx))) ** 2 for x, y in zip(xs, ys, strict=True))
    se = math.sqrt(res / (n - 2) / sxx) if n > 2 else None
    return b, se


def desvio(v):
    """Sample standard deviation; ``None`` below 2 values."""
    if len(v) < 2:
        return None
    m = math.fsum(v) / len(v)
    return math.sqrt(math.fsum((x - m) ** 2 for x in v) / (len(v) - 1))


def _efeito_numerico(texto):
    """First absolute number in a measured-effect text, or ``None`` when nothing was measured."""
    if not texto or "sem sobreposic" in texto.lower() or "nao medid" in texto.lower():
        return None
    m = re.search(r"[-+]?\d+(?:[.,]\d+)?", texto)
    return abs(float(m.group(0).replace(",", "."))) if m else None


def luz(quebras_no_mandato, variacao, cobertura, modelo):
    """Data-confidence light of one cell, section D of the amendment.

    Parameters
    ----------
    quebras_no_mandato : list of dict
        Catalogue rows whose break year falls inside the term.
    variacao : float or None
        Start-to-end change of the cell (absolute value is compared with measured effects).
    cobertura : float
        Share of the term's years with data (0 to 1).
    modelo : bool
        True when the series is a model estimate published by the source.

    Returns
    -------
    str
        ``"vermelho"``, ``"amarelo"`` or ``""``.
    """
    if cobertura < 0.5:
        return "vermelho"
    cor = ""
    for q in quebras_no_mandato:
        ef = _efeito_numerico(q.get("efeito_medido", ""))
        if q["tipo_de_quebra"] in ("mudanca_de_regra", "metodo_estatistico"):
            if ef is None:
                return "vermelho"
            if variacao is not None and ef >= abs(variacao):
                return "vermelho"
            cor = "amarelo"
        else:
            cor = "amarelo"
    if modelo or cobertura < 0.8:
        cor = cor or "amarelo"
    return cor


def _ano_quebra(q):
    """First four-digit year in the break date, or ``None``."""
    m = re.search(r"(19|20)\d\d", q["data_quebra"])
    return int(m.group(0)) if m else None


def celula(cfg, serie, anos, anos_prev, quebras, dec):
    """Compute one (indicator, term) cell on one base.

    Parameters
    ----------
    cfg : dict
        Indicator configuration (polarity, kind).
    serie : dict
        ``{year: value}`` of the base.
    anos : list of int
        Years of the term.
    anos_prev : list of int
        Years of the previous term (for the flow change).
    quebras : list of dict
        Catalogue rows of this indicator.
    dec : int
        Displayed decimals (sets the "stable" band: one unit of the last decimal).

    Returns
    -------
    dict or None
        The cell, or ``None`` when fewer than 2 years (or less than half of a long term) have data.
    """
    pts = [(y, serie[y]) for y in anos if y in serie]
    if len(pts) < 2 or len(pts) < math.ceil(len(anos) / 2):
        return None
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    antes = serie.get(anos[0] - 1)
    inicio = antes if antes is not None else ys[0]
    fim = ys[-1]
    media = math.fsum(ys) / len(ys)
    if cfg["tipo"] == "nivel":
        variacao = fim - inicio
        vol = desvio([b - a for a, b in zip(ys, ys[1:], strict=False)])
    else:
        prev = [serie[y] for y in anos_prev if y in serie]
        variacao = (media - math.fsum(prev) / len(prev)) if len(prev) >= 2 else None
        vol = desvio(ys)
    b, se = ols(xs, ys)
    acel = None
    if len(pts) >= 4:
        h = len(pts) // 2
        b1, _ = ols(xs[:h], ys[:h])
        b2, _ = ols(xs[-h:], ys[-h:])
        acel = None if b1 is None or b2 is None else b2 - b1
    sd = desvio(ys)
    desvio_fim = (fim - media) / sd if sd else None
    depois = serie.get(anos[-1] + 1)
    reversao = None if depois is None else depois - fim
    maximo, minimo = max(ys), min(ys)
    n_anos_span = max(1, anos[-1] - (anos[0] - 1)) if antes is not None else max(1, xs[-1] - xs[0])
    geom = ((fim / inicio) ** (1 / n_anos_span) - 1) * 100 if inicio > 0 and fim > 0 else None
    acumulado = (math.prod(1 + v / 100 for v in ys) - 1) * 100 if cfg["tipo"] == "fluxo" else None
    unidade = 10 ** (-dec)
    if variacao is None:
        direcao = "sem_base"
    elif abs(variacao) < unidade:
        direcao = "estavel"
    else:
        bom = variacao > 0 if cfg["pol"] == "mais" else variacao < 0
        direcao = "melhorou" if bom else "piorou"
    no_mandato = [
        q for q in quebras if (a := _ano_quebra(q)) is not None and anos[0] <= a <= anos[-1]
    ]
    return {
        "inicio": inicio,
        "maximo": maximo,
        "minimo": minimo,
        "tend_geom_pct": geom,
        "acumulado_pct": acumulado,
        "por_ano_simples": variacao / n_anos_span if variacao is not None else None,
        "fim": fim,
        "media": media,
        "variacao": variacao,
        "direcao": direcao,
        "tendencia": b,
        "tendencia_ep": se,
        "aceleracao": acel,
        "volatilidade": vol,
        "desvio_fim": desvio_fim,
        "reversao": reversao,
        "n": len(pts),
        "n_anos": len(anos),
        "de": xs[0],
        "ate": xs[-1],
        "luz": luz(no_mandato, variacao, len(pts) / len(anos), cfg.get("modelo", False)),
        "quebras": [q["id"] for q in no_mandato],
    }


def construir():
    """Compute every cell for every indicator, base and term.

    Returns
    -------
    dict
        ``indicadores`` (configuration, bases with their points, cells per term and base,
        secondary series) and ``governos``.
    """
    obs = _lido("observations.csv")
    quebras = _lido("quebras.csv")
    govs = carregar()
    for g in govs:
        g["anos"] = anos_do_mandato(g)
    pre_real = {
        "id": "pre_real",
        "nome": "Antes do Real (1964-1994)",
        "anos": list(range(1964, 1995)),
        "no_infografico": "AGREGADO",
    }
    govs = [pre_real, *govs]  # the aggregated window is evaluated like a term, on each base
    saida = []
    for ind, cfg in INDICADORES.items():
        qs = [q for q in quebras if any(k in q["indicador"] for k in cfg["quebras"])]
        bases = []
        for rotulo, trecho, y0, y1 in cfg["bases"]:
            s = {y: v for y, v in _serie(obs, ind, trecho).items() if y0 <= y <= y1}
            celulas = {}
            for i, g in enumerate(govs):
                anos = [y for y in g["anos"] if y0 <= y <= y1]
                if len(anos) < len(g["anos"]) and len(anos) < 2:
                    continue
                if g["id"] == "pre_real" and len(anos) < 5:
                    continue  # the aggregated window needs at least five years on this base
                prev = [y for y in (govs[i - 1]["anos"] if i > 1 else []) if y0 <= y <= y1]
                c = celula(cfg, s, anos, prev, qs, cfg["dec"])
                if c:
                    c["cruza_base"] = len(anos) < len(g["anos"])
                    celulas[g["id"]] = c
            bases.append(
                {
                    "rotulo": rotulo,
                    "inicio": y0,
                    "fim": y1,
                    "pontos": [[y, round(v, 6)] for y, v in sorted(s.items())],
                    "celulas": celulas,
                }
            )
        secund = []
        for rotulo, trecho in cfg.get("secundarias", []):
            s = _serie(obs, ind, trecho)
            secund.append(
                {"rotulo": rotulo, "pontos": [[y, round(v, 6)] for y, v in sorted(s.items())]}
            )
        valores = [v for b in bases for _, v in b["pontos"]]
        positivo = bool(valores) and min(valores) > 0
        # bounded = a share or an index (0-1, 0-100); a rate such as "% a.a." is not bounded
        limitado = (
            cfg["un"].startswith(("0 a 1", "índice 0"))
            or any(k in cfg["un"] for k in ("fração", "% da", "% dos", "% de", "cobertura"))
            or cfg["un"] == "%"
        )
        cfg = {
            **cfg,
            "log": positivo and not limitado and max(valores) / min(valores) > 20,
            "classe_unidade": classe_unidade(cfg),
        }
        saida.append(
            {
                "id": ind,
                **{k: v for k, v in cfg.items() if k not in ("bases", "secundarias", "quebras")},
                "bases": bases,
                "secundarias": secund,
                "quebras": [
                    {
                        "id": q["id"],
                        "ano": _ano_quebra(q),
                        "tipo": q["tipo_de_quebra"],
                        "quando": q["data_quebra"][:80],
                        "razao": q["razao_declarada_pela_fonte"][:220],
                        "efeito": q["efeito_medido"][:160],
                        "direcao": q["direcao_do_efeito"],
                        "melhoria": q["apresentada_como_aprimoramento"],
                    }
                    for q in qs
                    if _ano_quebra(q)
                ],
            }
        )
    return {
        "schema": 1,
        "definicoes": __doc__,
        "governos": [
            {
                "id": g["id"],
                "nome": g["nome"],
                "posse": g.get("posse", date(1964, 1, 1)).isoformat(),
                "saida": g.get("saida", date(1994, 12, 31)).isoformat(),
                "anos": g["anos"],
                "omitido": g["no_infografico"] == "NAO",
                "agregado": g["id"] == "pre_real",
            }
            for g in govs
        ],
        "indicadores": saida,
    }


def gravar():
    """Write ``output/dinamica.json``; return the number of cells."""
    d = construir()
    (RAIZ / "output").mkdir(exist_ok=True)
    (RAIZ / "output" / "dinamica.json").write_text(
        json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    return sum(len(b["celulas"]) for i in d["indicadores"] for b in i["bases"])


if __name__ == "__main__":
    print(f"cells: {gravar()}")
