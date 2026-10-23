"""Literature layer (amendments 07-09): the sealed inclusion rules, on bundle and harvest code."""

import importlib.util
import json
from pathlib import Path

from govfc import literatura

RAIZ = Path(__file__).resolve().parents[1]
L = json.loads((RAIZ / "output" / "literatura.json").read_text(encoding="utf-8"))

spec = importlib.util.spec_from_file_location(
    "coletar", RAIZ / "data" / "raw" / "literatura-fase3" / "coletar.py"
)
coletar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coletar)


def test_every_included_study_passed_the_five_sealed_steps():
    assert L["estudos"], "the latest round included nothing"
    for s in L["estudos"]:
        assert s["doi"] and s["quartil_sjr"] == "Q1" and s["sjr_edicao"] == "2024", s["chave"]
        assert s["desenho"] and s["mandatos"] and s["episodios"], s["chave"]
    assert all(x["motivo"] for x in L["excluidos"])
    assert sum(L["por_mandato"].values()) >= len(L["estudos"])


def test_every_completed_round_is_published_with_its_counts():
    assert [r["emenda"] for r in L["rodadas"]] == [n for n, _ in literatura.RODADAS]
    assert L["rodadas"][0]["trabalhos"] == 1329 and L["rodadas"][0]["incluidos"] == 7
    assert L["rodadas"][1]["trabalhos"] == 532 and L["rodadas"][1]["incluidos"] == 14
    assert L["rodadas"][2]["trabalhos"] == 5457 and L["rodadas"][2]["incluidos"] == 36
    assert L["rodadas"][3]["trabalhos"] == 6497 and L["rodadas"][3]["incluidos"] == 38
    assert L["rodadas"][-1]["incluidos"] == len(L["estudos"])
    assert [r["consultas"] for r in L["rodadas"]] == [40, 40, 40, 46]
    assert len(L["episodios"]) == 23 and all(e["lidos_en"] <= 200 for e in L["episodios"])
    assert [e["numero"] for e in L["episodios"][-3:]] == ["21", "22", "23"]  # amendment 10
    assert not L["pendente"], "all four sealed rounds are complete"


def test_design_words_are_matched_on_word_boundaries_and_siglas_as_written():
    import re

    d07 = re.compile(r"\b(" + "|".join(re.escape(d) for d in coletar.DESENHOS_07) + r")\b", re.I)
    d09 = re.compile(r"\b(" + "|".join(re.escape(d) for d in coletar.DESENHOS_08) + r")\b", re.I)
    sig = re.compile(r"\b(" + "|".join(re.escape(s) for s in coletar.SIGLAS_08) + r")\b")
    assert not d07.search("policy instruments and matching grants under a VAR framework")
    assert d07.search("We use a Regression Discontinuity design") and d07.search(
        "instrumental variables"
    )
    assert not d07.search("difference in differences") and d09.search("difference in differences")
    assert sig.search("a DiD estimator") and not sig.search("did it work") and not sig.search("iv")
    assert coletar.RE_BRASIL.search("Brazil's municipalities") and not coletar.RE_BRASIL.search(
        "Brazilwood"
    )
    assert (
        coletar.issn_norm("1542-4863") == "15424863"
        and coletar.issn_norm("0004-282x") == "0004282X"
    )


def test_result_sentences_come_from_the_abstract_only():
    txt = "We study X. The program reduced infant mortality by 10%. It is large. Effects persist."
    assert coletar.frases_resultado(txt) == [
        "The program reduced infant mortality by 10%.",
        "Effects persist.",
    ]


def test_committed_bundle_equals_fresh_build():
    novo = literatura.construir()
    assert [s["chave"] for s in novo["estudos"]] == [s["chave"] for s in L["estudos"]]
    assert novo["rodadas"] == L["rodadas"]
