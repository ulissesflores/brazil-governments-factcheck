"""Constroi series/mundo.csv, series/termos_de_troca.csv e series/crescimento_contexto.csv a partir do BRUTO.

Sem rede. Rodar: python3 -I .../mundo/scripts/construir.py
Regras: valor ausente fica ausente (sem interpolacao); nada e escolhido depois de ver resultado:
os indicadores e as unidades vem do pre-registro (Emenda 01, secoes A e B 'Growth context').
Cabecalho de saida: indicador,fonte,definicao_linha,pais_ou_grupo,ano,valor,unidade,nota,vintage
"""
import csv
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
import xlsx_min as xl  # noqa: E402

COLS = ["indicador", "fonte", "definicao_linha", "pais_ou_grupo", "ano", "valor", "unidade", "nota", "vintage"]
PAISES = ["BRA", "ARG", "CHL", "COL", "MEX", "PER", "URY", "VEN"]
GRUPOS = ["WLD", "LCN", "UMC"]
UNIDADES = PAISES + GRUPOS
ID2ISO = {"1W": "WLD", "ZJ": "LCN", "XT": "UMC"}
V_WDI = "WDI 2026-10-08 (baixado 2026-10-19)"
V_PIP = "PIP release 20260922, PPC 2017 (versao corrente em 2026-10-19)"
NOTA_VEN = "VEN: dados sinalizados, nao omitidos; cobertura e lacunas por indicador em RESULTADO.md"


def gravar(caminho, linhas):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, COLS, lineterminator="\n")
        w.writeheader()
        for r in linhas:
            w.writerow({c: ("" if r.get(c) is None else r[c]) for c in COLS})
    return len(linhas)


