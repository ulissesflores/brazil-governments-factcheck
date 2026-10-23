#!/usr/bin/env python3
"""Constroi series/ibge_fase2_longo.csv e series/sobreposicoes.csv a partir de bruto/ (somente leitura).

Requer xlrd (leitura de .xls). Rodar com `python3 -I construir_series.py` num interpretador com xlrd.
Nada e estimado nem interpolado; razoes sao computadas so entre componentes do MESMO ano e da MESMA base
(linha). Bases nunca sao emendadas: cada `definicao_linha` e uma base.
"""
import csv
import gzip
import io
import json
import re
import statistics
import sys
import zipfile
from pathlib import Path

import xlrd

AQUI = Path(__file__).resolve().parent
BRUTO = AQUI / "bruto"
SAIDA = AQUI / "series"

# --- baixado_em por arquivo, lido da cadeia de hash --------------------------------------------
BAIXADO = {}
for lin in (AQUI / "manifest.jsonl").read_text().splitlines():
    r = json.loads(lin)
    BAIXADO[Path(r["arquivo"]).name] = r["timestamp_utc"][:10]

LINHAS = []  # (indicador,fonte,definicao_linha,ano,mes_ou_trimestre,valor,unidade,nota,vintage)


def emit(ind, fonte, defn, ano, valor, unidade, nota, vintage):
    LINHAS.append([ind, fonte, defn, int(ano), "", valor, unidade, nota, vintage])


def num(x):
    if isinstance(x, (int, float)):
        return float(x)
    return None


# =============================================================================================
# 1. IPEADATA (concatenada pelo proprio Ipeadata)
# =============================================================================================
def ler_json(p):
    b = Path(p).read_bytes()
    if b[:2] == b"\x1f\x8b":
        b = gzip.decompress(b)
    return json.loads(b)


META = {}
mcomp = BRUTO / "ipeadata-Metadados-completo.json"
if mcomp.exists():
    for r in ler_json(mcomp)["value"]:
        if r["SERCODIGO"].startswith("SCN10_"):
            META[r["SERCODIGO"]] = r

L_IPEA = "ipeadata_concatenada"
NOTA_IPEA = (
    "Serie concatenada pelo Ipeadata (nao por nos): 1947-1989 SCN Consolidadas; 1990-1994 SCN ref. 1985; "
    "1995-1999 estimativas das Contas Nacionais Trimestrais ref. 2010; 2000+ SCN ref. 2010 (metadado Ipeadata)"
)
IPEA = {}
for cod, ind, unid in [
    ("SCN10_VAITN10", "va_industria_transformacao", "R$ milhoes correntes (moeda convertida pelo Ipeadata)"),
    ("SCN10_PIBN10", "pib_mercado", "R$ milhoes correntes (moeda convertida pelo Ipeadata)"),
    ("SCN10_PIBPBN10", "pib_precos_basicos", "R$ milhoes correntes (moeda convertida pelo Ipeadata)"),
    ("SCN10_CFGGN10", "consumo_final_governo", "R$ milhoes correntes (moeda convertida pelo Ipeadata)"),
    ("SCN10_XBSZN10", "exportacoes_bens_servicos", "R$ milhoes correntes (moeda convertida pelo Ipeadata)"),
    ("SCN10_MBSZN10", "importacoes_bens_servicos", "R$ milhoes correntes (moeda convertida pelo Ipeadata)"),
    ("SCN10_VAITY10", "ind_transf_pib_publicado_ipeadata_pct", "% (razao publicada pelo Ipeadata)"),
]:
    arq = BRUTO / f"ipeadata-{cod}-valores.json"
    if not arq.exists():
        print("FALTA", arq.name, file=sys.stderr)
        continue
    upd = (META.get(cod) or {}).get("SERATUALIZACAO", "")[:10]
    vint = f"Ipeadata SERATUALIZACAO {upd or 'n/d'}; baixado {BAIXADO[arq.name]}"
    for r in ler_json(arq)["value"]:
        if r["VALVALOR"] is None:
            continue
        ano = int(r["VALDATA"][:4])
        v = abs(r["VALVALOR"]) if cod == "SCN10_MBSZN10" else r["VALVALOR"]
        IPEA.setdefault(ind, {})[ano] = v
        emit(ind, f"Ipeadata {cod}", L_IPEA, ano, v, unid, NOTA_IPEA, vint)

