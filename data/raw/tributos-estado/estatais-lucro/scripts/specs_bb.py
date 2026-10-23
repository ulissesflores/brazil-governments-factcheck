"""Banco do Brasil: lucro líquido anual (R$ milhões nos Relatórios Anuais; R$ mil nas Demonstrações Contábeis)."""
from estatais_lib import extrai

E = 'banco-do-brasil'
RA_DEF = ('quadro de indicadores do Relatório Anual (rótulo da fonte: "%s"); o quadro não diz se é consolidado ou '
          'controladora; o ativo total do mesmo quadro coincide com o do Conglomerado (consolidado); '
          'legislação societária (Lei 6.404/76) com normas do Banco Central (BR GAAP bancário); exercício anual')
DC_BM = ('Demonstração do Resultado, coluna BB-Banco Múltiplo (controladora/individual); legislação societária '
         '(Lei 6.404/76) e normas do Banco Central (BR GAAP bancário/COSIF); exercício anual; R$ mil')
DC_CO = ('Demonstração do Resultado, coluna BB-Consolidado; legislação societária (Lei 6.404/76) e normas do Banco '
         'Central (BR GAAP bancário/COSIF); exercício anual; R$ mil')


def specs():
    S = []
    ra = lambda arq, vint, fonte, anc, cols, rot, **k: S.extend(extrai(
        E, arq, 'layout', anc, cols, RA_DEF % rot, 'R$ milhões', fonte, vint, **k))
    # Relatório Anual 1998: texto do capítulo Desempenho Financeiro
    S += extrai(E, 'bb-ra-Relatorio-Anual-1998.pdf', 'layout', r'Com o lucro l[ií]quido apurado no exerc[ií]cio, R\$',
                [(0, 1998)], 'texto "lucro líquido apurado no exercício" do capítulo Desempenho Financeiro do Relatório Anual; '
                'seção sobre resultado consolidado (legislação societária); exercício 1998', 'R$ milhões',
                'Banco do Brasil, Relatório Anual 1998', 'Relatório Anual 1998 (publicado em 1999)')
    ra('bb-ra-Relatorio-Anual-1999.pdf', 'Relatório Anual 1999 (publicado em 2000)', 'Banco do Brasil, Relatório Anual 1999',
       r'^\s*Resultado(?=\s+\(?\d)', [(0, 1999), (1, 1998), (2, 1997), (3, 1996), (4, 1995)], 'Resultado',
       apos=r'Banco do Brasil em Grandes N[uú]meros', minnums=5)
    ra('bb-ra-Relatorio-Anual-2000.pdf', 'Relatório Anual 2000 (publicado em 2001)', 'Banco do Brasil, Relatório Anual 2000',
       r'^\s*Lucro L[ií]quido(?=\s+\d)', [(0, 2000), (1, 1999), (2, 1998), (3, 1997)], 'Lucro Líquido', minnums=4)
    ra('bb-ra-Relatorio-Anual-2001.pdf', 'Relatório Anual 2001 (publicado em 2002)', 'Banco do Brasil, Relatório Anual 2001',
       r'^\s*Lucro L[ií]quido(?=\s+\d)', [(0, 1998), (1, 1999), (2, 2000), (3, 2001)], 'Lucro Líquido', minnums=4)
    ra('bb-ra-Relatorio-Anual-e-de-Responsabilidade-Social-2002.pdf', 'Relatório Anual e de Responsabilidade Social 2002 (publicado em 2003)',
       'Banco do Brasil, Relatório Anual e de Responsabilidade Social 2002', r'^\s*Lucro L[ií]quido(?=\s+\d)',
       [(0, 1998), (1, 1999), (2, 2000), (3, 2001), (4, 2002)], 'Lucro Líquido', minnums=5)
    ra('bb-ra-Relatorio-Anual-e-de-Responsabilidade-Socioambiental-2003.pdf', 'Relatório Anual e de Responsabilidade Socioambiental 2003 (publicado em 2004)',
       'Banco do Brasil, Relatório Anual e de Responsabilidade Socioambiental 2003', r'^\s*Lucro L[ií]quido(?=\s+\d)',
       [(0, 1999), (1, 2000), (2, 2001), (3, 2002), (4, 2003)], 'Lucro Líquido', minnums=5)
    ra('bb-ra-Relatorio-Anual-2004.pdf', 'Relatório Anual 2004 (publicado em 2005)', 'Banco do Brasil, Relatório Anual 2004',
       r'^\s*Lucro L[ií]quido(?=\s+\d)', [(0, 2000), (1, 2001), (2, 2002), (3, 2003), (4, 2004)], 'Lucro Líquido', minnums=5)
    ra('bb-ra-Relatorio-Anual-2005.pdf', 'Relatório Anual 2005 (publicado em 2006)', 'Banco do Brasil, Relatório Anual 2005',
       r'^\s*Lucro L[ií]quido(?=\s+\d)', [(0, 2001), (1, 2002), (2, 2003), (3, 2004), (4, 2005)], 'Lucro Líquido', minnums=5)
    ra('bb-ra-Relatorio-Anual-2006.pdf', 'Relatório Anual 2006 (publicado em 2007)', 'Banco do Brasil, Relatório Anual 2006',
       r'^\s*Lucro L[ií]quido(?=\s+4\.154)', [(0, 2005), (1, 2006)], 'Lucro Líquido', minnums=2)
    ra('bb-ra-Relatorio-Anual-2007-Parte-I.pdf', 'Relatório Anual 2007, Parte I (publicado em 2008)', 'Banco do Brasil, Relatório Anual 2007 (Parte I)',
       r'^\s*Lucro L[ií]quido(?=\s+2\.381)', [(0, 2003), (1, 2004), (2, 2005), (3, 2006), (4, 2007)], 'Lucro Líquido', minnums=5)
    ra('bb-rda-Relatorio-de-Administracao-2008.pdf', 'Relatório da Administração 2008 (publicado em 2009)', 'Banco do Brasil, Relatório da Administração 2008',
       r'^\s*Lucro L[ií]quido(?=\s+5\.058)', [(0, 2007), (1, 2008)], 'Lucro Líquido', minnums=2)
    ra('bb-ra-Relatorio-Anual-2010.pdf', 'Relatório Anual 2010 (publicado em 2011)', 'Banco do Brasil, Relatório Anual 2010',
       r'^\s*Lucro L[ií]quido(?=\s+11\.703)', [(1, 2009)], 'Lucro Líquido', minnums=2)

    # Demonstrações Contábeis do 4T/exercício: DRE com 6 colunas: [2S N, N, N-1] banco múltiplo e [2S N, N, N-1] consolidado
    dc = [('bb-dc-Demonstracoes-Contabeis-2002.pdf', 2002, 'Demonstrações Contábeis 2002'),
          ('bb-dc-Demonstracoes-Contabeis-2003.pdf', 2003, 'Demonstrações Contábeis 2003'),
          ('bb-dc-Demonstracoes-Contabeis-2004.pdf', 2004, 'Demonstrações Contábeis 2004'),
          ('bb-dc-Demonstracoes-Contabeis-2005.pdf', 2005, 'Demonstrações Contábeis 2005'),
          ('bb-dc-Demonstracoes-Contabeis-2006.pdf', 2006, 'Demonstrações Contábeis 2006'),
          ('bb-dc-Demonstracoes-Contabeis-4T07.pdf', 2007, 'Demonstrações Contábeis 4T07'),
          ('bb-dc-Demonstracoes-Contabeis-4T08.pdf', 2008, 'Demonstrações Contábeis 4T08'),
          ('bb-dc-Demonstracoes-Contabeis-4T09.pdf', 2009, 'Demonstrações Contábeis 4T09'),
          ('bb-dc-Demonstracoes-Contabeis-4T10.pdf', 2010, 'Demonstrações Contábeis 4T10')]
    for arq, n, rot in dc:
        v = f'{rot} (publicado em {n + 1})'
        f = f'Banco do Brasil, {rot}'
        anc = r'^\s*LUCRO L[IÍ]QUIDO\b[ .]*(\(Nota[^)]*\))?'
        cols = [(1, n, DC_BM), (2, n - 1, DC_BM), (4, n, DC_CO), (5, n - 1, DC_CO)]
        if n == 2010: cols = [(2, 2009, DC_BM), (5, 2009, DC_CO)]  # 2010 é coberto pela CVM/DFP do solicitante
        S += extrai(E, arq, 'layout', anc, cols, DC_BM, 'R$ mil', f, v, minnums=6)
    return S
