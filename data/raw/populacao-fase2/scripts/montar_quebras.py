#!/usr/bin/env python3
"""Escreve quebras.csv (cabecalho identico ao de moeda-fiscal/quebras.csv). Numeros do campo efeito_medido vem de derivado/conferencia_mesmo_ano.csv."""
import csv
P = "/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/populacao-fase2/"
H = open("/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/moeda-fiscal/quebras.csv", encoding="utf-8").readline().strip().split(",")
C = {int(r["ano"]): r for r in csv.DictReader(open(P + "derivado/conferencia_mesmo_ano.csv"))}
def v(a, k): return C[a][k]
TN = "http://tabnet.datasus.gov.br/cgi/"
IB = "https://ftp.ibge.gov.br/Registro_Civil/Tabelas_de_Resultados/2024/xlsx/indice_tabelas_registro_civil.xlsx"
R = []
R.append(["obitos_total_por_ocorrencia / _por_residencia", "DATASUS SIM TabNet obt09uf (1979-1995) e obt10uf (1996-2026)", "1996 (CID-9 ate 1995; CID-10 desde 1996)",
          "CID-9 (9a Revisao), base TabNet obt09uf", "CID-10 (10a Revisao), base TabNet obt10uf",
          "Devido as diferencas entre as revisoes nao foi possivel gerar uma lista que as compatibilizasse (nota DATASUS)", TN + "sim/Mortalidade_Geral_1996_2012.pdf",
          "A partir de 1996, as declaracoes de obito passaram a ser codificadas utilizando-se a 10a Revisao da Classificacao Internacional de Doencas - CID-10. Ate entao, era utilizada a 9a Revisao - CID-9. Devido as diferencas entre as revisoes, nao foi possivel gerar uma lista que as compatibilizasse.",
          "nenhuma no total de obitos (a revisao muda a codificacao da CAUSA, nao a contagem); incompativel por causa", "texto da nota tecnica; o total e todas as causas",
          f"total SIM 1995 = {v(1995,'sim_obitos_ocorrencia')} -> 1996 = {v(1996,'sim_obitos_ocorrencia')} (+1,7%); razao SIM/ONU WPP 0,8451 -> 0,8569; variacao ano a ano vizinha: 1994->1995 +0,7%, 1996->1997 -0,6%",
          "derivado/conferencia_mesmo_ano.csv (script scripts/conferencia.py)", "nao declarado pela fonte", "nenhuma: indicador fora do infografico original; afeta a serie indicada", "mudanca_de_classificacao"])
R.append(["obitos_total_por_ocorrencia (SIM 1979-2010)", "DATASUS SIM TabNet", "1979-2010, cobertura crescente (sem data unica)",
          "SIM com cobertura incompleta de obitos nas decadas de 1980-1990", "SIM com cobertura proxima da completa (razao a ONU ~1,0 em 2010)",
          "nao declarada no texto salvo da nota do TabNet (a nota nao cita cobertura/sub-registro de obitos)", TN + "sim/Mortalidade_Geral_1979_1995.pdf",
          "(nota sem trecho sobre cobertura; a razao e inferida da comparacao com a ONU, que e estimativa)", "SIM subestima obitos nos anos iniciais (razao < 1)", "comparacao com ONU WPP 2024 (estimativa, nao verdade-terreno)",
          f"SIM/ONU WPP: 1980 = {v(1980,'sim/wpp')}; 1990 = {v(1990,'sim/wpp')}; 2000 = {v(2000,'sim/wpp')}; 2010 = {v(2010,'sim/wpp')}",
          "derivado/conferencia_mesmo_ano.csv", "nao declarado pela fonte", "nenhuma: indicador fora do infografico original", "cobertura"])
R.append(["obitos_total_por_* (SIM, 2011)", "DATASUS SIM TabNet obt10uf", "2011", "formulario antigo da Declaracao de Obito", "novo formulario, com maior detalhamento; os dois formularios coexistiram em 2011",
          "maior detalhamento das informacoes coletadas", TN + "sim/Mortalidade_Geral_1996_2012.pdf",
          "Em 2011, houve uma mudanca no conteudo da Declaracao de Obito, com maior detalhamento das informacoes coletadas. Para este ano, foram utilizados simultaneamente os dois formularios.",
          "desconhecida", "nota diz ver documento 'Consolidacao da base de dados de 2011', nao baixado", "nao medido no total", "nao medido: sem pareamento dos dois formularios",
          "nao declarado pela fonte", "nenhuma: indicador fora do infografico original", "mudanca_de_formulario"])
