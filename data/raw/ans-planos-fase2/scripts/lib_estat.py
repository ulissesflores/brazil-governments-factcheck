def mediana(v):
    v = sorted(v); n = len(v)
    if n == 0: return None
    return v[n//2] if n % 2 else (v[n//2-1] + v[n//2]) / 2
def media_pond(pares):
    """pares = [(valor, peso)] ; peso<=0 ignorado"""
    s = sum(w for _, w in pares if w > 0)
    return None if s == 0 else sum(x*w for x, w in pares if w > 0) / s
def mediana_pond(pares):
    p = sorted((x, w) for x, w in pares if w > 0); tot = sum(w for _, w in p)
    if tot == 0: return None
    acc = 0
    for x, w in p:
        acc += w
        if acc >= tot/2: return x
