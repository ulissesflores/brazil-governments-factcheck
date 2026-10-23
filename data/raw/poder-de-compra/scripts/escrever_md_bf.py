#!/usr/bin/env python3
"""Escreve ../bolsa_familia_linhas.md: tabelas a partir de ../series/bolsa_familia_linhas*.csv; todo trecho citado e conferido (assert) contra os arquivos hasheados.
python3 -I escrever_md_bf.py   (sem rede)"""
import csv
import html
import json
import re
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
D = RAIZ.parent
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def htm(p):
    b = Path(p).read_bytes()
    try:
        t = b.decode("utf-8")
    except UnicodeDecodeError:
        t = b.decode("cp1252")
    return norm(html.unescape(re.sub(r"(?is)<(script|style).*?</\1>", "", re.sub(r"<[^>]+>", " ", t))))


def pdf(p):
    return norm(subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True, check=True).stdout)


PL = D / "quebras/bruto/planalto"
F = {
    "lei10836": htm(D / "dominios-1/bruto/doc/leg/lei_10836_pbf.htm"),
    "em47": htm(RAIZ / "bruto/planalto-EM47-2003-mp132.html"),
    "d5209": htm(PL / "d5209-2004.html"), "d5749": htm(PL / "d5749-2006.html"), "d6824": htm(PL / "d6824-2009.html"),
    "d6917": htm(PL / "d6917-2009.html"), "d8232": htm(PL / "d8232-2014.html"), "d8794": htm(PL / "d8794-2016.html"),
    "d9396": htm(PL / "d9396-2018.html"), "d10851": htm(RAIZ / "bruto/planalto-decreto-10851-2021.html"),
    "d10852": htm(PL / "d10852-2021.html"), "d11013": htm(PL / "d11013-2022.html"),
    "d11566": htm(D / "dominios-1/bruto/doc/leg/dec_11566_2023.htm"), "l14601": htm(PL / "l14601-2023.html"),
    "em1164": pdf(RAIZ / "bruto/planalto-EM-mp1164-2023.pdf"),
}


def Q(k, t):
    t = norm(t)
    nospace = lambda x: re.sub(r"\s+", "", x)
    assert nospace(t) in nospace(F[k]), (k, t[:70])   # compara sem espacos: a extracao de HTML separa o "o" ordinal sobrescrito
    return t


rows = list(csv.DictReader(open(RAIZ / "series/bolsa_familia_linhas.csv")))
anual = list(csv.DictReader(open(RAIZ / "series/bolsa_familia_linhas_anual.csv")))
n = lambda x, c=2: ("" if x in ("", None) else f"{float(x):.{c}f}".replace(".", ","))

out = []
w = out.append
w("# Linhas de elegibilidade do Bolsa Familia, 2004-2025\n")
w("Gerado por `scripts/escrever_md_bf.py` a partir de `series/bolsa_familia_linhas.csv` e `series/bolsa_familia_linhas_anual.csv` (calculados por `scripts/bolsa_familia.py`). Todo trecho entre aspas foi conferido por programa contra o arquivo hasheado em `bruto/` desta pasta, em `../quebras/bruto/planalto/` ou em `../dominios-1/bruto/doc/leg/`.\n")
w("> [!IMPORTANT]\n> Resposta curta. (1) **A linha nao e indexada a nada na lei nem nos decretos**: e um valor em reais fixado e, de tempos em tempos, \"majorado\" pelo Poder Executivo. (2) **A justificativa escrita e minima**: a Exposicao de Motivos da MP 132/2003 diz que os valores foram adotados \"para inicio da operacionalizacao\"; os decretos de 2006, 2009 e 2018 dizem apenas \"atualizacao\" ou \"reajuste\" de \"valores referenciais\"; os de 2014 e 2016 nao dizem nada alem de \"Altera\". (3) A linha de extrema pobreza e **metade** da linha de pobreza (50/100, 60/120, 70/140, 77/154...; em 2009-04, 69/137, arredondada para cima). (4) Medida contra o salario minimo, a linha de pobreza cai de **0,385** do salario minimo (set/2004) para **0,165** (jun/2023) e **0,134** (set/2026; o texto consolidado da Lei 14.601 lido em 19/10/2026 mantem o art. 5, II em R$ 218, sem \"Redacao dada\" nesse artigo; a unica alteracao no texto, Lei 15.348/2026, trata do Auxilio Gas). Em reais de set/2026 (INPC) a linha de pobreza foi de R$ 324,79 (2004) a R$ 361,99 (2006, maximo) a R$ 218,00 (2026).\n")
w("Glosas: **linha de pobreza** = renda mensal por pessoa da familia abaixo da qual a familia pode receber o beneficio; **per capita** = dividida pelo numero de pessoas; **PPC** (paridade do poder de compra) = taxa de conversao que iguala o poder de compra entre paises; **INPC/IPCA** = indices de inflacao do IBGE usados para trazer valores antigos a reais de hoje; **ppc 2017** = linhas do Banco Mundial calculadas com precos de 2017.\n")

