"""Phase-2 composite index: the sealed rules, checked one by one on the committed bundle."""

import json
from pathlib import Path

import pytest

from govfc import indice
from govfc.indice import agregar, ajustar_pesos, ampi, balizas, encadear, pontuar

RAIZ = Path(__file__).resolve().parents[1]
BUNDLE = json.loads((RAIZ / "output" / "indice.json").read_text(encoding="utf-8"))
ITENS = {i["id"]: i for i in BUNDLE["itens"]}
N = BUNDLE["versoes"]["N"]
NP = BUNDLE["versoes"]["N+P"]


def test_polarity_is_applied_before_the_goalposts():
    serie = {1995: 10.0, 2000: 2.0, 2010: 6.0}
    bal = balizas(serie, "menor", (1995, 2024))
    assert bal == (-10.0, -2.0)  # worst = 10 (polarised -10), best = 2
    p = pontuar(serie, "menor", bal)
    assert p[1995] == 0 and p[2000] == 100 and p[2010] == pytest.approx(50)


def test_goalposts_are_frozen_on_the_base_period_and_scores_are_not_clipped():
    assert BUNDLE["periodo_base"] == [1995, 2024]
    for i in BUNDLE["itens"]:
        assert i["balizas"]["periodo"] == [1995, 2024]
    p = ITENS["homicidios"]["pontos"]
    assert all(0 <= v <= 100 for a, v in p.items() if 1995 <= int(a) <= 2024)
    assert any(
        v < 0 or v > 100 for i in BUNDLE["itens"] for a, v in i["pontos"].items() if int(a) < 1995
    )


def test_breaks_are_chained_only_through_a_measured_overlap():
    serie, efeitos = encadear(
        [("velha", {2000: 10.0, 2001: 11.0}), ("nova", {2001: 13.0, 2002: 14.0})], "diferenca"
    )
    assert efeitos[0]["sobreposicao"] == 1 and efeitos[0]["efeito"] == {"diferenca": 2.0}
    assert serie == {2000: 12.0, 2001: 13.0, 2002: 14.0}
    serie, efeitos = encadear(
        [("velha", {2000: 1.0, 2001: 2.0, 2002: 3.0}), ("nova", {2004: 9.0})], "diferenca"
    )
    assert (
        efeitos[0]["sobreposicao"] == 0 and efeitos[0]["mantida"] == "velha" and 2004 not in serie
    )
    d = ITENS["divida"]["encadeamento"][0]
    assert d["sobreposicao"] == 20 and d["efeito"]["diferenca"] == pytest.approx(-9.06, abs=0.01)


def test_no_imputation_and_the_coverage_rule():
    assert "2000" not in N["serie"]  # the PNAD skipped 2000: too few items that year
    assert N["cobertura"]["2000"] < 0.7 < N["cobertura"]["2005"]
    assert all(a in N["serie"] for a, c in N["cobertura"].items() if c >= 0.7 and int(a) >= 1995)
    assert all(float(N["cobertura"][a]) >= 0.7 for a in N["serie"])


def test_area_weights_fall_back_to_equal_when_effective_importance_cannot_be_equalised():
    k = len(N["areas"])
    assert N["pesos"]["convergiu"] is False
    assert all(w == pytest.approx(1 / k) for w in N["pesos"]["ajustados"].values())
    assert N["importancia_efetiva"]["Segurança"] < 0.05  # homicides rose then fell: uncorrelated


def test_weight_tuning_stays_inside_the_declared_box():
    areas = {
        y: {"a": float(y), "b": float(y) * 3 + (y % 2), "c": 50.0 + (y % 3)}
        for y in range(1995, 2025)
    }
    pesos, _, it = ajustar_pesos(areas, ["a", "b", "c"])
    assert it <= 100 and all(0.5 / 3 - 1e-9 <= w <= 2 / 3 + 1e-9 for w in pesos.values())


def test_aggregation_default_is_arithmetic_with_scenarios():
    s = {2001: {"x": 20.0, "y": 80.0}}
    assert agregar(s, {"x": 0.5, "y": 0.5})[2001] == 50.0
    assert agregar(s, {"x": 0.5, "y": 0.5}, "geometrica")[2001] == pytest.approx(40.0)
    assert ampi([20.0, 80.0]) == pytest.approx(50.0 - 30.0 * 0.6)
    assert set(N["cenarios"]) == {
        "S1_pesos_nominais_iguais",
        "geometrica",
        "nao_compensatoria_ampi",
    }


def test_term_candles_open_on_the_year_before_the_inauguration_or_declare_otherwise():
    c = {x["gov"]: x for x in N["candles_mandato"]}
    assert c["fhc"]["anos"] == [1995, 2002] and "1994" in c["fhc"]["nota"]
    assert c["lula12"]["o"] == pytest.approx(c["fhc"]["c"])
    assert c["bolsonaro"]["o"] == pytest.approx(N["serie"]["2018"])


