"""Brazil against the pre-registered reference groups, term by term, from ONE source per indicator.

Section A of ``data/raw/preregistro/PREREGISTRATION-EMENDA-01.md``: world (WLD), Latin America and
the Caribbean (LCN), upper-middle-income countries (UMC) and seven Latin American countries. For
every indicator that the ``mundo`` collection carries, Brazil and each reference come from the
SAME series of the same source (World Bank WDI or PIP, UNODC, WUENIC, V-Dem via OWID), so the
difference "Brazil minus reference" compares like with like. The term mean uses the years of the
term that both Brazil and the reference have; a term with fewer than 2 common years, or fewer
than half of its years, gets no value. This is description: no causality, no "wave of the world"
adjustment, no score.
"""

import csv
import json
from pathlib import Path

from govfc.dinamica import anos_do_mandato
from govfc.mandatos import carregar

RAIZ = Path(__file__).resolve().parents[2]
CURADO = RAIZ / "data" / "curated"

GRUPOS = ["WLD", "LCN", "UMC"]
PAISES = ["ARG", "CHL", "COL", "MEX", "PER", "URY", "VEN"]
NOMES = {
    "WLD": "Mundo",
    "LCN": "América Latina e Caribe",
    "UMC": "Renda média-alta",
    "ARG": "Argentina",
    "CHL": "Chile",
    "COL": "Colômbia",
    "MEX": "México",
    "PER": "Peru",
    "URY": "Uruguai",
    "VEN": "Venezuela",
}

#: indicator -> (name pt-BR, unit, polarity, decimals); polarity = usual reading, as in dinamica.
INDICADORES = {
    "mun_pib_cresc": ("Crescimento real do PIB", "% a.a.", "mais", 1),
    "mun_pibpc_ppc": ("PIB per capita, US$ PPC constantes", "US$ PPC 2021", "mais", 0),
    "mun_expvida": ("Expectativa de vida ao nascer", "anos", "mais", 1),
    "mun_mortinf": ("Mortalidade infantil", "por mil", "menos", 1),
    "mun_pobreza_685": ("Pobreza, US$ 6,85/dia (PPC 2017)", "%", "menos", 1),
    "mun_pobreza_830_ppc2021": ("Pobreza, US$ 8,30/dia (PPC 2021)", "%", "menos", 1),
    "mun_gini": ("Índice de Gini", "0 a 100 (PIP)", "menos", 1),
    "mun_homic": ("Homicídios por 100 mil", "por 100 mil", "menos", 1),
    "mun_dtp3": ("Cobertura vacinal DTP3", "%", "mais", 0),
    "mun_inflacao": ("Inflação ao consumidor", "% a.a.", "menos", 1),
    "mun_desemprego_oit": ("Desemprego (modelo OIT)", "%", "menos", 1),
    "mun_polyarchy": ("Democracia eleitoral (V-Dem)", "0 a 1", "mais", 2),
    "mun_divext_rnb": ("Dívida externa total (Banco Mundial, IDS)", "% da RNB", "menos", 1),
}


def _series():
    """Read the ``mun_*`` observations into ``{indicator: {code: {year: value}}}``."""
    out = {}
    with open(CURADO / "observations.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if not r["indicador"].startswith("mun_") or not r["periodo"].isdigit():
                continue
            codigo = r["serie"].rsplit(" | ", 1)[-1]
            out.setdefault(r["indicador"], {}).setdefault(codigo, {})[int(r["periodo"])] = float(
                r["valor"]
            )
    return out


def media_comum(a, b, anos):
    """Term means of two series over the years both have.

    Parameters
    ----------
    a, b : dict
        ``{year: value}`` for Brazil and for the reference.
    anos : list of int
        Years of the term.

    Returns
    -------
    tuple
        ``(mean_a, mean_b, n)`` or ``(None, None, n)`` when fewer than 2 common years or fewer
        than half of the term's years are available.
    """
    comuns = [y for y in anos if y in a and y in b]
    if len(comuns) < 2 or len(comuns) < len(anos) / 2:
        return None, None, len(comuns)
    return (
        sum(a[y] for y in comuns) / len(comuns),
        sum(b[y] for y in comuns) / len(comuns),
        len(comuns),
    )


def construir():
    """Compute Brazil minus reference for every indicator, reference and term.

    Returns
    -------
    dict
        ``indicadores``: for each indicator, ``referencias`` with per-term ``bra``, ``ref``,
        ``dif``, ``n`` and ``leitura`` (``brasil_melhor`` / ``brasil_pior`` / ``igual`` by the
        indicator's polarity, with a band of one unit of the displayed precision).
    """
    series = _series()
    govs = carregar()
    for g in govs:
        g["anos"] = anos_do_mandato(g)
    saida = []
    for ind, (nome, un, pol, dec) in INDICADORES.items():
        por_codigo = series.get(ind, {})
        bra = por_codigo.get("BRA", {})
        refs = []
        for cod in GRUPOS + PAISES:
            ref = por_codigo.get(cod)
            if not ref:
                continue
            celulas = {}
            for g in govs:
                mb, mr, n = media_comum(bra, ref, g["anos"])
                if mb is None:
                    continue
                dif = mb - mr
                if abs(dif) < 10 ** (-dec):
                    leitura = "igual"
                else:
                    melhor = dif > 0 if pol == "mais" else dif < 0
                    leitura = "brasil_melhor" if melhor else "brasil_pior"
                celulas[g["id"]] = {
                    "bra": mb,
                    "ref": mr,
                    "dif": dif,
                    "n": n,
                    "n_anos": len(g["anos"]),
                    "leitura": leitura,
                }
            refs.append(
                {
                    "codigo": cod,
                    "nome": NOMES[cod],
                    "grupo": cod in GRUPOS,
                    "pontos": [[y, round(v, 6)] for y, v in sorted(ref.items())],
                    "celulas": celulas,
                }
            )
        saida.append(
            {
                "id": ind,
                "nome": nome,
                "un": un,
                "pol": pol,
                "dec": dec,
                "bra": [[y, round(v, 6)] for y, v in sorted(bra.items())],
                "referencias": refs,
            }
        )
    return {"schema": 1, "definicoes": __doc__, "indicadores": saida}


def gravar():
    """Write ``output/mundo.json``; return the number of cells."""
    d = construir()
    (RAIZ / "output").mkdir(exist_ok=True)
    (RAIZ / "output" / "mundo.json").write_text(
        json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    return sum(len(r["celulas"]) for i in d["indicadores"] for r in i["referencias"])


if __name__ == "__main__":
    print(f"cells: {gravar()}")
