# quebras.csv: uma linha por quebra metodologica ou de vintage. Toda citacao e verificada, caractere a caractere, contra o arquivo local
# (citacoes.py); numeros de "efeito_medido" vem de saida/medidas.json (calculado por calc.py), nunca digitados.
# Rode: python3 -I calc.py && python3 -I gerar_quebras.py
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import citacoes  # noqa: E402

H = pathlib.Path(__file__).resolve().parent
M = json.load(open(H / "saida" / "medidas.json"))
EM = json.load(open(H / "saida" / "efeito_mecanico_resumo.json")) if (H / "saida" / "efeito_mecanico_resumo.json").exists() else {}


def n(x, nd=2, sinal=False):
    s = f"{x:+.{nd}f}" if sinal else f"{x:.{nd}f}"
    return s.replace(".", ",")


LINHAS = []
FALHAS = []


def q(indicador, serie, data, antigo, novo, razao, url, chave, trecho, direcao, como_dir, efeito, como_medido, aprim, celulas, tipo):
    if trecho != "n/a":
        try:
            citacoes.verifica(chave, trecho)
        except AssertionError as e:
            FALHAS.append(f"{indicador} | {data}: {e}")
    assert direcao in ("eleva", "reduz", "ambigua", "desconhecida"), direcao
    assert aprim in ("sim", "nao", "nao_declarado"), aprim
    assert tipo in ("metodo_estatistico", "mudanca_de_regra", "revisao_de_vintage"), tipo
    LINHAS.append({"indicador": indicador, "serie": serie, "data_quebra": data, "metodo_antigo": antigo, "metodo_novo": novo,
                   "razao_declarada_pela_fonte": razao, "fonte_primaria_url": url, "trecho_citado": trecho, "direcao_do_efeito": direcao,
                   "como_a_direcao_foi_determinada": como_dir, "efeito_medido": efeito, "como_medido": como_medido,
                   "apresentada_como_aprimoramento": aprim, "celulas_do_infografico_afetadas": celulas, "tipo_de_quebra": tipo})


SEM = "sem sobreposicao nos dados baixados"
IBGE9729 = "https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/9729-ibge-realiza-seminario-para-jornalistas-sobre-a-atualizacao-do-sistema-de-contas-nacionais"
IBGE9726 = "https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/9726-em-2011-pib-da-nova-serie-cresceu-3-9-e-chegou-a-r-4-375-trilhoes"
IBGE13264 = "https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/13264-asi-ibge-divulga-nova-serie-do-sistema-de-contas-nacionais"
IPCA_MET = "https://biblioteca.ibge.gov.br/visualizacao/livros/liv65477.pdf"

# ================================== PIB ==================================
q("PIB", "SCN10_PIBG10 (Ipeadata/IBGE)", "1990-1991 (IBGE assume as contas em 1990; nova serie SNA 1993 publicada em 1997 para 1990-1997)",
  "Sistema de Contas Nacionais Consolidadas da FGV: sistema simplificado, mais agregado, revisado a cada Censo Economico (1947-1989)",
  "SCN do IBGE, referencia 1985, com a 3a versao do manual de contas nacionais da ONU (SNA 1993), estrutura ampliada",
  "adocao da terceira versao do Manual de Contas Nacionais da ONU, que altera a base de dados e amplia toda a estrutura do SCN",
  IBGE9729, "release_9729",
  "De 1947 a 1989, o desempenho da economia brasileira era medido pelo Sistema de Contas Nacionais Consolidadas (SCN) da Fundação Getúlio Vargas. [...] Em 1997, o IBGE adotou a terceira versão do Manual de Contas Nacionais da ONU, alterando não apenas a base de dados do SCN, mas ampliando toda a sua estrutura. Tal mudança levou à divulgação de uma nova série das Contas Nacionais, de 1990 a 1997.",
  "desconhecida", "nao ha sobreposicao FGV x IBGE nos arquivos baixados", SEM, "nenhuma medicao possivel com os dados desta pasta", "sim",
  "PIB Ditadura (1968-1973, 11,1): serie FGV; PIB Itamar (1992-1994, 2,5): ref. 1985; as duas atravessam o mesmo salto de fonte quando comparadas", "mudanca_de_regra")
q("PIB", "SCN10_PIBG10 (Ipeadata/IBGE)", "1995-1996 (emenda da ref. 1985 com a ref. 2010 retropolada)",
  "SCN referencia 1985 (1991-1995)", "Contas Trimestrais referencia 2010 retropoladas (1996-2000) e depois SCN referencia 2010 anual (2001 em diante)",
  "preservar a comparabilidade ao longo do tempo: 2000-2009 foi refeito por inteiro e 1995-1999 foi retropolado so no valor adicionado em 12 atividades, nos usos finais, impostos e importacoes",
  "https://ftp.ibge.gov.br/Contas_Nacionais/Sistema_de_Contas_Nacionais/Notas_Metodologicas_2010/17_retropolacao_tabelas_recursos_usos.pdf", "scn2010_nota17",
  "Para preservar a comparabilidade dos dados ao longo do tempo, foi preciso refazer as tabelas do período 2000 – 2009 incorporando as mudanças conceituais e de algoritmos além das mudanças de classificação da revisão adotadas a partir de 2010. [...] Para o período 1995 – 1999, a retropolação foi feita para o valor adicionado por atividade econômica (com agregação em 12 atividades), para os usos finais, impostos e importações.",
  "desconhecida", "nao ha a serie ref. 1985 para 1996-2000 nos arquivos baixados", SEM, "a serie antiga de 1996-2000 nao foi obtida", "sim",
  "PIB FHC (1995-2002, 2,3): 1995 vem da ref. 1985, 1996-2000 das Contas Trimestrais ref. 2010 e 2001-2002 do SCN ref. 2010 (tres vintages numa celula)", "mudanca_de_regra")
q("PIB", "SCN10_PIBG10 (Ipeadata/IBGE); vintage anterior a 2015", "2007-03 (ref. 1985 -> ref. 2000)",
  "SCN referencia 1985", "SCN referencia 2000: incorpora pesquisas anuais do IBGE, declaracoes fiscais das empresas (DIPJ), POF 2003, Censo Agropecuario 1996",
  "incorporar as pesquisas anuais do IBGE e a DIPJ e atualizar conceitos e definicoes segundo as ultimas recomendacoes das Nacoes Unidas",
  IBGE13264, "release_13264",
  "atualiza conceitos e definições introduzindo as últimas recomendações das Nações Unidas e de outros organismos internacionais. [...] Em 2005, o PIB estimado na nova série das Contas Nacionais foi de R$ 2,148 trilhões e ficou 10,9% acima do valor estimado na série anterior. A taxa de variação em relação ao ano anterior foi de 2,9% enquanto na série antiga havia sido de 2,3%. [...] A taxa de variação em volume passou para 4,3%, enquanto na série anterior ela fora 4,4%.",
  "ambigua", "comparacao serie nova x antiga publicada pelo IBGE no mesmo release; a tabela ano a ano e imagem GIF (nao legivel), so 2 pontos em texto; direcao por ano dada por nota academica secundaria",
  "2000: taxa 4,4 -> 4,3 (-0,1 p.p.); 2005: 2,3 -> 2,9 (+0,6 p.p.); nivel corrente +7,1% (2000) e +10,9% (2005). Nota secundaria (A.C. Pastore, 21/03/2007): revisoes para baixo em 1996 e 1999 e para cima a partir de 2002",
  "sobreposicao medida pelo proprio IBGE (2 anos em texto) + fonte secundaria rotulada para a direcao dos demais anos; a serie ref. 2000 nao foi baixada", "sim",
  "nenhuma na serie vigente de 2001 em diante (superada em 2015); afetou FHC (1996-2002) e Lula 1-2 (2003-2006) nos vintages 2007-2014", "mudanca_de_regra")
q("PIB", "SCN10_PIBG10 (Ipeadata/IBGE)", "2015-03 (ref. 2000 -> ref. 2010)",
  "SCN referencia 2000 (SNA 1993, CNAE 1.0)", "SCN referencia 2010 (SNA 2008, CNAE 2.0); P&D e software passam a investimento",
  "incorporar as recomendacoes da mais recente revisao do manual de contas nacionais (ONU, FMI, OCDE, Banco Mundial), Censo Agropecuario 2006, POF 2008/09, Censo 2010 e CNAE 2.0",
  IBGE9726, "release_9726",
  "Em média, os valores correntes do PIB de 2000 a 2011, na nova série, ficaram 2,1% acima dos valores da série antiga. Nesse período, a taxa média anual de crescimento foi revisada de 3,5% na série anterior para 3,7% no SCN 2010. [...] Pela ótica da despesa, com a revisão metodológica do SCN 2010, cresceu a taxa de investimento (participação da Formação Bruta de Capital Fixo no PIB): de 19,5% para 20,6%, em 2010",
  "eleva", "comparacao nova x antiga publicada pelo IBGE (media 2000-2011)",
  "crescimento medio anual 2000-2011: 3,5% -> 3,7% (+0,2 p.p. ao ano); PIB corrente +2,1%; taxa de investimento 2010: 19,5% -> 20,6%",
  "sobreposicao medida pelo proprio IBGE (media do periodo; a tabela ano a ano e imagem)", "sim",
  "PIB FHC 2000-2002, Lula 1-2 (4,0) e Dilma 2011: a serie vigente ja e a ref. 2010; o efeito por governo nao e decomponivel porque a fonte so publica a media 2000-2011", "mudanca_de_regra")
