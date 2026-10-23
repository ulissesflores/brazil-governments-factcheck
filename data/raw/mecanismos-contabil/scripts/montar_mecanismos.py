"""Escreve mecanismos.csv. Cada linha e um mecanismo documentado; os numeros vem dos brutos desta pasta
(ver coluna fonte_primaria_url e RESULTADO.md). Texto autoral, sem rede. Uso: python3 -I montar_mecanismos.py <pasta_mecanismos>"""
import csv, pathlib, sys
base = pathlib.Path(sys.argv[1])
COLS = ["id","mecanismo","tipo","janela_inicio","janela_fim","governo_que_aplica","governo_que_paga","atribuicao","magnitude_medida","unidade","como_medida","reversao_medida","fonte_primaria_url","trecho_citado","camada_de_evidencia","vintage","nota"]
R = []
def add(**k):
    row = {c: k.get(c, "") for c in COLS}
    assert set(k) <= set(COLS), set(k) - set(COLS)
    R.append(row)
P = "https://www.planalto.gov.br/ccivil_03"
IBGE_NM1 = "https://biblioteca.ibge.gov.br/visualizacao/livros/liv102216.pdf"
RTN = "https://www.tesourotransparente.gov.br/ckan/dataset/ab56485b-9c40-4efb-8563-9ce3e1973c4b/resource/527ccdb1-3059-42f3-bf23-b5e3ab4c6dc6/download/seriehistoricajul26.xlsx"
VRTN = "RTN seriehistoricajul26.xlsx (Tesouro Nacional, jul/2026); valores sujeitos a revisao"

# ---------------- Bloco 1: atividades ilegais no PIB ----------------
add(id="MC01", mecanismo="Incluir comercializacao de drogas ilicitas (e jogos de azar, contrabando) no PIB: previsto na nova serie do SCN, NAO aplicado na serie vigente",
    tipo="mudanca_de_regra_estatistica", janela_inicio="2019-01-01", janela_fim="2027-12-31",
    governo_que_aplica="nenhum ate 2026-10-19 (nao_aplicavel: so planejado; publicacao prevista depois das eleicoes de 2026)", governo_que_paga="n/a",
    atribuicao="decisao_de_orgao_independente",
    magnitude_medida="nao medida: o IBGE nao publicou estimativa do efeito sobre o nivel do PIB", unidade="n/a",
    como_medida="leitura integral da Nota Metodologica n. 1 do SCN ref. 2021 (out/2025) e busca por 'ilegal/ilicit/droga/entorpec/prostitu/contraband/clandestin' em 21 das 22 notas metodologicas do SCN ref. 2010 (a 22a, 19_substituida, nao baixada)",
    reversao_medida="n/a (mudanca ainda nao publicada)",
    fonte_primaria_url=IBGE_NM1,
    trecho_citado="'novas estimativas de contrabando e jogos de azar; ... estimativa da comercializacao de drogas, estimativa de medidas liquidas ...' | 'O cronograma preliminar do projeto de mudanca de ano base ... preve a finalizacao e divulgacao dos resultados depois das eleicoes de 2026, em 2027' (IBGE, SCN ref. 2021, Nota Metodologica n. 1, v.1, out/2025)",
    camada_de_evidencia="dado", vintage="IBGE NM1 v.1 out/2025; busca em 2026-10-19",
    nota="Resposta a 'o Brasil incluiu trafico de drogas no PIB?': NAO na serie vigente (ref. 2010). Evidencia direta: a NM1 lista a estimativa de comercializacao de drogas como item NOVO da ref. 2021. Evidencia indireta: 0 mencoes a drogas/atividades ilegais em 20 das 21 notas 2010 lidas. Datas divergentes: a NM1 diz 'em 2027'; Aos Fatos e O Povo (citando nota do IBGE) dizem 2028; nao reconciliado (a pagina 'IBGE esclarece SCN', agencia 48080, deu 403 e nao foi lida). Mudanca iniciada em 2023 (NM1) com discussao desde 2019 e estimativa-teste em 2021 (nota do IBGE ao O Povo). Camara dos Deputados: RIC 2628/2026 pede quais atividades ilicitas constam dos modelos (so contexto, noticia de terceiros).")
add(id="MC02", mecanismo="Contrabando ja tem estimativa parcial na serie vigente (ref. 2010): usada para excluir contrabando da base do imposto de importacao",
    tipo="contabilidade", janela_inicio="2015-03-01", janela_fim="2026-10-19",
    governo_que_aplica="serie publicada desde mar/2015 (Dilma); retropolada a 1995", governo_que_paga="n/a", atribuicao="decisao_de_orgao_independente",
    magnitude_medida="nao informada na nota", unidade="n/a",
    como_medida="busca textual nas notas metodologicas SCN ref. 2010; unica ocorrencia na Nota 19 (margens e impostos)", reversao_medida="n/a",
    fonte_primaria_url="https://ftp.ibge.gov.br/Contas_Nacionais/Sistema_de_Contas_Nacionais/Notas_Metodologicas_2010/19_margens_e_impostos_20200928.pdf",
    trecho_citado="'Adicionalmente, para o imposto de importacao foram excluidos da base de calculo os valores decorrentes das estimativas de contrabando.' (IBGE, NM 19, secao 4.3.1)",
    camada_de_evidencia="dado", vintage="NM 19 versao 2020-09-28",
    nota="Limite do 'nao se aplica': a nota mostra que existe ALGUMA estimativa de contrabando na ref. 2010; nao informa se ela entra no valor adicionado/PIB nem a magnitude. A NM1 de 2025 chama de 'novas estimativas de contrabando' as da ref. 2021. Por isso MC01 vale com precisao para drogas; para contrabando o texto lido nao decide.")
add(id="MC03", mecanismo="Contexto: UE (ESA 2010) e Reino Unido incluem atividades ilegais no PIB desde 2014 (Blue Book 2014)",
    tipo="mudanca_de_regra_estatistica", janela_inicio="2014-09-01", janela_fim="2014-09-30",
    governo_que_aplica="n/a (nao brasileiro)", governo_que_paga="n/a", atribuicao="decisao_de_orgao_independente",
    magnitude_medida="nao coletada (o artigo do ONS 'Inclusion of illegal drugs and prostitution' nao foi lido)", unidade="n/a",
    como_medida="leitura do artigo do ONS 'Revisions to GDP in Blue Book 2016'", reversao_medida="n/a",
    fonte_primaria_url="https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/articles/nationalaccountsarticles/revisionstogrossdomesticproductinbluebook2016",
    trecho_citado="'improvements were implemented to the measurement of illegal activities in Blue Book 2014' (ONS, 2016). Aos Fatos (2026): 'Desde 2014 ... Italia, Reino Unido e Espanha passaram a contabilizar trafico de drogas, prostituicao e contrabando no calculo do PIB.'",
    camada_de_evidencia="literatura", vintage="ONS Blue Book 2016; Aos Fatos 2026-09",
    nota="So contexto, como pedido. A frase do ONS confirma 'illegal activities' em Blue Book 2014 e nao cita drogas no trecho lido; drogas/prostituicao vem do titulo do artigo do ONS referido no mesmo texto. A frase do Aos Fatos e secundaria. A obrigatoriedade na UE vem da nota do IBGE ao O Povo ('passou a ser obrigatoria para os paises da Uniao Europeia no meio da decada passada'), sem fonte primaria lida.")

