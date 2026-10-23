#!/usr/bin/env python3
"""Constroi series/ e derivado/ a partir de bruto/ (nada digitado a mao).
Uso: python3 -I construir_series.py   (pasta da fase fixa abaixo)
"""
import csv, gzip, json, re, html, os
from collections import defaultdict

P = "/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/populacao-fase2/"
BR, SE, DE = P + "bruto/", P + "series/", P + "derivado/"
HDR = ["indicador", "fonte", "definicao_linha", "ano", "mes_ou_trimestre", "valor", "unidade", "nota", "vintage"]
ACQ = "baixado 2026-10-21"
MES = {"Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4, "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
       "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12, "Ignorado": "ignorado"}


def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HDR)
        w.writerows(rows)
    print(path.split("populacao-fase2/")[1], len(rows))


# ---------- DATASUS TabNet ----------
def tabnet(fn):
    h = open(BR + fn, encoding="latin-1").read()
    cells = []
    for m in re.finditer(r"<TD[^>]*>\s*(\d{4})\s*<TD[^>]*>\s*([\d.]+)\s*<TD[^>]*>\s*([\d.]+)", h, re.I):
        cells.append((int(m.group(1)), int(m.group(2).replace(".", "")), int(m.group(3).replace(".", ""))))
    return cells


def vintage_datasus(ano, final_ate=2024):
    if ano <= final_ate:
        return f"DATASUS dados finais (extracao 02/12/2025); {ACQ}"
    if ano == 2025:
        return f"DATASUS 2025 preliminar (extracao 28/07/2026); {ACQ}"
    return f"DATASUS 2026 2a previa (extracao 01/09/2026); {ACQ}"


sim = []
for fn, defn, cid in (("tabnet_sim_obt09uf_ano.html", "obt09uf, CID-9, 1979-1995", "CID-9"),
                      ("tabnet_sim_obt10uf_ano.html", "obt10uf, CID-10, 1996-2026", "CID-10")):
    for ano, oc, rs in tabnet(fn):
        nota_base = f"todas as causas, Brasil; classificacao {cid}"
        if ano == 2025:
            nota_base += "; ano PRELIMINAR"
        if ano == 2026:
            nota_base += "; ano INCOMPLETO (2a previa, nao e total anual)"
        v = vintage_datasus(ano) if cid == "CID-10" else f"DATASUS TabNet obt09uf (base 1979-1995, sem carimbo de extracao na pagina); {ACQ}"
        sim.append(("obitos_total_por_ocorrencia", "DATASUS SIM (TabNet)", defn + ", Obitos p/Ocorrenc", ano, "", oc, "pessoas", nota_base, v))
        sim.append(("obitos_total_por_residencia", "DATASUS SIM (TabNet)", defn + ", Obitos p/Residenc", ano, "", rs, "pessoas", nota_base, v))
write(SE + "datasus_sim_obitos.csv", sim)

sn = []
for ano, oc, rs in tabnet("tabnet_sinasc_nvuf_ano.html"):
    nota = "Brasil; SINASC implantado em todas as UF desde 1994 mas em algumas a coleta nao cobria todos os municipios (nota tecnica DATASUS)" if ano <= 1999 else "Brasil"
    if ano == 2025:
        nota += "; ano PRELIMINAR"
    if ano == 2026:
        nota += "; ano INCOMPLETO (2a previa, nao e total anual)"
    v = vintage_datasus(ano)
    sn.append(("nascidos_vivos_por_ocorrencia", "DATASUS SINASC (TabNet)", "nvuf, Nascim p/ocorrenc, ano do nascimento", ano, "", oc, "pessoas", nota, v))
    sn.append(("nascidos_vivos_por_residencia_mae", "DATASUS SINASC (TabNet)", "nvuf, Nascim p/resid.mae, ano do nascimento", ano, "", rs, "pessoas", nota, v))
write(SE + "datasus_sinasc_nascidos.csv", sn)


