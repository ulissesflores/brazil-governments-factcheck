#!/usr/bin/env python3
"""Poder de compra, excesso monetario e trabalho: reconstrucao a partir do BRUTO ja hasheado.

Uso:  python3 -I construir.py        (sem rede; le so arquivos locais)
Le:   ../bruto (esta pasta), ../../economia-real, ../../quebras/bruto, ../../monetario/saida
Gera: ../series/poder_de_compra.csv, ../series/excesso_monetario.csv, ../series/trabalho.csv
      ../series/_conferencias.txt (provas de continuidade e extracao)
"""
import csv
import json
import math
import re
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent                      # poder-de-compra/
DADOS = RAIZ.parent                     # fontes/dados/
BRUTO = RAIZ / "bruto"
SERIES = RAIZ / "series"
SERIES.mkdir(exist_ok=True)
LOG = []

REF = (2026, 9)                          # base dos reais deflacionados: set/2026 = 100% do valor
HORAS_MES = 220                          # horas de trabalho por mes: o DIEESE divide o salario minimo por 220 h/mes "desde outubro de 1988" (metodologia da cesta, jan/2016, secao 4)
VINT_DL = "baixado 2026-10-19"

# ---------------------------------------------------------------- leitura
meta = {r["SERCODIGO"]: r for r in json.load(open(DADOS / "economia-real/meta/ipeadata-Metadados-catalogo-completo-raw.json"))["value"]}


def ipea(arq, nivel=("", "Brasil")):
    d = {}
    for x in json.load(open(arq))["value"]:
        if x["VALVALOR"] is None or x["NIVNOME"] not in nivel:
            continue
        d[(int(x["VALDATA"][:4]), int(x["VALDATA"][5:7]))] = float(x["VALVALOR"])
    return d


def vint_ip(cod):
    a = (meta.get(cod, {}).get("SERATUALIZACAO") or "")[:10]
    return f"Ipeadata {cod}, {VINT_DL}; atualizada na fonte em {a or 'n/d'}"


def sgs(arq):
    d = {}
    for x in json.load(open(arq)):
        dd, mm, aa = x["data"].split("/")
        d[(int(aa), int(mm))] = float(x["valor"])
    return d


def idx_de_variacao(var, base=100.0):
    """Indice encadeado a partir de variacoes mensais (%). O mes anterior ao primeiro vale `base`."""
    ks = sorted(var)
    out, v = {}, base
    for k in ks:
        v *= 1 + var[k] / 100
        out[k] = v
    return out


def meses(d):
    return sorted(d)


def media_anual(m, exigir12=True):
    por = {}
    for (a, mm), v in m.items():
        por.setdefault(a, []).append(v)
    return {a: sum(v) / len(v) for a, v in por.items() if (len(v) == 12 or not exigir12)}


# ---------------------------------------------------------------- series mensais
sm = ipea(DADOS / "economia-real/ipeadata-MTE12_SALMIN12-raw.json")          # R$ atuais (moeda convertida pelo Ipeadata)
cesta_bruta = ipea(DADOS / "quebras/bruto/ipeadata-DIEESE12_CBSP12-raw.json")  # moeda da epoca
cortes = [((1967, 1), 1000), ((1986, 3), 1000), ((1989, 1), 1000), ((1993, 8), 1000), ((1994, 7), 2750)]


def divisor(k):
    d = 1
    for ini, f in cortes:
        if ini > k:
            d *= f
    return d


cesta = {k: v / divisor(k) for k, v in cesta_bruta.items()}                  # R$ atuais
# prova de continuidade nos meses de corte
LOG.append("CONTINUIDADE DA CESTA NOS CORTES DE MOEDA (razao do mes sobre o anterior, cesta convertida x IGP-DI)")
igp = ipea(DADOS / "economia-real/ipeadata-IGP12_IGPDI12-raw.json")
ks = meses(cesta)
for c, f in cortes:
    i = ks.index(c)
    k0, k1 = ks[i - 1], ks[i]
    LOG.append(f"  {c[0]}-{c[1]:02d} (divisor {f}): cesta {cesta[k1] / cesta[k0]:.3f} | IGP-DI {igp[k1] / igp[k0]:.3f} | cesta sem conversao {cesta_bruta[k1] / cesta_bruta[k0]:.5f}")

