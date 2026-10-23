"""Single, pre-declared verdict rule applied to every infographic number.

The rule is fixed before any result is looked at and is applied identically to every row
(Ulisses Flores, 2026-10-19; documented in ``REPRODUCIBILITY.md``). It compares the number
*as printed* on the infographic with the number reproduced from primary data under the
primary specification of that row.
"""

from decimal import ROUND_HALF_UP, Decimal

REPRODUZ = "REPRODUZ"
APROXIMADO = "APROXIMADO"
NAO_REPRODUZ = "NAO_REPRODUZ"
NAO_VERIFICADO = "NAO_VERIFICADO"

#: Absolute tolerance, in percentage points, for rows whose unit is a percentage.
TOL_PP = Decimal("0.3")
#: Relative tolerance (5 %) for any unit.
TOL_REL = Decimal("0.05")

SIMBOLO = {REPRODUZ: "✅", APROXIMADO: "⚠️", NAO_REPRODUZ: "❌", NAO_VERIFICADO: "❓"}


def parse_impresso(texto):
    """Parse a number as printed on the infographic.

    Parameters
    ----------
    texto : str
        Printed value, e.g. ``"7.6"``, ``"1088"``, ``"~34"``, ``"+42.8"``, ``"-13.9"``.

    Returns
    -------
    value : decimal.Decimal
        The numeric value (sign kept, ``~`` and ``+`` and ``%`` removed).
    casas : int
        Number of decimal places printed.
    """
    limpo = texto.strip().lstrip("~").lstrip("+").rstrip("%*").replace(",", ".")
    valor = Decimal(limpo)
    casas = -valor.as_tuple().exponent if valor.as_tuple().exponent < 0 else 0
    return valor, casas


def veredito(impresso, reproduzido, unidade):
    """Classify one infographic number against its reproduction.

    Parameters
    ----------
    impresso : str
        The number as printed on the infographic.
    reproduzido : float or None
        The value reproduced under the row's primary specification, or ``None`` when the
        primary source could not be reached.
    unidade : str
        ``"pct"`` for percentages (absolute tolerance in percentage points applies) or any
        other string (only the relative tolerance applies).

    Returns
    -------
    str
        ``REPRODUZ`` if the reproduction rounds (half up) to the printed value at the printed
        precision; ``APROXIMADO`` if not, but within 0.3 percentage points (``unidade="pct"``)
        or within 5 % relative; ``NAO_REPRODUZ`` otherwise; ``NAO_VERIFICADO`` if
        ``reproduzido`` is ``None``.
    """
    if reproduzido is None:
        return NAO_VERIFICADO
    alvo, casas = parse_impresso(impresso)
    rep = Decimal(repr(reproduzido))
    arred = rep.quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP)
    if arred == alvo:
        return REPRODUZ
    dif = abs(rep - alvo)
    if unidade == "pct" and dif <= TOL_PP:
        return APROXIMADO
    if alvo != 0 and dif / abs(alvo) <= TOL_REL:
        return APROXIMADO
    return NAO_REPRODUZ
