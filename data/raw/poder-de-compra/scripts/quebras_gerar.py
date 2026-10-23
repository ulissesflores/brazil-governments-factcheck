#!/usr/bin/env python3
"""Gera ../quebras.csv (mesmas colunas de ../../quebras/quebras.csv). Cada trecho citado e CONFERIDO contra o texto do arquivo hasheado (assert).
python3 -I quebras_gerar.py   (sem rede; usa pdftotext)"""
import csv
import html
import json
import re
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
D = RAIZ.parent
norm = lambda s: re.sub(r"\s+", " ", s)


def pdf(p):
    return norm(subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True, check=True).stdout)


def htm(p):
    return norm(html.unescape(re.sub(r"<[^>]+>", " ", Path(p).read_bytes().decode("utf-8", "ignore"))))


def meta(cod, campo="SERCOMENTARIO"):
    for r in json.load(open(D / "economia-real/meta/ipeadata-Metadados-catalogo-completo-raw.json"))["value"]:
        if r["SERCODIGO"] == cod:
            return norm(html.unescape(re.sub(r"<[^>]+>", " ", r[campo] or "")))


FONTES = {
    "nt_pnadc": pdf(RAIZ / "bruto/ibge-pnadc-notas-tecnicas-v1.19.pdf"),
    "nt_pme_pnad": pdf(D / "quebras/bruto/ibge-liv101823.pdf"),
    "nt03_2021": pdf(D / "quebras/bruto/ibge-liv101866.pdf"),
    "cesta": pdf(RAIZ / "bruto/dieese-metodologia-cesta-basica-2016.pdf"),
    "icv": htm(RAIZ / "bruto/dieese-icv-pagina-novo.html"),
    "l14601": htm(D / "quebras/bruto/planalto/l14601-2023.html"),
    "mte": meta("MTE12_SALMIN12"), "sr": meta("GAC12_SALMINRE12"), "fipe": meta("FIPE12_IPCFIPE12"),
}
COLS = ["indicador", "serie", "data_quebra", "metodo_antigo", "metodo_novo", "razao_declarada_pela_fonte", "fonte_primaria_url", "trecho_citado", "direcao_do_efeito",
        "como_a_direcao_foi_determinada", "efeito_medido", "como_medido", "apresentada_como_aprimoramento", "celulas_do_infografico_afetadas", "tipo_de_quebra"]
BIB = "https://biblioteca.ibge.gov.br/visualizacao/livros/"
L = []


def q(fonte, trecho, **kw):
    assert norm(trecho) in FONTES[fonte], (fonte, trecho[:60])
    L.append({**{c: "" for c in COLS}, "trecho_citado": norm(trecho), **kw})


q("nt_pnadc", "Este conceito de pessoas ocupadas, adotado a partir do quarto trimestre de 2015, já está ajustado à Resolução I da 19a CIET",
  indicador="Trabalho", serie="PNAD Continua, pessoas ocupadas (SIDRA 4093, 4099)", data_quebra="2015T4",
  metodo_antigo="ocupada: trabalho remunerado sem ajuda a parente em outro domicilio; afastamento remunerado por doenca ou licenca por <4 meses; sem remuneracao so se continuava a receber parte do pagamento",
  metodo_novo="ocupada ajustada a Resolucao I da 19a CIET: inclui trabalho sem remuneracao direta em ajuda a parente que reside em outro domicilio; afastamento de ate 4 meses",
  razao_declarada_pela_fonte="ajuste a Resolucao I da 19a CIET", fonte_primaria_url=BIB + "liv102172_notas_tecnicas.pdf",
  direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="o IBGE nao publica serie nos dois conceitos nos arquivos baixados",
  efeito_medido="sem sobreposicao nos dados baixados", como_medido="nenhuma medicao possivel", apresentada_como_aprimoramento="sim",
  celulas_do_infografico_afetadas="nivel da ocupacao e taxa de desocupacao PNADC, Dilma 2011-2016 (a quebra cai dentro do mandato)", tipo_de_quebra="metodo_estatistico")
