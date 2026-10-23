"""Constroi series/*.csv (CSV longo), derivado/*.csv e dados_resultado.json a partir do bruto/ hasheado. Sem rede. Nada estimado."""
import csv, json, statistics as st
from pathlib import Path
P = Path(__file__).resolve().parent.parent
man = {}
for l in (P / "manifest.jsonl").read_text().splitlines():
    m = json.loads(l); man[Path(m["arquivo"]).name] = m

def vint(fname):
    m = man[fname]
    return f"bruto/{fname} adquirido {m['timestamp_utc']} sha256 {m['sha256'][:12]}"

def load(c):
    d = json.load(open(P / f"bruto/sgs_{c}.json"))
    out = {}
    for x in d:
        ano, mes = int(x["data"][6:]), int(x["data"][3:5])
        assert (ano, mes) not in out, (c, ano, mes)
        out[(ano, mes)] = float(x["valor"])
    return out

# codigo: (nome curto do indicador, definicao_linha, unidade, nota)
S = {
 4513: ("divida_liquida_setor_publico_pib", "Divida liquida do setor publico, total, setor publico consolidado (% do PIB), saldo fim de periodo; abrangencia sem Petrobras e sem Eletrobras, retroagida a dez/2001", "Percentual do PIB", "Catalogo BCB: inicio 01-12-2001; antes disso nao ha esta serie no SGS"),
 13762: ("dbgg_pib_metodologia_2008", "Divida bruta do governo geral (% do PIB), metodologia utilizada a partir de 2008 (inclui operacoes compromissadas do BC; exclui titulos livres na carteira do BC)", "Percentual do PIB", ""),
 4537: ("dbgg_pib_metodologia_ate_2007", "Divida bruta do governo geral (% do PIB), metodologia utilizada ate 2007 (inclui toda a carteira de titulos publicos do BC; exclui compromissadas); BCB segue publicando", "Percentual do PIB", ""),
 29037: ("endividamento_familias_renda_total", "Endividamento das familias com o SFN em relacao a renda acumulada dos ultimos doze meses (RNDBF)", "Percentual", ""),
 29038: ("endividamento_familias_renda_ex_habitacional", "Endividamento das familias com o SFN exceto credito habitacional em relacao a renda acumulada dos ultimos 12 meses (RNDBF)", "Percentual", ""),
 29034: ("comprometimento_renda_familias_total", "Comprometimento de renda das familias com o servico da divida com o SFN, com ajuste sazonal (RNDBF)", "Percentual", "media movel trimestral, ajustado sazonalmente (conceito do catalogo)"),
 29035: ("comprometimento_renda_familias_ex_habitacional", "Comprometimento de renda das familias com o servico da divida com o SFN exceto credito habitacional, com ajuste sazonal (RNDBF)", "Percentual", "media movel trimestral, ajustado sazonalmente (conceito do catalogo)"),
 19882: ("endividamento_familias_antiga_19882", "Serie antiga SGS 19882 (encerrada em ago/2021). Nome oficial NAO encontrado (CKAN vazio, 2 tentativas); lida como endividamento total pela ordem de grandeza (59,9 em 08/2021 vs 49,9 da 29037 em 07/2026) e pelo par com 19881; hipotese, nao confirmada", "Percentual (unidade nao documentada; lida como percentual da renda)", "metadados nao achados"),
 19881: ("endividamento_familias_antiga_19881", "Serie antiga SGS 19881 (encerrada em ago/2021). Nome oficial NAO encontrado (CKAN vazio, 2 tentativas); lida como endividamento exceto credito habitacional pela ordem de grandeza; hipotese, nao confirmada", "Percentual (unidade nao documentada; lida como percentual da renda)", "metadados nao achados"),
 3546: ("reservas_internacionais_caixa_usd_mi", "Reservas internacionais, saldo mensal (SGS 3546). Conferido contra as series diarias do BCB: coincide com o CONCEITO CAIXA (SGS 13621) no ultimo dia util do mes em 331 de 337 meses (os 6 restantes diferem por 1 a 67 US$ mi); NAO coincide com o conceito liquidez (SGS 13982) a partir de set/2008", "US$ milhoes", "CKAN sem registro para 3546 (2 tentativas); nome oficial nao achado; conceito identificado por comparacao (ver derivado/conferencia_reservas_3546_vs_13621_13982.csv); o pedido dizia conceito liquidez: DESVIO declarado"),
 4468: ("dlsp_saldo_gf_bc_rs_mi", "Divida liquida do setor publico, saldos em R$ milhoes, governo federal e Banco Central (NAO e % do PIB; NAO e consolidado)", "Milhoes de reais", "valores de 1991-1994 vem de moedas anteriores convertidas; ordem de grandeza nao comparavel com os saldos atuais (mesma ressalva de mudanca de unidade ja registrada em moeda-fiscal/quebras.csv)"),
 4471: ("dlsp_saldo_estaduais_municipais_rs_mi", "Divida liquida do setor publico, saldos em R$ milhoes, governos estaduais e municipais (NAO e % do PIB; NAO e consolidado)", "Milhoes de reais", "valores de 1991-1994 vem de moedas anteriores convertidas; ordem de grandeza nao comparavel com os saldos atuais"),
}
data = {}
(P / "series").mkdir(exist_ok=True); (P / "derivado").mkdir(exist_ok=True)
for c, (nome, defin, un, nota) in S.items():
    data[c] = load(c)
    with open(P / "series" / f"{nome}_sgs{c}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow("indicador,fonte,definicao_linha,ano,mes_ou_trimestre,valor,unidade,nota,vintage".split(","))
        for (a, m), v in sorted(data[c].items()):
            w.writerow([nome, f"BCB SGS {c}", defin, a, m, v, un, nota, vint(f"sgs_{c}.json")])

# 3546 x 13621 (caixa) x 13982 (liquidez): ultimo dia util do mes
def diario(c, tags):
    out = {}
    for tag in tags:
        for x in json.load(open(P / f"bruto/sgs_{c}_{tag}.json")):
            out[(int(x["data"][6:]), int(x["data"][3:5]), int(x["data"][:2]))] = float(x["valor"])
    return out
def fim_mes(daily):
    last = {}
    for (a, m, d), v in sorted(daily.items()): last[(a, m)] = (d, v)
    return last
caixa = fim_mes(diario(13621, ["1998-2007", "2008-2017", "2018-2026_repeticao"]))
liq = fim_mes(diario(13982, ["2008-2017", "2018-2026"]))
ks = sorted(k for k in caixa if k in data[3546])
with open(P / "derivado/conferencia_reservas_3546_vs_13621_13982.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ano", "mes", "reservas_3546", "caixa_13621_ultimo_dia_util", "dif_3546_menos_caixa", "liquidez_13982_ultimo_dia_util", "dif_3546_menos_liquidez"])
    for k in sorted(set(caixa) | set(liq)):
        if k not in data[3546]: continue
        c = caixa.get(k, (None, None))[1]; l = liq.get(k, (None, None))[1]
        w.writerow([k[0], k[1], data[3546][k], c, "" if c is None else data[3546][k] - c, l, "" if l is None else data[3546][k] - l])
