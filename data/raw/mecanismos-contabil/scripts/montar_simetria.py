"""Escreve simetria-por-governo.csv: para cada classe de mecanismo e CADA governo de mandatos.csv (15), um valor medido,
'sem_dado', 'nao_aplicavel', 'nao_encontrado' ou 'evento_documentado', sempre com a razao. Numeros calculados dos CSVs de series/
(que vem dos brutos com hash). Ano -> governo: o que exerceu a Presidencia na maior parte dos dias do ano (mandatos.csv).
Uso: python3 -I montar_simetria.py <pasta_mecanismos> <mandatos.csv>. Sem rede."""
import csv, datetime as dt, pathlib, sys, statistics as st
base = pathlib.Path(sys.argv[1]); man = list(csv.DictReader(open(sys.argv[2], encoding="utf8")))
G = [(m["id"], m["nome"], dt.date.fromisoformat(m["posse"]), dt.date.fromisoformat(m["saida"])) for m in man]
NOME = {g[0]: g[1] for g in G}; ORDEM = [g[0] for g in G]
def gov_do_ano(y):
    best, bd = None, -1
    for gid, _, a, b in G:
        s, e = max(a, dt.date(y, 1, 1)), min(b, dt.date(y + 1, 1, 1))
        d = (e - s).days
        if d > bd: best, bd = gid, d
    return best
def le(f):
    d = {}
    for r in csv.DictReader(open(base / "series" / f, encoding="utf8")):
        if r["valor"] != "": d.setdefault(r["indicador"], {})[int(r["ano"])] = float(r["valor"])
    return d
rtn = le("rtn-resultado-primario-extraordinarias.csv"); rap = le("restos-a-pagar-estoque-fim-de-ano.csv"); gt = le("gastos-tributarios-federais.csv")
pib = rtn["pib_nominal_rs_mi"]
def anos_gov(gid, anos): return sorted(y for y in anos if gov_do_ano(y) == gid)
def media(ind, gid, serie=rtn):
    ys = anos_gov(gid, serie[ind]); v = [serie[ind][y] for y in ys]
    return (st.mean(v), ys, max(v), ys[v.index(max(v))]) if v else (None, [], None, None)
out = []
def cel(cid, cname, gid, status, valor="", un="", janela="", razao="", mec="", fonte=""):
    out.append([cid, cname, gid, NOME[gid], status, valor, un, janela, razao, mec, fonte])
def f2(x): return f"{x:.2f}"
def janela(ys): return f"{ys[0]}-{ys[-1]} ({len(ys)} anos)" if ys else ""
# ---------- C01 atividade ilegal no PIB ----------
for g in ORDEM:
    if g in ("fhc", "lula12", "dilma", "temer", "bolsonaro", "lula3"):
        cel("C01", "atividade_ilegal_no_PIB", g, "nao_aplicavel", "", "", "serie vigente do PIB (ref. 2010, retropolada a 1995)",
            "a serie vigente nao inclui estimativa de comercializacao de drogas (item novo da ref. 2021, prevista para depois das eleicoes de 2026); contrabando tem estimativa parcial (nota 19) de alcance desconhecido", "MC01;MC02", "IBGE NM1 SCN ref. 2021; NM 19 SCN ref. 2010")
    else:
        cel("C01", "atividade_ilegal_no_PIB", g, "sem_dado", "", "", "", "o PIB deste periodo no dado publicado vem de referencias anteriores a 2010 (FGV ate 1989; IBGE ref. 1985 e 2000), cujas notas metodologicas nao foram lidas", "MC01", "")
