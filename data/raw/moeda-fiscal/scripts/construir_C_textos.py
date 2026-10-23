"""Bloco C: regras_emendas.csv, rp_identificadores.csv, eventos_fiscais.csv, marcos.csv.
Toda data e todo trecho saem do TEXTO baixado (bruto/ em moeda-fiscal, ou bruto/ldo em mecanismos-contabil, ja na cadeia
daquela pasta): a data vem do titulo do ato e o trecho e substring exata (espacos colapsados). Sem rede.
Rodar: python3 -I construir_C_textos.py"""
import csv, json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import DADOS, PASTA, html_texto, manifest

MES = {m: i for i, m in enumerate(["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"], 1)}
MAN = {"moeda-fiscal": manifest()}
_cc = {}
for l in (DADOS / "mecanismos-contabil/manifest.jsonl").read_text(encoding="utf-8").splitlines():
    r = json.loads(l); _cc[r["arquivo"]] = (r["timestamp_utc"], r["sha256"], r["url"])
MAN["mecanismos-contabil"] = _cc
FALHAS = []


def base(pasta):
    return PASTA if pasta == "moeda-fiscal" else DADOS / pasta


def flat(pasta, arq):
    p = base(pasta) / arq
    if arq.endswith(".pdf"):
        t = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
    else:
        b = p.read_bytes()
        try:
            t = b.decode("utf8")
        except UnicodeDecodeError:
            t = b.decode("cp1252", errors="replace")
        import html
        t = re.sub(r"(?s)<(script|style|noscript).*?</\1>", "", t)
        t = re.sub(r"(?i)</(p|div|li|h\d|tr|br)>|<br\s*/?>", "\n", t)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t.replace("\xa0", " "))


def data_titulo(t):
    m = re.search(r"(?:DE|,)\s+(\d{1,2})º?\s+DE\s+([A-ZÇ]+)\s+DE\s+(\d{4})", t[:700], re.I)
    if not m:
        return ""
    return f"{int(m.group(3)):04d}-{MES[m.group(2).upper()]:02d}-{int(m.group(1)):02d}"


def data_assin(t):
    m = re.search(r"(?:Brasília|Senado Federal),\s+(?:em\s+)?(\d{1,2})º?\s+de\s+([a-zç]+)\s+de\s+(\d{4})", t, re.I)
    return f"{int(m.group(3)):04d}-{MES[m.group(2).upper()]:02d}-{int(m.group(1)):02d}" if m else ""


def trecho(t, pat, n=420, antes=0):
    m = re.search(pat, t)
    if not m:
        return None
    i = max(0, m.start() - antes)
    s = t[i:i + n]
    return s + (" [...]" if i + n < len(t) else "")


def proc(pasta, arq):
    ts, sh, url = MAN[pasta].get(arq, ("", "", ""))
    return url, sh, ts


def linha(pasta, arq, pat, n=420, antes=0, **kw):
    t = flat(pasta, arq)
    url, sh, ts = proc(pasta, arq)
    tr = trecho(t, pat, n, antes)
    if tr is None:
        FALHAS.append((arq, pat))
        tr = "NAO LOCALIZADO NO TEXTO COM O PADRAO: " + pat
    return dict(data=kw.pop("data", None) or data_titulo(t), url=url, arquivo=f"{pasta}/{arq}", sha256=sh, trecho=tr, **kw)


def gravar(nome, cols, linhas):
    p = PASTA / nome
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for l in linhas:
            w.writerow({c: l.get(c, "") for c in cols})


# ------------------------------------------------------------------ regras_emendas.csv
P = "moeda-fiscal"
R = []
def r(id_, arq, aspecto, mudou, pat, n=420, vig=None, **kw):
    l = linha(P, arq, pat, n, id=id_, instrumento=kw.pop("instrumento"), aspecto=aspecto, o_que_mudou=mudou, **kw)
    t = flat(P, arq)
    l["vigencia_no_texto"] = trecho(t, vig, 260) if vig else ""
    R.append(l)


