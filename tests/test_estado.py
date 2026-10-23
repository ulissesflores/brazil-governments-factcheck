"""Amendment-03 layers on the page: tax burden by base, state profits, paid amendments, acts."""

import csv
import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
T = json.loads((RAIZ / "output" / "terminal.json").read_text(encoding="utf-8"))
IND = {i["id"]: i for i in T["indicadores"]}


def _linha(ind, trecho):
    return next(dict(ln["pontos"]) for ln in IND[ind]["linhas"] if trecho in ln["rotulo"])


def test_tax_burden_by_base_comes_from_one_edition_and_adds_up_to_the_total():
    bases = IND["carga_base"]["linhas"]
    assert [ln["rotulo"] for ln in bases] == [
        "Renda",
        "Folha de salários",
        "Propriedade",
        "Bens e serviços",
        "Transações financeiras",
        "Outros tributos",
    ]
    soma = sum(dict(ln["pontos"])["2024-01-01"] for ln in bases)
    total = _linha("carga_base", "Renda")  # same edition, same table: the aggregate row
    assert total["2024-01-01"] == pytest.approx(9.0995, abs=1e-4)
    rows = csv.DictReader(
        open(
            RAIZ / "data/raw/tributos-estado/series/receita-ctb-por-base-por-edicao.csv",
            encoding="utf-8",
        )
    )
    tot = next(
        float(r["valor"])
        for r in rows
        if r["indicador"] == "receita_ctb_base_0__edicao_2024" and r["ano"] == "2024"
    )
    assert soma == pytest.approx(tot, abs=0.05)


def test_state_owned_profits_keep_one_line_per_accounting_basis_in_reais():
    for chave in ("petrobras", "bb", "caixa", "eletrobras", "correios"):
        i = IND[f"lucro_{chave}"]
        assert i["un"].startswith("R$ milhões") and len(i["linhas"]) >= 2
        assert all("US$" not in ln["rotulo"] for ln in i["linhas"])
    assert _linha("lucro_petrobras", "consolidado, BR GAAP")["2009-01-01"] == 28981.708
    recentes = [
        v for ln in IND["lucro_correios"]["linhas"] for t, v in ln["pontos"] if t >= "2023-01-01"
    ]
    assert recentes and max(recentes) < 0  # losses in 2023-2025, as published


def test_paid_amendments_by_type_and_as_a_share_of_gdp():
    total = _linha("emendas_pagas", "Todos os tipos")
    assert round(total["2019-01-01"], 1) == 6.0 and round(total["2024-01-01"], 1) == 31.4
    pago, com_rap = (dict(ln["pontos"]) for ln in IND["emendas_pib"]["linhas"])
    assert 0 < pago["2024-01-01"] < com_rap["2024-01-01"] < 1
    assert "CGU" in IND["emendas_pib"]["un"] and "RTN" in IND["emendas_pib"]["un"]


def test_tax_and_bureaucracy_acts_are_listed_with_their_source():
    atos = T["atos"]
    assert len(atos) == 44 and all(a["url"].startswith("https://") for a in atos)
    assert sum(a["url"].startswith("https://www.planalto.gov.br/") for a in atos) >= 40
    assert atos == sorted(atos, key=lambda a: a["data"])
    assert any(a["instrumento"].startswith("Lei 11.598/2007") for a in atos)  # REDESIM


def test_the_2020_retention_rule_is_in_the_break_catalogue():
    rows = list(csv.DictReader(open(RAIZ / "data/curated/quebras.csv", encoding="utf-8")))
    q = [r for r in rows if "14.040" in r["metodo_novo"]]
    assert len(q) == 1 and q[0]["tipo_de_quebra"] == "mudanca_de_regra"
    assert "0,6% (2020)" in q[0]["efeito_medido"]
