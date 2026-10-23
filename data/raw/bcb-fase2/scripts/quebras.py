"""Gera quebras.csv. Trechos citados sao extraidos por busca de ancoras no texto dos PDFs hasheados (nada digitado de memoria)."""
import csv, json, re, subprocess, html
from pathlib import Path
P = Path(__file__).resolve().parent.parent
ref = json.load(open(P / "derivado/_resumo.json"))
def txt(pdf):
    t = subprocess.run(["pdftotext", str(P / "bruto" / pdf), "-"], capture_output=True, text=True).stdout
    return re.sub(r"\s+", " ", t.replace("\f", " ")).replace("- ", "-") if False else re.sub(r"\s+", " ", t.replace("\f", " "))
def trecho(t, ini, fim):
    a = t.index(ini); b = t.index(fim, a) + len(fim)
    return t[a:b]
ri = txt("doc_ri_2008_03_boxe_dbgg.pdf")
nt = txt("doc_nota_tecnica_47_2018.pdf")
q1 = trecho(ri, "Na metodologia utilizada anteriormente", "total da DBGG")
q1 = trecho(ri, "Na metodologia utilizada anteriormente", "operações compromissadas")  # primeira ocorrencia, ate o fim da enumeracao
q1 = trecho(ri, "Na metodologia utilizada anteriormente", "externa dessas três esferas do setor público.")
q2 = trecho(ri, "a parcela desses títulos que compõe a carteira do Banco Central", "com a dívida do Tesouro.")
q3 = trecho(ri, "em vigor a partir de janeiro de 2008", "endividamento de origem eminentemente fiscal.")
q4 = trecho(nt, "No conceito de DBGG que passou a vigorar a partir de 2008", "deixaram de ser computados na nova metodologia da DBGG.")
ck = json.load(open(P / "bruto/ckan_4513.json"))["result"]["results"][0]["notes"]
ck = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", ck)))
q5 = trecho(ck, "A exclusão da Petrobras das estatísticas fiscais", "retroagiu a dezembro de 2001.")
sob = ref["sob"]["2006-12 a 2025-12"]; sob2 = ref["sob"]["2006-12 a ultimo mes"]; fam = ref["fam"]
H = "indicador,serie,data_quebra,metodo_antigo,metodo_novo,razao_declarada_pela_fonte,fonte_primaria_url,trecho_citado,direcao_do_efeito,como_a_direcao_foi_determinada,efeito_medido,como_medido,apresentada_como_aprimoramento,celulas_do_infografico_afetadas,tipo_de_quebra".split(",")
assert H == next(csv.reader(open(P.parent / "moeda-fiscal/quebras.csv")))
RI = "https://www.bcb.gov.br/htms/relinf/port/2008/03/ri200803b4p.pdf"
rows = [
 ["dbgg_pib (divida bruta do governo geral, % do PIB)", "BCB SGS 4537 (metodologia utilizada ate 2007; segue publicada) e SGS 13762 (metodologia utilizada a partir de 2008; inicio 2006-12)",
  "vigencia em 2008-01; serie nova retroagida a 2006-12",
  "DBGG com toda a carteira de titulos publicos do Banco Central, sem as operacoes compromissadas",
  "DBGG com a divida mobiliaria em mercado do Tesouro e as operacoes compromissadas do Banco Central, sem os titulos livres na carteira do BC",
  "refletir mais fielmente no indicador o endividamento de origem eminentemente fiscal (Relatorio de Inflacao, marco/2008)",
  RI + " ; nota tecnica complementar: https://www.bcb.gov.br/content/publicacoes/notastecnicas/47_notas_tecnicas_julho_2018.pdf",
  f"[Relatorio de Inflacao mar/2008, boxe] \"{q3}\" \"{q1}\" \"{q2}\" [Nota Tecnica BCB 47, jul/2018] \"{q4}\"",
  "reduz", f"medida na sobreposicao: SGS 13762 menor que SGS 4537 em todos os {sob2['n']} meses de {sob2['ini'][0]}-{sob2['ini'][1]:02d} a {sob2['fim'][0]}-{sob2['fim'][1]:02d} (diferenca minima {sob2['min']} pp)",
  f"diferenca (antiga menos nova) em pontos percentuais do PIB, 2006-12 a 2025-12 (n={sob['n']}): media {sob['media']}, mediana {sob['mediana']}, desvio-padrao {sob['dp']}, minimo {sob['min']}, maximo {sob['max']}; 2006-12 a {sob2['fim'][0]}-{sob2['fim'][1]:02d} (n={sob2['n']}): media {sob2['media']}. NAO e constante: media anual vai de {min(v[0] for v in ref['sob_ano'].values())} a {max(v[0] for v in ref['sob_ano'].values())} pp (tabela em RESULTADO.md); encadear por diferenca media unica e uma aproximacao a ser declarada",
  "bcb-fase2/derivado/sobreposicao_dbgg.csv (SGS 4537 menos SGS 13762, mes a mes, valores do bruto hasheado)",
  "sim: o texto do BCB apresenta a mudanca como contínuo aperfeicoamento das estatisticas fiscais e maior aderencia entre DBGG e resultado primario",
  "nenhuma: indicador fora do infografico original; afeta o item Divida bruta do governo geral/PIB do indice da fase 2", "metodo_estatistico"],
 ["dlsp_pib (divida liquida do setor publico, % do PIB)", "BCB SGS 4513 (setor publico consolidado, inicio 2001-12)",
  "2001-12 (inicio da serie); exclusao da Petrobras em 2009-05 e da Eletrobras em 2010-11, retroagidas a 2001-12",
  "abrangencia com Petrobras e Eletrobras (series 'encerradas em abril de 2009', so nas tabelas especiais do BCB)",
  "abrangencia sem Petrobras e sem Eletrobras, calculada desde 2001-12",
  "caracteristicas especificas das empresas, regras de governanca corporativa similares as de privadas de capital aberto e autonomia para captar recursos",
  "https://dadosabertos.bcb.gov.br/api/3/action/package_search?rows=5&q=codigo_sgs%3A4513",
  q5, "desconhecida", "a serie antiga (com Petrobras) nao foi baixada; a pagina de tabelas especiais do BCB (https://www.bcb.gov.br/estatisticas/tabelasespeciais) e uma aplicacao JavaScript e nao foi lida sem navegador",
  "nao medido: sem a serie antiga nao ha sobreposicao. ANTES de 2001-12 nao existe SGS 4513; o catalogo SGS so tem saldos em R$ milhoes de 1991 em diante para GF+BC (SGS 4468) e estaduais+municipais (SGS 4471), sem % do PIB, sem estatais e em moeda convertida",
  "nenhuma medicao feita; ver RESULTADO.md", "nao declarado pela fonte",
  "nenhuma: indicador fora do infografico original; Contexto (C) da fase 2, nao pontua", "metodo_estatistico"],
 ["endividamento_familias_renda (endividamento das familias com o SFN / renda acumulada 12 meses)", "BCB SGS 19882 (total) e 19881 (exceto habitacional), antigas, ate 2021-08; SGS 29037 e 29038 (RNDBF), desde 2005-01",
  "2021-08 (ultimo dado das series antigas 19881/19882; as novas cobrem 2005-01 a 2026-07)",
  "series antigas SGS 19881/19882: nome oficial, unidade e metodo NAO encontrados (CKAN vazio em duas tentativas para cada codigo; pagina de metadados do SGS indisponivel)",
  "series SGS 29037/29038 (RNDBF): endividamento = valor atual das dividas das familias com o SFN / renda das familias acumulada nos ultimos 12 meses (conceito do catalogo)",
  "nao encontrada: nenhuma nota do BCB sobre a substituicao foi localizada",
  "https://dadosabertos.bcb.gov.br/api/3/action/package_search?rows=5&q=codigo_sgs%3A29037",
  "nao ha trecho a citar: o BCB nao publicou, nas fontes lidas, nota sobre as series 19881/19882. Conceito da serie nova (catalogo, SGS 29037): \"Endividamento - Relacao entre o valor atual das dividas das familias com o Sistema Financeiro Nacional e a renda das familias acumulada nos ultimos doze meses.\"",
  "reduz", f"medida na sobreposicao: serie nova menor que a antiga em todos os {fam['19882_vs_29037']['n']} meses (par 19882/29037) e em todos os {fam['19881_vs_29038']['n']} meses (par 19881/29038); 0 meses iguais. O PAR (19882=total, 19881=exceto habitacional) foi inferido pela ordem de grandeza: hipotese, nao confirmada pela fonte",
  f"diferenca (antiga menos nova), pp: par 19882/29037 media {fam['19882_vs_29037']['media']}, minimo {fam['19882_vs_29037']['min']}, maximo {fam['19882_vs_29037']['max']}; par 19881/29038 media {fam['19881_vs_29038']['media']}, minimo {fam['19881_vs_29038']['min']}, maximo {fam['19881_vs_29038']['max']}. A diferenca cresce no tempo no par total (media {ref['fam_ano']['19882_vs_29037']['2005']} pp em 2005; {ref['fam_ano']['19882_vs_29037']['2021']} pp em 2021): a quebra NAO e um deslocamento constante",
  "bcb-fase2/derivado/sobreposicao_endividamento_familias.csv (serie antiga menos serie nova, mes a mes)",
  "nao declarado pela fonte", "nenhuma: indicador fora do infografico original; afeta o item Endividamento das familias/renda do indice da fase 2", "metodo_estatistico"],
]
with open(P / "quebras.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(H); w.writerows(rows)
print(len(rows), "linhas")
for q in (q1, q2, q3, q4, q5): print("-", q[:120], "...", q[-60:])
