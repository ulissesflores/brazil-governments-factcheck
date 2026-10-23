# Metadados CKAN (dadosabertos.bcb.gov.br): confirma o NOME e o campo codigo_sgs de cada serie SGS.
# Salva a resposta bruta de package_search (q=codigo_sgs:<cod>) em bruto/ckan_<cod>.json.
# Uso: python3 baixar_ckan.py cod1 cod2 ...   (tem rede; os scripts de analise NAO tem)
import json, sys, time, urllib.parse, urllib.request, pathlib
out = pathlib.Path(__file__).parent / "bruto"; out.mkdir(exist_ok=True)
for c in sys.argv[1:]:
    if (out / f"ckan_{c}.json").exists(): print(c, "ja existe (nao sobrescrevo: esta no manifest)"); continue
    u = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?rows=5&q=" + urllib.parse.quote(f"codigo_sgs:{c}")
    raw = None
    for t in range(6):
        try:
            raw = urllib.request.urlopen(u, timeout=40).read(); json.loads(raw); break
        except Exception: raw = None; time.sleep(2 + t)
    if not raw: print(c, "FALHOU"); continue
    res = [r for r in json.loads(raw)["result"]["results"] if str(r.get("codigo_sgs")) == c]
    if not res: print(c, "SEM PACOTE com codigo_sgs =", c); continue
    (out / f"ckan_{c}.json").write_bytes(raw)
    print(c, "|", res[0]["title"], "|", {k: res[0].get(k) for k in ("periodicidade", "unidade_medida", "data_inicio_serie", "data_fim_serie") if k in res[0]})
