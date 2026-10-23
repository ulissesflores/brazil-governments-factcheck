"""Caixa Econômica Federal: lucro líquido anual, R$ mil (BR GAAP e, a partir de 2016, também IFRS)."""
import re
from estatais_lib import extrai


def fz(txt):
    """regex tolerante a espaços inseridos no meio das palavras (texto 'raw' de PDF) e a acento perdido."""
    m = {'Í': '[IÍ]', 'Á': '[AÁ]', 'Ã': '[AÃ]', 'Ç': '[CÇ]', 'Ó': '[OÓ]', 'É': '[EÉ]'}
    return r'\s*'.join(m.get(c, re.escape(c)) for c in txt if c != ' ')

E = 'caixa'
IND = ('individual (CAIXA), BR GAAP (Lei 6.404/76 e normas do Banco Central/CMN), Demonstração do Resultado, '
       'exercício anual, R$ mil')
IND_SEM_CONS = ('demonstrações da CAIXA (a fonte não traz coluna consolidada), BR GAAP (Lei 6.404/76 e normas do Banco '
                'Central/CMN), Demonstração do Resultado, exercício anual, R$ mil')
CONS = ('consolidado (CAIXA e controladas), BR GAAP (Lei 6.404/76 e normas do Banco Central/CMN), Demonstração do '
        'Resultado, exercício anual, R$ mil')
CONS_ATR = ('consolidado BR GAAP, linha "Lucro líquido atribuível ao controlador" (exclui participação de não controladores), '
            'exercício anual, R$ mil')
CONS_TOT = ('consolidado BR GAAP, linha "Lucro líquido total" (inclui participação de não controladores), '
            'exercício anual, R$ mil')
IFRS_ATR = 'consolidado, IFRS, lucro líquido atribuível ao controlador, exercício anual, R$ mil'
IFRS_TOT = 'consolidado, IFRS, lucro líquido total (inclui não controladores) / "do exercício" quando a fonte não separa, exercício anual, R$ mil'


