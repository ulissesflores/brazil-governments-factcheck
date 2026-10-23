"""Gera quebras.csv, comparacao_regra.csv, comparacao_regra.md e series/gates_quebras.txt.

Uso: python3 -I scripts/gerar_quebras_comparacao.py     (sem rede; so le arquivos locais)
 - confere a cadeia de hash antes de tudo;
 - cada `trecho_citado` e conferido LITERALMENTE (sem acento/pontuacao/caixa) contra o arquivo local citado;
   se algum nao for achado, o script para sem escrever nada;
 - efeito_medido e calculado aqui, de series/edu_rendimento.csv (nunca digitado).
Dependencias externas locais: pdftotext, textutil (macOS) e soffice (so para tabelas_ciclos_2000.xls).
"""
import csv
import html
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib  # noqa: E402
from ufs import uf as norm_uf  # noqa: E402

RAIZ = lib.RAIZ
SER = os.path.join(RAIZ, "series")
GATES = []


def gate(ok, msg):
    GATES.append(("OK  " if ok else "FALHA ") + msg)
    if not ok:
        print("FALHA:", msg)
        sys.exit(1)


# ---------------------------------------------------------------- dados
DADOS = {}
for r in csv.DictReader(open(os.path.join(SER, "edu_rendimento.csv"), encoding="utf-8")):
    DADOS[(r["indicador"], r["uf"], int(r["ano"]))] = float(r["valor"])
ANOS = sorted({k[2] for k in DADOS})
UFS27 = [u for u in __import__("ufs").UFS]


def val(ind, uf, ano):
    return DADOS.get((ind, uf, ano))


def f2(x):
    return "" if x is None else ("%.2f" % x)


# ---------------------------------------------------------------- tabela INEP de ciclos (1999)
def ler_ciclos_1999():
    xls = os.path.join(lib.BRUTO, "tabelas_ciclos_2000.xls")
    with tempfile.TemporaryDirectory() as tmp:
        cs = lib.converter(xls, tmp)
        rows = lib.ler_csv(cs[0])
        texto = "\n".join(" ".join(r) for r in rows)
    i = next(k for k, r in enumerate(rows) if r and r[0].startswith("Número de matrículas"))
    out = {}
    for r in rows[i:]:
        if len(r) < 8:
            continue
        u = norm_uf(r[0])
        if u is None or u.startswith("REG"):
            continue
        n = lambda s: lib.num(s) or 0.0  # noqa: E731  ('-' = 0)
        out[u] = dict(total=n(r[1]), seriado_pct=n(r[3]), ciclos_n=n(r[4]), ciclos_pct=n(r[5]), mista_pct=n(r[7]))
    return out, texto


CICLOS99, TEXTO_CICLOS99 = ler_ciclos_1999()
gate(len(CICLOS99) == 28, "tabelas_ciclos_2000.xls (matriculas por forma de organizacao, 1999): %d localidades lidas" % len(CICLOS99))
# controle: ciclos% + mista% <= 10 (todas as redes, 1999)
CTRL = sorted(u for u, d in CICLOS99.items() if u != "BR" and d["ciclos_pct"] + d["mista_pct"] <= 10.0)
gate(len(CTRL) >= 8, "grupo sem a regra (ciclos%% + mista%% <= 10 em 1999, INEP): %d UFs: %s" % (len(CTRL), ",".join(CTRL)))


def media_ctrl(ind, ano):
    v = [DADOS[(ind, u, ano)] for u in CTRL if (ind, u, ano) in DADOS]
    return (sum(v) / len(v), len(v)) if v else (None, 0)


# ---------------------------------------------------------------- texto dos arquivos para conferir trechos
_CACHE = {}


def _norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def _txt_html(b):
    try:
        t = b.decode("utf-8")
    except UnicodeDecodeError:
        t = b.decode("latin-1")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def texto_de(spec):
    """spec: 'caminho' | 'zip.zip::membro'. Devolve texto normalizado."""
    if spec in _CACHE:
        return _CACHE[spec]
    if spec == "@ciclos1999":
        t = TEXTO_CICLOS99
    else:
        if "::" in spec:
            z, m = spec.split("::")
            with zipfile.ZipFile(os.path.join(RAIZ, z)) as zz, tempfile.TemporaryDirectory() as tmp:
                p = os.path.join(tmp, "x" + os.path.splitext(m)[1])
                open(p, "wb").write(zz.read(m))
                t = _ler(p)
        else:
            t = _ler(os.path.join(RAIZ, spec))
    _CACHE[spec] = _norm(t)
    return _CACHE[spec]


def _ler(p):
    e = os.path.splitext(p)[1].lower()
    if e == ".pdf":
        return subprocess.run(["pdftotext", p, "-"], capture_output=True).stdout.decode("utf-8", "replace")
    if e in (".html", ".htm"):
        return _txt_html(open(p, "rb").read())
    if e == ".doc":
        return subprocess.run(["textutil", "-convert", "txt", "-stdout", p], capture_output=True).stdout.decode("utf-8", "replace")
    return open(p, encoding="utf-8", errors="replace").read()


# ---------------------------------------------------------------- efeito medido nos dados
RE_EF = "edu_reprovacao_ef_total__estadual"
AB_EF = "edu_abandono_ef_total__estadual"


def _antes(uf, Y, ind):
    c = [a for a in ANOS if a < Y and (ind, uf, a) in DADOS and media_ctrl(ind, a)[1]]
    return c[-1] if c else None


def _depois(uf, ano_min, ind):
    c = [a for a in ANOS if a >= ano_min and (ind, uf, a) in DADOS and media_ctrl(ind, a)[1]]
    return c[0] if c else None


def efeito(uf, Y, rotulo=""):
    """Reprovacao e abandono do EF total, rede estadual: ano-base (ultimo ano < Y), 1o ano >= Y e 1o ano >= Y+3.
    Mostra a UF, a media simples do grupo sem a regra e a diferenca das variacoes (pp)."""
    partes = []
    for nome, ind in (("reprovacao", RE_EF), ("abandono", AB_EF)):
        b = _antes(uf, Y, ind)
        if b is None:
            partes.append("%s: sem ano-base disponivel antes de %d" % (nome, Y))
            continue
        pts = []
        for ymin in (Y, Y + 3):
            y = _depois(uf, ymin, ind)
            if y is None or y == b or any(p[0] == y for p in pts):
                continue
            du = val(ind, uf, y) - val(ind, uf, b)
            cm_b, _ = media_ctrl(ind, b)
            cm_y, n = media_ctrl(ind, y)
            dc = cm_y - cm_b
            pts.append((y, "%s %s: %d %.2f -> %d %.2f (%+.2f pp); grupo sem a regra (n=%d) %.2f -> %.2f (%+.2f pp); dif. das variacoes %+.2f pp"
                        % (uf, nome, b, val(ind, uf, b), y, val(ind, uf, y), du, n, cm_b, cm_y, dc, du - dc)))
        partes.extend(p[1] for p in pts)
    return " | ".join(partes)


def _cobertura(pred):
    return sum(1 for k in DADOS if pred(k))


N_PRE2007 = _cobertura(lambda k: k[2] <= 2005)
N_ESTADUAL_EF_9805 = _cobertura(lambda k: k[2] in range(1996, 2002) and "ef_" in k[0] and k[0].endswith("__estadual"))

# ---------------------------------------------------------------- numeros de 2005 x 2007 (INEP)
CAL = {r["uf"]: r for r in csv.DictReader(open(os.path.join(SER, "calibracao_2005.csv")))}
SOB = {r["uf"]: r for r in csv.DictReader(open(os.path.join(SER, "sobreposicao_2007.csv")))}


def passo_2005_2007():
    a = [(u, float(CAL[u]["aband_publicada"]), float(SOB[u]["aband_tx_rendimento2007"]),
          float(CAL[u]["reprov_publicada"]), float(SOB[u]["reprov_tx_rendimento2007"])) for u in CAL if u in SOB]
    dab = [x[2] - x[1] for x in a]
    dre = [x[4] - x[3] for x in a]
    br = next(x for x in a if x[0] == "BR")
    ref = []
    for ind in ("edu_abandono_ef_total__total", "edu_reprovacao_ef_total__total"):
        ref.append("%s BR 2007->2009 %+.2f pp" % (ind.split("_")[1], val(ind, "BR", 2009) - val(ind, "BR", 2007)))
    return ("Brasil EF total (todas as redes), tabela 5.5 de 2005 -> tabela 6.6.1/planilha de 2007: abandono %.1f -> %.1f (%+.1f pp), reprovacao %.1f -> %.1f (%+.1f pp); "
            "em %d localidades o abandono caiu em %d e a reprovacao caiu em %d; media das variacoes: abandono %+.2f pp, reprovacao %+.2f pp; "
            "referencia de variacao de 2 anos com metodo constante: %s. Mistura mudanca de metodo e mudanca real: nao ha ano de sobreposicao 2005/2007 (2006 nao existe)."
            % (br[1], br[2], br[2] - br[1], br[3], br[4], br[4] - br[3], len(a), sum(d < 0 for d in dab), sum(d < 0 for d in dre),
               sum(dab) / len(dab), sum(dre) / len(dre), "; ".join(ref)))


PASSO0507 = passo_2005_2007()


