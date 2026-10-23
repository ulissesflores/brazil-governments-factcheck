"""Serie anual do resultado primario do Governo Central (Tesouro, RTN) com decomposicao das linhas de receita
nao-tributaria. Le derivado/rtn/15-2_2.csv (R$ mi correntes) e 16-2_2_A.csv (fracao do PIB), gerados do bruto
bruto/tesouro-rtn-serie-historica-jul26.xlsx por scripts/xlsx_para_csv.py. Sem rede. Uso: python3 -I serie_rtn.py <pasta_mecanismos>"""
import csv, sys, pathlib
base = pathlib.Path(sys.argv[1])
VINT = "seriehistoricajul26.xlsx (Tesouro Nacional, RTN, boletim de jul/2026; valores sujeitos a revisao)"
def le(f):
    rows = list(csv.reader(open(base / "derivado/rtn" / f, encoding="utf8")))
    hdr = next(r for r in rows if r and r[0] == "Discriminação")
    anos = [int(x) for x in hdr[1:] if x]
    d = {}
    for r in rows[rows.index(hdr) + 1:]:
        k = r[0].strip()
        if k and k not in d:  # primeira ocorrencia (as tabelas repetem rotulos so no memorando)
            d[k] = {a: (float(r[i + 1]) if r[i + 1] not in ("", None) else None) for i, a in enumerate(anos)}
    return anos, d
anos, v = le("15-2_2.csv"); _, p = le("16-2_2_A.csv")
def achar(d, pref):
    for k in d:
        if k.startswith(pref): return k
    raise KeyError(pref)
L = {  # rotulo curto: (prefixo, definicao)
 "receita_total": ("1. RECEITA TOTAL", "Receita total do Governo Central, conceito de caixa (RTN, linha 1)"),
 "concessoes_permissoes": ("1.4.1  Concessões", "Receitas nao administradas pela RFB, 1.4.1 Concessoes e Permissoes (inclui bonus de assinatura de leiloes)"),
 "dividendos_participacoes": ("1.4.2  Dividendos", "Receitas nao administradas pela RFB, 1.4.2 Dividendos e Participacoes"),
 "operacoes_com_ativos": ("1.4.8.1 d/q", "Receitas de operacoes com ativos (d/q 1.4.8 Demais receitas nao administradas)"),
 "exploracao_recursos_naturais": ("1.4.4  Receitas de Exploração", "1.4.4 Receitas de exploracao de recursos naturais (royalties; tratada como recorrente neste dossie, so informativa)"),
 "resultado_primario_acima_da_linha": ("5. RESULTADO PRIMÁRIO GOVERNO CENTRAL - ACIMA", "Resultado primario do Governo Central, acima da linha (linha 5)"),
 "ajuste_caixa_competencia": ("6.2 Ajuste Metodológico Caixa", "Ajuste metodologico caixa-competencia (subsidios e subvencoes; linha 6.2)"),
 "resultado_primario_abaixo_da_linha": ("8. RESULTADO PRIMÁRIO DO GOVERNO CENTRAL", "Resultado primario do Governo Central, abaixo da linha (linha 8), referencia do BCB/Tesouro"),
 "memo_fundo_soberano": ("Fundo Soberano do Brasil", "Memorando: despesa/aporte do Fundo Soberano do Brasil excluido do primario (valor do memorando do RTN)"),
 "memo_pac": ("PAC 15/", "Memorando: despesas do PAC (Tesouro deixou de divulgar a partir de 2020)"),
}
pib = v[achar(v, "PIB Nominal")] if any(k.startswith("PIB Nominal") for k in v) else p[achar(p, "PIB Nominal")]
out = []
def put(ind, fonte, defn, ano, val, un, nota=""):
    out.append([ind, fonte, defn, ano, "" if val is None else (f"{val:.6f}".rstrip("0").rstrip(".")), un, nota, VINT])
for nome, (pref, defn) in L.items():
    kv = achar(v, pref); kp = achar(p, pref)
    for a in anos:
        put(nome + "_rs_mi", "Tesouro RTN tab 2.2", defn, a, v[kv][a], "R$ milhoes correntes")
        pv = p[kp][a]
        put(nome + "_pct_pib", "Tesouro RTN tab 2.2-A", defn, a, None if pv is None else pv * 100, "% do PIB")
# proxies (soma das linhas oficiais; NAO e classificacao oficial de 'nao recorrente')
base_k = achar(v, L["resultado_primario_acima_da_linha"][0]); pk = achar(p, L["resultado_primario_acima_da_linha"][0])
kc, kd, ka = (achar(v, L[x][0]) for x in ("concessoes_permissoes", "dividendos_participacoes", "operacoes_com_ativos"))
pc, pd_, pa = (achar(p, L[x][0]) for x in ("concessoes_permissoes", "dividendos_participacoes", "operacoes_com_ativos"))
for a in anos:
    g = lambda d, k: d[k][a] or 0.0
    rs_a = v[base_k][a] - g(v, kc) - g(v, ka)
    rs_b = rs_a - g(v, kd)
    pa_ = (p[pk][a] - g(p, pc) - g(p, pa)) * 100
    pb_ = pa_ - g(p, pd_) * 100
    defA = "PROXY deste dossie = linha 5 menos 1.4.1 Concessoes e Permissoes menos 1.4.8.1 Operacoes com ativos (soma de linhas oficiais; nao e a classificacao 'nao recorrente' do Tesouro)"
    defB = "PROXY deste dossie = proxy A menos 1.4.2 Dividendos e Participacoes"
    put("primario_sem_concessoes_e_ativos_rs_mi", "calculo sobre Tesouro RTN tab 2.2", defA, a, rs_a, "R$ milhoes correntes")
    put("primario_sem_concessoes_ativos_dividendos_rs_mi", "calculo sobre Tesouro RTN tab 2.2", defB, a, rs_b, "R$ milhoes correntes")
    put("primario_sem_concessoes_e_ativos_pct_pib", "calculo sobre Tesouro RTN tab 2.2-A", defA, a, pa_, "% do PIB")
    put("primario_sem_concessoes_ativos_dividendos_pct_pib", "calculo sobre Tesouro RTN tab 2.2-A", defB, a, pb_, "% do PIB")
    put("pib_nominal_rs_mi", "Tesouro RTN tab 2.2 (memorando)", "PIB nominal usado pelo Tesouro como denominador", a, pib[a], "R$ milhoes correntes")
w = csv.writer(open(base / "series/rtn-resultado-primario-extraordinarias.csv", "w", newline="", encoding="utf8"))
w.writerow(["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]); w.writerows(out)
print(len(out), "linhas;", anos[0], anos[-1])
