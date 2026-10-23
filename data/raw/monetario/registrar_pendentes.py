# Registra no manifest.jsonl os brutos de bruto/ que baixar.py / baixar_ckan.py salvaram ANTES de passar pelo manifest.
# Cada um entra como "metadata reconstruida" (timestamp = mtime). Nao reescreve nem remove nada: so appenda.
import importlib.util, json, pathlib, urllib.parse
aqui = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("mt", aqui.parent / "manifest_tool.py"); mt = importlib.util.module_from_spec(spec); spec.loader.exec_module(mt)
man = aqui / "manifest.jsonl"
ja = {json.loads(l)["arquivo"] for l in man.read_text().splitlines()} if man.exists() else set()
def url(nome):
    n = nome[:-5]
    if n.startswith("bcb_sgs_"): return f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{n[8:]}/dados?formato=json"
    if n.startswith("ckan_"): return "https://dadosabertos.bcb.gov.br/api/3/action/package_search?rows=5&q=" + urllib.parse.quote(f"codigo_sgs:{n[5:]}")
    if n.startswith("ipea_"): return f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{n[5:]}')"
    return ""
for f in sorted((aqui / "bruto").glob("*.json")):
    rel = f.relative_to(aqui).as_posix()
    if rel in ja: continue
    mt.registrar_local(aqui, f, url=url(f.name), nota="metadata reconstruida: baixado por baixar.py/baixar_ckan.py (curl/urllib, HTTP 200, JSON valido) antes de passar pelo manifest; timestamp = mtime do arquivo")
    print("registrado", rel)
