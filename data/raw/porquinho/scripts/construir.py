#!/usr/bin/env python3
"""Porquinho: R$ 100.000 em dinheiro vivo desde 1 de janeiro de 1995. Reconstrucao so a partir de brutos hasheados.

Uso:   python3 -I construir.py          (sem rede; le so arquivos locais)
Le:    ../bruto (esta pasta)  e, por reuso, ../../inflacao, ../../poder-de-compra, ../../economia-real, ../../quebras/bruto
Gera:  ../series/porquinho.csv            formato longo: linha,ano,mes,valor,unidade,nota,vintage
       ../series/porquinho_por_governo.csv
       ../series/_conferencias.txt
Pre-registro: ../../preregistro/PREREGISTRATION-EMENDA-03.md, secao E. Nenhuma linha alem das registradas.
Sem opiniao, sem nota, sem ranking. O imposto inflacionario NUNCA e somado a inflacao: nao e calculado em lugar nenhum.

CONVENCOES (todas as linhas)
  tempo   linha (ano, mes) = estado ao FIM do mes (linhas de fonte mensal de preco/juro) ou media do mes (cambio, ouro, IPC).
          O ponto de partida "1 de janeiro de 1995" = fim de dez/1994 = linha (1994, 12): valor 100.000 em todas as linhas de R$.
          Fronteira de mandato em dia 1 (ex.: 2003-01-01) = linha do mes anterior; 2016-08-31 = linha de ago/2016.
  taxa    t_k = taxa mensal da fonte em %; fator = 1 + t_k/100.  Indice I(m) = produto dos fatores de jan/1995 ate m;  I(1994-12) = 1.
  (a) caixa_real_X(m)      = 100000 / I_X(m)                       X = ipca (SGS 433), inpc (SGS 188), igpdi (SGS 190), ipcfipe (Ipeadata
                             FIPE12_FIPE0001, taxa mensal), ipea_renda_muito_baixa (DIMAC12_INF1, emenda), icv_dieese (anual, emenda).
                             unidade: R$ de dez/1994 (= poder de compra do 1 jan 1995). Nunca somado a nada.
                             Emenda Ipea: ate dez/2006 a linha e igual a caixa_real_ipca; de jan/2007 em diante o deflator e o Ipea (INF1).
                             Emenda ICV: ate dez/1996 igual a caixa_real_ipca; so ha taxa anual 1997-2019 (dez/dez): pontos de dezembro, sem interpolar.
  (b) poupanca_nominal(m)  = 100000 * prod_{k=1995-01..m} (1 + p_k/100),  p_k = SGS 25 no dia 01 do mes k (aniversario dia 1; a taxa do periodo
                             que comeca no dia 1 do mes k e creditada no dia 1 do mes k+1 = fim do mes k). SGS 25 e a regra de quem depositou ate
                             03/05/2012 (0,5% a.m. + TR), que continua publicada: um deposito de jan/1995 segue nela. Bruto de imposto/tarifa.
      poupanca_real_ipca(m)= poupanca_nominal(m) / I_ipca(m).
      selic_nominal(m)     = 100000 * prod (1 + s_k/100),  s_k = SGS 4390 (Selic acumulada no mes);  selic_real_ipca = selic_nominal / I_ipca.
  (c) caixa_menos_poupanca_real_ipca(m) = caixa_real_ipca(m) - poupanca_real_ipca(m)    (R$ de dez/1994; negativo = o que a caixa perdeu para a poupanca)
  (d) caixa_em_anos_pib_per_capita_nominal(ano) = 100000 / (GAC_PIBCAPN do ano * 1000)   linha anual (mes vazio); PIB per capita nominal do Ipea
      caixa_em_salarios_minimos(m) = 100000 / SM nominal vigente do mes (Ipeadata MTE12_SALMIN12)
      caixa_em_cestas_dieese_sp(m) = 100000 / custo nominal da cesta basica DIEESE-SP do mes (Ipeadata DIEESE12_CBSP12)
  (e) PTAX_m = SGS 3698 (dolar venda, media do mes, R$/US$).  C(m) = indice de preco da referencia, C(1994-12)=1 (mesma data-base).
      usd_nominal(m) = 100000 / PTAX_m                                 usd_poder_compra_ref = usd_nominal(m) * CPI_EUA(1994-12)/CPI_EUA(m)
      chf_nominal(m) = 100000 * EXSZUS_m / PTAX_m   (EXSZUS = CHF por US$, FRED, media do mes)
                                                                        chf_poder_compra_ref = chf_nominal(m) * CPI_CH(1994-12)/CPI_CH(m)  (SNB LD2010100)
      sdr_nominal(m) = usd_nominal(m) * XDR_USD_m   (IMF ER, DES por US$, media do mes)
                                                                        sdr_poder_compra_ref = sdr_nominal(m) * CPI_EUA(1994-12)/CPI_EUA(m)  (DES nao tem inflacao propria: CPI dos EUA, declarado)
      ouro_oncas(m)  = usd_nominal(m) / GOLD_m  (Banco Mundial Pink Sheet, US$/onca troy, media do mes). Quantidade fisica: nao se deflaciona
                       (numerador e denominador teriam o mesmo CPI e se cancelam: deflacionar onças por CPI nao define grandeza).
      ouro_preco_real_usd_oz(m) = GOLD_m * CPI_EUA(1994-12)/CPI_EUA(m)   (a referencia ouro deflacionada pelo CPI dos EUA, declarado; US$ de dez/1994 por onca)
Por governo: valor no fim do mes de fronteira (inicio) e no fim do mes de fronteira (fim); variacao % = fim/inicio - 1;
  anualizada = (fim/inicio)^(12/n_meses) - 1, n_meses = meses entre as linhas usadas; linha anual: ano completo mais recente antes da fronteira.
"""
import csv
import datetime
import json
import math
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent                       # porquinho/
BRUTO = RAIZ / "bruto"
DADOS = RAIZ.parent                      # fontes/dados/
SERIES = RAIZ / "series"
SERIES.mkdir(exist_ok=True)
BASE = (1994, 12)
ULTIMO = (2026, 9)                       # ultimo mes inteiro (hoje 2026-10-20); cada linha termina onde a sua fonte termina
CAIXA = 100000.0
LOG = []


