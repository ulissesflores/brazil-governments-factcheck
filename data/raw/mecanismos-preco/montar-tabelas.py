#!/usr/bin/env python3
"""Monta mecanismos.csv e simetria-por-governo.csv. Le so arquivos locais (rodar depois de calcular-gap.py e extrair-series.py).

Uso: python3 -I montar-tabelas.py   (a partir da pasta mecanismos-preco)
Os numeros dos episodios vem dos CSVs em series/ e de ../inflacao (IPCA, somente leitura); o texto dos trechos citados foi conferido
a olho contra os arquivos em bruto/ (e contra historia/bruto/ para os congelamentos).
"""
import csv, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
VINT = "2026-10-19"
MAND = Path("/Users/ulissesflores/Developer/brazil-governments-factcheck/data/curated/mandatos.csv")
GOVS = [r["id"] for r in csv.DictReader(MAND.open())]
COLS = ["id", "mecanismo", "tipo", "janela_inicio", "janela_fim", "governo_que_aplica", "governo_que_paga", "atribuicao",
        "magnitude_medida", "unidade", "como_medida", "reversao_medida", "fonte_primaria_url", "trecho_citado",
        "camada_de_evidencia", "vintage", "nota"]

cide = {int(r["ano"]): float(r["valor"]) for r in csv.DictReader((HERE / "series/cide-combustiveis-receita-anual.csv").open())}
dif_cide = (cide[2012] + cide[2013] + cide[2014]) - 3 * cide[2011]
wide = {int(r["ano"]): r for r in csv.DictReader((HERE / "gap-anual-mandatos.csv").open())}
porgov = {r["governo"]: r for r in csv.DictReader((HERE / "gap-por-governo.csv").open())}
ipca = {(int(x["data"][6:]), int(x["data"][3:5])): float(x["valor"]) for x in
        json.loads((HERE.parent / "inflacao/ipca-sgs433-raw.json").read_text())}


def comp(meses):
    v = 1.0
    for m in meses:
        v *= 1 + ipca[m] / 100
    return (v - 1) * 100


