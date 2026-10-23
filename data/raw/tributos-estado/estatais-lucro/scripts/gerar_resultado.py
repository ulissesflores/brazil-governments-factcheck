"""Gera RESULTADO.md a partir de series/*.csv e quebras.csv (sem rede)."""
import csv, collections, re
from decimal import Decimal

BASE = '/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/estatais-lucro'
EMP = [('petrobras', 'Petrobras'), ('banco-do-brasil', 'Banco do Brasil'), ('eletrobras', 'Eletrobras'), ('caixa', 'Caixa Econômica Federal'),
       ('correios', 'Correios (ECT)')]


def rot(emp, r):
    d, u = r['definicao_linha'].lower(), r['unidade'].lower()
    if emp == 'petrobras':
        if 'us gaap' in d and 'us$' in u: return 'consolidado, US GAAP (US$)'
        if 'ifrs' in d: return 'IFRS controladora (uso local)' if d.startswith('controladora') else 'IFRS consolidado (uso local)'
        if d.startswith('controladora'): return 'controladora, BR GAAP (R$)'
        return 'consolidado, BR GAAP (R$)'
    if emp == 'banco-do-brasil':
        if 'banco múltiplo' in d: return 'controladora (banco múltiplo), Demonstrações'
        if 'consolidado' in d and 'demonstração' in d: return 'consolidado, Demonstrações'
        return 'quadro/texto do Relatório Anual'
    if emp == 'eletrobras':
        if 'ifrs' in d: return 'IFRS (consolidado)'
        if 'us gaap' in d: return 'US GAAP em R$ (consolidado)'
        return 'BR GAAP (Lei 6.404/76)'
    if emp == 'caixa':
        if 'ifrs' in d: return 'IFRS (consolidado)'
        if d.startswith('individual'): return 'BR GAAP individual'
        if d.startswith('consolidado'): return 'BR GAAP consolidado'
        return 'BR GAAP (CAIXA, sem coluna consolidada)'
    if emp == 'correios':
        if 'consolidadas' in d: return 'consolidado'
        return 'individual / empresa'
    return 'outra'


SUF = {'R$ mil': 'mil', 'R$ milhões': 'mi', 'R$': 'R$', 'US$ milhões': 'US$ mi'}


def fmt(v):
    d = Decimal(v)
    s = format(abs(d), 'f')
    ip, _, fp = s.partition('.')
    ip = f'{int(ip):,}'.replace(',', '.')
    out = ip + (',' + fp if fp else '')
    return ('-' if d < 0 else '') + out


def tabela(emp):
    rows = list(csv.DictReader(open(f'{BASE}/series/lucro-liquido-{emp}.csv')))
    cols = sorted({rot(emp, r) for r in rows})
    anos = sorted({int(r['ano']) for r in rows})
    head = '| Ano | ' + ' | '.join(cols) + ' |'
    sep = '|---|' + '---|' * len(cols)
    out = [head, sep]
    for a in anos:
        cel = []
        for c in cols:
            vs = [r for r in rows if int(r['ano']) == a and rot(emp, r) == c]
            if not vs: cel.append(''); continue
            g = collections.OrderedDict()
            for r in sorted(vs, key=lambda r: r['vintage']):
                g.setdefault(fmt(r['valor']) + ' ' + SUF.get(r['unidade'], r['unidade']), []).append(r['vintage'].split(' (')[0].split(',')[0][:48])
            if len(g) == 1:
                (v, eds), = g.items(); cel.append(f'{v} [{len(eds)} ed.]')
            else:
                cel.append('; '.join(f'{v} [{len(eds)} ed., 1ª: {eds[0]}]' for v, eds in g.items()))
        out.append(f'| {a} | ' + ' | '.join(cel) + ' |')
    return '\n'.join(out), rows, anos


md = []
md.append('# Lucro líquido anual de cinco estatais federais: coleta nas demonstrações da própria empresa\n')
md.append('Escopo: Petrobras, Banco do Brasil e Eletrobras 1995-2009 (o resto da série está com o solicitante); Caixa e Correios 1995-2025. '
          'Só números, definição e vintage: sem nota, sem ranking. Moeda e unidade do documento, sem deflacionar nem converter. '
          'Células: valor + unidade (mil = R$ mil; mi = R$ milhões; R$ = reais com centavos; US$ mi = US$ milhões). "[n ed.]" = número de edições (documentos) que trazem o valor; quando o mesmo ano tem valores diferentes entre edições, cada valor aparece com a primeira edição que o traz. '
          'Cada linha de `series/*.csv` leva, na coluna `nota`, arquivo, página e linha do bruto; `quebras.csv` cita o trecho.\n')
