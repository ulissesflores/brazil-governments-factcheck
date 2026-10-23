#!/usr/bin/env python3
"""Recalcula, SEM REDE, as series sociais a partir de ./bruto e confere o infografico.

Uso:  python3 -I recalcula.py
Saidas (em ./series): pobreza.csv, gini.csv, expvida.csv, mortinf.csv, conferencia.md
Antes de ler, confere o sha256 de cada arquivo bruto contra manifest.jsonl (cadeia de hash).
Unico binario externo opcional: pdftotext (so para 2 PDFs; sem ele esses 2 blocos ficam de fora).
"""

import csv, hashlib, json, os, re, subprocess, sys, zipfile
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(AQUI, "bruto")
OUT = os.path.join(AQUI, "series")
os.makedirs(OUT, exist_ok=True)


# ---------- integridade: sha256 do bruto lido == manifest ----------
def verifica_manifest():
    man = os.path.join(AQUI, "manifest.jsonl")
    ok = ruim = 0
    for linha in open(man, "rb"):
        r = json.loads(linha)
        p = os.path.join(AQUI, r["arquivo"])
        if os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == r["sha256"]:
            ok += 1
        else:
            ruim += 1
            print("MANIFEST DIVERGE:", r["arquivo"])
    print(f"manifest: {ok} arquivos conferem, {ruim} divergem")
    if ruim:
        sys.exit(1)


# ---------- leitor minimo de xlsx (stdlib) ----------
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def _col(ref):
    n = 0
    for c in re.match(r"[A-Z]+", ref).group():
        n = n * 26 + ord(c) - 64
    return n - 1


def le_xlsx(path):
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    nomes = [s.get("name") for s in ET.fromstring(z.read("xl/workbook.xml")).find("m:sheets", NS)]
    out = {}
    for i, n in enumerate(nomes, 1):
        rows = []
        for r in ET.fromstring(z.read("xl/worksheets/sheet%d.xml" % i)).iter("{%s}row" % NS["m"]):
            row = {}
            for c in r.findall("m:c", NS):
                v = c.find("m:v", NS)
                t = c.get("t")
                if v is None:
                    val = None
                elif t == "s":
                    val = ss[int(v.text)]
                else:
                    val = v.text
                row[_col(c.get("r"))] = val
            rows.append(row)
        out[n] = rows
    return out


def vir(s):
    return float(s.replace(",", "."))


def jload(rel):
    return json.load(open(os.path.join(B, rel), encoding="utf-8"))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# cada linha: (indicador, fonte_id, descricao_da_linha_ou_def, ano, valor, unidade, nota)
P, G, E, M = [], [], [], []  # pobreza, gini, expvida, mortalidade infantil

# ================= POBREZA =================
# 1) PIP (Banco Mundial): 2017 PPP 2.15/3.65/6.85 e 2021 PPP 3.00/4.20/8.30
for ppp, linhas in ((2017, ("2.15", "3.65", "6.85")), (2021, ("3.00", "4.20", "8.30"))):
    for l in linhas:
        for r in jload(f"pip_ppp{ppp}_line{l}.json"):
            P.append(
                (
                    "pobreza",
                    "PIP",
                    f"US$ {l}/dia PPC{ppp}",
                    int(r["reporting_year"]),
                    round(r["headcount"] * 100, 2),
                    "%",
                    f"{r['survey_acronym']} {r['welfare_type']}",
                )
            )
            G.append(
                (
                    "gini",
                    "PIP",
                    "renda dom. per capita",
                    int(r["reporting_year"]),
                    round(r["gini"] * 100, 2) / 100,
                    "0-1",
                    f"{r['survey_acronym']} {r['comparable_spell']}",
                )
            ) if l == ("6.85" if ppp == 2017 else "8.30") else None
