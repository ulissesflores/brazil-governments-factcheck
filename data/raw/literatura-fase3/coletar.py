#!/usr/bin/env python3
"""Coleta ``literatura-fase3``: executa, por código, o protocolo da EMENDA-07 §B (rodada 07) e da EMENDA-08 §B (rodada 08).

Uso: ``PYTHONPATH=<repo>/code python3 coletar.py --emenda 08 [--so-derivar]``. Sem ``--so-derivar``, faz as
consultas ao OpenAlex e ao Crossref pela cadeia de hash (``govfc.chain.baixar``); com a flag, só re-deriva
``series/`` a partir do ``bruto/`` já hasheado (reprodutibilidade = do bruto, nunca de nova consulta).
Rodada 07: ``openalex-`` -> ``series/emenda07/``; 08: ``openalex8-`` -> ``series/emenda08/``; 09: ``openalex9-`` -> ``series/``; 10 (EMENDA-10): mesmo bruto da 09 + episodios 21-23 -> ``series/emenda10/``.
"""

import argparse
import csv
import json
import re
import time
from pathlib import Path
from urllib.parse import quote

from govfc.chain import baixar

AQUI = Path(__file__).resolve().parent
BRUTO = AQUI / "bruto"
SJR = AQUI.parent / "referencias-fase2" / "bruto" / "scimago-journalrank-wayback-20251026.csv"
SJR_EDICAO = "2024"

# EMENDA-07 §B2: número, episódio, mandatos, consulta em inglês, consulta em português
EPISODIOS = [
    ("01", "Plano Real e estabilização", ["fhc"], "Plano Real stabilization Brazil inflation effect", "Plano Real estabilização inflação efeito"),
    ("02", "Metas de inflação e câmbio flutuante (1999)", ["fhc"], "Brazil inflation targeting floating exchange rate effect", "metas de inflação câmbio flutuante Brasil efeito"),
    ("03", "Lei de Responsabilidade Fiscal (2000)", ["fhc"], "Brazil Fiscal Responsibility Law effect municipalities", "Lei de Responsabilidade Fiscal efeito municípios"),
    ("04", "Bolsa Escola e Bolsa Família (2001-)", ["fhc", "lula12", "dilma"], "Bolsa Familia impact evaluation Brazil", "Bolsa Família avaliação de impacto"),
    ("05", "Valorização do salário mínimo (2005-)", ["lula12", "dilma"], "Brazil minimum wage increase inequality employment effect", "salário mínimo Brasil desigualdade emprego efeito"),
    ("06", "Boom de commodities e crescimento 2003-11", ["lula12"], "Brazil commodity boom growth terms of trade", "boom de commodities Brasil crescimento termos de troca"),
    ("07", "Crise de 2008 e resposta", ["lula12"], "Brazil 2008 financial crisis response credit public banks", "crise de 2008 Brasil bancos públicos crédito resposta"),
    ("08", "Minha Casa Minha Vida (2009-)", ["lula12", "dilma"], "Minha Casa Minha Vida housing program impact", "Minha Casa Minha Vida impacto"),
    ("09", "BNDES subsidiado e conteúdo local (2008-14)", ["lula12", "dilma"], "BNDES subsidized credit firms effect Brazil", "BNDES crédito subsidiado efeito empresas"),
    ("10", "Desonerações e nova matriz econômica (2011-14)", ["dilma"], "Brazil payroll tax exemption employment effect", "desoneração da folha emprego efeito Brasil"),
    ("11", "Recessão de 2014-16 e suas causas", ["dilma", "temer"], "Brazil 2014 2016 recession causes", "recessão brasileira 2014 2016 causas"),
    ("12", "Lava Jato e efeitos econômicos (2014-18)", ["dilma", "temer"], "Lava Jato corruption investigation economic effects Brazil", "Lava Jato efeitos econômicos"),
    ("13", "Teto de gastos (2016)", ["temer", "bolsonaro"], "Brazil spending cap constitutional amendment 95 effect", "teto de gastos emenda constitucional 95 efeito"),
    ("14", "Reforma trabalhista (2017)", ["temer", "bolsonaro"], "Brazil 2017 labor reform effect employment", "reforma trabalhista 2017 efeito emprego"),
    ("15", "Reforma da Previdência (2019)", ["bolsonaro"], "Brazil 2019 pension reform effect", "reforma da previdência 2019 efeito"),
    ("16", "Pandemia, Auxílio Emergencial e vacinação (2020-21)", ["bolsonaro"], "Brazil Auxilio Emergencial cash transfer pandemic effect", "Auxílio Emergencial pandemia efeito"),
    ("17", "Desmatamento e fiscalização (2004-24)", ["lula12", "dilma", "temer", "bolsonaro", "lula3"], "Amazon deforestation enforcement policy effect Brazil", "desmatamento Amazônia fiscalização política efeito"),
    ("18", "Pix e autonomia do Banco Central (2020-21)", ["bolsonaro"], "Pix instant payments Brazil effect", "Pix pagamentos instantâneos efeito"),
    ("19", "Arcabouço fiscal (2023)", ["lula3"], "Brazil 2023 fiscal framework effect", "arcabouço fiscal 2023 efeito"),
    ("20", "Bolsa Família 2023 e transferências recentes", ["lula3"], "Brazil cash transfer 2023 Bolsa Familia effect", "Bolsa Família 2023 efeito"),
]

