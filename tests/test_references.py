"""Bibliography: every DOI checked against Crossref; anchors are Q1 journals checked on Scimago."""

import csv
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
Q1 = RAIZ / "data" / "raw" / "referencias-q1"
LINHAS = list(csv.DictReader(open(Q1 / "referencias-q1.csv", encoding="utf-8")))
ANCORAS = [r for r in LINHAS if r["papel"] == "ancora"]


def test_every_reference_was_checked_against_crossref():
    assert len(LINHAS) >= 130
    assert all(r["crossref_conferido"] == "sim" for r in LINHAS)
    for r in LINHAS:
        assert (Q1 / r["arquivo_crossref"]).exists(), r["chave_bibtex"]


def test_anchors_are_q1_with_a_scimago_record_on_disk():
    assert len(ANCORAS) >= 100
    for r in ANCORAS:
        assert r["scimago_quartil"] == "Q1", r["chave_bibtex"]
        assert (Q1 / r["arquivo_scimago"]).exists(), r["chave_bibtex"]


def test_every_methodological_theme_has_at_least_one_anchor():
    temas = {r["tema"] for r in LINHAS}
    assert len(temas) == 12
    for t in temas:
        assert any(r["tema"] == t for r in ANCORAS), t


def test_q2_journals_are_complementary_not_anchors():
    """Revista de Economia Política (Cysne 2004, Barrionuevo 2015) and J. Cryptology are Q2."""
    for chave in ("cysne2004", "barrionuevo2015", "haber1991"):
        r = next((x for x in LINHAS if x["chave_bibtex"].lower().startswith(chave[:8])), None)
        if r is not None:
            assert r["papel"] == "complementar", chave


def test_bib_and_csv_agree():
    bib = (RAIZ / "docs" / "references-q1.bib").read_text(encoding="utf-8")
    chaves = re.findall(r"^@\w+\{([^,]+),", bib, flags=re.M)
    assert len(chaves) == len(LINHAS)
    assert set(chaves) == {r["chave_bibtex"] for r in LINHAS}


def test_old_short_bibliography_dois_resolve_to_crossref_records():
    bib = (RAIZ / "docs" / "references.bib").read_text(encoding="utf-8")
    for doi in re.findall(r"doi = \{([^}]+)\}", bib):
        nome = "crossref-doi-" + re.sub(r"[/()]", "_", doi) + ".json"
        rec = json.loads((RAIZ / "data" / "raw" / "referencias" / nome).read_text(encoding="utf-8"))
        assert rec["message"]["DOI"].lower() == doi.lower()