# =============================================================================================
# 2. IBGE SCN ref. 2010, edicao 2023
# =============================================================================================
L_2010 = "ibge_scn_ref2010_ed2023"
V_2010 = "IBGE SCN edicao 2023 (arquivo no FTP de 2025-11-06); baixado 2026-10-20"
N_2010 = "SCN referencia 2010, valores correntes; 2000-2023"


def col_corrente_ano(s):
    """tab10_1: ano na linha 4 (primeira coluna do par), 'Corrente' na linha 5."""
    anos, ult = {}, None
    for c in range(s.ncols):
        v4, v5 = s.cell_value(4, c), s.cell_value(5, c)
        if isinstance(v4, float) and 1900 < v4 < 2100:
            ult = int(v4)
        if str(v5).strip() == "Corrente" and ult is not None:
            anos[ult] = c
    return anos


tab10 = xlrd.open_workbook(BRUTO / "scn-ref2010-vint2023-tab10_1.xls").sheet_by_index(0)
cols = col_corrente_ano(tab10)
for r in range(tab10.nrows):
    rot = str(tab10.cell_value(r, 1)).strip()
    if rot == "Total":
        for a, c in cols.items():
            emit("pib_precos_basicos", "IBGE SCN tab10_1 (VAB total a precos basicos)", L_2010, a, num(tab10.cell_value(r, c)),
                 "R$ milhoes correntes", N_2010 + "; 'Total' do valor adicionado bruto", V_2010)
    if rot == "Indústrias de transformação":
        for a, c in cols.items():
            emit("va_industria_transformacao", "IBGE SCN tab10_1", L_2010, a, num(tab10.cell_value(r, c)),
                 "R$ milhoes correntes", N_2010, V_2010)

tab05 = xlrd.open_workbook(BRUTO / "scn-ref2010-vint2023-tab05.xls").sheet_by_index(0)
col05 = {}
for c in range(tab05.ncols):
    m = re.match(r"(\d{4})\s*valor\s*corrente", str(tab05.cell_value(4, c)).replace("\n", " "))
    if m:
        col05[int(m.group(1))] = c
sec = None
for r in range(tab05.nrows):
    rot = str(tab05.cell_value(r, 0)).replace("\n", " ").strip()
    if rot.startswith("A - "):
        sec = "A"
    elif rot.startswith("B - "):
        sec = "B"
    elif rot.startswith("C - "):
        sec = "C"
    alvo = None
    if sec == "A" and rot == "Total":
        alvo = "pib_mercado"
    elif sec == "B" and rot.startswith("Despesa de consumo do governo"):
        alvo = "consumo_final_governo"
    elif sec == "B" and rot.startswith("Exportação de bens e serviços"):
        alvo = "exportacoes_bens_servicos"
    elif sec == "B" and rot.startswith("Importação de bens e serviços"):
        alvo = "importacoes_bens_servicos"
    if alvo:
        for a, c in col05.items():
            v = num(tab05.cell_value(r, c))
            if v is not None:
                emit(alvo, "IBGE SCN tab05", L_2010, a, abs(v), "R$ milhoes correntes", N_2010, V_2010)

tab06 = xlrd.open_workbook(BRUTO / "scn-ref2010-vint2023-tab06.xls").sheet_by_index(0)
PIB06 = {}
for r in range(tab06.nrows):
    a = tab06.cell_value(r, 0)
    if isinstance(a, float) and 1990 < a < 2100:
        v = num(tab06.cell_value(r, 1))
        PIB06[int(a)] = v
        if int(a) < 2000:
            emit("pib_mercado", "IBGE SCN tab06 (PIB 1996-1999 retropolado pelas CNT ref. 2010)", L_2010, int(a), v,
                 "R$ milhoes correntes", "SCN ref. 2010, tab06; 1996-1999 sao o trecho retropolado (so PIB, sem valor adicionado por atividade)",
                 V_2010)

