"""Gera quebras.csv. Cada trecho citado é recuperado do bruto (falha se não existir). Sem rede.
uso: python3 -I scripts/gerar_quebras.py
"""
import sys, csv, json, re
sys.path.insert(0, '/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/estatais-lucro/scripts')
import estatais_lib as L

# url do bruto = última entrada da cadeia de hash para o arquivo
URL = {}
for l in open(L.BASE + '/manifest.jsonl'):
    d = json.loads(l)
    URL[d['arquivo'].split('/')[-1]] = d.get('url') or ''


def T(arq, modo, rx, junta=0, apos=None, occ=1, fmt='br'):
    pi, li, texto, _ = L.acha(arq, modo, rx, apos=apos, occ=occ, junta=junta, minnums=0, fmt=fmt)
    loc = f'pág. {pi}, linha {li}' if modo not in ('html', 'txt') else f'linha {li} do texto convertido'
    t = L.norm(texto)
    m = re.search(rx, t, re.I)
    if m: t = t[m.start():]
    return f'«{t[:330]}» ({arq}, {loc})'


def U(*arqs):
    return ' | '.join(URL.get(a, '?') for a in arqs)


Q = []


def q(serie, data, tipo, antigo, novo, razao, arqs, trechos, direcao, como_dir, efeito, como_med, aprim):
    Q.append(dict(indicador='lucro_liquido', serie=serie, data_quebra=data, tipo_de_quebra=tipo, metodo_antigo=antigo,
                  metodo_novo=novo, razao_declarada_pela_fonte=razao, fonte_primaria_url=U(*arqs),
                  trecho_citado=' || '.join(trechos), direcao_do_efeito=direcao, como_a_direcao_foi_determinada=como_dir,
                  efeito_medido=efeito, como_medido=como_med, apresentada_como_aprimoramento=aprim))


# ---------------- PETROBRAS
FA = 'petrobras-wb-financial-analysis-99.pdf'
q('petrobras', '1999-10-15 (aplicada retroativamente a 1999-01-01)', 'mudanca_de_regra',
  'custos de prospecção e perfuração de petróleo e gás lançados como despesa no período em que incorridos, depreciação linear dos equipamentos de produção',
  'método dos esforços bem-sucedidos: capitaliza custos de campos economicamente viáveis, deprecia por unidade de produção, provisiona o abandono de instalações; também mudou a contabilização de benefícios de pensão/saúde e de manutenção programada',
  'adequar as práticas às das grandes petroleiras internacionais e criar métricas de desempenho compatíveis com as práticas internacionais',
  [FA],
  [T(FA, 'layout', r'On October 15, 1999, PETROBRAS.s Board of Directors approved changes', junta=3),
   T(FA, 'layout', r'Up to December 31, 1998, under the previous accounting policy PETROBRAS, conservatively', junta=1),
   T(FA, 'layout', r'^\s*Net income for the year\s+\(1\.750\.064\)')],
  'reduz o lucro de 1999', 'sinal negativo na linha "Net income for the year" da tabela de efeitos da própria fonte',
  '-1.750.064 mil R$ sobre o lucro líquido de 1999 (lucro consolidado publicado depois da mudança: R$ 1.757 milhões)',
  'tabela "Effects of the changes in accounting practices through December 31, 1999" (nota 2(b)(vi)); 1998 (R$ 1.389 milhões) não foi reapresentado: a série 1998 -> 1999 mistura duas práticas',
  'sim (justificada como alinhamento às práticas internacionais)')

q('petrobras', '2003-01-01', 'mudanca_de_regra',
  'US GAAP com SFAS 19: custos de abandono reconhecidos como depreciação (US$ 284 milhões em 2002)',
  'SFAS 143 (obrigações de desativação de ativos): depreciação sobre a obrigação em DD&A e accretion em exploração; efeito cumulativo no resultado',
  'adoção do SFAS 143',
  ['petrobras-20f-fy2003-d20f.htm'],
  [T('petrobras-20f-fy2003-d20f.htm', 'html', r'^Cumulative effect of change in accounting principle, net of taxes\s*\(2\)', fmt='us', occ=1),
   T('petrobras-20f-fy2003-d20f.htm', 'html', r'as a result of our adoption of SFAS 143', fmt='us')],
  'aumenta o lucro de 2003', 'sinal positivo (697) na linha do efeito cumulativo, dentro do lucro de US$ 6.559 milhões',
  '+US$ 697 milhões em 2003 (efeito cumulativo líquido de impostos)',
  'linha "Cumulative effect of change in accounting principle, net of taxes | 697" do quadro de dados selecionados', 'não declarado (apresentada como adoção de norma)')

