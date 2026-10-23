#!/usr/bin/env python3
"""Build the one-page terminal (``output/raio-x.html``) from the template and the sealed outputs.

The template ``scripts/page/raiox.html`` carries the page (CSS, HTML, JavaScript, lightweight-charts
4.1.3 from unpkg) with five placeholders; this script replaces them with ``output/terminal.json``,
``output/indice.json``, ``output/auditoria.json``, ``output/mundo.json`` and
``output/literatura.json``. The rendered page is informational (not hashed): it is a view of the
sealed JSON, never a source.
Usage: ``python3 scripts/build_page.py [saida.html]``.
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEMPLATE = RAIZ / "scripts" / "page" / "raiox.html"
PLACEHOLDERS = {
    "__DATA__": "terminal.json",
    "__INDICE__": "indice.json",
    "__AUDIT__": "auditoria.json",
    "__MUNDO__": "mundo.json",
    "__LIT__": "literatura.json",
}


def construir(saida):
    """Render the page into ``saida`` and return its size in bytes."""
    html = TEMPLATE.read_text(encoding="utf-8")
    for marca, nome in PLACEHOLDERS.items():
        dados = json.loads((RAIZ / "output" / nome).read_text(encoding="utf-8"))
        if marca not in html:
            raise SystemExit(f"placeholder {marca} missing in template")
        texto = json.dumps(dados, ensure_ascii=False, separators=(",", ":"))
        # U+FFFD arrives inside source data (an author name as OpenAlex serves it); the data stays
        # as served, and the page writes it as a JSON escape so the HTML file carries no raw U+FFFD.
        html = html.replace(marca, texto.replace("�", "\\ufffd"))
    saida.write_text(html, encoding="utf-8")
    return len(html.encode("utf-8"))


if __name__ == "__main__":
    destino = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "output" / "raio-x.html"
    print(f"{destino} {construir(destino)} bytes")