q("nt_pnadc", "Este conceito de pessoas desocupadas, adotado a partir do segundo trimestre 2016, já está ajustado à Resolução I da 19a CIET",
  indicador="Trabalho", serie="PNAD Continua, taxa de desocupacao (SIDRA 4099)", data_quebra="2016T2",
  metodo_antigo="desocupada incluia quem ja tinha conseguido trabalho para comecar depois da semana de referencia, sem limite de tempo para o inicio",
  metodo_novo="so entra quem comecaria em menos de quatro meses apos a semana de referencia",
  razao_declarada_pela_fonte="ajuste a Resolucao I da 19a CIET", fonte_primaria_url=BIB + "liv102172_notas_tecnicas.pdf",
  direcao_do_efeito="reduz", como_a_direcao_foi_determinada="o novo criterio e mais restritivo que o antigo (um subconjunto): so pode manter ou diminuir o numero de desocupados",
  efeito_medido="sem sobreposicao nos dados baixados", como_medido="nenhuma medicao possivel; magnitude nao publicada nos arquivos baixados", apresentada_como_aprimoramento="sim",
  celulas_do_infografico_afetadas="taxa de desocupacao PNADC, Dilma (2011-2016) e Temer (2016-2018): a quebra cai na fronteira dos dois mandatos", tipo_de_quebra="metodo_estatistico")
q("nt_pme_pnad", "Desde 2012, quando teve início o processo de implantação da PNAD Contínua, o IBGE vem mantendo paralelamente o levantamento das duas principais pesquisas sobre a força de trabalho do País",
  indicador="Trabalho", serie="PNAD anual (Ipeadata DISOC_DESE) -> PNAD Continua (SIDRA 4562/4099)", data_quebra="2012 (inicio da PNAD Continua; PNAD anual termina em 2015)",
  metodo_antigo="PNAD: pessoas de 10 anos ou mais; desocupada = tomou providencia efetiva NA SEMANA de referencia",
  metodo_novo="PNAD Continua: pessoas de 14 anos ou mais; desocupada = tomou providencia efetiva no periodo de referencia de 30 DIAS e estava disponivel na semana",
  razao_declarada_pela_fonte="harmonizacao metodologica do Sistema Integrado de Pesquisas Domiciliares (SIPD)", fonte_primaria_url=BIB + "liv101823.pdf",
  direcao_do_efeito="ambigua", como_a_direcao_foi_determinada="a janela de busca de 30 dias tende a elevar e o corte de idade em 14 anos tende a alterar a forca de trabalho; o sinal medido na sobreposicao muda de ano para ano",
  efeito_medido="PNADC menos PNAD: +0,67 p.p. em 2012 (7,4 contra 6,728), +0,15 p.p. em 2013 (7,3 contra 7,148), -0,54 p.p. em 2014 (7,0 contra 7,538)",
  como_medido="sobreposicao 2012-2014 entre economia-real/saida-desemprego-anual.csv, colunas PNAD_DISOC_DESE_Brasil e PNADC_SIDRA_4562 (a PNADC anual vem arredondada a 0,1)",
  apresentada_como_aprimoramento="sim", celulas_do_infografico_afetadas="desemprego anual 1992-2015 (PNAD) contra 2012-2026 (PNADC): a comparacao entre Itamar/FHC/Lula e Dilma em diante cruza esta quebra", tipo_de_quebra="metodo_estatistico")
q("nt03_2021", "a partir do segundo trimestre de 2020, o IBGE alterou a forma de coleta de dados da Pesquisa, que antes era totalmente feita de forma presencial, para exclusivamente por telefone",
  indicador="Trabalho", serie="PNAD Continua, todos os indicadores (SIDRA 4093, 4099, 6813)", data_quebra="2020T2 (coleta so por telefone) e 2021 (reponderacao)",
  metodo_antigo="coleta presencial; pesos sem calibracao por sexo e grupo etario",
  metodo_novo="coleta exclusivamente por telefone a partir de 2020T2; reponderacao com calibracao por sexo e grupo etario divulgada em 2021",
  razao_declarada_pela_fonte="seguranca de entrevistados e entrevistadores na pandemia; queda da taxa de aproveitamento da amostra", fonte_primaria_url=BIB + "liv101866.pdf",
  direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="a nota diz que simulacoes nao apontaram vies nos principais indicadores de Brasil, Grandes Regioes e UFs; nao ha comparacao dos dois metodos no mesmo trimestre",
  efeito_medido="sem sobreposicao nos dados baixados", como_medido="nenhuma medicao possivel por mim; o IBGE reporta nao ter achado vies nos principais indicadores", apresentada_como_aprimoramento="nao_declarado",
  celulas_do_infografico_afetadas="PNADC Bolsonaro (2019-2022): a quebra cai no meio do mandato", tipo_de_quebra="metodo_estatistico")
