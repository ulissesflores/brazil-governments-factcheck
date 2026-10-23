"""Baixa, pela cadeia de hash (so o hash fica no repositorio), as bases anuais 'Despesas e Transferencias Totais da Uniao
(criterio valor pago)' do Tesouro Transparente (CKAN 8675a0a4-31c5-4593-a24d-fb8e17376eca), 2008-2025, para estender as
emendas pagas antes de 2014 pelo identificador RP. Pedido do Ulisses 2026-10-23 ("e tesouro?"). Idempotente."""
import json, os, subprocess, sys, time
from pathlib import Path
PASTA = Path(__file__).resolve().parent.parent
REPO = "/Users/ulissesflores/Developer/brazil-governments-factcheck"
env = dict(os.environ, PYTHONPATH=REPO + "/code")
BASE = "https://www.tesourotransparente.gov.br/ckan/dataset/8675a0a4-31c5-4593-a24d-fb8e17376eca/resource/"
ARQ = {2025: "f40d5431-058d-48b8-9ab6-065fb0fce5b3/download/limite-gastos-lc200dez25.xlsx", 2024: "f0ed603a-a3b2-4ed3-8c22-f62c57e146aa/download/limite-gastos-lc200dez24.xlsx",
       2023: "44c1aa69-a1ef-4efd-8e77-8346f8883c38/download/tetodez23.xlsx", 2022: "96744fdd-91c6-46e0-a1c4-253fae51936c/download/tetodez22.xlsx",
       2021: "a66311e0-fb60-4354-b6d4-5ed3dbe7b297/download/tetodez21.xlsx", 2020: "ea213a0b-26f0-4525-90ec-4e0c3847a48e/download/tetodez20.xlsx",
       2019: "e9ae7557-a334-4353-9b02-3f08641afcf7/download/base-despesas-2019.xlsx", 2018: "5d9c3471-9c13-409f-a84a-556b8acf07c7/download/base-despesas-2018.xlsx",
       2017: "9fdccd4d-cb62-4a89-9f22-988299bfda28/download/base-despesas-2017.xlsx", 2016: "903c1716-d304-4fed-9f1d-322a4e21bbbf/download/base-despesas-2016.xlsx",
       2015: "a6767172-8749-4470-9949-91825e6ab72a/download/base-despesas-2015.xlsx", 2014: "f0abf45a-5cbe-49fc-92c9-44ce3c743f2b/download/base-despesas-2014.xlsx",
       2013: "889ee485-2dc8-492b-8bd2-dff0b0785817/download/base-despesas-2013.xlsx", 2012: "975adef6-f5d8-4335-897e-f8c4a5a5aeaf/download/base-despesas-2012.xlsx",
       2011: "52735d4b-5262-4f2d-9164-fac9de715779/download/base-despesas-2011.xlsx", 2010: "3ee45d85-7dbd-44d9-8e79-382dc8edec7f/download/base-despesas-2010.xlsx",
       2009: "8c524683-dce0-4059-9bbb-d213a551ec39/download/base-despesas-2009.xlsx", 2008: "bb0004d4-0d15-4916-96a3-6fa4b30307d5/download/base-despesas-2008.xlsx"}
feitos = {Path(json.loads(l)["arquivo"]).name for l in (PASTA / "manifest.jsonl").read_text().splitlines() if l.strip()}
for ano, res in sorted(ARQ.items()):
    dest = f"bruto/tesouro-despesas/despesas-transferencias-uniao-{ano}.xlsx"
    if Path(dest).name in feitos:
        continue
    r = subprocess.run([sys.executable, "-m", "govfc.chain", "add", str(PASTA), BASE + res, str(PASTA / dest), "--nota",
                        f"Tesouro Transparente, Despesas e Transferencias Totais da Uniao (criterio valor pago), base anual {ano}, XLSX; so o hash no repositorio"],
                       capture_output=True, text=True, cwd=REPO, env=env)
    print(ano, "OK" if r.returncode == 0 else "FALHA " + (r.stderr or r.stdout)[-200:], flush=True)
    time.sleep(3)
