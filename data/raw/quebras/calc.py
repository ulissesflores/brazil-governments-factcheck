# Quebras de metodo: comparativo a metodo constante + medidas de sobreposicao.
# Le SOMENTE brutos ja baixados (hash em manifest.jsonl de cada pasta). Sem rede.
# Rode: python3 -I calc.py     (a partir de qualquer pasta; grava em ./saida e ./comparativo-metodo-constante.csv)
import csv
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from carga import *  # noqa: E402,F401,F403

SAIDA = H / "saida"
SAIDA.mkdir(exist_ok=True)
M = {}  # medidas, gravadas em saida/medidas.json


def r3(x):
    return None if x is None else round(x, 3)


# ----------------------------------------------------------------------------------------------
# Governos. Convencao: cada ano-calendario pertence a quem governou a maior parte dele.
# ----------------------------------------------------------------------------------------------
GOV = [
    ("Castelo Branco", 1964, 1966), ("Costa e Silva + Medici", 1967, 1973), ("Geisel", 1974, 1978),
    ("Figueiredo", 1979, 1984), ("Sarney", 1985, 1989), ("Collor", 1990, 1992), ("Itamar Franco", 1993, 1994),
    ("FHC", 1995, 2002), ("Lula 1-2", 2003, 2010), ("Dilma", 2011, 2016), ("Temer", 2017, 2018),
    ("Bolsonaro", 2019, 2022), ("Lula 3", 2023, 2025),
]
# Janelas impressas no infografico (infografico-transcrito.csv), por indicador de fluxo.
_IG_BASE = {"Itamar Franco": (1992, 1994), "FHC": (1995, 2002), "Lula 1-2": (2003, 2010), "Dilma": (2011, 2016),
            "Temer": (2016, 2018), "Bolsonaro": (2019, 2022), "Lula 3": (2023, 2025)}
IG = {
    "pib": {**_IG_BASE, "Costa e Silva + Medici": (1968, 1973)},
    "ipca": {**_IG_BASE, "Costa e Silva + Medici": (1967, 1973)},
    "desemprego": {**_IG_BASE, "Costa e Silva + Medici": (1968, 1973), "Bolsonaro": (2019, 2020)},
    "salmin": {**_IG_BASE, "Costa e Silva + Medici": (1968, 1973)},
    "nivel": {},  # pobreza, Gini, expectativa de vida: o infografico usa 1 ano por governo (ver vintage-do-infografico.csv)
}


def janelas(chave):
    out = [("mandato", g, a, b) for g, a, b in GOV]
    for g, (a, b) in IG[chave].items():
        m = [x for x in GOV if x[0] == g][0]
        if (a, b) != (m[1], m[2]):
            out.append(("infografico", g, a, b))
    return out