q('petrobras', '1998-01-01', 'mudanca_de_unidade',
  'valores em US$ até 31/12/1997 remensurados do real por taxas históricas (itens não monetários), taxa de fim de período (monetários) e média mensal (resultado), porque o Brasil era economia altamente inflacionária pelo SFAS 52',
  'a partir de 1998 convertidos do real pelo critério de conversão do SFAS 52',
  'a fonte explica que o Brasil era economia de alta inflação (inflação acumulada de 3 anos acima de 100%) até 01/01/1998',
  ['petrobras-20f-fy2001-d20f.txt'],
  [T('petrobras-20f-fy2001-d20f.txt', 'txt', r'highly inflationary economy, defined under SFAS 52 as an', junta=3, fmt='us')],
  'indeterminada', 'a fonte não mede o efeito', 'não medido',
  'não medido; o lucro de 1997 em US$ (US$ 1.419 milhões) não é comparável por construção ao de 1998 (US$ 378 milhões)', 'não declarado')

q('petrobras', '2010-01-01 (primeiro trimestre de 2010)', 'mudanca_de_regra',
  'demonstrações locais em BR GAAP (Lei 6.404/76 e normas da CVM): lucro controladora 2009 = R$ 29.313.418 mil',
  'demonstrações locais em IFRS: lucro controladora 2009 reapresentado = R$ 29.958.745 mil; lucro consolidado IFRS (inclui não controladores) 2009 = R$ 33.344.072 mil contra R$ 28.981.708 mil em BR GAAP (depois de minoritários)',
  'a empresa escolheu apresentar as demonstrações locais em IFRS pela primeira vez no primeiro trimestre de 2010; o BR GAAP estava em convergência ao IFRS (Lei 11.638/07)',
  ['petrobras-20f-fy2010-pbraform20f2010.htm', 'petrobras-dfp-2009-brgaap.pdf', 'petrobras-dfp-2010-ifrs.pdf'],
  [T('petrobras-20f-fy2010-pbraform20f2010.htm', 'html', r'The Company chose to present its financial statements for local purposes for the first time', fmt='us'),
   T('petrobras-dfp-2009-brgaap.pdf', 'layout', r'^3\.1[0-9]\s+Lucro/Preju[ií]zo do Per[ií]odo', occ=1),
   T('petrobras-dfp-2010-ifrs.pdf', 'layout', r'^3\.11\s+Lucro/Preju[ií]zo do Per[ií]odo')],
  'aumenta o lucro da controladora de 2009 (2008 não mudou)', 'diferença entre a linha 3.15 da DFP 2009 (BR GAAP) e a linha 3.11 da DFP 2010 (IFRS), mesma entidade e mesmo ano',
  'controladora 2009: +645.327 mil R$ (29.313.418 -> 29.958.745); controladora 2008: 0 (36.469.549 nos dois)',
  'subtração das duas linhas; a diferença no consolidado não é comparável porque a definição mudou (depois de minoritários -> inclui minoritários)',
  'não declarado (apresentada como convergência)')

q('petrobras', '2009 (20-F do exercício 2009)', 'mudanca_de_regra',
  'linha do 20-F "Net income for the year" (consolidado, US GAAP)',
  'linha do 20-F "Net income for the year attributable to Petrobras", com não controladores apresentados à parte',
  'a fonte não declara, no trecho lido, a razão do rótulo novo',
  ['petrobras-20f-fy2009-pbraform20f2009.htm', 'petrobras-20f-fy2008-y76586e20vf.htm'],
  [T('petrobras-20f-fy2009-pbraform20f2009.htm', 'html', r'^Net income for the year attributable to Petrobras', fmt='us'),
   T('petrobras-20f-fy2008-y76586e20vf.htm', 'html', r'^Net income for the year\s*\(1\)', fmt='us')],
  'sem efeito nos valores já publicados', 'os anos repetidos (2008: 18.879; 2007: 13.138; 2006: 12.826; 2005: 10.344) são idênticos nas duas edições',
  '0 nos anos repetidos', 'comparação ano a ano entre o 20-F do exercício 2008 e o do exercício 2009', 'não declarado')

# ---------------- BANCO DO BRASIL
q('banco-do-brasil', '1997 (exercício reapresentado na edição 2000)', 'revisao_de_vintage',
  'Relatório Anual 1999: Resultado de 1997 = R$ 573 milhões', 'Relatório Anual 2000: Lucro Líquido de 1997 = R$ 574 milhões',
  'a fonte não declara a razão da diferença',
  ['bb-ra-Relatorio-Anual-1999.pdf', 'bb-ra-Relatorio-Anual-2000.pdf'],
  [T('bb-ra-Relatorio-Anual-1999.pdf', 'layout', r'^\s*Resultado(?=\s+\(?\d)', apos=r'Banco do Brasil em Grandes N[uú]meros'),
   T('bb-ra-Relatorio-Anual-2000.pdf', 'layout', r'^\s*Lucro L[ií]quido(?=\s+\d)')],
  'aumenta R$ 1 milhão', 'comparação direta dos dois quadros', '+1 milhão R$ (573 -> 574)',
  'subtração das duas linhas; pode ser arredondamento, a fonte não diz', 'não')