# O indice IGP-DI do Ipeadata tem um salto de nivel de x1,182 em 1994-07 frente a cadeia das taxas mensais do BCB (SGS 190, desde 1980).
# Diagnostico: o indice do Ipeadata reproduz a taxa ANUAL de 1994 (1.093,9%, ver monetario/RESULTADO.md) e a cadeia mensal do SGS da 909,7%.
# Mantido o indice do Ipeadata como publicado; o salto fica registrado em _conferencias.txt e em quebras.csv.
_sg = sgs(DADOS / "inflacao/igpdi-sgs190-raw.json")
_p = 1.0
for _m in range(1, 13):
    _p *= 1 + _sg[(1994, _m)] / 100
AJ_IGP = (igp[(1994, 7)] / igp[(1994, 6)]) / (1 + _sg[(1994, 7)] / 100)
LOG.append(f"IGP-DI 1994-07: indice Ipeadata jul/jun = {igp[(1994, 7)] / igp[(1994, 6)]:.4f}; taxa oficial SGS 190 = {_sg[(1994, 7)]}%; salto de nivel = {AJ_IGP:.4f}")
LOG.append(f"IGP-DI 1994 dez/dez: indice Ipeadata {(igp[(1994, 12)] / igp[(1993, 12)] - 1) * 100:.1f}% | cadeia das taxas mensais do SGS 190 {(_p - 1) * 100:.1f}% | (cadeia SGS 433 do IPCA em 1994 = 916,4%)")

inpc_var = sgs(DADOS / "economia-real/bcb-sgs188-raw.json")                    # 1979-04 a 2026-09
ipca_var = sgs(DADOS / "economia-real/bcb-sgs433-raw.json")                    # 1980-01 a 2026-09
inpc = idx_de_variacao(inpc_var)
ipca = idx_de_variacao(ipca_var)
fipe = ipea(RAIZ / "bruto/ipeadata-FIPE12_IPCFIPE12-raw.json")                  # indice jun/1994=100
dim1 = idx_de_variacao(ipea(RAIZ / "bruto/ipeadata-DIMAC12_INF1-raw.json"))     # Ipea, % a.m., renda muito baixa
dim2 = idx_de_variacao(ipea(RAIZ / "bruto/ipeadata-DIMAC12_INF2-raw.json"))     # Ipea, renda baixa
for nome, s in (("SM", sm), ("cesta", cesta), ("INPC", inpc), ("IGP-DI", igp), ("IPC-Fipe", fipe), ("IPCA", ipca), ("Ipea renda muito baixa", dim1), ("Ipea renda baixa", dim2)):
    ms = meses(s)
    buracos = [k for k in range(len(ms) - 1) if (ms[k + 1][0] * 12 + ms[k + 1][1]) - (ms[k][0] * 12 + ms[k][1]) != 1]
    LOG.append(f"COBERTURA {nome}: {ms[0]} a {ms[-1]}, {len(ms)} meses, buracos={len(buracos)}")

# ---------------------------------------------------------------- linhas
LIN = []
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]


def emite(ind, fonte, defin, anual, unid, nota, vint, ano_min=None, ano_max=2025, casas=4):
    for a in sorted(anual):
        if (ano_min and a < ano_min) or a > ano_max:
            continue
        v = anual[a]
        if v is None or (isinstance(v, float) and math.isnan(v)):
            continue
        # valores minusculos (moeda antes dos cortes de zeros) em notacao cientifica; o resto arredondado
        LIN.append([ind, fonte, defin, a, f"{v:.6e}" if abs(v) < 1e-3 else round(v, casas), unid, nota, vint])


