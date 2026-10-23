#!/usr/bin/env python3
"""Render the documentation templates (``docs-src/<lang>/*.tmpl``) with numbers from the results.

Every number in the prose is a ``{{token}}`` filled from ``output/results.json`` and
``data/curated/mandatos.csv``, so the five languages cannot disagree and a stale number cannot
survive a rebuild. ``tests/test_docs.py`` re-renders and compares with the committed files.
"""

import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "code"))

from govfc.i18n import DECIMAL, LINGUAS  # noqa: E402
from govfc.mandatos import cobertura  # noqa: E402

DESTINO = {
    "README.md.tmpl": lambda lang: "README.md" if lang == "en" else f"README.{lang}.md",
    "METHODOLOGY.md.tmpl": lambda lang: f"docs/{lang}/METHODOLOGY.md",
}


def tokens(lang="en"):
    """Return the token -> text mapping used by every template.

    Parameters
    ----------
    lang : str
        Language code: it selects the decimal mark and the thousands separator.

    Returns
    -------
    dict
        Counts per verdict, the number of printed numbers, and the coverage of the terms.
    """
    res = json.loads((RAIZ / "output" / "results.json").read_text(encoding="utf-8"))
    tot = res["resumo"]["total"]
    cob = cobertura()
    cur = RAIZ / "data" / "curated"
    conta = {
        n: sum(1 for _ in open(cur / f"{n}.csv", encoding="utf-8")) - 1
        for n in ("observations", "indicators", "quebras")
    }
    milhar = "," if DECIMAL[lang] == "." else "."

    def inteiro(n):
        """Integer with the language's thousands separator."""
        return f"{n:,}".replace(",", milhar)

    def dec1(x):
        """One-decimal number with the language's marks."""
        return f"{x:,.1f}".replace(",", "\x00").replace(".", DECIMAL[lang]).replace("\x00", milhar)

    saida = {
        "n_obs": inteiro(conta["observations"]),
        "n_ind": str(conta["indicators"]),
        "n_quebras": str(conta["quebras"]),
        "n_total": str(sum(tot.values())),
        "n_reproduz": str(tot.get("REPRODUZ", 0)),
        "n_aproxima": str(tot.get("APROXIMADO", 0)),
        "n_nao": str(tot.get("NAO_REPRODUZ", 0)),
        "n_nv": str(tot.get("NAO_VERIFICADO", 0)),
        "omitido_pct": f"{cob['pct_omitido']:.1f}".replace(".", DECIMAL[lang]),
        "omitido_meses": f"{cob['omitidos']:.1f}".replace(".", DECIMAL[lang]),
        "total_meses": f"{cob['total']:.1f}".replace(".", DECIMAL[lang]),
    }
    saida.update(_tokens_fases_2_e_3(inteiro, dec1))
    return saida