BB8 = 'bb-dc-Demonstracoes-Contabeis-4T08.pdf'
q('banco-do-brasil', '2008-01-01 (exercício 2008)', 'mudanca_de_regra',
  'lucro líquido calculado sem os efeitos da Lei 11.638/07 e da MP 449/08: R$ 8.870.636 mil',
  'lucro líquido com os efeitos da Lei 11.638/07 e da MP 449/08 (nova lei contábil e convergência às normas internacionais): R$ 8.802.869 mil',
  'o quadro de conciliação da nota explicativa lista despesa por análise de recuperabilidade (impairment) de R$ 83.671 mil e efeitos tributários de R$ 15.904 mil (a própria fonte grafa "Lei n.º 11.938/07")',
  [BB8],
  [T(BB8, 'layout', r'Lucro l[ií]quido do exerc[ií]cio e patrim.nio l[ií]quido sem efeitos da Lei'),
   T(BB8, 'layout', r'Lucro l[ií]quido do exerc[ií]cio e patrim.nio l[ií]quido com efeitos da Lei')],
  'reduz o lucro de 2008', 'quadro de conciliação com e sem os efeitos, na própria nota',
  '-67.767 mil R$ no lucro de 2008 (8.870.636 -> 8.802.869)', 'subtração das duas linhas do quadro; a soma dos itens do quadro (-83.671 + 15.904) dá o mesmo valor', 'não declarado (apresentada como adequação à lei)')

BB10 = 'bb-dc-Demonstracoes-Contabeis-4T10.pdf'
q('banco-do-brasil', '2010-01-01', 'mudanca_de_regra',
  'até 2009 o lucro de BB-Banco Múltiplo e o de BB-Consolidado eram iguais (2009: R$ 10.147.522 mil nos dois, na edição 4T09)',
  'a partir da edição 4T10 as duas colunas divergem: 2010 múltiplo R$ 11.758.093 mil e consolidado R$ 11.703.165 mil; 2009 consolidado reapresentado = R$ 10.148.111 mil',
  'a fonte remete à nota 24.g (conciliação do patrimônio líquido do BB-Consolidado) e não explica o delta de 2009 no trecho lido',
  ['bb-dc-Demonstracoes-Contabeis-4T09.pdf', BB10],
  [T('bb-dc-Demonstracoes-Contabeis-4T09.pdf', 'layout', r'^\s*LUCRO L[IÍ]QUIDO(?=(?:\s+\d[\d.]*){6}\s*$)'),
   T(BB10, 'layout', r'^\s*LUCRO L[IÍ]QUIDO\s+\(Nota 24\.g\)')],
  'consolidado 2010 menor que o individual; consolidado 2009 maior em R$ 589 mil', 'subtração das colunas na própria DRE',
  '2010: consolidado - múltiplo = -54.928 mil R$; 2009: consolidado reapresentado - original = +589 mil R$',
  'diferença entre colunas da DRE 4T10 e entre a coluna 2009 da DRE 4T09 e a da DRE 4T10', 'não declarado')

# ---------------- ELETROBRAS
E9 = 'eletrobras-20f-2011-07-01-d20f.htm'
E8 = 'eletrobras-20f-2009-07-01-d20f.htm'
q('eletrobras', '2009 (20-F do exercício 2009, entregue em 2011-07-01 após pedido de prazo)', 'revisao_de_vintage',
  '20-F do exercício 2008 (US GAAP, R$ mil): lucro 2008 = 8.567.447; 2007 = 655.130; 2006 = 1.026.275; 2005 = 1.221.872',
  '20-F do exercício 2009 (US GAAP "restated"): 2008 = 8.001.925; 2007 = 707.377; 2006 = 337.390; 2005 = 944.788',
  'a empresa concluiu que certos itens deviam ter sido contabilizados de forma diferente nas demonstrações de 2008 e 2007 (tratamento de investimentos em coligadas, contratos de arrendamento, juros capitalizados no imobilizado e outras receitas operacionais de coligadas não consolidadas)',
  [E9, E8],
  [T(E9, 'html', r'we concluded that certain line items should properly have been accounted for differently', fmt='us'),
   T(E9, 'html', r'^\(1\) \| Restatement relates to changes in treatment of certain investments', fmt='us'),
   T(E8, 'html', r'^Net income for the year(?= \|)', fmt='us'),
   T(E9, 'html', r'^Net income \(loss\) for the year(?= \|)', fmt='us')],
  'mistos: 2008 -565.522; 2007 +52.247; 2006 -688.885; 2005 -277.084 (R$ mil)', 'subtração ano a ano entre as duas edições',
  '2008: 8.567.447 -> 8.001.925; 2007: 655.130 -> 707.377; 2006: 1.026.275 -> 337.390; 2005: 1.221.872 -> 944.788 (R$ mil)',
  'comparação das linhas "Net income for the year" dos dois 20-F', 'não: apresentada como correção de tratamento contábil')