R.append(["obitos_total_por_* e nascidos_vivos_por_* (anos recentes)", "DATASUS SIM e SINASC TabNet", "2024 final; 2025 preliminar; 2026 previa",
          "dados finais (extracao 02/12/2025)", "2025 preliminar (extracao 28/07/2026); 2026 2a previa (extracao 01/09/2026), ano incompleto",
          "consolidacao: a base nacional so e considerada completa quando todas as UF enviaram dados", TN + "sim/Mortalidade_Geral_1996_2012.pdf",
          "Dados finais disponiveis ate 2024 - data de extracao 02/12/2025. Dados de 2025 - Preliminares - data de extracao 28/07/2026. Dados de 2026 - 2a previa - data de extracao 01/09/2026. (nota na pagina do TabNet; ver bruto/tabnet_sim_obt10uf_ano.html)",
          "2025 pode subir ao ser consolidado; 2026 e parcial (nao e total anual)", "texto da nota", f"2026 parcial: SIM 912.010 obitos e SINASC 1.504.579 nascidos (so parte do ano)", "leitura direta do TabNet", "nao declarado pela fonte",
          "nenhuma: indicador fora do infografico original", "vintage_preliminar"])
R.append(["nascidos_vivos_por_ocorrencia / _por_residencia_mae (SINASC 1994-2000s)", "DATASUS SINASC TabNet nvuf", "1994 em diante, implantacao gradual",
          "SINASC implantado em todas as UF desde 1994 mas coleta nao cobria todos os municipios", "cobertura gradualmente completa",
          "a implantacao do SINASC foi gradativa (nota DATASUS)", TN + "sinasc/Nascidos_Vivos_1994_2012.pdf",
          "A implantacao do SINASC foi gradativa. Assim, ao analisar os dados, deve-se atentar que, apesar de implantado em todas as Unidades da Federacao desde 1994, em algumas delas a coleta nao abrange todos os municipios.",
          "SINASC subestima nascimentos nos primeiros anos", "texto da nota + comparacao com ONU WPP 2024 (estimativa)",
          f"SINASC/ONU WPP: 1994 = {v(1994,'sinasc/wpp')}; 1995 = {v(1995,'sinasc/wpp')}; 2000 = {v(2000,'sinasc/wpp')}; 2010 = {v(2010,'sinasc/wpp')}",
          "derivado/conferencia_mesmo_ano.csv", "nao declarado pela fonte", "nenhuma: indicador fora do infografico original", "cobertura"])
R.append(["nascidos_vivos_por_* (SINASC, 2011)", "DATASUS SINASC TabNet nvuf", "2011", "formulario antigo da Declaracao de Nascido Vivo", "novo formulario, mais detalhado; os dois coexistiram em 2011",
          "maior detalhamento das informacoes coletadas", TN + "sinasc/Nascidos_Vivos_1994_2012.pdf",
          "Em 2011, houve uma mudanca no conteudo da Declaracao de Nascidos Vivos, com maior detalhamento das informacoes coletadas. Para este ano, foram utilizados simultaneamente os dois formularios.",
          "desconhecida", "nota remete a documento 'Consolidacao do SINASC - 2011', nao baixado", "nao medido no total", "nao medido", "nao declarado pela fonte", "nenhuma: indicador fora do infografico original", "mudanca_de_formulario"])