NOTA_SM = "Ate abr/1984 o salario minimo tinha valores regionais; a serie Ipeadata traz o MAIOR vigente no pais (Ipea). Valores em reais atuais por conversao de moeda feita pelo Ipeadata (5 cortes de zeros)."
NOTA_CESTA = ("Cesta basica de alimentos do DIEESE, municipio de Sao Paulo. Valores convertidos para reais atuais dividindo pelo mesmo divisor acumulado de moeda "
              "(cortes jan/1967, mar/1986, jan/1989, ago/1993, jul/1994; ver _conferencias.txt). Metodologia atualizada em jan/2016 (Ipeadata).")

# nominais
sm_a = media_anual(sm)
cesta_a = media_anual(cesta)
emite("salario_minimo_nominal", "Ipeadata MTE12_SALMIN12 (MTE)", "media dos 12 meses do ano, R$ atuais (sem correcao de precos)", sm_a, "R$ atuais", NOTA_SM, vint_ip("MTE12_SALMIN12"), 1948)
emite("cesta_basica_dieese_sp_nominal", "Ipeadata DIEESE12_CBSP12 (DIEESE)", "media dos 12 meses do ano, R$ atuais (sem correcao de precos)", cesta_a, "R$ atuais", NOTA_CESTA, vint_ip("DIEESE12_CBSP12"), 1959)

# razao SM / cesta e horas
razao_m = {k: sm[k] / cesta[k] for k in cesta if k in sm and cesta[k] > 0}
razao_a = media_anual(razao_m)
horas_a = {a: HORAS_MES / v for a, v in razao_a.items()}
emite("cestas_por_salario_minimo", "derivado: MTE12_SALMIN12 / DIEESE12_CBSP12", "media anual da razao mensal salario minimo / custo da cesta SP",
      razao_a, "cestas por salario minimo", NOTA_SM + " Razao independente do deflator.", vint_ip("MTE12_SALMIN12") + " | " + vint_ip("DIEESE12_CBSP12"), 1959, casas=4)
emite("horas_de_trabalho_por_cesta", "derivado: 220 / (cestas por salario minimo)", f"horas de trabalho no salario minimo bruto para comprar 1 cesta SP; {HORAS_MES} h/mes",
      horas_a, "horas", f"Formula do proprio DIEESE (metodologia da cesta, jan/2016, secao 4): horas = custo da cesta x {HORAS_MES} / salario minimo vigente, com 220 h/mes 'desde outubro de 1988'. Aqui a cesta e a de Sao Paulo e os {HORAS_MES} h sao aplicados a TODOS os anos, tambem antes de out/1988 (convencao deste arquivo; nao verifiquei a jornada anterior nos arquivos baixados).",
      vint_ip("MTE12_SALMIN12") + " | " + vint_ip("DIEESE12_CBSP12"), 1959, casas=2)

# SM real por deflator
defl = [
    ("INPC", inpc, "BCB SGS 188 (IBGE), mensal encadeado", "1979-04", "INPC cobre familias de 1 a 5 salarios minimos (IBGE); serie comeca em abr/1979", "economia-real/bcb-sgs188-raw.json; baixado 2026-10-19"),
    ("IGP-DI", igp, "Ipeadata IGP12_IGPDI12 (FGV)", "1944-01", "IGP-DI e indice geral de precos (atacado, consumidor e construcao); nao e indice de custo de vida. O indice do Ipeadata tem salto de nivel de x1,182 em jul/1994 frente as taxas mensais do SGS 190 (ver _conferencias.txt e quebras.csv); mantido como publicado porque reproduz a taxa anual de 1994", vint_ip("IGP12_IGPDI12")),
    ("IPC-Fipe", fipe, "Ipeadata FIPE12_IPCFIPE12 (Fipe/USP)", "1939-01", "Familias paulistanas com renda de 1 a 10 salarios minimos; so Regiao Metropolitana de Sao Paulo", vint_ip("FIPE12_IPCFIPE12")),
    ("IPCA", ipca, "BCB SGS 433 (IBGE), mensal encadeado", "1980-01", "IPCA: familias de 1 a 40 salarios minimos (IBGE); incluido so como referencia oficial", "economia-real/bcb-sgs433-raw.json; baixado 2026-10-19"),
    ("Ipea renda muito baixa", dim1, "Ipeadata DIMAC12_INF1 (Ipea)", "2006-07", "NAO E O IPC-C1 da FGV. E o Indicador Ipea de Inflacao por Faixa de Renda, faixa 'renda muito baixa'; comeca em jul/2006", vint_ip("DIMAC12_INF1")),
    ("Ipea renda baixa", dim2, "Ipeadata DIMAC12_INF2 (Ipea)", "2006-07", "NAO E O IPC-C1 da FGV. E o Indicador Ipea de Inflacao por Faixa de Renda, faixa 'renda baixa'; comeca em jul/2006", vint_ip("DIMAC12_INF2")),
]
real_a = {}
for nome, idx, fonte, ini, nota_ind, vint in defl:
    mref = REF if REF in idx else max(idx)
    ref = idx[mref]
    rot = f"{mref[1]:02d}/{mref[0]}"
    real_m = {k: sm[k] * ref / idx[k] for k in sm if k in idx}
    ra = media_anual(real_m)
    real_a[nome] = ra
    emite(f"salario_minimo_real_{nome.replace(' ', '_').replace('-', '').lower()}", fonte,
          f"media dos 12 meses do salario minimo mensal deflacionado por {nome}, em R$ de {rot}",
          ra, f"R$ de {rot}", nota_ind + ". " + NOTA_SM + ("" if mref == REF else f" Base {rot} porque a serie termina nesse mes."), vint, 1948)