E10 = 'eletrobras-20f-2011-10-17-d212707d20f.htm'
q('eletrobras', '2010-01-01 (primeiro exercício em IFRS)', 'mudanca_de_regra',
  'US GAAP: lucro 2009 = -R$ 1.538.558 mil (20-F do exercício 2009, reapresentado)',
  'IFRS: lucro 2009 = R$ 1.250.140 mil (20-F do exercício 2010)',
  'estas são as primeiras demonstrações da Eletrobras em IFRS; até 31/12/2009 eram em US GAAP e a administração alterou métodos contábeis, de avaliação e de consolidação para cumprir o IFRS; o comparativo de 2009 foi reapresentado',
  [E10, E9],
  [T(E10, 'html', r'These consolidated financial statements are the first Eletrobras financial statements to be prepared in compliance with IFRS', junta=4, fmt='us'),
   T(E10, 'html', r'^Net income of the year(?= \|)', fmt='us'),
   T(E9, 'html', r'^Net income \(loss\) for the year(?= \|)', fmt='us')],
  'aumenta o lucro de 2009 (de prejuízo para lucro)', 'subtração das duas linhas, mesmo exercício', '+R$ 2.788.698 mil (-1.538.558 -> 1.250.140)',
  'diferença entre as linhas do 20-F do exercício 2009 e do exercício 2010', 'não declarado (apresentada como exigência de adoção do IFRS)')

q('eletrobras', '2008-01-01 (exercício 2008)', 'mudanca_de_regra',
  'BR GAAP antes da Lei 11.638/2007', 'BR GAAP com a Lei 11.638/2007 (reconhecimento de provisão para redução ao valor recuperável, impairment, nas investidas)',
  'o Relatório da Administração atribui R$ 650 milhões de provisão de impairment à adoção da Lei 11.638/2007',
  ['eletrobras-rda-2008.pdf'],
  [T('eletrobras-rda-2008.pdf', 'layout', r'R\$ 650 milh.es decorrente da ado..o da Lei 11\.638/2007')],
  'reduz o resultado de equivalência patrimonial de 2008', 'o texto diz que o impairment foi "decorrente da adoção da Lei"',
  'R$ 650 milhões de impairment no resultado de equivalência (efeito líquido no lucro não isolado pela fonte)', 'texto do Relatório da Administração 2008', 'não declarado')

q('eletrobras', '2006 (edição 2006 do Relatório da Administração)', 'mudanca_de_unidade',
  'edições 2004 e 2005: lucro em R$ mil (2005: 974.589)', 'edição 2006: lucro em R$ milhões arredondados (2005: 975; 2006: 1.161)',
  'a fonte não declara', ['eletrobras-rda-2005.pdf', 'eletrobras-rda-2006.pdf'],
  [T('eletrobras-rda-2005.pdf', 'layout', r'^\s*Exerc[ií]cio(?=\s+1\.100\.340)'), T('eletrobras-rda-2006.pdf', 'layout', r'^\s*Lucro L[ií]quido do Exerc[ií]cio(?=\s+1\.100)')],
  'indeterminada (arredondamento)', 'comparação do mesmo ano nas duas edições', 'até R$ 0,4 milhão por ano por arredondamento', 'diferença entre 974.589 mil e 975 milhões', 'não')

# ---------------- CAIXA
C8 = 'caixa-df-2008-portugues.pdf'
q('caixa', '2007 (exercício 2007 reapresentado na edição 2008)', 'revisao_de_vintage',
  'lucro líquido de 2007 publicado em 2008: R$ 2.510.098 mil (Relatório da Administração 4T07: R$ 2.510 milhões)',
  'lucro líquido de 2007 ajustado na Nota 2 das demonstrações de 2008: R$ 2.392.454 mil',
  'a Nota 2 lista os ajustes: (i) contabilização das despesas correntes de 2007 das obrigações da patrocinadora com o Plano Saúde CAIXA; (ii) reversão de provisão relacionada à realização de créditos tributários de IR e CSLL (diferenças temporárias)',
  [C8, 'caixa-rda-2007-4T07.pdf'],
  [T(C8, 'layout', r'Lucro l[ií]quido do exerc[ií]cio(?=\s+2\.510\.098)'),
   T(C8, 'layout', r'\(i\)[\s\x07]+Contabiliza\S*o das despesas correntes do exerc\S*cio de 2007'),
   T(C8, 'layout', r'\(ii\)[\s\x07]+Revers\S*o de provis\S*o relacionada'),
   T('caixa-rda-2007-4T07.pdf', 'ocr', r'O lucro l.quido no exerc.cio de 2007 foi de R\$', junta=1)],
  'reduz o lucro de 2007', 'coluna "Ajustes" negativa na própria nota', '-117.644 mil R$ (2.510.098 -> 2.392.454)',
  'coluna "Ajustes" da Nota 2 (Original / Ajustes / Ajustado)', 'não: correção/ajuste')

