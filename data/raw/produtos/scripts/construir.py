#!/usr/bin/env python3
"""Produtos (bloco "produtos", emenda 03, secao F): reconstrucao a partir do BRUTO ja hasheado.

Uso:  python3 -I construir.py        (sem rede; le so arquivos locais)
Le:   ../bruto (esta pasta), ../../economia-real, ../../inflacao, ../../quebras,
      /Users/ulissesflores/Developer/brazil-governments-factcheck/data/curated/mandatos.csv
Gera: ../series/produtos.csv, ../series/produtos_em_horas.csv, ../series/produtos_por_governo.csv,
      ../series/_conferencias.txt

Sem opiniao, sem nota, sem causa. Nenhum produto tem elasticidade-preco zero (ver elasticidade.md).
"""
import csv
import datetime
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent                       # produtos/
DADOS = RAIZ.parent                      # fontes/dados/
BRUTO = RAIZ / "bruto"
SERIES = RAIZ / "series"
SERIES.mkdir(exist_ok=True)
sys.path.insert(0, str(AQUI))
import xlsx_min  # noqa: E402

MANDATOS = Path("/Users/ulissesflores/Developer/brazil-governments-factcheck/data/curated/mandatos.csv")
HORAS_MES = 220          # DIEESE: salario minimo / 220 h por mes (metodologia da cesta, secao 4)
DIAS_MES = 365 / 12      # mesma escolha de quebras/pobreza-linhas-em-reais-reais.csv
LOG = []
HOJE = "2026-10-20"
VINT_DIEESE = f"DIEESE, banco de dados publico da Pesquisa Nacional da Cesta Basica, consulta POST em {HOJE}"
VINT_ANP = f"ANP, serie historica do levantamento de precos (mensal Brasil), baixado {HOJE}"
VINT_EE = f"Ipeadata ELETRO12_CEETRES12 (ANEEL desde 2003; Eletrobras ate 2002), baixado {HOJE}"
VINT_BUS = f"Prefeitura de Sao Paulo, planilha tarifaria (pagina capturada 2026-01-02, baixada {HOJE}) + fontes secundarias na nota"


def log(s):
    LOG.append(s)


# ---------------------------------------------------------------- leitura
def num_br(v):
    v = v.strip()
    if v in ("", "-"):
        return None
    return float(v.replace(".", "").replace(",", "."))


def dieese(arq):
    h = (BRUTO / "dieese" / arq).read_text(encoding="utf-8", errors="replace")
    out = {}
    for d, v in re.findall(r"<tr>\s*<td>([^<]*)</td>\s*<td>([^<]*)</td>", h):
        m, y = d.split("-")
        out[(int(y), int(m))] = num_br(v)
    return out


ITENS = {  # produto -> (arquivo, unidade do preco, quantidade mensal DL 399 regiao 1 [para a conferencia])
    "arroz": ("arroz", "R$/kg", 3.0),
    "feijao": ("feijao", "R$/kg", 4.5),
    "pao_frances": ("pao", "R$/kg", 6.0),
    "cafe_em_po": ("cafe", "R$/kg", 0.6),
    "acucar": ("acucar", "R$/kg", 3.0),
    "leite": ("leite", "R$/litro", 7.5),
    "oleo": ("oleo", "R$/embalagem de oleo (o gasto mensal do DIEESE usa 1 x preco; tamanho nao declarado, 900 mL presumido)", 1.0),
    "carne_bovina": ("carne", "R$/kg", 6.0),
}
EXTRA_CONF = {"farinha": 1.5, "batata": 6.0, "tomate": 9.0, "banana": 7.5, "manteiga": 0.75}  # so p/ conferir unidades
dados_d = {p: dieese(f"dieese-sp-{a}-tipo4.html") for p, (a, _, _) in ITENS.items()}
extra_d = {n: dieese(f"dieese-sp-{n}-tipo4.html") for n in EXTRA_CONF}
total_gasto = dieese("dieese-sp-total-tipo5.html")

CORTES = [((1967, 1), 1000), ((1986, 3), 1000), ((1989, 1), 1000), ((1993, 8), 1000), ((1994, 7), 2750)]  # = poder-de-compra/scripts/construir.py


def divisor(k):
    d = 1
    for ini, f in CORTES:
        if ini > k:
            d *= f
    return d


