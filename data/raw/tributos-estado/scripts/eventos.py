# Gera eventos_tributarios.csv a partir de bruto/planalto/*.html (so le bruto, sem rede). python3 -I eventos.py
import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import txt  # noqa: E402

MESES = "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split()
# governos: rotulos e datas canonicos de ../porquinho/bruto/mandatos.csv (leitura; posse <= data < saida)
MANDATOS = [(r["posse"], r["saida"], r["nome"]) for r in csv.DictReader(open(RAIZ.parent / "porquinho/bruto/mandatos.csv", encoding="utf-8"))]
P = "https://www.planalto.gov.br/ccivil_03"
# (id, data_do_ato, instrumento, tributo, sentido, base_do_sentido, arquivo, url, regex_do_trecho, nota)
E = [
 ("ec12", "1996-08-15", "Emenda Constitucional 12/1996", "CPMF", "cria", "texto do ato (outorga competencia para instituir)", "/constituicao/emendas/emc/emc12.htm", r"Art\. 74 A união poderá instituir contribuição provisória sobre movimentação.{0,120}natureza financeira\.", "autoriza a instituicao; aliquota maxima 0,25% no § 1º"),
 ("l9311", "1996-10-24", "Lei 9.311/1996", "CPMF", "cria", "texto do ato", "/leis/l9311.htm", r"Art\. 1º É instituída a Contribuição Provisória sobre Movimentação.{0,140}CPMF\.", ""),
 ("ec21", "1999-03-18", "Emenda Constitucional 21/1999", "CPMF", "prorroga", "texto do ato (ementa e art. 75 do ADCT)", "/constituicao/emendas/emc/emc21.htm", r"É prorrogada, por trinta e seis meses, a cobrança da contribuição provisória.{0,160}", "a ementa diz 'prorroga, alterando a aliquota'; o valor da aliquota nao foi extraido desta linha"),
 ("ec37", "2002-06-12", "Emenda Constitucional 37/2002", "CPMF", "prorroga", "texto do ato", "/constituicao/emendas/emc/emc37.htm", r"será cobrada até 31 de dezembro de 2004\.", "mesma EC cria aliquota minima de 2% de ISS (art. 156 § 3º); nao tratada aqui"),
 ("ec42", "2003-12-19", "Emenda Constitucional 42/2003", "CPMF", "prorroga", "texto do ato", "/constituicao/emendas/emc/emc42.htm", r"Art\. 90\. O prazo previsto no caput do art\. 84 deste Ato.{0,100}31 de dezembro de 2007\.", ""),
 ("senado2007", "2007-12-13", "Votacao da PEC 89/2007 no Plenario do Senado (Agencia Senado)", "CPMF", "extingue", "noticia da Agencia Senado: rejeicao da prorrogacao; cobranca deixa de ser feita desde 1/1/2008", "SENADO", r"A PEC recebeu 45 votos favoráveis, 34 votos contrários.{0,230}", "extincao por vencimento do prazo do ADCT art. 84 (EC 42/2003) sem nova prorrogacao; fonte secundaria institucional (nao e texto de lei)"),
 ("l10336", "2001-12-19", "Lei 10.336/2001", "Cide-combustiveis", "cria", "texto do ato", "/leis/leis_2001/l10336.htm", r"Art\. 1o Fica instituída a Contribuição de Intervenção no Domínio Econômico incidente sobre a importação e a comercialização de petróleo.{0,100}\(Cide\)", ""),
 ("l9317", "1996-12-05", "Lei 9.317/1996", "Simples (federal)", "cria", "texto do ato (ementa)", "/leis/l9317.htm", r"institui o Sistema Integrado de Pagamento de Impostos e Contribuições das Microempresas e das Empresas de Pequeno Porte - SIMPLES", "revogada pela LC 123/2006 (Planalto)"),
 ("lc123", "2006-12-14", "Lei Complementar 123/2006", "Simples Nacional", "cria", "texto do ato", "/leis/lcp/lcp123.htm", r"Fica instituído o Regime Especial Unificado de Arrecadação de Tributos e Contribuições devidos pelas Microempresas e Empresas de Pequeno Porte - Simples Nacional\.", "texto consolidado: o artigo pode ter redacao posterior"),
 ("lc128", "2008-12-19", "Lei Complementar 128/2008", "MEI (Simples Nacional)", "cria", "texto do ato", "/leis/lcp/lcp128.htm", r"Art\. 18-A\. O Microempreendedor Individual - MEI poderá optar pelo recolhimento.{0,200}", ""),
 ("l12546", "2011-12-14", "Lei 12.546/2011", "contribuicao previdenciaria patronal (desoneracao da folha, CPRB)", "altera", "texto do ato (ementa): troca a incidencia; o efeito sobre a carga depende do setor e nao foi medido", "/_ato2011-2014/2011/lei/l12546.htm", r"altera a incidência das contribuições previdenciárias devidas pelas empresas que menciona", "texto consolidado; origem na MP 540/2011"),
 ("l12715", "2012-09-17", "Lei 12.715/2012", "CPRB (desoneracao da folha)", "altera", "texto do ato: fixa alíquota de 2% sobre receita bruta em substituicao as contribuicoes do art. 22 incisos I e III da Lei 8.212", "/_ato2011-2014/2012/lei/l12715.htm", r"Art\. 7º Até 31 de dezembro de 2014, contribuirão sobre o valor da receita bruta.{0,300}à alíquota de 2% \(dois por cento\)", "amplia a lista de setores; ver nota da linha da Lei 13.161/2015"),
 ("l13161", "2015-08-31", "Lei 13.161/2015", "CPRB (desoneracao da folha)", "aumenta", "comparacao de atos: 2% no art. 7º da Lei 12.715/2012 contra 4,5% no art. 7º-A desta lei (com excecoes listadas no texto)", "/_ato2015-2018/2015/lei/l13161.htm", r"Art\. 7º -A\. A alíquota da contribuição sobre a receita bruta prevista no art\. 7º será de 4,5%.{0,160}", "a comparacao e entre as aliquotas dos dois artigos; setores com excecao tem outro valor"),
 ("l13670", "2018-05-30", "Lei 13.670/2018", "CPRB (reoneracao parcial)", "aumenta", "texto do ato: revoga o inciso II do art. 7º e dispositivos do art. 8º da Lei 12.546", "/_ato2015-2018/2018/lei/L13670.htm", r"Art\. 12\. Ficam revogados:.{0,300}", "reoneracao parcial: o trecho mostra as revogacoes; ver ementa ('altera ... quanto a contribuicao previdenciaria sobre a receita bruta')"),
 ("l14784", "2023-12-27", "Lei 14.784/2023", "CPRB (desoneracao da folha)", "prorroga", "texto do ato (ementa)", "/_ato2023-2026/2023/lei/L14784.htm", r"Prorroga até 31 de dezembro de 2027 os prazos de que tratam os arts\. 7º e 8º da Lei nº 12\.546", "promulgada apos derrubada de veto total; ha ADI 7633 anotada no texto"),
 ("l14973", "2024-09-16", "Lei 14.973/2024", "CPRB (reoneracao gradual)", "aumenta", "texto do ato: 'substituicao parcial' das contribuicoes, 2025 a 2027, com percentual crescente do art. 22 da Lei 8.212", "/_ato2023-2026/2024/lei/L14973.htm", r"Art\. 9º-A\. Nos exercícios de 2025 a 2027.{0,300}", "regime de transicao; sentido deduzido do texto (parcela da aliquota da Lei 8.212 volta gradualmente)"),
 ("lc192", "2022-03-11", "Lei Complementar 192/2022", "ICMS-combustiveis", "altera", "texto do ato: define combustiveis com incidencia unica (monofasica)", "/leis/lcp/lcp192.htm", r"Art\. 1º Esta Lei Complementar define, nos termos da alínea h do inciso XII do § 2º do art\. 155.{0,200}", "sentido sobre a carga nao extraido do texto"),
 ("lc194", "2022-06-23", "Lei Complementar 194/2022", "ICMS (combustiveis, energia, comunicacoes, transporte coletivo)", "reduz", "texto do ato: veda aliquota superior a das operacoes em geral para esses bens (art. 18-A do CTN, parágrafo único I)", "/leis/lcp/lcp194.htm", r"Art\. 18-A\. Para fins da incidência do imposto de que trata o inciso II do caput do art\. 155.{0,420}", "efeito na arrecadacao dos estados nao medido aqui"),
 ("ec132", "2023-12-20", "Emenda Constitucional 132/2023", "IBS/CBS (reforma do consumo)", "cria", "texto do ato (art. 156-A)", "/constituicao/emendas/emc/emc132.htm", r"Art\. 156-A\. Lei complementar instituirá imposto sobre bens e serviços de competência compartilhada entre Estados, Distrito Federal e Municípios\.", "autoriza por lei complementar"),
 ("lc214", "2025-01-16", "Lei Complementar 214/2025", "IBS e CBS", "cria", "texto do ato", "/leis/lcp/lcp214.htm", r"Art\. 1º Ficam instituídos: I - o Imposto sobre Bens e Serviços \(IBS\).{0,260}", ""),
 ("l9249", "1995-12-26", "Lei 9.249/1995", "IRPJ", "altera", "texto do ato fixa 15% + adicional de 10%; aliquota anterior nao lida", "/leis/l9249.htm", r"Art\. 3º A alíquota do imposto de renda das pessoas jurídicas é de quinze por cento\..{0,200}", "o texto consolidado traz duas redacoes do § 1º; trecho do caput"),
 ("l9249div", "1995-12-26", "Lei 9.249/1995 (art. 10)", "IRPF/IRPJ sobre dividendos", "reduz", "texto do ato: lucros e dividendos nao ficam sujeitos ao imposto na fonte nem integram a base do beneficiario", "/leis/l9249.htm", r"Art\. 10\. Os lucros ou dividendos calculados com base nos resultados apurados a partir do mês de janeiro de 1996.{0,330}", "regra alterada pela Lei 15.270/2025 (tributacao de dividendos a altas rendas); ver linha desta"),
 ("l9250", "1995-12-26", "Lei 9.250/1995", "IRPF (tabela progressiva)", "altera", "texto do ato; tabela anterior nao lida", "/leis/l9250.htm", r"Art\. 3º O imposto de renda incidente sobre os rendimentos de que tratam os arts\. 7°, 8° e 12.{0,200}", ""),
 ("l11482", "2007-05-31", "Lei 11.482/2007", "IRPF (tabela)", "altera", "texto do ato (ementa)", "/_ato2007-2010/2007/lei/l11482.htm", r"Efetua alterações na tabela do imposto de renda da pessoa física", "tambem reduz a zero a aliquota da CPMF em hipoteses que menciona (ementa)"),
 ("l12469", "2011-08-26", "Lei 12.469/2011", "IRPF (tabela)", "altera", "texto do ato (ementa)", "/_ato2011-2014/2011/lei/l12469.htm", r"Altera os valores constantes da tabela do Imposto sobre a Renda da Pessoa Física", ""),
 ("l13149", "2015-07-21", "Lei 13.149/2015", "IRPF (tabela)", "altera", "texto do ato (ementa)", "/_ato2015-2018/2015/lei/l13149.htm", r"para dispor sobre os valores da tabela mensal do Imposto sobre a Renda da Pessoa Física", ""),
 ("l14663", "2023-08-28", "Lei 14.663/2023", "IRPF (tabela)", "altera", "texto do ato (ementa)", "/_ato2023-2026/2023/lei/L14663.htm", r"altera os valores da tabela mensal do Imposto sobre a Renda da Pessoa Física.{0,120}", "conversao da MPv 1.172/2023"),
 ("l15270a", "2025-11-26", "Lei 15.270/2025", "IRPF (reducao do imposto devido na base mensal e anual)", "reduz", "texto do ato (art. 1º)", "/_ato2023-2026/2025/lei/L15270.htm", r"Art\. 1º Esta Lei altera a Lei nº 9\.250.{0,300}", ""),
 ("l15270b", "2025-11-26", "Lei 15.270/2025", "IRPF (tributacao minima de altas rendas)", "cria", "texto do ato (art. 1º)", "/_ato2023-2026/2025/lei/L15270.htm", r"a tributação mínima para as pessoas físicas que auferem altas rendas", ""),
 ("d6696", "2008-12-17", "Decreto 6.696/2008", "IPI (caminhoes e chassis)", "reduz", "texto do ato: Anexo fixa aliquota 0 para os codigos listados", "/_ato2007-2010/2008/decreto/D6696.htm", r"Art\. 1º Fica alterada para os percentuais indicados no Anexo as alíquotas do Imposto sobre Produtos Industrializados.{0,240}", "revogado pelo Decreto 7.660/2011 (Planalto)"),
 ("d7567", "2011-09-15", "Decreto 7.567/2011", "IPI (industria automotiva)", "altera", "texto do ato (ementa); ha reducao para quem cumpre requisitos e a tabela e alterada; direcao liquida nao extraida", "/_ato2011-2014/2011/decreto/D7567.htm", r"Regulamenta os arts\. 5º e 6º da Medida Provisória nº 540.{0,230}", "revogado pelo Decreto 7.819/2012 (Planalto)"),
 ("d10979", "2022-02-25", "Decreto 10.979/2022", "IPI (reducao geral)", "reduz", "texto do ato: 'ficam reduzidas'", "/_ato2019-2022/2022/decreto/D10979.htm", r"Art\. 1º As alíquotas do Imposto sobre Produtos Industrializados - IPI incidentes sobre os produtos classificados.{0,420}", "revogado pelo Decreto 11.055/2022; ADI 7153 anotada"),
 ("d6339", "2008-01-03", "Decreto 6.339/2008", "IOF", "altera", "texto do ato (ementa); valor anterior nao lido", "/_ato2007-2010/2008/decreto/D6339.htm", r"Altera as alíquotas do Imposto sobre Operações de Crédito, Câmbio e Seguro, ou relativas a Títulos ou Valores Mobiliários - IOF\.", "primeiro ato do ano da extincao da CPMF (texto mostra 0,0082% ao dia para mutuario pessoa fisica)"),
 ("d6983", "2009-10-19", "Decreto 6.983/2009", "IOF-cambio (entrada de capital estrangeiro em renda fixa/variavel)", "cria", "texto do ato: 2% sobre ingresso por investidor estrangeiro (aliquota anterior nao lida)", "/_ato2007-2010/2009/decreto/D6983.htm", r"nas liquidações de operações de câmbio para ingresso de recursos no País, realizadas por investidor estrangeiro, para aplicação no mercado financeiro e de capitais: dois por cento", "'cria' no sentido de incidencia nova de 2%: a incidencia anterior sobre esse fluxo nao foi lida; tratar como 'altera' se contestado"),
 ("d7323", "2010-10-04", "Decreto 7.323/2010", "IOF-cambio (renda fixa)", "aumenta", "comparacao de atos: 2% (Decreto 6.983/2009) -> 4% (este)", "/_ato2007-2010/2010/decreto/D7323.htm", r"contratadas a partir de 5 de outubro de 2010 por investidor estrangeiro, para ingresso de recursos no País.{0,200}quatro por cento", "revogado pelo Decreto 7.412/2010"),
 ("d7330", "2010-10-18", "Decreto 7.330/2010", "IOF-cambio (renda fixa)", "aumenta", "comparacao de atos: 4% (Decreto 7.323/2010) -> 6% (este)", "/_ato2007-2010/2010/decreto/D7330.htm", r"contratadas a partir de 19 de outubro de 2010 por investidor estrangeiro, para ingresso de recursos no País.{0,230}seis por cento", "revogado pelo Decreto 7.412/2010"),
 ("d7412", "2010-12-30", "Decreto 7.412/2010", "IOF", "reduz", "texto do ato: 'a aliquota do IOF fica reduzida para 0,38%', com excecoes", "/_ato2007-2010/2010/decreto/D7412.htm", r"Art\. 15-A\. A alíquota do IOF fica reduzida para trinta e oito centésimos por cento, observadas as seguintes exceções.{0,200}", "revoga os decretos de 2009/2010; as excecoes mantem 6% etc.; arts revogados pelo Decreto 8.325/2014"),
 ("d10997", "2022-03-15", "Decreto 10.997/2022", "IOF-credito", "reduz", "texto do ato: 'a aliquota do IOF fica reduzida ... a zero'", "/_ato2019-2022/2022/decreto/D10997.htm", r"Art\. 15-C\. A alíquota do IOF fica reduzida: I - a zero.{0,160}", "o cronograma de reducao gradual (itens II a IV) consta como revogado pelo Decreto 11.153/2022 no Planalto"),
 ("d12466", "2025-05-22", "Decreto 12.466/2025", "IOF (cambio, credito, seguros)", "altera", "texto do ato lista aliquotas (3,5% em varias operacoes de cambio); a aliquota anterior nao foi lida", "/_ato2023-2026/2025/decreto/D12466.htm", r"nas liquidações de operações de câmbio, para aquisição de moeda estrangeira, em espécie: 3,5% \(três inteiros e cinco décimos por cento\)", "revogado pelo Decreto 12.499/2025; sustado pelo Decreto Legislativo 176/2025 (Planalto, 'Vide'); sentido de aumento NAO verificado no texto lido"),
 ("d12467", "2025-05-23", "Decreto 12.467/2025", "IOF", "altera", "texto do ato altera o Decreto 6.306 e o Decreto 12.466", "/_ato2023-2026/2025/decreto/D12467.htm", r"Altera o Decreto nº 6\.306, de 14 de dezembro de 2007, que regulamenta.{0,200}e o Decreto nº 12\.466, de 22 de maio de 2025\.", "Planalto: revogado pelo Decreto 12.499 e sustado pelo DL 176/2025"),
 ("d12499", "2025-06-11", "Decreto 12.499/2025", "IOF", "altera", "texto do ato (ementa)", "/_ato2023-2026/2025/decreto/D12499.htm", r"Altera o Decreto nº 6\.306, de 14 de dezembro de 2007, que regulamenta.{0,160}", "Planalto: 'Vide Decreto Legislativo nº 176, de 2025'"),
]


