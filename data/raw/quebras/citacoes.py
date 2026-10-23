# Verificador de citacoes: toda frase em "trecho_citado" tem de existir, literalmente (apos normalizar espacos, hifenizacao de quebra de
# linha e aspas), no arquivo local indicado. Frase que nao for achada derruba o script (nada inventado entra no CSV).
import html
import json
import pathlib
import re

H = pathlib.Path(__file__).resolve().parent
D = H.parent
DER = H / "derivado"
BR = H / "bruto"

_TROCA = {"ă": "ã", "ę": "ê", "ő": "õ", "ŕ": "à", "Ă": "Ã", "Ę": "Ê", "Ő": "Õ",
          "’": "'", "‘": "'", "“": '"', "”": '"', " ": " ", "­": ""}


def norm(t):
    for a, b in _TROCA.items():
        t = t.replace(a, b)
    t = re.sub(r"-\n\s*(?=[a-zà-ú])", "", t)
    t = re.sub(r"\s+", " ", t)
    return re.sub(r" ([.,;:)])", r"\1", t).replace("( ", "(").strip()


def _html(arq):
    t = pathlib.Path(arq).read_text(encoding="cp1252", errors="replace")
    t = re.sub(r"(?s)<(script|style).*?</\1>", "", t)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def _ipeadata():
    """Campo SERCOMENTARIO de todas as series (catalogo e metadados do bloco social)."""
    linhas = []
    for arq in (D / "economia-real/meta/ipeadata-Metadados-catalogo-completo-raw.json", D / "social/bruto/ipea_metadados_all.json"):
        for x in json.load(open(arq))["value"]:
            com = re.sub(r"<[^>]+>", " ", (x.get("SERCOMENTARIO") or "")).replace("\r\n", " ")
            linhas.append(f"[{x['SERCODIGO']}] {x['SERNOME']} :: {html.unescape(com)}")
    return "\n".join(linhas)


def _ler(*partes):
    out = []
    for p in partes:
        p = pathlib.Path(p)
        out.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(out)