q("PIB", "SCN10_PIBG10 x SIDRA 9810 x SCN10_PIB10", "revisoes anuais e dados preliminares (2018-2019; 2023-2025)",
  "valor publicado numa edicao", "valor publicado em outra edicao/serie",
  "o proprio comentario da serie Ipeadata declara que 2022-2023 sao preliminares estimados das Contas Trimestrais ref. 2010",
  "http://www.ipeadata.gov.br/api/odata4/Metadados", "ipeadata",
  "Para 2022 e 2023, resultados preliminares estimados a partir das Contas Nacionais Trimestrais Referência 2010.",
  "desconhecida", "diferenca entre duas fontes do mesmo ano; sem direcao sistematica",
  f"2018: SIDRA 1,7 contra Ipeadata {n(M['pib_sidra9810_x_ipeadata']['2018']['ipeadata'])} ({n(M['pib_sidra9810_x_ipeadata']['2018']['dif'], 2, True)} p.p.); 2019: 1,3 contra {n(M['pib_sidra9810_x_ipeadata']['2019']['ipeadata'])} ({n(M['pib_sidra9810_x_ipeadata']['2019']['dif'], 2, True)} p.p.); 2024: taxa {n(M['pib_indice_x_taxa_2024']['taxa_SCN10_PIBG10'], 3)} contra razao do indice {n(M['pib_indice_x_taxa_2024']['razao_do_indice_SCN10_PIB10'], 3)}",
  "comparacao direta de duas series publicadas para o mesmo ano (calc.py, medidas.json: pib_sidra9810_x_ipeadata)", "nao_declarado",
  "PIB Temer (2016-2018, 0,7: 2018) e Bolsonaro (2019); Lula 3* (2023-2025, 2,9*: asterisco do infografico = estimativa)", "revisao_de_vintage")

# ================================== IPCA ==================================
q("IPCA", "IPCA (SGS 433 BCB; IBGE/SNIPC)", "1967-1973 (indice inexistente)",
  "indices de precos ao consumidor do Ministerio do Trabalho (1948-1978)", "IPCA, criado em dez/1979",
  "O IPCA foi criado em dezembro de 1979 como medida da inflacao; antes, a producao de indices estava a cargo do Ministerio do Trabalho",
  IPCA_MET, "ipca_liv65477",
  "No período compreendido entre 1948 e 1978, a produção de índices de preços esteve a cargo do então Ministério do Trabalho [...] dezembro de 1979 - Foi criado, também através do SNIPC, o Índice Nacional de Preços ao Consumidor Amplo - IPCA, como medida da inflação brasileira.",
  "desconhecida", "o rotulo 'IPCA 1967-1973' nao corresponde a nenhuma serie com esse nome; a serie usada nao foi identificada", "nao identificavel",
  "sem serie com o nome IPCA antes de 1979/1980; IGP-DI/FGV existe desde 1944 (outro indice)", "nao_declarado",
  "IPCA Ditadura (1967-1973, 20,3)", "mudanca_de_regra")
q("IPCA", "IPCA (SGS 433 BCB; IBGE/SNIPC)", "1986-02/03 (Plano Cruzado)",
  "serie em cruzeiros; coleta do dia 15 do mes anterior ao dia 14", "serie encerrada em 28/02/1986 ('fevereiro-linha'); nova base mar/1986=100; coleta passa a mes civil",
  "Decreto-Lei 2.284, de 10/03/1986 (ato legal do Plano Cruzado)",
  IPCA_MET, "ipca_liv65477",
  "Ficou estabelecido que o INPC e IPCA teriam suas séries em cruzeiros encerradas, utilizando-se, para tanto, o vetor de preços em vigor no dia 28.02.1986, o que acarretou procedimentos especiais, que culminaram com o cálculo dos índices de fechamento das séries chamadas \"fevereiro-linha\" [...] seu período de coleta, que anteriormente era do dia 15 do mês anterior ao dia 14 do mês de referência, aproximadamente, passou a ser o mês civil, tal como o INPC.",
  "desconhecida", "sem sobreposicao: as duas series nao coexistem em arquivo baixado", SEM, "nenhuma medicao possivel", "nao_declarado",
  "nenhuma celula do infografico (Sarney/Collor nao constam); afeta IPCA acumulado de qualquer janela que cruze fev-mar/1986", "mudanca_de_regra")
q("IPCA", "IPCA (SGS 433 BCB; IBGE/SNIPC)", "1989-06 (estrutura de pesos POF 1987-88)",
  "pesos do Endef 1974-75; faixa 1 a 30 salarios minimos", "pesos da POF 1987-88; faixa 1 a 40 salarios minimos; pesos regionais da PNAD 1987",
  "atualizar as estruturas de consumo com a nova pesquisa de orcamentos familiares",
  IPCA_MET, "ipca_liv65477",
  "Através da POF 1987-1988, tais estruturas foram atualizadas e implantadas em junho de 1989.",
  "desconhecida", "sem sobreposicao nem contrafactual publicado para este episodio", SEM, "BCB (EE70) mede so 1999, 2006 e 2012", "sim",
  "nenhuma celula do infografico (Sarney/Collor nao constam); define o regime em que Itamar 1992-1993 e calculado", "metodo_estatistico")
q("IPCA", "IPCA (SGS 433 BCB; IBGE/SNIPC)", "1991-01 (Goiania entra; estruturas simplificadas)",
  "10 areas (9 regioes metropolitanas + Brasilia); estruturas originais da POF", "11 areas com Goiania; estruturas simplificadas ate dez/1993",
  "garantir maior representatividade da Regiao Centro-Oeste; estruturas da POF 'consideradas muito extensas'",
  IPCA_MET, "ipca_liv65477",
  "Em janeiro de 1991, o Município de Goiânia passou a integrar o Sistema para garantir maior representatividade da Região Centro-Oeste. [...] A partir de janeiro de 1991, o então Departamento de Índices de Preços decidiu simplificá-las, por terem sido consideradas muito extensas.",
  "desconhecida", "sem sobreposicao", SEM, "nenhuma medicao possivel", "sim",
  "IPCA Itamar (1992-1994, 1088): 1992 e 1993 sob estruturas simplificadas, 1994 sob estruturas originais", "metodo_estatistico")
q("IPCA", "IPCA (SGS 433 BCB; IBGE/SNIPC)", "1994-01 (formula do subitem)",
  "media aritmetica simples dos relativos de produtos no subitem", "media geometrica dos relativos; volta as estruturas originais da POF; base dez/1993=100",
  "propriedade de circularidade dos numeros-indice e substituicao de produtos no nivel de subitem",
  IPCA_MET, "ipca_liv65477",
  "Até dezembro de 1993, o índice de um subitem, de modo geral, era obtido agregando-se os relativos dos produtos, através da média aritmética simples. [...] de janeiro de 1994, a variação do subitem passou a ser calculada utilizando-se a média geométrica dos relativos dos produtos. [...] Esta decisão foi tomada com base em estudos realizados no então Departamento de Índices de Preços, que privilegiou atender dois importantes aspectos: a propriedade de circularidade dos números-índice",
  "reduz", "inferencia de composicao (media geometrica <= media aritmetica); NAO medida: o IBGE nao publica o contrafactual", "nao medido",
  "desigualdade entre medias; magnitude depende da dispersao dos relativos (alta em 1993-1994)", "sim",
  "IPCA Itamar (1992-1994, 1088) cruza a quebra; IPCA FHC (1995-2002) fica integralmente depois", "metodo_estatistico")
q("IPCA", "IPCA (SGS 433 BCB; IBGE/SNIPC)", "1999-08 (POF 1995-96)",
  "pesos da POF 1987-88", "pesos da POF 1995-96; pesos regionais da Contagem da Populacao 1996",
  "atualizar a cesta de consumo",
  "https://www.bcb.gov.br/conteudo/relatorioinflacao/EstudosEspeciais/EE070_Impacto_de_atualizacoes_na_cesta_de_referencia_do_IPCA.pdf", "bcb_ee070",
  "(i) da POF 1987-1988 para a POF 1995-1996, em agosto de 1999",
  "eleva", "contrafactual do Banco Central (EE70/2019): IPCA recalculado com a cesta anterior nos 3 anos antes e nos 3 anos depois",
  f"3 anos antes (ago/96-jul/99): 4,56% a.a. com a cesta antiga contra 5,27% com a nova (+0,71 p.p. ao ano); 3 anos depois (ago/99-set/01): 6,91 contra 6,97 (+0,06 p.p. ao ano): efeito depende do periodo",
  "ESTIMATIVA (contrafactual) do BCB, nao dado bruto", "nao_declarado", "IPCA FHC (1995-2002): a quebra cai no 5o ano do mandato", "metodo_estatistico")
q("IPCA", "IPCA (SGS 433 BCB; IBGE/SNIPC)", "2006-07 (POF 2002-03; itens sazonais de Paasche para Laspeyres)",
  "pesos da POF 1995-96; itens sazonais alimenticios por Paasche", "pesos da POF 2002-03; itens sazonais por Laspeyres",
  "'de acordo com a boa pratica dos produtores de estatisticas de precos, alguns aprimoramentos serao incorporados'",
  "https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/Sistema_de_Indices_de_Precos_ao_Consumidor/Notas_Tecnicas/snipc_nota_tecnica_2005_02.pdf", "snipc_nt_2005_02",
  "o IBGE passará a calcular os índices com base nas estruturas de gastos de consumo da Pesquisa de Orçamentos Familiares realizada no período de julho de 2002 a agosto de 2003. Nesta oportunidade, de acordo com a boa prática dos produtores de estatísticas de preços, alguns aprimoramentos serão incorporados aos índices",
  "ambigua", "contrafactual do Banco Central (EE70/2019)",
  "3 anos antes (jul/03-jun/06): +0,40 p.p. ao ano (5,78 contra 6,17); 3 anos depois (jul/06-ago/08): -0,34 p.p. ao ano (5,15 contra 4,81): o sinal troca",
  "ESTIMATIVA (contrafactual) do BCB, nao dado bruto", "sim", "IPCA Lula 1-2 (2003-2010, 5,6): a quebra cai no 4o ano", "metodo_estatistico")
q("IPCA", "IPCA (SGS 433 BCB; IBGE/SNIPC)", "2012-01 (POF 2008-09)",
  "pesos da POF 2002-03", "pesos da POF 2008-09 (populacao-objetivo do INPC cai para 1 a 5 SM)",
  "substituir as fontes ponderadoras por pesquisas mais recentes, visando maior precisao",
  IPCA_MET, "ipca_liv65477",
  "A partir do mês de referência de janeiro de 2012, foram incorporadas as estruturas de gastos geradas pela POF 2008-2009.",
  "reduz", "contrafactual do Banco Central (EE70/2019); sinal igual nas duas janelas",
  "3 anos antes (jan/09-dez/11): -0,49 p.p. ao ano (5,57 contra 5,08); 3 anos depois (jan/12-fev/14): -0,56 p.p. ao ano (6,58 contra 6,01)",
  "ESTIMATIVA (contrafactual) do BCB, nao dado bruto", "nao_declarado", "IPCA Dilma (2011-2016, 8,7): a quebra cai no inicio do 2o ano", "metodo_estatistico")