R.append(["nascidos_vivos_registrados_no_ano (IBGE RC)", "IBGE Registro Civil SIDRA tab. 192 (1984-2002) e 2609/2679 (2003-2024)", "1984-2002 (registro gratuito desde Lei 9.534, dez/1997) e 2003+",
          "registros do ano incluem registro tardio acumulado (antes de 1997 o registro era pago; sub-registro historicamente alto)", "registros do ano com sub-registro baixo e registros tardios em queda",
          "a gratuidade do registro de nascimento passou a vigorar em 1997 (art. 30 da Lei 9.534, de 10.12.1997); houve melhora paulatina da cobertura desde 2000 (IBGE nota tecnica 01/2020)", "https://biblioteca.ibge.gov.br/visualizacao/periodicos/3099/rc_sev_esn_2018.pdf",
          "Desde o final da decada de 1990 e ao longo dos anos 2000, inumeras campanhas e iniciativas governamentais para a erradicacao do sub-registro foram implementadas, sendo a mais importante delas a determinacao da gratuidade do registro de nascimento, que passou a vigorar em 1997 (Art. 30 da Lei n. 9.534, de 10.12.1997).",
          "'registrados no ano' superestima os nascimentos do ano quando ha registro tardio (anos 1996-2002) e subestima quando ha sub-registro", "comparacao com SINASC e ONU WPP no mesmo ano",
          f"registrados/ONU WPP: 1996 = {v(1996,'rc_registrados/wpp ')}; 1997 = {v(1997,'rc_registrados/wpp ')}; 2000 = {v(2000,'rc_registrados/wpp ')}; 2002 = {v(2002,'rc_registrados/wpp ')}; 2010 = {v(2010,'rc_registrados/wpp ')}; 2023 = {v(2023,'rc_registrados/wpp ')}",
          "derivado/conferencia_mesmo_ano.csv", "nao declarado pela fonte", "nenhuma: indicador fora do infografico original", "cobertura"])
R.append(["nascidos_vivos_ocorridos_no_ano (IBGE RC)", "IBGE Registro Civil SIDRA tab. 706 (1984-2002) e 2612 (2003-2024)", "2002 -> 2003 (troca de tabela SIDRA)",
          "tab. 706 (1984-2002)", "tab. 2612 (2003-2024)", "nao declarada no que foi baixado (portal ibge.gov.br bloqueado por Cloudflare; nao li as notas das tabelas)", IB,
          "(sem trecho: tabelas distintas no catalogo de agregados do IBGE, periodos 1984-2002 e 2003-2024)", "salto para cima em 2003", "comparacao de 2002 com 2003 contra SINASC e ONU, que nao tem salto",
          f"RC ocorridos 2002 = {v(2002,'ibge_rc_nascidos_ocorridos')} -> 2003 = {v(2003,'ibge_rc_nascidos_ocorridos')} (+8,9%); SINASC 2002 = {v(2002,'sinasc_nascidos_ocorrencia')} -> 2003 = {v(2003,'sinasc_nascidos_ocorrencia')} (-0,7%); ONU WPP 2002 -> 2003 = -2,5% (calculado) (derivado/conferencia_mesmo_ano.csv)",
          "derivado/conferencia_mesmo_ano.csv", "nao declarado pela fonte", "nenhuma: indicador fora do infografico original", "metodo_estatistico"])
R.append(["obitos_ocorridos_e_registrados_no_ano -> obitos_ocorridos_no_ano (IBGE RC)", "IBGE Registro Civil SIDRA tab. 367 (1984-2002) e 2654 (2003-2024)", "2002 -> 2003",
          "obitos ocorridos E registrados no mesmo ano (definicao restrita)", "obitos ocorridos no ano (registro completado ate o fechamento)", "definicoes distintas nas tabelas (nomes das variaveis no catalogo SIDRA: v224 e v343)", "https://servicodados.ibge.gov.br/api/v3/agregados/367/metadados",
          "var 224 'Numero de obitos ocorridos e registrados no ano' (tab. 367, 1984-2002); var 343 'Numero de obitos ocorridos no ano' (tab. 2654, 2003-2024)", "salto para cima em 2003 (definicao menos restrita)",
          "comparacao com SIM e ONU no mesmo ano", f"RC/ONU WPP: 2002 = {v(2002,'rc_ocorridos/wpp')}; 2003 = {v(2003,'rc_ocorridos/wpp')}; SIM/ONU 2002 = {v(2002,'sim/wpp')}; 2003 = {v(2003,'sim/wpp')}",
          "derivado/conferencia_mesmo_ano.csv", "nao declarado pela fonte", "nenhuma: indicador fora do infografico original", "mudanca_de_definicao"])
