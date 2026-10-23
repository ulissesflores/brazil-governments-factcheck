"""Descriptive dynamics: definitions of the pre-registration amendment, pinned on real cells."""

import json
from pathlib import Path

import pytest

from govfc import dinamica
from govfc.dinamica import celula, desvio, luz, ols

RAIZ = Path(__file__).resolve().parents[1]
DIN = json.loads((RAIZ / "output" / "dinamica.json").read_text(encoding="utf-8"))
IND = {i["id"]: i for i in DIN["indicadores"]}


def cel(ind, base_idx, gov):
    return IND[ind]["bases"][base_idx]["celulas"][gov]


def test_ols_on_a_straight_line_has_zero_error():
    b, se = ols([2000, 2001, 2002, 2003], [1.0, 3.0, 5.0, 7.0])
    assert b == pytest.approx(2.0)
    assert se == pytest.approx(0.0)


def test_ols_needs_three_points():
    assert ols([2000, 2001], [1.0, 2.0]) == (None, None)


def test_sample_standard_deviation():
    assert desvio([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]) == pytest.approx(2.138, abs=1e-3)
    assert desvio([1.0]) is None


def test_direction_follows_polarity_not_sign():
    """The same rise is an improvement when "more is better" and a worsening otherwise."""
    serie = {1999: 10.0, 2000: 11.0, 2001: 12.0, 2002: 13.0, 2003: 14.0}
    mais = celula({"tipo": "nivel", "pol": "mais"}, serie, [2000, 2001, 2002, 2003], [], [], 1)
    menos = celula({"tipo": "nivel", "pol": "menos"}, serie, [2000, 2001, 2002, 2003], [], [], 1)
    assert mais["direcao"] == "melhorou" and menos["direcao"] == "piorou"
    assert mais["inicio"] == 10.0 and mais["fim"] == 14.0 and mais["variacao"] == 4.0
    assert mais["tendencia"] == pytest.approx(1.0)


def test_stable_band_is_one_unit_of_the_displayed_precision():
    serie = {1999: 10.00, 2000: 10.02, 2001: 10.05, 2002: 10.04}
    c = celula({"tipo": "nivel", "pol": "mais"}, serie, [2000, 2001, 2002], [], [], 1)
    assert c["direcao"] == "estavel"


def test_too_little_data_gives_no_cell():
    assert (
        celula({"tipo": "nivel", "pol": "mais"}, {2000: 1.0}, [2000, 2001, 2002, 2003], [], [], 1)
        is None
    )


def test_light_rule_from_the_amendment():
    q_nao_medida = {"tipo_de_quebra": "mudanca_de_regra", "efeito_medido": "sem sobreposicao"}
    q_medida_pequena = {
        "tipo_de_quebra": "metodo_estatistico",
        "efeito_medido": "+0,5 p.p. na sobreposicao",
    }
    q_vintage = {"tipo_de_quebra": "revisao_de_vintage", "efeito_medido": ""}
    assert luz([q_nao_medida], 3.0, 1.0, False) == "vermelho"
    assert luz([q_medida_pequena], 3.0, 1.0, False) == "amarelo"
    assert luz([q_medida_pequena], 0.4, 1.0, False) == "vermelho"  # effect as large as the change
    assert luz([q_vintage], 3.0, 1.0, False) == "amarelo"
    assert luz([], 3.0, 0.4, False) == "vermelho"
    assert luz([], 3.0, 0.7, False) == "amarelo"
    assert luz([], 3.0, 1.0, True) == "amarelo"
    assert luz([], 3.0, 1.0, False) == ""


def test_a_term_that_crosses_two_bases_has_no_principal_value_in_either():
    """FHC spans the CID-9 (1995) and CID-10 (1996-2002) homicide bases."""
    bases = IND["seg_homic_taxa"]["bases"]
    assert "fhc" not in bases[0]["celulas"]  # only 1995 under CID-9: not enough years
    assert bases[1]["celulas"]["fhc"]["cruza_base"] is True


def test_homicide_direction_is_not_a_rank():
    """Highest change is not '1st': direction only, and a rise reads as worsening."""
    c = cel("seg_homic_taxa", 1, "fhc")
    assert c["fim"] > c["inicio"] and c["direcao"] == "piorou"


def test_pinned_cells():
    c = cel("inflacao_igpdi", 0, "fhc")
    assert c["direcao"] == "melhorou"
    c = cel("expvida", 0, "bolsonaro")
    assert c["direcao"] == "piorou" and c["luz"] == "amarelo"
    c = cel("senhoriagem_pib", 0, "sarney")
    assert c["media"] == pytest.approx(5.88, abs=0.02)


def test_committed_dinamica_equals_a_fresh_build():
    novo = dinamica.construir()
    for a, b in zip(novo["indicadores"], DIN["indicadores"], strict=True):
        assert a["id"] == b["id"]
        for ba, bb in zip(a["bases"], b["bases"], strict=True):
            assert set(ba["celulas"]) == set(bb["celulas"])
            for g in ba["celulas"]:
                assert ba["celulas"][g]["direcao"] == bb["celulas"][g]["direcao"]
                assert ba["celulas"][g]["luz"] == bb["celulas"][g]["luz"]


def test_candle_fields_and_pre_real_window():
    """Amendment 02: open/close/high/low, the aggregated 1964-1994 window, the per-year rule."""
    c = cel("inflacao_igpdi", 0, "pre_real")
    assert c["n"] == 31 and c["maximo"] == pytest.approx(2708.17, abs=0.01)  # 1993
    assert c["minimo"] == pytest.approx(15.54, abs=0.01)  # 1973
    assert IND["inflacao_ipca"]["log"] is True  # all positive, max/min > 20
    assert IND["inflacao_igpdi"]["log"] is False  # 2017 and 2023 are negative: no log by rule
    assert (
        IND["pib_pc_var_real"]["log"] is False
        and IND["pib_pc_var_real"]["classe_unidade"] == "media"
    )
    assert IND["desemprego"]["classe_unidade"] == "pp"
    assert IND["cestas_por_salario_minimo"]["classe_unidade"] == "pct_geom"
    assert IND["expvida"]["classe_unidade"] == "unid"
    c = cel("pib_pc_var_real", 0, "lula12")
    assert (c["inicio"], c["fim"]) == (pytest.approx(1.8, abs=0.1), pytest.approx(6.7, abs=0.1))
    assert c["maximo"] >= c["fim"] and c["minimo"] <= c["inicio"]
    assert c["acumulado_pct"] is not None
    c = cel("cestas_por_salario_minimo", 0, "pre_real")
    assert c["tend_geom_pct"] == pytest.approx(-3.1, abs=0.05)
    assert DIN["governos"][0]["id"] == "pre_real" and DIN["governos"][0]["agregado"] is True
