"""Constroi series/*.csv, janelas.csv e quebras.csv do bloco dominios-2 (saude, seguranca, alimentacao,
ambiente, democracia). SO LE O BRUTO (sem rede). Confere o sha256 de cada bruto contra o manifest
da sua subpasta antes de ler.

Uso: python3 -I /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-2/scripts/construir.py
"""
import csv, datetime, hashlib, html, json, re, statistics, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent                       # .../dominios-2
sys.path.insert(0, str(AQUI))
import xlsx_min                          # noqa: E402

MANDATOS = Path("/Users/ulissesflores/Developer/brazil-governments-factcheck/data/curated/mandatos.csv")
SERIES = RAIZ / "series"
SERIES.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------- hash
_MANIFESTS = {}


def _manifest(pasta):
    if pasta not in _MANIFESTS:
        linhas = [json.loads(l) for l in (RAIZ / pasta / "manifest.jsonl").read_text().splitlines() if l.strip()]
        ult = {}
        for l in linhas:
            ult[l["arquivo"]] = l          # a linha mais nova do arquivo vale
        _MANIFESTS[pasta] = ult
    return _MANIFESTS[pasta]


def bruto(pasta, arquivo):
    """Caminho do bruto, depois de conferir o sha256 contra a ultima linha do manifest da pasta."""
    p = RAIZ / pasta / arquivo
    esperado = _manifest(pasta)[arquivo]["sha256"]
    real = hashlib.sha256(p.read_bytes()).hexdigest()
    if real != esperado:
        sys.exit(f"HASH DIVERGE: {pasta}/{arquivo}")
    return p


# ----------------------------------------------------------------------------- governos
def carregar_mandatos():
    out = []
    for r in csv.DictReader(MANDATOS.open(encoding="utf-8")):
        out.append({"id": r["id"], "inicio": datetime.date.fromisoformat(r["posse"]),
                    "fim": datetime.date.fromisoformat(r["saida"])})
    return out


GOVS = carregar_mandatos()


def governo_do_intervalo(ini, fim):
    """Governo com mais dias dentro de [ini, fim) (regra unica, a mesma para todo indicador)."""
    melhor, dias = None, 0
    for g in GOVS:
        d = (min(fim, g["fim"]) - max(ini, g["inicio"])).days
        if d > dias:
            melhor, dias = g["id"], d
    return melhor


def intervalo_calendario(ano):
    return datetime.date(ano, 1, 1), datetime.date(ano + 1, 1, 1)


def intervalo_prodes(ano):                # ano PRODES T = 1 ago (T-1) a 31 jul T
    return datetime.date(ano - 1, 8, 1), datetime.date(ano, 8, 1)


# ----------------------------------------------------------------------------- leitores
def wb(pasta, codigo):
    j = json.loads(bruto(pasta, f"bruto/wb_{codigo}.json").read_text())
    return {int(r["date"]): r["value"] for r in j[1] if r["value"] is not None}


def tabnet(arquivo):
    t = (RAIZ / "seguranca" / arquivo).read_bytes().decode("latin1")
    bruto("seguranca", arquivo)
    corpo = html.unescape(t[t.index("<PRE>") + 5:t.index("</PRE>")])
    linhas = [l for l in corpo.strip().split("\n") if l.strip() and l.strip() != "&"]
    cab = [c.strip('"') for c in linhas[0].split(";")]
    anos = [int(c) for c in cab[1:] if c.isdigit()]
    tab = {}
    for l in linhas[1:]:
        p = l.split(";")
        rot = p[0].strip('"').strip()
        vals = {}
        for a, v in zip(anos, p[1:]):
            v = v.strip('"')
            if v not in ("", "-"):
                vals[a] = int(v)
        tab[rot] = vals
    return tab


def linha_que_comeca(tab, prefixo):
    ach = [k for k in tab if k.startswith(prefixo)]
    assert len(ach) == 1, (prefixo, ach)
    return tab[ach[0]]


# ----------------------------------------------------------------------------- saida de series
SERIES_ROWS = {}      # dominio -> lista de dicts
META = {}             # indicador -> dict(dominio, intervalo, segmento(ano)->str, papel)


def add_serie(dominio, ind, fonte, definicao, valores, unidade, nota, segmento, papel, vintage,
              intervalo=intervalo_calendario, nota_ano=None):
    """Uma (indicador, vintage) = uma serie. Mesma vintage nunca e sobrescrita; vintage nova = linhas novas."""
    assert (ind, vintage) not in META, (ind, vintage)
    for ano in sorted(valores):
        SERIES_ROWS.setdefault(dominio, []).append({
            "indicador": ind, "fonte": fonte, "definicao_linha": definicao, "ano": ano,
            "valor": valores[ano], "unidade": unidade,
            "nota": (nota_ano or {}).get(ano, nota), "vintage": vintage})
    META[(ind, vintage)] = {"dominio": dominio, "intervalo": intervalo, "segmento": segmento, "papel": papel,
                            "valores": dict(valores)}


def arred(x, n=4):
    return round(x, n)


# ============================================================================= SAUDE
mmr = wb("saude", "SH.STA.MMRT")
mmr_ne = wb("saude", "SH.STA.MMRT.NE")
add_serie("sau", "sau_mortmat", "WB-WDI-SH.STA.MMRT(MMEIG-modelado)",
          "razao de mortalidade materna, estimativa modelada (OMS/UNICEF/UNFPA/BM/ONU-Pop), por 100 mil nascidos vivos",
          mmr, "por 100 mil nv",
          "MODELO, nao contagem; WDI atualizado 2026-10-08 (bruto/wb_SH.STA.MMRT.json). Origem de 1985-1999 vs 2000-2023 nao verificada nos arquivos baixados",
          lambda a: "MMEIG-modelado", "primario", "WDI 2026-10-08 (MMEIG)")
add_serie("sau", "sau_mortmat_nacional", "WB-WDI-SH.STA.MMRT.NE(estimativa-nacional)",
          "razao de mortalidade materna, estimativa nacional compilada pelo MMEIG (dados do pais), por 100 mil nv",
          mmr_ne, "por 100 mil nv",
          "sensibilidade; dado do pais (SIM/SINASC) como compilado pelo MMEIG; 1995-2022",
          lambda a: "estimativa-nacional(SIM/SINASC)", "sensibilidade", "WDI 2026-10-08 (MMEIG)")

# DTP3: WIISE (WUENIC revisao 2025) -> xlsx
wiise = bruto("saude", "bruto/who_wiise_coverage-data.xlsx")
_it = xlsx_min.ler(str(wiise))
_h = next(_it)
_ix = {n: i for i, n in enumerate(_h)}
dtp = {"WUENIC": {}, "ADMIN": {}, "OFFICIAL": {}}
for r in _it:
    if len(r) > 10 and r[_ix["CODE"]] == "BRA" and r[_ix["ANTIGEN"]] == "DTPCV3" and r[_ix["COVERAGE_CATEGORY"]] in dtp:
        if r[_ix["COVERAGE"]] != "":
            dtp[r[_ix["COVERAGE_CATEGORY"]]][int(r[_ix["YEAR"]])] = float(r[_ix["COVERAGE"]])
