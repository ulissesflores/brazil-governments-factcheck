#!/usr/bin/env python3
"""Escreve quebras.csv. Cada trecho_citado e conferido literalmente contra o PDF baixado (pdftotext)."""
import csv, re, subprocess
from pathlib import Path
P = Path("/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/ipca-itens-fase2")
FTP = "https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/Sistema_de_Indices_de_Precos_ao_Consumidor/"
def txt(n):
    t = subprocess.run(["pdftotext", "-layout", str(P / "bruto/ibge" / n), "-"], capture_output=True, text=True).stdout
    t = re.sub(r"\s+", " ", t)
    return re.sub(r"(\w)- (\w)", r"\1\2", t)  # junta hifenizacao de fim de linha do PDF
T = {k: txt(v) for k, v in {
    "nt11": "snipc-nt-01-2011-estruturas-pof-2008-2009.pdf", "nt19": "snipc-nt-02-2019-estruturas-pof-2017-2018.pdf",
    "nt20_03": "snipc-nt-03-2020-plano-de-saude.pdf", "nt20_05": "snipc-nt-05-2020-plano-de-saude.pdf",
    "mc6": "snipc-metodos-de-calculo-6ed.pdf"}.items()}
def q(k, s):
    s = re.sub(r"\s+", " ", s)
    assert s in T[k], (k, s[:60])
    return s
SEM = "nenhuma: indicador fora do infografico original; afeta a serie indicada no campo serie"
NOVERLAP = "nao medido: as tabelas SIDRA nao se sobrepoem em nenhum mes (cada uma comeca no mes seguinte ao fim da anterior), logo nao ha mes calculado nas duas estruturas"
rows = []
H = ["indicador","serie","data_quebra","metodo_antigo","metodo_novo","razao_declarada_pela_fonte","fonte_primaria_url","trecho_citado",
     "direcao_do_efeito","como_a_direcao_foi_determinada","efeito_medido","como_medido","apresentada_como_aprimoramento",
     "celulas_do_infografico_afetadas","tipo_de_quebra"]
rows.append(["ipca_{geral,aluguel_residencial}_var_mensal","IBGE SIDRA t58 -> t655 (geral c72/2640 -> c315/7169; aluguel c72/1935 -> c315/7448)","1999-08",
 "tabela 58 (1991-01 a 1999-07), classificacao c72; lista de categorias baixada nao tem subitem de plano de saude","tabela 655 (1999-08 a 2006-06), classificacao c315, com 6203001 Plano de saude (c315/7696)",
 "nao declarada nos arquivos baixados; o titulo SIDRA apenas delimita 'de agosto/1999 ate junho/2006'. O Metodos de calculo 6a ed. lista a POF 1995-1996 entre as que geraram estruturas de ponderacao, sem datar a implantacao",
 FTP+"Metodos_de_calculo/Metodos_de_Calculo_6ed.pdf",
 q("mc6","POF 1987-1988, POF 1995-1996, POF 2002-2003 e POF 2008-2009."),
 "desconhecida","nao ha mes sobreposto; a data de implantacao de agosto/1999 NAO foi confirmada em nota tecnica baixada (so o corte de periodo do SIDRA)",
 "nao medido: "+NOVERLAP.split(": ",1)[1],
 "peso mensal do aluguel residencial em ago/1999 (primeiro mes da t656) = 5.9172%; nao ha peso da t58 baixado para comparar",
 "nao declarado pela fonte",SEM,"mudanca_de_cesta"])
rows.append(["ipca_{geral,aluguel_residencial}_var_mensal","IBGE SIDRA t58 (set/1991 e abr/1991)","1991-04 e 1991-09",
 "serie mensal","abr/1991 do aluguel vem '-' na fonte; ago/1991 nao existe na tabela 58 e set/1991 do geral (33,71%) coincide com 2 meses compostos de 15,63% (SGS 433 traz 15,63 em ago e set)",
 "nao declarada nos arquivos baixados","https://servicodados.ibge.gov.br/api/v3/agregados/58/periodos",
 "periodos da tabela 58 em 1991: 199101, 199102, 199103, 199104, 199105, 199106, 199107, 199109, 199110, 199111, 199112 (sem 199108)",
 "desconhecida","contagem dos periodos da tabela 58 baixada; comparacao com BCB SGS 433","set/1991 geral: SIDRA 33,71% vs SGS 433 15,63% (diferenca 18,08 pp); (1,1563^2 - 1) = 33,70%",
 "diferenca direta SIDRA x SGS 433 por mes (scripts/construir.py); composicao 1,1563^2 e minha inferencia, nao declarada pelo IBGE","nao declarado pela fonte",SEM,"lacuna_na_fonte"])
