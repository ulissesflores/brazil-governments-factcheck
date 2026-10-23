"""Extrai taxas de rendimento (aprovacao, reprovacao, abandono) por UF a partir de `bruto/`.

Uso:  python3 -I scripts/extrair.py [--cache DIR]
 - confere a cadeia de hash (manifest.jsonl) e o sha256 de cada bruto;
 - converte xls/xlsx com `soffice --headless --convert-to csv` (unica dependencia externa) e le o PDF de 1998
   com `pdftotext -layout`; sem rede;
 - grava series/edu_rendimento.csv, series/calibracao_2005.csv, series/sobreposicao_2007.csv e series/gates.txt.

Dois passes (nunca emendados sem marca):
  (i)  2007-2025: taxa PUBLICADA pelo INEP (planilhas 'Taxas de Rendimento por Brasil/Regioes/UFs');
  (ii) 1994-2005: CONTAGENS das Sinopses/Censo (aprovados, reprovados, afastados por abandono) -> taxa CALCULADA
       com a formula da Nota Tecnica 004/2011 (X / (APR+REP+ABA)). 1994-1995 so tem aprovados e reprovados.
"""
import collections
import csv
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contagens  # noqa: E402
import lib  # noqa: E402
import taxas  # noqa: E402
from ufs import UFS  # noqa: E402

SAIDA = os.path.join(lib.RAIZ, "series")
GATES = []


def gate(ok, msg):
    GATES.append(("OK  " if ok else "FALHA ") + msg)
    if not ok:
        print("FALHA:", msg, file=sys.stderr)


def manifest_por_arquivo():
    d = {}
    for raw in open(os.path.join(lib.RAIZ, "manifest.jsonl"), "rb"):
        r = json.loads(raw)
        d[r["arquivo"]] = r
    return d


def vintage_de(arq, man):
    r = man.get(arq)
    if not r:
        return arq
    m = re.search(r"/web/(\d{8})\d*id_/", r["url"])
    if m:
        t = m.group(1)
        return "%s; Wayback snapshot %s-%s-%s; registrado %s" % (os.path.basename(arq), t[:4], t[4:6], t[6:], r["timestamp_utc"][:10])
    return "%s; servidor INEP; registrado %s" % (os.path.basename(arq), r["timestamp_utc"][:10])


REDE_NORM = {"total": "total", "publico": "publica", "publica": "publica", "federal": "federal", "estadual": "estadual",
             "municipal": "municipal", "privada": "privada", "privado": "privada", "particular": "privada"}
NIVEL_TXT = {("ef", "total"): "ef_total", ("ef", "ai"): "ef_ai", ("ef", "af"): "ef_af", ("em", "total"): "em_total"}
NOME_NIVEL = {
    "ef_total": "ensino fundamental (total)", "ef_ai": "ensino fundamental, anos iniciais",
    "ef_af": "ensino fundamental, anos finais", "em_total": "ensino medio (total)",
}


def def_recorte(ano, nivel_chave):
    """Definicao do recorte de serie conforme o ano (3 definicoes distintas de 'anos iniciais')."""
    if nivel_chave == "ef_ai":
        if ano <= 2006:
            return "1a a 4a serie (ensino fundamental de 8 anos)"
        if ano <= 2011:
            return "1a a 4a serie / 1o ao 5o ano (rotulo INEP: EF de 8 e 9 anos misturados)"
        return "1o ao 5o ano (EF de 9 anos)"
    if nivel_chave == "ef_af":
        if ano <= 2006:
            return "5a a 8a serie (ensino fundamental de 8 anos)"
        if ano <= 2011:
            return "5a a 8a serie / 6o ao 9o ano (rotulo INEP: EF de 8 e 9 anos misturados)"
        return "6o ao 9o ano (EF de 9 anos)"
    return NOME_NIVEL[nivel_chave]