# =============================================================================================
# 3. IBGE SCN ref. 2000, edicao 2009
# =============================================================================================
L_2000 = "ibge_scn_ref2000_ed2009"
V_2000 = "IBGE SCN edicao 2009 (arquivo no FTP, data de listagem 2016-08-17); baixado 2026-10-20"
N_2000 = "SCN referencia 2000, valores correntes; 1995-2009 (1995-1999 retropolados pelo IBGE)"
zf = zipfile.ZipFile(BRUTO / "scn-ref2000-vint2009-sinoticas.zip")


def xls_do_zip(zf, nome):
    return xlrd.open_workbook(file_contents=zf.read(nome)).sheet_by_index(0)


def linhas_ano(s, linha_anos):
    return {int(s.cell_value(linha_anos, c)): c for c in range(s.ncols)
            if isinstance(s.cell_value(linha_anos, c), float) and 1900 < s.cell_value(linha_anos, c) < 2100}


for periodo, arq in (("1995_1999", "1995_1999/tab04.xls"), ("2000_2009", "2000_2009/tab04.xls")):
    s = xls_do_zip(zf, arq)
    anos = linhas_ano(s, 4)
    secB = False
    for r in range(s.nrows):
        rot = str(s.cell_value(r, 0)).replace("\n", " ").strip()
        if rot.startswith("A - "):
            sec = "A"
        elif rot.startswith("B - "):
            sec = "B"
        elif rot.startswith("C - "):
            sec = "C"
        alvo = None
        if sec == "A" and rot == "Total":
            alvo = "pib_mercado"
        elif sec == "B" and rot.startswith("Despesa de consumo da administração pública"):
            alvo = "consumo_final_governo"
        elif sec == "B" and rot.startswith("Exportação de bens e serviços"):
            alvo = "exportacoes_bens_servicos"
        elif sec == "B" and rot.startswith("Importação de bens e serviços"):
            alvo = "importacoes_bens_servicos"
        if alvo:
            for a, c in anos.items():
                v = num(s.cell_value(r, c))
                if v is not None:
                    emit(alvo, f"IBGE SCN {arq}", L_2000, a, abs(v), "R$ milhoes correntes", N_2000, V_2000)

# valor adicionado: 2000-2009 (classes 0301..0334) e 1995-1999 (codigos 04..32)
s = xls_do_zip(zf, "2000_2009/tab09.xls")
anos = {}
ult = None
for c in range(s.ncols):
    v4 = s.cell_value(4, c)
    if isinstance(v4, float):
        ult = int(v4)
    if str(s.cell_value(5, c)).strip() == "Corrente" and ult:
        anos[ult] = c
soma, ind_tot, ext, util, cons, total = {}, {}, {}, {}, {}, {}
for r in range(6, s.nrows):
    cod, rot = str(s.cell_value(r, 0)).strip(), str(s.cell_value(r, 1)).strip()
    for a, c in anos.items():
        v = num(s.cell_value(r, c))
        if v is None:
            continue
        if rot == "Total":
            total[a] = v
        elif rot == "Indústria":
            ind_tot[a] = v
        elif re.fullmatch(r"03(0[1-9]|[12]\d|3[0-4])", cod):
            soma[a] = soma.get(a, 0) + v
        elif cod in ("0201", "0202", "0203"):
            ext[a] = ext.get(a, 0) + v
        elif cod == "0501":
            cons[a] = v
        elif cod == "0401" or (cod == "" and rot.startswith("limpeza urbana")):
            util[a] = v
