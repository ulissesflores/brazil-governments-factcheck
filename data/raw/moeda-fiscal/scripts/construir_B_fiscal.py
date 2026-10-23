"""Bloco B (fiscal): RTN Governo Central (receita, despesa, discricionarias) e NFSP por nivel.
Le SO disco: mecanismos-contabil/derivado/rtn/*.csv (planilha do Tesouro ja hasheada em mecanismos-contabil/manifest.jsonl)
e moeda-fiscal/bruto/bcb (SGS + CKAN). Sem rede. Rodar: python3 -I construir_B_fiscal.py"""
import csv, datetime, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import DADOS, PASTA, ckan, escrever, fmt, manifest, sgs, vintage

M = manifest()
HOJE = max(v[0] for v in M.values())[:10]
DL_A, DL_M = int(HOJE[:4]), int(HOJE[5:7])

# ------------------------------------------------------------------ RTN (Tesouro Nacional)
RTN = DADOS / "mecanismos-contabil/derivado/rtn"
cm = {}
for l in (DADOS / "mecanismos-contabil/manifest.jsonl").read_text(encoding="utf-8").splitlines():
    r = json.loads(l); cm[r["arquivo"]] = r
xl = cm["bruto/tesouro-rtn-serie-historica-jul26.xlsx"]
VINT_RTN = (f"mecanismos-contabil/bruto/tesouro-rtn-serie-historica-jul26.xlsx (boletim de jul/2026, 'dados sujeitos a alteracao'; "
            f"adquirido {xl['timestamp_utc']} sha256 {xl['sha256'][:12]}; CSV de aba em mecanismos-contabil/derivado/rtn/ via xlsx_para_csv.py)")


def ler(nome):
    return list(csv.reader((RTN / nome).open(encoding="utf-8")))


def token(label):
    t = label.strip().split()
    return t[0] if t else ""


def tabela(nome):
    """-> (cabecalho, {token: (label, [valores])}) a partir da linha 'Discriminação'; so a 1a ocorrencia de cada token."""
    r = ler(nome)
    h = next(i for i, row in enumerate(r) if row and row[0].strip() == "Discriminação")
    linhas = {}
    for row in r[h + 1:]:
        lab = row[0].strip() if row else ""
        if not lab or lab.startswith(("Obs", "Memorando")) or re.match(r"^\d+/ ", lab):
            continue
        t = lab.split()[0].rstrip(".")
        if t not in linhas:
            linhas[t] = (re.sub(r"\s+", " ", lab), row[1:])
    return r[h][1:], linhas


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# linhas da tabela 2.1 / 2.1-A (anual, caixa) e 1.1 (mensal)
L21 = [("1", "receita_total"), ("2", "transferencias_repartição_receita"), ("3", "receita_liquida"), ("4", "despesa_total"),
       ("4.1", "despesa_beneficios_previdenciarios"), ("4.2", "despesa_pessoal_e_encargos"), ("4.3", "despesa_outras_obrigatorias"),
       ("4.4", "despesa_poder_executivo_sujeita_programacao_financeira"), ("4.4.1", "despesa_obrigatorias_com_controle_de_fluxo"),
       ("4.4.2", "despesa_discricionarias"), ("5", "resultado_primario_acima_da_linha"), ("8", "resultado_primario_abaixo_da_linha"),
       ("9", "juros_nominais"), ("10", "resultado_nominal")]
L21 = [(a, b.replace("ç", "c").replace("ã", "a")) for a, b in L21]
SEM_PUB = {"4.4.1", "4.4.2"}  # a fonte grava 0 antes de 2008: nao e valor, e linha nao publicada


def emitir_anual(arq_rs, arq_pct, prefixo, tabela_nome, linhas_sel, nota_extra=""):
    cab, ln = tabela(arq_rs)
    cab2, ln2 = tabela(arq_pct)
    for tok, nome in linhas_sel:
        if tok not in ln or tok not in ln2:
            print("AVISO linha ausente", tok, nome, prefixo); continue
        for (cabx, lnx, un, sufixo, mult) in ((cab, ln, "R$ milhoes correntes", "rs_mi", 1.0), (cab2, ln2, "% do PIB", "pct_pib", 100.0)):
            label, vals = lnx[tok]
            # primeiro ano nao-zero para as linhas que a fonte so passa a publicar depois
            vv = [num(v) for v in vals]
            ini = next((i for i, v in enumerate(vv) if v not in (None, 0.0)), None) if tok in SEM_PUB else 0
            out = []
            for a, v in zip(cabx, vv):
                if v is None or not a.strip().isdigit():
                    continue
                i = cabx.index(a)
                if ini is None or i < ini:
                    continue
                out.append(dict(indicador=f"{prefixo}_{nome}_{sufixo}", fonte=f"Tesouro Nacional, RTN, tabela {tabela_nome}{'-A' if sufixo=='pct_pib' else ''}",
                                definicao_linha=label, ano=int(a), valor=fmt(v * mult), unidade=un,
                                nota=(nota_extra + ("; % do PIB = fracao da planilha x 100" if sufixo == "pct_pib" else "")).strip("; "), vintage=VINT_RTN))
            if tok in SEM_PUB and ini:
                if out:
                    out[0]["nota"] = (out[0]["nota"] + f"; anos anteriores a {out[0]['ano']}: a planilha grava 0, tratado como linha nao publicada (sem valor)").strip("; ")
            escrever(f"rtn_{prefixo}_{nome}_{sufixo}", out)