def calib_txt():
    n = len(CAL)
    ok = sum(1 for r in CAL.values() if max(abs(float(r["dif_aprov_pp"])), abs(float(r["dif_reprov_pp"])), abs(float(r["dif_aband_pp"]))) <= 0.15)
    mx_re = max(abs(float(r["dif_reprov_pp"])) for r in CAL.values())
    mx_ab, uf_ab = max((abs(float(r["dif_aband_pp"])), r["uf"]) for r in CAL.values())
    mx_px = max(abs(float(r["dif_proxy_pp"])) for r in CAL.values())
    return ("Taxa calculada das contagens da Sinopse x tabela 5.5 publicada, 2005, EF: %d de %d localidades dentro de 0,15 p.p. nas tres taxas; "
            "maior |dif| reprovacao %.2f p.p.; abandono %.2f p.p. (%s); proxy reprov/(aprov+reprov) %.2f p.p." % (ok, n, mx_re, mx_ab, uf_ab, mx_px))


CALTXT = calib_txt()
SOBTXT = "28 localidades, max |dif| 0.0 p.p. entre 'Resultados Censo Escolar 2007' (6.6.1) e a planilha tx_rendimento 2007 (EF total)"

# ---------------------------------------------------------------- quebras
SEC = "FONTE SECUNDARIA | "
N = "NORMA NAO LOCALIZADA (texto)"
Q = []


def q(**k):
    base = dict(indicador="", serie="", data_quebra="", tipo_de_quebra="", metodo_antigo="", metodo_novo="", razao_declarada_pela_fonte="",
                fonte_primaria_url="", trecho_citado="", arquivo_local="", direcao_do_efeito="", como_a_direcao_foi_determinada="",
                efeito_medido="", como_medido="", apresentada_como_aprimoramento="", celulas_afetadas="")
    base.update(k)
    Q.append(base)


IND_TX = "taxas de aprovacao, reprovacao e abandono do EF (INEP)"
S_TX = "series/edu_rendimento.csv (edu_aprovacao/reprovacao/abandono_*)"
NT = "bruto/nt_indicadores_rendimento_%s.pdf"

# ---- (i) definicoes do INEP
q(indicador=IND_TX, serie=S_TX, data_quebra="2005 -> 2007",
  tipo_de_quebra="definicao_taxa",
  metodo_antigo="Sinopse do Censo Escolar ate 2005: contagens agregadas por escola (aprovados, reprovados, afastados por abandono, afastados por transferencia, admitidos apos 30/3); taxa publicada na tabela 5.5 (formula nao descrita no arquivo)",
  metodo_novo="Educacenso 2007+: registro individual do aluno (modulo Situacao do Aluno, coletado no ano seguinte); taxa = X/(APR+REP+ABA); fora do denominador falecidos e SIR (sem informacao)",
  razao_declarada_pela_fonte="a coleta com identificacao do aluno 'permitiu retratar o alunado ... de uma forma mais aperfeicoada'",
  fonte_primaria_url="bruto/sinopse_2007_antiga.zip (Texto_introdutorio_.pdf)",
  trecho_citado="Em 2005 teve início um ciclo de reformulação operacional e metodológica do Censo Escolar, com a montagem de um cadastro de alunos e docentes da educação básica, que culminou, em 2007, com a implantação do sistema Educacenso",
  arquivo_local="bruto/sinopse_2007_antiga.zip::Texto_introdutorio_.pdf",
  direcao_do_efeito="abandono publicado cai e aprovacao sobe entre os dois anos (sinal medido); parte pode ser mudanca real",
  como_a_direcao_foi_determinada="diferenca entre a tabela 5.5 de 2005 e a tabela de 2007, mesmas 28 localidades; nao ha 2006",
  efeito_medido=PASSO0507, como_medido="series/calibracao_2005.csv (coluna publicada) x series/sobreposicao_2007.csv (coluna tx_rendimento2007)",
  apresentada_como_aprimoramento="sim (INEP: 'um aprimoramento no conhecimento da realidade educacional brasileira')",
  celulas_afetadas="todas as taxas por UF e rede de 2007 em diante (linhas do edu_rendimento.csv com ano >= 2007) contra as de 2005 e antes (%d linhas com ano <= 2005)" % N_PRE2007)

q(indicador=IND_TX, serie=S_TX, data_quebra="1994-2005 (contagens) x 2005 (publicada)",
  tipo_de_quebra="definicao_taxa",
  metodo_antigo="taxa publicada pelo INEP em 2005 (tabela 5.5 da Sinopse)",
  metodo_novo="taxa recalculada neste dossie das contagens da Sinopse com a formula X/(APR+REP+ABA) da NT de 2011; usada para 1996-2001 e 2004",
  razao_declarada_pela_fonte="(nenhuma: o recalculo e deste dossie; a Sinopse so traz contagens para 1996-2001)",
  fonte_primaria_url="bruto/resultados_censo_escolar_2006.zip (Resultados_censo_escolar2006.pdf)",
  trecho_citado="5.5 Indicadores de Rendimento Escolar – Aprovação, Reprovação e Abandono",
  arquivo_local="bruto/resultados_censo_escolar_2006.zip::Resultados_censo_escolar2006.pdf",
  direcao_do_efeito="erro de abandono calculado pode ser grande em poucas UFs; reprovacao e proxy reprov/(aprov+reprov) quase iguais as publicadas",
  como_a_direcao_foi_determinada="comparacao direta calculada x publicada em 2005",
  efeito_medido=CALTXT, como_medido="series/calibracao_2005.csv (gerada por scripts/extrair.py)",
  apresentada_como_aprimoramento="nao se aplica",
  celulas_afetadas="%d linhas de edu_rendimento.csv com ano <= 2005 (todas calculadas, nao publicadas)" % N_PRE2007)

q(indicador="matricula e taxas do Censo Escolar", serie="series/edu_rendimento.csv", data_quebra="2007",
  tipo_de_quebra="cobertura_censo",
  metodo_antigo="coleta agregada por escola; referencia na pratica do fim de marco ('Alunos Admitidos apos 30/3/2005')",
  metodo_novo="Educacenso: cadastro individual de aluno e professor; data de referencia = ultima quarta-feira de maio; identifica aluno com mais de uma matricula",
  razao_declarada_pela_fonte="retratar 'com maior exatidao' os alunos matriculados com frequencia regular",
  fonte_primaria_url="bruto/sinopse_2007_antiga.zip (Texto_introdutorio_.pdf)",
  trecho_citado="Porém, parte da queda de matrícula registrada em 2007 deve-se às mudanças no procedimento de coleta das informações do Censo Escolar, que, ao contar com informações dos indivíduos e ter a data de referência da coleta modificada, reduziu de maneira drástica a dupla contagem de alunos.",
  arquivo_local="bruto/sinopse_2007_antiga.zip::Texto_introdutorio_.pdf",
  direcao_do_efeito="matricula total de 2007 menor que a de 2006 (dupla contagem retirada); efeito direto sobre taxa nao informado pela fonte",
  como_a_direcao_foi_determinada="texto do INEP; o numero de matriculas de 2006 e 2007 nao esta em series/ (so o texto)",
  efeito_medido="INEP: reducao de quase tres milhoes de matriculas na educacao basica entre 2006 e 2007 (-5,2%), 'em parte' por demografia e 'em parte' pela mudanca de coleta; parcela nao separada pela fonte",
  como_medido="citacao da Sinopse 2007 (Texto introdutorio); nao recalculado",
  apresentada_como_aprimoramento="sim ('um aprimoramento no conhecimento da realidade educacional brasileira')",
  celulas_afetadas="todas as celulas de 2007 em diante e a comparacao com 2005 e antes")

q(indicador="matricula e taxas do Censo Escolar", serie="series/edu_rendimento.csv", data_quebra="2005 (referencia 30/3) -> 2007 (ultima quarta-feira de maio)",
  tipo_de_quebra="cobertura_censo",
  metodo_antigo="data de referencia do fim de marco",
  metodo_novo="ultima quarta-feira de maio",
  razao_declarada_pela_fonte="ver linha anterior",
  fonte_primaria_url="bruto/resultados_censo_escolar_2006.zip (Resultados_censo_escolar2006.pdf)",
  trecho_citado="5.4 Alunos Admitidos após 30/3/2005",
  arquivo_local="bruto/resultados_censo_escolar_2006.zip::Resultados_censo_escolar2006.pdf",
  direcao_do_efeito="nao determinada", como_a_direcao_foi_determinada="nao medida (so o titulo da tabela 5.4 mostra a data antiga)",
  efeito_medido="nao medido", como_medido="-", apresentada_como_aprimoramento="sim (mesma fonte da linha anterior)",
  celulas_afetadas="todas as taxas de 2005 e antes contra 2007 em diante")

q(indicador=IND_TX, serie=S_TX, data_quebra="2007 (publicacao 'Resultados' x planilha de taxas)",
  tipo_de_quebra="sobreposicao_de_publicacoes",
  metodo_antigo="'Resultados do Censo Escolar 2007' (tabela 6.6.1, 2009)", metodo_novo="planilha 'Taxas de Rendimento por Brasil/Regioes/UFs' 2007",
  razao_declarada_pela_fonte="(nao ha)", fonte_primaria_url="series/gates.txt (derivado de bruto/sinopse_2007_antiga.zip e bruto/tx_rendimento_brasil_regioes_UFs_2007.zip)",
  trecho_citado="OK  sobreposicao 2007 (Resultados Censo Escolar 2007 6.6.1 x tx_rendimento 2007, EF total): 28 localidades, max |dif| 0.0 p.p.",
  arquivo_local="series/gates.txt", direcao_do_efeito="nenhuma", como_a_direcao_foi_determinada="diferenca nula",
  efeito_medido=SOBTXT, como_medido="series/sobreposicao_2007.csv", apresentada_como_aprimoramento="nao se aplica",
  celulas_afetadas="nenhuma: as duas publicacoes de 2007 coincidem")

