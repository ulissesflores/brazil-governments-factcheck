"""Gera mundo/quebras.csv (mesmas colunas das outras pastas). Sem rede. Os numeros vem de medidas_efeito.csv (rode medir.py antes);
os trechos citados foram conferidos nos brutos (docs/bruto, pwt_maddison/bruto, ipea/bruto, invpub/bruto, wdi_arquivo/bruto).
Rodar: python3 -I .../mundo/scripts/quebras.py
"""
import csv
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
import construir as cn  # noqa: E402
import medir  # noqa: E402

COLS = ["indicador", "serie", "data_quebra", "tipo_de_quebra", "metodo_antigo", "metodo_novo", "razao_declarada_pela_fonte", "fonte_primaria_url", "trecho_citado",
        "direcao_do_efeito", "como_a_direcao_foi_determinada", "efeito_medido", "como_medido", "apresentada_como_aprimoramento"]
MED = list(csv.DictReader(open(RAIZ / "medidas_efeito.csv")))
SEM = "sem sobreposicao"


def g(medida, alvo, trecho=""):
    for r in MED:
        if r["medida"] == medida and r["alvo"] == alvo and trecho in r["descricao"]:
            return r
    return None


def v(medida, alvo, trecho="", campo="valor", nd=2):
    r = g(medida, alvo, trecho)
    if r is None:
        return "n/d"
    x = r[campo]
    try:
        return f"{float(x):+.{nd}f}"
    except ValueError:
        return x


def nota_med(medida, alvo, trecho=""):
    r = g(medida, alvo, trecho)
    return r["nota"] if r else ""


def linha(**k):
    return {c: k.get(c, "") for c in COLS}


def pip_spells():
    """Uma linha por inicio de trecho comparavel (comparable_spell) do PIP, por pais, so em dados nacionais (e ARG urbano)."""
    out = []
    rows = list(csv.DictReader(open(RAIZ / "bruto/pip/pip_685_ppp2017.csv")))
    for c in cn.PAISES:
        rs = [r for r in rows if r["country_code"] == c and (r["reporting_level"] == "national" or c == "ARG")]
        rs.sort(key=lambda r: int(r["reporting_year"]))
        prev = None
        for r in rs:
            sp = (r["comparable_spell"], r["welfare_type"], r["survey_acronym"].split("-")[0])
            if prev is not None and r["comparable_spell"] != prev["comparable_spell"]:
                mudou = []
                if r["welfare_type"] != prev["welfare_type"]:
                    mudou.append(f"conceito de bem-estar {prev['welfare_type']} -> {r['welfare_type']}")
                if r["survey_acronym"] != prev["survey_acronym"]:
                    mudou.append(f"pesquisa {prev['survey_acronym']} -> {r['survey_acronym']}")
                out.append(linha(
                    indicador="mun_pobreza_685;mun_pobreza_830_ppc2021;mun_gini", serie=f"PIP {c} ({r['reporting_level']})", data_quebra=f"{r['reporting_year']}-01-01",
                    tipo_de_quebra="metodo_estatistico", metodo_antigo=f"trecho comparavel {prev['comparable_spell']} ({prev['survey_acronym']}, {prev['welfare_type']})",
                    metodo_novo=f"trecho comparavel {r['comparable_spell']} ({r['survey_acronym']}, {r['welfare_type']})",
                    razao_declarada_pela_fonte="o PIP separa as pesquisas em trechos nao comparaveis entre si (campo comparable_spell); nao declara efeito" + ("; mudou: " + "; ".join(mudou) if mudou else ""),
                    fonte_primaria_url="https://api.worldbank.org/pip/v1/pip?country=" + c + "&year=all&povline=6.85&ppp_version=2017&fill_gaps=false&format=csv (bruto/pip/pip_685_ppp2017.csv)",
                    trecho_citado=f"comparable_spell: '{prev['comparable_spell']}' -> '{r['comparable_spell']}'", direcao_do_efeito="desconhecida",
                    como_a_direcao_foi_determinada="nao ha ano coberto pelos dois trechos nos brutos baixados", efeito_medido=SEM,
                    como_medido="nenhum ano com as duas medidas; so vizinhanca descritiva em RESULTADO.md", apresentada_como_aprimoramento="nao_declarado"))
            prev = r
    return out


WDI_MAP = {"NY.GDP.MKTP.KD.ZG": "mun_pib_cresc", "SP.DYN.LE00.IN": "mun_expvida", "SP.DYN.IMRT.IN": "mun_mortinf", "VC.IHR.PSRC.P5": "mun_homic", "SH.IMM.IDPT": "mun_dtp3",
           "FP.CPI.TOTL.ZG": "mun_inflacao", "SL.UEM.TOTL.ZS": "mun_desemprego_oit", "TT.PRI.MRCH.XD.WD": "tt_wdi", "NE.GDI.FTOT.ZS": "cc_fbcf_pib"}