# ---------------- Bloco 2: contabilidade fiscal ----------------
add(id="MC04", mecanismo="Cessao onerosa de 2010: R$ 74,8 bi de receita primaria do Tesouro, em troca de titulos a Petrobras (capitalizacao de R$ 42,9 bi lancada como despesa primaria)",
    tipo="antecipacao_de_receita", janela_inicio="2010-06-30", janela_fim="2010-12-31",
    governo_que_aplica="Lula (2o mandato)", governo_que_paga="Dilma Rousseff (e seguintes: o contrato da cessao foi revisado em 2019, nao lido aqui)",
    atribuicao="ato_de_governo", magnitude_medida="74,81 bi de receita (1,93% do PIB de 2010); efeito liquido sobre o primario de 2010 = 74,81 - 42,93 = 31,88 bi (0,82% do PIB)", unidade="R$ bilhoes correntes e % do PIB",
    como_medida="linha 1.4.8.1 do RTN (receitas de operacoes com ativos, 2010) e Quadros 4.3/4.4 do Relatorio Anual 2010 do BCB (cessao onerosa 74 808; capitalizacao da Petrobras 42 928, em R$ milhoes); PIB 2010 = 3.885.847 R$ mi (RTN)",
    reversao_medida="2019: Lei 13.885 (17/10/2019) trata dos leiloes dos volumes excedentes 'descontada a despesa decorrente da revisao do contrato de cessao onerosa'; a despesa da revisao nao foi lida e nao esta medida; a linha 1.4.8.1 do RTN nao repete valor desta ordem depois de 2010 (maximo posterior 12,4 bi em 2012)",
    fonte_primaria_url="https://www.bcb.gov.br/pec/boletim/banual2010/rel2010cap4p.pdf",
    trecho_citado="'impactos do ingresso de R$74,8 bilhoes, sem correspondencia no exercicio precedente, da receita decorrente da cessao onerosa de exploracao de petroleo no pre-sal' (BCB, Relatorio Anual 2010) | Lei 12.276/2010 art. 1 par. 3: 'O pagamento devido pela Petrobras ... devera ser efetivado prioritariamente em titulos da divida publica mobiliaria federal'",
    camada_de_evidencia="dado", vintage=VRTN + "; BCB RA 2010",
    nota="O 'efeito liquido' e conta deste dossie sobre duas linhas oficiais; a imprensa (Gazeta do Povo, nao baixada) traz 31,9 bi e diz que a meta de 2010 so foi cumprida com a capitalizacao: alegacao, nao verificada contra a meta oficial (a LDO 2010 foi alterada em 30/12/2010, ver MC13). Ligacao com MC06: a composicao dos R$ 93,3 bi de concessoes de 2019 nao esta aberta no RTN; os leiloes dos volumes excedentes da cessao onerosa (Lei 13.885/2019) sao candidatos a parte do valor, sem prova nesta pasta. Antes de qualquer rotulo 'antecipacao', o dado diz apenas: receita unica de 74,8 bi no primario de 2010; a contrapartida de 42,9 bi esta como despesa primaria.")
add(id="MC05", mecanismo="Fundo Soberano do Brasil: memorando do RTN de -R$ 14,2 bi em 2008 e +R$ 12,4 bi em 2012, este ultimo igual a linha de receitas de operacoes com ativos do mesmo ano",
    tipo="contabilidade", janela_inicio="2008-01-01", janela_fim="2012-12-31",
    governo_que_aplica="Lula (2o mandato) em 2008; Dilma em 2012", governo_que_paga="Dilma Rousseff (2012: receita extraordinaria) | indeterminado",
    atribuicao="ato_de_governo", magnitude_medida="2008: -14,24 bi (0,46% do PIB); 2012: +12,40 bi (0,26% do PIB)", unidade="R$ bilhoes correntes e % do PIB",
    como_medida="memorando 'Fundo Soberano do Brasil' e linha 1.4.8.1 do RTN; Quadro 4.2 do BCB RA 2010 (2008: 14 244)", reversao_medida="2012: o resgate zera o aporte de 2008 em ordem de grandeza (12,4 contra 14,2); nao ha reversao medida alem disso",
    fonte_primaria_url=RTN, trecho_citado="RTN, memorando 'Fundo Soberano do Brasil': 2008 = -14.244; 2012 = 12.400 (R$ milhoes); linha '1.4.8.1 d/q Receitas de Operacoes com Ativos' 2012 = 12.400",
    camada_de_evidencia="dado", vintage=VRTN, nota="Coincidencia exata 12.400 nas duas linhas e inferencia deste dossie (mesmo ano e valor), nao afirmacao do Tesouro.")
add(id="MC06", mecanismo="Concessoes e permissoes (bonus de assinatura) contadas como receita primaria no ano: pico de R$ 93,3 bi em 2019",
    tipo="antecipacao_de_receita", janela_inicio="2019-01-01", janela_fim="2019-12-31",
    governo_que_aplica="Bolsonaro", governo_que_paga="indeterminado (receita unica; custo para o seguinte nao medido)", atribuicao="indeterminado",
    magnitude_medida="93,28 bi (1,26% do PIB); media 1997-2025: 0,26% do PIB (calculo deste dossie sobre a linha 1.4.1)", unidade="R$ bilhoes correntes e % do PIB",
    como_medida="linha 1.4.1 Concessoes e Permissoes do RTN, tab. 2.2/2.2-A", reversao_medida="nao medida",
    fonte_primaria_url=RTN, trecho_citado="RTN tab. 2.2, linha '1.4.1 Concessoes e Permissoes', 2019 = 93.281 (R$ milhoes)",
    camada_de_evidencia="dado", vintage=VRTN, nota="A composicao do valor (quais leiloes) nao esta aberta na tabela lida; nao atribuo a nenhum leilao. Candidato: leiloes dos volumes excedentes da cessao onerosa (Lei 13.885, 17/10/2019, que fala em 'despesa decorrente da revisao do contrato de cessao onerosa'), ligado a MC04, sem prova nesta pasta. Outros picos: 1998 0,93% do PIB; 2013 0,41%; 2022 0,46% (ver series/rtn-resultado-primario-extraordinarias.csv).")
add(id="MC07", mecanismo="Pedaladas: atrasos de repasses do Tesouro a bancos publicos e ao FGTS em 2013-2014 (pagamentos a descoberto)",
    tipo="adiamento_de_despesa", janela_inicio="2013-01-01", janela_fim="2015-12-31",
    governo_que_aplica="Dilma Rousseff (2013-2014); a Caixa/FGTS/BNDES ja registram adiantamentos desde 2010 (MC08)", governo_que_paga="Dilma Rousseff (quitacao em dez/2015)",
    atribuicao="ato_de_governo", magnitude_medida="aprox. 40 bi (TCU Secom); passivo do Acordao 825/2015 = 55,6 bi (0,93% do PIB de 2015); total pago em 2015 = 72,4 bi (1,21% do PIB de 2015)", unidade="R$ bilhoes e % do PIB",
    como_medida="noticia oficial do TCU sobre o Acordao 3297/2015 (valor 'aproximadamente R$ 40 bilhoes') e nota do Ministerio da Fazenda (R$ 72,4 bi pagos em 2015; 55,6 bi passivo do Acordao; 16,8 bi de 2015)",
    reversao_medida="55,6 bi pagos em dez/2015 (nota da Fazenda); a LDO 2015 (Lei 13.199, 03/12/2015) deixou reduzir a meta em ate 57,013 bi pelo pagamento desses passivos",
    fonte_primaria_url="https://portal.tcu.gov.br/imprensa/noticias/tcu-analisa-recursos-da-uniao-e-do-banco-central-contra-decisao-sobre-pedaladas-fiscais",
    trecho_citado="TCU 14/12/2015: 'atrasos de repasses do Tesouro Nacional a bancos publicos oficiais em 2013 e 2014 ... Esses valores, que somam aproximadamente R$ 40 bilhoes' | Fazenda: 'O montante de R$ 72,4 bilhoes ... foi pago ao longo do ano de 2015, sendo que o passivo referido no Acordao do TCU foi de R$ 55,6 bilhoes, e os restantes R$ 16,8 bilhoes referentes as despesas do exercicio de 2015.'",
    camada_de_evidencia="decisao_de_orgao_de_controle", vintage="TCU Acordao 825/2015 (abr/2015) e 3297/2015 (09/12/2015, TC 021.643/2014-8); nota da Fazenda de fev/2016",
    nota="O numero de acordao citado no pedido (2.461/2015) NAO foi confirmado: busca nao achou documento com esse numero; os acordaos das pedaladas sao 825/2015 e 3297/2015 (cf. nota 10 do RTN). A nota da Fazenda foi lida em republicacao (jornalcontabil.com.br) e nao no site do Ministerio. Divergencia 40 vs 55,6: o TCU fala em 'aproximadamente' R$ 40 bi na noticia; a Fazenda usa 55,6 para o passivo do Acordao (concepcao diferente de base, nao reconciliada).")