q(indicador=IND_TX, serie=S_TX, data_quebra="2008 -> 2009 -> 2010 -> 2011",
  tipo_de_quebra="definicao_taxa",
  metodo_antigo="NT 2008 (regra 5): matricula inicial 'Abandono' vira abandono na origem se a(s) escola(s) de admissao posterior informar 'Transferido' ou 'Abandono'",
  metodo_novo="NT 2009: exige rendimento em mais de uma escola posterior ou transferido/abandono em pelo menos duas; NT 2010: tres condicoes (5.1-5.3); NT 2011 e 2013: so se 'transferido' ou 'abandono' em TODAS as escolas posteriores",
  razao_declarada_pela_fonte="regras 'adotadas, em ordem de prioridade' para resolver conflitos de informacao; a nota nao explica cada ajuste",
  fonte_primaria_url="bruto/nt_indicadores_rendimento_2011.pdf (OCR em series/ocr/)",
  trecho_citado="a matrícula será considerada como situação final “Abandono” na origem se possuir “Transferido” ou “abandono” em todas as escolas de admissão posterior",
  arquivo_local="series/ocr/nt_indicadores_rendimento_2011.ocr.txt",
  direcao_do_efeito="criterio do abandono na origem fica mais estreito de 2008 para 2011 (menos matriculas classificadas como abandono); magnitude desconhecida",
  como_a_direcao_foi_determinada="leitura comparada do texto das NTs 2008, 2009, 2010, 2011 e 2013; o INEP so conta os casos de cada regra em 2008",
  efeito_medido="nao medido; NT 2008 informa 3.966.400 matriculas na regra 6 (abandono sem admissao posterior) e 4.766 na regra 5 (todas as etapas e modalidades)",
  como_medido="contagens citadas da NT 2008 (series/ocr/nt_indicadores_rendimento_2008.ocr.txt)",
  apresentada_como_aprimoramento="nao declarado (a NT descreve criterios 'para dirimir duvidas e garantir a transparencia')",
  celulas_afetadas="taxas de abandono e aprovacao 2008-2011 por UF (nao separavel do restante)")

q(indicador=IND_TX, serie=S_TX, data_quebra="2008 (NT 2009 para o Censo 2009)",
  tipo_de_quebra="definicao_taxa",
  metodo_antigo="Educacao Especial classificada como 'sem informacao' (fora das taxas)",
  metodo_novo="a partir de 2009 a Educacao Especial deixa de ter o campo 'sem informacao' e e tratada como o ensino regular",
  razao_declarada_pela_fonte="pedido da Secretaria de Educacao Especial",
  fonte_primaria_url="bruto/nt_indicadores_rendimento_2010.pdf",
  trecho_citado="A partir de 2009, a pedido da Secretaria de Educação Especial (SEESP) solicitou que não houvesse o campo Sem Informação para a modalidade de Educação Especial",
  arquivo_local=NT % "2010",
  direcao_do_efeito="nao determinada", como_a_direcao_foi_determinada="nao medida",
  efeito_medido="nao medido", como_medido="-", apresentada_como_aprimoramento="nao declarado",
  celulas_afetadas="taxas de 2009 em diante contra 2008 e antes (so a parte que depende de matriculas de educacao especial)")

q(indicador="taxa de nao resposta (TNR); nao entra nas tres taxas", serie="(nao esta em series/)", data_quebra="2010 -> 2016",
  tipo_de_quebra="definicao_taxa",
  metodo_antigo="TNR = SIR/(n - FAL) x 100 (NT 2010)", metodo_novo="TNR = SIR/(APR+REP+ABA+SIR) x 100 (documento INEP 2017/2018)",
  razao_declarada_pela_fonte="(nao declarada)", fonte_primaria_url="bruto/doc_taxas_rendimento_escolar_2017.pdf",
  trecho_citado="Taxa de não resposta = [SIR/(APR + REP + ABA+ SIR)] X 100",
  arquivo_local="bruto/doc_taxas_rendimento_escolar_2017.pdf",
  direcao_do_efeito="nenhuma sobre aprovacao, reprovacao e abandono (a formula das tres taxas e a mesma de 2008)",
  como_a_direcao_foi_determinada="comparacao das formulas nos textos",
  efeito_medido="nao se aplica as tres taxas", como_medido="-", apresentada_como_aprimoramento="nao declarado",
  celulas_afetadas="nenhuma das tres taxas")

q(indicador="aprovacao, reprovacao e abandono do EF, recortes 'anos iniciais' e 'anos finais'", serie="edu_*_ef_ai__* e edu_*_ef_af__*",
  data_quebra="2005 (Lei 11.114) e 2006-02-06 (Lei 11.274); prazo ate 2010",
  tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="EF de 8 anos (1a a 4a serie e 5a a 8a serie), matricula obrigatoria aos 7 anos",
  metodo_novo="EF de 9 anos, iniciando aos 6 anos (1o ao 5o ano e 6o ao 9o ano); redes migram em momentos diferentes ate 2010",
  razao_declarada_pela_fonte="(a lei nao traz exposicao de motivos no texto)",
  fonte_primaria_url="https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11274.htm",
  trecho_citado="O ensino fundamental obrigatório, com duração de 9 (nove) anos, gratuito na escola pública, iniciando-se aos 6 (seis) anos de idade",
  arquivo_local="normas/planalto_lei_11274_2006.html",
  direcao_do_efeito="nao determinada: o recorte 'anos iniciais' passa de 4 para 5 anos de escolaridade e 'anos finais' de 4 para 4 (6o ao 9o)",
  como_a_direcao_foi_determinada="texto da lei; nao ha ano de sobreposicao 8 x 9 anos separado nas planilhas",
  efeito_medido="nao medido: as planilhas de 2007-2010 trazem os dois recortes misturados (rotulo 'EF de 8 e 9 anos misturados' em edu_rendimento.csv)",
  como_medido="-", apresentada_como_aprimoramento="nao declarado no texto da lei",
  celulas_afetadas="edu_*_ef_ai__* e edu_*_ef_af__* de 2007 em diante")

q(indicador="aprovacao, reprovacao e abandono antes de 1996", serie="edu_reprov_sobre_aprov_mais_reprov_* (1994-1995)",
  data_quebra="1994-1995",
  tipo_de_quebra="cobertura_censo",
  metodo_antigo="Sinopse 1995 e 1996 trazem so aprovados e reprovados (taxa de abandono nao existe)", metodo_novo="a partir de 1996 as contagens incluem 'afastados por abandono'",
  razao_declarada_pela_fonte="(nao ha)", fonte_primaria_url="bruto/sinopse_educacao_basica_1995.xlsm e bruto/sinopse_educacao_basica_1996.xls",
  trecho_citado="OK  sinopse_educacao_basica_1996.xls: 2 tabelas de contagem lidas, anos [1995]",
  arquivo_local="series/gates.txt", direcao_do_efeito="1994-1995 so permite o proxy reprov/(aprov+reprov)",
  como_a_direcao_foi_determinada="so duas tabelas de contagem lidas nesses dois arquivos (aprovados e reprovados)",
  efeito_medido="proxy disponivel; abandono indisponivel em 1994 e 1995", como_medido="series/gates.txt; scripts/extrair.py (docstring)",
  apresentada_como_aprimoramento="nao se aplica",
  celulas_afetadas="abandono e aprovacao 1994-1995 (inexistentes)")

# ---- (ii) normas
FED = "https://www.planalto.gov.br/ccivil_03/leis/l9394.htm"
q(indicador="reprovacao e abandono no EF (todas as redes estaduais)", serie="edu_reprovacao_ef_*__estadual; edu_abandono_ef_*__estadual",
  data_quebra="1996-12-20", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="progressao por serie", metodo_novo="LDB art. 32: facultado desdobrar o EF em ciclos; escolas seriadas podem adotar progressao continuada",
  razao_declarada_pela_fonte="(nao ha no texto da lei)", fonte_primaria_url=FED,
  trecho_citado="§ 1o É facultado aos sistemas de ensino desdobrar o ensino fundamental em ciclos.",
  arquivo_local="normas/planalto_lei_9394_1996.html",
  direcao_do_efeito="norma permissiva: a reprovacao pode cair onde o sistema adotar a regra", como_a_direcao_foi_determinada="texto da lei (autoriza, nao obriga)",
  efeito_medido="nao medido (efeito depende de cada norma estadual abaixo)", como_medido="-",
  apresentada_como_aprimoramento="nao declarado no texto da lei",
  celulas_afetadas="todas as UFs; so produz efeito onde o sistema estadual adotou ciclos ou progressao continuada")

q(indicador="reprovacao e abandono no EF, rede estadual de SP", serie="edu_*_ef_*__estadual UF=SP",
  data_quebra="1984 (Ciclo Basico, 1a e 2a series); vigente em 1997 segundo o CEE",
  tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="seriacao com reprovacao ao fim de cada serie", metodo_novo="Ciclo Basico: as duas series iniciais formam um ciclo (rede estadual)",
  razao_declarada_pela_fonte="'O atual ciclo basico ... ja adotado na rede estadual'",
  fonte_primaria_url="https://www.ceesp.sp.gov.br/wp-content/uploads/2024/11/d9in8-97.pdf (Indicacao CEE 8/97); data de 1984: FONTE SECUNDARIA redalyc.org/pdf/298/29832102.pdf",
  trecho_citado="O atual ciclo básico, formado pelos dois anos iniciais do ensino fundamental, já adotado na rede estadual",
  arquivo_local="normas/ceesp_d9in8-97.pdf",
  direcao_do_efeito="reprovacao nas duas primeiras series tende a cair (sem retencao no ciclo)", como_a_direcao_foi_determinada="texto da Indicacao; ato de 1984 nao localizado",
  efeito_medido="fora da janela da serie (1996+): ato de 1984 sem dados; ver linha de 1998", como_medido="-",
  apresentada_como_aprimoramento="sim ('sinais evidentes de que tal mecanismo tem condicoes de ser assimilado')",
  celulas_afetadas="UF=SP, anos iniciais, 1996-1997")