# ---------- IBGE SIDRA ----------
def sidra(fn):
    d = json.load(open(BR + fn))
    return d[1:]


def sidra_ano(fn, ind, defn, tab, nota, dimkey="D3N"):
    out = []
    for r in sidra(fn):
        if r["V"] in ("...", "-", "X"):
            continue
        out.append((ind, f"IBGE Estatisticas do Registro Civil (SIDRA tab. {tab})", defn, int(r[dimkey]), "", int(r["V"]), "pessoas",
                    nota, f"SIDRA API; {ACQ}; ultimo ano da tabela 2024"))
    return out


ib = []
ib += sidra_ano("sidra_192_registrados_ano.json", "nascidos_vivos_registrados_no_ano", "nascidos vivos registrados no ano (periodo = ano do registro), todos os anos de nascimento", 192,
                "Brasil; serie 1984-2002; total de registros do ano, inclui nascimentos de anos anteriores (registro tardio)")
ib += sidra_ano("sidra_2609_registrados_ano.json", "nascidos_vivos_registrados_no_ano", "nascidos vivos registrados no ano (periodo = ano do registro), todos os anos de nascimento, por residencia da mae", 2609,
                "Brasil; exclui maes residentes no exterior/ignorado; tab. 2679 (lugar do registro) e a contagem completa")
ib += sidra_ano("sidra_2679_registrados_ano.json", "nascidos_vivos_registrados_no_ano_lugar_registro", "nascidos vivos registrados no ano (periodo = ano do registro), por lugar do registro", 2679,
                "Brasil; contagem por lugar do registro (inclui maes residentes no exterior)")
ib += sidra_ano("sidra_706_ocorridos_ano.json", "nascidos_vivos_ocorridos_no_ano", "nascidos vivos ocorridos no ano (ano de nascimento = ano da pesquisa), registrados ate o fechamento da coleta", 706,
                "Brasil; serie 1984-2002; sub-registro nao corrigido")
ib += sidra_ano("sidra_2612_ocorridos_ano.json", "nascidos_vivos_ocorridos_no_ano", "nascidos vivos ocorridos no ano, por residencia da mae (total)", 2612,
                "Brasil; sub-registro nao corrigido")
ib += sidra_ano("sidra_363_obitos_registrados_ano.json", "obitos_registrados_no_ano", "obitos registrados no ano (periodo = ano do registro), total de anos de ocorrencia", 363,
                "Brasil; serie 1984-2002; inclui registro tardio de obitos de anos anteriores")
ib += sidra_ano("sidra_2682_obitos_registrados_ano.json", "obitos_registrados_no_ano", "obitos registrados no ano (periodo = ano do registro), por residencia do falecido", 2682,
                "Brasil; exclui residentes no exterior/ignorado")
ib += sidra_ano("sidra_2684_obitos_registrados_ano.json", "obitos_registrados_no_ano_lugar_registro", "obitos registrados no ano (periodo = ano do registro), por lugar do registro", 2684,
                "Brasil; contagem por lugar do registro")
ib += sidra_ano("sidra_367_obitos_ocorridos_registrados_ano.json", "obitos_ocorridos_e_registrados_no_ano", "obitos ocorridos E registrados no mesmo ano (def. restrita, 1984-2002)", 367,
                "Brasil; definicao diferente de 'ocorridos no ano' de 2003+ (ver quebras.csv)")
ib += sidra_ano("sidra_2654_obitos_ocorridos_ano.json", "obitos_ocorridos_no_ano", "obitos ocorridos no ano, por residencia do falecido (total)", 2654,
                "Brasil; sub-registro nao corrigido")