wuenic = dtp["WUENIC"]
wb_dtp = wb("saude", "SH.IMM.IDPT")
add_serie("sau", "sau_dtp3", "OMS/UNICEF-WUENIC-rev2025(WIISE-export)",
          "cobertura vacinal DTP3 (3a dose) em criancas < 12 meses, estimativa WUENIC, % ",
          {a: v for a, v in wuenic.items()}, "%",
          "WUENIC revisao de 2025 (export WIISE baixado em 2026-10-19); inclui 2025",
          lambda a: "WUENIC-rev2025", "primario", "WUENIC 2025 (WIISE export 2026-10-19)")
add_serie("sau", "sau_dtp3_admin", "OMS-WIISE-cobertura-administrativa(Brasil)",
          "cobertura administrativa DTP3 (doses aplicadas / populacao-alvo informada pelo pais), %",
          dtp["ADMIN"], "%", "sensibilidade: dado administrativo bruto do pais, nao a estimativa WUENIC",
          lambda a: "administrativa", "sensibilidade", "WIISE export 2026-10-19")
add_serie("sau", "sau_dtp3", "WB-WDI-SH.IMM.IDPT(WUENIC de revisao anterior a 2025)",
          "cobertura DPT/DTP3 em criancas 12-23 meses, WDI (replica WUENIC; 2023 e 2024 diferem da revisao 2025)",
          wb_dtp, "%", "OUTRA VINTAGE do mesmo indicador (nao sobrescreve): WDI 2026-10-08 traz 2023=90, 2024=91; WUENIC 2025 traz 86 e 90; demais anos iguais",
          lambda a: "WUENIC-rev-anterior(WDI)", "vintage-anterior", "WUENIC anterior a 2025 (via WDI 2026-10-08)")
ghed = wb("saude", "SH.XPD.GHED.GD.ZS")
add_serie("sau", "sau_gasto_pub_pib", "WB-WDI-SH.XPD.GHED.GD.ZS(OMS-GHED)",
          "gasto do governo geral em saude, % do PIB (OMS Global Health Expenditure Database, atualizado 2025-12-12)",
          ghed, "% do PIB",
          "INFORMATIVO: 2000-2023 = 24 anos < 30 anos da regra de inclusao 2; nao ha serie comparavel de 30 anos no que foi baixado",
          lambda a: "GHED", "informativo(<30 anos)", "WDI 2026-10-08 (GHED 2025-12-12)")

# ============================================================================= SEGURANCA
ipea = json.loads(bruto("seguranca", "bruto/ipea_AVIOL12_HOMIC_Brasil_derivado.json").read_text())["value"]
homic_n = {int(r["VALDATA"][:4]): int(r["VALVALOR"]) for r in ipea}
popproj = {int(r["VALDATA"][:4]): r["VALVALOR"] for r in
           json.loads(bruto("seguranca", "bruto/ipeadata_POP_PROJE_Brasil_derivado.json").read_text())["value"]}
popcenso = {int(r["VALDATA"][:4]): r["VALVALOR"] for r in
            json.loads(bruto("seguranca", "bruto/ipeadata_POPTOT_Brasil_derivado.json").read_text())["value"]}

seg_cid = lambda a: "SIM-CID9" if a <= 1995 else "SIM-CID10"
add_serie("seg", "seg_homic_n", "Ipeadata-AVIOL12_HOMIC(MS/SIM)",
          "numero de homicidios, obitos por residencia: CID-9 E960-E978 e E990-E999 (1979-95); CID-10 X85-Y09 e Y35 (1996-)",
          homic_n, "obitos", "contagem; conta de 1979 existe mas nao ha populacao projetada de 1979 para taxa",
          seg_cid, "primario(contagem)", "Ipeadata AVIOL12_HOMIC (serie atualizada 2026-07-08; SIM final ate 2024)")
taxa = {a: homic_n[a] / popproj[a] * 1e5 for a in homic_n if a in popproj}
add_serie("seg", "seg_homic_taxa", "Ipeadata-AVIOL12_HOMIC / IBGE-Projecao-rev2024(POP_PROJE)",
          "homicidios por 100 mil habitantes; denominador = populacao projetada a 1o jul, IBGE revisao 2024 (um so vintage 1980-2024)",
          {a: arred(v) for a, v in taxa.items()}, "por 100 mil hab",
          "calculado por construir.py; a 2022 a projecao (210,86 mi) difere do Censo 2022 (203,08 mi): ver quebras.csv",
          seg_cid, "primario", "Ipeadata AVIOL12_HOMIC (2026-07-08) + IBGE Projecao rev.2024")
unodc = wb("seguranca_unodc", "VC.IHR.PSRC.P5")
add_serie("seg", "seg_homic_taxa_unodc", "WB-WDI-VC.IHR.PSRC.P5(UNODC)",
          "homicidios intencionais por 100 mil (UNODC via WDI); fonte nacional de Brasil nao verificada nos arquivos baixados",
          {a: arred(v) for a, v in unodc.items()}, "por 100 mil hab", "sensibilidade 1990-2023",
          lambda a: "UNODC(WDI)", "sensibilidade", "WDI 2026-10-08 (UNODC)")

e10 = tabnet("bruto/tabnet_ext10_grupo_ano.html")
e09 = tabnet("bruto/tabnet_ext09_grupo_ano.html")
agress10 = e10["Agressões"]
interv10 = e10["Intervenções legais e operações de guerra"]
indet10 = e10["Eventos (fatos) cuja intenção é indeterminada"]
homic9 = linha_que_comeca(e09, "E55 Homic")
indet9 = linha_que_comeca(e09, ".. E560")
indet = {**indet9, **indet10}
add_serie("seg", "seg_homic_indet_taxa", "Ipeadata-AVIOL12_HOMIC + TabNet-SIM(intencao indeterminada) / POP_PROJE",
          "homicidios + mortes por eventos de intencao indeterminada (CID-9 E980-E989 'E560'; CID-10 Y10-Y34), por 100 mil",
          {a: arred((homic_n[a] + indet[a]) / popproj[a] * 1e5) for a in homic_n if a in popproj and a in indet},
          "por 100 mil hab", "sensibilidade: limite superior se parte das mortes de intencao indeterminada for homicidio",
          seg_cid, "sensibilidade", "Ipeadata (2026-07-08) + SIM TabNet (final ate 2024, extracao 02/12/2025) + IBGE Projecao rev.2024")