# ---------- C02/C03 receitas nao tributarias de caixa unico ----------
for cid, nome, ind, mec in (("C02", "concessoes_e_operacoes_com_ativos_pct_pib", None, "MC04;MC05;MC06"), ("C03", "dividendos_e_participacoes_pct_pib", "dividendos_participacoes_pct_pib", "")):
    for g in ORDEM:
        if cid == "C02":
            ys = anos_gov(g, rtn["concessoes_permissoes_pct_pib"])
            vals = {y: rtn["concessoes_permissoes_pct_pib"][y] + rtn["operacoes_com_ativos_pct_pib"][y] for y in ys}
            if ys:
                pk = max(vals, key=vals.get)
                cel(cid, nome, g, "medido", f2(st.mean(vals.values())), "% do PIB, media anual", janela(ys), f"pico {f2(vals[pk])}% em {pk}; linhas 1.4.1 + 1.4.8.1 do RTN (soma de linhas oficiais, nao e a classificacao 'nao recorrente' do Tesouro)", mec, "Tesouro RTN tab 2.2-A")
                continue
        else:
            m, ys, pk, ypk = media(ind, g)
            if ys:
                cel(cid, nome, g, "medido", f2(m), "% do PIB, media anual", janela(ys), f"pico {f2(pk)}% em {ypk}; linha 1.4.2 do RTN", mec, "Tesouro RTN tab 2.2-A"); continue
        cel(cid, nome, g, "sem_dado", "", "", "", "o RTN anual comeca em 1997; nao achei serie comparavel (receita por natureza, caixa) para antes de 1997", mec, "")
# ---------- C04 meta alterada durante o exercicio ----------
C4 = {
 "lula12": ("evento_documentado", "2", "leis que mudaram a meta (art. 2)", "2009-2010", "Leis 12.053 (09/10/2009: meta 3,80%->2,50% do PIB) e 12.377 (30/12/2010: meta 3,30%->3,10%, Eletrobras fora). Outras 2 leis (11.477/2007, 12.182/2009) mudaram so o teto de abatimento: MC10", "MC11;MC13"),
 "dilma": ("evento_documentado", "2", "leis que mudaram a meta (art. 2)", "2013-2015", "Leis 12.901/2013 e 13.199 (03/12/2015: superavit de 66,3 bi -> deficit de 48,9 bi). Outras 2 leis (12.795/2013, 13.053 de 15/12/2014) mudaram so o teto de abatimento: MC10", "MC10;MC11"),
 "temer": ("evento_documentado", "2", "atos", "2016-2017", "Leis 13.291 (25/05/2016, assinada por Michel Temer interino; mandatos.csv ainda mostra Dilma ate 31/08/2016) e 13.480 (13/09/2017)", "MC11"),
 "bolsonaro": ("evento_documentado", "2", "atos (minimo coletado)", "2022", "EC 123 (14/07/2022) e EC 126 (21/12/2022, efeito em 2023) retiram despesas da meta (nao mudam o numero da meta); atos de 2019-2021 (incl. calamidade 2020) nao coletados", "MC20;MC21"),
}
for g in ORDEM:
    if g in C4:
        s, v, u, j, r, mec = C4[g]; cel("C04", "meta_de_resultado_primario_alterada_na_vigencia", g, s, v, u, j, r, mec, "Planalto (leis e ECs)")
    elif g in ("castelo", "costa_silva", "junta", "medici", "geisel", "figueiredo"):
        cel("C04", "meta_de_resultado_primario_alterada_na_vigencia", g, "nao_aplicavel", "", "", "", "nao havia meta de resultado primario fixada em lei (LDO e Anexo de Metas Fiscais sao posteriores: CF/1988 e LRF/2000); o orcamento monetario era controlado pelo CMN (MC23)", "MC23", "")
    elif g == "lula3":
        cel("C04", "meta_de_resultado_primario_alterada_na_vigencia", g, "sem_dado", "", "", "2023-2026", "LC 200/2023 criou novo regime (MC22); leis modificadoras das LDOs 2023-2026 e exclusoes da meta nao coletadas", "MC22", "")
    elif g == "fhc":
        cel("C04", "meta_de_resultado_primario_alterada_na_vigencia", g, "sem_dado", "", "", "2001-2002", "LDOs 2001-2002 lidas sem clausula de reducao da meta; leis modificadoras e LDOs 1995-2000 nao pesquisadas", "MC10", "Planalto LDO 2001-2002")
    else:
        cel("C04", "meta_de_resultado_primario_alterada_na_vigencia", g, "sem_dado", "", "", "", "LDOs/leis do periodo nao pesquisadas", "", "")