def _tokens_fases_2_e_3(inteiro, dec1):
    """Numbers of the composite index, the literature layer, the terminal and the external debt.

    Parameters
    ----------
    inteiro, dec1 : callable
        Formatters for an integer and for a one-decimal number in the target language.

    Returns
    -------
    dict
        Token -> text, all read from the sealed outputs and collections, never typed by hand.
    """
    out_dir = RAIZ / "output"
    indice = json.loads((out_dir / "indice.json").read_text(encoding="utf-8"))
    lit = json.loads((out_dir / "literatura.json").read_text(encoding="utf-8"))
    term = json.loads((out_dir / "terminal.json").read_text(encoding="utf-8"))
    raw = RAIZ / "data" / "raw"
    areas = {i["area"] for i in indice["itens"]}
    refs2 = sum(
        1
        for r in csv.DictReader(
            open(raw / "referencias-fase2" / "referencias.csv", encoding="utf-8")
        )
        if r["status"] == "confirmada"
    )
    bib = (RAIZ / "docs" / "references-q1.bib").read_text(encoding="utf-8")
    ext = raw / "externo-fase3" / "series"

    def ultimo(nome, indicador=None):
        """Last (value, "YYYY-MM") of one series file, optionally of one indicator in it."""
        linhas = [
            r
            for r in csv.DictReader(open(ext / nome, encoding="utf-8"))
            if indicador is None or r["indicador"] == indicador
        ]
        r = max(linhas, key=lambda r: (int(r["ano"]), int(r["mes_ou_trimestre"])))
        return float(r["valor"]), f"{r['ano']}-{int(r['mes_ou_trimestre']):02d}"

    restrita, data_restrita = ultimo("divida_externa_bruta_restrita_usd_mi_sgs3684.csv")
    bpm6, _ = ultimo("divida_externa_bruta_bpm6_usd_mi_sgs25563.csv")
    liq_pib, data_liq = ultimo("divida_externa_liquida_pib_pct_sgs11409.csv")
    tab31 = "tabela31_nota_jan2026.csv"
    liq, data_tab31 = ultimo(tab31, "tab31_divida_externa_liquida_usd_mi")
    ativos = (
        ultimo(tab31, "tab31_creditos_brasileiros_exterior_usd_mi")[0]
        + ultimo(tab31, "tab31_haveres_bancos_comerciais_usd_mi")[0]
    )
    fech = {r["gov"]: r["fechamento"] for r in indice["versoes"]["N"]["robustez"]}
    out = {
        "n_itens": inteiro(len(indice["itens"])),
        "n_areas": inteiro(len(areas)),
        "n_areas_n": inteiro(len(areas - {"Premissas econômicas"})),
        "n_sorteios": inteiro(indice["sorteios"]),
        "n_emendas": inteiro(len(list((raw / "preregistro").glob("PREREGISTRATION-EMENDA-??.md")))),
        "n_refs_fase2": inteiro(refs2),
        "n_refs_q1": inteiro(bib.count("\n@") + bib.startswith("@")),
        "n_lit_rodadas": inteiro(len(lit["rodadas"])),
        "n_episodios": inteiro(len(lit["episodios"])),
        "n_estudos": inteiro(len(lit["estudos"])),
        "n_term_ind": inteiro(len(term["indicadores"])),
        "n_tests": inteiro(
            sum(
                t.read_text(encoding="utf-8").count("\ndef test_")
                for t in (RAIZ / "tests").glob("test_*.py")
            )
        ),
        "n_dominios": inteiro(len(term["dominios"])),
        "div_restrita_bi": dec1(restrita / 1000),
        "div_bpm6_bi": dec1(bpm6 / 1000),
        "div_data": data_restrita,
        "div_liq_bi": dec1(liq / 1000),
        "div_liq_data": data_tab31,
        "div_liq_pib": dec1(liq_pib),
        "div_liq_pib_data": data_liq,
        "div_ativos_bi": dec1(ativos / 1000),
    }
    for r in lit["rodadas"]:
        out[f"lit{r['emenda']}_trab"] = inteiro(r["trabalhos"])
        out[f"lit{r['emenda']}_inc"] = inteiro(r["incluidos"])
    for gov, v in fech.items():
        out[f"idx_{gov}"] = dec1(v)
    return out


def renderizar(texto, mapa):
    """Replace every ``{{token}}``; an unknown token is an error, never silently kept."""

    def troca(m):
        """Return the token's text or raise on an unknown token."""
        if m.group(1) not in mapa:
            raise KeyError(f"unknown token {{{{{m.group(1)}}}}}")
        return mapa[m.group(1)]

    return re.sub(r"\{\{(\w+)\}\}", troca, texto)


def main():
    """Render every template found under ``docs-src``; return 0."""
    for lang in LINGUAS:
        mapa = tokens(lang)
        pasta = RAIZ / "docs-src" / lang
        for nome, destino in DESTINO.items():
            fonte = pasta / nome
            if fonte.exists():
                alvo = RAIZ / destino(lang)
                alvo.parent.mkdir(parents=True, exist_ok=True)
                alvo.write_text(
                    renderizar(fonte.read_text(encoding="utf-8"), mapa), encoding="utf-8"
                )
                print(alvo.relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
