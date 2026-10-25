"""External debt layer: BCB numbers as hashed, concepts kept apart, net level as published."""

import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
T = json.loads((RAIZ / "output" / "terminal.json").read_text(encoding="utf-8"))
IND = {i["id"]: i for i in T["indicadores"]}
SERIES = RAIZ / "data" / "raw" / "externo-fase3" / "series"


def _csv(nome):
    with open(SERIES / nome, newline="", encoding="utf-8") as fh:
        return {
            (int(r["ano"]), int(r["mes_ou_trimestre"])): float(r["valor"])
            for r in csv.DictReader(fh)
        }


def _linha(ind, trecho):
    return next(dict(ln["pontos"]) for ln in IND[ind]["linhas"] if trecho in ln["rotulo"])


def test_bcb_published_values_as_hashed():
    restrita = _csv("divida_externa_bruta_restrita_usd_mi_sgs3684.csv")
    assert restrita[(2026, 6)] == 407102.75  # Tabela 15 da Nota de set/2026: 407.102,7
    assert restrita[(2025, 12)] == 386147.93  # DivExt_T.xls dez/2025: 386.148
    assert _csv("divida_externa_bruta_bpm6_usd_mi_sgs25563.csv")[(2026, 6)] == 869522
    assert _csv("divida_externa_setor_publico_restrita_usd_mi_sgs21521.csv")[(2026, 6)] == 143810.6
    assert _csv("divida_externa_liquida_pib_pct_sgs11409.csv")[(2025, 9)] == -0.9
    assert _csv("nfsp_juros_nominais_12m_pib_pct_sgs5760.csv")[(2026, 8)] == 8.86


def test_quarterly_sgs_dates_are_moved_to_the_quarter_end_month():
    for nome in SERIES.glob("*_sgs*.csv"):
        meses = {k[1] for k in _csv(nome.name)}
        if len(meses) == 4:
            assert meses == {3, 6, 9, 12}, nome.name


def test_the_two_bcb_concepts_stay_on_separate_labelled_lines():
    rotulos = [ln["rotulo"] for ln in IND["divext"]["linhas"]]
    assert any("SGS 3684" in r for r in rotulos) and any("SGS 25563" in r for r in rotulos)
    restrita, bpm6 = _linha("divext", "SGS 3684"), _linha("divext", "SGS 25563")
    assert restrita["2026-06-01"] == 407102.75 and bpm6["2026-06-01"] == 869522
    assert min(restrita) == "1972-12-01" and min(bpm6) == "2002-03-01"
    assert IND["divext_reservas"]["linhas"][1]["pontos"][-1][1] > 0  # reservas, BCB SGS 3546


def test_discontinued_ratios_end_where_the_bcb_stopped_them():
    for ind in ("divext_pib", "divext_liquida_pib", "divext_publico", "pii_pib"):
        ultimo = IND[ind]["linhas"][0]["pontos"][-1]
        assert ultimo[0] == "2025-09-01", ind  # nothing extended into 2026
        assert "descontinuada" in IND[ind]["nota"]
    assert _linha("divext_liquida_pib", "SGS 11409")["2025-09-01"] == -0.9
    assert "nada foi prolongado" in IND["divext_liquida_pib"]["nota"]


def test_net_external_debt_level_is_still_published_and_turned_positive_in_jun_2026():
    # Correction of 2026-10-24: the first version claimed no official 2026 value existed.
    liq = _csv("divida_externa_liquida_usd_mi_sgs3685.csv")
    assert liq[(2026, 6)] == 5083.49  # the headline number of 21/10/2026, official
    assert liq[(2026, 3)] == -1100.3 and liq[(2025, 12)] == -8701.59  # Dec/2025 revised
    assert max(k for k, v in liq.items() if v > 0 and k < (2026, 1)) == (2007, 9)
    assert all(v < 0 for k, v in liq.items() if (2007, 12) <= k <= (2026, 3))
    tab = {}
    with open(SERIES / "tabela31_nota_jan2026.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["indicador"] == "tab31_divida_externa_liquida_usd_mi":
                tab[(int(r["ano"]), int(r["mes_ou_trimestre"]))] = float(r["valor"])
    for k in ((2024, 6), (2024, 9), (2024, 12), (2025, 6), (2025, 9)):
        assert liq[k] == tab[k], k  # the SGS series is Table 31's column M
    pontos = dict(IND["divext_liquida"]["linhas"][0]["pontos"])
    assert pontos["2026-06-01"] == 5083.49 and min(pontos) == "1987-06-01"
    assert "continua publicado" in IND["divext_liquida"]["nota"]


def test_official_net_external_debt_table_is_negative_through_dec_2025():
    tab = {}
    with open(SERIES / "tabela31_nota_jan2026.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            chave = (int(r["ano"]), int(r["mes_ou_trimestre"]))
            tab.setdefault(r["indicador"], {})[chave] = float(r["valor"])
    liq = tab["tab31_divida_externa_liquida_usd_mi"]
    assert liq[(2025, 12)] == -17217.78 and all(v < 0 for v in liq.values())
    k = (2025, 12)
    partes = (
        tab["tab31_divida_externa_bruta_usd_mi"][k]
        - tab["tab31_reservas_usd_mi"][k]
        - tab["tab31_creditos_brasileiros_exterior_usd_mi"][k]
        - tab["tab31_haveres_bancos_comerciais_usd_mi"][k]
    )
    assert round(partes, 1) == round(liq[k], 1)  # the BCB definition, from its own table


def test_nominal_result_sign_is_inverted_like_the_primary_one():
    nominal = dict(IND["nominal"]["linhas"][0]["pontos"])
    assert nominal["2026-08-01"] == -9.48  # BCB publishes +9.48 (deficit)
    assert "sinal" in IND["nominal"]["nota"] and "positivo = superávit" in IND["nominal"]["un"]


def test_world_external_debt_uses_one_source_and_the_group_the_source_has():
    m = IND["mun_divext_rnb"]
    # IDS has no world or Latin America aggregate; upper-middle income is the group it carries
    assert [ln["rotulo"] for ln in m["linhas"]] == ["Brasil", "Renda média-alta"]
    brasil = dict(m["linhas"][0]["pontos"])
    assert round(brasil["2024-01-01"], 1) == 28.7
