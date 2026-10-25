"""Terminal bundle: yearly candles on rates, pinned on the 12-month IPCA."""

import json
from pathlib import Path

import pytest

from govfc import terminal
from govfc.terminal import candles_anuais, taxa_12m, variacao_12m

RAIZ = Path(__file__).resolve().parents[1]
T = json.loads((RAIZ / "output" / "terminal.json").read_text(encoding="utf-8"))
IND = {i["id"]: i for i in T["indicadores"]}


def test_yearly_candle_from_monthly_values():
    serie = {"2000-11": 9.0, "2000-12": 10.0, "2001-01": 11.0, "2001-06": 8.0, "2001-12": 12.0}
    c = candles_anuais(serie)
    assert c[-1] == {"t": "2001-01-01", "o": 10.0, "h": 12.0, "l": 8.0, "c": 12.0, "n": 3}


def test_12_month_rate_compounds_and_needs_consecutive_months():
    taxas = {f"2001-{m:02d}": 1.0 for m in range(1, 13)}
    assert taxa_12m(taxas)["2001-12"] == pytest.approx(12.6825, abs=1e-3)
    del taxas["2001-06"]
    assert "2001-12" not in taxa_12m(taxas)


def test_12_month_change_of_a_level():
    assert variacao_12m({"2000-03": 50.0, "2001-03": 60.0})["2001-03"] == pytest.approx(20.0)


def test_ipca_2015_candle_closes_at_the_published_12_month_rate():
    c = next(c for c in IND["inflacao"]["candles"] if c["t"].startswith("2015"))
    assert round(c["c"], 2) == 10.67  # IBGE, IPCA acumulado em 2015
    assert round(c["o"], 2) == 6.41  # IPCA acumulado em 2014
    assert c["c"] > c["o"]  # a green candle here means inflation accelerated


def test_no_candles_on_levels_that_only_rise():
    for i in T["indicadores"]:
        assert i["id"] not in ("ipca", "igpdi", "m0", "m1", "m3")
    assert all(i["candles"] == [] for i in T["indicadores"] if i["freq"] == "anual")


def test_signed_band_only_where_a_second_variable_exists():
    com = [i["id"] for i in T["indicadores"] if i["faixa"]]
    assert com == ["selic", "emissao"]
    p = dict((t[:7], v) for t, v in IND["emissao"]["faixa"]["pontos"])
    assert p["2020-12"] > 0  # base money grew faster than prices in 2020


def test_old_and_new_method_lines_overlap_where_the_sources_do():
    m1 = {ln["rotulo"]: {p[0] for p in ln["pontos"]} for ln in IND["emissao"]["linhas"]}
    antigo = next(v for k, v in m1.items() if "antigo" in k)
    novo = next(v for k, v in m1.items() if "Novo" in k)
    assert len(antigo & novo) >= 180  # 2003-12 to 2018-06, monthly


def test_every_indicator_belongs_to_one_domain():
    ids = [i for d in T["dominios"] for i in d["ids"]]
    assert sorted(ids) == sorted(IND) and len(ids) == len(set(ids))


def _principal(ind, gov):
    m = next(m for m in IND[ind]["mandatos"] if m["gov"] == gov)
    return (
        next(b for b in m["bases"] if b["k"] == m["principal"])
        if m["principal"] is not None
        else None
    )


def test_selic_candle_sits_on_the_copom_target_not_on_the_business_day_noise():
    c = {x["t"][:4]: x for x in IND["selic"]["candles"]}
    assert c["2022"]["c"] == 13.75 and c["2022"]["o"] == 9.25  # SGS 432, Dec/2021 and Dec/2022
    assert c["2018"]["c"] == 6.5  # the monthly over annualized gave 6.04 in Dec/2018
    assert min(c) == "1999"  # no Selic candle before the target exists


def test_m0_feb_2001_transcription_error_is_suppressed_not_rewritten():
    p = dict((t[:7], v) for t, v in IND["emissao"]["linhas"][0]["pontos"])
    assert "2002-02" not in p and "2001-02" not in p and "2002-03" in p
    c = next(x for x in IND["emissao"]["candles"] if x["t"].startswith("2002"))
    assert c["l"] > 10  # before amendment 05 the low was 0.00002%