# indices: variacao anual dez/dez de cada indice (para o leitor ver a relacao com o salario minimo real)
def dez_dez(idx):
    return {a: (idx[(a, 12)] / idx[(a - 1, 12)] - 1) * 100 for a in range(1940, 2026) if (a, 12) in idx and (a - 1, 12) in idx}


for nome, idx, fonte, ini, nota_ind, vint in defl:
    emite(f"inflacao_dez_dez_{nome.replace(' ', '_').replace('-', '').lower()}", fonte, f"variacao de dezembro a dezembro do {nome}", dez_dez(idx), "% a.a.", nota_ind, vint, 1940, casas=3)

# ICV-DIEESE: so taxas anuais publicadas em notas do DIEESE; o hiato 2020-2023 impede encadear
ICV = {  # ano: (valor %, arquivo, trecho que prova)
    1997: (6.1, "dieese-icv-1997-2004-relatorio.pdf", r"Total Geral\s+6,1\s+0,5\s+9,6\s+7,2\s+9,4\s+12,9\s+9,6\s+7,7"),
    1998: (0.5, "dieese-icv-1997-2004-relatorio.pdf", r"Total Geral\s+6,1\s+0,5"),
    1999: (9.6, "dieese-icv-1997-2004-relatorio.pdf", r"Total Geral\s+6,1\s+0,5\s+9,6"),
    2000: (7.2, "dieese-icv-1997-2004-relatorio.pdf", r"Total Geral\s+6,1\s+0,5\s+9,6\s+7,2"),
    2001: (9.4, "dieese-icv-1997-2004-relatorio.pdf", r"Total Geral\s+6,1\s+0,5\s+9,6\s+7,2\s+9,4"),
    2002: (12.9, "dieese-icv-1997-2004-relatorio.pdf", r"Total Geral\s+6,1\s+0,5\s+9,6\s+7,2\s+9,4\s+12,9"),
    2003: (9.6, "dieese-icv-1997-2004-relatorio.pdf", r"Total Geral\s+6,1\s+0,5\s+9,6\s+7,2\s+9,4\s+12,9\s+9,6"),
    2004: (7.70, "dieese-icv-2004.pdf", r"variação acumulada de 7,70%"),
    2005: (4.54, "dieese-icv-2005.pdf", r"subiu 4,54%"),
    2006: (2.57, "dieese-icv-2006.pdf", r"Total Geral\s+2,57"),
    2007: (4.80, "dieese-icv-2007.pdf", r"Total Geral\s+4,80\s+5,55"),
    2008: (6.11, "dieese-icv-2008.pdf", r"Total Geral\s+6,11"),
    2009: (4.05, "dieese-icv-2009.pdf", r"Total Geral\s+4,05"),
    2010: (6.91, "dieese-icv-2010.pdf", r"Total Geral\s+6,91"),
    2011: (6.09, "dieese-icv-2011.pdf", r"Total Geral\s+6,09"),
    2012: (6.41, "dieese-icv-2012.pdf", r"Total Geral\s+6,41"),
    2013: (6.04, "dieese-icv-2013.pdf", r"Total Geral\s+6,04"),
    2014: (6.73, "dieese-icv-2014.pdf", r"Total Geral\s+6,73"),
    2015: (11.46, "dieese-icv-2015.pdf", r"Total Geral\s+11,46"),
    2016: (6.15, "dieese-icv-2016.pdf", r"Total Geral\s+6,15"),
    2017: (2.44, "dieese-icv-2017.pdf", r"Total Geral\s+2,44"),
    2018: (3.89, "dieese-icv-2018.pdf", r"Total Geral\s+3,89"),
    2019: (3.09, "dieese-icv-2019.pdf", r"Total Geral\s+3,09"),
}
LOG.append("ICV-DIEESE: conferencia da taxa anual no texto do PDF (pdftotext -layout)")
txt_cache = {}
for a, (v, arq, rx) in sorted(ICV.items()):
    if arq not in txt_cache:
        txt_cache[arq] = subprocess.run(["pdftotext", "-layout", str(BRUTO / arq), "-"], capture_output=True, text=True, check=True).stdout
    ok = re.search(rx, txt_cache[arq]) is not None
    LOG.append(f"  {a}: {v:>6}  {arq}  prova '{rx}' -> {'OK' if ok else 'NAO ACHEI'}")
    assert ok, (a, arq, rx)
