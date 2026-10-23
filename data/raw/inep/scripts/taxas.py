"""Parser das planilhas 'Taxas de Rendimento por Brasil/Regioes/UFs' do INEP (2007-2025).

Mapeia colunas pelo ROTULO humano do cabecalho (nunca por posicao nem pelo codigo-maquina:
em 2019 a linha de codigos esta desalinhada do cabecalho humano).
"""
import re
import unicodedata

from ufs import uf as norm_uf

TIPOS = {"aprova": "aprovacao", "reprova": "reprovacao", "abandon": "abandono"}


def _s(x):
    x = unicodedata.normalize("NFKD", x or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", x).strip()


def _tipo(txt):
    for k, v in TIPOS.items():
        if k in txt:
            return v
    return None


def _nivel_sub(group, sub):
    """(nivel, recorte) a partir de rotulos ja normalizados. recorte in total/ai/af/None."""
    g, s = group, sub
    if "nao seriado" in s or "nao-seriado" in s or "nao seriado" in g:
        return None
    em = "medio" in g or "medio" in s
    ef = ("fundamental" in g or "fundamental" in s) and not em
    if em:
        if re.search(r"\btotal\b", s) and "nao" not in s:
            return ("em", "total")
        return None
    if ef:
        if re.search(r"anos iniciais|1a a 4a|1o ao 5o|1o a 5o", s):
            return ("ef", "ai")
        if re.search(r"anos finais|5a a 8a|6o ao 9o|6o a 9o", s):
            return ("ef", "af")
        if re.search(r"\btotal\b", s):
            return ("ef", "total")
    return None


def parse(rows, ano_nome):
    """rows: linhas do csv da aba de UFs (ou Brasil). Devolve lista de dicts.

    Cada dict: ano, uf, loc, rede, tipo, nivel, recorte, valor (float|None), rotulo.
    """
    i0 = next(i for i, r in enumerate(rows) if r and re.fullmatch(r"(19|20)\d\d", r[0].strip()))
    # cabecalho = linhas entre a 1a que traz 'Taxa de <tipo>' e i0
    ini = next(i for i, r in enumerate(rows) if any(re.match(r"\s*taxa de (aprova|reprova|abandon)", _s(c)) for c in r))
    hdr = [r for r in rows[ini:i0] if any(c.strip() for c in r)]
    ncol = max(len(r) for r in rows[ini:i0 + 1])
    # propaga rotulos para a direita em cada linha de cabecalho
    filled = []
    for r in hdr:
        cur, out = "", []
        for j in range(ncol):
            c = r[j].strip() if j < len(r) else ""
            if c:
                cur = c
            out.append(cur)
        filled.append(out)
    # linha de codigos-maquina (ultima, ex.: 'tap_FUN,tap_F14' ou '1_CAT_FUN'): descartada
    def _codigos(r):
        ne = [c.strip() for c in r if c.strip()]
        return len(ne) > 8 and sum(bool(re.fullmatch(r"[A-Za-z0-9_]+", c)) for c in ne) > 0.8 * len(ne) \
            and not any(re.fullmatch(r"(19|20)\d\d", c) for c in ne)
    while _codigos(hdr[-1]):
        hdr.pop()
        filled.pop()
    # colunas de identificacao: linha que comeca com 'Ano'
    idrow = next((r for r in hdr if _s(r[0]) == "ano"), None)
    idx_id = hdr.index(idrow)
    ids = [_s(c) for c in (idrow if idrow else [])]
    def col(*nomes):
        for j, c in enumerate(ids):
            if any(c == n for n in nomes):
                return j
        return None
    c_uf = col("uf", "unidade geografica", "no_cod", "unidgeo", "abrangencia")
    c_loc = col("localizacao", "tipoloca", "no_categoria")
    c_rede = col("rede", "dependencia administrativa", "dependad", "no_dependencia")
    assert None not in (c_uf, c_loc, c_rede), (ids[:8])
    primeira_dado = max(c_uf, c_loc, c_rede) + 1
    cols = []
    for j in range(primeira_dado, ncol):
        # tipo: ultimo rotulo (de cima p/ baixo) que contenha aprova/reprova/abandon, olhando linhas 'Taxa de ...'
        tipo = None
        for f in filled:
            t = _tipo(_s(f[j]))
            if t and re.match(r"taxa de", _s(f[j])):
                tipo = t
        sub = _s(filled[-1][j]) if filled else ""
        # grupo = todos os rotulos acima do ultimo, concatenados
        group = " | ".join(_s(f[j]) for f in filled[idx_id:-1])
        # em 2007-2011 o subrotulo traz o tipo e o nivel (ex.: 'total aprovacao fundamental')
        full = group + " | " + sub
        if tipo is None:
            tipo = _tipo(sub)
        # o tipo do bloco vem do rotulo 'taxa de X - ...' do grupo; sub que cite outro tipo e erro
        ns = _nivel_sub(group, sub)
        cols.append((j, tipo, ns, full))
    out = []
    for r in rows[i0:]:
        if not r or not re.fullmatch(r"(19|20)\d\d", r[0].strip()):
            continue
        u = norm_uf(r[c_uf])
        if u is None:
            continue
        loc = _s(r[c_loc])
        rede = _s(r[c_rede])
        for j, tipo, ns, full in cols:
            if ns is None or tipo is None or j >= len(r):
                continue
            out.append(dict(ano=int(r[0]), uf=u, loc=loc, rede=rede, tipo=tipo, nivel=ns[0], recorte=ns[1],
                            raw=r[j].strip(), rotulo=full))
    return out