def specs():
    S = []
    U = 'R$ mil'
    # --- Demonstrações anuais 2002-2008 (3 colunas [2º semestre N, N, N-1])
    pre = [
        ('caixa-df-2002-portugues.pdf', 2002, r'^\s*Lucro/preju[ií]zo l[ií]quido(?=\s+[\d(])'),
        ('caixa-df-2003-portugues.pdf', 2003, r'^\s*Lucro l[ií]quido(?=\s+\d)'),
        ('caixa-df-2004-portugues.pdf', 2004, r'^\s*Lucro l[ií]quido do semestre/exerc[ií]cio(?=\s+\d)'),
        ('caixa-df-2005-portugues.pdf', 2005, r'^\s*Lucro l[ií]quido do semestre/exerc[ií]cio(?=\s+\d)'),
        ('caixa-df-2006-portugues.pdf', 2006, r'^\s*Lucro l[ií]quido do semestre/\s*exerc[ií]cio(?=\s+\d)'),
        ('caixa-df-2008-portugues.pdf', 2008, r'^\s*LUCRO L[IÍ]QUIDO DO SEMESTRE/EXERC[IÍ]CIO\.*'),
    ]
    for arq, n, anc in pre:
        S += extrai(E, arq, 'layout', anc, [(1, n), (2, n - 1)], IND_SEM_CONS, U, f'Caixa Econômica Federal, Demonstrações Contábeis {n}',
                    f'Demonstrações Contábeis {n} (publicadas em {n + 1})', minnums=3,
                    obs='colunas: [2º semestre N, exercício N, exercício N-1]')
    # 2009 e 2010: quadro com 5 colunas [4T, 3T, 2S, exercício N, exercício N-1]
    S += extrai(E, 'caixa-dre-2009.pdf', 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO TRIMESTRE/EXERC[IÍ]CIO', [(3, 2009), (4, 2008)],
                IND_SEM_CONS, U, 'Caixa Econômica Federal, Demonstração do Resultado dez/2009', 'Demonstração do Resultado dez/2009 (publicada em 2010)',
                minnums=5, obs='colunas: [4º trim. 2009, 3º trim. 2009, 2º semestre 2009, exercício 2009, exercício 2008]')
    S += extrai(E, 'caixa-dre-2010.pdf', 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO PER[IÍ]ODO', [(3, 2010, CONS), (4, 2009, CONS + '; 2009 reapresentado nesta edição')],
                CONS, U, 'Caixa Econômica Federal, Demonstração do Resultado - Consolidado dez/2010',
                'Demonstração do Resultado - Consolidado dez/2010 (publicada em 2011)', minnums=5,
                obs='colunas: [4º trim. 2010, 3º trim. 2010, 2º semestre 2010, exercício 2010, exercício 2009]')
    # --- DCs BR GAAP com 6 colunas (individual [2S N, N, N-1] e consolidado idem): 2011, 2012
    for arq, n in [('caixa-dc-brgaap-2011.pdf', 2011), ('caixa-dc-brgaap-2012.pdf', 2012)]:
        anc = r'^\s*LUCRO L[IÍ]QUIDO(?: DO PER[IÍ]ODO)?(?=\s+\d)'
        S += extrai(E, arq, 'layout', anc, [(1, n, IND), (2, n - 1, IND), (4, n, CONS), (5, n - 1, CONS)], IND, U,
                    f'Caixa Econômica Federal, Demonstrações Contábeis BR GAAP dez/{n}', f'Demonstrações Contábeis BR GAAP dez/{n} (publicadas em {n + 1})',
                    minnums=6, obs='colunas: [indiv. 2S N, indiv. N, indiv. N-1, cons. 2S N, cons. N, cons. N-1]')
    # --- 8 colunas [ind 2S N, ind N, ind 2S N-1, ind N-1, cons 2S N, cons N, cons 2S N-1, cons N-1]
    oito = [('caixa-dc-brgaap-2013.pdf', 2013, 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO PER[IÍ]ODO(?=\s+\d)'),
            ('caixa-dc-brgaap-2014.pdf', 2014, 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO PER[IÍ]ODO(?=\s+\d)'),
            ('caixa-brgaap-2016T4-BrGaap-Demonstracoes-Contabeis-4T16-editavel.pdf', 2016, 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO SEMESTRE / EXERC[IÍ]CIO(?=\s+\d)'),
            ('caixa-brgaap-2017T4-DC-BrGaap-2017.pdf', 2017, 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO PER[IÍ]ODO(?=\s+\d)'),
            ('caixa-brgaap-2018T4-BrGaap-Demonstracoes-Contabeis-editavel.pdf', 2018, 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO PER[IÍ]ODO(?=\s+\d)'),
            ('caixa-brgaap-2019T4-BrGaap-Demonstracoes-Contabeis.pdf', 2019, 'layout', r'^\s*LUCRO\s+L[IÍ]QUIDO\s+DO\s+P\s*E\s*R\s*.\s*ODO(?=\s+\d)'),
            ('caixa-brgaap-2020T4-BrGaap-Demonstracoes-Contabeis-4T20.pdf', 2020, 'layout', r'^\s*LUCRO L[IÍ]QUIDO(?=\s+\d)')]
    for arq, n, modo, anc in oito:
        S += extrai(E, arq, modo, anc, [(1, n, IND), (3, n - 1, IND + '; ano anterior como reapresentado nesta edição'),
                                        (5, n, CONS), (7, n - 1, CONS + '; ano anterior como reapresentado nesta edição')], IND, U,
                    f'Caixa Econômica Federal, Demonstrações Contábeis BR GAAP dez/{n}', f'Demonstrações Contábeis BR GAAP dez/{n} (publicadas em {n + 1})',
                    minnums=8, obs='colunas: [indiv. 2S N, indiv. N, indiv. 2S N-1, indiv. N-1, cons. 2S N, cons. N, cons. 2S N-1, cons. N-1]')
    # 2015: DRE só consolidada, 4 colunas [2S N, N, 2S N-1, N-1]
    S += extrai(E, 'caixa-dc-brgaap-2015.pdf', 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO SEMESTRE / EXERC[IÍ]CIO(?=\s+\d)',
                [(1, 2015, CONS), (3, 2014, CONS + '; 2014 com a marca "Nota 3 (t)" (reapresentação) no cabeçalho')], CONS, U,
                'Caixa Econômica Federal, Demonstrações Contábeis BR GAAP dez/2015', 'Demonstrações Contábeis BR GAAP dez/2015 (publicadas em 2016)',
                minnums=4, obs='a DRE desta edição é consolidada (receitas da intermediação 144.471.785 = coluna consolidada de 2016)')
    # 2021-2024: texto em modo "raw" (o layout vem embaralhado); 6 colunas [ind 2S N, ind N, ind N-1, cons 2S N, cons N, cons N-1]
    for arq, n in [('caixa-brgaap-2021T4-BrGaap-Demonstracoes-Contabeis.pdf', 2021), ('caixa-brgaap-2022T4-BrGaap-Demonstracoes-Contabeis.pdf', 2022),
                   ('caixa-brgaap-2023T4-BrGaap-Demonstracoes-Contabeis.pdf', 2023), ('caixa-brgaap-2024T4-BrGaap-Demonstracoes-Contabeis.pdf', 2024)]:
        ft = f'Caixa Econômica Federal, Demonstrações Contábeis BR GAAP dez/{n}'
        vt = f'Demonstrações Contábeis BR GAAP dez/{n} (publicadas em {n + 1})'
        ob = 'texto extraído em modo raw (o layout do PDF vem embaralhado); colunas: [indiv. 2S N, indiv. N, indiv. N-1, cons. 2S N, cons. N, cons. N-1]'
        S += extrai(E, arq, 'raw', '^' + fz('LUCRO LÍQUIDO DO PERÍODO') + r'(?=\s+\d)', [(1, n, IND), (2, n - 1, IND)], IND, U, ft, vt, minnums=6, obs=ob)
        S += extrai(E, arq, 'raw', '^' + fz('LUCRO LÍQUIDO ATRIBUÍVEL AO CONTROLADOR') + r'(?=\s+\d)', [(4, n, CONS_ATR), (5, n - 1, CONS_ATR)], CONS_ATR, U, ft, vt, minnums=6, obs=ob)
        S += extrai(E, arq, 'raw', '^' + fz('LUCRO LÍQUIDO TOTAL') + r'(?=\s+\d)', [(4, n, CONS_TOT), (5, n - 1, CONS_TOT)], CONS_TOT, U, ft, vt, minnums=6, obs=ob)
    # 2025: a DRE não tem camada de texto; usa-se a Demonstração do Resultado Abrangente (2º semestre, exercício)
    arq = 'caixa-brgaap-2025T4-BrGaap-Demonstracoes-Contabeis.pdf'
    ft = 'Caixa Econômica Federal, Demonstrações Contábeis BR GAAP dez/2025'
    vt = 'Demonstrações Contábeis BR GAAP dez/2025 (publicadas em 2026)'
    ob = 'linha da Demonstração do Resultado Abrangente (a DRE desta edição não tem camada de texto); colunas: [indiv. 2S, indiv. exercício, cons. 2S, cons. exercício]'
    S += extrai(E, arq, 'raw', r'^Lucro l[ií]quido atribu[ií]vel ao controlador(?=\s+\d)', [(1, 2025, IND), (3, 2025, CONS_ATR)], IND, U, ft, vt, minnums=4, obs=ob)
    S += extrai(E, arq, 'raw', r'^Lucro l[ií]quido total(?=\s+\d)', [(3, 2025, CONS_TOT)], CONS_TOT, U, ft, vt, minnums=4, obs=ob)

    # --- 2007: valor original (RdA 4T07, OCR) e reapresentação na Nota 2 das demonstrações de 2008
    S += extrai(E, 'caixa-rda-2007-4T07.pdf', 'ocr', r'O lucro l.quido no exerc.cio de 2007 foi de R\$', [(0, 2007)],
                'texto do Relatório da Administração: lucro líquido do exercício de 2007 da CAIXA (valor original, antes da reapresentação de 2008), R$ milhões',
                'R$ milhões', 'Caixa Econômica Federal, Relatório da Administração 4T07', 'Relatório da Administração dez/2007 (publicado em 2008)')
    S += extrai(E, 'caixa-df-2008-portugues.pdf', 'layout', r'Lucro l[ií]quido do exerc[ií]cio(?=\s+2\.510\.098)',
                [(0, 2007, IND_SEM_CONS.replace('exercício anual', 'exercício 2007, coluna "Original" da Nota 2 (valor publicado antes do ajuste)')),
                 (2, 2007, IND_SEM_CONS.replace('exercício anual', 'exercício 2007, coluna "Ajustado" da Nota 2 (depois do ajuste de R$ 117.644 mil)'))],
                IND_SEM_CONS, 'R$ mil', 'Caixa Econômica Federal, Demonstrações Contábeis 2008, Nota 2',
                'Demonstrações Contábeis 2008 (publicadas em 2009)', minnums=3,
                obs='colunas: [Original, Ajustes, Ajustado]; ajuste (i) = despesas correntes de 2007 das obrigações da patrocinadora com o Plano Saúde CAIXA')
    # --- IFRS consolidado (2016-2025)
    for arq, n in [('caixa-ifrs-2012T4-IFRS-Demonstracoes-contabeis-consolidadas.pdf', 2012), ('caixa-ifrs-2013T4-IFRS-Demonstracoes-Contabeis-Consolidadas.pdf', 2013),
                   ('caixa-ifrs-2014T4-IFRS-Demonstracoes-Contabeis-Consolidadas.pdf', 2014), ('caixa-ifrs-2015T4-IFRS-Demonstracoes-Contabeis-Consolidadas.pdf', 2015)]:
        S += extrai(E, arq, 'layout', r'^\s*LUCRO L.QUIDO DO EXERC.CIO(?=\s+[\d(])', [(0, n, IFRS_TOT), (1, n - 1, IFRS_TOT)], IFRS_TOT, U,
                    f'Caixa Econômica Federal, Demonstrações Contábeis Consolidadas IFRS dez/{n}', f'IFRS dez/{n} (publicadas em {n + 1})', minnums=2)
    ifrs = [('caixa-ifrs-2016T4-IFRS-Demonstracoes-Contabeis-Consolidadas.pdf', 2016, r'^LUCRO L.QUIDO DO EXERC.CIO(?=\s+[\d(])', [(0, 2016, IFRS_TOT), (1, 2015, IFRS_TOT)]),
            ('caixa-ifrs-2017T4-IFRS-Demonstracoes-Contabeis-2017.pdf', 2017, r'^LUCRO L.QUIDO DO EXERC.CIO(?=\s+[\d(])', [(0, 2017, IFRS_TOT), (1, 2016, IFRS_TOT)]),
            ('caixa-ifrs-2018T4-IFRS-Demonstracoes-Contabeis-2018.pdf', 2018, r'^LUCRO L.QUIDO DO EXERC.CIO(?=\s+[\d(])', [(0, 2018, IFRS_TOT), (1, 2017, IFRS_TOT + '; 2017 na coluna "IFRS 9" (recalculado com a nova norma, Nota 2(u))'), (2, 2017, IFRS_TOT + '; 2017 na coluna "IAS 39" (critério anterior, reapresentado)')]),
            ('caixa-ifrs-2019T4-IFRS-Demonstracoes-Contabeis-2019.pdf', 2019, r'^LUCRO L.QUIDO DO EXERC.CIO(?=\s+[\d(])', [(0, 2019, IFRS_TOT), (1, 2018, IFRS_TOT)]),
            ('caixa-ifrs-2020T4-IFRS-Demonstracoes-Contabeis-Consolidadas.pdf', 2020, r'^LUCRO L.QUIDO DO PER.ODO(?=\s+[\d(])', [(0, 2020, IFRS_TOT), (1, 2019, IFRS_TOT)]),
            ('caixa-ifrs-2021T4-IFRS-Demonstracoes-Contabeis-Consolidadas.pdf', 2021, r'^LUCRO L.QUIDO DO PER.ODO(?=\s+[\d(])', [(0, 2021, IFRS_TOT)])]
    for arq, n, anc, cols in ifrs:
        S += extrai(E, arq, 'raw', anc, cols, IFRS_TOT, U, f'Caixa Econômica Federal, Demonstrações Contábeis Consolidadas IFRS dez/{n}',
                    f'IFRS dez/{n} (publicadas em {n + 1})', minnums=len(cols), obs='texto extraído em modo raw')
    for arq, n in [('caixa-ifrs-2022T4-IFRS-Demonstracoes-Contabeis-Consolidadas.pdf', 2022), ('caixa-ifrs-2023T4-IFRS-Demonstracoes-contabeis-consolidadas-4T23.pdf', 2023),
                   ('caixa-ifrs-2024T4-IFRS-Demonstracoes-contabeis-consolidadas-4T24.pdf', 2024), ('caixa-ifrs-2025T4-IFRS-Demonstracoes-contabeis-consolidadas-4T25.pdf', 2025)]:
        ft = f'Caixa Econômica Federal, Demonstrações Contábeis Consolidadas IFRS dez/{n}'
        vt = f'IFRS dez/{n} (publicadas em {n + 1})'
        S += extrai(E, arq, 'raw', r'^LUCRO L[IÍ]QUIDO ATRIBU[IÍ]VEL AO CONTROLADOR(?=\s+[\d(])', [(0, n, IFRS_ATR), (1, n - 1, IFRS_ATR)], IFRS_ATR, U, ft, vt, minnums=2, obs='texto extraído em modo raw')
        S += extrai(E, arq, 'raw', r'^LUCRO L[IÍ]QUIDO TOTAL(?=\s+[\d(])', [(0, n, IFRS_TOT), (1, n - 1, IFRS_TOT)], IFRS_TOT, U, ft, vt, minnums=2, obs='texto extraído em modo raw')
    return S