add_serie("seg", "seg_indet_pct", "TabNet-SIM",
          "intencao indeterminada / (homicidios + intencao indeterminada) x 100  [CID-9: E560 e E55; CID-10: Y10-Y34 e Agressoes]",
          {a: arred(indet[a] / ((homic9.get(a) or agress10.get(a)) + indet[a]) * 100) for a in indet},
          "%", "diagnostico de qualidade do SIM, nao e resultado de politica",
          seg_cid, "diagnostico", "SIM TabNet (final ate 2024, extracao 02/12/2025; CID-9 consulta 2026-10-19)")
o10 = tabnet("bruto/tabnet_obt10_capitulo_ano.html")
o09 = tabnet("bruto/tabnet_obt09_capitulo_ano.html")
maldef = {**{a: v / o09["Total"][a] * 100 for a, v in linha_que_comeca(o09, "XVI.").items()},
          **{a: v / o10["Total"][a] * 100 for a, v in linha_que_comeca(o10, "XVIII.").items()}}
add_serie("seg", "seg_maldef_pct", "TabNet-SIM",
          "obitos por causas mal definidas (CID-9 cap. XVI; CID-10 cap. XVIII) / total de obitos x 100",
          {a: arred(v) for a, v in maldef.items()}, "%",
          "diagnostico de qualidade/cobertura do SIM, nao e resultado de politica", seg_cid, "diagnostico",
          "SIM TabNet (final ate 2024, extracao 02/12/2025; CID-9 consulta 2026-10-19)")

# ============================================================================= ALIMENTACAO
fao = list(csv.DictReader(bruto("alimentacao", "bruto/fao_fs_Brazil_derivado.csv").open(encoding="utf-8")))
pou, pou_nota = {}, {}
for r in fao:
    if r["Item Code"] == "210041":
        a0, a1 = map(int, r["Year"].split("-"))
        centro = (a0 + a1) // 2
        v = r["Value"]
        if v.startswith("<"):
            pou[centro] = float(v[1:])
            pou_nota[centro] = f"CENSURADO: FAO publica '{v}' (valor real abaixo do limiar); grava-se o limiar como teto; media trienal {r['Year']}"
        else:
            pou[centro] = float(v)
            pou_nota[centro] = f"media trienal {r['Year']} atribuida ao ano do meio"
add_serie("ali", "ali_pou", "FAO-FAOSTAT-SuiteFoodSecurity(SOFI-2026)",
          "prevalencia de subalimentacao (% da populacao), media movel de 3 anos atribuida ao ano central",
          pou, "%", "", lambda a: "FAOSTAT-vintage-2026", "primario(<30 anos: 2001-2024)", "FAOSTAT 2026-07-10 (SOFI 2026)",
          nota_ano=pou_nota)
add_serie("ali", "ali_pou", "FAO-SOFI-2015(Anexo)",
          "prevalencia de subalimentacao, SOFI 2015, medias 1990-92, 2000-02, 2005-07, 2010-12, 2014-16 (ano central); '<5,0' tomado como 5,0 (teto)",
          {1991: 14.8, 2001: 11.2, 2006: 5.0, 2011: 5.0, 2015: 5.0}, "%",
          "sensibilidade; vintage antigo; Brasil p. do Anexo (linha 'Brazil ... 14.8 11.2 <5.0 <5.0 <5.0' em bruto/fao_sofi2015_i4646e.pdf); 2006, 2011 e 2015 CENSURADOS em <5,0",
          lambda a: "SOFI2015", "vintage-anterior", "SOFI 2015")

# ============================================================================= AMBIENTE
pr = json.loads(bruto("ambiente", "bruto/terrabrasilis_rates2026.json").read_text())
prodes, prodes_ufs = {}, {}
for p in pr["periods"]:
    ano = p["endDate"]["year"]
    prodes[ano] = sum(a["area"] for f in p["features"] for a in f["areas"])
assert prodes[1988] == 21050 and prodes[2025] == 5731 and prodes[2024] == 6518 and prodes[2022] == 11594
prod_seg = lambda a: ("PRODES-analogico(1988-2000)" if a <= 2000 else
                      "PRODES-digital(2001-2005)" if a <= 2005 else "PRODES-TerraAmazon(2006-)")
add_serie("amb", "amb_prodes_amz", "INPE-PRODES(TerraBrasilis, soma dos 9 estados da Amazonia Legal)",
          "taxa anual de desmatamento por corte raso, km2, ano PRODES = 1 ago (T-1) a 31 jul T; valores consolidados 1988-2025",
          {a: v for a, v in prodes.items() if a <= 2025}, "km2/ano",
          "soma dos 9 estados; testes: 1988=21.050, 2022=11.594, 2024=6.518, 2025=5.731 (notas tecnicas do INPE). 1993 e 1994 tem o MESMO valor 14.896 no JSON",
          prod_seg, "primario", "PRODES TerraBrasilis rates2026.json (atualizado 2026-10-16)", intervalo=intervalo_prodes,
          nota_ano={1993: "valor identico a 1994 (14.896): par de anos, nao dois valores independentes", 1994: "valor identico a 1993 (14.896): par de anos, nao dois valores independentes"})
add_serie("amb", "amb_prodes_amz", "INPE-PRODES-estimativa(Nota Tecnica 2026-10-16)",
          "ESTIMATIVA PRODES 2026 (1 ago 2025 a 31 jul 2026): 271 de 516 tiles, nao consolidada",
          {2026: prodes[2026]}, "km2/ano", "nunca entra na media da serie consolidada; metodo de amostragem diferente do consolidado",
          lambda a: "PRODES-estimativa-271tiles", "linha-a-parte", "PRODES 2026 estimativa (Nota Tecnica 2026-10-16, 271 tiles)", intervalo=intervalo_prodes)
add_serie("amb", "amb_prodes_amz", "INPE-PRODES-estimativa(Nota Tecnica PRODES 2024 consolidada, Tabela 3)",
          "ESTIMATIVA PRODES 2024 divulgada em outubro de 2024 (268 tiles), publicada ANTES da taxa consolidada de 6.518",
          {2024: 6288}, "km2/ano", "outra vintage do mesmo ano (consolidado = 6.518); lida da Tabela 3 de bruto/inpe_nt_prodes_2024_consolidada.pdf",
          lambda a: "PRODES-estimativa-268tiles", "vintage-anterior", "PRODES 2024 estimativa (out/2024, 268 tiles)", intervalo=intervalo_prodes)

# ============================================================================= DEMOCRACIA
owid = list(csv.DictReader(bruto("democracia", "bruto/owid_vdem_polyarchy_BRA.csv").open(encoding="utf-8")))
vdem = {int(r["year"]): float(r["electdem_vdem__estimate_best"]) for r in owid if r["entity"] == "Brazil" and r["electdem_vdem__estimate_best"] != ""}
add_serie("dem", "dem_polyarchy", "V-Dem-v16(via OWID, CC BY 4.0)",
          "indice de democracia eleitoral v2x_polyarchy, 0-1, estimativa pontual (sem intervalo de credibilidade neste arquivo)",
          vdem, "indice 0-1",
          "V-Dem v16 (2026-03-17) por redistribuicao OWID; o zip oficial v16 (26.867.425 bytes) nao foi baixado (> 25 MB). Arquivo bruto traz todos os paises",
          lambda a: "V-Dem-v16", "primario", "V-Dem v16 (OWID, 2026-03-17)")