def num(x):
    """float ou None (celula vazia, '..' ou 'ND' = nao disponivel)."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def fmt(v):
    return repr(round(v, 6)) if v is not None else ""


def wdi(codigo, base="bruto/wdi"):
    """{(unidade, ano): valor} de um bruto WDI (formato /v2/country/.../indicator)."""
    d = json.load(open(RAIZ / base / f"{codigo}.json"))[1]
    out = {}
    for r in d:
        if r["value"] is None:
            continue
        u = r["countryiso3code"] or ID2ISO.get(r["country"]["id"], "")
        if u in UNIDADES:
            out[(u, int(r["date"]))] = float(r["value"])
    return out


def arquivo(codigo, versao):
    """{(unidade, ano): valor} de uma versao do arquivo WDI (fonte 57; bruto em wdi_arquivo/)."""
    d = json.load(open(RAIZ / f"wdi_arquivo/bruto/{codigo}_v{versao}.json"))["source"]["data"]
    return {(r["variable"][0]["id"], int(r["variable"][3]["id"][2:])): float(r["value"]) for r in d
            if r["value"] is not None and r["variable"][0]["id"] in UNIDADES}


def linhas_wdi(ind, codigo, defin, unid, nota_base="", primeiro=1960, vintage=V_WDI):
    out = []
    for (u, a), v in sorted(wdi(codigo).items()):
        if a < primeiro:
            continue
        nota = nota_base
        if u == "VEN":
            nota = (nota + "; " if nota else "") + NOTA_VEN
        out.append(dict(indicador=ind, fonte=f"WDI {codigo}", definicao_linha=defin, pais_ou_grupo=u, ano=a,
                        valor=fmt(v), unidade=unid, nota=nota, vintage=vintage))
    return out


def pip_linhas():
    out = []
    for arq, ind_p, linha, unid_p, vint in [
        ("bruto/pip/pip_685_ppp2017.csv", "mun_pobreza_685", "pessoas abaixo de US$ 6,85/dia (PPC 2017), % da populacao", "% da populacao", V_PIP),
        ("bruto/pip/pip_830_ppp2021.csv", "mun_pobreza_830_ppc2021", "pessoas abaixo de US$ 8,30/dia (PPC 2021; equivalente da linha 6,85 de 2017), % da populacao", "% da populacao",
         "PIP release 20260922, PPC 2021 (versao corrente em 2026-10-19)"),
    ]:
        for r in csv.DictReader(open(RAIZ / arq)):
            if r["country_code"] not in PAISES:
                continue
            ok_nac = r["reporting_level"] == "national"
            if not ok_nac and r["country_code"] != "ARG":
                continue  # urbano so entra onde nao existe nacional (ARG); URY/COL urbano fica fora
            nota = f"{r['welfare_type']}; {r['survey_acronym']}; trecho comparavel {r['comparable_spell']}; nivel {r['reporting_level']}"
            if not ok_nac:
                nota += " (SO URBANO: nao e comparavel com series nacionais)"
            if r["country_code"] == "VEN":
                nota += "; " + NOTA_VEN
            ano = int(r["reporting_year"])
            out.append(dict(indicador=ind_p, fonte="PIP (Banco Mundial)", definicao_linha=linha, pais_ou_grupo=r["country_code"], ano=ano,
                            valor=fmt(float(r["headcount"]) * 100), unidade=unid_p, nota=nota, vintage=vint))
            if arq.endswith("pip_685_ppp2017.csv"):
                out.append(dict(indicador="mun_gini", fonte="PIP (Banco Mundial)", definicao_linha="indice de Gini da renda (ou consumo) per capita, 0-100", pais_ou_grupo=r["country_code"], ano=ano,
                                valor=fmt(float(r["gini"]) * 100), unidade="pontos (0-100)", nota=nota, vintage=V_PIP))
    return sorted(out, key=lambda r: (r["indicador"], r["pais_ou_grupo"], r["ano"]))


def vdem_linhas():
    out = []
    for r in csv.DictReader(open(RAIZ / "vdem_owid/bruto/owid_electoral_democracy_index_8paises.csv")):
        if r["code"] not in PAISES or int(r["year"]) < 1960:
            continue
        out.append(dict(indicador="mun_polyarchy", fonte="V-Dem v16 (via OWID, CC BY 4.0)",
                        definicao_linha="indice de democracia eleitoral v2x_polyarchy, 0-1, estimativa pontual",
                        pais_ou_grupo=r["code"], ano=int(r["year"]), valor=fmt(float(r["electdem_vdem__estimate_best"])), unidade="indice 0-1",
                        nota="o bruto do OWID veio com todos os paises (filtro ignorado); so os 8 de interesse entram aqui" + ("; " + NOTA_VEN if r["code"] == "VEN" else ""),
                        vintage="V-Dem v16 (OWID, 2026-03-17), baixado 2026-10-19"))
    return sorted(out, key=lambda r: (r["pais_ou_grupo"], r["ano"]))


def mundo():
    L = []
    L += linhas_wdi("mun_pibpc_ppc", "NY.GDP.PCAP.PP.KD", "PIB per capita, PPC (US$ internacionais constantes de 2021)", "US$ intern. constantes 2021",
                    "WDI trocou a base do PPC: 2011 -> 2017 (arquivo 2020-05) -> 2021 (arquivo 2024-05); ver quebras.csv")
    L += linhas_wdi("mun_pib_cresc", "NY.GDP.MKTP.KD.ZG", "crescimento real anual do PIB", "% a.a.")
    L += linhas_wdi("mun_expvida", "SP.DYN.LE00.IN", "expectativa de vida ao nascer, total", "anos", "estimativa modelada (Divisao de Populacao da ONU), nao contagem")
    L += linhas_wdi("mun_mortinf", "SP.DYN.IMRT.IN", "mortalidade infantil (menores de 1 ano)", "por mil nascidos vivos", "estimativa do grupo interagencias da ONU (IGME), nao registro")
    L += pip_linhas()
    L += linhas_wdi("mun_homic", "VC.IHR.PSRC.P5", "homicidios intencionais por 100 mil habitantes (UNODC via WDI)", "por 100 mil",
                    "definicao UNODC de homicidio intencional; Brasil usa o SIM/MS, com troca CID-9 -> CID-10 em 1996 (ver dominios-2)")
    L += linhas_wdi("mun_dtp3", "SH.IMM.IDPT", "imunizacao DTP3, % das criancas de 12-23 meses", "%", "estimativa WHO/UNICEF (WUENIC)")
    L += linhas_wdi("mun_inflacao", "FP.CPI.TOTL.ZG", "inflacao ao consumidor, variacao anual (FMI/IFS)", "% a.a.",
                    "WDI so traz Argentina de 2018 em diante e Venezuela ate 2016: lacuna da fonte, sem preenchimento")
    L += linhas_wdi("mun_desemprego_oit", "SL.UEM.TOTL.ZS", "desemprego total, % da forca de trabalho (estimativa MODELADA da OIT)", "% da forca de trabalho",
                    "MODELO: estimativa modelada da OIT, nao pesquisa nacional; semaforo amarelo pela regra D da Emenda 01")
    L += linhas_wdi("mun_divext_rnb", "DT.DOD.DECT.GN.ZS", "estoque total de divida externa (publica, garantida, privada nao garantida, FMI e curto prazo; IDS do Banco Mundial), % da renda nacional bruta", "% da RNB",
                    "IDS cobre so paises de renda baixa e media: sem CHL, URY, WLD e LCN (lacuna da fonte); o agregado de renda media-alta (UMC) existe; conceito do Banco Mundial, distinto dos dois conceitos do BCB (externo-fase3)",
                    vintage="WDI/IDS 2025-12-03 (baixado 2026-10-23)")
    L += vdem_linhas()
    ordem = {}
    for r in L:
        ordem.setdefault(r["indicador"], len(ordem))
    L.sort(key=lambda r: (ordem[r["indicador"]], r["pais_ou_grupo"], int(r["ano"])))
    return L


def ipea(codigo):
    v = json.load(open(RAIZ / f"ipea/bruto/ipea_{codigo}.json"))["value"]
    return {int(x["VALDATA"][:4]): float(x["VALVALOR"]) for x in v if x["VALVALOR"] is not None}


def termos_de_troca():
    L = []
    for cod, ind, defin, nota, vint in [
        ("FUNCEX_TTR", "tt_funcex", "termos de troca do Brasil, indice (media 2018 = 100), anual",
         "1879-1973 IBGE Estatisticas Historicas (ajustado conforme Estatisticas do Seculo XX); a partir de 1974 Funcex; serie ENCADEADA em 1973/1974 (nota da fonte)",
         "Ipeadata FUNCEX_TTR (atualizada 2026-03-26), baixado 2026-10-19"),
        ("HIST_TROCA", "tt_histtroca", "termos de troca do Brasil, indice (media 1995 = 100), anual, serie INATIVA (interrompida em 1975)",
         "IBGE Estatisticas Historicas do Brasil 1990 via Estatisticas do Seculo XX; serie interrompida", "Ipeadata HIST_TROCA (atualizada 2003-10-17), baixado 2026-10-19"),
    ]:
        for a, v in sorted(ipea(cod).items()):
            L.append(dict(indicador=ind, fonte=f"Ipeadata {cod}", definicao_linha=defin, pais_ou_grupo="BRA", ano=a, valor=fmt(v),
                          unidade="indice", nota=nota, vintage=vint))
    for (u, a), v in sorted(wdi("TT.PRI.MRCH.XD.WD").items(), key=lambda kv: (kv[0][0] != "BRA", kv[0])):
        L.append(dict(indicador="tt_wdi", fonte="WDI TT.PRI.MRCH.XD.WD (UNCTAD)", definicao_linha="termos de troca de mercadorias (net barter), indice 2015 = 100",
                      pais_ou_grupo=u, ano=a, valor=fmt(v), unidade="indice", nota=("VEN: dados sinalizados" if u == "VEN" else ""), vintage=V_WDI))
    # serie longa do WDI: a versao corrente so traz Brasil de 2005 em diante; a versao 202507 do arquivo traz 1980-2023 (mesmos valores nos anos comuns)
    for (u, a), v in sorted(arquivo("TT.PRI.MRCH.XD.WD", "202507").items(), key=lambda kv: (kv[0][0] != "BRA", kv[0])):
        L.append(dict(indicador="tt_wdi_arq", fonte="WDI arquivo v202507 TT.PRI.MRCH.XD.WD (UNCTAD)", definicao_linha="termos de troca de mercadorias (net barter), indice; mesma base da serie corrente (razao 1,000 nos anos comuns); o rotulo do arquivo diz 2000=100, rotulo desatualizado",
                      pais_ou_grupo=u, ano=a, valor=fmt(v), unidade="indice", nota="o WDI corrente (2026-10-08) NAO traz estes anos antes de 2005: serie encurtada pela fonte" + ("; VEN: dados sinalizados" if u == "VEN" else ""),
                      vintage="WDI arquivo, versao 202507, baixado 2026-10-19"))
    return L


def ler_fgv(arq):
    """Devolve {linha: {ano: valor}} das duas abas do xlsx FGV IBRE (nominal e % do PIB)."""
    out = {}
    for aba in ("Valores nominais", "Em % do PIB"):
        rows = list(xl.ler(arq, aba))
        anos = [int(x) for x in rows[0][1:] if x]
        for r in rows[1:]:
            if not r or not r[0]:
                continue
            if r[0].startswith("Investimentos l"):
                break  # 2o bloco da aba = investimento liquido de depreciacao (a partir de 2010); fora do escopo, nao misturar com o bloco bruto
            out[(aba, r[0])] = {a: num(v) for a, v in zip(anos, r[1:]) if num(v) is not None}
    return out


def crescimento_contexto():
    L = []
    fgv = ler_fgv(RAIZ / "invpub/bruto/fgv_investimentos_publicos_1947-2025.xlsx")
    V_FGV = "FGV IBRE Observatorio de Politica Fiscal, serie 1947-2025 (publicada 2026-04-10), baixado 2026-10-19"
    NOTA_FGV = ("1947-1994 IBGE Estatisticas do Seculo XX; 1995+ IBGE Contas Nacionais Trimestrais; investimento publico 1995+ de Gobetti (2006) e Orair (2016), "
                "2011+ Tesouro Nacional (aquisicao de ativos nao financeiros), estatais 2015+ SEST; trocas de fonte em 1995, 2011 e 2015 (aba Comentarios)")
    for a, v in sorted(fgv[("Em % do PIB", "FBCF")].items()):
        L.append(dict(indicador="cc_fbcf_pib", fonte="FGV IBRE (dados IBGE SCN)", definicao_linha="formacao bruta de capital fixo, % do PIB (precos correntes)", pais_ou_grupo="BRA", ano=a,
                      valor=fmt(v), unidade="% do PIB", nota=NOTA_FGV, vintage=V_FGV))
    p = ipea("PAN_FBKFPIBV")
    for a, v in sorted(p.items()):
        L.append(dict(indicador="cc_fbcf_pib", fonte="Ipeadata PAN_FBKFPIBV (IPEA)", definicao_linha="taxa de investimento nominal (FBCF, % do PIB)", pais_ou_grupo="BRA", ano=a, valor=fmt(v),
                      unidade="% do PIB", nota="IPEA a partir do SCN/IBGE; so 1996+", vintage="Ipeadata PAN_FBKFPIBV (atualizada 2026-03-10), baixado 2026-10-19"))
    for (u, a), v in sorted(wdi("NE.GDI.FTOT.ZS").items()):
        L.append(dict(indicador="cc_fbcf_pib", fonte="WDI NE.GDI.FTOT.ZS", definicao_linha="formacao bruta de capital fixo, % do PIB (WDI)", pais_ou_grupo=u, ano=a, valor=fmt(v),
                      unidade="% do PIB", nota="mesma fonte para Brasil e referencias" + ("; " + NOTA_VEN if u == "VEN" else ""), vintage=V_WDI))
    rot = {"GG": "governo geral (central + estados + municipios)", "SP (GG+EPU)": "setor publico = governo geral + empresas publicas da Uniao (EPU)",
           "GC": "governo central", "GE": "governos estaduais", "GM": "governos municipais", "EPU": "empresas publicas da Uniao"}
    for k, d in rot.items():
        for a, v in sorted(fgv[("Em % do PIB", k)].items()):
            L.append(dict(indicador="cc_invpub_pib", fonte="FGV IBRE Observatorio de Politica Fiscal", definicao_linha=f"investimento publico, % do PIB: {d}", pais_ou_grupo="BRA", ano=a,
                          valor=fmt(v), unidade="% do PIB", nota="LITERATURA/COMPILACAO (nao e serie oficial unica): " + NOTA_FGV, vintage=V_FGV))
    # IMF ICSD: investimento do governo geral / PIB, 8 paises, mesmo conceito
    rows = xl.ler(RAIZ / "invpub/bruto/IMFInvestmentandCapitalStockDataset2021.xlsx", "Dataset")
    h = next(rows)
    ix = {k: h.index(k) for k in ("isocode", "year", "igov_rppp", "GDP_rppp")}
    for r in rows:
        r = r + [""] * (len(h) - len(r))
        if r[ix["isocode"]] in PAISES and r[ix["igov_rppp"]] and r[ix["GDP_rppp"]]:
            v = float(r[ix["igov_rppp"]]) / float(r[ix["GDP_rppp"]]) * 100
            L.append(dict(indicador="cc_invpub_pib", fonte="IMF ICSD 2021", definicao_linha="investimento do governo geral (FBCF) / PIB, ambos em US$ internacionais constantes de 2017",
                          pais_ou_grupo=r[ix["isocode"]], ano=int(r[ix["year"]]), valor=fmt(v), unidade="% do PIB",
                          nota="calculado aqui: igov_rppp / GDP_rppp; conceito FBCF do governo geral, exclui empresas estatais; vai ate 2019" + ("; " + NOTA_VEN if r[ix["isocode"]] == "VEN" else ""),
                          vintage="IMF Investment and Capital Stock Dataset, edicao maio/2021, baixado 2026-10-19"))
    # PWT 10.01 e 11.0
    for arq, ver, base in [("pwt1001.xlsx", "PWT 10.01", "2017"), ("pwt110.xlsx", "PWT 11.0", "2021")]:
        rows = xl.ler(RAIZ / "pwt_maddison/bruto" / arq, "Data")
        h = next(rows)
        ix = {k: h.index(k) for k in ("countrycode", "year", "rtfpna", "rnna", "rgdpna", "rgdpo", "pop")}
        for r in rows:
            r = r + [""] * (len(h) - len(r))
            cc = r[ix["countrycode"]]
            if cc not in PAISES:
                continue
            ano = int(r[ix["year"]])
            vint = f"{ver} ({'publicado 2023-01-23' if ver.endswith('01') else 'publicado 2025-10-07'}), baixado 2026-10-19"
            if cc == "BRA":
                for col, ind, defin, un in [
                    ("rtfpna", "cc_ptf_pwt", f"PTF (produtividade total dos fatores) a precos nacionais constantes (legenda PWT: {base}=1)", f"indice ({base}=1)"),
                    ("rnna", "cc_estoque_capital_pwt", f"estoque de capital a precos nacionais constantes (legenda PWT: mil. {base}US$)", f"milhoes de US$ de {base}"),
                    ("rgdpna", "cc_pib_real_pwt", f"PIB real a precos nacionais constantes (legenda PWT: mil. {base}US$)", f"milhoes de US$ de {base}"),
                ]:
                    v = num(r[ix[col]])
                    if v is not None:
                        L.append(dict(indicador=ind, fonte=ver, definicao_linha=defin, pais_ou_grupo=cc, ano=ano, valor=fmt(v), unidade=un,
                                      nota=f"PWT coluna {col}; PTF e residuo estimado, nao observado", vintage=vint))
            v3, v2 = num(r[ix["rgdpna"]]), num(r[ix["pop"]])
            if v3 is not None and v2:
                L.append(dict(indicador="cc_pibpc_na_pwt", fonte=ver, definicao_linha=f"PIB real a precos nacionais constantes (rgdpna) por habitante, em US$ de {base} (crescimento coerente com as contas nacionais; nivel NAO comparavel entre paises)",
                              pais_ou_grupo=cc, ano=ano, valor=fmt(v3 / v2), unidade=f"US$ {base} a precos nacionais",
                              nota="rgdpna/pop; use so a variacao ao longo do tempo, nao o nivel entre paises" + ("; " + NOTA_VEN if cc == "VEN" else ""), vintage=vint))
            v1 = num(r[ix["rgdpo"]])
            if v1 is not None and v2:
                L.append(dict(indicador="cc_pibpc_pwt", fonte=ver, definicao_linha=f"PIB real do lado da producao (rgdpo) por habitante, US$ internacionais PPC de {base}",
                              pais_ou_grupo=cc, ano=ano, valor=fmt(v1 / v2), unidade=f"US$ intern. {base}",
                              nota="rgdpo/pop; comparavel entre paises" + ("; " + NOTA_VEN if cc == "VEN" else ""), vintage=vint))
    # Maddison 2023
    rows = xl.ler(RAIZ / "pwt_maddison/bruto/mpd2023_web.xlsx", "Full data")
    h = next(rows)
    ix = {k: h.index(k) for k in ("countrycode", "year", "gdppc")}
    for r in rows:
        r = r + [""] * (len(h) - len(r))
        if r[ix["countrycode"]] in PAISES and r[ix["gdppc"]] and int(r[ix["year"]]) >= 1900:
            L.append(dict(indicador="cc_pibpc_maddison", fonte="Maddison Project Database 2023", definicao_linha="PIB per capita em US$ de 2011 (PPC historica, gdppc)",
                          pais_ou_grupo=r[ix["countrycode"]], ano=int(r[ix["year"]]), valor=fmt(float(r[ix["gdppc"]])), unidade="US$ intern. 2011",
                          nota="serie historica reconstruida; ano-base de PPC 2011 (diferente de WDI/PWT)" + ("; " + NOTA_VEN if r[ix["countrycode"]] == "VEN" else ""),
                          vintage="Maddison Project Database 2023 (mpd2023_web.xlsx), baixado 2026-10-19"))
    ordem = {}
    for r in L:
        ordem.setdefault((r["indicador"], r["fonte"]), len(ordem))
    L.sort(key=lambda r: (ordem[(r["indicador"], r["fonte"])], r["pais_ou_grupo"], int(r["ano"])))
    return L


if __name__ == "__main__":
    print("mundo.csv", gravar(RAIZ / "series/mundo.csv", mundo()))
    print("termos_de_troca.csv", gravar(RAIZ / "series/termos_de_troca.csv", termos_de_troca()))
    print("crescimento_contexto.csv", gravar(RAIZ / "series/crescimento_contexto.csv", crescimento_contexto()))