# 2) IBGE SIS (xlsx derivado dos zips oficiais): US$2,15 / 3,65 / 6,85 PPC2017 e 50% da mediana
for ed in ("2024", "2025"):
    wb = le_xlsx(f"{B}/xlsx{ed}/Tabela 2.17 (PobrCarac_BR).xlsx")
    nomes = ("US$ 2,15 PPC2017", "US$ 3,65 PPC2017", "US$ 6,85 PPC2017", "50% da mediana")
    for aba, rows in wb.items():
        if "CV" in aba:
            continue
        tot = next(r for r in rows if r.get(0) == "Total")
        for k, nm in enumerate(nomes):
            P.append(
                (
                    "pobreza",
                    f"IBGE-SIS{ed}",
                    nm,
                    int(aba),
                    round(num(tot[2 + k]), 2),
                    "%",
                    f"Tabela 2.17, edicao SIS {ed}",
                )
            )
    g = le_xlsx(f"{B}/xlsx{ed}/Tabela 2.13 (Indice_Gini_Geo).xlsx")
    for aba, rows in g.items():
        if "CV" in aba:
            continue
        br = next(r for r in rows if r.get(0) == "Brasil")
        G.append(
            (
                "gini",
                f"IBGE-SIS{ed}",
                "renda dom. per capita (PNADC)",
                int(aba),
                round(num(br[1]), 4),
                "0-1",
                f"Tabela 2.13, edicao SIS {ed}",
            )
        )
# 2b) IBGE SIS 2018/2019/2020 (linhas PPC 2011: 1,90 / 3,20 / 5,50), tabelas "hiato"/"outras medidas de pobreza"
for ed, arqs in (
    ("2018", ("Tabela 2.28", "Tabela 2.28a")),
    ("2019", ("Tabela 2.28", "Tabela 2.28a", "Tabela 2.28b")),
    ("2020", ("Tabela 2.25", "Tabela 2.25a", "Tabela 2.25b")),
):
    for a in arqs:
        wb = le_xlsx(f"{B}/xlsx{ed}/{a}.xlsx")
        for aba, rows in wb.items():
            txt = " ".join(v for r in rows for v in r.values() if isinstance(v, str))
            linha = re.search(r"US\$ (\d,\d) PPC 2011", txt).group(1)
            hdr = next(r for r in rows if any(v == "Percentual" for v in r.values()))
            col = min(k for k, v in hdr.items() if v == "Percentual")
            tot = next(r for r in rows if r.get(0) == "Total")
            P.append(
                (
                    "pobreza",
                    f"IBGE-SIS{ed}-PPC2011",
                    f"US$ {linha} PPC2011",
                    int(aba),
                    round(num(tot[col]), 2),
                    "%",
                    f"{a}, edicao SIS {ed}",
                )
            )
# 3) IBGE SIDRA/ODS (agregados 5877 nacional=US$8,30 PPC2021; 5817 internacional=US$3,00 PPC2021)
for ag, nm in (
    (5877, "linha nacional ODS US$ 8,30 PPC2021"),
    (5817, "linha internacional ODS US$ 3,00 PPC2021"),
):
    for ano, v in jload(f"sidra/dados_{ag}.json")[0]["resultados"][0]["series"][0]["serie"].items():
        P.append(("pobreza", f"SIDRA-{ag}", nm, int(ano), num(v), "%", "PNADC"))


# 4) Ipeadata
def ipea(cod, niv=("Brasil", "")):
    return [
        (r["VALDATA"][:4], r["VALVALOR"])
        for r in jload(f"ipea_{cod}.json")["value"]
        if r.get("NIVNOME") in niv and r["VALVALOR"] is not None
    ]


for cod, nm in (
    ("PNADS_PERCPOBRE300", "PPC$3,00 (2021)"),
    ("PNADS_PERCPOBRE420", "PPC$4,20 (2021)"),
    ("PNADS_PERCPOBRE830", "PPC$8,30 (2021)"),
):
    for a, v in ipea(cod):
        P.append(
            (
                "pobreza",
                f"Ipeadata-{cod}",
                nm,
                int(a),
                round(v, 2),
                "%",
                "PNAD harmonizada a PNADC (Souza&Hecksher 2025)",
            )
        )
for a, v in ipea("DISOC_PPY"):
    P.append(
        (
            "pobreza",
            "Ipeadata-DISOC_PPY",
            "linha propria Ipea = 2x indigencia (cesta FAO), 24 regioes; serie INTERROMPIDA",
            int(a),
            round(v, 2),
            "%",
            "PNAD; sem anos de Censo",
        )
    )
for a, v in ipea("P0"):
    P.append(
        (
            "pobreza",
            "Ipeadata-P0",
            "renda fam. per capita < 50% do SM de set/1991 (Atlas 1998)",
            int(a),
            round(v, 2),
            "%",
            "Censo",
        )
    )
for a, v in ipea("ADH_PMPOB"):
    P.append(
        (
            "pobreza",
            "Ipeadata-ADH_PMPOB",
            "renda dom. per capita <= R$140 (ago/2010)",
            int(a),
            round(v, 2),
            "%",
            "Censo (Atlas DH)",
        )
    )