pol = {}
for r in csv.DictReader(bruto("democracia", "bruto/polity5_Brazil_derivado.csv").open(encoding="utf-8")):
    y, p2 = int(r["year"]), int(r["polity2"])
    if p2 > -66:
        pol[y] = p2
add_serie("dem", "dem_polity2", "Polity5-p5v2018(CSP)",
          "polity2, -10 (autocracia) a +10 (democracia); serie vai ate 2018", pol, "pontos -10..10",
          "sensibilidade; Polity5 termina em 2018; valores especiais -66/-77/-88 (interrupcao, anarquia, transicao) removidos se houver",
          lambda a: "Polity5", "sensibilidade", "Polity5 p5v2018 (arquivo de 2023-02-28)")
fh_rows = list(xlsx_min.ler(str(bruto("democracia", "bruto/freedomhouse_FIW_1973-2024.xlsx")), "Country Ratings, Statuses "))
anos_fh = fh_rows[1]
brz = [r for r in fh_rows if r and r[0].strip() == "Brazil"][0]
fh_pr, fh_cl, fh_nota = {}, {}, {}
for c in range(1, len(anos_fh), 3):
    y = anos_fh[c].strip()
    if y.isdigit() and c + 1 < len(brz):
        try:
            fh_pr[int(y)] = int(brz[c]); fh_cl[int(y)] = int(brz[c + 1])
        except ValueError:
            pass
    elif y:
        fh_nota[y] = (brz[c], brz[c + 1])
add_serie("dem", "dem_fh_direitos_politicos", "FreedomHouse-FIW-1973-2024",
          "Freedom House, direitos politicos, 1 (mais livre) a 7; ano = 'year under review'",
          fh_pr, "pontos 1..7", "sensibilidade; ESCALA INVERTIDA (1 e o melhor); edicao 2024; licenca nao verificada: so as 2 notas de Brasil sao reproduzidas",
          lambda a: "FH", "sensibilidade", "Freedom in the World 2024")
add_serie("dem", "dem_fh_liberdades_civis", "FreedomHouse-FIW-1973-2024",
          "Freedom House, liberdades civis, 1 (mais livre) a 7; ano = 'year under review'",
          fh_cl, "pontos 1..7", "sensibilidade; ESCALA INVERTIDA (1 e o melhor); edicao 2024",
          lambda a: "FH", "sensibilidade", "Freedom in the World 2024")

# ----------------------------------------------------------------------------- grava series
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]
for dom, rows in SERIES_ROWS.items():
    with (SERIES / f"{dom}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)

# ----------------------------------------------------------------------------- janelas
def fmt(x):
    return "" if x is None else (f"{x:.4f}".rstrip("0").rstrip(".") if isinstance(x, float) else str(x))


# regra de atribuicao alternativa (robustez): ano PRODES T tratado como o ano-calendario T-1 (data de inicio, ago)
_pv = META[("amb_prodes_amz", "PRODES TerraBrasilis rates2026.json (atualizado 2026-10-16)")]
META[("amb_prodes_amz|atribuicao-alternativa:ano-calendario-de-inicio", "PRODES TerraBrasilis rates2026.json (atualizado 2026-10-16)")] = {
    **_pv, "intervalo": intervalo_calendario, "valores": {a - 1: v for a, v in _pv["valores"].items()},
    "segmento": lambda a, f=_pv["segmento"]: f(a + 1)}

JAN = []
for (ind, vint), m in list(META.items()):
    por_gov = {g["id"]: [] for g in GOVS}
    for ano in sorted(m["valores"]):
        ini, fim = m["intervalo"](ano)
        g = governo_do_intervalo(ini, fim)
        if g:
            por_gov[g].append((ano, m["valores"][ano]))
    for g in GOVS:
        obs = por_gov[g["id"]]
        base = {"governo": g["id"], "inicio": g["inicio"].isoformat(), "fim": g["fim"].isoformat()}

        def linha(ind_nome, o, seg):
            if not o:
                return {"indicador": ind_nome, **base, "media": "", "valor_inicial": "", "valor_final": "",
                        "n_anos": 0, "segmento_metodo": seg or "sem dado no ano de maioria do mandato", "vintage": vint}
            vs = [v for _, v in o]
            return {"indicador": ind_nome, **base, "media": fmt(statistics.mean(vs)),
                    "valor_inicial": f"{fmt(o[0][1])} ({o[0][0]})", "valor_final": f"{fmt(o[-1][1])} ({o[-1][0]})",
                    "n_anos": len(o), "segmento_metodo": seg, "vintage": vint}

        segs = []
        for a, _ in obs:
            s = m["segmento"](a)
            if s not in segs:
                segs.append(s)
        seg_txt = " + ".join(segs) if len(segs) <= 1 else " + ".join(segs) + " (CRUZA QUEBRA DE METODO)"
        JAN.append(linha(ind, obs, seg_txt))
        if len(segs) > 1:                       # regra 4 do pre-registro: comparacao dentro de um unico metodo
            for s in segs:
                JAN.append(linha(f"{ind}|{s}", [(a, v) for a, v in obs if m["segmento"](a) == s], s))

with (RAIZ / "janelas.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["indicador", "governo", "inicio", "fim", "media", "valor_inicial", "valor_final",
                                      "n_anos", "segmento_metodo", "vintage"])
    w.writeheader()
    w.writerows(JAN)

# ----------------------------------------------------------------------------- medidas de sobreposicao (para quebras.csv)
MED = {}
# (1) FAO: SOFI 2015 vs vintage atual
MED["fao_2001"] = (11.2, pou[2001])
MED["fao_2006"] = (5.0, pou[2006])      # SOFI2015 '<5,0' vs atual
MED["fao_2011"] = (5.0, pou[2011])
# (2) WUENIC rev2025 vs WDI
dif = {a: wuenic[a] - wb_dtp[a] for a in wuenic if a in wb_dtp}
MED["wuenic_wdi_n"] = len(dif)
MED["wuenic_wdi_difs"] = {a: d for a, d in dif.items() if abs(d) > 0}
MED["wuenic_wdi_absmedia"] = statistics.mean(abs(d) for d in dif.values())
# (3) WUENIC vs administrativa
da = {a: dtp["ADMIN"][a] - wuenic[a] for a in wuenic if a in dtp["ADMIN"]}
MED["admin_menos_wuenic"] = da
# (4) populacao: projecao x censo
MED["pop_censo_vs_proj"] = {a: (popcenso[a], popproj[a]) for a in popcenso if a in popproj and a in (1980, 1991, 2000, 2010, 2022)}
MED["efeito_taxa_censo"] = {a: popproj[a] / popcenso[a] - 1 for a in MED["pop_censo_vs_proj"]}
# (5) PRODES estimativa x consolidado 2024 (nota tecnica): 6.288 -> 6.518
MED["prodes_2024"] = (6288, 6518, 6518 / 6288 - 1)
# (6) MMEIG modelado x nacional
raz = {a: mmr_ne[a] / mmr[a] for a in mmr_ne if a in mmr}
MED["mmr_ne_sobre_modelo"] = raz
# (7) Ipea x TabNet
rec = {}
for a in homic_n:
    if a in homic9:
        rec[a] = homic_n[a] - homic9[a]
    elif a in agress10:
        rec[a] = homic_n[a] - agress10[a] - interv10.get(a, 0)