def processar_taxas(tmp, man):
    """Passe (i): taxas publicadas 2007-2025. Devolve dict {(ano,uf,rede,nivel,tipo): (valor, arquivo)}."""
    out = {}
    zips = sorted(f for f in os.listdir(lib.BRUTO) if re.match(r"tx_rend.*\.zip$", f))
    for z in zips:
        nome = z[:-4]
        d = os.path.join(tmp, "tx", nome)
        arqs = lib.extrair_zip(os.path.join(lib.BRUTO, z), d)
        csvs = []
        for a in arqs:
            b = os.path.basename(a).upper()
            if re.search(r"REGI|REG_", b) and "BRASIL_REGIOES_UFS" not in b:
                continue  # arquivo so de regioes
            csvs += lib.converter(a, os.path.join(d, "csv_" + re.sub(r"\W", "_", b)))
        n0 = len(out)
        for c in csvs:
            rows = lib.ler_csv(c)
            if not any(r and re.fullmatch(r"(19|20)\d\d", r[0].strip()) for r in rows):
                continue  # aba vazia
            for o in taxas.parse(rows, c):
                u = o["uf"]
                if u.startswith("REG:") or o["loc"] != "total":
                    continue
                rede = REDE_NORM.get(o["rede"])
                v = lib.num(o["raw"])
                if rede is None or v is None:
                    continue
                out[(o["ano"], u, rede, NIVEL_TXT[(o["nivel"], o["recorte"])], o["tipo"])] = (v, "bruto/" + z)
        anos = sorted({k[0] for k in out if out[k][1].endswith(z)})
        ufs = {k[1] for k in out if out[k][1].endswith(z)}
        gate(len(ufs) == 28 and len(anos) == 1, "%s: %d anos %s, %d UFs+BR (esperado 28)" % (z, len(anos), anos, len(ufs)))
        gate(len(out) > n0, z + ": linhas lidas")
    # soma = 100
    g = collections.defaultdict(dict)
    for (ano, u, rede, nv, tipo), (v, _) in out.items():
        g[(ano, u, rede, nv)][tipo] = v
    tot = bad = 0
    for k, v in g.items():
        if len(v) == 3:
            tot += 1
            if not 99.7 <= sum(v.values()) <= 100.3:
                bad += 1
    gate(bad == 0, "taxas publicadas: aprovacao+reprovacao+abandono em [99,7; 100,3] em %d de %d celulas (falhas %d)" % (tot - bad, tot, bad))
    return out


def converter_xls(tmp, nome_bruto, pasta):
    p = os.path.join(lib.BRUTO, nome_bruto)
    if nome_bruto.endswith(".zip"):
        arq = lib.extrair_zip(p, os.path.join(tmp, pasta + "_raw"), so=r"\.xlsx?$")
        assert len(arq) == 1, (nome_bruto, arq)
        p = arq[0]
    return lib.converter(p, os.path.join(tmp, pasta))


def processar_contagens(tmp):
    """Passe (ii): contagens 1994-2005. Devolve dict {(ano, uf, rede, nivel, recorte, tipo): n} e fontes."""
    fontes = [
        ("sinopse_educacao_basica_1995.xlsm", "s1995"), ("sinopse_educacao_basica_1996.xls", "s1996"),
        ("censo_1997.zip", "s1997"), ("sinopse_1999.zip", "s1999"), ("sinopse_2000.zip", "s2000"),
        ("sinopse_2001.zip", "s2001"), ("sinopse_2002.zip", "s2002"), ("censo_2005.zip", "s2005"),
        ("resultados_censo_escolar_2006.zip", "s2006"),
    ]
    res, origem = {}, {}
    for nome, pasta in fontes:
        converter_xls(tmp, nome, pasta)
        r, usados = contagens.ler_pasta(os.path.join(tmp, pasta))
        for k, v in r.items():
            res[k] = v
            origem[k] = "bruto/" + nome
        gate(len(usados) >= 2, "%s: %d tabelas de contagem lidas, anos %s" % (nome, len(usados), sorted({u[2] for u in usados})))
    # PDF do Censo 1998 (rendimento de 1997): texto via pdftotext
    pdf_zip = os.path.join(lib.BRUTO, "censo_miolo_1998.zip")
    arq = lib.extrair_zip(pdf_zip, os.path.join(tmp, "s1998_raw"), so=r"\.pdf$")
    txt = subprocess.run(["pdftotext", "-layout", arq[0], "-"], check=True, capture_output=True).stdout.decode("utf-8", "replace")
    r, usados = contagens.ler_pdf_texto(txt)
    for k, v in r.items():
        res[k] = v
        origem[k] = "bruto/censo_miolo_1998.zip"
    gate(len(usados) >= 10, "censo_miolo_1998.zip (PDF): %d tabelas de contagem lidas" % len(usados))
    return res, origem