cx_igual = sum(1 for k in ks if caixa[k][1] == data[3546][k]); cx_abs = [abs(caixa[k][1] - data[3546][k]) for k in ks if caixa[k][1] != data[3546][k]]
kl = sorted(k for k in liq if k in data[3546]); lq_igual = sum(1 for k in kl if liq[k][1] == data[3546][k])
lq_prim_dif = next(k for k in kl if liq[k][1] != data[3546][k])
# serie extra: liquidez, ultimo dia util do mes, 2008+ (valor observado de um dia; nao e media nem estimativa)
nomeL = "reservas_internacionais_liquidez_fim_de_mes_usd_mi"
defL = "Reservas internacionais, conceito liquidez (SGS 13982, diaria): valor do ultimo dia util COM DADO do mes (valor observado, nao media, nao estimado)"
with open(P / "series" / f"{nomeL}_sgs13982.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow("indicador,fonte,definicao_linha,ano,mes_ou_trimestre,valor,unidade,nota,vintage".split(","))
    for (a, m), (d, v) in sorted(liq.items()):
        w.writerow([nomeL, "BCB SGS 13982", defL, a, m, v, "US$ milhoes", f"dado de {d:02d}/{m:02d}/{a}; serie diaria comeca em 02/01/2008" + ("; MES INCOMPLETO (ultimo dado do mes ate a coleta)" if (a, m) == (2026, 10) else ""), vint("sgs_13982_2008-2017.json") + " ; " + vint("sgs_13982_2018-2026.json")])
liqtab = {f"{a}-12": liq.get((a, 12)) for a in (2010, 2016, 2018, 2022)}
liq_ult = max(liq)

# Sobreposicao DBGG
nova, ant = data[13762], data[4537]
meses = sorted(k for k in nova if k in ant)
rows = [(k, nova[k], ant[k], round(ant[k] - nova[k], 2)) for k in meses]
with open(P / "derivado/sobreposicao_dbgg.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ano", "mes", "dbgg_metodologia_2008_sgs13762", "dbgg_metodologia_ate_2007_sgs4537", "diferenca_antiga_menos_2008_pp", "janela_do_preregistro_2006_2025"])
    for (a, m), n, o, df in rows: w.writerow([a, m, n, o, df, "sim" if a <= 2025 else "nao (2026, fora da janela citada no preregistro)"])
