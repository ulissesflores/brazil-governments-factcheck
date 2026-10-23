# vintage-do-infografico.csv: em que fonte/vintage/linha cada numero impresso de pobreza, Gini e expectativa de vida aparece.
# Le social/series/*.csv (derivados do recalcula.py do bloco social, brutos com hash no manifest de la) e o infografico transcrito.
# Rode: python3 -I gerar_vintage.py
import csv
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from carga import *  # noqa: E402,F401,F403

INFO = D.parent / "infografico-transcrito.csv"
SS = SO / "series"
TIPOS = {
    "pobreza": ("pobreza.csv", "pobreza_pct", "pobreza_ano", 1),
    "gini": ("gini.csv", "gini", "gini_ano", 2),
    "expectativa de vida": ("expvida.csv", "expectativa_vida_anos", "expvida_ano", 1),
}
# O grao de arredondamento do que esta impresso decide o que e "exatamente".


def arred(v, nd):
    return round(v + 1e-9, nd)


def parse_val(s):
    s = s.strip()
    aprox = s.startswith("~")
    m = re.search(r"[\d.]+", s.replace(",", "."))
    return float(m.group()), aprox


def parse_ano(s):
    anos = [int(x) for x in re.findall(r"\b(1[89]\d\d|20\d\d)\b", s)]
    if re.search(r"anos\s+(\d{4})", s):
        a = int(re.search(r"anos\s+(\d{4})", s).group(1))
        return a, a + 9, s.strip()
    return anos[0], anos[0], s.strip()


# prioridade da fonte na hora de eleger a "melhor correspondencia" (menor numero = mais plausivel como origem)
PRIO = ["IBGE-SIS2018", "IBGE-SIS2019", "IBGE-SIS2020", "IBGE-SIS2024", "IBGE-SIS2025", "IBGE-Tabuas2024", "IBGE-Tabua-como-publicada",
        "SIDRA", "IBGE-Projecao", "Ipeadata-DEPIS", "Ipeadata-DISOC_PPY", "Ipeadata-PGINI", "PIP", "WB", "Ipeadata"]


def prio(fonte):
    for i, p in enumerate(PRIO):
        if fonte.startswith(p):
            return i
    return len(PRIO)


def vintage_txt(fonte, linha):
    return f"{fonte} | {linha}"


