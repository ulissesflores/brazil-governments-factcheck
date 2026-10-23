"""The terminal view (amendments 03 G and 04): yearly candles on RATES, one JSON per indicator.

A candle only means something on a series that goes up and down: a 12-month rate, a growth
rate, a ratio, a real wage. Price and money LEVELS only rise, so they get no candle here; the
page shows 12-month inflation, the Selic, 12-month growth of the monetary base against that
inflation, the bank money multiplier and 4-quarter GDP growth. Open = last value of the previous
year, close = last value of the year, high/low = the extremes of the monthly (or quarterly)
values; colour is the raw direction (close above open = up) and the header says what "up" means.
Old and new method lines are never spliced: each base is its own series and the candles sit on
one declared base. Series that exist once a year are drawn as a line. A signed band (``faixa``)
is emitted only where a second variable with a sign exists (money growth minus inflation, real
interest). Dated events come from the money-and-fiscal collection's ``marcos.csv``. Nothing here
is an estimate.
"""

import csv
import json
import re
from pathlib import Path

from govfc.explica import EXPLICA, PRODUTOS, explica_mundo, explica_produto
from govfc.mandatos import carregar

RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw"
CURADO = RAIZ / "data" / "curated"


def _lido(caminho):
    """Read a CSV into a list of dicts."""
    with open(caminho, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _ipea(nome):
    """Ipeadata raw JSON -> ``{"YYYY-MM": value}`` (a quarter keeps its first month)."""
    j = json.loads((RAW / "economia-real" / nome).read_text(encoding="utf-8"))["value"]
    return {r["VALDATA"][:7]: float(r["VALVALOR"]) for r in j if r["VALVALOR"] is not None}


def _bcb_mensal(arquivo):
    """BCB SGS monthly JSON -> ``{"YYYY-MM": percent}``."""
    dados = json.loads((RAW / "inflacao" / arquivo).read_text())
    return {f"{r['data'][-4:]}-{r['data'][3:5]}": float(r["valor"]) for r in dados}


def _longo(colecao, nome):
    """Long-format ``series/*.csv`` of a collection -> ``{"YYYY-MM": v}`` or ``{year: v}``."""
    out = {}
    for r in _lido(RAW / colecao / "series" / nome):
        if r["valor"] in ("", "NA"):
            continue
        mes = r.get("mes_ou_trimestre", "")
        chave = f"{int(r['ano'])}-{int(mes):02d}" if mes else int(r["ano"])
        out[chave] = float(r["valor"])
    return out


def _porquinho(linha):
    """One line of ``porquinho/series/porquinho.csv`` -> ``{"YYYY-MM": v}``."""
    out = {}
    for r in _lido(RAW / "porquinho" / "series" / "porquinho.csv"):
        if r["linha"] == linha and r["mes"] and r["valor"]:
            out[f"{int(r['ano'])}-{int(r['mes']):02d}"] = float(r["valor"])
    return out


def _produto_horas(produto, coluna="horas_salario_minimo"):
    """Hours of work to buy one unit of ``produto`` (``produtos_em_horas.csv``) -> ``{"YYYY-MM": h}``."""
    out = {}
    for r in _lido(RAW / "produtos" / "series" / "produtos_em_horas.csv"):
        if r["produto"] == produto and r["granularidade"] == "mensal" and r[coluna]:
            out[f"{int(r['ano'])}-{int(r['mes']):02d}"] = float(r[coluna])
    return out


def _produto_anual(produto, coluna="horas_decil10_ppc2017"):
    """Annual rows of one product in ``produtos_em_horas.csv`` -> ``{year: v}``."""
    out = {}
    for r in _lido(RAW / "produtos" / "series" / "produtos_em_horas.csv"):
        if r["produto"] == produto and r["granularidade"] == "anual" and r[coluna]:
            out[int(r["ano"])] = float(r[coluna])
    return out


PPC2017_EM_REAIS = (
    2.3273771  # R$ de 2017 por US$ PPC 2017 (IBGE SIS, consumo privado), como na coleta de produtos
)


def _renda_decil_mensal(decis, obs):
    """Mean per-capita household income of the given deciles (PIP, PPC 2017) -> ``{year: R$ nominais por mês}``.

    US$ PPC/dia x 365/12 x R$ 2,3273771 = R$ de 2017 por mês; x IPCA médio do ano / IPCA médio de 2017 =
    R$ nominais do ano. The newest comparable survey wins for a year (PNADC-E1, then PNADC-E5, then PNAD).
    """
    ipca = _bcb_mensal("ipca-sgs433-raw.json")
    nivel, idx = 100.0, {}
    for k in sorted(ipca):
        nivel *= 1 + ipca[k] / 100
        idx.setdefault(int(k[:4]), []).append(nivel)
    media = {a: sum(v) / len(v) for a, v in idx.items()}
    pref = {"PNADC-E1": 0, "PNADC-E5": 1, "PNAD": 2}
    por_ano = {}
    for r in obs:
        if (
            r["indicador"] != "renda_decil"
            or "PPC 2017" not in r["serie"]
            or not re.fullmatch(r"\d{4}", r["periodo"])
        ):
            continue
        m = re.match(r"PIP decil (\d+) \((\S+), income", r["serie"])
        if not m or int(m.group(1)) not in decis:
            continue
        a, d, pesq = int(r["periodo"]), int(m.group(1)), m.group(2)
        atual = por_ano.setdefault(a, {}).get(d)
        if atual is None or pref.get(pesq, 9) < pref.get(atual[1], 9):
            por_ano[a][d] = (float(r["valor"]), pesq)
    out = {}
    for a, dd in por_ano.items():
        if len(dd) == len(decis) and a in media and 2017 in media:
            usd_dia = sum(v for v, _ in dd.values()) / len(decis)
            out[a] = usd_dia * 365 / 12 * PPC2017_EM_REAIS * media[a] / media[2017]
    return out


def _preco_medio_anual(produto):
    """Mean nominal price of the year (R$ atuais) of one product -> ``{year: R$}``."""
    por = {}
    for r in _lido(RAW / "produtos" / "series" / "produtos_em_horas.csv"):
        if r["produto"] == produto and r["granularidade"] == "mensal" and r["preco_R$_atuais"]:
            por.setdefault(int(r["ano"]), []).append(float(r["preco_R$_atuais"]))
    return {a: sum(v) / len(v) for a, v in por.items()}


def _derivado_mensal(colecao, nome):
    """Monthly rows of one derived CSV (``data/raw/<colecao>/derivado/<nome>``) -> ``{"YYYY-MM": v}``."""
    out = {}
    for r in _lido(RAW / colecao / "derivado" / nome):
        if r["valor"] not in ("", "NA") and r["mes_ou_trimestre"]:
            out[f"{int(r['ano'])}-{int(r['mes_ou_trimestre']):02d}"] = float(r["valor"])
    return out


def _salario_minimo_nominal():
    """Nominal minimum wage of each month (R$ atuais), from the products file -> ``{"YYYY-MM": R$}``."""
    out = {}
    for r in _lido(RAW / "produtos" / "series" / "produtos_em_horas.csv"):
        if (
            r["produto"] == "arroz"
            and r["granularidade"] == "mensal"
            and r["salario_minimo_R$_atuais"]
        ):
            out[f"{int(r['ano'])}-{int(r['mes']):02d}"] = float(r["salario_minimo_R$_atuais"])
    return out


def _tabela_ans(coluna):
    """One column of ``ans-planos-fase2/derivado/tabela_por_ano.csv`` -> ``{year: %}``."""
    out = {}
    for r in _lido(RAW / "ans-planos-fase2" / "derivado" / "tabela_por_ano.csv"):
        if r[coluna] not in ("", "NA") and re.fullmatch(r"\d{4}", r["ano"]):
            out[int(r["ano"])] = float(r[coluna])
    return out


def _longo_ind(colecao, nome, indicador, coluna="valor"):
    """Annual rows of one ``indicador`` in a long CSV -> ``{year: v}`` (sub-annual rows skipped)."""
    out = {}
    for r in _lido(RAW / colecao / "series" / nome):
        if (
            r["indicador"] == indicador
            and re.fullmatch(r"\d{4}", r["ano"])
            and r[coluna] not in ("", "NA")
        ):
            out[int(r["ano"])] = float(r[coluna])
    return out


CTB_BASE = "receita-ctb-por-base-por-edicao.csv"
#: the six aggregate bases of table INC02B (code, label); the total is in the indicator ``carga``
CTB_BASES = [
    ("1000", "Renda"),
    ("2000", "Folha de salários"),
    ("3000", "Propriedade"),
    ("4000", "Bens e serviços"),
    ("5000", "Transações financeiras"),
    ("9000", "Outros tributos"),
]
ESTATAIS = [
    ("petrobras", "Petrobras (1997-2009)", "petrobras"),
    ("bb", "Banco do Brasil (1995-2009)", "banco-do-brasil"),
    ("caixa", "Caixa (2001-2025)", "caixa"),
    ("eletrobras", "Eletrobras (2000-2009)", "eletrobras"),
    ("correios", "Correios (2000-2025)", "correios"),
]
EMENDAS = "emendas_pagas_por_tipo_e_ano.csv"
EMENDAS_TIPOS = [
    (
        "emenda_individual_transferencias_com_finalidade_definida",
        "Individuais (finalidade definida)",
    ),
    ("emenda_individual_transferencias_especiais", "Individuais (transferências especiais, 'Pix')"),
    ("emenda_de_bancada", "Bancada estadual"),
    ("emenda_de_comissao", "Comissão"),
    ("emenda_de_relator", "Relator-geral"),
    ("total", "Todos os tipos"),
]


def _lucro(empresa):
    """Net profit lines of one state-owned company, one line per accounting basis, in R$ millions.

    Reads ``tributos-estado/estatais-lucro/series/lucro-liquido-<empresa>.csv``: every distinct
    ``definicao_linha`` (consolidated or parent company, BR GAAP, IFRS or US GAAP in reais) is a line
    of its own, never spliced; US$ lines are left out (another currency). Values in R$ thousands or
    units are rescaled to R$ millions, a unit change only.
    """
    por = {}
    for r in _lido(
        RAW / "tributos-estado" / "estatais-lucro" / "series" / f"lucro-liquido-{empresa}.csv"
    ):
        if r["valor"] in ("", "NA") or r["unidade"].startswith("US$"):
            continue
        fator = {"R$ mil": 1e-3, "R$": 1e-6, "R$ milhões": 1.0}[r["unidade"]]
        linha = por.setdefault(r["definicao_linha"], {})
        linha.setdefault(int(r["ano"]), float(r["valor"]) * fator)
    linhas = sorted(por.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [(k[:90], v) for k, v in linhas if len(v) >= 3]


def _atos():
    """Tax and bureaucracy acts (amendment 03 §C and §D), as the collection read them on planalto.gov.br."""
    out = []
    pasta = RAW / "tributos-estado"
    for nome, campo in (("eventos_tributarios.csv", "tributo"), ("eventos_burocracia.csv", None)):
        for r in _lido(pasta / nome):
            out.append(
                {
                    "data": r["data"],
                    "instrumento": r["instrumento"],
                    "tributo": r.get("tributo", "") if campo else "",
                    "tema": "" if campo else "burocracia e registro de empresas",
                    "sentido": r["sentido"],
                    "governo": r["governo"],
                    "url": r["url"],
                    "nota": r.get("base_do_sentido", "")[:120],
                }
            )
    return sorted(out, key=lambda e: e["data"])


def _ministerios(coluna):
    """``ministerios-por-ano.csv`` column -> ``{year: n}`` (count on 1 January)."""
    rows = _lido(RAW / "tributos-estado" / "ministerios" / "series" / "ministerios-por-ano.csv")
    return {int(r["ano"]): float(r[coluna]) for r in rows if r[coluna]}


def indice_100(d):
    """Rebase a monthly dict so its first value is 100."""
    ks = sorted(d)
    base = d[ks[0]]
    return {k: 100 * d[k] / base for k in ks} if base else {}


def _consecutivos(chaves):
    """True when monthly keys are consecutive months."""
    for a, b in zip(chaves, chaves[1:], strict=False):
        if int(a[:4]) * 12 + int(a[5:7]) + 1 != int(b[:4]) * 12 + int(b[5:7]):
            return False
    return True


def taxa_12m(taxas):
    """12-month compounded rate (%) from monthly rates (%): needs 12 consecutive months."""
    ks = sorted(taxas)
    out = {}
    for i in range(11, len(ks)):
        janela = ks[i - 11 : i + 1]
        if not _consecutivos(janela):
            continue
        f = 1.0
        for k in janela:
            f *= 1 + taxas[k] / 100
        out[ks[i]] = 100 * (f - 1)
    return out


def variacao_12m(nivel):
    """12-month change (%) of a monthly level (or 4-quarter change of a quarterly index)."""
    out = {}
    for k, v in nivel.items():
        k0 = f"{int(k[:4]) - 1}-{k[5:7]}"
        if k0 in nivel and nivel[k0] > 0 and v > 0:
            out[k] = 100 * (v / nivel[k0] - 1)
    return out


def razao(num, den):
    """Element-wise ratio of two ``{"YYYY-MM": v}`` dicts on the common keys."""
    return {k: num[k] / den[k] for k in num if k in den and den[k]}


def diferenca(a, b):
    """Element-wise ``a - b`` on the common keys."""
    return {k: a[k] - b[k] for k in a if k in b}


def candles_anuais(serie):
    """Yearly candles from a sub-annual ``{"YYYY-MM": value}`` series.

    Returns
    -------
    list of dict
        ``{"t": "YYYY-01-01", "o", "h", "l", "c", "n"}`` per year with at least 2 observations;
        open = last value of the previous year when it exists.
    """
    por_ano = {}
    for k, v in sorted(serie.items()):
        por_ano.setdefault(int(k[:4]), []).append(v)
    out, prev_close = [], None
    for ano in sorted(por_ano):
        vals = por_ano[ano]
        if len(vals) < 2:
            prev_close = vals[-1]
            continue
        o = prev_close if prev_close is not None else vals[0]
        out.append(
            {
                "t": f"{ano}-01-01",
                "o": o,
                "h": max(vals + [o]),
                "l": min(vals + [o]),
                "c": vals[-1],
                "n": len(vals),
            }
        )
        prev_close = vals[-1]
    return out


def _anual(obs, ind, trecho):
    """Annual ``{year: value}`` from the curated observations for one indicator and label."""
    out = {}
    for r in obs:
        if r["indicador"] == ind and trecho in r["serie"] and re.fullmatch(r"\d{4}", r["periodo"]):
            out.setdefault(int(r["periodo"]), float(r["valor"]))
    return out


def _pontos(d):
    """``{year|"YYYY-MM": v}`` -> sorted ``[["YYYY-MM-DD", v], ...]``."""
    out = []
    for k, v in sorted(d.items(), key=lambda kv: str(kv[0])):
        k = str(k)
        t = f"{k}-01-01" if len(k) == 4 else f"{k}-01"
        out.append([t, round(v, 6)])
    return out


MARCOS_EM = {
    "REAL-1994-07-01": ["*"],
    "CAMBIO-1999-01-15": ["inflacao", "emissao", "selic"],
    "METAS-INFLACAO-1999": ["inflacao", "selic"],
    "CRISE-2002": ["inflacao", "selic", "pib"],
    "CRISE-2008-RI": ["pib", "desemprego", "emissao", "selic", "primario"],
    "RECESSAO-2014-2016": ["pib", "desemprego", "primario", "divida"],
    "OMS-2020-03-11": ["*"],
    "LC179-2021": ["inflacao", "emissao", "selic", "multiplicador"],
}
MARCOS_ROTULO = {
    "REAL-1994-07-01": "Plano Real",
    "CAMBIO-1999-01-15": "Câmbio flutuante",
    "METAS-INFLACAO-1999": "Metas de inflação",
    "CRISE-2002": "Crise de 2002",
    "CRISE-2008-RI": "Crise financeira global",
    "RECESSAO-2014-2016": "Recessão 2014-16 (Codace)",
    "OMS-2020-03-11": "Pandemia",
    "LC179-2021": "Autonomia do BC",
}


def _marcos():
    """Dated events from ``moeda-fiscal/marcos.csv``, one per cluster, with the source text."""
    out = []
    for r in _lido(RAW / "moeda-fiscal" / "marcos.csv"):
        if r["id"] not in MARCOS_EM:
            continue
        t = r["data"] if len(r["data"]) == 10 else r["data"] + "-01"
        out.append(
            {
                "t": t,
                "rotulo": MARCOS_ROTULO[r["id"]],
                "fonte": r["evento"],
                "em": MARCOS_EM[r["id"]],
            }
        )
    return sorted(out, key=lambda e: e["t"])


QUEBRAS = {
    "inflacao": ["IPCA", "IGP"],
    "selic": ["selic", "Selic"],
    "emissao": ["Agregados"],
    "multiplicador": ["Agregados"],
    "moeda_pib": ["Agregados"],
    "salmin": ["Salario"],
    "pib": ["PIB"],
    "desemprego": ["Desemprego"],
    "primario": ["rtn", "nfsp", "Primario"],
    "discricionarias": ["rtn", "discricion"],
    "expvida": ["Expectativa"],
    "pobreza": ["Pobreza"],
    "gini": ["Gini"],
    "homic": ["seg_homic", "Homic"],
    "reprov": ["edu_reprov", "edu_repetentes", "Reprov"],
    "saeb": ["Saeb"],
    "tit": [],
    "porquinho_reais": ["porquinho", "poupanca", "PTAX"],
    "porquinho_refs": ["porquinho", "PTAX", "ouro"],
    "porquinho_brasil": ["porquinho", "Salario", "cesta"],
    "produtos_comida": [],
    "carga": ["ctb", "carga", "Carga"],
    "ministerios": ["minist"],
    "cargos": ["pep", "DAS", "FCPE"],
    "cargos_sem_vinculo": ["pep", "DAS", "FCPE"],
    "estatais": ["nfsp", "estatais"],
    "produtos_energia": [],
    "divida": ["Divida", "DBGG"],
}

# Amendment 05 §8: BCB SGS 1788 carries in Feb/2001 the value 47,891,196, 13% above Jan and
# Mar/2001 and equal to Feb/2002 (47,891,206) to five digits; the raw value stays in the chain,
# the two 12-month changes that use it are not shown.
M0_SUPRIMIDOS = ("2001-02", "2002-02")

# Amendment 05 §9: the staff panel's count falls 74% between Dec/2020 and Dec/2021 with no cause
# in the panel's changelog; the series is shown as two bases, never as one line.
CARGOS_CORTE = 2021

# Amendment 05 §11: 1997-2005 computed from the counts of grades 1-4 (8-year primary); 2006+
# as published for the early years of the 9-year primary.
REPROV_CORTE = 2006

PRODUTOS_TIPOS_IGNORADOS = {
    "inicio",
    "unidade",
    "saltos",
    "definicao",
    "conversao",
    "aproximacao",
    "pesquisa",
}


def _quebras_produtos(produtos):
    """Breaks of the products collection (``produtos/quebras.csv``) for the given product ids."""
    out = []
    for r in _lido(RAW / "produtos" / "quebras.csv"):
        if r["tipo"] in PRODUTOS_TIPOS_IGNORADOS:
            continue
        if not any(p in r["produto"] for p in produtos):
            continue
        m = re.search(r"(19|20)\d\d", r["data"])
        if not m:
            continue
        out.append(
            {
                "ano": m.group(0),
                "tipo": "mudanca_de_unidade" if r["tipo"] == "moeda" else r["tipo"],
                "razao": r["descricao"][:200],
                "efeito": r["medida_ou_efeito"][:120],
            }
        )
    return out


def _quebras_ipca_itens():
    """Breaks of the IPCA sub-item collection (``ipca-itens-fase2/quebras.csv``)."""
    out = []
    for r in _lido(RAW / "ipca-itens-fase2" / "quebras.csv"):
        m = re.search(r"(19|20)\d\d", r["data_quebra"])
        if m:
            out.append(
                {
                    "ano": m.group(0),
                    "tipo": r["tipo_de_quebra"],
                    "razao": r["razao_declarada_pela_fonte"][:200],
                    "efeito": r["efeito_medido"][:120],
                }
            )
    return out


def _corte(d, ano, antes=True):
    """Split an annual ``{year: v}`` dict at ``ano``: the years before it, or from it on."""
    return {a: v for a, v in d.items() if (a < ano) == antes}


PRE_REAL = {
    "id": "pre_real",
    "nome": "Antes do Real (1964-1994)",
    "curto": "1964-94",
    "posse": "1964-01-01",
    "saida": "1995-01-01",
}
COLUNAS = ["pre_real", "fhc", "lula12", "dilma", "temer", "bolsonaro", "lula3"]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def decimais(valores):
    """Displayed decimals from the median absolute value: 0 at >= 100 (or for counts), 1 at >= 1.5, else 2."""
    v = sorted(abs(x) for x in valores)
    m = v[len(v) // 2] if v else 1
    if all(float(x).is_integer() for x in v):
        return 0
    return 0 if m >= 100 else 1 if m >= 1.5 else 2


def fim_de_trimestre(d):
    """Re-key a quarterly ``{"YYYY-MM": v}`` dict from the first to the last month of each quarter."""
    return {f"{k[:4]}-{int(k[5:7]) + 2:02d}": v for k, v in d.items()}


def fmt_br(v, dec):
    """Brazilian number format: thousands with a dot, decimals with a comma."""
    s = f"{v:,.{dec}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def quando(t, freq):
    """'2002-12-01' -> 'dez/2002' (monthly), '4º tri/2002' (quarterly) or '2002' (annual)."""
    a, m = t[:4], int(t[5:7])
    if freq == "anual":
        return a
    if freq == "trimestral":
        return f"{(m - 1) // 3 + 1}º tri/{a}"
    return f"{MESES[m - 1]}/{a}"


def unidade_curta(un):
    """Prefix and suffix used to print one value of an indicator in a sentence."""
    if un.startswith("R$"):
        return "R$ ", ""
    if un.startswith("%"):
        return "", "%"
    if un.startswith("horas"):
        return "", " h"
    for chave, suf in (
        ("anos", " anos"),
        ("pontos", " pontos"),
        ("por 100 mil", " por 100 mil"),
        ("vezes", " vezes"),
    ):
        if chave in un:
            return "", suf
    return "", ""


def mandatos(linhas, govs, freq):
    """Per-term cells on each base: start, end, extremes (amendment 05 §2).

    Parameters
    ----------
    linhas : list of dict
        ``{"rotulo", "pontos": [[t, v], ...]}`` in declared order (the first is the main base).
    govs : list of dict
        Terms with ISO ``posse`` and ``saida``.
    freq : str
        ``"anual"``, ``"mensal"`` or ``"trimestral"``: sets how recent a start or end must be.

    Returns
    -------
    list of dict
        One entry per term: ``gov``, ``principal`` (index of the base that has both a start
        and an end inside the recency window and hugs the term best, or ``None``) and
        ``bases``. Start = last
        published value before the inauguration; end = last published value before the exit;
        max/min = extremes of the values published inside the term plus the start.
    """
    # months a start/end may lag the date: 13 for sub-annual series; 2 years + 11 months for
    # annual ones (the PNAD skipped 1994, 2000 and 2010; the Saeb is biennial)
    janela = 13 if freq != "anual" else 35

    def atraso(t, ref):
        """Months between a published date ``t`` and the reference date ``ref``."""
        return int(ref[:4]) * 12 + int(ref[5:7]) - int(t[:4]) * 12 - int(t[5:7])

    out = []
    for g in govs:
        posse, saida = g["posse"], g["saida"]
        corrente = g.get("corrente", False)  # term in course: the end is the latest value
        bases, candidatos = [], []
        for k, ln in enumerate(linhas):
            pts = ln["pontos"]
            antes = [p for p in pts if p[0] < posse]
            dentro = [p for p in pts if posse <= p[0] < saida]
            ini = antes[-1] if antes else None
            fim = dentro[-1] if dentro else None
            if ini is None and fim is None:
                continue
            ok_ini = ini is not None and atraso(ini[0], posse) <= janela
            ok_fim = fim is not None and (corrente or atraso(fim[0], saida) <= janela)
            vals = ([ini] if ok_ini else []) + dentro
            bases.append(
                {
                    "k": k,
                    "inicio": ini if ok_ini else None,
                    "fim": fim if ok_fim else None,
                    "max": max(vals, key=lambda p: p[1]) if vals else None,
                    "min": min(vals, key=lambda p: p[1]) if vals else None,
                    "n": len(dentro),
                }
            )
            if ok_ini and ok_fim:
                # the base that hugs the term best wins (smallest total lag); ties keep order
                candidatos.append((atraso(ini[0], posse) + atraso(fim[0], saida), k))
        principal = min(candidatos)[1] if candidatos else None
        out.append({"gov": g["id"], "principal": principal, "bases": bases})
    return out


def frase(nome, un, linha, freq):
    """One computed sentence: the main base's first value from Dec/1994 on and its last value."""
    pts = [p for p in linha["pontos"] if p[0] >= "1994-12"] or linha["pontos"]
    if len(pts) < 2:
        return ""
    dec = decimais([p[1] for p in pts])
    pre, suf = unidade_curta(un)
    (t0, v0), (t1, v1) = pts[0], pts[-1]
    return f"{nome}: {pre}{fmt_br(v0, dec)}{suf} em {quando(t0, freq)}; {pre}{fmt_br(v1, dec)}{suf} em {quando(t1, freq)}."


CURTO = {
    "castelo": "Castelo",
    "costa_silva": "Costa e Silva",
    "medici": "Médici",
    "geisel": "Geisel",
    "figueiredo": "Figueiredo",
    "sarney": "Sarney",
    "collor": "Collor",
    "itamar": "Itamar",
    "fhc": "FHC",
    "lula12": "Lula 1-2",
    "dilma": "Dilma",
    "temer": "Temer",
    "bolsonaro": "Bolsonaro",
    "lula3": "Lula 3",
}

#: Units of the phase-2 index items that get their own chart here (the index stores values without units).
UN_ITENS = {
    "pibpc": "US$ PPC de 2021 por habitante",
    "fbcf": "% do PIB",
    "ptf": "índice (2017 = 1)",
    "renda_trab": "R$ a preços constantes, média mensal",
    "informalidade": "% dos ocupados",
    "subalimentacao": "% da população",
    "mortinf": "por mil nascidos vivos",
    "mortmat": "por 100 mil nascidos vivos",
    "dtp3": "% das crianças de 1 ano",
    "prenatal": "% dos nascidos vivos",
    "analfabetismo": "% da população de 15 anos ou mais",
    "agua": "% dos domicílios",
    "esgoto": "% dos domicílios",
    "desmatamento": "km² por ano",
    "familias": "% da renda acumulada em 12 meses",
    "reservas": "% do PIB",
    "pd": "% do PIB",
    "pesquisadores": "por milhão de habitantes",
    "patentes": "pedidos por milhão de habitantes",
    "eci": "índice (Atlas of Economic Complexity)",
    "internet": "% dos domicílios",
    "industria": "% do PIB",
    "governo": "% do PIB",
    "abertura": "% do PIB",
    "libdem": "0 a 1",
    "corrupcao": "0 a 1",
    "legcon": "0 a 1",
    "jucon": "0 a 1",
    "estatal": "escala V-Dem (maior = menos propriedade estatal)",
}
#: World comparison: references drawn beside Brazil (groups first; countries only when the source has no group).
MUNDO_REFS = ["WLD", "LCN", "UMC", "ARG", "CHL", "COL", "MEX", "URY"]

DOMINIOS = [
    ("Preços e moeda", ["inflacao", "selic", "emissao", "multiplicador", "moeda_pib", "tit"]),
    ("Atividade e renda", ["pib", "pibpc", "fbcf", "ptf", "salmin", "renda_trab"]),
    ("Trabalho", ["desemprego", "informalidade"]),
    (
        "Fiscal e dívida",
        [
            "primario",
            "nominal",
            "juros_nominais",
            "discricionarias",
            "divida",
            "familias",
            "reservas",
        ],
    ),
    (
        "Setor externo e dívida externa",
        [
            "divext",
            "divext_reservas",
            "divext_pib",
            "divext_liquida_pib",
            "divext_publico",
            "pii_pib",
        ],
    ),
    ("Pobreza e desigualdade", ["pobreza", "gini", "subalimentacao"]),
    ("Saúde", ["expvida", "mortinf", "mortmat", "dtp3", "prenatal"]),
    ("Segurança", ["homic", "homic_n"]),
    ("População", ["nascimentos", "obitos"]),
    ("Educação", ["reprov", "saeb", "analfabetismo"]),
    ("Moradia e infraestrutura", ["agua", "esgoto", "internet"]),
    ("Ambiente", ["desmatamento"]),
    ("Ciência e tecnologia", ["pd", "pesquisadores", "patentes", "eci"]),
    ("Instituições (V-Dem)", ["libdem", "corrupcao", "legcon", "jucon"]),
    ("Premissas econômicas (camada P)", ["industria", "governo", "abertura", "estatal"]),
    (
        "Estado e tributos",
        [
            "carga",
            "carga_base",
            "ministerios",
            "cargos",
            "cargos_sem_vinculo",
            "estatais",
            "lucro_petrobras",
            "lucro_bb",
            "lucro_caixa",
            "lucro_eletrobras",
            "lucro_correios",
            "emendas_pagas",
            "emendas_pib",
        ],
    ),
    (
        "O porquinho (R$ 100 mil de dez/1994)",
        ["porquinho_reais", "porquinho_refs", "porquinho_brasil"],
    ),
    (
        "Produtos em horas de trabalho",
        [f"prod_{p}" for p in PRODUTOS] + ["aluguel_saude", "plano_saude"],
    ),
    (
        "Brasil e o mundo (mesma fonte para todos)",
        [
            "mun_pib_cresc",
            "mun_pibpc_ppc",
            "mun_inflacao",
            "mun_desemprego_oit",
            "mun_pobreza_685",
            "mun_pobreza_830_ppc2021",
            "mun_gini",
            "mun_expvida",
            "mun_mortinf",
            "mun_dtp3",
            "mun_homic",
            "mun_polyarchy",
            "mun_divext_rnb",
        ],
    ),
]


def construir():
    """Build the terminal bundle.

    Returns
    -------
    dict
        ``governos`` (bands), ``eventos`` (dated markers from ``marcos.csv``), ``dominios``
        (tab groups), ``indicadores``.
    """
    eventos = _marcos()
    obs = _lido(CURADO / "observations.csv")
    quebras = _lido(CURADO / "quebras.csv")
    mensal = {r["ym"]: r for r in _lido(RAW / "monetario" / "saida" / "mensal.csv")}
    anual = {int(r["ano"]): r for r in _lido(RAW / "monetario" / "saida" / "anual.csv")}

    def col(nome):
        """Monthly column of ``mensal.csv`` as ``{"YYYY-MM": float}``."""
        return {k: float(r[nome]) for k, r in mensal.items() if r[nome]}

    def col_anual(nome):
        """Annual column of ``anual.csv`` as ``{year: float}``."""
        return {a: float(r[nome]) for a, r in anual.items() if r[nome]}

    ipca12 = taxa_12m(_bcb_mensal("ipca-sgs433-raw.json"))
    inpc12 = taxa_12m(_bcb_mensal("inpc-sgs188-raw.json"))
    igpdi12 = variacao_12m(col("igpdi_idx"))
    m0, m1, m1n = col("M0_fim"), col("M1_fim"), col("M1_novo")
    m3, m3n = col("M3_reg2001"), col("M3_novo")
    m0_12 = variacao_12m(m0)
    for k in M0_SUPRIMIDOS:  # amendment 05 §8: the source carries Feb/2002's value in Feb/2001
        m0_12.pop(k, None)
    salmin = _ipea("ipeadata-GAC12_SALMINRE12-raw.json")
    pib_4t = fim_de_trimestre(variacao_12m(_ipea("ipeadata-SCN104_PIBPMAS104-raw.json")))
    pme_a = _ipea("ipeadata-PME12_TDA12-raw.json")
    pme_n = _ipea("ipeadata-PAN12_TD12-raw.json")
    selic_aa = _longo("moeda-fiscal", "selic_over_mensal_ipeadata_PAN12_TJOVER12.csv")
    meta = _longo("moeda-fiscal", "selic_meta_copom_fim_de_mes_sgs432.csv")
    juro_real = _longo("moeda-fiscal", "juro_real_ex_post_anual_ipca.csv")
    prim_rtn = _longo("moeda-fiscal", "rtn_gc_caixa_resultado_primario_acima_da_linha_pct_pib.csv")
    nfsp = _longo(
        "moeda-fiscal", "nfsp_primario_setor_publico_consolidado_anual_pct_pib_sgs5793.csv"
    )
    prim_nfsp = {a: -v for a, v in nfsp.items()}
    discr = _longo("moeda-fiscal", "rtn_gc_caixa_despesa_discricionarias_pct_pib.csv")
    # externo-fase3 (2026-10-23): external debt and the carrying cost of public debt, BCB SGS series
    # named by the BCB's explanatory note of 24/02/2026; quarterly series keyed by quarter-end month.
    ext = {
        c: _longo("externo-fase3", f"{nome}_sgs{c}.csv")
        for c, nome in {
            3684: "divida_externa_bruta_restrita_usd_mi",
            25563: "divida_externa_bruta_bpm6_usd_mi",
            21521: "divida_externa_setor_publico_restrita_usd_mi",
            11407: "divida_externa_restrita_pib_pct",
            11409: "divida_externa_liquida_pib_pct",
            11408: "divida_externa_setor_publico_pct",
            12506: "pii_liquida_pib_pct",
            5760: "nfsp_juros_nominais_12m_pib_pct",
            5727: "nfsp_resultado_nominal_12m_pib_pct",
        }.items()
    }
    reservas_mensal = _longo("bcb-fase2", "reservas_internacionais_caixa_usd_mi_sgs3546.csv")
    pib_nominal = _longo_ind(
        "mecanismos-contabil", "rtn-resultado-primario-extraordinarias.csv", "pib_nominal_rs_mi"
    )
    NOTA_DESC = "série descontinuada pelo BCB em fev/2026 (Nota Explicativa de 24/02/2026); mostrada como publicada, sem prolongamento"
    pq = {
        k: _porquinho(k)
        for k in (
            "caixa_real_ipca",
            "caixa_real_igpdi",
            "poupanca_real_ipca",
            "selic_real_ipca",
            "usd_poder_compra_ref",
            "chf_poder_compra_ref",
            "sdr_poder_compra_ref",
            "ouro_oncas",
            "caixa_em_salarios_minimos",
            "caixa_em_cestas_dieese_sp",
        )
    }
    {
        k: _produto_horas(k)
        for k in (
            "arroz",
            "feijao",
            "carne_bovina",
            "pao_frances",
            "leite",
            "botijao_glp_13kg",
            "gasolina_comum",
            "energia_residencial",
            "onibus_sp_tarifa_basica",
        )
    }
    te = "tributos-estado"
    ctb_ipea = _longo_ind(
        te,
        "ipea-td583-carga-tributaria-1947-1996.csv",
        "ipea_td583_carga_tributaria_global_pct_pib",
    )
    ctb_rfb24 = _longo_ind(
        te, "receita-ctb-total-por-edicao.csv", "receita_ctb_total_pct_pib__edicao_2024"
    )
    ctb_rfb20 = _longo_ind(
        te, "receita-ctb-total-por-edicao.csv", "receita_ctb_total_pct_pib__edicao_2020"
    )
    ctb_stn = _longo_ind(
        te, "tesouro-ctb-governo-geral-por-boletim.csv", "tesouro_ctb_geral_pct_pib__boletim_2025"
    )
    cargos_mil = _longo_ind(
        te, "pep-cargos-comissionados.csv", "pep_cargos_das_fcpe_cce_fce_por_mil_ativos"
    )
    cargos_sv = _longo_ind(
        te, "pep-cargos-comissionados.csv", "pep_cargos_das_fcpe_cce_fce_sem_cargo_efetivo_pct"
    )
    est = {
        k: {a: -v for a, v in _longo_ind(te, "nfsp-estatais-bcb.csv", k).items()}
        for k in (
            "nfsp_primario_empresas_estatais_pct_pib",
            "nfsp_primario_empresas_estatais_federais_pct_pib",
            "nfsp_primario_empresas_estatais_estaduais_pct_pib",
        )
    }
    pnadc = {}
    for r in obs:
        if r["indicador"] == "taxa_de_desocupacao" and "-T" in r["periodo"]:
            a, t = r["periodo"].split("-T")
            pnadc[f"{a}-{int(t) * 3:02d}"] = float(r["valor"])  # keyed by the quarter's last month

    def ind(
        id_,
        nome,
        un,
        pol,
        freq,
        candles=None,
        linhas=(),
        escala="linear",
        nota="",
        base="",
        sobe="",
        faixa=None,
        forma="linha",
        quebras_proprias=(),
        explica=None,
    ):
        """Assemble one indicator entry (lines, candles, breaks, per-term cells, one sentence)."""
        qs = list(quebras_proprias)
        for q in quebras:
            if not any(k in q["indicador"] for k in QUEBRAS.get(id_, [])):
                continue
            m = re.search(r"(19|20)\d\d", q["data_quebra"])
            if m:
                qs.append(
                    {
                        "ano": m.group(0),
                        "tipo": q["tipo_de_quebra"],
                        "razao": q["razao_declarada_pela_fonte"][:200],
                        "efeito": q["efeito_medido"][:120],
                    }
                )
        linhas_out = [{"rotulo": r, "pontos": _pontos(d)} for r, d in linhas]
        return {
            "id": id_,
            "nome": nome,
            "un": un,
            "pol": pol,
            "freq": freq,
            "escala": escala,
            "forma": forma,
            "nota": nota,
            "base_candle": base,
            "sobe": sobe,
            "candles": candles or [],
            "linhas": linhas_out,
            "faixa": {"rotulo": faixa[0], "pontos": _pontos(faixa[1])} if faixa else None,
            "eventos": [e["t"] for e in eventos if "*" in e["em"] or id_ in e["em"]],
            "quebras": qs,
            "explica": explica or EXPLICA.get(id_) or {},
            "mandatos": mandatos(linhas_out, [PRE_REAL, *govs], freq),
            "frase": frase(nome, un, linhas_out[0], freq) if linhas_out else "",
        }

    govs = [
        {
            "id": g["id"],
            "nome": g["nome"],
            "curto": CURTO[g["id"]],
            "posse": g["posse"].isoformat(),
            "saida": g["saida"].isoformat(),
            "corrente": "data de referencia" in g["fonte"],
        }
        for g in carregar()
        if g["id"] in CURTO
    ]
    saida = [
        ind(
            "carga",
            "Carga tributária bruta",
            "% do PIB (bases separadas, nunca emendadas)",
            "neutro",
            "anual",
            None,
            [
                ("Receita Federal, edição 2024 (série 2002-2024, sem FGTS e Sistema S)", ctb_rfb24),
                ("Receita Federal, edição 2020 (série 2002-2020, definição anterior)", ctb_rfb20),
                (
                    "Tesouro Nacional, governo geral, GFSM 2014 (boletim 2025, rótulos de 1 casa)",
                    ctb_stn,
                ),
                ("Ipea TD 583 (Varsano et al. 1998), 1947-1996, literatura", ctb_ipea),
            ],
            nota="cada edição da Receita muda a definição e o PIB: o mesmo ano muda entre vintages (2023 = 32,11 na edição 2023 e 30,22 na 2024); lacuna 1997-2001 na compilação longa",
        ),
        ind(
            "ministerios",
            "Ministérios em 1º de janeiro",
            "contagem na norma vigente em 1º de janeiro",
            "neutro",
            "anual",
            None,
            forma="pontos",
            linhas=[
                ("Órgãos que a norma chama de Ministério", _ministerios("n_ministerios")),
                (
                    "Mais os cargos com status de ministro (classe C)",
                    _ministerios("n_ministerios_mais_status"),
                ),
            ],
            nota="contagem pela lei ou medida provisória de organização da Presidência vigente em 1º de janeiro (Planalto); as mudanças do ano anterior estão em quebras.csv da coleta",
        ),
        ind(
            "cargos",
            "Cargos em comissão e funções de confiança",
            "DAS, FCPE, CCE e FCE por mil servidores ativos do Executivo civil (dezembro)",
            "neutro",
            "anual",
            None,
            [
                (
                    "Painel Estatístico de Pessoal, 1999-2020 (DAS e FCPE)",
                    _corte(cargos_mil, CARGOS_CORTE),
                ),
                (
                    "Painel Estatístico de Pessoal, 2021-2025 (DAS, FCPE, CCE e FCE)",
                    _corte(cargos_mil, CARGOS_CORTE, False),
                ),
            ],
            nota="transcrito do painel Qlik do PEP (a API pede chave). A contagem cai 74% entre dez/2020 e dez/2021 (22.542 -> 5.789) sem causa no changelog do painel; a Lei 14.204/2021 (CCE/FCE) é candidata, mas a fonte não explica a lacuna: duas bases, nunca uma linha",
        ),
        ind(
            "cargos_sem_vinculo",
            "Cargos em comissão ocupados por quem não é servidor",
            "% das ocupações de DAS, FCPE, CCE e FCE sem cargo efetivo (dezembro)",
            "neutro",
            "anual",
            None,
            [
                ("Painel Estatístico de Pessoal, 1999-2020", _corte(cargos_sv, CARGOS_CORTE)),
                (
                    "Painel Estatístico de Pessoal, 2021-2025",
                    _corte(cargos_sv, CARGOS_CORTE, False),
                ),
            ],
            nota="mesma fonte e mesma quebra de 2021 do indicador anterior: duas bases",
        ),
        ind(
            "estatais",
            "Resultado primário das empresas estatais",
            "% do PIB (positivo = superávit; sinal do BCB invertido)",
            "mais",
            "anual",
            None,
            [
                (
                    "Todas as estatais (BCB NFSP, 2002+)",
                    est["nfsp_primario_empresas_estatais_pct_pib"],
                ),
                ("Federais", est["nfsp_primario_empresas_estatais_federais_pct_pib"]),
                ("Estaduais (1998+)", est["nfsp_primario_empresas_estatais_estaduais_pct_pib"]),
            ],
            nota="Petrobras sai do perímetro em mai/2009 e Eletrobras em nov/2010 (documentado no CKAN do BCB): a série federal muda de perímetro ali; o lucro por empresa está nos cinco gráficos seguintes, uma linha por norma contábil",
        ),
        ind(
            "carga_base",
            "Carga tributária por base de incidência",
            "% do PIB (edição 2024 da Receita Federal)",
            "neutro",
            "anual",
            None,
            [
                (
                    rotulo,
                    _longo_ind("tributos-estado", CTB_BASE, f"receita_ctb_base_{cod}__edicao_2024"),
                )
                for cod, rotulo in CTB_BASES
            ],
            nota="tabela INC02B da edição 2024 de 'Carga Tributária no Brasil', 2002-2024; cada edição revisa os anos anteriores (quebras.csv da coleta); os seis agregados somam o total mostrado em 'Carga tributária bruta'",
        ),
        *[
            ind(
                f"lucro_{chave}",
                f"Lucro líquido: {nome}",
                "R$ milhões correntes (moeda e norma contábil da demonstração)",
                "neutro",
                "anual",
                None,
                _lucro(arquivo),
                nota="uma linha por norma contábil e perímetro (consolidado ou controladora; BR GAAP, IFRS ou US GAAP em reais), lidas nas demonstrações da própria empresa e nunca emendadas; valores nominais, sem deflação; linhas em US$ ficam fora",
            )
            for chave, nome, arquivo in ESTATAIS
        ],
        ind(
            "emendas_pagas",
            "Emendas parlamentares pagas, por tipo",
            "R$ bilhões correntes (pago no exercício da emenda)",
            "neutro",
            "anual",
            None,
            [
                (
                    rotulo,
                    {
                        a: v / 1000
                        for a, v in _longo_ind(
                            "moeda-fiscal", EMENDAS, f"emendas_pago_exercicio__{s}"
                        ).items()
                    },
                )
                for s, rotulo in EMENDAS_TIPOS
            ],
            nota="Portal da Transparência (CGU), base completa de emendas: soma de 'Valor Pago' por ano orçamentário e tipo; o que foi pago em anos seguintes (restos a pagar) está em 'Emendas pagas / PIB'; antes de 2014 a base não existe",
        ),
        ind(
            "emendas_pib",
            "Emendas parlamentares pagas / PIB",
            "% do PIB (numerador CGU, denominador Tesouro RTN)",
            "neutro",
            "anual",
            None,
            [
                (
                    "Pago no exercício da emenda, todos os tipos",
                    {
                        a: 100 * v
                        for a, v in razao(
                            _longo_ind("moeda-fiscal", EMENDAS, "emendas_pago_exercicio__total"),
                            pib_nominal,
                        ).items()
                    },
                ),
                (
                    "Pago no exercício mais restos a pagar pagos depois (atribuídos ao ano da emenda)",
                    {
                        a: 100 * v
                        for a, v in razao(
                            {
                                k: p
                                + _longo_ind(
                                    "moeda-fiscal", EMENDAS, "emendas_rap_pagos__total"
                                ).get(k, 0.0)
                                for k, p in _longo_ind(
                                    "moeda-fiscal", EMENDAS, "emendas_pago_exercicio__total"
                                ).items()
                            },
                            pib_nominal,
                        ).items()
                    },
                ),
            ],
            nota="duas fontes declaradas: emendas da CGU sobre o PIB nominal que o Tesouro usa no RTN; o ano corrente está incompleto (pagamentos em curso)",
        ),
        ind(
            "porquinho_reais",
            "O porquinho em reais: caixa, poupança e Selic",
            "R$ de dez/1994 (poder de compra pelo IPCA; IGP-DI como linha)",
            "mais",
            "mensal",
            None,
            [
                (
                    "R$ 100 mil guardados em dinheiro, deflacionados pelo IPCA",
                    pq["caixa_real_ipca"],
                ),
                ("Os mesmos R$ 100 mil deflacionados pelo IGP-DI", pq["caixa_real_igpdi"]),
                (
                    "Na poupança (rendimento SGS 25), deflacionados pelo IPCA",
                    pq["poupanca_real_ipca"],
                ),
                ("Na Selic (SGS 4390), deflacionados pelo IPCA", pq["selic_real_ipca"]),
            ],
            escala="log",
            nota="escala de log: a caixa cai de 100.000 para 13.208, a Selic sobe para 1.131.005; o vão entre caixa e poupança é a face regressiva (quem não tem conta). Sem candle: dinheiro parado só perde",
        ),
        ind(
            "porquinho_refs",
            "O porquinho em moedas e ouro",
            "índice, dez/1994 = 100 (cada medida deflacionada pela inflação da própria referência)",
            "mais",
            "mensal",
            None,
            [
                ("Em reais, pelo IPCA", indice_100(pq["caixa_real_ipca"])),
                ("Em dólares, pelo CPI dos EUA", indice_100(pq["usd_poder_compra_ref"])),
                ("Em francos suíços, pelo CPI da Suíça", indice_100(pq["chf_poder_compra_ref"])),
                (
                    "Em DES do FMI, pelo CPI dos EUA (declarado)",
                    indice_100(pq["sdr_poder_compra_ref"]),
                ),
                ("Em onças de ouro (quantidade)", indice_100(pq["ouro_oncas"])),
            ],
            escala="log",
            nota="100 = dez/1994 em cada medida; ouro pelo Pink Sheet do Banco Mundial (a LBMA bloqueia o acesso); DES deflacionado pelo CPI dos EUA por falta de deflator próprio",
        ),
        ind(
            "porquinho_brasil",
            "O porquinho no que ele compra",
            "índice, dez/1994 = 100",
            "mais",
            "mensal",
            None,
            [
                ("Em reais, pelo IPCA", indice_100(pq["caixa_real_ipca"])),
                ("Em salários mínimos", indice_100(pq["caixa_em_salarios_minimos"])),
                ("Em cestas básicas DIEESE-SP", indice_100(pq["caixa_em_cestas_dieese_sp"])),
            ],
            escala="log",
            nota="o mesmo dinheiro medido em salários mínimos cai mais que pelo IPCA porque o mínimo subiu acima da inflação; em cestas, menos",
        ),
        ind(
            "inflacao",
            "Inflação em 12 meses",
            "% acumulado em 12 meses",
            "menos",
            "mensal",
            candles_anuais(ipca12),
            [("IPCA, IBGE", ipca12), ("INPC, IBGE", inpc12), ("IGP-DI, FGV (desde 1945)", igpdi12)],
            escala="symlog",
            base="IPCA",
            sobe="verde = a inflação de dezembro ficou acima da de dezembro anterior (acelerou); vermelho = desacelerou",
            nota="pavio = taxas em 12 meses de cada mês do ano; na vista completa, escala simétrica de log para 5.000% e 2% caberem no mesmo eixo",
        ),
        ind(
            "selic",
            "Juro básico, Selic",
            "% ao ano",
            "neutro",
            "mensal",
            candles_anuais(meta),
            [
                ("Meta do Copom, fim de mês, BCB SGS 432 (desde 1999)", meta),
                (
                    "Selic over do mês anualizada, Ipeadata PAN12 (desde 1974; oscila até 1 ponto com os dias úteis do mês)",
                    selic_aa,
                ),
            ],
            escala="symlog",
            base="meta do Copom",
            sobe="verde = a meta de dezembro ficou acima da de dezembro anterior (apertou); vermelho = afrouxou",
            faixa=(
                "Juro real no ano: Selic acumulada contra IPCA acumulado (positivo = rende acima da inflação)",
                juro_real,
            ),
            nota="candle sobre a meta do Copom (emenda 05 §7): a over mensal anualizada carrega o número de dias úteis do mês (dez/2022: 14,30% com meta de 13,75%); antes de 1999 só a linha da over, sem candle. A faixa de baixo é o juro real ex-post do ano, calculado pela coleta",
        ),
        ind(
            "emissao",
            "Emissão de moeda contra inflação",
            "% em 12 meses",
            "menos",
            "mensal",
            candles_anuais(m0_12),
            [
                ("Base monetária M0, BCB (uma base desde 1946)", m0_12),
                ("IPCA em 12 meses", ipca12),
                ("M1 conceito antigo (até 2018)", variacao_12m(m1)),
                ("M1 conceito Novo (desde 2003)", variacao_12m(m1n)),
            ],
            escala="symlog",
            base="M0",
            sobe="verde = a base monetária cresceu mais rápido que no ano anterior",
            faixa=(
                "M0 menos IPCA, em 12 meses (positivo = moeda acima dos preços)",
                diferenca(m0_12, ipca12),
            ),
            nota="as duas definições de M1 correm juntas de 2003 a 2018 e o vão é a mudança de método",
        ),
        ind(
            "multiplicador",
            "Dinheiro criado pelos bancos",
            "M3 dividido pela base monetária (vezes)",
            "neutro",
            "mensal",
            candles_anuais(razao(m3n, m0)),
            [
                ("M3 Novo / M0 (desde dez/2001)", razao(m3n, m0)),
                ("M3 regime 2001 / M0 (1988-2018)", razao(m3, m0)),
            ],
            base="M3 Novo / M0",
            sobe="verde = cada real emitido sustenta mais reais de meios de pagamento ao fim do ano",
            nota="quantos reais de meios de pagamento amplos existem para cada real emitido pelo Banco Central",
        ),
        ind(
            "moeda_pib",
            "Moeda em relação ao PIB",
            "% do PIB (média dos 12 saldos mensais sobre o PIB do ano)",
            "neutro",
            "anual",
            None,
            [
                ("M1 / PIB, conceito antigo", col_anual("M1_med12_pib_pct")),
                ("M1 / PIB, Novo", col_anual("M1_novo_med12_pib_pct")),
                ("M2 / PIB, regime 2001", col_anual("M2_2001_med12_pib_pct")),
                ("M2 / PIB, Novo", col_anual("M2_novo_med12_pib_pct")),
                ("M3 / PIB, regime 2001", col_anual("M3_2001_med12_pib_pct")),
                ("M3 / PIB, Novo", col_anual("M3_novo_med12_pib_pct")),
            ],
            nota="média dos 12 saldos mensais, não o saldo de dezembro: na hiperinflação dezembro sozinho mistura preços de meses diferentes",
        ),
        ind(
            "pib",
            "Crescimento do PIB",
            "% contra o mesmo trimestre do ano anterior",
            "mais",
            "trimestral",
            candles_anuais(pib_4t),
            [
                ("IBGE, contas trimestrais (4 trimestres)", pib_4t),
                (
                    "PIB anual, IBGE/SCN via Ipeadata (desde 1948)",
                    _anual(obs, "pib_var_real", "Ipeadata"),
                ),
            ],
            base="contas trimestrais",
            sobe="verde = o crescimento do 4º trimestre ficou acima do 4º trimestre anterior",
            nota="pavio = crescimento em 4 trimestres de cada trimestre do ano; a linha anual cobre desde 1948",
        ),
        ind(
            "salmin",
            "Salário mínimo real",
            "R$ de set/2026 (Ipea, deflator INPC)",
            "mais",
            "mensal",
            candles_anuais(salmin),
            [("Salário mínimo real, Ipea", salmin)],
            base="Ipea",
            sobe="verde = o mínimo de dezembro compra mais que o de dezembro anterior",
        ),
        ind(
            "desemprego",
            "Taxa de desemprego",
            "% da força de trabalho",
            "menos",
            "trimestral",
            candles_anuais(pnadc),
            [
                ("PNAD Contínua, Brasil (trimestral, 2012+)", pnadc),
                ("PME nova, 6 regiões metropolitanas (2002-2015)", pme_n),
                ("PME antiga, 6 regiões metropolitanas (1980-2002)", pme_a),
            ],
            base="PNAD Contínua",
            sobe="verde = mais desemprego no fim do ano que no fim do anterior",
            nota="três bases; nas sobreposições (2002; 2012-2015) as linhas correm juntas e o vão é a mudança de método",
        ),
        ind(
            "primario",
            "Resultado primário",
            "% do PIB (positivo = superávit)",
            "mais",
            "anual",
            None,
            [
                ("Governo Central, acima da linha, Tesouro RTN (desde 1997)", prim_rtn),
                ("Setor público consolidado, BCB NFSP, sinal invertido (desde 2002)", prim_nfsp),
            ],
            nota="duas medidas distintas, não emendadas: o Tesouro mede o Governo Central pelo caixa; o BCB mede todo o setor público pela dívida (NFSP positiva é déficit, aqui invertida para positivo = superávit)",
        ),
        ind(
            "discricionarias",
            "Despesas discricionárias do Governo Central",
            "% do PIB",
            "neutro",
            "anual",
            None,
            [("Tesouro RTN, linha 4.4.2, conceito de caixa (desde 2008)", discr)],
            nota="a linha de discricionárias só existe no RTN desde 2008; antes a planilha traz zero, tratado como não publicado",
        ),
        ind(
            "divida",
            "Dívida bruta do governo geral",
            "% do PIB",
            "menos",
            "anual",
            None,
            [
                ("BCB, metodologia desde 2008", _anual(obs, "divida_pib", "desde 2008")),
                ("BCB, metodologia até 2007", _anual(obs, "divida_pib", "até 2007")),
            ],
            nota="duas metodologias publicadas em paralelo; nunca emendadas",
        ),
        ind(
            "nominal",
            "Resultado nominal do setor público (12 meses)",
            "% do PIB (positivo = superávit)",
            "mais",
            "mensal",
            None,
            [
                (
                    "Setor público consolidado, BCB NFSP 12 meses, sinal invertido (desde 2002)",
                    {k: -v for k, v in ext[5727].items()},
                )
            ],
            nota="resultado primário menos juros nominais; o BCB publica NFSP positiva como déficit, aqui o sinal é invertido para positivo = superávit, como em 'Resultado primário'",
        ),
        ind(
            "juros_nominais",
            "Juros nominais da dívida pública (12 meses)",
            "% do PIB",
            "menos",
            "mensal",
            None,
            [("Setor público consolidado, BCB NFSP 12 meses (desde 2002)", ext[5760])],
            nota="o custo de carregar a dívida: juros apropriados em 12 meses sobre o PIB do mesmo período",
        ),
        ind(
            "divext",
            "Dívida externa bruta",
            "US$ milhões",
            "neutro",
            "trimestral",
            None,
            [
                (
                    "Conceito restrito ('a chamada dívida externa bruta'), BCB SGS 3684 (desde 1972)",
                    ext[3684],
                ),
                (
                    "Conceito BPM6: inclui operações intercompanhia e títulos no mercado doméstico com não residentes, BCB SGS 25563 (desde 2002)",
                    ext[25563],
                ),
                (
                    "Dívida externa do setor público, conceito restrito, BCB SGS 21521 (desde 1990)",
                    ext[21521],
                ),
            ],
            nota="duas medidas do mesmo BCB, nunca somadas nem emendadas: a restrita é a da manchete; a BPM6 é 'a dívida externa brasileira' na definição oficial. Valores nominais em dólar: não descontam inflação nem crescimento",
        ),
        ind(
            "divext_reservas",
            "Dívida externa bruta e reservas internacionais",
            "US$ milhões",
            "neutro",
            "trimestral",
            None,
            [
                (
                    "Dívida externa bruta, conceito restrito, fim de trimestre, BCB SGS 3684",
                    ext[3684],
                ),
                (
                    "Reservas internacionais, conceito caixa, fim de mês, BCB SGS 3546",
                    reservas_mensal,
                ),
            ],
            nota="o cruzamento das duas linhas em 2026 é o fato da notícia; 'dívida menos reservas' NÃO é a dívida externa líquida do BCB, que subtrai também créditos brasileiros no exterior e haveres de bancos comerciais (ver 'Dívida externa líquida / PIB')",
        ),
        ind(
            "divext_pib",
            "Dívida externa bruta / PIB",
            "% do PIB",
            "menos",
            "trimestral",
            None,
            [
                (
                    "Conceito restrito sobre o PIB de 12 meses em US$, BCB SGS 11407 (1971-2025)",
                    ext[11407],
                )
            ],
            nota=NOTA_DESC
            + "; denominador em dólares correntes: a razão também se move com o câmbio",
        ),
        ind(
            "divext_liquida_pib",
            "Dívida externa líquida / PIB",
            "% do PIB (negativo = credor externo líquido)",
            "menos",
            "trimestral",
            None,
            [
                (
                    "Conceito antigo do BCB: bruta restrita menos reservas, créditos no exterior e haveres de bancos, BCB SGS 11409 (1971-2025)",
                    ext[11409],
                )
            ],
            nota=NOTA_DESC
            + " por não aderir ao BPM6; o último valor oficial é -0,9% em set/2025; não há valor oficial de 2026 em nenhum conceito e nada foi calculado aqui",
        ),
        ind(
            "divext_publico",
            "Dívida externa do setor público / dívida externa bruta",
            "%",
            "neutro",
            "trimestral",
            None,
            [("Conceito restrito, BCB SGS 11408 (1971-2025)", ext[11408])],
            nota=NOTA_DESC
            + "; o BCB revisou a divisão público/privado de dez/2020 a set/2025 em mar/2026",
        ),
        ind(
            "pii_pib",
            "Posição de investimento internacional líquida / PIB",
            "% do PIB (negativo = passivos externos maiores que ativos)",
            "neutro",
            "trimestral",
            None,
            [
                (
                    "Ativos externos menos passivos externos, sobre o PIB de 12 meses em US$, BCB SGS 12506 (2002-2025)",
                    ext[12506],
                )
            ],
            nota=NOTA_DESC + "; inclui ações e investimento direto, não só dívida",
        ),
        ind(
            "tit",
            "Imposto inflacionário",
            "% do PIB no ano",
            "menos",
            "anual",
            None,
            forma="coluna",
            linhas=[
                (
                    "Cysne e Coimbra-Lisboa, fórmula mensal, base M1, deflator IGP-DI (desde 1947)",
                    _anual(
                        obs,
                        "senhoriagem_pib",
                        "Transferências inflacionárias totais TIT, fórmula mensal",
                    ),
                ),
                (
                    "A mesma fórmula com o IPCA (desde 1981)",
                    _anual(obs, "senhoriagem_pib", "TIT com IPCA"),
                ),
            ],
            nota="fluxo do ano em % do PIB: perda de poder de compra do dinheiro em mãos do público e dos depósitos à vista; com o IGP-DI negativo em 12 meses (2025: -1,2%) o valor fica negativo, por isso a variante com IPCA corre ao lado",
        ),
        ind(
            "pobreza",
            "Pobreza, US$ 6,85/dia (PPC 2017)",
            "% da população",
            "menos",
            "anual",
            None,
            [
                ("Banco Mundial PIP", _anual(obs, "pobreza", "PIP | US$ 6.85/dia PPC2017")),
                ("IBGE SIS 2025", _anual(obs, "pobreza", "IBGE-SIS2025 | US$ 6,85 PPC2017")),
            ],
        ),
        ind(
            "gini",
            "Desigualdade, índice de Gini",
            "0 a 1",
            "menos",
            "anual",
            None,
            [
                ("Banco Mundial PIP", _anual(obs, "gini", "PIP | renda dom")),
                ("IBGE PNAD antiga (Ipeadata)", _anual(obs, "gini", "Ipeadata-PGINI")),
                ("IBGE SIS 2025 (PNADC)", _anual(obs, "gini", "IBGE-SIS2025")),
            ],
        ),
        ind(
            "expvida",
            "Expectativa de vida ao nascer",
            "anos",
            "mais",
            "anual",
            None,
            [
                ("ONU via Banco Mundial (um vintage)", _anual(obs, "expvida", "WB-WDI")),
                ("IBGE, série vigente 2025", _anual(obs, "expvida", "IBGE-Tabuas2024")),
                ("IBGE, tábua como publicada", _anual(obs, "expvida", "Tabua-como-publicada")),
            ],
        ),
        ind(
            "homic",
            "Homicídios por 100 mil habitantes",
            "por 100 mil",
            "menos",
            "anual",
            None,
            [
                (
                    "SIM / Ipeadata (CID-9 até 1995, CID-10 desde 1996)",
                    _anual(obs, "seg_homic_taxa", ""),
                )
            ],
        ),
        ind(
            "homic_n",
            "Homicídios: número de mortes no ano",
            "pessoas mortas por agressão no ano (óbitos por residência)",
            "menos",
            "anual",
            None,
            [
                (
                    "SIM / DATASUS via Ipeadata (CID-9 até 1995, CID-10 desde 1996)",
                    _anual(obs, "seg_homic_n", "AVIOL12"),
                )
            ],
            nota="contagem absoluta; a taxa por 100 mil está no indicador ao lado; mortes de intenção indeterminada não entram",
            explica=EXPLICA.get("homic_n"),
        ),
        ind(
            "reprov",
            "Reprovação, ensino fundamental anos iniciais",
            "% dos matriculados, Brasil",
            "menos",
            "anual",
            None,
            [
                (
                    "INEP, Censo Escolar, 1997-2005: calculada das contagens, 1ª a 4ª série (fundamental de 8 anos)",
                    _corte(_anual(obs, "edu_reprovacao_ef_ai__total", "| BR"), REPROV_CORTE),
                ),
                (
                    "INEP, Censo Escolar, 2006-2025: como publicada, anos iniciais (fundamental de 9 anos)",
                    _corte(_anual(obs, "edu_reprovacao_ef_ai__total", "| BR"), REPROV_CORTE, False),
                ),
            ],
            nota="duas bases (emenda 05 §11); 2020 = 0,6% é o ano das normas excepcionais da pandemia (a norma entra no catálogo de quebras quando for lida na fonte); a proficiência do Saeb corre ao lado porque a regra de progressão não a move",
        ),
        ind(
            "saeb",
            "Saeb, matemática, 5º ano",
            "pontos",
            "mais",
            "anual",
            None,
            forma="pontos",
            linhas=[("INEP, Saeb (bienal)", _anual(obs, "edu_saeb_MT_EF_5ano_4serie", ""))],
        ),
    ]
    mediana = _renda_decil_mensal((5, 6), obs)
    ipc = "ipca-itens-fase2"
    sm_nom = _salario_minimo_nominal()
    sm_idx = {k: 100 * v / sm_nom["1999-12"] for k, v in sm_nom.items() if k >= "1999-12"}
    i_alug = _derivado_mensal(ipc, "indice_ipca_aluguel_residencial_dez1999_100.csv")
    i_plano = _derivado_mensal(ipc, "indice_ipca_plano_saude_dez1999_100.csv")
    saida.append(
        ind(
            "aluguel_saude",
            "Aluguel e plano de saúde contra o salário mínimo e o IPCA",
            "índice, dez/1999 = 100 (acima de 100 = subiu mais que a referência)",
            "menos",
            "mensal",
            candles_anuais(razao({k: 100 * v for k, v in i_plano.items()}, sm_idx)),
            [
                (
                    "Plano de saúde / salário mínimo",
                    razao({k: 100 * v for k, v in i_plano.items()}, sm_idx),
                ),
                (
                    "Aluguel residencial / salário mínimo",
                    razao({k: 100 * v for k, v in i_alug.items()}, sm_idx),
                ),
                (
                    "Plano de saúde / IPCA geral",
                    _derivado_mensal(ipc, "razao_ipca_plano_saude_sobre_geral_dez1999_100.csv"),
                ),
                (
                    "Aluguel residencial / IPCA geral",
                    _derivado_mensal(
                        ipc, "razao_ipca_aluguel_residencial_sobre_geral_dez1999_100.csv"
                    ),
                ),
            ],
            base="plano de saúde / salário mínimo",
            sobe="verde = o plano de saúde pesou mais no salário mínimo em dezembro que no dezembro anterior; vermelho = pesou menos",
            nota="subitens do IPCA (SIDRA, 5 tabelas encadeadas pela continuidade declarada pelo IBGE; sem mês de sobreposição entre tabelas) como número-índice; o salário mínimo é o nominal do mês; o plano de saúde tem 10 meses de variação zero em 2000-01 antes de o IBGE usar o reajuste da ANS",
            quebras_proprias=_quebras_ipca_itens(),
            explica=EXPLICA.get("aluguel_saude"),
        )
    )
    fontes = {
        "botijao_glp_13kg": "ANP, 2001+",
        "gasolina_comum": "ANP, 2001+",
        "energia_residencial": "Eletrobras/ANEEL, tarifa média, 1994+",
        "onibus_sp_tarifa_basica": "Prefeitura de São Paulo, 1994+",
    }
    for pid, nome in PRODUTOS.items():
        h = _produto_horas(pid)
        if pid == "energia_residencial":
            h = {k: 100 * v for k, v in h.items()}
        d10 = _produto_anual(pid)
        preco = _preco_medio_anual(pid)
        med = {a: preco[a] / mediana[a] * 220 for a in preco if a in mediana and mediana[a]}
        if pid == "energia_residencial":
            d10 = {k: 100 * v for k, v in d10.items()}
            med = {k: 100 * v for k, v in med.items()}
        fonte = fontes.get(pid, "DIEESE, preço médio de São Paulo, 1959+")
        saida.append(
            ind(
                f"prod_{pid}",
                nome[0].upper() + nome[1:] + " em horas de trabalho",
                "horas de trabalho ao salário mínimo (220 h/mês)",
                "menos",
                "mensal",
                candles_anuais(h),
                [
                    ("Horas ao salário mínimo", h),
                    ("Horas à renda per capita mediana (média dos decis 5 e 6, PIP, anual)", med),
                    ("Horas à renda per capita do décimo mais rico (PIP, anual)", d10),
                ],
                base="salário mínimo",
                sobe=f"verde = {nome} custou mais horas de trabalho em dezembro que no dezembro anterior; vermelho = menos",
                nota=f"preço médio do mês ({fonte}) dividido pelo salário mínimo nominal do mês e multiplicado por 220; até abr/1984 o mínimo é o maior regional",
                quebras_proprias=_quebras_produtos([pid.split("_")[0]]),
                explica=explica_produto(pid, fonte),
            )
        )
    pop = "populacao-fase2"

    def P(nome, indicador, ate=2025):
        """Annual rows of one population indicator, dropping the incomplete current year."""
        return {a: v for a, v in _longo_ind(pop, nome, indicador).items() if a <= ate}

    saida.append(
        ind(
            "nascimentos",
            "Nascimentos por ano",
            "pessoas nascidas vivas no ano",
            "neutro",
            "anual",
            None,
            [
                (
                    "SINASC, nascidos vivos por ocorrência (DATASUS, 1994+; 2025 preliminar)",
                    P("datasus_sinasc_nascidos.csv", "nascidos_vivos_por_ocorrencia"),
                ),
                (
                    "IBGE Registro Civil, nascidos ocorridos no ano (1984+)",
                    P("ibge_registro_civil.csv", "nascidos_vivos_ocorridos_no_ano"),
                ),
                (
                    "IBGE Registro Civil, nascidos registrados no ano (1984+)",
                    P("ibge_registro_civil.csv", "nascidos_vivos_registrados_no_ano"),
                ),
                (
                    "ONU WPP 2024, estimativa (1950+; projeção a partir de 2024)",
                    P("onu_wpp2024.csv", "nascimentos_wpp"),
                ),
            ],
            nota="2026 fica fora (prévia incompleta); registrados no ano incluem nascidos em anos anteriores (sub-registro recuperado); salto de +8,9% entre 2002 e 2003 nos 'ocorridos' do IBGE por troca de tabela",
            explica=EXPLICA.get("nascimentos"),
        )
    )
    saida.append(
        ind(
            "obitos",
            "Óbitos por ano, todas as causas",
            "pessoas mortas no ano",
            "neutro",
            "anual",
            None,
            [
                (
                    "SIM, óbitos por ocorrência, CID-10 (DATASUS, 1996+; 2025 preliminar)",
                    {
                        a: v
                        for a, v in P(
                            "datasus_sim_obitos.csv", "obitos_total_por_ocorrencia"
                        ).items()
                        if a >= 1996
                    },
                ),
                (
                    "SIM, óbitos por ocorrência, CID-9 (1979-1995)",
                    {
                        a: v
                        for a, v in P(
                            "datasus_sim_obitos.csv", "obitos_total_por_ocorrencia"
                        ).items()
                        if a < 1996
                    },
                ),
                (
                    "IBGE Registro Civil, óbitos ocorridos no ano (2003+)",
                    P("ibge_registro_civil.csv", "obitos_ocorridos_no_ano"),
                ),
                (
                    "IBGE Registro Civil, óbitos registrados no ano (1984+)",
                    P("ibge_registro_civil.csv", "obitos_registrados_no_ano"),
                ),
                (
                    "ONU WPP 2024, estimativa (1950+; projeção a partir de 2024)",
                    P("onu_wpp2024.csv", "obitos_wpp"),
                ),
            ],
            nota="2026 fica fora (prévia incompleta); em 1980-2000 o SIM registra 72% a 87% dos óbitos estimados pela ONU (sub-registro); 2021 é o pico da pandemia",
            explica=EXPLICA.get("obitos"),
        )
    )
    saida.append(
        ind(
            "plano_saude",
            "Plano de saúde: reajuste anual, individual contra coletivo",
            "% ao ano (reajuste aplicado no ano)",
            "menos",
            "anual",
            None,
            [
                (
                    "Teto da ANS para planos individuais (ciclo de maio)",
                    _tabela_ans("ans_teto_individual_ciclo_maio_ano_pct"),
                ),
                (
                    "IPCA, subitem plano de saúde (dez/dez)",
                    _tabela_ans("ipca_plano_saude_dez_dez_pct"),
                ),
                (
                    "Coletivos médico-hospitalares, média ponderada por beneficiários (ANS, 2005+)",
                    _tabela_ans("rpc_med_media_pond_benef_pct"),
                ),
                (
                    "Coletivos com menos de 30 vidas, média ponderada (ANS, 2013+)",
                    _tabela_ans("rpc_med_agrup_lt30_media_pond_benef_pct"),
                ),
                ("IPCA geral (dez/dez)", _tabela_ans("ipca_geral_dez_dez_pct")),
            ],
            nota="o IBGE acompanha só contratos individuais e familiares e usa o reajuste fixado pela ANS, diluído em 12 meses (Métodos de cálculo, 7ª ed., 2013, p. 35); os coletivos vêm dos comunicados de reajuste das operadoras à ANS (6,2 GB brutos; só o hash no repositório), incluindo contratos sem reajuste; dez/2014-dez/2024 compostos: teto 132%, IPCA plano 135%, coletivos 217%, menos de 30 vidas 301%, IPCA geral 75%",
            explica=EXPLICA.get("plano_saude"),
        )
    )

    # Phase-2 index items without a chart of their own: every declared base as its own line, raw
    # values (the index chains them; the chart never does). ``homicidios`` is the ``homic`` series.
    from govfc import indice as _indice  # local import: ``indice`` imports this module

    ja = {s["id"] for s in saida}
    for id_, _area, nome, direcao, _camada, _modo, bases in _indice._itens(
        _indice._lido("observations.csv")
    ):
        if id_ in ja or id_ == "homicidios":
            continue
        # newest base first: it is the main line (sentence and term cells), as everywhere else
        linhas = [(rotulo, {a: v for a, v in d.items() if a >= 1950}) for rotulo, d in bases if d][
            ::-1
        ]
        saida.append(
            ind(
                id_,
                nome,
                UN_ITENS[id_],
                "mais" if direcao == "maior" else "menos",
                "anual",
                linhas=linhas,
                nota="item do índice composto: a nota de 0 a 100 usa a série encadeada pela sobreposição medida; aqui cada base é a sua própria linha",
            )
        )

    # Brazil against the pre-registered references (amendment 01 §A), one source per indicator.
    mundo = json.loads((RAIZ / "output" / "mundo.json").read_text(encoding="utf-8"))
    for m in mundo["indicadores"]:
        refs = {r["codigo"]: r for r in m["referencias"] if r["pontos"]}
        grupos = [c for c in MUNDO_REFS[:3] if c in refs]
        escolhidos = grupos or [c for c in MUNDO_REFS[3:] if c in refs][:4]
        linhas = [("Brasil", {a: v for a, v in m["bra"] if a >= 1950})] + [
            (refs[c]["nome"], {a: v for a, v in refs[c]["pontos"] if a >= 1950}) for c in escolhidos
        ]
        saida.append(
            ind(
                m["id"],
                m["nome"],
                m["un"],
                m["pol"],
                "anual",
                linhas=linhas,
                nota="Brasil e referências da MESMA série da mesma fonte (Banco Mundial WDI/PIP, UNODC, OMS/UNICEF, V-Dem via OWID); a leitura é a diferença Brasil menos referência",
                explica=explica_mundo(m["nome"], [refs[c]["nome"] for c in escolhidos]),
            )
        )
    return {
        "schema": 8,
        "definicoes": __doc__,
        "governos": govs,
        "agregados": [PRE_REAL],
        "colunas": COLUNAS,
        "eventos": [{k: e[k] for k in ("t", "rotulo", "fonte")} for e in eventos],
        "eventos_nota": "marcos.csv da coleta moeda-fiscal (uma data por acontecimento, com a fonte primária)",
        "atos": _atos(),
        "dominios": [{"nome": n, "ids": ids} for n, ids in DOMINIOS],
        "indicadores": saida,
    }


def gravar():
    """Write ``output/terminal.json``; return the number of indicators."""
    d = construir()
    (RAIZ / "output").mkdir(exist_ok=True)
    (RAIZ / "output" / "terminal.json").write_text(
        json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    return len(d["indicadores"])


if __name__ == "__main__":
    print(f"indicators: {gravar()}")