def stats(sub):
    ds = [r[3] for r in sub]
    return dict(n=len(ds), media=round(st.mean(ds), 3), dp=round(st.stdev(ds), 3), min=min(ds), max=max(ds), mediana=round(st.median(ds), 3),
                ini=sub[0][0], fim=sub[-1][0])
sob = {"2006-12 a 2025-12": stats([r for r in rows if r[0][0] <= 2025]), "2006-12 a ultimo mes": stats(rows)}
por_ano = {}
for r in rows: por_ano.setdefault(r[0][0], []).append(r[3])
sob_ano = {a: (round(st.mean(v), 2), len(v), min(v), max(v)) for a, v in por_ano.items()}

# Sobreposicao familias
def ov(old, new):
    ks = sorted(k for k in data[old] if k in data[new])
    return [(k, data[new][k], data[old][k], round(data[old][k] - data[new][k], 2)) for k in ks]
f1, f2 = ov(19882, 29037), ov(19881, 29038)
with open(P / "derivado/sobreposicao_endividamento_familias.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["par", "ano", "mes", "serie_nova", "serie_antiga", "diferenca_antiga_menos_nova"])
    for nome, rr in (("19882_vs_29037", f1), ("19881_vs_29038", f2)):
        for (a, m), n, o, df in rr: w.writerow([nome, a, m, n, o, df])
def fstats(rr):
    ds = [r[3] for r in rr]; return dict(n=len(ds), media=round(st.mean(ds), 3), dp=round(st.stdev(ds), 3), min=min(ds), max=max(ds), ini=rr[0][0], fim=rr[-1][0],
        n_iguais=sum(1 for d in ds if d == 0))
fam = {"19882_vs_29037": fstats(f1), "19881_vs_29038": fstats(f2)}
fam_ano = {}
for nome, rr in (("19882_vs_29037", f1), ("19881_vs_29038", f2)):
    t = {}
    for r in rr: t.setdefault(r[0][0], []).append(r[3])
    fam_ano[nome] = {a: round(st.mean(v), 2) for a, v in t.items()}

# valores-chave
chaves = [(1994, 12), (2002, 12), (2010, 12), (2016, 12), (2018, 12), (2022, 12)]
tab = {}
for c in S:
    ult = max(data[c]); ini = min(data[c])
    tab[c] = dict(nome=S[c][0], ini=ini, ult=ult, n=len(data[c]), ult_v=data[c][ult], chaves={f"{a}-{m:02d}": data[c].get((a, m)) for a, m in chaves})
json.dump(dict(tab=tab, sob=sob, sob_ano=sob_ano, fam=fam, fam_ano=fam_ano,
               reservas=dict(n_caixa=len(ks), caixa_iguais=cx_igual, caixa_dif_max=max(cx_abs), caixa_dif_min=min(cx_abs), n_liq=len(kl), liq_iguais=lq_igual, liq_primeira_dif=lq_prim_dif,
                             liq_dez=liqtab, liq_ult=(liq_ult, liq[liq_ult])),
               ref_ri=[(r[0], r[3]) for r in rows if r[0] in ((2006, 12), (2007, 12), (2008, 1))],
               valores_dbgg_ri=[(r[0], r[1], r[2]) for r in rows if r[0] in ((2006, 12), (2007, 12), (2008, 1))]),
          open(P / "derivado/_resumo.json", "w"), ensure_ascii=False, indent=1, default=str)
print("ok")