# EMENDA-07 §B3 d: desenhos (limite de palavra, sem distinguir maiúsculas); siglas como escritas
DESENHOS_07 = [
    "difference-in-differences", "differences-in-differences", "diff-in-diff", "regression discontinuity",
    "instrumental variable", "instrumental variables", "synthetic control", "randomized", "randomised",
    "natural experiment", "event study", "event-study", "fixed effects", "fixed-effects", "panel data",
    "propensity score", "matching estimator", "structural model", "general equilibrium", "calibrated",
    "calibration", "vector autoregress", "diferenças em diferenças", "diferenças-em-diferenças",
    "descontinuidade", "variável instrumental", "variáveis instrumentais", "controle sintético",
    "experimento natural", "efeitos fixos", "dados em painel", "escore de propensão", "equilíbrio geral",
]
SIGLAS_07 = ["DSGE", "VAR model"]
# EMENDA-08 §B3: acréscimos
DESENHOS_08 = DESENHOS_07 + [
    "difference in differences", "differences in differences", "triple differences", "two-way fixed effects",
    "quasi-experimental", "quasi-experiment", "counterfactual", "causal effect", "causal effects",
    "regression kink", "bunching", "quase-experimental", "contrafactual", "efeito causal", "efeitos causais",
]
SIGLAS_08 = ["DiD", "RDD", "RCT", "IV", "DSGE", "VAR model"]
RE_BRASIL = re.compile(r"\b(Brazil|Brazilian|Brasil)\b|brasileir", re.I)
# EMENDA-07 §B4: palavras de resultado
RESULTADO = [
    "effect", "effects", "impact", "impacts", "increase", "increased", "increases", "decrease", "decreased",
    "reduce", "reduced", "reduces", "reduction", "raise", "raised", "cause", "caused", "led to",
    "associated with", "efeito", "efeitos", "impacto", "aumento", "aumentou", "redução", "reduziu",
    "diminuiu", "causou",
]
RE_RESULTADO = re.compile(r"\b(" + "|".join(re.escape(w) for w in RESULTADO) + r")\b", re.I)

# EMENDA-09 §B1: consultas curtas (número -> (inglês, português))
CONSULTAS_09 = {
    "01": ("Plano Real", "Plano Real"), "02": ("inflation targeting Brazil", "metas de inflação Brasil"),
    "03": ("Fiscal Responsibility Law Brazil", "Lei de Responsabilidade Fiscal"), "04": ("Bolsa Familia", "Bolsa Família"),
    "05": ("minimum wage Brazil", "salário mínimo Brasil"), "06": ("commodity boom Brazil", "commodities Brasil crescimento"),
    "07": ("Brazil 2008 crisis", "crise de 2008 Brasil"), "08": ("Minha Casa Minha Vida", "Minha Casa Minha Vida"),
    "09": ("BNDES", "BNDES"), "10": ("payroll tax Brazil", "desoneração da folha"),
    "11": ("Brazil recession 2015", "recessão 2015 Brasil"), "12": ("Lava Jato", "Lava Jato"),
    "13": ("spending cap Brazil", "teto de gastos"), "14": ("labor reform Brazil", "reforma trabalhista"),
    "15": ("pension reform Brazil", "reforma da previdência"), "16": ("Auxilio Emergencial", "Auxílio Emergencial"),
    "17": ("Amazon deforestation policy", "desmatamento Amazônia política"), "18": ("Pix Brazil", "Pix Banco Central"),
    "19": ("fiscal framework Brazil", "arcabouço fiscal"), "20": ("cash transfer Brazil 2023", "Bolsa Família 2023"),
}

