"""Biblioteca de extração (sem rede): lê os brutos em bruto/ e devolve linhas de série com proveniência.

Uso: python3 -I scripts/gerar_series.py  (sys.path é ajustado explicitamente porque -I remove o diretório do script)
"""
import os, re, subprocess, sys, importlib.util
from decimal import Decimal

BASE = '/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/estatais-lucro'
BRUTO = BASE + '/bruto'
SCRIPTS = BASE + '/scripts'
TXT = SCRIPTS + '/_txt'   # só para OCR (derivado do bruto por scripts/ocr.sh)

_cache = {}


def _html2txt():
    spec = importlib.util.spec_from_file_location('html2txt', SCRIPTS + '/html2txt.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def paginas(arq, modo):
    """lista de páginas; cada página = lista de linhas. modo: layout | raw | html | ocr | txt"""
    k = (arq, modo)
    if k in _cache: return _cache[k]
    p = BRUTO + '/' + arq
    if modo in ('layout', 'raw'):
        t = subprocess.run(['pdftotext', '-' + modo, p, '-'], capture_output=True).stdout.decode('utf-8', 'replace')
        pg = t.split('\f')
    elif modo == 'ocr':
        stem = os.path.splitext(arq)[0]
        t = open(f'{TXT}/{stem}.ocr.txt', encoding='utf-8').read()
        pg = t.split('\f')
    elif modo == 'html':
        raw = open(p, 'rb').read().decode('latin-1')
        h = _html2txt(); ps = h.P(); ps.feed(raw)
        t = ''.join(ps.out).replace('\xa0', ' ')
        t = re.sub(r'[ \t]+', ' ', t); t = re.sub(r'\n\s*\n+', '\n', t)
        pg = [t]
    elif modo == 'txt':
        pg = [open(p, 'rb').read().decode('latin-1')]
    else:
        raise ValueError(modo)
    r = [x.split('\n') for x in pg]
    _cache[k] = r
    return r


_BR = re.compile(r'\(?\s*-?\d{1,3}(?:\.\d{3})+(?:,\d+)?\s*\)?|\(?\s*-?\d+(?:,\d+)?\s*\)?')
_US = re.compile(r'\(?\s*-?\d{1,3}(?:,\d{3})+(?:\.\d+)?\s*\)?|\(?\s*-?\d+(?:\.\d+)?\s*\)?')


def nums(s, fmt='br'):
    out = []
    s = re.sub(r'(?<=\d)\.\s+(?=\d{3}\b)', '.', s) if fmt == 'br' else s
    for m in (_BR if fmt == 'br' else _US).finditer(s):
        t = m.group(0)
        neg = t.strip().startswith('(') or t.strip().startswith('-')
        d = re.sub(r'[()\s-]', '', t)
        d = d.replace('.', '').replace(',', '.') if fmt == 'br' else d.replace(',', '')
        v = Decimal(d)
        out.append(-v if neg else v)
    return out


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def acha(arq, modo, ancora, apos=None, occ=1, minnums=1, fmt='br', antes=None, junta=0):
    """devolve (pagina, linha, texto_linha, [numeros apos a ancora]) da occ-ésima linha que casa."""
    pg = paginas(arq, modo)
    rx = re.compile(ancora, re.I)
    ra = re.compile(apos, re.I) if apos else None
    liberado = ra is None
    rb = re.compile(antes, re.I) if antes else None
    n = 0
    for pi, lines in enumerate(pg, 1):
        for li, l in enumerate(lines, 1):
            if not liberado:
                if ra.search(l): liberado = True
                else: continue
            if rb and rb.search(l): raise LookupError(f'{arq}: ancora {ancora!r} nao achada antes de {antes!r}')
            lj = ' '.join(lines[li - 1:li + junta]) if junta else l
            m = rx.search(lj)
            if not m: continue
            ns = nums(lj[m.end():], fmt)
            if len(ns) < minnums: continue
            n += 1
            if n == occ: return pi, li, lj, ns
    raise LookupError(f'{arq}: ancora {ancora!r} (apos={apos!r}, occ={occ}) nao achada')


def valstr(d):
    s = format(d, 'f')
    if '.' in s: s = s.rstrip('0').rstrip('.')
    return s


class Linha(dict):
    pass


def extrai(emp, arq, modo, ancora, cols, definicao, unidade, fonte, vintage, fmt='br', apos=None, occ=1,
           minnums=1, antes=None, obs='', junta=0):
    """cols: lista de (indice_numero, ano[, definicao_alternativa])."""
    pi, li, texto, ns = acha(arq, modo, ancora, apos, occ, minnums, fmt, antes, junta)
    saida = []
    for c in cols:
        idx, ano = c[0], c[1]
        d = c[2] if len(c) > 2 and c[2] else definicao
        if idx >= len(ns):
            raise LookupError(f'{arq}: so {len(ns)} numeros na linha {li}: {norm(texto)[:120]}')
        loc = f'pág. {pi}, linha {li}' if modo != 'html' and modo != 'txt' else f'linha {li} do texto convertido'
        if modo == 'ocr': loc += ' (texto OCR do PDF-imagem)'
        nota = f'bruto/{arq}, {loc}: «{norm(texto)[:170]}»'
        if obs: nota += ' | ' + obs
        saida.append(Linha(empresa=emp, indicador='lucro_liquido', fonte=fonte, definicao_linha=d, ano=ano,
                           valor=valstr(ns[idx]), unidade=unidade, nota=nota, vintage=vintage))
    return saida


def manual(emp, arq, ano, valor, definicao, unidade, fonte, vintage, onde, trecho):
    """valor lido visualmente na imagem do PDF (sem camada de texto confiável)."""
    return [Linha(empresa=emp, indicador='lucro_liquido', fonte=fonte, definicao_linha=definicao, ano=ano,
                  valor=valor, unidade=unidade, nota=f'bruto/{arq}, {onde} (leitura visual da imagem): «{trecho}»',
                  vintage=vintage)]