info = list(csv.DictReader(open(INFO, encoding="utf-8")))
saida, sel = [], []
for tipo, (arq, cval, cano, nd) in TIPOS.items():
    base = list(csv.DictReader(open(SS / arq, encoding="utf-8")))
    for r in base:
        r["ano"] = int(r["ano"])
        r["valor"] = float(r["valor"])
    for ln in info:
        gov = ln["coluna"]
        v, aprox = parse_val(ln[cval])
        a0, a1, rot = parse_ano(ln[cano])
        alvo = round(v, nd)
        cand = []
        for r in base:
            ok = (round(arred(r["valor"], nd)) == round(alvo) if aprox else abs(arred(r["valor"], nd) - alvo) < 1e-9)
            if ok:
                dist = 0 if a0 <= r["ano"] <= a1 else min(abs(r["ano"] - a0), abs(r["ano"] - a1))
                cand.append((dist, prio(r["fonte"]), r["ano"], r["fonte"], r["definicao_linha"], r["valor"]))
        cand.sort()
        no_ano = [c for c in cand if c[0] == 0]
        perto = [c for c in cand if 0 < c[0] <= 3]
        longe = [c for c in cand if c[0] > 3]
        # valores das fontes no ano rotulado (para ver o que a fonte diz AQUI)
        no_rotulo = sorted({(r["fonte"], r["definicao_linha"], r["ano"], r["valor"]) for r in base if a0 <= r["ano"] <= a1})
        exatos = {(c[3], c[4], c[2]) for c in cand}
        quase = []
        for r in base:
            if (r["fonte"], r["definicao_linha"], r["ano"]) in exatos:
                continue
            dist = 0 if a0 <= r["ano"] <= a1 else min(abs(r["ano"] - a0), abs(r["ano"] - a1))
            if dist <= 3 and abs(r["valor"] - v) <= 10 ** -nd and not aprox:
                quase.append((dist, prio(r["fonte"]), r["ano"], r["fonte"], r["definicao_linha"], r["valor"]))
        quase.sort()
        melhor = (no_ano or perto or [None])[0]
        if melhor:
            if melhor[0] == 0:
                aval = "bate no ano rotulado"
            else:
                aval = f"bate em OUTRO ano ({melhor[2]}; deslocamento {melhor[2] - a0:+d} ano[s])"
        elif longe:
            aval = "so ha coincidencia a mais de 3 anos do rotulo (nao tratada como origem)"
        else:
            aval = "nao reproduz em nenhuma serie baixada"
        # para anos-rotulo unicos, lista curta do que as principais fontes dizem no ano
        resumo = "; ".join(f"{f}[{l[:34]}]={val}" for f, l, a, val in no_rotulo[:14])
        saida.append({
            "indicador": tipo, "governo_celula": gov, "valor_impresso": ln[cval], "ano_rotulo": rot,
            "avaliacao": aval,
            "melhor_correspondencia_fonte_vintage_linha": (vintage_txt(melhor[3], melhor[4]) if melhor else ""),
            "melhor_correspondencia_ano": (melhor[2] if melhor else ""),
            "melhor_correspondencia_valor": (melhor[5] if melhor else ""),
            "outras_correspondencias_ate_3_anos": " || ".join(f"{c[3]} | {c[4]} | {c[2]} = {c[5]}" for c in (no_ano + perto)[1:6]),
            "quase_correspondencias_ate_3_anos_diferenca_menor_que_1_unidade_da_ultima_casa": " || ".join(f"{c[3]} | {c[4]} | {c[2]} = {c[5]}" for c in quase[:4]),
            "coincidencias_a_mais_de_3_anos_mais_proximas": " || ".join(f"{c[3]} | {c[4]} | {c[2]} = {c[5]}" for c in longe[:3]),
            "o_que_as_fontes_dizem_no_ano_rotulo": resumo,
            "vintage_colada_na_linha": "",  # preenchido abaixo
        })
        sel.append((tipo, gov, melhor))

# vintage colada: por indicador, quantas fontes/linhas distintas aparecem nas melhores correspondencias
por_ind = {}
for s in saida:
    por_ind.setdefault(s["indicador"], []).append(s)
for ind, ls in por_ind.items():
    fontes = sorted({l["melhor_correspondencia_fonte_vintage_linha"] for l in ls if l["melhor_correspondencia_fonte_vintage_linha"]})
    sem = [l["governo_celula"] for l in ls if not l["melhor_correspondencia_fonte_vintage_linha"]]
    txt = (f"SIM: {len(fontes)} fonte/vintage/linha distintas nas celulas que reproduzem ({'; '.join(fontes)})"
           + (f"; sem origem identificada: {', '.join(sem)}" if sem else ""))
    for l in ls:
        l["vintage_colada_na_linha"] = txt if len(fontes) > 1 else "NAO: uma so fonte/vintage/linha"

CAB = list(saida[0].keys())
with open(H / "vintage-do-infografico.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=CAB)
    w.writeheader()
    w.writerows(saida)
json.dump([{"indicador": s["indicador"], "governo": s["governo_celula"], "melhor": m} for s, (_, _, m) in zip(saida, sel)],
          open(H / "saida" / "vintage_melhores.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(saida), "linhas")
for s in saida:
    print(s["indicador"][:6], s["governo_celula"][:14].ljust(14), s["valor_impresso"].ljust(6), s["ano_rotulo"][:20].ljust(20), s["avaliacao"][:48], "|", s["melhor_correspondencia_fonte_vintage_linha"][:60])