# EMENDA-10 §B: episódios 21-23 e consultas curtas (mesmos parâmetros da rodada 09)
EPISODIOS_10 = [
    ("21", "Dívida externa, reservas internacionais e vulnerabilidade externa (1994-)", ["fhc", "lula12", "dilma", "temer", "bolsonaro", "lula3"], "external debt Brazil", "dívida externa Brasil"),
    ("22", "Acumulação de reservas e quitação com o FMI (2005-2008)", ["lula12"], "international reserves Brazil", "reservas internacionais Brasil"),
    ("23", "Trajetória da dívida pública bruta e custo de carregamento (2014-)", ["dilma", "temer", "bolsonaro", "lula3"], "public debt Brazil", "dívida pública Brasil"),
]
CONSULTAS_10 = dict(CONSULTAS_09, **{n: (en, pt) for n, _nome, _govs, en, pt in EPISODIOS_10})

# EMENDA-12 §B: episódios 24-27 (instituições: autonomia do BC, regras fiscais, imprensa, poderes); mesmos parâmetros
TODOS = ["fhc", "lula12", "dilma", "temer", "bolsonaro", "lula3"]
EPISODIOS_12 = [
    ("24", "Autonomia do Banco Central: de fato desde as metas (1999) e de direito pela LC 179 (2021)", TODOS, "central bank independence Brazil", "autonomia do Banco Central"),
    ("25", "Regras fiscais como classe: LRF (2000), teto de gastos (2016) e arcabouço (2023)", TODOS, "fiscal rules Brazil", "regras fiscais Brasil"),
    ("26", "Liberdade de imprensa e de expressão (1995-)", TODOS, "press freedom Brazil", "liberdade de imprensa Brasil"),
    ("27", "Independência judicial e separação de poderes (1995-)", TODOS, "judicial independence Brazil", "independência judicial Brasil"),
]
CONSULTAS_11 = dict(CONSULTAS_10, **{n: (en, pt) for n, _nome, _govs, en, pt in EPISODIOS_12})

# rodada -> emenda que a rege, quando os números diferem (a rodada 11 é a EMENDA-12)
RODADA_EMENDA = {"11": "12"}