def checar_contagens(res):
    """Gates: Total = soma das redes; soma das series confere; 28 localidades por (ano, tabela)."""
    falhas = 0
    n = 0
    for (ano, u, rede, nv, rec, tipo), v in list(res.items()):
        if rede != "Total" or rec == "soma_series_confere":
            continue
        partes = [res.get((ano, u, r, nv, rec, tipo)) for r in ("Federal", "Estadual", "Municipal", "Privada")]
        if all(p is None for p in partes):
            continue
        n += 1
        if abs(v - sum(p or 0 for p in partes)) > 2:
            falhas += 1
    gate(falhas == 0, "contagens: Total = Federal+Estadual+Municipal+Privada em %d de %d celulas (falhas %d)" % (n - falhas, n, falhas))
    bad = [k for k, v in res.items() if k[4] == "soma_series_confere" and v != 1.0]
    gate(not bad, "contagens por serie: Total = soma das series em todos os casos (falhas %d)" % len(bad))
    # anos x tipos disponiveis
    anos = sorted({k[0] for k in res})
    gate(True, "contagens: anos de referencia %s" % anos)


def calibrar_2005(res, tmp, taxas_pub):
    """Compara a taxa calculada das contagens de 2005 com a tabela 5.5 (taxas publicadas) do mesmo arquivo."""
    cs = [c for c in os.listdir(os.path.join(tmp, "s2006")) if c.endswith("-5.5.csv")]
    assert len(cs) == 1, cs
    rows = lib.ler_csv(os.path.join(tmp, "s2006", cs[0]))
    from ufs import uf as nu
    pub = {}
    for r in rows:
        u = nu(r[0]) if r else None
        if u and not u.startswith("REG") and len(r) >= 4:
            pub[u] = [lib.num(x) for x in r[1:4]]
    linhas = []
    for u, (a, rp, b) in pub.items():
        A, R, B = (res.get((2005, "BR" if u == "BR" else u, "Total", "ef", "total", t)) for t in ("aprovacao", "reprovacao", "abandono"))
        if None in (A, R, B) or None in (a, rp, b):
            continue
        t = A + R + B
        ca, cr, cb = 100 * A / t, 100 * R / t, 100 * B / t
        # proxy sem abandono
        pp = 100 * rp / (a + rp)
        cp = 100 * R / (A + R)
        linhas.append([u, a, rp, b, round(ca, 2), round(cr, 2), round(cb, 2), round(ca - a, 2), round(cr - rp, 2), round(cb - b, 2), round(pp, 2), round(cp, 2), round(cp - pp, 2)])
    with open(os.path.join(SAIDA, "calibracao_2005.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["uf", "aprov_publicada", "reprov_publicada", "aband_publicada", "aprov_calculada", "reprov_calculada", "aband_calculada",
                    "dif_aprov_pp", "dif_reprov_pp", "dif_aband_pp", "reprov_sobre_aprov_mais_reprov_publicada", "idem_calculada", "dif_proxy_pp"])
        w.writerows(linhas)
    n = len(linhas)
    ok15 = sum(1 for r in linhas if max(abs(r[7]), abs(r[8]), abs(r[9])) <= 0.15)
    mx_rep = max(abs(r[8]) for r in linhas)
    mx_ab = max(abs(r[9]) for r in linhas)
    mx_px = max(abs(r[12]) for r in linhas)
    gate(True, "calibracao 2005 (contagem -> taxa vs tabela 5.5 publicada, EF, %d localidades): %d dentro de 0,15 p.p. nas tres taxas; "
         "max |dif| reprovacao %.2f p.p.; abandono %.2f p.p.; proxy R/(A+R) %.2f p.p. (ver series/calibracao_2005.csv)" % (n, ok15, mx_rep, mx_ab, mx_px))
    return mx_rep, mx_ab, mx_px