resumo = []
for emp, nome in EMP:
    t, rows, anos = tabela(emp)
    resumo.append((nome, len(rows), anos))
    md.append(f'## {nome}\n')
    md.append(f'{len(rows)} linhas em `series/lucro-liquido-{emp}.csv`; anos com dado: {anos[0]} a {anos[-1]} ({len(anos)} anos).\n')
    md.append(t + '\n')

md.append('## Quebras registradas\n')
q = list(csv.DictReader(open(f'{BASE}/quebras.csv')))
c = collections.Counter((x['serie'], x['tipo_de_quebra']) for x in q)
md.append(f'{len(q)} linhas em `quebras.csv` (mudança de norma contábil, de unidade, de perímetro e reapresentações de exercícios). Contagem por série e tipo:\n')
md.append('| Série | mudanca_de_regra | revisao_de_vintage | mudanca_de_unidade |')
md.append('|---|---|---|---|')
for s in ['petrobras', 'banco-do-brasil', 'eletrobras', 'caixa', 'correios']:
    md.append(f'| {s} | {c[(s, "mudanca_de_regra")]} | {c[(s, "revisao_de_vintage")]} | {c[(s, "mudanca_de_unidade")]} |')
md.append('')

md.append('## NÃO achado (evidência negativa, ano a ano)\n')
md.append('| Empresa | Anos | O que não foi achado e por quê |')
md.append('|---|---|---|')
nao = [
    ('Petrobras', '1995, 1996', 'sem série. O 20-F mais antigo no EDGAR em texto é o do exercício 2001 (arquivado em 2002-07-01) e traz 1997-2001; o 20-F do exercício 2000 não está na lista de filings (só 6-K em papel em 2001-2002). A Wayback Machine do site de RI (www2.petrobras.com.br/ri) lista relatórios e demonstrações só a partir de 1999.'),
    ('Petrobras', '1997', 'só em US$ (US GAAP, US$ 1.419 milhões, 20-F do exercício 2001); lucro em R$ de 1997 não achado.'),
    ('Petrobras', '1998, 2000', 'em R$ só como coluna comparativa (1998 na edição 1999; 2000 na edição 2001); a edição original de cada um desses exercícios não foi achada.'),
    ('Petrobras', '2004', 'o PDF "Petrobras_DF_2004" da Wayback tem camada de texto corrompida (dígitos perdidos), não foi lido; o valor de 2004 vem dos comparativos da DF 2005 e da DFP 2006.'),
    ('Banco do Brasil', '1995, 1996', 'só no quadro de cinco anos do Relatório Anual 1999 (comparativo). O Relatório Anual 1997 tem 26,2 MB (acima do teto de 25 MB, não baixado) e o 1998 não traz série com lucro desses anos; Relatório Anual 2008 (30,1 MB) também não baixado.'),
    ('Banco do Brasil', '1997', 'o Relatório Anual 1997 não foi baixado (teto de tamanho); 1997 vem das edições 1999 (573) e 2000 (574).'),
    ('Eletrobras', '1995-1999', 'sem série. O Relatório da Administração 2004 recua só até 2000; a Wayback do domínio eletrobras.gov.br (119 PDFs listados) não tem demonstração anterior a 2001; as páginas relatorio_anual_2000/2001.asp apontam para PDFs que a Wayback não guardou (404).'),
    ('Eletrobras', '2000', 'só como comparativo da edição 2004 do Relatório da Administração; a edição original (relatorio_anual_2000_port.pdf) não foi guardada pela Wayback.'),
    ('Eletrobras', '2003, 2004 (US GAAP)', 'o Form 20-F de registro (2008) declara que não incluiu 2003 e 2004 porque os dados "cannot be provided on a restated basis without unreasonable effort and expense"; só há 2003-2004 em BR GAAP.'),
    ('Eletrobras', '20-F/A de 2011-12-02, 2012-01-31 e 2012-04-25', 'baixados e não usados: as cifras de lucro (R$ 812.171 mil / 861.975 mil; R$ 278.621 mil / 219.631 mil; prejuízo de R$ 194.734 mil / lucro de R$ 1.598.785 mil) não correspondem à Eletrobras consolidada; a entidade de cada um não foi identificada.'),
    ('Caixa', '1995-2000', 'sem série. O site da CAIXA publica demonstrações a partir de 2002 (páginas "demonstrativos-de-AAAA" respondem 404 para 1999-2001); 2001 só aparece como comparativo da edição 2002 (prejuízo de R$ 4.687.332 mil).'),
    ('Caixa', '2007 (demonstração original)', 'o arquivo CEF_Portugues_122007.zip não baixou (a URL devolve HTML de erro); o valor original (R$ 2.510.098 mil) vem da Nota 2 das demonstrações de 2008 e, em R$ 2.510 milhões, do Relatório da Administração 4T07 (lido por OCR).'),
    ('Caixa', '2016 (URL antiga)', 'DC_BrGaap_2016.pdf devolve 404; a edição de 2016 usada é a do site de RI (4T16, "editável").'),
    ('Caixa', '2025 (DRE)', 'a página da DRE do PDF não tem camada de texto; o lucro de 2025 vem da Demonstração do Resultado Abrangente (sem comparativo de 2024 nessa página).'),
    ('Caixa', 'IFRS antes de 2012', 'não achado: o catálogo do RI da CAIXA traz IFRS consolidado a partir de 2012.'),
    ('Correios', '1995-1999', 'sem série. O site publica demonstrações de 2001 em diante; 2000 só como comparativo da edição 2001 (R$ 192.201.615,95).'),
    ('Correios', '2009', 'a DRE desta edição não saiu em texto; o lucro (R$ 117,55 milhões) vem da Demonstração dos Fluxos de Caixa, e R$ 117.546.308,83 da DMPL da edição 2010 (leitura visual).'),
]
for e, a, t in nao:
    md.append(f'| {e} | {a} | {t} |')