LINHAS = []  # linhas do comparativo
V_PIP = "PIP API v1, versao corrente em 2026-10-19 (mais recente listada: 20260922); baixado 2026-10-19"
VINT = {
    "P": "Ipeadata SCN10_PIBG10 (atualizada 2026-07-10); baixado 2026-10-19",
    "I": "BCB SGS 433 (IPCA mensal como publicado); baixado 2026-10-19",
    "U1": "Ipeadata PME12_TDA12 (inativa, 2003-02-18); baixado 2026-10-19", "U2": "Ipeadata PAN12_TD12 (inativa, 2016-02-02); baixado 2026-10-19",
    "U3": "Ipeadata Dese_Pnad (atual. 2015-11-17); baixado 2026-10-19", "U4": "Ipeadata Dese_Pnad (atual. 2015-11-17); baixado 2026-10-19",
    "U5": "IBGE SIDRA 4562, serie reponderada (nov/2021) como disponivel em 2026-10-19",
    "S1": "Ipeadata GAC12_SALMINRE12 (atual. 2026-10-09); baixado 2026-10-19", "S2": "Ipeadata GAC12_SALMINRE12 (atual. 2026-10-09); baixado 2026-10-19",
    "S3": "DERIVADO por este script: MTE12_SALMIN12 / IGP12_IGPDI12 (Ipeadata, baixados 2026-10-19)",
    "S4": "DERIVADO por este script: MTE12_SALMIN12 / INPC (SGS 188)", "S5": "DERIVADO por este script: MTE12_SALMIN12 / IPCA (SGS 433)",
    "B-": V_PIP, "Z-IBGE-SIS2020": "IBGE SIS edicao 2020; tabelas baixadas 2026-10-19", "Z-IBGE-SIS2025": "IBGE SIS edicao 2025 (publ. 2025-12-03); baixada 2026-10-19",
    "Z-SIDRA": "IBGE SIDRA 5877; baixada 2026-10-19", "Z-Ipeadata-DISOC": "Ipeadata DISOC_PPY (inativa, 2016-01-06)",
    "Z-Ipeadata-PNADS": "Ipeadata PNADS_PERCPOBRE830 (atual. 2026-05-25); SERIE HARMONIZADA PELO IPEA",
    "G-PIP": V_PIP, "G-IBGE": "IBGE SIS edicao 2025", "G-Ipeadata-PGINI": "Ipeadata PGINI (inativa, 2016-01-07)", "G-Ipeadata-PNADS": "Ipeadata PNADS_GINI (atual. 2026-05-25); SERIE HARMONIZADA PELO IPEA",
    "E-WDI": "Banco Mundial WDI SP.DYN.LE00.IN (UN WPP; lastupdated 2026-10-08)", "E-PUB": "IBGE Tabuas Completas, cada ano na edicao em que foi publicado (baixadas 2026-10-19)",
    "E-REV18": "Ipeadata DEPIS_ESVIDA (rev. 2018; atual. 2023-05-30)", "E-REV13": "IBGE SIDRA 1174 (rev. 2013)",
    "M": "BCB SGS via monetario/saida/anual.csv (bloco monetario), baixado 2026-10-19",
}


def vintage_de(seg):
    ks = [k for k in VINT if seg.startswith(k)]
    return VINT[max(ks, key=len)] if ks else ""



def compacto(anos):
    anos = sorted(anos)
    if not anos:
        return ""
    partes, ini, ant = [], anos[0], anos[0]
    for a in anos[1:]:
        if a == ant + 1:
            ant = a
            continue
        partes.append(f"{ini}" if ini == ant else f"{ini}-{ant}")
        ini = ant = a
    partes.append(f"{ini}" if ini == ant else f"{ini}-{ant}")
    return ",".join(partes)


def emite(indicador, segmento, metodo, y0, y1, serie, tipo, chave, min_anos_parcial=2, rotulo_anos=None, destino=None, vint=None):
    """serie: {ano: valor}. tipo 'taxa' (composicao) ou 'nivel' (ultimo menos primeiro)."""
    anos_seg = f"{y0}-{y1}" if rotulo_anos is None else rotulo_anos
    for kind, g, a, b in janelas(chave):
        dentro = (y0 <= a and b <= y1)
        yrs = [y for y in range(a, b + 1) if y0 <= y <= y1 and y in serie]
        if dentro and not yrs:
            continue
        if not dentro and len(yrs) < min_anos_parcial:
            continue
        vals = [serie[y] for y in yrs]
        media = sum(vals) / len(vals)
        if tipo == "taxa":
            p = 1.0
            for v in vals:
                p *= 1 + v / 100
            var = (p - 1) * 100
        else:
            var = (vals[-1] - vals[0]) if len(vals) >= 2 else None
        total = b - a + 1
        if dentro and len(yrs) == total:
            cob = "inteiro"
        elif dentro:
            cob = f"inteiro no segmento, com lacunas de dados (faltam {compacto(set(range(a, b + 1)) - set(yrs))})"
        else:
            cob = f"PARCIAL: {len(yrs)} de {total} anos do governo ({compacto(yrs)})"
        (LINHAS if destino is None else destino).append({
            "indicador": indicador, "segmento": segmento, "metodo": metodo, "anos": anos_seg, "governo": g,
            "janela_usada": f"{kind} {a}-{b}; {cob}", "valor_medio": r3(media),
            "variacao_no_segmento": r3(var), "n_anos": len(yrs), "vintage": vint if vint else vintage_de(segmento),
        })


