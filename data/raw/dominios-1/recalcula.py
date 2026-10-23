#!/usr/bin/env python3
"""Recalcula, SEM REDE, as series dos dominios-1 a partir de ./bruto e gera series/*.csv, janelas.csv, quebras.csv.

Uso:  python3 -I recalcula.py
Antes de ler, confere o sha256 de cada arquivo bruto contra manifest.jsonl (cadeia de hash).
Dominios: edu, mor, tbl, pre, ass, mat. Sem serie comparavel (cul, laz, tra e partes de edu/mor/pre/ass):
ver busca-sem-serie.csv e RESULTADO.md.
"""
import csv, datetime, gzip, hashlib, html, json, os, re, sys, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(AQUI, "bruto")
OUT = os.path.join(AQUI, "series")
os.makedirs(OUT, exist_ok=True)
MANDATOS = "/Users/ulissesflores/Developer/brazil-governments-factcheck/data/curated/mandatos.csv"
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage", "dependente_de_regra"]


# ---------- integridade: sha256 do bruto lido == manifest ----------
def verifica_manifest():
    man = os.path.join(AQUI, "manifest.jsonl")
    ok = ruim = 0
    prev = hashlib.sha256(b"").hexdigest()
    for linha in open(man, "rb"):
        r = json.loads(linha)
        if r["prev_hash"] != prev:
            print("CADEIA QUEBRADA em seq", r["seq"]); sys.exit(1)
        prev = hashlib.sha256(linha).hexdigest()
        p = os.path.join(AQUI, r["arquivo"])
        if os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == r["sha256"]:
            ok += 1
        else:
            ruim += 1; print("MANIFEST DIVERGE:", r["arquivo"])
    print(f"manifest: {ok} arquivos conferem, {ruim} divergem; cabeca da cadeia {prev[:16]}")
    if ruim: sys.exit(1)


# ---------- leitores ----------
def jload(nome):
    b = open(os.path.join(B, nome), "rb").read()
    if b[:2] == b"\x1f\x8b": b = gzip.decompress(b)
    return json.loads(b)


def ipea(sercodigo, nivel="Brasil"):
    """[(ano, valor)] do Ipeadata OData bruto, nivel Brasil (ou '' para series nacionais sem nivel)."""
    v = jload(f"ipea_{sercodigo}.json")["value"]
    return [(int(r["VALDATA"][:4]), r["VALVALOR"]) for r in v if r["NIVNOME"] == nivel and r["VALVALOR"] is not None]


def ipea_mensal(sercodigo):
    v = jload(f"ipea_{sercodigo}.json")["value"]
    return [(r["VALDATA"][:7], r["VALVALOR"]) for r in v if r["VALVALOR"] is not None]


def ipea_meta(sercodigo):
    m = jload(f"meta/ipea_meta_{sercodigo}.json")["value"][0]
    return m


def sidra_series(nome):
    """Achata o JSON do SIDRA em lista de dicts: variavel, classificacoes{id:cat}, ano, valor(float|None)."""
    out = []
    for var in jload(nome):
        for res in var["resultados"]:
            cl = {c["id"]: list(c["categoria"].items())[0] for c in res["classificacoes"]}
            for s in res["series"]:
                for ano, val in s["serie"].items():
                    try: f = float(val)
                    except ValueError: f = None
                    out.append({"var": var["id"], "cl": cl, "ano": int(ano[:4]), "v": f})
    return out


# ---------- governos e janelas ----------
def governos():
    gs = []
    for r in csv.DictReader(open(MANDATOS, encoding="utf-8")):
        gs.append({"id": r["id"], "nome": r["nome"], "ini": datetime.date.fromisoformat(r["posse"]),
                   "fim": datetime.date.fromisoformat(r["saida"])})
    return gs


def governo_do_ano(gs, ano):
    """Regra fixa: o ano pertence ao governo que ocupa o cargo em 1 de julho (ponto medio) do ano."""
    d = datetime.date(ano, 7, 1)
    for g in gs:
        if g["ini"] <= d < g["fim"]:
            return g
    return None


def janelas(indicador_id, pontos, gs, segmento_de):
    """pontos: [(ano, valor)] de UMA serie primaria. Devolve linhas de janelas.csv, uma por governo."""
    linhas = []
    for g in gs:
        obs = sorted((a, v) for a, v in pontos if governo_do_ano(gs, a) is g)
        seg = sorted({segmento_de(a) for a, _ in obs})
        linhas.append({
            "indicador": indicador_id, "governo": g["nome"], "inicio": g["ini"].isoformat(), "fim": g["fim"].isoformat(),
            "media": f"{sum(v for _, v in obs) / len(obs):.4f}" if obs else "",
            "valor_inicial": f"{obs[0][1]:.4f}" if obs else "",
            "valor_final": f"{obs[-1][1]:.4f}" if obs else "",
            "n_anos": len(obs),
            "segmento_metodo": "; ".join(seg) if obs else "sem observacao na janela",
        })
    return linhas


def tabnet_sinasc():
    """{ano: {'nenhuma','1a3','4a6','1a6ne','7mais','ign','total'}} do HTML bruto do TabNet (colunas ';')."""
    txt = open(os.path.join(B, "tabnet_sinasc_prenatal_ano_1994_2025.html"), "rb").read().decode("latin-1")
    out = {}
    for ln in txt.splitlines():
        m = re.match(r'^"(\d{4})";(.*)$', ln.strip())
        if not m: continue
        v = [0 if x == "-" else int(x) for x in m.group(2).split(";")]
        out[int(m.group(1))] = dict(zip(["nenhuma", "1a3", "4a6", "1a6ne", "7mais", "ign", "total"], v))
    return out


# ---------- construtores de series (formato longo) ----------
ROWS = {"edu": [], "mor": [], "tbl": [], "pre": [], "ass": [], "mat": []}


def L(dom, ind, fonte, defn, ano, valor, un, nota="", dep=None, vint=None):
    ROWS[dom].append({"indicador": ind, "fonte": fonte, "definicao_linha": defn, "ano": ano,
                      "valor": f"{valor:.4f}".rstrip("0").rstrip(".") if isinstance(valor, float) else valor,
                      "unidade": un, "nota": nota, "vintage": vint, "dependente_de_regra": dep})


def cat(rec, clid):
    return rec["cl"][clid][0]


def sid(nome, **filtros):
    """Valores SIDRA com classificacao fixada: filtros={'61':'2512', ...} (ids de categoria); devolve {ano: valor}."""
    out = {}
    for r in sidra_series(nome):
        if all(cat(r, k) == v for k, v in filtros.items()) and r["v"] is not None:
            out[r["ano"]] = r["v"]
    return out


def build_edu():
    A = "edu_analfab15"
    d = "pessoas de 15 anos ou mais que nao sabem ler e escrever um bilhete simples, % da populacao de 15+"
    m = ipea_meta("ADH_T_ANALF15M")
    for a, v in ipea("ADH_T_ANALF15M"):
        L("edu", A, "Atlas-DH-Censo(ADH_T_ANALF15M)", d + "; Censos 1991/2000/2010/2022", a, v, "%",
          f"primaria; Ipeadata ADH_T_ANALF15M, SERATUALIZACAO {m['SERATUALIZACAO'][:10]}")
    for a, v in ipea("TXA15M7091"):
        L("edu", A, "Ipea-Atlas1998(TXA15M7091)", d + "; Censos 1970/1980/1991, processamento Atlas 1998", a, v, "%",
          "segmento anterior a 1991, fonte e processamento diferentes; ver quebras.csv")
    # recalculo independente a partir das tabelas do universo/amostra do Censo no SIDRA
    g15 = ["1143", "1144", "1145", "1146", "1147", "1148", "1149", "1150", "1151", "1152", "1153", "1154", "2503"]
    for ano in (1991, 2000):
        tot = sum(v for r in sidra_series("sidra_204_alfab_1991_2000.json") for v in [r["v"]]
                  if r["ano"] == ano and cat(r, "59") == "0" and cat(r, "58") in g15)
        nao = sum(r["v"] for r in sidra_series("sidra_204_alfab_1991_2000.json")
                  if r["ano"] == ano and cat(r, "59") == "1024" and cat(r, "58") in g15)
        L("edu", A, "IBGE-SIDRA-Censo(recalculo)", d + f"; tabela 204 (grupos de idade 15+), Censo {ano}", ano, 100 * nao / tot, "%",
          "sensibilidade: recalculo proprio")
    r10 = {r["var"]: r["v"] for r in sidra_series("sidra_3149_alfab_2010.json")}
    L("edu", A, "IBGE-SIDRA-Censo(recalculo)", d + "; tabela 3149 (universo), Censo 2010", 2010,
      100 * (r10["950"] - r10["2376"]) / r10["950"], "%", "sensibilidade: recalculo proprio")
    r22 = {cat(r, "59"): r["v"] for r in sidra_series("sidra_9542_alfab_2022.json")}
    L("edu", A, "IBGE-SIDRA-Censo(recalculo)", d + "; tabela 9542 (universo), Censo 2022", 2022,
      100 * r22["1024"] / r22["93024"], "%", "sensibilidade: recalculo proprio")
    # anual: PNAD (2004-2015), PNADC (2012-2025)
    for r in sidra_series("sidra_1187_alfab15_pnad_2004_2015.json"):
        if cat(r, "2") == "6794" and r["v"] is not None:
            L("edu", A, "IBGE-PNAD(IDS1187)", "100 - taxa de alfabetizacao 15+ (PNAD anual; Norte rural incluido desde 2004)",
              r["ano"], 100 - r["v"], "%", "sensibilidade anual; encerrada em 2015")
    for r in sidra_series("sidra_7113_analfab15_pnadc_2016_2025.json"):
        if r["v"] is not None:
            L("edu", A, "IBGE-PNADC(SIDRA7113)", "taxa de analfabetismo 15+ (PNADC anual, 5a visita)", r["ano"], r["v"], "%",
              "sensibilidade anual")
    for a, v in ipea("PNADCA_TXA15MUF"):
        L("edu", A, "IBGE-PNADC(Ipea PNADCA_TXA15MUF)", "taxa de analfabetismo 15+ (PNADC anual)", a, v, "%",
          "sensibilidade anual; inclui 2012-2015, sobreposicao com a PNAD")


def build_mor():
    # ----- agua: % de domicilios particulares permanentes com rede geral como forma de abastecimento (IBGE, Censo)
    A = "mor_agua_rede_geral"
    d = "domicilios particulares permanentes com abastecimento de agua por rede geral, % do total de domicilios"
    t91 = sid("sidra_179_agua_1991.json", **{"1": "0"})
    r91 = {r["cl"]["61"][0]: r["v"] for r in sidra_series("sidra_179_agua_1991.json")}
    L("mor", A, "IBGE-Censo(SIDRA)", d + "; 1991 = com+sem canalizacao interna, rede geral (tab. 179)", 1991,
      100 * (r91["1033"] + r91["1035"]) / r91["0"], "%", "primaria")
    r00 = {r["cl"]["61"][0]: r["v"] for r in sidra_series("sidra_1436_agua_2000.json")}
    L("mor", A, "IBGE-Censo(SIDRA)", d + "; 2000 tab. 1436", 2000, 100 * r00["92853"] / r00["0"], "%", "primaria")
    r10 = {r["cl"]["61"][0]: r["v"] for r in sidra_series("sidra_3217_agua_2010.json")}
    L("mor", A, "IBGE-Censo(SIDRA)", d + "; 2010 tab. 3217", 2010, 100 * r10["92853"] / r10["0"], "%", "primaria")
    r22 = {r["cl"]["301"][0]: r["v"] for r in sidra_series("sidra_6804_agua_2022.json")}
    L("mor", A, "IBGE-Censo(SIDRA)", d + "; 2022 tab. 6804 (domicilios ocupados, rede geral como principal forma)", 2022,
      100 * r22["31471"] / r22["72053"], "%", "primaria")
    for a, v in ipea("ADH_T_AGUA"):
        L("mor", "mor_agua_encanada_pop", "Atlas-DH-Censo(ADH_T_AGUA)",
          "populacao em domicilios com agua canalizada (qualquer origem) para um ou mais comodos, % da populacao", a, v, "%",
          "sensibilidade; definicao diferente (canalizacao, nao rede geral)")
    # ----- esgoto adequado: rede geral/pluvial + fossa septica, % do total de domicilios
    E = "mor_esgoto_adequado"
    de = "domicilios com escoadouro por rede geral (ou pluvial) ou fossa septica, % do total de domicilios"
    s91 = {r["cl"]["1612"][0]: r["v"] for r in sidra_series("sidra_256_esgoto_1991.json")}
    L("mor", E, "IBGE-Censo(SIDRA)", de + "; 1991 tab. 256, so instalacao sanitaria exclusiva do domicilio", 1991,
      100 * (s91["120451"] + s91["120452"]) / s91["0"], "%", "primaria; universo de 1991 = so exclusivas (sem compartilhadas)")
    s00 = {r["cl"]["11558"][0]: r["v"] for r in sidra_series("sidra_1437_esgoto_2000.json")}
    L("mor", E, "IBGE-Censo(SIDRA)", de + "; 2000 tab. 1437", 2000, 100 * (s00["92855"] + s00["92856"]) / s00["0"], "%", "primaria")
    s10 = {r["cl"]["299"][0]: r["v"] for r in sidra_series("sidra_3216_esgoto_2010.json")}
    L("mor", E, "IBGE-Censo(SIDRA)", de + "; 2010 tab. 3216 (banheiro exclusivo + sanitario)", 2010,
      100 * (s10["2945"] + s10["2946"] + s10["2959"] + s10["2960"]) / s10["0"], "%", "primaria")
    s22 = {r["cl"]["11558"][0]: r["v"] for r in sidra_series("sidra_6805_esgoto_2022.json")}
    L("mor", E, "IBGE-Censo(SIDRA)", de + "; 2022 tab. 6805 (rede/pluvial + fossa septica ligada ou nao)", 2022,
      100 * (s22["72110"] + s22["72111"] + s22["72112"]) / s22["46292"], "%", "primaria")
    for a, v in ipea("PDIAE"):
        L("mor", E, "Ipea-PDIAE(Atlas1998<=1991;SIDRA>=2000)", "mesma ideia; Ipeadata PDIAE, compilacao Ipea",
          a, v, "%", "sensibilidade/extensao: 1970-1991 vem do Atlas 1998, 2000+ das tabelas SIDRA; ver quebras.csv")
    for a, v in ipea("PDIEREDE"):
        L("mor", "mor_esgoto_rede", "IBGE-Censo(Ipeadata PDIEREDE)", "domicilios com esgoto por rede geral, % do total",
          a, v, "%", "sensibilidade")
    for a, v in ipea("ADH_T_LUZ"):
        L("mor", "mor_luz", "Atlas-DH-Censo(ADH_T_LUZ)", "populacao em domicilios com iluminacao eletrica, % da populacao",
          a, v, "%", "so 1991-2010 (19 anos): nao qualifica pela regra de cobertura; relatado mesmo assim")