q("IPCA", "IPCA (SGS 433 BCB; IBGE/SNIPC)", "2014-01 e 2018-05 (cobertura geografica)",
  "11 areas (9 RMs, Brasilia, Goiania)", "13 areas (+Vitoria e Campo Grande, jan/2014) e 16 areas (+Rio Branco, Sao Luis, Aracaju, mai/2018)",
  "ampliar a abrangencia geografica durante a vigencia da POF 2008-09",
  "https://www.bcb.gov.br/content/ri/relatorioinflacao/201912/ri201912b7p.pdf", "bcb_ri201912",
  "com a inclusão da região metropolitana de Vitória e do município de Campo Grande, em janeiro de 2014; e posteriormente com a incorporação dos municípios de Rio Branco, São Luís e Aracaju, em maio de 2018.",
  "desconhecida", "sem contrafactual publicado", SEM, "nenhuma medicao possivel (as cinco areas somam 6,6% do IPCA em 2020, segundo a Tabela 1 do BCB)", "nao_declarado",
  "IPCA Dilma (2014-2016) e Temer (2018)", "metodo_estatistico")
q("IPCA", "IPCA (SGS 433 BCB; IBGE/SNIPC)", "2020-01 (POF 2017-18)",
  "pesos da POF 2008-09 (vigentes por 96 meses, jan/2012-dez/2019)", "pesos da POF 2017-18: alimentacao e bebidas 24,58% -> 18,99%; transportes 18,28% -> 20,84%; comunicacao 3,65% -> 6,19% (jan/2018)",
  "refletir as mudancas no padrao de consumo captadas pela POF 2017-2018",
  "https://www.bcb.gov.br/content/ri/relatorioinflacao/201912/ri201912b7p.pdf", "bcb_ri201912",
  "A nova estrutura reflete as mudanças no padrão de consumo das populações-objetivo captadas pela Pesquisa de Orçamentos Familiares (POF) 2017-2018, em substituição à estrutura atual derivada da POF 2008-2009, que vigorou por 96 meses (de janeiro de 2012 a dezembro de 2019).",
  "reduz", "media dos contrafactuais; o BCB tambem fala em 'viés desinflacionário de atualizações da cesta de referência'; o sinal NAO se repete todo ano",
  f"BCB 2017-2019: -0,09 p.p. ao ano (3,46 contra 3,55); 2017 +0,24, 2018 -0,27, 2019 -0,23. Reconstrucao por grupos deste dossie 2020-2025 (estimativa): efeito por ano {', '.join(n(M['ipca_cf_2020_2025']['por_ano'][str(y)]['efeito_pp'], 2, True) for y in range(2020, 2026))} p.p.; media {n(M['ipca_cf_2020_2025']['efeito_medio_anual_pp'], 2, True)} p.p. ao ano; acumulado 2020-2025 {n(M['ipca_cf_2020_2025']['acumulado_2020_2025']['antigos'], 1)}% (pesos antigos) contra {n(M['ipca_cf_2020_2025']['acumulado_2020_2025']['novos'], 1)}% (novos)",
  "ESTIMATIVAS (contrafactuais): BCB EE70 e reconstrucao por 9 grupos com SIDRA 1419/7060 (valida: reproduz o IPCA publicado de 2018 em 3,744 e 2020 em 4,518)", "nao_declarado",
  "IPCA Bolsonaro (2019-2022, 6,4): 2020-2022 sob a cesta nova; IPCA Lula 3* (2023-2025)", "metodo_estatistico")

# ================================== DESEMPREGO ==================================
q("Desemprego", "PME antiga (Ipeadata PME12_TDA12)", "1982 (revisao completa), 1988 e 1993 (parciais, so amostragem)",
  "PME de 1980", "PME revisada em 1982; ajustes de plano amostral em 1988 e 1993",
  "n/d (a fonte apenas registra as revisoes)",
  "https://www.ibge.gov.br/estatisticas/sociais/trabalho/9183-pesquisa-mensal-de-emprego-antiga-metodologia.html", "pme_antiga_pagina",
  "A PME foi iniciada em 1980, sendo submetida a uma revisão completa em 1982 e a duas parciais, em 1988 e 1993, por meio das quais foram realizados ajustamentos restritos somente ao plano de amostragem.",
  "desconhecida", "sem sobreposicao baixada", SEM, "nenhuma medicao possivel", "nao_declarado",
  "Desemprego Itamar (1992-1994, 6,8): a revisao amostral de 1993 cai dentro da janela", "metodo_estatistico")
q("Desemprego", "PNAD anual (Ipeadata Dese_Pnad / DISOC_DESE)", "1992 (conceito de trabalho)",
  "PNAD ate 1991: nao contava como ocupados os trabalhadores na producao para o proprio consumo e na construcao para o proprio uso", "PNAD desde 1992: conceito de trabalho mais abrangente",
  "captar grupos envolvidos em atividade economica que antes nao entravam na populacao ocupada; questionario permite harmonizar com os levantamentos anteriores",
  "https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2012/notas_tecnicas.pdf", "sis2012_notas",
  "A partir da PNAD 1992, para captar determinados grupos de pessoas envolvidas em atividade econômica que, anteriormente, não eram incluídas na população ocupada, o conceito de trabalho tornou-se mais abrangente, incluindo, na captação como pessoa ocupada, os trabalhadores na produção para o próprio consumo e os trabalhadores na construção para o próprio uso.",
  "desconhecida", "nenhum dado PNAD pre-1992 nos arquivos baixados; o IBGE diz que o questionario permite recalcular no conceito antigo", SEM, "nenhuma medicao possivel", "sim",
  "Desemprego Itamar (1992-1994): primeiro ano da PNAD no conceito novo; 'Ditadura' (1968-1973) nao tem PNAD", "metodo_estatistico")
q("Desemprego e Gini", "PNAD anual", "2004 (area rural do Norte)",
  "PNAD 1992-2003 sem a area rural de RO, AC, AM, RR, PA e AP", "PNAD 2004 em diante com area urbana e rural em todas as UFs",
  "inclusao das areas rurais da antiga Regiao Norte",
  "https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2012/notas_tecnicas.pdf", "sis2012_notas",
  "As estatísticas do período de 1992 a 2003 apresentadas para o Brasil foram obtidas considerando as informações de todas as áreas pesquisadas, representando, [...] portanto, a totalidade do País, com exceção somente das áreas rurais de Rondônia, Acre, Amazonas, Roraima, Pará e Amapá;",
  "desconhecida", "sem sobreposicao baixada (nao ha PNAD 2004 sem a area rural); uma fonte secundaria (Hoffmann, USP) diria efeito desprezivel na desigualdade, mas NAO foi lida ❓", SEM, "nenhuma medicao possivel", "sim",
  "Desemprego Lula 1-2 (2003-2010, 8,4->6,5): 2003 sem a area rural, 2004+ com; Gini FHC 2002 sem, Lula 1-2 2010 com", "metodo_estatistico")
q("Desemprego e Gini", "PNAD anual 2001-2009", "pesos reponderados (projecao populacional Revisao 2008)",
  "pesos de expansao originais da PNAD", "novos pesos baseados na revisao 2008 das projecoes populacionais, tendencia 2000-2010",
  "alinhar a expansao da PNAD as projecoes populacionais revistas",
  "https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2012/notas_tecnicas.pdf", "sis2012_notas",
  "A partir das estimativas de população geradas em sintonia com as informações da revisão 2008 das projeções populacionais, utilizando a tendência 2000-2010, foram produzidos novos pesos para expansão dos resultados da PNAD para o período de 2001 a 2009.",
  "desconhecida", "nao ha a PNAD 2001-2009 com os pesos antigos nos arquivos baixados", SEM, "nenhuma medicao possivel", "sim",
  "Desemprego, Gini e pobreza Lula 1-2 (2003-2009)", "revisao_de_vintage")
