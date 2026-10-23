"""Published numbers = test assertions. Every figure the article quotes is pinned here.

Two kinds of check: (1) the committed ``output/results.json`` equals a fresh build from the
sealed inputs; (2) key numbers are recomputed by independent code straight from the RAW files
(not through the derived CSVs the engine reads), so a bug in a derivation script cannot hide.
"""

import csv
import json
import math
from pathlib import Path

import pytest

from govfc import build_results

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
RES = json.loads((RAIZ / "output" / "results.json").read_text(encoding="utf-8"))
LINHA = {r["id"]: r for r in RES["linhas"]}


def test_committed_results_equal_a_fresh_build():
    novo = build_results.construir()
    assert [r["id"] for r in novo] == [r["id"] for r in RES["linhas"]]
    assert [r["veredito"] for r in novo] == [r["veredito"] for r in RES["linhas"]]
    assert [r["valor_reproduzido"] for r in novo] == [r["valor_reproduzido"] for r in RES["linhas"]]


def test_scoreboard_counts():
    assert RES["resumo"]["total"] == {
        "APROXIMADO": 19,
        "NAO_REPRODUZ": 29,
        "NAO_VERIFICADO": 7,
        "REPRODUZ": 2,
    }
    assert sum(RES["resumo"]["total"].values()) == 57  # 56 cells, the Lula 1-2 unemployment has two


def test_the_two_exact_reproductions_are_gini_2014_and_2018():
    exatos = sorted(r["id"] for r in RES["linhas"] if r["veredito"] == "REPRODUZ")
    assert exatos == ["dilma.gini", "temer.gini"]


def test_no_inflation_row_reproduces_exactly():
    assert all(r["veredito"] != "REPRODUZ" for r in RES["linhas"] if r["indicador"] == "inflacao")


@pytest.mark.parametrize(
    ("id_", "valor"),
    [
        ("itamar.inflacao", 1504.2245),
        ("fhc.inflacao", 9.2464),
        ("dilma.inflacao", 6.9369),
        ("temer.inflacao", 4.327),
        ("lula3.inflacao", 4.5723),
        ("dilma.pib", 0.4304),
        ("itamar.pib", 3.4112),
    ],
)
def test_pinned_values(id_, valor):
    assert LINHA[id_]["valor_reproduzido"] == pytest.approx(valor, abs=1e-4)


def _bcb(arquivo):
    """Monthly BCB SGS file -> {(year, month): percent}, read raw."""
    dados = json.loads((RAW / "inflacao" / arquivo).read_text())
    return {(int(r["data"][-4:]), int(r["data"][3:5])): float(r["valor"]) for r in dados}


def test_ipca_independent_recomputation_from_the_raw_json():
    ipca = _bcb("ipca-sgs433-raw.json")
    anual = {
        a: math.prod(1 + ipca[(a, m)] / 100 for m in range(1, 13)) - 1 for a in range(1992, 2026)
    }
    media = lambda a, b: 100 * sum(anual[x] for x in range(a, b + 1)) / (b - a + 1)  # noqa: E731
    assert media(1995, 2002) == pytest.approx(LINHA["fhc.inflacao"]["valor_reproduzido"], abs=1e-3)
    assert media(2011, 2016) == pytest.approx(
        LINHA["dilma.inflacao"]["valor_reproduzido"], abs=1e-3
    )
    assert 100 * anual[2015] == pytest.approx(10.67, abs=0.01)  # the 2015 IPCA everyone remembers


def test_gdp_independent_recomputation_from_the_raw_json():
    j = json.loads((RAW / "economia-real" / "ipeadata-SCN10_PIBG10-raw.json").read_text())
    taxa = {int(r["VALDATA"][:4]): r["VALVALOR"] for r in j["value"]}
    itamar = sum(taxa[a] for a in (1992, 1993, 1994)) / 3
    assert itamar == pytest.approx(LINHA["itamar.pib"]["valor_reproduzido"], abs=1e-3)


def test_mandate_months_agree_with_the_monetary_block():
    """The monetary agent used its own term dates; they must match the curated table."""
    from govfc.mandatos import carregar

    meses = {r["id"]: r["meses"] for r in carregar()}
    sen = {r["janela"]: r["meses"] for r in RES["monetario"]["senhoriagem"]}
    assert sen["FHC"] == round(meses["fhc"])
    assert sen["Lula 1-2"] == round(meses["lula12"])
    assert sen["Sarney"] == round(meses["sarney"])
    assert sen["Geisel"] == round(meses["geisel"])


def test_seigniorage_reproduces_cysne_and_coimbra_lisboa_table_1():
    """The monthly formula reproduces the authors' own table (DOI 10.1590/0101-35172004-1602)."""
    with open(RAW / "monetario" / "saida" / "reproducao_cysne.csv", newline="") as fh:
        linhas = list(csv.DictReader(fh))
    tit = next(
        r for r in linhas if r["serie_minha"] == "c_TIT_mensal_pib" and r["periodo"] == "1947-2003"
    )
    assert float(tit["erro_abs_medio_pp"]) == pytest.approx(0.181, abs=1e-3)
    assert float(tit["correlacao"]) >= 0.998
    anual = next(
        r for r in linhas if r["serie_minha"] == "b_anual_igpdi_pib" and r["periodo"] == "1980-1994"
    )
    assert float(anual["correlacao"]) < 0.1  # the annual shortcut fails in hyperinflation


def test_seigniorage_in_hyperinflation_vs_after_the_real_plan():
    sen = {r["janela"]: r for r in RES["monetario"]["senhoriagem"]}
    assert sen["Sarney"]["c_TIT_mensal_pib"] == pytest.approx(5.883, abs=1e-3)
    assert sen["FHC"]["c_TIT_mensal_pib"] == pytest.approx(0.522, abs=1e-3)
    assert sen["Lula 3"]["c_TIT_mensal_pib"] == pytest.approx(0.04, abs=0.01)


def test_arithmetic_and_geometric_means_agree_except_in_hyperinflation():
    """Claim in METHODOLOGY section 5: they differ by < 0.3 pp everywhere but Itamar 1992-94."""
    for r in RES["linhas"]:
        if r["indicador"] not in ("pib", "inflacao") or r["valor_reproduzido"] is None:
            continue
        geo = next(a for a in r["sensibilidade"] if "geometric mean" in a["rotulo"])["valor"]
        dif = abs(r["valor_reproduzido"] - geo)
        if r["id"] == "itamar.inflacao":
            assert round(r["valor_reproduzido"]) == 1504
            assert round(geo) == 1373
        else:
            assert dif < 0.3, (r["id"], dif)
