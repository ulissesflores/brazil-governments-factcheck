"""The verdict rule: rounding, tolerances, and the no-reproduction case."""

import pytest

from govfc.verdict import (
    APROXIMADO,
    NAO_REPRODUZ,
    NAO_VERIFICADO,
    REPRODUZ,
    parse_impresso,
    veredito,
)


@pytest.mark.parametrize(
    ("impresso", "reproduzido", "unidade", "esperado"),
    [
        ("3.4", 3.35, "pct", REPRODUZ),  # 3.35 rounds half up to the printed 3.4
        ("3.4", 3.3464, "pct", APROXIMADO),  # 3.3464 rounds to 3.3; 0.05 pp away
        ("7.6", 7.37, "pct", APROXIMADO),  # 0.23 pp
        ("4.9", 4.57, "pct", NAO_REPRODUZ),  # 0.33 pp and 6.7 % relative
        ("1088", 1504.22, "pct", NAO_REPRODUZ),  # 38 % relative
        ("0.59", 0.60, "indice", APROXIMADO),  # 1.7 % relative, no pp rule for indices
        ("0.59", 0.53, "indice", NAO_REPRODUZ),  # 10 % relative
        ("62.6", 62.55, "anos", REPRODUZ),
    ],
)
def test_rule(impresso, reproduzido, unidade, esperado):
    assert veredito(impresso, reproduzido, unidade) == esperado


def test_not_verified_when_no_reproduction():
    assert veredito("0.59", None, "indice") == NAO_VERIFICADO


def test_zero_target_uses_only_the_absolute_tolerance():
    assert veredito("0.0", 0.2, "pct") == APROXIMADO
    assert veredito("0.0", 0.2, "indice") == NAO_REPRODUZ


def test_parse_printed_forms():
    assert parse_impresso("~34") == (34, 0)
    assert parse_impresso("+42.8") == (parse_impresso("42.8")[0], 1)
    assert parse_impresso("2.9*")[0] == parse_impresso("2.9")[0]
    assert parse_impresso("-13.9")[0] < 0