def log(*a):
    LOG.append(" ".join(str(x) for x in a))


def prox(k):
    y, m = k
    return (y + 1, 1) if m == 12 else (y, m + 1)


def ant(k):
    y, m = k
    return (y - 1, 12) if m == 1 else (y, m - 1)


def meses_entre(a, b):
    return (b[0] - a[0]) * 12 + (b[1] - a[1])


MESES = []
k = BASE
while k <= ULTIMO:
    MESES.append(k)
    k = prox(k)

# ------------------------------------------------------------------ leitura
def sgs_mensal(arq):
    d = {}
    for x in json.load(open(arq)):
        dd, mm, aa = x["data"].split("/")
        d[(int(aa), int(mm))] = float(x["valor"])
    return d


def sgs_diaria(arqs):
    d = {}
    for a in arqs:
        for x in json.load(open(a)):
            dd, mm, aa = x["data"].split("/")
            d[(int(aa), int(mm), int(dd))] = float(x["valor"])
    return d


def ipea(arq):
    d = {}
    for x in json.load(open(arq))["value"]:
        if x["VALVALOR"] is None or x["NIVNOME"] not in ("", "Brasil"):
            continue
        d[(int(x["VALDATA"][:4]), int(x["VALDATA"][5:7]))] = float(x["VALVALOR"])
    return d


def fred(arq):
    d = {}
    for r in list(csv.reader(open(arq)))[1:]:
        if len(r) == 2 and r[1] not in (".", ""):
            d[(int(r[0][:4]), int(r[0][5:7]))] = float(r[1])
    return d


def indice(taxas, base=BASE, fim=ULTIMO):
    """I(base)=1; fator mensal 1+t/100. Para no ultimo mes consecutivo disponivel."""
    out, v, k = {base: 1.0}, 1.0, prox(base)
    while k <= fim and k in taxas:
        v *= 1 + taxas[k] / 100
        out[k] = v
        k = prox(k)
    return out


def exige_continua(nome, d, ate):
    ks = sorted(d)
    for a, b in zip(ks, ks[1:]):
        assert b == prox(a), f"{nome}: buraco entre {a} e {b}"
    log(f"{nome}: {ks[0]} ate {ks[-1]} ({len(ks)} meses), continua")