def desloca(y, m, k):
    t = y * 12 + (m - 1) + k
    return (t // 12, t % 12 + 1)


def janelas_ipca(y, m):
    """IPCA composto em 6 meses antes do mes do ato, 6 meses a partir dele (inclusive) e 6 meses depois."""
    antes = [desloca(y, m, -k) for k in range(6, 0, -1)]
    durante = [desloca(y, m, k) for k in range(0, 6)]
    depois = [desloca(y, m, k) for k in range(6, 12)]
    return comp(antes), comp(durante), comp(depois)


def txt_ipca(y, m):
    a, d, p = janelas_ipca(y, m)
    return (f"IPCA composto (BCB SGS 433): mes de referencia {m:02d}/{y} (primeiro mes cheio apos o ato): 6 meses antes = {a:.1f}%; 6 meses a partir dele = {d:.1f}%; "
            f"6 meses seguintes = {p:.1f}%. Descritivo; nao isola o efeito do congelamento")


NOTA_IPCA = "O IPCA tem quebra de serie em fev-mar/1986 e em 1990-91 (ver historia/RESULTADO.md secoes 4 e 5)."
R = []


def add(**k):
    k.setdefault("vintage", VINT)
    k.setdefault("nota", "")
    R.append({c: k.get(c, "") for c in COLS})


# ---------------------------------------------------------------- A. diferenca monitorados x livres em ano eleitoral
for y in (1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022):
    w = wide[y]
    aplica = w["governo_no_cargo_31dez"]
    seg = w["governo_seguinte_no_csv"]
    paga = f"seguinte_no_csv={seg}; no_cargo_em_31/12 de Y+1={w['governo_31dez_Y1'] or '-'}, Y+2={w['governo_31dez_Y2'] or '-'}, Y+3={w['governo_31dez_Y3'] or '-'}"
    add(id=f"GAP-{y}", mecanismo=f"Diferenca entre IPCA livres e monitorados no ano eleitoral federal de {y}",
        tipo="represamento_de_preco", janela_inicio=f"{y}-01", janela_fim=f"{y}-12", governo_que_aplica=aplica, governo_que_paga=paga,
        atribuicao="indeterminado", magnitude_medida=w["gap_pp"], unidade="p.p. (livres menos monitorados; positivo = monitorados subiram menos)",
        como_medida=f"acumulado do ano de BCB SGS 11428 (livres={w['livres_acum']}%) menos SGS 4449 (monitorados={w['monitorados_acum']}%); preco relativo monitorados/livres = {w['preco_relativo_pct']}%",
        reversao_medida=(f"gap em {y+1} = {w['reversao_t1']} p.p.; soma dos gaps {y+1}-{y+3} = {w['reversao_soma_3'] or 'janela incompleta'} p.p.; "
                         f"preco relativo em {y+1} = {w['rel_reversao_t1']}%; soma dos precos relativos {y+1}-{y+3} = {w['rel_reversao_soma_3'] or 'janela incompleta'}%"),
        fonte_primaria_url="https://api.bcb.gov.br/dados/serie/bcdata.sgs.11428/dados?formato=json&dataInicial=01/01/1991&dataFinal=30/09/2026 ; https://api.bcb.gov.br/dados/serie/bcdata.sgs.4449/dados?formato=json",
        trecho_citado="BCB: preços monitorados são \"aqueles que são direta ou indiretamente determinados pelos governos federal, estadual ou municipal\" (Relatório Anual 2015, nota 3; via historia/RESULTADO.md 5.2)",
        camada_de_evidencia="dado",
        nota=("Regra do ano: governo no cargo em 31/12; o governo 'pago' tem duas leituras mecanicas (proxima linha do mandatos.csv e quem estava no cargo em Y+1..Y+3), a fase 2 escolhe. "
              "Monitorados inclui decisoes estaduais, municipais e de agencias reguladoras, nao so do governo federal. "
              + ("1994: o ano mistura hiperinflacao e Plano Real, o gap em p.p. nao e comparavel com os demais; usar o preco relativo. " if y == 1994 else "")))

# ---------------------------------------------------------------- B. congelamentos e controles legais de precos (historia)
H = "https://www.planalto.gov.br/ccivil_03/"
add(id="CTL-CIP-1968", mecanismo="Conselho Interministerial de Precos (CIP), orgao federal de controle de precos",
    tipo="represamento_de_preco", janela_inicio="1968-08-29", janela_fim="1991-04-25 (data do decreto revogador citada no cabecalho do Decreto 91.240/1985; decreto revogador nao lido)",
    governo_que_aplica="costa_silva (instituicao); em vigor tambem nos governos medici, geisel, figueiredo e sarney", governo_que_paga="sem dado",
    atribuicao="ato_de_governo", magnitude_medida="sem medida oficial nesta colheita", unidade="", como_medida="",
    reversao_medida="sem dado", fonte_primaria_url="https://planalto.gov.br/ccivil_03/decreto/1980-1989/1985-1987/D91240.htm",
    trecho_citado="O Conselho Inteministerial de Preços, CIP, instituído pelo Decreto nº 63.196, de 29 de agosto de 1968 é o órgão através do qual o Governo Federal deixará e fará executar a política de abastecimento e preços no mercado interno",
    camada_de_evidencia="dado", nota="O Decreto 63.196/1968 em si nao foi baixado (404 na URL tentada); a data vem da citacao no Decreto 91.240/1985. Sem serie de precos tabelados nem de custo.")
add(id="CTL-CRUZADO-1986", mecanismo="Congelamento geral de precos (Plano Cruzado)", tipo="represamento_de_preco",
    janela_inicio="1986-02-27", janela_fim="sem prazo no DL 2.284; Cruzado II em 1986-11-21 (DL 2.290, citado pelo IBGE; texto nao lido)", governo_que_aplica="sarney",
    governo_que_paga="sarney (a inflacao volta a subir ainda no mandato)", atribuicao="ato_de_governo", magnitude_medida="sem medida oficial", unidade="",
    como_medida=txt_ipca(1986, 3), reversao_medida="IPCA mensal 1986 (BCB SGS 433): out 1,90; nov 5,45; dez 11,65",
    fonte_primaria_url=H + "decreto-lei/del2284.htm", trecho_citado="Art 35. Ficam congelados todos os preços nos níveis do dia 27 de fevereiro de 1986.",
    camada_de_evidencia="dado", nota=NOTA_IPCA + " O IPCA em cruzeiros foi encerrado em fev/1986.")
add(id="CTL-BRESSER-1987", mecanismo="Congelamento de precos por 90 dias (Plano Bresser)", tipo="represamento_de_preco",
    janela_inicio="1987-06-12", janela_fim="1987-09-10 (prazo maximo de 90 dias a contar de 12/06/1987, calculo proprio)", governo_que_aplica="sarney", governo_que_paga="sarney",
    atribuicao="ato_de_governo", magnitude_medida="sem medida oficial", unidade="", como_medida=txt_ipca(1987, 7),
    reversao_medida="ver como_medida (6 meses seguintes)", fonte_primaria_url=H + "decreto-lei/del2335.htm",
    trecho_citado="Art. 1º Ficam congelados, pelo prazo máximo de 90 (noventa) dias, todos os preços, inclusive os referentes a mercadorias, prestações de serviços e tarifas, nos níveis dos preços já autorizados ou dos preços à vista efetivamente praticados no dia 12 de junho de 1987.",
    camada_de_evidencia="dado", nota=NOTA_IPCA)
add(id="CTL-VERAO-1989", mecanismo="Congelamento de precos por prazo indeterminado (Plano Verao)", tipo="represamento_de_preco",
    janela_inicio="1989-01-14", janela_fim="sem prazo no texto legal (Lei 7.730 art. 8)", governo_que_aplica="sarney", governo_que_paga="sarney; sucessor collor (inflacao de 1990, ver serie IPCA)",
    atribuicao="ato_de_governo", magnitude_medida="sem medida oficial", unidade="", como_medida=txt_ipca(1989, 2),
    reversao_medida="ver como_medida (6 meses seguintes)", fonte_primaria_url=H + "leis/l7730.htm",
    trecho_citado="Art. 8º Ficam congelados, por prazo indeterminados, todos os preços, inclusive os referentes a mercadorias, prestação de serviços e tarifas, nos níveis dos preços já autorizados pelos órgãos oficiais competentes ou dos preços efetivamente praticados no dia 14 de janeiro de 1989.",
    camada_de_evidencia="dado", nota=NOTA_IPCA + " 1989 e ano eleitoral federal (eleicao em 15/11/1989); sem serie livres/monitorados antes de 1991.")
add(id="CTL-COLLOR1-1990", mecanismo="Vedacao de reajuste de precos sem autorizacao do Ministro (Plano Collor I)", tipo="represamento_de_preco",
    janela_inicio="1990-03-15", janela_fim="revogada pela Lei 8.178/1991 (cabecalho do Planalto)", governo_que_aplica="collor", governo_que_paga="collor",
    atribuicao="ato_de_governo", magnitude_medida="sem medida oficial", unidade="", como_medida=txt_ipca(1990, 4), reversao_medida="ver como_medida (6 meses seguintes)",
    fonte_primaria_url=H + "leis/l8030.htm",
    trecho_citado="Art. 1° Ficam vedados, por tempo indeterminado, a partir da data de publicação da Medida Provisória n° 154, de 15 de março de 1990, quaisquer reajustes de preços de mercadorias e serviços em geral, sem a prévia autorização em portaria do Ministro da Economia, Fazenda e Planejamento.",
    camada_de_evidencia="dado", nota=NOTA_IPCA + " Texto novo nesta colheita (nao estava em historia/RESULTADO.md).")
add(id="CTL-COLLOR2-1991", mecanismo="Preco so pode subir com autorizacao previa do Ministerio (Plano Collor II)", tipo="represamento_de_preco",
    janela_inicio="1991-01-30", janela_fim="sem dado", governo_que_aplica="collor", governo_que_paga="collor; sucessor itamar (inflacao de 1992-93)",
    atribuicao="ato_de_governo", magnitude_medida="sem medida oficial", unidade="", como_medida=txt_ipca(1991, 2), reversao_medida="ver como_medida (6 meses seguintes)",
    fonte_primaria_url=H + "leis/l8178.htm",
    trecho_citado="Art. 1° Os preços de bens e serviços efetivamente praticados em 30 de janeiro de 1991 somente poderão ser majorados mediante prévia e expressa autorização do Ministério da Economia, Fazenda e Planejamento.",
    camada_de_evidencia="dado", nota=NOTA_IPCA)

# ---------------------------------------------------------------- C. represamento / mudanca de regra no indice de precos
add(id="IDX-IPC-1987", mecanismo="Inflacao anterior ao Plano 'represada' no IPC de junho/1987", tipo="mudanca_de_regra_estatistica",
    janela_inicio="1987-06", janela_fim="1987-07", governo_que_aplica="sarney", governo_que_paga="sarney (o IPC de junho captou 35 dias e o de julho 12)",
    atribuicao="ato_de_governo", magnitude_medida="35 dias no IPC de junho; 12 dias no de julho", unidade="dias de coleta captados no mes",
    como_medida="descricao metodologica do proprio IBGE", reversao_medida="o mes seguinte capta menos dias (12), compensando",
    fonte_primaria_url="https://biblioteca.ibge.gov.br/visualizacao/livros/liv65477.pdf",
    trecho_citado="o governo determinou que a inflação ocorrida até o dia da divulgação do Plano (15.06) seria \"represada\" no IPC correspondente ao mês de junho",
    camada_de_evidencia="dado", nota="Cópia local do IBGE em historia/bruto/ibge-ipca/liv65477.txt (linha 2722). Instrumento citado pelo IBGE: DL 2.335 e Portaria 186/1987 do Ministerio da Fazenda.")
add(id="IDX-IPC-1989", mecanismo="Inflacao anterior ao Plano 'represada' no IPC de janeiro/1989", tipo="mudanca_de_regra_estatistica",
    janela_inicio="1989-01", janela_fim="1989-02", governo_que_aplica="sarney", governo_que_paga="sarney (o IPC de janeiro captou 51 dias e o de fevereiro 11)",
    atribuicao="ato_de_governo", magnitude_medida="51 dias no IPC de janeiro; 11 dias no de fevereiro", unidade="dias de coleta captados no mes",
    como_medida="descricao metodologica do proprio IBGE", reversao_medida="o mes seguinte capta menos dias (11)",
    fonte_primaria_url="https://biblioteca.ibge.gov.br/visualizacao/livros/liv65477.pdf",
    trecho_citado="Como nos planos anteriores, o governo determinou que a inflação ocorrida até o dia 15 de janeiro seria \"represada\"; assim, o IPC de janeiro captou a inflação ocorrida em 51 dias, enquanto o IPC de fevereiro, em 11 dias.",
    camada_de_evidencia="dado", nota="Cópia local: historia/bruto/ibge-ipca/liv65477.txt (linha 2732).")
add(id="IDX-IPC-1986", mecanismo="Expurgo de itens do IPC (supérfluos; emprestimo compulsorio sobre combustiveis e automoveis, DL 2.288 de 23/07/1986)",
    tipo="mudanca_de_regra_estatistica", janela_inicio="1986-07", janela_fim="1986-11", governo_que_aplica="sarney", governo_que_paga="sarney",
    atribuicao="ato_de_governo", magnitude_medida="sem medida oficial nesta colheita", unidade="", como_medida="", reversao_medida="sem dado",
    fonte_primaria_url="https://atlas.fgv.br/verbete/6297", trecho_citado="expurgou do índice da inflação as variações de preços de produtos considerados supérfluos, como cigarros e bebidas",
    camada_de_evidencia="literatura", nota="Fonte e a CPDOC/FGV (verbete 6297) lida em historia/RESULTADO.md 5.1; o DL 2.288 e o DL 2.290 nao foram lidos. A avaliacao 'medida cosmetica' e do autor do verbete e nao entra aqui.")
add(id="IDX-1973", mecanismo="Indice oficial de 1973 sob impacto de precos tabelados (ICV-FGV 12,6% contra DIEESE 26,1%)", tipo="mudanca_de_regra_estatistica",
    janela_inicio="1973-01", janela_fim="1973-12", governo_que_aplica="medici", governo_que_paga="sem dado", atribuicao="indeterminado",
    magnitude_medida="12,6 contra 26,1 (dois indices diferentes para o mesmo ano)", unidade="% ao ano (citacao)", como_medida="citacao de historiador; nao e medida propria",
    reversao_medida="sem dado", fonte_primaria_url="https://atlas.fgv.br/verbete/6001",
    trecho_citado="a partir desse momento os índices oficiais, principalmente em 1973, sofreram o forte impacto de preços tabelados que, na prática, eram amplamente desrespeitados",
    camada_de_evidencia="literatura", nota="Texto de Luis Aranha Correia do Lago (CPDOC/FGV). Interpretacao de historiador sobre dois indices; nao e verificacao independente. O outro agente do bloco (estatisticas) pode tratar o caso com mais fontes.")

# ---------------------------------------------------------------- D. combustiveis
add(id="PETRO-2011-2014", mecanismo="Resultado do segmento derivados da Petrobras com precos internos de gasolina e diesel controlados (2011-2014)",
    tipo="represamento_de_preco", janela_inicio="2011-01", janela_fim="2014-12", governo_que_aplica="dilma",
    governo_que_paga="dilma (resultado da empresa 2011-2014); reversao 2015-2016 em dilma e temer", atribuicao="indeterminado",
    magnitude_medida="-41,0", unidade="US$ bilhoes correntes (soma 2011-2014 do lucro liquido do segmento derivados)",
    como_medida="linha 5.1 da Tabela 1 do Ipea (Petrobras DFP/RMF): 2011 -5,7; 2012 -11,7; 2013 -8,2; 2014 -15,4; soma conferida em series/petrobras-resultado-derivados-ipea.csv",
    reversao_medida="mesmo segmento: 2015 +5,7 e 2016 +5,7 (US$ bi); IPCA gasolina 2013 6,51%, 2014 2,89%, 2015 20,10% (BCB, via historia/RESULTADO.md)",
    fonte_primaria_url="https://repositorio.ipea.gov.br/bitstream/11058/8111/1/Radar_n53_Petrobras.pdf",
    trecho_citado="De 2011 a 2014, o total dos prejuízos com a comercialização de combustíveis somou US$ 41 bilhões e explica grande parte da deterioração da situação financeira da Petrobras.",
    camada_de_evidencia="literatura",
    nota=("O Ipea (Radar 53, out/2017, Jose Mauro de Morais) escreve que a queda dos lucros 'era decorrência direta dos prejuizos na revenda de combustiveis ... como consequencia dos controles que o governo federal vinha exercendo nos precos'. "
          "O numero e resultado contabil de segmento, nao 'subsidio': inclui cambio e importacao. Atribuicao 'indeterminado' porque o preco e decisao formal da empresa; o TCU ainda nao julgou o merito (PETRO-TCU). A Petrobras e as DFP originais nao foram lidas."))
add(id="PETRO-TCU", mecanismo="TCU: representacao sobre a politica de reajuste de precos de combustiveis da Petrobras (2002-2019; indicios em 2011-2015)",
    tipo="represamento_de_preco", janela_inicio="2011", janela_fim="2015", governo_que_aplica="dilma", governo_que_paga="sem medida oficial",
    atribuicao="indeterminado", magnitude_medida="sem medida oficial (merito nao julgado)", unidade="", como_medida="",
    reversao_medida="sem medida oficial",
    fonte_primaria_url="https://static.poder360.com.br/2025/01/030.033-2016-0-AC-Petrobras-politica-de-reajuste-de-precos-de-combustiveis.pdf",
    trecho_citado="INDÍCIOS DE IRREGULARIDADES OCORRIDAS NO PERÍODO ENTRE 2011 E 2015. PROCESSO BAIXADO EM DILIGÊNCIA PARA REINSTRUÇÃO, COM AMPLIAÇÃO DO ESCOPO.",
    camada_de_evidencia="decisao_de_orgao_de_controle",
    nota=("Embargos de declaracao contra o Acordao 2.607/2023 (que corrigiu de oficio o Acordao 2.163/2023): o TCU reconheceu a insubsistencia de itens (9.7 e 9.8) do Acordao 2.163/2023 porque \"nao houve, naquela assentada, julgamento de merito\"; o escopo foi ampliado para jul/2002-set/2023 e o conselho de administracao foi excluido da relacao processual. "
          "O voto lido na sessao de 25/10/2023, segundo a imprensa (InfoMoney, nao primaria), fala em 'possiveis graves irregularidades ... entre setembro de 2012 e outubro de 2014', sem valor em reais. Copia hospedada pelo Poder360, conferir no portal do TCU."))
add(id="CIDE-2012-2015", mecanismo="CIDE-combustiveis reduzida a zero por decreto e restabelecida em 2015", tipo="represamento_de_preco",
    janela_inicio="2012-06-22", janela_fim="2015-01-28 (decreto que restabelece; aliquotas de maio de 2015 em diante)", governo_que_aplica="dilma", governo_que_paga="dilma (restabelece em 2015)",
    atribuicao="ato_de_governo", magnitude_medida="receita bruta anual da CIDE-combustiveis: 2011 8.924,1; 2012 2.736,1; 2013 34,9; 2014 13,8; 2015 3.312,2; 2016 5.699,7",
    unidade="R$ milhoes correntes", como_medida="Ipeadata SRF12_CIDE12 (Min. Economia/SRF), soma dos 12 meses, series/cide-combustiveis-receita-anual.csv",
    reversao_medida="receita sobe de 13,8 (2014) para 3.312,2 (2015) e 5.699,7 (2016)",
    fonte_primaria_url="https://www2.camara.leg.br/legin/fed/decret/2012/decreto-7764-22-junho-2012-613431-norma-pe.html ; https://www2.camara.leg.br/legin/fed/decret/2015/decreto-8395-28-janeiro-2015-780095-norma-pe.html",
    trecho_citado="DECRETO Nº 7.764, DE 22 DE JUNHO DE 2012. Altera o Decreto nº 5.060, de 30 de abril de 2004, que reduz as alíquotas da Contribuição de Intervenção no Domínio Econômico incidente sobre a importação e a comercialização de petróleo e seus derivados, gás natural e seus derivados, e álcool etílico combustível - CIDE.",
    camada_de_evidencia="dado",
    nota=(f"Diferenca aritmetica contra a receita de 2011 mantida constante nos tres anos (calculo proprio sobre series/cide-combustiveis-receita-anual.csv, nao e estimativa oficial): (2012+2013+2014) - 3x2011 = {dif_cide:.1f} R$ mi (valores com 1 casa). "
          "O Demonstrativo de Gastos Tributarios da Receita (2016) registra a CIDE com so R$ 0,6 mi em 2014: aliquota zerada por decreto nao conta como gasto tributario. "
          "O Decreto 7.764 consta como revogado no Decreto 8.395 (busca do dia). Os textos em bruto/legislacao/ sao paginas de ementa da Camara."))
add(id="IPCA-ADM-2013-2015", mecanismo="IPCA de gasolina, energia residencial e onibus urbano, 2013-2015 (precos que o governo administra direta ou indiretamente)", tipo="represamento_de_preco",
    janela_inicio="2013-01", janela_fim="2015-12", governo_que_aplica="dilma", governo_que_paga="dilma (2015)", atribuicao="indeterminado",
    magnitude_medida="energia residencial 2013 -15,65%; 2014 +17,06%; 2015 +50,99%. Gasolina 6,51; 2,89; 20,10. Onibus 0,04; 3,86; 15,09. Monitorados 1,54; 5,32; 18,07; livres 7,29; 6,72; 8,51",
    unidade="% no ano", como_medida="Relatorios Anuais do BCB 2014 e 2015 (via historia/RESULTADO.md 5.2), series/ipca-itens-administrados-bcb.csv",
    reversao_medida="2015 e o ano da subida: monitorados 18,07% contra livres 8,51%",
    fonte_primaria_url="https://www.bcb.gov.br/pec/boletim/banual2015/rel2015p.pdf ; https://www.bcb.gov.br/content/controleinflacao/controleinflacao_docs/carta_aberta/carta2015.pdf",
    trecho_citado="realinhamento dos preços administrados em relação aos livres",
    camada_de_evidencia="dado", nota="A frase e o diagnostico do Copom (Relatorio de Inflacao dez/2014) e da Carta Aberta do BCB de 08/01/2016; o BCB nao atribui intencao. As atribuicoes de motivo eleitoral sao alegacoes de terceiros e nao entram.")
add(id="ENER-MP579-2012", mecanismo="MP 579/2012 (Lei 12.783/2013): reducao de encargos e tarifas de energia, com aportes da Uniao na CDE", tipo="represamento_de_preco",
    janela_inicio="2012-09-11", janela_fim="2015-01 (Uniao deixa de aportar na CDE; quotas dos consumidores sobem)", governo_que_aplica="dilma", governo_que_paga="dilma (2015) e consumidores em 2015-2018; temer",
    atribuicao="ato_de_governo", magnitude_medida="Recursos da Uniao na CDE (orcado): 2013 8.460; 2014 11.805; 2015 a 2018 zero. CGU: subsidio publico de 2013-2014 = R$ 28,5 bi (valores reais de 2018)",
    unidade="R$ milhoes correntes (tabela) e R$ bilhoes de 2018 (CGU)", como_medida="CGU, Relatorio de Avaliacao da CDE, Tabela 1 (dados Aneel) e Grafico 1; series/cde-receitas-orcadas-cgu.csv",
    reversao_medida="Quotas CDE-Uso (pagas pelos consumidores): 1.024 (2013); 1.700 (2014); 18.920 (2015); 11.853 (2016); 9.348 (2017); 14.160 (2018). IPCA energia residencial 2015: +50,99%",
    fonte_primaria_url="https://www.gov.br/cgu/pt-br/assuntos/auditoria-e-fiscalizacao/avaliacao-da-gestao-dos-administradores/prestacao-de-contas-do-presidente-da-republica/arquivos/2019-1/relatorio-de-avaliacao-da-conta-de-desenvolvimento-energetico-cde.pdf",
    trecho_citado="O quadro generalizado de perdas provocado pela MP 579/2012, somado à maior restrição fiscal, que ficou mais evidente a partir de 2015, levou a União a deixar de fazer novos aportes discricionários à CDE",
    camada_de_evidencia="decisao_de_orgao_de_controle",
    nota=("Valores da Tabela 1 sao ORCADOS, nao executados. O relatorio da CGU atribui as perdas ao conjunto MP 579 + crise hidrica + leilao de 2004 nao contratado; nao so a decisao de preco. "
          "Revisao tarifaria extraordinaria da Aneel em fev/2015 (media 23,4%) so aparece em imprensa; nao lida em fonte primaria. Relacao com a classe 'contabilidade' (CDE) fica com o outro agente."))
add(id="ENER-RTE-2002", mecanismo="Recomposicao tarifaria extraordinaria apos o racionamento de 2001 (Lei 10.438/2002)", tipo="adiamento_de_despesa",
    janela_inicio="2001-06-01 (periodo das areas sujeitas ao Percee)", janela_fim="sem dado (vigora pelo periodo necessario a compensacao do montante apurado pela Aneel)",
    governo_que_aplica="fhc", governo_que_paga="consumidores em anos seguintes (lula12 incluido); valor por governo: sem dado", atribuicao="decisao_legislativa",
    magnitude_medida="teto legal da recomposicao: ate 2,9% (residencial, rural, iluminacao publica) e ate 7,9% (demais); total em R$: sem medida oficial nesta colheita",
    unidade="% sobre a tarifa (teto legal)", como_medida="texto da Lei 10.438/2002, art. 4 par. 1", reversao_medida="sem dado",
    fonte_primaria_url="https://www.planalto.gov.br/ccivil_03/leis/2002/l10438.htm",
    trecho_citado="até 2,9% (dois vírgula nove por cento), para os consumidores integrantes das Classes Residencial, Rural e iluminação pública; ... até 7,9% (sete vírgula nove por cento), para os demais consumidores",
    camada_de_evidencia="dado", nota="NAO e represamento: e recuperacao de custo de uma crise de oferta (racionamento), incluida para ter um item de energia fora de 2012-2015. Atribuicao do choque inicial nao e tratada.")
add(id="ENER-COVID-2020", mecanismo="Conta Covid: emprestimo as distribuidoras de energia que atenuou reajustes tarifarios de 2020 e 2021", tipo="adiamento_de_despesa",
    janela_inicio="2020", janela_fim="2025 (amortizacao pela CDE entre 2021 e 2025)", governo_que_aplica="bolsonaro", governo_que_paga="bolsonaro e lula3 (amortizacao 2021-2025)",
    atribuicao="ato_de_governo", magnitude_medida="15,3", unidade="R$ bilhoes", como_medida="valor total do emprestimo segundo voto-vista do Diretor-Geral da Aneel (10/12/2024)",
    reversao_medida="amortizacao pela CDE entre 2021 e 2025 (texto do voto); calendario por ano: sem dado",
    fonte_primaria_url="https://static.poder360.com.br/2024/12/distribuidoras-voto-sandoval.pdf",
    trecho_citado="A Conta Covid foi um empréstimo feito às distribuidoras, no valor total de R$ 15,3 bilhões ... os valores emprestados às distribuidoras eram integralmente reconhecidos como componentes financeiros negativos nos processos tarifários de 2020 e 2021, atenuando seus efeitos.",
    camada_de_evidencia="decisao_de_orgao_de_controle", nota="Documento da Aneel (regulador), copia hospedada pelo Poder360. Motivo declarado: pandemia. Nao e ano eleitoral federal. O decreto do governo nao foi lido.")
add(id="DIESEL-2018", mecanismo="Subvencao ao diesel apos a greve de maio de 2018 (Lei 13.723/2018, conversao da MP 838)", tipo="represamento_de_preco",
    janela_inicio="2018-06-08 (R$ 0,07/l ate 07/06; ate R$ 0,30/l a partir de 08/06)", janela_fim="2018-12-31", governo_que_aplica="temer", governo_que_paga="temer (orcamento de 2018)",
    atribuicao="decisao_legislativa", magnitude_medida="teto legal de R$ 9,5 bilhoes; valor pago: sem medida oficial nesta colheita", unidade="R$ bilhoes (teto)",
    como_medida="texto da lei, art. 7", reversao_medida="sem dado", fonte_primaria_url="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13723.htm",
    trecho_citado="A subvenção econômica de que tratam os arts. 1º e 2º desta Lei ficará limitada ao valor total de R$ 9.500.000.000,00 (nove bilhões e quinhentos milhões de reais).",
    camada_de_evidencia="dado", nota="O teto nao e o desembolso. A reducao de CIDE e PIS/Cofins do mesmo pacote (Decreto 9.391/2018, nao lido) nao tem estimativa da Receita nesta colheita: a serie 'Desoneracoes Instituidas' comeca em 2019. 2018 e ano eleitoral federal.")
add(id="DIESEL-2021", mecanismo="PIS/Cofins do diesel e do GLP domestico reduzidos a zero (Decreto 10.638/2021)", tipo="represamento_de_preco",
    janela_inicio="2021-03-01", janela_fim="2021-04-30 (diesel); GLP sem prazo na planilha", governo_que_aplica="bolsonaro", governo_que_paga="bolsonaro; estimativa do GLP tambem 2022 e 2023",
    atribuicao="ato_de_governo", magnitude_medida="diesel 3.001,99 (2021); GLP 674,68 (2021), 922,06 (2022), 945,11 (2023)", unidade="R$ milhoes (estimativa da Receita)",
    como_medida="Receita Federal, planilha Desoneracoes Instituidas 2021, linhas 14 e 15", reversao_medida="fim do prazo do diesel em 30/04/2021 (planilha)",
    fonte_primaria_url="https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/relatorios/renuncia/gastos-tributarios-bases-efetivas/desoneracoes-instituidas-2021/view",
    trecho_citado="Altera o parágrafo único do art. 1º do Decreto nº 5.059, de 30 de abril de 2004, para aumentar o coeficiente de redução ... para 1 (um inteiro) ... reduzindo, desta forma, o valor das referidas contribuições incidentes nas operações com óleo diesel e suas correntes.",
    camada_de_evidencia="dado", nota="Estimativa ex-ante da Receita, nao arrecadacao observada. Medida de compensacao na planilha: Item 7, EM 40/2021.")
add(id="LC192-2022", mecanismo="LC 192/2022: PIS/Cofins zero sobre diesel, GLP, querosene de aviacao e biodiesel; ICMS monofasico sobre combustiveis", tipo="represamento_de_preco",
    janela_inicio="2022-03-11", janela_fim="2022-12-31", governo_que_aplica="bolsonaro", governo_que_paga="bolsonaro (2022); lula3 estende a medida em 2023 (MP 1.157)",
    atribuicao="decisao_legislativa", magnitude_medida="14.932,41", unidade="R$ milhoes (estimativa da Receita para 2022)",
    como_medida="Receita Federal, Desoneracoes Instituidas 2022, linha 26", reversao_medida="prazo ate 31/12/2022; em 2023 a MP 1.157 reduz de novo (ver MP1157-2023)",
    fonte_primaria_url="https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/relatorios/renuncia/gastos-tributarios-bases-efetivas/desoneracoes-instituidas-2022/view",
    trecho_citado="Reduz para zero ponto percentuais (0%) as alíquotas da Contribuição para o PIS/Pasep e da Cofins incidentes sobre a receita bruta decorrente da venda de óleo diesel e suas correntes, da venda de gás liquefeito de petróleo ... de querosene de aviação",
    camada_de_evidencia="dado", nota="Lei sancionada em ano eleitoral federal; originada no Congresso (iniciativa legislativa nao verificada aqui). Compensacao: 'Artigo 8 da LC 192/22'. A parte ICMS (estadual) nao tem estimativa oficial federal nesta colheita.")
add(id="LC194-2022", mecanismo="LC 194/2022: PIS/Cofins e CIDE zero sobre diesel, biodiesel, GLP e querosene de aviacao; teto de ICMS sobre combustiveis, energia, comunicacoes e transporte", tipo="represamento_de_preco",
    janela_inicio="2022-06-23", janela_fim="2022-12-31 (federal); ICMS: sem prazo", governo_que_aplica="bolsonaro", governo_que_paga="lula3 (compensacao aos estados, LC 201/2023)",
    atribuicao="decisao_legislativa", magnitude_medida="16.511,22 (2022) e 18.616 (2023) na estimativa federal da Receita; ICMS: ver LC201-2023", unidade="R$ milhoes",
    como_medida="Receita Federal, Desoneracoes Instituidas 2022, linha 39 (gasto tributario: 'Em Analise')", reversao_medida="ver LC201-2023 e MP1157-2023",
    fonte_primaria_url="https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/relatorios/renuncia/gastos-tributarios-bases-efetivas/desoneracoes-instituidas-2022/view",
    trecho_citado="Reduz para zero as alíquotas da Contribuição para o PIS/Pasep, da Cofins e CIDE-Combustíveis sobre óleo diesel; de biodiesel; de gás liquefeito, derivado de petróleo e de gás natural; e de querosene de aviação.",
    camada_de_evidencia="dado", nota="O valor de 2023 (18.616) esta na coluna do ano seguinte da planilha com prazo ate 31/12/2022: a planilha nao explica; tratar com cautela. Ano eleitoral federal. Estimativas da Comsefaz (R$ 102 a 109 bi de ICMS em 12 meses) estao em LC194-COMSEFAZ.")
add(id="LC201-2023", mecanismo="Uniao compensa os estados pela perda de ICMS de 2022 causada pela LC 194", tipo="adiamento_de_despesa",
    janela_inicio="2023-10-24", janela_fim="ate 2025 (cronograma de pagamento: sem dado nesta colheita)", governo_que_aplica="bolsonaro (LC 194, jun/2022)", governo_que_paga="lula3",
    atribuicao="decisao_legislativa", magnitude_medida="27.014,9", unidade="R$ milhoes (quantia nominal fixada em lei)",
    como_medida="LC 201/2023, art. 2", reversao_medida="e a propria conta paga: compensacao integral 'a titulo de quitacao total'",
    fonte_primaria_url="https://www2.camara.leg.br/legin/fed/leicom/2023/leicomplementar-201-24-outubro-2023-794851-normaatualizada-pl.pdf",
    trecho_citado="Art. 2º ... a União compensará a quantia nominal de R$ 27.014.900.000,00 (vinte e sete bilhões quatorze milhões e novecentos mil reais) aos Estados e ao Distrito Federal, a título de quitação total do valor devido em razão da redução da arrecadação do ICMS ocasionada pela aplicação do disposto na referida Lei Complementar",
    camada_de_evidencia="dado", nota="Valor de compensacao negociado e fixado por lei, nao e a perda estimada. Compensacao com abatimento de valores ja usufruidos por tutela do STF.")
add(id="LC194-COMSEFAZ", mecanismo="Estimativa de perda de ICMS dos estados com as LC 192 e 194 (associacao dos secretarios de Fazenda)", tipo="represamento_de_preco",
    janela_inicio="2022-06", janela_fim="2023-06 (12 meses seguintes a LC 194)", governo_que_aplica="bolsonaro", governo_que_paga="estados; parte compensada pela uniao (LC201-2023)",
    atribuicao="decisao_legislativa", magnitude_medida="102 a 109; observada pela entidade: 45", unidade="R$ bilhoes (perda contrafactual em 12 meses; perda do periodo)",
    como_medida="nota tecnica 023/2023 da Comsefaz (metodo: arrecadacao contrafactual com variacao do PIB nominal ou da base)", reversao_medida="LC 201/2023 compensa R$ 27,0 bi (limite fixado em lei)",
    fonte_primaria_url="https://static.poder360.com.br/2023/11/NOTA-TECNICA-COMSEFAZ-023-2023-Impactos-das-LCs-192.22-e-LCs-194.22-sobre-arrecadacao-de-ICMS-dos-estados1-1.pdf",
    trecho_citado="a queda efetiva medida a partir do exercício contrafatual apresentado abaixo varia de R$ 102 bilhões a R$ 109 bilhões.",
    camada_de_evidencia="alegacao", nota="Parte interessada (entidade dos secretarios estaduais). Sem estimativa de orgao oficial neste ponto (STN, Receita, TCU, Congresso nao localizados em uma busca dirigida).")
add(id="MP1157-2023", mecanismo="MP 1.157/2023: reducao de PIS/Cofins sobre combustiveis em 2023; MP 1.163/2023 reduz aliquotas de gasolina, alcool, GNV e querosene", tipo="represamento_de_preco",
    janela_inicio="2023-01-01", janela_fim="2023-12-31 (prazos da planilha)", governo_que_aplica="lula3", governo_que_paga="lula3",
    atribuicao="ato_de_governo", magnitude_medida="MP 1.157: 25.000 (2023); MP 1.163: 6.610 (2023)", unidade="R$ milhoes (estimativa da Receita/EM)",
    como_medida="Receita Federal, Desoneracoes Instituidas 2023, linhas 11 e 13 (fonte da estimativa: EM 1/2023 MF e EM 26/2023 MF)", reversao_medida="CIDE-combustiveis: 1.273,0 (2023); 2.914,5 (2024); 3.232,5 (2025)",
    fonte_primaria_url="https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/relatorios/renuncia/gastos-tributarios-bases-efetivas/desoneracoes-instituidas-2023/view",
    trecho_citado="Reduz as alíquotas da Contribuição para o Programa de Integração Social e o Programa de Formação do Patrimônio do Servidor Público - PIS/Pasep e da Contribuição para o Financiamento da Seguridade Social - Cofins incidentes sobre operações realizadas com óleo diesel , biodiesel , gás liquefeito de petróleo, álcool, querosene de aviação, gás natural veicular e gasolina.",
    camada_de_evidencia="dado", nota="Continua, no governo seguinte, o regime de 2022. As duas estimativas podem se sobrepor (MP 1.163 altera o regime da MP 1.157); nao somar. Fim da medida apos 2023: nao verificado.")
add(id="PETRO-ECDG-2023", mecanismo="TCU acompanha a Estrategia Comercial de Diesel e Gasolina da Petrobras (maio/2023)", tipo="represamento_de_preco",
    janela_inicio="2023-05-16", janela_fim="em curso na data do acordao", governo_que_aplica="lula3", governo_que_paga="sem dado",
    atribuicao="indeterminado", magnitude_medida="sem medida oficial", unidade="", como_medida="", reversao_medida="sem dado",
    fonte_primaria_url="https://static.poder360.com.br/2024/11/acordao-tcu-petrobras.pdf",
    trecho_citado="AUSÊNCIA DE NORMA INTERNA CONTENDO DETALHAMENTO DA FORMA DE EXECUÇÃO DA ESTRATÉGIA. DETERMINAÇÃO. CONTINUIDADE DO ACOMPANHAMENTO.",
    camada_de_evidencia="decisao_de_orgao_de_controle", nota="TC 015.281/2023-0. O TCU nao classificou os riscos como irregulares naquele momento; sem valor em reais. Copia Poder360, conferir no TCU.")

# ---------------------------------------------------------------- E. desoneracoes setoriais
add(id="IPI-AUTO-2009", mecanismo="Reducao do IPI de automoveis (dez/2008 a 2009)", tipo="renuncia_temporaria", janela_inicio="2008-12", janela_fim="2009",
    governo_que_aplica="lula12", governo_que_paga="lula12", atribuicao="ato_de_governo", magnitude_medida="volume desonerado 1.817 no 1o semestre de 2009; custo apos descontar outros tributos 559",
    unidade="R$ milhoes", como_medida="estudo do Ipea citado no Acordao 713/2014 do TCU, itens 2.1.7.28 a 2.1.7.32",
    reversao_medida="sem dado", fonte_primaria_url="https://www.mpc.es.gov.br/wp-content/uploads/2014/07/Acordao-TCU-713-2014-Plenario.pdf",
    trecho_citado="Assim, descontando o impacto positivo do IPI reduzido apenas sobre outros tributos federais, chega-se a um custo da redução de alíquotas de R$ 559 milhões (volume total desonerado, R$ 1.817 milhões, menos R$ 1.258 milhões).",
    camada_de_evidencia="decisao_de_orgao_de_controle", nota="Tipo 'renuncia_temporaria' fora da lista do pedido (a lista nao tem rotulo para renuncia tributaria). Motivo declarado na fonte: crise de 2008-09. Estudo do Ipea (nao do TCU); o TCU so o reproduz.")
add(id="DESON-IPI-IR-2008-2012", mecanismo="Desoneracao bruta de IR e IPI (concedida desde 2008), total por ano", tipo="renuncia_temporaria", janela_inicio="2008", janela_fim="2012",
    governo_que_aplica="lula12 e dilma", governo_que_paga="uniao, estados e municipios via fundos de participacao", atribuicao="ato_de_governo",
    magnitude_medida="2008 61,51; 2009 59,46; 2010 70,58; 2011 77,23; 2012 85,20 (soma 353,98)", unidade="R$ bilhoes correntes (desoneracao bruta)",
    como_medida="Acordao 713/2014 TCU, Tabela 3 (dados STN e RFB)", reversao_medida="sem dado", fonte_primaria_url="https://www.mpc.es.gov.br/wp-content/uploads/2014/07/Acordao-TCU-713-2014-Plenario.pdf",
    trecho_citado="Desoneração bruta (Db) 61.508.767 59.457.746 70.576.558 77.234.422 85.200.686 353.978.179 (R$ milhares)",
    camada_de_evidencia="decisao_de_orgao_de_controle", nota="Agrega todas as renuncias de IR e IPI do periodo, nao so as temporarias, e atravessa dois governos (a divisao 2008-2010 / 2011-2012 coincide com Lula e Dilma pelo ano calendario, nao pelo ato). Mecanismo exato do pedido (IPI automoveis 2012-2014, Regime Automotivo/Inovar-Auto) sem valor proprio nesta colheita.")
add(id="FOLHA-2011-2015", mecanismo="Desoneracao da folha de salarios (Lei 12.546/2011 e alteracoes)", tipo="renuncia_temporaria", janela_inicio="2011-12 (Lei de 14/12/2011)", janela_fim="indeterminado; reoneracao parcial por Leis 13.161/2015 e 13.202/2015 (citadas pela Receita, nao lidas)",
    governo_que_aplica="dilma", governo_que_paga="dilma e governos seguintes (o gasto continua em 2016-2019)", atribuicao="decisao_legislativa",
    magnitude_medida="2014 22.107,3; 2015 25.199,1; 2016 14.546,6 (proj.); 2017 13.704,1; 2018 12.104,7; 2019 10.155,4", unidade="R$ milhoes (gasto tributario, estimativa da Receita)",
    como_medida="Receita Federal, DGT Bases Efetivas 2016 (serie 2014-2019), Quadro XXVI; series/receita-gastos-tributarios-folha-cide.csv", reversao_medida="queda de 25.199,1 (2015) para 14.546,6 (2016)",
    fonte_primaria_url="https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/relatorios/renuncia/gastos-tributarios-bases-efetivas/dgt-bases-efetivas-2016-serie-2014-a-2019-quadros/view",
    trecho_citado="Desoneração da Folha de Salários | Cont. Previdência Social | Lei 12.546/12, art. 7º a 11; Lei 12.715/12, art. 55 e 56 ... Lei n° 13.161/15, Lei n° 13.202/15 (Base conceitual e gerencial, DGT 2016)",
    camada_de_evidencia="dado", nota="Valores de 2014-2015 sao 'bases efetivas' e os de 2016 em diante projecao, segundo o cabecalho do quadro. 2012-2013 nao aparecem neste DGT. A compensacao do Tesouro ao RGPS nao foi medida. Ainda em vigor ao final da serie, portanto parte do custo cai em governos seguintes sem ser ato deles.")

with (HERE / "mecanismos.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(R)
print("mecanismos.csv", len(R), "linhas")

# ---------------------------------------------------------------- simetria por governo
S_COLS = ["classe", "governo", "status", "valor", "unidade", "detalhe", "razao", "ids_mecanismos"]
S = []


def sim(classe, gov, status, valor="", unidade="", razao="", ids=""):
    """status final so com o vocabulario do pedido: medido | sem dado | nao_aplicavel. A distincao fina vai para `detalhe`."""
    detalhe = ""
    if status in ("instrumento_sem_medida", "sem achado", "sem dado"):
        detalhe = {"instrumento_sem_medida": "instrumento_achado_sem_medida", "sem achado": "nada_achado_nesta_colheita", "sem dado": "nao_colhido"}[status]
        if valor:
            detalhe += ": " + valor
        status, valor = "sem dado", ""
    S.append(dict(classe=classe, governo=gov, status=status, valor=valor, unidade=unidade, detalhe=detalhe, razao=razao, ids_mecanismos=ids))


# K1 e K2: diferenca monitorados x livres
for g in GOVS:
    p = porgov[g]
    if p["meses_com_dado"] == "0":
        for c in ("K1_preco_relativo_monitorados_vs_livres_na_janela", "K2_soma_gap_pp_anos_31dez"):
            sim(c, g, "sem dado", razao="SGS 11428 e 4449 comecam em jan/1991; o IPCA nasce sem decomposicao oficial livres/monitorados antes disso. Nao reconstruido.")
    else:
        parc = f" ({p['nota']})" if p["nota"] else ""
        sim("K1_preco_relativo_monitorados_vs_livres_na_janela", g, "medido", p["preco_relativo_monitorados_vs_livres_pct"], "% composto na janela do mandato",
            f"janela {p['janela']}, {p['meses_com_dado']} meses; negativo = monitorados subiram menos que livres; 12 meses seguintes = {p['preco_relativo_12m_seguintes_pct'] or 'sem dado'}%{parc}", "serie gap-por-governo.csv")
        sim("K2_soma_gap_pp_anos_31dez", g, "medido" if p["soma_gap_anos_31dez_pp"] else "sem dado", p["soma_gap_anos_31dez_pp"], "p.p. (soma dos gaps anuais)",
            "anos atribuidos pela regra 31/12; soma de p.p. sob hiperinflacao (1991-1994) nao e comparavel com anos de inflacao baixa" if g in ("collor", "itamar") else "anos atribuidos pela regra 31/12", "gap-anual-mandatos.csv")

# K3: controle legal geral de precos
k3 = {
    "castelo": ("sem dado", "", "Controle de precos da CONEP (1965) so citado em resumo de busca, nao lido em fonte primaria", ""),
    "costa_silva": ("instrumento_sem_medida", "1 (CIP, 29/08/1968)", "instrumento localizado, sem serie de precos nem de custo", "CTL-CIP-1968"),
    "junta": ("sem dado", "", "mandato de dois meses; nada colhido", ""),
    "medici": ("instrumento_sem_medida", "CIP em vigor; 1973 em literatura", "CIP herdado; 1973: precos tabelados e indices divergentes (CPDOC)", "CTL-CIP-1968;IDX-1973"),
    "geisel": ("sem dado", "", "CIP em vigor (herdado); nada especifico colhido", "CTL-CIP-1968"),
    "figueiredo": ("sem dado", "", "CIP em vigor (herdado); nada especifico colhido", "CTL-CIP-1968"),
    "sarney": ("instrumento_sem_medida", "3 congelamentos (1986, 1987, 1989) + CIP", "tres decretos/leis de congelamento geral; custo nao medido; IPCA descritivo no mecanismo", "CTL-CRUZADO-1986;CTL-BRESSER-1987;CTL-VERAO-1989"),
    "collor": ("instrumento_sem_medida", "2 (Lei 8.030/1990, Lei 8.178/1991)", "duas leis de controle de reajuste; custo nao medido", "CTL-COLLOR1-1990;CTL-COLLOR2-1991"),
}
for g in GOVS:
    if g in k3:
        st, v, rz, ids = k3[g]
        sim("K3_controle_legal_geral_de_precos", g, st, v, "instrumentos achados", rz, ids)
    else:
        sim("K3_controle_legal_geral_de_precos", g, "sem achado", "", "", "nenhum controle geral achado na colheita historia; nao e prova de ausencia (busca dirigida por plano, nao varredura)", "")

# K4: represamento ou mudanca de regra no indice de precos
k4 = {"sarney": ("instrumento_sem_medida", "2 episodios IBGE (jun/1987, jan/1989) + expurgos de 1986", "IBGE documenta 'represada' no IPC; efeito em pontos de indice nao medido", "IDX-IPC-1987;IDX-IPC-1989;IDX-IPC-1986"),
      "medici": ("instrumento_sem_medida", "1973 (literatura)", "dois indices contemporaneos divergem (CPDOC); nao ha medida propria", "IDX-1973")}
for g in GOVS:
    if g in k4:
        st, v, rz, ids = k4[g]
        sim("K4_represamento_ou_mudanca_de_regra_no_indice_de_precos", g, st, v, "episodios", rz, ids)
    else:
        sim("K4_represamento_ou_mudanca_de_regra_no_indice_de_precos", g, "sem achado", "", "", "nao localizado em IBGE/BCB nesta colheita; nao e prova de ausencia", "")

# K5: preco de combustivel na estatal
for g in GOVS:
    if g == "dilma":
        sim("K5_preco_de_combustivel_na_petrobras", g, "medido", "-41,0", "US$ bi (soma 2011-2014 do resultado do segmento derivados)", "Ipea, a partir das DFP da Petrobras; TCU sem merito julgado", "PETRO-2011-2014;PETRO-TCU")
    elif g == "lula3":
        sim("K5_preco_de_combustivel_na_petrobras", g, "instrumento_sem_medida", "ECDG 16/05/2023", "", "TCU acompanha; sem valor", "PETRO-ECDG-2023")
    else:
        sim("K5_preco_de_combustivel_na_petrobras", g, "sem dado", "", "", "resultado do segmento derivados nao colhido para este governo (a tabela do Ipea cobre 2006, 2010-2017); politica de precos de cada periodo nao lida", "")

# K6: reducao temporaria de tributo sobre combustiveis
k6 = {"dilma": ("medido", "CIDE: receita 8.924 (2011) para 13,8 (2014)", "R$ mi", "CIDE-2012-2015"),
      "temer": ("instrumento_sem_medida", "subvencao com teto de R$ 9,5 bi; valor pago nao medido", "R$ bi (teto)", "DIESEL-2018"),
      "bolsonaro": ("medido", "estimativas da Receita: 3.001,99 (2021); 14.932,41 e 16.511,22 (2022)", "R$ mi", "DIESEL-2021;LC192-2022;LC194-2022;LC194-COMSEFAZ"),
      "lula3": ("medido", "estimativas da Receita/EM: 25.000 e 6.610 (2023); compensacao aos estados R$ 27.014,9 mi (pela LC 194)", "R$ mi", "MP1157-2023;LC201-2023")}
for g in GOVS:
    if g in k6:
        st, v, u, ids = k6[g]
        sim("K6_reducao_temporaria_de_tributo_sobre_combustiveis", g, st, v, u, "estimativas oficiais ex-ante (Receita) ou receita observada (CIDE), nao comparaveis entre si; nao somar", ids)
    elif g in ("castelo", "costa_silva", "junta", "medici", "geisel", "figueiredo", "sarney", "collor", "itamar"):
        sim("K6_reducao_temporaria_de_tributo_sobre_combustiveis", g, "sem dado", "", "", "CIDE-combustiveis so existe desde a Lei 10.336 de 2001; outros tributos sobre combustiveis do periodo nao colhidos", "")
    elif g == "fhc":
        sim("K6_reducao_temporaria_de_tributo_sobre_combustiveis", g, "sem dado", "", "", "CIDE criada pela Lei 10.336/2001 e arrecadada desde 2002 (R$ 7.228 mi no ano); reducoes de aliquota no periodo nao colhidas", "")
    else:  # lula12
        sim("K6_reducao_temporaria_de_tributo_sobre_combustiveis", g, "sem dado", "", "", "a receita da CIDE cai de 7.939 (2007) para 5.934 (2008) e 4.828 (2009) e volta a 7.738 (2010); o instrumento nao foi lido, sem atribuicao de causa", "")

# K7: tarifa de energia diferida ou subsidiada
k7 = {"fhc": ("instrumento_sem_medida", "ate 2,9% e 7,9% sobre a tarifa (teto legal)", "% (teto)", "recuperacao do custo do racionamento de 2001; total em R$ nao medido", "ENER-RTE-2002"),
      "dilma": ("medido", "8.460 (2013) e 11.805 (2014) da Uniao na CDE; zero a partir de 2015", "R$ mi (orcado)", "CGU/Aneel; quotas dos consumidores sobem de 1.700 (2014) para 18.920 (2015)", "ENER-MP579-2012"),
      "bolsonaro": ("medido", "15,3", "R$ bi (emprestimo Conta Covid)", "amortizacao pela CDE entre 2021 e 2025", "ENER-COVID-2020"),
      "lula3": ("sem dado", "", "", "amortizacao da Conta Covid cai neste governo (2023-2025); valor por ano nao colhido", "ENER-COVID-2020")}
for g in GOVS:
    if g in k7:
        st, v, u, rz, ids = k7[g]
        sim("K7_tarifa_de_energia_diferida_ou_subsidiada", g, st, v, u, rz, ids)
    else:
        sim("K7_tarifa_de_energia_diferida_ou_subsidiada", g, "sem dado", "", "", "nao colhido para este governo", "")

# K8: desoneracao setorial temporaria
k8 = {"lula12": ("medido", "1.817 desonerado no 1o semestre de 2009; custo 559", "R$ mi", "IPI de automoveis; estudo do Ipea via TCU", "IPI-AUTO-2009;DESON-IPI-IR-2008-2012"),
      "dilma": ("medido", "folha: 22.107,3 (2014) e 25.199,1 (2015); IR+IPI bruto 2011: 77,23 e 2012: 85,20", "R$ mi (folha) e R$ bi (IR+IPI)", "DGT 2016 e TCU 713/2014; IPI de automoveis 2012-2014 sem valor proprio", "FOLHA-2011-2015;DESON-IPI-IR-2008-2012"),
      "temer": ("sem dado", "", "", "folha segue em vigor (14.546,6 projetado para 2016, 12.104,7 para 2018), mas nao ha ato novo do governo medido", "FOLHA-2011-2015"),
      "bolsonaro": ("sem dado", "", "", "folha segue em vigor (projecao de 10.155,4 para 2019); atos novos do governo (Desoneracoes Instituidas 2019 a 2022) nao triados para este tema", "FOLHA-2011-2015"),
      "lula3": ("sem dado", "", "", "MP 1.202/2023 mexe na folha (revoga parte da desoneracao); nao triada", "")}
for g in GOVS:
    if g in k8:
        st, v, u, rz, ids = k8[g]
        sim("K8_desoneracao_setorial_temporaria", g, st, v, u, rz, ids)
    else:
        sim("K8_desoneracao_setorial_temporaria", g, "sem dado", "", "", "nao colhido para este governo; DGT da Receita comeca em 2014", "")

with (HERE / "simetria-por-governo.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=S_COLS)
    w.writeheader()
    w.writerows(S)
print("simetria-por-governo.csv", len(S), "linhas")
