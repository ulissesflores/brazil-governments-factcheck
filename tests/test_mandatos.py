"""Term dates -> months covered and omitted (cross-checked against the history RESULTADO)."""

from govfc.mandatos import cobertura


def test_omitted_share():
    c = cobertura()
    assert c["ids_omitidos"] == ["castelo", "geisel", "figueiredo", "sarney", "collor"]
    assert round(c["omitidos"], 1) == 257.6
    assert round(c["total"], 1) == 750.1
    assert round(c["pct_omitido"], 1) == 34.3