# mensal
for fn, ind, defn, tab, col in (("sidra_2612_nascidos_mes.json", "nascidos_vivos_ocorridos_no_ano_mensal", "nascidos vivos ocorridos no ano, por mes do nascimento", 2612, "D4N"),
                                ("sidra_2654_obitos_mes.json", "obitos_ocorridos_no_ano_mensal", "obitos ocorridos no ano, por mes de ocorrencia", 2654, "D4N")):
    for r in sidra(fn):
        if r[col] == "Total" or r["V"] in ("...", "-", "X"):
            continue
        ib.append((ind, f"IBGE Estatisticas do Registro Civil (SIDRA tab. {tab})", defn, int(r["D3N"]), MES[r[col]], int(r["V"]), "pessoas",
                   "Brasil; mes 'ignorado' = sem mes declarado", f"SIDRA API; {ACQ}"))
write(SE + "ibge_registro_civil.csv", ib)

# derivado: por ano de nascimento / ocorrencia (soma dos registros 2003-2024; matriz)
dv = []
for fn, ind, defn, tab, ycol in (("sidra_2609_matriz_ano_registro_x_ano_nascimento.json", "nascidos_vivos_por_ano_de_nascimento_registrados_2003_2024",
                                  "soma dos registros feitos 2003-2024 de nascidos no ano Y (matriz ano de registro x ano de nascimento)", 2609, "D4N"),
                                 ("sidra_2682_matriz_ano_registro_x_ano_ocorrencia.json", "obitos_por_ano_de_ocorrencia_registrados_2003_2024",
                                  "soma dos registros feitos 2003-2024 de obitos ocorridos no ano Y (matriz ano de registro x ano de ocorrencia)", 2682, "D4N")):
    acc = defaultdict(int)
    for r in sidra(fn):
        y = r[ycol]
        if re.fullmatch(r"\d{4}", y) and r["V"] not in ("...", "-", "X") and 2003 <= int(r["D3N"]) <= 2024:
            acc[int(y)] += int(r["V"])
    for y in sorted(acc):
        if y >= 2003:
            dv.append((ind, f"IBGE RC SIDRA tab. {tab} (derivado: soma da matriz)", defn, y, "", acc[y], "pessoas",
                       "DERIVADO: soma; anos recentes ficam incompletos (registro tardio ainda chegando); anos < 2003 nao entram (registros de 1984-2002 estao em outra tabela)", f"SIDRA API; {ACQ}"))
write(DE + "ibge_rc_por_ano_de_ocorrencia_soma_matriz.csv", dv)


# ---------- Banco Mundial WDI ----------
def wdi(code):
    d = json.load(open(BR + f"wdi_{code}.json"))
    meta, rows = d[0], d[1]
    return meta["lastupdated"], {int(r["date"]): r["value"] for r in rows}, rows[0]["indicator"]["value"]


wd = []
W = {}
for code, ind, un in (("SP.DYN.CBRT.IN", "taxa_bruta_natalidade", "por mil habitantes"), ("SP.DYN.CDRT.IN", "taxa_bruta_mortalidade", "por mil habitantes"),
                      ("SP.POP.TOTL", "populacao_total", "pessoas")):
    lu, vals, nome = wdi(code)
    W[code] = vals
    for a in sorted(vals):
        if vals[a] is None:
            continue
        wd.append((ind, f"Banco Mundial WDI {code}", nome, a, "", vals[a], un,
                   "Brasil; estimativa (modelo ONU/Divisao de Populacao via WDI), NAO e registro", f"WDI lastupdated {lu}; {ACQ}"))
write(SE + "wdi_banco_mundial.csv", wd)

lu = wdi("SP.POP.TOTL")[0]
wde = []
for a in sorted(W["SP.POP.TOTL"]):
    cb, cd, pop = W["SP.DYN.CBRT.IN"].get(a), W["SP.DYN.CDRT.IN"].get(a), W["SP.POP.TOTL"].get(a)
    if None in (cb, cd, pop) or a < 1960:
        continue
    for ind, taxa in (("nascimentos_estimados_wdi", cb), ("obitos_estimados_wdi", cd)):
        wde.append((ind, "DERIVADO de Banco Mundial WDI (taxa bruta x populacao / 1000)", "formula: SP.DYN.CBRT.IN (ou CDRT) x SP.POP.TOTL / 1000",
                    a, "", round(taxa * pop / 1000), "pessoas",
                    "ESTIMATIVA derivada (taxas ONU/WPP via WDI), nao registro; arredondado a unidade", f"WDI lastupdated {lu}; {ACQ}"))