# inflacao (reuso ../inflacao + extensao 2026 desta pasta)
IPCA_T = {**sgs_mensal(DADOS / "inflacao/ipca-sgs433-raw.json"), **sgs_mensal(BRUTO / "sgs433-ipca-2026.json")}
INPC_T = {**sgs_mensal(DADOS / "inflacao/inpc-sgs188-raw.json"), **sgs_mensal(BRUTO / "sgs188-inpc-2026.json")}
IGPDI_T = {**sgs_mensal(DADOS / "inflacao/igpdi-sgs190-raw.json"), **sgs_mensal(BRUTO / "sgs190-igpdi-2026.json")}
FIPE_T = ipea(DADOS / "poder-de-compra/bruto/ipeadata-FIPE12_FIPE0001-raw.json")
INF1_T = ipea(DADOS / "poder-de-compra/bruto/ipeadata-DIMAC12_INF1-raw.json")
I_IPCA, I_INPC, I_IGPDI, I_FIPE = (indice(IPCA_T), indice(INPC_T), indice(IGPDI_T), indice(FIPE_T))
for nome, ix in (("IPCA", I_IPCA), ("INPC", I_INPC), ("IGP-DI", I_IGPDI), ("IPC-Fipe", I_FIPE)):
    log(f"indice {nome}: {BASE} ate {max(ix)}  I(fim)={ix[max(ix)]:.6f}")
assert max(I_IPCA) == ULTIMO

# Ipea renda muito baixa: emenda em dez/2006 (INF1 so existe desde 2006-07; pre-registro diz 2007+)
EMENDA_IPEA = (2006, 12)
I_IPEA = {k: I_IPCA[k] for k in I_IPCA if k <= EMENDA_IPEA}
v, k = I_IPCA[EMENDA_IPEA], prox(EMENDA_IPEA)
while k in INF1_T and k <= ULTIMO:
    v *= 1 + INF1_T[k] / 100
    I_IPEA[k] = v
    k = prox(k)
log(f"Ipea renda muito baixa: INF1 {min(INF1_T)} ate {max(INF1_T)}; indice emendado ate {max(I_IPEA)}")

# ICV-DIEESE: taxas anuais dez/dez 1997-2019 (reuso poder-de-compra/series/poder_de_compra.csv)
ICV = {}
for r in csv.DictReader(open(DADOS / "poder-de-compra/series/poder_de_compra.csv")):
    if r["indicador"] == "inflacao_dez_dez_icv_dieese":
        ICV[int(r["ano"])] = float(r["valor"])
assert sorted(ICV) == list(range(1997, 2020))
I_ICV = {(1996, 12): I_IPCA[(1996, 12)]}
for a in range(1997, 2020):
    I_ICV[(a, 12)] = I_ICV[(a - 1, 12)] * (1 + ICV[a] / 100)

# poupanca (SGS 25 principal; SGS 195 so conferencia) e Selic
S25 = sgs_diaria([BRUTO / f for f in (
    "sgs25-poupanca-1995-2000.json", "sgs25-poupanca-2001-2004.json", "sgs25-poupanca-2005-2012.json",
    "sgs25-poupanca-2012-2017.json", "sgs25-poupanca-2018-2026-refeito.json")])
S195 = sgs_diaria([BRUTO / f for f in ("sgs195-poupanca-2012-2017.json", "sgs195-poupanca-2018-2022.json", "sgs195-poupanca-2022-2026.json")])
P25 = {(y, m): v for (y, m, d), v in S25.items() if d == 1}
P195 = {(y, m): v for (y, m, d), v in S195.items() if d == 1}
SELIC_T = sgs_mensal(BRUTO / "sgs4390-selic-mensal.json")
for nome, t in (("poupanca SGS25 dia 1", P25), ("poupanca SGS195 dia 1", P195), ("Selic SGS4390", SELIC_T)):
    ks = [k for k in sorted(t) if k >= (1995, 1)]
    log(f"{nome}: {ks[0]} ate {ks[-1]} ({len(ks)} meses)")
I_POUP = indice(P25)
I_SELIC = indice(SELIC_T)
assert max(I_POUP) >= ULTIMO and max(I_SELIC) >= ULTIMO

# relativas
SM = ipea(DADOS / "economia-real/ipeadata-MTE12_SALMIN12-raw.json")
CESTA = ipea(DADOS / "quebras/bruto/ipeadata-DIEESE12_CBSP12-raw.json")
PIBPC = {k[0]: v * 1000 for k, v in ipea(DADOS / "economia-real/ipeadata-GAC_PIBCAPN-raw.json").items()}