add(id="MC08", mecanismo="Adiantamentos de CEF, FGTS e BNDES a Uniao para pagar programas (Bolsa Familia, Seguro-Desemprego, Abono, MCMV, PSI): omitidos das estatisticas de divida e de resultado primario",
    tipo="contabilidade", janela_inicio="2010-01-01", janela_fim="2014-12-31",
    governo_que_aplica="Lula (2o mandato, 2010) e Dilma (2011-2014)", governo_que_paga="Dilma Rousseff", atribuicao="ato_de_governo",
    magnitude_medida="R$ 37,5 bi de passivos da Uniao sem registro no BGU 2014; R$ 26,16 bi de creditos do BNDES contra o Tesouro em 31/12/2014 (R$ 23,9 bi so do PSI)", unidade="R$ bilhoes",
    como_medida="Parecer Previo do TCU sobre as contas de 2014 (TC 005.335/2015-9), itens 1-4 e item 6 da opiniao modificada sobre o BGU; o valor do BNDES vem de documento de defesa citado em acordao posterior (nao baixado)",
    reversao_medida="ver MC07 (quitacao em 2015)", fonte_primaria_url="https://www.camara.leg.br/internet/comissao/index/mista/orca/contas/2014/03-TCU_-_Contas_do_Governo_-_Exercicio_de_2014/01-TC-005335-2015-9-PARECER-PREVIO-MIN-AN-Exercicio_de_2014.pdf",
    trecho_citado="'adiantamentos concedidos pelo FGTS a Uniao para cobertura de despesas no ambito do Programa Minha Casa Minha Vida nos exercicios de 2010 a 2014' | 'adiantamentos concedidos pelo BNDES a Uniao para cobertura de despesas no ambito do Programa de Sustentacao do Investimento nos exercicios de 2010 a 2014' | 'Ausencia de registro de passivos da Uniao relativos a repasse de recursos de programas sociais, no valor de R$ 37,5 bilhoes'",
    camada_de_evidencia="decisao_de_orgao_de_controle", vintage="Parecer previo de 07/10/2015",
    nota="O parecer recomendou a REJEICAO das contas de 2014 (nao ocorria desde 1937, segundo a noticia do TCU); o Congresso nao e coberto aqui. A parte de 2010 (Lula) e citada pelo TCU sem valor separado por ano: 'sem dado' para a divisao por governo.")
add(id="MC09", mecanismo="Retificacao irregular de restos a pagar nao processados e demais distorcoes do Balanco Geral da Uniao 2014",
    tipo="contabilidade", janela_inicio="2014-01-01", janela_fim="2014-12-31",
    governo_que_aplica="Dilma Rousseff", governo_que_paga="indeterminado", atribuicao="ato_de_governo",
    magnitude_medida="subavaliacao do passivo nao financeiro em 185 bi (retificacao de RAP); ausencia de contingenciamento de pelo menos 28,54 bi; inscricao irregular de 1,367 bi em RAP do MCMV; subavaliacao da equivalencia patrimonial em 15 bi", unidade="R$ bilhoes",
    como_medida="Parecer Previo do TCU, fundamentos da opiniao modificada sobre o BGU (item 5) e irregularidades da execucao orcamentaria (itens 7 e 9)", reversao_medida="nao medida",
    fonte_primaria_url="https://www.camara.leg.br/internet/comissao/index/mista/orca/contas/2014/03-TCU_-_Contas_do_Governo_-_Exercicio_de_2014/01-TC-005335-2015-9-PARECER-PREVIO-MIN-AN-Exercicio_de_2014.pdf",
    trecho_citado="'Retificacao irregular dos Restos a Pagar nao processados, subavaliando o Passivo Nao Financeiro em R$ 185 bilhoes' | 'ausencia de contingenciamento de despesas discricionarias da Uniao no montante de pelo menos R$ 28,54 bilhoes, quando da edicao do Decreto 8.367/2014'",
    camada_de_evidencia="decisao_de_orgao_de_controle", vintage="Parecer previo de 07/10/2015", nota="Aponta distorcao do balanco (estoque de passivo), nao do resultado primario do ano.")
for (mid, ano_ldo, lei, texto, mag, un, nota_) in []: pass
add(id="MC10", mecanismo="Abatimento de despesas de investimento (PPI/PAC) da meta de resultado primario, com limites fixados na LDO",
    tipo="contabilidade", janela_inicio="2006-01-01", janela_fim="2015-12-31",
    governo_que_aplica="Lula (1o e 2o mandatos, 2006-2010); Dilma (2011-2015)", governo_que_paga="indeterminado (e regra de calculo da meta; a despesa abatida ocorre de fato)",
    atribuicao="decisao_legislativa",
    magnitude_medida="limites autorizados em lei (R$ bi): 2006: 3,0 | 2007: 4,59 (depois 11,283) | 2008: 13,825 | 2009: 15,567 (depois 28,5) | 2010: 22,5 (depois 29,8) | 2011: 32,0 | 2012: 40,6 | 2013: 45,2 (depois 65,2, incluindo desoneracoes) | 2014: 67,0 e, desde 15/12/2014, 'ate o montante' das desoneracoes e do PAC, sem teto numerico | 2015: 28,667 (PAC) na meta original", unidade="R$ bilhoes correntes (teto de autorizacao, nao valor usado)",
    como_medida="leitura do art. 3 das LDOs 2006-2015 e das leis que o alteraram (Leis 11.477/2007, 12.182/2009, 12.795/2013 e 13.053/2014; Planalto); LDOs 2001-2005 buscadas por clausula de reducao da meta: nenhuma encontrada no corpo da lei",
    reversao_medida="nao medida: o texto legal fixa so o teto; o valor efetivamente abatido por ano nao foi coletado",
    fonte_primaria_url=P + "/_ato2011-2014/2013/lei/l12919.htm",
    trecho_citado="LDO 2014 art. 3 (Lei 13.053, 15/12/2014): 'A meta de resultado a que se refere o art. 2o podera ser reduzida ate o montante das desoneracoes de tributos e dos gastos relativos ao Programa de Aceleracao do Crescimento - PAC' | LDO 2013 art. 3 (red. Lei 12.795/2013): 'pode ser reduzida em ate R$ 65.200.000.000,00 ... em face da realizacao dos investimentos prioritarios ... e de desoneracoes de tributos'",
    camada_de_evidencia="dado", vintage="Planalto, textos compilados acessados em 2026-10-19",
    nota="Medida em R$ nominais de cada ano; para %PIB ver simetria-por-governo.csv (PIB do RTN, 1997+). A regra existe de forma ININTERRUPTA de 2006 a 2015; em 2016-2017 as LDOs lidas nao trazem a clausula. Nenhum juizo: o abatimento tem origem legislativa e e publico.")
