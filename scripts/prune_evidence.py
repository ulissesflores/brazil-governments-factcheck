#!/usr/bin/env python3
"""Keep third-party and heavy evidence as hash plus URL only (Seal 2), after listing what goes.

Policy (see ``REPRODUCIBILITY.md``): files under ``data/raw`` are redistributed only when they are
small, structured numeric data (JSON, CSV, JSONL) or our own derivation scripts and reports.
Everything else (PDF, ZIP, spreadsheets, HTML pages, extracted text, images) and any raw file
larger than 3 MB stays recorded in its ``manifest.jsonl`` (URL, bytes, sha256) but is not stored
here. Derived series and reports (``series/``, ``derivado/``, ``saida/``) stay whatever their size:
Seal 1 reads them.
Run without ``--apply`` for a dry run.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
LIMITE = 3 * 1024 * 1024
GUARDA = {".json", ".csv", ".jsonl", ".py", ".sh"}
#: our own reports and notes stay even though they are Markdown or text
PROPRIOS = {
    "RESULTADO.md",
    "MANIFEST-PROTOCOLO.md",
    "PREREGISTRATION.md",
    "mistura-do-infografico.md",
}


def candidatos():
    """List the files under ``data/raw`` that the policy removes from storage.

    Returns
    -------
    list of pathlib.Path
        Files to drop, sorted; manifests and files that the engine reads are never listed.
    """
    fora = []
    for f in sorted(RAW.rglob("*")):
        if not f.is_file() or f.name == "manifest.jsonl" or f.name in PROPRIOS:
            continue
        derivado = f.parent.name in {"saida", "series", "derivado"} or f.name.startswith(
            ("saida-", "recalcula")
        )
        if derivado and f.suffix in GUARDA | {".md"}:
            continue  # derived series and reports stay whatever their size (Seal 1 reads them)
        if f.suffix not in GUARDA or f.stat().st_size > LIMITE:
            fora.append(f)
        elif f.suffix == ".json" and "bruto" not in f.parts and f.stat().st_size <= LIMITE:
            continue
    return fora


def main(argv):
    """Print the plan; delete the files only with ``--apply``.

    Parameters
    ----------
    argv : list of str
        Command-line arguments.

    Returns
    -------
    int
        Always ``0``.
    """
    fora = candidatos()
    total = sum(f.stat().st_size for f in fora)
    print(f"{len(fora)} files, {total / 1e6:.1f} MB leave storage (hash+URL stay in manifests)")
    if "--apply" in argv:
        for f in fora:
            f.unlink()
        for d in sorted(
            {p for f in fora for p in f.parents if p != RAW and RAW in p.parents}, reverse=True
        ):
            if d.exists() and not any(d.iterdir()):
                d.rmdir()
        print("applied")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
