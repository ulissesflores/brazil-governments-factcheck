"""Coleta (COM rede) de tabelas do TabNet/DATASUS por POST e registro na cadeia de hash.
Uso: python3 coletar_tabnet.py   (grava em ../seguranca/bruto e chama manifest_tool add-local)."""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tabnet_lib import post
BASE = Path(__file__).resolve().parent.parent / "seguranca"
TOOL = "/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py"
y10 = [f"{{}}br{y%100:02d}.dbf" for y in range(1996, 2025)]
y09 = [f"{{}}br{y%100:02d}.dbf" for y in range(1979, 1996)]
JOBS = [
 ("tabnet_ext10_grupo_ano.html", "sim/cnv/ext10br.def", "Grupo_CID10", "Ano_do_Óbito", "ext", y10),
 ("tabnet_ext09_grupo_ano.html", "sim/cnv/ext09br.def", "Grupo_CID9", "Ano_do_Óbito", "ext", y09),
 ("tabnet_obt10_capitulo_ano.html", "sim/cnv/obt10br.def", "Capítulo_CID-10", "Ano_do_Óbito", "obt", y10),
 ("tabnet_obt09_capitulo_ano.html", "sim/cnv/obt09br.def", "Capítulo_CID-9", "Ano_do_Óbito", "obt", y09),
 ("tabnet_ext10_categoria_ano.html", "sim/cnv/ext10br.def", "Categoria_CID10", "Ano_do_Óbito", "ext", y10),
 ("tabnet_ext09_categoria_ano.html", "sim/cnv/ext09br.def", "Categoria_CID9", "Ano_do_Óbito", "ext", y09),
]
for nome, path, lin, col, pref, arqs in JOBS:
    corpo = post(path, lin, col, "Óbitos_p/Residênc", [a.format(pref) for a in arqs])
    alvo = BASE / "bruto" / nome
    alvo.write_bytes(corpo)
    url = f"http://tabnet.datasus.gov.br/cgi/tabcgi.exe?{path} [POST Linha={lin}; Coluna={col}; Incremento=Óbitos_p/Residênc; Arquivos={arqs[0].format(pref)}..{arqs[-1].format(pref)}; formato=prn]"
    subprocess.run(["python3", "-I", TOOL, "add-local", str(BASE), str(alvo), "--url", url, "--nota", "baixado agora por POST (timestamp = mtime do arquivo recem-gravado); parametros na url"], check=True)