add(id="MC11", mecanismo="Meta de resultado primario (art. 2 da LDO) alterada durante o exercicio: 2009, 2010, 2013, 2015, 2016, 2017 (seis leis); as outras quatro leis modificadoras (2007, 2009-12, 2013, 2014) so mudaram o teto de abatimento, ver MC10",
    tipo="contabilidade", janela_inicio="2009-10-09", janela_fim="2017-09-13",
    governo_que_aplica="Lula (Lei 12.053 de 09/10/2009; Lei 12.377 de 30/12/2010); Dilma (Lei 12.901/2013; Lei 13.199 de 03/12/2015); Temer (Lei 13.291 de 25/05/2016, assinada por Michel Temer como interino; Lei 13.480 de 13/09/2017)",
    governo_que_paga="indeterminado", atribuicao="decisao_legislativa",
    magnitude_medida="2009: meta do setor publico consolidado de 3,80% para 2,50% do PIB | 2010: de 3,30% para 3,10% (Eletrobras excluida do calculo) em 30/12/2010 | 2011: de R$ 125,5 bi para R$ 117,89 bi | 2015: de superavit de R$ 66,3 bi para DEFICIT de R$ 48,9 bi (03/12/2015) | 2016: de superavit de R$ 30,554 bi para DEFICIT de R$ 163,9 bi (25/05/2016) | 2017: de deficit de R$ 143,1 para R$ 163,1 bi (13/09/2017)", unidade="% do PIB e R$ bilhoes",
    como_medida="comparacao do texto original e do texto alterado do art. 2 de cada LDO (Planalto) e do Quadro BCB RA 2010 para 2010",
    reversao_medida="nao se aplica (e mudanca da meta, nao da apuracao)",
    fonte_primaria_url=P + "/_ato2015-2018/2015/lei/l13199.htm",
    trecho_citado="Lei 13.199/2015 (LDO 2015) art. 2: 'resultado primario deficitario, para o setor publico consolidado nao financeiro, de R$ 48.908.400.000,00' (redacao anterior: superavit de R$ 66.325.000.000,00) | par. 4: 'A meta ... considera a receita de concessoes e permissoes relativas aos leiloes das Usinas Hidroeletricas - UHEs nao renovadas estimadas em R$ 11.050.000.000,00' | par. 5 II: a meta 'podera ser reduzida' pelo 'pagamento, em 2015, ate o montante de R$ 57.013.000.000,00, referente a passivos' ao FGTS, BNDES e outros",
    camada_de_evidencia="dado", vintage="Planalto, textos compilados acessados em 2026-10-19",
    nota="Contagem por governo na simetria: 2 / 2 / 2 (Lula, Dilma, Temer). Leis que mudaram so o teto de abatimento do art. 3 (MC10): 11.477/2007, 12.182/2009 (29/12/2009), 12.795/2013 e 13.053/2014 (15/12/2014). Data de 25/05/2016 cai no afastamento de Dilma (12/05/2016, Temer interino); mandatos.csv atribui o periodo a Dilma ate 31/08/2016, mas a lei traz a assinatura de Michel Temer: atribuido a Temer e marcado como ambiguidade. Mudanca da meta pode aproximar a meta do que e atingivel; o dado nao diz isso, so mostra a data e o tamanho.")
add(id="MC12", mecanismo="Exclusao de empresas estatais (Petrobras, depois Eletrobras) do calculo da meta do setor publico",
    tipo="contabilidade", janela_inicio="2009-01-01", janela_fim="2017-12-31",
    governo_que_aplica="Lula (Petrobras na LDO 2009; Eletrobras pela Lei 12.377 de 30/12/2010); Dilma e Temer (mantem)", governo_que_paga="indeterminado", atribuicao="decisao_legislativa",
    magnitude_medida="nao medida", unidade="n/a",
    como_medida="leitura do paragrafo 1 do art. 2 das LDOs 2009-2017", reversao_medida="n/a",
    fonte_primaria_url=P + "/_ato2007-2010/2010/lei/l12377.htm",
    trecho_citado="LDO 2010 art. 2 par. 1 (red. Lei 12.377/2010): 'As empresas dos Grupos Petrobras e Eletrobras nao serao consideradas na meta de resultado primario, de que trata o caput deste artigo, relativa ao Programa de Dispendios Globais.' | BCB RA 2010: Lei 12.377 'autorizou que fosse conferido tratamento especifico ao Grupo Eletrobras, excluindo-o do calculo do resultado fiscal do setor publico'",
    camada_de_evidencia="dado", vintage="Planalto 2026-10-19; BCB RA 2010", nota="Exclusao da meta nao altera a linha 'Governo Central' do RTN (usada nas series desta pasta). Ayres et al. (2018) descrevem que BNDES e Petrobras ficavam fora das estatisticas fiscais no periodo (MC21), sem quantificar nas linhas lidas.")
add(id="MC13", mecanismo="Regra de abatimento no ultimo dia do exercicio: LDO 2010 alterada em 30/12/2010 (meta 3,30% -> 3,10%) e LDO 2010 com abatimento PAC elevado em 29/12/2009 (22,5 -> 29,8 bi)",
    tipo="contabilidade", janela_inicio="2009-12-29", janela_fim="2010-12-30",
    governo_que_aplica="Lula (2o mandato)", governo_que_paga="indeterminado", atribuicao="decisao_legislativa",
    magnitude_medida="meta -0,20 p.p. do PIB; teto de abatimento +7,3 bi (de 22,5 para 29,8)", unidade="p.p. do PIB e R$ bilhoes",
    como_medida="BCB RA 2010 (texto: 'a meta de superavit primario para 2010 foi reduzida de 3,3% para 3,1% do PIB') e Leis 12.182/2009 e 12.377/2010 (Planalto)",
    reversao_medida="n/a", fonte_primaria_url="https://www.bcb.gov.br/pec/boletim/banual2010/rel2010cap4p.pdf",
    trecho_citado="'A Lei no 12.377, de 30 de dezembro de 2010, autorizou que fosse conferido tratamento especifico ao Grupo Eletrobras, excluindo-o do calculo do resultado fiscal do setor publico. Em consequencia, a meta de superavit primario para 2010 foi reduzida de 3,3% para 3,1% do PIB.' (BCB, RA 2010)",
    camada_de_evidencia="dado", vintage="BCB RA 2010", nota="O resultado primario do setor publico consolidado de 2010 nao foi coletado aqui (so Governo Central, 2,00% do PIB pela linha 5 do RTN); portanto nao ha comparacao meta x resultado.")
add(id="MC14", mecanismo="Restos a pagar: estoque inscrito para o exercicio seguinte, no fim de cada mandato (Lula 1-2 -> Dilma)",
    tipo="adiamento_de_despesa", janela_inicio="2010-12-31", janela_fim="2011-12-31",
    governo_que_aplica="Lula (1o e 2o mandatos)", governo_que_paga="Dilma Rousseff", atribuicao="indeterminado",
    magnitude_medida="128,9 bi inscritos em 31/12/2010 (3,32% do PIB de 2010)", unidade="R$ bilhoes correntes e % do PIB",
    como_medida="Tabela 2 do Relatorio de Avaliacao dos Restos a Pagar 2026 (Tesouro) e PIB do RTN", reversao_medida="no ano seguinte: pagos R$ 74,1 bi, cancelados R$ 16,6 bi, a pagar R$ 38,3 bi (reinscritos)",
    fonte_primaria_url="https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/thot/arquivos/publicacoes/53729_1689657/Relatorio%20RAP_2026.pdf",
    trecho_citado="Tabela 2, linha 2010/2011: Inscritos e Reinscritos 128,9; Cancelados 16,6; Pagos 74,1; A Pagar 38,3 (R$ bilhoes correntes)",
    camada_de_evidencia="dado", vintage="Relatorio RAP 2026 (Tesouro)", nota="O estoque de RAP inclui despesas financeiras; a serie so comeca em 31/12/2007 (62,5 bi). 'Sem dado' para os governos anteriores. RAP e instrumento orcamentario normal; o numero mede o tamanho do que passou ao governo seguinte, nao irregularidade.")
