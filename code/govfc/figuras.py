"""Figures as code. Every number drawn comes from ``output/results.json``.

Claim-map (no figure without a claim):

* ``placar`` -- claim: "of the 57 numbers printed on the infographic, only 2 reproduce from
  public data and 30 do not" (counts read from ``results.json``).
"""

import json
from pathlib import Path

from govfc.i18n import COLUNAS, DECIMAL, INDICADORES, PLACAR
from govfc.svg import Cena
from govfc.verdict import APROXIMADO, NAO_REPRODUZ, NAO_VERIFICADO, REPRODUZ

RAIZ = Path(__file__).resolve().parents[2]
URL_REPO = "github.com/ulissesflores/brazil-governments-factcheck"

# Brand palette (ulisses-website app/globals.css and data/artigos-charts.ts, read 2026-10-19).
MARINHO, SUPERFICIE = "#101d2a", "#14191f"
OURO, OURO_CLARO, AZUL, CINZA = "#a48f65", "#c4ad7f", "#60a5fa", "#64748b"
TEXTO, TEXTO2 = "#f5f0e6", "#94a3b8"

ORDEM_IND = ["pib", "inflacao", "desemprego", "salmin", "pobreza", "gini", "expvida"]
ORDEM_COL = ["ditadura", "itamar", "fhc", "lula12", "dilma", "temer", "bolsonaro", "lula3"]
CASAS = {
    "pib": 1,
    "inflacao": 1,
    "desemprego": 1,
    "salmin": 1,
    "pobreza": 1,
    "gini": 2,
    "expvida": 1,
}


def carregar_resultados():
    """Read ``output/results.json``.

    Returns
    -------
    dict
        The parsed results document.
    """
    return json.loads((RAIZ / "output" / "results.json").read_text(encoding="utf-8"))


def selo_curto():
    """Return the first 16 hex digits of the sealed ``chain_hash``, or ``"pending"``."""
    p = RAIZ / "output" / "provenance.json"
    return json.loads(p.read_text())["chain_hash"][:16] if p.exists() else "pending"


def fmt(valor, casas, lang, pct=False):
    """Format a number with the decimal mark of ``lang`` (and ``%`` when ``pct``).

    Parameters
    ----------
    valor : float
        The number.
    casas : int
        Decimal places.
    lang : str
        Language code.
    pct : bool
        Append a percent sign.

    Returns
    -------
    str
        The formatted number.
    """
    s = f"{valor:.{casas}f}".replace(".", DECIMAL[lang])
    return s + "%" if pct else s


def _impresso_fmt(txt, lang, pct):
    """Localise a printed token (keeps ``~``, ``+`` and ``-``; drops ``*``)."""
    token = txt.split(" ")[0].rstrip("*")
    return token.replace(".", DECIMAL[lang]) + ("%" if pct else "")


def _casas_impresso(txt):
    """Number of decimal places in a printed token."""
    token = txt.split(" ")[0].rstrip("*")
    return len(token.split(".")[1]) if "." in token else 0


def _marca(c, cx, cy, ver):
    """Draw the verdict mark: shape plus colour, never colour alone."""
    if ver == REPRODUZ:
        c.circulo(cx, cy, 8, fill=AZUL)
    elif ver == APROXIMADO:
        c.circulo(cx, cy, 8, stroke=AZUL, sw=2)
        c.caminho(f"M {cx:.1f} {cy - 8:.1f} A 8 8 0 0 0 {cx:.1f} {cy + 8:.1f} Z", fill=AZUL)
    elif ver == NAO_REPRODUZ:
        c.rect(cx - 8, cy - 8, 16, 16, fill=OURO, rx=2)
        c.linha(cx - 4, cy - 4, cx + 4, cy + 4, MARINHO, 2)
        c.linha(cx - 4, cy + 4, cx + 4, cy - 4, MARINHO, 2)
    else:
        c.circulo(cx, cy, 8, stroke=CINZA, sw=2, dash="3 3")


def _cor_valor(ver):
    """Colour of the reproduced value by verdict (gold = what the reader should see first)."""
    return {REPRODUZ: AZUL, APROXIMADO: AZUL, NAO_REPRODUZ: OURO_CLARO}.get(ver, TEXTO2)