w("## 1. A linha e indexada a algo?\n")
w("Texto original da Lei 10.836/2004 (art. 2, par. 6), a unica regra de atualizacao:\n")
w("> " + Q("lei10836", "Os valores dos benefícios e os valores referenciais para caracterização de situação de pobreza ou extrema pobreza de que tratam os §§ 2º e 3º poderão ser majorados pelo Poder Executivo, em razão da dinâmica socioeconômica do País e de estudos técnicos sobre o tema, atendido o disposto no parágrafo único do art. 6º") + "\n")
w("O paragrafo unico do art. 6 e o limite orcamentario:\n")
w("> " + Q("lei10836", "O Poder Executivo deverá compatibilizar a quantidade de beneficiários do Programa Bolsa Família com as dotações orçamentárias existentes") + "\n")
w("Leitura: \"poderao ser majorados\" (facultativo, e so para cima), \"em razao da dinamica socioeconomica e de estudos tecnicos\" (sem indice, sem periodicidade), \"atendido o limite orcamentario\". **Nao ha formula, indice nem referencia ao salario minimo para a linha de entrada.** A unica referencia ao salario minimo no programa aparece em 2023, e e a regra de **saida** (Lei 14.601/2023, art. 6, par. 1):\n")
w("> " + Q("l14601", "Na hipótese de a renda familiar per capita mensal superar o valor de meio salário mínimo, excluído de seu cálculo o valor dos benefícios financeiros do Programa Bolsa Família") + " [...], a família será desligada do Programa.\n")
w("A linha de entrada de 2023 e fixada **em lei** em reais:\n")
w("> " + Q("l14601", "cuja renda familiar per capita mensal seja igual ou inferior a R$ 218,00 (duzentos e dezoito reais)") + " (art. 5, II)\n")
w("Outro ponto do Decreto 5.209/2004 (art. 18, par. 1): a linha e um teto de elegibilidade, nao o unico criterio de selecao:\n")
w("> " + Q("d5209", "As famílias elegíveis ao Programa Bolsa Família, identificadas no Cadastramento Único do Governo Federal, poderão ser selecionadas a partir de um conjunto de indicadores sociais capazes de estabelecer com maior acuidade as situações de vulnerabilidade social e econômica") + "\n")

w("## 2. Justificativa de cada ato\n")
w("Os decretos publicados no Planalto nao trazem Exposicao de Motivos; o que existe e a **ementa** (titulo) e o **preambulo**. A unica Exposicao de Motivos achada para a linha e a da MP 132/2003 (E.M. 47/Casa Civil, 20/10/2003), que cria o programa:\n")
w("> " + Q("em47", "Para início da operacionalização do Bolsa Família, foi considerada em situação de extrema pobreza a família cuja renda per capita for de até R$ 50,00 (cinqüenta reais). Já como família em situação de pobreza foi considerada aquela cuja renda per capita seja de até R$ 100,00 (cem reais).") + "\n")
w("A E.M. nao explica como R$ 50 e R$ 100 foram escolhidos, nao os liga ao salario minimo e nao menciona atualizacao futura (conferido por busca no texto: nenhuma ocorrencia de \"reajust\", \"salario minimo\", \"indexa\" ou \"majora\"; \"atualizado\" aparece uma vez, sobre o Cadastro Unico).\n")
w("| inicio | ato | texto de ementa/preambulo (literal) | justificativa dada |")
w("|---|---|---|---|")
J = [
    ("2004-09", "Decreto 5.209/2004, art. 18", "d5209", "Regulamenta a Lei no 10.836, de 9 de janeiro de 2004, que cria o Programa Bolsa Família, e dá outras providências", "nenhuma"),
    ("2006-04", "Decreto 5.749/2006", "d5749", "dispondo sobre atualizações de valores referenciais para caracterização das situações de pobreza e extrema pobreza no âmbito do Programa Bolsa Família", "\"atualizacoes de valores referenciais\" (sem indice)"),
    ("2009-04", "Decreto 6.824/2009", "d6824", "atualizando os valores referenciais para caracterização das situações de pobreza e extrema pobreza no âmbito do Programa Bolsa Família", "\"atualizando os valores referenciais\" (sem indice)"),
    ("2009-09", "Decreto 6.917/2009", "d6917", "Altera os arts. 18, 19 e 28 do Decreto no 5.209, de 17 de setembro de 2004, que regulamenta a Lei no 10.836, de 9 de janeiro de 2004, que cria o Programa Bolsa Família", "nenhuma"),
    ("2014-06", "Decreto 8.232/2014", "d8232", "Altera o Decreto nº 5.209, de 17 de setembro de 2004, que regulamenta o Programa Bolsa Família, e o Decreto nº 7.492, de 2 de junho de 2011, que institui o Plano Brasil Sem Miséria", "nenhuma"),
    ("2016-07", "Decreto 8.794/2016", "d8794", "Altera o Decreto nº 5.209, de 17 de setembro de 2004, que regulamenta a Lei nº 10.836, de 9 de janeiro de 2004, que cria o Programa Bolsa Família, e o Decreto nº 7.492, de 2 de junho de 2011, que institui o Plano Brasil Sem Miséria, e dá outras providências", "nenhuma"),
    ("2018-07", "Decreto 9.396/2018", "d9396", "para reajustar valores referenciais de caracterização das situações de pobreza e de extrema pobreza e os de benefícios do Programa Bolsa Família", "\"reajustar valores referenciais\" (sem indice)"),
    ("2021-11", "Decreto 10.851/2021 (5/11/2021; linha de R$ 200/100 do Bolsa Familia, revogado pelo 10.852)", "d10851", "para reajustar os valores referenciais de caracterização das situações de pobreza e de extrema pobreza e os valores dos benefícios do Programa Bolsa Família", "\"reajustar os valores referenciais\" (sem indice)"),
    ("2021-11", "Decreto 10.852/2021, art. 20 (Auxilio Brasil)", "d10852", "Regulamenta o Programa Auxílio Brasil, instituído pela Medida Provisória nº 1.061, de 9 de agosto de 2021", "nenhuma no decreto; a E.M. da MP 1.061/2021 nao traz nenhum valor em reais (conferido por busca)"),
    ("2022-03", "Decreto 11.013/2022", "d11013", "Altera o Decreto nº 10.852, de 8 de novembro de 2021, que regulamenta o Programa Auxílio Brasil", "nenhuma"),
    ("2023-06", "Lei 14.601/2023, art. 5, II", "l14601", "cuja renda familiar per capita mensal seja igual ou inferior a R$ 218,00", "nenhuma; a E.M. da MP 1.164/2023 nao menciona R$ 218 nem salario minimo (conferido por busca)"),
]
for ini, ato, k, tr, just in J:
    w(f"| {ini} | {ato} | \"{Q(k, tr)}\" | {just} |")
