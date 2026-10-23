"""Gera RESULTADO.md (tabelas a partir de derivado/*.csv; texto fixo no proprio script). Depois cola a saida do chain verify."""
import csv, pathlib, subprocess, json
BASE = pathlib.Path(__file__).resolve().parent.parent
T = {int(r["ano"]): r for r in csv.DictReader(open(BASE/"derivado/tabela_por_ano.csv"))}
J = {r["janela"]: r for r in csv.DictReader(open(BASE/"derivado/acumulados_janelas_ans.csv"))}
def v(x, d=2):
    return "" if x in ("", None) else f"{float(x):.{d}f}".replace(".", ",")
def n(x):
    return "" if x in ("", None) else f"{int(float(x)):,}".replace(",", ".")
linhas = []
for y in range(2000, 2027):
    r = T[y]
    linhas.append(f"| {y} | {v(r['ans_teto_individual_ciclo_maio_ano_pct'])} | {v(r['ipca_plano_saude_abr_ano_a_abr_ano_mais1_pct'])} | {v(r['ipca_plano_saude_dez_dez_pct'])} | {v(r['ipca_geral_dez_dez_pct'])} | {v(r['agrupamento_pda055_media_pond_benef_pct'])} | {v(r['rpc_med_mediana_pct'])} | {v(r['rpc_med_media_pond_benef_pct'])} | {v(r['rpc_med_agrup_lt30_media_pond_benef_pct']) if y >= 2013 else ''} | {v(r['rpc_med_fora_agrup_media_pond_benef_pct'])} | {n(r['rpc_med_benef'])} |")
tab_ano = "\n".join(linhas)
def jr(j, cols):
    return " | ".join(v(J[j].get(c, "")) for c in cols)
cols = ["ans_teto_individual_composto_pct", "ipca_plano_saude_pct", "ipca_geral_pct", "coletivos_MED_TODOS_media_pond_composto_pct", "coletivos_MED_AGRUP_media_pond_composto_pct", "coletivos_MED_NAO_AGRUP_media_pond_composto_pct", "coletivos_MED_EMP_TODOS_media_pond_composto_pct", "coletivos_MED_ADE_TODOS_media_pond_composto_pct", "coletivos_PDA055_media_pond_composto_pct", "coletivos_MED_TODOS_media_pond_SEM_ZEROS_composto_pct", "coletivos_MED_AGRUP_media_pond_SEM_ZEROS_composto_pct"]
jan = "\n".join(f"| {j} | {jr(j, cols)} |" for j in ["dez/1999-dez/2024", "dez/2001-dez/2024", "dez/2004-dez/2024", "dez/2012-dez/2024", "dez/2014-dez/2024", "dez/2018-dez/2022"])
am = list(csv.DictReader(open(BASE/"derivado/amil_comparacoes_rotulo.csv")))
am_l = []
for r in am:
    if r["faixa_etaria"] in ("0 a 18", "44 a 48", "59+"):
        am_l.append(f"| {r['data_a']} -> {r['data_b']} | {r['rotulo_a']} -> {r['rotulo_b']} | {r['faixa_etaria']} | {r['mensalidade_a_rs']} -> {r['mensalidade_b_rs']} | {r['variacao_pct']} |")
am_t = "\n".join(am_l)
man = [json.loads(l) for l in open(BASE/"manifest.jsonl")]
sha = {pathlib.Path(m["arquivo"]).name: m["sha256"] for m in man}
mt = open(BASE/"RESULTADO.template.md", encoding="utf8").read()
out = mt.replace("{{TAB_ANO}}", tab_ano).replace("{{JANELAS}}", jan).replace("{{AMIL}}", am_t)
for k in ("Metodos_de_Calculo_6ed.pdf", "snipc_nota_tecnica_2020_03.pdf", "snipc_nota_tecnica_2020_05.pdf", "tabela_reajustes_individuais_2026.xlsx", "pagina-reajuste-coletivos.html", "pagina-metodologia-calculo-individuais.html", "dicionario-pda-043-rpc.ods", "cqcs-ans-divulga-painel-rpc-2021-07-27.html", "pagina-reajuste-individuais-familiares.html", "pda-055-Percentuais_de_Reajuste_de_Agrupamento.csv", "pda-008-caracteristicas_produtos_saude_suplementar.csv", "pagina-painel-reajuste-planos-coletivos.html", "pagina-manual-rpc.html", "Manual_RPC_3.1.7.pdf", "2013_08_27_srm_calculo_7ed.zip", "cdx-amil.com.br-status200.txt"):
    out = out.replace("{{SHA:" + k + "}}", sha[k])
rj = json.load(open(BASE/"derivado/rpc_histogramas.json"))["arquivos"]
out = out.replace("{{N_MAN}}", str(len(man))).replace("{{N_RPC}}", str(len(rj))).replace("{{N_LINHAS}}", f"{sum(rj.values()):,}".replace(",", ".")).replace("{{N_PDF}}", str(sum(1 for m in man if m["arquivo"].endswith(".pdf") and "/amil-wayback/" in m["arquivo"])))
vf = subprocess.run("cd /Users/ulissesflores/Developer/brazil-governments-factcheck && PYTHONPATH=code python3 -m govfc.chain verify " + str(BASE), shell=True, capture_output=True, text=True)
out = out.replace("{{VERIFY}}", (vf.stdout + vf.stderr).strip() + f"\n(exit {vf.returncode}; manifest com {len(man)} linhas)")
(BASE/"RESULTADO.md").write_text(out, encoding="utf8")
print("ok", len(out))
