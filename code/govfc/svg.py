"""Minimal SVG scene builder (standard library only) that records every text for a fit check.

A scene is a list of primitives; :meth:`Cena.svg` renders it. Each :meth:`Cena.texto` call
stores the string, size, weight and the width budget (``maxw``) so that
:mod:`govfc.medidor` can measure the text in the real font and reject any label that would be
clipped. The output is deterministic: no random numbers, no timestamps.
"""

import re
from html import escape

_INTERVALO = re.compile(r"\d+[–-]\d+")

FAMILIA = "Fahkwang, 'Noto Sans Hebrew', system-ui, sans-serif"


def tem_hebraico(s):
    """Return ``True`` if ``s`` contains a Hebrew letter."""
    return any("֐" <= c <= "׿" for c in s)


def proteger_rtl(s):
    """Prefix a Hebrew string with a right-to-left mark when its first strong letter is Latin.

    ``unicode-bidi: plaintext`` takes the base direction from the first *strong* character;
    digits and punctuation are neutral. A Hebrew sentence that starts with a Latin letter would
    otherwise resolve left-to-right, so it gets RLM (U+200F, zero width).
    """
    if not tem_hebraico(s):
        return s
    # digit-dash-digit inside RTL text would display reversed ("1–2" as "2–1"): isolate it LTR
    s = _INTERVALO.sub(lambda m: "\u2066" + m.group(0) + "\u2069", s)
    for c in s:
        if c.isalpha():
            return s if "\u0590" <= c <= "\u05ff" else "\u200f" + s
    return s


class Cena:
    """An SVG scene with a fixed size, a background colour and recorded texts."""

    def __init__(self, largura, altura, fundo, titulo, descricao):
        """Create a scene.

        Parameters
        ----------
        largura, altura : int
            Canvas size in pixels.
        fundo : str
            Background colour (hex).
        titulo : str
            Accessible title (``<title>``).
        descricao : str
            Accessible description (``<desc>`` and ``aria-label``): for assistive technology
            the description *is* the chart, so it states every number the chart shows.
        """
        self.largura, self.altura, self.fundo = largura, altura, fundo
        self.titulo, self.descricao = titulo, descricao
        self.itens, self.textos = [], []

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1, rx=0, dash="", op=1.0):
        """Add a rectangle."""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op != 1.0 else ""
        self.itens.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>'
        )

    def linha(self, x1, y1, x2, y2, stroke, sw=1, dash=""):
        """Add a straight line."""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.itens.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def circulo(self, cx, cy, r, fill="none", stroke="none", sw=1, dash=""):
        """Add a circle."""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.itens.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def caminho(self, d, fill="none", stroke="none", sw=1, dash="", op=1.0):
        """Add a path (``d`` is the SVG path data)."""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op != 1.0 else ""
        self.itens.append(
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linejoin="round" stroke-linecap="round"{da}{o}/>'
        )

    def texto(self, x, y, s, size, fill, bold=False, anchor="start", maxw=None):
        """Add a text and record it for the fit check.

        Parameters
        ----------
        x, y : float
            Anchor point (baseline).
        s : str
            The string.
        size : float
            Font size in pixels.
        fill : str
            Colour (hex).
        bold : bool
            Bold weight.
        anchor : str
            Physical side: ``start`` = left edge at ``x``, ``end`` = right edge at ``x``,
            ``middle`` = centred (mirrored internally for right-to-left strings).
        maxw : float or None
            Width budget in pixels; ``None`` means "must fit the canvas".
        """
        s = proteger_rtl(s)
        if tem_hebraico(
            s
        ):  # with direction=rtl, SVG "start" is the RIGHT edge: keep the API physical
            anchor = {"start": "end", "end": "start"}.get(anchor, anchor)
        orcamento = maxw if maxw is not None else self.largura
        self.textos.append({"s": s, "size": size, "bold": bold, "maxw": orcamento})
        rtl = ' direction="rtl" unicode-bidi="plaintext"' if tem_hebraico(s) else ""
        w = ' font-weight="700"' if bold else ""
        self.itens.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{w}{rtl}>{escape(s)}</text>'
        )

    def svg(self):
        """Render the scene as an SVG document (string)."""
        cab = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.largura} {self.altura}" '
            f'width="{self.largura}" height="{self.altura}" role="img" '
            f'aria-label="{escape(self.descricao, quote=True)}" font-family="{FAMILIA}">'
        )
        corpo = [
            f"<title>{escape(self.titulo)}</title>",
            f"<desc>{escape(self.descricao)}</desc>",
            f'<rect width="{self.largura}" height="{self.altura}" fill="{self.fundo}"/>',
            *self.itens,
        ]
        return cab + "\n" + "\n".join(corpo) + "\n</svg>\n"