q(indicador="reprovacao e abandono no EF, rede estadual de SP", serie="edu_*_ef_*__estadual UF=SP",
  data_quebra="1997-07-30 (aprovada); homologada Res. SE de 04/08/97, DOE 05/08/97", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="progressao por serie (ciclo basico so nas duas series iniciais)",
  metodo_novo="Deliberacao CEE 09/97: regime de progressao continuada no EF de oito anos, em um ou mais ciclos",
  razao_declarada_pela_fonte="viabilizar universalizacao, acesso e permanencia, regularizar fluxo idade/serie e melhorar a qualidade (Indicacao CEE 8/97)",
  fonte_primaria_url="https://www.ceesp.sp.gov.br/wp-content/uploads/2024/11/d9in8-97.pdf",
  trecho_citado="Fica instituído no Sistema de Ensino do Estado de São Paulo o regime de progressão continuada, no ensino fundamental, com duração de oito anos.",
  arquivo_local="normas/ceesp_d9in8-97.pdf",
  direcao_do_efeito="reprovacao deve cair; a Indicacao fala em reduzir 'repetencia' e 'evasao'", como_a_direcao_foi_determinada="texto da Indicacao 8/97 (objetivo declarado) + dado",
  efeito_medido=efeito("SP", 1998), como_medido="series/edu_rendimento.csv; 1998 = primeiro ano letivo sob a Res. SE 4/98; grupo sem a regra = UFs com ciclos% + mista% <= 10 na tabela INEP 1999",
  apresentada_como_aprimoramento="sim (texto da Indicacao: 'a inovacao mais relevante e positiva na historia recente da educacao no Estado de Sao Paulo')",
  celulas_afetadas="UF=SP, rede estadual, EF anos iniciais, finais e total, 1998 em diante")

q(indicador="reprovacao e abandono no EF, rede estadual de SP", serie="edu_*_ef_*__estadual UF=SP",
  data_quebra="1997-07-30", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="avaliacao com funcao de reter", metodo_novo="Indicacao CEE 8/97: avaliacao de progresso, nao punitiva",
  razao_declarada_pela_fonte="'a repetencia constitui um pernicioso ralo' de recursos",
  fonte_primaria_url="https://www.ceesp.sp.gov.br/wp-content/uploads/2024/11/d9in8-97.pdf",
  trecho_citado="é preciso substituir uma concepção de avaliação escolar punitiva e excludente por uma concepção de avaliação de progresso e de desenvolvimento da aprendizagem",
  arquivo_local="normas/ceesp_d9in8-97.pdf",
  direcao_do_efeito="reprovacao deve cair", como_a_direcao_foi_determinada="texto da Indicacao",
  efeito_medido="ver linha anterior (mesmo conjunto de celulas)", como_medido="-", apresentada_como_aprimoramento="sim",
  celulas_afetadas="idem")

q(indicador="reprovacao e abandono no EF, rede estadual de SP", serie="edu_*_ef_*__estadual UF=SP",
  data_quebra="1997-12-17", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="-", metodo_novo="Indicacao CEE 22/97: avaliacao e transicao entre ciclos sob progressao continuada",
  razao_declarada_pela_fonte="orientar a avaliacao sob o novo regime",
  fonte_primaria_url="https://www.ceesp.sp.gov.br/wp-content/uploads/2024/11/ind22-97.pdf",
  trecho_citado="A escola organizada em mais de um ciclo deve garantir também a progressão continuada na transição de um para outro ciclo.",
  arquivo_local="normas/ceesp_ind22-97.pdf",
  direcao_do_efeito="a retencao fica restrita a casos fora da transicao entre ciclos", como_a_direcao_foi_determinada="texto da Indicacao",
  efeito_medido="ver linha de 1997-07-30", como_medido="-", apresentada_como_aprimoramento="nao declarado",
  celulas_afetadas="idem")

q(indicador="reprovacao e abandono no EF, rede estadual de SP", serie="edu_*_ef_*__estadual UF=SP",
  data_quebra="1998-01-15", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="seriacao no EF (ciclo basico nas 2 series iniciais)", metodo_novo="Resolucao SE 4/98: EF em dois ciclos (1a-4a e 5a-8a serie); reprovacao so ao fim de cada ciclo e por frequencia abaixo de 75%",
  razao_declarada_pela_fonte="segue a Deliberacao CEE 09/97",
  fonte_primaria_url=SEC + "https://legado.anped.org.br/sites/default/files/gt05-1047-int.doc (texto da Res. SE 4/98 NAO LOCALIZADO)",
  trecho_citado="A progressão continuada foi implantada na rede estadual paulista através da Resolução no 4/98 de 15/01/98, organizando o ensino fundamental em dois ciclos",
  arquivo_local="normas/anped_gt05_1047_progressao_continuada_sp.doc",
  direcao_do_efeito="reprovacao dentro do ciclo vedada: queda esperada na 1a, 2a, 3a, 5a, 6a e 7a series",
  como_a_direcao_foi_determinada="texto da norma segundo a fonte secundaria + dado",
  efeito_medido=efeito("SP", 1998), como_medido="series/edu_rendimento.csv (ver linha da Deliberacao 09/97; mesmas celulas)",
  apresentada_como_aprimoramento="sim (objetivo declarado: eliminar a cultura da repetencia)",
  celulas_afetadas="UF=SP, rede estadual, 1998 em diante (4.436.407 alunos segundo a fonte secundaria)")

q(indicador="reprovacao e abandono no EF, rede estadual de SP", serie="edu_*_ef_*__estadual UF=SP",
  data_quebra="2003-08-15", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="recuperacao intensiva nas ferias de janeiro (aplicada em 1998, 1999 e 2000)", metodo_novo="Resolucao SE 84/2003 extingue a recuperacao intensiva",
  razao_declarada_pela_fonte="(nao localizada)",
  fonte_primaria_url=SEC + "https://www.redalyc.org/pdf/684/68480212.pdf (texto da Res. SE 84/2003 NAO LOCALIZADO)",
  trecho_citado="Foi extinta em 2003, pela Resolução SE 84, de 15/08/2003.",
  arquivo_local="normas/redalyc_68480212.pdf",
  direcao_do_efeito="nao determinada", como_a_direcao_foi_determinada="norma retira uma etapa de recuperacao; o dado de 2002/2003 nao existe",
  efeito_medido=efeito("SP", 2003), como_medido="series/edu_rendimento.csv; 2002 e 2003 ausentes (primeiro ano disponivel apos a norma: 2004)",
  apresentada_como_aprimoramento="nao declarado na fonte secundaria", celulas_afetadas="UF=SP, rede estadual, 2004 em diante")

q(indicador="reprovacao e abandono no EF, rede estadual de SP", serie="edu_*_ef_*__estadual UF=SP",
  data_quebra="2014 (anunciado 2013-11-08)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="dois ciclos; retencao possivel no 4o/5o e no 8o/9o ano",
  metodo_novo="tres ciclos (1o-3o, 4o-6o, 7o-9o); retencao possivel ao fim de cada etapa",
  razao_declarada_pela_fonte="'medida significa avanco conquistado de forma democratica' (dirigente regional); consultas a rede desde 2011",
  fonte_primaria_url=SEC + "https://www.dgabc.com.br/Noticia/493316/rede-estadual-passa-a-reprovar-mais-vezes (numero da resolucao/deliberacao NAO LOCALIZADO)",
  trecho_citado="prevê divisão dos alunos em três ciclos de aprendizagem e não mais em dois: do 1º ao 3º ano, do 4º ao 6º e do 7º ao 9º. Com isso, haverá possibilidade de retenção ao fim de cada etapa.",
  arquivo_local="normas/dgabc_2013-11-09_rede_estadual_reprovar_mais.html",
  direcao_do_efeito="restringe a regra: reprovacao pode subir", como_a_direcao_foi_determinada="texto da noticia + dado de 2013-2017",
  efeito_medido=efeito("SP", 2014), como_medido="series/edu_rendimento.csv; grupo sem a regra definido em 1999, nao reverificado em 2014",
  apresentada_como_aprimoramento="sim (titulo da propria Secretaria em 2011: 'reorganizacao do ensino fundamental de nove anos'; Indicacao ALESP 1929/2015 chama de 'aprimoramento da progressao continuada')",
  celulas_afetadas="UF=SP, rede estadual, 2014 em diante")

q(indicador="reprovacao e abandono no EF, rede municipal de SP (capital)", serie="(nao ha serie municipal em series/)",
  data_quebra="1992", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="seriacao", metodo_novo="Regimento Comum das Escolas Municipais: tres ciclos (1a-3a, 4a-6a, 7a-8a); reprovacao possivel ao fim de cada ciclo",
  razao_declarada_pela_fonte="democratizacao do ensino",
  fonte_primaria_url=SEC + "https://www.scielo.br/j/ep/a/bMn89qFD5Hs56YCLjZnJpzF/?format=pdf&lang=pt (decreto/regimento NAO LOCALIZADO)",
  trecho_citado="No município de São Paulo a implementação dos ciclos no ensino fundamental ocorreu em 1992, ao final do primeiro mandato do PT, e abrangeu todas as escolas municipais.",
  arquivo_local="normas/scielo_ep_barretto_sousa_2004.pdf",
  direcao_do_efeito="queda de reprovacao esperada na rede municipal", como_a_direcao_foi_determinada="texto da fonte secundaria",
  efeito_medido="nao medido (a serie estadual nao inclui a rede municipal da capital)", como_medido="-",
  apresentada_como_aprimoramento="sim ('alternativa capaz de contribuir para a democratizacao do ensino')",
  celulas_afetadas="nenhuma celula de series/ (rede municipal por UF nao esta no recorte)")

