# Gera series/ministerios-1-de-janeiro.csv, series/ministerios-por-ano.csv e series/quebras.csv a partir do bruto (sem rede).
# Uso: python3 -I scripts/gerar.py       (derruba com erro se qualquer ancora da spec.py nao casar com o texto baixado)
import csv, glob, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import T, BASE, url_de, itens_lista, art_lista, nome_min, data_cab
import spec

SAIDA = os.path.join(BASE, "series")
VINTAGE = "baixado do Planalto em 2026-10-20 (UTC); norma vigente em 1/1 do ano da linha"

def chave(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()

def limpa_item(it):
    it = re.sub(r"\s*\((Incluíd[oa]|Redação|Revogad[oa]|Vide)[^)]*\)", "", it)
    it = re.sub(r"^a\s+(?=Controladoria)", "", it)
    return re.sub(r"[;.,\s]+$", "", it).strip()

def lista_auto(arq, ini, fim):
    seg = art_lista(arq, ini, fim)
    itens, nums = itens_lista(seg)
    vistos, out = set(), []
    for it in itens:
        it = limpa_item(it)
        if it and it not in vistos:
            vistos.add(it); out.append(it)
    return seg, out, lib.numeracao_ok(nums)

# ---- cadeia de MPs (1995-2001): lista do art. 13 em cada reedicao baixada --------------------------------------------
def cadeia():
    rows = []
    for f in sorted(glob.glob(os.path.join(BASE, "bruto", "mpv-*.html"))):
        arq = "bruto/" + os.path.basename(f)
        t = T(arq); d = data_cab(arq)
        if not d or not re.search(spec.RI, t): continue
        seg = art_lista(arq, spec.RI, spec.FIM13)
        itens, nums = itens_lista(seg)
        rows.append((d, arq, [limpa_item(x) for x in itens], lib.numeracao_ok(nums)))
    rows.sort()
    return rows
CADEIA = cadeia()

def transicoes(d0, d1):
    """texto sobre as reedicoes baixadas com data em (d0, d1]: mudancas de lista de uma para a seguinte"""
    ant = None
    for d, arq, its, ok in CADEIA:
        if d <= d0: ant = set(its)
    sel = [(d, arq, its, ok) for d, arq, its, ok in CADEIA if d0 < d <= d1]
    if not sel: return "nenhuma versão da série baixada no intervalo"
    partes, n_dif = [], 0
    for d, arq, its, ok in sel:
        s = set(its)
        if ant is not None and s != ant:
            n_dif += 1
            partes.append("%s (%s): saiu %s; entrou %s" % (os.path.basename(arq).replace("mpv-", "MP ").replace(".html", ""), d, sorted(ant - s), sorted(s - ant)))
        ant = s
    base = "%d versões baixadas no intervalo (%s a %s), %d com mudança de lista" % (len(sel), sel[0][0], sel[-1][0], n_dif)
    return base + ("; " + "; ".join(partes) if partes else "; lista idêntica em todas")

def varredura_anotacoes(arq, ini, fim):
    """atos citados nas anotacoes 'Redacao dada / Incluido / Revogado' dentro do trecho do artigo"""
    seg = art_lista(arq, ini, fim)
    return sorted(set(re.findall(r"(?:Redação dada|Incluíd[oa]|Revogad[oa])\s+pel[ao]s?\s+(?:Lei|Medida Provisória|Lei Complementar)\s*(?:nº|n°|no)?\s*[\d\.]+,?\s*de\s*\d{4}", seg)))

def base_art25():
    """redacao original do art. 25 da Lei 10.683: no compilado, a 1a ocorrencia de cada numeral e o texto original (as demais sao redacoes posteriores)"""
    seg = art_lista("bruto/l10683-original.html", r"Art\. 25\. Os Ministérios são os seguintes:", r"Art\. 26\.")
    pad = re.compile(r"(?:(?<=\s)|^)([IVXL]{1,8})\s*[-–—]\s*")
    ms = list(pad.finditer(seg)); vistos, partes = set(), []
    for k, m in enumerate(ms):
        if m.group(1) in vistos or m.group(1) not in lib.ROM[:23]: continue
        vistos.add(m.group(1))
        fim = ms[k+1].start() if k+1 < len(ms) else len(seg)
        partes.append("%s - %s" % (m.group(1), seg[m.end():fim].strip()))
    return " ".join(partes)

# ---- constroi as linhas ----------------------------------------------------------------------------------------------
EXPECT_N = {1995:20,1996:20,1997:20,1998:20,1999:20,2000:20,2001:20,2002:20,2003:23,2004:23,2005:23,2006:23,2007:23,2008:23,2009:23,2010:24,2011:24,
            2012:24,2013:24,2014:24,2015:24,2016:23,2017:21,2018:22,2019:16,2020:16,2021:17,2022:18,2023:31,2024:32,2025:32,2026:32}
linhas = []
prev_nomes = None
for e in spec.SPEC:
    ano = e["ano"]
    # --- lista de Ministerios
    if e["lista"][0] == "auto":
        _, arq_l, ini, fim = e["lista"]
        seg, itens, num_ok = lista_auto(arq_l, ini, fim)
        trecho = seg   # artigo inteiro, sem teto
        nomes = [nome_min(x) for x in itens]
        met_lista = "lida no próprio artigo (%s)%s" % (arq_l, "" if num_ok else "; ATENÇÃO: numeração romana com erro tipográfico no original, contados os itens, não os numerais")
    else:
        _, nomes_man, arqs_chk, arq_t, rx_t, n_t = e["lista"]
        for nm in nomes_man:
            if not any(nm.replace("Ministério ", "", 1) in T(a) for a in arqs_chk):
                raise SystemExit("ano %d: ministério %r não achado em %s" % (ano, nm, arqs_chk))
        m = re.search(lib.R(rx_t), T(arq_t))
        if not m: raise SystemExit("ano %d: trecho %r não achado em %s" % (ano, rx_t, arq_t))
        trecho = T(arq_t)[m.start(): m.start() + max(n_t, m.end() - m.start())]
        if ano <= 2015:
            trecho = ("[texto original, 1ª ocorrência de cada inciso no compilado da Lei 10.683, art. 25: " + base_art25() + "]" +
                      ("" if arq_t == "bruto/l10683-original.html" else " || [" + os.path.basename(arq_t) + ": " + trecho + "]"))
        nomes = [nome_min(x) for x in nomes_man]
        met_lista = "reconstruída da redação original + atos que alteraram incisos (cada nome conferido nos textos: %s)" % ", ".join(os.path.basename(a) for a in arqs_chk)
    assert len(set(nomes)) == len(nomes), (ano, "duplicados")
    if len(nomes) != EXPECT_N[ano]:
        raise SystemExit("ano %d: %d ministérios, esperado %d: %s" % (ano, len(nomes), EXPECT_N[ano], nomes))
    # --- status
    status = {"A": [], "B": [], "C": []}
    descr_status = []
    for arq_s, rx, base, itens in e["status"]:
        m = re.search(lib.R(rx), T(arq_s))
        if not m: raise SystemExit("ano %d: âncora de status %r não achada em %s" % (ano, rx[:80], arq_s))
        txt_m = m.group(0)
        for tipo, nome, ch in itens:
            if ch not in txt_m: raise SystemExit("ano %d: chave %r não está no trecho da âncora (%s)" % (ano, ch, nome))
            if nome not in [x[0] for x in status[tipo]]:
                status[tipo].append((nome, base, arq_s))
    # evita contar o mesmo orgao em duas classes
    vistos = set()
    for tipo in "ABC":
        novos = []
        for nome, base, arq_s in status[tipo]:
            if nome in vistos: continue
            vistos.add(nome); novos.append((nome, base, arq_s))
        status[tipo] = novos
    nA, nB, nC = (len(status[k]) for k in "ABC")
    n = len(nomes)
    total = n + nA + nB + nC
    # --- textos
    d0 = "%d-01-01" % (ano - 1); d1 = "%d-01-01" % ano
    atos = e["atos"]
    if atos == "AUTO":
        atos = "Reedições de MP: " + transicoes(d0, d1)
    elif ano <= 2002:
        pass
    if prev_nomes is not None:
        s0, s1 = set(prev_nomes), set(nomes)
        atos += " | Diferença de lista entre 1/1/%d e 1/1/%d (comparação literal dos nomes): saíram %s; entraram %s." % (ano - 1, ano, sorted(s0 - s1), sorted(s1 - s0))
    prev_nomes = nomes
    dou = re.search(r"D\.?\s?O\.?\s?U\.?\s+de\s+[\dº°\.]+(?:\s*[-(]?\s*Edi[cç][aã]o [Ee]xtra\)?)?", T(e["arq"]))
    dou_txt = ("rodapé do Planalto: '%s'" % dou.group(0).strip()) if dou else "data do DOU não informada no arquivo"
    verif = ("nao_verificado (parcial). " if e["nv"] else "VERIFICADO NO TEXTO. ") + "Lista: " + met_lista + ". " + e["verif"] + " " + dou_txt + "."
    if e["nv"]: verif += " Não verificado: " + e["nv"]
    lst_st = []   # um item por orgao, rotulo [A|B|C]; a base normativa aparece uma vez por grupo, entre {}
    for tipo in "ABC":
        por_base = {}
        for nome, base, arq_s in status[tipo]:
            por_base.setdefault(base, []).append(nome)
        for base, ns in por_base.items():
            lst_st.append("[%s] %s {%s}" % (tipo, ", ".join(ns), base))
    linhas.append(dict(ano=ano, norma=e["norma"], data=e["data"], url=url_de(e["arq"]) or "", nomes=sorted(nomes, key=chave), n=n, nA=nA, nB=nB, nC=nC,
                       total=total, status=lst_st, trecho=trecho, atos=atos, verif=verif, arq=e["arq"]))

# ---- confere que a norma escolhida e a ultima da cadeia com data <= 1/1 (1996-2002) ------------------------------------
ESPERADO_CADEIA = {1996: "bruto/mpv-1226.html", 1997: "bruto/mpv-1549.html", 1998: "bruto/mpv-1549-38.html", 1999: "bruto/mpv-1795.html",
                   2000: "bruto/mpv-1999-13.html", 2001: "bruto/mpv-2049-26.html", 2002: "bruto/mpv-2216-37.html"}
for ano, arq in ESPERADO_CADEIA.items():
    ult = [x for x in CADEIA if x[0] <= "%d-01-01" % ano][-1]
    if ult[1] != arq: raise SystemExit("cadeia: última versão <= 1/1/%d é %s, spec usa %s" % (ano, ult[1], arq))

os.makedirs(SAIDA, exist_ok=True)
# ---- (b) ministerios-por-ano.csv ----------------------------------------------------------------------------------------
with open(os.path.join(SAIDA, "ministerios-por-ano.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ano", "norma_vigente_em_1_jan", "data_da_norma", "n_ministerios", "n_ministerios_mais_status", "lista_ministerios", "lista_status",
                "url_norma", "trecho_literal_do_artigo_da_lista", "atos_posteriores_que_mudaram_a_lista_no_ano_anterior", "verificacao"])
    for r in linhas:
        w.writerow([r["ano"], r["norma"], r["data"], r["n"], r["total"], "; ".join(r["nomes"]), "; ".join(r["status"]) or "(nenhum)", r["url"], r["trecho"], r["atos"], r["verif"]])

# ---- (a) ministerios-1-de-janeiro.csv ------------------------------------------------------------------------------------
DEF = {
 "n_ministerios": "Itens que a norma vigente em 1/1 chama de Ministérios (artigo 'Os Ministérios são os seguintes')",
 "n_ministerios_mais_status": "n_ministerios + órgãos fora da lista cujo titular a norma declara Ministro de Estado (A), Ministro Extraordinário (B) ou com prerrogativas equivalentes às de Ministro de Estado (C)",
 "n_status_ministro_de_estado_declarado": "Classe A: órgãos/cargos fora da lista de Ministérios que a norma declara Ministros de Estado (par. único ou cargo 'Ministro de Estado Chefe da ...')",
 "n_status_ministro_extraordinario": "Classe B: cargos/gabinetes de 'Ministro de Estado Extraordinário' (Esportes, Política Fundiária, Projetos Especiais, Segurança Alimentar), que a norma não lista como Ministério",
 "n_status_prerrogativas_equivalentes": "Classe C: cargos cujo titular tem 'prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado'",
}
CAMPO = {"n_ministerios": "n", "n_ministerios_mais_status": "total", "n_status_ministro_de_estado_declarado": "nA", "n_status_ministro_extraordinario": "nB", "n_status_prerrogativas_equivalentes": "nC"}
with open(os.path.join(SAIDA, "ministerios-1-de-janeiro.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"])
    for r in linhas:
        nota = "Ministérios (ordem alfabética): " + "; ".join(r["nomes"]) + ". || Órgãos com status (fora da lista, classes A/B/C): " + ("; ".join(r["status"]) if r["status"] else "nenhum") + \
               ". || Verificação: " + r["verif"].split(".")[0] + "."
        for ind in DEF:
            w.writerow([ind, r["url"], "%s — data da norma: %s — %s" % (r["norma"], r["data"], DEF[ind]), r["ano"], r[CAMPO[ind]], "unidades", nota, VINTAGE])


# ---- (c) quebras.csv -------------------------------------------------------------------------------------------------------
L = {r["ano"]: r for r in linhas}
def cad_n(arq):
    for d, a, its, ok in CADEIA:
        if a == arq: return len(its)
def ef(a, b):
    x, y = L[a], L[b]
    return ("n_ministerios %d→%d; n_ministerios_mais_status %d→%d (A %d→%d, B %d→%d, C %d→%d), entre as fotos de 1/1/%d e 1/1/%d"
            % (x["n"], y["n"], x["total"], y["total"], x["nA"], y["nA"], x["nB"], y["nB"], x["nC"], y["nC"], a, b))
COMO_FOTO = "diferença entre as duas fotos de 1 de janeiro vizinhas desta pasta (series/ministerios-por-ano.csv); inclui outros atos do mesmo intervalo, listados na coluna de atos"
COMO_CAD = "contagem de itens do art. 13 nas duas versões consecutivas da MP (scripts/gerar.py, cadeia de reedições)"
COMO_DIR = "leitura e comparação literal dos textos das duas normas"
SEM_RAZAO = "não declarada no texto da norma baixada (exposição de motivos não lida)"
SEM_APRIM = "não declarada no texto da norma"
Q = []
def q(data, antigo, novo, trechos, direcao, efeito, como_med, razao=SEM_RAZAO, aprim=SEM_APRIM, ind="n_ministerios; n_ministerios_mais_status", como_dir=COMO_DIR):
    Q.append(dict(ind=ind, data=data, antigo=antigo, novo=novo, trechos=trechos, direcao=direcao, como_dir=como_dir, efeito=efeito, como_med=como_med, razao=razao, aprim=aprim))
q("1996-05-10", "Ministério da Agricultura, do Abastecimento e da Reforma Agrária", "Ministério da Agricultura e do Abastecimento (sem 'Reforma Agrária')",
  [("bruto/mpv-1384.html", r"III - da Agricultura, do Abastecimento e da Reforma Agrária", 70), ("bruto/mpv-1450.html", r"III - da Agricultura e do Abastecimento", 50)],
  "neutro na contagem; muda o escopo da pasta (a norma baixada não diz para onde foi a reforma agrária)", "n_ministerios %d→%d" % (cad_n("bruto/mpv-1384.html"), cad_n("bruto/mpv-1450.html")), COMO_CAD)
q("1999-01-01", "20 Ministérios da série MP 813/1.549 (inclui Administração Federal e Reforma do Estado; Planejamento e Orçamento; Educação e do Desporto; Indústria, do Comércio e do Turismo; Trabalho; Meio Ambiente, dos Recursos Hídricos e da Amazônia Legal)",
  "20 Ministérios da MP 1.795 (extingue o da Administração Federal e Reforma do Estado; cria Orçamento e Gestão, Esporte e Turismo, Desenvolvimento, Indústria e Comércio; Educação; Trabalho e Emprego; Meio Ambiente)",
  [("bruto/mpv-1795.html", r"Art\. 13\. Os Ministérios são os seguintes:.{0,520}XX - dos Transportes\.", 600)],
  "neutro no total; troca da composição de 6 pastas (nomes e competências deixam de ser comparáveis)", "n_ministerios %d→%d; saíram 6 nomes e entraram 6 (ver atos da linha de 1999)" % (cad_n("bruto/mpv-1651-43.html"), cad_n("bruto/mpv-1795.html")), COMO_CAD)
q("1999-06-10", "Ministérios da Aeronáutica, do Exército e da Marinha (3) e Estado-Maior das Forças Armadas (Ministro de Estado pelo par. único)", "Ministério da Defesa (1); par. único passa a citar o Chefe da Casa Militar no lugar do EMFA",
  [("bruto/mpv-1799-6.html", r"V - da Defesa", 40), ("bruto/mpv-1799-6.html", r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil e o Chefe da Casa Militar da Presidência da República", 200)],
  "reduz n_ministerios em 2 (3 pastas militares viram 1); em A, o EMFA sai e a Casa Militar entra (efeito líquido 0)", "n_ministerios %d→%d; A: EMFA sai, Casa Militar entra (2→2)" % (cad_n("bruto/mpv-1799-4.html"), cad_n("bruto/mpv-1799-6.html")), COMO_CAD)
q("1999-07-29", "18 Ministérios (MP 1.799-6/1.911-7)", "19 Ministérios: cria Integração Nacional; renomeia Desenvolvimento, Indústria e Comércio Exterior e Planejamento, Orçamento e Gestão",
  [("bruto/mpv-1911-8.html", r"Art\. 13\. Os Ministérios são os seguintes:.{0,620}dos Transportes\.", 620)],
  "aumenta n_ministerios em 1; par. único passa a incluir a Secretaria-Geral (A +1)", "n_ministerios %d→%d" % (cad_n("bruto/mpv-1911-7.html"), cad_n("bruto/mpv-1911-8.html")), COMO_CAD)
q("1999-12-14", "Gabinete do Ministro de Estado Extraordinário de Política Fundiária (classe B, fora da lista)", "Ministério da Política Fundiária e do Desenvolvimento Agrário (item XV da lista de Ministérios; renomeado 'do Desenvolvimento Agrário' em 13/1/2000)",
  [("bruto/mpv-1999-13.html", r"XV - da Política Fundiária e do Desenvolvimento Agrário", 70), ("bruto/mpv-1999-13.html", r"XII - o Gabinete do Ministro de Estado Extraordinário de Política Fundiária em Ministério da Política Fundiária e do Desenvolvimento Agrário", 160)],
  "aumenta n_ministerios em 1 e reduz B em 1 (soma n_ministerios_mais_status inalterada)", "n_ministerios %d→%d; B 1→0" % (cad_n("bruto/mpv-1911-11.html"), cad_n("bruto/mpv-1999-13.html")), COMO_CAD)
q("2001-12-10", "Ministro de Estado Chefe da Secretaria de Comunicação de Governo (A) citado no art. 13, § 1º da MP 2.216-37", "cargo extinto por decreto; a Secretaria vira Secretaria de Estado de Comunicação de Governo",
  [("bruto/d4046.html", r"Fica extinto o cargo de Ministro de Estado Chefe da Secretaria de Comunicação de Governo da Presidência da República", 140)],
  "reduz A em 1 sem alterar o texto da lei (o texto compilado continua citando o cargo, com remissão ao decreto)", "A 6→5 (texto do § 1º lista 6 órgãos; 5 com cargo vigente)", "leitura do decreto contra o § 1º da MP 2.216-37", ind="n_ministerios_mais_status; n_status_ministro_de_estado_declarado")
q("2003-01-01", "20 Ministérios (Lei 9.649/1998 na redação da MP 2.216-37)", "23 Ministérios (MP 103; revoga a Lei 9.649); Ministro Extraordinário de Segurança Alimentar (B) e 4 Secretários Especiais com equivalência (C)",
  [("bruto/mpv-0103.html", r"Art\. 25\. Os Ministérios são os seguintes:.{0,640}XXIII - do Turismo\.", 700)],
  "aumenta n_ministerios em 3 e muda a composição (cria Cidades, Esporte, Turismo, Assistência e Promoção Social; extingue Previdência e Assistência Social, Indústria... conforme diferença de lista)", ef(2002, 2003), COMO_FOTO)
q("2004-01-23", "Ministério da Assistência Social + Ministro Extraordinário de Segurança Alimentar e Combate à Fome (B)", "Ministério do Desenvolvimento Social e Combate à Fome; cargo e gabinete Extraordinário extintos; Secretaria de Coordenação Política entra em A",
  [("bruto/mpv-0163.html", r"II - do Desenvolvimento Social e Combate à Fome", 60), ("bruto/l10869.html", r"Art\. 10\. Ficam extintos os cargos de Ministro de Estado Extraordinário de Segurança Alimentar e Combate à Fome", 130)],
  "neutro em n_ministerios (renomeação/fusão); B −1, A +1", ef(2004, 2005), COMO_FOTO + " (2005 inclui também a Lei 11.036, BC)")
q("2004-08-13", "Presidente do Banco Central: cargo de Natureza Especial, fora do par. único", "cargo transformado em cargo de Ministro de Estado (MP 207, Lei 11.036 de 22/12/2004)",
  [("bruto/l11036.html", r"Art\. 2º O cargo de Natureza Especial de Presidente do Banco Central do Brasil fica transformado em cargo de Ministro de Estado", 140)],
  "aumenta A em 1 (n_ministerios inalterado)", "A +1 (Presidente do Banco Central), vigente até a LC 179/2021", "leitura do art. 2º da Lei 11.036 e do par. único", ind="n_ministerios_mais_status; n_status_ministro_de_estado_declarado")
q("2005-07-21", "par. único do art. 25 cita a Secretaria de Comunicação de Governo e Gestão Estratégica e a de Coordenação Política; CDES com Secretário Especial (C)", "MP 259 (Lei 11.204): cita a Secretaria de Relações Institucionais; extingue o Ministro Chefe da SECOM e o Secretário Especial do CDES",
  [("bruto/l11204.html", r"Art\. 4º Ficam extintos: I - o cargo de Ministro de Estado Chefe da Secretaria de Comunicação de Governo e Gestão Estratégica", 200)],
  "reduz A em 1 (SECOM) e C em 1 (CDES)", ef(2005, 2006), COMO_FOTO)
q("2007-03-28", "Comunicação social dentro da Secretaria-Geral (sem Ministro Chefe)", "Secretaria de Comunicação Social criada; titular volta ao par. único (MP 360; Lei 11.497 de 28/6/2007)",
  [("bruto/l11497.html", r"Art\. 2o Fica criada a Secretaria de Comunicação Social da Presidência da República", 90)],
  "aumenta A em 1", ef(2007, 2008) + " (inclui MP 369, Portos, em C)", COMO_FOTO, ind="n_ministerios_mais_status; n_status_ministro_de_estado_declarado")
q("2007-05-07", "sem Secretaria Especial de Portos", "Secretaria Especial de Portos, titular com prerrogativas equivalentes às de Ministro (MP 369; Lei 11.518 de 5/9/2007)",
  [("bruto/l11518.html", r"O cargo de Secretário Especial de Portos terá prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado", 150)],
  "aumenta C em 1", "C +1 (ver linhas 2007 e 2008)", "leitura do par. único do art. 7º", ind="n_ministerios_mais_status; n_status_prerrogativas_equivalentes")
q("2008-02-20", "Secretário Especial da SEPPIR com prerrogativas equivalentes (C)", "cargo transformado em Ministro de Estado Chefe da SEPPIR (MP 419; Lei 11.693 de 11/6/2008)",
  [("bruto/l11693.html", r"Art\. 4º-A\. Fica transformado o cargo de Secretário Especial de Políticas de Promoção da Igualdade Racial no cargo de Ministro de Estado Chefe", 190)],
  "C −1 e A +1: o órgão muda de classe, o total não muda", "C→A para a SEPPIR (total inalterado)", "leitura da lei", ind="n_status_prerrogativas_equivalentes; n_status_ministro_de_estado_declarado")
q("2008-07-23", "par. único sem Secretaria de Assuntos Estratégicos", "Lei 11.754 cria a SAE com Ministro de Estado Chefe e reescreve o par. único sem citar a SEPPIR",
  [("bruto/l11754.html", r"Art\. 4o Fica criado o cargo de Ministro de Estado Chefe da Secretaria de Assuntos Estratégicos da Presidência da República", 140)],
  "aumenta A em 1 (SAE); a SEPPIR passa a ser A pelo cargo e não pelo par. único (sem efeito na contagem)", ef(2008, 2009), COMO_FOTO, ind="n_ministerios_mais_status; n_status_ministro_de_estado_declarado")
q("2009-06-26", "Secretaria Especial de Aquicultura e Pesca (Secretário Especial = C)", "Ministério da Pesca e Aquicultura (Lei 11.958)",
  [("bruto/l11958.html", r"Art\. 4o Fica criado o cargo de Ministro de Estado da Pesca e Aquicultura", 90), ("bruto/l11958.html", r"XXIII - do Turismo; e XXIV - da Pesca e Aquicultura\.", 70)],
  "aumenta n_ministerios em 1 e reduz C em 1 (a MP 437/2008, revogada, tentara o mesmo em 29/7/2008)", ef(2009, 2010), COMO_FOTO,
  razao="ementa: 'dispõe sobre a transformação da Secretaria Especial de Aquicultura e Pesca da Presidência da República em Ministério da Pesca e Aquicultura'; motivos não lidos")
q("2010-03-24", "Direitos Humanos, Políticas para as Mulheres e Portos com Secretários Especiais de prerrogativas equivalentes (C)", "os três viram Ministros de Estado Chefes (MP 483; Lei 12.314 de 19/8/2010) e a CGU passa a ter Ministro Chefe",
  [("bruto/mpv-0483.html", r"I - de Secretário Especial dos Direitos Humanos no cargo de Ministro de Estado Chefe da Secretaria de Direitos Humanos", 140)],
  "C −3, A +3 (total inalterado): fim da classe C como categoria usada", ef(2010, 2011), COMO_FOTO, ind="n_status_prerrogativas_equivalentes; n_status_ministro_de_estado_declarado")
q("2011-03-18", "par. único lista nominalmente os Chefes de Secretaria", "par. único passa a dizer 'os titulares das Secretarias da Presidência da República' (MP 527; Lei 12.462 de 4/8/2011); cria a Secretaria de Aviação Civil",
  [("bruto/l12462.html", r"Parágrafo único\. São Ministros de Estado: I - os titulares dos Ministérios; II - os titulares das Secretarias da Presidência da República", 160)],
  "aumenta A em 1 (Aviação Civil) e muda a regra: novas Secretarias da Presidência passam a ter Ministro por definição genérica", ef(2011, 2012), COMO_FOTO)
q("2013-03-28", "9 Secretarias da Presidência com titular Ministro", "10 (cria a Secretaria da Micro e Pequena Empresa; Lei 12.792)",
  [("bruto/l12792.html", r"XIII - pela Secretaria da Micro e Pequena Empresa", 60)],
  "aumenta A em 1", ef(2013, 2014), COMO_FOTO, razao="ementa: 'criando a Secretaria da Micro e Pequena Empresa, cargo de Ministro de Estado e cargos em comissão'")
q("2015-10-05", "24 Ministérios + 15 órgãos A", "23 Ministérios + 8 A (MP 696): extingue Previdência Social, Pesca e Aquicultura; cria Mulheres, Igualdade Racial e Direitos Humanos; revoga 6 Secretarias",
  [("bruto/mpv-0696.html", r"Art\. 8º Ficam revogados os seguintes dispositivos da Lei nº 10\.683, de 28 de maio de 2003 : I - os incisos III , VII a X e XIII do caput do art\. 1º", 180)],
  "reduz n_ministerios em 1 e A em 7", ef(2015, 2016), COMO_FOTO)
q("2016-05-12", "23 Ministérios + 8 A", "21 Ministérios + 5 A (MP 726, convertida na Lei 13.341; MP 728 recria Cultura e Educação); Controladoria-Geral da União passa de órgão A para item da lista de Ministérios",
  [("bruto/l13341.html", r"X - da Transparência, Fiscalização e Controladoria-Geral da União - CGU", 80)],
  "reduz n_ministerios em 2 e A em 3; a CGU muda de classe (A→Ministério): n_ministerios +1 e A −1 por reclassificação, sem mudar o total", ef(2016, 2017), COMO_FOTO)
q("2017-11-01", "Lei 10.683/2003 (revogada)", "Lei 13.502/2017 (MP 782): nova lei de organização, 22 Ministérios (Direitos Humanos separado) e 6 A (inclui Secretaria-Geral)",
  [("bruto/l13502-compilada.html", r"Art\. 22\. São Ministros de Estado: I - os titulares dos Ministérios; II - o Chefe da Casa Civil", 120)],
  "aumenta n_ministerios em 1 e A em 1", ef(2017, 2018), COMO_FOTO)
q("2018-02-26", "Ministério da Justiça e Segurança Pública (1 item)", "MP 821: cria o Ministério Extraordinário da Segurança Pública e transforma o da Justiça e Segurança Pública em Ministério da Justiça (Lei 13.690, 10/7/2018, torna-o 'da Segurança Pública' sem 'Extraordinário')",
  [("bruto/mpv-0821.html", r"Art\. 1º É criado o Ministério Extraordinário da Segurança Pública e transformado o Ministério da Justiça e Segurança Pública em Ministério da Justiça", 160)],
  "aumenta n_ministerios em 1 entre 26/2/2018 e 31/12/2018 (o item 'Extraordinário' conta como Ministério porque a norma o lista no artigo dos Ministérios); NÃO aparece nas fotos de 1/1", "22→23 na lista da Lei 13.502 após a MP 821 (leitura do compilado); revertido em 1/1/2019 pela MP 870", "leitura do compilado da Lei 13.502 (itens IX-A, XIII, XXIII)")
q("2019-01-01", "22 Ministérios + 6 A (Lei 13.502)", "16 Ministérios + 6 A (MP 870; Lei 13.844): Economia funde Fazenda, Planejamento, Indústria e Trabalho; a CGU consta como item da lista",
  [("bruto/mpv-0870.html", r"Art\. 19\. Os Ministérios são os seguintes:.{0,520}XVI - a Controladoria-Geral da União", 560)],
  "reduz n_ministerios em 6", ef(2018, 2019), COMO_FOTO)
q("2020-06-10", "Ministério da Ciência, Tecnologia, Inovações e Comunicações", "divide em Ministério da Ciência, Tecnologia e Inovações e Ministério das Comunicações (MP 980; Lei 14.074 de 14/10/2020)",
  [("bruto/l14074.html", r"Altera a Lei nº 13\.844, de 18 de junho de 2019, para criar o Ministério da Ciência, Tecnologia e Inovações e o Ministério das Comunicações", 160)],
  "aumenta n_ministerios em 1", ef(2020, 2021), COMO_FOTO, razao="ementa da Lei 14.074: 'para criar o Ministério da Ciência, Tecnologia e Inovações e o Ministério das Comunicações'")
q("2021-02-25", "Presidente do Banco Central é Ministro de Estado (art. 20, VII)", "LC 179 revoga o inciso VII do art. 20 da Lei 13.844 (autonomia do Banco Central)",
  [("bruto/lc179.html", r"Art\. 13\. Ficam revogados: I - o inciso VII do caput do art\. 20 da Lei nº 13\.844, de 18 de junho de 2019", 140)],
  "reduz A em 1 (n_ministerios inalterado)", "A 6→5 (fotos de 1/1/2021 e 1/1/2022; 2022 também inclui a recriação do Trabalho e Previdência)", "leitura da LC", ind="n_ministerios_mais_status; n_status_ministro_de_estado_declarado")
q("2021-07-28", "sem Ministério do Trabalho (extinto em 2019)", "Ministério do Trabalho e Previdência recriado (MP 1.058; Lei 14.261 de 16/12/2021)",
  [("bruto/l14261.html", r"Cria o Ministério do Trabalho e Previdência", 60)],
  "aumenta n_ministerios em 1", ef(2021, 2022), COMO_FOTO)
q("2023-01-01", "18 Ministérios + 5 A (Lei 13.844 vigente em 1/1/2022)", "31 Ministérios + 6 A (MP 1.154; Lei 14.600): divide a Economia e recria pastas; Secretarias de Relações Institucionais e de Comunicação Social voltam a A",
  [("bruto/mpv-1154-2023.html", r"Art\. 18\. São Ministros de Estado: I - os titulares dos Ministérios; II - o titular da Casa Civil", 120)],
  "aumenta n_ministerios em 13 e A em 1", ef(2022, 2023), COMO_FOTO)
q("2023-09-13", "31 Ministérios (Lei 14.600)", "32: Ministério do Empreendedorismo, da Microempresa e da Empresa de Pequeno Porte, por desmembramento (MP 1.187; Lei 14.816 de 16/1/2024)",
  [("bruto/l14816.html", r"Art\. 1º É criado, por desmembramento do Ministério do Desenvolvimento, Indústria, Comércio e Serviços, o Ministério do Empreendedorismo", 180)],
  "aumenta n_ministerios em 1", ef(2023, 2024), COMO_FOTO)

cols = ["indicador", "serie", "data_quebra", "tipo_de_quebra", "metodo_antigo", "metodo_novo", "razao_declarada_pela_fonte", "fonte_primaria_url", "trecho_citado",
        "direcao_do_efeito", "como_a_direcao_foi_determinada", "efeito_medido", "como_medido", "apresentada_como_aprimoramento"]
with open(os.path.join(SAIDA, "quebras.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(cols)
    for x in Q:
        tr = []
        for arq, rx, n in x["trechos"]:
            m = re.search(lib.R(rx), T(arq))
            if not m: raise SystemExit("quebra %s: trecho %r não achado em %s" % (x["data"], rx[:70], arq))
            tr.append(T(arq)[m.start(): max(m.end(), m.start() + n)][:700])
        w.writerow([x["ind"], "ministerios-1-de-janeiro", x["data"], "mudanca_de_regra", x["antigo"], x["novo"], x["razao"], url_de(x["trechos"][0][0]) or "",
                    " || ".join(tr), x["direcao"], x["como_dir"], x["efeito"], x["como_med"], x["aprim"]])
print("quebras:", len(Q))

# ---- resumo para log ------------------------------------------------------------------------------------------------------
print("ano  n  A B C  total")
for r in linhas: print(r["ano"], r["n"], r["nA"], r["nB"], r["nC"], r["total"])
print("anotações no art. 25 do compilado da Lei 10.683:", varredura_anotacoes("bruto/l10683-original.html", r"Art\. 25\. Os Ministérios são os seguintes", r"Art\. 26\."))

# ---- RESULTADO.md ----------------------------------------------------------------------------------------------------------
CURTA = {1995:"MP 813 (1/1/1995)",1996:"MP 1.226 (14/12/1995)",1997:"MP 1.549 (18/12/1996)",1998:"MP 1.549-38 (31/12/1997)",1999:"MP 1.795 (1/1/1999)",2000:"MP 1.999-13 (14/12/1999)",
 2001:"MP 2.049-26 (21/12/2000)",2002:"MP 2.216-37 (31/8/2001) + Dec. 4.046",2003:"MP 103 (1/1/2003)",2004:"Lei 10.683 (28/5/2003)",2005:"Lei 10.683 + Leis 10.869 e 11.036",
 2006:"Lei 10.683 + Lei 11.204 (5/12/2005)",2007:"idem 2006",2008:"Lei 10.683 + Leis 11.497 e 11.518 (2007)",2009:"Lei 10.683 + Leis 11.693 e 11.754 (2008)",2010:"Lei 10.683 + Lei 11.958 (26/6/2009)",
 2011:"Lei 10.683 + Lei 12.314 (19/8/2010)",2012:"Lei 10.683 + Leis 12.462 e 12.545 (2011)",2013:"idem 2012",2014:"Lei 10.683 + Lei 12.792 (28/3/2013)",2015:"idem 2014",
 2016:"MP 696 (2/10/2015)",2017:"Leis 13.341 e 13.345 (2016)",2018:"Lei 13.502 (1/11/2017)",2019:"MP 870 (1/1/2019)",2020:"Lei 13.844 (18/6/2019)",2021:"Lei 13.844 + Lei 14.074 (2020)",
 2022:"Lei 13.844 + Leis 14.261 e LC 179 (2021)",2023:"MP 1.154 (1/1/2023)",2024:"Lei 14.600 + MP 1.187 (13/9/2023)",2025:"idem 2024 (Lei 14.816)",2026:"idem 2024 (Lei 14.816)"}
tab = ["| Ano | Norma vigente em 1/1 | Ministérios | A | B | C | Ministérios + status |", "|---|---|---:|---:|---:|---:|---:|"]
for r in linhas:
    tab.append("| %d | %s | %d | %d | %d | %d | %d |" % (r["ano"], CURTA[r["ano"]], r["n"], r["nA"], r["nB"], r["nC"], r["total"]))
md = """# D1 — Ministérios no Brasil em 1º de janeiro, 1995-2026 (normas do Planalto)

Só contagem, norma e lista. Cada linha vem do texto baixado do Planalto (cadeia de hash em `manifest.jsonl` desta pasta). Gerado por `scripts/gerar.py`.

## Achado

""" + "\n".join(tab) + """

Regra de contagem (a mesma em todos os anos):

- **Ministérios** = itens do artigo que a norma abre com "Os Ministérios são os seguintes" (art. 13 da Lei 9.649/1998 e MPs de 1995-2002; art. 25 da Lei 10.683/2003; art. 21 da Lei 13.502/2017; art. 19 da Lei 13.844/2019; art. 17 da Lei 14.600/2023). A Controladoria-Geral da União conta como Ministério nos anos em que a norma a põe nesse artigo (2016-2026, com redações diferentes) e como órgão A nos anos 2003-2015.
- **A** = órgão fora dessa lista cujo titular a norma declara Ministro de Estado (parágrafo "São Ministros de Estado ..." ou cargo "Ministro de Estado Chefe da ...").
- **B** = cargo ou gabinete de "Ministro de Estado Extraordinário" (Esportes, Política Fundiária, Projetos Especiais, Segurança Alimentar); a norma não o lista como Ministério (exceto o Ministério Extraordinário da Segurança Pública, 2018, que está no artigo da lista e conta como Ministério).
- **C** = titular com "prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado".
- **Ministérios + status** = soma das quatro colunas. Cada órgão conta uma vez. As colunas A, B e C estão separadas para quem preferir outra definição de "status".

Série em uma linha (Ministérios + status): """ + ", ".join("%d:%d" % (r["ano"], r["total"]) for r in linhas) + """.
Só Ministérios: """ + ", ".join("%d:%d" % (r["ano"], r["n"]) for r in linhas) + """.

## Quebras (a série não é comparável em linha reta)

`series/quebras.csv` traz """ + str(len(Q)) + """ eventos com o trecho citado. Os que mais mudam a definição:

- 1999-06-10: Exército, Marinha e Aeronáutica viram o Ministério da Defesa (3 itens -> 1; MP 1.799-6).
- 1999-12-14: o Gabinete do Ministro Extraordinário de Política Fundiária (B) vira Ministério (item da lista).
- 2008-2010: Igualdade Racial, Direitos Humanos, Mulheres e Portos passam de C (equivalência) a A (Ministro de Estado Chefe); em 2011 o parágrafo deixa de listar nomes e passa a dizer "os titulares das Secretarias da Presidência da República" (mudança na regra de definição).
- 2016: a Controladoria-Geral da União passa de A para item da lista de Ministérios; desde 2019 consta como "Controladoria-Geral da União" (sem a palavra "Ministério") no artigo dos Ministérios.
- 2018: um Ministério Extraordinário (Segurança Pública, 26/2 a 31/12/2018) existiu entre duas fotos de 1/1 e não aparece na série.
- 2021: o Presidente do Banco Central deixa de ser Ministro de Estado (LC 179, 25/2/2021); contava em A desde 2004-2005.

## O que não foi achado ou não foi verificado

- Ato que criou o Gabinete do Ministro Extraordinário de Política Fundiária (existência confirmada nos Decretos 1.888, 1.918 e 2.321, de 1996-1997) e o de Projetos Especiais (citado na MP 1.795): não localizados. A classe B de 1997, 1998 e 1999 é por continuidade (linhas marcadas `nao_verificado`).
- Lei 9.649/1998 original (27/5/1998) não foi baixada; só o compilado de 2001 e as MPs. Não afeta as fotos de 1/1/1998 e 1/1/1999 (a MP 1.795 reescreve o art. 13), mas o art. 23 (equivalência da Casa Militar, 1999) foi lido só no compilado.
- Cargos de Ministro Extraordinário criados fora da lei de organização: não houve busca sistemática em 1995-1998. Tentativa de achar o ato de criação de Política Fundiária: WebSearch, varredura das MPs 1.385 a 1.449 (26 existem em `/MPV/Antigas/`, nenhuma trata do tema; baixadas em memória, sem registro) e dos Decretos 1.880 a 1.892 de 1996: nada. Outro Ministro Extraordinário do período, se houver, não está na série.
- Texto original da Lei 10.683/2003 não existe em arquivo próprio no Planalto: lido no compilado, onde o trecho sem anotação é o original.
- Decretos que extinguem ou criam cargos ministeriais fora das leis lidas: só o Decreto 4.046/2001 foi achado (pela remissão no compilado). Outros podem existir para anos não cobertos pelas anotações.
- Data de publicação no DOU: lida só quando o rodapé do Planalto a traz (coluna `verificacao`). Se a MP 1.549-38 saiu em 1-2/1/1998, vale a -37, de lista idêntica.
- Exposições de motivos das MPs não foram lidas: a coluna "razão declarada" de `quebras.csv` diz isso.
- 2026: o texto compilado da Lei 14.600 baixado em 20/10/2026 não mostra mudança do art. 17 ou 18 em 2025-2026 (já inclui a Lei 15.352 de 25/2/2026 em outro dispositivo); atos que o Planalto ainda não anotou não estariam refletidos.
- Efeitos de estrutura (decretos de estrutura regimental) das MPs 696/2015, 726/2016 e da Lei 13.502/2017 dependem de decretos não lidos; a lista de Ministérios vale desde a publicação.

## Ressalvas

- 2002: o texto do § 1º da MP 2.216-37 ainda cita o Chefe da Secretaria de Comunicação de Governo como Ministro; o Decreto 4.046 (10/12/2001) extinguiu o cargo e a série desconta (A=5, total 26). Leitura literal do parágrafo, sem o decreto: A=6, total 27.\n- "Ministério" é o que a norma lista; "Ministro de Estado" inclui o Presidente do Banco Central (2005-2021) e o Advogado-Geral da União (2001-2026) por determinação legal.
- Reedições de MP (1995-2001): só as versões baixadas entram na comparação de listas; reedições intermediárias não baixadas (ex.: 1.549-25, 1.799-2, 1.799-3, 1.799-5, 1.999-11, 1.999-12) podem ter lista diferente das vizinhas. Em cada 1º de janeiro a versão usada é a última baixada com data <= 1/1, e o intervalo até a seguinte baixada é de ~30 dias (ciclo de reedição), então nenhuma versão vigente em 1/1 ficou de fora. A comparação é automatizada e tolera erros de numeração romana do texto do Planalto (anotados em `verificacao`).
- Cadeia de hash: `bruto/mpv-0111.html` tem uma linha antiga errada (baixei por engano a Lei 10.678 com esse nome) e foi re-baixado como MP 111 verdadeira; duas cópias de arquivos de outro agente (`l9649-compilada`, `l13502-compilada`) foram re-registradas para corrigir a URL. `chain.py verify` dá OK com 3 linhas "superseded".
"""
open(os.path.join(BASE, "RESULTADO.md"), "w", encoding="utf-8").write(md)
