"""Eletrobras (Centrais Elétricas Brasileiras): lucro líquido anual, R$ (mil, milhões conforme a edição)."""
from estatais_lib import extrai

E = 'eletrobras'
BR_CONS = ('consolidado, BR GAAP (Lei 6.404/76), "Lucro Líquido do Exercício" depois da participação minoritária e da '
           'participação nos lucros; Demonstração de Resultado Consolidada do Relatório da Administração; R$ mil')
BR_TXT = ('texto do Relatório da Administração sobre o lucro do exercício da ELETROBRÁS (BR GAAP, Lei 6.404/76); '
          'o texto não diz se é controladora ou consolidado')
ATR = 'consolidado, US GAAP em reais, atribuível aos acionistas da Companhia (exclui não controladores), R$ mil'
USG = ('consolidado, US GAAP em reais (norma do 20-F/Form 20-F de registro), "Net income for the year" depois de '
       'minoritários, R$ mil')


def specs():
    S = []
    S += extrai(E, 'eletrobras-wb-relatorio-anual-2001.pdf', 'layout', r'^\s*Lucro l[ií]quido\s+1,255\.9\s+(?=\d)',
                [(0, 2001, 'texto/quadro do Relatório Anual 2001 em R$ milhões; coluna R$ da linha "Lucro líquido" (BR GAAP, Lei 6.404/76); '
                           'o quadro tem colunas US$ e R$ com cabeçalho desalinhado; consolidado/controladora não declarado')],
                BR_TXT, 'R$ milhões', 'Eletrobras, Relatório Anual 2001 (Wayback Machine)', 'Relatório Anual 2001 (publicado em 2002)',
                fmt='br', minnums=2, obs='colunas da linha: [2000 US$ milhões, 2001 R$ milhões, 2001 US$ milhões]; o 1º número (US$) foi pulado pela âncora')
    S += extrai(E, 'eletrobras-rda-2004.pdf', 'layout', r'^\s*Lucro L[ií]quido do Exerc[ií]cio(?=\s+[\d(])',
                [(0, 2000), (1, 2001), (2, 2002), (3, 2003), (4, 2004)], BR_CONS, 'R$ mil',
                'Eletrobras, Relatório da Administração 2004', 'Relatório da Administração 2004 (publicado em 2005)', minnums=5)
    S += extrai(E, 'eletrobras-rda-2005.pdf', 'layout', r'^\s*Exerc[ií]cio(?=\s+1\.100\.340)',
                [(0, 2002), (1, 2003), (2, 2004), (3, 2005)], BR_CONS, 'R$ mil',
                'Eletrobras, Relatório da Administração 2005', 'Relatório da Administração 2005 (publicado em 2006)', minnums=4,
                obs='o rótulo "Lucro Líquido do" está na linha anterior; colunas 2002 a 2005')
    S += extrai(E, 'eletrobras-rda-2006.pdf', 'layout', r'^\s*Lucro L[ií]quido do Exerc[ií]cio(?=\s+1\.100)',
                [(0, 2002), (1, 2003), (2, 2004), (3, 2005), (4, 2006)],
                BR_CONS.replace('R$ mil', 'R$ milhões (arredondado na fonte)'), 'R$ milhões',
                'Eletrobras, Relatório da Administração 2006', 'Relatório da Administração 2006 (publicado em 2007)', minnums=5)
    S += extrai(E, 'eletrobras-rda-2007.pdf', 'layout', r'encerrou o exerc[ií]cio de 2007 com lucro de R\$', [(0, 2007)], BR_TXT,
                'R$ milhões', 'Eletrobras, Relatório da Administração 2007', 'Relatório da Administração 2007 (publicado em 2008)')
    S += extrai(E, 'eletrobras-rda-2007.pdf', 'layout', r'No exerc[ií]cio de 2006, a empresa registrou lucro de R\$', [(0, 2006)], BR_TXT,
                'R$ milhões', 'Eletrobras, Relatório da Administração 2007', 'Relatório da Administração 2007 (publicado em 2008)')
    S += extrai(E, 'eletrobras-rda-2008.pdf', 'layout', r'Um excepcional lucro l[ií]quido de R\$', [(0, 2008)],
                BR_TXT + '; a fonte escreve "R$6.136.497 milhões", mas o mesmo documento diz "R$ 6,1 bilhões": a unidade correta é R$ mil',
                'R$ mil', 'Eletrobras, Relatório da Administração 2008', 'Relatório da Administração 2008 (publicado em 2009)')
    S += extrai(E, 'eletrobras-rda-2009.pdf', 'layout', r'O lucro foi de R\$', [(0, 2009)], BR_TXT, 'R$ milhões',
                'Eletrobras, Relatório da Administração 2009', 'Relatório da Administração 2009 (publicado em 2010)')
    S += extrai(E, 'eletrobras-rda-2009.pdf', 'layout', r'^empresa registrou R\$', [(0, 2008)], BR_TXT, 'R$ milhões',
                'Eletrobras, Relatório da Administração 2009', 'Relatório da Administração 2009 (publicado em 2010)',
                obs='frase continua da linha anterior: "No mesmo período do exercício de 2008 a / empresa registrou R$ 6.136 milhões"')

    # 20-F / Form 20-F (SEC): US GAAP em R$ mil
    S += extrai(E, 'eletrobras-20fr12b-2008-07-21-d20fr12b.htm', 'html', r'^Net income for the year(?= \|)',
                [(0, 2007), (1, 2006), (2, 2005)], USG, 'R$ mil', 'Eletrobras, Form 20-F de registro (SEC), Consolidated Income Statement',
                'Form 20-F de registro (20FR12B), SEC 2008-07-21', fmt='us', minnums=3,
                obs='a fonte declara que os dados de 2003 e 2004 não foram incluídos porque "cannot be provided on a restated basis without unreasonable effort and expense"')
    S += extrai(E, 'eletrobras-20fr12ba-2008-09-08-d20fr12ba.htm', 'html', r'^Net income for the year(?= \|)',
                [(0, 2007), (1, 2006), (2, 2005)], USG, 'R$ mil', 'Eletrobras, Form 20-F de registro, Amendment 1 (SEC)',
                'Form 20-F de registro, emenda 1 (20FR12B/A), SEC 2008-09-08', fmt='us', minnums=3)
    S += extrai(E, 'eletrobras-20f-2009-07-01-d20f.htm', 'html', r'^Net income for the year(?= \|)',
                [(0, 2008), (1, 2007), (2, 2006), (3, 2005)], USG, 'R$ mil', 'Eletrobras, Form 20-F exercício 2008 (SEC)',
                '20-F do exercício 2008 (SEC 2009-07-01)', fmt='us', minnums=4)
    S += extrai(E, 'eletrobras-20f-2011-07-01-d20f.htm', 'html', r'^Net income \(loss\) for the year(?= \|)',
                [(0, 2009, USG + '; reapresentado'), (1, 2008, USG + '; reapresentado'), (2, 2007, USG + '; reapresentado'),
                 (3, 2006, USG + '; reapresentado'), (4, 2005, USG + '; reapresentado')], USG, 'R$ mil',
                'Eletrobras, Form 20-F exercício 2009 (SEC, entregue em 2011)', '20-F do exercício 2009 (SEC 2011-07-01)',
                fmt='us', minnums=5)
    S += extrai(E, 'eletrobras-20f-2011-07-01-d20f.htm', 'html', r'^Net income \(loss\) attributable to the Company.s stockholders(?= \|)',
                [(0, 2009, ATR),
                 (1, 2008, ATR), (2, 2007, ATR), (3, 2006, ATR), (4, 2005, ATR)], USG, 'R$ mil',
                'Eletrobras, Form 20-F exercício 2009 (SEC, entregue em 2011)', '20-F do exercício 2009 (SEC 2011-07-01)',
                fmt='us', minnums=5)
    S += extrai(E, 'eletrobras-20f-2011-10-17-d212707d20f.htm', 'html', r'^Net income of the year(?= \|)',
                [(1, 2009, 'consolidado, IFRS (adotado no 20-F do exercício 2010, em substituição ao US GAAP), "Net income of the year", R$ mil')],
                'consolidado, IFRS, R$ mil', 'R$ mil', 'Eletrobras, Form 20-F exercício 2010 (SEC)', '20-F do exercício 2010 (SEC 2011-10-17)',
                fmt='us', minnums=2)
    S += extrai(E, 'eletrobras-20f-2011-10-17-d212707d20f.htm', 'html', r'^Attributable to controlling shareholders(?= \|)',
                [(1, 2009, 'consolidado, IFRS, parte atribuível aos acionistas controladores, R$ mil')],
                'consolidado, IFRS, atribuível a controladores, R$ mil', 'R$ mil', 'Eletrobras, Form 20-F exercício 2010 (SEC)',
                '20-F do exercício 2010 (SEC 2011-10-17)', fmt='us', minnums=2)
    S += extrai(E, 'eletrobras-20f-2012-05-22-d350457d20f.htm', 'html', r'^Net income for the year(?= \|)',
                [(2, 2009, 'consolidado, IFRS, "Net income for the year", R$ mil')],
                'consolidado, IFRS, R$ mil', 'R$ mil', 'Eletrobras, Form 20-F exercício 2011 (SEC)', '20-F do exercício 2011 (SEC 2012-05-22)',
                fmt='us', minnums=3)
    return S
