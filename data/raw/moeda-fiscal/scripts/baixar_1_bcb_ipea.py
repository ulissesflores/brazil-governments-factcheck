"""Baixa (sequencial, com a cadeia de hash do chain.py) as series SGS, CKAN e Ipeadata da pasta moeda-fiscal.
Uso: python3 -I baixar_1_bcb_ipea.py   (rede; unico script desta pasta que usa rede para BCB/Ipeadata)
Cada arquivo vai para a cadeia via `chain.py add`; falha apos 4 tentativas do chain.py = registra no log e segue."""
import subprocess, sys, time
from pathlib import Path
PASTA = Path(__file__).resolve().parent.parent
CHAIN = "/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py"
SGS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{c}/dados?formato=json"
CKAN = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?rows=5&q=codigo_sgs%3A{c}"
IPEA = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{c}')"
IPEAMETA = "http://www.ipeadata.gov.br/api/odata4/Metadados('{c}')"

jobs = []
# Selic, inflacao, credito, compulsorios
sgs_full = [4390, 433, 190, 20622, 20625, 20628, 28215, 28217, 28867, 28868,
            17633, 1849, 1848, 1850, 1797, 1828, 17624, 17625]
# NFSP % PIB acum 12m (nominal 5717-27, juros 5750-60, primario 5783-93); fluxo mensal R$ (nominal 4573-83, juros 4606-16, primario 4639-49)
nfsp = list(range(5717, 5728)) + list(range(5750, 5761)) + list(range(5783, 5794)) \
     + list(range(4573, 4584)) + list(range(4606, 4617)) + list(range(4639, 4650))
for c in sgs_full + nfsp + [432]:
    jobs.append((CKAN.format(c=c), f"bruto/bcb/ckan_{c}.json"))
for c in sgs_full + nfsp:
    jobs.append((SGS.format(c=c), f"bruto/bcb/sgs_{c}.json"))
# 432 (meta Selic, diaria): janelas de 10 anos
for a, b, tag in [("01/01/1996", "31/12/2005", "1996-2005"), ("01/01/2006", "31/12/2015", "2006-2015"), ("01/01/2016", "20/10/2026", "2016-2026")]:
    jobs.append((SGS.format(c=432) + f"&dataInicial={a}&dataFinal={b}", f"bruto/bcb/sgs_432_{tag}.json"))
for c in ["BM12_TJOVER12", "PAN12_TJOVER12", "BM366_TJOVER366"]:
    jobs.append((IPEA.format(c=c), f"bruto/ipea/{c}.json"))
    jobs.append((IPEAMETA.format(c=c), f"bruto/ipea/{c}_metadados.json"))

feitos = set()
man = PASTA / "manifest.jsonl"
if man.exists():
    import json
    for l in man.read_text().splitlines():
        feitos.add(json.loads(l)["arquivo"])
for i, (url, dest) in enumerate(jobs, 1):
    if dest in feitos and (PASTA / dest).exists():
        continue
    r = subprocess.run(["python3", "-I", CHAIN, "add", str(PASTA), url, dest], capture_output=True, text=True)
    print(i, len(jobs), dest, "OK" if r.returncode == 0 else "FALHA " + (r.stderr or r.stdout)[-200:], flush=True)
    time.sleep(0.5)