def test_robustness_is_deterministic_and_reports_rank_stability():
    r = {x["gov"]: x for x in N["robustez"]}
    assert BUNDLE["sorteios"] == 10_000 and BUNDLE["semente"] == 20261020
    assert all(x["p5"] <= x["fechamento"] <= x["p95"] for x in r.values())
    assert 0 <= r["lula12"]["fracao_mantem_posicao"] <= 1
    novo = indice.construir()["versoes"]["N"]
    assert [x["fracao_mantem_posicao"] for x in novo["robustez"]] == [
        x["fracao_mantem_posicao"] for x in N["robustez"]
    ]


def test_items_follow_the_three_doors():
    assert all(i["direcao"] in ("maior", "menor") for i in BUNDLE["itens"])
    assert sorted(i["id"] for i in BUNDLE["itens"] if i["camada"] == "P") == [
        "abertura",
        "estatal",
        "governo",
        "industria",
    ]
    assert all(i["area"] == "Premissas econômicas" for i in BUNDLE["itens"] if i["camada"] == "P")
    assert set(NP["areas"]) - set(N["areas"]) == {"Premissas econômicas"}
    assert (
        ITENS["estatal"]["direcao"] == "maior"
    )  # V-Dem codebook: a higher v2clstown value = less state ownership
    assert "saeb" in ITENS and not any(k.startswith("saeb_") for k in ITENS)  # one concept, once
    assert "dívida líquida" not in " ".join(b for i in BUNDLE["itens"] for b in i["bases"]).lower()


def test_yearly_candles_sit_on_the_monthly_index_and_december_equals_the_annual_value():
    for a in ("2005", "2015", "2024"):
        assert N["mensal"][a + "-12"] == pytest.approx(N["serie"][a], abs=1e-3)  # amendment 06 §1
    c = {x["t"][:4]: x for x in N["candles_ano"]}
    assert c["2016"]["o"] == pytest.approx(N["mensal"]["2015-12"]) and c["2016"][
        "c"
    ] == pytest.approx(N["mensal"]["2016-12"])
    assert c["2016"]["l"] <= min(c["2016"]["o"], c["2016"]["c"]) and c["2016"]["h"] >= max(
        c["2016"]["o"], c["2016"]["c"]
    )
    assert all(x["n"] == 12 for x in N["candles_ano"] if x["t"] < "2025")
    assert "2000" not in c  # a year without index has no candle


def test_carry_forward_is_a_labelled_scenario_that_reaches_the_current_year():
    cf = N["cenario_carry_forward"]
    assert "cenário" in cf["nota"] and "não é o índice padrão" in cf["nota"]
    c = {x["t"][:4]: x for x in cf["candles_ano"]}
    assert c["2025"]["n"] == 12 and "2026" in c and "incompleto" in c["2026"]["nota"]
    assert "2000" in c and "2000" not in {x["t"][:4] for x in N["candles_ano"]}
    assert N["serie"]["2024"] == pytest.approx(
        N["mensal"]["2024-12"], abs=1e-3
    )  # the default is untouched


def test_term_reading_uses_the_candle_window_and_skips_off_scale_points():
    L = {r["gov"]: r for r in N["leitura_mandatos"]}
    assert [r["gov"] for r in N["leitura_mandatos"]] == [c["gov"] for c in N["candles_mandato"]]
    assert L["fhc"]["anos"] == [1995, 2002] and L["lula12"]["anos"] == [2002, 2010]
    assert L["dilma"]["anos"] == [2010, 2016] and L["temer"]["anos"] == [2015, 2018]
    c = {x["gov"]: x for x in N["candles_mandato"]}
    for g, r in L.items():
        assert r["abertura"] == round(c[g]["o"], 2) and r["fechamento"] == round(c[g]["c"], 2)
        assert r["subiram"] + r["cairam"] <= r["n_itens"]
        assert all(0 <= ITENS[m["id"]]["pontos"][str(m["de"])] <= 100 for m in r["mais_subiram"])
        assert all(
            m["pontos"] >= n["pontos"]
            for m, n in zip(r["mais_subiram"], r["mais_subiram"][1:], strict=False)
        )
    assert (
        "inflacao" not in [m["id"] for m in L["fhc"]["mais_subiram"]]
        or L["fhc"]["mais_subiram"][0]["de"] >= 1995
    )
    assert (
        L["lula12"]["mais_subiram"][0]["pontos"] > 50
        and L["dilma"]["mais_cairam"][0]["pontos"] < -40
    )
