#!/usr/bin/env python3
"""Constroi series/ e derivado/ a partir de bruto/ (somente o que foi baixado pela cadeia de hash).

Nada estimado, nada interpolado: se um mes falta ou nao e numerico, o script para.
Roda com: python3 -I construir.py
"""
import csv
import json
import sys
from pathlib import Path

P = Path("/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/ipca-itens-fase2")
COLS = ["indicador", "fonte", "definicao_linha", "ano", "mes_ou_trimestre", "valor", "unidade", "nota", "vintage"]

# vintage = arquivo + instante do download + 12 primeiros hex do sha256, lidos do manifest da cadeia
MAN = {}
for ln in (P / "manifest.jsonl").read_text().splitlines():
    r = json.loads(ln)
    MAN[r["arquivo"].replace(str(P) + "/", "")] = r  # a ultima linha vence; manifest guarda caminho absoluto


def vint(arq):
    r = MAN[arq]
    return f"{arq} adquirido {r['timestamp_utc']} sha256 {r['sha256'][:12]}"


NOME = {"7169": "geral", "2640": "geral", "7448": "aluguel_residencial", "1935": "aluguel_residencial", "7696": "plano_saude"}
DEF = {
    "geral": "IPCA - Indice geral",
    "aluguel_residencial": "IPCA - subitem 2101001 Aluguel residencial",
    "plano_saude": "IPCA - subitem 6203001 Plano de saude",
}
VAR = {"63": ("var_mensal", "%", "variacao mensal"), "66": ("peso_mensal", "%", "peso mensal"),
       "2265": ("acum_12m", "%", "variacao acumulada em 12 meses")}

# (arquivo bruto, tabela SIDRA, classificacao)
SIDRA = [
    ("bruto/ibge/sidra-58-v63.json", "58", "c72"),
    ("bruto/ibge/sidra-655-v63.json", "655", "c315"),
    ("bruto/ibge/sidra-656-v66.json", "656", "c315"),
    ("bruto/ibge/sidra-2938-v63-66.json", "2938", "c315"),
    ("bruto/ibge/sidra-1419-v63-66-2265.json", "1419", "c315"),
    ("bruto/ibge/sidra-7060-v63-66-2265.json", "7060", "c315"),
]

SIMB = {}
dados = {}  # (indicador_base, tabela) -> {(ano, mes): float}
log = []
for arq, tab, cls in SIDRA:
    rows = json.loads((P / arq).read_text())[1:]
    ags = {}
    for r in rows:
        v = r["V"]
        try:
            x = float(v)
        except ValueError:
            if v not in ("-", "..."):
                sys.exit(f"valor nao numerico inesperado em {arq}: {r}")
            x = None  # simbolo SIDRA preservado em SIMB; nada e preenchido
            SIMB[(NOME[r["D4C"]], r["D2C"], tab, r["D3C"])] = v
        item = r["D4C"]
        var = r["D2C"]
        ano, mes = int(r["D3C"][:4]), int(r["D3C"][4:])
        ags.setdefault((NOME[item], var), {})[(ano, mes)] = x
    for (nm, var), ser in ags.items():
        meses = sorted(ser)
        # contiguidade: nenhum mes faltando entre o primeiro e o ultimo
        esp = []
        a, m = meses[0]
        while (a, m) <= meses[-1]:
            esp.append((a, m))
            m += 1
            if m == 13:
                a, m = a + 1, 1
        falt = [k for k in esp if k not in ser]
        if falt:
            if tab != "58":
                sys.exit(f"meses faltando em {arq} {nm} {var}: {falt[:5]}")
            log.append(f"tabela 58 {nm}: meses ausentes na fonte (nao preenchidos): {falt}")
        dados[(nm, var, tab)] = ser
        vn, un, vdesc = VAR[var]
        ind = f"ipca_{nm}_{vn}"
        out = P / "series" / f"{ind}_sidra{tab}.csv"
        with out.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(COLS)
            for (a, m) in meses:
                x = ser[(a, m)]
                sb = SIMB.get((nm, var, tab, f"{a}{m:02d}"))
                extra = ("; ATENCAO: a tabela 58 nao tem ago/1991 e este valor (set/1991) parece cobrir ago+set (SGS 433 traz 15,63 nos dois meses; "
                         "1,1563^2-1 = 33,70%, SIDRA 33,71): nao usar como variacao de um mes") if (tab == "58" and (a, m) == (1991, 9) and var == "63" and nm == "geral") else ""
                w.writerow([ind, f"IBGE SIDRA t{tab} v{var}", f"{DEF[nm]}, {vdesc}", a, m, "" if x is None else x, un,
                            f"base {tab}; {arq}" + extra + (f"; valor da fonte = '{sb}' (sem numero; nao preenchido nem estimado)" if sb else ""),
                            vint(arq)])
        log.append(f"{ind}_sidra{tab}.csv: {len(meses)} meses {meses[0]}..{meses[-1]}")