def rev_wdi_rows():
    out = []
    for ind, nome in WDI_MAP.items():
        for a_, b_, data in [("202403", "202507", "2025-07-01"), ("202507", "2026-10-08", "2026-10-08")]:
            rb = next((r for r in MED if r["medida"] == "revisao_wdi" and r["alvo"] == "BRA" and r["descricao"] == f"{ind}: {a_} -> {b_}"), None)
            ro = next((r for r in MED if r["medida"] == "revisao_wdi" and r["alvo"] == "demais 10 unidades" and r["descricao"] == f"{ind}: {a_} -> {b_}"), None)
            if not rb or not ro:
                continue
            if rb["valor"].startswith("0/") and ro["valor"].startswith("0/"):
                continue  # nada mudou nas 11 unidades: nao e quebra
            out.append(linha(
                indicador=nome, serie=f"WDI {ind}", data_quebra=data, tipo_de_quebra="revisao_de_vintage", metodo_antigo=f"WDI versao {a_}", metodo_novo=f"WDI versao {b_}",
                razao_declarada_pela_fonte="nao declarada: o WDI nao publica lista de revisoes por indicador nos arquivos baixados",
                fonte_primaria_url=f"https://api.worldbank.org/v2/sources/57/country/BRA/series/{ind}/version/{a_ if a_ != '2026-10-08' else ''} (bruto/wdi_arquivo/bruto/{ind}_v{a_}.json) e bruto/wdi/{ind}.json",
                trecho_citado="sem trecho: a mudanca aparece so na comparacao dos valores", direcao_do_efeito="desconhecida",
                como_a_direcao_foi_determinada="sinal nao agregado: ha anos que sobem e anos que descem", efeito_medido=f"BRA: {rb['valor']} valores comuns alterados ({rb['nota']}); demais 10 unidades: {ro['valor']} ({ro['nota']})",
                como_medido=f"sobreposicao: mesmos paises e anos em duas versoes do WDI (versao {a_} do arquivo e {b_} {'do arquivo' if b_ != '2026-10-08' else 'corrente baixada em 2026-10-19'})",
                apresentada_como_aprimoramento="nao_declarado"))
    return out


def classe_rows():
    saida, fy, cont, dados = medir.classes()
    n = {f_: c for f_, c in cont}
    out = []
    ind = "mun_pibpc_ppc;mun_pib_cresc;mun_expvida;mun_mortinf;mun_dtp3;mun_inflacao;mun_desemprego_oit;mun_homic;tt_wdi;cc_fbcf_pib"
    for c, (seq, trans) in saida.items():
        for i in range(1, len(fy)):
            if seq[i] != seq[i - 1]:
                ano_fim = int(fy[i][2:]) + (2000 if int(fy[i][2:]) < 50 else 1900)
                quote = ""
                if c == "ARG":
                    quote = "Due to the limitations of the Atlas method in classifying countries experiencing persistent high inflation, Argentina and Türkiye remain classified as upper-middle-income. (nota da pagina corrente, aplicada a classificacao atual)"
                out.append(linha(
                    indicador=ind, serie=f"classe de renda do Banco Mundial: {dados[c][0]} (agregado UMC do WDI)", data_quebra=f"{ano_fim - 1}-07-01", tipo_de_quebra="mudanca_de_regra",
                    metodo_antigo=f"{fy[i-1]}: classe {seq[i-1] or '(sem classe)'}", metodo_novo=f"{fy[i]}: classe {seq[i] or '(sem classe)'}",
                    razao_declarada_pela_fonte="as classificacoes sao definidas todo 1o de julho e ficam fixas no ano fiscal (nota da planilha OGHIST); os limites de renda sao reajustados todo ano",
                    fonte_primaria_url="https://datacatalogfiles.worldbank.org/ddh-published/0037712/DR0090754/OGHIST.xlsx (oghist/bruto/OGHIST.xlsx)",
                    trecho_citado=quote or "Income classifications are set each year on July 1 for all World Bank member economies, and all other economies with populations of more than 30,000.",
                    direcao_do_efeito="ambigua", como_a_direcao_foi_determinada="muda a composicao do agregado UMC (e do grupo de renda), sem sinal unico para cada indicador",
                    efeito_medido=f"numero de economias na classe UM (renda media alta) no OGHIST: {fy[i-1]}={n[fy[i-1]]} -> {fy[i]}={n[fy[i]]}; NAO foi verificado se o agregado UMC do WDI recalcula o passado com a classificacao corrente",
                    como_medido="contagem direta no OGHIST (todas as economias da planilha); nao reconstrui o agregado WDI sem o pais", apresentada_como_aprimoramento="nao_declarado"))
    return out


