"""Junta teto individual ANS, agrupamento (PDA-055), RPC (PDA-043) e IPCA (plano de saude, geral) em tabelas por ano e por janela.
Uso: python3 -I scripts/consolidar.py   (depois de construir_individual.py, construir_agrupamento.py, agregar_rpc.py)"""
import csv, json, sys, pathlib, hashlib
BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE/"scripts"))
from lib_estat import mediana, media_pond, mediana_pond
IPCA = BASE.parent/"ipca-itens-fase2/derivado"
def idx(nome):
    return {(int(r["ano"]), int(r["mes_ou_trimestre"])): float(r["valor"]) for r in csv.DictReader(open(IPCA/nome, encoding="utf8"))}
Ig, Ip = idx("indice_ipca_geral_dez1999_100.csv"), idx("indice_ipca_plano_saude_dez1999_100.csv")
Iteto = {(int(r["ano"]), int(r["mes_ou_trimestre"])): float(r["valor"]) for r in csv.DictReader(open(BASE/"derivado/indice_ans_teto_individual_dez1999_100.csv")) if r["ano"] != "1999"}
Iteto[(1999, 12)] = 100.0
teto = {int(r["ano"]): float(r["valor"]) for r in csv.DictReader(open(BASE/"series/ans_teto_individual_anual.csv"))}
agr = {}
for r in csv.DictReader(open(BASE/"derivado/agrupamento_por_ciclo.csv")):
    if r["tipo"] == "unico": agr[int(r["ciclo_inicio_maio"])] = r
R = json.load(open(BASE/"derivado/rpc_histogramas.json"))
def estat(ano, g, sem_zero=False):
    d = R["dados"].get(f"{ano}|{g}")
    if not d or not d["hist"]: return None
    h = {int(k): v for k, v in d["hist"].items() if not (sem_zero and int(k) == 0)}
    if not h: return None
    n = sum(v[0] for v in h.values()); b = sum(v[1] for v in h.values())
    # mediana por linha (contrato-plano comunicado)
    acc = 0; med = None
    for k in sorted(h):
        acc += h[k][0]
        if acc >= n/2: med = k/100; break
    pares = [(k/100, v[1]) for k, v in h.items()]
    big = sum(v[0] for k, v in h.items() if k > 10000)
    return {"n": n, "benef": b, "mediana": med, "media_pond": media_pond(pares), "mediana_pond": mediana_pond(pares), "n_pc_gt100": big,
            "negoc_excl": d["negoc_excluidas"], "parcelado": d["parcelado"], "benef_zero": d["benef_zero_ou_nulo"]}
def pct(a, b): return (a/b - 1)*100
def f(x, k=2): return "" if x is None else f"{x:.{k}f}"
GR = [("TODOS","todos"),("MED|TODOS","med"),("MED|AGRUP","med_agrup_lt30"),("MED|NAO_AGRUP","med_fora_agrup"),("MED|EMP|TODOS","med_empresarial"),("MED|ADE|TODOS","med_adesao"),("ODO|TODOS","odonto"),("SEM_JOIN|TODOS","sem_join")]
anos = range(2000, 2027)
linhas = []
for y in anos:
    ipca_ciclo = pct(Ip[(y+1, 4)], Ip[(y, 4)]) if (y+1, 4) in Ip else None
    ipca_ano = pct(Ip[(y, 12)], Ip[(y-1, 12)]) if (y, 12) in Ip else None
    ipcag_ano = pct(Ig[(y, 12)], Ig[(y-1, 12)]) if (y, 12) in Ig else None
    s = {g: estat(y, g) for g, _ in GR}
    a = agr.get(y)
    linhas.append([y, f(teto[y]), f(ipca_ciclo), f(ipca_ano), f(ipcag_ano),
                   f(float(a["mediana_simples_pct"])) if a else "", f(float(a["media_ponderada_benef_pct"])) if a else "",
                   *[(f(s[g]["mediana"]), f(s[g]["media_pond"]), s[g]["n"], s[g]["benef"]) if s[g] else ("", "", "", "") for g, _ in GR]])
cab = ["ano", "ans_teto_individual_ciclo_maio_ano_pct", "ipca_plano_saude_abr_ano_a_abr_ano_mais1_pct", "ipca_plano_saude_dez_dez_pct", "ipca_geral_dez_dez_pct",
       "agrupamento_pda055_mediana_operadoras_pct", "agrupamento_pda055_media_pond_benef_pct"]
for g in ["rpc_" + n for _, n in GR]: cab += [f"{g}_mediana_pct", f"{g}_media_pond_benef_pct", f"{g}_n_linhas", f"{g}_benef"]
with open(BASE/"derivado/tabela_por_ano.csv", "w", newline="", encoding="utf8") as fh:
    w = csv.writer(fh); w.writerow(cab)
    for l in linhas: w.writerow([l[0], *l[1:7], *[x for t in l[7:] for x in t]])
