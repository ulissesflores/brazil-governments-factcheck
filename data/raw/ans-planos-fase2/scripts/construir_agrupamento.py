"""ANS PDA-055: percentuais de reajuste do agrupamento de contratos coletivos (<30 vidas), por ciclo (maio-abril), 2013-2025.
Estatisticas por ciclo sobre operadoras (Unico): mediana simples, media ponderada por beneficiarios do agrupamento, mediana ponderada.
Confere contra as planilhas xlsx da ANS (pool de risco) em 2013 e 2016.  Uso: python3 -I scripts/construir_agrupamento.py"""
import csv, sys, pathlib, hashlib, collections
BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE/"scripts"))
from lib_estat import mediana, media_pond, mediana_pond
from xlsx_lib import ler_xlsx
F = BASE/"bruto/ans/pda-055-Percentuais_de_Reajuste_de_Agrupamento.csv"
sha = hashlib.sha256(F.read_bytes()).hexdigest()[:12]
VINT = f"bruto/ans/pda-055-Percentuais_de_Reajuste_de_Agrupamento.csv sha256 {sha}"
def f(x): return float(x.replace(",", ".")) if x.strip() else None
rows = list(csv.DictReader(open(F, encoding="utf8"), delimiter=";"))
por = collections.defaultdict(lambda: collections.defaultdict(list))
for r in rows:
    c = int(r["CICLO"]); w = f(r["QT_BENEF"]) or 0
    if r["TP_AGRUPAMENTO"].startswith("Ú") or r["TP_AGRUPAMENTO"].lower().startswith("u") or "nico" in r["TP_AGRUPAMENTO"]:
        v = f(r["PCT_UNICO"])
        if v is not None: por[c]["unico"].append((v, w, int(f(r["QT_CONTRATOS"]) or 0)))
    else:
        for k, col in (("sub_ambulatorial","PCT_AMBULATORIAL"),("sub_int_sem_obstetricia","PCT_INT_SEM_OBSTET"),("sub_int_com_obstetricia","PCT_INT_COM_OBSTET")):
            v = f(r[col])
            if v is not None: por[c][k].append((v, w, int(f(r["QT_CONTRATOS"]) or 0)))
out = []; der = []
for c in sorted(por):
    for k, L in por[c].items():
        vals = [x for x, _, _ in L]
        pares = [(x, w) for x, w, _ in L]
        stats = {"n_operadoras": len(L), "mediana_simples_pct": mediana(vals), "media_ponderada_benef_pct": media_pond(pares), "mediana_ponderada_benef_pct": mediana_pond(pares), "benef_total": sum(w for _, w, _ in L), "contratos_total": sum(n for _, _, n in L)}
        der.append([c, k] + [("" if v is None else (f"{v:.4f}" if isinstance(v, float) else v)) for v in stats.values()])
        for nome, v in stats.items():
            if v is None: continue
            out.append([f"ans_agrupamento_{k}_{nome}", "ANS dados abertos PDA-055 (agrupamento de contratos coletivos com menos de 30 beneficiarios)",
                        f"ciclo maio/{c} a abril/{c+1}; TP_AGRUPAMENTO={'Unico' if k=='unico' else 'Subagrupado: '+k}; estatistica sobre operadoras",
                        c, 5, f"{v:.4f}" if isinstance(v, float) else v, "%" if nome.endswith("_pct") else ("beneficiarios" if nome.startswith("benef") else "contagem"),
                        "ponderacao = QT_BENEF (beneficiarios no agrupamento da operadora); mediana_simples = uma observacao por operadora", VINT])
with open(BASE/"series/ans_agrupamento_pda055.csv","w",newline="",encoding="utf8") as fh:
    w = csv.writer(fh); w.writerow(["indicador","fonte","definicao_linha","ano","mes_ou_trimestre","valor","unidade","nota","vintage"]); w.writerows(out)
with open(BASE/"derivado/agrupamento_por_ciclo.csv","w",newline="",encoding="utf8") as fh:
    w = csv.writer(fh); w.writerow(["ciclo_inicio_maio","tipo","n_operadoras","mediana_simples_pct","media_ponderada_benef_pct","mediana_ponderada_benef_pct","benef_total","contratos_total"]); w.writerows(der)
# conferencia contra as planilhas xlsx da ANS
def conf(arq, ciclo, colreaj, colben):
    d = ler_xlsx(BASE/"bruto/ans/pool-de-risco"/arq); aba = next(a for a, l in d.items() if len(l) > 10)
    x = {}
    for l in d[aba]:
        a = l.get("A", "")
        if a.strip().isdigit() and l.get(colreaj,'-').strip() not in ('-',''): x[(a.strip().zfill(6), l.get("C","").strip().upper().replace("Ú","U"))] = (float(l[colreaj].replace(',', '.')), float((l.get(colben, '0') or '0').replace(',', '.')))
    ok = tot = 0; dif = []
    for r in rows:
        if int(r["CICLO"]) != ciclo or "nico" not in r["TP_AGRUPAMENTO"]: continue
        k = (r["REGISTRO_OPERADORA"].zfill(6), "UNICO")
        if k in x:
            tot += 1
            if abs(x[k][0] - f(r["PCT_UNICO"])) < 0.006: ok += 1
            else: dif.append((k, x[k][0], f(r["PCT_UNICO"])))
    return ok, tot, dif[:3], len([1 for r in rows if int(r["CICLO"]) == ciclo and "nico" in r["TP_AGRUPAMENTO"]]), len(x)
print("conf 2013:", conf("tabela-reajustes-pool-de-risco-2013_2014.xlsx", 2013, "D", "E"))
print("conf 2016:", conf("planilha-pool-de-risco_2016-2017.xlsx", 2016, "D", "F"))
print("conf 2022:", conf("Maio_de_2022__Abril_de_2023.xlsx", 2022, "D", "F"))
for r in der:
    if r[1] == "unico": print(r)
