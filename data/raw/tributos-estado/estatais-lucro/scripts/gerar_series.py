"""Gera series/lucro-liquido-<empresa>.csv a partir dos specs_*.py (lê só bruto/, sem rede).
uso: python3 -I scripts/gerar_series.py [empresa ...]
"""
import sys, csv, os
sys.path.insert(0, '/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/estatais-lucro/scripts')
import estatais_lib as L

MODS = {'banco-do-brasil': 'specs_bb', 'petrobras': 'specs_petrobras', 'eletrobras': 'specs_eletrobras',
        'caixa': 'specs_caixa', 'correios': 'specs_correios'}
COLS = ['indicador', 'fonte', 'definicao_linha', 'ano', 'valor', 'unidade', 'nota', 'vintage']

alvo = sys.argv[1:] or list(MODS)
for emp in alvo:
    mod = __import__(MODS[emp])
    rows = mod.specs()
    rows.sort(key=lambda r: (int(r['ano']), r['vintage'], r['definicao_linha']))
    os.makedirs(L.BASE + '/series', exist_ok=True)
    with open(f'{L.BASE}/series/lucro-liquido-{emp}.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction='ignore', lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    anos = sorted({int(r['ano']) for r in rows})
    print(emp, len(rows), 'linhas;', anos[0], '-', anos[-1], 'anos com dado:', len(anos))