PROTOCOLOS = {
    "07": {
        "prefixo": "openalex-",
        "saida": "series/emenda07",
        "teto": 40,
        "url": lambda q: "https://api.openalex.org/works?search=" + quote(q) + "&filter=type:article|review&sort=cited_by_count:desc&per_page=40",
        "desenhos": DESENHOS_07,
        "siglas": SIGLAS_07,
        "resumo_crossref": False,
    },
    "08": {
        "prefixo": "openalex8-",
        "saida": "series/emenda08",
        "teto": 100,
        "url": lambda q: "https://api.openalex.org/works?filter=title_and_abstract.search:" + quote(q) + ",type:article|review&sort=relevance_score:desc&per_page=100",
        "desenhos": DESENHOS_08,
        "siglas": SIGLAS_08,
        "resumo_crossref": True,
    },
    "09": {
        "prefixo": "openalex9-",
        "saida": "series",
        "teto": 200,
        "consultas": CONSULTAS_09,
        "url": lambda q: "https://api.openalex.org/works?filter=title_and_abstract.search:" + quote(q) + ",type:article|review&sort=relevance_score:desc&per_page=200",
        "desenhos": DESENHOS_08,
        "siglas": SIGLAS_08,
        "resumo_crossref": True,
    },
    # EMENDA-10 §C: mesmos parâmetros e mesmo prefixo da 09 (o bruto dos 20 episódios é reutilizado); 3 episódios a mais
    "10": {
        "prefixo": "openalex9-",
        "saida": "series/emenda10",
        "teto": 200,
        "consultas": CONSULTAS_10,
        "episodios": EPISODIOS + EPISODIOS_10,
        "url": lambda q: "https://api.openalex.org/works?filter=title_and_abstract.search:" + quote(q) + ",type:article|review&sort=relevance_score:desc&per_page=200",
        "desenhos": DESENHOS_08,
        "siglas": SIGLAS_08,
        "resumo_crossref": True,
    },
    # EMENDA-12 §C: mesmos parâmetros e prefixo das rodadas 09 e 10 (o bruto dos 23 episódios é reutilizado); 4 episódios a mais
    "11": {
        "prefixo": "openalex9-",
        "saida": "series/emenda11",
        "teto": 200,
        "consultas": CONSULTAS_11,
        "episodios": EPISODIOS + EPISODIOS_10 + EPISODIOS_12,
        "url": lambda q: "https://api.openalex.org/works?filter=title_and_abstract.search:" + quote(q) + ",type:article|review&sort=relevance_score:desc&per_page=200",
        "desenhos": DESENHOS_08,
        "siglas": SIGLAS_08,
        "resumo_crossref": True,
    },
}


def episodios(P):
    """Os episódios da rodada: os 20 da EMENDA-07 ou, na rodada 10, esses mais os 3 da EMENDA-10."""
    return P.get("episodios", EPISODIOS)


def consultas(P, num, en, pt):
    """As duas consultas de um episódio na rodada: as da emenda 07 ou as curtas da emenda 09."""
    return P["consultas"].get(num, (en, pt)) if "consultas" in P else (en, pt)


def issn_norm(s):
    """``1542-4863`` -> ``15424863``."""
    return s.replace("-", "").strip().upper()


def sjr():
    """ISSN normalizado -> (melhor quartil, título) na edição 2024 do SJR (mesmo arquivo da fase 2)."""
    out = {}
    with open(SJR, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            for i in r["Issn"].split(","):
                i = issn_norm(i)
                if i and i != "-":
                    out[i] = (r["SJR Best Quartile"], r["Title"])
    return out


def resumo_openalex(w):
    """Reconstrói o resumo do índice invertido do OpenAlex; ``None`` quando a editora não o cede."""
    inv = w.get("abstract_inverted_index")
    if not inv:
        return None
    pos = {}
    for palavra, idxs in inv.items():
        for k in idxs:
            pos[k] = palavra
    return " ".join(pos[k] for k in sorted(pos))


def resumo_crossref(cr):
    """Campo ``abstract`` do Crossref sem as marcas JATS; ``None`` se não houver."""
    a = cr.get("abstract")
    if not a:
        return None
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a)).strip() or None


def frases_resultado(texto):
    """Até 2 frases do resumo com uma palavra de resultado (§B4)."""
    frases = re.split(r"(?<=[.!?])\s+", texto)
    return [f.strip() for f in frases if RE_RESULTADO.search(f)][:2]


def crossref(doi, baixar_novo):
    """Registro do Crossref de um DOI (do bruto; baixa e hasheia se permitido). ``None`` quando não há."""
    nome = re.sub(r"[^A-Za-z0-9._-]", "_", doi)
    destino = f"bruto/crossref-{nome}.json"
    if not (AQUI / destino).exists():
        if not baixar_novo:
            return None
        try:
            baixar(AQUI, "https://api.crossref.org/works/" + quote(doi, safe=""), destino, nota=f"Crossref {doi}")
        except Exception as e:  # noqa: BLE001 - a falha da fonte é registrada, não escondida
            return {"erro": type(e).__name__}
        time.sleep(0.3)
    return json.loads((AQUI / destino).read_text(encoding="utf-8")).get("message", {})


def consultar(P):
    """As 40 consultas ao OpenAlex de uma rodada, pela cadeia de hash."""
    for num, _nome, _govs, en, pt in episodios(P):
        for lang, q in zip(("en", "pt"), consultas(P, num, en, pt), strict=True):
            destino = f"bruto/{P['prefixo']}{num}-{lang}.json"
            if (AQUI / destino).exists():
                continue
            baixar(AQUI, P["url"](q), destino, nota=f"OpenAlex, episodio {num} ({lang}): {q}")
            time.sleep(4)