# ----------------------------------------------------------------------------------------------
# 1. PIB real (variacao % a.a.)
# ----------------------------------------------------------------------------------------------
g = ipea_a("SCN10_PIBG10")
IND = "PIB real (var. % a.a.; variacao_no_segmento = crescimento acumulado %)"
for seg, met, a, b in [
    ("P1", "Sistema de Contas Nacionais Consolidadas (FGV), 1948-1990", 1948, 1990),
    ("P2", "SCN IBGE referencia 1985 (SNA 1993), 1991-1995", 1991, 1995),
    ("P3", "Contas Trimestrais referencia 2010 (retropoladas), 1996-2000", 1996, 2000),
    ("P4", "SCN IBGE referencia 2010 (SNA 2008), 2001-2025 (2023-2025 preliminar/estimado)", 2001, 2025),
    ("P5", "referencia 2010 continua: P3 + P4 (1996-2025)", 1996, 2025),
]:
    emite(IND, seg, met, a, b, g, "taxa", "pib")

# ----------------------------------------------------------------------------------------------
# 2. IPCA (variacao % acumulada no ano; BCB SGS 433)
# ----------------------------------------------------------------------------------------------
ipca_m = sgs(str(ER / "bcb-sgs433-raw.json"))
ipca_a = acum_anual(ipca_m)
IND = "IPCA (inflacao acumulada no ano, %; variacao_no_segmento = acumulada %)"
for seg, met, a, b in [
    ("I1", "SNIPC original: pesos Endef 1974-75; coleta do dia 15 ao 14; sem Goiania (anos completos 1981-1985)", 1981, 1985),
    ("I1b", "base mar/1986=100; coleta em mes civil; pesos Endef (mar/1986-mai/1989; anos completos 1987-1988)", 1987, 1988),
    ("I2", "POF 1987-88 desde jun/1989; media aritmetica no subitem; Goiania desde jan/1991 (anos 1990-1993)", 1990, 1993),
    ("I3", "media geometrica no subitem desde jan/1994; estruturas originais da POF 1987-88 (anos 1994-1998)", 1994, 1998),
    ("I4", "POF 1995-96 desde ago/1999 (anos 2000-2005)", 2000, 2005),
    ("I5", "POF 2002-03 desde jul/2006; itens sazonais por Laspeyres (anos 2007-2011)", 2007, 2011),
    ("I6", "POF 2008-09 desde jan/2012; 11 areas, 13 em jan/2014, 16 em mai/2018 (anos 2012-2019)", 2012, 2019),
    ("I7", "POF 2017-18 desde jan/2020 (anos 2020-2025)", 2020, 2025),
]:
    emite(IND, seg, met, a, b, ipca_a, "taxa", "ipca")

# ----------------------------------------------------------------------------------------------
# 3. Desemprego (% da forca de trabalho)
# ----------------------------------------------------------------------------------------------
ant = ipea("PME12_TDA12")
nov = ipea("PAN12_TD12")
ant_a = media_anual(ant)                       # 1980-2002
nov_a = media_anual(nov)                       # 2003-2015 (2002 tem 10 meses: fora)
pnad = {int(x["VALDATA"][:4]): float(x["VALVALOR"]) for x in json.load(open(ER / "ipeadata-Dese_Pnad-raw.json"))["value"]
        if x["NIVNOME"] == "Brasil" and x["VALVALOR"] is not None}
pnadc = {int(k): v for k, v in sidra_serie(ER / "sidra-pnadc-anual-t4562-raw.json", 4099).items()}
IND = "Desemprego (% da forca de trabalho; variacao_no_segmento = pp)"
emite(IND, "U1", "PME antiga: 6 RMs; 15+ anos; ref. 30 dias; 1980-2002", 1980, 2002, ant_a, "nivel", "desemprego")
emite(IND, "U2", "PME nova: 6 RMs; 10+ anos; semana de referencia (anos completos 2003-2015)", 2003, 2015, nov_a, "nivel", "desemprego")
emite(IND, "U3", "PNAD anual: Brasil sem area rural do Norte (exc. TO); 10+ anos; setembro (1992-2003; sem 1994 e 2000)", 1992, 2003, pnad, "nivel", "desemprego")
emite(IND, "U4", "PNAD anual: Brasil com area rural do Norte; 10+ anos; setembro (2004-2014; sem 2010)", 2004, 2014, pnad, "nivel", "desemprego")
emite(IND, "U5", "PNAD Continua: Brasil; 14+ anos; media dos 4 trimestres (2012-2025)", 2012, 2025, pnadc, "nivel", "desemprego")