q("Desemprego", "PME antiga (30 dias, 15+) -> PME nova (Ipeadata PME12_TDA12 -> PAN12_TD12)", "2002-03 (nova PME; antiga encerrada em dez/2002)",
  "15 anos ou mais; desemprego aberto; referencia semana (manchete) ou 30 dias (serie Ipeadata); malha setorial do Censo 1991",
  "10 anos ou mais; desocupado = sem trabalho na semana, disponivel e com procura nos 30 dias; coletor eletronico; malha do Censo 2000",
  "mudancas conceituais seguindo as recomendacoes da OIT, abertura comercial e globalizacao que mudaram a estrutura produtiva, comparabilidade internacional",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv1259.pdf", "liv1259",
  "Esses fatores levaram o IBGE a realizar uma revisão da PME em todos os seus aspectos, metodológicos e processuais, para que a investigação se ajustasse à realidade atual e continuasse produzindo indicadores para a análise conjuntural do mercado de trabalho metropolitano, tendo sempre presente a comparabilidade internacional. [...] 1 – implementação de algumas mudanças conceituais no tema trabalho, seguindo as recomendações internacionais; [...] A população desocupada na semana de referência compreende as pessoas sem trabalho na semana de referência, mas que estavam disponíveis para assumir um trabalho nessa semana e que tomaram alguma providência efetiva para conseguir trabalho no período de referência de 30 dias",
  "eleva", "sobreposicao medida: as duas PMEs foram calculadas nos mesmos meses (mar-dez/2002)",
  f"{M['pme_sobreposicao']['n_meses']} meses: nova menos antiga(30 dias) = {n(M['pme_sobreposicao']['media_pp'], 2, True)} p.p. em media (minimo {n(M['pme_sobreposicao']['min_pp'], 2, True)}, maximo {n(M['pme_sobreposicao']['max_pp'], 2, True)}). Decomposicao em 2 meses com a manchete da epoca: mar/2002 antiga-semana 7,1 -> antiga-30 dias {n(M['pme_semana_vs_30d']['2002-03']['antiga_30d_ipeadata'], 2)} (+{n(M['pme_semana_vs_30d']['2002-03']['efeito_periodo_ref_pp'], 2)} so por trocar semana por 30 dias) -> nova {n(M['pme_semana_vs_30d']['2002-03']['nova'], 1)} (+{n(M['pme_semana_vs_30d']['2002-03']['efeito_resto_vs_30d_pp'], 2)} do resto); nov/2002: 7,1 -> {n(M['pme_semana_vs_30d']['2002-11']['antiga_30d_ipeadata'], 2)} -> {n(M['pme_semana_vs_30d']['2002-11']['nova'], 1)} (resto +{n(M['pme_semana_vs_30d']['2002-11']['efeito_resto_vs_30d_pp'], 2)})",
  "calc.py/medidas.py (PME12_TDA12 x PAN12_TD12 mensais; manchetes das PDFs PME mar/2002 e nov/2002). O IBGE NAO decompoe o salto; o 'resto' agrega idade 10+, questionario, procura e malha. Contradicao entre fontes: o metadado Ipeadata de PAN12_TD12 diz 'Periodo de referencia: 30 dias' e o relatorio metodologico define desocupado pela semana; nao resolvida. Data: Ipeadata/SIDRA comecam em 2002-03; o IBGE (jul/2003) fala em serie desde out/2001 para o rendimento; Reis (Ipea, 2004) tambem aponta out/2001",
  "sim", "Desemprego FHC (1995-2002, 7,7: PME antiga/PNAD) e Lula 1-2 (2003-2010, 8,4 -> 6,5: PME nova): a transicao FHC->Lula cruza a quebra de ~+3,7 p.p.", "metodo_estatistico")
q("Desemprego", "PNAD anual (Dese_Pnad) -> PNAD Continua (SIDRA 4562/4099)", "2012 (PNAD Continua; PNAD anual encerrada em 2015)",
  "PNAD: 10+ anos; semana de referencia = ultima semana completa de setembro; desocupado = procurou trabalho NA SEMANA",
  "PNADC: 14+ anos; semana imediatamente anterior a entrevista (todo trimestre); desocupado = procura nos 30 dias e inclui quem ja conseguiu trabalho para comecar depois",
  "harmonizacao metodologica dos conceitos e classificacoes; indicadores de curto prazo com abrangencia nacional",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv101823.pdf", "nt_pme_pnad_pnadc",
  "Harmonização metodológica que visa uniformizar os conceitos e classificações dos indicadores produzidos pelo IBGE; [...] É importante ressaltar que as diferenças metodológicas existentes entre as pesquisas inviabilizam o processo de comparações entre elas.",
  "ambigua", "sobreposicao medida 2012-2014 (PNAD de setembro x PNADC; os sinais divergem porque as duas pesquisas mostram tendencias opostas em 2014)",
  f"PNADC menos PNAD: media {n(M['pnad_x_pnadc_desemprego']['media_dif_anual_pp'], 2, True)} p.p. (media dos 4 trimestres) e {n(M['pnad_x_pnadc_desemprego']['media_dif_3tri_pp'], 2, True)} p.p. (3o trimestre); por ano (3o tri): {', '.join(n(M['pnad_x_pnadc_desemprego'][str(y)]['dif_vs_3tri_pp'], 2, True) for y in (2012, 2013, 2014))}",
  "calc.py/medidas.py (Dese_Pnad Brasil x SIDRA 4099 3o trimestre e 4562 anual)", "sim",
  "Desemprego Dilma (2011-2016, 6,7): 2011 PNAD/PME, 2012+ PNADC; Temer (12,3), Bolsonaro (13,2), Lula 3* (9,3) so PNADC", "metodo_estatistico")
q("Desemprego", "PME nova -> PNAD Continua", "2016-03 (PME encerrada)",
  "PME: 6 regioes metropolitanas, 10+ anos", "PNADC: todo o pais, 14+ anos",
  "a PNADC substituiu a PME 'com metodologia atualizada' e abrangencia nacional, atendendo demanda dos usuarios",
  "https://www.ibge.gov.br/estatisticas/sociais/trabalho/9183-pesquisa-mensal-de-emprego-antiga-metodologia.html", "pme_antiga_pagina",
  "A PME foi substituída, com metodologia atualizada, pela [...] que abrange todo o País.",
  "eleva", "declaracao do IBGE (nota tecnica nov/2015): a PNADC mostra taxas mais altas que a PME nas regioes metropolitanas; o comparativo RM x RM nao foi baixado",
  "IBGE: 'taxas de desocupação sistematicamente mais elevadas que as da PME' (valor nao publicado na nota)",
  "declaracao da fonte; sem sobreposicao medida aqui (PNADC por RM nao baixada)", "sim",
  "Desemprego Dilma (2011-2016, 6,7: PME nova ate 2015) e Temer (12,3: PNADC)", "metodo_estatistico")
q("Desemprego", "PNAD anual x PNAD Continua", "citacao do mesmo documento", "-", "-", "-",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv101823.pdf", "nt_pme_pnad_pnadc",
  "Os resultados trimestrais da PNAD Contínua, para as regiões metropolitanas, mostram taxas de desocupação sistematicamente mais elevadas que as da PME.",
  "eleva", "declaracao da fonte", "ver linha anterior", "declaracao da fonte", "nao_declarado", "ver linha anterior", "metodo_estatistico")
q("Desemprego", "PNAD Continua (SIDRA 4099/4562)", "2020-03 / 2020-T2 a 2021-T2 (coleta por telefone)",
  "coleta presencial", "coleta exclusivamente por telefone (ate jun/2021), com queda do aproveitamento da amostra",
  "risco de contaminacao pelo coronavirus de entrevistados e entrevistadores",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv101960.pdf", "nt03_2022_modulos",
  "o IBGE alterou a forma de coleta de dados da Pesquisa, anteriormente presencial, para exclusivamente por telefone. Essa alteração gerou impactos na coleta dos dados e consequente redução na taxa de aproveitamento da amostra",
  "desconhecida", "o IBGE reporta simulacoes que nao apontaram vies nos principais indicadores (Brasil, regioes, UFs), mas nao ha serie paralela presencial",
  "IBGE: simulacoes 'não apontaram viés para os principais indicadores'; aproveitamento de 1as visitas em 2020: 47,4% (contra 72,7% nas 5as)", "declaracao do IBGE (NT 03/2021 e NT 05/2021); sem sobreposicao medida aqui", "nao_declarado",
  "Desemprego Bolsonaro (2019-2022, 13,2 '2019-2020 pico')", "metodo_estatistico")
q("Desemprego, Gini e pobreza", "PNAD Continua (SIDRA, Ipeadata, SIS)", "2021-11 (reponderacao e serie historica refeita)",
  "pesos da PNADC pela projecao populacional (Censo 2010), sem calibracao por sexo e idade", "pesos com calibracao por sexo e grupo etario; serie historica refeita",
  "o IBGE entendeu que a reponderacao deveria ser feita imediatamente apos a queda de aproveitamento causada pela pandemia",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv101866.pdf", "nt03_2021_reponderacao",
  "A partir da divulgação em novembro de 2021, as estimativas mensais e trimestrais da PNAD Contínua serão calculadas incorporando o novo método de ponderação, refazendo, inclusive, a série histórica dos indicadores [...] a partir dos resultados do próximo Censo Demográfico, as estimativas dos totais populacionais serão revistas e, portanto, a PNAD Contínua terá, novamente, seus indicadores recalculados.",
  "desconhecida", "a serie antiga (pesos anteriores) nao foi baixada; todo valor PNADC baixado em 2026 ja e o reponderado", SEM, "o IBGE guarda os pesos antigos nos microdados (nao baixados)", "sim",
  "todas as celulas PNADC: Temer, Bolsonaro, Lula 3*, Dilma 2012-2016; Gini 2014-2024; pobreza 2018-2024", "revisao_de_vintage")

# ================================== SALARIO MINIMO ==================================
q("Salario minimo real", "GAC12_SALMINRE12 (Ipea) e MTE12_SALMIN12", "1940-1984 (faixas regionais) e mai/1984 (minimo nacional)",
  "salario minimo diferenciado por estados e sub-regioes", "salario minimo nacionalmente unificado em maio de 1984",
  "n/d; a serie usa o MAIOR minimo vigente no pais enquanto houve faixas",
  "http://www.ipeadata.gov.br/api/odata4/Metadados", "ipeadata",
  "Os dados para o período em que a legislação federal permitia faixas diversificadas referem-se ao maior salário mínimo vigente no país.",
  "desconhecida", "por construcao a serie nao tem salto em 1984, mas o minimo efetivo das regioes mais pobres antes de 1984 era menor; a planilha regional do Ipea nao foi baixada ❓", "nao medido", "nenhuma medicao possivel", "nao_declarado",
  "Salario minimo Ditadura (1968-1973, 42,8), e demais janelas ate 1984", "mudanca_de_regra")
