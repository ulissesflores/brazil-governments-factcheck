"""Baixa (sequencial, com a cadeia de hash) os textos legais e documentos de apoio de moeda-fiscal.
Uso: python3 -I baixar_2_planalto.py  (rede). Le a lista de scripts/alvos_2.tsv: destino<TAB>url"""
import json, subprocess, sys, time
from pathlib import Path
PASTA = Path(__file__).resolve().parent.parent
CHAIN = "/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py"
FORCAR = len(sys.argv) > 2 and sys.argv[2] == 'forcar'  # rebaixa mesmo se ja esta na cadeia (linha nova; a antiga fica)
feitos = set()
man = PASTA / "manifest.jsonl"
if man.exists():
    for l in man.read_text(encoding="utf-8").splitlines():
        feitos.add(json.loads(l)["arquivo"])
alvos = [l.split("\t") for l in (Path(__file__).parent / (sys.argv[1] if len(sys.argv) > 1 else "alvos_2.tsv")).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
for i, (dest, url) in enumerate(alvos, 1):
    if dest in feitos and (PASTA / dest).exists() and not FORCAR:
        continue
    r = subprocess.run(["python3", "-I", CHAIN, "add", str(PASTA), url.strip(), dest.strip()], capture_output=True, text=True)
    print(i, len(alvos), dest, "OK" if r.returncode == 0 else "FALHA " + (r.stderr or r.stdout)[-200:], flush=True)
    time.sleep(0.5)