assert "218" not in F["em1164"], "a EM 1164 cita 218?"
w("")
w("Nota de cobertura: a tabela do CSV `../quebras/bolsa-familia-linhas-elegibilidade.csv` nao tem a linha do Decreto 10.851/2021 (linha de R$ 200 e R$ 100 do Bolsa Familia, 5/11/2021, tres dias antes do Decreto 10.852); os valores sao os mesmos do Auxilio Brasil, entao a tabela numerica abaixo nao muda.\n")

w("## 3. Linha contra 1/4 e 1/2 do salario minimo, linha internacional e linha do Atlas\n")
w("Comparadores, todos em reais do mes de inicio do ato:\n")
w("* **1/4 e 1/2 do salario minimo vigente** (`MTE12_SALMIN12`, Ipeadata). Sao os cortes habituais do debate publico; **nao** sao a regra do programa.")
w("* **Linhas internacionais do Banco Mundial em PPC 2017**: US$ 2,15 por dia (extrema pobreza) e US$ 3,65 por dia (pobreza de renda media-baixa), com o fator IBGE SIS de R$ 2,3273771 por US$ PPC, ja usado em `../quebras/pobreza-linhas-em-reais-reais.csv`: R$ 152,20 e R$ 258,39 por mes a precos de 2017, atualizados ate cada mes pelo IPCA (media de 2017 como base; reproduz R$ 241,59 e R$ 410,14 em set/2026 do arquivo da pasta quebras). Multiplicador 365/12 dias, escolha do script de la.")
w("* **Linhas do Atlas do Desenvolvimento Humano (PNUD, Ipea e Fundacao Joao Pinheiro)**, as linhas de extrema pobreza e de pobreza que o Ipea publica no Ipeadata: extrema pobreza = \"renda domiciliar per capita igual ou inferior a R$ 70,00 mensais, em reais de agosto de 2010\" (`ADH_PIND`); pobreza = \"igual ou inferior a R$ 140,00 mensais, em reais de agosto de 2010\" (`ADH_PMPOB`). Textos do catalogo de metadados do Ipeadata (`../economia-real/meta/ipeadata-Metadados-catalogo-completo-raw.json`). Atualizadas pelo IPCA a partir de ago/2010. Nao achei outra linha propria do Ipea.\n")
w("Colunas de razao: linha do programa dividida pelo comparador (1,00 = igual; abaixo de 1 = linha do programa menor que o comparador).\n")
hdr = "| inicio | programa | pobreza R$ | extrema R$ | SM R$ | pobreza/SM | pobreza/(1/2 SM) | extrema/(1/4 SM) | pobreza / US$ 3,65 | extrema / US$ 2,15 | pobreza / Atlas pobre | extrema / Atlas extrema | pobreza em R$ set/2026 (INPC) | extrema em R$ set/2026 | SM em R$ set/2026 |"
w(hdr)
w("|" + "---|" * 15)
for r in rows:
    w(f"| {r['inicio']} | {r['programa']} | {n(r['linha_pobreza_R$'],0)} | {n(r['linha_extrema_R$'],0)} | {n(r['SM_vigente_R$'],0)} | {n(r['pobreza_/_SM'],3)} | {n(r['pobreza_/_meio_SM'],3)} | {n(r['extrema_/_um_quarto_SM'],3)} | {n(r['pobreza_/_US$3,65'],3)} | {n(r['extrema_/_US$2,15'],3)} | {n(r['pobreza_/_Atlas_pobre'],3)} | {n(r['extrema_/_Atlas_extrema'],3)} | {n(r['pobreza_real_set2026_INPC'])} | {n(r['extrema_real_set2026_INPC'])} | {n(r['SM_real_set2026_INPC'])} |")
