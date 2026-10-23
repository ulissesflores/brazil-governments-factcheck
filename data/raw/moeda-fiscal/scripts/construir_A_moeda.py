"""Bloco A (moeda): Selic over, meta Copom, juro real ex-post, credito % PIB, compulsorios, multiplicadores e velocidade.
Le SO bruto em disco (moeda-fiscal/bruto e monetario/saida); sem rede. Rodar: python3 -I construir_A_moeda.py
Saidas: series/*.csv (formato longo) e derivado/conferencia_selic.csv."""
import csv, json, math, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import PASTA, DADOS, ckan, escrever, fmt, ipea, manifest, sgs, vintage

M = manifest()
# mes do download: valores de "acumulada no mes" desse mes sao parciais e ficam de fora
DL = max(v[0] for v in M.values())[:7]
DL_A, DL_M = int(DL[:4]), int(DL[5:7])
HOJE = max(v[0] for v in M.values())[:10]


def meta_ipea(cod):
    """Metadado do Ipeadata: arquivo proprio desta pasta; se faltar, o catalogo completo ja hasheado em monetario/bruto."""
    p = PASTA / f"bruto/ipea/{cod}_metadados.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))["value"][0]
        except Exception:
            pass
    cat = json.loads((DADOS / "monetario/bruto/ipea_METADADOS_catalogo_completo.json").read_text(encoding="utf-8"))["value"]
    return next(r for r in cat if r["SERCODIGO"] == cod)


# ---------------------------------------------------------------- Selic over mensal
def serie_mensal_ipea(cod, rotulo, nota_extra=""):
    md = meta_ipea(cod)
    vint = vintage(f"bruto/ipea/{cod}.json")
    linhas, dados = [], {}
    for a, m, d, v in ipea(f"bruto/ipea/{cod}.json"):
        if v is None:
            continue
        if (a, m) >= (DL_A, DL_M):
            continue  # mes corrente do download: parcial
        dados[(a, m)] = v
        linhas.append(dict(indicador="selic_over_mensal", fonte=f"Ipeadata {cod} ({md.get('FNTSIGLA','')})",
                           definicao_linha=md["SERNOME"], ano=a, mes_ou_trimestre=m, valor=fmt(v),
                           unidade=f"{md.get('UNINOME','')} (metadado Ipeadata)", nota=nota_extra, vintage=vint))
    return linhas, dados


ip_pan, d_pan = serie_mensal_ipea("PAN12_TJOVER12", "pan", "Ipeadata: percentagem anualizada, elaboracao Ipea; coincide com (1+BM12_TJOVER12/100)^12-1 (ver derivado/conferencia_selic.csv)")
ip_bm, d_bm = serie_mensal_ipea("BM12_TJOVER12", "bm", "mes corrente do download excluido (dado parcial segundo o metadado do Ipeadata)")
escrever("selic_over_mensal_ipeadata_PAN12_TJOVER12", ip_pan)
escrever("selic_over_mensal_ipeadata_BM12_TJOVER12", ip_bm)

c4390 = ckan(4390)
d_4390, l4390 = {}, []
for dd, mm, aa, v in sgs("bruto/bcb/sgs_4390.json"):
    if v is None or (aa, mm) >= (DL_A, DL_M):
        continue
    d_4390[(aa, mm)] = v
    l4390.append(dict(indicador="selic_over_mensal", fonte="BCB SGS 4390", definicao_linha=c4390["title"], ano=aa,
                      mes_ou_trimestre=mm, valor=fmt(v), unidade=f"% a.m. ({c4390['unidade_medida']})", nota="",
                      vintage=vintage("bruto/bcb/sgs_4390.json")))
escrever("selic_over_mensal_sgs4390", l4390)