# ---------- C05 deducao de investimento da meta ----------
LIM = {2006: 3.0, 2007: 11.283, 2008: 13.825, 2009: 28.5, 2010: 29.8, 2011: 32.0, 2012: 40.6, 2013: 65.2, 2014: 67.0, 2015: 28.667}
for g in ORDEM:
    ys = [y for y in LIM if gov_do_ano(y) == g]
    if ys:
        pc = {y: LIM[y] * 1000 / pib[y] * 100 for y in ys}; pk = max(pc, key=pc.get)
        extra = "; 2014: depois de 15/12/2014 sem teto numerico (Lei 13.053)" if 2014 in ys else ""
        cel("C05", "teto_de_abatimento_da_meta_por_investimento_pac_ppi", g, "medido", f2(pc[pk]), "% do PIB (maior teto anual autorizado)", f"LDOs {ys[0]}-{ys[-1]} ({len(ys)} anos com clausula)",
            f"teto em lei, nao valor usado; maximo em {pk}: R$ {LIM[pk]:.3f} bi{extra}", "MC10", "Planalto LDOs")
    elif g in ("fhc",):
        cel("C05", "teto_de_abatimento_da_meta_por_investimento_pac_ppi", g, "nao_encontrado", "", "", "LDOs 2001-2002", "LDOs 2001-2002 sem clausula de reducao da meta no corpo da lei; LDOs 1995-2000 nao lidas", "MC10", "Planalto LDOs")
    elif g == "temer":
        cel("C05", "teto_de_abatimento_da_meta_por_investimento_pac_ppi", g, "nao_encontrado", "", "", "LDOs 2016-2017", "LDOs 2016 e 2017 sem clausula de reducao por PAC/PPI no corpo da lei (art. 3 da LDO 2017 vetado)", "MC10", "Planalto LDOs")
    elif g in ("bolsonaro", "lula3"):
        cel("C05", "teto_de_abatimento_da_meta_por_investimento_pac_ppi", g, "sem_dado", "", "", "", "LDOs 2018+ nao lidas", "", "")
    elif g in ("castelo", "costa_silva", "junta", "medici", "geisel", "figueiredo"):
        cel("C05", "teto_de_abatimento_da_meta_por_investimento_pac_ppi", g, "nao_aplicavel", "", "", "", "sem meta de resultado primario em lei", "MC23", "")
    else:
        cel("C05", "teto_de_abatimento_da_meta_por_investimento_pac_ppi", g, "sem_dado", "", "", "", "LDOs do periodo nao lidas", "", "")
# lula12 tem 2006-2010 (5 de 8 anos): anos 2003-2005 sem clausula no corpo da LDO 2005 (2003-2004 LDOs lidas sem clausula)
for r in out:
    if r[0] == "C05" and r[2] == "lula12": r[8] += "; LDOs 2003-2005 sem clausula de reducao da meta no corpo da lei"
# ---------- C06 restos a pagar ----------
stk = rap["rap_estoque_total_rs_bi"]; stkp = rap["rap_estoque_total_pct_pib"]
for g in ORDEM:
    _, _, a, b = [x for x in G if x[0] == g][0]
    fim = b.year - 1  # ultimo 31/12 anterior ou igual a saida (saida 01/01 -> 31/12 do ano anterior)
    ini = a.year - 1
    if fim in stk and g not in ("junta",):
        s_ini = stk.get(ini); ctx = f"estoque herdado em 31/12/{ini}: " + (f"R$ {s_ini:.1f} bi" if s_ini else "sem dado (serie comeca em 31/12/2007)")
        if g == "lula3": ctx += "; mandato em curso, posicao em 31/12/2025"
        cel("C06", "restos_a_pagar_estoque_em_31_12_do_ultimo_ano_do_mandato", g, "medido", f"{stk[fim]:.1f}", "R$ bilhoes correntes", f"31/12/{fim}",
            f"{stkp[fim]:.2f}% do PIB; {ctx}", {"lula12": "MC14", "dilma": "MC15", "temer": "MC16", "bolsonaro": "MC17", "lula3": "MC17"}.get(g, ""), "Tesouro Relatorio RAP 2026 Tab 2")
    elif g == "junta":
        cel("C06", "restos_a_pagar_estoque_em_31_12_do_ultimo_ano_do_mandato", g, "nao_aplicavel", "", "", "", "mandato de 60 dias, sem 31/12 dentro do periodo", "", "")
    else:
        cel("C06", "restos_a_pagar_estoque_em_31_12_do_ultimo_ano_do_mandato", g, "sem_dado", "", "", f"31/12/{fim}", "a serie do Tesouro comeca em 31/12/2007; nao achei estoque anterior (Siga Brasil nao consultado)", "", "")
