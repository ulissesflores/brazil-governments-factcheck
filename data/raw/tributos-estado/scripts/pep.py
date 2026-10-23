# PEP: cargos comissionados (DAS, FCPE, CCE, FCE) por ano, por 1.000 servidores ativos e parcela sem cargo efetivo. So le bruto/pep. python3 -I pep.py
import csv, json
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
man = {json.loads(l)["arquivo"]: json.loads(l) for l in (RAIZ / "manifest.jsonl").read_text().splitlines()}
arq = "bruto/pep/pep-dezembro-e-ultimo-mes-transcrito-do-qlik.csv"
vint = "PEP (Ministerio da Gestao), consulta ao Qlik em 2026-10-20; transcricao sha256 %s" % man[arq]["sha256"][:12]
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]
L = [l.split("|") for l in (RAIZ / arq).read_text().strip().split("\n")[1:]]
rows = []
F = "Painel Estatistico de Pessoal (PEP), Ministerio da Gestao e da Inovacao"
for r in L:
    mes, at, vt, tot_all, tot, sc, fam = r
    ano = mes[:4] if mes.endswith("-12") else mes
    note = "dezembro" if mes.endswith("-12") else "ULTIMO MES DISPONIVEL (setembro de 2026), nao e ano fechado"
    at, tot, sc, tot_all = int(at), int(tot), int(sc), int(tot_all)
    rows.append(("pep_servidores_ativos_executivo_civil", F, "Servidores ativos do Poder Executivo Federal civil pela medida 'Quantidade de ativos' do PEP (exclui situacoes EST-41, COLAB, PCCTAE, MAGIS e aposentados/instituidores de pensao); " + note, ano, at, "pessoas", "denominador", vint))
    rows.append(("pep_cargos_das_fcpe_cce_fce_total", F, "Ocupacoes de DAS, FCPE (ate 2022), CCE e FCE (desde 2021-22) + correlatas: soma dos agrupamentos 'DAS, FCPE e correlatas' e 'CCE & FCE' do PEP; " + note, ano, tot, "vinculos", "inclui FCI, FCD, FDI, FPR quando o PEP as agrupa em 'correlatas'; ver quebras.csv sobre a queda de 2020-12 para 2021-01", vint))
    rows.append(("pep_cargos_das_fcpe_cce_fce_por_mil_ativos", "calculo desta pasta sobre PEP", "Ocupacoes de DAS/FCPE/CCE/FCE por 1.000 servidores ativos do Executivo civil; " + note, ano, round(tot / at * 1000, 2), "por 1.000 ativos", "divisao dos dois indicadores acima, mesmo mes", vint))
    rows.append(("pep_cargos_das_fcpe_cce_fce_sem_cargo_efetivo", F, "Parte das ocupacoes acima em que o ocupante nao tem cargo efetivo registrado ('Grupo Cargo' = 'S/cargo'); aproximacao do 'sem vinculo' do pedido; " + note, ano, sc, "vinculos", "o PEP nao rotula este campo como 'sem vinculo'; e a ausencia de cargo efetivo no registro de pessoal", vint))
    rows.append(("pep_cargos_das_fcpe_cce_fce_sem_cargo_efetivo_pct", "calculo desta pasta sobre PEP", "Parcela do total de ocupacoes DAS/FCPE/CCE/FCE sem cargo efetivo registrado; " + note, ano, round(sc / tot * 100, 2), "% do total", "", vint))
    rows.append(("pep_cargos_comissionados_e_funcoes_todos_agrupamentos", F, "Total de cargos e funcoes de confianca de todos os agrupamentos do PEP (inclui FG, funcoes tecnicas, agencias reguladoras, IFE); " + note, ano, tot_all, "vinculos", "grupos nulos suprimidos; o conjunto de agrupamentos muda: ver quebras.csv", vint))
    for f in fam.split(","):
        k, v = f.split(":")
        t, s = v.split("/")
        nome = {"DAS": "DAS", "FPE": "FCPE", "CCX": "CCE", "FEX": "FCE"}.get(k, k)
        rows.append(("pep_funcao_%s_total" % nome.lower(), F, "Ocupacoes da familia %s (prefixo '%s' do campo 'Nivel Funcao'); %s" % (nome, k, note), ano, int(t), "vinculos", "dos quais sem cargo efetivo: %s" % s, vint))
with open(RAIZ / "series/pep-cargos-comissionados.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(COLS); w.writerows(rows)
print(len(rows))