for a in sorted(anos):
    chk = ind_tot[a] - ext[a] - util[a] - cons[a]
    emit("va_industria_transformacao", "IBGE SCN 2000_2009/tab09 (soma das classes 0301-0334)", L_2000, a, soma[a], "R$ milhoes correntes",
         N_2000 + f"; derivado por soma das 34 classes de transformacao 0301-0334; conferencia pelo residuo Industria-extrativas-utilidades-construcao = {chk:.0f}",
         V_2000)
    emit("pib_precos_basicos", "IBGE SCN 2000_2009/tab09 (VAB total)", L_2000, a, total[a], "R$ milhoes correntes",
         N_2000 + "; 'Total' do valor adicionado bruto a precos basicos", V_2000)
    assert abs(chk - soma[a]) < 1.5, (a, chk, soma[a])

s = xls_do_zip(zf, "1995_1999/tab09.xls")
anos = {}
ult = None
for c in range(s.ncols):
    v4 = s.cell_value(4, c)
    if isinstance(v4, float):
        ult = int(v4)
    if str(s.cell_value(5, c)).strip() == "Corrente" and ult:
        anos[ult] = c
soma, ind_tot, outros, total = {}, {}, {}, {}
for r in range(6, s.nrows):
    cod, rot = str(s.cell_value(r, 0)).strip(), str(s.cell_value(r, 1)).strip()
    for a, c in anos.items():
        v = num(s.cell_value(r, c))
        if v is None:
            continue
        if rot == "Total da economia":
            total[a] = v
        elif rot == "Indústria":
            ind_tot[a] = v
        elif re.fullmatch(r"(0[4-9]|[12]\d|3[0-2])", cod):
            soma[a] = soma.get(a, 0) + v
        elif cod in ("02", "03", "33", "34"):
            outros[a] = outros.get(a, 0) + v
for a in sorted(anos):
    chk = ind_tot[a] - outros[a]
    emit("va_industria_transformacao", "IBGE SCN 1995_1999/tab09 (soma dos codigos 04-32)", L_2000, a, soma[a], "R$ milhoes correntes",
         N_2000 + f"; derivado por soma dos codigos 04-32 (classificacao N80); conferencia pelo residuo Industria-02-03-33-34 = {chk:.0f}",
         V_2000)
    emit("pib_precos_basicos", "IBGE SCN 1995_1999/tab09 (VAB total)", L_2000, a, total[a], "R$ milhoes correntes",
         N_2000 + "; 'Total da economia' do valor adicionado bruto", V_2000)
    assert abs(chk - soma[a]) < 1.5, (a, chk, soma[a])

# =============================================================================================
# 4. IBGE SCN Consolidadas 1947-1989 (edicao 2009)
# =============================================================================================
L_CONS = "ibge_scn_consolidadas_1947-1989"
V_CONS = "IBGE SCN Consolidadas (arquivo consolidada.zip da edicao 2009; listagem FTP 2016-08-17); baixado 2026-10-20"
zc = zipfile.ZipFile(BRUTO / "scn-vint2009-consolidada.zip")


def quadro(wb, n):
    for nome in wb.sheet_names():
        if nome.lower().replace(" ", "") == f"quadro{n}":
            return wb.sheet_by_name(nome)
    raise KeyError(n)


