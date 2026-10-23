#!/usr/bin/env python3
"""Escreve ../definicoes.md. Todo trecho citado e conferido (sem espacos) contra o texto do arquivo hasheado em ../bruto.
python3 -I escrever_md_definicoes.py   (sem rede; usa pdftotext)"""
import json
import re
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent


def pdf(p):
    return subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True, check=True).stdout


F = {
    "oit": pdf(RAIZ / "bruto/oit-19a-ciet-2013-resolucao-i-original-wayback-2019.pdf"),
    "ibge": pdf(RAIZ / "bruto/ibge-pnadc-notas-tecnicas-v1.19.pdf"),
    "retro": pdf(RAIZ / "bruto/ibge-pnadc-retrospectiva-2012-2020.pdf"),
}
ns = lambda x: re.sub(r"\s+", "", x)


def Q(k, t):
    assert ns(t) in ns(F[k]), (k, t[:80])
    return re.sub(r"\s+", " ", t).strip()


sid = json.load(open(RAIZ / "bruto/sidra-4093-pnadc-trimestral-raw.json"))
ult = {int(v["id"]): v["resultados"][0]["series"][0]["serie"]["202602"] for v in sid}
PIA, FORA, FT, OCUP = (int(float(ult[c])) for c in (1641, 4094, 4088, 4090))

URL_OIT = "https://www.ilo.org/global/statistics-and-databases/standards-and-guidelines/resolutions-adopted-by-international-conferences-of-labour-statisticians/WCMS_230304/lang--en/index.htm"
URL_IBGE = "https://biblioteca.ibge.gov.br/visualizacao/livros/liv102172_notas_tecnicas.pdf"
URL_RETRO = "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Principais_destaques_PNAD_continua/2012_2020/PNAD_continua_retrospectiva_2012_2020.pdf"
URL_OITPDF = "https://www.ilo.org/wcmsp5/groups/public/---dgreports/---stat/documents/normativeinstrument/wcms_230304.pdf"
o = []
w = o.append
w("# Definicoes oficiais: ocupado, desocupado, forca de trabalho, desalento\n")
w("Gerado por `scripts/escrever_md_definicoes.py`; cada trecho entre aspas foi conferido por programa (sem considerar espacos e quebras de linha) contra o arquivo hasheado em `bruto/`. Termos tecnicos vem com glosa.\n")
w("> [!IMPORTANT]\n> **Receber beneficio (Bolsa Familia, BPC, seguro-desemprego, aposentadoria) muda a classificacao? Nao.** Nem o IBGE nem a OIT usam a condicao de receber beneficio como criterio: a classificacao depende so de trabalhar na semana de referencia, procurar trabalho e estar disponivel. A OIT diz o mais perto disso, e o que diz e que quem recebe transferencia nao relacionada a emprego **nao conta como ocupado** (par. 31(d)); isso nao o torna desocupado nem o tira da forca de trabalho: se ele procurar trabalho e estiver disponivel, e desocupado; se nao, esta fora da forca de trabalho. **Limite da prova**: nenhum dos dois documentos tem a frase \"receber Bolsa Familia nao altera a classificacao\"; a resposta e a leitura dos criterios (e do par. 31) e esta marcada como inferencia onde nao e citacao.\n")

w("## 1. Fontes\n")
w(f"* **OIT, 19a Conferencia Internacional de Estatisticos do Trabalho (CIET), 2013, Resolucao I** (\"Resolution concerning statistics of work, employment and labour underutilization\"). Texto original, captura do Internet Archive de 12/04/2019: `bruto/oit-19a-ciet-2013-resolucao-i-original-wayback-2019.pdf`. Pagina oficial: {URL_OIT}. O PDF vivo hoje no endereco {URL_OITPDF} e a versao **emendada em 2023** (21a CIET, Resolucao II), baixada em `bruto/oit-19a-ciet-2013-resolucao-i.pdf`; os paragrafos citados aqui tem o mesmo numero e o mesmo texto nas duas versoes (par. 15, 16, 27, 31, 47, 51, 52).")
w(f"* **IBGE, PNAD Continua, Notas tecnicas, versao 1.19**: {URL_IBGE} (`bruto/ibge-pnadc-notas-tecnicas-v1.19.pdf`). A propria nota diz que os conceitos de ocupada (desde 2015T4) e desocupada (desde 2016T2) estao ajustados a Resolucao I da 19a CIET.")
w(f"* **IBGE, PNAD Continua, principais destaques 2012-2020**, notas de rodape 2 e 3: {URL_RETRO} (`bruto/ibge-pnadc-retrospectiva-2012-2020.pdf`).\n")

