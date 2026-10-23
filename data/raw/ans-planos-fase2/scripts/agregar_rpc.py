"""Agrega o conjunto ANS PDA-043 RPC (reajuste de planos coletivos, comunicado pelas operadoras) em histogramas por ano x grupo.
Streaming (nao carrega o CSV); percentual em centesimos como chave; saida: derivado/rpc_histogramas.json + rpc_por_ano.csv.
Grupos (CD_AGRUPAMENTO): AGRUP = 1 ou 2 (contrato no agrupamento = coletivo com menos de 30 beneficiarios, RN 565/2022);
NAO_AGRUP = 0 (inclui 30+ vidas E as excecoes legais de <30 fora do agrupamento); TODOS.  LG_NEGOCIACAO=1 (aviso de reajuste em negociacao) e excluido.
Uso: python3 -I scripts/agregar_rpc.py"""
import csv, sys, json, glob, pathlib, collections, hashlib, io
BASE = pathlib.Path(__file__).resolve().parent.parent
csv.field_size_limit(10**7)
arqs = sorted(glob.glob(str(BASE/"bruto/ans/rpc/*.csv"))) + [str(BASE/"bruto/ans/pda-043-rpc-201501.csv")]
arqs = sorted(set(arqs))
# H[(ano, grupo)] = {"hist": {centesimos: [n, benef]}, contadores}
H = collections.defaultdict(lambda: {"hist": collections.defaultdict(lambda: [0, 0]), "linhas": 0, "negoc_excluidas": 0, "parcelado": 0, "adesao_flag": 0, "benef_zero_ou_nulo": 0, "pc_vazio": 0})
# produtos (PDA-008): ID_PLANO -> (cobertura, contratacao)  [retrato atual do cadastro; ID_PLANO ausente = SEM_JOIN]
prod = {}
with open(BASE/"bruto/ans/produtos/pda-008-caracteristicas_produtos_saude_suplementar.csv", encoding="utf8", newline="") as f:
    for r in csv.DictReader(f, delimiter=";"):
        cob = "MED" if r["COBERTURA"].startswith("M") else ("ODO" if r["COBERTURA"].startswith("O") else "NA")
        gc = r["GR_CONTRATACAO"]; ct = "EMP" if gc == "Coletivo empresarial" else ("ADE" if gc == "Coletivo por adesão" else "OUT")
        prod[r["ID_PLANO"]] = (cob, ct)
por_arquivo = {}
for a in arqs:
    n = 0
    with open(a, encoding="utf8", errors="replace", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            n += 1
            ano = r["DT_INIC_APLICACAO"][:4]
            if r["LG_NEGOCIACAO"] == "1":
                for g in ("TODOS", "AGRUP" if r["CD_AGRUPAMENTO"] in ("1", "2") else "NAO_AGRUP"): H[(ano, g)]["negoc_excluidas"] += 1
                continue
            pc = r["PC_PERCENTUAL"].strip()
            ag = "AGRUP" if r["CD_AGRUPAMENTO"] in ("1", "2") else "NAO_AGRUP"
            cob, ct = prod.get(r["ID_PLANO"], ("SEM_JOIN", "SEM_JOIN"))
            grupos = ["TODOS", ag, f"{cob}|TODOS", f"{cob}|{ag}", f"{cob}|{ct}|TODOS", f"{cob}|{ct}|{ag}"]
            if not pc:
                for g in grupos: H[(ano, g)]["pc_vazio"] += 1
                continue
            v = round(float(pc.replace(",", ".")) * 100)
            try: w = int(r["QT_BENEF_COMUNICADO"] or 0)
            except ValueError: w = 0
            for g in grupos:
                d = H[(ano, g)]; d["linhas"] += 1
                h = d["hist"][v]; h[0] += 1; h[1] += max(w, 0)
                if w <= 0: d["benef_zero_ou_nulo"] += 1
                if r["LG_PARCELADO"] == "1": d["parcelado"] += 1
                if r["LG_ADESAO"] == "1": d["adesao_flag"] += 1
    por_arquivo[pathlib.Path(a).name] = n
    print(pathlib.Path(a).name, n, flush=True)
out = {f"{a}|{g}": {**{k: v for k, v in d.items() if k != "hist"}, "hist": {str(k): v for k, v in sorted(d["hist"].items())}} for (a, g), d in sorted(H.items())}
(BASE/"derivado/rpc_histogramas.json").write_text(json.dumps({"arquivos": por_arquivo, "dados": out}, ensure_ascii=False))
print("ok", len(out))