def sobreposicao_2007(tmp, taxas_pub):
    """2007 esta em duas fontes: planilha tx_rendimento 2007 e 'Resultados Censo Escolar 2007' (6.6.x)."""
    cs = converter_xls(tmp, "sinopse_2007_antiga.zip", "s2007")
    alvo = [c for c in cs if c.endswith("-6.6.1.csv")]
    assert len(alvo) == 1, alvo
    rows = lib.ler_csv(alvo[0])
    from ufs import uf as nu
    linhas = []
    for r in rows:
        u = nu(r[0]) if r else None
        if u and not u.startswith("REG") and len(r) >= 4:
            a, rp, b = (lib.num(x) for x in r[1:4])
            pa, pr, pb = (taxas_pub.get((2007, u, "total", "ef_total", t), (None,))[0] for t in ("aprovacao", "reprovacao", "abandono"))
            if None in (a, rp, b, pa, pr, pb):
                continue
            linhas.append([u, a, rp, b, pa, pr, pb, round(a - pa, 2), round(rp - pr, 2), round(b - pb, 2)])
    with open(os.path.join(SAIDA, "sobreposicao_2007.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["uf", "aprov_resultados2007", "reprov_resultados2007", "aband_resultados2007", "aprov_tx_rendimento2007", "reprov_tx_rendimento2007",
                    "aband_tx_rendimento2007", "dif_aprov_pp", "dif_reprov_pp", "dif_aband_pp"])
        w.writerows(linhas)
    mx = max(max(abs(r[7]), abs(r[8]), abs(r[9])) for r in linhas) if linhas else None
    gate(bool(linhas), "sobreposicao 2007 (Resultados Censo Escolar 2007 6.6.1 x tx_rendimento 2007, EF total): %d localidades, max |dif| %s p.p." % (len(linhas), mx))


COLS = ["indicador", "fonte", "definicao_linha", "uf", "ano", "valor", "unidade", "nota", "vintage", "dependente_de_regra"]
TIPO_NOME = {"aprovacao": "taxa de aprovacao", "reprovacao": "taxa de reprovacao", "abandono": "taxa de abandono"}


