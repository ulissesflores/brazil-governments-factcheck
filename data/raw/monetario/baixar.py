# Baixa o BRUTO (JSON) do BCB SGS e do Ipeadata para bruto/. Tem rede; os scripts de analise (analisar_*.py) nao tem.
# BCB: https://api.bcb.gov.br/dados/serie/bcdata.sgs.<cod>/dados?formato=json   (sem janela: serie inteira; API intermitente -> retry)
# Ipea: http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='<cod>')
import json, sys, time, urllib.request, pathlib, concurrent.futures as cf
out = pathlib.Path(__file__).parent / "bruto"; out.mkdir(exist_ok=True)
BCB = sys.argv[1].split(",") if len(sys.argv) > 1 and sys.argv[1] else []
IPEA = sys.argv[2].split(",") if len(sys.argv) > 2 and sys.argv[2] else []
def job(kind, c):
    f = out / (f"bcb_sgs_{c}.json" if kind == "bcb" else f"ipea_{c}.json")
    if f.exists() and f.stat().st_size > 5:
        return kind, c, "ja existe"
    u = (f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{c}/dados?formato=json" if kind == "bcb"
         else f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{c}')")
    for t in range(8):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
            j = json.loads(raw)
            n = len(j if kind == "bcb" else j["value"])
            f.write_bytes(raw); return kind, c, f"ok n={n} bytes={len(raw)}"
        except Exception as e:
            err = str(e)[:60]; time.sleep(2 + 2 * t)
    return kind, c, "FALHOU " + err
with cf.ThreadPoolExecutor(6) as ex:
    futs = [ex.submit(job, "bcb", c) for c in BCB] + [ex.submit(job, "ipea", c) for c in IPEA]
    for fu in cf.as_completed(futs): print(*fu.result(), flush=True)