icv_a = {a: v[0] for a, v in ICV.items()}
emite("inflacao_dez_dez_icv_dieese", "DIEESE, notas anuais do ICV (PDF)", "variacao de janeiro a dezembro do ICV-DIEESE geral, municipio de Sao Paulo",
      icv_a, "% a.a.", "ICV-DIEESE: familias paulistanas, tres estratos de renda; so ha taxas anuais publicadas (a serie longa nao e baixavel: 'Banco de Dados ainda nao disponivel' no site do DIEESE). Hiato: pesquisa suspensa em mar/2020 e retomada em ago/2023 com nova ponderacao (POF 2017/18); nao encadeia. 2005: 4,54% na nota de 2005 e 4,55% na nota de 2006.",
      "DIEESE, notas baixadas 2026-10-19 (hash em manifest.jsonl)", 1997, casas=2)
# indice encadeado dez/1996 = 100 (so de 1997 a 2019) e SM de dezembro deflacionado por ICV e, lado a lado, pelo INPC, na mesma base dez/2019
icv_idx = {1996: 100.0}
for a in range(1997, 2020):
    icv_idx[a] = icv_idx[a - 1] * (1 + icv_a[a] / 100)
sm_dez_icv = {a: sm[(a, 12)] * icv_idx[2019] / icv_idx[a] for a in range(1996, 2020) if (a, 12) in sm}
sm_dez_inpc = {a: sm[(a, 12)] * inpc[(2019, 12)] / inpc[(a, 12)] for a in range(1996, 2020) if (a, 12) in sm}
emite("salario_minimo_dezembro_real_icv_dieese", "derivado: MTE12_SALMIN12 / ICV-DIEESE encadeado (dez/1996=100)", "salario minimo de DEZEMBRO deflacionado pelo ICV-DIEESE, em R$ de dez/2019",
      sm_dez_icv, "R$ de dez/2019", "So 1996-2019: antes de 1997 nao ha taxa anual do ICV baixada e depois de 2019 ha o hiato. Base e dez/2019, diferente das outras linhas (set/2026). Taxas anuais arredondadas (0,1 p.p. em 1997-1999).",
      "derivado; ICV como na linha inflacao_dez_dez_icv_dieese; " + vint_ip("MTE12_SALMIN12"), 1996, 2019, casas=2)