write(DE + "wdi_nascimentos_obitos_estimados.csv", wde)

# ---------- ONU WPP 2024 ----------
wp = []
WPP = {}
with gzip.open(BR + "wpp2024_demographic_indicators_medium.csv.gz", "rt", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        if r["ISO3_code"] == "BRA":
            a = int(r["Time"])
            if a > 2026:
                continue
            WPP[a] = r
for a in sorted(WPP):
    r = WPP[a]
    nota = "Brasil; variante Medium; estimativa/projecao ONU, NAO e registro; unidade original mil, convertida x1000"
    nota += "; ANO DE PROJECAO segundo a documentacao do WPP 2024 (estima ate 2023; limite NAO verificado no arquivo baixado)" if a >= 2024 else ""
    for ind, col, un in (("nascimentos_wpp", "Births", "pessoas"), ("obitos_wpp", "Deaths", "pessoas")):
        wp.append((ind, "ONU World Population Prospects 2024", f"Demographic Indicators Medium, coluna {col}", a, "", round(float(r[col]) * 1000), un, nota, f"WPP 2024; {ACQ}"))
write(SE + "onu_wpp2024.csv", wp)

# ---------- saldo e razao por base ----------
def dd(rows, ind):
    return {r[3]: r[5] for r in rows if r[0] == ind and r[4] == ""}


bases = {
    "DATASUS (SIM obitos por ocorrencia x SINASC nascidos por ocorrencia)": (dd(sn, "nascidos_vivos_por_ocorrencia"), dd(sim, "obitos_total_por_ocorrencia"), "1994-2025 (2026 excluido: incompleto)", "n/a"),
    "IBGE Registro Civil, registrados no ano (nasc. registrados x obitos registrados, lugar do registro/ residencia)": (
        {**dd(ib, "nascidos_vivos_registrados_no_ano"), **dd(ib, "nascidos_vivos_registrados_no_ano_lugar_registro")},
        {**dd(ib, "obitos_registrados_no_ano"), **dd(ib, "obitos_registrados_no_ano_lugar_registro")}, "1984-2024", "n/a"),
    "IBGE Registro Civil, ocorridos no ano (nascidos ocorridos x obitos ocorridos; 1984-2002 obitos = ocorridos E registrados)": (
        dd(ib, "nascidos_vivos_ocorridos_no_ano"), {**dd(ib, "obitos_ocorridos_e_registrados_no_ano"), **dd(ib, "obitos_ocorridos_no_ano")}, "1984-2024", "n/a"),
    "Banco Mundial WDI (derivado, estimativa)": (dd(wde, "nascimentos_estimados_wdi"), dd(wde, "obitos_estimados_wdi"), "1960-2024", "n/a"),
    "ONU WPP 2024 (estimativa)": (dd(wp, "nascimentos_wpp"), dd(wp, "obitos_wpp"), "1950-2026", "n/a"),
}
sr = []
for nome, (nasc, obt, per, _) in bases.items():
    for a in sorted(set(nasc) & set(obt)):
        if "DATASUS" in nome and a >= 2026:
            continue
        if "DATASUS" in nome and a < 1994:
            continue
        if "WPP" in nome and a > 2025:
            continue
        sd = nasc[a] - obt[a]
        sr.append(("saldo_nascimentos_menos_obitos", nome, "nascimentos - obitos", a, "", sd, "pessoas", "calculado no ano; bases nunca emendadas", ACQ))
        sr.append(("razao_obitos_por_nascimento", nome, "obitos / nascimentos", a, "", round(obt[a] / nasc[a], 4), "razao", "calculado no ano; bases nunca emendadas", ACQ))
write(DE + "saldo_e_razao_por_base.csv", sr)