def principais():
    L = []
    P = "https://www.worldbank.org/en/news/press-release/2020/05/19/new-purchasing-power-parities-show-low-and-middle-income-economies-account-for-half-of-the-global-economy"
    base_label = ("rotulo de unidade do arquivo WDI diz 'constant 2011 international $' em TODAS as versoes (rotulo desatualizado, verificado em 8 versoes); "
                  "a troca de base foi identificada pelo salto de nivel entre versoes consecutivas (varredura de 54 versoes de 2018-11 a 2026-07) e pela data da divulgacao do ICP")
    r1 = lambda a: v("troca_ppc_wdi_2011_2017", a, "", "valor")
    L.append(linha(
        indicador="mun_pibpc_ppc", serie="WDI NY.GDP.PCAP.PP.KD", data_quebra="2020-05-01", tipo_de_quebra="metodo_estatistico",
        metodo_antigo="PIB per capita PPC em US$ internacionais constantes, base PPC 2011 (ICP 2011)", metodo_novo="base PPC 2017 (ICP 2017), versao 202005 do WDI",
        razao_declarada_pela_fonte="novos PPCs do ICP para o ano de referencia 2017; no release lido nao ha discussao do efeito sobre as series de PIB per capita do WDI",
        fonte_primaria_url=P + " (docs/bruto/wb_press_icp2017_2020-05-19.html)",
        trecho_citado="WASHINGTON, May 19, 2020 — New purchasing power parities (PPPs) for reference year 2017 that adjust for differences in the cost of living across economies were released today by the International Comparison Program (ICP).",
        direcao_do_efeito="eleva", como_a_direcao_foi_determinada=base_label + "; sinal do nivel do Brasil: razao v202005/v202004 > 1 em todos os 29 anos comuns",
        efeito_medido=(f"nivel do PIB pc, variacao % mediana 1990-2018: BRA {r1('BRA')}, ARG {r1('ARG')}, CHL {r1('CHL')}, COL {r1('COL')}, MEX {r1('MEX')}, PER {r1('PER')}, URY {r1('URY')}, WLD {r1('WLD')}, LCN {r1('LCN')}, UMC {r1('UMC')}; "
                       f"razao Brasil/referencia, variacao % mediana: BRA/ARG {v('troca_ppc_wdi_2011_2017','BRA/ARG')}, BRA/CHL {v('troca_ppc_wdi_2011_2017','BRA/CHL')}, BRA/COL {v('troca_ppc_wdi_2011_2017','BRA/COL')}, BRA/MEX {v('troca_ppc_wdi_2011_2017','BRA/MEX')}, "
                       f"BRA/PER {v('troca_ppc_wdi_2011_2017','BRA/PER')}, BRA/URY {v('troca_ppc_wdi_2011_2017','BRA/URY')}, BRA/WLD {v('troca_ppc_wdi_2011_2017','BRA/WLD')}, BRA/LCN {v('troca_ppc_wdi_2011_2017','BRA/LCN')}, BRA/UMC {v('troca_ppc_wdi_2011_2017','BRA/UMC')}; "
                       "para cada pais o fator e praticamente o mesmo em todos os anos: muda o nivel e a razao entre paises, nao as taxas de crescimento do pais"),
        como_medido="sobreposicao: 11 unidades x 29 anos (1990-2018) em duas versoes do arquivo WDI (fonte 57) baixadas em 2026-10-19: 202004 (antes) e 202005 (depois)",
        apresentada_como_aprimoramento="nao_declarado"))
    r2 = lambda a: v("troca_ppc_wdi_2017_2021", a, "", "valor")
    L.append(linha(
        indicador="mun_pibpc_ppc", serie="WDI NY.GDP.PCAP.PP.KD", data_quebra="2024-05-01", tipo_de_quebra="metodo_estatistico",
        metodo_antigo="base PPC 2017 (versao 202403 do WDI)", metodo_novo="base PPC 2021 (ICP 2021), versao 202405 do WDI; o WDI corrente rotula 'constant 2021 international $'",
        razao_declarada_pela_fonte="resultados do ciclo ICP 2021 divulgados em 30/05/2024, com dados revisados de 2017 e extrapolacao de PPCs para 2022-23",
        fonte_primaria_url="https://www.worldbank.org/en/programs/icp/data (docs/bruto/wb_icp_data.html) e https://www.stats.gov.cn/english/PressRelease/202406/t20240603_1954216.html (docs/bruto/stats_cn_icp2021.html)",
        trecho_citado="Results from the International Comparison Program (ICP) 2021 cycle include data for the reference year 2021, revised data for the reference year 2017, purchasing power parity (PPP) time series for 2018 to 2020, and extrapolated GDP PPPs for 2022 and 2023.",
        direcao_do_efeito="eleva", como_a_direcao_foi_determinada=base_label + "; sinal do nivel do Brasil: razao v202405/v202403 > 1 em todos os 33 anos comuns",
        efeito_medido=(f"nivel do PIB pc, variacao % mediana 1990-2022: BRA {r2('BRA')}, ARG {r2('ARG')}, CHL {r2('CHL')}, COL {r2('COL')}, MEX {r2('MEX')}, PER {r2('PER')}, URY {r2('URY')}, WLD {r2('WLD')}, LCN {r2('LCN')}, UMC {r2('UMC')}; "
                       f"razao Brasil/referencia, variacao % mediana: BRA/ARG {v('troca_ppc_wdi_2017_2021','BRA/ARG')}, BRA/CHL {v('troca_ppc_wdi_2017_2021','BRA/CHL')}, BRA/COL {v('troca_ppc_wdi_2017_2021','BRA/COL')}, BRA/MEX {v('troca_ppc_wdi_2017_2021','BRA/MEX')}, "
                       f"BRA/PER {v('troca_ppc_wdi_2017_2021','BRA/PER')}, BRA/URY {v('troca_ppc_wdi_2017_2021','BRA/URY')}, BRA/WLD {v('troca_ppc_wdi_2017_2021','BRA/WLD')}, BRA/LCN {v('troca_ppc_wdi_2017_2021','BRA/LCN')}, BRA/UMC {v('troca_ppc_wdi_2017_2021','BRA/UMC')}; "
                       "fator por pais praticamente constante nos anos: as taxas de crescimento do pais ficam, o nivel e a ordem entre paises mudam"),
        como_medido="sobreposicao: 11 unidades x 33 anos (1990-2022) em duas versoes do arquivo WDI baixadas em 2026-10-19: 202403 (antes) e 202405 (depois)", apresentada_como_aprimoramento="nao_declarado"))
    L.append(linha(
        indicador="mun_pibpc_ppc", serie="WDI NY.GDP.PCAP.PP.KD", data_quebra="2024-12-01", tipo_de_quebra="revisao_de_vintage",
        metodo_antigo="WDI versao 202405 (PPC 2021, contas nacionais da epoca)", metodo_novo="WDI versao 202412 (mesma base PPC 2021; contas nacionais revisadas)",
        razao_declarada_pela_fonte="nao declarada nos arquivos baixados", fonte_primaria_url="bruto/wdi_arquivo/bruto/NY.GDP.PCAP.PP.KD_v202405.json e _v202412.json",
        trecho_citado="sem trecho: mudanca vista so na comparacao dos valores", direcao_do_efeito="eleva", como_a_direcao_foi_determinada="razao v202412/v202405 > 1 em todos os anos comuns para o Brasil",
        efeito_medido=f"BRA {v('revisao_wdi_apos_2021','BRA')}% (mediana; {nota_med('revisao_wdi_apos_2021','BRA')}); LCN {v('revisao_wdi_apos_2021','LCN')}%; razao BRA/LCN {v('revisao_wdi_apos_2021','BRA/LCN')}%",
        como_medido="sobreposicao 11 unidades x 33 anos em duas versoes do arquivo WDI", apresentada_como_aprimoramento="nao_declarado"))
    # PIP: troca de linha/PPC
    pb = lambda a: v("troca_ppc_pip", a, "pobreza: linha 8,30", "valor")
    L.append(linha(
        indicador="mun_pobreza_685;mun_pobreza_830_ppc2021", serie="PIP linha de pobreza US$ 6,85 (PPC 2017) -> US$ 8,30 (PPC 2021)", data_quebra="2025-06-05", tipo_de_quebra="metodo_estatistico",
        metodo_antigo="linha de US$ 6,85/dia em precos internacionais de 2017", metodo_novo="linha de US$ 8,30/dia em precos internacionais de 2021",
        razao_declarada_pela_fonte="atualizacao das linhas com PPC 2021; a metodologia para escolher as linhas nao mudou",
        fonte_primaria_url="https://blogs.worldbank.org/en/opendata/the-world-bank-s-new-global-poverty-lines-in-2021-prices (docs/bruto/wb_blog_new_poverty_lines_2021_prices.html)",
        trecho_citado="from $6.85 (in 2017 prices) to $8.30 (in 2021 prices) in the case of upper-middle-income countries. [...] While there have been updates to the underlying data, the Bank’s methodology for setting its poverty lines has remained unchanged.",
        direcao_do_efeito="eleva", como_a_direcao_foi_determinada="diferenca de medianas (8,30/2021 menos 6,85/2017) positiva para todos os paises exceto URY (-0,11 pp)",
        efeito_medido=(f"pontos percentuais, mediana dos anos com dado, headcount(8,30/2021) menos headcount(6,85/2017), release 20260922: BRA {pb('BRA')}, ARG {pb('ARG')}, CHL {pb('CHL')}, COL {pb('COL')}, MEX {pb('MEX')}, PER {pb('PER')}, URY {pb('URY')}, VEN {pb('VEN')}; "
                       "efeito sobre (Brasil menos referencia), pp: " + ", ".join(f"BRA-{r} {v('troca_ppc_pip', 'BRA-' + r, 'efeito da troca')}" for r in ["ARG", "CHL", "COL", "MEX", "PER", "URY", "VEN"])),
        como_medido="sobreposicao: mesmo release do PIB (20260922), dois PPCs, anos de pesquisa em comum; os arquivos pip_685_ppp2017.csv e pip_830_ppp2021.csv. O pre-registro fixa 6,85/2017 como primaria; 8,30/2021 e sensibilidade", apresentada_como_aprimoramento="sim"))
    pr = lambda m, c, t="pobreza 6,85": (g("revisao_pip", c, f"{t}: release 20260922 vs {m}") or {}).get("valor", "n/d")
    L.append(linha(
        indicador="mun_pobreza_685;mun_gini", serie="PIP release 20250930 -> 20260324 -> 20260922 (PPC 2017)", data_quebra="2026-09-22", tipo_de_quebra="revisao_de_vintage",
        metodo_antigo="PIP release 20250930", metodo_novo="PIP release 20260922", razao_declarada_pela_fonte="nao declarada nos arquivos baixados",
        fonte_primaria_url="https://api.worldbank.org/pip/v1/versions (bruto/pip/_versions.json); bruto/pip/pip_685_ppp2017_rel20250930.csv, _rel20260324.csv, _rel20260922.csv",
        trecho_citado="sem trecho: mudanca vista so na comparacao dos valores", direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="sinal nao agregado",
        efeito_medido=(f"pobreza 6,85: maior diferenca absoluta BRA {pr('20250930','BRA')} pp ({nota_med('revisao_pip','BRA','pobreza: release 20260922 vs 20250930')}); ARG {pr('20250930','ARG')}; VEN {pr('20250930','VEN')}; "
                       f"Gini BRA {pr('20250930','BRA','Gini')} pontos; 20260324 vs 20260922: diferenca maxima {pr('20260324','BRA')} (BRA), nenhum valor alterado. Releases 20250401 e 20240627 devolveram HTTP 500 do servidor em 2026-10-19 e nao foram comparados"),
        como_medido="sobreposicao nos mesmos paises e anos de pesquisa em tres releases baixados", apresentada_como_aprimoramento="nao_declarado"))
    # PWT
    L.append(linha(
        indicador="cc_pibpc_pwt;cc_pibpc_na_pwt;cc_pib_real_pwt;cc_estoque_capital_pwt;cc_ptf_pwt", serie="Penn World Table 10.0 -> 10.01", data_quebra="2023-01-23", tipo_de_quebra="revisao_de_vintage",
        metodo_antigo="PWT 10.0 (publicado 2021-01-15)", metodo_novo="PWT 10.01 (publicado 2023-01-23)",
        razao_declarada_pela_fonte="atualizacao menor; muda parte do calculo dos precos de investimento, com impacto principal no crescimento do capital",
        fonte_primaria_url="https://www.rug.nl/ggdc/productivity/pwt/news (pwt_maddison/bruto/pwt_news.html)",
        trecho_citado="We have released a minor update of the Penn World Table, version 10.01. This update changes part of the calculation of investment prices and most notably impact capital growth.",
        direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="PWT 10.0 nao foi baixado", efeito_medido=SEM, como_medido="nenhum ano com as duas versoes nos brutos; o estoque de capital e a PTF aqui sao da 10.01", apresentada_como_aprimoramento="nao_declarado"))
    pw = lambda a: v("versao_pwt", a, "PIB pc (rgdpo/pop)", "valor")
    g1 = g("versao_pwt", "BRA", "Lula1-2"); g2 = g("versao_pwt", "BRA", "Dilma"); k1 = g("versao_pwt", "BRA", "rnna"); k2 = g("versao_pwt", "BRA", "rtfpna")
    L.append(linha(
        indicador="cc_pibpc_pwt;cc_pibpc_na_pwt;cc_pib_real_pwt;cc_estoque_capital_pwt;cc_ptf_pwt", serie="Penn World Table 10.01 -> 11.0", data_quebra="2025-10-07", tipo_de_quebra="metodo_estatistico",
        metodo_antigo="PWT 10.01: ano de referencia 2017, PPC do ICP 2017, contas nacionais ate 2019", metodo_novo="PWT 11.0: ano de referencia 2021, PPC do ICP 2021, contas nacionais revisadas ate 2023",
        razao_declarada_pela_fonte="novos PPCs do ICP 2021, contas nacionais revisadas e estendidas, mudancas de fonte e de escolha",
        fonte_primaria_url="https://dataverse.nl/api/access/datafile/554031 (pwt_maddison/bruto/pwt110_whatsnew.pdf)",
        trecho_citado="The changes fall into three broad categories, namely: I) the incorporation of new purchasing power parities (PPPs) data for the years 2017 to 2021; II) the incorporation of revised and extended National Accounts data, covering the period up to 2023; III) changes to data sources and choices.",
        direcao_do_efeito="eleva", como_a_direcao_foi_determinada="mediana da razao PIB pc (11.0 / 10.01) positiva para BRA e para as 7 referencias",
        efeito_medido=(f"PIB pc rgdpo/pop, variacao % mediana do nivel 1950-2019: BRA {pw('BRA')}, ARG {pw('ARG')}, CHL {pw('CHL')}, COL {pw('COL')}, MEX {pw('MEX')}, PER {pw('PER')}, URY {pw('URY')}; razao BRA/ref: " +
                       ", ".join(f"BRA/{r} {v('versao_pwt','BRA/'+r,'razao BRA/ref')}" for r in ["ARG", "CHL", "COL", "MEX", "PER", "URY", "VEN"]) +
                       (f"; crescimento medio anual do PIB pc de BRA (rgdpo/pop) Lula 1-2: {g1['valor']}; Dilma: {g2['valor']} (pp/ano); variacao acumulada 2002->2010: estoque de capital {k1['valor']}, PTF {k2['valor']} (%) [10.01 / 11.0]" if g1 and g2 and k1 and k2 else "")),
        como_medido="sobreposicao: 1950-2019, as duas versoes xlsx baixadas em 2026-10-19 (rgdpo, pop, rnna, rtfpna)", apresentada_como_aprimoramento="sim"))
    # Maddison
    fc = lambda f_, y: (g("fontes_cruzadas", f_, f"em {y}") or {}).get("valor", "-")
    L.append(linha(
        indicador="cc_pibpc_maddison", serie="Maddison Project Database 2023 vs PWT 10.01 / PWT 11.0 / WDI", data_quebra="2023-01-01", tipo_de_quebra="metodo_estatistico",
        metodo_antigo="PWT 10.01 (PPC 2017), PWT 11.0 e WDI (PPC 2021)", metodo_novo="Maddison 2023: US$ internacionais de 2011 (PPC 2011), serie reconstruida",
        razao_declarada_pela_fonte="o MPD 2023 usa PPC de 2011 (planilha GDPpc: 'GDP pc 2011 prices'); o mes do release nao foi verificado (data_quebra = ano)",
        fonte_primaria_url="https://dataverse.nl/api/access/datafile/421302 (pwt_maddison/bruto/mpd2023_web.xlsx, aba GDPpc, celula A1)", trecho_citado="GDP pc 2011 prices",
        direcao_do_efeito="ambigua", como_a_direcao_foi_determinada="comparacao entre FONTES diferentes, nao revisao da mesma fonte",
        efeito_medido="razao Brasil / mediana de ARG,CHL,COL,MEX,PER,URY (Maddison / PWT 10.01 / PWT 11.0 / WDI): " + "; ".join(
            f"{y}: {fc('Maddison 2023 (PPC 2011)', y)} / {fc('PWT 10.01 (PPC 2017)', y)} / {fc('PWT 11.0 (PPC 2021)', y)} / {fc('WDI corrente (PPC 2021)', y)}" for y in (1980, 1990, 2002, 2010, 2016, 2019)),
        como_medido="comparacao direta das 4 fontes nos anos comuns (nao e sobreposicao de duas versoes da mesma serie); VEN fora da mediana por falta de cobertura em PWT/WDI", apresentada_como_aprimoramento="nao_declarado"))
    # termos de troca
    f_ = lambda a: (g("encadeamento_tt", "BRA", a) or {}).get("valor", "n/d")
    L.append(linha(
        indicador="tt_funcex", serie="Ipeadata FUNCEX_TTR", data_quebra="1974-01-01", tipo_de_quebra="metodo_estatistico",
        metodo_antigo="1879-1973: IBGE Estatisticas Historicas do Brasil (ajustado conforme Estatisticas do Seculo XX)", metodo_novo="de 1974: dados da Funcex, serie encadeada",
        razao_declarada_pela_fonte="serie composta: duas fontes encadeadas em 1973/1974",
        fonte_primaria_url="http://www.ipeadata.gov.br/api/odata4/Metadados('FUNCEX_TTR') (ipea/bruto/ipea_meta_FUNCEX_TTR.json)",
        trecho_citado="Para 1879-1973, Estatísticas históricas do Brasil: séries econômicas, demográficas e sociais de 1550 a 1988. [...] A partir de 1974, dados da Funcex. Nota: Até 1973, série encadeada e convertida para a base 2006=100.",
        direcao_do_efeito="reduz", como_a_direcao_foi_determinada="razao FUNCEX_TTR/HIST_TROCA cai em 1974 em relacao ao nivel constante de 1901-1973",
        efeito_medido=(f"razao FUNCEX_TTR / HIST_TROCA (HIST_TROCA = IBGE puro, inativa, ate 1975): constante ate 1973 (desvio maximo 0,00%); em 1974 desvio {f_('desvio % da razao FUNCEX_TTR/HIST_TROCA em 1974')}%, em 1975 {f_('desvio % da razao FUNCEX_TTR/HIST_TROCA em 1975')}%; "
                       f"variacao 1973->1974: {f_('variacao % do indice em 1974')} (FUNCEX / HIST). ATENCAO: o nome da serie diz 'media 2018 = 100' e a nota diz 'base 2006=100': incoerencia na propria fonte"),
        como_medido="sobreposicao 1901-1975 entre FUNCEX_TTR e HIST_TROCA (mesma origem IBGE ate 1973), ambos baixados em 2026-10-19", apresentada_como_aprimoramento="nao_declarado"))
    # FGV / investimento publico
    ifgv = lambda a, b, ch: (next((r for r in MED if r["medida"] == "revisao_fgv" and f"vintage {a} -> {b}" in r["descricao"] and ch in r["descricao"]), None) or {})
    for ano, ind, ant, novo, quote in [
        ("1995", "cc_invpub_pib;cc_fbcf_pib", "IBGE Estatisticas do Seculo XX (1947-1994)", "IBGE Contas Nacionais Trimestrais; investimento publico de Gobetti (2006) e Orair (2016)",
         "As informações de investimentos públicos a partir de 1995 são de Gobetti (2006) e Orair (2016). Para detalhes metodológicos, ver o apêndice de Orair (2016)."),
        ("2011", "cc_invpub_pib", "Gobetti (2006) / Orair (2016)", "Tesouro Nacional, conceito 'aquisicao de ativos nao financeiros'",
         "A partir de 2011, Secretaria do Tesouro Nacional, disponível em: https://www.tesourotransparente.gov.br/publicacoes/boletim-trimestral-de-estatisticas-fiscais-do-governo-geral/2020/25. Utiliza-se o conceito de \"aquisição de ativos não financeiros\""),
        ("2015", "cc_invpub_pib", "estatais federais: fonte anterior", "estatais federais: Boletim de Investimentos SEST/ME",
         "As informações das empresas estatais a partir de 2015 foram compiladas a partir do Boletim de Investimentos, publicados pelo SEST/ME")]:
        L.append(linha(
            indicador=ind, serie="FGV IBRE Observatorio de Politica Fiscal, investimentos publicos 1947-2025", data_quebra=f"{ano}-01-01", tipo_de_quebra="metodo_estatistico", metodo_antigo=ant, metodo_novo=novo,
            razao_declarada_pela_fonte="a aba 'Comentarios' lista as fontes por periodo; nao declara efeito da troca",
            fonte_primaria_url="https://observatorio-politica-fiscal.ibre.fgv.br/series-historicas/investimentos-publicos/investimentos-publicos-serie-historica-1947-2025 (invpub/bruto/fgv_investimentos_publicos_1947-2025.xlsx, aba Comentarios)",
            trecho_citado=quote, direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="fontes primarias antigas e novas nao se sobrepoem nos brutos",
            efeito_medido=SEM + ("; nota: ICSD (FBCF do governo geral) menos FGV (governo geral), anos comuns 1960-2019: " + (g("conceito_invpub", "BRA") or {}).get("valor", "n/d") + " pp [mediana / min / max]" if ano == "1995" else ""),
            como_medido="nenhum ano com as duas fontes; a comparacao ICSD x FGV e entre conceitos, nao medida do efeito da troca", apresentada_como_aprimoramento="nao_declarado"))
    for a, b, d in [(2023, 2024, "2025-04-22"), (2024, 2025, "2026-04-10")]:
        rs, rf = ifgv(a, b, "setor publico"), ifgv(a, b, "FBCF")
        L.append(linha(
            indicador="cc_invpub_pib;cc_fbcf_pib", serie=f"FGV IBRE investimentos publicos: vintage {a} -> {b}", data_quebra=d, tipo_de_quebra="revisao_de_vintage", metodo_antigo=f"planilha 1947-{a}", metodo_novo=f"planilha 1947-{b}",
            razao_declarada_pela_fonte="a pagina da serie descreve a atualizacao e diz que os dados diferem um pouco dos de Borca Jr. por conceito (nota [1]); nao lista revisoes por ano",
            fonte_primaria_url=f"https://observatorio-politica-fiscal.ibre.fgv.br/series-historicas/investimentos-publicos (invpub/bruto/fgv_investimentos_publicos_1947-{a}.xlsx e -{b}.xlsx)",
            trecho_citado="Os dados aqui apresentados diferem um pouco dos dados analisados por Borça Jr", direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="poucos anos alterados, sem sinal unico",
            efeito_medido=f"investimento do setor publico: {rs.get('valor','n/d')} anos alterados, {rs.get('nota','')}; FBCF: {rf.get('valor','n/d')}, {rf.get('nota','')}",
            como_medido="sobreposicao dos anos 1947-2023 (ou 2024) entre duas planilhas baixadas em 2026-10-19", apresentada_como_aprimoramento="nao_declarado"))
    fb = g("fbcf_fontes", "BRA", "SCN10")
    L.append(linha(
        indicador="cc_fbcf_pib", serie="FBCF % do PIB (FGV/IBGE) e Ipeadata SCN10 / PAN_FBKFPIBV", data_quebra="1995-01-01", tipo_de_quebra="metodo_estatistico",
        metodo_antigo="IBGE Estatisticas do Seculo XX (contas nacionais consolidadas, 1947-1994)", metodo_novo="IBGE Contas Nacionais Trimestrais (1995+)",
        razao_declarada_pela_fonte="a aba 'Comentarios' da planilha FGV lista a fonte por periodo; sem efeito declarado",
        fonte_primaria_url="invpub/bruto/fgv_investimentos_publicos_1947-2025.xlsx, aba Comentarios",
        trecho_citado="As informações da FBCF e do PIB no período 1947-1994 são das tabelas históricas das contas nacionais na publicação estatísticas do Século XX do IBGE.",
        direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="sem ano coberto pelas duas fontes na planilha FGV",
        efeito_medido=("Ipeadata PAN_FBKFPIBV menos FGV 1996-2025: " + (g("fbcf_fontes", "BRA", "PAN_FBKFPIBV") or {}).get("valor", "n/d") + " pp [mediana / min / max]; WDI menos FGV 1970-2025: " + (g("fbcf_fontes", "BRA", "WDI") or {}).get("valor", "n/d") +
                       ((" ; Ipeadata SCN10 (FBKF/PIB nominais) menos FGV: " + fb["valor"] + " pp, " + fb["nota"]) if fb else "")),
        como_medido="comparacao entre FGV e outras series do IBGE nos anos em que ambas existem; o efeito da troca de 1994 para 1995 em si nao tem ano duplo", apresentada_como_aprimoramento="nao_declarado"))
    # homicidios
    L.append(linha(
        indicador="mun_homic", serie="UNODC via WDI VC.IHR.PSRC.P5 (Brasil: SIM/DATASUS)", data_quebra="1996-01-01", tipo_de_quebra="mudanca_de_regra", metodo_antigo="CID-9", metodo_novo="CID-10",
        razao_declarada_pela_fonte="ver dominios-2/quebras.csv (seg_homic_taxa, 1996-01-01): adocao da CID-10; sem lista de compatibilizacao",
        fonte_primaria_url="http://tabnet.datasus.gov.br/cgi/sim/Mortalidade_Geral_1996_2012.pdf (copia em dominios-2/seguranca/bruto)",
        trecho_citado="Devido às diferenças entre as revisões, não foi possível gerar uma lista que as compatibilizasse. (citado de dominios-2/quebras.csv, nao relido aqui)",
        direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="remete a dominios-2", efeito_medido=SEM, como_medido="nao refeito nesta pasta; a serie WDI do Brasil comeca em 1990 e atravessa 1996", apresentada_como_aprimoramento="nao_declarado"))
    return L


def main():
    L = principais() + pip_spells() + rev_wdi_rows() + classe_rows()
    L.sort(key=lambda r: (r["tipo_de_quebra"], r["indicador"], r["data_quebra"]))
    with (RAIZ / "quebras.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(L)
    print("quebras.csv", len(L))


if __name__ == "__main__":
    main()
