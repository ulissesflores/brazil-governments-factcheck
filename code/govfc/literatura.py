"""Literature layer (amendments 07, 08 and 09): what peer-reviewed Q1 studies measured about each term's episodes.

The collection ``data/raw/literatura-fase3`` holds, hashed, every OpenAlex and Crossref response of
four sealed rounds (07: full-text search sorted by citations, cap 40; 08: title-and-abstract
search by relevance, cap 100; 09: short queries, cap 200; 10: the raw of 09 plus episodes 21-23
on external debt, reserves and public debt, amendment 10). ``coletar.py`` in the collection applies
the inclusion steps by code (DOI; Q1 in the SJR 2024 edition; Brazil in title or abstract; an
identification design named in the abstract; Crossref type journal-article) and lists EVERY
returned work with its status and motive. This module only reshapes the latest round's tables
(and the earlier rounds' counts) into ``output/literatura.json``: no score, no sum, no verdict.
"""

import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
COLECAO = RAIZ / "data" / "raw" / "literatura-fase3"
#: Completed rounds, oldest first; the last one is the round the page shows. Round 09 ran on
#: 2026-10-22/23 in two sittings (the OpenAlex daily budget stopped it at query 20 of 40). Round 10
#: (amendment 10) reuses the hashed raw of round 09 and adds episodes 21-23 (external debt, reserves,
#: public debt): 46 queries, 6 of them new.
#: Round 11 (amendment 12, 2026-10-25) reuses the raw of rounds 09/10 and adds episodes 24-27 (central
#: bank independence, fiscal rules as a class, press freedom, judicial independence): 54 queries, 8 new.
RODADAS = [
    ("07", "series/emenda07"),
    ("08", "series/emenda08"),
    ("09", "series"),
    ("10", "series/emenda10"),
    ("11", "series/emenda11"),
]
PREREGISTRO = [
    f"data/raw/preregistro/PREREGISTRATION-EMENDA-{n}.md" for n in ("07", "08", "09", "10", "12")
]


def _lido(caminho):
    """Read a CSV into a list of dicts."""
    with open(caminho, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _rodada(emenda, pasta):
    """Counts of one round: queries, distinct works, included, motives."""
    linhas = _lido(COLECAO / pasta / "literatura_todos.csv")
    motivos = {}
    for r in linhas:
        k = r["motivo"] or "incluido"
        motivos[k] = motivos.get(k, 0) + 1
    return {
        "emenda": emenda,
        "consultas": 2 * len(_lido(COLECAO / pasta / "episodios.csv")),
        "trabalhos": len(linhas),
        "incluidos": sum(1 for r in linhas if r["status"] == "incluido"),
        "motivos": dict(sorted(motivos.items(), key=lambda kv: -kv[1])),
    }


def construir():
    """Build the bundle from the latest round (09) plus the counts of the earlier rounds."""
    ultima = RODADAS[-1][1]
    linhas = _lido(COLECAO / ultima / "literatura_todos.csv")
    episodios = _lido(COLECAO / ultima / "episodios.csv")
    estudos, excluidos = [], []
    for r in linhas:
        base = {
            "chave": r["chave"],
            "titulo": r["titulo"],
            "periodico": r["periodico"],
            "ano": int(r["ano"]) if r["ano"] else None,
            "episodios": r["episodios"].split("; "),
        }
        if r["status"] == "incluido":
            estudos.append(
                {
                    **base,
                    "doi": r["doi"],
                    "autores": r["autores"],
                    "quartil_sjr": r["quartil_sjr"],
                    "sjr_edicao": r["sjr_edicao"],
                    "citacoes_openalex": int(r["citacoes_openalex"] or 0),
                    "mandatos": r["mandatos"].split("; "),
                    "desenho": r["desenho"],
                    "frases_resultado": [f for f in r["frases_resultado"].split(" | ") if f],
                }
            )
        else:
            excluidos.append({**base, "motivo": r["motivo"], "quartil_sjr": r["quartil_sjr"]})
    por_mandato = {}
    for e in estudos:
        for g in e["mandatos"]:
            por_mandato[g] = por_mandato.get(g, 0) + 1
    eps = []
    for e in episodios:
        n = e["numero"]
        exc = {}
        for x in excluidos:
            if n in x["episodios"]:
                exc[x["motivo"]] = exc.get(x["motivo"], 0) + 1
        eps.append(
            {
                "numero": n,
                "nome": e["episodio"],
                "mandatos": e["mandatos"].split("; "),
                "consulta_en": e["consulta_en"],
                "consulta_pt": e["consulta_pt"],
                "total_en": int(e["total_openalex_en"]),
                "lidos_en": int(e["lidos_en"]),
                "total_pt": int(e["total_openalex_pt"]),
                "lidos_pt": int(e["lidos_pt"]),
                "incluidos": [s["chave"] for s in estudos if n in s["episodios"]],
                "excluidos_por_motivo": dict(sorted(exc.items(), key=lambda kv: -kv[1])),
            }
        )
    return {
        "schema": 1,
        "definicoes": __doc__,
        "preregistro": PREREGISTRO,
        "regra": "Incluído = DOI no Crossref com tipo journal-article; periódico Q1 na edição 2024 do SJR; Brasil no título ou no resumo; desenho de identificação nomeado no resumo (lista fechada, por palavra). Sem nota, soma ou veredito; o número por mandato reflete os anos decorridos e os episódios declarados, nunca a qualidade do governo nem o sentido dos resultados.",
        "rodadas": [_rodada(n, p) for n, p in RODADAS],
        "pendente": "",
        "episodios": eps,
        "estudos": estudos,
        "excluidos": excluidos,
        "por_mandato": por_mandato,
    }


def gravar():
    """Write ``output/literatura.json``; return the number of included studies."""
    d = construir()
    (RAIZ / "output" / "literatura.json").write_text(
        json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    return len(d["estudos"])


if __name__ == "__main__":
    print(f"studies: {gravar()}")
