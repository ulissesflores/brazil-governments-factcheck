"""Constroi series/amil_pf_rj_tabelas_wayback.csv a partir do texto (pdftotext -layout) das tabelas de vendas PF RJ da Amil
capturadas no Wayback. So o bloco 'Individual' (faixa etaria x plano), coluna a coluna, sem inferir nada.
Uso: python3 -I scripts/construir_amil.py  (rodar de dentro da pasta ans-planos-fase2)"""
import re, csv, json, hashlib, pathlib
BASE = pathlib.Path(__file__).resolve().parent.parent
FAIXAS = ["0 a 18","19 a 23","24 a 28","29 a 33","34 a 38","39 a 43","44 a 48","49 a 53","54 a 58","59+"]
NUM = r"\d+(?:\.\d{3})*,\d{2}"
def num(s): return float(s.replace(".","").replace(",","."))
ROW = re.compile(rf"^\s*(?:(\d{{1,2}})\s*(?:a|-)\s*(\d{{2}})|>\s*=\s*59)\s+(.*)$")
def linhas(path): return open(path,encoding="utf8",errors="replace").read().split("\n")
def blocos_2006(path):
    """blocos com cabecalho 'FAIXA ETARIA <rotulos>' seguido de 10 linhas de faixa."""
    L = linhas(path); out = []; i = 0; produto = ""; secao = ""
    while i < len(L):
        ln = L[i]
        if re.search(r"Tabela de Vendas", ln): secao = re.sub(r"\s+"," ",ln).strip()
        m = re.match(r"^\s{10,}(AMIL \d+|AMIL|NEXT[A-ZÓ ]*|REFER[ÊE]NCIA)\s{3,}N", ln)
        if m: produto = m.group(1).strip()
        if re.match(r"^\s*FAIXA ET", ln):
            rot = [x.strip() for x in re.split(r"\s{2,}", ln.strip())][1:]
            rows = []; j = i + 1
            while j < len(L) and len(rows) < 10:
                r = ROW.match(L[j])
                if r:
                    ns = re.findall(NUM, r.group(3))
                    rows.append([num(x) for x in ns[:len(rot)]])
                j += 1
            out.append({"secao": secao, "produto_titulo": produto, "rotulos": rot, "linhas": rows, "linha_arquivo": i + 1})
            i = j; continue
        i += 1
    return out
SAIDA = []
def emite(arq, data_captura, validade, blocos, filtro):
    for b in blocos:
        if not filtro(b): continue
        if len(b["linhas"]) != 10: continue
        for ci, rot in enumerate(b["rotulos"]):
            for fi, fx in enumerate(FAIXAS):
                v = b["linhas"][fi]
                if ci >= len(v): continue
                SAIDA.append([arq, data_captura, validade, b["secao"], b["produto_titulo"], rot, "Rio de Janeiro", fx, f"{v[ci]:.2f}", b["linha_arquivo"]])
T = BASE/"derivado/texto-amil"
b05 = blocos_2006(T/"20060511_AMIL-TabVendasPF200605-RJ.txt")
emite("bruto/amil-wayback/20060511_AMIL-TabVendasPF200605-RJ.pdf","2006-05-11","a partir de maio de 2006", b05, lambda b: "INDIVIDUAL" in b["secao"].upper() and "FAMILIAR" not in b["secao"].upper())
b11 = blocos_2006(T/"20070228_AMIL-tabPF200611-RJ.txt")
emite("bruto/amil-wayback/20070228_AMIL-tabPF200611-RJ.pdf","2007-02-28","a partir de novembro (de 2006, pelo nome do arquivo)", b11, lambda b: "INDIVIDUAL" in b["secao"].upper() and "FAMILIAR" not in b["secao"].upper())
# 2009-02 e 2010-01: formato de tabelao; bloco 'INDIVIDUAL OU GRUPAL' (primeiro), rotulos lidos do cabecalho do PDF
def tabelao(path, rotulos, ini):
    L = linhas(path); rows = []
    for k in range(ini, len(L)):
        r = ROW.match(L[k])
        if r:
            rows.append([num(x) for x in re.findall(NUM, r.group(3))[:len(rotulos)]])
            if len(rows) == 10: return rows, ini + 1
    return None, None
ro09 = ["Amil 110 Nacional QP","Amil 120 Nacional QP","Amil 130 Nacional QP","Amil 140 Nacional QP","Amil 150 Nacional R 2.1.2 QP","Amil 160 Nacional R 3.3.4 QP","Amil 160 Nacional R 5.5.6 QP"]
rows, ln = tabelao(T/"20090306_Amil-TabVendas-PF200902-RJ.txt", ro09, 20)
b = {"secao":"Pessoa Fisica - INDIVIDUAL OU GRUPAL","produto_titulo":"Tabela de Venda Amil 2009","rotulos":ro09,"linhas":rows,"linha_arquivo":ln}
emite("bruto/amil-wayback/20090306_Amil-TabVendas-PF200902-RJ.pdf","2009-03-06","tabela de fevereiro de 2009 (nome do arquivo PF200902)",[b],lambda b:True)
ro10 = ["Blue Classico Niteroi QC","Blue Classico Niteroi QP","Amil Blue I Nacional QC","Amil Blue I Nacional QP","Amil Blue II Nacional QC","Amil Blue II Nacional QP","Amil Blue III Nacional QP","Amil Blue IV Nacional QP"]
rows, ln = tabelao(T/"20100602_Tabela_PF_RJ_012010.txt", ro10, 0)
b = {"secao":"Pessoa Fisica - INDIVIDUAL OU GRUPAL","produto_titulo":"Tabela de Vendas 2009/2010 (validade ate 28/2/2010)","rotulos":ro10,"linhas":rows,"linha_arquivo":ln}
emite("bruto/amil-wayback/20100602_Tabela_PF_RJ_012010.pdf","2010-06-02","precos e planos validos ate 28/2/2010 (texto do PDF)",[b],lambda b:True)
MAN = {}
for l in open(BASE/"manifest.jsonl", encoding="utf8"):
    d = json.loads(l); MAN[pathlib.Path(d["arquivo"]).name] = (d["url"], d["sha256"])
out = BASE/"series/amil_pf_rj_tabelas_wayback.csv"
with open(out,"w",newline="",encoding="utf8") as f:
    w = csv.writer(f); w.writerow(["arquivo_bruto","data_captura_wayback","validade_segundo_o_documento","secao","produto_titulo","coluna_rotulo_no_documento","praca","faixa_etaria","mensalidade_rs","linha_no_txt", "url_arquivada", "sha256_do_pdf"])
    w.writerows([r + list(MAN[pathlib.Path(r[0]).name]) for r in SAIDA])
print(len(SAIDA), "linhas ->", out)