# RPC: series longas
vint = "bruto/ans/rpc/*.csv + bruto/ans/pda-043-rpc-201501.csv (hashes em manifest.jsonl); derivado/rpc_histogramas.json"
sl = []
for y in range(2005, 2027):
    for g, nome in GR:
        s = estat(y, g)
        if not s: continue
        defin = f"ANS RPC (PDA-043), reajustes comunicados pelas operadoras, inicio de aplicacao em {y}; grupo={nome}; exclui avisos de 'reajuste em negociacao'"
        for k, un, nt in (("mediana", "%", "mediana por linha (contrato x plano comunicado)"), ("media_pond", "%", "media ponderada por QT_BENEF_COMUNICADO"), ("mediana_pond", "%", "mediana ponderada por QT_BENEF_COMUNICADO"), ("n", "linhas", "linhas comunicadas"), ("benef", "beneficiarios", "soma de QT_BENEF_COMUNICADO")):
            sl.append([f"ans_rpc_{nome}_{k}", "ANS dados abertos PDA-043 Reajuste de Planos Coletivos", defin, y, "", f(s[k], 4) if isinstance(s[k], float) else s[k], un, nt, vint])
with open(BASE/"series/ans_rpc_coletivos_por_ano.csv", "w", newline="", encoding="utf8") as fh:
    w = csv.writer(fh); w.writerow(["indicador", "fonte", "definicao_linha", "ano", "mes_ou_trimestre", "valor", "unidade", "nota", "vintage"]); w.writerows(sl)
# indices compostos a partir de taxas anuais
def composto(taxas, base_ano):
    """base_ano = dezembro anterior ao primeiro ano COM dado; para no primeiro buraco."""
    ys = sorted(y for y, v in taxas.items() if v is not None)
    if not ys: return {}
    base = ys[0] - 1; I = {base: 100.0}
    for y in range(ys[0], max(ys) + 1):
        if taxas.get(y) is None: break
        I[y] = I[y-1]*(1+taxas[y]/100)
    return I
ind = {}
for g in ("TODOS", "MED|TODOS", "MED|AGRUP", "MED|NAO_AGRUP", "MED|EMP|TODOS", "MED|ADE|TODOS"):
    for k in ("mediana", "media_pond"):
        t = {}
        for y in range(2005, 2026):
            s = estat(y, g); t[y] = s[k] if s else None
        ind[(g, k)] = composto(t, 2004)
for g in ("MED|TODOS", "MED|AGRUP", "MED|NAO_AGRUP"):
    t = {}
    for y in range(2005, 2026):
        e = estat(y, g, sem_zero=True); t[y] = e["media_pond"] if e else None
    ind[(g, "media_pond_SEM_ZEROS")] = composto(t, 2004)
ind[("PDA055", "media_pond")] = composto({y: float(agr[y]["media_ponderada_benef_pct"]) for y in agr}, 2012)
ind[("PDA055", "mediana")] = composto({y: float(agr[y]["mediana_simples_pct"]) for y in agr}, 2012)
with open(BASE/"derivado/indices_compostos_coletivos.csv", "w", newline="", encoding="utf8") as fh:
    w = csv.writer(fh); w.writerow(["serie", "estatistica", "base_dez_do_ano", "ano", "indice", "nota"])
    for (g, k), I in ind.items():
        for y, v in sorted(I.items()):
            w.writerow([g, k, min(I), y, f"{v:.4f}", "I(ano)=I(ano-1)*(1+taxa do ano/100); taxa do ano = estatistica dos reajustes com INICIO de aplicacao no ano; ordem de grandeza, nao preco pago"])
# janelas
def jan(a, b):
    r = {"janela": f"dez/{a}-dez/{b}", "ans_teto_individual_composto_pct": pct(Iteto[(b, 12)], Iteto[(a, 12)]), "ipca_plano_saude_pct": pct(Ip[(b, 12)], Ip[(a, 12)]), "ipca_geral_pct": pct(Ig[(b, 12)], Ig[(a, 12)])}
    for (g, k), I in ind.items():
        if a in I and b in I: r[f"coletivos_{g.replace(chr(124),chr(95))}_{k}_composto_pct"] = pct(I[b], I[a])
    return r
J = [jan(1999, 2024), jan(2001, 2024), jan(2004, 2024), jan(2012, 2024), jan(2014, 2024), jan(2018, 2022)]
cols = sorted({k for r in J for k in r}, key=lambda k: (k != "janela", k))
with open(BASE/"derivado/acumulados_janelas_ans.csv", "w", newline="", encoding="utf8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
    for r in J: w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})
for r in J: print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