for a, v in ipea("ADH_PIND"):
    P.append(
        (
            "pobreza",
            "Ipeadata-ADH_PIND",
            "renda dom. per capita <= R$70 (ago/2010)",
            int(a),
            round(v, 2),
            "%",
            "Censo (Atlas DH)",
        )
    )

# ================= GINI =================
for a, v in ipea("PGINI"):
    G.append(
        (
            "gini",
            "Ipeadata-PGINI",
            "renda dom. per capita (PNAD antiga, serie interrompida)",
            int(a),
            round(v, 4),
            "0-1",
            "PNAD; sem 1991, 1994, 2000, 2010",
        )
    )
for a, v in ipea("PNADCA_GINIUF"):
    G.append(
        (
            "gini",
            "Ipeadata-PNADCA_GINIUF",
            "renda dom. per capita (PNADC anual)",
            int(a),
            round(v, 4),
            "0-1",
            "PNADC",
        )
    )
for ano, v in jload("sidra/dados_7435.json")[0]["resultados"][0]["series"][0]["serie"].items():
    G.append(
        (
            "gini",
            "SIDRA-7435",
            "renda dom. per capita, precos medios do ano (PNADC)",
            int(ano),
            num(v),
            "0-1",
            "PNADC",
        )
    )
for a, v in ipea("PNADS_GINI"):
    G.append(
        (
            "gini",
            "Ipeadata-PNADS_GINI",
            "harmonizada: PNAD<=2011 multiplicada por fator que iguala 2012",
            int(a),
            round(v / 100, 4),
            "0-1",
            "Souza&Hecksher 2025",
        )
    )
for r in jload("wb_SI.POV.GINI.json")[1]:
    if r["value"] is not None:
        G.append(
            (
                "gini",
                "WB-WDI-SI.POV.GINI",
                "Banco Mundial (PIP)",
                int(r["date"]),
                round(r["value"] / 100, 4),
                "0-1",
                "",
            )
        )
for a, v in ipea("ADH_GINI"):
    G.append(
        (
            "gini",
            "Ipeadata-ADH_GINI",
            "renda dom. per capita, CENSO (Atlas DH)",
            int(a),
            round(v, 4),
            "0-1",
            "Censo",
        )
    )