CONS = {}
for arq in ("tab47_55.xls", "tab56_64.xls", "tab65_69.xls", "tab70_80.xls", "tab80_89.xls"):
    wb = xlrd.open_workbook(file_contents=zc.read(arq))
    for n in ("1", "7"):
        s = quadro(wb, n)
        unid = None
        anos = {}
        for r in range(s.nrows):
            row = s.row_values(r)
            for c in row:
                if isinstance(c, str) and re.search(r"C[Rr]\$", c):
                    unid = c.strip()
            ys = {}
            for c, v in enumerate(row[1:], 1):
                m = re.match(r"\s*(19\d\d)", str(v))
                if m:
                    ys[int(m.group(1))] = c
            if len(ys) >= 4 and not anos:
                anos = ys
        assert anos, (arq, n)
        un = f"{unid or 'moeda da epoca (cabecalho sem unidade)'} (moeda da epoca, milhoes; nao convertida)"
        for r in range(s.nrows):
            rot = str(s.cell_value(r, 0)).strip()
            alvo = None
            if n == "1":
                if rot == "Produto Interno Bruto":
                    alvo = "pib_mercado"
                elif rot.startswith("1.5 - Consumo final das administra"):
                    alvo = "consumo_final_governo"
                elif rot.startswith("1.8 - Exporta"):
                    alvo = "exportacoes_bens_servicos"
                elif rot.startswith("1.9 - Menos"):
                    alvo = "importacoes_bens_servicos"
            else:
                if rot == "Transformação":
                    alvo = "va_industria_transformacao"
                elif rot == "Produto Interno Bruto a Custo de Fatores":
                    alvo = "pib_precos_basicos"
            if alvo:
                for a, c in anos.items():
                    v = num(s.cell_value(r, c))
                    if v is not None:
                        CONS.setdefault((alvo, a), []).append((arq, v))
                        dup = a == 1980 and arq == "tab70_80.xls"
                        emit(alvo, f"IBGE SCN Consolidadas {arq} quadro{n}", L_CONS + ("_1980_duplicado_tab70_80" if dup else ""), a, v, un,
                             "SCN Consolidadas (referencia 1980 e anteriores); valor adicionado da transformacao e PIB 'a custo de fatores' "
                             "(aproxima precos basicos); "
                             + ("1980 aparece em dois arquivos com valores diferentes (unidade e revisao); esta linha guarda o de tab70_80, a linha principal usa tab80_89" if dup else ""),
                             V_CONS)

# =============================================================================================
# 5. IBGE CNT (SIDRA 1846): soma dos 4 trimestres de valores correntes
# =============================================================================================
L_CNT = "ibge_cnt_ref2010_soma4tri"
cnt = json.loads((BRUTO / "sidra-1846-cnt-valores-correntes.json").read_bytes())
V_CNT = f"SIDRA 1846 (CNT), baixado {BAIXADO['sidra-1846-cnt-valores-correntes.json']}; ultimo trimestre disponivel 2026-T2"
mapa = {"90693": "va_industria_transformacao", "90705": "pib_precos_basicos", "90707": "pib_mercado",
        "93405": "consumo_final_governo", "93407": "exportacoes_bens_servicos", "93408": "importacoes_bens_servicos"}
tri = {}
for r in cnt[1:]:
    if r["D4C"] in mapa and r["V"] not in ("-", "...", "X", ".."):
        tri.setdefault((mapa[r["D4C"]], int(r["D3C"][:4])), {})[r["D3C"][4:]] = float(r["V"])
for (ind, a), q in sorted(tri.items()):
    if sorted(q) == ["01", "02", "03", "04"]:
        emit(ind, "IBGE SIDRA 1846 (soma dos 4 trimestres)", L_CNT, a, abs(sum(q.values())), "R$ milhoes correntes",
             "CNT ref. 2010; soma aritmetica dos 4 trimestres de valores correntes (derivada por nos; nao e publicacao anual do IBGE)", V_CNT)

# =============================================================================================
# 6. Internet nos domicilios
# =============================================================================================
def sidra_linhas(arq):
    return json.loads((BRUTO / arq).read_bytes())[1:]


def ok(v):
    return v not in ("-", "...", "X", "..", "")


L_MC = "pnad_microcomputador_com_internet_2003-2015"
V_MC = f"SIDRA 2387 (dados de 2003-2015; modificacao SIDRA ver periodos); baixado {BAIXADO['sidra-2387-pnad-microcomputador-internet.json']}"
for r in sidra_linhas("sidra-2387-pnad-microcomputador-internet.json"):
    if r["D4C"] != "99581" or not ok(r["V"]):
        continue
    a = int(r["D3C"])
    if r["D5C"] == "104296" and r["D2C"] == "1000096":
        emit("internet_domicilios_pct", "IBGE SIDRA 2387 PNAD", L_MC, a, float(r["V"]), "% dos domicilios particulares permanentes",
             "Conceito: domicilios COM MICROCOMPUTADOR COM ACESSO A INTERNET (nao inclui acesso so por celular/tablet)", V_MC)
    if r["D5C"] == "104296" and r["D2C"] == "96":
        emit("internet_domicilios_mil", "IBGE SIDRA 2387 PNAD", L_MC, a, float(r["V"]), "mil domicilios",
             "numerador; mesmo conceito", V_MC)
    if r["D5C"] == "104306" and r["D2C"] == "96":
        emit("domicilios_total_mil", "IBGE SIDRA 2387 PNAD", L_MC, a, float(r["V"]), "mil domicilios", "denominador", V_MC)