def test_series_with_an_unexplained_jump_are_two_bases():
    assert len(IND["cargos"]["linhas"]) == 2 and len(IND["reprov"]["linhas"]) == 2
    assert _principal("cargos", "bolsonaro") is None  # the base changes inside the term
    assert _principal("cargos", "lula3")["k"] == 1


def test_term_cells_start_before_the_inauguration_and_end_inside_the_term():
    fhc = _principal("inflacao", "fhc")
    assert fhc["inicio"][0] == "1994-12-01" and round(fhc["inicio"][1], 1) == 916.4
    assert fhc["fim"][0] == "2002-12-01" and round(fhc["fim"][1], 1) == 12.5
    dilma = _principal("salmin", "dilma")
    assert dilma["fim"][0] == "2016-08-01"  # Dilma leaves on 2016-08-31
    assert _principal("pobreza", "fhc")["inicio"][0] == "1993-01-01"  # the PNAD skipped 1994
    assert _principal("expvida", "lula3")["fim"][0] == "2024-01-01"  # term in course: latest value
    assert all(len(i["mandatos"]) == 15 for i in T["indicadores"])  # 14 terms + the pre-Real window


def test_every_indicator_has_a_computed_sentence():
    assert IND["inflacao"]["frase"] == "Inflação em 12 meses: 916,4% em dez/1994; 4,3% em dez/2025."
    assert IND["ministerios"]["frase"] == "Ministérios em 1º de janeiro: 20 em 1995; 32 em 2026."
    assert all(i["frase"] for i in T["indicadores"])


def test_every_series_has_its_four_block_explanation():
    for i in T["indicadores"]:
        assert set(i["explica"]) == {"o_que", "como", "porque", "cuidado"}, i["id"]
        assert all(len(i["explica"][k]) > 40 for k in i["explica"]), i["id"]
    assert len([i for i in T["indicadores"] if i["id"].startswith("prod_")]) == 12


def test_products_are_one_series_each_with_three_yardsticks():
    g = IND["prod_gasolina_comum"]
    assert [ln["rotulo"][:5] for ln in g["linhas"]] == ["Horas", "Horas", "Horas"]
    p = dict((t[:7], v) for t, v in g["linhas"][0]["pontos"])
    assert (
        round(p["2002-12"], 2) == 2.2 and round(p["2026-09"], 2) == 0.89
    )  # R$ 2,00 / (200/220) and R$ 6,54 / (1621/220)


def test_committed_bundle_equals_fresh_build():
    novo = terminal.construir()
    assert [i["id"] for i in novo["indicadores"]] == [i["id"] for i in T["indicadores"]]
    assert novo["indicadores"][0]["candles"] == T["indicadores"][0]["candles"]


def test_every_index_item_has_its_own_chart_with_one_line_per_base_newest_first():
    idx = json.loads((RAIZ / "output" / "indice.json").read_text(encoding="utf-8"))
    for it in idx["itens"]:
        assert it["id"] == "homicidios" or it["id"] in IND  # homicidios is the ``homic`` series
        if it["id"] in terminal.UN_ITENS:  # items that had no chart before: raw bases, newest first
            assert [ln["rotulo"] for ln in IND[it["id"]]["linhas"]] == it["bases"][::-1], it["id"]
            assert IND[it["id"]]["candles"] == []
    assert len(terminal.UN_ITENS) == 29
    inf = IND["informalidade"]
    assert inf["linhas"][0]["rotulo"].startswith("PNADC") and inf["frase"].endswith("em 2025.")
    assert inf["pol"] == "menos" and IND["libdem"]["pol"] == "mais"


def test_world_series_draw_brazil_beside_the_preregistered_references():
    m = IND["mun_pib_cresc"]
    assert [ln["rotulo"] for ln in m["linhas"]] == [
        "Brasil",
        "Mundo",
        "América Latina e Caribe",
        "Renda média-alta",
    ]
    g = IND["mun_gini"]  # the PIP has no group aggregates: the first four countries stand in
    assert g["linhas"][0]["rotulo"] == "Brasil" and len(g["linhas"]) == 5
    assert all(i["id"].startswith("mun_") for i in T["indicadores"][-13:])
    assert len(T["indicadores"]) == 102 and len(T["dominios"]) == 19