# ----------------------------------------------------------------------------------------------
# 4. Salario minimo real
# ----------------------------------------------------------------------------------------------
real = ipea("GAC12_SALMINRE12")
nom = ipea("MTE12_SALMIN12")
igp = ipea("IGP12_IGPDI12")
inpc_v = sgs(str(ER / "bcb-sgs188-raw.json"))
ipca_v = sgs(str(ER / "bcb-sgs433-raw.json"))


def indice_acum(var_pct, ini):
    """Indice encadeado (base 1 no mes anterior a 'ini') a partir de variacoes mensais."""
    meses = sorted(k for k in var_pct if k >= ini)
    idx, v = {}, 1.0
    for k in meses:
        v *= 1 + var_pct[k] / 100
        idx[k] = v
    return idx


def taxas_de_nivel(niveis_anuais, y0, y1):
    """Taxa anual so entre anos consecutivos DENTRO de [y0, y1] (nao atravessa a quebra)."""
    return {y: (niveis_anuais[y] / niveis_anuais[y - 1] - 1) * 100 for y in range(y0 + 1, y1 + 1)
            if y in niveis_anuais and y - 1 in niveis_anuais and y - 1 >= y0}


real_a = media_anual(real)
IND = "Salario minimo real (var. % a.a. da media anual; variacao_no_segmento = acumulada %)"
emite(IND, "S1", "serie Ipea oficial, deflator IGPC-Mtb (jan/1948-mar/1979); maior minimo regional", 1948, 1978,
      taxas_de_nivel(real_a, 1948, 1978), "taxa", "salmin")
emite(IND, "S2", "serie Ipea oficial, deflator INPC (abr/1979 em diante; 1,2225 em jul/1994; minimo nacional desde mai/1984)", 1980, 2025,
      taxas_de_nivel(real_a, 1980, 2025), "taxa", "salmin")
# Deflator unico (metodo que nao muda): nominal / indice.
igp_real = {k: nom[k] / igp[k] for k in nom if k in igp}
emite(IND, "S3", "nominal / IGP-DI (FGV) em todos os anos, sem trocar de deflator (1944-2025)", 1944, 2025,
      taxas_de_nivel(media_anual(igp_real), 1944, 2025), "taxa", "salmin")
inpc_idx = indice_acum(inpc_v, (1979, 4))
inpc_real = {k: nom[k] / inpc_idx[k] for k in inpc_idx if k in nom}
emite(IND, "S4", "nominal / INPC (IBGE) em todos os anos, sem trocar de deflator (1980-2025)", 1980, 2025,
      taxas_de_nivel(media_anual(inpc_real), 1980, 2025), "taxa", "salmin")
ipca_idx = indice_acum(ipca_v, (1980, 1))
ipca_real = {k: nom[k] / ipca_idx[k] for k in ipca_idx if k in nom}
emite(IND, "S5", "nominal / IPCA (IBGE) em todos os anos, sem trocar de deflator (1981-2025)", 1981, 2025,
      taxas_de_nivel(media_anual(ipca_real), 1981, 2025), "taxa", "salmin")

# medida: acumulado por governo sob cada deflator (media anual a media anual; ano anterior ao inicio como base)


def acum_gov(niveis_anuais, a, b):
    if a - 1 in niveis_anuais and b in niveis_anuais:
        return (niveis_anuais[b] / niveis_anuais[a - 1] - 1) * 100
    return None


sm = {"Ipea composto": real_a, "IGP-DI": media_anual(igp_real), "INPC": media_anual(inpc_real), "IPCA": media_anual(ipca_real)}
M["salmin_por_governo"] = {}
for kind, gname, a, b in janelas("salmin"):
    M["salmin_por_governo"][f"{gname}|{kind}|{a}-{b}"] = {k: r3(acum_gov(v, a, b)) for k, v in sm.items()}

# ----------------------------------------------------------------------------------------------
# 5. Pobreza (% da populacao)
# ----------------------------------------------------------------------------------------------
PS = SO / "series" / "pobreza.csv"
IND = "Pobreza (% da populacao; variacao_no_segmento = pp)"
pipd = {}
for ppp, linhas in ((2017, ("2.15", "3.65", "6.85")), (2021, ("3.00", "4.20", "8.30"))):
    for l in linhas:
        pipd[(ppp, l)] = {a: r["headcount"] * 100 for a, r in pip(SO / "bruto" / f"pip_ppp{ppp}_line{l}.json").items()}