def ipea(arq):
    d = {}
    for x in json.load(open(arq))["value"]:
        if x["VALVALOR"] is None:
            continue
        d[(int(x["VALDATA"][:4]), int(x["VALDATA"][5:7]))] = float(x["VALVALOR"])
    return d


sm = ipea(DADOS / "economia-real/ipeadata-MTE12_SALMIN12-raw.json")      # R$ atuais (conversao de moeda feita pelo Ipeadata)

# conferencia de unidades: preco x quantidade do DL 399 reproduz o gasto mensal publicado
log("CONFERENCIA DE UNIDADES: soma(preco x quantidade DL 399, regiao 1) / gasto mensal publicado (Total da cesta)")
todos = {**{p: (dados_d[p], ITENS[p][2]) for p in ITENS}, **{n: (extra_d[n], q) for n, q in EXTRA_CONF.items()}}
for k in [(1960, 6), (1975, 6), (1985, 6), (2005, 6), (2012, 6), (2015, 6), (2016, 6), (2019, 5), (2024, 5), (2026, 8)]:
    s = sum(d[k] * q for d, q in todos.values() if d.get(k) is not None)
    log(f"  {k[0]}-{k[1]:02d}: soma {s:.2f} | publicado {total_gasto[k]:.2f} | razao {s / total_gasto[k]:.4f}")

