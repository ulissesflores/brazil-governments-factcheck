"""Baixa metadados CKAN e bruto SGS das series BCB da fase 2, via cadeia de hash (govfc.chain add)."""
import subprocess, os, sys, time
from pathlib import Path
PASTA = Path(__file__).resolve().parent.parent
REPO = "/Users/ulissesflores/Developer/brazil-governments-factcheck"
SGS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{c}/dados?formato=json"
CKAN = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?rows=5&q=codigo_sgs%3A{c}"
codes = [4513, 13762, 4537, 29037, 29038, 29034, 29035, 19882, 19881, 3546]
env = dict(os.environ, PYTHONPATH=REPO + "/code")
def add(url, dest, nota):
    r = subprocess.run([sys.executable, "-m", "govfc.chain", "add", str(PASTA), url, str(PASTA / dest), "--nota", nota],
                       capture_output=True, text=True, cwd=REPO, env=env)
    print(dest, "OK" if r.returncode == 0 else "FALHA " + (r.stderr or r.stdout)[-300:], flush=True)
for c in codes:
    add(CKAN.format(c=c), f"bruto/ckan_{c}.json", f"metadados CKAN do SGS {c}")
    time.sleep(0.5)
for c in codes:
    add(SGS.format(c=c), f"bruto/sgs_{c}.json", f"serie completa SGS {c}, sem janela")
    time.sleep(0.5)