M["pip_headcount"] = {f"{k[0]}|{k[1]}": {str(a): r3(v) for a, v in d.items()} for k, d in pipd.items()}
for (ppp, l), d in pipd.items():
    nome = f"Banco Mundial PIP, US$ {l}/dia, PPC {ppp}"
    emite(IND, f"B-{ppp}-{l}-a", f"{nome}; PNAD (spell 1981-2011 segundo o PIP)", 1981, 2011, d, "nivel", "nivel")
    emite(IND, f"B-{ppp}-{l}-b", f"{nome}; PNADC (spell 2012-2024 segundo o PIP)", 2012, 2024, d, "nivel", "nivel")
    emite(IND, f"B-{ppp}-{l}-c", f"{nome}; serie unica 1981-2024 que ATRAVESSA a quebra PNAD->PNADC de 2012 (marcada pelo proprio PIP)", 1981, 2024, d, "nivel", "nivel")
for fonte, linha, nome, y0, y1 in [
    ("IBGE-SIS2020-PPC2011", "US$ 5,5 PPC2011", "IBGE SIS ed. 2020, US$ 5,50 PPC 2011 (PNADC)", 2012, 2019),
    ("IBGE-SIS2025", "US$ 6,85 PPC2017", "IBGE SIS ed. 2025, US$ 6,85 PPC 2017 (PNADC)", 2012, 2024),
    ("IBGE-SIS2025", "US$ 3,65 PPC2017", "IBGE SIS ed. 2025, US$ 3,65 PPC 2017 (PNADC)", 2012, 2024),
    ("IBGE-SIS2025", "US$ 2,15 PPC2017", "IBGE SIS ed. 2025, US$ 2,15 PPC 2017 (PNADC)", 2012, 2024),
    ("SIDRA-5877", "linha nacional ODS US$ 8,30 PPC2021", "IBGE SIDRA 5877, linha nacional ODS US$ 8,30 PPC 2021 (PNADC)", 2012, 2024),
    ("Ipeadata-DISOC_PPY", "linha propria Ipea = 2x indigencia (cesta FAO), 24 regioes; serie INTERROMPIDA", "Ipea DISOC_PPY, linha propria (PNAD, sem anos de Censo)", 1976, 2014),
    ("Ipeadata-PNADS_PERCPOBRE830", "PPC$8,30 (2021)", "Ipea PNADS harmonizada, US$ 8,30 PPC 2021 (PNAD<=2011 multiplicada por fator que iguala 2012)", 1995, 2025),
]:
    d = serie_csv(PS, fonte, linha)
    emite(IND, f"Z-{fonte}-{linha[:12]}", nome, y0, y1, d, "nivel", "nivel")

# ----------------------------------------------------------------------------------------------
# 6. Gini (0 a 1)
# ----------------------------------------------------------------------------------------------
GS = SO / "series" / "gini.csv"
IND = "Gini da renda domiciliar per capita (0-1; variacao_no_segmento = pontos de Gini)"
pip_gini = {a: r["gini"] for a, r in pip(SO / "bruto" / "pip_ppp2017_line6.85.json").items()}
emite(IND, "G-PIP-a", "Banco Mundial PIP; PNAD (spell 1981-2011)", 1981, 2011, pip_gini, "nivel", "nivel")
emite(IND, "G-PIP-b", "Banco Mundial PIP; PNADC (spell 2012-2024)", 2012, 2024, pip_gini, "nivel", "nivel")
emite(IND, "G-PIP-c", "Banco Mundial PIP; serie unica 1981-2024 que ATRAVESSA a quebra PNAD->PNADC de 2012", 1981, 2024, pip_gini, "nivel", "nivel")
for fonte, linha, nome, y0, y1 in [
    ("IBGE-SIS2025", "renda dom. per capita (PNADC)", "IBGE SIS ed. 2025 (PNADC; 2020-2022 em quintas visitas)", 2012, 2024),
    ("Ipeadata-PGINI", "renda dom. per capita (PNAD antiga, serie interrompida)", "Ipea PGINI (PNAD antiga; sem anos de Censo e 1994)", 1976, 2011),
    ("Ipeadata-PNADS_GINI", "harmonizada: PNAD<=2011 multiplicada por fator que iguala 2012", "Ipea PNADS_GINI harmonizada (PNAD<=2011 x fator; PNADC desde 2012)", 1995, 2025),
]:
    d = serie_csv(GS, fonte, linha)
    emite(IND, f"G-{fonte}", nome, y0, y1, d, "nivel", "nivel")