# ---------- C07 gasto tributario ----------
for g in ORDEM:
    ys = anos_gov(g, gt["gasto_tributario_federal_pct_pib"])
    if ys:
        ef = [y for y in ys if (y <= 2013 or 2019 <= y <= 2023)]
        pr = [y for y in ys if y >= 2024]
        v = [gt["gasto_tributario_federal_pct_pib"][y] for y in ys]
        rz = f"anos efetivos: {ef}; projecao PLOA: {pr}" if pr else f"anos efetivos: {ef}"
        total = len([y for y in range(max(1964, G[ORDEM.index(g)][2].year), min(2026, G[ORDEM.index(g)][3].year) + 1) if gov_do_ano(y) == g])
        cel("C07", "gasto_tributario_federal_pct_pib", g, "medido", f2(st.mean(v)), "% do PIB, media anual", f"{len(ys)} de {total} anos do governo", rz, "MC18", "RFB DGT; Ipea NT 19")
    else:
        cel("C07", "gasto_tributario_federal_pct_pib", g, "sem_dado", "", "", "", "nao achei, nas fontes baixadas, estimativa federal de gasto tributario para os anos deste governo (serie oficial lida: 2007-2013 e 2019-2026; 2002 = 2,1% so por citacao secundaria)", "MC18", "")
# ---------- C08 passivos com bancos publicos / atraso de repasses ----------
adj = rtn["ajuste_caixa_competencia_pct_pib"]
for g in ORDEM:
    if g == "dilma":
        cel("C08", "passivos_do_tesouro_com_bancos_publicos_e_fundos", g, "medido", "55.6", "R$ bilhoes (passivo do Acordao 825/2015 pago em dez/2015)", "2013-2015",
            "0,93% do PIB de 2015; total pago em 2015 R$ 72,4 bi (1,21%); TCU: aprox. R$ 40 bi na noticia; a LDO 2015 permitiu abater ate R$ 57,013 bi da meta pelo pagamento", "MC07;MC08;MC09", "TCU; Fazenda; Lei 13.199")
    elif g == "lula12":
        cel("C08", "passivos_do_tesouro_com_bancos_publicos_e_fundos", g, "evento_documentado", "", "", "2010", "TCU cita adiantamentos do FGTS (MCMV) e do BNDES (PSI) 'nos exercicios de 2010 a 2014'; valor por ano nao separado", "MC08", "TCU Parecer previo 2014")
    elif g in ("temer", "bolsonaro", "lula3"):
        ys = anos_gov(g, adj); v = [adj[y] for y in ys]
        cel("C08", "passivos_do_tesouro_com_bancos_publicos_e_fundos", g, "medido", f"{st.mean(v):.3f}", "% do PIB, media anual do ajuste caixa-competencia de subsidios (RTN 6.2)", janela(ys),
            "analogo MEDIDO no regime posterior aos acordaos 825 e 3297/2015: diferenca entre caixa e competencia dos subsidios, nao e passivo omitido", "MC07", "Tesouro RTN tab 2.2-A linha 6.2")
    elif g == "fhc":
        cel("C08", "passivos_do_tesouro_com_bancos_publicos_e_fundos", g, "sem_dado", "", "", "", "nao coletado (securitizacoes e 'moedas podres' do periodo nao pesquisadas)", "", "")
    elif g in ("castelo", "costa_silva", "junta", "medici", "geisel", "figueiredo", "sarney"):
        cel("C08", "passivos_do_tesouro_com_bancos_publicos_e_fundos", g, "sem_dado", "", "", "", "ver C09 (conta movimento): o analogo pre-1988 e outra classe", "MC23", "")
    else:
        cel("C08", "passivos_do_tesouro_com_bancos_publicos_e_fundos", g, "sem_dado", "", "", "", "nao coletado", "", "")
