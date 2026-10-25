"""Baixa, pela cadeia de hash (govfc.chain add), as fontes primarias da divida externa e do custo da divida publica.

Pedido do Ulisses (2026-10-23): "voltamos a ter divida externa... quero que entre tambem na pesquisa, o aumento da
divida e etc". Dimensao "ext" do pre-registro original (PREREGISTRATION.md, tabela de dimensoes: "external debt").
Os codigos do SGS vem da Nota Explicativa do BCB de 24/02/2026 (Nota para a Imprensa - Estatisticas do Setor Externo,
secao "Estatisticas e Indicadores do Setor Externo"), que nomeia cada serie; nada foi adivinhado.
Uso: ``PYTHONPATH=<repo>/code python3 scripts/baixar.py`` (idempotente: pula o que ja esta na cadeia).
"""
import json, os, subprocess, sys, time
from pathlib import Path

PASTA = Path(__file__).resolve().parent.parent
REPO = "/Users/ulissesflores/Developer/brazil-governments-factcheck"
SGS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{c}/dados?formato=json"
TE = "https://www.bcb.gov.br/content/estatisticas/Documents/Tabelas_especiais/"
NOTA = "https://www.bcb.gov.br/content/estatisticas/hist_estatisticassetorexterno/"
env = dict(os.environ, PYTHONPATH=REPO + "/code")

# codigo: nota (nome dado pela Nota Explicativa do BCB de 24/02/2026 ou pelo catalogo CKAN do BCB)
SERIES = {
    3684: "divida externa bruta, conceito restrito (sem intercompanhia e sem titulos no mercado domestico), US$ milhoes, trimestral desde 1972T4; data do SGS = primeiro mes do trimestre, posicao de fim de trimestre",
    7941: "operacoes intercompanhia (investimento direto), US$ milhoes, trimestral",
    22160: "titulos de divida negociados no mercado domestico em poder de nao residentes, US$ milhoes, trimestral",
    25563: "divida externa bruta inclusive operacoes intercompanhia e titulos de divida negociados no mercado domestico (conceito BPM6/EDS 2013), US$ milhoes, trimestral desde 2002",
    21521: "divida externa bruta do setor publico, conceito restrito, US$ milhoes, trimestral desde 1990 (o BCB revisou a divisao publico/privado de dez/2020 a set/2025 em mar/2026)",
    4192: "PIB mensal em US$ milhoes correntes (denominador das razoes do BCB: soma de 12 meses)",
    11408: "divida externa do setor publico / divida externa bruta, %, DESCONTINUADA pelo BCB em fev/2026",
    11409: "divida externa liquida / PIB, %, DESCONTINUADA pelo BCB em fev/2026 (construcao original nao adere ao BPM6/EDS 2013)",
    3685: "divida externa liquida, US$ milhoes, trimestral desde 1987T2, AINDA PUBLICADA (acrescentada em 2026-10-24: a serie e a coluna M da Tabela 31 das Notas ate jan/2026, bruta restrita menos reservas, creditos brasileiros no exterior e haveres de bancos comerciais; coincide com a Tabela 31 em jun/2024-set/2025; 2026T2 = +5.083,49, o numero da manchete de 21/10/2026)",
    24010: "posicao de investimento internacional liquida, US$ milhoes, trimestral desde 2002",
    12506: "posicao de investimento internacional liquida / PIB, %, DESCONTINUADA pelo BCB em fev/2026",
    22705: "exportacoes de bens e servicos, US$ milhoes, mensal desde 1995",
    5760: "NFSP sem desvalorizacao cambial, % do PIB, fluxo acumulado em 12 meses, juros nominais, setor publico consolidado (CKAN 5760)",
    5727: "NFSP sem desvalorizacao cambial, % do PIB, fluxo acumulado em 12 meses, resultado nominal, setor publico consolidado (CKAN 5727; positivo = deficit)",
    5793: "NFSP sem desvalorizacao cambial, % do PIB, fluxo acumulado em 12 meses, resultado primario, setor publico consolidado (CKAN 5793; positivo = deficit)",
}
#: 11407 sem janela devolve HTML de erro do BCB; com janela devolve a serie (conferido 2026-10-23)
SERIES_JANELA = {
    11407: "divida externa bruta (conceito restrito, SGS 3684) / PIB (SGS 4192, 12 meses), %, DESCONTINUADA pelo BCB em fev/2026; baixada com janela 1970-2026 porque sem janela o endpoint devolve erro",
}
ARQUIVOS = [
    (TE + "DivExt_T.xls", "bruto/DivExt_T.xls", "Tabela especial 'Divida externa bruta e divida externa de curto prazo por vencimento residual': trimestral 2001T4-2026T2 por setor do devedor; memo 'divida externa do setor publico' no conceito amplo (linha 103)"),
    (TE + "PIIMoeda_T.xlsx", "bruto/PIIMoeda_T.xlsx", "Tabela especial 'PII - instrumentos de divida - distribuicao por moeda e setor institucional - ativos e passivos' (base do conceito BPM6 de divida externa liquida, segundo a Nota Explicativa)"),
    (NOTA + "202601_Tabelas_de_estatisticas_do_setor_externo.xlsx", "bruto/202601_Tabelas_de_estatisticas_do_setor_externo.xlsx", "Nota para a Imprensa de jan/2026: ultima edicao com a Tabela 31 'Indicadores de sustentabilidade da divida externa' (divida externa liquida oficial, conceito antigo, ate dez/2025)"),
    (NOTA + "202609_Tabelas_de_estatisticas_do_setor_externo.xlsx", "bruto/202609_Tabelas_de_estatisticas_do_setor_externo.xlsx", "Nota para a Imprensa de set/2026: Tabela 15 (divida externa bruta por devedor e prazo, jun/2026 = 407.102,7)"),
    (NOTA + "202602_Texto_de_estatisticas_do_setor_externo.pdf", "bruto/202602_Texto_de_estatisticas_do_setor_externo.pdf", "Nota para a Imprensa de 24/02/2026: reorganizacao das tabelas e Nota Explicativa com as formas de calculo e os codigos SGS (fonte das definicoes usadas aqui)"),
    ("https://www.bcb.gov.br/ftp/NotaEcon/nm4bpm6p.pdf", "bruto/nm4bpm6p.pdf", "Nota metodologica do BCB (jun/2015): estatisticas de divida externa no padrao BPM6 / EDS 2013"),
    ("https://bpmoney.com.br/?p=429071", "bruto/noticia_bpmoney_2026-10-21.html", "noticia que motivou o pedido (BP Money, 21/10/2026): define divida externa liquida como bruta menos reservas; guardada como evidencia, nao como fonte"),
]