q("Salario minimo real", "GAC12_SALMINRE12 (Ipea)", "1944-01, 1948-01 e 1979-04 (trocas de deflator)",
  "IPC-SP/Fipe (jul/1940-jan/1944), IPC-RJ/FGV (jan/1944-jan/1948), IGPC-Mtb (jan/1948-mar/1979)", "INPC (abr/1979 em diante)",
  "n/d no metadado (referencia: Corseuil 2002, Ipea TD 897)",
  "http://www.ipeadata.gov.br/api/odata4/Metadados", "ipeadata",
  "Série em reais (R$) constantes do último mês, elaborada pelo Ipea, deflacionando-se o salário mínimo nominal pelos seguintes índices:",
  "ambigua", "comparacao da serie oficial com o mesmo nominal dividido por um unico indice (IGP-DI) em todos os anos; o INPC so existe desde abr/1979",
  f"acumulado real por governo, serie Ipea contra IGP-DI unico: Castelo Branco {n(M['salmin_por_governo']['Castelo Branco|mandato|1964-1966']['Ipea composto'], 1, True)}% contra {n(M['salmin_por_governo']['Castelo Branco|mandato|1964-1966']['IGP-DI'], 1, True)}%; Costa e Silva+Medici {n(M['salmin_por_governo']['Costa e Silva + Medici|mandato|1967-1973']['Ipea composto'], 1, True)}% contra {n(M['salmin_por_governo']['Costa e Silva + Medici|mandato|1967-1973']['IGP-DI'], 1, True)}%; Geisel {n(M['salmin_por_governo']['Geisel|mandato|1974-1978']['Ipea composto'], 1, True)}% contra {n(M['salmin_por_governo']['Geisel|mandato|1974-1978']['IGP-DI'], 1, True)}%; Figueiredo {n(M['salmin_por_governo']['Figueiredo|mandato|1979-1984']['Ipea composto'], 1, True)}% contra {n(M['salmin_por_governo']['Figueiredo|mandato|1979-1984']['IGP-DI'], 1, True)}%; Bolsonaro {n(M['salmin_por_governo']['Bolsonaro|mandato|2019-2022']['Ipea composto'], 1, True)}% contra {n(M['salmin_por_governo']['Bolsonaro|mandato|2019-2022']['IGP-DI'], 1, True)}%",
  "calc.py (media anual a media anual; ano anterior ao inicio como base). O sinal depende do governo: a troca de deflator nao favorece nem prejudica de modo uniforme", "nao_declarado",
  "Salario minimo Ditadura (1968-1973, 42,8: IGPC-Mtb) contra Dilma/Bolsonaro (INPC)", "mudanca_de_regra")
q("Salario minimo real", "GAC12_SALMINRE12 (Ipea)", "1994-07 (troca de moeda: cruzeiro real -> real)",
  "deflator em cruzeiros reais", "variacao do deflator de jul/1994 multiplicada por 1,2225",
  "ajuste pela mudanca de unidade monetaria, 'para mitigar diferencas desta mudanca'",
  "http://www.ipeadata.gov.br/api/odata4/Metadados", "ipeadata",
  "O deflator sofre ajuste em função da mudança de unidade monetária de cruzeiros reais para reais. Para mitigar diferenças desta mudança, a variação do deflator em julho de 1994 foi multiplicada por 1,2225.",
  "ambigua", "comparacao da serie Ipea com nominal/INPC sem fator (o INPC do SGS 188 ja reproduz a serie fora de jul/1994 dentro de 0,01%)",
  f"acumulado real por governo (serie Ipea contra nominal/INPC puro): Itamar {n(M['salmin_fator_1994']['Itamar Franco']['ipea'], 1, True)}% contra {n(M['salmin_fator_1994']['Itamar Franco']['inpc_puro'], 1, True)}%; FHC {n(M['salmin_fator_1994']['FHC']['ipea'], 1, True)}% contra {n(M['salmin_fator_1994']['FHC']['inpc_puro'], 1, True)}%; Collor e Lula 1-2 sem diferenca. Efeito do fator: reduz Itamar, eleva FHC",
  "calc.py. Nao ha explicacao documentada de por que o fator e necessario se o INPC puro reproduz a serie; ❓", "nao_declarado",
  "Salario minimo Itamar (1992-1994, -13,9) e FHC (1995-2002, 4,8)", "mudanca_de_regra")

# ================================== POBREZA ==================================
HIST_URL = "https://blogs.worldbank.org/en/opendata/updating-international-poverty-line-2017-ppps"
q("Pobreza", "linhas internacionais do Banco Mundial e do IBGE (SIS)", "2022-09 (PPC 2011 -> PPC 2017: US$ 1,90/3,20/5,50 -> 2,15/3,65/6,85)",
  "linhas US$ 1,90, 3,20 e 5,50 por dia (PPC 2011)", "linhas US$ 2,15, 3,65 e 6,85 por dia (PPC 2017)",
  "lancamento de novos PPCs pelo ICP (2020); nova metodologia (mediana das linhas nacionais harmonizadas) e dados atualizados; a linha foi calibrada para nao mover a pobreza GLOBAL em 2017",
  HIST_URL, "wb_blog_2017ppp",
  "The decision follows the release in 2020 of new purchasing power parities (PPPs) by the International Comparison Program (ICP). [...] $2.17 is the line that holds constant global poverty in 2017, the year of the PPP data.",
  "eleva", "sobreposicao medida no Brasil: mesmos microdados PNADC 2012-2019, IBGE SIS (edicao 2020, 5,50 PPC 2011) contra SIS (edicao 2025, 6,85 PPC 2017)",
  f"linha superior 5,50 -> 6,85: {n(EM.get('US$ 5,50 (PPC 2011) -> US$ 6,85 (PPC 2017)', {}).get('media_pp', 0), 2, True)} p.p. em media (minimo {n(EM.get('US$ 5,50 (PPC 2011) -> US$ 6,85 (PPC 2017)', {}).get('min_pp', 0), 2, True)}, maximo {n(EM.get('US$ 5,50 (PPC 2011) -> US$ 6,85 (PPC 2017)', {}).get('max_pp', 0), 2, True)}); 3,20 -> 3,65: {n(EM.get('US$ 3,20 (PPC 2011) -> US$ 3,65 (PPC 2017)', {}).get('media_pp', 0), 2, True)}; 1,90 -> 2,15: {n(EM.get('US$ 1,90 (PPC 2011) -> US$ 2,15 (PPC 2017)', {}).get('media_pp', 0), 2, True)}. Valor da linha em R$/mes (set/2026): 5,50/PPC 2011 = R$ 643; 6,85/PPC 2017 = R$ 770",
  "pobreza-efeito-mecanico.csv (mistura a troca de linha com a revisao entre edicoes do SIS, que e <=0,5 p.p.). O PIP nao serve mais a versao PPC 2011 (a API devolve erro 500 para versoes antigas), entao nao ha medida PIP para esta troca", "sim",
  "Pobreza Dilma (2014, 22,1 ~ linha 5,50), Temer (2018, 26,5 ~ 5,50), Bolsonaro (2021, 31,6 ~ 6,85) e Lula 3* (2024, 27,4 ~ 6,85): a linha muda no meio da fileira", "mudanca_de_regra")
q("Pobreza", "linhas internacionais (Banco Mundial PIP; IBGE SIDRA 5817/5877; Ipea PNADS)", "2025-06 (PPC 2017 -> PPC 2021: US$ 2,15/3,65/6,85 -> 3,00/4,20/8,30)",
  "linhas US$ 2,15, 3,65 e 6,85 por dia (PPC 2017)", "linhas US$ 3,00, 4,20 e 8,30 por dia (PPC 2021)",
  "novos PPCs de 2021 e base maior de linhas nacionais; a fonte afirma que as linhas 'nao refletem ambicoes crescentes' e sim o custo de necessidades basicas melhor medido",
  "https://blogs.worldbank.org/en/opendata/the-world-bank-s-new-global-poverty-lines-in-2021-prices", "wb_blog_2021prices",
  "The international poverty line of $2.15 (in 2017 prices) has been updated to $3.00 (in 2021 prices), leading to an upward revision of the population in extreme poverty by 125 million people in 2022. [...] these revised lines do not reflect rising ambitions of what it means to be non-poor but largely reflect better measured cost of basic needs in the poorest countries of the world.",
  "eleva", "sobreposicao medida no Brasil: o PIP serve o mesmo pais, ano e pesquisa nas duas versoes de PPC (1981-2024)",
  f"2,15 (2017) -> 3,00 (2021): {n(EM['US$ 2.15 (PPC 2017) -> US$ 3.00 (PPC 2021)']['media_pp'], 2, True)} p.p. em media (de {n(EM['US$ 2.15 (PPC 2017) -> US$ 3.00 (PPC 2021)']['min_pp'], 2, True)} a {n(EM['US$ 2.15 (PPC 2017) -> US$ 3.00 (PPC 2021)']['max_pp'], 2, True)}); 3,65 -> 4,20: {n(EM['US$ 3.65 (PPC 2017) -> US$ 4.20 (PPC 2021)']['media_pp'], 2, True)} p.p.; 6,85 -> 8,30: {n(EM['US$ 6.85 (PPC 2017) -> US$ 8.30 (PPC 2021)']['media_pp'], 2, True)} p.p. (de {n(EM['US$ 6.85 (PPC 2017) -> US$ 8.30 (PPC 2021)']['min_pp'], 2, True)} a {n(EM['US$ 6.85 (PPC 2017) -> US$ 8.30 (PPC 2021)']['max_pp'], 2, True)}). Valor da linha em R$/mes (set/2026): 6,85/PPC 2017 = R$ 770; 8,30/PPC 2021 = R$ 817",
  "pobreza-efeito-mecanico.csv (40 anos, mesma pesquisa; so a linha/PPC muda)", "sim",
  "nenhuma celula impressa usa 3,00/4,20/8,30 diretamente; a 'linha nacional' do IBGE nos ODS (SIDRA 5877) e 8,30 PPC 2021: 2024 = 26,5 contra 23,1 na 6,85 (SIS 2025)", "mudanca_de_regra")
q("Pobreza", "Banco Mundial WDI SI.POV.DDAY / LMIC / UMIC", "2026 (o mesmo codigo de indicador muda de linha)",
  "SI.POV.DDAY ja designou US$ 1,00/1,25/1,90/2,15", "SI.POV.DDAY hoje = US$ 3,00 (PPC 2021); LMIC = 4,20; UMIC = 8,30",
  "o codigo acompanha a linha oficial vigente",
  "https://api.worldbank.org/v2/country/BRA/indicator/SI.POV.DDAY?format=json&per_page=20000", "wdi_dday",
  "Poverty headcount ratio at $3.00 a day (2021 PPP) (% of population)",
  "eleva", "o valor de 2022 baixado do WDI em 2026 (4,9) e o da linha 3,00; o mesmo codigo, na linha 2,15, daria 3,50 (PIP)",
  "WDI SI.POV.DDAY Brasil 2022 = 4,9; PIP 2,15 (PPC 2017) = 3,50 no mesmo ano", "comparacao WDI x PIP baixados (pobreza-leque-series.csv)", "nao_declarado",
  "nenhuma celula impressa; risco para quem cita 'WDI SI.POV.DDAY' sem data de download", "revisao_de_vintage")
