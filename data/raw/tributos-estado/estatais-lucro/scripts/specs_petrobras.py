"""Petrobras: lucro líquido anual. (a) US GAAP em US$ milhões (20-F, SEC); (b) BR GAAP/Lei 6.404 em R$ (DFs e relatórios)."""
from estatais_lib import extrai

E = 'petrobras'
USD_DEF = ('consolidado, US GAAP (norma do 20-F), US$ milhões, "Net income for the year" (lucro líquido do exercício '
           'depois da participação de minoritários); valores em dólar convertidos do real pelo critério SFAS 52')
USD_DEF_ATTR = ('consolidado, US GAAP, US$ milhões, "Net income for the year attributable to Petrobras" (atribuível à '
                'Petrobras, exclui participação de não controladores)')
RS_CONS = ('consolidado, BR GAAP (Lei 6.404/76 e normas da CVM), lucro líquido do exercício depois da dedução da '
           'participação de minoritários, R$ mil')
RS_CTRL = 'controladora (Petróleo Brasileiro S.A. individual), BR GAAP (Lei 6.404/76 e normas da CVM), R$ mil'


def specs():
    S = []
    # ---- (a) 20-F, US$ milhões, US GAAP; cada edição traz 5 anos [N, N-1, ..., N-4]; só anos <= 2009
    ed = [
        ('petrobras-20f-fy2001-d20f.txt', 'txt', 2001, r'^Net income(?= \.{3,})', USD_DEF, '20-F do exercício 2001 (arquivado na SEC em 2002-07-01)'),
        ('petrobras-20f-fy2002-y87469e20vf.htm', 'html', 2002, r'^Net income(?= \|)', USD_DEF, '20-F do exercício 2002 (SEC, 2003-06-19)'),
        ('petrobras-20f-fy2003-d20f.htm', 'html', 2003, r'^Net income for the year(?= \|)', USD_DEF, '20-F do exercício 2003 (SEC, 2004-06-30)'),
        ('petrobras-20f-fy2004-d20f.htm', 'html', 2004, r'^Net income for the year(?= \|)', USD_DEF, '20-F do exercício 2004 (SEC, 2005-06-30)'),
        ('petrobras-20f-fy2005-y22597e20vf.htm', 'html', 2005, r'^Net income for the year(?= \|)', USD_DEF, '20-F do exercício 2005 (SEC, 2006-06-28)'),
        ('petrobras-20f-fy2006-y36368e20vf.htm', 'html', 2006, r'^Net income for the year(?= \|)', USD_DEF, '20-F do exercício 2006 (SEC, 2007-06-26)'),
        ('petrobras-20f-fy2007-c73239e20vf.htm', 'html', 2007, r'^Net income for the year(?:\s*\(\d\))?(?= \|)', USD_DEF, '20-F do exercício 2007 (SEC, 2008-05-19)'),
        ('petrobras-20f-fy2008-y76586e20vf.htm', 'html', 2008, r'^Net income for the year(?:\s*\(\d\))?(?= \|)', USD_DEF, '20-F do exercício 2008 (SEC, 2009-05-22)'),
        ('petrobras-20f-fy2009-pbraform20f2009.htm', 'html', 2009, r'^Net income for the year attributable to Petrobras(?:\s*\(\d\))?(?= \|)', USD_DEF_ATTR, '20-F do exercício 2009 (SEC, 2010-05-20)'),
        ('petrobras-20f-fy2010-pbraform20f2010.htm', 'html', 2010, r'^Net income for the year attributable to Petrobras(?:\s*\(\d\))?(?= \|)', USD_DEF_ATTR, '20-F do exercício 2010 (SEC, 2011-05-26)'),
    ]
    for arq, modo, n, anc, dfn, vint in ed:
        cols = [(i, n - i) for i in range(5) if 1997 <= n - i <= 2009]
        S += extrai(E, arq, modo, anc, cols, dfn, 'US$ milhões', 'Petrobras, Form 20-F (SEC), "Selected Financial Data"',
                    vint, fmt='us', minnums=5)

    # ---- (b) BR GAAP em R$
    # Financial Analysis 1999 (inglês): R$ milhões
    S += extrai(E, 'petrobras-wb-financial-analysis-99.pdf', 'layout', r'^\s*Net income\s+R\$ millions',
                [(0, 1999), (1, 1998)],
                'consolidado, BR GAAP (Lei 6.404/76) com as mudanças de prática contábil aprovadas em 15/10/1999 aplicadas '
                'retroativamente a 01/01/1999 (1998 não reapresentado); R$ milhões; lucro líquido consolidado depois da '
                'eliminação intercompanhias e da participação de minoritários',
                'R$ milhões', 'Petrobras, Financial Analysis and Consolidated Financial Statements 1999 (Wayback Machine)',
                'Demonstrações de 1999 (publicadas em 2000)', minnums=2)
    # DF 2001 (aparece 2001 e 2000): consolidado [2001, 2000], controladora [2001, 2000]
    for arq, vint, ft, n in [
        ('petrobras-wb-dc-brgaap-port.pdf', 'Demonstrações Contábeis 2001 (parecer de 4/2/2002)', 'Petrobras, Demonstrações Contábeis 2001 (Wayback Machine)', 2001),
        ('petrobras-wb-rademostraport.pdf', 'Demonstrações Contábeis 2002 (Relatório Anual 2002)', 'Petrobras, Relatório Anual 2002 - Demonstrações (Wayback Machine)', 2002),
        ('petrobras-wb-analise-dc-2003.pdf', 'Análise Financeira e Demonstrações Contábeis 2003', 'Petrobras, Análise Financeira e Demonstrações Contábeis 2003 (Wayback Machine)', 2003),
    ]:
        anc = r'^\s*Lucro l[ií]quido do exerc[ií]cio(?=\s+[\d(])'
        ap = None
        cols = [(0, n, RS_CONS), (1, n - 1, RS_CONS), (2, n, RS_CTRL), (3, n - 1, RS_CTRL)]
        S += extrai(E, arq, 'layout', anc, cols, RS_CONS, 'R$ mil', ft, vint, minnums=4, apos=ap)
    S += extrai(E, 'petrobras-wb-df-2005.pdf', 'layout', r'^\s*Lucro l[ií]quido do exerc[ií]cio(?=\s+[\d(])',
                [(0, 2005, RS_CONS), (1, 2004, RS_CONS), (2, 2005, RS_CTRL), (3, 2004, RS_CTRL)], RS_CONS, 'R$ mil',
                'Petrobras, Demonstrações Financeiras 2005 (Wayback Machine)', 'Demonstrações Financeiras 2005', minnums=4)
    # atas das Assembleias Gerais Ordinárias (Wayback Machine): valor em reais com centavos, controladora
    ata_def = ('controladora (Petróleo Brasileiro S.A. individual), BR GAAP (Lei 6.404/76), "%s" na proposta de destinação aprovada em AGO; '
               'valor em reais com centavos')
    S += extrai(E, 'petrobras-wb-ata-ago-2000.pdf', 'layout', r'exerc.cio de 1999, no montante de R\$', [(0, 1999)], ata_def % 'resultado do exercício',
                'R$', 'Petrobras, Ata da AGO de 2000 (Wayback Machine)', 'Ata da AGO de 2000 (exercício 1999)', junta=1)
    S += extrai(E, 'petrobras-wb-ata-ago-2001.pdf', 'layout', r'exerc.cio de 2000, no montante de R\$', [(0, 2000)], ata_def % 'resultado do exercício',
                'R$', 'Petrobras, Ata da AGO de 2001 (Wayback Machine)', 'Ata da AGO de 2001 (exercício 2000)', junta=1)
    S += extrai(E, 'petrobras-wb-ata-ago-2002.pdf', 'layout', r'destina..o do lucro l.quido do exerc.cio de 2001, no montante de R\$', [(0, 2001)],
                ata_def % 'lucro líquido do exercício', 'R$', 'Petrobras, Ata da AGO de 2002 (Wayback Machine)', 'Ata da AGO de 2002 (exercício 2001)', junta=1)
    # DFP (CVM) 2006-2009 via site de RI: 3 colunas [N, N-1, N-2]
    dfp = [('petrobras-dfp-2006-brgaap.pdf', 2006), ('petrobras-dfp-2007-brgaap.pdf', 2007),
           ('petrobras-dfp-2008-brgaap.pdf', 2008), ('petrobras-dfp-2009-brgaap.pdf', 2009)]
    for arq, n in dfp:
        vint = f'DFP {n} (BR GAAP), site de RI da Petrobras'
        ft = f'Petrobras, DFP {n} (BR GAAP)'
        anc = r'^3\.1[0-9]\s+Lucro/Preju[ií]zo do Per[ií]odo'
        S += extrai(E, arq, 'layout', anc, [(0, n, RS_CTRL), (1, n - 1, RS_CTRL), (2, n - 2, RS_CTRL)], RS_CTRL, 'R$ mil',
                    ft, vint, minnums=3)
        S += extrai(E, arq, 'layout', anc, [(0, n, RS_CONS), (1, n - 1, RS_CONS), (2, n - 2, RS_CONS)], RS_CONS, 'R$ mil',
                    ft, vint, minnums=3, apos=r'DEMONSTRA..O DO RESULTADO CONSOLIDADO')
    # DFP 2010 (IFRS, uso local): 2009 e 2008 reapresentados (controladora)
    S += extrai(E, 'petrobras-dfp-2010-ifrs.pdf', 'layout', r'^3\.11\s+Lucro/Preju[ií]zo do Per[ií]odo',
                [(1, 2009, 'controladora, IFRS (uso local, primeira adoção em 2010), R$ mil; 2009 reapresentado'),
                 (2, 2008, 'controladora, IFRS (uso local), R$ mil; 2008')],
                'controladora, IFRS, R$ mil', 'R$ mil', 'Petrobras, DFP 2010 (IFRS)', 'DFP 2010 (IFRS), site de RI da Petrobras', minnums=3)
    S += extrai(E, 'petrobras-dfp-2010-ifrs.pdf', 'layout', r'^3\.11\s+Lucro/Preju[ií]zo Consolidado do Per[ií]odo',
                [(1, 2009, 'consolidado, IFRS (uso local, primeira adoção em 2010), "Lucro/Prejuízo Consolidado do Período" (inclui não controladores), R$ mil; 2009 reapresentado'),
                 (2, 2008, 'consolidado, IFRS (uso local), "Lucro/Prejuízo Consolidado do Período" (inclui não controladores), R$ mil; 2008 reapresentado')],
                'consolidado, IFRS, R$ mil', 'R$ mil', 'Petrobras, DFP 2010 (IFRS)', 'DFP 2010 (IFRS), site de RI da Petrobras', minnums=3,
                apos=r'DFs Consolidadas / Demonstra..o do Resultado$')
    return S