q('caixa', '2010-01-01', 'mudanca_de_regra',
  'demonstração do resultado da CAIXA sem coluna consolidada (dez/2009: lucro R$ 2.999.706 mil)',
  'demonstração do resultado consolidada (dez/2010; 2009 comparativo = R$ 3.000.298 mil)',
  'a fonte não declara no trecho lido', ['caixa-dre-2009.pdf', 'caixa-dre-2010.pdf'],
  [T('caixa-dre-2009.pdf', 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO TRIMESTRE/EXERC[IÍ]CIO'), T('caixa-dre-2010.pdf', 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO PER[IÍ]ODO')],
  'aumenta o lucro de 2009 em R$ 592 mil', 'subtração das duas linhas', '+592 mil R$ (2.999.706 -> 3.000.298)', 'comparação das duas edições; perímetro e razão do delta não declarados', 'não declarado')

DC13 = 'caixa-dc-brgaap-2013.pdf'
q('caixa', '2013 (exercício 2012 reapresentado na edição 2013)', 'revisao_de_vintage',
  'lucro 2012 publicado em 2013 (DC dez/2012): R$ 6.066.054 mil nas duas colunas', 'lucro 2012 reapresentado (DC dez/2013, Nota 3(t)): R$ 5.639.608 mil',
  'Nota 3(t): mudança de prática contábil de benefícios a empregados (CPC 33 R1) e de contas de depósito encerradas por inconformidades cadastrais (orientação do Banco Central em nov/2013, aplicada retroativamente via CPC 23); a nota diz que os efeitos foram reconhecidos no patrimônio líquido e que a DRE do CPC 33 não é reapresentada, mas a linha de lucro de 2012 difere entre as edições (causa do delta não explicitada)',
  ['caixa-dc-brgaap-2012.pdf', DC13],
  [T('caixa-dc-brgaap-2012.pdf', 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO PER[IÍ]ODO(?=\s+\d)'), T(DC13, 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO PER[IÍ]ODO(?=\s+\d)'),
   T(DC13, 'layout', r'Mudan.a de pr.tica cont.bil . Contas Encerradas por Inconformidades Cadastrais')],
  'reduz o lucro de 2012', 'subtração das duas edições', '-426.446 mil R$ (6.066.054 -> 5.639.608), individual e consolidado', 'diferença entre a coluna 2012 da DC dez/2012 e a da DC dez/2013', 'não: correção/mudança de prática')

C16 = 'caixa-brgaap-2016T4-BrGaap-Demonstracoes-Contabeis-4T16-editavel.pdf'
q('caixa', '2016 (exercício 2015 reapresentado na edição 2016)', 'revisao_de_vintage',
  'lucro consolidado 2015 publicado em 2016 (DC dez/2015): R$ 7.156.354 mil', 'lucro 2015 reapresentado (DC dez/2016, Nota 3(t)): consolidado R$ 7.111.714 mil; individual R$ 5.797.026 mil',
  'Nota 3(t): reclassificação de instrumentos híbridos de capital e dívida, segregação das provisões para contingências judiciais, e depósitos em poupança simplificada (atualização monetária 2006-2016) em atendimento à Circular BACEN 3.763/15, com retificação de erro nos termos do CPC 23',
  ['caixa-dc-brgaap-2015.pdf', C16],
  [T('caixa-dc-brgaap-2015.pdf', 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO SEMESTRE / EXERC[IÍ]CIO(?=\s+\d)'), T(C16, 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO SEMESTRE / EXERC[IÍ]CIO(?=\s+\d)'),
   T(C16, 'layout', r'^\(iii\)\s+Dep.sitos em contas de poupan.a simplificada', junta=2)],
  'reduz o lucro consolidado de 2015', 'subtração das duas edições (consolidado)', 'consolidado: -44.640 mil R$ (7.156.354 -> 7.111.714); individual 2015 só existe na edição 2016 (5.797.026)',
  'diferença entre a DC dez/2015 (consolidada) e a coluna consolidada 2015 da DC dez/2016', 'não: correção')