r("EC86-a", "bruto/planalto/ec86-2015.html", "emendas individuais: limite de aprovacao", "Fixa em 1,2% da receita corrente liquida prevista no projeto o limite das emendas individuais, metade para saude (art. 166, par. 9)",
  r"§ 9º As emendas individuais ao projeto de lei orçamentária serão aprovadas no limite de 1,2%", 380, instrumento="Emenda Constitucional 86/2015", vig=r"Esta Emenda Constitucional entra em vigor")
r("EC86-b", "bruto/planalto/ec86-2015.html", "emendas individuais: execucao obrigatoria", "Torna obrigatoria a execucao orcamentaria e financeira das programacoes do par. 9, em montante de 1,2% da RCL realizada no exercicio anterior (art. 166, par. 11)",
  r"§ 11\. É obrigatória a execução orçamentária e financeira das programações a que se refere o § 9º", 400, instrumento="Emenda Constitucional 86/2015")
r("EC100-a", "bruto/planalto/ec100-2019.html", "emendas de bancada: execucao obrigatoria", "Estende a garantia de execucao as emendas de bancada estadual ou do DF, ate 1% da RCL realizada no exercicio anterior (art. 166, par. 12)",
  r"§ 12\. A garantia de execução de que trata o § 11", 330, instrumento="Emenda Constitucional 100/2019", vig=r"Art\. 4º Esta Emenda Constitucional entra em vigor")
r("EC100-b", "bruto/planalto/ec100-2019.html", "emendas de bancada: percentual de transicao", "Fixa em 0,8% o montante do par. 12 no exercicio subsequente ao da promulgacao (art. 2 da emenda)",
  r"Art\. 2º O montante previsto no § 12 do art\. 166", 250, instrumento="Emenda Constitucional 100/2019")
r("EC105-a", "bruto/planalto/ec105-2019.html", "emendas individuais: transferencia especial e com finalidade definida", "Acrescenta o art. 166-A: emendas individuais impositivas podem alocar recursos a Estados, DF e Municipios por transferencia especial ou transferencia com finalidade definida",
  r"Art\. 166-A\. As emendas individuais impositivas", 330, instrumento="Emenda Constitucional 105/2019", vig=r"Art\. 3º Esta Emenda Constitucional entra em vigor")
r("EC105-b", "bruto/planalto/ec105-2019.html", "emendas individuais: piso de transferencia no 1o semestre", "Assegura, no primeiro semestre do exercicio seguinte ao da publicacao, transferencia minima de 60% dos recursos do inciso I (transferencia especial)",
  r"Art\. 2º No primeiro semestre do exercício financeiro subsequente", 300, instrumento="Emenda Constitucional 105/2019")
r("EC126-a", "bruto/planalto/ec126-2022.html", "emendas individuais: limite de aprovacao", "Eleva para 2% da RCL do exercicio anterior ao do encaminhamento do projeto o limite das emendas individuais (art. 166, par. 9), metade para saude",
  r"§ 9º As emendas individuais ao projeto de lei orçamentária serão aprovadas no limite de 2%", 330, instrumento="Emenda Constitucional 126/2022", vig=r"Art\. 10\. Esta Emenda Constitucional entra em vigor")
r("EC126-b", "bruto/planalto/ec126-2022.html", "emendas individuais: divisao Deputados e Senadores", "Divide o limite de 2%: 1,55% para emendas de Deputados e 0,45% para as de Senadores (art. 166, par. 9-A)",
  r"§ 9º-A Do limite a que se refere o § 9º", 260, instrumento="Emenda Constitucional 126/2022")
r("EC126-c", "bruto/planalto/ec126-2022.html", "relator-geral: emendas para ampliacao de dotacoes em 2023", "Autoriza, para a lei orcamentaria de 2023, o relator-geral a apresentar emendas para ampliacao de dotacoes (art. 5)",
  r"Art\. 5º Para o exercício financeiro de 2023, a ampliação de dotações orçamentárias", 520, instrumento="Emenda Constitucional 126/2022")