q("cesta", "o DIEESE também atualizou a metodologia da Pesquisa Nacional da Cesta Básica de Alimentos, a partir de janeiro de 2016",
  indicador="Poder de compra", serie="Cesta basica DIEESE, Sao Paulo (Ipeadata DIEESE12_CBSP12)", data_quebra="2016-01",
  metodo_antigo="coleta e ponderacao ate dez/2015 (nao descrita nos arquivos baixados)",
  metodo_novo="mudanca em: estrutura das cestas por regiao, locais de coleta, ponderacao por tipo de equipamento de comercio, cadastro e amostra dos locais, tipos/marcas/unidades por produto, questionarios e calendario; pesquisa passa a 27 capitais",
  razao_declarada_pela_fonte="ampliar a abrangencia para as 27 capitais e atualizar a metodologia", fonte_primaria_url="https://www.dieese.org.br/metodologia/metodologiaCestaBasica2016.pdf",
  direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="sem serie nos dois metodos; os produtos e quantidades mensais continuam os do Decreto-Lei 399/1938 (a fonte diz que 'continua em vigor')",
  efeito_medido="sem sobreposicao nos dados baixados", como_medido="nenhuma medicao possivel", apresentada_como_aprimoramento="sim",
  celulas_do_infografico_afetadas="cestas por salario minimo e horas por cesta, Dilma (2011-2016) e Temer (2016-2018)", tipo_de_quebra="metodo_estatistico")
q("icv", "Assim, há um hiato na série histórica do ICV",
  indicador="Poder de compra", serie="ICV-DIEESE, Sao Paulo (notas anuais do DIEESE)", data_quebra="2020-03 a 2023-07 (pesquisa suspensa; retomada com resultados de julho/2023)",
  metodo_antigo="ponderacao pela POF do DIEESE de 1994/1995 (base julho de 1996)", metodo_novo="ponderacao pela POF 2017/2018 do IBGE, com itens incluidos e excluidos",
  razao_declarada_pela_fonte="a decisao de parar o campo na pandemia e o trabalho de compatibilizacao com a POF significaram a suspensao por anos, o que torna impossivel voltar com o indice no tempo, para encadeamento da serie",
  fonte_primaria_url="https://www.dieese.org.br/analiseicv/icvNovo.html", direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="serie descontinuada, sem encadeamento",
  efeito_medido="nao encadeia", como_medido="a fonte afirma que nao e possivel", apresentada_como_aprimoramento="sim",
  celulas_do_infografico_afetadas="ICV-DIEESE so existe de 1997 a 2019 neste arquivo; Bolsonaro e Lula 3 ficam sem ICV", tipo_de_quebra="metodo_estatistico")
q("mte", "Nota: Os dados desta série para o período em que a legislação federal definia faixas diversificadas referem-se ao maior salário mínimo vigente no país.",
  indicador="Poder de compra", serie="Salario minimo nominal (Ipeadata MTE12_SALMIN12)", data_quebra="1984-05 (unificacao nacional do salario minimo)",
  metodo_antigo="valores diferenciados por estado e subregiao desde 1940; a serie registra o MAIOR vigente", metodo_novo="salario minimo nacionalmente unificado",
  razao_declarada_pela_fonte="n/d (a fonte registra a unificacao)", fonte_primaria_url="http://www.ipeadata.gov.br/api/odata4/Metadados('MTE12_SALMIN12')",
  direcao_do_efeito="eleva", como_a_direcao_foi_determinada="a serie pre-1984 usa o maior piso regional; o piso medio era menor, entao o valor real pre-1984 aqui e um teto, nao a media",
  efeito_medido="sem sobreposicao nos dados baixados", como_medido="nenhuma medicao possivel; Ipea tem outra pagina com a evolucao dos minimos regionais, nao baixada", apresentada_como_aprimoramento="nao_declarado",
  celulas_do_infografico_afetadas="salario minimo real e cestas por salario minimo, governos de 1964 a Figueiredo (1979-1984)", tipo_de_quebra="mudanca_de_regra")
