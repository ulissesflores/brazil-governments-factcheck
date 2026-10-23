# SEST/MGI, Relatorio Agregado das Empresas Estatais Federais (RAEEF): resultado liquido por empresa (tabelas de 5 anos) e agregados. So le derivado/txt. python3 -I sest_raeef.py
import csv, json, re
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]
DOCS = {"19-20": ("sest-raeef-19-20", {"banco_do_brasil": 552, "caixa": 1592, "correios": 3075, "eletrobras": 3207, "petrobras": 5025}),
        "21-22": ("sest-raeef-21-22", {"banco_do_brasil": 2185, "caixa": 2566, "correios": 4692, "eletrobras": 2937, "petrobras": 7014})}
def num(s):
    s = s.strip()
    if s in ("-", "N.D.*", "N.D."):
        return None
    neg = s.startswith("(") or s.startswith("-")
    v = float(s.strip("()-").replace(".", "").replace(",", "."))
    return -v if neg else v
rows = []
for ed, (stem, emp) in DOCS.items():
    arq = "bruto/%s.pdf" % stem.replace("sest-raeef", "sest-raeef")
    r = man[arq]
    L = (RAIZ / ("derivado/txt/%s.txt" % stem)).read_text().split("\n")
    vint = "SEST/MGI RAEEF %s; baixado %s sha256 %s" % (ed, r["timestamp_utc"][:10], r["sha256"][:12])
    for e, s0 in emp.items():
        blk = L[s0 - 1: s0 + 120]
        h = next(((k, re.findall(r"20\d\d", l)) for k, l in enumerate(blk) if len(re.findall(r"\b20\d\d\b", l)) == 5 and not re.search(r"[A-Za-z]{4}", l.replace("Conta", ""))), None)
        k = next(k for k, l in enumerate(blk) if re.match(r"\s*Resultado L\S{0,3}quido", l))
        toks = re.findall(r"\(?-?[\d.]+(?:,\d)?\)?|(?<!\S)-(?!\S)|N\.D\.\*?", re.split(r"L\S{0,3}quido", blk[k], maxsplit=1)[1])
        vals = [num(t) for t in toks]
        assert h and len(vals) == 5, (ed, e, blk[k], toks)
        for ano, v in zip(h[1], vals):
            if v is None:
                continue
            un = "R$ mil (valores com decimais na edicao 21-22, inteiros na 19-20)"
            rows.append(("sest_resultado_liquido_%s_rs_mil" % e, "SEST/MGI, RAEEF %s (tabela 'Dados Contabeis' da empresa)" % ed, "Resultado liquido anual de %s, dados contabeis (consolidados quando a tabela diz 'consolidados'); edicao %s do relatorio" % (e, ed), int(ano), v, un, "linha %d do texto extraido de %s.pdf; valor negativo = prejuizo" % (s0 + k, stem), vint))
# agregados citados no texto da edicao 21-22
r = man["bruto/sest-raeef-21-22.pdf"]
vint = "SEST/MGI RAEEF 21-22; baixado %s sha256 %s" % (r["timestamp_utc"][:10], r["sha256"][:12])
L = (RAIZ / "derivado/txt/sest-raeef-21-22.txt").read_text()
for rx, ind, ano, v, d in [
    (r"lucro líquido recorde, de\s+R\$ 187,7 bilhões", "sest_lucro_liquido_estatais_controle_direto_rs_bi", 2021, 187.7, "Resultado liquido das empresas estatais federais de controle direto (47 empresas, segundo o painel 'Estatais Federais em Numeros')"),
    (r"R\$ 60,6 bilhões", "sest_lucro_liquido_estatais_controle_direto_rs_bi", 2020, 60.6, "idem, exercicio 2020 citado no texto da edicao 21-22 ('o triplo do valor apurado em 2020')"),
    (r"R\$ 101,0 Bi", "sest_dividendos_e_jcp_pagos_estatais_rs_bi", 2021, 101.0, "Dividendos e JCP pagos em 2021 por todas as estatais federais (relativos a anos anteriores e antecipacao do proprio exercicio)"),
    (r"R\$ 43 Bi", "sest_dividendos_e_jcp_pagos_a_uniao_rs_bi", 2021, 43.0, "Dividendos e JCP pagos a Uniao em 2021 (painel 'Estatais Federais em Numeros')")]:
    assert re.search(rx, L), rx
    rows.append((ind, "SEST/MGI, RAEEF 21-22 (texto)", d, ano, v, "R$ bilhoes", "numero arredondado do texto; perimetro: estatais federais de controle direto", vint))
rows.sort(key=lambda x: (x[0], x[3], x[1]))
with open(RAIZ / "series/sest-raeef-estatais.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(COLS); w.writerows(rows)
print(len(rows))