r("LC210-a", "bruto/planalto/lc210-2024.html", "emendas de bancada: destinacao", "Bancada estadual somente destina recursos a projetos e acoes estruturantes da unidade da Federacao, vedada individualizacao por membro (art. 2); ate 8 emendas por bancada (art. 3)",
  r"Art\. 2º As emendas de bancada estadual de que trata o § 12", 330, instrumento="Lei Complementar 210/2024", vig=r"Art\. 16\. Esta Lei Complementar entra em vigor")
r("LC210-b", "bruto/planalto/lc210-2024.html", "emendas de comissao", "Somente comissoes permanentes da Camara, do Senado e do Congresso podem apresentar emendas de comissao (art. 4)",
  r"Art\. 4º Somente poderão apresentar emendas as comissões permanentes", 330, instrumento="Lei Complementar 210/2024")
r("LC210-c", "bruto/planalto/lc210-2024.html", "emendas individuais: transferencia especial", "Autor informa objeto e valor da transferencia especial ao indicar o ente beneficiado (art. 7); beneficiario indica conta no Transferegov.br (art. 8)",
  r"Art\. 7º No caso das emendas individuais impositivas previstas no inciso I", 330, instrumento="Lei Complementar 210/2024")
r("LC210-d", "bruto/planalto/lc210-2024.html", "limite de crescimento das emendas", "Estabelece limite de crescimento das emendas parlamentares aos projetos de lei orcamentaria anual em despesas primarias (art. 11)",
  r"Art\. 11\. Fica estabelecido limite de crescimento das emendas parlamentares", 420, instrumento="Lei Complementar 210/2024")
for x in R:
    x["data"] = x["data"]
gravar("regras_emendas.csv", ["id", "data", "instrumento", "aspecto", "o_que_mudou", "vigencia_no_texto", "url", "arquivo", "sha256", "trecho"], R)

# ------------------------------------------------------------------ rp_identificadores.csv (RP 6/7/8/9 nas LDOs baixadas)
RP = []
for arq, rot in (("bruto/planalto/ldo2020-lei13898.html", "LDO 2020"), ("bruto/planalto/ldo2021-lei14116.html", "LDO 2021"),
                 ("bruto/planalto/ldo2022-lei14194.html", "LDO 2022"), ("bruto/planalto/ldo2023-lei14436.html", "LDO 2023"),
                 ("bruto/planalto/ldo2024-lei14791.html", "LDO 2024"), ("bruto/planalto/ldo2025-lei15080.html", "LDO 2025")):
    if not (PASTA / arq).exists():
        RP.append(dict(data="", url="", arquivo=f"moeda-fiscal/{arq}", sha256="", trecho="ARQUIVO NAO BAIXADO", ato=rot)); continue
    t = flat(P, arq)
    l = linha(P, arq, r"individuais, de execução obrigatória", 1150, antes=120, ato=rot)
    RP.append(l)
gravar("rp_identificadores.csv", ["ato", "data", "url", "arquivo", "sha256", "trecho"], RP)

# ------------------------------------------------------------------ eventos_fiscais.csv
E = []
def ev(id_, arq, pasta, tipo, pat, n=420, antes=0, nota="", instr=None, data=None):
    t = flat(pasta, arq)
    titulo = re.search(r"(LEI COMPLEMENTAR|EMENDA CONSTITUCIONAL|LEI|DECRETO LEGISLATIVO|DECRETO)\s+N\s*[º°oO]*\s*([\d.]+)", t[:400], re.I)
    d = data or data_titulo(t)
    if instr:
        ins = instr
    elif titulo:
        ins = f"{titulo.group(1).title()} {titulo.group(2)}/{d[:4]}"
    else:
        ins = arq
    pats = pat if isinstance(pat, list) else [pat]
    escolhido = next((q for q in pats if re.search(q, t)), pats[0])
    l = linha(pasta, arq, escolhido, n, antes, id=id_, instrumento=ins, tipo_de_evento=tipo, nota=nota, data=d)
    E.append(l)