q("sr", "O deflator sofre ajuste em função da mudança de unidade monetária de cruzeiros reais para reais. Para mitigar diferenças desta mudança, a variação do deflator em julho de 1994 foi multiplicada por 1,2225.",
  indicador="Poder de compra", serie="Salario minimo real (Ipeadata GAC12_SALMINRE12) e deflacionamento em geral", data_quebra="1994-07 (cruzeiro real -> real; divisor 2.750)",
  metodo_antigo="precos e salarios em cruzeiros reais (precos medidos como media do mes)", metodo_novo="reais; a conversao em 1 de julho de 1994 coincide com inflacao mensal de dois digitos",
  razao_declarada_pela_fonte="mitigar diferencas da mudanca de unidade monetaria", fonte_primaria_url="http://www.ipeadata.gov.br/api/odata4/Metadados('GAC12_SALMINRE12')",
  direcao_do_efeito="eleva", como_a_direcao_foi_determinada="no indice IGP-DI do Ipeadata a razao jul/jun/1994 e 1,2471 contra 1,0547 da taxa oficial do SGS 190: o nivel do indice fica 18,2% acima da cadeia das taxas mensais dali em diante; o Ipea diz ter multiplicado a variacao do deflator de jul/1994 por 1,2225",
  efeito_medido="IGP-DI de 1994 dez/dez: 1.093,9% no indice do Ipeadata contra 909,7% na cadeia das taxas mensais do SGS 190; SM real 1994 por INPC: 550,39 aqui contra 541,79 na serie do Ipea (+1,6%), e 1991-1993 e 1995-1996 coincidem ate o centavo",
  como_medido="series/_conferencias.txt (salto 1,1824) e comparacao com economia-real/saida-salmin-real-anual.csv; o indice do Ipeadata reproduz a taxa anual de 1994 citada em monetario/RESULTADO.md, por isso foi mantido como publicado",
  apresentada_como_aprimoramento="sim", celulas_do_infografico_afetadas="Itamar (1993-1994) e FHC (1995): ano de 1994 em SM real, cestas por SM e horas por cesta", tipo_de_quebra="mudanca_de_unidade")
q("fipe", "Em 1968 o cálculo foi transferido para IPE- USP - Instituto de Pesquisas Econômicas da Universidade de São Paulo",
  indicador="Poder de compra", serie="IPC-Fipe, Sao Paulo (Ipeadata FIPE12_IPCFIPE12)", data_quebra="1939 (inicio), 1968 (para o IPE-USP) e 1973 (Fipe)",
  metodo_antigo="'Indice Ponderado de Custo de Vida na Classe Operaria na Cidade de Sao Paulo' (Prefeitura, 1939)", metodo_novo="'Indice de Precos ao Consumidor (Custo de Vida) da Classe de Renda Familiar Modal no Municipio de Sao Paulo' (Fipe, 1973); hoje, familias com renda de 1 a 10 salarios minimos",
  razao_declarada_pela_fonte="n/d", fonte_primaria_url="http://www.ipeadata.gov.br/api/odata4/Metadados('FIPE12_IPCFIPE12')",
  direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="mudanca de populacao de referencia e de instituicao, sem sobreposicao nos dados baixados",
  efeito_medido="sem sobreposicao nos dados baixados", como_medido="nenhuma medicao possivel", apresentada_como_aprimoramento="nao_declarado",
  celulas_do_infografico_afetadas="SM real por IPC-Fipe antes de 1973", tipo_de_quebra="metodo_estatistico")
q("l14601", "cuja renda familiar per capita mensal seja igual ou inferior a R$ 218,00",
  indicador="Pobreza", serie="linha de elegibilidade do Bolsa Familia (Lei 14.601/2023, art. 5, II)", data_quebra="2023-06",
  metodo_antigo="duas linhas (pobreza e extrema pobreza) fixadas por decreto, a ultima R$ 210 e R$ 105 (Auxilio Brasil, Decreto 11.013/2022)", metodo_novo="linha unica de R$ 218 fixada em LEI; criterio de saida passa a ser renda per capita acima de meio salario minimo (art. 6, par. 1)",
  razao_declarada_pela_fonte="a Exposicao de Motivos da MP 1.164/2023 nao menciona a linha de R$ 218 (conferido: sem 'R$ 218' no texto)", fonte_primaria_url="https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/Mpv/mpv1164.htm",
  direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="a linha real em R$ de set/2026 (INPC) vai de 252,58 (2022-03) a 249,27 (2023-06), -1,3%, mas a linha de extrema pobreza deixa de existir",
  efeito_medido="-1,3% na linha de pobreza em termos reais; extrema pobreza sem linha propria", como_medido="series/bolsa_familia_linhas.csv", apresentada_como_aprimoramento="nao_declarado",
  celulas_do_infografico_afetadas="Lula 3: qualquer comparacao de 'extrema pobreza' pela regra do programa nao tem mais linha", tipo_de_quebra="mudanca_de_regra")
with open(RAIZ / "quebras.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, COLS)
    w.writeheader()
    w.writerows(L)
print(len(L), "quebras escritas; todos os trechos conferidos contra os arquivos")