q(indicador="reprovacao e abandono no EF, rede municipal de SP (capital)", serie="(nao ha serie municipal em series/)",
  data_quebra="1997-2000", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="tres ciclos", metodo_novo="dois ciclos de quatro anos, 'com possibilidade de reprovacao ao final de cada ciclo', para acompanhar o agrupamento da rede estadual",
  razao_declarada_pela_fonte="acompanhar o agrupamento da rede estadual",
  fonte_primaria_url=SEC + "https://www.scielo.br/j/ep/a/bMn89qFD5Hs56YCLjZnJpzF/?format=pdf&lang=pt (decreto municipal NAO LOCALIZADO)",
  trecho_citado="por decreto da administração municipal, altera-se a organização dos ciclos para acompanhar o agrupamento proposto na rede estadual paulista",
  arquivo_local="normas/scielo_ep_barretto_sousa_2004.pdf",
  direcao_do_efeito="muda os pontos de retencao (de tres para dois, nas series 4a e 8a)", como_a_direcao_foi_determinada="texto da fonte secundaria",
  efeito_medido="nao medido", como_medido="-", apresentada_como_aprimoramento="nao declarado",
  celulas_afetadas="nenhuma celula de series/")

# MG
UFU = "https://repositorio.ufu.br/bitstream/123456789/27152/1/Avalia%c3%a7%c3%a3oContextoRegime.pdf"
UFUF = "normas/ufu_ciclos_mg.pdf"
q(indicador="reprovacao e abandono no EF, rede estadual de MG", serie="edu_*_ef_*__estadual UF=MG",
  data_quebra="1984-12-06 (Res. SEE/MG 5231/84; CBA em todas as escolas em 1985)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="seriacao", metodo_novo="Ciclo Basico de Alfabetizacao (CBA)", razao_declarada_pela_fonte="Plano Mineiro de Educacao 1985/1987",
  fonte_primaria_url=SEC + UFU + " (texto da Res. 5231/84 NAO LOCALIZADO)",
  trecho_citado="colocou em prática o CBA, como diretriz expressa no Plano Mineiro de Educação 1985/1987, através da resolução n° 523 I dc 06/12/84",
  arquivo_local=UFUF, direcao_do_efeito="reprovacao nas series iniciais tende a cair", como_a_direcao_foi_determinada="descricao do CBA na fonte secundaria",
  efeito_medido="fora da janela (1996+)", como_medido="-", apresentada_como_aprimoramento="sim",
  celulas_afetadas="UF=MG, anos iniciais, 1996 em diante (CBA continua vigente)")
q(indicador="reprovacao e abandono no EF, rede estadual de MG", serie="edu_*_ef_*__estadual UF=MG",
  data_quebra="1991 (Res. SEE/MG 6806/91)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="CBA interrompido na gestao anterior", metodo_novo="CBA retomado 'com objetivos um pouco diferentes'", razao_declarada_pela_fonte="(nao localizada)",
  fonte_primaria_url=SEC + UFU + " (texto da Res. 6806/91 NAO LOCALIZADO)",
  trecho_citado="o CBA foi retomado nos termos da Resolução n° 6806/91",
  arquivo_local=UFUF, direcao_do_efeito="idem", como_a_direcao_foi_determinada="idem",
  efeito_medido="fora da janela (1996+)", como_medido="-", apresentada_como_aprimoramento="nao declarado", celulas_afetadas="UF=MG, anos iniciais, 1996 em diante")
q(indicador="reprovacao e abandono no EF, rede estadual de MG", serie="edu_*_ef_*__estadual UF=MG",
  data_quebra="1996-12-20 (publicada) / 1997", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="CBA nas 2 primeiras series", metodo_novo="Res. SEE/MG 7915: CBA passa a articular as tres primeiras series em 1997", razao_declarada_pela_fonte="(nao localizada)",
  fonte_primaria_url=SEC + UFU + " (texto da Res. 7915 NAO LOCALIZADO)",
  trecho_citado="Em 1997, o CBA passou a articular as três primeiras séries do Ensino Fundamental, nos termos da Resolução n° 7915, publicada em 20 de dezembro de 1996",
  arquivo_local=UFUF, direcao_do_efeito="reprovacao na 3a serie tende a cair", como_a_direcao_foi_determinada="texto da fonte secundaria",
  efeito_medido=efeito("MG", 1997), como_medido="series/edu_rendimento.csv; 1996 so tem EF total; mistura com a linha de 1998",
  apresentada_como_aprimoramento="nao declarado", celulas_afetadas="UF=MG, rede estadual, 1997 em diante")
q(indicador="reprovacao e abandono no EF, rede estadual de MG", serie="edu_*_ef_*__estadual UF=MG",
  data_quebra="1997 (Res. SEE/MG 8086/97); obrigatoria a partir de 1998", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="CBA (3 series) e seriacao nas demais", metodo_novo="progressao continuada em dois ciclos de quatro anos, obrigatoria em todas as escolas da rede",
  razao_declarada_pela_fonte="'o regime seriado se apresentava por estruturas excludentes e seletivas'",
  fonte_primaria_url=SEC + UFU + " (texto da Res. 8086/97 NAO LOCALIZADO)",
  trecho_citado="A partir de 1998, em caráter obrigatório para todas as escolas da rede estadual de ensino, entrou em vigor a reorganização dos tempos escolares previsto na Resolução 8086/97.",
  arquivo_local=UFUF, direcao_do_efeito="reprovacao deve cair", como_a_direcao_foi_determinada="texto da fonte secundaria + dado",
  efeito_medido=efeito("MG", 1998), como_medido="series/edu_rendimento.csv; 1998 = primeiro ano obrigatorio",
  apresentada_como_aprimoramento="sim (progressao continuada como alternativa a exclusao)", celulas_afetadas="UF=MG, rede estadual, 1998 em diante")
q(indicador="reprovacao e abandono no EF, rede estadual de MG", serie="edu_*_ef_*__estadual UF=MG",
  data_quebra="1999 (Res. SEE/MG 12/99)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="dois ciclos obrigatorios", metodo_novo="a escola reexamina e decide a forma de organizacao do EF para o ano letivo de 1999 (flexibilizacao)",
  razao_declarada_pela_fonte="'a necessidade de se substituir a cultura da reprovacao pela cultura da progressao continuada da aprendizagem com sucesso'",
  fonte_primaria_url=SEC + UFU + " (texto da Res. 12/99 NAO LOCALIZADO)",
  trecho_citado="Atribuir à escola, para o exercício do ano letivo de 1999, a responsabilidade de reexaminar a forma de organização do Ensino Fundamental adotada",
  arquivo_local=UFUF, direcao_do_efeito="restringe a regra (deixa de ser obrigatoria); reprovacao pode subir onde a escola voltar a seriacao",
  como_a_direcao_foi_determinada="texto da fonte secundaria; Barretto e Mitrulis (2001) dizem que a gestao seguinte 'opta pela flexibilizacao da medida' e que o Censo 2000 mostra 'grande' adesao",
  efeito_medido=efeito("MG", 1999), como_medido="series/edu_rendimento.csv; INEP 1999: 69,5% das matriculas do EF de MG em escolas so com ciclos (tabelas_ciclos_2000.xls)",
  apresentada_como_aprimoramento="sim (a propria resolucao fala em 'progressao continuada ... com sucesso')", celulas_afetadas="UF=MG, rede estadual, 1999 em diante")
q(indicador="reprovacao e abandono no EF, rede estadual de MG", serie="edu_*_ef_*__estadual UF=MG",
  data_quebra="2000-01-20 (Res. SEE/MG 006/2000)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="dois ciclos (Res. 8086/97)", metodo_novo="tres ciclos: Basico, Intermediario e Avancado", razao_declarada_pela_fonte="(nao localizada)",
  fonte_primaria_url=SEC + UFU + " (texto da Res. 006/2000 NAO LOCALIZADO)",
  trecho_citado="20 de janeiro de 2000, por meio da Resolução n° 006, a SEE/MG propôs a organização do ensino fundamental dividida em três ciclos",
  arquivo_local=UFUF, direcao_do_efeito="muda os pontos de retencao; sentido nao determinado", como_a_direcao_foi_determinada="texto da fonte secundaria",
  efeito_medido=efeito("MG", 2000), como_medido="series/edu_rendimento.csv", apresentada_como_aprimoramento="nao declarado",
  celulas_afetadas="UF=MG, rede estadual, 2000 em diante")
q(indicador="reprovacao e abandono no EF, rede estadual de MG", serie="edu_*_ef_*__estadual UF=MG",
  data_quebra="2004 (hipotese do briefing)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="-", metodo_novo="NORMA NAO LOCALIZADA: nenhuma fonte baixada registra revogacao ou restricao em 2004 em MG",
  razao_declarada_pela_fonte="-", fonte_primaria_url="-",
  trecho_citado="O estado de Minas Gerais, que adotara para a sua rede o regime de ciclos entre 1995 e 1998, opta, na gestão política que se segue, pela flexibilização da medida",
  arquivo_local="normas/scielo_ea_barretto_mitrulis_2001.html", direcao_do_efeito="-",
  como_a_direcao_foi_determinada="a flexibilizacao documentada e de 1999 (linha de Res. 12/99), nao de 2004",
  efeito_medido="nao medido", como_medido="-", apresentada_como_aprimoramento="-", celulas_afetadas="-")

