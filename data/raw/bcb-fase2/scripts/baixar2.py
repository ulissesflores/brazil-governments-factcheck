"""Segunda rodada: confirmacao do conceito de 3546 (reservas liquidez diaria 13982), DLSP R$ mi 1991+ (4468, 4471), nota oficial de 2008."""
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
for c in (13982, 4468, 4471, 29029):
    add(CKAN.format(c=c), f"bruto/ckan_{c}.json", f"metadados CKAN do SGS {c}")
for c in (4468, 4471, 29029):
    add(SGS.format(c=c), f"bruto/sgs_{c}.json", f"serie completa SGS {c}, sem janela")
for a, b, tag in [("01/01/2008", "31/12/2017", "2008-2017"), ("01/01/2018", "20/10/2026", "2018-2026")]:
    add(SGS.format(c=13982) + f"&dataInicial={a}&dataFinal={b}", f"bruto/sgs_13982_{tag}.json", f"SGS 13982 (reservas, conceito liquidez, diaria) janela {tag}; serve so para conferir o conceito de 3546")
add("https://www.bcb.gov.br/htms/relinf/port/2008/03/ri200803b4p.pdf", "bruto/doc_ri_2008_03_boxe_dbgg.pdf", "Relatorio de Inflacao mar/2008, boxe Alteracao na Metodologia de Calculo da DBGG (fonte primaria da mudanca de 2008)")
add("https://www.bcb.gov.br/htms/infecon/seriehistDLSPBruta2007.asp", "bruto/doc_seriehistDLSPBruta2007.html", "pagina do BCB da serie DBGG no conceito ate 2007")