def build_mat():
    d = tabnet_sinasc()
    for a in sorted(d):
        r = d[a]; conh = r["total"] - r["ign"]
        if a == 1994 or conh <= 0:
            continue  # 1994: 100% ignorado
        nota = "final" if a <= 2024 else "PRELIMINAR (2025): fora das janelas"
        if 100 * r["ign"] / r["total"] > 10:
            nota = "FORA_DA_JANELA: mais de 10% dos nascimentos com numero de consultas ignorado (regra fixa, ver RESULTADO)"
        L("mat", "mat_prenatal7", "MS-SINASC(TabNet)",
          "nascidos vivos (residencia da mae) cuja mae fez 7 ou mais consultas de pre-natal, % dos nascidos com numero de consultas informado",
          a, 100 * r["7mais"] / conh, "%", nota + f"; ignorado={100 * r['ign'] / r['total']:.1f}% dos nascimentos")
        L("mat", "mat_prenatal_ignorado", "MS-SINASC(TabNet)", "nascidos vivos com numero de consultas ignorado, % do total",
          a, 100 * r["ign"] / r["total"], "%", ("PRELIMINAR (2025): fora das janelas; " if a > 2024 else "") + "indicador de qualidade do registro")
        L("mat", "mat_prenatal_nenhuma", "MS-SINASC(TabNet)",
          "nascidos vivos cuja mae nao fez nenhuma consulta, % dos nascidos com numero informado", a, 100 * r["nenhuma"] / conh, "%", nota)


def build_tbl():
    for a, v in ipea("DISOC_INFI", nivel=""):
        L("tbl", "tbl_informalidade", "Ipea-PNAD(DISOC_INFI)",
          "(empregados sem carteira + conta propria) / (protegidos + sem carteira + conta propria), % (definicao I do Ipea; PNAD)",
          a, v, "%", "primaria; serie interrompida em 2014; sem 1994, 2000 e 2010 (anos de Censo / sem PNAD)")
    for r in sidra_series("sidra_4708_informalidade_pnadc_2016_2025.json"):
        if r["v"] is not None:
            L("tbl", "tbl_informalidade_ibge", "IBGE-PNADC(SIDRA4708)", "taxa de informalidade das pessoas ocupadas de 14+ (definicao IBGE/PNADC)",
              r["ano"], r["v"], "%", "OUTRA definicao; nao emendada com a do Ipea")
    ix = ipca_indice(); base = ix[(2025, 12)]
    nome_pnad = "IBGE-PNAD(SIDRA1871 deflacionado)"
    for r in sidra_series("sidra_1871_rendimento_nominal_pnad_2001_2015.json"):
        if cat(r, "2") == "6794" and cat(r, "12025") == "99149" and r["var"] == "778" and r["v"] is not None:
            L("tbl", "tbl_renda_trabalho_real", nome_pnad,
              "rendimento medio mensal de todos os trabalhos, ocupados 10+, PNAD (setembro), deflacionado pelo IPCA de setembro, em R$ de dez/2025",
              r["ano"], r["v"] * base / ix[(r["ano"], 9)], "R$ dez/2025", f"primaria (PNAD 2001-2015); nominal R$ {r['v']:.0f}; 2001-2015 = 15 anos, nao qualifica pela cobertura")
    for r in sidra_series("sidra_4027_rendimento_nominal_pnad15mais_2012_2015.json"):
        if cat(r, "2") == "6794" and cat(r, "12025") == "99149" and r["var"] == "4015" and r["v"] is not None:
            L("tbl", "tbl_renda_trabalho_real", "IBGE-PNAD(SIDRA4027 deflacionado, 15+)", "idem, ocupados 15+ (tabela 2012-2015)", r["ano"],
              r["v"] * base / ix[(r["ano"], 9)], "R$ dez/2025", f"sensibilidade; nominal R$ {r['v']:.0f}")
    for r in sidra_series("sidra_427_rendimento_real_pnad_1996_2006.json"):
        if r["var"] == "1906" and r["v"] is not None:
            L("tbl", "tbl_renda_trabalho_real", "IBGE-PNAD(SIDRA427 real divulgado)", "rendimento medio mensal REAL de todos os trabalhos, ocupados 10+ (valor como publicado pelo IBGE)",
              r["ano"], r["v"], "R$ (base de precos nao declarada nos metadados)", "sensibilidade 1996-2006, unica fonte para 1996-2000; em 2006 o valor real (795) fica perto do nominal (782), sugerindo precos de ~set/2006, sem confirmacao")
    for r in sidra_series("sidra_4660_rendimento_nominal_pnadc_2012_2025.json"):
        if r["var"] == "5929" and r["v"] is not None:
            med = sum(ix[(r["ano"], m)] for m in range(1, 13) if (r["ano"], m) in ix) / len([m for m in range(1, 13) if (r["ano"], m) in ix])
            L("tbl", "tbl_renda_trabalho_real", "IBGE-PNADC(SIDRA4660 nominal deflacionado)",
              "rendimento medio mensal habitual de todos os trabalhos, ocupados 14+, PNADC anual, deflacionado pela media anual do IPCA, em R$ de dez/2025",
              r["ano"], r["v"] * base / med, "R$ dez/2025", f"nominal R$ {r['v']:.0f}; 2012-2025 = 14 anos")
    for r in sidra_series("sidra_4660_rendimento_real_pnadc_2012_2025.json"):
        if r["var"] == "5933" and r["v"] is not None:
            L("tbl", "tbl_renda_trabalho_real", "IBGE-PNADC(SIDRA4660)",
              "rendimento medio mensal real, todos os trabalhos, habitual, ocupados 14+ (R$ a precos medios do ano da divulgacao, como publicado)",
              r["ano"], r["v"], "R$", "sensibilidade: valor real como publicado pelo IBGE (base de precos propria)")
    for a, v in ipea("PAN_RRPE", nivel=""):
        L("tbl", "tbl_renda_trabalho_real", "IBGE-PNADC(Ipea PAN_RRPE)", "rendimento real medio do trabalho principal efetivo (media anual da serie mensal)",
          a, v, "R$", "sensibilidade: outra variavel da mesma pesquisa")


def build_pre_ass():
    pib = dict(ipea("PAN_PIBPMV", nivel=""))  # R$ milhoes
    comp = {}
    for cod, nome in (("MPAS12_RESPRGPS12", "resultado"), ("MPAS12_ARRLIQ12", "arrecadacao_liquida"), ("MPAS12_BENPREV12", "beneficios")):
        porano = {}
        for ym, val in ipea_mensal(cod):
            porano.setdefault(int(ym[:4]), []).append(val)
        comp[nome] = {a: sum(v) for a, v in porano.items() if len(v) == 12}
    for nome, rot in (("resultado", "resultado primario do RGPS (arrecadacao liquida - beneficios previdenciarios)"),
                      ("arrecadacao_liquida", "arrecadacao liquida do RGPS"), ("beneficios", "beneficios previdenciarios do RGPS")):
        for a in sorted(comp[nome]):
            if a in pib:
                L("pre", f"pre_rgps_{nome}_pib", "MPS-fluxo-de-caixa(Ipeadata MPAS12_*) / IBGE-PIB(PAN_PIBPMV)",
                  f"{rot}, soma de 12 meses, % do PIB nominal", a, 100 * comp[nome][a] / (pib[a] * 1000), "% do PIB",
                  "serie mensal comeca em 2003-02: so anos completos 2004+ (22 anos): nao qualifica pela regra de cobertura",
                  )
    # ---- assistencia: BPC e PBF por 1000 habitantes
    pop = dict(ipea("DEPIS_POP", nivel=""))
    idos = dict(ipea("BPC_idos")); defi = dict(ipea("BPC_defi"))
    for a in sorted(idos):
        if a in defi and a in pop:
            anom = defi[a] < 1000  # 2016: 74 beneficios, valor incompativel com 2015 e 2017
            L("ass", "ass_bpc_por_mil_hab", "MDS-BPC(Ipeadata BPC_idos+BPC_defi) / IBGE-Pop(DEPIS_POP)",
              "beneficios do BPC (idosos + pessoas com deficiencia) em dezembro, por 1000 habitantes", a,
              1000 * (idos[a] + defi[a]) / pop[a], "por mil hab.",
              ("ANOMALIA de publicacao: BPC_defi = %d beneficios; mantido como publicado, fora das janelas. " % defi[a] if anom else "")
              + "regra de elegibilidade mudou (idade 70/67/65; criterio de renda); ver quebras.csv", )
    for a, v in sorted(ipea("FAM_PBF")):
        if a in pop:
            L("ass", "ass_pbf_familias_por_mil_hab", "MDS-PBF(Ipeadata FAM_PBF) / IBGE-Pop(DEPIS_POP)",
              "beneficios do Bolsa Familia/Auxilio Brasil em dezembro, por 1000 habitantes (programa criado em 2004)",
              a, 1000 * v / pop[a], "por mil hab.", "so 2004+ (22 anos): nao qualifica pela regra de cobertura; programa renomeado 2021-2023")


# ---------- SAEB: proficiencia media Brasil (rotulos dos graficos do INEP; extraidos com pdftotext -bbox) ----------
import subprocess