# externas
PTAX = sgs_mensal(BRUTO / "sgs3698-ptax-venda-media-mensal.json")
PTAX_FIM = sgs_mensal(BRUTO / "sgs3696-dolar-venda-fim-mes.json")
CPI_US = fred(BRUTO / "fred-CPIAUCSL.csv")
CHF_USD = fred(BRUTO / "fred-EXSZUS.csv")
CPI_CH_FRED = fred(BRUTO / "fred-CHECPIALLMINMEI.csv")
CPI_CH = {}
for r in csv.reader(open(BRUTO / "snb-plkopr-ipc-suica.csv", encoding="utf-8-sig"), delimiter=";"):
    if len(r) == 3 and r[1] == "LD2010100" and r[2]:
        CPI_CH[(int(r[0][:4]), int(r[0][5:7]))] = float(r[2])
XDR = {}
for ano, mes, val in re.findall(r'<Obs TIME_PERIOD="(\d{4})-M(\d{2})" OBS_VALUE="([^"]+)"', (BRUTO / "imf-er-usa-xdr_usd-pa-m.xml").read_text()):
    XDR[(int(ano), int(mes))] = float(val)
USD_XDR = {}
for ano, mes, val in re.findall(r'<Obs TIME_PERIOD="(\d{4})-M(\d{2})" OBS_VALUE="([^"]+)"', (BRUTO / "imf-er-usa-usd_xdr-pa-m.xml").read_text()):
    USD_XDR[(int(ano), int(mes))] = float(val)


def ouro_wb():
    z = zipfile.ZipFile(BRUTO / "wb-pinksheet-monthly.xlsx")
    M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    ss = ["".join(t.text or "" for t in si.iter(M + "t")) for si in ET.fromstring(z.read("xl/sharedStrings.xml"))]
    sh = ET.fromstring(z.read("xl/worksheets/sheet2.xml"))
    out, cab = {}, {}
    for row in sh.find(M + "sheetData"):
        cel = {}
        for c in row:
            v = c.find(M + "v")
            if v is not None:
                cel[re.match(r"[A-Z]+", c.get("r")).group()] = ss[int(v.text)] if c.get("t") == "s" else v.text
        n = int(row.get("r"))
        if n == 5:
            cab = cel
        if n == 6:
            assert cab["BR"] == "Gold" and cel["BR"] == "($/troy oz)", (cab.get("BR"), cel.get("BR"))
        m = re.fullmatch(r"(\d{4})M(\d{2})", cel.get("A", ""))
        if m and "BR" in cel:
            out[(int(m.group(1)), int(m.group(2)))] = float(cel["BR"])
    return out


OURO = ouro_wb()
for nome, t in (("PTAX 3698", PTAX), ("CPI EUA", CPI_US), ("EXSZUS", CHF_USD), ("CPI Suica SNB", CPI_CH), ("IMF XDR_USD", XDR), ("ouro WB", OURO)):
    ks = sorted(k for k in t if k >= BASE)
    log(f"{nome}: {ks[0]} ate {ks[-1]} ({len(ks)} meses; faltam: {[k for k in MESES if k not in t and k <= ks[-1]]})")

# ------------------------------------------------------------------ vintage (curto) e emissao
V_INF = "SGS 433/188/190 ate 2025-12 de ../inflacao (baixado 2026-10-19) + 2026 desta pasta (baixado 2026-10-20)"
V_BCB = "BCB SGS, baixado 2026-10-20"
LINHAS = []          # (linha, ano, mes|None, valor, unidade, nota, vintage)
DADOSL = {}          # linha -> {chave: valor}  chave (ano, mes) ou (ano, None)
UNID = {}


def emit(linha, chave, valor, unidade, nota, vint):
    LINHAS.append((linha, chave[0], chave[1], valor, unidade, nota, vint))
    DADOSL.setdefault(linha, {})[chave] = valor
    UNID[linha] = unidade


def serie_caixa(linha, ix, nota, vint):
    for k in MESES:
        if k in ix:
            emit(linha, k, CAIXA / ix[k], "R$ de dez/1994", nota, vint)