# BCB SGS 433
sgs = {}
for r in json.loads((P / "bruto/bcb/sgs_433.json").read_text()):
    d, m, a = r["data"].split("/")
    sgs[(int(a), int(m))] = float(r["valor"])
ms = sorted(sgs)
with (P / "series" / "ipca_geral_var_mensal_bcb_sgs433.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(COLS)
    for (a, m) in ms:
        w.writerow(["ipca_geral_var_mensal", "BCB SGS 433", "IPCA - Variacao mensal (conferencia)", a, m, sgs[(a, m)], "%",
                    "conferencia do IPCA geral; bruto/bcb/sgs_433.json", vint("bruto/bcb/sgs_433.json")])
log.append(f"bcb sgs433: {len(ms)} meses {ms[0]}..{ms[-1]}")

# conferencia: IPCA geral SIDRA x SGS 433, mes a mes, onde ambos existem
conf = []
for tab in ("58", "655", "2938", "1419", "7060"):
    s = dados[("geral", "63", tab)]
    dif = [(k, s[k], sgs[k]) for k in s if k in sgs and abs(s[k] - sgs[k]) > 1e-9]  # geral nao tem lacunas
    n = sum(1 for k in s if k in sgs)
    conf.append((tab, n, dif))

# ---------- derivado ----------
# cadeia principal: 655 -> 2938 -> 1419 -> 7060 (meses contiguos, mesmos codigos 7169/7448/7696).
ORDEM = ["655", "2938", "1419", "7060"]
cad = {}
for nm in ("geral", "aluguel_residencial", "plano_saude"):
    s = {}
    for t in ORDEM:
        for k, v in dados[(nm, "63", t)].items():
            assert k not in s, ("sobreposicao", nm, k)
            s[k] = (v, t)
    cad[nm] = s
ks = sorted(cad["geral"])
assert all(sorted(cad[n]) == ks for n in cad)
# contiguidade global
for i in range(1, len(ks)):
    a, m = ks[i - 1]
    nx = (a, m + 1) if m < 12 else (a + 1, 1)
    assert ks[i] == nx, ("quebra de contiguidade", ks[i - 1], ks[i])

BASE = (1999, 12)
FORM = ("I(t)=I(t-1)*(1+r(t)/100), r = variacao mensal publicada (%) da tabela SIDRA de cada periodo; "
        "I(dez/1999)=100; encadeamento 655->2938->1419->7060 sem mes de sobreposicao (ver RESULTADO.md, regra de encadeamento)")
idx = {}
for nm in cad:
    I = {BASE: 100.0}
    for k in ks:
        if k <= BASE:
            continue
        a, m = k
        prev = (a, m - 1) if m > 1 else (a - 1, 12)
        I[k] = I[prev] * (1 + cad[nm][k][0] / 100)
    idx[nm] = I

IND = {"geral": "indice_ipca_geral_dez1999_100", "aluguel_residencial": "indice_ipca_aluguel_residencial_dez1999_100",
       "plano_saude": "indice_ipca_plano_saude_dez1999_100"}
D = P / "derivado"


def escreve(nome, ind, fonte, defin, serie, unid, nota, arqs):
    with (D / nome).open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for k in sorted(serie):
            w.writerow([ind, fonte, defin, k[0], k[1], f"{serie[k]:.10f}", unid, nota, "; ".join(vint(x) for x in arqs)])


ARQ_CAD = ["bruto/ibge/sidra-655-v63.json", "bruto/ibge/sidra-2938-v63-66.json",
           "bruto/ibge/sidra-1419-v63-66-2265.json", "bruto/ibge/sidra-7060-v63-66-2265.json"]
for nm, I in idx.items():
    escreve(f"{IND[nm]}.csv", IND[nm], "derivado de IBGE SIDRA t655+t2938+t1419+t7060 v63", f"{DEF[nm]}, numero-indice encadeado",
            I, "indice (dez/1999=100)", FORM, ARQ_CAD)
for nm, ind in (("aluguel_residencial", "razao_ipca_aluguel_residencial_sobre_geral_dez1999_100"),
                ("plano_saude", "razao_ipca_plano_saude_sobre_geral_dez1999_100")):
    R = {k: 100 * idx[nm][k] / idx["geral"][k] for k in idx[nm]}
    escreve(f"{ind}.csv", ind, "derivado de IBGE SIDRA t655+t2938+t1419+t7060 v63",
            f"preco relativo: indice do subitem / indice geral, x100 (dez/1999=100)", R, "razao (dez/1999=100)",
            "R(t)=100*I_subitem(t)/I_geral(t), I como em indice_*_dez1999_100.csv; " + FORM, ARQ_CAD)

# base 58: sem numero-indice derivado (ago/1991 nao existe na tabela 58 e abr/1991 do aluguel vem '-'); so a serie bruta em series/

# janelas
JAN = [((1999, 12), (2024, 12)), ((2014, 12), (2024, 12)), ((2018, 12), (2022, 12)), ((2001, 12), (2024, 12))]  # a ultima e sensibilidade (plano de saude muda de metodo em 2001)
jl = []
for a, b in JAN:
    row = {"janela": f"dez/{a[0]}-dez/{b[0]}"}
    for nm in cad:
        row[nm] = (idx[nm][b] / idx[nm][a] - 1) * 100
    row["razao_aluguel_sobre_geral"] = ((idx["aluguel_residencial"][b] / idx["geral"][b]) / (idx["aluguel_residencial"][a] / idx["geral"][a]) - 1) * 100
    row["razao_plano_saude_sobre_geral"] = ((idx["plano_saude"][b] / idx["geral"][b]) / (idx["plano_saude"][a] / idx["geral"][a]) - 1) * 100
    # conferencia do geral por SGS 433 (composicao dos relativos mensais)
    x = 1.0
    k = a
    while k != b:
        k = (k[0], k[1] + 1) if k[1] < 12 else (k[0] + 1, 1)
        x *= 1 + sgs[k] / 100
    row["geral_sgs433"] = (x - 1) * 100
    jl.append(row)
with (D / "acumulados_janelas.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["janela", "ipca_geral_pct", "aluguel_residencial_pct", "plano_saude_pct", "preco_relativo_aluguel_pct",
                "preco_relativo_plano_saude_pct", "ipca_geral_conferencia_sgs433_pct", "nota"])
    for r in jl:
        w.writerow([r["janela"], f"{r['geral']:.4f}", f"{r['aluguel_residencial']:.4f}", f"{r['plano_saude']:.4f}",
                    f"{r['razao_aluguel_sobre_geral']:.4f}", f"{r['razao_plano_saude_sobre_geral']:.4f}", f"{r['geral_sgs433']:.4f}",
                    "acumulado = I(fim)/I(inicio)-1 sobre o numero-indice encadeado (dez/1999=100); relativo = razao dos acumulados; "
                    "cada acumulado parte de taxas mensais publicadas com 2 casas decimais"])