def placar(res, lang):
    """Build the redone infographic: printed number vs reproduced number, with a verdict mark.

    Parameters
    ----------
    res : dict
        Parsed ``results.json``.
    lang : str
        One of ``pt-BR``, ``en``, ``es``, ``it``, ``he``.

    Returns
    -------
    govfc.svg.Cena
        The scene (call ``.svg()`` to render it).
    """
    linhas = {r["id"]: r for r in res["linhas"]}
    cont = res["resumo"]["total"]
    n = sum(cont.values())
    textos = {k: (v[lang] if isinstance(v, dict) else v) for k, v in PLACAR.items()}
    ctg = textos["contagem"].format(
        n=n,
        r=cont.get(REPRODUZ, 0),
        a=cont.get(APROXIMADO, 0),
        x=cont.get(NAO_REPRODUZ, 0),
        u=cont.get(NAO_VERIFICADO, 0),
    )
    desc = [textos["titulo"] + ". " + ctg + "."]
    W, H = 1760, 1430
    x0, cw, gap, rh = 350, 165, 7, 128
    c = Cena(W, H, MARINHO, textos["titulo"], "")
    rtl = lang == "he"
    ax, ah = (W - 40, "end") if rtl else (40, "start")  # header block follows the text direction
    c.texto(ax, 74, textos["titulo"], 44, TEXTO, bold=True, anchor=ah, maxw=W - 80)
    c.texto(ax, 122, ctg, 23, OURO_CLARO, anchor=ah, maxw=W - 80)
    c.texto(ax, 160, textos["celula"], 19, TEXTO2, anchor=ah, maxw=W - 80)
    for i, (ver, rot) in enumerate(
        zip([REPRODUZ, APROXIMADO, NAO_REPRODUZ, NAO_VERIFICADO], textos["legenda"], strict=True)
    ):
        lx = 40 + i * 430
        _marca(c, lx + 9, 207, ver)
        c.texto(lx + 26, 213, rot, 18, TEXTO, maxw=395)
    for j, col in enumerate(ORDEM_COL):
        nome, anos = COLUNAS[col][lang]
        cx = x0 + j * (cw + gap)
        c.texto(cx + cw / 2, 282, nome, 21, TEXTO, bold=True, anchor="middle", maxw=cw)
        c.texto(cx + cw / 2, 308, anos, 17, TEXTO2, anchor="middle", maxw=cw)
    for i, ind in enumerate(ORDEM_IND):
        y = 330 + i * (rh + 8)
        nome, dica = INDICADORES[ind][lang]
        lx, la = (x0 - 20, "end") if rtl else (40, "start")
        c.texto(lx, y + 52, nome, 22, TEXTO, bold=True, anchor=la, maxw=290)
        c.texto(lx, y + 82, dica, 16, TEXTO2, anchor=la, maxw=290)
        for j, col in enumerate(ORDEM_COL):
            cx = x0 + j * (cw + gap)
            ids = [k for k in linhas if k.split(".")[0] == col and k.split(".")[1] == ind]
            itens = [linhas[k] for k in ids]
            alerta = any(r["veredito"] == NAO_REPRODUZ for r in itens)
            c.rect(cx, y, cw, rh, fill=SUPERFICIE, stroke=OURO if alerta else "none", sw=2, rx=8)
            fatia = (cw - 16) / len(itens)
            for k, r in enumerate(itens):
                ix = cx + 8 + k * fatia
                pct = r["unidade"] == "pct"
                imp = _impresso_fmt(r["impresso"], lang, pct)
                c.texto(ix, y + 34, imp, 17 if len(itens) == 1 else 14, TEXTO2, maxw=fatia - 22)
                _marca(c, ix + fatia - 16, y + 28, r["veredito"])
                if r["valor_reproduzido"] is None:
                    rep = "—"
                else:
                    rep = fmt(r["valor_reproduzido"], _casas_impresso(r["impresso"]), lang, pct)
                c.texto(
                    ix,
                    y + 84,
                    rep,
                    26 if len(itens) == 1 else 18,
                    _cor_valor(r["veredito"]),
                    bold=True,
                    maxw=fatia - 6,
                )
                desc.append(f"{COLUNAS[col][lang][0]}, {INDICADORES[ind][lang][0]}: {imp} / {rep}.")
    yb = 330 + 7 * (rh + 8) + 30
    c.texto(ax, yb, textos["rodape_regra"], 17, TEXTO2, anchor=ah, maxw=W - 80)
    c.texto(ax, yb + 28, textos["rodape_fonte"], 17, TEXTO2, anchor=ah, maxw=W - 80)
    pie = f"SHA-256: {selo_curto()} · {URL_REPO} · CC BY 4.0"
    c.texto(ax, yb + 60, pie, 17, OURO_CLARO, anchor=ah, maxw=W - 80)
    if rtl:
        c.texto(ax, yb + 90, PLACAR["traducao_he"], 15, TEXTO2, anchor=ah, maxw=W - 80)
    c.descricao = " ".join(desc)
    return c
