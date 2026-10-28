"""Figures: every label fits (measured in the real font), the gate can fail, bidi rule holds."""

import re

import pytest

from govfc import figuras, medidor
from govfc.i18n import LINGUAS
from govfc.svg import Cena, proteger_rtl, tem_hebraico

pytest.importorskip("PIL")
RES = figuras.carregar_resultados()


@pytest.mark.parametrize("lang", LINGUAS)
def test_placar_labels_fit(lang):
    assert medidor.estouros(figuras.placar(RES, lang)) == []


def test_fit_check_can_fail():
    """Negative test: a gate that never rejects only stamps. Lengthen a label on purpose."""
    c = Cena(400, 100, "#000", "t", "d")
    c.texto(10, 40, "um rótulo comprido o bastante para estourar o orçamento", 20, "#fff", maxw=120)
    assert len(medidor.estouros(c)) == 1


@pytest.mark.parametrize("lang", LINGUAS)
def test_every_number_cell_comes_from_results(lang):
    """Each pure-number label on the placar is a printed value or a reproduced value."""
    svg = figuras.placar(RES, lang).svg()
    permitidos = set()
    for r in RES["linhas"]:
        pct = r["unidade"] == "pct"
        permitidos.add(figuras._impresso_fmt(r["impresso"], lang, pct))
        if r["valor_reproduzido"] is not None:
            casas = figuras._casas_impresso(r["impresso"])
            permitidos.add(figuras.fmt(r["valor_reproduzido"], casas, lang, pct))
    soltos = []
    for t in re.findall(r"<text[^>]*>([^<]*)</text>", svg):
        if re.fullmatch(r"[~+\-]?\d[\d.,]*%?", t) and t not in permitidos:
            soltos.append(t)
    assert soltos == []


def test_hebrew_first_strong_rule():
    assert proteger_rtl("ABC אבג").startswith("‏")
    assert not proteger_rtl("אבג ABC").startswith("‏")
    assert "⁦" in proteger_rtl("לולה 1–2")  # digit-dash-digit isolated LTR


def test_all_hebrew_strings_start_with_a_hebrew_letter_or_rlm():
    svg = figuras.placar(RES, "he").svg()
    for t in re.findall(r"<text[^>]*>([^<]*)</text>", svg):
        if tem_hebraico(t):
            primeiro = next((c for c in t if c.isalpha()), "")
            assert "֐" <= primeiro <= "׿" or t.startswith("‏"), t


IND = figuras.carregar_indice()


@pytest.mark.parametrize("lang", LINGUAS)
def test_areas_labels_fit(lang):
    assert medidor.estouros(figuras.areas(IND, lang)) == []


def test_areas_cells_come_from_the_index_and_only_the_extremes_separate():
    vn = IND["versoes"]["N"]
    cel = figuras._abre_fecha(vn)
    cand = {c["gov"]: c for c in vn["candles_mandato"]}
    for gov in figuras.ORDEM_MANDATOS:
        assert cel[(gov, figuras.ROTULO_INDICE)] == (cand[gov]["o"], cand[gov]["c"])
    assert cel[("fhc", "Instituições")][0] == vn["scores_areas"]["1995"]["Instituições"]
    assert cel[("temer", "Instituições")][0] == vn["scores_areas"]["2015"]["Instituições"]
    rob = {r["gov"]: r for r in vn["robustez"]}
    assert rob["lula3"]["posicao"] == 1 and rob["fhc"]["posicao"] == 6
    assert all(rob[g]["fracao_mantem_posicao"] < 0.8 for g in ("dilma", "temer", "bolsonaro"))
    svg = figuras.areas(IND, "pt-BR").svg()
    assert "Instituições" in svg and "—" in svg  # Educação and Moradia have no closing score


def test_areas_hebrew_strings_start_with_a_hebrew_letter_or_rlm():
    svg = figuras.areas(IND, "he").svg()
    for s in re.findall(r">([^<]+)</text>", svg):
        if tem_hebraico(s):
            assert s[0] == "‏" or "א" <= s[0] <= "ת", s