# PR
q(indicador="reprovacao e abandono no EF, rede estadual do PR", serie="edu_*_ef_*__estadual UF=PR",
  data_quebra="1988-03-14", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="seriacao", metodo_novo="Decreto 2545: Ciclo Basico de Alfabetizacao nas series iniciais",
  razao_declarada_pela_fonte="'necessidade de reversao do insucesso escolar nas series iniciais'",
  fonte_primaria_url=SEC + "https://publicacoes.fcc.org.br/eae/article/download/2163/2120/8210 (texto do Decreto 2545 NAO LOCALIZADO)",
  trecho_citado="A implantação do Ciclo Básico de Alfabetização, em 14 de março de 1988, pelo Decreto nº 2545",
  arquivo_local="normas/fcc_eae_parana_ciclo_basico.pdf", direcao_do_efeito="reprovacao nas series iniciais tende a cair",
  como_a_direcao_foi_determinada="texto da fonte secundaria", efeito_medido="fora da janela (1996+)", como_medido="-",
  apresentada_como_aprimoramento="sim", celulas_afetadas="UF=PR, anos iniciais, 1996 em diante; INEP 1999: 6,8% das matriculas em escolas so com ciclos")

# CE
q(indicador="reprovacao e abandono no EF, rede estadual do CE", serie="edu_*_ef_*__estadual UF=CE",
  data_quebra="1997 (ciclos); implantacao gradativa 1998-2000", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="seriacao", metodo_novo="ciclos (4: 3 anos + 3 x 2 anos), previstos em 40% das escolas em 1998, mais 40% em 1999 e toda a rede em 2000",
  razao_declarada_pela_fonte="inspirado na 'Escola Plural', orientacoes da Unesco e fundamentacao vygotskyana",
  fonte_primaria_url=SEC + "https://www.scielo.br/j/ea/a/K6mBgJwFvzgyhHkNrBbPfNF/?lang=pt (documento 'Ceara, 1997' citado por Barretto e Mitrulis; texto NAO LOCALIZADO)",
  trecho_citado="Dados do Censo Escolar desse ano revelam, contudo, que a organização em ciclos ainda abrange apenas cerca de 60% das escolas estaduais cearenses.",
  arquivo_local="normas/scielo_ea_barretto_mitrulis_2001.html", direcao_do_efeito="reprovacao deve cair onde a regra vigora", como_a_direcao_foi_determinada="texto da fonte secundaria",
  efeito_medido=efeito("CE", 1998), como_medido="series/edu_rendimento.csv; implantacao parcial (60% das escolas estaduais em 2000)",
  apresentada_como_aprimoramento="nao declarado", celulas_afetadas="UF=CE, rede estadual, 1998 em diante")
q(indicador="reprovacao e abandono no EF, rede estadual do CE", serie="edu_*_ef_*__estadual UF=CE",
  data_quebra="1998 (Parecer CEC 1014/98)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="-", metodo_novo="Parecer 1014/98 do Conselho Estadual de Educacao do Ceara (sobre ciclos)", razao_declarada_pela_fonte="(nao localizada)",
  fonte_primaria_url=SEC + "https://anpuh.org.br/uploads/anais-simposios/pdf/2019-01/1548206571_cb23d99dbf04fb9855c6acf6a996323f.pdf (texto do Parecer NAO LOCALIZADO)",
  trecho_citado="Cf. Parecer nº 1014/98 do Conselho Estadual de Educação do Ceará",
  arquivo_local="normas/anpuh_2019_ceara_parecer1014.pdf", direcao_do_efeito="nao determinada", como_a_direcao_foi_determinada="so a citacao da existencia do parecer",
  efeito_medido="ver linha anterior", como_medido="-", apresentada_como_aprimoramento="nao declarado", celulas_afetadas="UF=CE, rede estadual")

# MS
q(indicador="reprovacao e abandono no EF, rede estadual de MS", serie="edu_*_ef_*__estadual UF=MS",
  data_quebra="1998-02-10 (Res. SED 1.222/98)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="seriacao (com projeto piloto TAL em 8 escolas)", metodo_novo="EF de 9 anos em tres ciclos de tres anos; Ciclo I imediato em 1998, os demais gradativos",
  razao_declarada_pela_fonte="(a dissertacao descreve implantacao 'emergencial e verticalizada')",
  fonte_primaria_url=SEC + "https://posgraduacao.ufms.br/portal/trabalho-arquivos/download/631 (texto da Res. SED 1.222/98 NAO LOCALIZADO)",
  trecho_citado="Fica instituído o Ensino Fundamental, com duração de 09 (nove) anos, devendo o seu currículo ser desenvolvido em 03 (três) Ciclos com 03 (três) anos cada um",
  arquivo_local="normas/ufms_ciclos_ms_1998_2002.pdf", direcao_do_efeito="reprovacao deve cair; EF de 9 anos tambem muda o recorte",
  como_a_direcao_foi_determinada="texto da norma segundo a fonte secundaria + dado",
  efeito_medido=efeito("MS", 1998), como_medido="series/edu_rendimento.csv", apresentada_como_aprimoramento="nao declarado",
  celulas_afetadas="UF=MS, rede estadual, 1998 em diante")
q(indicador="reprovacao e abandono no EF, rede estadual de MS", serie="edu_*_ef_*__estadual UF=MS",
  data_quebra="2001 (Res. SED 1.452/00, de 18/12/2000)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="EF de 9 anos organizado em ciclos (Res. SED 1.401/2000)", metodo_novo="EF de 8 anos; ciclos so nos anos iniciais (Ciclo I e II de 2 anos), serie nos anos finais",
  razao_declarada_pela_fonte="(nao localizada)",
  fonte_primaria_url=SEC + "https://posgraduacao.ufms.br/portal/trabalho-arquivos/download/631 (texto da Res. SED 1.452/00 NAO LOCALIZADO)",
  trecho_citado="o Ensino Fundamental, a partir de 2001, terá a duração de 8 (oito) anos, com o currículo organizado por ciclos nos anos iniciais e por série nos anos finais",
  arquivo_local="normas/ufms_ciclos_ms_1998_2002.pdf", direcao_do_efeito="restringe a regra: volta a seriacao nos anos finais; reprovacao nos anos finais pode subir",
  como_a_direcao_foi_determinada="texto da fonte secundaria + dado",
  efeito_medido=efeito("MS", 2001), como_medido="series/edu_rendimento.csv", apresentada_como_aprimoramento="nao declarado",
  celulas_afetadas="UF=MS, rede estadual, anos finais, 2001 em diante")

# MT
q(indicador="reprovacao e abandono no EF, rede estadual de MT", serie="edu_*_ef_*__estadual UF=MT",
  data_quebra="2002-11-05 (Res. 262/02-CEE/MT)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="normas gerais das Res. 118/01 e 150/99-CEE/MT (textos NAO LOCALIZADOS)", metodo_novo="normas aplicaveis a organizacao curricular por ciclos de formacao no EF e no medio do sistema estadual",
  razao_declarada_pela_fonte="Lei Complementar 49/98, art. 10, e Parecer 289/02-CEB/CEE/MT",
  fonte_primaria_url="https://fep.if.usp.br/~profis/arquivo/docs_curriculares/MT/Mato_Grosso_Resolucao_262_02_CEE_Ciclos_de_Formacao.pdf",
  trecho_citado="Estabelece as normas aplicáveis para a organização curricular por ciclos de formação no Ensino Fundamental e Médio do Sistema Estadual de Ensino de Mato Grosso.",
  arquivo_local="normas/mt_resolucao_262_02_cee.pdf", direcao_do_efeito="regula escolas que optarem por ciclos; reprovacao pode cair nelas",
  como_a_direcao_foi_determinada="a norma e opcional ('as instituicoes que estruturarem'); sem dado de 2002-2003",
  efeito_medido=efeito("MT", 2003), como_medido="series/edu_rendimento.csv; primeiro ano disponivel apos a norma: 2004",
  apresentada_como_aprimoramento="nao declarado", celulas_afetadas="UF=MT, rede estadual, 2004 em diante (adesao opcional)")

# RJ / PE / RS / ES / RN
BM = "https://www.scielo.br/j/ea/a/K6mBgJwFvzgyhHkNrBbPfNF/?lang=pt"
q(indicador="reprovacao e abandono no EF, rede estadual do RJ", serie="edu_*_ef_*__estadual UF=RJ",
  data_quebra="1994", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="seriacao", metodo_novo="'bloco unico' (flexibiliza o tempo de aprender, semelhante ao ciclo basico) na proposta curricular do estado",
  razao_declarada_pela_fonte="semelhante ao ciclo basico quanto a flexibilizacao do tempo de aprender",
  fonte_primaria_url=SEC + BM + " (ato normativo NAO LOCALIZADO)",
  trecho_citado="o bloco único, já presente na formulação da proposta curricular do município da capital, publicada em 1991-92, foi incorporado pela do estado em 1994.",
  arquivo_local="normas/scielo_ea_barretto_mitrulis_2001.html", direcao_do_efeito="reprovacao nas series iniciais tende a cair",
  como_a_direcao_foi_determinada="texto da fonte secundaria", efeito_medido="fora da janela (1996+)", como_medido="-",
  apresentada_como_aprimoramento="nao declarado",
  celulas_afetadas="UF=RJ, 1996 em diante; B&M: 78,7% das escolas estaduais com ciclos em 2000 (sistemas mistos)")