# ---------- C09 financiamento fora do orcamento via BC/BB ----------
SUB = {"castelo": ("0,5 (1960-64) e 1,1 (1965-72)", "1964-1967"), "costa_silva": ("1,1 (1965-72)", "1967-1969"), "junta": ("1,1 (1965-72)", "1969"),
       "medici": ("1,1 (1965-72) e 1,6 (1973-80)", "1969-1974"), "geisel": ("1,6 (1973-80)", "1974-1979"), "figueiredo": ("1,6 (1973-80) e -4,5 (1981-94)", "1979-1985"),
       "sarney": ("-4,5 (1981-94)", "1985-1990")}
for g in ORDEM:
    if g in SUB:
        v, j = SUB[g]
        cel("C09", "transferencias_BC_BB_e_operacoes_fora_do_orcamento", g, "medido_no_subperiodo_nao_no_governo", v, "% do PIB por ano, media do subperiodo de Ayres et al.", j,
            "residuo da identidade orcamentaria do artigo (tabela 1, linha 8), aproximacao do deficit do orcamento monetario; o subperiodo nao coincide com o mandato" + ("; Conta Movimento congelada em 1986, Suprimentos Especiais extinta em 1988" if g in ("figueiredo", "sarney") else ""), "MC23", "Ayres et al. NBER w25421 tab. 1")
    else:
        cel("C09", "transferencias_BC_BB_e_operacoes_fora_do_orcamento", g, "nao_aplicavel", "", "", "", "Conta Movimento (1986) e Suprimentos Especiais (1988) extintas; STN criada em 10/03/1986; CF/1988 manda uma conta unica no BC", "MC23", "Tesouro Historia; Ayres et al.")
# ---------- C10 regra fiscal alterada por EC/LC ----------
C10 = {"temer": ("1", "EC 95 (15/12/2016)", "MC19"),
       "bolsonaro": ("6", "ECs 106 (07/05/2020), 109 (15/03/2021), 113 (08/12/2021), 114 (16/12/2021), 123 (14/07/2022), 126 (21/12/2022)", "MC19;MC20;MC21"),
       "lula3": ("1", "LC 200 (30/08/2023)", "MC22")}
for g in ORDEM:
    if g in C10:
        v, r, mec = C10[g]; cel("C10", "emenda_ou_lei_complementar_que_altera_regra_fiscal", g, "evento_documentado", v, "atos (coletados)", "2016-2026", r + "; so os atos pedidos no briefing foram coletados", mec, "Planalto")
    else:
        cel("C10", "emenda_ou_lei_complementar_que_altera_regra_fiscal", g, "sem_dado", "", "", "", "coleta restrita a 2016-2026 (EC 95 e emendas de 2020-2022, LC 200); atos anteriores (p.ex. DRU, LRF 2000, Fundo Social de Emergencia 1994) nao pesquisados", "", "")