L_UT = "pnad_utilizacao_internet_2013-2015"
V_UT = f"SIDRA 5144 (suplemento PNAD); baixado {BAIXADO['sidra-5144-pnad-utilizacao-internet.json']}"
for r in sidra_linhas("sidra-5144-pnad-utilizacao-internet.json"):
    if r["D4C"] != "6795" or not ok(r["V"]):
        continue
    a = int(r["D3C"])
    if r["D5C"] == "33299" and r["D2C"] == "5949":
        emit("internet_domicilios_pct", "IBGE SIDRA 5144 PNAD", L_UT, a, float(r["V"]), "% dos domicilios particulares permanentes",
             "Conceito: domicilios COM UTILIZACAO DA INTERNET (qualquer equipamento) no periodo de referencia", V_UT)
    if r["D5C"] == "33299" and r["D2C"] == "96":
        emit("internet_domicilios_mil", "IBGE SIDRA 5144 PNAD", L_UT, a, float(r["V"]), "mil domicilios", "numerador; mesmo conceito", V_UT)
    if r["D5C"] == "33298" and r["D2C"] == "96":
        emit("domicilios_total_mil", "IBGE SIDRA 5144 PNAD", L_UT, a, float(r["V"]), "mil domicilios", "denominador", V_UT)

L_PC = "pnadc_tic_utilizacao_internet_2016+"
V_PC = f"SIDRA 7307 (PNAD Continua TIC); baixado {BAIXADO['sidra-7307-pnadc-tic-utilizacao-internet.json']}"
for r in sidra_linhas("sidra-7307-pnadc-tic-utilizacao-internet.json"):
    if r["D4C"] != "6795" or not ok(r["V"]):
        continue
    a = int(r["D3C"])
    if r["D5C"] == "48534" and r["D2C"] == "9784":
        emit("internet_domicilios_pct", "IBGE SIDRA 7307 PNADC TIC", L_PC, a, float(r["V"]), "% dos domicilios",
             "Conceito: domicilios COM UTILIZACAO DE INTERNET; PNAD Continua (nova amostra e questionario)", V_PC)
    if r["D5C"] == "48534" and r["D2C"] == "162":
        emit("internet_domicilios_mil", "IBGE SIDRA 7307 PNADC TIC", L_PC, a, float(r["V"]), "mil domicilios", "numerador; mesmo conceito", V_PC)
    if r["D5C"] == "33298" and r["D2C"] == "162":
        emit("domicilios_total_mil", "IBGE SIDRA 7307 PNADC TIC", L_PC, a, float(r["V"]), "mil domicilios", "denominador", V_PC)

# =============================================================================================
# 7. Razoes por linha (mesma base, mesmo ano) e sobreposicoes
# =============================================================================================
COMP = {}
vint_de, nota_de = {}, {}
for ind, fonte, defn, ano, _, v, un, nota, vint in LINHAS:
    COMP.setdefault((defn, ind), {})[ano] = v  # ultima ocorrencia (consolidadas 1980 em 2 arquivos: ver abaixo)
    vint_de[defn] = vint

