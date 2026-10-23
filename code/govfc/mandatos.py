"""Government terms (1964-2026) and the share of time the infographic leaves out.

Months are ``days / 30.4375`` (the mean Gregorian month). The last term ends at the repository
reference date, not at the end of the mandate. Source dates: ``data/curated/mandatos.csv``.
"""

import csv
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
MES = 30.4375


def carregar():
    """Read the curated terms.

    Returns
    -------
    list of dict
        One dict per term with ``posse`` and ``saida`` as :class:`datetime.date` and
        ``meses`` (float).
    """
    with open(RAIZ / "data" / "curated" / "mandatos.csv", newline="", encoding="utf-8") as fh:
        linhas = list(csv.DictReader(fh))
    for r in linhas:
        r["posse"] = date.fromisoformat(r["posse"])
        r["saida"] = date.fromisoformat(r["saida"])
        r["meses"] = (r["saida"] - r["posse"]).days / MES
    return linhas


def cobertura():
    """Sum the months covered and omitted by the infographic.

    Returns
    -------
    dict
        ``total``, ``cobertos`` and ``omitidos`` in months, ``pct_omitido`` and the ids of
        the omitted terms (the 0.4-month interim of Mazzilli is not in the table).
    """
    ls = carregar()
    omit = [r for r in ls if r["no_infografico"] == "NAO" and r["id"] != "junta"]
    cobertos = sum(r["meses"] for r in ls if r["no_infografico"] == "SIM")
    cobertos += sum(r["meses"] for r in ls if r["id"] == "junta")  # inside the 1967-1974 column
    om = sum(r["meses"] for r in omit)
    return {
        "total": cobertos + om,
        "cobertos": cobertos,
        "omitidos": om,
        "pct_omitido": 100 * om / (cobertos + om),
        "ids_omitidos": [r["id"] for r in omit],
    }
