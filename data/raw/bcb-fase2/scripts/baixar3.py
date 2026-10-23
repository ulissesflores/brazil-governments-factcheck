"""Repeticao unica dos metadados CKAN que vieram vazios (3546, 19881, 19882) ou invalidos (4471)."""
import subprocess, os, sys, time
from pathlib import Path
PASTA = Path(__file__).resolve().parent.parent
REPO = "/Users/ulissesflores/Developer/brazil-governments-factcheck"
CKAN = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?rows=5&q=codigo_sgs%3A{c}"
env = dict(os.environ, PYTHONPATH=REPO + "/code")
for c in (4471, 3546, 19881, 19882):
    r = subprocess.run([sys.executable, "-m", "govfc.chain", "add", str(PASTA), CKAN.format(c=c), str(PASTA / f"bruto/ckan_{c}_repeticao.json"), "--nota", f"repeticao unica do CKAN {c} (primeira tentativa vazia ou invalida)"],
                       capture_output=True, text=True, cwd=REPO, env=env)
    print(c, "OK" if r.returncode == 0 else "FALHA " + (r.stderr or r.stdout)[-300:], flush=True)
    time.sleep(1)
