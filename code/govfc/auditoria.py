"""Window audit: whether the end-to-end direction of each series hides the opposite direction in the last 10 or 20 years.

For every series of the terminal (on its declared main base) and every scored item of the composite
index, the audit takes the value at four dates (start of the post-Real window, 20 years ago, 10 years
ago, start of the current term) and the latest value, computes the change in each window, reads it
with the series' declared polarity, and raises a flag whenever the whole-period reading and a recent
window disagree. For the products in hours of work it does the same on three yardsticks (minimum wage,
median per-capita income, top-decile income), because the yardstick itself can manufacture an
improvement. Nothing is estimated: a window without a published value at both ends is "sem dado".
"""

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
JANELAS = [("inicio", 1995), ("20 anos", 2004), ("10 anos", 2014), ("mandato", 2022)]
ESTAVEL = 0.01  # relative change below this (of the start value) reads as stable
POL = {"mais": "mais", "menos": "menos", "maior": "mais", "menor": "menos"}


def leitura(delta, pol, base):
    """Read a change with the declared polarity: ``melhorou``, ``piorou``, ``estavel`` or ``neutro``."""
    pol = POL.get(pol)
    if pol is None:
        return "neutro"
    limite = ESTAVEL * abs(base) if base else ESTAVEL
    if abs(delta) <= limite:
        return "estavel"
    return "melhorou" if (delta > 0) == (pol == "mais") else "piorou"


def _por_ano(pontos):
    """``[[t, v], ...]`` -> ``{year: last value of the year}``."""
    out = {}
    for t, v in pontos:
        out[int(t[:4])] = v
    return out


def _janelas(serie, pol):
    """Compute the windows of one ``{year: value}`` series."""
    anos = sorted(serie)
    if not anos:
        return None
    fim = anos[-1]
    out = {"ultimo_ano": fim, "ultimo": serie[fim], "janelas": {}}
    for nome, y in JANELAS:
        y_ok = next(
            (a for a in anos if a >= y and a < fim), None
        )  # first available year at or after the window start
        if y_ok is None or y_ok >= fim:
            out["janelas"][nome] = None
            continue
        d = serie[fim] - serie[y_ok]
        out["janelas"][nome] = {
            "de": y_ok,
            "valor_inicial": serie[y_ok],
            "variacao": d,
            "leitura": leitura(d, pol, serie[y_ok]),
        }
    longa = out["janelas"].get("20 anos") or out["janelas"].get("inicio")
    dec = out["janelas"].get("10 anos")
    mand = out["janelas"].get("mandato")
    out["bandeira"] = ""
    if longa and dec and longa["leitura"] == "melhorou" and dec["leitura"] == "piorou":
        out["bandeira"] = "melhora de ponta a ponta esconde piora nos últimos 10 anos"
    elif longa and mand and longa["leitura"] == "melhorou" and mand["leitura"] == "piorou":
        out["bandeira"] = "melhora de ponta a ponta esconde piora no mandato corrente"
    elif longa and dec and longa["leitura"] == "piorou" and dec["leitura"] == "melhorou":
        out["bandeira"] = "piora de ponta a ponta esconde melhora nos últimos 10 anos"
    return out


def construir():
    """Audit every terminal series and every index item; return the table and its summary."""
    T = json.loads((RAIZ / "output" / "terminal.json").read_text(encoding="utf-8"))
    IDX = json.loads((RAIZ / "output" / "indice.json").read_text(encoding="utf-8"))
    linhas = []
    for i in T["indicadores"]:
        if i["id"].startswith("prod_"):
            for ln in i["linhas"]:
                r = _janelas(_por_ano(ln["pontos"]), i["pol"])
                if r:
                    linhas.append(
                        {
                            "grupo": "produto",
                            "id": i["id"],
                            "nome": i["nome"],
                            "regua": ln["rotulo"],
                            "pol": i["pol"],
                            "un": i["un"],
                            **r,
                        }
                    )
            continue
        if i["candles"]:
            serie = {int(c["t"][:4]): c["c"] for c in i["candles"]}
            r = _janelas(serie, i["pol"])
            if r:
                base = "candle: " + (i.get("base_candle") or i["linhas"][0]["rotulo"])
                linhas.append(
                    {
                        "grupo": "indicador",
                        "id": i["id"],
                        "nome": i["nome"],
                        "regua": base,
                        "pol": i["pol"],
                        "un": i["un"],
                        **r,
                    }
                )
        else:  # one row per base: a series with two bases is never read across the break
            for ln in i["linhas"]:
                r = _janelas(_por_ano(ln["pontos"]), i["pol"])
                if r:
                    linhas.append(
                        {
                            "grupo": "indicador",
                            "id": i["id"],
                            "nome": i["nome"],
                            "regua": ln["rotulo"],
                            "pol": i["pol"],
                            "un": i["un"],
                            **r,
                        }
                    )
    for it in IDX["itens"]:
        serie = {int(a): v for a, v in it["valores"].items()}
        r = _janelas(serie, it["direcao"])
        if r:
            linhas.append(
                {
                    "grupo": "item do índice",
                    "id": it["id"],
                    "nome": it["nome"],
                    "regua": it["bases"][-1],
                    "pol": it["direcao"],
                    "un": "",
                    **r,
                }
            )
    for k, V in IDX["versoes"].items():
        serie = {int(a): v for a, v in V["serie"].items()}
        r = _janelas(serie, "mais")
        if r:
            linhas.append(
                {
                    "grupo": "índice",
                    "id": "idx:" + k,
                    "nome": f"Índice composto · {k}",
                    "regua": "índice anual (dezembro)",
                    "pol": "mais",
                    "un": "0 a 100",
                    **r,
                }
            )
    resumo = {}
    for nome, _ in JANELAS:
        c = {"melhorou": 0, "piorou": 0, "estavel": 0, "neutro": 0, "sem_dado": 0}
        for ln in linhas:
            if ln["grupo"] != "indicador" or ln["ultimo_ano"] < 2020:
                continue  # the summary counts only bases that reach the present
            j = ln["janelas"].get(nome)
            c["sem_dado" if j is None else j["leitura"]] += 1
        resumo[nome] = c
    return {
        "schema": 1,
        "definicoes": __doc__,
        "janelas": [{"nome": n, "de": y} for n, y in JANELAS],
        "limiar_estavel": ESTAVEL,
        "linhas": linhas,
        "bandeiras": [ln for ln in linhas if ln["bandeira"]],
        "resumo_indicadores": resumo,
    }


def gravar():
    """Write ``output/auditoria.json``; return the number of flagged rows."""
    d = construir()
    (RAIZ / "output" / "auditoria.json").write_text(
        json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    return len(d["bandeiras"])


if __name__ == "__main__":
    print(f"flags: {gravar()}")