ev("LRF", "bruto/planalto/lc101-2000.html", P, "norma fiscal", r"Art\. 1 o Esta Lei Complementar estabelece normas de finanças públicas", 360)
ev("LRF-metas", "bruto/planalto/lc101-2000.html", P, "meta fiscal (previsao legal)", r"Anexo de Metas Fiscais, em que serão estabelecidas metas anuais", 330, 60, instr="Lei Complementar 101/2000, art. 4, par. 1")
ev("EC95", "bruto/planalto/ec95-2016.html", P, "teto de gastos", r"Art\. 106 \. Fica instituído o Novo Regime Fiscal", 330)
ev("EC95-107", "bruto/planalto/ec95-2016.html", P, "teto de gastos", r"Art\. 107 \. Ficam estabelecidos, para cada exercício, limites individualizados", 380, instr="Emenda Constitucional 95/2016, art. 107")
ev("EC103", "bruto/planalto/ec103-2019.html", P, "reforma da previdencia", r"Altera o sistema de previdência social e estabelece regras de transição", 200)
ev("LC200", "bruto/planalto/lc200-2023.html", P, "regime fiscal sustentavel", r"Institui regime fiscal sustentável", 420)
ev("LC200-lim", "bruto/planalto/lc200-2023.html", P, "limite de despesa primaria", r"Art\. 3º Com fundamento no inciso VIII do caput do art\. 163", 420, instr="Lei Complementar 200/2023, art. 3")
ev("DLG6", "bruto/planalto/dlg6-2020.html", P, "calamidade publica (art. 65 LRF)", r"Art\. 1º Fica reconhecida, exclusivamente para os fins do art\. 65", 420, nota="data da assinatura lida de 'Brasilia, ...' no fim do texto", instr="Decreto Legislativo 6/2020", data=data_assin(flat(P, "bruto/planalto/dlg6-2020.html")))
ev("EC126-meta", "bruto/planalto/ec126-2022.html", P, "excecao ao teto", r"Art\. 3º O limite estabelecido no inciso I do caput do art\. 107", 380, instr="Emenda Constitucional 126/2022, art. 3")

LDOS_P = [("bruto/planalto/ldo2018-lei13473.html", "LDO 2018"), ("bruto/planalto/ldo2019-lei13707.html", "LDO 2019"), ("bruto/planalto/ldo2020-lei13898.html", "LDO 2020"),
          ("bruto/planalto/ldo2021-lei14116.html", "LDO 2021"), ("bruto/planalto/ldo2022-lei14194.html", "LDO 2022"), ("bruto/planalto/ldo2023-lei14436.html", "LDO 2023"),
          ("bruto/planalto/ldo2024-lei14791.html", "LDO 2024"), ("bruto/planalto/ldo2025-lei15080.html", "LDO 2025")]
LDOS_C = [(f"bruto/ldo/{f}", rot) for f, rot in [
    ("lei9995-ldo2001.html", "LDO 2001"), ("lei10266-ldo2002.html", "LDO 2002"), ("lei10524-ldo2003.html", "LDO 2003"), ("lei10707-ldo2004.html", "LDO 2004"),
    ("lei10934-ldo2005.html", "LDO 2005"), ("lei11178-ldo2006.html", "LDO 2006"), ("lei11439-ldo2007.html", "LDO 2007"), ("lei11514-ldo2008.html", "LDO 2008"),
    ("lei11768-ldo2009.html", "LDO 2009"), ("lei12053-altera-ldo2009.html", "Altera LDO 2009"), ("lei12017-ldo2010.html", "LDO 2010"),
    ("lei12182-altera-ldo2010-pac.html", "Altera LDO 2010 (PAC)"), ("lei12309-ldo2011.html", "LDO 2011"), ("lei12377-altera-ldo2010-2011.html", "Altera LDO 2010/2011"),
    ("lei12465-ldo2012.html", "LDO 2012"), ("lei12708-ldo2013.html", "LDO 2013"), ("lei12919-ldo2014.html", "LDO 2014"), ("lei13053-altera-ldo2014.html", "Altera LDO 2014"),
    ("lei13080-ldo2015.html", "LDO 2015"), ("lei13199-altera-ldo2015.html", "Altera LDO 2015"), ("lei13242-ldo2016.html", "LDO 2016"),
    ("lei13291-altera-ldo2016.html", "Altera LDO 2016"), ("lei13408-ldo2017.html", "LDO 2017"), ("lei13480-altera-ldo2017.html", "Altera LDO 2017")]]