MED["ipea_menos_tabnet"] = rec
MED["indet_saltos"] = {"1989->1990": (homic9[1989] + indet9[1989], homic9[1990] + indet9[1990], homic9[1989], homic9[1990], indet9[1989], indet9[1990]),
                       "2018->2019": (agress10[2018] + indet10[2018], agress10[2019] + indet10[2019], agress10[2018], agress10[2019], indet10[2018], indet10[2019])}
MED["cid_1995_1996"] = (homic_n[1995], homic_n[1996], homic_n[1994], homic_n[1997])
MED["maldef"] = {a: maldef[a] for a in (1979, 1985, 1990, 1995, 1996, 2000, 2010, 2024)}

json.dump({k: ({str(a): b for a, b in v.items()} if isinstance(v, dict) else v) for k, v in MED.items()},
          (RAIZ / "saida_medidas.json").open("w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("series:", {d: len(r) for d, r in SERIES_ROWS.items()}, "| janelas:", len(JAN))
print("FH ano/status extras:", fh_nota)
for k, v in MED.items():
    print(k, v if not isinstance(v, dict) or len(v) < 12 else {a: v[a] for a in list(v)[:12]})


# ============================================================================= quebras.csv
def pct(x, n=1):
    return f"{x * 100:+.{n}f}%".replace(".", ",")


Q = []


def quebra(ind, serie, data, antigo, novo, razao, url, trecho, direcao, como_dir, efeito, como_med, aprim, tipo):
    assert tipo in ("metodo_estatistico", "mudanca_de_regra", "revisao_de_vintage"), tipo
    assert direcao in ("eleva", "reduz", "ambigua", "desconhecida"), direcao
    assert aprim in ("sim", "nao", "nao_declarado"), aprim
    Q.append({"indicador": ind, "serie": serie, "data_quebra": data, "tipo_de_quebra": tipo, "metodo_antigo": antigo,
              "metodo_novo": novo, "razao_declarada_pela_fonte": razao, "fonte_primaria_url": url, "trecho_citado": trecho,
              "direcao_do_efeito": direcao, "como_a_direcao_foi_determinada": como_dir, "efeito_medido": efeito,
              "como_medido": como_med, "apresentada_como_aprimoramento": aprim})


NT96 = "http://tabnet.datasus.gov.br/cgi/sim/Mortalidade_Geral_1996_2012.pdf (copia: seguranca/bruto/datasus_nota_Mortalidade_Geral_1996_2012.pdf)"
n94, n95, n96, n97 = homic_n[1994], homic_n[1995], homic_n[1996], homic_n[1997]
SEMOV = "sem sobreposicao"

# ---- seguranca / SIM
quebra("seg_homic_taxa", "SIM homicidios (Ipeadata AVIOL12_HOMIC)", "1996-01-01",
       "CID-9: E960-E978 (+E990-E999 no rotulo do Ipeadata)", "CID-10: X85-Y09 (agressoes) + Y35 (intervencao legal)",
       "adocao da 10a revisao da CID; a nota do DATASUS nao discute o efeito sobre as series",
       NT96,
       "A partir de 1996, as declarações de óbito passaram a ser codificadas utilizando-se a 10ª Revisão da Classificação Internacional de Doenças - CID-10. Até então, era utilizada a 9ª Revisão - CID-9. Devido às diferenças entre as revisões, não foi possível gerar uma lista que as compatibilizasse.",
       "desconhecida", "a fonte diz que nao ha lista de compatibilizacao; nao ha ano codificado nas duas revisoes nos brutos baixados",
       SEMOV, f"nenhum ano com dupla codificacao; apenas variacao anual vizinha, descritiva: 1994-95 {pct(n95 / n94 - 1)}, 1995-96 {pct(n96 / n95 - 1)}, 1996-97 {pct(n97 / n96 - 1)}",
       "nao_declarado", "mudanca_de_regra")
quebra("seg_indet_pct", "SIM causa de intencao indeterminada (TabNet)", "1996-01-01",
       "CID-9: grupo E56/E560 'Lesoes em que se ignora acidente ou intencao' (E980-E989)", "CID-10: grupo 'Eventos (fatos) cuja intencao e indeterminada' (Y10-Y34)",
       "mesma troca de revisao (ver linha CID-9/CID-10); rotulos dos grupos conferidos nas tabelas baixadas",
       "http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sim/cnv/ext10br.def e ?sim/cnv/ext09br.def (POST; brutos em seguranca/bruto/tabnet_ext09_grupo_ano.html e tabnet_ext10_grupo_ano.html)",
       "CID-9 '.. E560 Lesões em que se ignora acident ou intenc' (1995: 10.196) | CID-10 'Eventos (fatos) cuja intenção é indeterminada' (1996: 9.820)",
       "desconhecida", "equivalencia de codigos E980-E989/Y10-Y34 NAO verificada contra o texto das duas CID; so os rotulos do DATASUS",
       SEMOV, f"nenhum ano duplo; 1995 {indet9[1995]} -> 1996 {indet10[1996]} (descritivo)", "nao_declarado", "mudanca_de_regra")
quebra("seg_homic_taxa", "SIM intervencao legal (dentro de 'homicidios' do Ipeadata)", "1996-01-01",
       "CID-9: Ipeadata rotula E990-E999 como 'Intervencoes legais' e as soma a E960-E978", "CID-10: Y35 (intervencao legal); TabNet agrupa Y35-Y36 'Intervencoes legais e operacoes de guerra'",
       "definicao do Ipeadata; o comentario da serie nao explica a escolha",
       "http://www.ipeadata.gov.br/api/odata4/Metadados (SERCODIGO AVIOL12_HOMIC; copia em social/bruto/ipea_metadados_all.json)",
       "Para o período de 1979 a 1995 foram considerados os códigos CIDs 9: E960-E978 (Homicídios e lesões provocadas intencionalmente outras pessoas) e E990-E999 (Intervenções legais). De 1996 em diante, foram utilizados os códigos CIDs 10: X85-Y09 (agressão) e Y35 (intervenção legal).",
       "ambigua", "o rotulo 'E990-E999 = intervencoes legais' nao foi conferido contra a CID-9; no CID-10 as intervencoes legais sao pequenas em 1996 (35 obitos) e crescem depois (2003: 491; 2024: 2.644)",
       SEMOV, "nenhum ano duplo; Ipeadata menos TabNet (E55 ou Agressoes+interv.) varia de {} a {} obitos/ano".format(min(rec.values()), max(rec.values())),
       "nao_declarado", "mudanca_de_regra")
quebra("seg_maldef_pct", "SIM causa mal definida (TabNet)", "1996-01-01",
       "CID-9 capitulo XVI 'Sintomas, sinais e afeccoes mal definidas'", "CID-10 capitulo XVIII 'Sintomas, sinais e achados anormais...'; TabNet oferece lista propria de 4 elementos de causas mal definidas",
       "mesma troca de revisao", NT96,
       "A causa de óbito pode ser recuperada segundo: 22 Capítulos 264 Grupos 2045 Categorias 144 elementos da Lista CID-BR 28 4 elementos da lista de causas mal definidas",
       "desconhecida", "mapeamento XVI -> XVIII nao verificado codigo a codigo",
       SEMOV, f"proporcao de mal definidas no total de obitos: 1995 {maldef[1995]:.1f}% -> 1996 {maldef[1996]:.1f}% (descritivo, sem duplo codigo)",
       "nao_declarado", "mudanca_de_regra")
quebra("seg_homic_taxa", "SIM fluxo e periodicidade de envio (cobertura)", "2009-02-11",
       "fluxo e prazos de envio de DO/DN definidos por normas anteriores (nao baixadas)", "Portaria SVS/MS 116/2009: regulamenta coleta, fluxo e periodicidade de envio de obitos e nascidos vivos",
       "regulamentar coleta de dados, fluxo e periodicidade (preambulo da Portaria)",
       "https://app.wiki.saude.es.gov.br/vigilancia/sistemas/portaria_116_2009_-_coleta_e_fluxo_sistemas.pdf (copia: seguranca/bruto/portaria_svs_116_2009_es.pdf; a copia do MPBA devolveu HTML de erro)",
       "PORTARIA Nº 116, DE 11 DE FEVEREIRO DE 2009 - Regulamenta a coleta de dados, fluxo e periodicidade de envio das informações sobre óbitos e nascidos vivos para os Sistemas de Informações em Saúde sob gestão da Secretaria de Vigilância em Saúde.",
       "desconhecida", "norma de fluxo/prazo; o sinal sobre a contagem de homicidios nao e determinavel sem serie de cobertura (nao baixada)",
       SEMOV, "serie de cobertura do SIM nao baixada; proxy descritivo de qualidade (mal definidas/total): 2000 {:.1f}% -> 2010 {:.1f}% -> 2024 {:.1f}%".format(maldef[2000], maldef[2010], maldef[2024]),
       "nao_declarado", "mudanca_de_regra")
quebra("seg_homic_taxa", "SIM formulario da Declaracao de Obito", "2011-01-01",
       "formulario antigo da DO", "novo formulario da DO (2011: os dois formularios usados simultaneamente)",
       "maior detalhamento das informacoes coletadas", NT96,
       "Em 2011, houve uma mudança no conteúdo da Declaração de Óbito, com maior detalhamento das informações coletadas. Para este ano, foram utilizados simultaneamente os dois formulários.",
       "desconhecida", "a nota remete a outro documento ('Consolidacao da base de dados de 2011') nao baixado",
       SEMOV, "contagens por formulario nao disponiveis nos brutos", "sim", "mudanca_de_regra")
quebra("seg_homic_taxa", "SIM atualizacao CID-10 v2019 no sistema", "2025-01-01",
       "CID-10 versao 2008 (vigente ate 2024)", "CID-10 v2019 (186 codigos novos, 235 descricoes alteradas, 105 excluidos)",
       "transicao da CID-10 para a CID-11 no Brasil", NT96,
       "Em janeiro de 2025, foi atualizada a CID10 v-2019 no Sistema de Informações sobre Mortalidade (SIM)... até 2024, a versão vigente da CID-10 era a de 2008.",
       "desconhecida", "afeta a tabulacao de codigos; efeito sobre agressoes (X85-Y09) nao examinado",
       SEMOV, "serie termina em 2024 (dado final); 2025 e preliminar e fora da serie", "nao_declarado", "mudanca_de_regra")
quebra("seg_homic_taxa", "denominador populacional (IBGE)", "2022-08-01",
       "populacao = Censo na data censitaria (Ipeadata POPTOT)", "populacao = IBGE Projecao revisao 2024, 1o jul (Ipeadata POP_PROJE)",
       "projecao intercensitaria da populacao", "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='POP_PROJE') e (SERCODIGO='POPTOT') (copias em economia-real/, derivados em seguranca/bruto/)",
       "projeção da evolução anual da população residente no Brasil até 1º jul. 2070, por sexo e idade, revisto em 2024",
       "reduz", "aritmetica: taxa = obitos/populacao; populacao projetada > Censo em 1991, 2000, 2010 e 2022, portanto a taxa com projecao e menor",
       "taxa(projecao)/taxa(censo)-1: " + "; ".join(f"{a} {pct(popcenso[a] / popproj[a] - 1)}" for a in sorted(MED['pop_censo_vs_proj'])),
       "razao populacao Censo / populacao projetada nos 5 anos de Censo em que as duas series existem (Ipeadata POPTOT x POP_PROJE); datas de referencia diferem (Censo ~1 ago/1 set, projecao 1 jul)",
       "nao_declarado", "revisao_de_vintage")
# ---- saude
quebra("sau_dtp3", "WUENIC (OMS/UNICEF)", "2025 (revisao de julho de 2026)",
       "WUENIC de revisao anterior (via WDI, atualizado 2026-10-08)", "WUENIC revisao 2025 (export WIISE, 2026-10-19)",
       "revisao anual das estimativas; nenhuma justificativa por pais nos arquivos baixados",
       "https://immunizationdata.who.int/ (export https://srhdpeuwpubsa-geecgzbpd5h0fueu.z01.azurefd.net/whdh/WIISE/export/coverage-data.xlsx)",
       "(sem nota de revisao baixada) valores: 2023 = 86 (rev. 2025) vs 90 (WDI); 2024 = 90 vs 91",
       "reduz", "diferenca aritmetica nova - antiga nos anos em que as duas vintages existem",
       "dif. rev.2025 menos WDI: " + "; ".join(f"{a}: {d:+.0f} pp" for a, d in sorted(MED["wuenic_wdi_difs"].items())) + f"; nos outros {MED['wuenic_wdi_n'] - len(MED['wuenic_wdi_difs'])} dos {MED['wuenic_wdi_n']} anos comuns a diferenca e zero",
       "comparacao ano a ano das duas vintages guardadas em series/sau.csv", "nao_declarado", "revisao_de_vintage")
quebra("sau_mortmat_nacional", "RMM nacional (SIM/SINASC, compilada pelo MMEIG)", "2008-06-05",
       "investigacao de obitos maternos sem obrigatoriedade nacional uniforme (norma anterior: Portaria 1.172/2004, citada no preambulo)", "Portaria GM/MS 1.119/2008: obitos maternos e de mulheres em idade fertil sao eventos de investigacao obrigatoria",
       "o real dimensionamento do obito materno e dificultado pelo sub-registro de obitos e pela subenumeracao da morte materna",
       "https://platform.who.int/docs/default-source/mca-documents/policy-documents/law/bra-mn-91-02-law-2008-prt-portaria-n---1-119--de-5-de-junho-de-2008.pdf (copia: saude/bruto/portaria_ms_1119_2008.pdf)",
       "Considerando que o real dimensionamento do óbito materno no Brasil é dificultado pelo sub-registro de óbitos e pela subenumeração da morte materna ... Art. 2º - Os óbitos maternos e os óbitos de mulheres em idade fértil, independentemente da causa declarada, são considerados eventos de investigação obrigatória",
       "ambigua", "o objetivo e achar mais mortes (tende a elevar a contagem), mas a serie nacional baixada cai de {} (2007) para {} (2008); sinal nao separavel".format(mmr_ne[2007], mmr_ne[2008]),
       SEMOV, "a serie nacional so existe como razao (denominador SINASC); nenhuma serie 'antes/depois' sob as duas regras",
       "sim", "mudanca_de_regra")
# ---- alimentacao
quebra("ali_pou", "FAO prevalencia de subalimentacao", "2015 -> 2026 (SOFI 2015 vs FAOSTAT 2026-07-10)",
       "SOFI 2015; limiar de censura '<5,0'", "FAOSTAT/SOFI 2026; limiar de censura '<2,5'",
       "nao declarada nos documentos baixados (o SOFI 2015 nao menciona revisao de seus numeros anteriores)",
       "https://www.fao.org/3/i4646e/i4646e.pdf (copia: alimentacao/bruto/fao_sofi2015_i4646e.pdf) e https://bulks-faostat.fao.org/production/Food_Security_Data_E_All_Data_(Normalized).zip",
       "SOFI 2015, Anexo, linha 'Brazil': PoU 14.8 (1990-92), 11.2 (2000-02), <5.0 (2005-07), <5.0 (2010-12), <5.0 (2014-16) | FAOSTAT 2026: 10.5 (2000-02), 5.1 (2005-07), 2.7 (2010-12)",
       "ambigua", "2000-02: novo menor que antigo; 2005-07: novo (5,1) maior que o teto antigo (<5,0); 2010-12: compativel",
       f"2000-02: {MED['fao_2001'][1]} - {MED['fao_2001'][0]} = {MED['fao_2001'][1] - MED['fao_2001'][0]:+.1f} pp; 2005-07: 5,1 vs '<5,0' (novo acima do teto antigo); 2010-12: 2,7 vs '<5,0' (compativel)",
       "comparacao dos 3 periodos trienais comuns as duas vintages; 1990-92 (14,8) so existe no SOFI 2015", "nao_declarado", "revisao_de_vintage")
quebra("ali_pou", "FAO prevalencia de subalimentacao", "2012 (media 2011-13) a 2020 e 2024 (media 2023-25)",
       "valor numerico publicado", "valor publicado como '<2,5' (censurado)",
       "convencao de censura abaixo de 2,5%",
       "https://api.worldbank.org/v2/indicator/SN.ITK.DEFC.ZS?format=json (copia: alimentacao/bruto/wbmeta_SN.ITK.DEFC.ZS.json); valores em alimentacao/bruto/fao_fs_Brazil_derivado.csv",
       "Data showing as 2.5 may signify a prevalence of undernourishment below 2.5%.",
       "eleva", "aritmetica: troca de um valor desconhecido abaixo de 2,5 por 2,5 so pode manter ou elevar o valor",
       SEMOV, f"{sum(1 for v in pou_nota.values() if v.startswith('CENSURADO'))} das {len(pou)} medias trienais estao censuradas (2011-13 a 2018-20 e 2023-25); o valor real nao e publicado",
       "nao_declarado", "metodo_estatistico")
# ---- ambiente
NTM = "https://data.inpe.br/biomasbr/wp-content/uploads/sites/3/2026/09/nt_deslocamentomascara.pdf (copia: ambiente/bruto/inpe_nt_deslocamentomascara_2026-09.pdf; nota datada de 31/07/2017, publicada em 29/09/2026)"
quebra("amb_prodes_amz", "PRODES Amazonia Legal", "1988 a 2000",
       "-", "PRODES Analogico: foto-interpretacao visual de ~220 cenas Landsat 5 TM impressas 1:250.000, digitalizadas manualmente",
       "descricao de metodo (nao e justificativa)", NTM,
       "Esta forma de atuação foi empregada durante o período 1988 a 2000 e recebeu o nome de PRODES Analógico.",
       "desconhecida", "a nota nao da efeito em km2", SEMOV, "nao ha duplo metodo em nenhum ano", "nao_declarado", "metodo_estatistico")
quebra("amb_prodes_amz", "PRODES Amazonia Legal", "2000 a 2005",
       "PRODES Analogico", "PRODES Digital: classificacao digital assistida por computador (SPRING)",
       "descricao de metodo", NTM,
       "Entre 2000 e 2005, o INPE passou a adotar o processo de interpretação via classificação digital assistida pelo computador para fazer a identificação das áreas desmatadas.",
       "desconhecida", "a nota nao da efeito em km2", SEMOV, "nao ha duplo metodo em nenhum ano; limites 2000/2001/2005/2006 na tabela de janelas sao leitura nossa do texto", "nao_declarado", "metodo_estatistico")
quebra("amb_prodes_amz", "PRODES Amazonia Legal", "apos 2005",
       "PRODES Digital (SPRING)", "TerraAmazon: foto-interpretacao com digitalizacao direta na tela",
       "descricao de metodo", NTM,
       "Após 2005, houve uma grande mudança na forma de gerenciar as informações do projeto... No PRODES voltou-se a utilizar a foto interpretação, mas digitalizando os polígonos diretamente na tela do computador.",
       "desconhecida", "a nota nao da efeito em km2", SEMOV, "nao ha duplo metodo em nenhum ano", "nao_declarado", "metodo_estatistico")
quebra("amb_prodes_amz", "PRODES Amazonia Legal (mascara vetorial)", "2015",
       "mascara vetorial com deslocamentos em relacao as imagens ortorretificadas", "mascara inteira ajustada ao Landsat 8 de 2013 (deslocamentos X/Y por cena de 0 a 240 m)",
       "deslocamento entre a mascara do PRODES e as imagens de satelite", NTM,
       "Em 2015 o INPE tomou a decisão de promover o ajuste de toda máscara vetorial do PRODES, tomando-se como base de referência as imagens ortorretificadas do Landsat 8 do ano de 2013.",
       "desconhecida", "a nota nao informa se o ajuste altera a area dos poligonos nem as taxas anuais ja divulgadas", SEMOV, "areas antes/depois do ajuste nao disponiveis nos brutos",
       "sim", "metodo_estatistico")
quebra("amb_prodes_amz", "PRODES Amazonia Legal (poligonos 2008-2012)", "2017",
       "poligonos 2008-2012 agregados na mascara", "poligonos 2008-2012 recuperados e ajustados; passam a ser identificaveis ano a ano",
       "atender demandas do setor de controle da cadeia produtiva da carne e da soja", NTM,
       "Em 2017 foi possível reprocessar esta mascara, principalmente para atender demandas do setor de controle da cadeia produtiva da carne e soja. A base de dados poligonal de 2008 a 2012 foi recuperada e ajustada",
       "desconhecida", "a nota nao informa efeito nas taxas", SEMOV, "taxas anuais de 2008-2012 antes/depois nao disponiveis", "sim", "revisao_de_vintage")
quebra("amb_prodes_amz", "PRODES Amazonia Legal (1993 e 1994)", "1993-1994",
       "-", "os anos 1993 e 1994 aparecem com o MESMO valor, 14.896 km2",
       "nenhuma justificativa baixada (rodape da tabela do INPE nao obtido: o portal da OBT devolve HTTP 401)",
       "https://terrabrasilis.dpi.inpe.br/app/prodes/dashboard/deforestation/files/rates2026.json (copia: ambiente/bruto/terrabrasilis_rates2026.json)",
       "(nenhum trecho) 1993: 14896; 1994: 14896 (soma dos 9 estados)",
       "desconhecida", "identidade exata dos 9 valores estaduais nos dois anos nao foi testada; so a soma",
       SEMOV, "dois anos de Itamar entram na janela com valor identico", "nao_declarado", "metodo_estatistico")
quebra("amb_prodes_amz", "PRODES estimativa x consolidado", "anual (2024 medido)",
       "estimativa de outubro: subconjunto de 268 tiles prioritarios (2024)", "taxa consolidada: 516 tiles (2024)",
       "a estimativa usa tiles prioritarios (>= 90% do desmatamento do ano anterior e dos avisos DETER); o consolidado cobre toda a Amazonia Legal",
       "https://data.inpe.br/biomasbr/wp-content/uploads/sites/3/2025/07/Nota_tecnica_PRODES_2024_consolidada.pdf (copia: ambiente/bruto/inpe_nt_prodes_2024_consolidada.pdf)",
       "Tabela 3: ALB estimativa 268 tiles 6.288 km2; consolidada 516 tiles 6.518 km2; variação 3,66%",
       "eleva", "diferenca aritmetica consolidado - estimativa (ALB total; por estado a diferenca vai de -0,55% a +39,13%)",
       f"2024: {MED['prodes_2024'][0]} -> {MED['prodes_2024'][1]} km2 ({pct(MED['prodes_2024'][2], 2)}); 2026 e apenas estimativa (3.335 km2, 271 tiles) e fica fora da media consolidada",
       "as duas vintages de 2024 estao em series/amb.csv", "nao_declarado", "revisao_de_vintage")
quebra("amb_prodes_amz", "PRODES Amazonia Legal (sensores)", "ate 2024 (data exata nao verificada)",
       "Landsat 5/7/8 (segundo a nota de mascara)", "Sentinel-2 MSI + Sentinel-1 SAR (+ALOS-2 PALSAR-2) no programa BiomasBR; deteccao >= 1 ha, contabilizacao >= 6,25 ha",
       "manter compatibilidade com a serie historica iniciada em 1988",
       "https://data.inpe.br/biomasbr/wp-content/uploads/sites/3/2025/07/Nota_tecnica_PRODES_2024_consolidada.pdf e .../2026/10/Nota_tecnica_EstimativaPRODES_AMZ_2026.pdf (copias em ambiente/bruto/)",
       "Foram registradas e mapeadas as áreas desmatadas maiores que 1 hectare. Porém, visando manter a compatibilidade com a série histórica iniciada em 1988, apenas os polígonos maiores que 6,25 hectares foram contabilizados para cálculo da taxa.",
       "desconhecida", "a propria fonte afirma compatibilidade mas nao mede o efeito; nao ha ano mapeado pelos dois sensores nos brutos",
       SEMOV, "-", "nao_declarado", "metodo_estatistico")
# ---- democracia
quebra("dem_polyarchy", "V-Dem v2x_polyarchy (via OWID)", "v15 (mar/2025) -> v16 (2026-03-17)",
       "V-Dem v15 (nao obtida)", "V-Dem v16, redistribuida por OWID com imputacao propria para alguns paises",
       "V-Dem revisa a serie inteira a cada versao; OWID declara imputacao para paises pequenos (arquivo de imputacao citado)",
       "https://ourworldindata.org/grapher/electoral-democracy-index e https://doi.org/10.23696/vdemds26 (copia da pagina: democracia/bruto/owid_pagina_metadados.html)",
       "Expert estimates of the extent to which political leaders are elected under comprehensive voting rights in free and fair elections, and freedoms of association and expression are guaranteed. | For more details on the imputation methodology and which countries are affected, refer to this file.",
       "desconhecida", "so a v16 foi obtida; o zip oficial v15 (25.953.685 bytes) e v16 (26.867.425 bytes) nao foi baixado (teto de 25 MB)",
       SEMOV, "v15 nao baixada", "nao_declarado", "revisao_de_vintage")
quebra("dem_fh_direitos_politicos", "Freedom House FIW", "1981-1989",
       "ano-calendario ('year under review' = 1972..1980)", "periodos de revisao nao-calendario (ex.: 'Nov.1984-Nov.1985'); ano-calendario so volta em 1990",
       "nao declarada", "https://freedomhouse.org/sites/default/files/2024-02/Country_and_Territory_Ratings_and_Statuses_FIW_1973-2024.xlsx (copia: democracia/bruto/freedomhouse_FIW_1973-2024.xlsx)",
       "linha 'Year(s) Under Review': 'Jan.1981-Aug. 1982', 'Aug.1982-Nov.1983', 'Nov.1983-Nov.1984', 'Nov.1984-Nov.1985', 'Nov.1985-Nov.1986', 'Nov.1986-Nov.1987', 'Nov.1987-Nov.1988', 'Nov.1988-Dec.1989'",
       "desconhecida", "periodos nao coincidem com o ano-calendario",
       SEMOV, "as 8 observacoes 1981-89 NAO foram convertidas em ano e ficam fora de series/dem.csv", "nao_declarado", "metodo_estatistico")

QC = ["indicador", "serie", "data_quebra", "tipo_de_quebra", "metodo_antigo", "metodo_novo", "razao_declarada_pela_fonte",
      "fonte_primaria_url", "trecho_citado", "direcao_do_efeito", "como_a_direcao_foi_determinada", "efeito_medido",
      "como_medido", "apresentada_como_aprimoramento"]
with (RAIZ / "quebras.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=QC)
    w.writeheader()
    w.writerows(Q)
print("quebras:", len(Q))
