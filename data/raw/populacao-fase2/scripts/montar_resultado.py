#!/usr/bin/env python3
"""Gera RESULTADO.md: tabelas vem dos CSV (nada digitado); verify roda ao vivo."""
import csv, subprocess, os
P = "/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/populacao-fase2/"
tab = subprocess.run(["python3", "-I", P + "scripts/tabela_anos_chave.py"], capture_output=True, text=True).stdout
ver = subprocess.run("cd /Users/ulissesflores/Developer/brazil-governments-factcheck && PYTHONPATH=code python3 -m govfc.chain verify " + P, shell=True, capture_output=True, text=True)
verify = (ver.stdout + ver.stderr).strip() + f" (codigo de saida {ver.returncode})"
S = {}
for r in csv.DictReader(open(P + "derivado/saldo_e_razao_por_base.csv")):
    S.setdefault((r["fonte"], r["indicador"]), {})[int(r["ano"])] = r["valor"]
YRS = [1964, 1970, 1980, 1990, 1994, 2000, 2010, 2016, 2020, 2021, 2024]
def fm(v): return "-" if v is None else (f"{int(v):,}".replace(",", ".") if "." not in v else v.replace(".", ","))
sal = ["| Base | " + " | ".join(map(str, YRS)) + " |", "|---|" + "---|" * len(YRS)]
for (f, ind), d in S.items():
    if ind == "saldo_nascimentos_menos_obitos":
        sal.append(f"| {f} | " + " | ".join(fm(d.get(a)) for a in YRS) + " |")
raz = ["| Base | " + " | ".join(map(str, YRS)) + " |", "|---|" + "---|" * len(YRS)]
for (f, ind), d in S.items():
    if ind == "razao_obitos_por_nascimento":
        raz.append(f"| {f} | " + " | ".join(fm(d.get(a)) for a in YRS) + " |")
conf = ["| Ano | SIM obitos | IBGE RC obitos ocorridos | IBGE RC obitos registrados | ONU WPP obitos | SINASC nascidos | IBGE RC nascidos ocorridos | IBGE RC nascidos registrados | ONU WPP nascimentos |", "|---|---|---|---|---|---|---|---|---|"]
for r in csv.DictReader(open(P + "derivado/conferencia_mesmo_ano.csv")):
    if int(r["ano"]) in (1990, 2000, 2010, 2016, 2020, 2021, 2022, 2023, 2024):
        g = lambda k: fm(r[k]) if r[k] else "-"
        conf.append(f"| {r['ano']} | {g('sim_obitos_ocorrencia')} | {g('ibge_rc_obitos_ocorridos')} | {g('ibge_rc_obitos_registrados')} | {g('onu_wpp_obitos')} | {g('sinasc_nascidos_ocorrencia')} | {g('ibge_rc_nascidos_ocorridos')} | {g('ibge_rc_nascidos_registrados')} | {g('onu_wpp_nascimentos')} |")
conf2 = ["| Ano | SIM / ONU | RC obitos ocorridos / ONU | RC obitos registrados / ONU | SINASC / ONU | RC nascidos ocorridos / ONU | RC nascidos registrados / ONU |", "|---|---|---|---|---|---|---|"]
for r in csv.DictReader(open(P + "derivado/conferencia_mesmo_ano.csv")):
    if int(r["ano"]) in (1980, 1990, 2000, 2010, 2016, 2020, 2021, 2022, 2023, 2024):
        g = lambda k: r[k].replace(".", ",") if r[k] else "-"
        conf2.append(f"| {r['ano']} | {g('sim/wpp')} | {g('rc_ocorridos/wpp')} | {g('rc_registrados/wpp')} | {g('sinasc/wpp')} | {g('rc_ocorridos/wpp ')} | {g('rc_registrados/wpp ')} |")
T = open(P + "scripts/RESULTADO.template.md", encoding="utf-8").read()
out = T.replace("{{TABELA_CHAVE}}", tab.strip()).replace("{{SALDO}}", "\n".join(sal)).replace("{{RAZAO}}", "\n".join(raz)).replace("{{CONF_ABS}}", "\n".join(conf)).replace("{{CONF_RAZAO}}", "\n".join(conf2)).replace("{{VERIFY}}", verify)
open(P + "RESULTADO.md", "w", encoding="utf-8").write(out)
print(len(out))
