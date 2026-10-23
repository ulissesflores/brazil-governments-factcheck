#!/usr/bin/env python3
"""Write ``output/figures/<name>.<lang>.svg`` for every figure and language, after a fit check.

Requires Pillow (``pip install pillow``) only for the fit check; the SVG itself is plain text.
Figures are outside the seal (informational), but every number they show is read from
``output/results.json`` and pinned by ``tests/test_figures.py``.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "code"))

from govfc import figuras, medidor  # noqa: E402
from govfc.i18n import LINGUAS  # noqa: E402


def main():
    """Render all figures; exit 1 if any label overflows its width budget."""
    saida = RAIZ / "output" / "figures"
    saida.mkdir(parents=True, exist_ok=True)
    res = figuras.carregar_resultados()
    ruins = 0
    for lang in LINGUAS:
        cena = figuras.placar(res, lang)
        for e in medidor.estouros(cena):
            print(f"OVERFLOW placar.{lang}: {e}")
            ruins += 1
        (saida / f"placar.{lang}.svg").write_text(cena.svg(), encoding="utf-8")
        print(f"placar.{lang}.svg")
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main())
