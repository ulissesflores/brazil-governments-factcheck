"""Gera mundo/RESULTADO.md a partir dos CSVs ja construidos (sem rede). Rodar por ultimo:
python3 -I .../mundo/scripts/resultado.py
Descricao apenas: sem causalidade, sem nota, sem ranking de merito.
"""
import csv
import math
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
import janelas as jn  # noqa: E402

CHAIN = "/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py"
REFS7 = ["ARG", "CHL", "COL", "MEX", "PER", "URY", "VEN"]
GOVS = jn.governos()
ANO_GOV = {a: jn.governo_do_ano(GOVS, a) for a in range(1940, 2030)}
JAN = list(csv.DictReader(open(RAIZ / "janelas.csv")))
MED = list(csv.DictReader(open(RAIZ / "medidas_efeito.csv")))
QUE = list(csv.DictReader(open(RAIZ / "quebras.csv")))


def serie(arq, ind, fonte_ini="", unid="BRA"):
    out = {}
    for r in csv.DictReader(open(RAIZ / f"series/{arq}.csv")):
        if r["indicador"] == ind and r["pais_ou_grupo"] == unid and r["fonte"].startswith(fonte_ini):
            out[int(r["ano"])] = float(r["valor"])
    return out


def anos_gov(g):
    return sorted(a for a, x in ANO_GOV.items() if x == g)