DUP1980 = {ind: lst for (ind, a), lst in CONS.items() if a == 1980 and len(lst) > 1}
RAZOES = [
    ("ind_transf_sobre_pib_mercado_pct", "va_industria_transformacao", "pib_mercado"),
    ("ind_transf_sobre_pib_basico_pct", "va_industria_transformacao", "pib_precos_basicos"),
    ("consumo_governo_sobre_pib_mercado_pct", "consumo_final_governo", "pib_mercado"),
]
SHARES = {}
for defn in {k[0] for k in COMP}:
    vint = vint_de[defn]
    for nome, num_, den in RAZOES:
        a_, b_ = COMP.get((defn, num_), {}), COMP.get((defn, den), {})
        for ano in sorted(set(a_) & set(b_)):
            if b_[ano]:
                v = 100 * a_[ano] / b_[ano]
                SHARES.setdefault((defn, nome), {})[ano] = v
                emit(nome, "derivado: razao de componentes da mesma base e do mesmo ano", defn, ano, v, "%",
                     f"{num_} / {den}", vint)
    x, m, p = COMP.get((defn, "exportacoes_bens_servicos"), {}), COMP.get((defn, "importacoes_bens_servicos"), {}), COMP.get((defn, "pib_mercado"), {})
    for ano in sorted(set(x) & set(m) & set(p)):
        v = 100 * (x[ano] + m[ano]) / p[ano]
        SHARES.setdefault((defn, "abertura_comercial_sobre_pib_mercado_pct"), {})[ano] = v
        emit("abertura_comercial_sobre_pib_mercado_pct", "derivado: razao de componentes da mesma base e do mesmo ano", defn, ano, v, "%",
             "(exportacoes + importacoes) / pib_mercado", vint)
for ano, v in IPEA.get("ind_transf_pib_publicado_ipeadata_pct", {}).items():
    SHARES.setdefault((L_IPEA, "ind_transf_pib_publicado_ipeadata_pct"), {})[ano] = v
for (defn, ind), d in COMP.items():
    if ind in ("internet_domicilios_pct",):
        SHARES[(defn, ind)] = d

# --- gravacao ---------------------------------------------------------------------------------
SAIDA.mkdir(exist_ok=True)
CAB = ["indicador", "fonte", "definicao_linha", "ano", "mes_ou_trimestre", "valor", "unidade", "nota", "vintage"]
with open(SAIDA / "ibge_fase2_longo.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(CAB)
    for l in sorted(LINHAS, key=lambda x: (x[0], x[2], x[3], x[1])):
        w.writerow(l)

# sobreposicoes: pares de linhas, mesmo indicador (razao), anos comuns
PARES = []
for nome in ("ind_transf_sobre_pib_mercado_pct", "ind_transf_sobre_pib_basico_pct", "consumo_governo_sobre_pib_mercado_pct",
             "abertura_comercial_sobre_pib_mercado_pct", "internet_domicilios_pct"):
    linhas = [k[0] for k in SHARES if k[1] == nome]
    for i, A in enumerate(sorted(linhas)):
        for B in sorted(linhas)[i + 1:]:
            comum = sorted(set(SHARES[(A, nome)]) & set(SHARES[(B, nome)]))
            if comum:
                dif = [SHARES[(B, nome)][a] - SHARES[(A, nome)][a] for a in comum]
                PARES.append((nome, A, B, comum[0], comum[-1], len(comum), statistics.mean(dif), min(dif), max(dif)))
# publicado Ipeadata vs razao Ipeadata
for A in (L_IPEA,):
    pub = SHARES.get((A, "ind_transf_pib_publicado_ipeadata_pct"), {})
    for nome in ("ind_transf_sobre_pib_mercado_pct", "ind_transf_sobre_pib_basico_pct"):
        cal = SHARES.get((A, nome), {})
        comum = sorted(set(pub) & set(cal))
        if not comum:
            continue
        dif = [cal[a] - pub[a] for a in comum]
        PARES.append((f"{nome}", "ipeadata_publicado(VAITY10)", f"ipeadata_razao_dos_niveis", comum[0], comum[-1], len(comum),
                      statistics.mean(dif), min(dif), max(dif)))
with open(SAIDA / "sobreposicoes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["indicador", "linha_A", "linha_B", "ano_ini", "ano_fim", "n_anos", "dif_media_B_menos_A_pp", "dif_min_pp", "dif_max_pp"])
    for p in PARES:
        w.writerow([p[0], p[1], p[2], p[3], p[4], p[5], f"{p[6]:.3f}", f"{p[7]:.3f}", f"{p[8]:.3f}"])
print(len(LINHAS), "linhas;", len(PARES), "pares de sobreposicao")