rows.append(["ipca_plano_saude_var_mensal","IBGE SIDRA t655 c315/7696","2001-07 (aprox.; a fonte diz 'desde 2001')",
 "ago/1999 a jun/2001: serie irregular, com +3,65% em ago/2000 e dez meses de variacao 0,0 (set/2000 a jun/2001)",
 "a partir de jul/2001: fracao mensal do reajuste anual de contratos individuais (~0,65% a 0,71% ao mes em 2001-2002); metodo descrito pelo IBGE: reajuste anual de cada operadora -> raiz 12 -> media geometrica",
 "descricao do metodo no Metodos de calculo; o texto nao explica como o subitem era medido antes de 2001",
 FTP+"Metodos_de_calculo/Metodos_de_Calculo_6ed.pdf",
 q("mc6","o IBGE, desde 2001, apropria os percentuais de reajuste incidentes sobre os contratos assinados num período de um ano ou mais, abrangendo a maioria dos usuários."),
 "desconhecida","nao ha serie sobreposta nos dois metodos; so o padrao dos dados e o texto 'desde 2001'","10 meses seguidos de variacao 0,0 (2000-09 a 2001-06) contra 0,68-0,71 ao mes de 2001-07 a 2001-12",
 "leitura direta de series/ipca_plano_saude_var_mensal_sidra655.csv","nao declarado pela fonte",
 "nenhuma: indicador fora do infografico original; as janelas dez/1999-dez/2024 do RESULTADO.md cruzam esta quebra (janela de sensibilidade dez/2001-dez/2024 incluida)","metodo_estatistico"])
rows.append(["ipca_*_var_mensal","IBGE SIDRA t655 -> t2938","2006-07","estrutura de ponderacao anterior (t655, ate 2006-06)","estrutura de ponderacao da POF 2002-2003 (t2938, desde 2006-07)",
 "atualizacao das estruturas de ponderacao a partir da POF 2002-2003; no mesmo ato os itens sazonais alimenticios deixaram de ser tratados a parte (Paasche com pesos mensais -> Laspeyres com pesos anuais)",
 FTP+"Metodos_de_calculo/Metodos_de_Calculo_6ed.pdf",
 q("mc6","Com a implantação das estruturas de ponderação em julho de 2006, passou-se a adotar a fórmula geral do Snipc – Laspeyres com pesos anuais."),
 "desconhecida",NOVERLAP.replace("nao medido: ",""),
 "peso mensal: aluguel residencial 3.7804% (2006-06) -> 2.6907% (2006-07); plano de saude 2.7911% -> 3.1642%",
 "diferenca dos pesos mensais publicados no ultimo mes da t656 e no primeiro da t2938 (series/*peso_mensal*); o salto inclui a evolucao Laspeyres de um mes, nao so o reset","nao declarado pela fonte",SEM,"mudanca_de_cesta"])
rows.append(["ipca_*_var_mensal","IBGE SIDRA t2938 -> t1419","2012-01","estrutura POF 2002-2003 (t2938, ate 2011-12)","estrutura POF 2008-2009 (t1419, desde 2012-01)",
 "atualizacao das estruturas de ponderacao a partir da POF 2008-2009; concepcao geral inalterada",
 FTP+"Notas_Tecnicas/atualizacao_das_estruturas_POF2008_2009.pdf",
 q("nt11","A partir do mês de referência de janeiro de 2012, os resultados do Índice Nacional de Preços ao Consumidor Amplo - IPCA e do Índice Nacional de Preços ao Consumidor - INPC, a serem divulgados em fevereiro, terão incorporadas as estruturas de gastos geradas a partir da Pesquisa de Orçamentos Familiares - POF 2008-2009.")
 +" | "+q("nt11","A concepção geral do sistema de índices se mantém inalterada tanto no que se refere aos procedimentos de coleta, crítica e imputação, quanto ao método geral de cálculo e abrangência geográfica, tendo sido atualizadas algumas nomenclaturas de subitens."),
 "desconhecida",NOVERLAP.replace("nao medido: ",""),
 "peso mensal: aluguel residencial 2.9408% (2011-12) -> 3.6971% (2012-01); plano de saude 3.5112% -> 3.0481%",
 "diferenca dos pesos mensais publicados em dez/2011 (t2938) e jan/2012 (t1419); inclui um mes de evolucao Laspeyres","atualizacao de estruturas, nao apresentada como aprimoramento",SEM,"mudanca_de_cesta"])