C18 = 'caixa-brgaap-2018T4-BrGaap-Demonstracoes-Contabeis-editavel.pdf'
q('caixa', '2018 (exercício 2017 reapresentado na edição 2018)', 'revisao_de_vintage',
  'lucro 2017 publicado em 2018 (DC dez/2017): individual R$ 12.461.461 mil; consolidado R$ 12.516.121 mil', 'lucro 2017 reapresentado (DC dez/2018, Nota 3(n)): individual R$ 12.433.401 mil; consolidado R$ 12.488.061 mil',
  'Nota 3(n): (n.1) FGTS: a rentabilidade mínima garantida ao Fundo passa a ser tratada como instrumento financeiro derivativo (de Resolução CMN 4.512/16 para Circular BACEN 3.082/02); (n.2) ajustes na baixa e amortização de intangível de software; aplicados retrospectivamente (CPC 23)',
  ['caixa-brgaap-2017T4-DC-BrGaap-2017.pdf', C18],
  [T('caixa-brgaap-2017T4-DC-BrGaap-2017.pdf', 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO PER[IÍ]ODO(?=\s+\d)'), T(C18, 'layout', r'^\s*LUCRO L[IÍ]QUIDO DO PER[IÍ]ODO(?=\s+\d)'),
   T(C18, 'layout', r'Essa revis.o culminou na altera..o de procedimentos cont.beis referentes . rentabilidade m.nima', junta=2)],
  'reduz o lucro de 2017', 'subtração das duas edições', '-28.060 mil R$ no individual e no consolidado', 'diferença entre colunas 2017 das DC dez/2017 e dez/2018', 'não: correção')

I17 = 'caixa-ifrs-2017T4-IFRS-Demonstracoes-Contabeis-2017.pdf'
I18 = 'caixa-ifrs-2018T4-IFRS-Demonstracoes-Contabeis-2018.pdf'
q('caixa', '2018-01-01 (adoção do IFRS 9 nas demonstrações IFRS)', 'mudanca_de_regra',
  'IAS 39: lucro IFRS consolidado 2017 = R$ 20.251.123 mil (edição 2017); reapresentado como R$ 18.981.081 mil na coluna "IAS 39" da edição 2018',
  'IFRS 9: lucro IFRS 2017 recalculado = R$ 6.253.150 mil (coluna "IFRS 9" da edição 2018); lucro IFRS 2018 = R$ 8.436.220 mil',
  'a edição 2018 apresenta duas colunas para 2017, "IFRS 9" e "IAS 39 (Nota 2(u))"; o cabeçalho remete à Nota 2(u) e a perdas esperadas calculadas com o IFRS 9',
  [I17, I18],
  [T(I17, 'raw', r'^LUCRO L.QUIDO DO EXERC.CIO(?=\s+[\d(])'), T(I18, 'raw', r'^RESULTADO L.QUIDO DO EXERC.CIO(?=\s+[\d(])'), T(I18, 'raw', r'^IAS 39$')],
  'reduz fortemente o lucro IFRS de 2017 na coluna IFRS 9', 'subtração das colunas', '2017: -R$ 13.997.973 mil (20.251.123 -> 6.253.150, coluna IFRS 9); -R$ 1.270.042 mil (20.251.123 -> 18.981.081, coluna IAS 39)',
  'comparação da edição IFRS 2017 com as duas colunas de 2017 da edição IFRS 2018', 'não declarado (apresentada como adoção de norma)')

C21 = 'caixa-brgaap-2021T4-BrGaap-Demonstracoes-Contabeis.pdf'
q('caixa', '2021 (exercício 2021)', 'mudanca_de_regra',
  'até 2020 as linhas consolidadas de lucro não separavam participação de não controladores (2020: R$ 13.169.364 mil em todas)',
  'a partir da edição 2021 a DRE separa "lucro líquido atribuível ao controlador" (2021: R$ 17.017.896 mil) de "lucro líquido total" (R$ 17.268.262 mil); a linha "lucro líquido do período" da edição 2022 mistura as duas bases (2022 = atribuível, 2021 = total)',
  'a fonte não declara a razão no trecho lido', [C21],
  [T(C21, 'raw', r'^LUCRO L.QUIDO ATRIBU.VEL AO CONTROLADOR(?=\s+\d)'), T(C21, 'raw', r'^LUCRO L.QUIDO TOTAL(?=\s+\d)')],
  'o total é maior que o atribuível', 'subtração das duas linhas', '2021: total - atribuível = +250.366 mil R$', 'diferença entre as linhas da DRE 2021', 'não declarado')

# ---------------- CORREIOS
D6, D7 = 'correios-df-2006.pdf', 'correios-df-2007.pdf'
q('correios', '2006/2007 (edição 2007)', 'mudanca_de_regra',
  'edição 2006: "Lucro líquido do exercício" = R$ 328.585.114,31, e a reversão de juros sobre capital próprio (R$ 198.321.281,93) vinha depois, em "Resultado do exercício" = R$ 526.906.396,24',
  'edição 2007: a reversão de JCP entra antes da linha "Lucro líquido do exercício"; 2006 reapresentado = R$ 526.906.396,24 e 2007 = R$ 829.235.017,87',
  'a fonte não declara a razão do reposicionamento da linha', [D6, D7],
  [T(D6, 'layout', r'^\s*LUCRO L.QUIDO DO EXERC.CIO(?=\s+\d)'), T(D6, 'layout', r'^\s*RESULTADO DO EXERC.CIO(?=\s+\d)'), T(D7, 'layout', r'^\s*REVERS.O DOS JUROS S/CAPITAL PR.PRIO')],
  'aumenta a linha "lucro líquido" de 2006', 'soma da linha de reversão de JCP ao lucro da edição 2006', '+R$ 198.321.281,93 em 2006 (328.585.114,31 -> 526.906.396,24)',
  'diferença entre "Lucro líquido do exercício" da edição 2006 e o da edição 2007 para 2006', 'não')

q('correios', '2008 e 2011 (edições 2008, 2010 e 2011)', 'mudanca_de_unidade',
  'edições até 2007: reais com centavos (2007 = 829.235.017,87)', 'edição 2008: R$ milhões com 1 decimal (2008 = 801,1); edição 2009: R$ milhões (2009 = 117,55 na DFC); edição 2010: reais com centavos (2010 = 826.947.319,57); edição 2011: R$ mil (2011 = 882.747)',
  'a fonte não declara', ['correios-df-2007.pdf', 'correios-df-2008.pdf', 'correios-df-2011.pdf'],
  [T('correios-df-2008.pdf', 'layout', r'^\s*LUCRO L.QUIDO DO EXERC.CIO(?=\s+\d)'), T('correios-df-2011.pdf', 'ocr', r'DEMONSTRA..O DO RESULTADO DOS EXERC.CIOS FINDOS EM 31 DE DEZEMBRO \(em milhares')],
  'indeterminada (arredondamento)', 'a mesma série muda de unidade entre edições', 'perda de precisão: 801,1 milhões vs reais com centavos', 'comparação das unidades declaradas', 'não')

D10 = 'correios-df-2010.pdf'
q('correios', '2008-01-01 e 2010 (Leis 11.638/2007 e 11.941/2009; CPCs)', 'mudanca_de_regra',
  'prática contábil anterior à Lei 11.638/2007', 'práticas da Lei 11.638/2007 e da Lei 11.941/2009 com pronunciamentos do CPC (custo atribuído, vida útil econômica, etc. a partir de 2014 para imobilizado)',
  'convergência da contabilidade brasileira às práticas internacionais (texto da Nota 2.1 de 2010)', [D10],
  [T(D10, 'ocr', r'2\.1 . Ado..o da Lei n. 11\.638/2007 e da Lei 11\.941/2009', junta=2)],
  'indeterminada', 'a fonte não mede o efeito', 'não medido', 'não medido', 'sim (convergência às normas internacionais)')

D11 = 'correios-df-2011.pdf'
q('correios', '2011 (exercício 2010 reapresentado)', 'revisao_de_vintage',
  'lucro 2010 publicado em 2011: R$ 826.947 mil', 'lucro 2010 reapresentado: R$ 818.966 mil',
  'recálculo de PIS/COFINS de jan/2007 a dez/2010 (regime misto de tributação) e de IRPJ/CSLL do mesmo período (provisões indedutíveis, incentivo fiscal cultural), com ajustes em receitas canceladas e encargos financeiros',
  [D11, D10],
  [T(D11, 'ocr', r'^Resultado do Per.odo 826\.947'), T(D11, 'ocr', r'^\(1\) Valores adv.ndos do rec.lculo de PIS/COFINS', junta=2)],
  'reduz o lucro de 2010', 'coluna "Ajustes" negativa na tabela da nota', '-7.981 mil R$ (826.947 -> 818.966)', 'tabela de reapresentação da nota (Publicado / Ajustes / Reapresentado)', 'não: correção')

D13, D14, D15 = 'correios-df-2013.pdf', 'correios-df-2014.pdf', 'correios-df-2015.pdf'
q('correios', '2013 (exercício 2012 reapresentado na edição 2013)', 'revisao_de_vintage',
  'lucro 2012 publicado em 2013: R$ 1.044.061 mil', 'lucro 2012 reapresentado: R$ 1.113.287 mil',
  'apresentação retrospectiva nos termos do CPC 23 "em decorrência de ajustes nas demonstrações contábeis"', ['correios-df-2012.pdf', D13],
  [T('correios-df-2012.pdf', 'ocr', r'^Lucro L.quido do Per.odo(?=\s+\d)'), T(D13, 'ocr', r'^Lucro L.quido do Per.odo(?=\s+\d)'),
   T(D13, 'ocr', r'As informa..es est.o sendo apresentadas de forma retrospectiva conforme Pronunciamento', junta=2)],
  'aumenta o lucro de 2012', 'subtração das duas edições', '+69.226 mil R$ (1.044.061 -> 1.113.287)', 'diferença entre colunas 2012 das DF 2012 e 2013 (OCR)', 'não: correção')

q('correios', '2014 (exercício 2013 reapresentado na edição 2014)', 'revisao_de_vintage',
  'lucro 2013 publicado em 2014: R$ +325.278 mil', 'lucro 2013 reapresentado: prejuízo de R$ 312.511 mil',
  'Nota 4 (apresentação retrospectiva): benefício pós-emprego, obrigação atuarial de saúde (R$ 868.071 mil), ajustes de critério de provisão de despesas médicas e reclassificações',
  [D13, D14],
  [T(D13, 'ocr', r'^Lucro L.quido do Per.odo(?=\s+\d)'), T(D14, 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'),
   T(D14, 'layout', r'Obriga..o atuarial - Sa.de')],
  'reduz o lucro de 2013 (inverte o sinal)', 'subtração das duas edições', '-637.789 mil R$ (+325.278 -> -312.511)', 'diferença entre a coluna 2013 da DF 2013 (OCR) e a coluna 2013 reapresentada da DF 2014 (texto)', 'não: correção')

q('correios', '2015 (exercício 2014 reapresentado na edição 2015)', 'revisao_de_vintage',
  'lucro 2014 publicado em 2015: R$ +9.913 mil', 'lucro 2014 reapresentado: prejuízo de R$ 20.309 mil',
  'Nota 3.3: provisão de contingências cíveis e trabalhistas/precatórios de R$ 30.222 mil nas despesas gerais e administrativas; a fonte diz que o lucro de 2014 "passa ao status de prejuízo contábil"',
  [D14, D15],
  [T(D14, 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'), T(D15, 'ocr', r'^RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'),
   T(D15, 'ocr', r'Apesar da reapresenta..o do lucro de 2014', junta=1)],
  'reduz o lucro de 2014 (inverte o sinal)', 'a própria nota afirma que o lucro passou a prejuízo', '-30.222 mil R$ (9.913 -> -20.309)', 'diferença entre colunas 2014 das DF 2014 e 2015; igual ao ajuste de despesas da Nota 3.3', 'não: correção')

D22, D23, D24, D25 = 'correios-df-2022.pdf', 'correios-df-2023.pdf', 'correios-df-2024.pdf', 'correios-df-2025.pdf'
q('correios', '2023 (exercício 2022 reapresentado na edição 2023)', 'revisao_de_vintage',
  'prejuízo 2022 publicado em 2023: R$ 808.781 mil (colunas 2021 e 2020 "reclassificado")', 'prejuízo 2022 reapresentado: R$ 767.580 mil',
  'Nota 4: "garantir maior aderência às informações divulgadas nas demonstrações contábeis" (reapresentação e reclassificação)', [D22, D23],
  [T(D22, 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'), T(D23, 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'),
   T(D23, 'layout', r'Com o objetivo de garantir maior ader.ncia', junta=2)],
  'reduz o prejuízo de 2022', 'subtração das duas edições', '+41.201 mil R$ (-808.781 -> -767.580)', 'diferença entre as colunas 2022 das DF 2022 e 2023', 'não declarado')

q('correios', '2024 (exercício 2023 reapresentado na edição 2024)', 'revisao_de_vintage',
  'prejuízo 2023 publicado em 2024: R$ 596.625 mil', 'prejuízo 2023 reapresentado: R$ 633.509 mil',
  'Nota 4: "assegurar a conformidade e a precisão das informações apresentadas" (reapresentação e reclassificação)', [D23, D24],
  [T(D23, 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'), T(D24, 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'),
   T(D24, 'layout', r'Com o objetivo de assegurar a conformidade e a precis.o', junta=2)],
  'aumenta o prejuízo de 2023', 'subtração das duas edições', '-36.884 mil R$ (-596.625 -> -633.509)', 'diferença entre as colunas 2023 das DF 2023 e 2024', 'não declarado')

q('correios', '2025 (exercício 2024 reapresentado na edição 2025)', 'revisao_de_vintage',
  'prejuízo 2024 publicado em 2025: R$ 2.591.248 mil', 'prejuízo 2024 reapresentado: R$ 2.447.229 mil',
  'revisão das estimativas das contingências trabalhistas (cumulatividade do Adicional de Atividade de Distribuição e/ou Coleta Externa e do Adicional de Periculosidade), por recomendação da Controladoria-Geral da União; a fonte diz que "não configura mudança de políticas contábeis"',
  [D24, D25],
  [T(D24, 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'), T(D25, 'layout', r'^\s*RESULTADO L.QUIDO DO PER.ODO(?=\s+[\d(])'),
   T(D25, 'layout', r'Em 2025, a Empresa reapresentou as demonstra..es cont.beis', junta=3)],
  'reduz o prejuízo de 2024', 'subtração das duas edições; a tabela da Nota 4 mostra ajuste trabalhista (144.019) em 31/12/2024', '+144.019 mil R$ (-2.591.248 -> -2.447.229)',
  'diferença entre as colunas 2024 das DF 2024 e 2025; igual ao ajuste trabalhista da tabela', 'não: apresentada como revisão de estimativa por recomendação de órgão de controle')


COLS = ['indicador', 'serie', 'data_quebra', 'tipo_de_quebra', 'metodo_antigo', 'metodo_novo', 'razao_declarada_pela_fonte',
        'fonte_primaria_url', 'trecho_citado', 'direcao_do_efeito', 'como_a_direcao_foi_determinada', 'efeito_medido',
        'como_medido', 'apresentada_como_aprimoramento']
TIPOS = {'metodo_estatistico', 'mudanca_de_regra', 'revisao_de_vintage', 'mudanca_de_unidade'}
assert all(r['tipo_de_quebra'] in TIPOS for r in Q)
with open(L.BASE + '/quebras.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLS, lineterminator='\n')
    w.writeheader(); w.writerows(Q)
print(len(Q), 'quebras')