META_ANTES = r"(?:deverão|devem|deverá)[^.]{0,30}(?:levar em conta|ser compatíve\w+ com)[^.]{0,60}(?:obtenção|superávit|meta)"
META2 = r"O superávit a que se refere|A meta de resultado a que se refere"
META = r"(meta de (?:superávit|déficit|deficit|resultado)[^.]{0,40}primário|superávit primário (?:de|do|dos|para|equivalente)|meta[s]? de superávit)"
NOTA_LDO = ("primeira ocorrencia no texto; a pagina do Planalto pode trazer tambem redacao alterada por lei posterior (ver url). "
            "Meta e a do ato citado, nao o resultado apurado")
for arq, rot in LDOS_C:
    ev(rot.replace(" ", "-"), arq, "mecanismos-contabil", "meta de resultado primario (LDO)", [META_ANTES, META, META2], 700, 160, NOTA_LDO + "; texto lido do arquivo ja na cadeia de mecanismos-contabil")
for arq, rot in LDOS_P:
    if (PASTA / arq).exists():
        ev(rot.replace(" ", "-"), arq, P, "meta de resultado primario (LDO)", [META_ANTES, META, META2], 700, 160, NOTA_LDO)
gravar("eventos_fiscais.csv", ["id", "data", "instrumento", "tipo_de_evento", "url", "arquivo", "sha256", "trecho", "nota"], E)

# ------------------------------------------------------------------ marcos.csv (eixo do tempo)
MK = []
def mc(id_, evento, categoria, pasta, arq, pat, n=420, data=None, antes=0, nota="", fonte=""):
    t = flat(pasta, arq)
    l = linha(pasta, arq, pat, n, antes, id=id_, evento=evento, categoria=categoria, nota=nota, fonte_primaria=fonte)
    if data:
        l["data"] = data
    MK.append(l)


mc("REAL-URV", "Lei 8.880: institui a Unidade Real de Valor (URV); conversao da MP 482/1994", "plano (Real)", P, "bruto/planalto/lei8880-1994.html", r"Art\. 1º - Fica instituída a Unidade Real de Valor", 330, fonte="Presidencia da Republica, Planalto")
mc("REAL-1994-07-01", "O Real passa a ser a unidade do Sistema Monetario Nacional", "plano (Real)", P, "bruto/planalto/lei9069-1995.html", r"Art\. 1º A partir de 1º de julho de 1994", 300, data="1994-07-01",
   nota="data de efeito lida do texto; a Lei 9.069 (conversao da MPv 1.027/1995) e de 1995-06-29", fonte="Presidencia da Republica, Planalto")
mc("CAMBIO-1999-01-15", "Mercado cambial passa a operar em livre flutuacao (data de efeito segundo a Analise do Mercado de Cambio do BCB)", "crise (1999)", P, "bruto/marcos/bcb-cambio-1999-politica-cambial.html",
   r"A partir de 15 de Janeiro de 1999, o mercado cambial brasileiro passou", 330, data="1999-01-15", nota="o mesmo documento do BCB data o Comunicado 6.565 em 18.01.1999 (linha CAMBIO-1999-01-18); as duas datas sao registradas, nenhuma escolhida", fonte="Banco Central do Brasil")
mc("CAMBIO-1999-01-18", "Comunicado BCB 6.565: Banco Central deixa o mercado definir a taxa de cambio", "crise (1999)", P, "bruto/marcos/bcb-cambio-1999-politica-cambial.html",
   r"o Banco Central, através do Comunicado nº 6\.565, de 18\.01\.1999", 420, antes=170, data="1999-01-18", fonte="Banco Central do Brasil")