serie_caixa("caixa_real_ipca", I_IPCA, "100000/I_IPCA; base fim de dez/1994", V_INF)
serie_caixa("caixa_real_inpc", I_INPC, "100000/I_INPC", V_INF)
serie_caixa("caixa_real_igpdi", I_IGPDI, "100000/I_IGPDI", V_INF)
serie_caixa("caixa_real_ipcfipe", I_FIPE, "100000/I_IPC-Fipe", "Ipeadata FIPE12_FIPE0001, baixado 2026-10-19 (../poder-de-compra)")
serie_caixa("caixa_real_ipea_renda_muito_baixa", {k: v for k, v in I_IPEA.items() if k >= EMENDA_IPEA}, "ate dez/2006 igual ao IPCA (emenda); jan/2007+ deflator Ipea INF1", "Ipeadata DIMAC12_INF1, baixado 2026-10-19 (../poder-de-compra); IPCA como acima")
serie_caixa("caixa_real_icv_dieese", I_ICV, "so pontos de dezembro; ate dez/1996 igual ao IPCA (emenda); taxa anual do DIEESE 1997-2019", "../poder-de-compra/series/poder_de_compra.csv (notas anuais DIEESE)")

for k in MESES:
    if k in I_POUP:
        emit("poupanca_nominal", k, CAIXA * I_POUP[k], "R$ correntes", "SGS 25 dia 1; creditado no fim do mes", V_BCB)
        emit("poupanca_real_ipca", k, CAIXA * I_POUP[k] / I_IPCA[k], "R$ de dez/1994", "poupanca_nominal/I_IPCA", V_BCB + "; " + V_INF)
        emit("caixa_menos_poupanca_real_ipca", k, CAIXA / I_IPCA[k] - CAIXA * I_POUP[k] / I_IPCA[k], "R$ de dez/1994", "caixa_real_ipca - poupanca_real_ipca", V_BCB + "; " + V_INF)
    if k in I_SELIC:
        emit("selic_nominal", k, CAIXA * I_SELIC[k], "R$ correntes", "SGS 4390 acumulada no mes", V_BCB)
        emit("selic_real_ipca", k, CAIXA * I_SELIC[k] / I_IPCA[k], "R$ de dez/1994", "selic_nominal/I_IPCA", V_BCB + "; " + V_INF)

for a in range(BASE[0] + 0, 2025):
    if a in PIBPC:
        emit("caixa_em_anos_pib_per_capita_nominal", (a, None), CAIXA / PIBPC[a], "anos de PIB per capita nominal", "anual; GAC_PIBCAPN (R$ mil x1000); serie estimada pelo Ipea", "Ipeadata GAC_PIBCAPN, atualizada na fonte em 2025-08-20 (../economia-real)")
for k in MESES:
    if k in SM:
        emit("caixa_em_salarios_minimos", k, CAIXA / SM[k], "salarios minimos", "100000 / SM nominal vigente do mes", "Ipeadata MTE12_SALMIN12 (../economia-real)")
    if k in CESTA:
        emit("caixa_em_cestas_dieese_sp", k, CAIXA / CESTA[k], "cestas DIEESE Sao Paulo", "100000 / custo nominal da cesta do mes", "Ipeadata DIEESE12_CBSP12 (../quebras/bruto)")

# externas
def ate_onde(*dicts):
    """Meses (BASE..ULTIMO) em que TODAS as fontes tem dado. Buraco isolado (ex.: CPI dos EUA de out/2025, nao coletado) = sem linha naquele mes."""
    return [k for k in MESES if all(k in d for d in dicts)]


V_X = "PTAX SGS 3698 (BCB, 2026-10-20)"
for k in ate_onde(PTAX):
    u = CAIXA / PTAX[k]
    emit("usd_nominal", k, u, "US$ correntes", "100000/PTAX venda media do mes", V_X)
    if k in CPI_US:
        emit("usd_poder_compra_ref", k, u * CPI_US[BASE] / CPI_US[k], "US$ de dez/1994", "usd_nominal x CPI_EUA(dez/94)/CPI_EUA(mes)", V_X + "; FRED CPIAUCSL (curl 2026-10-20)")
for k in ate_onde(PTAX, CHF_USD):
    c = CAIXA * CHF_USD[k] / PTAX[k]
    emit("chf_nominal", k, c, "CHF correntes", "100000 x EXSZUS/PTAX; media do mes", V_X + "; FRED EXSZUS (curl 2026-10-20)")
    if k in CPI_CH:
        emit("chf_poder_compra_ref", k, c * CPI_CH[BASE] / CPI_CH[k], "CHF de dez/1994", "chf_nominal x CPI_CH(dez/94)/CPI_CH(mes); CPI Suica = SNB plkopr LD2010100", "SNB cubo plkopr, baixado 2026-10-20")