def escrever(taxas_pub, cont, origem, man):
    linhas = []
    # --- passe (i): publicadas
    for (ano, u, rede, nv, tipo), (v, arq) in sorted(taxas_pub.items()):
        ind = "edu_%s_%s__%s" % (tipo, nv, rede)
        defl = "%s, %s, rede %s, localizacao total (INEP, taxa publicada); recorte: %s" % (TIPO_NOME[tipo], "Brasil" if u == "BR" else "UF", rede, def_recorte(ano, nv))
        linhas.append([ind, "INEP/Censo Escolar - Taxas de Rendimento (planilha publicada)", defl, u, ano, v, "%", "valor como publicado; arquivo " + os.path.basename(arq),
                       vintage_de(arq, man), "sim"])
    # proxy R/(A+R) a partir das publicadas
    g = collections.defaultdict(dict)
    for (ano, u, rede, nv, tipo), (v, arq) in taxas_pub.items():
        g[(ano, u, rede, nv)][tipo] = (v, arq)
    for (ano, u, rede, nv), d in sorted(g.items()):
        if "aprovacao" in d and "reprovacao" in d and d["aprovacao"][0] + d["reprovacao"][0] > 0:
            a, r = d["aprovacao"][0], d["reprovacao"][0]
            linhas.append(["edu_reprov_sobre_aprov_mais_reprov_%s__%s" % (nv, rede), "INEP/Censo Escolar - derivado das taxas publicadas",
                           "reprovacao/(aprovacao+reprovacao) x100, sem abandono no denominador; %s, rede %s; recorte: %s" % ("Brasil" if u == "BR" else "UF", rede, def_recorte(ano, nv)),
                           u, ano, round(100 * r / (a + r), 2), "%", "calculado de taxas com 1 casa decimal (erro de arredondamento ate ~0,1 p.p.)",
                           vintage_de(d["reprovacao"][1], man), "sim"])
    # --- passe (ii): contagens
    anos = sorted({k[0] for k in cont})
    redes = ["Total", "Federal", "Estadual", "Municipal", "Privada"]
    rmap = {"Total": "total", "Federal": "federal", "Estadual": "estadual", "Municipal": "municipal", "Privada": "privada"}
    for ano in anos:
        for u in ["BR"] + UFS:
            for rede in redes:
                for nvl, rec in (("ef", "total"), ("ef", "ai"), ("ef", "af"), ("em", "total")):
                    nv = NIVEL_TXT[(nvl, rec)]
                    c = {t: cont.get((ano, u, rede, nvl, rec, t)) for t in ("aprovacao", "reprovacao", "abandono")}
                    A, R, B = c["aprovacao"], c["reprovacao"], c["abandono"]
                    arq = origem.get((ano, u, rede, nvl, rec, "aprovacao")) or origem.get((ano, u, rede, nvl, rec, "reprovacao")) or ""
                    vint = vintage_de(arq, man) if arq else ""
                    if A is not None and R is not None and A + R > 0:
                        linhas.append(["edu_reprov_sobre_aprov_mais_reprov_%s__%s" % (nv, rmap[rede]), "INEP/Censo Escolar - contagens calculadas",
                                       "reprovados/(aprovados+reprovados) x100, sem abandono no denominador; %s, rede %s; recorte: %s" % ("Brasil" if u == "BR" else "UF", rmap[rede], def_recorte(ano, nv)),
                                       u, ano, round(100 * R / (A + R), 2), "%", "calculado de contagens (aprovados e reprovados) da Sinopse; ano de referencia = ano do rendimento",
                                       vint, "sim"])
                    if None not in (A, R, B) and A + R + B > 0:
                        t = A + R + B
                        for tipo, x in (("aprovacao", A), ("reprovacao", R), ("abandono", B)):
                            linhas.append(["edu_%s_%s__%s" % (tipo, nv, rmap[rede]), "INEP/Censo Escolar - contagens calculadas",
                                           "%s calculada = X/(aprovados+reprovados+afastados por abandono) x100; %s, rede %s; recorte: %s" % (TIPO_NOME[tipo], "Brasil" if u == "BR" else "UF", rmap[rede], def_recorte(ano, nv)),
                                           u, ano, round(100 * x / t, 2), "%",
                                           "calculado de contagens da Sinopse com a formula da NT 004/2011; em 2005 difere da taxa publicada em alguns UFs (ver calibracao_2005.csv)",
                                           vint, "sim"])
    with open(os.path.join(SAIDA, "edu_rendimento.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(COLS)
        w.writerows(linhas)
    gate(True, "edu_rendimento.csv: %d linhas" % len(linhas))


def main():
    os.makedirs(SAIDA, exist_ok=True)
    n, cab = lib.conferir_cadeia()
    gate(True, "cadeia de hash: %d arquivos conferidos; cabeca (sha256 da ultima linha) %s" % (n, cab))
    man = manifest_por_arquivo()
    cache = None
    if "--cache" in sys.argv:
        cache = sys.argv[sys.argv.index("--cache") + 1]
    with tempfile.TemporaryDirectory() as tdir:
        tmp = cache or tdir
        os.makedirs(tmp, exist_ok=True)
        taxas_pub = processar_taxas(tmp, man)
        cont, origem = processar_contagens(tmp)
        checar_contagens(cont)
        calibrar_2005(cont, tmp, taxas_pub)
        sobreposicao_2007(tmp, taxas_pub)
        escrever(taxas_pub, cont, origem, man)
    open(os.path.join(SAIDA, "gates.txt"), "w", encoding="utf-8").write("\n".join(GATES) + "\n")
    print("\n".join(GATES))


if __name__ == "__main__":
    main()