def tab_dez2015(f):
    import html as _h
    h = (BRUTO / "dieese" / f).read_text(encoding="utf-8", errors="replace")
    cab = [re.sub(r"\s+", " ", _h.unescape(c)).strip() for c in re.findall(r"<th[^>]*>(.*?)</th>", h, re.S)][1:]
    cel = [num_br(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", h, re.S)[1:]]
    return dict(zip(cab, cel))


gasto15 = tab_dez2015("dieese-data-dez2015-velho.html")
NOMEDB = {"arroz": "Arroz", "feijao": "Feijão", "pao_frances": "Pão", "cafe_em_po": "Café", "acucar": "Açúcar", "leite": "Leite", "oleo": "Óleo", "carne_bovina": "Carne"}
log("CONFERENCIA ITEM A ITEM (dez/2015, metodo antigo): gasto mensal publicado do item / preco medio do item = quantidade implicita")
for p, nome in NOMEDB.items():
    qi = gasto15[nome] / dados_d[p][(2015, 12)]
    log(f"  {p}: gasto {gasto15[nome]:.2f} / preco {dados_d[p][(2015, 12)]:.2f} = {qi:.3f} (quantidade do DL 399, regiao 1: {ITENS[p][2]})")
log("OLEO: quantidade implicita = (gasto total - soma dos outros 12 itens x quantidade DL 399) / preco do oleo; 1960-2026 em 1,00 +-0,02 (nao 0,75)")

# ---------------------------------------------------------------- ANP
def anp_mensal(arq):
    c = list(xlsx_min.ler(BRUTO / "anp" / arq).values())[0]
    linhas = sorted({k[0] for k in c})
    hdr = next(r for r in linhas if str(c.get((r, 1), "")).strip().upper() == "MÊS")
    cab = {str(c.get((hdr, j), "")).upper().replace("Ç", "C"): j for j in range(1, 20)}
    jpreco = next(j for n, j in cab.items() if n.startswith("PRECO MEDIO REVENDA") or n.startswith("PREÇO MÉDIO REVENDA") or n.startswith("PRECO MÉDIO REVENDA"))
    jpostos = cab["NÚMERO DE POSTOS PESQUISADOS"] if "NÚMERO DE POSTOS PESQUISADOS" in cab else 3
    out = {"GLP": {}, "GASOLINA COMUM": {}}
    for r in linhas:
        if r <= hdr:
            continue
        prod = str(c.get((r, 2), "")).strip().upper()
        if prod in out:
            d = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(c[(r, 1)]))
            out[prod][(d.year, d.month)] = (c[(r, jpreco)], c.get((r, jpostos)))
    return out


a1 = anp_mensal("mensal-brasil-2001-a-2012.xlsx")
a2 = anp_mensal("mensal-brasil-desde-jan2013.xlsx")
anp = {k: {**a1[k], **a2[k]} for k in a1}
for k in anp:
    ms = sorted(anp[k])
    falt = [(y, m) for y in range(2001, 2027) for m in range(1, 13) if (2001, 7) <= (y, m) <= ms[-1] and (y, m) not in anp[k]]
    log(f"ANP {k}: {len(ms)} meses de {ms[0]} a {ms[-1]}; meses ausentes no intervalo: {falt}")
    log(f"ANP {k}: postos pesquisados min/max {min(v[1] for v in anp[k].values()):.0f}/{max(v[1] for v in anp[k].values()):.0f}")

# ---------------------------------------------------------------- BEN/EPE anual (so para cobrir 1994-2000)
ben_gas = {k[0]: v / 1000 for k, v in ipea(BRUTO / "anp/ipeadata-ANP_PRGASOL-raw.json").items()}   # R$/m3 -> R$/l
ben_glp = {k[0]: v * 13 / 1000 for k, v in ipea(BRUTO / "anp/ipeadata-ANP_PRGLP-raw.json").items()}  # R$/t -> R$/13 kg
for y in (2002, 2003, 2005, 2010, 2012, 2013, 2018, 2022, 2025):
    ag = [v[0] for k, v in anp["GASOLINA COMUM"].items() if k[0] == y]
    al = [v[0] for k, v in anp["GLP"].items() if k[0] == y]
    if len(ag) == 12:
        log(f"BEN x ANP {y}: gasolina BEN {ben_gas[y]:.3f} | ANP media {sum(ag) / 12:.3f} (razao {ben_gas[y] / (sum(ag) / 12):.3f}); GLP 13 kg BEN {ben_glp[y]:.2f} | ANP {sum(al) / 12:.2f} (razao {ben_glp[y] / (sum(al) / 12):.3f})")

# ---------------------------------------------------------------- energia
ee = {k: v / 1000 for k, v in ipea(BRUTO / "energia/ipeadata-ELETRO12_CEETRES12-raw.json").items() if k >= (1994, 7)}   # R$/MWh -> R$/kWh

# ---------------------------------------------------------------- onibus (municipio de Sao Paulo)
# (mes de vigencia, tarifa, fonte). Regra: mes da publicacao; publicacao nos ultimos dias de dezembro -> janeiro seguinte.
ONIBUS = [
    ((1994, 7), 0.50, "Band 2026-01-06 (historico desde o Plano Real); ANTP/G1 2018-12-31 ('R$ 0,50 em 1994'); Wikipedia pt SPTrans (R$ 0,50 em marco/1995)"),
    ((1995, 6), 0.65, "Wikipedia pt SPTrans ('aumentando para R$ 0,65 em junho de 1995'); fonte primaria nao aberta"),
    ((2005, 3), 2.00, "Prefeitura SP, planilha tarifaria: 'Publicada em 01/03/05, Decreto 45.749/05'"),
    ((2006, 12), 2.30, "Prefeitura SP: 'Publicada em 18/11/06, Decreto 47.919/06'; ICV-DIEESE: onibus municipal 0,00% de jan a nov/2006 (vigencia em dez/2006); CNN Brasil cita 30/11/2006"),
    ((2010, 1), 2.70, "Prefeitura SP: 'Publicada em 19/01/10, Decreto 51.134/09'; Terra: reajuste em janeiro"),
    ((2011, 1), 3.00, "Prefeitura SP: 'Publicada em 05/01/11, Decreto 52.041/10'"),
    ((2015, 1), 3.50, "Prefeitura SP: 'Publicada em 29/12/14, Portaria 106/14-SMT.GAB' (vigencia em janeiro/2015)"),
    ((2016, 1), 3.80, "Prefeitura SP: 'Publicada em 30/12/15, Portaria 121/15-SMT.GAB' (vigencia em janeiro/2016)"),
    ((2018, 1), 4.00, "Prefeitura SP: 'Publicada em 29/12/17, Portaria 229/17-SMT.GAB' (vigencia em janeiro/2018)"),
    ((2019, 1), 4.30, "Prefeitura SP: 'Publicada em 03/01/19'; ANTP/G1: vigencia a partir de 07/01/2019"),
    ((2020, 1), 4.40, "Prefeitura SP: 'Vigente a partir de 01/01/2020'"),
    ((2025, 1), 5.00, "Prefeitura SP: 'Vigente a partir de 06/01/2025'"),
    ((2026, 1), 5.30, "Band 2026-01-06 (portaria SMT; fonte secundaria; pagina da Prefeitura capturada antes da mudanca)"),
]
# 2013: R$ 3,20 publicada em 23/05/13 e revogada apos protestos; a tarifa em vigor no fim de cada mes de 2013 foi R$ 3,00 (Band) -> nao entra
# 2017-01: R$ 3,80 republicada em 02/01/17 (mesmo valor) -> sem mudanca


# Niveis de fim de ano DERIVADOS (nao observados) das taxas anuais do ICV-DIEESE para o "onibus municipal" (Tabela 8 de
# bruto/onibus/dieese-icv-2006-12-transporte.pdf): 1997 +12,50%, 1998 +11,11%, 1999 +15,00%, 2000 0, 2001 +21,74%, 2002 0,
# 2003 +21,44%, 2004 0, 2005 +17,66%, 2006 (ate nov) 0; acumulado 1997-nov/2006 = +150,00%. Ancorado na tarifa de R$ 2,00 (2005-03, Prefeitura):
# 2,00/1,1766 = 1,70 (fim de 2004); 1,70/1,2144 = 1,40 (2002); 1,40/1,2174 = 1,15 (2000); 1,15/1,15 = 1,00 (1998); 1,00/1,1111 = 0,90 (1997); 0,90/1,125 = 0,80 (dez/1996).
# Conta feita e conferida em series/_conferencias.txt. So dezembro de cada ano; o mes de cada reajuste dentro do ano nao e conhecido.
DERIVADOS_DEZ = {(1996, 12): 0.80, (1997, 12): 0.90, (1998, 12): 1.00, (1999, 12): 1.15, (2000, 12): 1.15, (2001, 12): 1.40, (2002, 12): 1.40, (2003, 12): 1.70, (2004, 12): 1.70}
_c = 1.0
for _r in (12.50, 11.11, 15.00, 0.0, 21.74, 0.0, 21.44, 0.0, 17.66):
    _c *= 1 + _r / 100
log(f"ICV-DIEESE onibus municipal, produto das taxas anuais 1997-2005: {(_c - 1) * 100:.2f}% (publicado: 150,00% ate nov/2006); 2,00/{_c:.4f} = {2.00 / _c:.3f} (dez/1996 derivado: 0,80)")


def onibus_serie():
    out = {}
    pontos = sorted(ONIBUS)
    for y in range(1994, 2027):
        for m in range(1, 13):
            k = (y, m)
            if k < (1994, 7) or k > (2026, 9):
                continue
            if k in DERIVADOS_DEZ:
                out[k] = DERIVADOS_DEZ[k]
                continue
            if (1995, 7) <= k < (2005, 3):
                continue                      # lacuna: so os dezembros derivados do ICV-DIEESE
            v = None
            for ini, t, _ in pontos:
                if ini <= k:
                    v = t
            out[k] = v
    return out


onibus = onibus_serie()

# ---------------------------------------------------------------- renda do decimo mais rico (PIP) e IPCA
import csv as _csv
pip = {"2017": {}, "2021": {}}
for r in _csv.DictReader(open(DADOS / "quebras/renda-por-decil.csv", encoding="utf-8")):
    if r["decil"] == "10":
        pip[r["ppc_base"]][int(r["ano"])] = (float(r["renda_per_capita_ppc_dolar_dia"]), r["pesquisa"], r["comparable_spell_segundo_a_fonte"])
fator = {}
for r in _csv.DictReader(open(DADOS / "quebras/pobreza-linhas-em-reais-reais.csv", encoding="utf-8")):
    m = re.search(r"PPC (\d{4})", r["linha"])
    fator[m.group(1)] = float(r["fator_R$_por_US$_PPC"])
log(f"Fatores R$ por US$ PPC (IBGE SIS / Ipeadata, como publicados): {fator}")

ipca_var = {}
for x in json.load(open(DADOS / "inflacao/ipca-sgs433-raw.json")):
    d, mm, aa = x["data"].split("/")
    ipca_var[(int(aa), int(mm))] = float(x["valor"])
ipca_idx, v = {}, 100.0
for k in sorted(ipca_var):
    v *= 1 + ipca_var[k] / 100
    ipca_idx[k] = v
ipca_ano = {}
for y in range(1980, 2027):
    ms = [ipca_idx.get((y, m)) for m in range(1, 13)]
    if all(x is not None for x in ms):
        ipca_ano[y] = sum(ms) / 12


def renda_decil10_mensal_nominal(ano, base):
    """US$ PPC/dia -> R$/mes a precos do ano-base (x 365/12 x fator IBGE) -> R$ nominais do ano (x IPCA medio do ano / IPCA medio do ano-base)."""
    if ano not in pip[base] or ano not in ipca_ano or int(base) not in ipca_ano:
        return None
    usd = pip[base][ano][0]
    return usd * DIAS_MES * fator[base] * ipca_ano[ano] / ipca_ano[int(base)]


# ---------------------------------------------------------------- series mensais finais (R$ atuais)
def conv(d):
    return {k: (v / divisor(k) if v is not None else None) for k, v in d.items()}


MENSAIS = {}   # produto -> dict {(ano, mes): valor em R$ atuais}
UNID = {}
FONTE = {}
DEFLINHA = {}
NOTAS = {}
for p, (a, un, q) in ITENS.items():
    MENSAIS[p] = {k: v for k, v in conv(dados_d[p]).items() if v is not None}
    UNID[p] = un
    FONTE[p] = "DIEESE, Pesquisa Nacional da Cesta Basica de Alimentos, Sao Paulo (banco de dados publico)"
    DEFLINHA[p] = "preco medio mensal em Sao Paulo (cidade 8, tipo de dado 4), convertido para reais atuais pelos cortes de moeda; nao ha deflacionamento"
    NOTAS[p] = "10 meses sem dado (1964-03 a 1964-12); metodologia 2016 a partir de 2016-01 (quebras.csv); antes de 1994-07 a moeda e a da epoca dividida pelo divisor acumulado"
MENSAIS["botijao_glp_13kg"] = {k: v[0] for k, v in anp["GLP"].items()}
UNID["botijao_glp_13kg"] = "R$/botijao 13 kg"
FONTE["botijao_glp_13kg"] = "ANP, levantamento de precos, preco medio de revenda, Brasil, mensal (produto GLP, R$/13kg)"
DEFLINHA["botijao_glp_13kg"] = "media simples dos precos de revenda coletados no mes em todo o Brasil; nao e preco de Sao Paulo"
NOTAS["botijao_glp_13kg"] = "serie comeca em 2001-07; sem pesquisa de 2020-08-18 a 2020-10-17; cobertura geografica e amostra mudam (quebras.csv)"
MENSAIS["gasolina_comum"] = {k: v[0] for k, v in anp["GASOLINA COMUM"].items()}
UNID["gasolina_comum"] = "R$/litro"
FONTE["gasolina_comum"] = "ANP, levantamento de precos, preco medio de revenda, Brasil, mensal (gasolina comum)"
DEFLINHA["gasolina_comum"] = "media simples dos precos de revenda coletados no mes em todo o Brasil; nao e preco de Sao Paulo"
NOTAS["gasolina_comum"] = NOTAS["botijao_glp_13kg"]
MENSAIS["energia_residencial"] = ee
UNID["energia_residencial"] = "R$/kWh"
FONTE["energia_residencial"] = "Ipeadata ELETRO12_CEETRES12 (tarifa media residencial = receita de fornecimento / consumo; Eletrobras ate 2002, ANEEL desde 2003), R$/MWh dividido por 1000"
DEFLINHA["energia_residencial"] = "tarifa MEDIA do Brasil (receita/consumo da classe residencial), nao a tarifa de uma distribuidora; inclui tributos? nao informado pela fonte"
NOTAS["energia_residencial"] = "so de 1994-07 a 2026-06; antes disso a serie mistura moedas e nao foi usada (quebras.csv)"
MENSAIS["onibus_sp_tarifa_basica"] = {k: v for k, v in onibus.items() if v is not None}
UNID["onibus_sp_tarifa_basica"] = "R$/passagem"
FONTE["onibus_sp_tarifa_basica"] = "Prefeitura de Sao Paulo / SPTrans, planilha tarifaria (ver notas por data em quebras.csv)"
DEFLINHA["onibus_sp_tarifa_basica"] = "tarifa basica do onibus municipal em vigor no mes (degrau); mes da publicacao = mes de vigencia, +-1 mes"
NOTAS["onibus_sp_tarifa_basica"] = "lacuna 1995-07 a 2005-02 exceto os dezembros de 1996 a 2004, DERIVADOS das taxas do ICV-DIEESE (nao observados); 2013: R$ 3,20 publicada e revogada, tarifa mantida R$ 3,00"
ORDEM = list(ITENS) + ["botijao_glp_13kg", "gasolina_comum", "energia_residencial", "onibus_sp_tarifa_basica"]
VINT = {**{p: VINT_DIEESE for p in ITENS}, "botijao_glp_13kg": VINT_ANP, "gasolina_comum": VINT_ANP, "energia_residencial": VINT_EE, "onibus_sp_tarifa_basica": VINT_BUS}

# series anuais auxiliares (EPE/BEN) para cobrir a ANP antes de 2001
AUX = {
    "gasolina_comum_epe_ben_anual": (ben_gas, "R$/litro", "EPE Balanco Energetico Nacional via Ipeadata ANP_PRGASOL (anual, R$/m3 / 1000)", "1973-1993 estimado pela fonte por variacao do preco em dolar; so anual"),
    "botijao_glp_13kg_epe_ben_anual": (ben_glp, "R$/botijao 13 kg", "EPE Balanco Energetico Nacional via Ipeadata ANP_PRGLP (anual, R$/t x 13/1000)", "1973-1993 estimado pela fonte por variacao do preco em dolar; so anual"),
}

ANOMALOS = {("energia_residencial", (2025, 7)), ("energia_residencial", (2025, 10))}
DERIV = {("onibus_sp_tarifa_basica", k) for k in DERIVADOS_DEZ}

# ---------------------------------------------------------------- produtos.csv (formato longo)
with open(SERIES / "produtos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["produto", "fonte", "definicao_linha", "ano", "mes", "valor", "unidade", "nota", "vintage"])
    n = 0
    for p in ORDEM:
        for k in sorted(MENSAIS[p]):
            nt = NOTAS[p] + ("; DERIVADO: nivel de fim de ano reconstruido das taxas do ICV-DIEESE (onibus municipal) ancoradas em R$ 2,00 de mar/2005; nao observado" if (p, k) in DERIV else "") + ("; VALOR ATIPICO: +72% sobre o mes anterior e queda no seguinte; mantido como publicado" if (p, k) in ANOMALOS else "")
            w.writerow([p, FONTE[p], DEFLINHA[p], k[0], k[1], f"{MENSAIS[p][k]:.10g}", UNID[p], nt, VINT[p]])
            n += 1
    for p in ITENS:   # tambem na moeda da epoca, como publicado
        for k in sorted(dados_d[p]):
            if dados_d[p][k] is None:
                continue
            w.writerow([p + "_moeda_da_epoca", FONTE[p], "preco como publicado, na moeda vigente no mes (cruzeiro, cruzado, cruzeiro novo, cruzado novo, cruzeiro real, real); NAO comparavel entre cortes", k[0], k[1], f"{dados_d[p][k]:.10g}", UNID[p] + " (moeda da epoca)", "", VINT_DIEESE])
            n += 1
    for p, (d, un, fonte, nota) in AUX.items():
        for y in sorted(d):
            w.writerow([p, fonte, "preco medio do ano (anual)", y, "", f"{d[y]:.10g}", un, nota, f"Ipeadata ANP_PR*, baixado {HOJE}"])
            n += 1
log(f"produtos.csv: {n} linhas")

# ---------------------------------------------------------------- horas
def media_anual(m, ano):
    vs = [m.get((ano, mm)) for mm in range(1, 13)]
    return sum(vs) / 12 if all(x is not None for x in vs) else None


def horas(preco, salario):
    return preco / (salario / HORAS_MES)


with open(SERIES / "produtos_em_horas.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["produto", "unidade", "granularidade", "ano", "mes", "preco_R$_atuais", "salario_minimo_R$_atuais",
                "horas_salario_minimo", "renda_decil10_mensal_R$_nominais_ppc2017", "horas_decil10_ppc2017",
                "razao_horas_sm_sobre_decil10_ppc2017", "horas_decil10_ppc2021", "nota"])
    for p in ORDEM:
        for k in sorted(MENSAIS[p]):
            if k not in sm:
                continue
            w.writerow([p, UNID[p], "mensal", k[0], k[1], f"{MENSAIS[p][k]:.10g}", f"{sm[k]:.10g}", f"{horas(MENSAIS[p][k], sm[k]):.6g}", "", "", "", "", "salario minimo do mes (Ipeadata MTE12_SALMIN12); ate abr/1984 e o maior regional"])
        for y in range(1948, 2027):
            pm, sa = media_anual(MENSAIS[p], y), media_anual(sm, y)
            if pm is None or sa is None:
                continue
            r17 = renda_decil10_mensal_nominal(y, "2017")
            r21 = renda_decil10_mensal_nominal(y, "2021")
            hs = horas(pm, sa)
            h17 = horas(pm, r17) if r17 else None
            h21 = horas(pm, r21) if r21 else None
            nota = "media dos 12 meses do preco e do salario minimo; renda do decimo mais rico = renda domiciliar per capita media do decil 10 (PIP), convertida US$ PPC/dia -> R$/mes x 365/12 x fator IBGE, e levada a R$ do ano pelo IPCA (media anual)"
            if y <= 1994:
                nota += "; ANO ATE 1994: media de serie mensal com inflacao alta, interpretar com cautela"
            if y in pip["2017"] and pip["2017"][y][1].startswith("PNADC"):
                nota += "; PNAD Continua"
            if p == "energia_residencial" and y == 2025:
                nota += "; a media de 2025 inclui dois meses atipicos (jul e out, +72%), mantidos como publicados"
            w.writerow([p, UNID[p], "anual", y, "", f"{pm:.10g}", f"{sa:.10g}", f"{hs:.6g}",
                        f"{r17:.6g}" if r17 else "", f"{h17:.6g}" if h17 else "", f"{(hs / h17):.6g}" if h17 else "", f"{h21:.6g}" if h21 else "", nota])
    for p, (d, un, fonte, nota0) in AUX.items():
        for y in sorted(d):
            sa = media_anual(sm, y)
            if sa is None:
                continue
            r17 = renda_decil10_mensal_nominal(y, "2017")
            hs = horas(d[y], sa)
            h17 = horas(d[y], r17) if r17 else None
            w.writerow([p, un, "anual", y, "", f"{d[y]:.10g}", f"{sa:.10g}", f"{hs:.6g}", f"{r17:.6g}" if r17 else "", f"{h17:.6g}" if h17 else "",
                        f"{(hs / h17):.6g}" if h17 else "", "", fonte + "; " + nota0])

# ---------------------------------------------------------------- por governo
man = [r for r in _csv.DictReader(open(MANDATOS, encoding="utf-8")) if r["id"] in ("fhc", "lula12", "dilma", "temer", "bolsonaro", "lula3")]


def d_(s):
    return datetime.date.fromisoformat(s)


def mes_anterior(k):
    return (k[0], k[1] - 1) if k[1] > 1 else (k[0] - 1, 12)


def nmeses(a, b):
    return (b[0] - a[0]) * 12 + (b[1] - a[1])


def ult_ate(serie, k, piso=(1900, 1)):
    """ultimo mes <= k com dado."""
    c = [x for x in serie if piso <= x <= k]
    return max(c) if c else None


with open(SERIES / "produtos_por_governo.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["produto", "renda", "governo", "inicio_mandato", "fim_mandato", "ponto_base", "ponto_final", "valor_base", "valor_final",
                "variacao_pct", "variacao_pct_ao_ano", "unidade_do_valor", "nota"])

    def linha(p, renda, m, base, fim, vb, vf, unid, anos, nota=""):
        if vb is None or vf is None or base is None or fim is None or anos <= 0:
            w.writerow([p, renda, m["nome"], m["posse"], m["saida"], base or "", fim or "", "", "", "", "", unid, nota or "sem dado em um dos pontos"])
            return
        var = (vf / vb - 1) * 100
        aa = ((vf / vb) ** (1 / anos) - 1) * 100
        w.writerow([p, renda, m["nome"], m["posse"], m["saida"], base, fim, f"{vb:.6g}", f"{vf:.6g}", f"{var:.4g}", f"{aa:.4g}", unid, nota])

    for m in man:
        posse, saida = d_(m["posse"]), d_(m["saida"])
        prim = (posse.year, posse.month) if posse.day == 1 else ((posse.year, posse.month + 1) if posse.month < 12 else (posse.year + 1, 1))
        base_m = mes_anterior(prim)                       # nivel herdado
        ultimo = d_(m["saida"]) - datetime.timedelta(days=1)
        fim_m = (ultimo.year, ultimo.month)
        # ano de base: ultimo ano civil completo ANTES da posse (posse a meio do ano nao divide o ano)
        ano_base = posse.year - 1
        ano_fim = ultimo.year if (ultimo.month == 12) else ultimo.year - 1
        for p in ORDEM:
            s = MENSAIS[p]
            # ---- nominal e horas ao salario minimo, mensal
            kb = base_m if base_m in s and base_m in sm else None
            kf = ult_ate(s, fim_m, (1994, 7))
            if kf is not None and (kf not in sm or nmeses(kf, fim_m) > 6):
                kf = None             # ponta final a mais de 6 meses do fim do mandato (lacuna ou serie encerrada): sem dado
            nb = f"mes-base ausente na serie" if kb is None else ""
            nf = ""
            if kf is not None and kf != fim_m:
                nf = f"serie termina em {kf[0]}-{kf[1]:02d}, antes do fim do mandato"
            n_m = nmeses(kb, kf) if kb and kf else 0
            if kb and kf:
                linha(p, "nominal_R$_atuais", m, f"{kb[0]}-{kb[1]:02d}", f"{kf[0]}-{kf[1]:02d}", s[kb], s[kf], UNID[p], n_m / 12, nf)
                linha(p, "sm_mensal_horas", m, f"{kb[0]}-{kb[1]:02d}", f"{kf[0]}-{kf[1]:02d}", horas(s[kb], sm[kb]), horas(s[kf], sm[kf]), "horas de trabalho ao salario minimo (220 h/mes)", n_m / 12, nf)
            else:
                linha(p, "nominal_R$_atuais", m, "", "", None, None, UNID[p], 0, "mes-base ou mes-final sem dado (ver lacunas na nota da serie)")
                linha(p, "sm_mensal_horas", m, "", "", None, None, "horas de trabalho ao salario minimo (220 h/mes)", 0, "mes-base ou mes-final sem dado")
            # ---- anual: sm_anual e decil10_anual (mesmos anos)
            anos_disp = [y for y in range(1948, 2027) if media_anual(s, y) is not None and media_anual(sm, y) is not None]
            yb = max([y for y in anos_disp if y <= ano_base], default=None)
            yf = max([y for y in anos_disp if y <= ano_fim], default=None)
            if yb is not None and yb < ano_base - 3:
                yb = None
            # sm_anual
            if yb and yf and yf > yb:
                hb, hf = horas(media_anual(s, yb), media_anual(sm, yb)), horas(media_anual(s, yf), media_anual(sm, yf))
                nt = "" if yb == ano_base and yf == ano_fim else f"ano-base pedido {ano_base}, usado {yb}; ano-final pedido {ano_fim}, usado {yf}"
                if yb <= 1994:
                    nt += "; ano-base com inflacao alta (media anual de serie mensal; interpretar com cautela)"
                linha(p, "sm_anual_horas", m, str(yb), str(yf), hb, hf, "horas de trabalho ao salario minimo (media anual)", yf - yb, nt)
            else:
                linha(p, "sm_anual_horas", m, "", "", None, None, "horas ao salario minimo (media anual)", 0, "ano-base ou ano-final sem dado anual completo")
            # decil10: precisa de renda nos anos
            ys = [y for y in anos_disp if renda_decil10_mensal_nominal(y, "2017")]
            yb2 = max([y for y in ys if y <= ano_base], default=None)
            yf2 = max([y for y in ys if y <= ano_fim], default=None)
            if yb2 is not None and yb2 < ano_base - 3:
                yb2 = None
            if yb2 and yf2 and yf2 > yb2:
                hb = horas(media_anual(s, yb2), renda_decil10_mensal_nominal(yb2, "2017"))
                hf = horas(media_anual(s, yf2), renda_decil10_mensal_nominal(yf2, "2017"))
                nt = "" if yb2 == ano_base and yf2 == ano_fim else f"ano-base pedido {ano_base}, usado {yb2}; ano-final pedido {ano_fim}, usado {yf2} (anos sem pesquisa PNAD: 1991, 1994, 2000, 2010)"
                if yb2 <= 1994:
                    nt += "; ano-base com inflacao alta"
                if yb2 <= 2011 < yf2:
                    nt += "; atravessa a quebra PNAD -> PNAD Continua (2011/2012)"
                linha(p, "decil10_anual_horas_ppc2017", m, str(yb2), str(yf2), hb, hf, "horas de trabalho a renda media do decimo mais rico (PIP, PPC 2017)", yf2 - yb2, nt)
            else:
                linha(p, "decil10_anual_horas_ppc2017", m, "", "", None, None, "horas a renda do decimo mais rico", 0, "ano-base ou ano-final sem dado")

(SERIES / "_conferencias.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
print("\n".join(LOG))