_FONTES = {
    "liv1259": lambda: _ler(DER / "ibge-liv1259.txt", DER / "ibge-liv1259.raw.txt"),
    "pme2002mar": lambda: _ler(DER / "ibge-pme-2002-mar.txt", DER / "ibge-pme-2002-mar.raw.txt"),
    "pme2002nov": lambda: _ler(DER / "ibge-pme-2002-nov.txt", DER / "ibge-pme-2002-nov.raw.txt"),
    "pme_antiga_pagina": lambda: _ler(BR / "ibge-pme-antiga-metodologia-jina.md"),
    "nt_pme_pnad_pnadc": lambda: _ler(DER / "ibge-liv101823.txt", DER / "ibge-liv101823.raw.txt"),
    "nt03_2021_reponderacao": lambda: _ler(DER / "ibge-liv101866.txt", DER / "ibge-liv101866.raw.txt"),
    "nt05_2021_rendimentos": lambda: _ler(DER / "ibge-liv101874.txt", DER / "ibge-liv101874.raw.txt"),
    "nt03_2022_modulos": lambda: _ler(DER / "ibge-liv101960.txt", DER / "ibge-liv101960.raw.txt"),
    "sis2012_notas": lambda: _ler(DER / "ibge-sis2012-notas-tecnicas.txt", DER / "ibge-sis2012-notas-tecnicas.raw.txt"),
    "proj2024": lambda: _ler(DER / "ibge-liv102111.txt", DER / "ibge-liv102111.raw.txt"),
    "proj2018": lambda: _ler(DER / "ibge-liv101597.txt", DER / "ibge-liv101597.raw.txt"),
    "bcb_ee070": lambda: _ler(DER / "bcb-ee070.txt", DER / "bcb-ee070.raw.txt"),
    "bcb_ri201912": lambda: _ler(DER / "bcb-ri201912.txt", DER / "bcb-ri201912.raw.txt"),
    "scn2010_nota17": lambda: _ler(DER / "ibge-scn2010-nota17.txt", DER / "ibge-scn2010-nota17.raw.txt"),
    "snipc_nt_2005_02": lambda: _ler(DER / "ibge-snipc-nt-2005-02.txt", DER / "ibge-snipc-nt-2005-02.raw.txt"),
    "puc_pib": lambda: _ler(DER / "puc-rio-revisao-pib.txt", DER / "puc-rio-revisao-pib.raw.txt"),
    "ipea_bmt23": lambda: _ler(DER / "ipea-bmt23.txt", DER / "ipea-bmt23.raw.txt"),
    "liv98593": lambda: _ler(DER / "ibge-liv98593.txt", DER / "ibge-liv98593.raw.txt"),
    "bcb_nt48": lambda: _ler(DER / "bcb-nt48.txt", DER / "bcb-nt48.raw.txt"),
    "bcb_nm2001": lambda: _ler(DER / "bcb-nm-2001.txt", DER / "bcb-nm-2001.raw.txt"),
    "bcb_nt03_2001": lambda: _ler(DER / "bcb-nt03-2001.txt", DER / "bcb-nt03-2001.raw.txt"),
    "bcb_museu": lambda: _ler(DER / "bcb-museu-padroes.txt", DER / "bcb-museu-padroes.raw.txt"),
    "wb_blog_2017ppp": lambda: _ler(DER / "wb-blog-updating-ipl-2017-ppps.txt"),
    "wb_blog_2021prices": lambda: _ler(DER / "wb-blog-new-lines-2021-prices.txt"),
    "wb_prwp7432": lambda: _ler(BR / "wb-pw7432-global-count-2012.pdf"),
    "sis2025_t217": lambda: _ler(DER / "sis2025-t2-17.txt"),
    "sis2025_t213": lambda: _ler(DER / "sis2025-t2-13.txt"),
    "wdi_meta": lambda: _ler(DER / "wdi-meta.txt"),
    "release_9726": lambda: _ler(BR / "ibge-release-9726-jina.md"),
    "release_9729": lambda: _ler(BR / "ibge-release-9729-jina.md"),
    "release_13264": lambda: _ler(BR / "ibge-release-13264-jina.md"),
    "ipca_liv65477": lambda: _ler(D / "historia/bruto/ibge-ipca/liv65477.txt"),
    "agencia_tabuas2024": lambda: _ler(D / "social/bruto/ibge_agencia_tabuas2024_jina.md"),
    "ipeadata": _ipeadata,
    "ibge_ipca_pesos_2020": lambda: _ler(BR / "ibge-ipca-pesos-2020-jina.md"),
    "ibge_complete_life_tables": lambda: _ler(BR / "ibge-complete-life-tables-jina.md"),
    "pip_json": lambda: _ler(D / "social/bruto/pip_ppp2017_line6.85.json"),
    "wdi_dday": lambda: _ler(D / "social/bruto/wb_SI.POV.DDAY.json"),
    "cysne2004": lambda: _ler(D / "monetario/referencias/cysne-2004.txt"),
    "reddy_minoiu": lambda: _ler(DER / "reddy-minoiu-0509005.txt"),
}
for f in ("d5209-2004", "d5749-2006", "d6824-2009", "d6917-2009", "d8232-2014", "d8794-2016", "d9396-2018", "d10852-2021", "d11013-2022", "d6491-2008", "l14601-2023"):
    _FONTES["plan_" + f] = (lambda f=f: _html(BR / "planalto" / f"{f}.html"))

_CACHE = {}


def corpus(chave):
    if chave not in _CACHE:
        _CACHE[chave] = norm(_FONTES[chave]())
    return _CACHE[chave]


def verifica(chave, trecho):
    """trecho: frases separadas por ' [...] '. Levanta AssertionError se alguma nao existir literalmente."""
    t = corpus(chave)
    for parte in trecho.split(" [...] "):
        p = norm(parte)
        assert p and p in t, f"CITACAO NAO ENCONTRADA em {chave}: {parte[:120]!r}"
    return True