R.append(["nascidos_vivos_registrados_no_ano vs _lugar_registro; obitos_registrados_no_ano vs _lugar_registro (IBGE RC 2003+)", "IBGE Registro Civil SIDRA tab. 2609 x 2679; 2682 x 2684", "2003-2024",
          "tab. 2609/2682: por lugar de residencia (mae/falecido); exclui residentes no exterior ou ignorados", "tab. 2679/2684: por lugar do registro (contagem completa dos registros no Brasil)",
          "recortes territoriais distintos", "https://servicodados.ibge.gov.br/api/v3/agregados/2679/metadados", "(nomes das tabelas no catalogo: 'lugar de residencia da mae' x 'lugar do registro')", "residencia < registro (exclui nao residentes)", "diferenca direta entre as duas tabelas, mesmo ano",
          "nascidos registrados 2003: 3.408.540 (residencia) x 3.426.727 (lugar do registro), diferenca +0,53%; obitos registrados 2003: 1.001.813 (residencia) x 1.005.882 (lugar do registro), +0,41%", "series/ibge_registro_civil.csv (duas linhas por ano)", "nao declarado pela fonte", "nenhuma: indicador fora do infografico original", "mudanca_de_definicao"])
R.append(["estimativa de sub-registro de nascimentos (IBGE, nao baixada como serie)", "IBGE Estatisticas do Registro Civil, nota tecnica 01/2020", "2015 -> 2020 (nota de 2020)",
          "estimativa por metodos demograficos indiretos (censos e pesquisas domiciliares)", "pareamento Registro Civil x SINASC com captura-recaptura; sub-registro = nao registrados ate o 1o trimestre do ano seguinte, sem registros tardios",
          "cobertura proxima da totalidade; metodo indireto deixou de se justificar", "https://biblioteca.ibge.gov.br/visualizacao/periodicos/3099/rc_sev_esn_2018.pdf",
          "Com a melhoria da qualidade e a cobertura do registro de nascimentos se aproximando da quase totalidade de nascimentos ocorridos no Pais, o IBGE entendeu que nao mais se justificaria a utilizacao de estimativas demograficas indiricas para o calculo da estimativa do sub-registro de nascimentos.".replace("indiricas", "indiretas"),
          "estimativas pre e pos nao comparaveis em nivel", "texto da nota", "nao medido: serie de sub-registro nao baixada (so a nota tecnica e dois decks de slides, bruto/ibge_sub_registro_2022_a.pdf e _b.pdf)", "n/a", "apresentada como metodo melhor (cobertura quase total)", "nenhuma: indicador fora do infografico original", "metodo_estatistico"])
R.append(["nascimentos_wpp / obitos_wpp / *_estimados_wdi (vintage ONU)", "ONU World Population Prospects 2024 (e Banco Mundial WDI, que a reproduz)", "ano 2024 em diante (WPP 2024 estima ate 2023)",
          "estimativa (anos <= 2023, conforme documentacao WPP 2024, nao verificado no arquivo)", "projecao variante Medium (anos >= 2024)", "WPP 2024 publicado em 2024; revisoes bienais substituem a serie inteira", "https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz",
          "(coluna Variant = Medium em todas as linhas; limite estimativa/projecao conforme documentacao do WPP 2024, que nao baixei: tratar como hipotese nao verificada no arquivo)",
          "projecao 2024+ acima dos registros em nascimentos", "comparacao com SINASC e Registro Civil, mesmo ano",
          f"SINASC/ONU WPP: 2023 = {v(2023,'sinasc/wpp')}; 2024 = {v(2024,'sinasc/wpp')}; RC registrados/WPP 2024 = {v(2024,'rc_registrados/wpp ')}",
          "derivado/conferencia_mesmo_ano.csv", "nao declarado pela fonte", "nenhuma: indicador fora do infografico original", "vintage_revisao"])
with open(P + "quebras.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(H)
    for r in R:
        assert len(r) == len(H), (len(r), len(H), r[0])
        w.writerow(r)
print(len(R), "quebras")