# ----------------------------------------------------------------------------------------------
# 7. Expectativa de vida ao nascer (anos)
# ----------------------------------------------------------------------------------------------
ES = SO / "series" / "expvida.csv"
IND = "Expectativa de vida ao nascer (anos; variacao_no_segmento = anos)"
wdi_e0 = wdi(SO / "bruto" / "wb_SP.DYN.LE00.IN.json")
emite(IND, "E-WDI", "ONU/WPP via Banco Mundial WDI (UMA vintage, 1960-2024, atualizada 2026-10-08)", 1960, 2024, wdi_e0, "nivel", "nivel")
pub = {}
for x in csv.DictReader(open(ES)):
    if x["fonte"] == "IBGE-Tabua-como-publicada":
        pub[int(x["ano"])] = float(x["valor"])
emite(IND, "E-PUB", "IBGE Tabua Completa de cada ano COMO PUBLICADA (um vintage por ano; so os anos baixados)", 2000, 2024, pub, "nivel", "nivel")
dep = serie_csv(ES, "Ipeadata-DEPIS_ESVIDA", "IBGE Projecao (rev. 2018)")
emite(IND, "E-REV18", "IBGE Projecao Revisao 2018 (Ipeadata DEPIS_ESVIDA, 2000-2022)", 2000, 2022, dep, "nivel", "nivel")
s1174 = serie_csv(ES, "SIDRA-1174", "IBGE Projecao (rev. 2013), serie IDS ate 2014")
emite(IND, "E-REV13", "IBGE Projecao Revisao 2013 (SIDRA 1174, 2000-2014)", 2000, 2014, s1174, "nivel", "nivel")
vig = serie_csv(ES, "IBGE-Tabuas2024-serie-vigente", "Agencia IBGE 28/11/2025 (reconstrucao 1940-2024)")
M["e0_vigente"] = {str(a): v for a, v in vig.items()}
M["e0_publicada"] = {str(a): v for a, v in pub.items()}
M["e0_rev18"] = {str(a): v for a, v in dep.items()}
M["e0_rev13"] = {str(a): v for a, v in s1174.items()}
M["e0_wdi"] = {str(a): v for a, v in wdi_e0.items()}
rev08 = {}
for x in csv.DictReader(open(ES)):
    if x["fonte"] == "IBGE-Projecao-rev2008":
        rev08[int(x["ano"])] = float(x["valor"])
M["e0_rev08"] = {str(a): v for a, v in rev08.items()}

# ----------------------------------------------------------------------------------------------
# 8. Agregados monetarios (% do PIB; media de 12 saldos mensais / PIB do ano) - reuso de monetario/saida/anual.csv
# ----------------------------------------------------------------------------------------------
rows = list(csv.DictReader(open(MO / "saida" / "anual.csv")))


def col(c):
    return {int(r["ano"]): float(r[c]) for r in rows if r[c] not in ("", None)}


IND = "Agregado monetario (% do PIB; variacao_no_segmento = pp)"
m0 = col("M0_med12_pib_pct")
emite(IND + " M0", "M0-a", "Base monetaria restrita, conceito anterior a 1980 (nao retropolado pelo BCB)", 1947, 1979, m0, "nivel", "nivel")
emite(IND + " M0", "M0-b", "Base monetaria restrita, conceito de 1980 em diante", 1980, 2025, m0, "nivel", "nivel")
emite(IND + " M1", "M1-a", "M1 conceito antigo (SGS 1827), 1947-2017", 1947, 2017, col("M1_med12_pib_pct"), "nivel", "nivel")
emite(IND + " M1", "M1-b", "M1 'Novo' (SGS 27791), 2002-2025", 2002, 2025, col("M1_novo_med12_pib_pct"), "nivel", "nivel")
for k in ("M2", "M3", "M4"):
    emite(IND + f" {k}", f"{k}-a", f"{k} metodologia de 2001 (series refeitas desde jul/1988, ate jun/2018), 1989-2017", 1989, 2017, col(f"{k}_2001_med12_pib_pct"), "nivel", "nivel")
    emite(IND + f" {k}", f"{k}-b", f"{k} 'Novo' (NT 48 de 2018; cooperativas, letras; sem nao residentes), 2002-2025", 2002, 2025, col(f"{k}_novo_med12_pib_pct"), "nivel", "nivel")