def derivar(P, baixar_novo=True):
    """Aplica os passos a-e a tudo que o bruto da rodada devolveu e grava a pasta de saída."""
    re_desenho = re.compile(r"\b(" + "|".join(re.escape(d) for d in P["desenhos"]) + r")\b", re.I)
    re_sigla = re.compile(r"\b(" + "|".join(re.escape(s) for s in P["siglas"]) + r")\b")
    quartis = sjr()
    trabalhos, cortes = {}, []
    for num, _nome, govs, _en, _pt in episodios(P):
        for lang in ("en", "pt"):
            dados = json.loads((BRUTO / f"{P['prefixo']}{num}-{lang}.json").read_text(encoding="utf-8"))
            cortes.append((num, lang, dados["meta"]["count"], len(dados["results"])))
            for w in dados["results"]:
                t = trabalhos.setdefault(w["id"], {"w": w, "episodios": [], "mandatos": set()})
                if num not in t["episodios"]:
                    t["episodios"].append(num)
                t["mandatos"].update(govs)
    linhas = []
    for oid, t in trabalhos.items():
        w = t["w"]
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        fonte = (w.get("primary_location") or {}).get("source") or {}
        issns = [issn_norm(i) for i in (fonte.get("issn") or [])]
        if fonte.get("issn_l"):
            issns.append(issn_norm(fonte["issn_l"]))
        titulo = w.get("title") or w.get("display_name") or ""
        reg = {
            "chave": oid.rsplit("/", 1)[-1], "doi": doi, "openalex_id": oid, "titulo": titulo,
            "autores": "; ".join(a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")),
            "periodico": fonte.get("display_name", ""), "issn": ", ".join(sorted(set(issns))),
            "ano": w.get("publication_year"), "quartil_sjr": "", "sjr_edicao": SJR_EDICAO,
            "citacoes_openalex": w.get("cited_by_count"), "episodios": "; ".join(t["episodios"]),
            "mandatos": "; ".join(sorted(t["mandatos"])), "desenho": "", "frases_resultado": "",
            "status": "excluido", "motivo": "",
        }
        q = next(((quartis[i][0], quartis[i][1]) for i in issns if i in quartis), None)
        if q:
            reg["quartil_sjr"] = q[0]
        if not doi:
            reg["motivo"] = "sem DOI"
        elif q is None:
            reg["motivo"] = "periódico fora do SJR 2024"
        elif q[0] != "Q1":
            reg["motivo"] = f"quartil {q[0]}"
        else:
            texto, origem, cr = resumo_openalex(w), "OpenAlex", None
            if texto is None and P["resumo_crossref"]:
                cr = crossref(doi, baixar_novo)
                texto, origem = (resumo_crossref(cr) if cr and "erro" not in cr else None), "Crossref"
            if not RE_BRASIL.search(titulo + " " + (texto or "")):
                reg["motivo"] = "não é sobre o Brasil"
            elif texto is None:
                reg["motivo"] = "sem resumo no OpenAlex" + (" nem no Crossref" if P["resumo_crossref"] else "")
            else:
                achados = sorted({m.group(0).lower() for m in re_desenho.finditer(texto)} | {m.group(0) for m in re_sigla.finditer(texto)})
                if not achados:
                    reg["motivo"] = "sem desenho declarado no resumo"
                else:
                    reg["desenho"] = "; ".join(achados) + (" (resumo: Crossref)" if origem == "Crossref" else "")
                    reg["frases_resultado"] = " | ".join(frases_resultado(texto))
                    if cr is None:
                        cr = crossref(doi, baixar_novo)
                    if cr is None:
                        reg["motivo"] = "Crossref não consultado"
                    elif "erro" in cr:
                        reg["motivo"] = f"Crossref sem registro ({cr['erro']})"
                    elif cr.get("type") != "journal-article":
                        reg["motivo"] = f"Crossref: tipo {cr.get('type')}"
                    else:
                        reg["status"] = "incluido"
        linhas.append(reg)
    linhas.sort(key=lambda r: (r["episodios"], -(r["citacoes_openalex"] or 0)))
    saida = AQUI / P["saida"]
    saida.mkdir(parents=True, exist_ok=True)
    campos = list(linhas[0].keys())
    for nome, sel in (("literatura_todos.csv", linhas), ("literatura_incluidos.csv", [r for r in linhas if r["status"] == "incluido"])):
        with open(saida / nome, "w", encoding="utf-8", newline="") as fh:
            wr = csv.DictWriter(fh, fieldnames=campos)
            wr.writeheader()
            wr.writerows(sel)
    with open(saida / "episodios.csv", "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["numero", "episodio", "mandatos", "consulta_en", "consulta_pt", "total_openalex_en", "lidos_en", "total_openalex_pt", "lidos_pt"])
        for num, nome, govs, en, pt in episodios(P):
            c = {lang: (tot, lidos) for n, lang, tot, lidos in cortes if n == num}
            qe, qp = consultas(P, num, en, pt)
            wr.writerow([num, nome, "; ".join(govs), qe, qp, c["en"][0], c["en"][1], c["pt"][0], c["pt"][1]])
    motivos = {}
    for r in linhas:
        k = r["motivo"] or "incluido"
        motivos[k] = motivos.get(k, 0) + 1
    return linhas, motivos, cortes


def resultado(emenda, P, linhas, motivos, cortes):
    """Escreve o RESULTADO.md da rodada com os números da coleta."""
    inc = [r for r in linhas if r["status"] == "incluido"]
    por_ep = {}
    for r in inc:
        for e in r["episodios"].split("; "):
            por_ep[e] = por_ep.get(e, 0) + 1
    amd = RODADA_EMENDA.get(emenda, emenda)
    md = [f"# Coleta `literatura-fase3`, rodada {emenda} (EMENDA-{amd} §B)", "", f"Gerado em {time.strftime('%Y-%m-%d')} por `coletar.py --emenda {emenda}`, do bruto hasheado. Regra executada por código; nenhuma seleção à mão.", "", "## Números", "", "| Medida | Valor |", "|---|---|",
          f"| Consultas ao OpenAlex | {len(cortes)} (teto {P['teto']} por consulta) |", f"| Trabalhos distintos devolvidos | {len(linhas)} |", f"| Incluídos (a-e) | {len(inc)} |"]
    md += [f"| {m} | {n} |" for m, n in sorted(motivos.items(), key=lambda x: -x[1])]
    md += ["", "## Incluídos por episódio", "", "| Episódio | Incluídos |", "|---|---|"]
    md += [f"| {num} {nome} | {por_ep.get(num, 0)} |" for num, nome, *_ in episodios(P)]
    md += ["", f"## Corte por consulta (teto {P['teto']})", "", "| Episódio | Língua | Total no OpenAlex | Lidos |", "|---|---|---|---|"]
    md += [f"| {n} | {lang} | {tot} | {lidos} |" for n, lang, tot, lidos in cortes]
    md += ["", "## Limitações (EMENDA-07 §B6)", "", "Lista de desenhos por palavra; quartil da edição 2024 do SJR; editoras que não cedem o resumo aparecem como `sem resumo`." + (" Ordem por citações (rodada 07): ver EMENDA-08 §A." if emenda == "07" else " Consultas longas (rodada 08): ver EMENDA-09 §A." if emenda == "08" else ""), ""]
    nome = "RESULTADO.md" if emenda == "09" else f"RESULTADO-emenda{emenda}.md"
    (AQUI / P["saida"] / nome if emenda != "09" else AQUI / nome).write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--emenda", choices=sorted(PROTOCOLOS), default="09")
    ap.add_argument("--so-derivar", action="store_true")
    x = ap.parse_args()
    P = PROTOCOLOS[x.emenda]
    if not x.so_derivar:
        consultar(P)
    linhas, motivos, cortes = derivar(P, baixar_novo=not x.so_derivar)
    resultado(x.emenda, P, linhas, motivos, cortes)
    print(json.dumps(motivos, ensure_ascii=False, indent=1))
