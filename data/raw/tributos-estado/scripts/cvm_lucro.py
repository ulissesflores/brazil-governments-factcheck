# Lucro liquido consolidado de Petrobras, Banco do Brasil e Eletrobras nos DFP da CVM (2010-2025). So le os zips baixados. python3 -I cvm_lucro.py
import csv, io, json, re, zipfile
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]
EMP = {"33.000.167/0001-01": "petrobras", "00.000.000/0001-91": "banco_do_brasil", "00.001.180/0001-26": "eletrobras"}
rows, achou = [], set()
for y in range(2010, 2026):
    arq = "bruto/cvm-dfp/dfp_cia_aberta_%d.zip" % y
    if arq not in man or not (RAIZ / arq).exists():
        print("sem", arq); continue
    z = zipfile.ZipFile(RAIZ / arq)
    nome = [n for n in z.namelist() if n.endswith("DRE_con_%d.csv" % y)][0]
    rd = csv.DictReader(io.StringIO(z.read(nome).decode("latin-1")), delimiter=";")
    for r in rd:
        e = EMP.get(r["CNPJ_CIA"])
        if not e:
            continue
        cd, ds = r["CD_CONTA"], r["DS_CONTA"]
        total = cd.count(".") == 1 and re.match(r"(?i)lucro", ds) and "consolidado" in ds.lower() and "antes" not in ds.lower() and "operaç" not in ds.lower()
        ctrl = cd.count(".") == 2 and re.search(r"(?i)controladora", ds) and "não" not in ds.lower()
        if not (total or ctrl):
            continue
        escala = {"MIL": 1000, "UNIDADE": 1}[r["ESCALA_MOEDA"]]
        v = float(r["VL_CONTA"]) * escala / 1e6
        ano = int(r["DT_FIM_EXERC"][:4])
        achou.add((e, y))
        tipo = "lucro_liquido_consolidado" if total else "lucro_liquido_atribuido_a_controladora"
        rows.append(("cvm_%s_%s_rs_mi" % (e, tipo), "CVM Dados Abertos, DFP (DRE consolidada)",
                     "%s, exercicio %d, conta %s '%s'; edicao do DFP referente a %s, %s" % (e, ano, cd, ds, r["DT_REFER"], "exercicio ULTIMO da edicao" if r["ORDEM_EXERC"] == "ÚLTIMO" else "exercicio PENULTIMO reapresentado na edicao seguinte"),
                     ano, round(v, 3), "R$ milhoes correntes", "arquivo %s; versao %s da DFP; moeda %s escala %s" % (nome, r["VERSAO"], r["MOEDA"], r["ESCALA_MOEDA"]),
                     "DFP %d (dt_refer %s, versao %s), zip baixado %s sha256 %s" % (y, r["DT_REFER"], r["VERSAO"], man[arq]["timestamp_utc"][:10], man[arq]["sha256"][:12])))
rows = sorted(set(rows), key=lambda x: (x[0], x[3], x[7]))
with open(RAIZ / "series/cvm-lucro-petrobras-bb-eletrobras.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(COLS); w.writerows(rows)
print(len(rows), sorted({(e, y) for e, y in achou}) [:3], "empresas-anos:", len(achou))