for k in ate_onde(PTAX, XDR):
    s_ = CAIXA / PTAX[k] * XDR[k]
    emit("sdr_nominal", k, s_, "DES correntes", "usd_nominal x DES por US$ (IMF ER XDR_USD, media do mes)", V_X + "; IMF ER (SDMX api.imf.org, 2026-10-20)")
    if k in CPI_US:
        emit("sdr_poder_compra_ref", k, s_ * CPI_US[BASE] / CPI_US[k], "DES de dez/1994", "sdr_nominal x CPI_EUA(dez/94)/CPI_EUA(mes); DES sem inflacao propria: CPI EUA (declarado)", "IMF ER; FRED CPIAUCSL")
for k in ate_onde(PTAX, OURO):
    emit("ouro_oncas", k, CAIXA / PTAX[k] / OURO[k], "onças troy", "usd_nominal / ouro US$ por onça (Pink Sheet, media do mes); quantidade, nao se deflaciona", V_X + "; Banco Mundial Pink Sheet (out/2026)")
    if k in CPI_US:
        emit("ouro_preco_real_usd_oz", k, OURO[k] * CPI_US[BASE] / CPI_US[k], "US$ de dez/1994 por onça", "ouro x CPI_EUA(dez/94)/CPI_EUA(mes) (CPI EUA, declarado)", "Banco Mundial Pink Sheet; FRED CPIAUCSL")

