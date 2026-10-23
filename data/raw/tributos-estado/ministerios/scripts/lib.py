# Funcoes comuns (so leem bruto; sem rede). Texto do Planalto -> texto normalizado; parser de listas "I - ...; II - ...".
import re, sys, json, glob, os
BASE = "/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/ministerios"
sys.path.insert(0, "/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/scripts")
import txt  # leitor existente (utf-8, senao cp1252)

_cache = {}
def T(arq):
    """texto normalizado (espacos colapsados) de um arquivo bruto relativo a BASE"""
    if arq not in _cache:
        _cache[arq] = re.sub(r"\s+", " ", txt.ler(os.path.join(BASE, arq))).strip()
    return _cache[arq]

def R(rx):
    """torna a regex tolerante a 'o' / 'º' / '°' depois de digito ou 'n' (o Planalto mistura as grafias)"""
    return re.sub(r"(?<=[\dn])[oº°](?![a-zA-Z])", "[oº°]", rx)

def achar(arq, rx, flags=re.I):
    m = re.search(rx, T(arq), flags)
    return m

def url_de(arq):
    """URL registrada na cadeia de hash para o arquivo (ultima linha do manifest)"""
    u = None
    for ln in open(os.path.join(BASE, "manifest.jsonl"), encoding="utf-8"):
        r = json.loads(ln)
        if r["arquivo"] == arq:
            u = r["url"]
    return u

ROM = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX",
       "XXI","XXII","XXIII","XXIV","XXV","XXVI","XXVII","XXVIII","XXIX","XXX","XXXI","XXXII"]

def itens_lista(seg, n=None):
    """Itens numerados em romano ("I - ...; II - ..."). Divide por qualquer numeral romano seguido de hifen
    (tolera 'l'/'Il'/'Ill' por I, numeral repetido/errado, ';' faltando). Devolve (itens, numerais_lidos)."""
    pad = re.compile(r"(?:(?<=\s)|^)([IVXLl]{1,8}(?:-[A-Z])?)\s*[-–—]\s*")
    ms = list(pad.finditer(seg))
    itens, nums = [], []
    for k, m in enumerate(ms):
        fim = ms[k+1].start() if k+1 < len(ms) else len(seg)
        it = seg[m.end():fim].strip()
        it = re.sub(r"[;.,\s]+$", "", it)
        it = re.sub(r"\s+e$", "", it).strip()
        it = re.sub(r"[;.,\s]+$", "", it)
        itens.append(it); nums.append(m.group(1))
    if n is not None and len(itens) != n:
        raise ValueError("esperava %d itens, achei %d: %r" % (n, len(itens), nums))
    return itens, nums

def numeracao_ok(nums):
    """True se a numeracao lida e I..N sem erro (apos trocar l->I)"""
    lidos = [x.replace("l", "I") for x in nums if "-" not in x]   # ignora XII-A etc.
    return lidos == ROM[:len(lidos)]

def nome_min(it):
    it = it.strip()
    if it.startswith("Ministério") or it.startswith("Controladoria"):
        return it
    return "Ministério " + it

def art_lista(arq, ini, fim=None):
    """segmento de texto entre a regex ini (inclusive) e fim (exclusive)"""
    t = T(arq)
    m = re.search(R(ini), t)
    if not m:
        raise ValueError("ini nao achado %s: %s" % (arq, ini))
    if fim:
        e = re.search(R(fim), t[m.end():])
        return t[m.start(): m.end() + (e.start() if e else 4000)]
    return t[m.start(): m.start() + 4000]

MES = {"JANEIRO":1,"FEVEREIRO":2,"MARÇO":3,"MARCO":3,"ABRIL":4,"MAIO":5,"JUNHO":6,"JULHO":7,"AGOSTO":8,"SETEMBRO":9,"OUTUBRO":10,"NOVEMBRO":11,"DEZEMBRO":12}
def data_cab(arq):
    m = re.search(r"(?:MEDIDA PROVIS.RIA|LEI|LEI COMPLEMENTAR|DECRETO)\s*N.{1,3}\s*[\d\.\-]+\s*,?\s*DE\s+(\d+)[º°]?\s*DE\s+(\w+)\s*(?:DE\s*)?(\d{4})", T(arq), re.I)
    if not m: return None
    return "%s-%02d-%02d" % (m.group(3), MES[m.group(2).upper()], int(m.group(1)))
