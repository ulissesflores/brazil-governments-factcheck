#!/usr/bin/env python3
"""Seal the repository with one SHA-256 ``chain_hash`` (build and ``--verify``).

Sealed files, in lexicographic order: ``run_all.py``, ``code/**/*.py``, ``tests/*.py``,
``scripts/*.py``, ``data/**`` (raw files, manifests, transcription, references),
``docs/**/*.md``, ``REPRODUCIBILITY.md``, this script, and the eight ``output/*.json``
(results, series, dinamica, mundo, terminal, indice, auditoria, literatura).
Chain: ``h_i = sha256(h_{i-1} + path + sha256(file))`` with ``h_0 = sha256(b"")``.
Outside the seal (informational): Python version, platform, rendered figures.
``--verify`` also recomputes every internal acquisition chain (``manifest.jsonl``).
"""

import hashlib
import json
import platform
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SAIDA = RAIZ / "output"
sys.path.insert(0, str(RAIZ / "code"))

from govfc.chain import verificar  # noqa: E402


def arquivos():
    """List the sealed files.

    Returns
    -------
    list of pathlib.Path
        Paths relative to the repository root, sorted by ``as_posix()``.
    """
    achados = {Path("run_all.py"), Path("REPRODUCIBILITY.md"), Path("make_provenance.py")}
    for padrao in ("code/**/*.py", "tests/*.py", "scripts/*.py", "docs/**/*.md", "docs/**/*.bib"):
        achados |= {p.relative_to(RAIZ) for p in RAIZ.glob(padrao) if p.is_file()}
    achados |= {
        p.relative_to(RAIZ)
        for p in (RAIZ / "data").rglob("*")
        if p.is_file() and "__pycache__" not in p.parts  # byte-code caches vary by interpreter
    }
    for nome in (
        "results.json",
        "series.json",
        "dinamica.json",
        "mundo.json",
        "terminal.json",
        "indice.json",
        "auditoria.json",
        "literatura.json",
    ):
        if (SAIDA / nome).exists():
            achados.add(Path("output") / nome)
    return sorted(achados, key=lambda p: p.as_posix())


def calcular():
    """Compute the sha256 of each sealed file and the chained hash.

    Returns
    -------
    itens : list of dict
        One ``{"path": str, "sha256": str}`` per file, in :func:`arquivos` order.
    cadeia : str
        Final ``chain_hash``.
    """
    cadeia = hashlib.sha256(b"").hexdigest()
    itens = []
    for rel in arquivos():
        h = hashlib.sha256((RAIZ / rel).read_bytes()).hexdigest()
        itens.append({"path": rel.as_posix(), "sha256": h})
        cadeia = hashlib.sha256((cadeia + rel.as_posix() + h).encode()).hexdigest()
    return itens, cadeia


def gravar():
    """Write ``output/provenance.json`` and ``output/hash-chain.md`` and print the seal."""
    itens, cadeia = calcular()
    SAIDA.mkdir(exist_ok=True)
    (SAIDA / "provenance.json").write_text(
        json.dumps(
            {"algorithm": "sha256-chain", "chain_hash": cadeia, "files": itens},
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )
    linhas = ["# Hash chain", "", f"chain_hash: `{cadeia}`", "", "| file | sha256 |", "|---|---|"]
    linhas += [f"| `{i['path']}` | `{i['sha256']}` |" for i in itens]
    linhas += [
        "",
        "## Informational (NOT hashed)",
        "",
        f"- Python {platform.python_version()} on {platform.system()}",
        "",
    ]
    (SAIDA / "hash-chain.md").write_text("\n".join(linhas))
    print(f"chain_hash {cadeia}")


def verificar_selo():
    """Recompute the seal and the acquisition chains; compare with ``output/provenance.json``.

    Returns
    -------
    int
        ``0`` if every file, the ``chain_hash`` and every ``manifest.jsonl`` chain match;
        ``1`` otherwise (each diverging file is printed).
    """
    alvo = SAIDA / "provenance.json"
    if not alvo.exists():
        print("provenance.json missing: run python make_provenance.py")
        return 1
    gravado = json.loads(alvo.read_text())
    itens, cadeia = calcular()
    codigo = 0
    if gravado["files"] != itens or gravado["chain_hash"] != cadeia:
        antigo = {i["path"]: i["sha256"] for i in gravado["files"]}
        for i in itens:
            if antigo.get(i["path"]) != i["sha256"]:
                print(f"DIVERGES: {i['path']}")
        print("PROVENANCE FAILED")
        codigo = 1
    for man in sorted((RAIZ / "data").rglob("manifest.jsonl")):
        print(f"acquisition chain {man.parent.relative_to(RAIZ).as_posix()}: ", end="")
        codigo |= verificar(man.parent, permitir_ausentes=True)
    if codigo == 0:
        print(f"provenance verified: chain_hash {cadeia}")
    return codigo


if __name__ == "__main__":
    sys.exit(verificar_selo()) if "--verify" in sys.argv else gravar()