add(id="MC15", mecanismo="Restos a pagar: estoque no fim do mandato (Dilma -> Temer, referencia 31/12/2015)",
    tipo="adiamento_de_despesa", janela_inicio="2015-12-31", janela_fim="2016-12-31",
    governo_que_aplica="Dilma Rousseff", governo_que_paga="Michel Temer", atribuicao="indeterminado",
    magnitude_medida="185,7 bi inscritos em 31/12/2015 (3,10% do PIB de 2015); pico anterior: 228,0 bi em 31/12/2014 (3,95%)", unidade="R$ bilhoes correntes e % do PIB",
    como_medida="Tabela 2 do Relatorio RAP 2026; PIB do RTN", reversao_medida="no ano seguinte (2015/2016): pagos R$ 105,6 bi, cancelados R$ 21,2 bi, a pagar R$ 58,9 bi",
    fonte_primaria_url="https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/thot/arquivos/publicacoes/53729_1689657/Relatorio%20RAP_2026.pdf",
    trecho_citado="Tabela 2, linha 2015/2016: 185,7 | 21,2 | 105,6 | 58,9; linha 2014/2015: 228,0 | 34,6 | 121,6 | 71,9",
    camada_de_evidencia="dado", vintage="Relatorio RAP 2026", nota="O mandato de Dilma terminou em 31/08/2016 (mandatos.csv); o estoque de 31/12/2016 (148,2 bi) ja e do governo seguinte. Escolhi 31/12/2015 por ser o ultimo 31/12 sob Dilma. O relatorio de 2019 diz que a queda de 2016/2017 em RAP processados decorre de mudanca de sistematica de pagamento de beneficios do INSS.")
add(id="MC16", mecanismo="Restos a pagar: estoque no fim do mandato (Temer -> Bolsonaro, 31/12/2018)",
    tipo="adiamento_de_despesa", janela_inicio="2018-12-31", janela_fim="2019-12-31",
    governo_que_aplica="Michel Temer", governo_que_paga="Jair Bolsonaro", atribuicao="indeterminado",
    magnitude_medida="189,6 bi inscritos em 31/12/2018 (2,71% do PIB de 2018)", unidade="R$ bilhoes correntes e % do PIB",
    como_medida="Tabela 2 do Relatorio RAP 2026; PIB do RTN", reversao_medida="2018/2019: pagos R$ 114,9 bi, cancelados R$ 29,8 bi, a pagar R$ 44,8 bi",
    fonte_primaria_url="https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/thot/arquivos/publicacoes/53729_1689657/Relatorio%20RAP_2026.pdf",
    trecho_citado="Tabela 2, linha 2018/2019: 189,6 | 29,8 | 114,9 | 44,8. Relatorio 2019: 'R$ 34,0 bilhoes (99,6%) se referem a mudanca na sistematica de pagamento de despesas associada a emissao da ordem bancaria'",
    camada_de_evidencia="dado", vintage="Relatorio RAP 2026 e 2019", nota="Aumento de 34,0 bi do estoque de 2018 para 2019 e efeito de calendario de pagamento (ordem bancaria), nao de fluxo, segundo o proprio Tesouro.")
add(id="MC17", mecanismo="Restos a pagar: estoque no fim do mandato (Bolsonaro -> Lula 3, 31/12/2022) e posicao em 31/12/2025",
    tipo="adiamento_de_despesa", janela_inicio="2022-12-31", janela_fim="2025-12-31",
    governo_que_aplica="Jair Bolsonaro", governo_que_paga="Lula (3o mandato)", atribuicao="indeterminado",
    magnitude_medida="255,1 bi inscritos em 31/12/2022 (2,53% do PIB); 391,5 bi em 31/12/2025 (3,07% do PIB), ja sob Lula 3", unidade="R$ bilhoes correntes e % do PIB",
    como_medida="Tabela 2 do Relatorio RAP 2026; PIB do RTN", reversao_medida="2022/2023: pagos R$ 183,5 bi, cancelados R$ 15,7 bi, a pagar R$ 55,8 bi",
    fonte_primaria_url="https://cdn.tesouro.gov.br/sistemas-internos/apex/producao/sistemas/thot/arquivos/publicacoes/53729_1689657/Relatorio%20RAP_2026.pdf",
    trecho_citado="Relatorio RAP 2026: 'Do aumento de R$ 79,1 bilhoes ... despesas financeiras, cujo aumento de R$ 65,4 bilhoes representou 82,7%'",
    camada_de_evidencia="dado", vintage="Relatorio RAP 2026", nota="O ultimo valor (391,5 bi) e do governo em curso: nao e herdado por ninguem ainda. 82,7% da alta de 2025/2026 e de despesas financeiras, nao primarias.")
add(id="MC18", mecanismo="Gasto tributario federal (renuncia de receita estimada pela RFB) em % do PIB",
    tipo="contabilidade", janela_inicio="2007-01-01", janela_fim="2026-12-31",
    governo_que_aplica="todos os governos 2007-2026 (serie descontinua)", governo_que_paga="n/a", atribuicao="decisao_legislativa",
    magnitude_medida="3,60% (2010) a 4,66% (2013) nos anos 2007-2013; 4,30% (2019), 4,32% (2020), 4,67% (2021), 4,89% (2022), 4,88% (2023) em bases efetivas; projecoes PLOA: 4,59% (2024), 4,40% (2025), 4,43% (2026)", unidade="% do PIB",
    como_medida="Quadro VI de cada edicao do DGT (Receita Federal) lido do .xlsx; 2007-2013 vem da Nota Tecnica Ipea n. 19 (rotulos do Grafico 2, citando a RFB)",
    reversao_medida="n/a", fonte_primaria_url="https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/relatorios/renuncia/gastos-tributarios-bases-efetivas",
    trecho_citado="DGT Bases Efetivas 2023, Quadro VI: TOTAL 534.030.416.744,70 (4,88% do PIB; PIB 10.943.344.667.905)",
    camada_de_evidencia="dado", vintage="DGT Bases Efetivas 2019-2023; DGT PLOA 2024-2026; Ipea NT 19 (2016)",
    nota="Lacunas: 2003-2006, 2014-2018 e todos os anos antes de 2003 ('sem dado'); o blog do FGV IBRE (bruto/ibre-desafios-gastos-tributarios.html) cita 2,1% do PIB em 2002 e 6,9% projetados para 2024, mas e o total federal + estadual (a mesma serie no relatorio IDOS diz federal ~4,5% e total ~7% em 2023-2024), logo nao e a serie federal e nao entra aqui. O valor e projecao em 2024-2026. A EC 109/2021 (art. 4) manda o Presidente enviar, em 6 meses, plano de reducao gradual de incentivos e beneficios federais de natureza tributaria cujas proposicoes levem 'esse montante, no prazo de ate 8 (oito) anos' a nao ultrapassar '2% (dois por cento) do produto interno bruto' (par. 1, II), com excecoes (par. 2); o escopo exato do 'montante' (se igual ao gasto tributario do DGT) nao foi conferido. Metodo (perda de arrecadacao, sem resposta comportamental) e estavel segundo o relatorio IDOS/CIAT, mas as edicoes mudam a lista de itens; compare so dentro de uma edicao.")