try:
    tb = subprocess.run(
        ["pdftotext", "-layout", os.path.join(B, "fgv_rbe_642_gini_censos.pdf"), "-"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    m = re.search(r"Índice de Gini\s+(0,\d{3})\s+(0,\d{3})\s+(0,\d{3})\s+(0,\d{3})\s+(0,\d{3})", tb)
    for a, v in zip((1960, 1970, 1980, 1979, 1990), m.groups()):
        G.append(
            (
                "gini",
                "Bonelli&Ramos-RBE1995-T1",
                "PEA com rendimento nao-nulo; 1960/70/80 censos, 1979/90 PNAD",
                a,
                vir(v),
                "0-1",
                "bruto/fgv_rbe_642_gini_censos.pdf, Tabela 1",
            )
        )
except (OSError, subprocess.CalledProcessError, AttributeError):
    print("aviso: pdftotext ausente ou linha nao achada; bloco Bonelli&Ramos omitido")

# ================= EXPECTATIVA DE VIDA e MORTALIDADE INFANTIL =================
for r in jload("wb_SP.DYN.LE00.IN.json")[1]:
    if r["value"] is not None:
        E.append(
            (
                "expvida",
                "WB-WDI-SP.DYN.LE00.IN",
                "UN WPP via Banco Mundial",
                int(r["date"]),
                round(r["value"], 2),
                "anos",
                "",
            )
        )
for r in jload("wb_SP.DYN.IMRT.IN.json")[1]:
    if r["value"] is not None:
        M.append(
            (
                "mortinf",
                "WB-WDI-SP.DYN.IMRT.IN",
                "UN IGME via Banco Mundial",
                int(r["date"]),
                round(r["value"], 2),
                "por mil",
                "",
            )
        )
for a, v in ipea("DEPIS_ESVIDA"):
    E.append(
        (
            "expvida",
            "Ipeadata-DEPIS_ESVIDA",
            "IBGE Projecao (rev. 2018)",
            int(a),
            round(v, 2),
            "anos",
            "",
        )
    )
for a, v in ipea("DEPIS_TMI"):
    M.append(
        (
            "mortinf",
            "Ipeadata-DEPIS_TMI",
            "IBGE Projecao (rev. 2018)",
            int(a),
            round(v, 2),
            "por mil",
            "",
        )
    )
for a, v in ipea("EVNNEW"):
    if 1940 <= int(a):
        E.append(
            (
                "expvida",
                "Ipeadata-EVNNEW",
                "Atlas DH (PNUD) 1998/2000 - INATIVA",
                int(a),
                round(v, 2),
                "anos",
                "",
            )
        )
for ano, v in jload("sidra/dados_1174.json")[0]["resultados"][0]["series"][0]["serie"].items():
    E.append(
        (
            "expvida",
            "SIDRA-1174",
            "IBGE Projecao (rev. 2013), serie IDS ate 2014",
            int(ano),
            num(v),
            "anos",
            "",
        )
    )
for ano, v in jload("sidra/dados_1175.json")[0]["resultados"][0]["series"][0]["serie"].items():
    M.append(
        (
            "mortinf",
            "SIDRA-1175",
            "IBGE (serie encerrada), 1990-2009",
            int(ano),
            num(v),
            "por mil",
            "",
        )
    )
# tabuas completas (primeira publicacao de cada ano): e0 e 1000*q0 da linha de idade 0
TAB = {
    2000: "tabuas_ibge/x/TEXTO_BRASIL_TABUA_COMPLETA_DE_MORTALIDADE_AMBOS_OS_SEXOS_2000_1_DECIMAL_DOU.xlsx",
    2005: "tabuas_ibge/x/TABUAS_COMPLETAS_DE_MORTALIDADE_AMBOS_OS_SEXOS_2005.xlsx",
    2010: "tabuas_ibge/x/ambos_2010.xlsx",
}
for y in range(2014, 2021):
    TAB[y] = f"tabuas_ibge/x/ambos_os_sexos_{y}.xlsx"
for y in range(2021, 2025):
    TAB[y] = f"tabuas_ibge/ambos_os_sexos_{y}.xlsx"
for y, rel in sorted(TAB.items()):
    wb = le_xlsx(os.path.join(B, rel))
    rows = next(iter(wb.values()))
    r0 = next(r for r in rows if r.get(0) == "0")
    E.append(
        (
            "expvida",
            "IBGE-Tabua-como-publicada",
            f"Tabua Completa de Mortalidade {y} (publicada no ano seguinte)",
            y,
            round(num(r0[6]), 2),
            "anos",
            rel,
        )
    )
    M.append(
        (
            "mortinf",
            "IBGE-Tabua-como-publicada",
            f"Tabua Completa de Mortalidade {y}: 1000*q0",
            y,
            round(num(r0[1]), 2),
            "por mil",
            rel,
        )
    )
# agencia IBGE 28/11/2025 (tabelas de e0 e TMI 1940-2024 da Tabua 2024)
md = open(os.path.join(B, "ibge_agencia_tabuas2024_jina.md"), encoding="utf-8").read()
sec_e, sec_m = md.split("**Mortalidade infantil recua"), None
for linha in sec_e[0].splitlines():
    c = [x.strip() for x in linha.strip("|").split("|")]
    if re.fullmatch(r"\d{4}", c[0]) and len(c) >= 4:
        E.append(
            (
                "expvida",
                "IBGE-Tabuas2024-serie-vigente",
                "Agencia IBGE 28/11/2025 (reconstrucao 1940-2024)",
                int(c[0]),
                vir(c[1]),
                "anos",
                "total",
            )
        )
for linha in sec_e[1].split("**Dos 20 aos 24")[0].splitlines():
    c = [x.strip() for x in linha.strip("|").split("|")]
    if re.fullmatch(r"\d{4}", c[0]) and len(c) >= 5:
        M.append(
            (
                "mortinf",
                "IBGE-Tabuas2024-serie-vigente",
                "Agencia IBGE 28/11/2025 (reconstrucao 1940-2024)",
                int(c[0]),
                vir(c[1]),
                "por mil",
                "",
            )
        )
# IBGE 2010 (Projecao rev. 2008): e0 e TMI 1980/1991/2000/2009 (texto do PDF)
try:
    t = subprocess.run(
        ["pdftotext", "-layout", os.path.join(B, "ibge_liv98593.pdf"), "-"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    seg = t[t.index("Tabela 2 - Esperança de Vida ao Nascer") :]
    seg = seg[: seg.index("Variação total")]
    for linha in seg.splitlines():
        m = re.match(r"\s+(1980|1991|2000)\s+(\d\d,\d\d)\s+(?:\d,\d\d\s+)?(\d\d,\d\d)", linha)
        if m:
            E.append(
                (
                    "expvida",
                    "IBGE-Projecao-rev2008",
                    "IBGE 'Observacoes sobre a evolucao da mortalidade' (2010), Tabela 2",
                    int(m[1]),
                    vir(m[2]),
                    "anos",
                    "",
                )
            )
            M.append(
                ("mortinf", "IBGE-Projecao-rev2008", "idem", int(m[1]), vir(m[3]), "por mil", "")
            )
    if re.search(r"2009\s+73,17", t) and "22,47" in t:
        E.append(("expvida", "IBGE-Projecao-rev2008", "idem", 2009, 73.17, "anos", "texto p.7"))
        M.append(("mortinf", "IBGE-Projecao-rev2008", "idem", 2009, 22.47, "por mil", "texto p.8"))
except (OSError, subprocess.CalledProcessError):
    print("aviso: pdftotext ausente; bloco IBGE-Projecao-rev2008 omitido")


def grava(nome, linhas):
    with open(os.path.join(OUT, nome), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota"])
        for l in sorted(set(linhas), key=lambda x: (x[1], x[2], x[3])):
            w.writerow(l)


# ================= CONFERENCIA do infografico =================
INFO = {
    "pobreza": [
        (1990, 42.6, "1990 (referencia)"),
        (1994, 34.0, "~34"),
        (2002, 28.9, ""),
        (2010, 21.4, ""),
        (2014, 22.1, ""),
        (2018, 26.5, ""),
        (2021, 31.6, ""),
        (2024, 27.4, ""),
    ],
    "gini": [
        (1970, 0.59, "anos 1970"),
        (1992, 0.60, ""),
        (2002, 0.59, ""),
        (2010, 0.53, ""),
        (2014, 0.52, ""),
        (2018, 0.54, ""),
        (2021, 0.58, ""),
        (2024, 0.51, ""),
    ],
    "expvida": [
        (1970, 62.6, ""),
        (1990, 67.1, ""),
        (2000, 70.4, ""),
        (2010, 73.9, ""),
        (2015, 75.2, ""),
        (2018, 75.7, ""),
        (2021, 72.8, ""),
        (2023, 76.4, ""),
    ],
}
SERIES = {"pobreza": P, "gini": G, "expvida": E}
TOL = {"pobreza": 0.05, "gini": 0.0051, "expvida": 0.051}


def confere():
    L = [
        "# Conferencia automatica (gerada por recalcula.py)\n",
        "Para cada valor do infografico: (a) o que as fontes dizem NO ANO rotulado; (b) em que ano/fonte o MESMO valor aparece (tolerancia = arredondamento da casa decimal do infografico). Isto detecta valor certo com ano errado.\n",
    ]
    for ind, alvos in INFO.items():
        L.append(f"\n## {ind}\n")
        for ano, alvo, obs in alvos:
            no_ano = sorted({f"{s[1]}[{s[2][:28]}]={s[4]}" for s in SERIES[ind] if s[3] == ano})
            bate = sorted(
                {
                    (s[3], s[1], s[2][:34], s[4])
                    for s in SERIES[ind]
                    if abs(s[4] - alvo) <= TOL[ind]
                },
                key=lambda x: (abs(x[0] - ano), x[0], x[1]),
            )[:8]
            L.append(f"- **{ind} {ano} = {alvo}** {obs}")
            L.append(
                f"  - no ano {ano}: "
                + ("; ".join(no_ano) if no_ano else "NENHUMA fonte tem esse ano")
            )
            L.append(
                f"  - mesmo valor em: "
                + (
                    "; ".join(f"{a} {f} [{d}]={v}" for a, f, d, v in bate)
                    + " (8 mais proximos do ano rotulado)"
                    if bate
                    else "nenhum ano/fonte"
                )
            )
    open(os.path.join(OUT, "conferencia.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    verifica_manifest()
    grava("pobreza.csv", P)
    grava("gini.csv", G)
    grava("expvida.csv", E)
    grava("mortinf.csv", M)
    confere()
    print(
        "linhas:",
        {
            "pobreza": len(set(P)),
            "gini": len(set(G)),
            "expvida": len(set(E)),
            "mortinf": len(set(M)),
        },
    )
    print("ok -> series/")