def media(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else None


def pearson(x, y):
    n = len(x)
    if n < 3:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return None if sx == 0 or sy == 0 else sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def ols(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    a = my - b * mx
    r = pearson(x, y)
    return a, b, r * r, n


def fx(x, nd=2, sinal=False):
    if x is None:
        return "-"
    return f"{x:+.{nd}f}" if sinal else f"{x:.{nd}f}"


def tabela(cab, linhas):
    s = "| " + " | ".join(cab) + " |\n|" + "|".join("---" for _ in cab) + "|\n"
    for l in linhas:
        s += "| " + " | ".join(str(c).replace("|", "/") for c in l) + " |\n"
    return s


def brasil_serie(ind):
    for arq in ("mundo", "termos_de_troca", "crescimento_contexto"):
        out = {}
        for r in csv.DictReader(open(RAIZ / f"series/{arq}.csv")):
            if r["indicador"] == ind.replace("_var_pct", "") and r["pais_ou_grupo"] == "BRA":
                out[int(r["ano"])] = float(r["valor"])
        if out:
            return var(out) if ind.endswith("_var_pct") else out
    return {}


def var(s):
    return {a: (v / s[a - 1] - 1) * 100 for a, v in s.items() if a - 1 in s and s[a - 1]}


def jan(ind, gov, ref, campo="media_brasil", fonte=""):
    for r in JAN:
        if r["indicador"] == ind and r["governo"] == gov and r["referencia"] == ref and r["fonte"].startswith(fonte):
            return r[campo]
    return ""


# ------------------------------------------------------------------ dados
cresc_bra = serie("mundo", "mun_pib_cresc")
cresc_lcn = serie("mundo", "mun_pib_cresc", unid="LCN")
cresc_umc = serie("mundo", "mun_pib_cresc", unid="UMC")
cresc_wld = serie("mundo", "mun_pib_cresc", unid="WLD")
cresc7 = {u: serie("mundo", "mun_pib_cresc", unid=u) for u in REFS7}
cresc_m7 = {a: media(cresc7[u][a] for u in REFS7 if a in cresc7[u]) for a in cresc_bra if all(a in cresc7[u] for u in REFS7)}
tt_fx = serie("termos_de_troca", "tt_funcex")
tt_fx_var = var(tt_fx)
tt_wdi = serie("termos_de_troca", "tt_wdi_arq")
tt_wdi_var = var(tt_wdi)


def janela_stats(g, nome):
    anos = [a for a in anos_gov(g)]
    comuns = [a for a in anos if a in cresc_bra and a in cresc_lcn]
    b = [cresc_bra[a] for a in comuns]
    l = [cresc_lcn[a] for a in comuns]
    m7 = [a for a in anos if a in cresc_bra and a in cresc_m7]
    b7 = [cresc_bra[a] for a in m7]
    s7 = [cresc_m7[a] for a in m7]
    tt = [a for a in anos if a in cresc_bra and a in tt_fx_var]
    ttb = [cresc_bra[a] for a in tt]
    ttv = [tt_fx_var[a] for a in tt]
    ini, fim = min(anos) - 1, max(anos)
    ttw = [a for a in anos if a in tt_wdi_var and a in cresc_bra]
    def mudou(d):
        if ini in d and fim in d:
            return (d[fim] / d[ini] - 1) * 100
        return None

    def mudou_disp(d):
        ys = [a for a in anos if a in d]
        if not ys:
            return None, None
        a0 = ini if ini in d else min(ys)
        return (d[max(ys)] / d[a0] - 1) * 100, f"{a0}-{max(ys)}"
    # concordancia de direcao da mudanca da taxa de crescimento ano a ano
    conc = tot = 0
    for a in comuns:
        if a - 1 in cresc_bra and a - 1 in cresc_lcn:
            tot += 1
            conc += ((cresc_bra[a] - cresc_bra[a - 1]) > 0) == ((cresc_lcn[a] - cresc_lcn[a - 1]) > 0)
    return dict(nome=nome, anos=(f"{min(comuns)}-{max(comuns)}" if comuns else "-"), n=len(comuns), mb=media(b), ml=media(l), dif=(media(b) - media(l)) if b else None,
                r_lcn=pearson(b, l), m7b=media(b7), m7=media(s7), r_m7=pearson(b7, s7), n7=len(m7), r_tt=pearson(ttb, ttv), n_tt=len(tt),
                tt_mudou=mudou(tt_fx), tt_wdi_mudou=mudou_disp(tt_wdi)[0], tt_wdi_per=mudou_disp(tt_wdi)[1], tt_media=media(ttv), conc=conc, tot=tot,
                tt_wdi_n=len(ttw), tt_wdi_r=pearson([cresc_bra[a] for a in ttw], [tt_wdi_var[a] for a in ttw]))


def dias_ano(ano):
    import datetime as dt
    ini, fim = dt.date(ano, 1, 1), dt.date(ano + 1, 1, 1)
    return {g: (min(sd, fim) - max(p, ini)).days for g, p, sd in GOVS if (min(sd, fim) - max(p, ini)).days > 0}


def main():
    L = []
    w = L.append
    # relacao historica (todos os anos com os dois lados)
    anos_h = sorted(a for a in cresc_bra if a in cresc_lcn and a in cresc_m7)
    a_l, b_l, r2_l, n_l = ols([cresc_lcn[a] for a in anos_h], [cresc_bra[a] for a in anos_h])
    a_7, b_7, r2_7, n_7 = ols([cresc_m7[a] for a in anos_h], [cresc_bra[a] for a in anos_h])
    anos_t = sorted(a for a in cresc_bra if a in tt_fx_var)
    r_tt_h = pearson([cresc_bra[a] for a in anos_t], [tt_fx_var[a] for a in anos_t])
    stats = {g: janela_stats(g, n) for g, n in [("lula12", "Lula 1-2"), ("dilma", "Dilma")]}
    todos = [janela_stats(gid, gid) for gid, _, _ in GOVS if len([a for a in anos_gov(gid) if a in cresc_bra]) >= 3]

    w("# Mundo: referencias internacionais, termos de troca e contexto de crescimento\n")
    w("Dossie governos-do-brasil-economia. Coleta em 2026-10-19. Pre-registro: `preregistro/PREREGISTRATION-EMENDA-01.md`, secao A e secao B (linha 'Growth context'). So descricao: sem causalidade, sem nota, sem ranking de merito.\n")
    w("Reproduzir (sem rede; confere o bruto contra o manifest antes): `python3 -I .../mundo/scripts/construir.py`, depois `medir.py`, `quebras.py`, `janelas.py`, `resultado.py`. Aquisicao (COM rede, nao rode por acaso): `scripts/baixar_*.sh` (um por cadeia de hash).\n")

    # ------------------------------------------------ 0
    w("## 0. Achado e NAO achado\n")
    s1, s2 = stats["lula12"], stats["dilma"]
    w("**Achado (descricao):**\n")
    w(f"1. Crescimento real do PIB, anos com dado nos dois lados. Lula 1-2 ({s1['anos']}): Brasil {fx(s1['mb'])} % a.a., America Latina e Caribe (LCN) {fx(s1['ml'])}, diferenca {fx(s1['dif'],2,True)} pp. Dilma ({s2['anos']}): Brasil {fx(s2['mb'])}, LCN {fx(s2['ml'])}, diferenca {fx(s2['dif'],2,True)} pp. A LCN inclui o proprio Brasil (peso grande no agregado): a media simples dos 7 paises sem o Brasil esta na secao 4.")
    w(f"2. Coincidencia de direcao, sem causalidade: na janela Lula 1-2 a correlacao anual entre o crescimento do Brasil e o da LCN e {fx(s1['r_lcn'])} (n={s1['n']}); na janela Dilma, {fx(s2['r_lcn'])} (n={s2['n']}). Com n tao pequeno, o intervalo e largo; o numero descreve a janela, nao estima uma lei.")
    w(f"3. Termos de troca do Brasil (Funcex via Ipeadata, indice com base 2018=100): variacao do indice do ano anterior ao governo ate o ultimo ano do governo: Lula 1-2 {fx(s1['tt_mudou'],1,True)} %, Dilma {fx(s2['tt_mudou'],1,True)} %. Pela WDI/UNCTAD (versao 202507 do arquivo do WDI, 1980-2023; o WDI corrente de 2026-10-08 so traz o Brasil de 2005 em diante, ou seja, a fonte encurtou a serie em 25 anos): Lula 1-2 {fx(s1['tt_wdi_mudou'],1,True)} % ({s1['tt_wdi_per']}), Dilma {fx(s2['tt_wdi_mudou'],1,True)} % ({s2['tt_wdi_per']}). Variacao anual media (Funcex): Lula 1-2 {fx(s1['tt_media'],2,True)} % a.a., Dilma {fx(s2['tt_media'],2,True)} % a.a.")
    w(f"4. Associacao historica (1961 em diante, {n_l} anos): crescimento do Brasil contra crescimento da LCN, coeficiente {fx(b_l)} e R2 {fx(r2_l)}; contra a media simples dos 7 paises, coeficiente {fx(b_7)} e R2 {fx(r2_7)}. Crescimento do Brasil contra variacao anual dos termos de troca (Funcex, {len(anos_t)} anos): correlacao {fx(r_tt_h)}.")
    w("5. As trocas de base do PPC (2011 -> 2017 em 05/2020; 2017 -> 2021 em 05/2024) mudam o NIVEL do PIB per capita em PPC e a razao Brasil/referencia, quase por um fator constante por pais: as taxas de crescimento do pais ficam. Medido por sobreposicao em duas versoes do arquivo do WDI (secao 6).")
    w("6. Mesma quebra, pobreza: a troca da linha US$ 6,85 (PPC 2017) para US$ 8,30 (PPC 2021), no mesmo release do PIP, muda o nivel e o sinal do 'Brasil menos referencia' para varias referencias (secao 6).\n")
    w("**NAO achado:**\n")
    w("- Nenhum teste de causalidade. Nenhuma estimativa de quanto 'foi mundo' e quanto 'foi governo': so coincidencia e diferenca. As correlacoes por janela tem n entre 3 e 9.")
    w("- PIB per capita em PPC do WDI so existe de 1990 em diante; antes disso, so PWT e Maddison, com outros anos-base de PPC (2017/2021 e 2011) e valores de nivel diferentes entre si (secao 6.3).")
    w("- Venezuela: sem PIB per capita PPC no WDI; inflacao so de 2009 a 2016; pobreza e Gini do PIP so ate 2006. Argentina: o WDI so traz inflacao a partir de 2018. Nada foi interpolado nem retirado depois de ver o resultado.")
    w("- Investimento publico: nao ha serie oficial unica. A serie longa e uma compilacao da FGV IBRE (IBGE ate 1994; Gobetti/Orair, Tesouro e SEST depois): marcada como LITERATURA/COMPILACAO. O ICSD do FMI (conceito FBCF do governo geral) vai ate 2019 e difere do FGV por " + (next((r["valor"] for r in MED if r["medida"] == "conceito_invpub"), "n/d")) + " pp do PIB [mediana / min / max], conceitos diferentes.")
    w("- Releases do PIP 20250401 e 20240627 devolveram erro 500 do servidor em 2026-10-19: so tres releases foram comparados. A troca 2011 -> 2017 do PPC no PIP nao pode ser medida.")
    w("- A planilha do Banco Mundial de classes de renda (OGHIST) termina em FY25; FY26 e FY27 nao foram lidos como serie (so a classe corrente via API).")
    w("- Nao ha, nos brutos, a serie de V-Dem v15 para ver revisao do indice; so a v16 via OWID.\n")

    # ------------------------------------------------ 1
    w("## 1. Regra de atribuicao ano -> governo\n")
    trans = [a for a in range(1964, 2027) if len(dias_ano(a)) > 1]
    d16 = dias_ano(2016)
    w("Cada ano-calendario pertence ao governo que o ocupa por MAIS DIAS (mesma regra de `dominios-2`; datas de `data/curated/mandatos.csv`, saida exclusiva). Anos com mais de um governo: " + ", ".join(map(str, trans)) + f"; ex.: 2016 fica com Dilma ({d16['dilma']} dias contra {d16['temer']} de Temer). A Junta Militar nunca fica com ano. Medias sao simples. As medias Brasil x referencia usam SO os anos em que os dois lados tem valor (por isso a media do Brasil muda de referencia para referencia em `janelas.csv`).\n")

    # ------------------------------------------------ 2 cobertura
    w("## 2. Cobertura (anos com valor)\n")
    cob = defaultdict(lambda: defaultdict(list))
    for arq in ("mundo", "termos_de_troca", "crescimento_contexto"):
        for r in csv.DictReader(open(RAIZ / f"series/{arq}.csv")):
            cob[(r["indicador"], r["fonte"][:34])][r["pais_ou_grupo"]].append(int(r["ano"]))
    linhas = []
    for (ind, fonte), D in cob.items():
        if ind.startswith("cc_") and not ind.startswith(("cc_fbcf", "cc_pibpc")) and False:
            continue
        b = D.get("BRA")
        rr = []
        for u in ["WLD", "LCN", "UMC"] + REFS7:
            if u in D:
                rr.append(f"{u} {len(D[u])}")
        linhas.append([ind, fonte, f"{min(b)}-{max(b)} ({len(b)})" if b else "-", ", ".join(rr) if rr else "so Brasil"])
    w(tabela(["indicador", "fonte", "Brasil: anos (n)", "n de anos por referencia"], linhas))
    w("")

    # ------------------------------------------------ 3 lula/dilma
    w("## 3. Lula 1-2 e Dilma: Brasil menos referencia, por indicador\n")
    w("Media anual dos anos em comum; diferenca = media do Brasil menos media da referencia. Colunas: LCN, UMC (renda media alta, definicao do Banco Mundial), WLD, e o menor e o maior da diferenca entre os 7 paises (ARG, CHL, COL, MEX, PER, URY, VEN). `n de anos comuns` = anos em comum com a LCN e com os 7 paises (min-max). Todas as combinacoes (14 governos, 11 referencias) estao em `janelas.csv`.\n")
    inds = [("mun_pib_cresc", "PIB real, % a.a.", ""), ("mun_pibpc_ppc_var_pct", "PIB pc PPC, variacao % a.a.", ""), ("mun_expvida", "expectativa de vida, anos", ""),
            ("mun_mortinf", "mortalidade infantil, por mil", ""), ("mun_homic", "homicidios, por 100 mil", ""), ("mun_dtp3", "DTP3, %", ""),
            ("mun_inflacao", "inflacao, % a.a.", ""), ("mun_desemprego_oit", "desemprego OIT (MODELO), %", ""), ("mun_pobreza_685", "pobreza US$ 6,85 PPC 2017, %", ""),
            ("mun_gini", "Gini, 0-100", ""), ("mun_polyarchy", "polyarchy V-Dem, 0-1", "")]
    for g, nome in [("lula12", "Lula 1-2 (2003-2010)"), ("dilma", "Dilma (2011-2016)")]:
        w(f"### {nome}\n")
        linhas = []
        for ind, rot, _ in inds:
            def d(ref, campo="diferenca_brasil_menos_ref"):
                x = jan(ind, g, ref, campo)
                return float(x) if x not in ("", None) else None
            difs7 = [d(r) for r in REFS7 if d(r) is not None]
            nl = jan(ind, g, "LCN", "n_anos")
            ns = [int(jan(ind, g, r, "n_anos")) for r in REFS7 if jan(ind, g, r, "n_anos") not in ("", None)]
            nn = f"LCN {nl or '-'}; 7 paises {min(ns)}-{max(ns)}" if ns else (f"LCN {nl}" if nl else "-")
            bra_proprio = media(v for a, v in brasil_serie(ind).items() if ANO_GOV.get(a) == g)
            col_b = fx(d("LCN", "media_brasil")) if d("LCN") is not None else (fx(bra_proprio) + " *" if bra_proprio is not None else "-")
            linhas.append([rot, col_b, fx(d("LCN", "media_referencia")), fx(d("LCN"), 2, True), fx(d("UMC"), 2, True), fx(d("WLD"), 2, True),
                           (f"{min(difs7):+.2f} a {max(difs7):+.2f}" if difs7 else "-"), nn])
        w(tabela(["indicador", "Brasil (anos comuns com LCN)", "LCN", "Brasil menos LCN", "Brasil menos UMC", "Brasil menos WLD", "Brasil menos cada um dos 7 paises (min a max)", "n de anos comuns"], linhas))
        w("`*` = media de todos os anos do Brasil na janela (nao ha agregado LCN para este indicador).\n")
        w("")
    w("Leitura: onde LCN/UMC/WLD estao vazios (homicidios nos agregados, pobreza, Gini, polyarchy) a referencia e so o conjunto de paises. Desemprego OIT e estimativa modelada; DTP3, expectativa de vida e mortalidade infantil sao estimativas de agencias da ONU, nao registros. Os 'Brasil menos' em niveis de PIB per capita PPC estao em `janelas.csv` mas dependem da base do PPC (secao 6); as variacoes anuais nao.\n")

    # ------------------------------------------------ 4 coincidencia
    w("## 4. Quanto do movimento do Brasil coincide com a America Latina e com os termos de troca\n")
    w("Descricao de coincidencia, nao de causa. Crescimento anual real do PIB (WDI NY.GDP.MKTP.KD.ZG). Termos de troca: Funcex (Ipeadata FUNCEX_TTR, anual desde 1850, encadeada em 1974; ver secao 6) e WDI/UNCTAD (TT.PRI.MRCH.XD.WD, versao 202507 do arquivo, 1980-2023; a versao corrente tem so 2005-2024). A LCN inclui o Brasil; por isso ha tambem a media simples dos 7 paises sem o Brasil.\n")
    linhas = []
    for s in [stats["lula12"], stats["dilma"]]:
        linhas.append([s["nome"], s["anos"], s["n"], fx(s["mb"]), fx(s["ml"]), fx(s["dif"], 2, True), fx(s["m7b"]) + " / " + fx(s["m7"]), fx(s["r_lcn"]), fx(s["r_m7"]), f"{s['conc']}/{s['tot']}"])
    w(tabela(["janela", "anos", "n (com LCN)", "PIB Brasil, % a.a.", "PIB LCN, % a.a.", "Brasil menos LCN, pp", "media 7 paises: Brasil / 7 paises (anos comuns)", "correlacao anual Brasil x LCN", "correlacao anual Brasil x media dos 7", "anos em que a mudanca de crescimento teve o mesmo sinal"], linhas))
    w("")
    linhas = []
    for s in [stats["lula12"], stats["dilma"]]:
        linhas.append([s["nome"], fx(s["tt_mudou"], 1, True), fx(s["tt_media"], 2, True), f"{fx(s['r_tt'])} (n={s['n_tt']})", f"{fx(s['tt_wdi_mudou'], 1, True)} ({s['tt_wdi_per']})", f"{fx(s['tt_wdi_r'])} (n={s['tt_wdi_n']})"])
    w(tabela(["janela", "termos de troca Funcex: variacao % do ano anterior ao governo ate o ultimo ano", "Funcex: variacao anual media, %", "correlacao crescimento do Brasil x variacao anual do indice (Funcex)", "termos de troca WDI: variacao %", "correlacao com WDI"], linhas))
    w("")
    w(f"Associacao historica para comparar com as janelas (todos os anos disponiveis, 1961 em diante; n={n_l}): crescimento do Brasil = {fx(a_l)} + {fx(b_l)} x crescimento da LCN (R2 {fx(r2_l)}); contra a media dos 7 paises: {fx(a_7)} + {fx(b_7)} x media (R2 {fx(r2_7)}). Aplicada sem ajuste as medias das janelas, a relacao historica com a LCN daria Brasil de {fx(a_l + b_l * stats['lula12']['ml'])} % a.a. em Lula 1-2 (observado {fx(stats['lula12']['mb'])}) e {fx(a_l + b_l * stats['dilma']['ml'])} % a.a. em Dilma (observado {fx(stats['dilma']['mb'])}). Isto e uma descricao dentro da amostra, nao uma previsao nem uma decomposicao causal.\n")
    w("Todos os governos com pelo menos 3 anos de dados de crescimento, na mesma metrica:\n")
    linhas = [[s["nome"], s["anos"], s["n"], fx(s["mb"]), fx(s["ml"]), fx(s["dif"], 2, True), fx(s["r_lcn"]), fx(s["tt_media"], 2, True), fx(s["r_tt"])] for s in todos]
    w(tabela(["governo", "anos", "n", "Brasil, % a.a.", "LCN, % a.a.", "Brasil menos LCN, pp", "correlacao Brasil x LCN", "termos de troca Funcex, variacao anual media %", "correlacao Brasil x termos de troca"], linhas))
    w("")

    # ------------------------------------------------ 5 crescimento contexto
    w("## 5. Contexto de crescimento (pre-registro, secao B)\n")
    fbcf = serie("crescimento_contexto", "cc_fbcf_pib", "FGV")
    sp = {}
    gg = {}
    for r in csv.DictReader(open(RAIZ / "series/crescimento_contexto.csv")):
        if r["indicador"] == "cc_invpub_pib" and r["fonte"].startswith("FGV") and r["pais_ou_grupo"] == "BRA":
            if "setor publico" in r["definicao_linha"]:
                sp[int(r["ano"])] = float(r["valor"])
            if r["definicao_linha"].endswith("governo geral (central + estados + municipios)"):
                gg[int(r["ano"])] = float(r["valor"])
    icsd = serie("crescimento_contexto", "cc_invpub_pib", "IMF")
    k10 = serie("crescimento_contexto", "cc_estoque_capital_pwt", "PWT 10.01")
    k11 = serie("crescimento_contexto", "cc_estoque_capital_pwt", "PWT 11.0")
    ptf10 = serie("crescimento_contexto", "cc_ptf_pwt", "PWT 10.01")
    ptf11 = serie("crescimento_contexto", "cc_ptf_pwt", "PWT 11.0")
    kv10, kv11, pv10, pv11 = var(k10), var(k11), var(ptf10), var(ptf11)
    mad = serie("crescimento_contexto", "cc_pibpc_maddison")
    madv = var(mad)
    pwtv = var(serie("crescimento_contexto", "cc_pibpc_na_pwt", "PWT 10.01"))
    pwtv11 = var(serie("crescimento_contexto", "cc_pibpc_na_pwt", "PWT 11.0"))
    pwto10 = var(serie("crescimento_contexto", "cc_pibpc_pwt", "PWT 10.01"))
    pwto11 = var(serie("crescimento_contexto", "cc_pibpc_pwt", "PWT 11.0"))
    wdiv = var(serie("mundo", "mun_pibpc_ppc"))
    linhas = []
    for gid, _, _ in GOVS:
        anos = anos_gov(gid)
        f_ = lambda d: (fx(media(d[a] for a in anos if a in d)) if any(a in d for a in anos) else "-")
        if not any(a in fbcf or a in sp for a in anos):
            continue
        linhas.append([gid, f_(fbcf), f_(sp), f_(gg), f_(icsd), f_(kv10), f_(kv11), f_(pv10), f_(pv11)])
    w("Media por governo (anos atribuidos pela regra da secao 1). FBCF e investimento publico em % do PIB; estoque de capital (rnna) e PTF (rtfpna) do PWT em variacao % a.a. calculada aqui (10.01 ate 2019; 11.0 ate 2023). `-` = sem dado.\n")
    w(tabela(["governo", "FBCF % PIB (FGV/IBGE)", "inv. publico % PIB: setor publico (FGV)", "inv. publico: governo geral (FGV)", "inv. publico governo geral (ICSD/FMI, ate 2019)", "estoque de capital, var. % a.a. (PWT 10.01)", "idem (PWT 11.0)", "PTF, var. % a.a. (PWT 10.01)", "idem (PWT 11.0)"], linhas))
    w("")
    w("Nota: PTF e residuo estimado pelo PWT, nao observado; o estoque de capital e construido por acumulacao do investimento (PWT), nao medido. Investimento publico FGV e compilacao (LITERATURA), com trocas de fonte em 1995, 2011 e 2015 (secao 6.7).\n")
    w("PIB per capita, variacao anual media (%) por governo, em cinco medidas: WDI (PPC 2021, 1991+), PWT 10.01 e 11.0 com rgdpna/pop (precos nacionais constantes, crescimento das contas nacionais), PWT 10.01 e 11.0 com rgdpo/pop (lado da producao a PPC encadeada, a medida que o PWT usa para comparar paises) e Maddison 2023 (PPC 2011). As duas familias de PWT dao taxas muito diferentes para o mesmo pais e periodo. Legenda do PWT, literal: rgdpo = 'Output-side real GDP at chained PPPs (in mil. 2017US$)' (2021US$ na 11.0); rgdpna = 'Real GDP at constant 2017 national prices (in mil. 2017US$)'. Sao medidas diferentes; esta pasta nao interpreta a diferenca (a documentacao do PWT sobre ela nao foi lida para este ponto), so a mostra.\n")
    linhas = []
    for gid, _, _ in GOVS:
        anos = anos_gov(gid)
        f_ = lambda d: (fx(media(d[a] for a in anos if a in d)) if any(a in d for a in anos) else "-")
        if gid == "junta":
            continue
        linhas.append([gid, f_(wdiv), f_(pwtv), f_(pwtv11), f_(pwto10), f_(pwto11), f_(madv)])
    w(tabela(["governo", "WDI", "PWT 10.01 (rgdpna/pop)", "PWT 11.0 (rgdpna/pop)", "PWT 10.01 (rgdpo/pop)", "PWT 11.0 (rgdpo/pop)", "Maddison 2023"], linhas))
    w("")

    # ------------------------------------------------ 6 quebras
    w("## 6. Quebras, revisoes e luzes de confianca dos dados\n")
    w("`quebras.csv` tem uma linha por quebra, no formato das outras pastas (tipo_de_quebra: metodo_estatistico, mudanca_de_regra, revisao_de_vintage). `medidas_efeito.csv` guarda cada numero medido. `quebras_na_janela` em `janelas.csv` lista as quebras que caem dentro de cada governo.\n")
    from collections import Counter
    c = Counter(r["tipo_de_quebra"] for r in QUE)
    w(f"Total: {len(QUE)} linhas ({', '.join(f'{k} {v}' for k, v in c.items())}).\n")

    w("### 6.1 Troca da base do PPC no WDI (PIB per capita), por sobreposicao de versoes\n")
    w("Cada coluna: variacao % mediana (anos comuns) do nivel do PIB per capita PPC entre a versao antiga e a nova do arquivo WDI (fonte 57, baixado em 2026-10-19). O rotulo de unidade do proprio arquivo diz 'constant 2011 international $' em todas as versoes (rotulo desatualizado); as trocas foram identificadas pelo salto de nivel entre versoes consecutivas e pelas datas de divulgacao do ICP (19/05/2020 e 30/05/2024).\n")
    linhas = []
    for u in ["BRA", "ARG", "CHL", "COL", "MEX", "PER", "URY", "WLD", "LCN", "UMC"]:
        def pick(m, a):
            for r in MED:
                if r["medida"] == m and r["alvo"] == a and r["descricao"].startswith("variacao % do nivel"):
                    return fx(float(r["valor"]), 2, True)
            return "-"
        def pickr(m, a):
            for r in MED:
                if r["medida"] == m and r["alvo"] == a and r["descricao"].startswith("variacao % da razao"):
                    return fx(float(r["valor"]), 2, True)
            return "-"
        linhas.append([u, pick("troca_ppc_wdi_2011_2017", u), pick("troca_ppc_wdi_2017_2021", u), pick("revisao_wdi_apos_2021", u),
                       "-" if u == "BRA" else pickr("troca_ppc_wdi_2011_2017", "BRA/" + u), "-" if u == "BRA" else pickr("troca_ppc_wdi_2017_2021", "BRA/" + u)])
    w(tabela(["unidade", "nivel: 2011->2017 (v202004->v202005), %", "nivel: 2017->2021 (v202403->v202405), %", "nivel: revisao 202405->202412, %", "razao Brasil/unidade: 2011->2017, %", "razao Brasil/unidade: 2017->2021, %"], linhas))
    w("")
    w("Efeito: a troca altera o nivel e a razao entre paises (ex.: Brasil/Argentina cai 18% na primeira troca), mas o fator e quase o mesmo em todos os anos de cada pais (min e max proximos em `medidas_efeito.csv`), de modo que a taxa de crescimento do pais fica. Luz de dados pela regra D: vermelha para qualquer comparacao de NIVEL entre paises que atravesse uma troca nao medida; aqui a troca foi medida por sobreposicao, entao a luz seria amarela para niveis e nenhuma para variacoes anuais.\n")

    w("### 6.2 Pobreza (PIP): linha 6,85 PPC 2017 contra 8,30 PPC 2021, mesmo release\n")
    linhas = []
    for u in ["BRA", "ARG", "CHL", "COL", "MEX", "PER", "URY", "VEN"]:
        a = next((r for r in MED if r["medida"] == "troca_ppc_pip" and r["alvo"] == u and "linha 8,30" in r["descricao"]), None)
        b = next((r for r in MED if r["medida"] == "troca_ppc_pip" and r["alvo"] == "BRA-" + u), None)
        linhas.append([u, fx(float(a["valor"]), 2, True) if a else "-", a["n"] if a else "-", "-" if u == "BRA" else (fx(float(b["valor"]), 2, True) if b else "-"), "" if u == "BRA" else (b["nota"] if b else "")])
    w(tabela(["pais", "mediana de (8,30/2021 menos 6,85/2017), pp", "n", "efeito sobre Brasil menos pais, pp (mediana)", "min a max"], linhas))
    w("")

    w("### 6.3 PWT 10.01 contra 11.0 e fontes de nivel (nao sao revisoes da mesma serie quando as fontes diferem)\n")
    linhas = []
    for r in MED:
        if r["medida"] == "versao_pwt" and r["alvo"] == "BRA" and ("Lula" in r["descricao"] or "Dilma" in r["descricao"] or "rnna" in r["descricao"] or "rtfpna" in r["descricao"]):
            linhas.append([r["descricao"], r["valor"]])
    w(tabela(["medida (PWT 10.01 / 11.0)", "valores"], linhas))
    w("")
    linhas = []
    anos_fc = (1980, 1990, 2002, 2010, 2016, 2019)
    for f_ in ["Maddison 2023 (PPC 2011)", "PWT 10.01 (PPC 2017)", "PWT 11.0 (PPC 2021)", "WDI corrente (PPC 2021)"]:
        row = [f_]
        for y in anos_fc:
            m = next((r for r in MED if r["medida"] == "fontes_cruzadas" and r["alvo"] == f_ and f"em {y}" in r["descricao"]), None)
            row.append(fx(float(m["valor"]), 3) if m else "-")
        linhas.append(row)
    w("Razao PIB per capita do Brasil / mediana de ARG, CHL, COL, MEX, PER, URY (VEN fora por falta de cobertura em PWT/WDI), por fonte:\n")
    w(tabela(["fonte"] + [str(y) for y in anos_fc], linhas))
    w("")
    w("O nivel relativo do Brasil entre as quatro fontes varia ate dezenas de pontos percentuais no mesmo ano (ex.: 1980); o WDI corrente nao existe antes de 1990. Nada aqui diz qual fonte esta certa.\n")

    w("### 6.4 Termos de troca: encadeamento da serie Funcex em 1974\n")
    linhas = [[r["descricao"], r["valor"], r["nota"]] for r in MED if r["medida"] == "encadeamento_tt"]
    w(tabela(["medida", "valor", "nota"], linhas))
    w("")
    w("O nome da serie no Ipeadata diz 'media 2018 = 100'; a nota diz 'Ate 1973, serie encadeada e convertida para a base 2006=100'. Outra incoerencia: a nota cita fonte IBGE a partir de 1879, mas a serie traz valores desde 1850. Incoerencias na propria fonte; nao resolvidas aqui.\n")

    w("### 6.5 Revisoes do WDI nos demais indicadores (Brasil), versao 202403 do arquivo -> 202507 -> corrente 2026-10-08\n")
    linhas = []
    for r in MED:
        if r["medida"] == "revisao_wdi" and r["alvo"] == "BRA":
            linhas.append([r["descricao"], r["valor"], r["nota"]])
    w(tabela(["indicador: versoes", "valores comuns alterados / comuns (Brasil)", "nota"], linhas))
    w("")

    w("### 6.6 Classes de renda do Banco Mundial\n")
    linhas = [[r["alvo"], r["valor"], r["nota"]] for r in MED if r["medida"] == "classe_renda" and r["estatistica"] == "n. de mudancas"]
    w(tabela(["pais", "mudancas FY89-FY25", "transicoes"], linhas))
    w("")
    r_um = next(r for r in MED if r["medida"] == "classe_renda" and "numero de economias" in r["descricao"])
    w(f"Economias na classe UM (renda media alta): {r_um['valor']}. Se o agregado UMC do WDI recalcula o passado com a classificacao corrente NAO foi verificado; se recalcula, a serie historica do agregado mistura paises de epocas diferentes. Pela API do WDI hoje: ARG, BRA, COL, MEX, PER = renda media alta; CHL e URY = alta; VEN = media baixa (classe corrente lida em 2026-10-19). Nota do Banco Mundial sobre a Argentina: 'Due to the limitations of the Atlas method in classifying countries experiencing persistent high inflation, Argentina and Türkiye remain classified as upper-middle-income.'\n")

    w("### 6.7 Investimento publico e FBCF\n")
    linhas = [[r["descricao"], r["valor"], r["nota"][:200]] for r in MED if r["medida"] in ("revisao_fgv", "conceito_invpub", "fbcf_fontes")]
    w(tabela(["medida", "valor", "nota"], linhas))
    w("")

    # ------------------------------------------------ 7 cadeia
    w("## 7. Cadeia de hash (resultado de `chain.py verify` por pasta)\n")
    linhas = []
    for d in [".", "wdi_arquivo", "ipea", "invpub", "pwt_maddison", "oghist", "vdem_owid", "docs"]:
        out = subprocess.run(["python3", "-I", CHAIN, "verify", str(RAIZ / d)], capture_output=True, text=True).stdout.strip().splitlines()
        linhas.append([("mundo/ (raiz: WDI e PIP)" if d == "." else "mundo/" + d), out[-1].replace("|", "/") if out else "sem saida"])
    w(tabela(["pasta", "resultado"], linhas))
    w("")
    w("Descoberta fora da cadeia: as buscas exploratorias que escolheram as series (catalogo de metadados do Ipeadata, paginas do rug.nl e do FGV, varredura de 54 versoes do arquivo WDI com 3 unidades e 1 ano, testes do PIP) foram feitas no scratchpad da sessao; tudo o que sustenta um numero foi re-adquirido pela cadeia (inclusive o catalogo, `ipea/bruto/ipea_catalogo_Metadados.json`). A varredura das 54 versoes nao esta na cadeia: o que entrou foram as 8 versoes do PIB pc PPC usadas nas medidas (201904, 202004, 202005, 202403, 202405, 202407, 202412, 202507).\n")
    w("Falhas de aquisicao registradas (nada foi omitido): PIP releases 20250401 e 20240627 (erro 500 do servidor, 4 tentativas, no log `scripts/baixar_wdi_pip.log`); uma tentativa de URL do blog 2017-ppp-poverty-lines (404, adivinhada, nao entrou no manifest). O bruto do OWID veio com todos os paises (o filtro da URL foi ignorado, 1,1 MB). Ipeadata SCN10_PIB10 e um indice real, nao o PIB nominal (baixado por engano, mantido na cadeia, nao usado); o nominal e SCN10_PIBN10. Nenhum arquivo passou de 25 MB (maior: PWT 10.01 xlsx, 6,5 MB).\n")

    w("## 8. Arquivos\n")
    w("- `series/mundo.csv`, `series/termos_de_troca.csv`, `series/crescimento_contexto.csv`: formato longo `indicador,fonte,definicao_linha,pais_ou_grupo,ano,valor,unidade,nota,vintage`.")
    w("- `janelas.csv`: indicador x governo x referencia (media Brasil, media referencia, diferenca, n_anos, quebras na janela). Para niveis/indices ha tambem a linha `<indicador>_var_pct`.")
    w("- `quebras.csv`, `medidas_efeito.csv`, `scripts/` (construir, medir, quebras, janelas, resultado; `baixar_*.sh` so com rede), `manifest.jsonl` por subpasta.\n")
    (RAIZ / "RESULTADO.md").write_text("\n".join(L), encoding="utf-8")
    print("RESULTADO.md", len("\n".join(L)))


if __name__ == "__main__":
    main()
