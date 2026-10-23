"""Correios (ECT): lucro/prejuízo líquido anual das demonstrações contábeis anuais (Lei 6.404/76; CPC a partir de 2010)."""
from estatais_lib import extrai, manual

E = 'correios'
DEF0 = ('lucro líquido do exercício da ECT (demonstrações da empresa; sem coluna consolidada), Lei 6.404/76 e NBC, '
        'DRE "Lucro líquido do exercício"; valor em reais com centavos; a DRE desta edição não tem linha de reversão de juros sobre capital próprio (a linha só aparece na edição 2006)')
DEF_JCP = ('resultado do exercício da ECT, Lei 6.404/76 e NBC, DRE "Resultado do exercício" = lucro líquido + reversão dos juros '
           'sobre capital próprio (JCP) de R$ 198.321.281,93; valor em reais com centavos')
DEF1 = ('lucro líquido do exercício da ECT (demonstrações da empresa), Lei 6.404/76 e NBC, DRE "Lucro líquido do exercício"; '
        'a partir da edição 2007 a linha INCLUI a reversão dos juros sobre capital próprio (JCP); valor em reais com centavos')
DEF_M = ('lucro líquido do exercício da ECT (demonstrações da empresa), DRE; inclui a reversão dos juros sobre capital próprio; '
         'R$ milhões (1 casa decimal na DRE de 2008; 2 casas na DFC de 2009)')
DEF_CPC = ('resultado líquido do período, demonstrações individuais da ECT, Lei 6.404/76 com CPCs (convergência às normas '
           'internacionais), R$ mil')
IND = 'resultado líquido do período, demonstrações INDIVIDUAIS da ECT, Lei 6.404/76 com CPCs, R$ mil'
CONS = 'resultado líquido do período, demonstrações CONSOLIDADAS (ECT e controladas), Lei 6.404/76 com CPCs, R$ mil'