q("Pobreza", "IBGE SIS (PNADC) x Banco Mundial PIP (PNADC)", "2012-2024 (mesma linha 6,85 PPC 2017, duas fontes)",
  "IBGE SIS: renda domiciliar per capita PNADC, ajustada pelo IPCA, fator PPC 2017 de consumo privado R$ 2,3273771", "PIP: mesma linha 6,85 e mesmo fator PPC 2017 (R$ 2,3274), mas welfare income do PIP com versao propria",
  "a causa da diferenca nao esta nas fontes lidas ❓ (o fator PPC e identico)",
  "https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2025/Tabelas/xls/2_Distribuicao_Renda_xls.zip", "sis2025_t217",
  "Taxa de conversão da paridade de poder de compra para consumo privado, R$ 2,3273771 para US$ 1,00 PPC 2017, valores diários tornados mensais e inflacionados pelo IPCA para anos recentes.",
  "reduz", "diferenca direta PIP menos SIS na mesma linha, mesmo ano e mesma pesquisa-base (PNADC)",
  f"PIP menos SIS (6,85): media {n(M['pip_x_sis_685']['media_dif_pp'], 2, True)} p.p. em 2012-2024 ({n(M['pip_x_sis_685']['media_dif_pp_sem_2020'], 2, True)} sem 2020); razao PIP/SIS ~0,79-0,82 nos anos 'normais', 0,605 em 2020, 0,774 em 2021, 0,741 em 2022",
  "medidas.json: pip_x_sis_685. Anomalia 2020 (PIP 18,8% contra SIS 31,1%) nao explicada ❓: PIP usa 5a visita so em 2020-2021 e 1a visita em 2022; o SIS usa 5as em 2020-2022", "nao_declarado",
  "Pobreza Bolsonaro (2021, 31,6 = SIS 2022): o PIP daria 23,4 em 2022 e 28,5 em 2021", "revisao_de_vintage")
q("Pobreza e Gini", "IBGE SIS (PNADC)", "2020-2022 (quintas visitas) contra 2012-2019 e 2023-2024 (primeiras visitas)",
  "indicadores anuais de rendimento de todas as fontes calculados nas primeiras visitas", "2020 (depois 2021-2022) calculados nas quintas visitas",
  "melhor aproveitamento da amostra: em 2020, 72,7% de entrevistas na 5a visita contra 47,4% na 1a (coleta por telefone na pandemia)",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv101874.pdf", "nt05_2021_rendimentos",
  "Já em 2020, o aproveitamento da amostra foi maior na base de quintas visitas (72,7% de entrevistas realizadas) do que na base de primeiras visitas (47,4% de entrevistas realizadas). [...] a proporção da população recebendo aposentadorias, aluguéis ou outras fontes de renda, a média do rendimento domiciliar per capita, o índice de Gini e todos os demais indicadores de rendimentos do ano de 2020 apresentados na divulgação foram calculados com base nas quintas visitas de 2020.",
  "desconhecida", "nao ha 2020-2022 em primeiras visitas nos arquivos baixados; o PIP usa 5a visita so em 2020-2021, o que torna as duas fontes incomparaveis nesses anos", SEM, "nenhuma medicao possivel", "sim",
  "Pobreza Bolsonaro (2021, 31,6) e Gini Bolsonaro (2021, 0,58); Lula 3 (2024) volta as primeiras visitas", "metodo_estatistico")
q("Pobreza e Gini", "IBGE SIS (PNADC) -> edicoes", "revisoes entre edicoes do SIS (2018, 2019, 2020, 2024, 2025)",
  "valor da edicao anterior", "valor da edicao seguinte (mesma linha, mesmo ano)",
  "n/d (nao lemos a nota da edicao)",
  "https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2025/Tabelas/xls/2_Distribuicao_Renda_xls.zip", "sis2025_t213",
  "Rendimentos deflacionados para reais médios do próprio ano.",
  "reduz", "diferenca entre edicoes",
  f"5,50 PPC 2011, 2017: SIS 2018 = {n(M['sis_edicoes_550']['2017']['SIS2018'])} contra SIS 2019/2020 = {n(M['sis_edicoes_550']['2017']['SIS2019'])} (-0,47 p.p.); 2016: {n(M['sis_edicoes_550']['2016']['SIS2018'])} contra {n(M['sis_edicoes_550']['2016']['SIS2019'])}; 6,85 PPC 2017: SIS 2024 contra SIS 2025, maximo {n(M['sis_edicoes_685']['max_abs_dif_pp_2012_2023'], 2)} p.p. (2023: {n(M['sis_edicoes_685']['2023']['SIS2024'])} contra {n(M['sis_edicoes_685']['2023']['SIS2025'])})",
  "medidas.json (sis_edicoes_550, sis_edicoes_685). O valor 26,5 do infografico (Temer, 2018) e o de 2017 na edicao 2018; as edicoes seguintes revisaram para 26,0", "nao_declarado",
  "Pobreza Temer (2018, 26,5 = 2017 da edicao SIS 2018); Lula 3* (2024, 27,4 = 2023 da edicao SIS 2024; a de 2025 revisou para 27,3)", "revisao_de_vintage")
q("Pobreza e Gini", "PNAD (Ipeadata) -> PNADC (Ipea PNADS harmonizada)", "2012 (PNAD -> PNADC) e harmonizacao Ipea",
  "PNAD anual ate 2011 (2014 no Ipeadata)", "PNADC desde 2012; Ipea multiplica toda a PNAD <= 2011 por um fator que iguala 2012",
  "juntar as duas pesquisas numa unica serie",
  "http://www.ipeadata.gov.br/api/odata4/Metadados", "ipeadata",
  "Até 2011, todos os resultados originais obtidos diretamente da fonte foram multiplicados pelo fator que, em 2012, iguala o resultado da antiga PNAD ao da PNAD Contínua.",
  "eleva", "sobreposicao medida para o Gini 2012-2014; para a pobreza nao ha PNAD x PNADC na mesma linha",
  f"Gini PNADC menos PNAD: {', '.join(n(M['pnad_x_pnadc_gini'][str(y)]['dif'], 3, True) for y in (2012, 2013, 2014))} (media {n(M['pnad_x_pnadc_gini']['media_dif'], 3, True)}); a serie harmonizada do Ipea fica {n(min(M['gini_harmonizado_dif'].values()), 3, True)} a {n(max(M['gini_harmonizado_dif'].values()), 3, True)} acima da PNAD original em 1995-2011 (razao ~1,02); razao PNADC/PNAD em 2012 = {n(M['gini_2012_pnad_x_pnadc_razao'], 3)}",
  "medidas.json (PGINI x SIDRA 7435; PNADS_GINI x PGINI). A harmonizacao e ESTIMATIVA do Ipea, mantida separada do dado bruto", "sim",
  "Gini FHC (2002, 0,59), Lula 1-2 (2010, 0,53), Dilma (2014, 0,52): numeros de PNAD (sem fator) ao lado de Temer (2018, 0,54) e Bolsonaro (2021, 0,58) de PNADC", "metodo_estatistico")
_bf = list(csv.DictReader(open(H / "bolsa-familia-linhas-elegibilidade.csv", encoding="utf-8")))
q("Pobreza", "linha de elegibilidade do Bolsa Familia / Auxilio Brasil (decretos)", "2004-09 a 2023-06 (10 atos)",
  "R$ 100 (pobreza) e R$ 50 (extrema pobreza), set/2004", "ate R$ 218 (linha unica), jun/2023; entre eles, Auxilio Brasil (R$ 200/100 em nov/2021; R$ 210/105 em mar/2022), outro programa",
  "reajustes por decreto dos 'valores referenciais'; em 2021 o Bolsa Familia e substituido pelo Auxilio Brasil, e em 2023 reinstituido com linha unica",
  "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/decreto/d5209.htm", "plan_d5209-2004",
  "caracterizadas pela renda familiar mensal per capita de até R$ 100,00 e R$ 50,00, respectivamente.",
  "ambigua", "valor nominal dos decretos deflacionado pelo INPC (SGS 188) para set/2026 e comparado ao salario minimo nominal do mes",
  f"linha de pobreza em R$ de set/2026: {_bf[0]['pobreza_R$_set2026_INPC']} (2004-09), {_bf[1]['pobreza_R$_set2026_INPC']} (2006-04), {_bf[3]['pobreza_R$_set2026_INPC']} (2009-09), {_bf[4]['pobreza_R$_set2026_INPC']} (2014-06), {_bf[6]['pobreza_R$_set2026_INPC']} (2018-07), {_bf[7]['pobreza_R$_set2026_INPC']} (2021-11), {_bf[9]['pobreza_R$_set2026_INPC']} (2023-06); em fracao do salario minimo: {n(float(_bf[0]['pobreza_em_fracao_do_SM_vigente']), 3)} -> {n(float(_bf[9]['pobreza_em_fracao_do_SM_vigente']), 3)}",
  "bolsa-familia-linhas-elegibilidade.csv (norma lida no Planalto; deflator INPC declarado)", "nao_declarado",
  "nenhuma celula impressa; mede o criterio de elegibilidade, nao a pobreza medida", "mudanca_de_regra")
