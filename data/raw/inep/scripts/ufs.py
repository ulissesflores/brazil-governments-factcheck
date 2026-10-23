"""Normaliza nomes de UF (com variacoes de grafia do INEP) para sigla."""
import re, unicodedata

SIGLAS = {
    "RO": "Rondônia", "AC": "Acre", "AM": "Amazonas", "RR": "Roraima", "PA": "Pará", "AP": "Amapá",
    "TO": "Tocantins", "MA": "Maranhão", "PI": "Piauí", "CE": "Ceará", "RN": "Rio Grande do Norte",
    "PB": "Paraíba", "PE": "Pernambuco", "AL": "Alagoas", "SE": "Sergipe", "BA": "Bahia",
    "MG": "Minas Gerais", "ES": "Espírito Santo", "RJ": "Rio de Janeiro", "SP": "São Paulo",
    "PR": "Paraná", "SC": "Santa Catarina", "RS": "Rio Grande do Sul", "MS": "Mato Grosso do Sul",
    "MT": "Mato Grosso", "GO": "Goiás", "DF": "Distrito Federal",
}
UFS = list(SIGLAS)
REGIAO = {
    "Norte": ["RO", "AC", "AM", "RR", "PA", "AP", "TO"],
    "Nordeste": ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"],
    "Sudeste": ["MG", "ES", "RJ", "SP"],
    "Sul": ["PR", "SC", "RS"],
    "Centro-Oeste": ["MS", "MT", "GO", "DF"],
}


def _k(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]", "", s)


_MAP = {_k(v): k for k, v in SIGLAS.items()}
_MAP.update({_k(k): k for k in SIGLAS})
_MAP.update({
    "rgdonorte": "RN", "rgdosul": "RS", "mgdosul": "MS", "mtgrossodosul": "MS", "matogrossodosul": "MS",
    "riograndedonorte": "RN", "riograndedosul": "RS", "distritofederal": "DF", "brasil": "BR",
    "matogrosso": "MT", "mgrossodosul": "MS",
})
for r in REGIAO:
    _MAP[_k(r)] = "REG:" + r
_MAP["centrooeste"] = "REG:Centro-Oeste"


def uf(nome):
    """Sigla da UF, 'BR' para Brasil, 'REG:<regiao>' para regiao, ou None."""
    return _MAP.get(_k(nome or ""))
