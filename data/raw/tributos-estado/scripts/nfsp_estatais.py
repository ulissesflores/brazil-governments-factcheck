# NFSP das empresas estatais: BCB SGS (anual por soma de fluxos mensais ou por dezembro de series acumuladas em 12 meses) e Ipeadata. So le bruto. python3 -I nfsp_estatais.py
import csv, glob, json, re
from collections import defaultdict
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]
CONV = "convencao do BCB: positivo = necessidade de financiamento (deficit); negativo = superavit (conferido em 5793: 2015 = +1,86 e 2008 = -3,33 % do PIB)"

def sgs(code):
    out = {}
    for f in sorted(glob.glob(str(RAIZ / ("bruto/bcb-sgs/sgs%s-*.json" % code)))):
        t = Path(f).read_text()
        if not t.startswith("["):
            continue
        for r in json.loads(t):
            d, m, y = r["data"].split("/")
            out[(int(y), int(m))] = float(r["valor"])
    return out

def vint(code):
    fs = sorted(glob.glob(str(RAIZ / ("bruto/bcb-sgs/sgs%s-*.json" % code))))
    ts = sorted(man[str(Path(f).relative_to(RAIZ))]["timestamp_utc"][:10] for f in fs if str(Path(f).relative_to(RAIZ)) in man)
    return "BCB SGS %s, baixado %s" % (code, ts[-1] if ts else "?")

NOMES = {"4645": "empresas estatais (total)", "4646": "empresas estatais federais", "4647": "empresas estatais estaduais", "4648": "empresas estatais municipais",
         "4579": "empresas estatais (total)", "4580": "empresas estatais federais", "4581": "empresas estatais estaduais", "4582": "empresas estatais municipais"}
rows = []
for code, nome in NOMES.items():
    tipo = "resultado primario" if code.startswith("464") else "resultado nominal"
    s = sgs(code)
    for y in sorted({k[0] for k in s}):
        ms = [m for (yy, m) in s if yy == y]
        completo = len(ms) == 12
        v = round(sum(s[(y, m)] for m in ms), 2)
        rows.append(("nfsp_%s_%s_rs_mi" % ("primario" if tipo.endswith("primario") else "nominal", nome.split("(")[0].strip().replace(" ", "_")), "BCB SGS %s" % code,
                     "NFSP sem desvalorizacao cambial, %s, %s, soma dos fluxos mensais do ano" % (tipo, nome), y, v, "R$ milhoes correntes",
                     "%s; %s" % (CONV, "ano completo" if completo else "ANO INCOMPLETO: %d meses" % len(ms)), vint(code)))
PIB = {"5789": ("resultado primario", "empresas estatais (total)"), "5790": ("resultado primario", "empresas estatais federais"), "5791": ("resultado primario", "empresas estatais estaduais"), "5792": ("resultado primario", "empresas estatais municipais"),
       "5723": ("resultado nominal", "empresas estatais (total)"), "5724": ("resultado nominal", "empresas estatais federais"), "5725": ("resultado nominal", "empresas estatais estaduais"), "5726": ("resultado nominal", "empresas estatais municipais")}
for code, (tipo, nome) in PIB.items():
    s = sgs(code)
    for (y, m), v in sorted(s.items()):
        if m == 12:
            rows.append(("nfsp_%s_%s_pct_pib" % ("primario" if tipo.endswith("primario") else "nominal", nome.split("(")[0].strip().replace(" ", "_")), "BCB SGS %s" % code, "NFSP sem desvalorizacao cambial, %s, %s, acumulado em 12 meses (valor de dezembro), %% do PIB" % (tipo, nome), y, v, "% do PIB", CONV, vint(code)))
DLSP = {"4474": "empresas estatais (total)", "4475": "empresas estatais federais", "4476": "empresas estatais estaduais", "4477": "empresas estatais municipais"}
for code, nome in DLSP.items():
    s = sgs(code)
    for (y, m), v in sorted(s.items()):
        if m == 12:
            rows.append(("dlsp_saldo_%s_rs_mi" % nome.split("(")[0].strip().replace(" ", "_"), "BCB SGS %s" % code, "Divida liquida do setor publico, saldo em dezembro, %s" % nome, y, v, "R$ milhoes correntes", "saldo; sinal: positivo = divida liquida", vint(code)))
# Ipeadata (series do BCB repassadas), mensais; soma anual
for c, tipo in (("BM12_NFEEPNS12", "primario"), ("BM12_NFEENNS12", "nominal")):
    f = RAIZ / ("bruto/ipeadata/%s.json" % c)
    if not f.exists():
        continue
    d = json.loads(f.read_text())["value"]
    s = defaultdict(dict)
    for r in d:
        if r["VALVALOR"] is None:
            continue
        s[int(r["VALDATA"][:4])][int(r["VALDATA"][5:7])] = r["VALVALOR"]
    # ANOMALIA: 10 linhas datadas de 1953-12 a 1954-09 (implausivel para uma serie do BCB que comeca em 2001-12): ficam FORA da agregacao anual
    for y in sorted(k for k in s if k >= 2001):
        completo = len(s[y]) == 12
        rows.append(("ipeadata_nfsp_estatais_%s_rs_mi" % tipo, "Ipeadata %s (Bacen/Notas Imprensa/F. Pub.)" % c, "NFSP estatais, %s, sem desvalorizacao cambial, soma dos fluxos mensais do ano; repassa serie do BCB em outra vintage e outro inicio que o SGS 4645" % tipo, y, round(sum(s[y].values()), 2), "R$ milhoes correntes", "%s; %s" % (CONV, "ano completo" if completo else "ANO INCOMPLETO: %d meses" % len(s[y])), "Ipeadata %s baixado %s" % (c, man["bruto/ipeadata/%s.json" % c]["timestamp_utc"][:10])))
with open(RAIZ / "series/nfsp-estatais-bcb.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(COLS); w.writerows(rows)
print(len(rows))