add(id="MC19", mecanismo="Teto de gastos (EC 95/2016): limite de despesa primaria corrigido por IPCA de junho; novo indexador em 2021",
    tipo="contabilidade", janela_inicio="2016-12-15", janela_fim="2023-08-31",
    governo_que_aplica="Michel Temer (criou); Bolsonaro (alterou o indexador)", governo_que_paga="n/a", atribuicao="decisao_legislativa",
    magnitude_medida="EC 95: limite de 2017 = despesa de 2016 corrigida em 7,2%; anos seguintes IPCA acumulado em 12 meses ate junho. EC 113/2021 (08/12/2021): passa ao IPCA do exercicio anterior (dez/dez). IFI (RAF 60, jan/2022): Orcamento 2022 aprovado com deficit de R$ 79,4 bi; IFI projeta R$ 106,2 bi (1,1% do PIB); Auxilio Brasil R$ 54,6 bi e emendas de relator R$ 16,5 bi 'possibilitados' pelo espaco aberto", unidade="% e R$ bilhoes",
    como_medida="texto das ECs 95, 113, 114 (Planalto) e leitura do RAF 60 da IFI (3 paginas)",
    reversao_medida="LC 200/2023 substituiu o teto (MC22)", fonte_primaria_url=P + "/constituicao/emendas/emc/emc113.htm",
    trecho_citado="EC 95 art. 107 par. 1 I: 'a despesa primaria paga no exercicio de 2016 ... corrigida em 7,2%'; II: 'IPCA ... para o periodo de doze meses encerrado em junho do exercicio anterior' | EC 113 art. 107 par. 1 II: 'IPCA ... apurado no exercicio anterior a que se refere a lei orcamentaria' | IFI RAF 60: 'Emendas Constitucionais no 113 e no 114, que restringiram o pagamento de precatorios pela Uniao e abriram espaco no teto de gastos'",
    camada_de_evidencia="dado", vintage="Planalto 2026-10-19; IFI RAF 60 (jan/2022)",
    nota="A IFI e fonte oficial do Senado, mas o resumo de 3 paginas nao traz o numero de 'espaco' no teto de 2022 (a imprensa cita R$ 112,6 bi/117,9 bi: alegacao, nao verificada). A EC 114 (16/12/2021) fixa limite de precatorios (art. 107-A) ate 2026 e destina o espaco a programa social e a seguridade; o STF invalidou o limite a partir de 2023 (Conjur, nao baixado).")
add(id="MC20", mecanismo="Estado de emergencia em 2022 (EC 123/2022): beneficios fora da meta e do teto, ano eleitoral",
    tipo="contabilidade", janela_inicio="2022-07-14", janela_fim="2022-12-31",
    governo_que_aplica="Jair Bolsonaro", governo_que_paga="n/a (despesa de 2022, via credito extraordinario)", atribuicao="decisao_legislativa",
    magnitude_medida="soma dos limites de despesa do art. 5 = R$ 41,25 bi (Auxilio Brasil +R$ 200 por 5 meses ate R$ 26 bi; gas R$ 1,05 bi; caminhoneiros R$ 5,4 bi; transporte publico R$ 2,5 bi; auxilio a estados com etanol ate R$ 3,8 bi; demais incisos R$ 2,0 e 0,5 bi) = 0,41% do PIB de 2022 (R$ 10.079.677 mi)", unidade="R$ bilhoes e % do PIB",
    como_medida="soma, feita por este dossie, dos tetos de cada inciso do art. 5 da EC 123, sem contar o valor unitario R$ 200, o auxilio unitario R$ 1.000 e a parcela mensal de R$ 760 mi (que ja esta dentro do teto de R$ 3,8 bi do inciso V = 5 x 0,76); PIB do RTN",
    reversao_medida="STF declarou inconstitucionais trechos da EC 123 em 01/08/2024 (ADI 7212; noticia SBT, nao baixada), com efeitos ja exauridos segundo comentario juridico (alegacao)",
    fonte_primaria_url=P + "/constituicao/emendas/emc/emc123.htm",
    trecho_citado="EC 123 art. 120 par. unico I b (ADCT): as despesas 'nao serao consideradas para fins de apuracao da meta de resultado primario ... e do limite estabelecido para as despesas primarias, conforme disposto no inciso I do caput do art. 107'",
    camada_de_evidencia="dado", vintage="Planalto 2026-10-19", nota="Bate com os R$ 41,25 bi da imprensa. Uma soma ingenua dos valores em reais do artigo da R$ 42,01 bi porque conta duas vezes a parcela mensal de R$ 760 mi do inciso V (teto de R$ 3,8 bi = 5 parcelas). O que consta do texto e o teto de gasto por inciso, nao o gasto realizado.")
add(id="MC21", mecanismo="PEC da Transicao (EC 126/2022): limite do teto de 2023 acrescido de R$ 145 bi, fora da meta primaria",
    tipo="contabilidade", janela_inicio="2022-12-21", janela_fim="2023-12-31",
    governo_que_aplica="Lula (3o mandato) executa em 2023; emenda promulgada em 21/12/2022 (periodo Bolsonaro, equipe de transicao)", governo_que_paga="indeterminado", atribuicao="decisao_legislativa",
    magnitude_medida="145,0 bi = 1,33% do PIB de 2023 (R$ 10.943.345 mi); mais R$ 9,85 bi de emendas do relator-geral", unidade="R$ bilhoes e % do PIB",
    como_medida="texto da EC 126, art. 3 e par. 8; PIB do RTN", reversao_medida="nao medida", fonte_primaria_url=P + "/constituicao/emendas/emc/emc126.htm",
    trecho_citado="'O limite estabelecido no inciso I do caput do art. 107 ... fica acrescido em R$ 145.000.000.000,00 ... para o exercicio financeiro de 2023.' Par. unico: 'nao serao consideradas para fins de verificacao do cumprimento da meta de resultado primario'",
    camada_de_evidencia="dado", vintage="Planalto 2026-10-19", nota="O resultado primario de 2023 foi -2,09% do PIB (RTN linha 5), sem a identificacao de quanto veio da ampliacao.")
add(id="MC22", mecanismo="Novo arcabouco fiscal (LC 200/2023): limites individualizados de despesa primaria com crescimento real vinculado a receita",
    tipo="contabilidade", janela_inicio="2023-08-30", janela_fim="2026-10-19",
    governo_que_aplica="Lula (3o mandato)", governo_que_paga="n/a", atribuicao="decisao_legislativa",
    magnitude_medida="nao medida nesta rodada", unidade="n/a", como_medida="leitura do art. 3 da LC 200 (Planalto); LC sob contestacao no STF (ADIs 7641, 7922, 8010, 7064 referidas no texto compilado)",
    reversao_medida="n/a", fonte_primaria_url=P + "/leis/lcp/lcp200.htm",
    trecho_citado="LC 200 art. 3: 'ficam estabelecidos, para cada exercicio a partir de 2024 ... limites individualizados para o montante global das dotacoes orcamentarias relativas a despesas primarias'",
    camada_de_evidencia="dado", vintage="Planalto 2026-10-19", nota="Exclusoes especificas da meta e do limite em 2024-2026 (calamidade no RS, precatorios) nao foram coletadas: 'sem dado'.")