# conferencia da cadeia contra o acumulado em 12 meses publicado (v2265) em 1419 e 7060
chk = []
for nm in cad:
    for t in ("1419", "7060"):
        pub = dados[(nm, "2265", t)]
        mx, kmx = 0.0, None
        n = 0
        for k, v in pub.items():
            if v is None:
                continue
            if k[0] < 2013 and t == "1419":
                continue  # 12 meses de 2012 usam meses de 2011 (outra tabela)
            if t == "7060" and k[0] == 2020:
                continue  # idem, janela inclui 2019
            a, m = k
            x = 1.0
            kk = k
            for _ in range(12):
                x *= 1 + cad[nm][kk][0] / 100
                kk = (kk[0], kk[1] - 1) if kk[1] > 1 else (kk[0] - 1, 12)
            d = abs((x - 1) * 100 - v)
            n += 1
            if d > mx:
                mx, kmx = d, k
        chk.append((nm, t, n, mx, kmx))

# quebras: pesos antes/depois
def pesos(nm, t, k):
    return dados[(nm, "66", t)].get(k)


pw = {}
for nm in ("aluguel_residencial", "plano_saude"):
    pw[nm] = {
        "1999-08": pesos(nm, "656", (1999, 8)),
        "2006-06": pesos(nm, "656", (2006, 6)), "2006-07": pesos(nm, "2938", (2006, 7)),
        "2011-12": pesos(nm, "2938", (2011, 12)), "2012-01": pesos(nm, "1419", (2012, 1)),
        "2019-12": pesos(nm, "1419", (2019, 12)), "2020-01": pesos(nm, "7060", (2020, 1)),
    }
ps = cad["plano_saude"]
amostra_ps = {f"{a}-{m:02d}": ps[(a, m)][0] for (a, m) in [(2020, 5), (2020, 6), (2020, 7), (2020, 8), (2020, 9), (2020, 10), (2020, 11),
                                                           (2020, 12), (2021, 1), (2021, 2)]}
json.dump({"log": log, "conf_sgs": [(t, n, d[:5]) for t, n, d in conf], "janelas": jl,
           "chk12": chk, "pesos": pw, "ps_2020": amostra_ps,
           "idx_pontos": {nm: {f"{a}-{m:02d}": I[(a, m)] for (a, m) in [(1999, 12), (2014, 12), (2018, 12), (2022, 12), (2024, 12), (2026, 9)]}
                          for nm, I in idx.items()}},
          (D / "_resumo_construcao.json").open("w"), indent=1, ensure_ascii=False)
print(json.dumps({"log": log, "conf_sgs": [(t, n, len(d)) for t, n, d in conf]}, ensure_ascii=False, indent=1))
