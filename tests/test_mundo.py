"""Brazil minus reference: same source on both sides, pre-registered groups, descriptive only."""

import json
from pathlib import Path

import pytest

from govfc import mundo

RAIZ = Path(__file__).resolve().parents[1]
M = json.loads((RAIZ / "output" / "mundo.json").read_text(encoding="utf-8"))
IND = {i["id"]: i for i in M["indicadores"]}


def ref(ind, cod):
    return next(r for r in IND[ind]["referencias"] if r["codigo"] == cod)


def test_pre_registered_groups_are_present_for_gdp_growth():
    assert {r["codigo"] for r in IND["mun_pib_cresc"]["referencias"]} >= {
        "WLD",
        "LCN",
        "UMC",
        "ARG",
        "CHL",
        "MEX",
    }


def test_gdp_growth_lula12_and_dilma_against_latin_america():
    """Numbers reported by the collection: 4.08 vs 3.76 (Lula 1-2) and 0.43 vs 1.74 (Dilma)."""
    c = ref("mun_pib_cresc", "LCN")["celulas"]
    assert c["lula12"]["bra"] == pytest.approx(4.08, abs=0.05)
    assert c["lula12"]["ref"] == pytest.approx(3.76, abs=0.05)
    assert c["lula12"]["leitura"] == "brasil_melhor"
    assert c["dilma"]["bra"] == pytest.approx(0.43, abs=0.05)
    assert c["dilma"]["ref"] == pytest.approx(1.74, abs=0.05)
    assert c["dilma"]["leitura"] == "brasil_pior"


def test_common_years_rule():
    a = {2000: 1.0, 2001: 2.0, 2002: 3.0, 2003: 4.0}
    b = {2000: 0.0, 2001: 0.0}
    assert mundo.media_comum(a, b, [2000, 2001, 2002, 2003]) == (1.5, 0.0, 2)
    assert mundo.media_comum(a, {2000: 0.0}, [2000, 2001, 2002, 2003])[0] is None


def test_no_interpolation_venezuela_gdp_per_capita_is_absent():
    assert "VEN" not in {r["codigo"] for r in IND["mun_pibpc_ppc"]["referencias"]}


def test_committed_equals_fresh_build():
    novo = mundo.construir()
    for a, b in zip(novo["indicadores"], M["indicadores"], strict=True):
        assert a["id"] == b["id"]
        for ra, rb in zip(a["referencias"], b["referencias"], strict=True):
            assert ra["codigo"] == rb["codigo"]
            assert {g: c["leitura"] for g, c in ra["celulas"].items()} == {
                g: c["leitura"] for g, c in rb["celulas"].items()
            }