# conferencia entre as tres fontes de Selic mensal (sem escolher vencedora)
anualiz = {k: ((1 + v / 100) ** 12 - 1) * 100 for k, v in d_bm.items()}
conf = []
for nome, (x, y) in {"BM12_vs_SGS4390": (d_bm, d_4390), "PAN12_vs_BM12_anualizado": (d_pan, anualiz)}.items():
    comuns = sorted(set(x) & set(y))
    difs = [(k, x[k], y[k]) for k in comuns if abs(x[k] - y[k]) > 0.005]
    conf.append(dict(par=nome, meses_em_comum=len(comuns), primeiro=f"{comuns[0][0]}-{comuns[0][1]:02d}" if comuns else "",
                     ultimo=f"{comuns[-1][0]}-{comuns[-1][1]:02d}" if comuns else "",
                     meses_diferentes_gt_0_005_pp=len(difs),
                     maior_diferenca_pp=max((abs(a - b) for _, a, b in difs), default=0),
                     exemplos=";".join(f"{k[0]}-{k[1]:02d}:{a}|{b}" for k, a, b in difs[:5])))
(PASTA / "derivado").mkdir(exist_ok=True)
with (PASTA / "derivado/conferencia_selic.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(conf[0]), lineterminator="\n")
    w.writeheader(); w.writerows(conf)

# ---------------------------------------------------------------- meta Selic (Copom)
meta_dia = {}
JAN432 = ("1996-2005", "2006-2015", "2016-2025", "2026")
for tag in JAN432:
    for dd, mm, aa, v in sgs(f"bruto/bcb/sgs_432_{tag}.json"):
        if v is not None:
            meta_dia[(aa, mm, dd)] = v
c432 = ckan(432)
futuras = sorted(k for k in meta_dia if f"{k[0]}-{k[1]:02d}-{k[2]:02d}" > HOJE)
for k in futuras:
    del meta_dia[k]
ult = defaultdict(dict)
for (a, m, d), v in sorted(meta_dia.items()):
    ult[(a, m)] = (d, v)
l432 = []
for (a, m), (d, v) in sorted(ult.items()):
    l432.append(dict(indicador="selic_meta_copom_fim_de_mes", fonte="BCB SGS 432", definicao_linha=c432["title"], ano=a,
                     mes_ou_trimestre=m, valor=fmt(v), unidade=f"% a.a. ({c432['unidade_medida']})",
                     nota=f"valor do ultimo dia com dado no mes (dia {d:02d})", vintage="; ".join(vintage(f"bruto/bcb/sgs_432_{t}.json") for t in JAN432)))
escrever("selic_meta_copom_fim_de_mes_sgs432", l432)

# mudancas da meta (datas em que o valor muda), a partir do diario
lm, prev = [], None
for (a, m, d), v in sorted(meta_dia.items()):
    if prev is not None and v != prev:
        lm.append(dict(indicador="selic_meta_copom_mudanca", fonte="BCB SGS 432", definicao_linha=c432["title"], ano=a,
                       mes_ou_trimestre=m, valor=fmt(v), unidade="% a.a.",
                       nota=f"dia {d:02d}; de {prev} para {v}", vintage="derivado do diario SGS 432 (4 janelas)"))
    prev = v
escrever("selic_meta_copom_mudancas_sgs432", lm)
primeiro_432 = min(meta_dia)

# Ipeadata BM366 (meta Copom diaria) - cobertura propria
bm366 = {}
for a, m, d, v in ipea("bruto/ipea/BM366_TJOVER366.json"):
    if v is not None and f"{a}-{m:02d}-{d:02d}" <= HOJE:
        bm366[(a, m, d)] = v
ult2 = defaultdict(dict)
for (a, m, d), v in sorted(bm366.items()):
    ult2[(a, m)] = (d, v)
md366 = meta_ipea("BM366_TJOVER366")
l366 = [dict(indicador="selic_meta_copom_fim_de_mes", fonte="Ipeadata BM366_TJOVER366", definicao_linha=md366["SERNOME"],
             ano=a, mes_ou_trimestre=m, valor=fmt(v), unidade=f"% a.a. (Ipeadata: {md366.get('UNINOME','')})",
             nota=f"valor do ultimo dia com dado no mes (dia {d:02d})", vintage=vintage("bruto/ipea/BM366_TJOVER366.json"))
        for (a, m), (d, v) in sorted(ult2.items())]
escrever("selic_meta_copom_fim_de_mes_ipeadata_BM366", l366)

# ---------------------------------------------------------------- juro real ex-post
def mensal_sgs(cod):
    return {(aa, mm): v for dd, mm, aa, v in sgs(f"bruto/bcb/sgs_{cod}.json") if v is not None}


def mensal_ipea(cod):
    return {(a, m): v for a, m, d, v in ipea(f"bruto/ipea/{cod}.json") if v is not None}


ipca, igpdi = mensal_ipea("PRECOS12_IPCAG12"), mensal_ipea("IGP12_IGPDIG12")
# conferencia: o SGS 433/190 (codigo ausente do CKAN) contra o Ipeadata, que traz o nome da serie no metadado
conf2 = []
BIG = {}  # meses em que SGS e Ipeadata divergem mais de 0,5 pp
for nome, cod, ipe in (("IPCA", 433, ipca), ("IGP-DI", 190, igpdi)):
    sg = mensal_sgs(cod)
    comuns = sorted(set(sg) & set(ipe))
    difs = sorted(((k, sg[k], ipe[k]) for k in comuns if abs(sg[k] - ipe[k]) > 0.0051), key=lambda t: -abs(t[1] - t[2]))
    BIG[nome] = {k: (a, b) for k, a, b in difs if abs(a - b) > 0.5}
    conf2.append(dict(par=f"SGS {cod} vs Ipeadata ({nome})", meses_em_comum=len(comuns), primeiro=f"{comuns[0][0]}-{comuns[0][1]:02d}",
                      ultimo=f"{comuns[-1][0]}-{comuns[-1][1]:02d}", meses_diferentes_gt_0_005_pp=len(difs),
                      maior_diferenca_pp=max((abs(a - b) for _, a, b in difs), default=0),
                      exemplos=";".join(f"{k[0]}-{k[1]:02d}:{a}|{b}" for k, a, b in difs[:5])))
with (PASTA / "derivado/conferencia_deflatores.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(conf2[0]), lineterminator="\n")
    w.writeheader(); w.writerows(conf2)
SEL = dict(d_bm)  # 1974+, Ipeadata BM12_TJOVER12 (% a.m.)
FILL = set()
for k, v in d_pan.items():  # meses nulos em BM12 (1986-03 a 05) existem em PAN12 (anualizada): de-anualiza
    if k not in SEL:
        SEL[k] = ((1 + v / 100) ** (1 / 12) - 1) * 100
        FILL.add(k)
for nome, ind, serie, cod, arqdefl, fdefl in (("ipca", "IPCA", ipca, "PRECOS12_IPCAG12", "bruto/ipea/PRECOS12_IPCAG12.json", "Ipeadata PRECOS12_IPCAG12 (IBGE/SNIPC)"),
                                              ("igpdi", "IGP-DI", igpdi, "IGP12_IGPDIG12", "bruto/ipea/IGP12_IGPDIG12.json", "Ipeadata IGP12_IGPDIG12 (FGV)")):
    cinfo = {"title": meta_ipea(cod)["SERNOME"]}
    lm_, la_ = [], []
    reais = {}
    for k in sorted(set(SEL) & set(serie)):
        r = ((1 + SEL[k] / 100) / (1 + serie[k] / 100) - 1) * 100
        reais[k] = r
        lm_.append(dict(indicador=f"juro_real_ex_post_mensal_{nome}", fonte=f"derivado: Ipeadata BM12_TJOVER12 e {fdefl}",
                        definicao_linha=f"((1+Selic over do mes)/(1+{ind} do mes)-1)*100, mesmo mes (ex-post)", ano=k[0],
                        mes_ou_trimestre=k[1], valor=fmt(r), unidade="% ao mes, real",
                        nota=f"Selic over {SEL[k]} % a.m.; {ind} {serie[k]} % a.m. ({cinfo['title']})" + ("; Selic mensal derivada de PAN12 por (1+a)^(1/12)-1 porque BM12_TJOVER12 e nulo neste mes" if k in FILL else "") + (f"; ATENCAO: SGS {433 if ind == 'IPCA' else 190} traz {BIG[ind][k][0]} e o Ipeadata {BIG[ind][k][1]} neste mes (divergencia > 0,5 pp); usado o Ipeadata" if k in BIG.get(ind, {}) else ""),
                        vintage=vintage("bruto/ipea/BM12_TJOVER12.json") + " | " + vintage(arqdefl)))
    escrever(f"juro_real_ex_post_mensal_{nome}", lm_)
    anos = sorted({k[0] for k in reais})
    for a in anos:
        meses = [(a, m) for m in range(1, 13)]
        if not all(k in reais for k in meses):
            continue  # ano incompleto: nao calculado
        fs = math.prod(1 + SEL[k] / 100 for k in meses)
        fp = math.prod(1 + serie[k] / 100 for k in meses)
        la_.append(dict(indicador=f"juro_real_ex_post_anual_{nome}", fonte=f"derivado: Ipeadata BM12_TJOVER12 e {fdefl}",
                        definicao_linha=f"(Selic over acumulada jan-dez / {ind} acumulado jan-dez - 1)*100, composicao de 12 taxas mensais",
                        ano=a, valor=fmt((fs / fp - 1) * 100), unidade="% ao ano, real",
                        nota=f"Selic over acumulada {(fs-1)*100:.6g} %; {ind} acumulado {(fp-1)*100:.6g} %",
                        vintage=vintage("bruto/ipea/BM12_TJOVER12.json") + " | " + vintage(arqdefl)))
    escrever(f"juro_real_ex_post_anual_{nome}", la_)

# ---------------------------------------------------------------- credito % PIB (uma base por codigo SGS)
def serie_sgs_mensal(cod, indicador, nota_fn=None, excluir_parcial=False):
    c = ckan(cod)
    arq = f"bruto/bcb/sgs_{cod}.json"
    ini = c.get("inicio_periodo") or ""
    # inicio_periodo vem em dd-mm-aaaa ou aaaa-mm-dd
    if ini and ini[2] == "-":
        ini_ym = (int(ini[6:10]), int(ini[3:5]))
    elif ini:
        ini_ym = (int(ini[:4]), int(ini[5:7]))
    else:
        ini_ym = None
    out = []
    for dd, mm, aa, v in sgs(arq):
        if v is None:
            continue
        if excluir_parcial and (aa, mm) >= (DL_A, DL_M):
            continue
        nota = ""
        if ini_ym and (aa, mm) < ini_ym:
            nota = f"antes do inicio_periodo declarado no catalogo CKAN do BCB ({ini_ym[0]}-{ini_ym[1]:02d}); metodologia dessas observacoes nao documentada no catalogo"
        if nota_fn:
            nota = (nota + " " + nota_fn(aa, mm)).strip()
        out.append(dict(indicador=indicador, fonte=f"BCB SGS {cod}", definicao_linha=c["title"], ano=aa, mes_ou_trimestre=mm,
                        valor=fmt(v), unidade=c.get("unidade_medida", ""), nota=nota, vintage=vintage(arq)))
    return out


credito = [(20622, "credito_sfn_total_pib"), (20625, "credito_sfn_recursos_livres_pib"), (20628, "credito_sfn_recursos_direcionados_pib"),
           (28215, "credito_ampliado_total_pib"), (28217, "credito_ampliado_empresas_e_familias_pib"),
           (28867, "credito_ampliado_empresas_pib"), (28868, "credito_ampliado_familias_pib"),
           (22052, "credito_sfn_setor_privado_total_rs_mi"), (22051, "credito_sfn_setor_publico_total_rs_mi")]
for cod, ind in credito:
    escrever(f"{ind}_sgs{cod}", serie_sgs_mensal(cod, ind))

# ---------------------------------------------------------------- compulsorios (saldos)
comp = [(17633, "compulsorios_saldo_total"), (1849, "compulsorios_recursos_a_vista_em_especie"),
        (1848, "compulsorios_poupanca_em_especie"), (1850, "compulsorios_depositos_a_prazo_em_especie"),
        (1797, "compulsorios_exigibilidade_adicional_em_especie"), (1828, "base_ampliada_depositos_compulsorios_em_especie"),
        (17624, "insuficiencia_direcionamento_credito_total"), (17625, "outros_recolhimentos_total")]
for cod, ind in comp:
    escrever(f"{ind}_sgs{cod}", serie_sgs_mensal(cod, ind))

# ---------------------------------------------------------------- multiplicadores e velocidade (derivados de monetario/saida)
MON = DADOS / "monetario/saida"
mens = list(csv.DictReader((MON / "mensal.csv").open(encoding="utf-8")))
anual = list(csv.DictReader((MON / "anual.csv").open(encoding="utf-8")))
mon_man = {}
for l in (DADOS / "monetario/manifest.jsonl").read_text(encoding="utf-8").splitlines():
    r = json.loads(l); mon_man[r["arquivo"]] = r
ARQ_M, ARQ_A = "monetario/saida/mensal.csv", "monetario/saida/anual.csv"


def f(x):
    return float(x) if x not in ("", None) else None


def mult(num, den, indicador, nome, regime):
    out = []
    for r in mens:
        n, d = f(r[num]), f(r[den])
        if n is None or d is None or d == 0:
            continue
        a, m = int(r["ym"][:4]), int(r["ym"][5:7])
        out.append(dict(indicador=indicador, fonte=f"derivado de {ARQ_M} (colunas {num} e {den}; origem BCB SGS/CKAN, ver monetario/RESULTADO.md)",
                        definicao_linha=f"{num} / {den}, saldos de fim de mes na mesma moeda do mes; regime de agregados: {regime}",
                        ano=a, mes_ou_trimestre=m, valor=fmt(n / d), unidade="razao (adimensional)",
                        nota="regimes de M1/M3 nunca emendados (monetario/RESULTADO.md secao 1.4)",
                        vintage=f"{ARQ_M} (construir.py da pasta monetario; bruto hasheado em monetario/manifest.jsonl)"))
    escrever(nome, out)


mult("M1_fim", "M0_fim", "multiplicador_M1_M0", "multiplicador_M1_M0_conceito_antigo", "M1 conceito antigo (SGS 1827), 1946-02 a 2018-06")
mult("M1_novo", "M0_fim", "multiplicador_M1_M0", "multiplicador_M1_M0_novo", "M1 Novo (SGS 27791), 2002-01 em diante")
mult("M3_reg2001", "M0_fim", "multiplicador_M3_M0", "multiplicador_M3_M0_regime2001", "M3 regime 2001 (SGS 1840), 1988-08 a 2018-06")
mult("M3_novo", "M0_fim", "multiplicador_M3_M0", "multiplicador_M3_M0_novo", "M3 Novo (SGS 27813), 2001-12 em diante")

for col, nome, regime in (("M1_med12_pib_pct", "velocidade_PIB_M1_media12_conceito_antigo", "M1 conceito antigo"),
                          ("M1_novo_med12_pib_pct", "velocidade_PIB_M1_media12_novo", "M1 Novo"),
                          ("M1_dez_pib_pct", "velocidade_PIB_M1_dezembro_conceito_antigo", "M1 conceito antigo, saldo de dezembro"),
                          ("M1_novo_dez_pib_pct", "velocidade_PIB_M1_dezembro_novo", "M1 Novo, saldo de dezembro")):
    out = []
    for r in anual:
        p = f(r[col])
        if p is None or p == 0:
            continue
        nota = "media dos 12 saldos mensais / PIB do ano" if "med12" in col else "saldo de dezembro / PIB do ano; distorcido em inflacao alta (monetario/RESULTADO.md secao 1.6)"
        out.append(dict(indicador="velocidade_PIB_M1", fonte=f"derivado de {ARQ_A} (coluna {col}; PIB de IBGE/Ipeadata, ver monetario/RESULTADO.md)",
                        definicao_linha=f"100 / ({col}) = PIB / M1; {regime}", ano=int(r["ano"]), valor=fmt(100 / p),
                        unidade="vezes por ano (PIB / M1)", nota=nota, vintage=f"{ARQ_A} (construir.py da pasta monetario)"))
    escrever(nome, out)

print("ok; mes do download", DL, "; datas futuras removidas da meta 432:", futuras, "; primeira data 432:", primeiro_432)