md.append('')
md.append('2022-2025 (que o SEST ainda não deu): Caixa e Correios estão cobertos pelas demonstrações das próprias empresas (Caixa: BR GAAP e IFRS 2022-2025; Correios: 2022-2025, com as reapresentações de 2022, 2023 e 2024 em `quebras.csv`). Não achado para 2025 nas duas: reapresentação posterior (a edição 1T2026 dos Correios diz que as demonstrações de 2025 foram reapresentadas; o lucro anual reapresentado de 2025 não está nesse documento trimestral).\n')

md.append('## Avisos de integridade\n')
for t in [
    'PDFs-imagem lidos por OCR (`scripts/ocr.sh`, tesseract por) ou por leitura visual: Correios 2001, 2004, 2010 a 2013, 2015 a 2017 e Caixa Relatório da Administração 4T07. A nota da linha diz "texto OCR" ou "leitura visual". Valores do OCR foram conferidos contra a edição seguinte; o OCR de 2004 errou um dígito (316.920.926,29) e foi corrigido pela imagem (316.928.926,29).',
    'Os 5 arquivos `bruto/caixa-brgaap-BrGaap-Demonstracoes-Contabeis*.pdf` e `bruto/caixa-brgaap-DC-BrGaap-2017.pdf` são duplicatas de nome colidido (baixados antes de o nome incluir ano e trimestre; a cadeia os marca "superseded"); `bruto/caixa-df-2007-portugues-zip.html`, `bruto/caixa-dc-brgaap-2016.html` e `bruto/eletrobras-wb-invest-relatorio_anual-asp.bin` são páginas de erro registradas na cadeia. Não são fonte de nenhuma linha.',
    '`bruto/sec-submissions-petrobras-002.json` foi registrado duas vezes (a primeira com a URL do arquivo principal por engano; a segunda com a URL correta).',
    '`bruto/correios-df-2017.pdf` tem 25.012.564 bytes (23,9 MiB; 25,01 MB decimais): baixado por estar abaixo de 25 MiB; está na margem do teto e é o único nessa situação.',
    'Os PDFs `bruto/caixa-dre-2006.pdf` e `bruto/caixa-dre-2007.pdf` são demonstrações trimestrais (1º trimestre) e não alimentam a série.',
    'Documentos da Wayback Machine (Petrobras, Eletrobras): a URL registrada é o endereço `web.archive.org/web/20100101000000id_/<original>`, que a Wayback resolve para a captura mais próxima.',
    'Petrobras US GAAP (20-F): o 20-F do exercício 2009 em diante rotula o lucro como "attributable to Petrobras"; nos anos repetidos os valores são idênticos aos das edições anteriores.',
    'Lucro de BB, Petrobras, Eletrobras, Caixa e Correios em R$ não é comparável entre empresas nem ao longo dos anos sem as definições da coluna `definicao_linha` e as linhas de `quebras.csv`.',
]:
    md.append(f'- {t}')
md.append('')
md.append('## Como reproduzir\n')
md.append('```bash\n'
          '# rede (registra na cadeia de hash): scripts/baixar.sh, scripts/mz_catalogo.sh, scripts/mz_lista.py\n'
          'scripts/ocr.sh bruto/<pdf-imagem>.pdf scripts/_txt/<pdf-imagem>.ocr.txt   # OCR, sem rede\n'
          'python3 -I scripts/gerar_series.py      # series/*.csv\n'
          'python3 -I scripts/gerar_quebras.py     # quebras.csv\n'
          'python3 -I scripts/gerar_resultado.py   # este arquivo\n'
          'python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py verify \\\n'
          '  /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/estatais-lucro\n'
          '```\n')
open(BASE + '/RESULTADO.md', 'w', encoding='utf-8').write('\n'.join(md))
print('ok', [(n, k, a[0], a[-1]) for n, k, a in resumo])
