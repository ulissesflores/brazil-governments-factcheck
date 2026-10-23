"""quebras.csv e derivado/compulsorios_identidade.csv. Le series/, derivado/, bruto/ e quebras/quebras.csv (outra pasta, so leitura).
Colunas = as de quebras/quebras.csv. Sem rede. Rodar depois de A, B e C: python3 -I construir_D_quebras.py"""
import csv, html, json, re, statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import DADOS, PASTA, ckan, manifest

M = manifest()
COLS = ["indicador", "serie", "data_quebra", "metodo_antigo", "metodo_novo", "razao_declarada_pela_fonte", "fonte_primaria_url", "trecho_citado",
        "direcao_do_efeito", "como_a_direcao_foi_determinada", "efeito_medido", "como_medido", "apresentada_como_aprimoramento",
        "celulas_do_infografico_afetadas", "tipo_de_quebra"]
Q = []


def limpa(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def serie(nome):
    out = {}
    p = PASTA / "series" / f"{nome}.csv"
    for r in csv.DictReader(p.open(encoding="utf-8")):
        k = (int(r["ano"]), int(r["mes_ou_trimestre"]) if r["mes_ou_trimestre"] else 0)
        out[k] = float(r["valor"])
    return out


def ckan_url(cod):
    return M[f"bruto/bcb/ckan_{cod}.json"][2]


def add(**kw):
    kw.setdefault("apresentada_como_aprimoramento", "nao declarado pela fonte")
    kw.setdefault("celulas_do_infografico_afetadas", "nenhuma: indicador fora do infografico original; afeta a serie indicada no campo serie")
    Q.append(kw)


# ------------------------------------------------------------ NFSP: abrangencia (Petrobras/Eletrobras) e unidade
n5793 = limpa(ckan(5793)["notes"])
tr = re.search(r"A exclusão da Petrobras e da Eletrobras deve-se.*?retroagiu a dezembro de 2001\.", n5793)
trecho_nfsp = tr.group(0) if tr else "NAO LOCALIZADO"
resumo = list(csv.DictReader((PASTA / "derivado/nfsp_codigos_confirmados_ckan.csv").open(encoding="utf-8")))
ini = {r["sgs"]: r["primeiro_mes"] for r in resumo}
add(indicador="nfsp_*_empresas_estatais_* e nfsp_*_setor_publico_consolidado_*", serie="BCB SGS 5723/5756/5789 (estatais) e 5727/5760/5793 (consolidado), % PIB 12 meses, e fluxos 4579/4612/4645, 4583/4616/4649",
    data_quebra="2009-05 (Petrobras) e 2010-11 (Eletrobras), com recalculo retroativo a 2001-12",
    metodo_antigo="setor publico com Petrobras (series 'encerradas em abril de 2009') e com Eletrobras", metodo_novo="setor publico sem Petrobras (desde dados de maio/2009) e sem Eletrobras (desde novembro/2010), retroagido a dezembro de 2001",
    razao_declarada_pela_fonte="caracteristicas especificas das empresas, regras de governanca corporativa similares as de privadas de capital aberto e autonomia para captar recursos",
    fonte_primaria_url=ckan_url(5793), trecho_citado=trecho_nfsp, direcao_do_efeito="desconhecida",
    como_a_direcao_foi_determinada="a serie com inclusao da Petrobras esta so nas 'tabelas especiais' do BCB, nao baixadas aqui",
    efeito_medido="nao medido: sem a serie antiga nao ha sobreposicao",
    como_medido=f"primeiro mes disponivel na API: consolidado 5793 = {ini.get('5793')}, estatais 5789 = {ini.get('5789')}; antes de 2001-12 a abrangencia nao e a nova (a nota so garante recalculo desde dez/2001)",
    tipo_de_quebra="metodo_estatistico")

# unidade: fluxos em R$ milhoes antes e depois do Real
f4639 = serie("nfsp_primario_governo_federal_e_banco_central_fluxo_mensal_rs_mi_sgs4639")
jan91 = [abs(v) for (a, m), v in f4639.items() if a == 1991]
dez95 = [abs(v) for (a, m), v in f4639.items() if a == 1995]
add(indicador="nfsp_*_fluxo_mensal_rs_mi", serie="BCB SGS 4573-4583, 4606-4616, 4639-4649 (fluxo mensal, R$ milhoes)", data_quebra="1994-07 (Real; cortes de zeros 1986, 1989, 1993)",
    metodo_antigo="moeda da epoca (cruzeiro novo, cruzado, cruzado novo, cruzeiro, cruzeiro real)", metodo_novo="real (R$)",
    razao_declarada_pela_fonte="a unidade da serie e declarada como R$ milhoes; o catalogo nao descreve a conversao dos valores anteriores a jul/1994",
    fonte_primaria_url=ckan_url(4639), trecho_citado=f"unidade_medida (CKAN, SGS 4639) = {ckan(4639).get('unidade_medida')}",
    direcao_do_efeito="ambigua", como_a_direcao_foi_determinada="nao aplicavel: comparacao de ordem de grandeza",
    efeito_medido=f"mediana do modulo do fluxo primario GF+BC: 1991 = {statistics.median(jan91):.4g} R$ mi; 1995 = {statistics.median(dez95):.4g} R$ mi",
    como_medido="mediana do modulo dos 12 fluxos mensais do ano, na serie 4639 como publicada; a magnitude de 1991 e compativel com valores convertidos para R$ de hoje, nao com R$ milhoes nominais da epoca; metodo de conversao do BCB NAO verificado",
    tipo_de_quebra="mudanca_de_unidade")

# ------------------------------------------------------------ RTN (notas de rodape da planilha)
rtn_url = "https://www.tesourotransparente.gov.br/ckan/dataset/ab56485b-9c40-4efb-8563-9ce3e1973c4b/resource/527ccdb1-3059-42f3-bf23-b5e3ab4c6dc6/download/seriehistoricajul26.xlsx"
rows = list(csv.reader((DADOS / "mecanismos-contabil/derivado/rtn/13-2_1.csv").open(encoding="utf-8")))
nota = {r[0][:2].strip(): re.sub(r"\s+", " ", r[0]) for r in rows if r and re.match(r"^\d/ ", r[0].strip())}
add(indicador="rtn_gc_caixa_transferencias_repartição_receita e despesas", serie="RTN tabela 2.1 (transferencias por repartição; despesa total)", data_quebra="2012-03-01",
    metodo_antigo="transferencias por repartição sem recursos de complementação do FGTS", metodo_novo="a partir de 01/03/2012 inclui recursos de complementação do FGTS e despesas realizadas com recursos dessa contribuição",
    razao_declarada_pela_fonte="Portaria STN nº 278, de 19/04/2012", fonte_primaria_url=rtn_url, trecho_citado=nota.get("2/", "NAO LOCALIZADO"),
    direcao_do_efeito="eleva", como_a_direcao_foi_determinada="leitura do texto da nota (a regra nova inclui itens)", efeito_medido="nao medido: a planilha nao traz a serie antiga",
    como_medido="sem sobreposicao", tipo_de_quebra="mudanca_de_regra")
add(indicador="rtn_gc_caixa_despesa_outras_obrigatorias e despesa_total", serie="RTN tabela 2.1 e 2.5 (linha Creditos Extraordinarios)", data_quebra="2019/2020 (ate 2019 nao inclui os creditos do PAC)",
    metodo_antigo="creditos extraordinarios sem os referentes ao PAC (ate 2019)", metodo_novo="creditos extraordinarios com os referentes ao PAC (2020 em diante)",
    razao_declarada_pela_fonte="nao declarada", fonte_primaria_url=rtn_url, trecho_citado=nota.get("9/", "NAO LOCALIZADO"),
    direcao_do_efeito="reduz", como_a_direcao_foi_determinada="leitura do texto da nota (omissao de itens ate 2019: nivel anterior a 2020 fica menor)", efeito_medido="nao medido: a planilha nao traz o valor omitido",
    como_medido="sem sobreposicao", tipo_de_quebra="mudanca_de_regra")
add(indicador="rtn_gc_caixa_resultado_primario_abaixo_da_linha e juros", serie="RTN tabela 2.1 (subsidios e subvenções)", data_quebra="2015-2016 (acordaos 825/2015 e 3.297/2015; mes de aplicacao nao declarado na nota)",
    metodo_antigo="STN registra impactos dos programas quando paga os saldos apurados pelas instituicoes financeiras operadoras", metodo_novo="BCB incorpora mensalmente os efeitos por competencia na apuracao abaixo da linha; STN continua registrando semestralmente nos pagamentos",
    razao_declarada_pela_fonte="conformidade com os Acordaos 825/2015 e 3.297/2015 do TCU", fonte_primaria_url=rtn_url, trecho_citado=nota.get("4/", "NAO LOCALIZADO"),
    direcao_do_efeito="ambigua", como_a_direcao_foi_determinada="a nota descreve diferenca de calendario entre acima e abaixo da linha, sem sinal", efeito_medido="nao medido", como_medido="a planilha traz a discrepancia estatistica (linha 7) mas nao decompoe esta causa",
    tipo_de_quebra="mudanca_de_regra")
add(indicador="rtn_gc_caixa_receita_total e resultado_primario", serie="RTN tabela 2.1 (PIS/Pasep nao reclamado)", data_quebra="2022-12 (EC 126/2022)",
    metodo_antigo="recursos do PIS/Pasep nao reclamados contam em Demais Receitas Nao Administradas (acima da linha)", metodo_novo="abaixo da linha, ajuste patrimonial com efeito nulo no primario; a planilha cria a linha de ajuste metodologico (6.3)",
    razao_declarada_pela_fonte="art. 121 do ADCT com redacao da EC 126/2022", fonte_primaria_url=rtn_url, trecho_citado=nota.get("5/", "NAO LOCALIZADO")[:700],
    direcao_do_efeito="ambigua", como_a_direcao_foi_determinada="a nota diz que ha diferenca entre os dois metodos, sem sinal", efeito_medido="nao medido aqui (linha 6.3 da tabela 2.1 traz o ajuste)", como_medido="nao calculado",
    tipo_de_quebra="mudanca_de_regra")
add(indicador="rtn_gc_caixa_despesa_discricionarias e obrigatorias_com_controle_de_fluxo", serie="RTN tabela 2.1, linhas 4.4.1 e 4.4.2", data_quebra="2008 (primeiro ano com valor)",
    metodo_antigo="linha nao publicada (a planilha grava 0 de 1997 a 2007)", metodo_novo="linha publicada de 2008 em diante",
    razao_declarada_pela_fonte="nao declarada", fonte_primaria_url=rtn_url, trecho_citado="Tabela 2.1: '4.4.1 Obrigatórias com Controle de Fluxo' e '4.4.2 Despesas Discricionárias' = 0 de 1997 a 2007 e valor positivo desde 2008 (planilha jul/2026)",
    direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="zero e ausencia de linha, nao valor", efeito_medido="serie discricionarias comeca em 2008; antes: sem serie",
    como_medido="leitura da planilha; zeros anteriores a 2008 descartados da serie (nao sao 0 de gasto)", tipo_de_quebra="mudanca_de_regra")
cx = serie("rtn_gc_caixa_despesa_discricionarias_rs_mi")
vp = serie("rtn_gc_valor_pago_discricionarias_valor_pago_rs_mi")
dif = {k: cx[k] - vp[k] for k in cx if k in vp}
mn, mx = min(dif, key=dif.get), max(dif, key=dif.get)
add(indicador="rtn_gc_caixa_despesa_discricionarias vs rtn_gc_valor_pago_discricionarias_valor_pago", serie="RTN tabela 2.1 (4.4.2, caixa) e tabela 2.5 (2.4.2, valor pago)", data_quebra="2008 em diante (duas apuracoes simultaneas)",
    metodo_antigo="tabela 2.1: Governo Central, conceito de caixa", metodo_novo="tabela 2.5: criterio de valor pago (base Despesas e Transferencias Totais da Uniao)",
    razao_declarada_pela_fonte="duas tabelas do mesmo boletim; a nota da 2.5 remete a base de dados abertos do Tesouro", fonte_primaria_url=rtn_url, trecho_citado="1/ Para mais informações, acesse https://www.tesourotransparente.gov.br/ckan/dataset/despesas-e-transferencias-totais (nota da tabela 2.5)",
    direcao_do_efeito="ambigua", como_a_direcao_foi_determinada="diferenca caixa menos valor pago muda de sinal ao longo dos anos" if min(dif.values()) < 0 < max(dif.values()) else "diferenca caixa menos valor pago tem um unico sinal",
    efeito_medido=f"caixa - valor pago, R$ mi: minimo {dif[mn]:.1f} ({mn[0]}), maximo {dif[mx]:.1f} ({mx[0]}); {len(dif)} anos em comum",
    como_medido="subtracao ano a ano das duas series ja gravadas em series/", tipo_de_quebra="metodo_estatistico")
add(indicador="rtn_* (todas)", serie="RTN seriehistoricajul26.xlsx", data_quebra="vintage jul/2026",
    metodo_antigo="vintage anterior do boletim (nao baixado)", metodo_novo="boletim de jul/2026, 'Dados sujeitos a alteracao'", razao_declarada_pela_fonte="revisao rotineira",
    fonte_primaria_url=rtn_url, trecho_citado="Obs.: Dados sujeitos à alteração.", direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="um unico vintage em disco",
    efeito_medido="nao medido", como_medido="a pasta mecanismos-contabil guarda o mesmo vintage; sem segundo vintage nao ha diferenca a medir", tipo_de_quebra="revisao_de_vintage")

# ------------------------------------------------------------ Selic e deflatores
conf = {r["par"]: r for r in csv.DictReader((PASTA / "derivado/conferencia_selic.csv").open(encoding="utf-8"))}
c1 = conf["BM12_vs_SGS4390"]; c2 = conf["PAN12_vs_BM12_anualizado"]
md_pan = json.loads((PASTA / "bruto/ipea/PAN12_TJOVER12_metadados.json").read_text(encoding="utf-8"))["value"][0]
md_bm = json.loads((PASTA / "bruto/ipea/BM12_TJOVER12_metadados.json").read_text(encoding="utf-8"))["value"][0]
add(indicador="selic_over_mensal", serie="Ipeadata PAN12_TJOVER12 (% a.a.) vs BM12_TJOVER12 (% a.m.)", data_quebra="serie inteira (1974-)", metodo_antigo="percentual ao mes (BM12)", metodo_novo="percentual anualizado, elaboracao Ipea (PAN12)",
    razao_declarada_pela_fonte="anualizacao pelo Ipea", fonte_primaria_url=M["bruto/ipea/PAN12_TJOVER12_metadados.json"][2], trecho_citado=re.sub(r"\s+", " ", md_pan.get("SERCOMENTARIO", ""))[:300],
    direcao_do_efeito="eleva", como_a_direcao_foi_determinada="juro anualizado e maior que o mensal por construcao", efeito_medido=f"{c2['meses_em_comum']} meses em comum; {c2['meses_diferentes_gt_0_005_pp']} meses diferem mais de 0,005 pp de (1+BM12)^12-1; maior diferenca {c2['maior_diferenca_pp']}",
    como_medido="PAN12 contra (1+BM12/100)^12-1 mes a mes (derivado/conferencia_selic.csv)", tipo_de_quebra="mudanca_de_unidade")
add(indicador="selic_over_mensal", serie="Ipeadata BM12_TJOVER12 vs BCB SGS 4390", data_quebra="mes corrente do download", metodo_antigo="mes fechado", metodo_novo="mes corrente com dado parcial",
    razao_declarada_pela_fonte="o metadado do Ipeadata avisa que o mes corrente e parcial", fonte_primaria_url=M["bruto/ipea/BM12_TJOVER12_metadados.json"][2], trecho_citado=re.sub(r"\s+", " ", md_bm.get("SERCOMENTARIO", ""))[:420],
    direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="mes parcial, valor final desconhecido", efeito_medido=f"BM12 contra SGS 4390: {c1['meses_em_comum']} meses em comum ({c1['primeiro']} a {c1['ultimo']}); {c1['meses_diferentes_gt_0_005_pp']} diferem mais de 0,005 pp; maior diferenca {c1['maior_diferenca_pp']} pp",
    como_medido="derivado/conferencia_selic.csv; o mes do download (2026-10) foi excluido das series", tipo_de_quebra="revisao_de_vintage")
cd = list(csv.DictReader((PASTA / "derivado/conferencia_deflatores.csv").open(encoding="utf-8")))
for r in cd:
    add(indicador="juro_real_ex_post_*", serie=r["par"], data_quebra=f"{r['primeiro']} a {r['ultimo']}", metodo_antigo="codigo SGS (ausente do catalogo CKAN do BCB: package_search codigo_sgs devolve 0)", metodo_novo="serie Ipeadata com nome no metadado",
        razao_declarada_pela_fonte="nao aplicavel", fonte_primaria_url=(M.get("bruto/ipea/PRECOS12_IPCAG12_metadados.json") or M["bruto/ipea/PRECOS12_IPCAG12.json"])[2] if "IPCA" in r["par"] else (M.get("bruto/ipea/IGP12_IGPDIG12_metadados.json") or M["bruto/ipea/IGP12_IGPDIG12.json"])[2],
        trecho_citado=f"{r['meses_em_comum']} meses em comum; {r['meses_diferentes_gt_0_005_pp']} diferem mais de 0,005 pp; maior diferenca {r['maior_diferenca_pp']} pp", direcao_do_efeito="desconhecida",
        como_a_direcao_foi_determinada="nao aplicavel", efeito_medido=r["exemplos"] or "nenhuma diferenca acima do limite", como_medido="derivado/conferencia_deflatores.csv (exemplos em ordem decrescente de diferenca); o deflator usado e o do Ipeadata", tipo_de_quebra="metodo_estatistico" if float(r["maior_diferenca_pp"]) > 0.5 else "revisao_de_vintage")

# ------------------------------------------------------------ credito
c20 = ckan(20622); c28 = ckan(28215)
s20 = serie("credito_sfn_total_pib_sgs20622")
var = [abs(s20[k] - s20[kp]) for kp, k in zip(sorted(s20), sorted(s20)[1:]) if 2005 <= k[0] <= 2009]
salto = s20[(2007, 3)] - s20[(2007, 2)]
add(indicador="credito_sfn_total_pib", serie="BCB SGS 20622", data_quebra="2007-03 (inicio_periodo no catalogo CKAN; a API entrega dados desde 1995-07)",
    metodo_antigo="observacoes de 1995-07 a 2007-02: metodologia nao descrita no catalogo", metodo_novo="2007-03 em diante: saldo de credito concedido pelo SFN / PIB 12 meses",
    razao_declarada_pela_fonte="nao declarada", fonte_primaria_url=ckan_url(20622), trecho_citado=f"inicio_periodo: {c20.get('inicio_periodo')}; " + limpa(c20["notes"])[:260],
    direcao_do_efeito="ambigua", como_a_direcao_foi_determinada=f"salto de mar/2007 contra fev/2007 = {salto:+.2f} pp, dentro da variacao mensal tipica",
    efeito_medido=f"salto 2007-02 -> 2007-03 = {salto:+.2f} pp; mediana do modulo da variacao mensal 2005-2009 = {statistics.median(var):.2f} pp",
    como_medido="ver series/credito_sfn_total_pib_sgs20622.csv; as linhas anteriores a 2007-03 trazem a flag na coluna nota", tipo_de_quebra="metodo_estatistico")
s28 = serie("credito_ampliado_total_pib_sgs28215")
primeiro = min(s28)
add(indicador="credito_ampliado_total_pib vs credito_sfn_total_pib", serie="BCB SGS 28215 vs SGS 20622", data_quebra=f"{primeiro[0]}-{primeiro[1]:02d} (inicio de 28215)",
    metodo_antigo="saldo de credito concedido pelo Sistema Financeiro Nacional", metodo_novo="credito ampliado: saldo de operacoes de credito e de titulos de divida",
    razao_declarada_pela_fonte="conceitos diferentes no catalogo do BCB", fonte_primaria_url=ckan_url(28215), trecho_citado=limpa(c28["notes"])[:200],
    direcao_do_efeito="eleva", como_a_direcao_foi_determinada="o conceito ampliado inclui titulos de divida alem das operacoes de credito (texto do catalogo)",
    efeito_medido=f"em {primeiro[0]}-{primeiro[1]:02d}: ampliado {s28[primeiro]} % do PIB; SFN {s20.get(primeiro)} % do PIB; diferenca {s28[primeiro]-s20.get(primeiro, float('nan')):.2f} pp",
    como_medido="subtracao no primeiro mes comum; as duas bases ficam em arquivos separados e nunca foram emendadas", tipo_de_quebra="metodo_estatistico")

# ------------------------------------------------------------ compulsorios: identidade da soma
comp = {n: serie(f) for n, f in (("total", "compulsorios_saldo_total_sgs17633"), ("vista", "compulsorios_recursos_a_vista_em_especie_sgs1849"),
        ("poup", "compulsorios_poupanca_em_especie_sgs1848"), ("prazo", "compulsorios_depositos_a_prazo_em_especie_sgs1850"), ("adic", "compulsorios_exigibilidade_adicional_em_especie_sgs1797"),
        ("outros", "outros_recolhimentos_total_sgs17625"))}
meses = sorted(set(comp["total"]) & set(comp["vista"]) & set(comp["poup"]) & set(comp["prazo"]) & set(comp["adic"]))
rel = []
for k in meses:
    soma = comp["vista"][k] + comp["poup"][k] + comp["prazo"][k] + comp["adic"][k]
    rel.append((k, comp["total"][k], soma, comp["total"][k] - soma, comp["outros"].get(k)))
with (PASTA / "derivado/compulsorios_identidade.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["ano", "mes", "total_17633", "soma_1849_1848_1850_1797", "diferenca", "outros_recolhimentos_17625"])
    for k, t, s_, d, o in rel:
        w.writerow([k[0], k[1], t, round(s_, 4), round(d, 4), o])
fecham = sum(1 for _, t, s_, d, o in rel if abs(d) <= max(1.0, abs(t) * 1e-4))
add(indicador="compulsorios_saldo_total", serie="BCB SGS 17633 vs soma de 1849, 1848, 1850, 1797", data_quebra="serie inteira",
    metodo_antigo="total publicado", metodo_novo="soma das quatro componentes em especie publicadas", razao_declarada_pela_fonte="nao declarada",
    fonte_primaria_url=ckan_url(17633), trecho_citado=limpa(ckan(17633)["notes"])[:200], direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="nao aplicavel",
    efeito_medido=f"{fecham} de {len(rel)} meses ({rel[0][0][0]}-{rel[0][0][1]:02d} a {rel[-1][0][0]}-{rel[-1][0][1]:02d}) fecham dentro de max(1, 0,01%); detalhe em derivado/compulsorios_identidade.csv",
    como_medido="identidade testada mes a mes; componentes nao catalogadas (titulos, 17625) podem explicar a diferenca - nao verificado", tipo_de_quebra="metodo_estatistico")

add(indicador="series BCB SGS (todas)", serie="bruto/bcb/sgs_*.json", data_quebra="vintage 2026-10-20", metodo_antigo="vintage anterior (nao baixado)", metodo_novo="consulta de 2026-10-20",
    razao_declarada_pela_fonte="series sujeitas a revisao", fonte_primaria_url="https://dadosabertos.bcb.gov.br/", trecho_citado="Tempestividade: Até quatro semanas após o mês de referência (catalogo CKAN 28215)",
    direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="um unico vintage em disco", efeito_medido="nao medido", como_medido="sem segundo vintage", tipo_de_quebra="revisao_de_vintage")

# ------------------------------------------------------------ heranca de quebras/quebras.csv (PIB e agregados monetarios)
base = list(csv.DictReader((DADOS / "quebras/quebras.csv").open(encoding="utf-8")))
def herda(filtro, indicador, serie_):
    for r in base:
        if filtro(r):
            x = {c: r[c] for c in COLS}
            x["indicador"] = indicador
            x["serie"] = f"{serie_} <- herdada de quebras/quebras.csv ({r['indicador']}: {r['serie']})"
            x["celulas_do_infografico_afetadas"] = "herdada: " + r["celulas_do_infografico_afetadas"]
            Q.append(x)
pib = lambda r: r["indicador"] == "PIB"
agr = lambda r: r["indicador"].startswith("Agregados monetarios") and "Ipeadata BM12" not in r["serie"]
for ind, ser in (("velocidade_PIB_M1", "series/velocidade_PIB_M1_*"), ):
    herda(pib, ind, ser); herda(agr, ind, ser)
herda(agr, "multiplicador_M1_M0 e multiplicador_M3_M0", "series/multiplicador_*")
herda(pib, "rtn_*_pct_pib", "series/rtn_*_pct_pib_*")
herda(pib, "nfsp_*_pct_pib", "series/nfsp_*_12m_pct_pib_* e *_anual_pct_pib_*")
herda(pib, "credito_*_pib", "series/credito_*")

with (PASTA / "quebras.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
    w.writeheader()
    for r in Q:
        w.writerow({c: r.get(c, "") for c in COLS})
from collections import Counter
print(len(Q), "linhas;", dict(Counter(r["tipo_de_quebra"] for r in Q)))
