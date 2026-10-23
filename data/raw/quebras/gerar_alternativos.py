# indicadores-alternativos.csv: para cada indicador do bloco, que indicador NAO depende da regra/definicao que mudou, com a fonte.
# Rode: python3 -I gerar_alternativos.py   (depois de calc.py; verifica a unica citacao que usa)
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import citacoes  # noqa: E402

H = pathlib.Path(__file__).resolve().parent
citacoes.verifica("ipea_bmt23", "e não passou por mudanças metodológicas no período de alterações da PME")
R = []


def a(ind, regra, alt, dep, porque, fonte, url, cob, baixado, onde, ress):
    R.append({"indicador_do_bloco": ind, "regra_ou_definicao_que_mudou": regra, "indicador_alternativo": alt, "depende_da_regra_que_mudou": dep,
              "por_que": porque, "fonte_e_codigo": fonte, "url_ou_api": url, "cobertura": cob, "baixado_nesta_pasta": baixado,
              "resultado_por_governo_em": onde, "ressalva": ress, "vintage": "baixado em 2026-10-19" if baixado == "sim" else "nao baixado"})


IPEA = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{}')"
a("PIB", "ano-base e Sistema de Contas Nacionais (FGV ate 1989; ref. 1985; 2000; 2010)", "consumo de energia eletrica (quantidade fisica)", "nao",
  "e quantidade medida em kWh/GWh, sem ano-base nem deflator do SCN", "Ipeadata ELETRO_CEET (Eletrobras)", IPEA.format("ELETRO_CEET"), "1952-2025", "sim",
  "alternativos-por-governo.csv (A-ELETRO)", "nao mede valor adicionado; a relacao energia/PIB muda com a estrutura produtiva")
a("PIB", "idem", "consumo final de energia eletrica do Balanco Energetico Nacional", "nao", "idem, outra instituicao (MME)", "Ipeadata CONSUMOTOT (MME)", IPEA.format("CONSUMOTOT"), "1961-2022", "sim",
  "alternativos-por-governo.csv (A-MME)", "serie com niveis Brasil/Estados/Regioes: so o Brasil foi usado")
a("PIB", "idem", "IBC-Br (BCB)", "parcialmente", "nao usa o ano-base do SCN, mas tem metodo proprio do BCB e e proxy, nao PIB", "Ipeadata SGS12_IBCBR12 (BCB)", IPEA.format("SGS12_IBCBR12"), "2003-2026", "sim",
  "alternativos-por-governo.csv (A-IBCBR)", "so a partir de 2003; nao cobre 'Ditadura', Itamar nem FHC")
a("IPCA", "pesos POF (1989, 1999, 2006, 2012, 2020), formula do subitem (1994), cobertura de areas (1991, 2014, 2018), serie encerrada em fev/1986", "IPC-Fipe (Sao Paulo)", "nao (as regras do IBGE)",
  "outra instituicao (Fipe/USP), outra cesta e outros pesos; nao e livre de regras proprias, que nao foram lidas ❓", "Ipeadata FIPE_FIPE0001", IPEA.format("FIPE_FIPE0001"), "1940-2025", "sim",
  "alternativos-por-governo.csv (A-FIPE)", "so Sao Paulo")
a("IPCA", "idem", "IGP-DI (FGV)", "nao (as regras do IBGE)", "outra instituicao; mistura precos ao produtor, construcao e consumidor", "Ipeadata IGP12_IGPDI12 (ja em economia-real/ e inflacao/)", "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='IGP12_IGPDI12')", "1944-2026", "sim (em outra pasta)",
  "ver inflacao/ e economia-real/", "IGP-DI nao e indice ao consumidor; so serve de teste de ordem de grandeza")
a("IPCA", "idem", "custo da cesta basica (DIEESE, Sao Paulo)", "nao", "preco de uma cesta fisica fixa", "Ipeadata DIEESE12_CBSP12", IPEA.format("DIEESE12_CBSP12"), "1959-2026", "sim",
  "usado no salario minimo em cestas (A-CESTA)", "a composicao da cesta tem regra propria que nao foi lida ❓")
a("Desemprego", "PME 2002 (15+ -> 10+, definicao de desocupado), PNAD -> PNADC (10+ -> 14+, procura na semana -> 30 dias), telefone 2020-21, reponderacao 2021",
  "Pesquisa de Emprego e Desemprego (PED, Seade/Dieese)", "nao (a PED nao mudou em 2002, segundo o Ipea)", "uma pesquisa que, segundo Reis (Ipea, 2004), nao passou por mudancas na epoca da revisao da PME",
  "Seade/Dieese, via Ipea bmt 23 (nota tecnica)", "https://repositorio.ipea.gov.br/bitstream/11058/5346/1/bmt_n.23_mudan%c3%a7as.pdf", "1997-2003 na nota; serie completa NAO baixada", "nao",
  "nao ha", "so regioes metropolitanas; os dados da PED nao foram obtidos ❓")
a("Desemprego", "idem", "emprego formal por registro administrativo (RAIS/CAGED do Ministerio do Trabalho)", "nao (nao e pesquisa domiciliar)", "conta vinculos registrados, sem definicao de 'desocupado'",
  "MTE RAIS/CAGED (nao baixado; URL e codigo nao verificados ❓)", "n/d", "n/d", "nao", "nao ha", "nao mede desemprego nem informalidade; so emprego formal")