q(indicador="reprovacao e abandono no EF, rede estadual de PE", serie="edu_*_ef_*__estadual UF=PE",
  data_quebra="1968", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="seriacao", metodo_novo="organizacao por niveis na escola primaria", razao_declarada_pela_fonte="'justificativa de cunho psicologico'",
  fonte_primaria_url=SEC + BM + " (ato normativo NAO LOCALIZADO)",
  trecho_citado="Pernambuco adotou a organização por níveis em 1968",
  arquivo_local="normas/scielo_ea_barretto_mitrulis_2001.html", direcao_do_efeito="fora da janela", como_a_direcao_foi_determinada="-",
  efeito_medido="fora da janela; B&M (2001): PE tem 'percentual de escolas estaduais com ciclos proximo ou inferior a 5%' em 2000 (grupo sem a regra deste dossie)", como_medido="-",
  apresentada_como_aprimoramento="nao declarado", celulas_afetadas="nenhuma na janela 1996+")
q(indicador="reprovacao e abandono no EF, rede estadual do RS", serie="edu_*_ef_*__estadual UF=RS",
  data_quebra="1958", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="seriacao", metodo_novo="classes de recuperacao ('uma modalidade de progressao continuada')", razao_declarada_pela_fonte="reprovacoes sem 'influencia positiva' (texto B&M)",
  fonte_primaria_url=SEC + BM + " (ato normativo NAO LOCALIZADO)",
  trecho_citado="O estado do Rio Grande do Sul, dando os primeiros passos nesse sentido, adotou em 1958 uma modalidade de progressão continuada",
  arquivo_local="normas/scielo_ea_barretto_mitrulis_2001.html", direcao_do_efeito="fora da janela", como_a_direcao_foi_determinada="-",
  efeito_medido="fora da janela; INEP 1999: RS 2,3% das matriculas em escolas so com ciclos; norma de ciclos do estado na decada de 1990 NAO LOCALIZADA", como_medido="-",
  apresentada_como_aprimoramento="nao declarado", celulas_afetadas="nenhuma na janela 1996+")
q(indicador="reprovacao e abandono no EF, redes estaduais de MS, ES, RN, RJ e MG", serie="edu_*_ef_*__estadual",
  data_quebra="ate 2000 (medida pelo Censo Escolar 2000)", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="-", metodo_novo="adesao medida (% de escolas estaduais com ciclos, sistemas mistos): MS 96,9, ES 93,4, RN 88,1, RJ 78,7, MG 73,6; SP 100",
  razao_declarada_pela_fonte="-", fonte_primaria_url=SEC + BM + " (normas de ES e RN NAO LOCALIZADAS)",
  trecho_citado="São Paulo é o único estado da federação em que todas as escolas estão organizadas sob esse regime.",
  arquivo_local="normas/scielo_ea_barretto_mitrulis_2001.html", direcao_do_efeito="-", como_a_direcao_foi_determinada="-",
  efeito_medido="adesao, nao efeito", como_medido="citacao", apresentada_como_aprimoramento="-", celulas_afetadas="ES e RN: regra_vigente 'nd' fora de 1999-2000")
q(indicador="tabela INEP de organizacao do EF por UF", serie="series/ciclos_1999_inep.csv",
  data_quebra="1999", tipo_de_quebra="mudanca_de_regra",
  metodo_antigo="-", metodo_novo="matriculas por forma de organizacao (seriado, ciclos, mais de uma forma), Brasil 1999, todas as redes",
  razao_declarada_pela_fonte="-", fonte_primaria_url="bruto/tabelas_ciclos_2000.xls (INEP, Wayback 2003-03-19)",
  trecho_citado="Número de matrículas por forma de organização, segundo as Unidades da Federação - Brasil 1999",
  arquivo_local="@ciclos1999", direcao_do_efeito="-", como_a_direcao_foi_determinada="-",
  efeito_medido="BR: 61,5% seriado, 23,0% ciclos, 15,5% mais de uma forma; SP 80,1% ciclos; MG 69,5%; grupo sem a regra deste dossie: " + ",".join(CTRL),
  como_medido="series/ciclos_1999_inep.csv (gerado deste arquivo)", apresentada_como_aprimoramento="-", celulas_afetadas="define regra_vigente e grupo sem a regra")

# ---------------------------------------------------------------- confere trechos
nfalha = []
for i, r in enumerate(Q, 1):
    t = _norm(r["trecho_citado"])
    ok = bool(t) and t in texto_de(r["arquivo_local"])
    GATES.append(("OK  " if ok else "FALHA ") + "linha %d trecho_citado em %s" % (i, r["arquivo_local"]))
    if not ok:
        nfalha.append(i)
if nfalha:
    print("trechos nao achados nas linhas", nfalha)
    for i in nfalha:
        print(i, Q[i - 1]["arquivo_local"], Q[i - 1]["trecho_citado"][:100])
    open(os.path.join(SER, "gates_quebras.txt"), "w").write("\n".join(GATES) + "\n")
    sys.exit(1)

COLS = ["indicador", "serie", "data_quebra", "tipo_de_quebra", "metodo_antigo", "metodo_novo", "razao_declarada_pela_fonte", "fonte_primaria_url",
        "trecho_citado", "direcao_do_efeito", "como_a_direcao_foi_determinada", "efeito_medido", "como_medido", "apresentada_como_aprimoramento", "celulas_afetadas"]