emite("salario_minimo_dezembro_real_inpc_mesma_base_do_icv", "derivado: MTE12_SALMIN12 / INPC", "salario minimo de DEZEMBRO deflacionado pelo INPC, em R$ de dez/2019 (comparavel com a linha do ICV)",
      sm_dez_inpc, "R$ de dez/2019", "Linha de comparacao: mesma base e mesmos anos da linha do ICV-DIEESE.", "economia-real/bcb-sgs188-raw.json; " + vint_ip("MTE12_SALMIN12"), 1996, 2019, casas=2)

with open(SERIES / "poder_de_compra.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(COLS)
    w.writerows(LIN)
LOG.append(f"poder_de_compra.csv: {len(LIN)} linhas, {len({l[0] for l in LIN})} indicadores")

# ---------------------------------------------------------------- excesso monetario
an = {int(r["ano"]): r for r in csv.DictReader(open(DADOS / "monetario/saida/anual.csv"))}
pib = {int(r["ano"]): float(r["pib_real_var_pct_SCN10_PIBG10"]) for r in csv.DictReader(open(DADOS / "economia-real/saida-pib-anual-1948-2025.csv"))}


def lvl(col, a):
    v = an.get(a, {}).get(col, "")
    return float(v) if v not in ("", None) else None


def cresc(col, a):
    x, y = lvl(col, a), lvl(col, a - 1)
    return (x / y - 1) * 100 if x is not None and y else None


ipca_dd = dez_dez(ipca)
igp_dd = dez_dez(igp)
EX = []
for a in range(1948, 2026):
    m0 = cresc("M0_dez", a)
    m1a = cresc("M1_dez", a) if a <= 2017 else None
    m1n = cresc("M1_novo_dez", a)
    m1 = m1a if a <= 2017 else m1n
    g = pib[a]
    nota = []
    if a == 2018:
        nota.append("M1: 2018 usa a serie 'Novo' (descontinuacao do conceito antigo em jun/2018; em dez/2017 o M1 sobe 5,2% so pela mudanca de conceito, ver monetario/RESULTADO.md)")
    if a == 2003:
        nota.append("M1 novo comeca em dez/2002; crescimento 2003 e o primeiro com a serie nova")
    if a <= 1994 and m0 is not None and m0 > 100:
        nota.append("crescimento nominal em hiperinflacao: o excesso e quase todo inflacao, nao informa sobre 'liquidez' sem outro deflator")
    EX.append({
        "ano": a,
        "M0_cresc_pct": m0, "M1_cresc_pct": m1, "M1_conceito": "antigo (SGS 1827)" if a <= 2017 else "Novo (SGS 27791)",
        "M1_novo_cresc_pct": m1n if a >= 2003 else None,
        "pib_real_cresc_pct": g,
        "excesso_M0_pp": None if m0 is None else m0 - g,
        "excesso_M1_pp": None if m1 is None else m1 - g,
        "igpdi_dez_dez_pct": igp_dd.get(a), "ipca_dez_dez_pct": ipca_dd.get(a),
        "nota": "; ".join(nota),
    })
CAB = ["ano", "M0_cresc_pct", "M1_cresc_pct", "M1_conceito", "M1_novo_cresc_pct", "pib_real_cresc_pct", "excesso_M0_pp", "excesso_M1_pp", "igpdi_dez_dez_pct", "ipca_dez_dez_pct", "nota"]
with open(SERIES / "excesso_monetario.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(CAB)
    for r in EX:
        w.writerow([("" if r[c] is None else (round(r[c], 3) if isinstance(r[c], float) else r[c])) for c in CAB])
LOG.append("excesso_monetario.csv: formula M_cresc = (M_dez(t)/M_dez(t-1)-1)*100 ; excesso = M_cresc - PIB_real_cresc (pontos percentuais); sem deflator")

# ---------------------------------------------------------------- trabalho
def sidra(arq):
    out = {}
    for v in json.load(open(arq)):
        s = v["resultados"][0]["series"][0]["serie"]
        out[int(v["id"])] = {k: (float(x) if x not in ("-", "...", "X", None, "") else None) for k, x in s.items()}
    return out


s1 = sidra(BRUTO / "sidra-4093-pnadc-trimestral-raw.json")
s2 = sidra(BRUTO / "sidra-4099-pnadc-subutilizacao-raw.json")
s3 = sidra(BRUTO / "sidra-6813-pnadc-desalento-raw.json")
TR = []
TC = ["indicador", "fonte", "definicao_linha", "ano", "trimestre", "valor", "unidade", "nota", "vintage"]
V_SID = "IBGE SIDRA via API agregados v3, baixado 2026-10-19; ultimo trimestre 2026T2"
IND = [
    ("nivel_da_ocupacao", s1[4097], "SIDRA 4093 var 4097", "pessoas ocupadas / pessoas de 14 anos ou mais (todas, inclusive fora da forca de trabalho)", "%"),
    ("taxa_de_participacao", s1[4096], "SIDRA 4093 var 4096", "forca de trabalho / pessoas de 14 anos ou mais", "%"),
    ("taxa_de_desocupacao", s2[4099], "SIDRA 4099 var 4099", "desocupados / forca de trabalho (ver definicoes.md)", "%"),
    ("taxa_composta_de_subutilizacao", s2[4118], "SIDRA 4099 var 4118", "(desocupados + subocupados por insuficiencia de horas + forca de trabalho potencial) / (forca de trabalho + forca de trabalho potencial)", "%"),
    ("taxa_combinada_desocupacao_e_forca_potencial", s2[4116], "SIDRA 4099 var 4116", "desocupados + forca de trabalho potencial, sobre forca de trabalho ampliada", "%"),
    ("percentual_de_desalentados", s3[9869], "SIDRA 6813 var 9869", "desalentados / (forca de trabalho + desalentados)", "%"),
]
for nome, ser, fonte, defin, unid in IND:
    for per in sorted(ser):
        a, q = int(per[:4]), int(per[4:])
        TR.append([nome, fonte, defin, a, f"T{q}", ser[per], unid, "trimestre fixo (nao movel); PNAD Continua comeca em 2012T1", V_SID])
    por = {}
    for per, v in ser.items():
        if v is not None:
            por.setdefault(int(per[:4]), []).append(v)
    for a in sorted(por):
        if len(por[a]) == 4:
            TR.append([nome, fonte, defin + " | media simples dos 4 trimestres", a, "ano", round(sum(por[a]) / 4, 3), unid, "media de 4 trimestres; 2026 nao entra (so 2 trimestres)", V_SID])
# pessoas fora da forca de trabalho (mil) e PIA
for cod, nome, defin in ((4094, "fora_da_forca_de_trabalho_mil_pessoas", "pessoas de 14+ fora da forca de trabalho"), (1641, "pessoas_de_14_anos_ou_mais_mil", "populacao de 14 anos ou mais")):
    for per in sorted(s1[cod]):
        TR.append([nome, f"SIDRA 4093 var {cod}", defin, int(per[:4]), f"T{int(per[4:])}", s1[cod][per], "mil pessoas", "trimestre fixo", V_SID])
# desemprego anual: PNAD (Ipeadata, 1992-2015), PME antiga (1980-2002, 6 regioes metropolitanas) e PNADC anual
des = list(csv.DictReader(open(DADOS / "economia-real/saida-desemprego-anual.csv")))
for r in des:
    a = int(r["ano"])
    if r["PME_antiga_15mais_30d_6RMs"] and a <= 2002:
        TR.append(["desemprego_PME_antiga_6RMs", "Ipeadata PME12_TDA12 (IBGE/PME)", "media dos meses; 15 anos ou mais; procura nos ultimos 30 dias; SO 6 regioes metropolitanas. NAO e a PNAD.", a, "ano", r["PME_antiga_15mais_30d_6RMs"], "%",
                   "taxa publicada pelo IBGE para 1980-2002 em 6 regioes metropolitanas; para a PNAD nacional de 1981-1990 ver desemprego_PNAD_anual_Brasil_derivado_dos_microdados", vint_ip("PME12_TDA12")])
    if r["PNAD_DISOC_DESE_Brasil"]:
        TR.append(["desemprego_PNAD_anual_Brasil", "Ipeadata DISOC_DESE (Ipea, microdados da PNAD)", "desocupados / PEA, 10 anos ou mais, semana de referencia, Brasil", a, "ano", r["PNAD_DISOC_DESE_Brasil"], "%",
                   "1992-2015; sem 1994 (Censo/contagem), sem 2000; serie interrompida; area rural do Norte excluida ate 2003", vint_ip("DISOC_DESE")])
micro = {int(r["ano"]): r for r in csv.DictReader(open(SERIES / "pnad_1981_1990_microdados.csv"))} if (SERIES / "pnad_1981_1990_microdados.csv").exists() else {}
MOTIVO = {1983: "Dados.zip de 29 MB", 1987: "arquivo PND1987N.DAT de 79 MB", 1989: "arquivo PND1989N.DAT de 100 MB", 1990: "arquivo PND1990N.DAT de 103 MB"}
for a in range(1981, 1991):
    if a in micro:
        m = micro[a]
        TR.append(["desemprego_PNAD_anual_Brasil_derivado_dos_microdados", f"IBGE, microdados da PNAD {a} (FTP do IBGE); calculo deste arquivo (scripts/pnad_microdados.py)",
                   "desocupados / PEA, 10 anos ou mais, semana de referencia; desocupado = V501 'procurou trabalho'; PEA = V501 em {trabalhou, tinha trabalho, procurou trabalho}; peso da pessoa", a, "ano", m["taxa_desocupacao_pct"], "%",
                   f"DERIVADO de microdados, NAO e numero publicado pelo IBGE; sem peso: {m['taxa_sem_peso_pct']}%; " + (f"com peso reponderado pelo Censo 91: {m['taxa_com_peso_alternativo_censo91_pct']}%; " if m["taxa_com_peso_alternativo_censo91_pct"] else "") + f"registros de pessoa: {m['registros_pessoa']}; 1981 em diante exclui a area rural da antiga Regiao Norte",
                   "IBGE FTP Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_anual/microdados, hash em manifest.jsonl"])
    else:
        TR.append(["desemprego_PNAD_anual_Brasil_derivado_dos_microdados", f"IBGE, microdados da PNAD {a} (FTP do IBGE)", "desocupados / PEA", a, "ano", "", "%",
                   f"NAO CALCULADO: os microdados existem no FTP do IBGE, mas o arquivo tem {MOTIVO.get(a, 'mais de 25 MB')}, acima do limite de 25 MB por arquivo desta tarefa" if a in MOTIVO else "NAO CALCULADO: sem PNAD em 1991 (ano de Censo)", "n/d"])
for a in (1970, 1980):
    TR.append(["desocupacao_Censo", f"IBGE, Censo Demografico {a}", "pessoas desocupadas / PEA", a, "ano", "", "%", "NAO OBTIDO: nenhuma tabela digital de desocupacao dos Censos 1970/1980 achada em SIDRA, Ipeadata (so PEA por setor) ou Series Estatisticas", "n/d"])
with open(SERIES / "trabalho.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(TC)
    w.writerows(TR)
LOG.append(f"trabalho.csv: {len(TR)} linhas")

# anual do SM real: sanidade contra economia-real/saida-salmin-real-anual.csv (Ipea, deflator INPC/IPCA misto)
ref = {int(r["ano"]): float(r["media_anual_real_R$_set2026"]) for r in csv.DictReader(open(DADOS / "economia-real/saida-salmin-real-anual.csv"))}
LOG.append("SANIDADE: SM real (media anual, R$ set/2026) aqui x economia-real/saida-salmin-real-anual.csv")
for a in (1960, 1980, 1990, 2000, 2010, 2020, 2025):
    LOG.append(f"  {a}: INPC {real_a['INPC'].get(a, float('nan')):.2f} | IGP-DI {real_a['IGP-DI'].get(a, float('nan')):.2f} | IPC-Fipe {real_a['IPC-Fipe'].get(a, float('nan')):.2f} | IPCA {real_a['IPCA'].get(a, float('nan')):.2f} | economia-real {ref.get(a, float('nan')):.2f}")
(SERIES / "_conferencias.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
print("\n".join(LOG))