q("Pobreza", "linha propria do Ipea (DISOC_PPY, PNAD) x linhas internacionais do SIS (PNADC)", "2012-2014 (a linha Ipea e interrompida em 2014)",
  "linha Ipea: 2 x linha de extrema pobreza (cesta FAO), regionalizada", "linhas internacionais em dolares PPC (IBGE SIS)",
  "n/d (sao series de instituicoes diferentes)",
  "http://www.ipeadata.gov.br/api/odata4/Metadados", "ipeadata",
  "A linha de pobreza aqui considerada é o dobro da linha de extrema pobreza, uma estimativa do valor de uma cesta de alimentos com o mínimo de calorias necessárias para suprir adequadamente uma pessoa",
  "desconhecida", "nao sao a mesma linha; a comparacao mostra so a distancia entre definicoes", f"2014: Ipea PPY {n(M['ppy_x_sis']['2014']['ipea_ppy_pnad'], 1)}% contra SIS 3,20 PPC 2011 {n(M['ppy_x_sis']['2014']['sis_3.20_ppc2011'], 1)}% e SIS 5,50 PPC 2011 {n(M['ppy_x_sis']['2014']['sis_5.50_ppc2011'], 1)}%",
  "medidas.json (ppy_x_sis)", "nao_declarado", "Pobreza Lula 1-2 (2010, 21,4 = PPY de 2009) e Dilma (2014, 22,1): o numero de 2010 e linha Ipea e o de 2014 e linha internacional", "mudanca_de_regra")
q("Pobreza e Gini", "Banco Mundial PIP (Brasil, 1981-2024)", "2012 (o proprio PIP separa PNAD e PNADC em dois 'spells')",
  "PNAD (survey_comparability = 0; spell 1981-2011)", "PNADC (survey_comparability = 1; spell 2012-2024; 5a visita em 2020-2021)",
  "o PIP marca a comparabilidade entre pesquisas; a razao da separacao nao esta no campo",
  "https://api.worldbank.org/pip/v1/pip?country=BRA&year=all&povline=6.85&ppp_version=2017&fill_gaps=false&format=json", "pip_json",
  "\"comparable_spell\":\"1981 - 2011\"",
  "ambigua", "o PIP publica 1981-2024 como uma so serie, mas marca o spell; a sobreposicao 2012-2014 PNAD x PNADC so existe para o Gini (fora do PIP)",
  f"Gini PNADC menos PNAD 2012-2014: {n(M['pnad_x_pnadc_gini']['media_dif'], 3, True)}; pobreza: sem sobreposicao na mesma linha (PNAD termina em 2011 no PIP)",
  "campo comparable_spell dos arquivos pip_*.json + medidas.json", "nao_declarado",
  "Pobreza e Gini: todas as celulas do infografico cruzam a quebra (FHC, Lula 1-2 em PNAD; Temer, Bolsonaro, Lula 3 em PNADC)", "metodo_estatistico")
q("Gini", "Banco Mundial PIP / WDI SI.POV.GINI", "1992 (valor isolado)",
  "PIP/WDI 1990 = 0,605 e 1993 = 0,601", "PIP/WDI 1992 = 0,531; PNAD (Ipeadata PGINI) 1992 = 0,583",
  "causa nao encontrada nas fontes lidas ❓",
  "https://api.worldbank.org/pip/v1/pip?country=BRA&year=all&povline=6.85&ppp_version=2017&fill_gaps=false&format=json", "pip_json",
  "\"reporting_year\":1992,\"reporting_level\":\"national\",\"survey_acronym\":\"PNAD\"",
  "reduz", "diferenca do valor de 1992 em relacao aos vizinhos e a PNAD do Ipea", "PIP 1992 = 0,531 contra PNAD 0,583 (-0,052) e vizinhos 0,605 (1990) e 0,601 (1993)",
  "comparacao direta de series baixadas", "nao_declarado", "Gini Itamar (1992, impresso 0,60 = valor de 1993): o PIP de 1992 daria 0,531", "revisao_de_vintage")
q("Gini", "Censo Demografico (Atlas DH) x PNAD", "Censos 1991, 2000, 2010 contra PNADs vizinhas",
  "PNAD (renda domiciliar per capita, amostra anual)", "Censo (microdados do Censo; Atlas DH/PNUD-Ipea-FJP)",
  "o Atlas e elaborado a partir dos microdados dos Censos; a razao do nivel mais alto nao esta declarada ❓",
  "http://www.ipeadata.gov.br/api/odata4/Metadados", "ipeadata",
  "Mede o grau de desigualdade existente na distribuição de indivíduos segundo a renda domiciliar per capita.",
  "eleva", "diferenca direta entre o Gini do Censo 2010 e as PNADs de 2009 e 2011",
  f"Censo 2010 = {n(M['censo_x_pnad_gini']['censo_2010'], 3)} contra PNAD 2009 = {n(M['censo_x_pnad_gini']['pnad_2009'], 3)} ({n(M['censo_x_pnad_gini']['dif_vs_2009'], 3, True)}) e PNAD 2011 = {n(M['censo_x_pnad_gini']['pnad_2011'], 3)} ({n(M['censo_x_pnad_gini']['dif_vs_2011'], 3, True)})",
  "medidas.json (censo_x_pnad_gini)", "nao_declarado", "Gini Lula 1-2 (2010, 0,53 = PNAD 2011, nao o Censo 2010 de 0,600)", "metodo_estatistico")

# ================================== EXPECTATIVA DE VIDA ==================================
q("Expectativa de vida", "projecoes IBGE: Revisao 2008 -> Revisao 2013", "c. 2013 (apos o Censo 2010)",
  "Projecao Revisao 2008 (e0 de 2000 = 70,46)", "Projecao Revisao 2013 (SIDRA 1174; e0 de 2000 = 69,8)",
  "o proprio IBGE antecipava em 2010 que as tabuas de 2001-2009 seriam reavaliadas com o Censo 2010; o documento da Revisao 2013 NAO foi lido ❓",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv98593.pdf", "liv98593",
  "Com os resultados do Censo Demográfico 2010 a tendência mostrada passará por um processo de avaliação e, se for o caso, reajustada aos novos parâmetros extraídos do levantamento censitário em curso. Este procedimento implicará numa minuciosa avaliação das tábuas de mortalidade correspondentes aos anos de 2001 a 2009",
  "reduz", "diferenca entre as duas revisoes no mesmo ano (2000)",
  f"2000: {n(M['e0_revisoes_ano2000']['rev2008'])} (Rev. 2008) -> {n(M['e0_revisoes_ano2000']['rev2013'], 1)} (Rev. 2013): -0,66 anos; a tabua de 2000 como publicada diz {n(M['e0_revisoes_ano2000']['tabua_2000_publicada'])}", "medidas.json (e0_revisoes_ano2000)", "sim",
  "Expectativa de vida FHC (2000, 70,4 ~ Rev. 2008) e Lula 1-2 (2010, 73,9 = Rev. 2013)", "revisao_de_vintage")
q("Expectativa de vida", "projecoes IBGE: Revisao 2013 -> Revisao 2018", "2018",
  "Projecao Revisao 2013", "Projecao Revisao 2018",
  "incorporar novas informacoes: revisaram-se a populacao de partida, a fecundidade e a migracao; os parametros de mortalidade NAO foram alterados",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv101597.pdf", "proj2018",
  "Para a Revisão 2018 os parâmetros de mortalidade não foram alterados.",
  "desconhecida", "diferenca entre as duas revisoes em 2000-2014",
  f"maximo {n(M['e0_rev13_x_rev18']['max_abs_dif'], 2)} ano de diferenca em {M['e0_rev13_x_rev18']['n_anos']} anos (2000: {n(M['e0_revisoes_ano2000']['rev2013'], 1)} contra {n(M['e0_revisoes_ano2000']['rev2018'])})",
  "medidas.json (e0_rev13_x_rev18): efeito desprezivel, como o IBGE declara", "sim", "Expectativa de vida Lula 1-2 (2010) e Dilma (2015): sem efeito", "revisao_de_vintage")
q("Expectativa de vida", "projecoes IBGE: Revisao 2018 -> Revisao 2024 (Censo 2022 e pandemia)", "2024-08 (tabuas divulgadas em 2025-11-28)",
  "Projecao Revisao 2018 (base Censo 2010; 2020-2022 sem os efeitos da Covid-19)", "Projecao Revisao 2024 (Censos 2000, 2010 e 2022; registros de obitos reais 2020-2023); tabuas reconstruidas 2000-2024",
  "incorporar o Censo 2022, registros mais recentes de nascimentos e obitos, migracao do Censo 2022; as tabuas dos anos de pandemia antes 'projetavam' a mortalidade de 2010",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv102111.pdf", "proj2024",
  "Elas incorporam os resultados do último Censo Demográfico, realizado em 2022; informações mais recentes dos registros de nascimentos e de óbitos; dados de migração interna, obtidos do Censo 2022; e dados de migração internacional, advindas de registros administrativos.",
  "ambigua", "diferenca entre vintages no mesmo ano: serie vigente (Rev. 2024) menos Rev. 2018 (Ipeadata) e menos a tabua do ano como publicada",
  f"vigente menos tabua publicada: 2000 {n(M['e0_publicada_x_vigente']['2000']['dif'], 2, True)}; 2010 {n(M['e0_publicada_x_vigente']['2010']['dif'], 2, True)}; 2019 {n(M['e0_publicada_x_vigente']['2019']['dif'], 2, True)}; 2020 {n(M['e0_publicada_x_vigente']['2020']['dif'], 2, True)}; 2021 {n(M['e0_publicada_x_vigente']['2021']['dif'], 2, True)}; 2022 {n(M['e0_publicada_x_vigente']['2022']['dif'], 2, True)}; 2023 {n(M['e0_publicada_x_vigente']['2023']['dif'], 2, True)}; 2024 {n(M['e0_publicada_x_vigente']['2024']['dif'], 2, True)} anos",
  "medidas.json (e0_publicada_x_vigente). O sinal troca: sobe nos anos 2000-2010 e cai nos anos de pandemia", "sim",
  "Expectativa de vida Bolsonaro (2021, 72,8: so existe na serie revisada; a tabua publicada diz 77,03) e Lula 3* (2023, 76,4)", "revisao_de_vintage")
