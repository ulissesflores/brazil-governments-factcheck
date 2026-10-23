"""ANS: teto de reajuste dos planos individuais/familiares (tabela oficial da ANS) -> series + indice composto (dez/1999=100).
Uso: python3 -I scripts/construir_individual.py   (de dentro de ans-planos-fase2)"""
import zipfile, re, csv, hashlib, pathlib
BASE = pathlib.Path(__file__).resolve().parent.parent
XLSX = BASE/"bruto/ans/tabela_reajustes_individuais_2026.xlsx"
sha = hashlib.sha256(XLSX.read_bytes()).hexdigest()
z = zipfile.ZipFile(XLSX)
ss = re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode(), flags=re.S)
ss = [re.sub(r"<[^>]+>","",s) for s in ss]
sh = z.read("xl/worksheets/sheet1.xml").decode()
linhas = []
for row in re.findall(r"<row [^>]*>(.*?)</row>", sh, flags=re.S):
    d = {}
    for attrs, v in re.findall(r"<c ([^>]*)>(?:<v>([^<]*)</v>)?</c>", row):
        if v == "": continue
        col = re.search(r'r="([A-Z]+)\d+"', attrs).group(1)
        d[col] = ss[int(v)] if 't="s"' in attrs else float(v)
    if "C" in d and "D" in d: linhas.append((d["C"], d["D"]))
dados = []
for per, v in linhas:
    m = re.match(r"maio/(\d{4}) a abril/(\d{4})", str(per))
    if m: dados.append((int(m.group(1)), int(m.group(2)), round(float(v)*100, 4)))
dados.sort()
assert [d[0] for d in dados] == list(range(2000, 2027)), [d[0] for d in dados]
VINT = f"bruto/ans/tabela_reajustes_individuais_2026.xlsx sha256 {sha[:12]}"
DEF = "ANS: percentual maximo de reajuste anual, planos individuais/familiares (Lei 9.656/98), periodo de aplicacao maio a abril"
with open(BASE/"series/ans_teto_individual_anual.csv","w",newline="",encoding="utf8") as f:
    w = csv.writer(f); w.writerow(["indicador","fonte","definicao_linha","ano","mes_ou_trimestre","valor","unidade","nota","vintage"])
    for a0, a1, v in dados:
        w.writerow(["ans_teto_reajuste_individual","ANS tabela_reajustes_individuais_2026.xlsx (pagina oficial 'Reajuste anual de planos individuais/familiares')",DEF,a0,5,f"{v:.2f}","%",f"periodo de aplicacao maio/{a0} a abril/{a1}; valor como publicado (2 casas)",VINT])
# indice composto: aplica cada reajuste em maio; I(dez/1999)=100
idx = 100.0; saida = [("1999-12", 100.0)]
mensal = {}
for a0, a1, v in dados:
    for mes in range(1, 13):
        if (a0, mes) == (a0, 5): idx *= (1 + v/100)
        mensal[(a0, mes)] = idx
with open(BASE/"derivado/indice_ans_teto_individual_dez1999_100.csv","w",newline="",encoding="utf8") as f:
    w = csv.writer(f); w.writerow(["indicador","fonte","definicao_linha","ano","mes_ou_trimestre","valor","unidade","nota","vintage"])
    w.writerow(["indice_ans_teto_individual_dez1999_100","derivado de ANS tabela_reajustes_individuais_2026.xlsx",DEF+"; indice composto","1999",12,"100.0000","indice (dez/1999=100)","base; nenhum reajuste antes de maio/2000",VINT])
    for (a, m), v in sorted(mensal.items()):
        w.writerow(["indice_ans_teto_individual_dez1999_100","derivado de ANS tabela_reajustes_individuais_2026.xlsx",DEF+"; indice composto",a,m,f"{v:.4f}","indice (dez/1999=100)","I(maio/a)=I(abril/a)*(1+teto/100); constante entre maios; e indice de TETOS em sequencia, nao preco efetivamente pago (ver RESULTADO.md)",VINT])
print("anos:", len(dados))
for a0,a1,v in dados: print(a0, v, f"{mensal[(a0,12)]:.2f}")