def _palavras(pdf, pagina):
    out = subprocess.run(["pdftotext", "-f", str(pagina), "-l", str(pagina), "-bbox", os.path.join(B, pdf), "-"],
                         capture_output=True, text=True).stdout
    return [(float(a), float(b), float(c), float(d), w) for a, b, c, d, w in
            re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', out)]


def saeb_presskit():
    """{(disciplina, etapa): {ano: valor}} do Press Kit Saeb 2019 (paginas 23=LP, 24=MT; 3 series por ano, y crescente = EM, anos finais, anos iniciais)."""
    res = {}
    for pag, disc in ((23, "LP"), (24, "MT")):
        ws = _palavras("doc/inep_presskit_saeb_2019.pdf", pag)
        lab = sorted(((x0 + x1) / 2, int(w)) for x0, y0, x1, y1, w in ws if re.fullmatch(r"(199[579]|200[13579]|201[13579])", w))
        nums = [((x0 + x1) / 2, (y0 + y1) / 2, int(w)) for x0, y0, x1, y1, w in ws if re.fullmatch(r"\d{3}", w)]
        for lx, ano in lab:
            c = sorted([(y, v) for x, y, v in nums if abs(x - lx) < 15 and 150 < v < 400])
            assert len(c) == 3, (disc, ano, c)
            for etapa, (_, v) in zip(("EM_3serie", "EF_9ano_8serie", "EF_5ano_4serie"), c):
                res.setdefault((disc, etapa), {})[ano] = v
    return res


def saeb_rel2023():
    """{(disciplina, etapa): {ano: valor}} 2011-2023 do Relatorio Saeb 2023 vol. 1 (graficos de proficiencia media)."""
    res = {}
    paginas = {49: ("LP", "EF_5ano_4serie"), 60: ("MT", "EF_5ano_4serie"), 83: ("LP", "EF_9ano_8serie"),
               93: ("MT", "EF_9ano_8serie"), 121: ("LP", "EM_3serie"), 130: ("MT", "EM_3serie")}
    for pag, chave in paginas.items():
        ws = _palavras("doc/inep_relatorio_saeb_2023_vol1.pdf", pag)
        lab = []
        for i, (x0, y0, x1, y1, w) in enumerate(ws):
            if w == "Saeb" and i + 1 < len(ws) and re.fullmatch(r"20\d\d", ws[i + 1][4]):
                lab.append(((x0 + ws[i + 1][2]) / 2, int(ws[i + 1][4])))
        nums = [((x0 + x1) / 2, (y0 + y1) / 2, int(w)) for x0, y0, x1, y1, w in ws if re.fullmatch(r"\d{3}", w) and 150 < int(w) < 400]
        cand = {ano: sorted((y, v) for x, y, v in nums if abs(x - lx) < 30) for lx, ano in lab}
        unico = {a: c[0] for a, c in cand.items() if len(c) == 1}
        assert len(lab) == 7 and unico, (pag, cand)
        ref = sum(y for y, _ in unico.values()) / len(unico)
        for ano, c in cand.items():
            y, v = min(c, key=lambda t: abs(t[0] - ref))
            res.setdefault(chave, {})[ano] = v
    return res


def build_saeb():
    pk, rl = saeb_presskit(), saeb_rel2023()
    nome = {"EF_5ano_4serie": "5o ano do EF (4a serie ate o EF de 8 anos)", "EF_9ano_8serie": "9o ano do EF (8a serie ate o EF de 8 anos)",
            "EM_3serie": "3a serie do ensino medio"}
    comp = []
    for (disc, etapa), serie in sorted(pk.items()):
        for ano, v in sorted(serie.items()):
            L("edu", f"edu_saeb_{disc}_{etapa}", "INEP-Saeb(PressKit2019)",
              f"proficiencia media Brasil, {'Lingua Portuguesa' if disc == 'LP' else 'Matematica'}, {nome[etapa]}; escala Saeb equalizada por TRI (0-500)",
              ano, float(v), "pontos", "rotulo do grafico do Press Kit; abrangencia varia por edicao (ver quebras.csv)")
    for (disc, etapa), serie in sorted(rl.items()):
        for ano, v in sorted(serie.items()):
            L("edu", f"edu_saeb_{disc}_{etapa}", "INEP-Saeb(Relatorio2023)",
              f"proficiencia media Brasil, {'Lingua Portuguesa' if disc == 'LP' else 'Matematica'}, {nome[etapa]}; escala Saeb equalizada por TRI (0-500)",
              ano, float(v), "pontos", "rotulo do grafico do Relatorio Saeb 2023 vol. 1")
            if ano in pk.get((disc, etapa), {}):
                comp.append((disc, etapa, ano, pk[(disc, etapa)][ano], v))
    return comp  # sobreposicao 2011-2019 entre as duas vintages


# ---------- limiares de elegibilidade (valor nominal e real) ----------
MESES = {m: i + 1 for i, m in enumerate("janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split())}


def legtxt(nome):
    pa = os.path.join(B, "doc", "leg", nome)
    if not os.path.exists(pa): pa = os.path.join(B, "doc", nome)
    t = open(pa, "rb").read().decode("latin-1")
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def data_assinatura(t):
    m = re.search(r"Bras[ií]lia, (\d+)(?:\s*[oº°])?\s+de (\w+) de (\d{4})", t) or re.search(r"\b(?:LEI|DECRETO)[^,]{0,25}, DE (\d+)(?:\s*[oº°])?\s+DE (\w+) DE (\d{4})", t, re.I)
    return datetime.date(int(m.group(3)), MESES[m.group(2).lower()], int(m.group(1)))


def ipca_indice():
    """{(ano, mes): indice} encadeado do IPCA mensal (SGS 433), base arbitraria; so para razoes entre meses."""
    idx, ac = {}, 1.0
    for r in jload("bcb_sgs433_ipca_mensal.json"):
        d, m, a = r["data"].split("/")
        ac *= 1 + float(r["valor"]) / 100
        idx[(int(a), int(m))] = ac
    return idx


def salmin_mensal():
    return {(int(ym[:4]), int(ym[5:7])): v for ym, v in ipea_mensal("MTE12_SALMIN12")}


# (arquivo, pobreza, extrema, trecho que deve existir no texto, nota)
PBF_EVENTOS = [
    ("dec_5209_2004.htm", 100, 50, r"R\$ 100,00 e R\$ 50,00", "Decreto 5.209/2004, art. 18"),
    ("dec_5749_2006.htm", 120, 60, r"R\$ 120,00 \(cento e vinte reais\) e R\$ 60,00", "Decreto 5.749/2006"),
    ("dec_6824_2009.htm", 137, 69, r"R\$ 137,00 \(cento e trinta e sete reais\) e R\$ 69,00", "Decreto 6.824/2009"),
    ("dec_6917_2009.htm", 140, 70, r"R\$ 140,00 \(cento e quarenta reais\) e R\$ 70,00", "Decreto 6.917/2009 (efeitos financeiros desde 1/9/2009)"),
    ("dec_8232_2014.htm", 154, 77, r"R\$ 154,00 \(cento e cinquenta e quatro reais\) e R\$ 77,00", "Decreto 8.232/2014"),
    ("dec_8794_2016.htm", 170, 85, r"R\$ 170,00 \(cento e setenta reais\) e de R\$ 85,00", "Decreto 8.794/2016"),
    ("dec_9396_2018.htm", 178, 89, r"R\$ 178,00 \(cento e setenta e oito reais\) e R\$ 89,00", "Decreto 9.396/2018"),
    ("dec_10852_2021_auxilio_brasil.htm", 200, 100, r"R\$ 100,00 \(cem reais\)", "Decreto 10.852/2021 (Auxilio Brasil substitui o Bolsa Familia)"),
    ("dec_11013_2022.htm", 210, 105, r"R\$ 210,00 \(duzentos e dez reais\)", "Decreto 11.013/2022"),
    ("dec_11566_2023.htm", 218, None, r"R\$ 218,00 \(duzentos e dezoito reais\)", "Decreto 11.566/2023 e Lei 14.601/2023 (linha unica)"),
]


def build_limiares():
    ix = ipca_indice(); base = ix[(2025, 12)]
    real = lambda nominal, a, m: nominal * base / ix[(a, m)]
    eventos = []
    for arq, pob, ext, rx, nota in PBF_EVENTOS:
        t = legtxt(arq)
        assert re.search(rx, t), (arq, rx)
        d = data_assinatura(t)
        if arq == "dec_6917_2009.htm": d = datetime.date(2009, 9, 1)  # efeitos financeiros declarados no proprio decreto
        eventos.append((d, pob, ext, nota))
    eventos.sort()
    ev_rows = []
    for d, pob, ext, nota in eventos:
        ev_rows.append({"programa": "Bolsa Familia/Auxilio Brasil", "data_vigencia": d.isoformat(), "instrumento": nota,
                        "linha_pobreza_nominal": pob, "linha_extrema_pobreza_nominal": ext if ext is not None else "",
                        "linha_pobreza_real_dez2025": f"{real(pob, d.year, d.month):.2f}",
                        "linha_extrema_pobreza_real_dez2025": f"{real(ext, d.year, d.month):.2f}" if ext is not None else ""})
    vigente = lambda ano: [e for e in eventos if e[0] <= datetime.date(ano, 12, 31)][-1] if eventos[0][0] <= datetime.date(ano, 12, 31) else None
    for ano in range(2004, 2026):
        e = vigente(ano)
        if not e: continue
        d, pob, ext, nota = e
        L("ass", "ass_pbf_limiar_pobreza_real", "Planalto(decretos/leis do PBF)+BCB-IPCA(SGS433)",
          "renda familiar per capita mensal maxima da linha de pobreza do programa, vigente em 31/dez, em R$ de dez/2025 (IPCA)",
          ano, real(pob, ano, 12), "R$ dez/2025", f"nominal R$ {pob}; {nota}; vigente desde {d.isoformat()}", dep="n/a (e a propria regra)")
        if ext is not None:
            L("ass", "ass_pbf_limiar_extrema_pobreza_real", "Planalto(decretos/leis do PBF)+BCB-IPCA(SGS433)",
              "idem, linha de extrema pobreza", ano, real(ext, ano, 12), "R$ dez/2025", f"nominal R$ {ext}; {nota}; vigente desde {d.isoformat()}",
              dep="n/a (e a propria regra)")
    # BPC: limiar de renda como fracao do salario minimo, em R$ reais; idade minima
    sm = salmin_mensal()
    t8742 = legtxt("planalto_lei_8742_loas.htm"); t14176 = legtxt("lei_14176_2021_bpc.htm"); t13981 = legtxt("lei_13981_2020_bpc.htm")
    assert re.search(r"inferior a 1/4 \(um quarto\) do salário mínimo", t8742)
    assert re.search(r"inferior a 1/2 \(meio\) salário-mínimo", t13981)
    assert re.search(r"para até 1/2 \(meio\) salário-mínimo", t14176)
    for ano in range(1996, 2026):
        smd = sm[(ano, 12)]
        L("ass", "ass_bpc_limiar_quarto_sm_real", "Planalto(Lei 8.742/1993 art. 20 par.3)+MTE(salario minimo)+BCB-IPCA",
          "1/4 do salario minimo per capita (criterio legal original do BPC), em R$ de dez/2025", ano, real(0.25 * smd, ano, 12), "R$ dez/2025",
          f"salario minimo dez/{ano} = R$ {smd}; texto legal vale de 1993 a hoje; STF/ADPF 662 e regulamento alteram a aplicacao (ver quebras.csv)",
          dep="n/a (e a propria regra)")
        if ano >= 2020:
            L("ass", "ass_bpc_limiar_meio_sm_real", "Planalto(Lei 13.981/2020; Lei 14.176/2021)+MTE+BCB-IPCA",
              "1/2 salario minimo per capita (texto da Lei 13.981/2020 e teto previsto na Lei 14.176/2021), em R$ de dez/2025", ano,
              real(0.5 * smd, ano, 12), "R$ dez/2025", "valor de REFERENCIA do texto legal; aplicacao sujeita a ADPF 662/regulamento", dep="n/a (e a propria regra)")
        idade = 70 if ano < 1998 else (67 if ano < 2004 else 65)
        L("ass", "ass_bpc_idade_minima", "Planalto(Lei 8.742/1993 art. 20 e 38; Lei 9.720/1998; Lei 10.741/2003 art. 34)",
          "idade minima do idoso para o BPC, vigente em 31/dez", ano, float(idade), "anos",
          "70 (texto original) -> 67 em 1/1/1998 (Lei 9.720/1998, art. 38) -> 65 (Estatuto do Idoso, Lei 10.741/2003, vigencia 2004)",
          dep="n/a (e a propria regra)")
    return ev_rows


def wb(cod):
    d = jload(f"wb_{cod}.json")
    return d[0].get("lastupdated", ""), [(int(x["date"]), x["value"]) for x in d[1] if x["value"] is not None]


def build_edu_extra():
    spec = [("SE.PRM.REPT.ZS", "edu_repetentes_primario_pct", "repetentes no ensino primario, % da matricula total", "%", "sim",
             "taxa de repetencia depende de regra (promocao automatica/ciclos, progressao continuada); serie WDI/UIS ate 2011"),
            ("SE.PRM.PRSL.ZS", "edu_persistencia_ultima_serie_primario", "persistencia ate a ultima serie do primario, % da coorte", "%", "sim",
             "indicador de fluxo, depende de regra; ate 2003"),
            ("SE.XPD.TOTL.GD.ZS", "edu_gasto_publico_pib", "gasto do governo em educacao, % do PIB", "% do PIB", "sim",
             "1995-2022 (25 pontos esparsos): nao qualifica pela regra de cobertura; depende de regras de vinculacao/Fundef/Fundeb"),
            ("SE.ADT.LITR.ZS", "edu_alfabetizacao_adultos_wdi", "alfabetizacao de adultos 15+, % (UIS/Banco Mundial)", "%", "nao",
             "pontos esparsos 1980-2024; definicao da fonte nacional (Censo/PNAD) repassada ao UIS")]
    for cod, ind, defn, un, dep, nota in spec:
        lu, serie = wb(cod)
        for a, v in sorted(serie):
            L("edu", ind, f"Banco Mundial WDI({cod})", defn, a, float(v), un, nota, dep=dep, vint=f"WDI lastupdated {lu}; baixado 2026-10-19")
    for a, v in ipea("MEDUCA"):
        L("edu", "edu_anos_estudo_25mais", "Ipea-Atlas(MEDUCA)", "media de anos de estudo, pessoas de 25+ (Censo, metodo PNUD)", a, v, "anos",
          "so Censos 1991 e 2000 no nivel Brasil", dep="nao")
    for r in sidra_series("sidra_7126_anosestudo_pnadc_2016_2025.json"):
        if r["v"] is not None:
            L("edu", "edu_anos_estudo_15mais", "IBGE-PNADC(SIDRA7126)", "numero medio de anos de estudo, pessoas de 15+ (PNADC anual)",
              r["ano"], r["v"], "anos", "so 2016+ (10 anos)", dep="nao")


# ---------- vintage e dependencia de regra ----------
BAIXADO = "baixado 2026-10-19"
VINT_COD = [("ADH_T_ANALF15M", "ADH_T_ANALF15M"), ("TXA15M7091", "TXA15M7091"), ("PNADCA_TXA15MUF", "PNADCA_TXA15MUF"),
            ("ADH_T_AGUA", "ADH_T_AGUA"), ("ADH_T_LUZ", "ADH_T_LUZ"), ("PDIAE", "PDIAE"), ("PDIEREDE", "PDIEREDE"),
            ("DISOC_INFI", "DISOC_INFI"), ("PAN_RRPE", "PAN_RRPE"), ("MPAS12", "MPAS12_RESPRGPS12"), ("BPC_idos", "BPC_idos"),
            ("FAM_PBF", "FAM_PBF"), ("MEDUCA", "MEDUCA"), ("MTE12", "MTE12_SALMIN12")]
DEP_SIM = {"ass_bpc_por_mil_hab", "ass_pbf_familias_por_mil_hab", "tbl_informalidade", "tbl_informalidade_ibge"}
DEP_PREFIXO_SIM = ("pre_rgps_",)


def vintage_de(fonte):
    partes = []
    for chave, cod in VINT_COD + [("DEPIS_POP", "DEPIS_POP"), ("PAN_PIBPMV", "PAN_PIBPMV"), ("BPC_defi", "BPC_defi")]:
        if chave in fonte and cod not in " ".join(partes):
            partes.append(f"Ipeadata {cod} SERATUALIZACAO {ipea_meta(cod)['SERATUALIZACAO'][:10]}")
    if "MTE" in fonte and "MTE12_SALMIN12" not in " ".join(partes):
        partes.append(f"Ipeadata MTE12_SALMIN12 SERATUALIZACAO {ipea_meta('MTE12_SALMIN12')['SERATUALIZACAO'][:10]}")
    if "IPCA" in fonte: partes.append("BCB SGS 433 (serie completa baixada 2026-10-19)")
    if "Planalto" in fonte: partes.append("texto compilado do Planalto em 2026-10-19")
    if partes: return "; ".join(partes) + f"; {BAIXADO}"
    if "SINASC" in fonte:
        return "SINASC/TabNet: dados finais ate 2024 (extracao 2025-12-02); 2025 preliminar (extracao 2026-07-28); " + BAIXADO
    if "PressKit2019" in fonte:
        return "INEP Press Kit Saeb 2019 (resultados divulgados em 2020-09-15)"
    if "Relatorio2023" in fonte:
        return "INEP Relatorio Saeb 2023 vol. 1 (Inep/MEC 2026; PDF de 2026-07-07)"
    if any(k in fonte for k in ("SIDRA", "IDS", "PNAD", "Censo")):
        return f"SIDRA/IBGE, consulta 2026-10-19 ({BAIXADO})"
    raise KeyError(fonte)


def dep_de(ind):
    if ind in DEP_SIM or ind.startswith(DEP_PREFIXO_SIM): return "sim"
    return "nao"


def escreve_csv(caminho, cols, linhas):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for r in linhas:
            w.writerow({c: r.get(c, "") for c in cols})


def fecha_series():
    for dom, rows in ROWS.items():
        for r in rows:
            if not r["vintage"]: r["vintage"] = vintage_de(r["fonte"])
            if not r["dependente_de_regra"]: r["dependente_de_regra"] = dep_de(r["indicador"])
        rows.sort(key=lambda r: (r["indicador"], r["fonte"], r["vintage"], int(r["ano"])))
        escreve_csv(os.path.join(OUT, f"{dom}.csv"), COLS, rows)
        print(f"series/{dom}.csv: {len(rows)} linhas, {len({r['indicador'] for r in rows})} indicadores")


def pontos(dom, ind, fonte):
    return sorted((int(r["ano"]), float(r["valor"])) for r in ROWS[dom]
                  if r["indicador"] == ind and r["fonte"] == fonte and not r["nota"].startswith(("ANOMALIA", "PRELIMINAR", "FORA_DA_JANELA")))


# ---------- dominios/indicadores sem serie comparavel: evidencia reproduzivel da busca ----------
SOCIAL = os.path.join(os.path.dirname(AQUI), "social")


def catalogo_ipea():
    """Catalogo Ipeadata (4071 series) baixado pela pasta social; conferido pelo sha256 do manifest dela."""
    p = os.path.join(SOCIAL, "bruto", "ipea_metadados_all.json")
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
    ok = any(json.loads(l)["sha256"] == sha and json.loads(l)["arquivo"] == "bruto/ipea_metadados_all.json"
             for l in open(os.path.join(SOCIAL, "manifest.jsonl"), "rb"))
    assert ok, "catalogo Ipeadata nao confere com o manifest da pasta social"
    return sha, json.load(open(p))["value"]


def busca_sem_serie():
    sha, cat_ip = catalogo_ipea()
    sid_cat = [(p["id"], a["id"], a["nome"]) for p in jload("sidra_catalogo_agregados.json") for a in p["agregados"]]
    linhas = []

    def cont_ip(rx, filtro=None):
        r = re.compile(rx, re.I)
        achados = [s for s in cat_ip if s["PAICODIGO"] == "BRA" and r.search(s["SERNOME"]) and not s["SERCODIGO"].startswith("HIST")
                   and (filtro is None or filtro(s))]
        return achados

    def cont_sid(rx):
        r = re.compile(rx, re.I)
        return [t for t in sid_cat if r.search(t[2])]

    def add(dom, cand, onde, termo, achou, conclusao):
        linhas.append({"dominio": dom, "indicador_candidato": cand, "onde_procurado": onde, "termo": termo,
                       "o_que_apareceu": achou, "conclusao": conclusao})

    ip = f"catalogo Ipeadata (4071 series; sha256 {sha[:12]}, pasta social)"
    c = cont_ip(r"(?<![a-z])cultur"); fed = [s["SERCODIGO"] for s in c]
    add("cul", "gasto federal na funcao cultura, % do orcamento", ip, "cultur", f"{len(c)} series: {', '.join(fed)}; todas de outro tipo (estaduais combinadas 'educacao e cultura' ou balanco de pagamentos)",
        "sem serie comparavel: o Ipeadata so tem a funcao Educacao+Cultura somada e so estadual/municipal; a funcao Cultura separada nasce na Portaria MOG 42/1999 (bruto/doc/portaria_mog_42_1999.odt)")
    c = cont_sid(r"cultur|bibliotec|museu|cinema|teatro")
    add("cul", "acesso a cultura (equipamentos/participacao)", "listagem de tabelas do SIDRA (bruto/sidra_catalogo_agregados.json)", "cultur|bibliotec|museu|cinema|teatro",
        f"{len(c)} tabelas; ids: {', '.join(str(x[1]) for x in c[:12])}{'...' if len(c) > 12 else ''}", "tabelas pontuais (MUNIC/POF/suplementos), sem serie anual nacional de 30 anos com metodo unico")
    c = cont_ip(r"lazer|desport|esporte"); cod = [s["SERCODIGO"] for s in c]
    add("laz", "gasto publico em desporto e lazer / acesso a lazer", ip, "lazer|desport|esporte", f"{len(c)} series: {', '.join(cod)}",
        "so DFDELE/DFDELM (despesa estadual/municipal na funcao Desporto e Lazer); DFDELE comeca em 2002 (24 anos, ver ipea_DFDELE.json): nao qualifica (<30 anos) e e despesa, nao acesso")
    c = cont_sid(r"lazer|esporte|desporto|turismo|viag")
    add("laz", "acesso a lazer", "listagem de tabelas do SIDRA", "lazer|esporte|desporto|turismo|viag", f"{len(c)} tabelas; ids: {', '.join(str(x[1]) for x in c[:12])}",
        "suplementos pontuais (ex.: turismo/viagens PNADC a partir de 2019, tabelas 6411/7229/7234/7251), sem serie de 30 anos")
    c = cont_ip(r"transport")
    cod = [s["SERCODIGO"] for s in c if s["SERCODIGO"].startswith("DFTRA")]
    add("tra", "acesso/qualidade do transporte publico (nacional)", ip, "transport",
        f"{len(c)} series; as que medem politica publica sao despesas estaduais/municipais por funcao: {', '.join(cod)}; o resto e producao/venda de veiculos, receitas de servicos e cambio",
        "sem serie comparavel de acesso: DFTRAE (despesa estadual, 1965-2025) e despesa, nao acesso, e a funcao Transporte inclui rodovias/infraestrutura; nao e uma medida do direito a transporte")
    c = cont_sid(r"deslocamento|transporte|mobilidade|tempo de viagem|casa.trabalho")
    add("tra", "tempo de deslocamento casa-trabalho / mobilidade", "listagem de tabelas do SIDRA", "deslocamento|transporte|mobilidade|casa-trabalho",
        f"{len(c)} tabelas; ids: {', '.join(str(x[1]) for x in c[:12])}", "tabelas pontuais; sem serie nacional anual de 30 anos com metodo unico")
    c = cont_sid(r"aposentad|benef[ií]cio.*previd|pensionista")
    add("pre", "% de 65+ com aposentadoria/pensao (PNAD)", "listagem de tabelas do SIDRA", "aposentad|beneficio previd|pensionista",
        f"{len(c)} tabelas relevantes (ex.: PD 1866/4022: aposentados 10+/15+ 2001-2015; CD 2964/3580: Censo); nenhuma com recorte 65+ e serie 1992-2025 de metodo unico",
        "sem serie comparavel; exigiria microdados PNAD 1981-2015 e PNADC (que nao pergunta igual) - nao coletado")
    c = cont_ip(r"previd|aposent")
    add("pre", "saldo da previdencia, % do PIB", ip, "previd|aposent", f"{len(c)} series: {', '.join(s['SERCODIGO'] for s in c)[:400]}",
        "MPAS12_* (fluxo de caixa mensal) comeca em 2003-02: 22 anos completos (2004-2025). Usado, mas nao qualifica pela regra de cobertura de 30 anos")
    c = cont_ip(r"assist[eê]ncia|bolsa|bpc|gasto social")
    add("ass", "gasto em assistencia social, % do PIB", ip, "assistencia|bolsa|BPC|gasto social",
        f"{len(c)} series; com 'assistencia social' como funcao: DFASPRE/DFASPRM (somada com previdencia, so estadual/municipal); nenhuma federal",
        "sem serie comparavel de gasto federal em assistencia; usadas apenas as series de cobertura (BPC 1996+, PBF 2004+)")
    linhas.append({"dominio": "edu", "indicador_candidato": "taxas de aprovacao, reprovacao, abandono e distorcao idade-serie (INEP; dependente_de_regra=sim)",
                   "onde_procurado": "download.inep.gov.br (URLs de planilhas testadas: .../portal_ideb/planilhas_para_download/{2019,2021,2023}/divulgacao_brasil_*.xlsx, .../indicadores_educacionais/taxas_de_rendimento_escolar/2023/tx_rend_brasil_regioes_ufs_2023.zip, .../informacoes_estatisticas/indicadores_educacionais/2023/TAXA_RENDIMENTO/...) e paginas gov.br/inep de Ideb/Saeb/Resultados",
                   "termo": "taxas de rendimento escolar", "o_que_apareceu": "404 em todas as URLs testadas; as paginas de resultados do gov.br/inep carregam o conteudo por JavaScript (o WebFetch devolve 'Aguarde. Carregando conteudo da aba...'); duas buscas na web nao devolveram o link da planilha",
                   "conclusao": "nao coletadas; a repetencia ficou so na serie WDI/UIS (1970-2011), marcada dependente_de_regra=sim"})
    linhas.append({"dominio": "tbl", "indicador_candidato": "rendimento do trabalho: PME (6 regioes metropolitanas)", "onde_procurado": "listagem de tabelas do SIDRA (pesquisa PE)",
                   "termo": "pme rendimento", "o_que_apareceu": "tabela 16 (PME antiga, rendimento NOMINAL, serie encerrada, moedas anteriores ao Real) e 2181-2187 (PME nova 2002-2016, real)", "conclusao": "nao coletada: cobre so 6 regioes metropolitanas, nao o Brasil; a serie nacional usada e a PNAD (1996-2015) + PNADC"})
    linhas.append({"dominio": "edu", "indicador_candidato": "IDEB (INEP)", "onde_procurado": "conhecimento do desenho da fonte + tentativa de achar a planilha no INEP (paginas dinamicas; URLs de download.inep.gov.br testadas deram 404)",
                   "termo": "ideb", "o_que_apareceu": "o Ideb e calculado desde 2005 (primeira edicao)", "conclusao": "nao qualifica pela cobertura (2005-2023 = 19 anos); planilha nao localizada; nao coletado"})
    linhas.append({"dominio": "edu", "indicador_candidato": "PISA (OCDE)", "onde_procurado": "pre-registro e documentos do INEP", "termo": "pisa",
                   "o_que_apareceu": "participacao do Brasil desde a edicao de 2000", "conclusao": "nao qualifica pela cobertura (2000-2022 = 22 anos, 8 pontos); nao coletado"})
    linhas.append({"dominio": "mor", "indicador_candidato": "deficit habitacional (Fundacao Joao Pinheiro)", "onde_procurado": "WebSearch 2026-10-19 (artigos sobre a metodologia FJP)",
                   "termo": "deficit habitacional serie historica", "o_que_apareceu": "estudos desde 1995 com Censo 1991; desde 2016 a PNADC e a unica fonte e variaveis foram excluidas",
                   "conclusao": "sem serie de metodo unico de 30 anos; relatorios FJP nao baixados"})
    return linhas


# ---------- quebras.csv ----------
QCOLS = ["indicador", "serie", "data_quebra", "metodo_antigo", "metodo_novo", "razao_declarada_pela_fonte", "fonte_primaria_url", "trecho_citado",
         "direcao_do_efeito", "como_a_direcao_foi_determinada", "efeito_medido", "como_medido", "apresentada_como_aprimoramento", "tipo_de_quebra"]


def doc_texto(rel):
    """Texto normalizado (espacos colapsados) de um documento do bruto/: .htm, .pdf ou .odt."""
    p = os.path.join(B, rel)
    if rel.endswith(".pdf"):
        t = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
    elif rel.endswith(".odt"):
        t = re.sub(r"<[^>]+>", " ", zipfile.ZipFile(p).read("content.xml").decode())
    elif rel.endswith(".json"):
        t = json.dumps(jload(rel), ensure_ascii=False)
    else:
        t = re.sub(r"<[^>]+>", " ", open(p, "rb").read().decode("latin-1"))
    return re.sub(r"\s+", " ", html.unescape(t))


def trecho(rel, rx, antes=0, depois=260):
    t = doc_texto(rel)
    m = re.search(rx, t)
    assert m, f"trecho nao encontrado em {rel}: {rx}"
    return t[max(0, m.start() - antes): m.end() + depois].strip()


def S(dom, ind, fonte):
    return {int(r["ano"]): float(r["valor"]) for r in ROWS[dom] if r["indicador"] == ind and r["fonte"] == fonte}


# ---------- janelas.csv ----------
PRIM = {"edu_analfab15": "Atlas-DH-Censo(ADH_T_ANALF15M)", "mor_agua_rede_geral": "IBGE-Censo(SIDRA)", "mor_esgoto_adequado": "IBGE-Censo(SIDRA)",
        "tbl_informalidade": "Ipea-PNAD(DISOC_INFI)", "tbl_renda_trabalho_real": "IBGE-PNAD(SIDRA1871 deflacionado)"}
JCOLS = ["indicador", "governo", "inicio", "fim", "media", "valor_inicial", "valor_final", "n_anos", "segmento_metodo"]


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")


def gera_janelas():
    gs = governos()
    out = []
    grupos = {}
    for dom, rows in ROWS.items():
        for r in rows:
            grupos.setdefault((dom, r["indicador"]), {}).setdefault(r["fonte"], []).append(r)
    for (dom, ind), porfonte in sorted(grupos.items()):
        if ind.startswith("edu_saeb_"):
            comp = {}
            for fonte in ("INEP-Saeb(PressKit2019)", "INEP-Saeb(Relatorio2023)"):  # a ultima vintage vence no ano comum
                for r in porfonte.get(fonte, []):
                    comp[int(r["ano"])] = (float(r["valor"]), fonte)
            out += janelas(ind, [(a, v) for a, (v, f) in comp.items()], gs, lambda a, c=comp: c[a][1] + ("; desenho amostral (1995-2003)" if a <= 2003 else "; desenho Aneb+Anresc/Prova Brasil (2005+)"))
            continue
        prim = PRIM.get(ind, next(iter(porfonte)) if len(porfonte) == 1 else None)
        for fonte, rows in porfonte.items():
            pts = pontos(dom, ind, fonte)
            ident = ind if fonte == prim else f"{ind}__{slug(fonte)}"
            out += janelas(ident, pts, gs, lambda a, f=fonte: f)
    escreve_csv(os.path.join(AQUI, "janelas.csv"), JCOLS, out)
    print(f"janelas.csv: {len(out)} linhas, {len({r['indicador'] for r in out})} identificadores")
    return out


def build_mor_pnad():
    # PNAD 2001-2015 (SIDRA 1955/1956; milhares de domicilios) e PNADC 2016+ (SIDRA 6731/6735/7192; distribuicao %)
    r = {}
    for x in sidra_series("sidra_1955_agua_pnad_2001_2015.json"):
        r.setdefault(cat(x, "61"), {})[x["ano"]] = x["v"]
    for ano, tot in sorted(r["0"].items()):
        L("mor", "mor_agua_rede_geral", "IBGE-PNAD(SIDRA1955)",
          "domicilios com agua de rede geral (com ou sem canalizacao interna), % do total; PNAD anual",
          ano, 100 * (r["1033"][ano] + r["1035"][ano]) / tot, "%", "sensibilidade anual; Norte rural fora ate 2003, dentro desde 2004 (ver quebras.csv)")
    for x in sidra_series("sidra_6731_agua_pnadc_2016_2025.json"):
        if cat(x, "825") == "46285" and x["v"] is not None:
            L("mor", "mor_agua_rede_geral", "IBGE-PNADC(SIDRA6731)", "domicilios com rede geral como principal fonte de agua, % do total; PNADC anual",
              x["ano"], x["v"], "%", "sensibilidade anual; outra pesquisa e outra pergunta (principal fonte)")
    e = {}
    for x in sidra_series("sidra_1956_esgoto_pnad_2001_2015.json"):
        e.setdefault(cat(x, "7173"), {})[x["ano"]] = x["v"]
    for ano, tot in sorted(e["0"].items()):
        fossa = e["99664"].get(ano)
        if fossa is None:
            fossa = (e["9490"].get(ano) or 0) + (e["9491"].get(ano) or 0)
        L("mor", "mor_esgoto_adequado", "IBGE-PNAD(SIDRA1956)",
          "domicilios com rede coletora ou fossa septica, % do total de domicilios; PNAD anual", ano,
          100 * (e["99663"][ano] + fossa) / tot, "%", "sensibilidade anual")
    s7 = {}
    for x in sidra_series("sidra_7192_esgoto_pnadc_2019_2025.json"):
        s7.setdefault(x["ano"], {})[cat(x, "11558")] = x["v"]
    for ano, d in sorted(s7.items()):
        if d.get("47930") is not None:
            L("mor", "mor_esgoto_adequado", "IBGE-PNADC(SIDRA7192)",
              "rede geral/pluvial + fossa septica (ligada ou nao), % dos domicilios COM banheiro/sanitario/buraco; PNADC anual", ano,
              d["47930"] + d["47931"] + d["47936"], "%", "sensibilidade; universo diferente (exclui domicilios sem instalacao); so 2019+")
            L("mor", "mor_esgoto_rede_ou_fossa_ligada", "IBGE-PNADC(SIDRA7192)", "rede geral/pluvial + fossa septica ligada a rede, % dos domicilios com banheiro etc.",
              ano, d["47930"] + d["47931"], "%", "sensibilidade; tabela nova a partir de 2019")
    for x in sidra_series("sidra_6735_esgoto_pnadc_2016_2018.json"):
        if cat(x, "11558") == "46290" and x["v"] is not None:
            L("mor", "mor_esgoto_rede_ou_fossa_ligada", "IBGE-PNADC(SIDRA6735)", "rede geral, pluvial ou fossa ligada a rede, % dos domicilios com banheiro etc.",
              x["ano"], x["v"], "%", "sensibilidade; tabela encerrada em 2018 (categorias diferentes da 7192)")


def monta():
    verifica_manifest()
    build_edu(); comp_saeb = build_saeb(); build_edu_extra()
    build_mor(); build_mor_pnad(); build_tbl(); build_pre_ass(); ev = build_limiares(); build_mat()
    return comp_saeb, ev



def gera_quebras(comp_saeb):
    P = "https://www.planalto.gov.br/ccivil_03"
    IP = "http://www.ipeadata.gov.br/api/odata4/Metadados('%s')"
    SD = "https://servicodados.ibge.gov.br/api/v3/agregados/%s/metadados"
    U_SIS12 = "https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2012/notas_tecnicas.pdf"
    U_NOTA13 = "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Nota_Tecnica/2013_12_09_nota_pnad_continua.pdf"
    U_AEPS = "http://www.ipeadata.gov.br/doc/AEPS-2018.pdf"
    U_SINASC = "http://tabnet.datasus.gov.br/cgi/sinasc/Nascidos_Vivos_1994_2012.pdf"
    U_COLET = "https://download.inep.gov.br/educacao_basica/saeb/documentos_edicoes_antigas/coletanea_de_documentos_de_edicoes_antigas.pdf"
    U_PK = "https://download.inep.gov.br/educacao_basica/saeb/2019/presskit/PressKit_Saeb_2019.pdf"
    U_R23 = "https://download.inep.gov.br/saeb/resultados/relatorio-saeb_volume_1_2023.pdf"
    U_PNADC20 = "https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/42a50edf01ee9b102e4c892fa5b03a7a.pdf"
    out = []

    def Q(**k):
        r = {c: "" for c in QCOLS}; r.update(k); out.append(r)

    f = lambda x: f"{x:+.2f}".replace(".", ",") if isinstance(x, float) else str(x)
    # ---------------- educacao: alfabetizacao ----------------
    atlas, ant = S("edu", "edu_analfab15", "Atlas-DH-Censo(ADH_T_ANALF15M)"), S("edu", "edu_analfab15", "Ipea-Atlas1998(TXA15M7091)")
    pnadc = S("edu", "edu_analfab15", "IBGE-PNADC(SIDRA7113)"); pnad = S("edu", "edu_analfab15", "IBGE-PNAD(IDS1187)")
    Q(indicador="edu_analfab15", serie="Ipea-Atlas1998(TXA15M7091) -> Atlas-DH-Censo(ADH_T_ANALF15M)", data_quebra="1991 (mesmo Censo, duas vintages)",
      metodo_antigo="Censos 1970/1980/1991 processados no Atlas do Desenvolvimento Humano, edicao 1998",
      metodo_novo="Censos 1991/2000/2010/2022 reprocessados nos microdados (Atlas DH PNUD/Ipea/FJP)",
      razao_declarada_pela_fonte="nao declarada (a metadata so cita o Atlas 1998)", fonte_primaria_url=IP % "TXA15M7091",
      trecho_citado=trecho("meta/ipea_meta_TXA15M7091.json", r"Percentual de pessoas de 15 ou mais anos", 0, 200),
      direcao_do_efeito="eleva", como_a_direcao_foi_determinada="sinal da diferenca na sobreposicao de 1991 (nova - antiga)",
      efeito_medido=f"{f(round(atlas[1991] - ant[1991], 2))} p.p. em 1991 ({atlas[1991]:.2f} contra {ant[1991]:.2f})",
      como_medido="mesmo ano (1991), mesma variavel (15+ que nao sabem ler nem escrever um bilhete simples); diferenca Atlas DH - Atlas 1998",
      apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="revisao_de_vintage")
    d22 = pnadc[2022] - atlas[2022]
    Q(indicador="edu_analfab15", serie="Atlas-DH-Censo(ADH_T_ANALF15M) / IBGE-PNAD(IDS1187) / IBGE-PNADC(SIDRA7113)", data_quebra="2022 (Censo x pesquisa domiciliar amostral no mesmo ano)",
      metodo_antigo="Censo Demografico: recenseamento, questionario do Censo", metodo_novo="PNAD (ate 2015) e PNAD Continua (desde 2016): amostra de domicilios",
      razao_declarada_pela_fonte="nao declarada para a taxa de analfabetismo", fonte_primaria_url=SD % "7113",
      trecho_citado=trecho("meta/sidra_meta_7113.json", r"Taxa de analfabetismo das pessoas de 15 anos ou mais de idade, por sexo e grupo de idade", 0, 40),
      direcao_do_efeito="reduz", como_a_direcao_foi_determinada="sinal da diferenca no unico ano com as duas fontes (2022)",
      efeito_medido=f"{f(round(d22, 2))} p.p. em 2022 (PNADC {pnadc[2022]:.1f} contra Censo {atlas[2022]:.2f}); Censo 2010 {atlas[2010]:.2f} contra PNAD 2009 {pnad.get(2009, float('nan')):.1f} e PNAD 2011 {pnad.get(2011, float('nan')):.1f} (anos diferentes, so indicativo)",
      como_medido="diferenca PNADC - Censo no mesmo ano (2022), mesma definicao de 15+ e mesma pergunta de alfabetizacao",
      apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="metodo_estatistico")
    Q(indicador="edu_analfab15", serie="IBGE-PNAD(IDS1187) -> IBGE-PNADC(SIDRA7113)", data_quebra="2016 (PNAD encerrada em 2015; PNADC anual desde 2016)",
      metodo_antigo="PNAD anual (1.100 municipios por ano)", metodo_novo="PNAD Continua (cerca de 3.500 municipios, coleta trimestral; indicadores anuais da 5a visita)",
      razao_declarada_pela_fonte="a PNAD Continua 'substituira' a PME e a PNAD, 'potencializando os resultados' e com cobertura territorial mais abrangente",
      fonte_primaria_url=U_NOTA13, trecho_citado=trecho("doc/ibge_nota_pnad_continua_2013.pdf", r"A PNAD Contínua substituirá", 0, 330) + " | MPS/AEPS 2018: " + trecho("doc/mps_aeps_2018.pdf", r"recomenda-se cautela na comparação", 0, 160),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="nao ha ano com as duas pesquisas na taxa de analfabetismo (PNAD 2004-2015; PNADC 2016+)",
      efeito_medido="sem sobreposicao", como_medido="IDS 1187 termina em 2015; SIDRA 7113 e Ipeadata PNADCA_TXA15MUF comecam em 2016",
      apresentada_como_aprimoramento="sim", tipo_de_quebra="metodo_estatistico")
    Q(indicador="edu_analfab15 (e tbl_renda_trabalho_real, mor_agua_rede_geral, mor_esgoto_adequado)", serie="IBGE-PNADC", data_quebra="2020-03 a 2021-06",
      metodo_antigo="coleta presencial", metodo_novo="coleta por telefone (a pesquisa foi desenhada para coleta presencial)",
      razao_declarada_pela_fonte="interrupcao da coleta presencial em 17/03/2020 (isolamento social)", fonte_primaria_url=U_PNADC20,
      trecho_citado=trecho("doc/ibge_pnadc_coleta_nao_presencial_2020.pdf", r"telefone desde 17 de março de 2020", 80, 120),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="a fonte nao quantifica o vies; indicadores anuais de educacao/habitacao de 2020 e 2021 nao existem nas series coletadas",
      efeito_medido="sem sobreposicao", como_medido="nao ha medida simultanea presencial x telefone nas series baixadas; anos 2020 e 2021 ausentes em SIDRA 7113/6731/7192",
      apresentada_como_aprimoramento="nao", tipo_de_quebra="metodo_estatistico")
    # ---------------- educacao: regras que mudam o que a taxa mede ----------------
    rep = S("edu", "edu_repetentes_primario_pct", "Banco Mundial WDI(SE.PRM.REPT.ZS)")
    Q(indicador="edu_repetentes_primario_pct", serie="Banco Mundial WDI(SE.PRM.REPT.ZS)", data_quebra="1996-12-20",
      metodo_antigo="reprovacao por serie como regra", metodo_novo="LDB: ciclos e progressao continuada permitidos (art. 23; art. 32, par. 2)",
      razao_declarada_pela_fonte="texto legal", fonte_primaria_url=P + "/leis/l9394.htm",
      trecho_citado=trecho("doc/leg/lei_9394_ldb.htm", r"progressão continuada", 160, 120),
      direcao_do_efeito="reduz", como_a_direcao_foi_determinada="inferida do texto: a regra admite promocao sem reprovacao; efeito nao medido",
      efeito_medido="sem sobreposicao (nao ha serie com e sem a regra); valores publicados: " + ", ".join(f"{a}={rep[a]:.1f}" for a in sorted(rep) if 1990 <= a <= 2011),
      como_medido="apenas os valores brutos publicados, sem atribuicao causal", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="mudanca_de_regra")
    Q(indicador="edu_repetentes_primario_pct", serie="Banco Mundial WDI(SE.PRM.REPT.ZS)", data_quebra="1998 (Sao Paulo)",
      metodo_antigo="series anuais com reprovacao", metodo_novo="regime de progressao continuada em ciclos na rede estadual de SP",
      razao_declarada_pela_fonte="nao localizada no texto oficial (Deliberacao CEE 9/97; Resolucao SE 4/98 nao baixadas)", fonte_primaria_url="https://www.scielo.br/pdf/pp/v21n3/v21n3a12.pdf",
      trecho_citado="FONTE SECUNDARIA: " + trecho("doc/leg/scielo_pp_progressao_continuada_sp.pdf", r"Deliberação no 09/97", 80, 200),
      direcao_do_efeito="reduz", como_a_direcao_foi_determinada="inferida do desenho do regime; efeito nao medido", efeito_medido="sem sobreposicao",
      como_medido="serie nacional; nao ha serie de SP com e sem o regime nas fontes coletadas", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="mudanca_de_regra")
    Q(indicador="edu_saeb_* (5o ano e 9o ano)", serie="INEP-Saeb(PressKit2019/Relatorio2023)", data_quebra="2006-02-06 (Lei 11.274); implantacao ate 2010",
      metodo_antigo="ensino fundamental de 8 anos (4a e 8a series)", metodo_novo="ensino fundamental de 9 anos, matricula obrigatoria a partir dos 6 anos (5o e 9o anos)",
      razao_declarada_pela_fonte="texto legal", fonte_primaria_url=P + "/_ato2004-2006/2006/lei/l11274.htm",
      trecho_citado=trecho("doc/leg/lei_11274_ef9anos.htm", r"duração de 9 \(nove\) anos", 120, 140),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="a serie do INEP rotula igual (5o/9o ano) para todos os anos; a equivalencia 4a serie = 5o ano nao foi medida aqui",
      efeito_medido="sem sobreposicao", como_medido="nao ha edicao do Saeb que aplique a prova nas duas estruturas", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="mudanca_de_regra")
    Q(indicador="edu_saeb_* (todas as etapas)", serie="INEP-Saeb(PressKit2019)", data_quebra="2005 (Portaria MEC 931/2005; Prova Brasil)",
      metodo_antigo="Saeb amostral em escolas publicas e privadas", metodo_novo="Saeb = Aneb (amostral) + Anresc/Prova Brasil (censitaria nas escolas publicas)",
      razao_declarada_pela_fonte="resultados por escola/municipio e insumo do Ideb", fonte_primaria_url=U_COLET,
      trecho_citado=trecho("doc/inep_saeb_coletanea_edicoes_antigas.pdf", r"Portaria Ministerial nº 931", 0, 330),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="o Press Kit publica uma unica serie nacional 1995-2019 sem separar a abrangencia",
      efeito_medido="sem sobreposicao", como_medido="nao ha media nacional pelas duas abrangencias na mesma edicao nas fontes baixadas", apresentada_como_aprimoramento="sim", tipo_de_quebra="metodo_estatistico")
    n_ig = sum(1 for c in comp_saeb if c[3] == c[4])
    Q(indicador="edu_saeb_* (todas as etapas)", serie="INEP-Saeb(PressKit2019) x INEP-Saeb(Relatorio2023)", data_quebra="2011-2019 (mesmas edicoes em duas vintages)",
      metodo_antigo="Press Kit 2019 (divulgado 2020-09-15)", metodo_novo="Relatorio Saeb 2023 vol. 1 (Inep/MEC 2026)",
      razao_declarada_pela_fonte="'a escala de proficiencia ... permaneceu a mesma das edicoes anteriores' (matriz antiga mantida para comparabilidade)", fonte_primaria_url=U_R23,
      trecho_citado=trecho("doc/inep_relatorio_saeb_2023_vol1.pdf", r"permaneceu a mesma das edições anteriores", 0, 78),
      direcao_do_efeito="ambigua", como_a_direcao_foi_determinada="efeito medido igual a zero (comparacao ponto a ponto dos rotulos dos graficos); nao ha sentido de efeito",
      efeito_medido=f"0 em {n_ig} de {len(comp_saeb)} pontos (valores arredondados identicos)", como_medido="6 series x 2011-2019 (5 edicoes), Press Kit contra Relatorio 2023",
      apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="revisao_de_vintage")
    gasto = S("edu", "edu_gasto_publico_pib", "Banco Mundial WDI(SE.XPD.TOTL.GD.ZS)")
    for data, antigo, novo, arq, rx, url in (
            ("1998-01-01", "financiamento sem fundo contabil estadual", "Fundef (EC 14/1996; Lei 9.424/1996 'implantado a partir de 1o de janeiro de 1998')", "doc/leg/lei_9424_fundef.htm",
             r"implantado, automaticamente, a partir de 1º de janeiro de 1998", P + "/leis/l9424.htm"),
            ("2007-01-01", "Fundef (so ensino fundamental)", "Fundeb (EC 53/2006; Lei 11.494/2007), toda a educacao basica", "doc/leg/ec_53_2006_fundeb.htm",
             r"Fundo de Manutenção e Desenvolvimento da Educação Básica", P + "/constituicao/emendas/emc/emc53.htm"),
            ("2009-11-11", "obrigatoriedade 6-14 anos", "EC 59/2009: educacao basica obrigatoria dos 4 aos 17 anos", "doc/leg/ec_59_2009.htm",
             r"dos 4 \(quatro\) aos 17 \(dezessete\) anos", P + "/constituicao/emendas/emc/emc59.htm"),
            ("2020-08-26", "Fundeb com prazo (ate 2020)", "Fundeb permanente (EC 108/2020; Lei 14.113/2020)", "doc/leg/ec_108_2020.htm",
             r"Fundeb", P + "/constituicao/emendas/emc/emc108.htm")):
        Q(indicador="edu_gasto_publico_pib", serie="Banco Mundial WDI(SE.XPD.TOTL.GD.ZS)", data_quebra=data, metodo_antigo=antigo, metodo_novo=novo,
          razao_declarada_pela_fonte="texto legal", fonte_primaria_url=url, trecho_citado=trecho(arq, rx, 60, 160),
          direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="a regra muda a vinculacao/distribuicao, nao o que e contado como gasto; efeito nao medido",
          efeito_medido="sem sobreposicao", como_medido="serie WDI 1995-2022 (25 pontos); valores brutos: " + ", ".join(f"{a}={gasto[a]:.2f}" for a in sorted(gasto)[:1] + sorted(gasto)[-1:]),
          apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="mudanca_de_regra")
    # ---------------- moradia ----------------
    ag = S("mor", "mor_agua_rede_geral", "IBGE-Censo(SIDRA)"); pc = S("mor", "mor_agua_rede_geral", "IBGE-PNADC(SIDRA6731)")
    s6803 = {cat(r, "1821"): r["v"] for r in sidra_series("sidra_6803_agua_ligacao_2022.json")}
    liga = 100 * sum(v for k, v in s6803.items() if k in ("72144", "72145", "72146", "72147", "72148", "72149", "72150", "72151", "72152")) / s6803["72129"]
    Q(indicador="mor_agua_rede_geral", serie="IBGE-Censo(SIDRA)", data_quebra="2022 (mesmo Censo, duas definicoes de 'rede geral')",
      metodo_antigo="'rede geral' = principal forma de abastecimento (1991, 2000, 2010 e 2022 tab. 6804)", metodo_novo="2022 passa a separar 'possui ligacao a rede geral' (tab. 6803) de 'a utiliza como principal forma'",
      razao_declarada_pela_fonte="nao declarada", fonte_primaria_url=SD % "6803",
      trecho_citado=trecho("meta/sidra_meta_6803.json", r"Domicílios particulares permanentes ocupados, por existência de ligação à rede geral", 0, 140),
      direcao_do_efeito="eleva", como_a_direcao_foi_determinada="sinal da diferenca dentro de 2022",
      efeito_medido=f"{f(round(liga - ag[2022], 2))} p.p. ({liga:.2f}% com ligacao contra {ag[2022]:.2f}% com rede como principal forma)",
      como_medido="mesmo Censo 2022, tab. 6803 contra 6804 (soma das categorias 'possui ligacao a rede geral')", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="metodo_estatistico")
    Q(indicador="mor_agua_rede_geral", serie="IBGE-Censo(SIDRA) x IBGE-PNADC(SIDRA6731)", data_quebra="2022 (Censo contra PNADC no mesmo ano)",
      metodo_antigo="Censo 2022, domicilios ocupados", metodo_novo="PNADC 2022, principal fonte de agua", razao_declarada_pela_fonte="nao declarada", fonte_primaria_url=SD % "6731",
      trecho_citado=trecho("meta/sidra_meta_6731.json", r"Domicílios e Moradores, por situação do domicílio e principal fonte de abastecimento de água", 0, 40),
      direcao_do_efeito="eleva", como_a_direcao_foi_determinada="sinal da diferenca no ano comum", efeito_medido=f"{f(round(pc[2022] - ag[2022], 2))} p.p. (PNADC {pc[2022]:.1f} contra Censo {ag[2022]:.2f})",
      como_medido="PNADC 2022 - Censo 2022", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="metodo_estatistico")
    s91 = {r["cl"]["1612"][0]: r["v"] for r in sidra_series("sidra_256_esgoto_1991.json")}
    ex = 100 * (s91["120451"] + s91["120452"]) / s91["0"]; com = 100 * (s91["120451"] + s91["120452"] + s91["120460"] + s91["120461"]) / s91["0"]
    Q(indicador="mor_esgoto_adequado", serie="IBGE-Censo(SIDRA) 1991", data_quebra="1991 contra 2000-2022",
      metodo_antigo="1991 (tab. 256): instalacao sanitaria so do domicilio", metodo_novo="2000-2022: tipo de esgotamento do banheiro ou sanitario (sem a distincao exclusiva/compartilhada)",
      razao_declarada_pela_fonte="nao declarada", fonte_primaria_url=SD % "256", trecho_citado=trecho("meta/sidra_meta_256.json", r"Domicílios particulares permanentes por instalação sanitária", 0, 60),
      direcao_do_efeito="eleva", como_a_direcao_foi_determinada="sinal da diferenca ao incluir as instalacoes compartilhadas em 1991",
      efeito_medido=f"{f(round(com - ex, 2))} p.p. em 1991 ({ex:.2f}% so exclusivas contra {com:.2f}% incluindo as compartilhadas com rede ou fossa septica)",
      como_medido="mesma tabela de 1991, soma das categorias 'comum a mais de um domicilio' com rede geral e com fossa septica", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="metodo_estatistico")
    pd = S("mor", "mor_esgoto_adequado", "Ipea-PDIAE(Atlas1998<=1991;SIDRA>=2000)"); es = S("mor", "mor_esgoto_adequado", "IBGE-Censo(SIDRA)")
    Q(indicador="mor_esgoto_adequado", serie="Ipea-PDIAE (Atlas 1998 ate 1991; SIDRA a partir de 2000)", data_quebra="1991 (costura de fontes: Atlas 1998 ate 1991, SIDRA desde 2000)",
      metodo_antigo="Atlas do Desenvolvimento Humano, edicao 1998 (1970, 1980, 1991); a metadata declara a unidade como 'porcentagem da populacao que vive em domicilios com instalacoes adequadas'", metodo_novo="tabelas do IBGE (SIDRA) de domicilios por tipo de esgotamento (2000, 2010, 2022); os numeros batem com a porcentagem de DOMICILIOS (diferenca <= 0,01 p.p.), nao de populacao, apesar do texto da metadata",
      razao_declarada_pela_fonte="a metadata descreve a costura sem justifica-la", fonte_primaria_url=IP % "PDIAE",
      trecho_citado=trecho("meta/ipea_meta_PDIAE.json", r"Os dados até 1991", 0, 220),
      direcao_do_efeito="eleva", como_a_direcao_foi_determinada="sinal da diferenca em 1991 (PDIAE - recalculo proprio com SIDRA 256); o efeito mistura troca de fonte, de unidade (populacao no Atlas 1998, domicilios no SIDRA) e de universo (instalacao exclusiva), e nao e separavel nos brutos baixados",
      efeito_medido=f"{f(round(pd[1991] - es[1991], 2))} p.p. em 1991 (PDIAE {pd[1991]:.2f} contra {es[1991]:.2f}); em 2000/2010/2022 a diferenca e {pd[2000] - es[2000]:+.2f}/{pd[2010] - es[2010]:+.2f}/{pd[2022] - es[2022]:+.2f}",
      como_medido="1991: PDIAE (Atlas 1998) contra a soma rede geral + fossa septica exclusivas do SIDRA 256; 2000+: PDIAE contra o recalculo proprio",
      apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="revisao_de_vintage")
    pe = S("mor", "mor_esgoto_adequado", "IBGE-PNADC(SIDRA7192)")
    s22 = {cat(r, "11558"): r["v"] for r in sidra_series("sidra_6805_esgoto_2022.json")}
    cen_mesmo_univ = 100 * (s22["72110"] + s22["72111"] + s22["72112"]) / (s22["46292"] - s22["92861"])
    Q(indicador="mor_esgoto_adequado", serie="IBGE-Censo(SIDRA) x IBGE-PNADC(SIDRA7192)", data_quebra="2022 (Censo contra PNADC no mesmo ano)",
      metodo_antigo="Censo 2022: % de todos os domicilios", metodo_novo="PNADC: % dos domicilios com banheiro/sanitario/buraco", razao_declarada_pela_fonte="nao declarada", fonte_primaria_url=SD % "7192",
      trecho_citado=trecho("meta/sidra_meta_7192.json", r"Domicílios e Moradores com banheiro, sanitário ou buraco para dejeções", 0, 100),
      direcao_do_efeito="eleva", como_a_direcao_foi_determinada="sinal da diferenca no ano comum, ja no mesmo universo",
      efeito_medido=f"{f(round(pe[2022] - cen_mesmo_univ, 2))} p.p. no mesmo universo (PNADC {pe[2022]:.1f} contra Censo {cen_mesmo_univ:.2f}); {f(round(pe[2022] - es[2022], 2))} p.p. contra o Censo no universo de todos os domicilios",
      como_medido="Censo 2022 recalculado sem os domicilios sem banheiro nem sanitario, contra PNADC 2022", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="metodo_estatistico")
    Q(indicador="mor_esgoto_rede_ou_fossa_ligada", serie="IBGE-PNADC(SIDRA6735) -> IBGE-PNADC(SIDRA7192)", data_quebra="2019",
      metodo_antigo="tabela 6735 (2016-2018): 'rede geral, rede pluvial ou fossa ligada a rede' contra 'fossa nao ligada'", metodo_novo="tabela 7192 (a partir de 2019): fossa septica ligada/nao ligada separadas",
      razao_declarada_pela_fonte="nao declarada", fonte_primaria_url=SD % "7192", trecho_citado="titulos no SIDRA: " + trecho("meta/sidra_meta_6735.json", r"tipo de esgotamento sanitário \(de 2016 até 2018\)", 20, 0) + " | " + trecho("meta/sidra_meta_7192.json", r"tipo de esgotamento sanitário \(a partir de 2019\)", 20, 0),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="sem ano comum", efeito_medido="sem sobreposicao", como_medido="2018 (66.6) e 2019 (68.1) sao anos distintos",
      apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="metodo_estatistico")
    Q(indicador="mor_agua_rede_geral / mor_esgoto_adequado (series PNAD)", serie="IBGE-PNAD(SIDRA1955/1956)", data_quebra="2003 -> 2004",
      metodo_antigo="PNAD 1992-2003 sem a area rural de RO, AC, AM, RR, PA, AP", metodo_novo="PNAD 2004+ cobre a area rural dessas 6 UFs",
      razao_declarada_pela_fonte="manter a homogeneidade dos resultados (para o periodo 1992-2003)", fonte_primaria_url=U_SIS12,
      trecho_citado=trecho("doc/ibge_sis2012_notas_tecnicas.pdf", r"A partir de 2004, a pesquisa passou a cobrir tanto", 0, 160),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="nao medida: seria preciso a cobertura rural do Norte por tipo de servico, nao baixada", efeito_medido="sem sobreposicao",
      como_medido="a PNAD nao publicou 2003 com e sem a area rural do Norte nas tabelas coletadas", apresentada_como_aprimoramento="sim", tipo_de_quebra="metodo_estatistico")
    # ---------------- trabalho ----------------
    Q(indicador="tbl_informalidade", serie="Ipea-PNAD(DISOC_INFI) -> IBGE-PNADC(SIDRA4708)", data_quebra="2014 -> 2016",
      metodo_antigo="Ipea definicao I sobre microdados da PNAD: (sem carteira + conta propria) / (protegidos + sem carteira + conta propria)", metodo_novo="IBGE/PNADC: taxa de informalidade das pessoas ocupadas de 14+",
      razao_declarada_pela_fonte="serie do Ipea interrompida (nao calculada nos anos de Censo)", fonte_primaria_url=IP % "DISOC_INFI",
      trecho_citado=trecho("meta/ipea_meta_DISOC_INFI.json", r"Uma das três diferentes definições", 0, 480),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="definicoes distintas e sem ano comum (Ipea ate 2014; IBGE desde 2016)", efeito_medido="sem sobreposicao",
      como_medido="series nao emendadas; relatadas em linhas separadas", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="metodo_estatistico")
    Q(indicador="tbl_informalidade", serie="Ipea-PNAD(DISOC_INFI) / IBGE-PNADC(SIDRA4708)", data_quebra="2017-11-11 (Lei 13.467/2017, vigencia apos 120 dias)",
      metodo_antigo="categorias de vinculo anteriores a reforma", metodo_novo="CLT passa a prever contrato intermitente (art. 443, par. 3)",
      razao_declarada_pela_fonte="texto legal", fonte_primaria_url=P + "/_ato2015-2018/2017/lei/l13467.htm", trecho_citado=trecho("doc/leg/lei_13467_2017_reforma_trabalhista.htm", r"Considera-se como intermitente o contrato de trabalho", 0, 260),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="regra pode mover trabalhadores entre 'com' e 'sem carteira'; efeito nao medido", efeito_medido="sem sobreposicao",
      como_medido="nao ha serie com e sem a regra", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="mudanca_de_regra")
    rp = S("tbl", "tbl_renda_trabalho_real", "IBGE-PNAD(SIDRA1871 deflacionado)"); r15 = S("tbl", "tbl_renda_trabalho_real", "IBGE-PNAD(SIDRA4027 deflacionado, 15+)")
    rc = S("tbl", "tbl_renda_trabalho_real", "IBGE-PNADC(SIDRA4660 nominal deflacionado)")
    razoes = {a: 100 * (rc[a] / rp[a] - 1) for a in (2012, 2013, 2014, 2015)}
    razoes15 = {a: 100 * (rc[a] / r15[a] - 1) for a in (2012, 2013, 2014, 2015)}
    Q(indicador="tbl_renda_trabalho_real", serie="IBGE-PNAD(SIDRA1871) -> IBGE-PNADC(SIDRA4660)", data_quebra="2012-2015 (sobreposicao) e 2016",
      metodo_antigo="PNAD: rendimento do mes de referencia (setembro), ocupados 10+ (ou 15+ na tabela 4027)", metodo_novo="PNADC: rendimento habitual, ocupados 14+, media anual",
      razao_declarada_pela_fonte="a PNADC 'substituira' a PNAD; AEPS 2018: 'recomenda-se cautela na comparacao'", fonte_primaria_url=U_NOTA13,
      trecho_citado=trecho("doc/ibge_nota_pnad_continua_2013.pdf", r"A PNAD Contínua substituirá", 0, 200) + " | " + trecho("doc/mps_aeps_2018.pdf", r"recomenda-se cautela na comparação", 0, 160),
      direcao_do_efeito="eleva", como_a_direcao_foi_determinada="sinal da razao PNADC/PNAD no periodo comum 2012-2015 (todos positivos)",
      efeito_medido=f"{sum(razoes.values()) / 4:+.1f}% em media (PNADC acima da PNAD, 10+): " + ", ".join(f"{a}: {razoes[a]:+.1f}% (10+) / {razoes15[a]:+.1f}% (15+)" for a in razoes),
      como_medido="razao entre o rendimento nominal da PNADC (tab. 4660, var. 5929) e o da PNAD (tab. 1871, 10+, e 4027, 15+) nos quatro anos com as duas pesquisas; definicoes de rendimento e idade diferentes, entao a razao junta metodo e definicao",
      apresentada_como_aprimoramento="sim", tipo_de_quebra="metodo_estatistico")
    # ---------------- previdencia ----------------
    Q(indicador="pre_rgps_*", serie="MPS-fluxo-de-caixa(Ipeadata MPAS12_*)", data_quebra="2007-03-16 (Lei 11.457/2007)",
      metodo_antigo="INSS arrecadava e fiscalizava as contribuicoes previdenciarias", metodo_novo="Secretaria da Receita Federal do Brasil assume a arrecadacao",
      razao_declarada_pela_fonte="transferencia de competencia (Super-Receita)", fonte_primaria_url=U_AEPS, trecho_citado=trecho("doc/mps_aeps_2018.pdf", r"O art\. 2º da Lei nº 11\.457", 0, 300),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="a fonte nao mede o efeito na serie", efeito_medido="sem sobreposicao", como_medido="serie mensal inicia em 2003-02; sem versao antiga e nova do mesmo mes",
      apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="mudanca_de_regra")
    Q(indicador="pre_rgps_arrecadacao_liquida_pib", serie="MPS-fluxo-de-caixa(Ipeadata MPAS12_ARRLIQ12)", data_quebra="2015",
      metodo_antigo="definicao de arrecadacao liquida anterior a 2015 (nao descrita no AEPS 2018)", metodo_novo="'valor da arrecadacao bruta deduzidos os ressarcimentos, restituicoes e repasses a terceiros'",
      razao_declarada_pela_fonte="nota de rodape da tabela 40.1 do AEPS; rubricas do fluxo de caixa 'sao criadas, extintas ou transformadas ao longo do tempo'", fonte_primaria_url=U_AEPS,
      trecho_citado=trecho("doc/mps_aeps_2018.pdf", r"A partir de 2015, Arrecadação Líquida corresponde", 0, 150) + " | " + trecho("doc/mps_aeps_2018.pdf", r"novas rubricas são criadas", 120, 80),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="a fonte nao informa o valor pela definicao antiga", efeito_medido="sem sobreposicao",
      como_medido="a serie do Ipeadata nao traz as duas definicoes", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="metodo_estatistico")
    Q(indicador="pre_rgps_*", serie="MPS-fluxo-de-caixa(Ipeadata MPAS12_*)", data_quebra="2019-11-13 (EC 103/2019)",
      metodo_antigo="regras de aposentadoria e pensao vigentes", metodo_novo="reforma da previdencia (regras de transicao)", razao_declarada_pela_fonte="texto constitucional",
      fonte_primaria_url=P + "/constituicao/emendas/emc/emc103.htm", trecho_citado=trecho("doc/leg/ec_103_2019_previdencia.htm", r"Altera o sistema de previdência social", 0, 100),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="efeito sobre beneficios e resultado nao medido", efeito_medido="sem sobreposicao", como_medido="nao ha serie com e sem a regra",
      apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="mudanca_de_regra")
    # ---------------- assistencia ----------------
    Q(indicador="ass_bpc_por_mil_hab / ass_bpc_idade_minima", serie="MDS-BPC(Ipeadata BPC_idos)", data_quebra="1998-01-01 (70 -> 67 anos)",
      metodo_antigo="idade minima 70 anos (texto original da LOAS)", metodo_novo="67 anos a partir de 1/1/1998 (Lei 9.720/1998), depois 65 anos (Estatuto do Idoso, Lei 10.741/2003, art. 34; vigencia 2004)",
      razao_declarada_pela_fonte="texto legal", fonte_primaria_url=P + "/leis/l8742.htm",
      trecho_citado=trecho("doc/planalto_lei_8742_loas.htm", r"idoso com 70 \(setenta\) anos ou mais", 120, 80) + " | " + trecho("doc/planalto_lei_8742_loas.htm", r"reduzir-se-á para sessenta e sete anos", 20, 90) + " | " + trecho("doc/planalto_lei_10741_estatuto_idoso.htm", r"Art\. 34\. Aos idosos, a partir de 65", 0, 120),
      direcao_do_efeito="eleva", como_a_direcao_foi_determinada="inferida do limiar: idade menor amplia o conjunto elegivel; efeito nao medido",
      efeito_medido="sem sobreposicao (benefícios de idosos em dezembro: 1997=88806, 1998=207031, 2003=664875, 2004=933164, valores brutos, nao atribuiveis a regra isolada)", como_medido="valores brutos de BPC_idos",
      apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="mudanca_de_regra")
    Q(indicador="ass_bpc_por_mil_hab / ass_bpc_limiar_*", serie="MDS-BPC(Ipeadata BPC_idos + BPC_defi)", data_quebra=f"{data_assinatura(legtxt('lei_13981_2020_bpc.htm')).isoformat()} (Lei 13.981/2020) e {data_assinatura(legtxt('lei_14176_2021_bpc.htm')).isoformat()} (Lei 14.176/2021)",
      metodo_antigo="renda familiar per capita inferior a 1/4 do salario minimo", metodo_novo="texto da Lei 13.981/2020: inferior a 1/2 salario minimo; Lei 14.176/2021: 1/4 com possibilidade de ampliar ate 1/2 (aplicacao sujeita a regulamento e a ADPF 662)",
      razao_declarada_pela_fonte="texto legal", fonte_primaria_url=P + "/_ato2019-2022/2021/lei/L14176.htm",
      trecho_citado=trecho("doc/leg/lei_13981_2020_bpc.htm", r"inferior a 1/2 \(meio\)", 120, 60) + " | " + trecho("doc/leg/lei_14176_2021_bpc.htm", r"ampliar o limite de renda", 60, 130),
      direcao_do_efeito="eleva", como_a_direcao_foi_determinada="inferida do limiar maior; a aplicacao efetiva nao foi verificada", efeito_medido="sem sobreposicao",
      como_medido="nao ha serie de concessoes por criterio", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="mudanca_de_regra")
    d = S("ass", "ass_bpc_por_mil_hab", "MDS-BPC(Ipeadata BPC_idos+BPC_defi) / IBGE-Pop(DEPIS_POP)")
    Q(indicador="ass_bpc_por_mil_hab", serie="MDS-BPC(Ipeadata BPC_defi)", data_quebra="2016 (vintage)",
      metodo_antigo="BPC_defi 2015 = 2.323.808; 2017 = 2.527.257", metodo_novo="BPC_defi 2016 = 74 (valor publicado no Ipeadata)",
      razao_declarada_pela_fonte="nao declarada", fonte_primaria_url=IP % "BPC_defi", trecho_citado=trecho("meta/ipea_meta_BPC_defi.json", r"Esta série apresenta o número de transferências do BPC somente para deficientes", 0, 160),
      direcao_do_efeito="reduz", como_a_direcao_foi_determinada="valor publicado e 4 ordens de grandeza menor que os vizinhos", efeito_medido="sem sobreposicao; valor mantido como publicado (74) e ano excluido das janelas",
      como_medido="comparacao com 2015 e 2017", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="revisao_de_vintage")
    fb = {a: v for a, v in ipea("FAM_PBF")}
    Q(indicador="ass_pbf_familias_por_mil_hab", serie="MDS-PBF(Ipeadata FAM_PBF)", data_quebra="2021-11-08 (Auxilio Brasil) e 2023-06-16 (volta do Bolsa Familia)",
      metodo_antigo="Bolsa Familia: linhas de pobreza e de extrema pobreza", metodo_novo="Auxilio Brasil (Lei 14.284/2021; linhas 200/100, depois 210/105) e, em 2023, Bolsa Familia com linha unica de R$ 218 per capita",
      razao_declarada_pela_fonte="texto legal; o Ipeadata registra a serie como uma so, com o programa 'renomeado' entre 2021 e 2023", fonte_primaria_url=P + "/_ato2023-2026/2023/lei/L14601.htm",
      trecho_citado=trecho("doc/leg/lei_14601_2023_pbf.htm", r"igual ou inferior a R\$ 218,00", 160, 40) + " | " + trecho("doc/leg/dec_10852_2021_auxilio_brasil.htm", r"extrema pobreza, caracterizada pela renda familiar mensal per capita no valor de até R\$ 100,00", 0, 40),
      direcao_do_efeito="eleva", como_a_direcao_foi_determinada="beneficios em dezembro: " + ", ".join(f"{a}={fb[a]:.0f}" for a in (2021, 2022, 2023)) + " (valores brutos; nao atribuiveis so a regra)",
      efeito_medido="sem sobreposicao", como_medido="nao ha serie com e sem a regra", apresentada_como_aprimoramento="sim", tipo_de_quebra="mudanca_de_regra")
    Q(indicador="ass_pbf_limiar_pobreza_real / ass_pbf_limiar_extrema_pobreza_real", serie="Planalto(decretos do PBF)", data_quebra="2023-06-16",
      metodo_antigo="duas linhas (pobreza e extrema pobreza) por decreto, reajustadas de forma irregular (2004-2022)", metodo_novo="linha unica de R$ 218 per capita (Decreto 11.566/2023; Lei 14.601/2023)",
      razao_declarada_pela_fonte="texto legal", fonte_primaria_url=P + "/_ato2023-2026/2023/decreto/D11566.htm", trecho_citado=trecho("doc/leg/dec_11566_2023.htm", r"caracterizada pela renda familiar per capita mensal de até R\$ 218,00", 100, 80),
      direcao_do_efeito="ambigua", como_a_direcao_foi_determinada="o valor nominal sobe (R$ 210 -> R$ 218) mas o valor real em R$ de dez/2025 cai (2022 -> 2023); ver series/limiares_eventos.csv", efeito_medido="sem sobreposicao; linha de pobreza em R$ de dez/2025 (vigente em 31/dez): " + ", ".join(f"{a}={v:.0f}" for a, v in sorted(S("ass", "ass_pbf_limiar_pobreza_real", "Planalto(decretos/leis do PBF)+BCB-IPCA(SGS433)").items()) if a in (2004, 2009, 2014, 2018, 2022, 2023, 2025)),
      como_medido="IPCA (BCB SGS 433) ate dez/2025", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="mudanca_de_regra")
    # ---------------- maternidade ----------------
    sn = tabnet_sinasc()
    a99, a00 = 100 * sn[1999]["7mais"] / (sn[1999]["total"] - sn[1999]["ign"]), 100 * sn[2000]["7mais"] / (sn[2000]["total"] - sn[2000]["ign"])
    Q(indicador="mat_prenatal7", serie="MS-SINASC(TabNet)", data_quebra="1995-1999 (categorias) e 2000",
      metodo_antigo="1995-1998: 1-6 consultas agrupadas ('De 1 a 6 consultas, nao especificado')", metodo_novo="1999+: 1-3 e 4-6 separadas; '7 e mais' sempre separada",
      razao_declarada_pela_fonte="'a existencia de categorias que se sobrepoem deve-se a alteracoes nos formularios ao longo do tempo'", fonte_primaria_url=U_SINASC,
      trecho_citado=trecho("doc/datasus_sinasc_notas_tecnicas.pdf", r"A existência de categorias que se sobrepõem deve-se a alterações nos formulários", 0, 60),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="a categoria '7 e mais' nao muda; o que muda e a parcela 'ignorado'",
      efeito_medido=f"sem sobreposicao; observado: 7+ entre os informados: {a99:.1f}% (1999, ignorado {100 * sn[1999]['ign'] / sn[1999]['total']:.1f}%) contra {a00:.1f}% (2000, ignorado {100 * sn[2000]['ign'] / sn[2000]['total']:.1f}%)",
      como_medido="razao 7+/(total - ignorado) nos dois anos; nao separavel de mudanca de comportamento", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="metodo_estatistico")
    Q(indicador="mat_prenatal7", serie="MS-SINASC(TabNet)", data_quebra="2011",
      metodo_antigo="Declaracao de Nascido Vivo (DN) anterior a 2011", metodo_novo="nova DN 'com maior detalhamento'; em 2011 os dois formularios foram usados simultaneamente",
      razao_declarada_pela_fonte="maior detalhamento das informacoes coletadas", fonte_primaria_url=U_SINASC, trecho_citado=trecho("doc/datasus_sinasc_notas_tecnicas.pdf", r"Em 2011, houve uma mudança no conteúdo da Declaração", 0, 330),
      direcao_do_efeito="desconhecida", como_a_direcao_foi_determinada="a tabela nacional nao separa os dois formularios", efeito_medido="sem sobreposicao",
      como_medido="2011 aparece agregado; documento 'Consolidacao do SINASC 2011' citado pela fonte nao foi baixado", apresentada_como_aprimoramento="sim", tipo_de_quebra="metodo_estatistico")
    Q(indicador="mat_prenatal7", serie="MS-SINASC(TabNet)", data_quebra="1994-2000 (implantacao gradual)",
      metodo_antigo="coleta em parte dos municipios", metodo_novo="cobertura crescente", razao_declarada_pela_fonte="'a implantacao do SINASC foi gradativa'", fonte_primaria_url=U_SINASC,
      trecho_citado=trecho("doc/datasus_sinasc_notas_tecnicas.pdf", r"A implantação do SINASC foi gradativa", 0, 200), direcao_do_efeito="desconhecida",
      como_a_direcao_foi_determinada="nao medida", efeito_medido=f"sem sobreposicao; observado: ignorado {100 * sn[1995]['ign'] / sn[1995]['total']:.1f}% (1995), {100 * sn[1998]['ign'] / sn[1998]['total']:.1f}% (1998), {100 * sn[2002]['ign'] / sn[2002]['total']:.1f}% (2002)",
      como_medido="parcela de nascimentos com numero de consultas ignorado; anos com mais de 10% ignorado ficam fora das janelas (regra fixa)", apresentada_como_aprimoramento="nao_declarado", tipo_de_quebra="metodo_estatistico")
    escreve_csv(os.path.join(AQUI, "quebras.csv"), QCOLS, out)
    print(f"quebras.csv: {len(out)} linhas")


if __name__ == "__main__":
    comp_saeb, ev = monta()
    fecha_series()
    escreve_csv(os.path.join(OUT, "limiares_eventos.csv"),
                ["programa", "data_vigencia", "instrumento", "linha_pobreza_nominal", "linha_extrema_pobreza_nominal",
                 "linha_pobreza_real_dez2025", "linha_extrema_pobreza_real_dez2025"], ev)
    gera_janelas()
    escreve_csv(os.path.join(AQUI, "busca-sem-serie.csv"), ["dominio", "indicador_candidato", "onde_procurado", "termo", "o_que_apareceu", "conclusao"],
                busca_sem_serie())
    gera_quebras(comp_saeb)