with open(SERIES / "porquinho.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["linha", "ano", "mes", "valor", "unidade", "nota", "vintage"])
    for lin, a, m, v, u, n, vt in LINHAS:
        w.writerow([lin, a, "" if m is None else m, f"{v:.6f}", u, n, vt])
log(f"porquinho.csv: {len(LINHAS)} linhas, {len(DADOSL)} indicadores")

# ------------------------------------------------------------------ por governo
def chave_fronteira(d):
    if d.day == 1:
        return ant((d.year, d.month))
    if (d + datetime.timedelta(days=1)).day == 1:
        return (d.year, d.month)
    raise ValueError(d)


MAND = []
for r in csv.DictReader(open(BRUTO / "mandatos.csv")):
    MAND.append((r["id"], r["nome"], datetime.date.fromisoformat(r["posse"]), datetime.date.fromisoformat(r["saida"])))
MAND = MAND[[m[0] for m in MAND].index("fhc"):]
log("mandatos:", [m[0] for m in MAND])


def busca(serie, chave, fim=False):
    """Valor no fim do mes `chave`; linha anual usa o ano completo mais recente ate a fronteira. Devolve (rotulo, valor) ou None."""
    d = DADOSL[serie]
    anual = any(k[1] is None for k in d)
    if anual:
        ano = chave[0] if chave[1] == 12 else chave[0] - 1
        anos = [k[0] for k in d]
        if fim and ano > max(anos):
            ano = max(anos)
        return (str(ano), d[(ano, None)]) if (ano, None) in d else None
    if chave in d:
        return (f"{chave[0]}-{chave[1]:02d}", d[chave])
    if fim:
        ult = max(k for k in d if k <= chave) if any(k <= chave for k in d) else None
        if ult and ult >= (2026, 1) and chave > max(d):   # mandato em curso: usa o ultimo mes da propria linha
            return (f"{ult[0]}-{ult[1]:02d}", d[ult])
    return None


def ano_de(rot):
    return int(rot[:4])


def meses_rot(r1, r2):
    if len(r1) == 4:
        return (int(r2) - int(r1)) * 12
    return meses_entre((int(r1[:4]), int(r1[5:])), (int(r2[:4]), int(r2[5:])))


DIFLIN = {"caixa_menos_poupanca_real_ipca"}
NOTA_LINHA = {
    "caixa_real_ipea_renda_muito_baixa": "emenda: ate dez/2006 a linha e o IPCA; deflator Ipea INF1 de jan/2007 em diante (linha so emitida de dez/2006)",
    "caixa_real_icv_dieese": "so pontos de dezembro 1996-2019; ate dez/1996 igual ao IPCA; sem interpolar (ICV anual, pesquisa suspensa em 2020-03)",
    "caixa_em_anos_pib_per_capita_nominal": "linha anual: ano completo mais recente antes da fronteira (1994 = ano do inicio de 1995); n_meses = 12 x anos entre os anos usados",
    "ouro_oncas": "quantidade fisica; nao se deflaciona",
    "poupanca_nominal": "SGS 25 (regra de deposito ate 03/05/2012, que segue publicada); SGS 195 so em _conferencias.txt",
}
out = []
for lin in DADOSL:
    for gid, nome, ini, fim in MAND:
        k0, k1 = chave_fronteira(ini), (chave_fronteira(fim) if fim <= datetime.date(2026, 9, 30) else ULTIMO)
        b0, b1 = busca(lin, k0), busca(lin, k1, fim=True)
        nota = NOTA_LINHA.get(lin, "")
        if fim > datetime.date(2026, 9, 30):
            nota = (nota + "; " if nota else "") + f"mandato em curso: fim = ultimo mes da linha (mandato registrado ate {fim})"
        if not b0 or not b1:
            miss = "inicio" if not b0 else "fim"
            out.append([lin, gid, nome, "", "", "", "", "", "", "", "", UNID[lin], f"sem observacao no limite de {miss} (linha anual/parcial); " + nota])
            continue
        (r0, v0), (r1, v1) = b0, b1
        n = meses_rot(r0, r1)
        if n <= 0:
            out.append([lin, gid, nome, r0, r1, f"{v0:.6f}", f"{v1:.6f}", "", "", "", n, UNID[lin], "janela vazia; " + nota])
            continue
        absv = v1 - v0
        pct = anual = ""
        if lin not in DIFLIN and v0 > 0 and v1 > 0:
            pct = f"{(v1 / v0 - 1) * 100:.4f}"
            anual = f"{((v1 / v0) ** (12 / n) - 1) * 100:.4f}"
        out.append([lin, gid, nome, r0, r1, f"{v0:.6f}", f"{v1:.6f}", f"{absv:.6f}", pct, anual, n, UNID[lin], nota])

with open(SERIES / "porquinho_por_governo.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["linha", "governo_id", "governo", "inicio_usado", "fim_usado", "valor_inicio", "valor_fim", "variacao_abs", "variacao_pct", "variacao_anualizada_pct_aa", "n_meses", "unidade", "nota"])
    w.writerows(out)

# ------------------------------------------------------------------ conferencias
def c(msg):
    log("CONF:", msg)


# 1. SGS 25 dia 1 contra Ipeadata ANBIMA12_TJPOUP12; SGS 195 dia 1 contra BM12_RNDPO12
a = ipea(BRUTO / "ipeadata-ANBIMA12_TJPOUP12-raw.json")
b = ipea(BRUTO / "ipeadata-BM12_RNDPO12-raw.json")
d1 = [k for k in P25 if k in a and abs(P25[k] - a[k]) > 0.0051]
d2 = [k for k in P195 if k in b and abs(P195[k] - b[k]) > 0.0051]
c(f"SGS 25 (dia 1) vs Ipeadata ANBIMA12_TJPOUP12: {sum(1 for k in P25 if k in a)} meses comparados, {len(d1)} divergencias > 0,0051")
c(f"SGS 195 (dia 1) vs Ipeadata BM12_RNDPO12: {sum(1 for k in P195 if k in b)} meses comparados, {len(d2)} divergencias > 0,0051")
# 2. PTAX
e = ipea(BRUTO / "ipeadata-BM12_ERV12-raw.json")
dd = [(k, PTAX[k], e[k]) for k in sorted(PTAX) if k in e and abs(PTAX[k] - e[k]) > 1e-9]
mx = max(dd, key=lambda t: abs(t[1] / t[2] - 1))
c(f"SGS 3698 vs Ipeadata BM12_ERV12 (venda, media): {sum(1 for k in PTAX if k in e)} meses, {len(dd)} diferem; maior diferenca relativa {abs(mx[1]/mx[2]-1)*100:.3f}% em {mx[0]} ({mx[1]} vs {mx[2]})")
e2 = ipea(BRUTO / "ipeadata-BM12_ERVF12-raw.json")
dd2 = [(k, PTAX_FIM[k], e2[k]) for k in sorted(PTAX_FIM) if k in e2 and abs(PTAX_FIM[k] - e2[k]) > 1e-9]
c(f"SGS 3696 vs Ipeadata BM12_ERVF12 (venda, fim): {len(dd2)} divergencias: {dd2}")
# 3. Selic
e3 = ipea(BRUTO / "ipeadata-BM12_TJOVER12-raw.json")
d3 = [k for k in SELIC_T if k in e3 and abs(SELIC_T[k] - e3[k]) > 0.0051]
c(f"SGS 4390 vs Ipeadata BM12_TJOVER12: {sum(1 for k in SELIC_T if k in e3)} meses, {len(d3)} divergencias > 0,0051")
# 4. IGP-DI cadeia SGS 190 vs indice Ipeadata
ix = {(int(x["VALDATA"][:4]), int(x["VALDATA"][5:7])): float(x["VALVALOR"]) for x in json.load(open(DADOS / "inflacao/igpdi-ipeadata-raw.json"))["value"] if x["VALVALOR"] is not None}
r_sgs = I_IGPDI[(2025, 12)]
r_ip = ix[(2025, 12)] / ix[(1994, 12)]
c(f"IGP-DI dez/1994->dez/2025: cadeia SGS 190 = {r_sgs:.6f}; indice Ipeadata IGP12_IGPDI12 = {r_ip:.6f}; razao {r_sgs/r_ip:.6f}")
# 5. IPC-Fipe cadeia vs indice Ipeadata
fx = ipea(DADOS / "poder-de-compra/bruto/ipeadata-FIPE12_IPCFIPE12-raw.json")
c(f"IPC-Fipe dez/1994->ago/2026: cadeia da taxa = {I_FIPE[(2026,8)]:.6f}; indice Ipeadata FIPE12_IPCFIPE12 = {fx[(2026,8)]/fx[(1994,12)]:.6f}")
# 6. IPCA: cadeia vs variacao 12 meses conhecida (dez/2025)
c(f"IPCA acumulado 12 meses a dez/2025 (cadeia SGS 433): {(I_IPCA[(2025,12)]/I_IPCA[(2024,12)]-1)*100:.4f}%")
# 7. IPC suico FRED (OECD MEI) vs SNB no overlap, taxas de 12 meses
ov = [k for k in CPI_CH_FRED if k in CPI_CH and k >= (1996, 1)]
rel = [abs((CPI_CH_FRED[k] / CPI_CH_FRED[(k[0] - 1, k[1])]) / (CPI_CH[k] / CPI_CH[(k[0] - 1, k[1])]) - 1) for k in ov if (k[0] - 1, k[1]) in CPI_CH_FRED]
c(f"IPC suico FRED CHECPIALLMINMEI ate {max(CPI_CH_FRED)} vs SNB LD2010100: {len(rel)} meses no overlap, maior diferenca na variacao de 12 meses = {max(rel)*100:.4f}% relativo")
# 8. regra nova da poupanca: SGS 195 a partir de jun/2012 (so para deposito novo) -- diferenca declarada, nao e linha
nova = {BASE: 1.0}
v = 1.0
for k in MESES[1:]:
    t = P25[k] if k < (2012, 6) else P195.get(k, P25[k])
    v *= 1 + t / 100
    nova[k] = v
k = ULTIMO
c(f"poupanca com a regra nova (SGS 195) a partir de jun/2012, em {k}: R$ {CAIXA*nova[k]:,.2f} nominais contra R$ {CAIXA*I_POUP[k]:,.2f} pela regra antiga (SGS 25); real IPCA {CAIXA*nova[k]/I_IPCA[k]:,.2f} contra {CAIXA*I_POUP[k]/I_IPCA[k]:,.2f}")
ks = [k for k in MESES if k >= (2012, 6) and P25[k] != P195[k]]
c(f"meses (dia 1) em que SGS 25 e SGS 195 diferem: {len(ks)}, de {ks[0]} a {ks[-1]}")
# 9. cambio: media do mes (usado) vs fim do mes (conferencia) no limite dos mandatos
for kk in ((2002, 12), (2010, 12), (2022, 12)):
    c(f"US$ por R$ 100.000 em {kk}: media do mes {CAIXA/PTAX[kk]:,.0f} ; fim do mes {CAIXA/PTAX_FIM[kk]:,.0f}")
# 10. escala
for lin in ("caixa_real_ipca", "poupanca_real_ipca", "selic_real_ipca", "usd_poder_compra_ref", "chf_poder_compra_ref", "sdr_poder_compra_ref", "ouro_oncas", "caixa_em_salarios_minimos", "caixa_em_cestas_dieese_sp"):
    d = DADOSL[lin]
    ult = max(k for k in d if k[1] is not None)
    c(f"{lin}: base {d.get(BASE, float('nan')):,.2f} -> {ult} {d[ult]:,.2f}")
(SERIES / "_conferencias.txt").write_text("\n".join(LOG) + "\n")
print("\n".join(LOG))
