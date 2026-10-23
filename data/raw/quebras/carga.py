# Carga dos dados brutos (so leitura, sem rede). Importado por calc.py.
# Rode os scripts com: python3 -I calc.py   (a partir desta pasta)
import csv
import json
import pathlib

H = pathlib.Path(__file__).resolve().parent          # .../dados/quebras
D = H.parent                                          # .../dados
ER = D / "economia-real"
SO = D / "social"
IN = D / "inflacao"
MO = D / "monetario"


def ipea(code, base=ER, nivel=None):
    """Ipeadata ValoresSerie -> {(ano, mes): valor}. Anual: mes=1."""
    arq = base / f"ipeadata-{code}-raw.json"
    r = {}
    for x in json.load(open(arq))["value"]:
        if nivel is not None and x["NIVNOME"] != nivel:
            continue
        if x["VALVALOR"] is None:
            continue
        r[(int(x["VALDATA"][:4]), int(x["VALDATA"][5:7]))] = float(x["VALVALOR"])
    return r


def ipea_a(code, base=ER, nivel=None):
    return {k[0]: v for k, v in ipea(code, base, nivel).items()}


def sgs(arq):
    """SGS BCB -> {(ano, mes): valor}."""
    return {(int(r["data"][-4:]), int(r["data"][3:5])): float(r["valor"]) for r in json.load(open(arq)) if r["valor"] not in ("", None)}


def media_anual(mensal, min_meses=12):
    por = {}
    for (a, m), v in mensal.items():
        por.setdefault(a, []).append(v)
    return {a: sum(v) / len(v) for a, v in por.items() if len(v) >= min_meses}


def acum_anual(mensal_pct, min_meses=12):
    """Variacao acumulada no ano (%) a partir de variacoes mensais (%)."""
    por = {}
    for (a, m), v in mensal_pct.items():
        por.setdefault(a, {})[m] = v
    r = {}
    for a, d in por.items():
        if len(d) >= min_meses:
            p = 1.0
            for v in d.values():
                p *= 1 + v / 100
            r[a] = (p - 1) * 100
    return r


def serie_csv(arq, fonte, linha):
    """social/series/*.csv -> {ano: valor} para (fonte, definicao_linha)."""
    r = {}
    for x in csv.DictReader(open(arq)):
        if x["fonte"] == fonte and x["definicao_linha"] == linha:
            r[int(x["ano"])] = float(x["valor"])
    return r


def sidra_serie(arq, var_id=None, classif=None):
    """SIDRA agregados JSON -> {periodo(str): float} da primeira serie."""
    d = json.load(open(arq))
    for v in d:
        if var_id is None or v["id"] == str(var_id):
            for r in v["resultados"]:
                if classif is None or any(c["categoria"].get(str(classif)) for c in r["classificacoes"]):
                    s = r["series"][0]["serie"]
                    return {k: float(x) for k, x in s.items() if x not in ("-", "...", "")}
    raise KeyError(arq)


def pip(arq):
    """PIP JSON -> {ano: registro}."""
    return {r["reporting_year"]: r for r in json.load(open(arq))}


def wdi(arq):
    d = json.load(open(arq))[1]
    return {int(x["date"]): x["value"] for x in d if x["value"] is not None}