rows.append(["ipca_*_var_mensal","IBGE SIDRA t1419 -> t7060","2020-01","estrutura POF 2008-2009 (t1419, ate 2019-12)","estrutura POF 2017-2018 (t7060, desde 2020-01)",
 "atualizacao das estruturas de ponderacao a partir da POF 2017-2018; concepcao geral inalterada",
 FTP+"Notas_Tecnicas/snipc_nota_tecnica_2019_02.pdf",
 q("nt19","A partir do mês de referência de janeiro de 2020, os resultados do Índice Nacional de Preços ao Consumidor Amplo - IPCA e do Índice Nacional de Preços ao Consumidor - INPC, a serem divulgados em fevereiro, terão incorporadas as estruturas de gastos geradas a partir da Pesquisa de Orçamentos Familiares - POF 2017-2018.")
 +" | "+q("nt19","A concepção geral do sistema de índices se mantém inalterada tanto no que se refere aos procedimentos de coleta, crítica e imputação, quanto ao método geral de cálculo e abrangência geográfica, tendo sido atualizadas algumas nomenclaturas de subitens."),
 "desconhecida",NOVERLAP.replace("nao medido: ",""),
 "peso mensal: aluguel residencial 3.8193% (2019-12) -> 3.7845% (2020-01); plano de saude 4.3414% -> 4.0243%",
 "diferenca dos pesos mensais publicados em dez/2019 (t1419) e jan/2020 (t7060); inclui um mes de evolucao Laspeyres","atualizacao de estruturas, nao apresentada como aprimoramento",SEM,"mudanca_de_cesta"])
rows.append(["ipca_plano_saude_var_mensal","IBGE SIDRA t7060 c315/7696","2020-09 a 2021-12",
 "fracao mensal do reajuste anual da ANS (ex.: +0,60% ao mes de mai a ago/2020)","set/2020: desconta o fator apropriado antecipadamente (-2,31%); out-dez/2020: variacao nula; 2021: fracao do reajuste suspenso de 2020 em 12 parcelas, somada a do novo ciclo",
 "a ANS suspendeu a aplicacao de reajustes ate o fim de 2020 (pandemia) e depois definiu a recomposicao em 12 parcelas em 2021",
 FTP+"Notas_Tecnicas/snipc_nota_tecnica_2020_03.pdf e snipc_nota_tecnica_2020_05.pdf",
 q("nt20_03","a Agência Nacional de Saúde Suplementar (ANS) decidiu suspender a aplicação de reajustes aos contratos de planos de saúde para todos os tipos de plano até o fim de 2020.")
 +" | "+q("nt20_03","Nos meses subsequentes, a variação do subitem plano de saúde será nula, até que seja anunciado o novo percentual de reajuste definido pela ANS.")
 +" | "+q("nt20_05","a recomposição dos reajustes suspensos em 2020, em decorrência da pandemia do novo Coronavírus, será realizada por meio de 12 parcelas no ano de 2021."),
 "desconhecida","nao se compara com contrafactual; a soma 2020-2021 e neutra por construcao (desconto e recomposicao)",
 "var. mensal: 2020-08 +0,60; 2020-09 -2,31; 2020-10/11/12 0,00; 2021-01 +0,66; 2021-02 +0,67",
 "leitura direta de series/ipca_plano_saude_var_mensal_sidra7060.csv","nao declarado pela fonte",SEM,"metodo_estatistico"])
with (P/"quebras.csv").open("w", newline="") as f:
    w = csv.writer(f); w.writerow(H); w.writerows(rows)
print(len(rows), "quebras")