def add(url, dest, nota):
    r = subprocess.run([sys.executable, "-m", "govfc.chain", "add", str(PASTA), url, str(PASTA / dest), "--nota", nota],
                       capture_output=True, text=True, cwd=REPO, env=env)
    print(dest, "OK" if r.returncode == 0 else "FALHA " + (r.stderr or r.stdout)[-300:], flush=True)
    time.sleep(0.8)


def ja_na_cadeia():
    man = PASTA / "manifest.jsonl"
    if not man.exists():
        return set()
    return {Path(json.loads(l)["arquivo"]).name for l in man.read_text().splitlines() if l.strip()}


if __name__ == "__main__":
    feitos = ja_na_cadeia()
    for c, nota in SERIES.items():
        if f"sgs_{c}.json" not in feitos:
            add(SGS.format(c=c), f"bruto/sgs_{c}.json", f"serie completa SGS {c}, sem janela: {nota}")
    for c, nota in SERIES_JANELA.items():
        if f"sgs_{c}.json" not in feitos:
            add(SGS.format(c=c) + "&dataInicial=01/01/1970&dataFinal=31/12/2026", f"bruto/sgs_{c}.json", f"SGS {c}, janela 1970-2026: {nota}")
    for url, dest, nota in ARQUIVOS:
        if Path(dest).name not in feitos:
            add(url, dest, nota)
