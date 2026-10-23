"""Curated layer: unique keys, vintage on every row, nature flags, and the vintage story pinned."""

import csv
import json
from pathlib import Path

import pytest

from govfc import curate

RAIZ = Path(__file__).resolve().parents[1]
OBS = list(csv.DictReader(open(RAIZ / "data" / "curated" / "observations.csv", encoding="utf-8")))


def valor(indicador, trecho_serie, periodo, vintage=""):
    achados = [
        float(r["valor"])
        for r in OBS
        if r["indicador"] == indicador
        and trecho_serie in r["serie"]
        and r["periodo"] == str(periodo)
        and vintage in r["vintage"]
    ]
    assert len(achados) == 1, (indicador, trecho_serie, periodo, achados)
    return achados[0]


OBS_UF = list(
    csv.DictReader(
        open(RAIZ / "data" / "curated" / "observations_educacao_uf.csv", encoding="utf-8")
    )
)


def test_committed_curated_files_equal_a_fresh_build():
    todas = curate.observacoes()
    fresco = [r for r in todas if not curate.eh_uf(r)]
    assert len(todas) == len(OBS) + len(OBS_UF)
    assert len(fresco) == len(OBS)
    for novo, antigo in zip(fresco, OBS, strict=True):
        assert (novo["indicador"], novo["serie"], novo["vintage"], novo["periodo"]) == (
            antigo["indicador"],
            antigo["serie"],
            antigo["vintage"],
            antigo["periodo"],
        )
        assert float(novo["valor"]) == pytest.approx(float(antigo["valor"]), rel=1e-12, abs=1e-12)


def test_every_row_has_a_vintage_a_value_and_a_known_nature():
    for r in OBS:
        assert r["vintage"] != ""
        assert r["valor"] != ""
        assert r["natureza"] in {"publicado", "derivado_deterministico", "modelo_de_terceiro"}
        assert r["dependente_de_regra"] in {"sim", "nao"}


def test_key_is_unique():
    chaves = [(r["indicador"], r["serie"], r["vintage"], r["periodo"]) for r in OBS]
    assert len(chaves) == len(set(chaves))


def test_every_catalogue_indicator_has_data():
    contagem = {}
    for r in OBS:
        contagem[r["indicador"]] = contagem.get(r["indicador"], 0) + 1
    assert set(curate.catalogo()) == set(contagem)


def test_the_same_line_gives_different_poverty_by_source_and_by_vintage():
    """US$ 6.85/day in 2018: World Bank 26.78, IBGE SIS 33.34 (ed. 2024) or 33.44 (ed. 2025)."""
    assert valor("pobreza", "PIP | US$ 6.85/dia PPC2017", 2018) == 26.78
    assert valor("pobreza", "IBGE-SIS2024 | US$ 6,85 PPC2017", 2018) == 33.34
    assert valor("pobreza", "IBGE-SIS2025 | US$ 6,85 PPC2017", 2018) == 33.44
    assert valor("pobreza", "PIP | US$ 6.85/dia PPC2017", 2020) == 18.8
    assert valor("pobreza", "IBGE-SIS2025 | US$ 6,85 PPC2017", 2020) == 31.06  # gap not explained


def test_life_expectancy_2021_depends_on_the_vintage():
    assert valor("expvida", "Tabua Completa de Mortalidade 2021", 2021) == 77.03
    assert valor("expvida", "Agencia IBGE", 2021) == 72.8
    assert valor("expvida", "WB-WDI-SP.DYN.LE00.IN", 2021) == 73.04


def test_ipca_2015_from_the_monthly_raw_series():
    meses = [valor("inflacao_mensal", "IPCA (BCB SGS 433)", f"2015-{m:02d}") for m in range(1, 13)]
    produto = 1.0
    for m in meses:
        produto *= 1 + m / 100
    assert round((produto - 1) * 100, 2) == 10.67


def test_two_public_debt_methods_stay_two_series():
    series = {r["serie"] for r in OBS if r["indicador"] == "divida_pib"}
    assert any("metodologia até 2007" in s for s in series)
    assert any("metodologia desde 2008" in s for s in series)


def test_bundle_has_no_verdict_score_or_ranking():
    texto = (RAIZ / "output" / "series.json").read_text(encoding="utf-8")
    dados = json.loads(texto)
    assert set(dados) == {
        "schema",
        "mandatos",
        "indicadores",
        "quebras",
        "mecanismos",
        "simetria",
    }

    # no verdict, score or ranking FIELD in the raw layer (a source's free text may say "ranking")
    def chaves(o, acc):
        if isinstance(o, dict):
            acc.update(o.keys())
            for v in o.values():
                chaves(v, acc)
        elif isinstance(o, list):
            for v in o:
                chaves(v, acc)
        return acc

    assert not {"veredito", "ranking", "nota_geral", "score", "pontos_merito"} & chaves(
        dados, set()
    )
    assert len(dados["mandatos"]) == 15
    assert all(
        q["tipo_de_quebra"]
        in {"metodo_estatistico", "mudanca_de_regra", "revisao_de_vintage", "mudanca_de_unidade"}
        for q in dados["quebras"]
    )


def test_breaks_have_stable_ids_and_a_declared_reason_or_an_explicit_unknown():
    qs = curate.quebras()
    assert [q["id"] for q in qs] == [f"q{i:03d}" for i in range(1, len(qs) + 1)]
    assert len(qs) >= 73
    for q in qs:
        assert q["razao_declarada_pela_fonte"].strip() != "", q["id"]