w("## 2. Definicoes\n")
w("### Pessoa em idade de trabalhar (IBGE)\n")
w("> " + Q("ibge", "Definem-se como pessoas em idade de trabalhar as pessoas de 14 anos ou mais de idade na data de referência.") + "\n")
w("### Ocupado (pessoa ocupada = tem trabalho)\n")
w("IBGE:\n")
w("> " + Q("ibge", "São classificadas como ocupadas na semana de referência as pessoas que, nesse período, trabalharam pelo menos uma hora completa em trabalho remunerado em dinheiro, produtos, mercadorias ou benefícios (moradia, alimentação, roupas, treinamento etc.), ou em trabalho sem remuneração direta em ajuda à atividade econômica de membro do domicílio ou parente que reside em outro domicílio, ou, ainda, as que tinham trabalho remunerado do qual estavam temporariamente afastadas nessa semana.") + "\n")
w("Glosa: \"benefícios (moradia, alimentação...)\" nesse texto sao **pagamento em especie pelo trabalho**, nao beneficio social.\n")
w("OIT (par. 27):\n")
w("> " + Q("oit", "Persons in employment are defined as all those of working age who, during a short reference period, were engaged in any activity to produce goods or provide services for pay or profit.") + "\n")
w("### Desocupado (desempregado: sem trabalho, procurando e disponivel)\n")
w("IBGE:\n")
w("> " + Q("ibge", "São classificadas como desocupadas na semana de referência as pessoas sem trabalho em ocupação nessa semana que tomaram alguma providência efetiva para consegui-lo no período de referência de 30 dias, e que estavam disponíveis para assumi-lo na semana de referência.") + "\n")
w("> " + Q("ibge", "Define-se como procura de trabalho em ocupação a tomada de alguma providência efetiva para consegui-lo, ou seja, o contato estabelecido com empregadores; a prestação de concurso; a inscrição em concurso; a consulta a agência de emprego, sindicato ou órgão similar; a resposta a anúncio de emprego") + " [...]\n")
w("OIT (par. 47):\n")
w("> " + Q("oit", "Persons in unemployment are defined as all those of working age who were not in employment, carried out activities to seek employment during a specified recent period and were currently available to take up employment given a job opportunity") + "\n")
w("### Forca de trabalho e fora da forca de trabalho\n")
w("IBGE:\n")
w("> " + Q("ibge", "São classificadas como na força de trabalho na semana de referência as pessoas ocupadas e as pessoas desocupadas nessa semana.") + "\n")
w("> " + Q("ibge", "São classificadas como fora da força de trabalho na semana de referência as pessoas que não estavam ocupadas nem desocupadas nessa semana.") + "\n")
w("OIT (par. 16):\n")
w("> " + Q("oit", "Priority is given to employment over the other two categories, and to unemployment over outside the labour force. The three categories of labour force status are, thus, mutually exclusive and exhaustive. The sum of persons in employment and in unemployment equals the labour force. Persons outside the labour force are those of working age who were neither in employment nor in unemployment in the short reference period.") + "\n")
w("### Forca de trabalho potencial e desalento (desalentado = quer trabalhar e esta disponivel, mas nao procura porque acha que nao vai achar)\n")
w("IBGE (nota 3 de rodape dos principais destaques):\n")
w("> " + Q("retro", "Composta pelo subgrupo de pessoas da força de trabalho potencial que não haviam realizado busca efetiva por trabalho por considerar que: não conseguiriam trabalho adequado; não tinham experiência profissional ou qualificação; não conseguiam trabalho por serem considerados muito jovens ou muito idosos ou não havia trabalho na localidade. Todavia, gostariam de ter um trabalho e estavam disponíveis para trabalhar na semana de referência.") + "\n")
w("OIT (par. 51 e 52):\n")
w("> " + Q("oit", "Potential labour force is defined as all persons of working age who, during the short reference period, were neither in employment nor in unemployment and:") + " (a) [...] unavailable jobseekers; or (b) " + Q("oit", "did not carry out activities to “seek employment”, but wanted employment and were “currently available” (i.e. available potential jobseekers).") + "\n")
w("> " + Q("oit", "Among those in paragraph 51(b) it may be useful to identify separately discouraged jobseekers, comprising those who did not “seek employment” for labour market-related reasons as listed in paragraph 80(b).") + "\n")
w("Glosa: o desalentado conta como **fora da forca de trabalho** (nao entra na taxa de desocupacao) e como parte da **subutilizacao** (taxa composta de subutilizacao = desocupados + subocupados por insuficiencia de horas + forca de trabalho potencial, sobre forca de trabalho ampliada).\n")