def specs():
    S = []
    f = lambda n: f'Correios, Demonstrações Contábeis {n}'
    v = lambda n: f'Demonstrações Contábeis {n} (publicadas em {n + 1})'
    # --- PDFs-imagem lidos visualmente (página renderizada e conferida a olho)
    S += manual(E, 'correios-df-2001.pdf', 2001, '506712415.85', DEF0, 'R$', f(2001), v(2001),
                'pág. 2 (página girada 90°), item "11. LUCRO LÍQUIDO DO EXERCÍCIO", coluna 2001', 'LUCRO LÍQUIDO DO EXERCÍCIO 506.712.415,85')
    S += manual(E, 'correios-df-2001.pdf', 2000, '192201615.95', DEF0, 'R$', f(2001), v(2001) + '; coluna 2000 (comparativo)',
                'pág. 2 (página girada 90°), item "11. LUCRO LÍQUIDO DO EXERCÍCIO", coluna 2000', 'LUCRO LÍQUIDO DO EXERCÍCIO 192.201.615,95')
    S += manual(E, 'correios-df-2004.pdf', 2004, '316928926.29', DEF0, 'R$', f(2004), v(2004),
                'pág. 3, "LUCRO LÍQUIDO DO EXERCÍCIO", coluna 2004 (o OCR leu 316.920.926,29; a imagem e o comparativo da edição 2005 dizem 316.928.926,29)',
                'LUCRO LÍQUIDO DO EXERCÍCIO 316.928.926,29 288.210.258,45')
    S += manual(E, 'correios-df-2004.pdf', 2003, '288210258.45', DEF0, 'R$', f(2004), v(2004) + '; coluna 2003 (comparativo)',
                'pág. 3, "LUCRO LÍQUIDO DO EXERCÍCIO", coluna 2003', 'LUCRO LÍQUIDO DO EXERCÍCIO 316.928.926,29 288.210.258,45')
    S += manual(E, 'correios-df-2010.pdf', 2010, '826947319.57', DEF_JCP.replace('R$ 198.321.281,93', 'JCP'), 'R$', f(2010), v(2010),
                'pág. 3 (Demonstração das Mutações do Patrimônio Líquido), linha "Resultado do período" de 2010, coluna Lucros Acumulados',
                'Resultado do período 826.947.319,57')
    S += manual(E, 'correios-df-2010.pdf', 2009, '117546308.83', DEF_JCP.replace('R$ 198.321.281,93', 'JCP'), 'R$', f(2010), v(2010) + '; linha de 2009 (comparativo)',
                'pág. 3 (Demonstração das Mutações do Patrimônio Líquido), linha "Resultado do período" de 2009, coluna Lucros Acumulados',
                'Resultado do período 117.546.308,83')
    # --- texto nativo, valores em reais
    anc = r'^\s*LUCRO L.QUIDO DO EXERC.CIO(?=\s+\d)'
    for n in (2002, 2003, 2005):
        S += extrai(E, f'correios-df-{n}.pdf', 'layout', anc, [(0, n), (1, n - 1)], DEF0, 'R$', f(n), v(n), minnums=2)
    S += extrai(E, 'correios-df-2006.pdf', 'layout', anc, [(0, 2006), (1, 2005)], DEF0, 'R$', f(2006), v(2006), minnums=2)
    S += extrai(E, 'correios-df-2006.pdf', 'layout', r'^\s*RESULTADO DO EXERC.CIO(?=\s+\d)', [(0, 2006), (1, 2005)], DEF_JCP, 'R$', f(2006), v(2006), minnums=2)
    S += extrai(E, 'correios-df-2007.pdf', 'layout', anc, [(0, 2007, DEF1), (1, 2006, DEF1 + '; 2006 reapresentado com a reversão de JCP incluída')], DEF1, 'R$', f(2007), v(2007), minnums=2)
    S += extrai(E, 'correios-df-2008.pdf', 'layout', anc, [(0, 2008), (1, 2007)], DEF_M, 'R$ milhões', f(2008), v(2008), minnums=2)
    S += extrai(E, 'correios-df-2009.pdf', 'layout', r'^\s*Lucro L.quido do Per.odo(?=\s+\d)', [(0, 2009), (1, 2008)], DEF_M, 'R$ milhões', f(2009), v(2009), minnums=2,
                obs='linha da Demonstração dos Fluxos de Caixa (a DRE desta edição não saiu em texto)')
    # --- OCR (PDF-imagem; valores conferidos entre edições sucessivas)
    ocr = [(2011, r'^Lucro Liquido do Periodo(?=\s+\d)', 2, [(0, 2011), (1, 2010)]),
           (2012, r'^Lucro L.quido do Per.odo(?=\s+\d)', 2, [(0, 2012), (1, 2011)]),
           (2013, r'^Lucro L.quido do Per.odo(?=\s+\d)', 2, [(0, 2013), (1, 2012)])]
    for n, a, mn, cols in ocr:
        S += extrai(E, f'correios-df-{n}.pdf', 'ocr', a, cols, DEF_CPC, 'R$ mil', f(n), v(n), minnums=mn)
    # --- texto nativo 2014 e 2018+: colunas conforme a edição
    S += extrai(E, 'correios-df-2014.pdf', 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])', [(0, 2014, IND), (1, 2013, IND + '; 2013 reapresentado'), (2, 2014, CONS)],
                IND, 'R$ mil', f(2014), v(2014), minnums=3, obs='colunas: [indiv. 2014, indiv. 2013, consolid. 2014]')
    for n in (2015, 2016):
        S += extrai(E, f'correios-df-{n}.pdf', 'ocr', r'^RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])',
                    [(0, n, IND), (1, n - 1, IND + '; ano anterior reapresentado'), (2, n, CONS), (3, n - 1, CONS + '; ano anterior reapresentado')], IND,
                    'R$ mil', f(n), v(n), minnums=4, obs='colunas: [indiv. N, indiv. N-1, consolid. N, consolid. N-1]')
    S += extrai(E, 'correios-df-2017.pdf', 'ocr', r'RESULTADO L.QUIDO DO EXERC.CIO(?=\s+[\d(])',
                [(0, 2017, IND), (1, 2016, IND + '; ano anterior reapresentado'), (2, 2017, CONS), (3, 2016, CONS + '; ano anterior reapresentado')], IND,
                'R$ mil', f(2017), v(2017), minnums=4, obs='colunas: [indiv. N, indiv. N-1, consolid. N, consolid. N-1]')
    for n in (2018, 2019):
        S += extrai(E, f'correios-df-{n}.pdf', 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])',
                    [(0, n, IND), (1, n - 1, IND + '; ano anterior como na edição'), (2, n, CONS), (3, n - 1, CONS + '; ano anterior como na edição')], IND,
                    'R$ mil', f(n), v(n), minnums=4, obs='colunas: [indiv. N, indiv. N-1, consolid. N, consolid. N-1]')
    for n, a in ((2020, r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'), (2021, r'^\s*RESULTADO L.QUIDO DO EXERC.CIO(?=\s+[\d(])'),
                 (2023, r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'), (2024, r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'),
                 (2025, r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])')):
        S += extrai(E, f'correios-df-{n}.pdf', 'layout', a, [(0, n, IND), (1, n - 1, IND + '; ano anterior como na edição (pode estar reapresentado)')], IND,
                    'R$ mil', f(n), v(n), minnums=2)
    S += extrai(E, 'correios-df-2022.pdf', 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])',
                [(0, 2022, IND), (1, 2021, IND + '; "reclassificado" na edição'), (2, 2020, IND + '; "reclassificado" na edição')], IND,
                'R$ mil', f(2022), v(2022), minnums=3, obs='colunas: [31/12/22, 31/12/21 reclassificado, 31/12/20 reclassificado]')
    return S
