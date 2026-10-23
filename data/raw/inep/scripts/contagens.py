"""Parser das tabelas de CONTAGEM (aprovados, reprovados, afastados por abandono) das Sinopses 1996-2006.

Le os csv de uma pasta (uma aba por arquivo, ja convertidos pelo soffice). Tabelas 'por Localizacao e
Dependencia Administrativa': por linha de UF, colunas = Total(Total,Federal,Estadual,Municipal,Privada)
+ Rural(...). Usa so o bloco 'Total' (localizacao total). Titulo da tabela traz o ano de REFERENCIA.
"""
import glob
import os
import re
import unicodedata

from lib import ler_csv, num
from ufs import uf as norm_uf


def _s(x):
    x = unicodedata.normalize("NFKD", x or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", x).strip()


def titulo(rows):
    """Titulo da tabela: a mais longa das celulas (nas 12 primeiras linhas) que comecam com 'N.N'.

    Quando o titulo quebra em duas linhas (sem ano no fim), junta a 1a celula da linha seguinte.
    """
    cand = []
    for k, r in enumerate(rows[:12]):
        for c in r[:2]:
            if re.match(r"\s*\"?\d+(\.\d+)+\s*[-\u2013]?", c):
                t = re.sub(r"\s+", " ", c).strip()
                if not re.search(r"(19|20)\d\d\s*\"?\s*$", t) and k + 1 < len(rows):
                    nx = re.sub(r"\s+", " ", rows[k + 1][0]).strip() if rows[k + 1] else ""
                    if nx and not nx.lower().startswith("unidade"):
                        t = t + " " + nx
                cand.append(t)
    return max(cand, key=len) if cand else ""


def classificar(t):
    """Titulo -> (tipo, nivel, recorte) para tabelas por localizacao e dependencia, ou None."""
    s = _s(t)
    if "localizacao" not in s or "dependencia" not in s:
        return None
    if re.search(r"diurno|noturno|nao.seriado|supletivo|especial|profissional|jovens|creche|pre-escola|alfabet|faixa", s):
        return None
    if "afastados por abandono" in s:
        tipo = "abandono"
    elif "reprovados" in s and "aprovados" not in s:
        tipo = "reprovacao"
    elif "aprovados" in s and "reprovados" not in s:
        tipo = "aprovacao"
    else:
        return None
    if "ensino medio" in s:
        return (tipo, "em", "total")
    if "ensino fundamental" in s:
        if re.search(r"1a a 4a|1a-4a|anos iniciais", s):
            return (tipo, "ef", "ai")
        if re.search(r"5a a 8a|5o a 8a|anos finais", s):
            return (tipo, "ef", "af")
        return (tipo, "ef", "total")
    return None


def classificar_serie(t):
    """Titulo -> tipo para tabelas EF 'por Serie' (colunas Total, 1a..8a), ou None."""
    s = _s(t)
    if "por serie" not in s or "dependencia" in s or "ensino fundamental" not in s:
        return None
    if re.search(r"diurno|noturno|nao.seriado|supletivo|especial|medio|faixa|1a a 4a|5a a 8a", s):
        return None
    if "afastados por abandono" in s:
        return "abandono"
    if "reprovados" in s and "aprovados" not in s:
        return "reprovacao"
    if "aprovados" in s and "reprovados" not in s:
        return "aprovacao"
    return None


REDES = ["Total", "Federal", "Estadual", "Municipal", "Privada"]


def registrar(res, ano, linhas, cl, serie_tipo=None):
    """linhas: [(nome_uf, [numeros])]. cl: (tipo, nivel, recorte) p/ dep; serie_tipo p/ por serie.

    Por serie: total (rede 'Total') + AI (1a-4a) + AF (5a-8a) a partir das colunas; confere Total = soma.
    """
    n = 0
    vistos = set()
    for nome, vals in linhas:
        u = norm_uf(nome)
        if u is None or u.startswith("REG:") or u in vistos:
            continue
        vistos.add(u)  # so a 1a ocorrencia: algumas abas repetem as linhas no rodape
        if serie_tipo:
            if len(vals) < 9 or any(v is None for v in vals[:9]):
                continue
            tot, ser = vals[0], vals[1:9]
            # tabela por serie so preenche o que nao veio de tabela por dependencia (que tem prioridade)
            res.setdefault((ano, u, "Total", "ef", "total", serie_tipo), tot)
            res.setdefault((ano, u, "Total", "ef", "ai", serie_tipo), sum(ser[:4]))
            res.setdefault((ano, u, "Total", "ef", "af", serie_tipo), sum(ser[4:]))
            res[(ano, u, "Total", "ef", "soma_series_confere", serie_tipo)] = float(abs(sum(ser) - tot) <= 1)
        else:
            tipo, nivel, rec = cl
            if len(vals) < 5 or all(v is None for v in vals[:5]):
                continue
            for rede, v in zip(REDES, vals[:5]):
                if v is not None:
                    res[(ano, u, rede, nivel, rec, tipo)] = v
        n += 1
    return n


def ler_pasta(pasta):
    """Devolve dict {(ano_ref, uf, rede, nivel, recorte, tipo): contagem} e lista de tabelas usadas."""
    res, usados = {}, []
    for f in sorted(glob.glob(os.path.join(pasta, "*.csv"))):
        rows = ler_csv(f)
        t = titulo(rows)
        if not t:
            continue
        cl, st = classificar(t), classificar_serie(t)
        if not (cl or st):
            continue
        if st and any("ano inicial" in _s(c) for r in rows[:12] for c in r):
            continue  # 2004-2006: coluna extra 'Ano Inicial' (EF de 9 anos); as tabelas por dependencia cobrem esses anos
        m = re.search(r"((?:19|20)\d\d)\s*\"?\s*$", t)
        if not m:
            continue
        ano = int(m.group(1))
        linhas = [(r[0], [num(x) for x in r[1:]]) for r in rows if r and norm_uf(r[0])]
        if cl and any("urbana" in _s(c) for r in rows[:12] for c in r):
            # Sinopse 2006 (rendimento 2005): Total | Urbana(Total,Fed,Est,Mun,Priv) | Rural(idem);
            # a rede total = urbana + rural, por dependencia
            def _z(x):
                return x or 0.0
            linhas = [(nm, [v[0]] + [_z(v[i]) + _z(v[i + 5]) for i in (2, 3, 4, 5)]) for nm, v in linhas if len(v) >= 11]
        n = registrar(res, ano, linhas, cl, st)
        usados.append((os.path.basename(f), t[:110], ano, n))
    return res, usados


def ler_pdf_texto(txt):
    """Tabelas do PDF 'censo-miolo-98' (pdftotext -layout): blocos que comecam em '4.N - <titulo> - AAAA'."""
    res, usados = {}, []
    L = txt.split("\n")
    i = 0
    while i < len(L):
        m = re.match(r"\s*(4\.\d+)\s*-\s*(\S.*)$", L[i])
        if not m or "...." in L[i]:
            i += 1
            continue
        t, j = L[i].strip(), i + 1
        while j < len(L) and L[j].strip() and not re.search(r"(19|20)\d\d\s*$", t):
            t += " " + L[j].strip()
            j += 1
        t = re.sub(r"\s+", " ", t)
        cl, st = classificar(t), classificar_serie(t)
        ma = re.search(r"((?:19|20)\d\d)\s*$", t)
        if not (cl or st) or not ma:
            i = j
            continue
        linhas = []
        k = j
        while k < len(L) and not L[k].strip().startswith("Fonte"):
            mm = re.match(r"\s*([A-Za-z\u00c0-\u00ff][A-Za-z\u00c0-\u00ff .\-]*?)\s{2,}((?:[\d.]+|-)(?:\s+(?:[\d.]+|-))+)\s*$", L[k])
            if mm and norm_uf(mm.group(1)):
                linhas.append((mm.group(1), [num(x) for x in mm.group(2).split()]))
            k += 1
        n = registrar(res, int(ma.group(1)), linhas, cl, st)
        usados.append(("pdf:" + m.group(1), t[:110], int(ma.group(1)), n))
        i = k
    return res, usados