a("Salario minimo real", "deflator (IPC-SP, IPC-RJ, IGPC-Mtb, INPC; fator 1,2225 em jul/1994), faixas regionais ate 1984", "salario minimo em cestas basicas DIEESE", "nao", "nao usa indice geral de precos; razao entre dois precos nominais na mesma moeda da epoca",
  "Ipeadata MTE12_SALMIN12 / DIEESE12_CBSP12 (derivado aqui, com os divisores de moeda do BCB)", IPEA.format("DIEESE12_CBSP12"), "1959-2025", "sim", "alternativos-por-governo.csv (A-CESTA)", "so Sao Paulo; o minimo ate 1984 e o maior regional")
a("Salario minimo real", "idem", "salario minimo nominal / UM indice unico (IGP-DI, INPC ou IPCA) em todos os anos", "nao (nao ha troca de deflator)", "tira a troca de deflator, nao o indice escolhido",
  "derivado em calc.py", "n/d", "IGP-DI 1944-2025; INPC 1979-2025; IPCA 1980-2025", "sim (series de entrada)", "comparativo-metodo-constante.csv (S3, S4, S5)", "o indice unico escolhido tambem muda o resultado: ver quebras.csv")
a("Pobreza", "linha (US$ 1,00/1,08/1,25/1,90/2,15/3,00; 3,20/3,65/4,20; 5,50/6,85/8,30), PPC (1985/1993/2005/2011/2017/2021), linhas nacionais",
  "renda domiciliar per capita real por decil e mediana", "nao (nao tem linha)", "mede a renda, nao quantos estao abaixo de um corte", "Banco Mundial PIP (decile1..10, mean, median)",
  "https://api.worldbank.org/pip/v1/pip?country=BRA&year=all&povline=6.85&ppp_version=2017&fill_gaps=false&format=json", "1981-2024 (anos de pesquisa)", "sim",
  "renda-por-decil.csv e renda-por-decil-por-governo.csv", "depende do PPC (2017 ou 2021) so para converter dolares; em reais a ordem entre governos nao muda")
a("Pobreza", "idem", "renda domiciliar per capita mediana, media e dos 40% mais pobres (SIS/IBGE)", "nao", "sem linha", "Ipeadata SIS_RDPCMEDIANO, SIS_RDPCMEDIO, SIS_RDPC40", IPEA.format("SIS_RDPCMEDIANO"), "2012-2024", "sim",
  "alternativos-por-governo.csv (A-SIS_*)", "2020-2022 em quintas visitas; so PNADC")
a("Gini", "PNAD -> PNADC (2012), Censo x PNAD, quintas visitas 2020-2022, harmonizacao Ipea", "Palma e participacao do 10o decil (PIP)", "parcialmente", "nao usa a formula do Gini, mas usa os mesmos microdados e herda a quebra PNAD->PNADC",
  "Banco Mundial PIP (decile1..10)", "mesma API do PIP", "1981-2024", "sim", "alternativos-por-governo.csv (A-PIP-a, A-PIP-b)", "ainda separado em dois spells (PNAD | PNADC)")
a("Gini", "idem", "razao entre a renda dos 10% mais ricos e dos 40% mais pobres (Ipea PPA)", "parcialmente", "idem", "Ipeadata PPA_L0_03RZ10R40P", IPEA.format("PPA_L0_03RZ10R40P"), "2016-2024", "sim",
  "alternativos-por-governo.csv (A-PPA)", "so PNADC e so 2016-2024")
a("Expectativa de vida", "projecoes IBGE (Rev. 2000, 2008, 2013, 2018, 2024), tabuas como publicadas x reconstruidas", "obitos e nascidos vivos REGISTRADOS (SIM/SINASC, Ministerio da Saude) e mortalidade infantil registrada", "nao (contagem direta)",
  "sao contagens, nao dependem de projecao populacional; mas sofrem sub-registro, que o proprio IBGE reconhece", "DATASUS SIM/SINASC (nao baixado; URL nao verificada ❓)", "n/d", "n/d", "nao", "nao ha",
  "taxa exige denominador (populacao), que volta a depender das projecoes")
a("Expectativa de vida", "idem", "UMA vintage unica para todos os anos (UN WPP via Banco Mundial)", "parcialmente", "tira a mistura de vintages dentro da serie, mas e outra instituicao com metodo proprio (inclui HIV)",
  "Banco Mundial WDI SP.DYN.LE00.IN", "https://api.worldbank.org/v2/country/BRA/indicator/SP.DYN.LE00.IN?format=json&per_page=20000", "1960-2024", "sim", "comparativo-metodo-constante.csv (E-WDI)", "0,3 a 1,5 ano abaixo da vigente do IBGE")
a("Agregados monetarios M1-M4", "conceito de base (1980), reformulacao de 2001, NT 48 de 2018", "papel-moeda emitido / em circulacao", "nao", "componente comum a todos os conceitos, nao e redefinido nas notas de 2001 e 2018",
  "BCB SGS 1786 (1980-) e Ipeadata HIST_PME (1946-1979); ja em monetario/ (PME_med12_pib_pct)", "ver monetario/manifest.jsonl", "1946-2025", "sim (em outra pasta)", "monetario/saida/anual.csv", "o conceito de papel-moeda emitido em 1946-1979 nao foi comparado ao de 1980 em fonte primaria ❓")
CAB = list(R[0].keys())
with open(H / "indicadores-alternativos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=CAB)
    w.writeheader()
    w.writerows(R)
print(len(R), "linhas")