def gov(d):
    return next((g for a, b, g in MANDATOS if a <= d < b), "?")


def main():
    linhas, falhas = [], []
    bruto = RAIZ / "bruto"
    man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
    for e in E:
        i, d, inst, trib, sent, base, arq, rx, nota = e
        if arq == "SENADO":
            f = "bruto/senado-cpmf-rejeicao-2007-12-13.html"
            url = "https://www12.senado.leg.br/noticias/materias/2007/12/13/senado-rejeita-prorrogacao-da-cpmf"
        if arq != "SENADO":
            chave = {"l9249div": "l9249", "l15270a": "l15270", "l15270b": "l15270"}.get(i, i)
            f = "bruto/planalto/%s.html" % chave
            url = P + arq
        t = re.sub(r"\s+", " ", txt.ler(RAIZ / f))
        m = re.search(rx, t)
        if not m:
            falhas.append((i, "trecho nao achado"))
            continue
        trecho = m.group(0).strip()
        ano, mes, dia = d.split("-")
        pat = r"%d\s*(?:º|o|°)?\s+de\s+%s\s+de\s+%s" % (int(dia), MESES[int(mes) - 1], ano)
        if arq != "SENADO" and not re.search(pat, t[:1500], re.I) and not re.search(pat.replace("de ", "DE "), t[:1500]):
            # data do ato tem de aparecer no cabecalho do arquivo
            falhas.append((i, "data %s nao aparece no cabecalho" % d))
        m_ = man.get(f)
        linhas.append({"data": d, "instrumento": inst, "tributo": trib, "sentido": sent, "base_do_sentido": base,
                       "governo": gov(d), "url": url, "trecho_literal": trecho, "arquivo_bruto": f,
                       "sha256_do_bruto": m_["sha256"] if m_ else "", "nota": nota,
                       "vintage": "texto do Planalto/Agencia Senado lido em %s (consolidado pode ter redacao posterior)" % (m_["timestamp_utc"][:10] if m_ else "?")})
    linhas.sort(key=lambda r: (r["data"], r["instrumento"]))
    cols = list(linhas[0].keys())
    with open(RAIZ / "eventos_tributarios.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(linhas)
    print(len(linhas), "eventos;", "falhas:", falhas)


main()