q("Expectativa de vida", "Tabuas Completas de Mortalidade 2020-2022 (como publicadas)", "2020-2022 (tabuas sem os efeitos da Covid-19)",
  "tabua de 2020 = projecao do nivel de mortalidade de 2010", "tabua revisada pos-Censo 2022 (ver linha anterior)",
  "o IBGE declara que as tabuas de 2020 NAO incorporam a pandemia e serao revistas com o Censo de 2022",
  "https://www.ibge.gov.br/en/statistics/social/population/17117-complete-life-tables.html", "ibge_complete_life_tables",
  "Therefore, the Tables for Brazil for the year of 2020 portray the projection of the mortality created with 2010 data, though not incorporating the effects of the Covid-19 pandemic on the increase of deaths in the Brazilian population.",
  "eleva", "a tabua como publicada superestima 2020-2021 em relacao a serie revisada", f"2020: 76,79 -> 74,8 ({n(M['e0_publicada_x_vigente']['2020']['dif'], 2, True)}); 2021: 77,03 -> 72,8 ({n(M['e0_publicada_x_vigente']['2021']['dif'], 2, True)})",
  "medidas.json (e0_publicada_x_vigente)", "sim", "Expectativa de vida Bolsonaro (2021, 72,8): quem usar a tabua de 2022 (77,03) contra a vigente muda o governo de 'melhor' para 'pior'", "revisao_de_vintage")
q("Expectativa de vida", "ONU/WPP via Banco Mundial WDI x IBGE", "fonte externa (nao e quebra interna)",
  "IBGE (tabuas e projecoes proprias)", "ONU World Population Prospects (espelhada pelo WDI)",
  "a UNPD incorpora a prevalencia estimada de HIV na projecao de alguns paises, incluindo o Brasil, o que reduz levemente a esperanca de vida",
  "https://biblioteca.ibge.gov.br/visualizacao/livros/liv98593.pdf", "liv98593",
  "Na determinação e projeção das tábuas de mortalidade de alguns países, a UNPD incorpora taxas de prevalência de infecção por HIV estimadas, o que resulta numa ligeira diminuição da esperança de vida.",
  "reduz", "diferenca WDI menos IBGE vigente nos marcos em que ambos existem",
  f"WDI menos IBGE vigente: {', '.join(y + ' ' + n(v['dif'], 2, True) for y, v in list(M['e0_wdi_x_vigente'].items()))} (so 2021 e 1960 ficam positivos)",
  "medidas.json (e0_wdi_x_vigente). O WDI nao informa a revisao do WPP usada (lastupdated 2026-10-08) ❓", "nao_declarado",
  "Expectativa de vida: a unica serie com UMA vintage para todos os anos (1960-2024) e a do WDI, 0,3 a 1,5 anos abaixo da vigente do IBGE", "revisao_de_vintage")
q("Expectativa de vida", "Atlas DH/PNUD (Ipeadata EVNNEW, inativa)", "1970-1980 e 1991-2000 (fonte e metodo proprios)",
  "tabua IBGE", "tabua usada pelo Atlas DH",
  "'estimativas podem diferir dependendo da tabua de vida utilizada'",
  "http://www.ipeadata.gov.br/api/odata4/Metadados", "ipeadata",
  "Estimativas podem diferir dependendo da tãbua de vida (taxas de mortalidade por idade) utilizadas.",
  "reduz", "diferenca Atlas DH menos IBGE vigente em 1970", "1970: Atlas 51,43 contra IBGE vigente 57,6 (-6,17 anos) e WDI 57,34", "comparacao direta de series baixadas (social/series/expvida.csv)", "nao_declarado",
  "Expectativa de vida Ditadura (1970, 62,6: nao e do Atlas; coincide com 1980 na Rev. 2008)", "revisao_de_vintage")

# ================================== AGREGADOS MONETARIOS ==================================
mq = {r["agregado"]: r for r in M["monetario_quebra_2018"]}
k17 = "dez2017 (NT48: M1 +5%, M3 -0,4%, M4 -6%)"
q("Agregados monetarios", "M0 (SGS 1788 / Ipeadata)", "1980 (novo conceito de base monetaria)",
  "base monetaria incluindo os depositos a vista do publico no Banco do Brasil (conceito ate 1986)", "conceito em que o Banco do Brasil e tratado como os demais bancos comerciais; BCB retroagiu a serie so ate 1980",
  "alinhar o tratamento do Banco do Brasil ao dos demais bancos",
  "https://www.scielo.br/j/rep/a/fFLPSd4bLmm45CZYQYQbQ4R/?format=pdf&lang=pt", "cysne2004",
  "A partir de 1980, utilizou-se o novo conceito de base monetária, em que o Banco do Brasil é tratado da mesma forma que os demais bancos comerciais.",
  "desconhecida", "sem sobreposicao da serie antiga com a nova antes de 1980", SEM, "nenhuma medicao possivel", "nao_declarado",
  "M0 (% do PIB): Ditadura 5,2 (1967-1974) contra Dilma 4,1, Bolsonaro 4,3 etc.", "mudanca_de_regra")
q("Agregados monetarios", "M2, M3, M4 (SGS 1837, 1840, 1843)", "2001-07 (series refeitas desde jul/1988)",
  "M2 com titulos publicos; M3 = M2 + poupanca; M4 com titulos de instituicoes financeiras", "M2 = M1 + depositos especiais + poupanca; M3 inclui fundos de renda fixa e compromissadas; M4 = M3 + titulos publicos",
  "Padrao Especial de Disseminacao de Dados (PEDD) do FMI e tendencias internacionais",
  "https://www.bcb.gov.br/ftp/infecon/NM-MeiosPagAmplp.pdf", "bcb_nm2001",
  "A reformulação foi implantada a partir do levantamento dos saldos de julho de 2001 e aplicada para elaboração de séries históricas desde julho de 1988.",
  "desconhecida", "as series anteriores a 2001 nao foram achadas no SGS (so as refeitas)", SEM, "nenhuma medicao possivel (bloco monetario)", "sim",
  "M2-M4 (% do PIB) Sarney e Collor (1 e 3 anos de dado apenas)", "mudanca_de_regra")
q("Agregados monetarios", "M1-M4 (SGS 1827/1837/1840/1843 -> 27791/27810/27813/27815)", "2018-11 (NT 48; series 'Novo' desde dez/2001)",
  "metodologia de 2001 (ate jun/2018)", "inclui cooperativas de credito, letras financeiras e de credito, compromissadas com titulos privados; exclui haveres de nao residentes",
  "novos instrumentos e instituicoes ganharam relevancia; o Manual de Estatisticas Monetarias e Financeiras 2016 (MFSM 2016) motivou a edicao",
  "http://www.ipeadata.gov.br/doc/NT%2048_Dstat_Dimob_novembro_2018.pdf", "bcb_nt48",
  "Inovações como essas, verificadas de forma similar nas principais economias, motivaram a edição do MFSM 2016. [...] Na posição de dezembro de 2017, ocorreu redução de 6% no valor nominal do M4, ante o saldo na metodologia anterior. [...] Em dezembro de 2017, o valor do M3 atual foi 0,4% menor que o anterior.",
  "ambigua", "sobreposicao medida (jan/2002-jun/2018): razao Novo/antigo mes a mes",
  f"dez/2017: M1 {n((float(mq['M1'][k17]) - 1) * 100, 1, True)}%, M2 {n((float(mq['M2'][k17]) - 1) * 100, 1, True)}%, M3 {n((float(mq['M3'][k17]) - 1) * 100, 1, True)}%, M4 {n((float(mq['M4'][k17]) - 1) * 100, 1, True)}% (NT 48: +5%, -0,4%, -6%); faixa de M4: {n((float(mq['M4']['minimo']) - 1) * 100, 1, True)}% a {n((float(mq['M4']['maximo']) - 1) * 100, 1, True)}%",
  "monetario/saida/agregados_quebra_2018.csv (bloco monetario) ✅ confere com o texto do BCB", "sim",
  "M1-M4 (% do PIB) Bolsonaro (2019-2022) e Lula 3* (2023-2025) so existem na serie Novo", "metodo_estatistico")
q("Agregados monetarios", "Ipeadata BM12_M2NCN12 e BM12_M1N12 (rotulagem)", "jan/2002-dez/2023 (rotulo do Ipeadata nao e o conteudo)",
  "rotulada M2 / M1 fim de periodo", "conteudo: depositos a vista (SGS 27790) / M1 media dos dias uteis (SGS 27788)",
  "n/d (erro de rotulagem, nao regra)",
  "http://www.ipeadata.gov.br/api/odata4/Metadados", "ipeadata",
  "n/a",
  "ambigua", "comparacao Ipeadata x BCB mes a mes", "264 meses identicos ao SGS 27790 (depositos a vista) em vez do M2; erro de nivel ~90%", "monetario/saida/agregados_ipea_auditoria.csv", "nao",
  "qualquer M2 do Ipeadata antes de 2024", "revisao_de_vintage")
q("Agregados monetarios e salario minimo", "unidade monetaria (SGS, Ipeadata)", "1967-02, 1986-03, 1989-01, 1993-08, 1994-07 (cortes de zeros)",
  "moeda anterior", "cruzeiro novo, cruzado, cruzado novo, cruzeiro real, real (divisores 1000, 1000, 1000, 1000, 2750)",
  "reformas monetarias (decretos e leis)",
  "https://www.bcb.gov.br/content/acessoinformacao/museudocs/pub/SintesePadroesMonetariosBrasileiros.pdf", "bcb_museu",
  "mil cruzeiros = um cruzeiro novo",
  "desconhecida", "efeito puramente de unidade; sem efeito nas razoes ao PIB depois de convertido", "divisor acumulado 2,75 x 10^15 para saldo anterior a fev/1967", "monetario/saida/fatores_de_conversao.csv", "nao_declarado",
  "M0-M4 (% do PIB) e salario minimo nominal em qualquer janela que cruze os cortes", "mudanca_de_regra")

if FALHAS:
    print("\n".join(FALHAS))
    sys.exit(f"{len(FALHAS)} citacoes nao encontradas")
CAB = ["indicador", "serie", "data_quebra", "metodo_antigo", "metodo_novo", "razao_declarada_pela_fonte", "fonte_primaria_url", "trecho_citado", "direcao_do_efeito",
       "como_a_direcao_foi_determinada", "efeito_medido", "como_medido", "apresentada_como_aprimoramento", "celulas_do_infografico_afetadas", "tipo_de_quebra"]
with open(H / "quebras.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=CAB)
    w.writeheader()
    w.writerows(LINHAS)
print(len(LINHAS), "quebras")