w("## 3. Receber beneficio muda a classificacao? Os trechos\n")
w("1. **A OIT exclui a transferencia da ocupacao, nao da forca de trabalho** (par. 31):\n")
w("> " + Q("oit", "Excluded from employment are:") + " [...] (c) " + Q("oit", "persons who are required to perform work as a condition of continued receipt of a government social benefit such as unemployment insurance;") + " (d) " + Q("oit", "persons receiving transfers, in cash or in kind, not related to employment;") + "\n")
w("   Leitura (inferencia minha a partir do par. 16 e 47): quem recebe transferencia sem trabalhar nao e ocupado; sera desocupado se procurar e estiver disponivel, ou estara fora da forca de trabalho. O recebimento em si nao entra em nenhum teste.")
w("2. **A OIT lista \"outras fontes de renda (aposentadorias, alugueis)\" apenas como razao para nao procurar trabalho, em analise de quem esta fora da forca de trabalho** (par. 80(b)):\n")
w("> " + Q("oit", "main reason for not “seeking employment”, not being “currently available” or not wanting employment:") + " [...] " + Q("oit", "other sources of income (pensions, rents); social exclusion;") + "\n")
w("   Isto e analise adicional opcional (\"may be used\"), nao criterio de classificacao.")
w("3. **No IBGE, beneficio e rendimento, nao condicao de trabalho.** Os criterios de condicao em relacao a forca de trabalho (secao 2) citam so trabalho na semana, providencia de procura em 30 dias e disponibilidade; busca por \"Bolsa Fam\", \"Prestacao Continuada\" e \"seguro-desemprego\" no texto das notas tecnicas v1.19 so acha ocorrencias na secao de rendimentos, fora das definicoes de ocupado, desocupado e forca de trabalho. Nessa secao o IBGE trata esses pagamentos como renda que **nao** vem de trabalho:\n")
w("> " + Q("ibge", "O rendimento de outras fontes compreende os rendimentos, recebidos em dinheiro, que não são oriundos de trabalho da semana de referência") + " [...]: " + Q("ibge", "Programa social - Rendimento do Benefício de Prestação Continuada - BPC, da Lei Orgânica da Assistência Social - LOAS (Lei n. 8.742, de 07.12.1993), Bolsa Família e de outros programas sociais do governo federal, estadual ou municipal;") + " " + Q("ibge", "Aposentadoria ou pensão de instituto de previdência ou do governo federal") + " [...]; " + Q("ibge", "Seguro-desemprego - Rendimento recebido do seguro-desemprego ou do seguro defeso;") + "\n")
w("   Leitura (inferencia minha): como esses valores entram como renda **de outras fontes** e a pessoa e classificada pelo trabalho/procura, receber Bolsa Familia, BPC, seguro-desemprego ou aposentadoria nao muda ocupado/desocupado/fora da forca de trabalho. A consulta a \"agência de emprego, sindicato ou órgão similar\" e uma forma de procura (secao 2); o texto nao trata de quem se cadastra so para receber beneficio sem procurar (lacuna, nao inferi nada).")
w("4. **Aposentadoria**: pessoa de 14 anos ou mais aposentada que nao trabalha nem procura esta fora da forca de trabalho; se trabalha, e ocupada (par. 27 e definicao do IBGE acima). Nao ha regra de idade maxima na PNAD Continua (o IBGE define a idade de trabalhar so pelo piso de 14 anos).\n")

w("## 4. Quanto da populacao em idade ativa recebe beneficio e esta fora da forca de trabalho?\n")
mil = lambda v: f"{v:,.0f}".replace(",", ".")
w(f"**Nao achei tabela oficial desse cruzamento.** O SIDRA tem (a) a condicao em relacao a forca de trabalho (tabela 4093) e (b) tabelas por domicilio de recebimento de programas sociais (7456 a 7458, 7447 a 7455), mas nenhuma cruza as duas coisas por pessoa. O que consta nos arquivos baixados e o denominador: em 2026T2 (SIDRA 4093, Brasil), {mil(PIA)} mil pessoas de 14 anos ou mais, das quais {mil(FT)} mil na forca de trabalho ({mil(OCUP)} mil ocupadas) e **{mil(FORA)} mil fora da forca de trabalho**; quantas delas recebem beneficio nao e informado ali.")
w("Fica como pendencia para quem tiver microdados da PNAD Continua (suplemento \"Rendimento de todas as fontes\"): o cruzamento exigiria os microdados, nao as tabelas publicadas.\n")
(RAIZ / "definicoes.md").write_text("\n".join(o) + "\n", encoding="utf-8")
print("ok")