# ---------------- Pre-1988 ----------------
add(id="MC23", mecanismo="Conta Movimento do Banco do Brasil no Banco Central e orcamento monetario: despesas financiadas fora do orcamento do Congresso",
    tipo="contabilidade", janela_inicio="1964-04-15", janela_fim="1986-03-10",
    governo_que_aplica="Castelo Branco, Costa e Silva, Junta, Medici, Geisel, Figueiredo e Sarney (ate mar/1986)", governo_que_paga="inflacao/senhoriagem e, apos 1986-1988, divida publica (sem decomposicao nas fontes lidas)",
    atribuicao="ato_de_governo", magnitude_medida="transferencias (residuo) entre BC e BB e outras operacoes fora do orcamento: 0,5% do PIB/ano (1960-64); 1,1 (1965-72); 1,6 (1973-80); -4,5 (1981-94)", unidade="% do PIB por ano (media do subperiodo)",
    como_medida="Ayres, Garcia, Guillen & Kehoe (NBER w25421), tabela 1, linha 8 'transfers (residual)' = (1)+(2)+(3)+(4)-(5)-(6)-(7)",
    reversao_medida="Conta Movimento congelada em 1986 (Plano Cruzado); substituida pela Conta de Suprimentos Especiais ate 1988; STN criada pelo Decreto 92.452 de 10/03/1986",
    fonte_primaria_url="https://www.nber.org/papers/w25421",
    trecho_citado="'the government operated at least three budgets: one that was discussed in Congress ..., the monetary budget that was controlled by the National Monetary Council ..., and the budget of the SOEs' | 'the end of the Conta de Movimento between the central bank and the Bank of Brazil. In practice, however, that only took place after 1988 because another account ..., Conta de Suprimentos Especiais, replaced Conta de Movimento until its extinction in 1988' (Ayres et al. 2018)",
    camada_de_evidencia="literatura", vintage="NBER w25421 (2018), copia em ../monetario/referencias/ayres.txt",
    nota="O 'residuo' e a conta do artigo, que o proprio texto chama de aproximacao do deficit do orcamento monetario; nao e a Conta Movimento isolada, e o sinal muda em 1981-94. Nao ha numero por governo, so por subperiodo. Para o texto oficial: Tesouro, 'Historia do Tesouro Nacional': STN criada em 10/03/1986 'incorporando as funcoes fiscais ate entao exercidas pelo Banco Central e pelo Banco do Brasil' e 'substituicao da conta movimento do governo no Banco do Brasil pela Conta Unica do Tesouro Nacional no Banco Central e a unificacao dos orcamentos federais'.")
add(id="MC24", mecanismo="Estatais e bancos publicos fora das estatisticas fiscais e 'contabilidade criativa' 2008-2014",
    tipo="contabilidade", janela_inicio="2008-01-01", janela_fim="2014-12-31",
    governo_que_aplica="Lula (2o mandato) e Dilma", governo_que_paga="indeterminado", atribuicao="ato_de_governo",
    magnitude_medida="nao quantificada nas linhas lidas", unidade="n/a", como_medida="descricao em Ayres et al. (2018), secao 3 final", reversao_medida="n/a",
    fonte_primaria_url="https://www.nber.org/papers/w25421",
    trecho_citado="'neither BNDES nor Petrobras was included in the public-sector fiscal statistics in that time, they did not show up in the official statistics. In fact, in those years the government started to implement budget maneuvers to artificially inflate its primary surplus to meet the fiscal policy targets ... popularly known as contabilidade criativa (creative accounting)'",
    camada_de_evidencia="literatura", vintage="NBER w25421 (2018)", nota="Qualificacao dos autores; o dossie so registra e liga aos itens medidos MC04-MC13.")

# ---------------- Bloco 3: estatistica ----------------
add(id="MC25", mecanismo="1973: indices de custo de vida registraram precos tabelados, nao os pagos no mercado paralelo; subestimacao reconhecida pelo governo em 1977",
    tipo="represamento_de_preco", janela_inicio="1973-01-01", janela_fim="1974-12-31",
    governo_que_aplica="Medici", governo_que_paga="Geisel (reajuste salarial indexado ao indice de 1973; campanha dos 34,1% em 1977; CPI na Camara)",
    atribuicao="ato_de_governo", magnitude_medida="dez/72-dez/73: Guanabara/FGV 13,71%; Sao Paulo/Bolsa de Mercadorias 14,05%; Belo Horizonte/UFMG 13,08%; Sao Paulo/DIEESE 26,68%; Curitiba/BDPR 33,33%; IGP-DI 15,5% (calculo deste dossie, Ipeadata); IGP-DI 1974: 34,5%", unidade="% a.a.",
    como_medida="relatorio comparativo de indices de custo de vida (nota 4 do artigo da RAE) e IGP-DI dez/dez do Ipeadata", reversao_medida="IGP-DI 1974 = 34,5% (contra 15,5% em 1973); DIEESE estimou perdas salariais de 34,1% para 1973-1974",
    fonte_primaria_url="https://periodicos.fgv.br/rbe/article/download/350/7759",
    trecho_citado="'Segundo sua analise [Mario Henrique Simonsen, 1977], na tentativa de manter a taxa de inflacao em torno de 12% em 1973 o Governo tabelou os precos de inumeros produtos ... Estes tabelamentos, feitos a niveis irrealistas, foram responsaveis pelo surgimento de mercados paralelos ... Os indices de precos, entretanto, registraram os precos tabelados e nao aqueles praticados no mercado negro' (M. S. Bastos Marques, Rev. Bras. Economia, descrevendo o documento do ministro da Fazenda de 1977)",
    camada_de_evidencia="literatura", vintage="RBE (Bastos Marques); DIEESE Memoria; Atlas FGV verbete 3036",
    nota="O mecanismo documentado e PRECO TABELADO capturado pelo indice, nao troca de metodo; a atribuicao do tabelamento e do governo, a do calculo do indice e da FGV (sem evidencia lida de interferencia na formula): marcado ato_de_governo para o tabelamento. O 'relatorio secreto do Banco Mundial' e o reconhecimento pelo Banco Mundial aparecem so em Atlas FGV e Memoria DIEESE (alegacao/literatura secundaria): o relatorio de 1977 nao foi achado. A cifra '22,5%' atribuida ao Banco Mundial por um blog NAO foi verificada e NAO e usada. CPDOC (Atlas verbete 6001): ICV-RJ 12,6% contra 26,1% do DIEESE em media (historia/RESULTADO.md).")
add(id="MC26", mecanismo="Plano Cruzado (1986): series do INPC/IPCA em cruzeiros encerradas em 28/02/1986; expurgo do emprestimo compulsorio no IPC de jul/ago de 1986",
    tipo="mudanca_de_regra_estatistica", janela_inicio="1986-02-28", janela_fim="1986-11-21",
    governo_que_aplica="Sarney", governo_que_paga="Sarney", atribuicao="ato_de_governo",
    magnitude_medida="serie 'fevereiro-linha'; efeito do compulsorio expurgado em jul e ago/1986 (nao quantificado)", unidade="n/a",
    como_medida="apendice do IBGE 'Revisoes metodologicas, utilizacao e vigencia dos indices do SNIPC'", reversao_medida="n/a",
    fonte_primaria_url="https://biblioteca.ibge.gov.br/visualizacao/livros/liv65477.pdf",
    trecho_citado="'julho de 1986 - Foi instituido o chamado \"emprestimo compulsorio\" sobre combustiveis e automoveis, sendo expurgado seu efeito sobre o IPC de julho e de agosto. Instrumento legal - Decreto-Lei no 2.288, de 23.07.1986' (IBGE)",
    camada_de_evidencia="dado", vintage="IBGE SNIPC 7a ed.", nota="Decreto-lei 2.290/1986 (nov/1986) mudou o IPC para base INPC; a CPDOC chama o pacote de Cruzado II de 'expurgo' de itens supérfluos (historia/RESULTADO.md); decreto nao lido no Planalto.")