emitir_anual("13-2_1.csv", "14-2_1_A.csv", "gc_caixa", "2.1", L21, "Governo Central, conceito de caixa; 2025 e o ultimo ano fechado no boletim")
# tabela 2.5 (criterio valor pago, 2008+)
L25 = [("2", "despesa_total_valor_pago"), ("2.1", "beneficios_previdenciarios_valor_pago"), ("2.2", "pessoal_valor_pago"), ("2.3", "outras_obrigatorias_valor_pago"),
       ("2.4", "poder_executivo_programacao_financeira_valor_pago"), ("2.4.1", "obrigatorias_controle_fluxo_valor_pago"), ("2.4.2", "discricionarias_valor_pago"),
       ("m.2", "memo_discricionarias_creditos_extraordinarios_valor_pago")]
emitir_anual("21-2_5.csv", "22-2_5_A.csv", "gc_valor_pago", "2.5", L25, "criterio de valor pago, 2008 em diante")

# mensal (tabela 1.1, R$ milhoes correntes)
r = ler("01-1_1.csv")
h = next(i for i, row in enumerate(r) if row and row[0].strip() == "Discriminação")
serial = r[h][1:]
meses = []
for s in serial:
    s = s.strip()
    meses.append((datetime.date(1899, 12, 30) + datetime.timedelta(days=int(float(s)))) if re.match(r"^\d+(\.0+)?$", s) else None)
cabm, lnm = tabela("01-1_1.csv")
for tok, nome in [(a, b) for a, b in L21 if a in ("1", "3", "4", "5", "8", "9", "10")]:
    label, vals = lnm[tok]
    out = []
    for d, v in zip(meses, vals):
        x = num(v)
        if d is None or x is None:
            continue
        out.append(dict(indicador=f"gc_caixa_{nome}_mensal_rs_mi", fonte="Tesouro Nacional, RTN, tabela 1.1", definicao_linha=label, ano=d.year,
                        mes_ou_trimestre=d.month, valor=fmt(x), unidade="R$ milhoes correntes", nota="mensal; sem versao mensal em % do PIB na planilha", vintage=VINT_RTN))
    escrever(f"rtn_gc_caixa_{nome}_mensal_rs_mi", out)

# ------------------------------------------------------------------ NFSP (BCB SGS)
def nivel(titulo):
    return titulo.split("Total - ")[-1].strip()


def slug(s):
    s = s.lower()
    for a, b in (("á", "a"), ("ã", "a"), ("â", "a"), ("é", "e"), ("ê", "e"), ("í", "i"), ("ó", "o"), ("ô", "o"), ("õ", "o"), ("ú", "u"), ("ç", "c")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def conceito(titulo):
    if "Resultado primário" in titulo: return "primario"
    if "Resultado nominal" in titulo: return "nominal"
    if "Juros nominais" in titulo: return "juros_nominais"
    raise ValueError(titulo)


blocos = [("12m_pct_pib", list(range(5717, 5728)) + list(range(5750, 5761)) + list(range(5783, 5794))),
          ("fluxo_mensal_rs_mi", list(range(4573, 4584)) + list(range(4606, 4617)) + list(range(4639, 4650)))]
resumo = []
for tipo, cods in blocos:
    for cod in cods:
        c = ckan(cod)
        if c is None:
            print("AVISO CKAN ausente", cod); continue
        tit = c["title"]; niv = nivel(tit); con = conceito(tit)
        arq = f"bruto/bcb/sgs_{cod}.json"
        dados = {(a, m): v for d, m, a, v in sgs(arq) if v is not None and (a, m) < (DL_A, DL_M)}
        base = f"nfsp_{con}_{slug(niv)}"
        un = c.get("unidade_medida", "")
        mensal = [dict(indicador=f"{base}_{tipo}", fonte=f"BCB SGS {cod}", definicao_linha=tit, ano=a, mes_ou_trimestre=m, valor=fmt(v),
                       unidade=un, nota="sinal conforme a fonte (ver RESULTADO.md); NFSP sem desvalorizacao cambial", vintage=vintage(arq))
                  for (a, m), v in sorted(dados.items())]
        escrever(f"{base}_{tipo}_sgs{cod}", mensal)
        if tipo == "12m_pct_pib":
            anual = [dict(indicador=f"{base}_anual_pct_pib", fonte=f"BCB SGS {cod}", definicao_linha=tit + " [valor de dezembro = ano civil]", ano=a,
                          valor=fmt(v), unidade=un, nota="fluxo acumulado em 12 meses lido em dezembro = soma do ano civil em % do PIB; sinal conforme a fonte",
                          vintage=vintage(arq)) for (a, m), v in sorted(dados.items()) if m == 12]
            escrever(f"{base}_anual_pct_pib_sgs{cod}", anual)
        resumo.append((cod, tit, un, min(dados) if dados else None, max(dados) if dados else None, len(dados)))
with (PASTA / "derivado/nfsp_codigos_confirmados_ckan.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["sgs", "titulo_ckan", "unidade_ckan", "primeiro_mes", "ultimo_mes_completo", "meses"])
    for cod, tit, un, a, b, n in resumo:
        w.writerow([cod, tit, un, f"{a[0]}-{a[1]:02d}" if a else "", f"{b[0]}-{b[1]:02d}" if b else "", n])
print("ok", len(resumo), "series NFSP")
