"""Fit check: measure every recorded text in the real font; reject labels that would be clipped.

An SVG does not measure text, so a label that does not fit is clipped silently. This module
measures each string with Pillow in the fonts shipped in ``assets/fonts`` (Fahkwang for Latin,
Noto Sans Hebrew for Hebrew) and returns the labels whose measured width exceeds their budget.
"""

from pathlib import Path

from govfc.svg import tem_hebraico

FONTES = Path(__file__).resolve().parents[2] / "assets" / "fonts"
_CACHE = {}


def _fonte(size, bold, hebraico):
    """Load (and cache) the PIL font for a size, weight and script."""
    from PIL import ImageFont

    chave = (size, bold, hebraico)
    if chave not in _CACHE:
        if hebraico:
            f = ImageFont.truetype(str(FONTES / "NotoSansHebrew.ttf"), size)
            f.set_variation_by_name("Bold" if bold else "Regular")
        else:
            f = ImageFont.truetype(
                str(FONTES / ("Fahkwang-Bold.ttf" if bold else "Fahkwang-Regular.ttf")), size
            )
        _CACHE[chave] = f
    return _CACHE[chave]


def largura(s, size, bold=False):
    """Measured width of ``s`` in pixels at ``size`` (Hebrew uses the Hebrew font).

    Parameters
    ----------
    s : str
        The string.
    size : float
        Font size in pixels.
    bold : bool
        Bold weight.

    Returns
    -------
    float
        Advance width in pixels.
    """
    return _fonte(size, bold, tem_hebraico(s)).getlength(s)


def estouros(cena):
    """List the recorded texts of a scene that do not fit their width budget.

    Parameters
    ----------
    cena : govfc.svg.Cena
        A scene built with :class:`govfc.svg.Cena`.

    Returns
    -------
    list of dict
        One entry per overflowing text: ``s``, ``medido``, ``maxw``.
    """
    ruins = []
    for t in cena.textos:
        w = largura(t["s"], t["size"], t["bold"])
        if w > t["maxw"]:
            ruins.append({"s": t["s"], "medido": round(w, 1), "maxw": t["maxw"]})
    return ruins
