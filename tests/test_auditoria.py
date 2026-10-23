"""Window audit: end-to-end direction against the last 10 and 20 years, on every series."""

import json
from pathlib import Path

from govfc.auditoria import leitura

RAIZ = Path(__file__).resolve().parents[1]
A = json.loads((RAIZ / "output" / "auditoria.json").read_text(encoding="utf-8"))
T = json.loads((RAIZ / "output" / "terminal.json").read_text(encoding="utf-8"))


def test_polarity_reading():
    assert leitura(-5.0, "menos", 20.0) == "melhorou" and leitura(5.0, "menos", 20.0) == "piorou"
    assert leitura(0.1, "mais", 20.0) == "estavel" and leitura(3.0, "neutro", 20.0) == "neutro"


def test_every_terminal_series_and_index_item_is_audited():
    ids = {r["id"] for r in A["linhas"]}
    assert all(i["id"] in ids for i in T["indicadores"])
    assert "idx:N" in ids and "idx:N+P" in ids


def test_products_are_audited_on_three_yardsticks():
    reguas = [r["regua"] for r in A["linhas"] if r["id"] == "prod_carne_bovina"]
    assert len(reguas) == 3 and any("mediana" in x for x in reguas)
    sm = next(
        r
        for r in A["linhas"]
        if r["id"] == "prod_carne_bovina" and r["regua"].startswith("Horas ao salário")
    )
    assert (
        sm["janelas"]["10 anos"]["leitura"] == "piorou"
    )  # beef: 6.5 h (2014) -> 7.6 h (2026) at the minimum wage


def test_flags_name_the_disagreement():
    assert A["bandeiras"] and all("esconde" in b["bandeira"] for b in A["bandeiras"])