with open(os.path.join(RAIZ, "quebras.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(COLS)
    for r in Q:
        w.writerow([r[c] for c in COLS])
GATES.append("OK  quebras.csv: %d linhas; todos os trechos achados literalmente nos arquivos locais" % len(Q))

# ---------------------------------------------------------------- ciclos_1999_inep.csv
with open(os.path.join(SER, "ciclos_1999_inep.csv"), "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["uf", "matriculas_ef_total", "pct_seriado", "matriculas_ciclos", "pct_ciclos", "pct_mais_de_uma_forma", "grupo_sem_a_regra"])
    for u, d in CICLOS99.items():
        w.writerow([u, int(d["total"]), d["seriado_pct"], int(d["ciclos_n"]), d["ciclos_pct"], d["mista_pct"], "sim" if u in CTRL else "nao"])

# ---------------------------------------------------------------- regra_vigente
def regra(uf, ano):
    """(valor, base, confianca). Norma localizada manda; depois a medida INEP 1999; depois extrapolacao do grupo sem a regra."""
    if uf == "SP":
        if ano <= 1997:
            return "parcial", "Ciclo Basico nas 2 series iniciais (Indicacao CEE 8/97); progressao continuada so em 1998 (Res. SE 4/98)", "norma_primaria"
        if ano <= 2013:
            return "sim", "Res. SE 4/98 (secundaria) sobre Deliberacao CEE 09/97 (primaria): 2 ciclos", "norma_primaria_e_secundaria"
        return "sim", "3 ciclos desde 2014 (noticia, resolucao NAO LOCALIZADA): retencao possivel ao fim de cada etapa", "secundaria"
    if uf == "MG":
        if ano <= 1997:
            return "parcial", "CBA nas series iniciais (Res. 5231/84, 6806/91, 7915/96; secundaria)", "secundaria"
        if ano == 1998:
            return "sim", "Res. SEE/MG 8086/97 obrigatoria desde 1998 (secundaria)", "secundaria"
        if ano <= 2000:
            return "parcial", "Res. 12/99 delega a escola; Res. 006/2000 3 ciclos (secundaria); INEP 1999: 69,5% das matriculas em ciclos", "secundaria"
        return "nd", "norma posterior a 2000 NAO LOCALIZADA", "-"
    if uf == "MS":
        if 1998 <= ano <= 2001:
            return "parcial", "Res. SED 1.222/98 (Ciclo I imediato, demais gradativos); 2001: ciclos so nos anos iniciais (Res. 1.452/00); secundaria", "secundaria"
    if uf == "CE" and 1998 <= ano <= 2000:
        return "parcial", "ciclos gradativos desde 1998; cerca de 60% das escolas estaduais em 2000 (B&M 2001; secundaria)", "secundaria"
    if uf == "RJ" and 1996 <= ano <= 2001:
        return "parcial", "'bloco unico' desde 1994 (secundaria); 78,7% das escolas estaduais com ciclos em 2000 (sistemas mistos)", "secundaria"
    if uf == "PR" and 1996 <= ano <= 2001:
        return "parcial", "Ciclo Basico de Alfabetizacao desde 1988 (Decreto 2545; secundaria); INEP 1999: 6,8% ciclos + 16,2% mista", "secundaria"
    if uf == "MT" and ano >= 2003:
        return "parcial", "Res. 262/02-CEE/MT regula escolas que optarem por ciclos (primaria; adesao opcional)", "norma_primaria"
    if uf in CTRL and 1996 <= ano <= 2001:
        return "nao", "INEP 1999: ciclos% + mista% <= 10 e nenhuma norma localizada; 1996-1998 e 2000-2001 sao extrapolacao (sem prova direta)", "medida_1999_extrapolada" if ano != 1999 else "medida_1999"
    if ano == 1999 and uf in CICLOS99:
        d = CICLOS99[uf]
        if d["ciclos_pct"] >= 50:
            return "sim", "INEP 1999: %.1f%% das matriculas em escolas so com ciclos (sem norma localizada)" % d["ciclos_pct"], "medida_1999"
        return "parcial", "INEP 1999: %.1f%% ciclos + %.1f%% mais de uma forma (sem norma localizada)" % (d["ciclos_pct"], d["mista_pct"]), "medida_1999"
    return "nd", "norma e medida nao localizadas para este ano", "-"


MET = [("reprovacao", "ef_ai"), ("reprovacao", "ef_af"), ("reprovacao", "ef_total"), ("abandono", "ef_ai"), ("abandono", "ef_af"), ("abandono", "ef_total")]
SUF = ["estadual", "total"]
head = ["uf", "ano", "regra_vigente", "regra_base", "regra_confianca", "origem_taxa"]
for tipo, rec in MET:
    for rede in SUF:
        head.append("%s_%s_%s" % (tipo, rec, rede))
for rec in ("ef_ai", "ef_af", "ef_total"):
    head.append("reprov_sobre_aprov_mais_reprov_%s_estadual" % rec)
head.append("calib2005_dif_abandono_pp")
head.append("flag_qualidade")
linhas = []
for uf in ["BR"] + UFS27:
    for ano in ANOS:
        if ano < 1996:
            continue
        rv = regra(uf, ano)
        row = [uf, ano, rv[0], rv[1], rv[2], "calculada_de_contagens" if ano <= 2005 else "publicada"]
        for tipo, rec in MET:
            for rede in SUF:
                row.append(f2(val("edu_%s_%s__%s" % (tipo, rec, rede), uf, ano)))
        for rec in ("ef_ai", "ef_af", "ef_total"):
            row.append(f2(val("edu_reprov_sobre_aprov_mais_reprov_%s__estadual" % rec, uf, ano)))
        row.append(CAL[uf]["dif_aband_pp"] if (ano <= 2005 and uf in CAL) else "")
        row.append("af_2000_suspeito: colunas ef_af (reprovacao, abandono, proxy) de 2000 fora do intervalo ai-total em 18 de 28 localidades; nao usar sem rever scripts/contagens.py" if ano == 2000 else "")
        linhas.append(row)
with open(os.path.join(RAIZ, "comparacao_regra.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(head)
    w.writerows(linhas)
GATES.append("OK  comparacao_regra.csv: %d linhas (UF x ano, 1996-2025 menos 2002, 2003 e 2006)" % len(linhas))

# ---------------------------------------------------------------- comparacao_regra.md
ANOS_T = [1996, 1997, 1998, 1999, 2000, 2001, 2004]
METR = [("reprovacao", "ef_total", "Reprovacao EF total"), ("reprovacao", "ef_ai", "Reprovacao EF anos iniciais"), ("reprovacao", "ef_af", "Reprovacao EF anos finais"),
        ("abandono", "ef_total", "Abandono EF total"), ("abandono", "ef_ai", "Abandono EF anos iniciais"), ("abandono", "ef_af", "Abandono EF anos finais"),
        ("proxy", "ef_total", "Proxy R/(A+R) EF total (nao depende do abandono)")]


def ind_de(tipo, rec):
    if tipo == "proxy":
        return "edu_reprov_sobre_aprov_mais_reprov_%s__estadual" % rec
    return "edu_%s_%s__estadual" % (tipo, rec)


def tabela(uf):
    out = []
    for tipo, rec, nome in METR:
        ind = ind_de(tipo, rec)
        out.append("**%s, rede estadual (%%)**\n" % nome)
        out.append("| ano | %s | grupo sem a regra (media simples) | n UFs | %s menos grupo | variacao de %s desde 1997 | variacao do grupo desde 1997 |" % (uf, uf, uf))
        out.append("|---|---|---|---|---|---|---|")
        b = val(ind, uf, 1997) if val(ind, uf, 1997) is not None else None
        gb = media_ctrl(ind, 1997)[0]
        for a in ANOS_T:
            v = val(ind, uf, a)
            g, n = media_ctrl(ind, a)
            if rec == "ef_af" and a == 2000:
                out.append("| 2000 | suspeito (%s) | suspeito (%s) | %d | - | - | - |" % (f2(v), f2(g), n))
                continue
            if v is None or g is None:
                out.append("| %d | sem dado | sem dado | 0 | - | - | - |" % a)
                continue
            dv = "%+.2f" % (v - b) if b is not None else "-"
            dg = "%+.2f" % (g - gb) if gb is not None else "-"
            out.append("| %d | %.2f | %.2f | %d | %+.2f | %s | %s |" % (a, v, g, n, v - g, dv, dg))
        out.append("")
    return "\n".join(out)


SAEB = {}
for r in csv.DictReader(open(os.path.join(RAIZ, "..", "dominios-1", "series", "edu.csv"), encoding="utf-8")):
    if r["indicador"].startswith("edu_saeb") and 1995 <= int(r["ano"]) <= 2005 and "PressKit" in r["fonte"]:
        SAEB.setdefault(r["indicador"], {})[int(r["ano"])] = r["valor"]
saeb_md = ["| ano | LP 4a serie | Mat 4a serie | LP 8a serie | Mat 8a serie |", "|---|---|---|---|---|"]
for a in (1995, 1997, 1999, 2001, 2003, 2005):
    g = lambda k: SAEB.get(k, {}).get(a, "-")  # noqa: E731
    saeb_md.append("| %d | %s | %s | %s | %s |" % (a, g("edu_saeb_LP_EF_5ano_4serie"), g("edu_saeb_MT_EF_5ano_4serie"), g("edu_saeb_LP_EF_9ano_8serie"), g("edu_saeb_MT_EF_9ano_8serie")))

md = []
md.append("# Reprovacao e abandono no EF antes e depois da regra de ciclos/progressao continuada, por UF\n")
md.append("Gerado por `scripts/gerar_quebras_comparacao.py` a partir de `series/edu_rendimento.csv`. Dados completos por UF e ano: `comparacao_regra.csv` (%d linhas). Normas: `quebras.csv`.\n" % len(linhas))
md.append("> [!IMPORTANT]\n> Descritivo. O grupo sem a regra e definido por UMA medida do INEP em 1999 (tabelas_ciclos_2000.xls) e estendido a 1996-2001 sem prova direta. Os anos de 1996 a 2005 sao taxas CALCULADAS das contagens da Sinopse (nao as publicadas); o abandono calculado erra ate %s p.p. numa UF (MT) e fica dentro de 0,15 p.p. em 18 de 28 localidades (`series/calibracao_2005.csv`); a reprovacao e o proxy R/(A+R) erram menos. 2002, 2003 e 2006 nao existem na serie. Os valores de 2000 do recorte anos finais (5a-8a serie) estao marcados 'suspeito': a reprovacao de 2000 nessa coluna fica fora do intervalo entre anos iniciais e total em 18 de 28 localidades (defeito provavel de extracao da Sinopse 2001, a rever; as linhas de EF total e anos iniciais de 2000 passam). A queda de 1996 para 1997 (SP, MG e o grupo) ocorre ANTES da Res. SE 4/98 e entre arquivos de origem diferentes (1996 vem de censo_1997.zip; 1997, do PDF do Censo 1998): nao e separavel aqui. 2007 em diante e taxa publicada (mudanca de metodo entre 2005 e 2007: ver `quebras.csv`).\n" % max(abs(float(r["dif_aband_pp"])) for r in CAL.values()))
md.append("## Como `regra_vigente` foi decidida\n")
md.append("- `sim`/`nao`/`parcial` vem das normas de `quebras.csv` (SP, MG, MS, CE, RJ, PR, MT) e da tabela INEP de 1999; `nd` = nem norma nem medida localizadas naquele ano.")
md.append("- Grupo sem a regra (%d UFs): %s. Criterio: matriculas em escolas so com ciclos + escolas com mais de uma forma <= 10%% em 1999, todas as redes, e nenhuma norma localizada. Barretto e Mitrulis (2001) confirmam pelo Censo 2000 que PA, PE, AL, RS e GO tinham ate 5%% das escolas estaduais com ciclos e PB e SE nenhuma; AC, RR e MA nenhuma.\n" % (len(CTRL), ", ".join(CTRL)))
md.append("## Tabela INEP: matriculas do EF por forma de organizacao, 1999 (`series/ciclos_1999_inep.csv`)\n")
md.append("| UF | % seriado | % so ciclos | % mais de uma forma | grupo sem a regra |")
md.append("|---|---|---|---|---|")
for u, d in sorted(CICLOS99.items(), key=lambda x: -x[1]["ciclos_pct"]):
    md.append("| %s | %.1f | %.1f | %.1f | %s |" % (u, d["seriado_pct"], d["ciclos_pct"], d["mista_pct"], "sim" if u in CTRL else "nao"))
md.append("\n## SP contra o grupo sem a regra (regra: Res. SE 4/98, 1998; Deliberacao CEE 09/97)\n")
md.append(tabela("SP"))
md.append("## MG contra o grupo sem a regra (CBA ate 1997; Res. 8086/97 obrigatoria em 1998; Res. 12/99 delega a escola; Res. 006/2000 tres ciclos)\n")
md.append(tabela("MG"))
md.append("## Saeb\n")
md.append("Saeb por UF 1995-2005 nao foi obtido em arquivo pequeno do INEP (o relatorio 'Medias de desempenho do SAEB/2005 em perspectiva comparada' so achado em copia atras de login do e-Disciplinas USP; a tese da UFMG baixada nao traz tabela por UF). Abaixo, so Brasil, de `../dominios-1/series/edu.csv` (INEP Press Kit Saeb 2019, escala 0-500; a abrangencia varia por edicao): nao serve para comparar SP com outras UFs.\n")
md.extend(saeb_md)
md.append("")
open(os.path.join(RAIZ, "comparacao_regra.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
GATES.append("OK  comparacao_regra.md escrito (SP e MG x grupo sem a regra, anos %s)" % ANOS_T)
open(os.path.join(SER, "gates_quebras.txt"), "w").write("\n".join(GATES) + "\n")
print("\n".join(GATES[-6:]))
print("quebras:", len(Q), "linhas; comparacao:", len(linhas))
