"""Quarta rodada: SGS 13621 (reservas, conceito caixa, diaria) para decidir se 3546 e caixa ou liquidez."""
import subprocess, os, sys, time
from pathlib import Path
PASTA = Path(__file__).resolve().parent.parent
REPO = "/Users/ulissesflores/Developer/brazil-governments-factcheck"
SGS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{c}/dados?formato=json"
CKAN = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?rows=5&q=codigo_sgs%3A{c}"
env = dict(os.environ, PYTHONPATH=REPO + "/code")
def add(url, dest, nota):
    r = subprocess.run([sys.executable, "-m", "govfc.chain", "add", str(PASTA), url, str(PASTA / dest), "--nota", nota],
                       capture_output=True, text=True, cwd=REPO, env=env)
    print(dest, "OK" if r.returncode == 0 else "FALHA " + (r.stderr or r.stdout)[-300:], flush=True)
    time.sleep(0.5)
add(CKAN.format(c=13621), "bruto/ckan_13621.json", "metadados CKAN do SGS 13621")
for a, b, tag in [("01/01/1998", "31/12/2007", "1998-2007"), ("01/01/2008", "31/12/2017", "2008-2017"), ("01/01/2018", "20/10/2026", "2018-2026")]:
    add(SGS.format(c=13621) + f"&dataInicial={a}&dataFinal={b}", f"bruto/sgs_13621_{tag}.json", f"SGS 13621 (reservas, conceito caixa, diaria) janela {tag}; serve so para conferir o conceito de 3546")