mc("METAS-INFLACAO-1999", "Decreto 3.088: sistematica de metas para a inflacao como diretriz do regime de politica monetaria", "regime monetario (1999)", P, "bruto/planalto/decreto3088-1999.html",
   r"Art\. 1 o Fica estabelecida, como diretriz para fixação do regime de política monetária", 300, data="1999-06-21", fonte="Presidencia da Republica, Planalto")
mc("CRISE-2002", "Relatorio de Inflacao de setembro/2002: nervosismo no mercado cambial na aproximacao das eleicoes", "crise (2002)", P, "bruto/marcos/bcb-ri-2002-09-cap1-atividade.pdf",
   r"A aproximação das eleições e a deterioração da conjuntura internacional", 420, data="2002-09", nota="data = mes do relatorio (precisao mensal); o relatorio descreve o periodo jun-ago/2002", fonte="Banco Central do Brasil")
mc("CRISE-2008-MP442", "Medida Provisoria 442: redesconto pelo BCB e Letra de Arrendamento Mercantil (resposta a crise financeira internacional)", "crise (2008)", P, "bruto/marcos/mpv442-2008.html",
   r"Dispõe sobre operações de redesconto pelo Banco Central do Brasil", 420, fonte="Presidencia da Republica, Planalto")
mc("CRISE-2008-RI", "Relatorio de Inflacao de dezembro/2008: agravamento da crise financeira internacional a partir de meados de setembro", "crise (2008)", P, "bruto/marcos/bcb-ri-2008-12-cap1-atividade.pdf",
   r"O agravamento, a partir de meados de setembro, da crise financeira internacional", 420, data="2008-09", nota="data = mes citado pelo BCB (meados de setembro); a fonte primaria da quebra do Lehman (8-K na SEC, 15/09/2008) devolveu HTTP 403 e nao esta na cadeia", fonte="Banco Central do Brasil")
mc("RECESSAO-2014-2016", "CODACE: pico em marco/2014 e vale em dezembro/2016 (recessao de 33 meses, abril/2014 a dezembro/2016)", "crise (2015)", P, "bruto/marcos/codace-comunicado-2020-06-29-copia-poder360.pdf",
   r"O CODACE também realizou a datação mensal da recessão de 2014-2016", 380, data="2014-04", nota="data = primeiro mes da recessao segundo o comunicado de 2020-06-29; a copia baixada e hospedada pelo Poder360, nao pela FGV (nao confirmada no site da FGV)", fonte="CODACE/FGV IBRE (copia do comunicado)")
mc("OMS-2020-03-11", "OMS: COVID-19 pode ser caracterizada como pandemia", "pandemia", P, "bruto/marcos/who-dg-remarks-2020-03-11.html",
   r"We have therefore made the assessment that COVID-19 can be characterized as a pandemic", 260, data="2020-03-11", fonte="Organizacao Mundial da Saude")
mc("DLG6-2020", "Decreto Legislativo 6: reconhece estado de calamidade publica (art. 65 da LRF)", "pandemia", P, "bruto/planalto/dlg6-2020.html",
   r"Art\. 1º Fica reconhecida, exclusivamente para os fins do art\. 65", 330, data=data_assin(flat(P, "bruto/planalto/dlg6-2020.html")), fonte="Congresso Nacional, Planalto")
mc("LC179-2021", "Lei Complementar 179: define os objetivos do Banco Central e dispoe sobre sua autonomia", "autonomia do Banco Central", P, "bruto/planalto/lc179-2021.html",
   r"Art\. 6º O Banco Central do Brasil é autarquia de natureza especial", 330, fonte="Presidencia da Republica, Planalto")
gravar("marcos.csv", ["id", "data", "evento", "categoria", "fonte_primaria", "url", "arquivo", "sha256", "trecho", "nota"], MK)
print("marcos:", len(MK))

print("regras:", len(R), "rp:", len(RP), "eventos:", len(E), "| falhas de ancora:", len(FALHAS))
for f in FALHAS:
    print("  FALHA", f)