# ---------- C11 estatistica de precos ----------
C11 = {
 "medici": ("1/0", "tabelamento de precos em 1973 capturado pelo indice (ato do governo)", "1973", "MC25"),
 "geisel": ("0/0", "recebe o custo: reconhecimento em 1977 (documento do ministro Simonsen), CPI e campanha salarial; ver MC25. Nenhum ato proprio de indice encontrado", "1974-1979", "MC25"),
 "sarney": ("4/1", "ato_de_governo: serie do IPCA encerrada em 28/02/1986, expurgo do compulsorio jul/ago 1986, IPC represado jun/1987, IPC represado jan/1989 | orgao independente: pesos POF 1987-88 (jun/1989)", "1985-1990", "MC26;MC27"),
 "collor": ("2/1", "ato_de_governo: IRVF com aluguel = BTN em jun-out/1990 (MP 189) e extincao do IPC por orientacao ministerial (fev/1991) | orgao independente: simplificacao das estruturas em jan/1991", "1990-1992", "MC28"),
 "itamar": ("0/1", "orgao independente: media geometrica do subitem em jan/1994", "1992-1994", "MC29"),
 "fhc": ("0/1", "orgao independente: POF 1995-96 em ago/1999", "1995-2002", "MC30"),
 "lula12": ("0/1", "orgao independente: POF 2002-03 em jul/2006", "2003-2010", "MC30"),
 "dilma": ("0/2", "orgao independente: POF 2008-09 em jan/2012; cobertura geografica em jan/2014", "2011-2016", "MC30"),
 "temer": ("0/1", "orgao independente: cobertura geografica em mai/2018", "2016-2018", "MC30"),
 "bolsonaro": ("0/1", "orgao independente: POF 2017-18 em jan/2020", "2019-2022", "MC30"),
}
for g in ORDEM:
    if g in C11:
        v, r, j, mec = C11[g]; cel("C11", "indice_de_precos_ato_de_governo_barra_orgao_independente", g, "medido" if g not in ("medici", "geisel") else "evento_documentado", v, "numero de eventos documentados: ato_de_governo / decisao_de_orgao_independente", j, r, mec, "IBGE SNIPC apendice; ../quebras/quebras.csv; literatura (MC25)")
    elif g == "lula3":
        cel("C11", "indice_de_precos_ato_de_governo_barra_orgao_independente", g, "nao_encontrado", "", "", "2023-2026", "../quebras/quebras.csv lista IPCA ate jan/2020; nenhum evento de 2023-2026 coletado", "", "")
    elif g == "junta":
        cel("C11", "indice_de_precos_ato_de_governo_barra_orgao_independente", g, "nao_aplicavel", "", "", "", "mandato de 60 dias", "", "")
    else:
        cel("C11", "indice_de_precos_ato_de_governo_barra_orgao_independente", g, "sem_dado", "", "", "", "indices do Ministerio do Trabalho (1948-1978) e a criacao do IPCA em dez/1979 existem, mas nao li historia de alteracoes deste periodo", "", "")
# ---------- C12 PIB metodologia ----------
C12 = {
 "collor": ("1", "IBGE assume as contas nacionais em 1990 (serie FGV ate 1989); efeito sem sobreposicao", "MC31"),
 "itamar": ("0", "nenhuma troca de metodo documentada em 1992-1994 nas fontes lidas", "MC31"),
 "fhc": ("1", "emenda da ref. 1985 com a ref. 2010 retropolada em 1995-96; efeito sem sobreposicao", "MC31"),
 "lula12": ("1", "mar/2007, ref. 2000: taxa de 2000 4,4->4,3, de 2005 2,3->2,9; nivel +7,1% (2000) e +10,9% (2005)", "MC31"),
 "dilma": ("1", "mar/2015, ref. 2010: crescimento 2000-2011 3,5->3,7% a.a.; PIB corrente +2,1%", "MC31"),
 "temer": ("0", "so revisoes anuais de vintage", "MC31"), "bolsonaro": ("0", "so revisoes anuais de vintage", "MC31"), "lula3": ("0", "so revisoes anuais; ref. 2021 prevista apos as eleicoes de 2026", "MC01;MC31"),
}
for g in ORDEM:
    if g in C12:
        v, r, mec = C12[g]; cel("C12", "troca_de_metodo_ou_ano_base_do_PIB", g, "medido" if v != "0" else "nao_encontrado", v, "trocas documentadas (todas por decisao_de_orgao_independente)", "", r, mec, "../quebras/quebras.csv; IBGE")
    elif g == "junta":
        cel("C12", "troca_de_metodo_ou_ano_base_do_PIB", g, "nao_aplicavel", "", "", "", "mandato de 60 dias", "", "")
    else:
        cel("C12", "troca_de_metodo_ou_ano_base_do_PIB", g, "sem_dado", "", "", "", "contas nacionais da FGV (1947-1989): historia de revisoes nao lida", "MC31", "")
cols = ["classe_id", "classe", "governo_id", "governo", "status", "valor", "unidade", "janela_dos_dados", "razao", "mecanismo_ids", "fonte"]
out.sort(key=lambda r: (r[0], ORDEM.index(r[2])))
with open(base / "simetria-por-governo.csv", "w", newline="", encoding="utf8") as f:
    w = csv.writer(f); w.writerow(cols); w.writerows(out)
print(len(out), "linhas;", len({r[0] for r in out}), "classes x", len(ORDEM), "governos")
from collections import Counter
print(Counter(r[4] for r in out))