w("\nA linha de 2026-09 e a mesma de 2023-06 (R$ 218): o texto consolidado da Lei 14.601 lido em 19/10/2026 nao tem alteracao no art. 5, II (a unica \"Redacao dada\" no texto, Lei 15.348/2026, trata do Auxilio Gas); nao procurei decreto posterior.\n")
w("Tabela ano a ano (linha em vigor em dezembro de cada ano; mesmos comparadores):\n")
w("| dez/ano | programa | em vigor desde | pobreza R$ | extrema R$ | SM R$ | pobreza/SM | extrema/(1/4 SM) | pobreza / US$ 3,65 | extrema / US$ 2,15 | extrema / Atlas extrema | pobreza em R$ set/2026 | extrema em R$ set/2026 |")
w("|" + "---|" * 13)
for r in anual:
    w(f"| {r['ano_dezembro']} | {r['programa']} | {r['inicio']} | {n(r['linha_pobreza_R$'],0)} | {n(r['linha_extrema_R$'],0)} | {n(r['SM_vigente_R$'],0)} | {n(r['pobreza_/_SM'],3)} | {n(r['extrema_/_um_quarto_SM'],3)} | {n(r['pobreza_/_US$3,65'],3)} | {n(r['extrema_/_US$2,15'],3)} | {n(r['extrema_/_Atlas_extrema'],3)} | {n(r['pobreza_real_set2026_INPC'])} | {n(r['extrema_real_set2026_INPC'])} |")
w("\n## 4. O que a tabela mostra (so leitura dos numeros)\n")
w("* Pobreza / salario minimo: 0,385 (2004-09), 0,295 (2009-04), 0,213 (2014-06), 0,187 (2018-07), 0,165 (2023-06), 0,134 (2026-09). A linha de extrema pobreza valia 0,77 de 1/4 do salario minimo em 2004-09, 0,69 em 2006-04, 0,60 em 2009, 0,43 em 2014-06 e 0,35 em 2022-03: o salario minimo subiu mais que a linha.")
w("* Em reais de set/2026 (INPC) a linha de pobreza vai de R$ 324,79 (2004-09) a R$ 361,99 (2006-04, maximo da serie), R$ 297,92 (2014-06), R$ 270,29 (2018-07), R$ 250,58 (2021-11) e R$ 249,27 (2023-06): queda de 31% do maximo de 2006 ao valor de 2023-06. Variacao real de cada ato frente ao anterior (INPC): 2006-04 +11,5%; 2009-04 -1,5%; 2009-09 +0,7%; 2014-06 -17,0%; 2016-07 -8,4%; 2018-07 -1,0%; 2021-11 -7,3%; 2022-03 +0,8%; 2023-06 -1,3%. Entre atos a linha nominal fica parada e perde valor real.")
w("* Contra as linhas internacionais, em reais do mes: a linha de extrema pobreza do programa esta em 0,68 (2004) a 0,75 (2009) de US$ 2,15 PPC 2017 e em 0,52-0,53 (2021-22); a de pobreza fica em 0,80 (2004) a 0,88 (2009) e em 0,61-0,62 (2021-23) de US$ 3,65. Contra o Atlas (R$ 70 de ago/2010), a extrema pobreza do programa era 1,04 em 2006-2009 e 0,73-0,74 em 2021-22.")
w("* Nenhuma das comparacoes diz que a linha \"deveria\" ser outra: os comparadores sao de natureza diferente (salario minimo e uma renda do trabalhador; linha do Banco Mundial e consumo em PPC de 2017; Atlas e renda domiciliar de 2010).")
(RAIZ / "bolsa_familia_linhas.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("ok", len(out), "linhas")