add(id="MC27", mecanismo="IPC 'represado' no plano: coleta de 35 dias em jun/1987 e 12 em jul; 51 dias em jan/1989 e 11 em fev",
    tipo="represamento_de_preco", janela_inicio="1987-06-12", janela_fim="1989-02-28",
    governo_que_aplica="Sarney", governo_que_paga="Sarney", atribuicao="ato_de_governo",
    magnitude_medida="jun/1987: 35 dias de coleta (jul: 12); jan/1989: 51 dias (fev: 11), contra ~30 dias de um mes", unidade="dias de coleta por indice mensal",
    como_medida="apendice do IBGE ao Sistema Nacional de Indices de Precos ao Consumidor (7a ed.)", reversao_medida="o IPC do mes seguinte capta so 12 e 11 dias: compensacao interna ao par de meses",
    fonte_primaria_url="https://biblioteca.ibge.gov.br/visualizacao/livros/liv65477.pdf",
    trecho_citado="'Como no Plano Cruzado, o governo determinou que a inflacao ocorrida ate o dia da divulgacao do Plano (15.06) seria \"represada\" no IPC correspondente ao mes de junho ... o IPC de junho captou a inflacao ocorrida em 35 dias, e o de julho, em 12 dias.' | 'janeiro de 1989 ... o IPC de janeiro captou a inflacao ocorrida em 51 dias, enquanto o IPC de fevereiro, em 11 dias.' (IBGE)",
    camada_de_evidencia="dado", vintage="IBGE SNIPC 7a ed.", nota="Ato legal: Decreto-Lei 2.335/1987 e Portaria 186/1987 (Fazenda); em 1989, plano de janeiro (Lei 7.730). O efeito em pontos percentuais do IPC nao foi coletado (a serie SGS 433 e IPCA, nao IPC). Rotulado 'represamento' porque o proprio IBGE usa a palavra.")
add(id="MC28", mecanismo="1990-1991: indexador IRVF com subitem aluguel igualado ao BTN (jun-out/1990) e extincao do IPC por 'orientacao ministerial' (fev/1991 ultimo IPC)",
    tipo="mudanca_de_regra_estatistica", janela_inicio="1990-05-30", janela_fim="1991-03-01",
    governo_que_aplica="Collor", governo_que_paga="Collor/Itamar (indexacao subsequente por TR; IRSM ate ago/1991)", atribuicao="ato_de_governo",
    magnitude_medida="nao medida (sem sobreposicao nos dados baixados)", unidade="n/a",
    como_medida="apendice do IBGE; MP 189/1990; Lei 8.177 e 8.178 de 01/03/1991", reversao_medida="n/a",
    fonte_primaria_url="https://biblioteca.ibge.gov.br/visualizacao/livros/liv65477.pdf",
    trecho_citado="'No ato de sua criacao, determinou-se que, entre junho de 1990 e outubro de 1990, a variacao do subitem \"aluguel\" seria igual a variacao do BTN no mes anterior' | 'extincao do IRVF e do ICB, atraves da Lei no 8.177 de 01.03.1991 e extincao do IPC, atraves de orientacao ministerial' (IBGE)",
    camada_de_evidencia="dado", vintage="IBGE SNIPC 7a ed.", nota="Ver quebras/quebras.csv para o ponto de vista de 'quebra de serie'. Para 1990 existem IPCA e INPC continuos no BCB: IPCA 67,55% (jan), 75,73% (fev) e 82,39% (mar/1990).")
add(id="MC29", mecanismo="IPCA: media geometrica para o subitem (jan/1994)",
    tipo="mudanca_de_regra_estatistica", janela_inicio="1994-01-01", janela_fim="1994-01-31",
    governo_que_aplica="Itamar Franco", governo_que_paga="indeterminado", atribuicao="decisao_de_orgao_independente",
    magnitude_medida="nao medida (direcao 'reduz' inferida pela desigualdade entre medias; nao medida)", unidade="n/a",
    como_medida="registro do IBGE; ver quebras/quebras.csv", reversao_medida="n/a", fonte_primaria_url="https://biblioteca.ibge.gov.br/visualizacao/livros/liv65477.pdf",
    trecho_citado="'Ate dezembro de 1993, o indice de um subitem ... era obtido ... atraves da media aritmetica simples. [...] de janeiro de 1994, a variacao do subitem passou a ser calculada utilizando-se a media geometrica dos relativos dos produtos.' (IBGE)",
    camada_de_evidencia="dado", vintage="IBGE SNIPC 7a ed.", nota="Sem evidencia de interferencia do governo: atribuido ao IBGE.")
add(id="MC30", mecanismo="IPCA: trocas de estrutura de pesos pela POF (1999, 2006, 2012, 2020) e cobertura geografica (2014, 2018)",
    tipo="mudanca_de_regra_estatistica", janela_inicio="1999-08-01", janela_fim="2020-01-31",
    governo_que_aplica="FHC (1999-08), Lula (2006-07), Dilma (2012-01 e 2014-01), Temer (2018-05), Bolsonaro (2020-01)", governo_que_paga="n/a", atribuicao="decisao_de_orgao_independente",
    magnitude_medida="efeito da troca de cesta (contrafactual do BCB), p.p./ano: 1999: +0,71 antes e +0,06 depois; 2006: +0,40 / -0,34; 2012: -0,49 / -0,56; 2017-2019: -0,09 (cesta nova menos antiga)", unidade="p.p. ao ano",
    como_medida="BCB Estudo Especial 70 e Relatorio de Inflacao dez/2019, reaproveitados de ../quebras/quebras.csv", reversao_medida="n/a",
    fonte_primaria_url="https://www.bcb.gov.br/conteudo/relatorioinflacao/EstudosEspeciais/EE070_Impacto_de_atualizacao_da_cesta.pdf",
    trecho_citado="ver ../quebras/quebras.csv, linhas IPCA 1999-08, 2006-07, 2012-01, 2020-01", camada_de_evidencia="dado", vintage="../quebras/quebras.csv (2026-10-19)",
    nota="Decisao do IBGE (orgao independente); sem evidencia, na fonte lida, de interferencia do governo. O sinal troca no mesmo mecanismo (+0,40 e -0,34 em 2006), portanto o mecanismo nao e sistematicamente favoravel nem desfavoravel.")
add(id="MC31", mecanismo="PIB: trocas de metodo e de ano de referencia (1990-91, 1995-96, 2007, 2015)",
    tipo="mudanca_de_regra_estatistica", janela_inicio="1990-01-01", janela_fim="2015-03-31",
    governo_que_aplica="Collor (IBGE assume as contas em 1990), Lula (mar/2007, ref. 2000), Dilma (mar/2015, ref. 2010)", governo_que_paga="n/a", atribuicao="decisao_de_orgao_independente",
    magnitude_medida="mar/2007: taxa de 2000 de 4,4 para 4,3 (-0,1 p.p.), de 2005 de 2,3 para 2,9 (+0,6 p.p.); nivel corrente +7,1% (2000) e +10,9% (2005) | mar/2015: crescimento medio 2000-2011 de 3,5 para 3,7% (+0,2 p.p./ano), PIB corrente +2,1%, investimento 2010 de 19,5 para 20,6%", unidade="p.p. e % do nivel",
    como_medida="releases do IBGE reaproveitados de ../quebras/quebras.csv", reversao_medida="n/a", fonte_primaria_url="https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/972",
    trecho_citado="ver ../quebras/quebras.csv, linhas PIB 2007-03 e 2015-03", camada_de_evidencia="dado", vintage="../quebras/quebras.csv",
    nota="Decisao do IBGE; na revisao de 2015 o ano-base novo vem com retropolacao da serie. O mecanismo e simetrico: o nivel sobe para todos os anos retropolados.")

with open(base / "mecanismos.csv", "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(R)
print(len(R), "mecanismos")