# ----------------------------------------------------------------------------------------------
# Escreve o comparativo
# ----------------------------------------------------------------------------------------------
CAB = ["indicador", "segmento", "metodo", "anos", "governo", "janela_usada", "valor_medio", "variacao_no_segmento", "n_anos", "vintage"]
with open(H / "comparativo-metodo-constante.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=CAB)
    w.writeheader()
    for l in LINHAS:
        w.writerow({k: ("" if l[k] is None else l[k]) for k in CAB})
print("comparativo:", len(LINHAS), "linhas")


# ----------------------------------------------------------------------------------------------
# 9. Indicadores ALTERNATIVOS que nao dependem da regra/definicao que mudou (series baixadas em quebras/bruto)
# ----------------------------------------------------------------------------------------------
ALT = []
QB = H / "bruto"


def ip_q(code, nivel=("", "Brasil")):
    return {(int(x["VALDATA"][:4]), int(x["VALDATA"][5:7])): float(x["VALVALOR"]) for x in json.load(open(QB / f"ipeadata-{code}-raw.json"))["value"]
            if x["VALVALOR"] is not None and x["NIVNOME"] in nivel}


def taxas(niv):
    return {y: (niv[y] / niv[y - 1] - 1) * 100 for y in niv if y - 1 in niv}


V_ALT = "Ipeadata {c}, baixado 2026-10-19"
eletro = {k[0]: v for k, v in ip_q("ELETRO_CEET").items()}
emite("ALT PIB: consumo de energia eletrica (Eletrobras, var. % a.a.; acumulado %)", "A-ELETRO", "consumo fisico de energia (quantidade), sem ano-base nem SCN", 1952, 2025, taxas(eletro), "taxa", "pib", destino=ALT, vint=V_ALT.format(c="ELETRO_CEET"))
mme = {k[0]: v for k, v in ip_q("CONSUMOTOT").items()}
emite("ALT PIB: consumo final de energia eletrica (MME/BEN, var. % a.a.; acumulado %)", "A-MME", "consumo fisico (BEN/MME), 1961-2022", 1961, 2022, taxas(mme), "taxa", "pib", destino=ALT, vint=V_ALT.format(c="CONSUMOTOT"))
ibcbr = media_anual(ip_q("SGS12_IBCBR12"))
emite("ALT PIB: IBC-Br (BCB, var. % a.a. da media anual; acumulado %)", "A-IBCBR", "proxy mensal do BCB, 2003-2025 (nao depende do ano-base do SCN; tem metodo proprio)", 2004, 2025, taxas(ibcbr), "taxa", "pib", destino=ALT, vint=V_ALT.format(c="SGS12_IBCBR12"))
fipe = {k[0]: v for k, v in ip_q("FIPE_FIPE0001").items()}
emite("ALT inflacao: IPC-Fipe, Sao Paulo (% a.a.; acumulado %)", "A-FIPE", "IPC da Fipe (USP), cesta e pesos proprios, 1940-2025", 1940, 2025, fipe, "taxa", "ipca", destino=ALT, vint=V_ALT.format(c="FIPE_FIPE0001"))
cest = ip_q("DIEESE12_CBSP12")
cortes_cesta = [((1967, 1), 1000), ((1986, 3), 1000), ((1989, 1), 1000), ((1993, 8), 1000), ((1994, 7), 2750)]  # a serie DIEESE troca de unidade em jan/1967 (BCB: 13/02/1967)


def divisor(k):
    d = 1
    for ini, f in cortes_cesta:
        if ini > k:
            d *= f
    return d


# cesta convertida para reais atuais (divide pelo mesmo divisor acumulado que o Ipeadata aplicou ao SM) e comparada ao SM em R$
sm_cestas = {k: nom[k] / (cest[k] / divisor(k)) for k in cest if k in nom}
emite("ALT salario minimo: numero de cestas basicas DIEESE-SP que 1 SM compra (cestas; variacao_no_segmento = cestas)", "A-CESTA", "SM nominal / custo da cesta basica DIEESE (Sao Paulo), 1959-2025; sem deflator de precos gerais",
      1959, 2025, media_anual(sm_cestas), "nivel", "salmin", destino=ALT, vint="DERIVADO: MTE12_SALMIN12 x divisores de moeda (BCB, Museu de Valores) / DIEESE12_CBSP12 (Ipeadata); baixados 2026-10-19")
# renda domiciliar per capita SIS (Brasil): real a precos de 2024 pelo IPCA medio anual
def sis_real(code):
    d = {k[0]: v for k, v in ip_q(code).items()}
    return {y: v * media_ano_ipca[2024] / media_ano_ipca[y] for y, v in d.items()}


media_ano_ipca = {}
_idx = indice_acum(ipca_v, (1980, 1))
for y in range(1980, 2027):
    ms = [k for k in _idx if k[0] == y]
    if len(ms) == 12:
        media_ano_ipca[y] = sum(_idx[k] for k in ms) / 12
for code, nm in (("SIS_RDPCMEDIANO", "renda domiciliar per capita MEDIANA"), ("SIS_RDPCMEDIO", "renda domiciliar per capita MEDIA"), ("SIS_RDPC40", "renda domiciliar per capita dos 40% mais pobres")):
    emite(f"ALT pobreza/desigualdade: {nm} (R$ de 2024 pelo IPCA; variacao = R$)", f"A-{code}", "SIS/IBGE (PNADC) sem linha de pobreza; 2020-2022 em quintas visitas", 2012, 2024, sis_real(code), "nivel", "nivel", destino=ALT,
          vint=V_ALT.format(c=code) + "; deflacionado aqui pelo IPCA (SGS 433)")
razao = {k[0]: v for k, v in ip_q("PPA_L0_03RZ10R40P").items()}
emite("ALT desigualdade: razao entre a renda dos 10% mais ricos e dos 40% mais pobres (Ipea PPA; variacao = pontos da razao)", "A-PPA", "razao de rendas, sem Gini nem linha", 2016, 2024, razao, "nivel", "nivel", destino=ALT, vint=V_ALT.format(c="PPA_L0_03RZ10R40P"))
_pd = pip(SO / "bruto" / "pip_ppp2017_line6.85.json")
palma = {a: r["decile10"] / sum(r[f"decile{i}"] for i in range(1, 5)) for a, r in _pd.items()}
top10 = {a: r["decile10"] * 100 for a, r in _pd.items()}
for nome, d in (("Palma (renda do 10o decil / renda dos 4 decis mais pobres)", palma), ("participacao do 10o decil na renda (%)", top10)):
    emite(f"ALT desigualdade: {nome} (PIP; variacao = pontos)", "A-PIP-a", "razao de decis, PNAD (spell 1981-2011 do PIP); sem a formula do Gini", 1981, 2011, d, "nivel", "nivel", destino=ALT, vint=V_PIP)
    emite(f"ALT desigualdade: {nome} (PIP; variacao = pontos)", "A-PIP-b", "razao de decis, PNADC (spell 2012-2024 do PIP)", 2012, 2024, d, "nivel", "nivel", destino=ALT, vint=V_PIP)
with open(H / "alternativos-por-governo.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=CAB)
    w.writeheader()
    w.writerows([{k: ("" if l[k] is None else l[k]) for k in CAB} for l in ALT])
print("alternativos:", len(ALT), "linhas")

# guarda series anuais usadas (para mistura/vintage)
M["series_anuais"] = {
    "pib": {str(k): v for k, v in g.items() if k >= 1948},
    "ipca": {str(k): r3(v) for k, v in ipca_a.items()},
    "desemprego_pme_antiga": {str(k): r3(v) for k, v in ant_a.items()},
    "desemprego_pme_nova": {str(k): r3(v) for k, v in nov_a.items()},
    "desemprego_pnad": {str(k): r3(v) for k, v in pnad.items()},
    "desemprego_pnadc": {str(k): v for k, v in pnadc.items()},
}
exec(open(H / "medidas.py", encoding="utf-8").read())  # noqa: S102 - nosso proprio codigo; preenche M
json.dump(M, open(SAIDA / "medidas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
print("medidas:", len(M), "chaves")
