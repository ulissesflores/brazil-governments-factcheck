"""Plain-language explanation of every series the terminal shows: what it is, how it is computed, why it matters, what to watch.

Every text is tied to a published definition or to an arithmetic rule declared in the pre-registration
and its amendments; nothing here attributes causes to governments. The page prints the four blocks under
the chart of each series.
"""

EXPLICA = {
    "carga_base": {
        "o_que": "Carga tributária bruta dividida pelas seis bases de incidência da Receita Federal (renda, folha de salários, propriedade, bens e serviços, transações financeiras e outros), em % do PIB, pela tabela INC02B da edição 2024 do relatório 'Carga Tributária no Brasil'.",
        "como": "Uma edição só (2024), que cobre 2002 a 2024, para que todos os anos sigam a mesma classificação; as edições anteriores revisam os anos passados e estão registradas como quebras. Os seis agregados somam o total mostrado em 'Carga tributária bruta'.",
        "porque": "Diz de onde vem o imposto: o Brasil tributa bens e serviços (consumo) muito mais que renda e propriedade, o traço regressivo mais citado do sistema. Em 2024 bens e serviços pesam cerca de metade da carga; renda, cerca de um quarto; propriedade, menos de 5% do total.",
        "cuidado": "A classificação é a da Receita (um tributo pode ser reclassificado entre edições); a edição 2024 traz valores que podem diferir dos publicados à época. Não diz quem paga de fato (incidência econômica), só sobre qual base o tributo é cobrado.",
    },
    "lucro_petrobras": {
        "o_que": "Lucro ou prejuízo líquido anual da Petrobras, em R$ milhões correntes, lido nas demonstrações contábeis da própria empresa (1997-2009), uma linha por norma contábil e perímetro (consolidado em BR GAAP, controladora, IFRS a partir de 2008).",
        "como": "Cada linha é uma norma contábil; nenhuma é emendada a outra. Valores nominais, convertidos só de unidade (R$ mil para R$ milhões). A linha em US$ (US GAAP do formulário 20-F) fica fora por ser outra moeda.",
        "porque": "O resultado da maior estatal é parte do que o Tesouro recebe em dividendos e do que o país discute sobre preços de combustíveis. De 1997 a 2009 o lucro consolidado em BR GAAP foi de cerca de R$ 1,4 bi (1998) a R$ 33 bi (2008).",
        "cuidado": "Valores nominais: R$ 10 bi em 2000 não são R$ 10 bi em 2009. A série da coleta termina em 2009; os anos seguintes não foram coletados. Normas diferentes dão lucros diferentes para o mesmo ano (BR GAAP e IFRS em 2008-2009 divergem), e isso é mostrado, não corrigido.",
    },
    "lucro_bb": {
        "o_que": "Lucro líquido anual do Banco do Brasil, em R$ milhões correntes, lido nos relatórios anuais e demonstrações da própria empresa (1995-2009), uma linha por fonte dentro das demonstrações (quadro de indicadores, DRE consolidada, DRE do banco múltiplo).",
        "como": "Cada linha é uma origem dentro das demonstrações; nenhuma é emendada. Valores nominais, convertidos só de unidade.",
        "porque": "O BB é o maior banco público e o seu resultado alimenta os dividendos da União. O quadro de indicadores vai de um prejuízo em 1995-1996 (saneamento de 1996) a lucros acima de R$ 8 bi em 2008-2009.",
        "cuidado": "Valores nominais e normas da época. A coleta termina em 2009. Lucro de banco depende de provisões e de normas do Banco Central que mudam; a comparação entre anos distantes é frágil.",
    },
    "lucro_caixa": {
        "o_que": "Lucro ou prejuízo líquido anual da Caixa Econômica Federal, em R$ milhões correntes, lido nas demonstrações da própria empresa (2001-2025), uma linha por norma e perímetro (individual e consolidado em BR GAAP; consolidado em IFRS).",
        "como": "Cada linha é uma norma e um perímetro; nenhuma é emendada. Valores nominais, convertidos só de unidade.",
        "porque": "A Caixa concentra o crédito habitacional e as transferências sociais do país. Em 2001 registrou prejuízo de R$ 4,7 bi (reestruturação do PROEF); nos anos 2010 e 2020 os lucros chegaram a dezenas de bilhões.",
        "cuidado": "Valores nominais ao longo de 25 anos; o lucro consolidado inclui participações (Caixa Seguridade), o individual não. Normas mudam em 2010 (IFRS) e as demonstrações trazem reapresentações de anos anteriores.",
    },
    "lucro_eletrobras": {
        "o_que": "Lucro ou prejuízo líquido anual da Eletrobras, em R$ milhões correntes, lido nas demonstrações da própria empresa (2000-2009), uma linha por norma (BR GAAP consolidado; US GAAP em reais do formulário 20-F; IFRS a partir de 2010).",
        "como": "Cada linha é uma norma; nenhuma é emendada. Valores nominais, convertidos só de unidade.",
        "porque": "A Eletrobras era a maior estatal do setor elétrico até a desestatização de 2022; o seu resultado dependia de tarifas, câmbio (dívida em dólar) e da remuneração das usinas. Os lucros oscilaram entre cerca de R$ 1 bi e R$ 6 bi nos anos 2000.",
        "cuidado": "Valores nominais; a coleta termina em 2009. BR GAAP e US GAAP em reais podem divergir bastante no mesmo ano por tratamento de câmbio e provisões.",
    },
    "lucro_correios": {
        "o_que": "Lucro ou prejuízo líquido anual dos Correios (ECT), em R$ milhões correntes, lido nas demonstrações da própria empresa (2000-2025), uma linha por perímetro (individual e consolidado).",
        "como": "Cada linha é um perímetro; nenhuma é emendada. Valores nominais, convertidos só de unidade (R$, R$ mil e R$ milhões para R$ milhões).",
        "porque": "Os Correios são a estatal de serviço universal com mais empregados; o seu resultado virou do lucro nos anos 2000 para prejuízos em 2013-2016 e de novo em 2022-2024, o que pesa no debate sobre privatização e sobre aportes do Tesouro.",
        "cuidado": "Valores nominais ao longo de 25 anos; o plano de saúde dos empregados (Postal Saúde) e provisões atuariais explicam parte dos prejuízos recentes e aparecem só nas notas explicativas, não nesta série.",
    },
    "emendas_pagas": {
        "o_que": "Valor pago de emendas parlamentares ao orçamento da União, por tipo (individuais com finalidade definida, individuais por transferência especial, de bancada estadual, de comissão e de relator-geral), em R$ bilhões correntes, no exercício da própria emenda. Fonte: Portal da Transparência (CGU), base completa de emendas, lida do arquivo hasheado.",
        "como": "Soma da coluna 'Valor Pago' por ano orçamentário e tipo, como a CGU classifica. O que foi inscrito em restos a pagar e pago em anos seguintes entra em 'Emendas pagas / PIB'. A base começa em 2014; o ano corrente está incompleto.",
        "porque": "As emendas são a parte do orçamento que o Congresso decide diretamente; o salto das emendas de relator em 2020-2022 e das transferências especiais e de comissão em 2024-2025 muda quem controla o gasto discricionário. O total pago no exercício foi de cerca de R$ 6 bi em 2019 para R$ 31 bi em 2024 e R$ 32 bi em 2025.",
        "cuidado": "Valores nominais em reais correntes. 'Pago no exercício' subestima o que cada emenda acabou pagando, porque parte vai para restos a pagar. A regra de cada tipo mudou por emenda constitucional (EC 86/2015, 100/2019, 105/2019, 126/2022, LC 210/2024): a tabela de regras está na coleta.",
    },
    "emendas_pib": {
        "o_que": "Emendas parlamentares pagas, todos os tipos, em % do PIB: numerador do Portal da Transparência (CGU), denominador o PIB nominal que o Tesouro usa no Resultado do Tesouro Nacional. Duas linhas: só o pago no exercício da emenda, e o pago no exercício mais os restos a pagar pagos depois, atribuídos ao ano da emenda.",
        "como": "Razão anual entre duas fontes declaradas, sem encadeamento. A linha com restos a pagar atribui ao ano da emenda o que foi pago depois, por isso os anos recentes ainda vão crescer.",
        "porque": "Em % do PIB a comparação entre anos não é distorcida pela inflação: o pago no exercício passou de cerca de 0,1% do PIB em 2019 para cerca de 0,3% em 2024.",
        "cuidado": "O ano corrente está incompleto nas duas linhas. O PIB do Tesouro é revisado; a CGU reclassifica tipos quando a regra muda. Não inclui emendas de 2014-2015 pagas por outros mecanismos antes da execução obrigatória (EC 86/2015).",
    },
    "nominal": {
        "o_que": "Resultado nominal do setor público consolidado (governo federal, Banco Central, estados, municípios e estatais, exceto Petrobras e Eletrobras), acumulado em 12 meses, em % do PIB. É o resultado primário menos os juros nominais da dívida. Fonte: Banco Central do Brasil (BCB), Necessidades de Financiamento do Setor Público (NFSP), série SGS 5727.",
        "como": "O BCB publica a NFSP com sinal positivo quando há déficit; aqui o sinal é invertido para que positivo signifique superávit, a mesma convenção do indicador 'Resultado primário'. Série mensal desde novembro de 2002, uma base única, sem encadeamento.",
        "porque": "É o número que diz se a dívida pública cresce ou encolhe pelo próprio orçamento: déficit nominal é dívida nova. O déficit foi de 5,2% do PIB em dez/2003, 2,4% em dez/2010, 10,2% em dez/2015, 5,8% em dez/2019 e 9,5% em ago/2026.",
        "cuidado": "O resultado nominal soma dois movimentos de natureza distinta, o esforço fiscal (primário) e o custo da dívida (juros), que a página mostra separados. Em 2015 e 2020-2021 a conta inclui efeitos de swaps cambiais do BCB, que o BCB classifica como juros.",
    },
    "juros_nominais": {
        "o_que": "Juros nominais apropriados sobre a dívida do setor público consolidado, acumulados em 12 meses, em % do PIB. Fonte: BCB, NFSP, série SGS 5760.",
        "como": "Fluxo de 12 meses dividido pelo PIB dos mesmos 12 meses, como o BCB publica. Série mensal desde novembro de 2002, base única.",
        "porque": "É o custo de carregar a dívida: quanto maior a taxa Selic e o estoque indexado a ela, maior a conta. Os juros foram 8,4% do PIB em dez/2003, 5,0% em dez/2010, 8,4% em dez/2015, 5,0% em dez/2019 e 8,9% em ago/2026.",
        "cuidado": "Juros nominais incluem a parte que só repõe a inflação; em anos de inflação alta a conta real é menor que a nominal. O resultado dos swaps cambiais do BCB entra aqui e pode inflar ou deflacionar o número em anos de câmbio volátil (2015, 2020).",
    },
    "divext": {
        "o_que": "Estoque de dívida externa bruta do Brasil, em US$ milhões, posição de fim de trimestre, nos dois conceitos que o BCB publica. Restrito (SGS 3684, desde 1972): empréstimos, títulos emitidos no exterior e créditos comerciais de residentes com não residentes. BPM6 (SGS 25563, desde 2002): o restrito mais as operações intercompanhia (empréstimos entre matriz e filial) e os títulos negociados no mercado doméstico em poder de não residentes. A terceira linha é a dívida externa do setor público no conceito restrito (SGS 21521).",
        "como": "Cada linha é uma série do BCB publicada como está; nenhuma é somada a outra nem prolongada. O BCB chama o conceito BPM6 de 'a dívida externa brasileira' e o restrito de 'a chamada dívida externa bruta' (Nota Explicativa de 24/02/2026). A data trimestral do SGS marca o primeiro mês do trimestre; aqui o ponto é colocado no último mês.",
        "porque": "O Brasil sempre teve dívida externa bruta; o que mudou ao longo do tempo foi o tamanho dela diante das reservas e do PIB. No conceito restrito: US$ 210,7 bi em dez/2002, 256,9 bi em dez/2010, 326,3 bi em dez/2016, 319,6 bi em dez/2022, 386,1 bi em dez/2025 e 407,1 bi em jun/2026, o maior valor nominal da série. No conceito BPM6: 869,5 bi em jun/2026, dos quais 287,0 bi são intercompanhia e 175,4 bi títulos domésticos.",
        "cuidado": "Valores nominais em dólar não descontam a inflação do dólar nem o crescimento da economia: para tamanho relativo, veja 'Dívida externa bruta / PIB'. Cerca de três quartos da dívida restrita é do setor privado (bancos e empresas). A dívida em títulos é marcada a valor de mercado desde 2001, então o estoque oscila com juros e câmbio mesmo sem emissão nova.",
    },
    "divext_reservas": {
        "o_que": "Dívida externa bruta no conceito restrito (SGS 3684, trimestral) e reservas internacionais no conceito caixa (SGS 3546, mensal), ambas do BCB, em US$ milhões, no mesmo gráfico.",
        "como": "Duas séries do BCB desenhadas juntas, sem nenhuma operação entre elas. Quando a linha das reservas fica acima da da dívida, as reservas cobrem toda a dívida externa bruta restrita.",
        "porque": "É o cruzamento que a imprensa chamou em outubro de 2026 de 'Brasil volta a ser devedor': em jun/2026 a dívida restrita (407,1 bi) superou as reservas (cerca de 402 bi). As reservas cobriam 94,9% da dívida em dez/2025, 99,1% em set/2024 e mais de 100% entre 2007 e 2023, segundo a Tabela 31 do próprio BCB.",
        "cuidado": "Dívida menos reservas NÃO é a dívida externa líquida do BCB: o conceito oficial subtrai também os créditos brasileiros no exterior e os haveres de bancos comerciais no exterior (US$ 36,6 bi em dez/2025). Com eles, a dívida externa líquida era NEGATIVA (credora) em -17,2 bi em dez/2025, último valor oficial; o BCB descontinuou o indicador em fev/2026 e não há valor oficial de 2026 em nenhum conceito. Nada foi calculado aqui.",
    },
    "divext_pib": {
        "o_que": "Dívida externa bruta no conceito restrito dividida pelo PIB acumulado em 12 meses em dólares correntes, em %. Fonte: BCB, série SGS 11407 (1971T4 a 2025T3).",
        "como": "Razão publicada pelo BCB, mostrada como está. O BCB descontinuou a série em fevereiro de 2026 e explicou como recalculá-la (SGS 3684 sobre a soma de 12 meses da SGS 4192); esta página não a prolonga.",
        "porque": "É o tamanho da dívida externa diante da economia, a medida que a literatura usa para falar de vulnerabilidade externa. A razão foi 53,8% em 1984, 41,2% em 1999, 41,8% em 2002, 14,1% em 2007, 12,0% em 2010, 18,2% em 2016 e 17,3% em set/2025.",
        "cuidado": "O denominador é o PIB em dólares correntes: quando o real se desvaloriza, a razão sobe mesmo com a dívida parada. O numerador é o conceito restrito; com o conceito BPM6 (que inclui intercompanhia e títulos domésticos) a razão seria cerca do dobro.",
    },
    "divext_liquida_pib": {
        "o_que": "Dívida externa líquida sobre o PIB, em %, no conceito antigo do BCB: dívida externa bruta restrita menos reservas internacionais, créditos brasileiros no exterior e haveres de bancos comerciais no exterior. Negativo significa que o país é credor externo líquido. Fonte: BCB, série SGS 11409 (1971T4 a 2025T3).",
        "como": "Razão publicada pelo BCB, mostrada como está. O BCB descontinuou a série em fevereiro de 2026 porque a construção original não adere ao padrão BPM6/EDS 2013 e passou a remeter à Posição de Investimento Internacional por instrumento de dívida. Não há valor oficial de 2026 em nenhum conceito e nada foi calculado aqui.",
        "porque": "É a medida que separa 'ter dívida externa' de 'dever ao exterior em termos líquidos'. A razão foi 46,3% do PIB em 1984, 32,4% em 1999, 32,7% em 2002, -0,9% em 2007 (primeiro ano credor), -2,4% em 2010, -3,8% em 2016, -1,4% em 2022 e -0,9% em set/2025.",
        "cuidado": "O último valor oficial do nível é -17,2 bi em dez/2025 (estimativa do BCB na Nota de jan/2026). A manchete de outubro de 2026 usou 'bruta menos reservas', que ignora cerca de US$ 36 bi de ativos: por essa conta o Brasil 'voltou a ser devedor' em jun/2026 (+5,1 bi); pela definição do BCB não há como saber, porque o indicador deixou de existir.",
    },
    "divext_publico": {
        "o_que": "Parcela da dívida externa bruta restrita que pertence ao setor público (governo geral, Banco Central e entidades públicas), em %. Fonte: BCB, série SGS 11408 (1971T4 a 2025T3), razão entre SGS 21521 e SGS 3684.",
        "como": "Razão publicada pelo BCB, mostrada como está; descontinuada em fevereiro de 2026 e não prolongada.",
        "porque": "Diz de quem é a dívida: a do setor privado não é obrigação do Tesouro. A parcela pública foi 69,1% em 1984, 46,5% em 1999, 59,4% em 2002, 44,5% em 2007, 40,5% em 2010, 39,9% em 2016 e 36,4% em set/2025.",
        "cuidado": "O BCB revisou a divisão entre público e privado de dez/2020 a set/2025 na Nota de março de 2026. No conceito BPM6 (com títulos domésticos em poder de não residentes), a dívida externa do setor público é bem maior (US$ 384,2 bi em jun/2026 contra 143,8 bi no restrito), porque inclui os títulos do Tesouro em reais comprados por estrangeiros.",
    },
    "pii_pib": {
        "o_que": "Posição de investimento internacional líquida sobre o PIB, em %: tudo que residentes têm no exterior (reservas, investimento direto, ações, títulos, depósitos) menos tudo que não residentes têm no Brasil. Fonte: BCB, série SGS 12506 (2002T1 a 2025T3).",
        "como": "Razão publicada pelo BCB sobre o PIB de 12 meses em dólares, mostrada como está; descontinuada em fevereiro de 2026 e não prolongada.",
        "porque": "É a medida mais ampla da posição externa do país, a que o BCB passou a preferir à dívida externa líquida. A posição foi -45,4% do PIB em 2002, -39,2% em 2007, -41,1% em 2010, -32,4% em 2016, -42,2% em 2022 e -51,6% em set/2025.",
        "cuidado": "Inclui ações e investimento direto, que não são dívida e cujo valor oscila com a bolsa e o câmbio: uma queda da bolsa brasileira 'melhora' a posição sem que ninguém pague nada. Negativo é a regra em economias que recebem investimento direto; o sinal não diz se o passivo é sustentável.",
    },
    "inflacao": {
        "o_que": "Quanto os preços ao consumidor subiram nos últimos 12 meses. O IPCA (IBGE) é o índice oficial da meta de inflação; o INPC (IBGE) pesa a cesta das famílias de renda mais baixa; o IGP-DI (FGV) mistura atacado, consumidor e construção e existe desde 1945.",
        "como": "Taxa acumulada em 12 meses = produto das 12 variações mensais menos 1. O candle de um ano abre na taxa de dezembro do ano anterior, fecha na de dezembro, e o pavio vai da menor à maior taxa de 12 meses observada nos meses do ano. Verde = a inflação acelerou no ano; vermelho = desacelerou.",
        "porque": "É o imposto que ninguém vota: corrói salário, poupança e contrato. Antes de 1994 a taxa anual passou de 2.000%; depois do Real ficou entre 2% e 13%, e o Banco Central persegue uma meta (hoje 3% ao ano, com tolerância de 1,5 ponto).",
        "cuidado": "Na vista completa o eixo é simétrico de log (5.000% e 2% no mesmo gráfico). O IPCA começa em 1980; antes disso só o IGP-DI existe. As cestas do IPCA foram atualizadas em 1989, 1991, 1999, 2006, 2012 e 2020 (catálogo de quebras).",
    },
    "selic": {
        "o_que": "O juro básico da economia: a meta fixada pelo Copom (Banco Central) desde 1999 e, como linha, a taxa efetiva (over) desde 1974, anualizada.",
        "como": "Candle sobre a meta do Copom no fim de cada mês (BCB SGS 432): abre na meta de dezembro anterior, fecha na de dezembro, pavio entre a menor e a maior meta do ano. A over mensal anualizada ((1 + taxa do mês)^12 − 1) fica como linha; ela oscila até 1 ponto com o número de dias úteis do mês, por isso não leva candle. A faixa de baixo é o juro real do ano: Selic acumulada menos IPCA acumulado.",
        "porque": "É o preço do dinheiro: define o custo da dívida pública, do crédito e o rendimento de quem poupa. O Brasil tem um dos juros reais mais altos do mundo desde o Real.",
        "cuidado": "Sem leitura de melhor: juro alto segura a inflação e encarece a dívida; juro baixo faz o contrário. Antes de 1999 não há meta, só a over; antes de 1995 os valores anualizados passam de 1.000% e não têm leitura econômica.",
    },
    "emissao": {
        "o_que": "Quanto a base monetária (M0: papel-moeda emitido mais reservas dos bancos no Banco Central) cresceu em 12 meses, comparado com a inflação. M1 (dinheiro em poder do público mais depósitos à vista) aparece nas duas definições do Banco Central, antiga (até 2018) e nova (desde 2003).",
        "como": "Variação em 12 meses do saldo de M0 (BCB SGS 1788, uma base contínua desde 1946). Candle anual sobre essa taxa; faixa de baixo = crescimento de M0 menos IPCA em 12 meses (positivo = emitiu acima dos preços). Fev/2001 e fev/2002 estão suprimidos: a série do BCB traz em fev/2001 o valor de fev/2002 (erro de transcrição na fonte, catalogado).",
        "porque": "É a 'impressão de dinheiro' medida: quando a base cresce muito acima dos preços por anos seguidos, a inflação tende a seguir; em 2020 a base cresceu bem acima dos preços e em 2021-22 a inflação subiu.",
        "cuidado": "Correlação não é causa única: a demanda por moeda também muda (Pix, juros, pandemia). Verde = a base cresceu mais rápido que no ano anterior, o que não é 'melhor' nem 'pior' por si.",
    },
    "multiplicador": {
        "o_que": "Quantos reais de meios de pagamento amplos (M3: dinheiro, depósitos, poupança, fundos e títulos de curto prazo) existem para cada real emitido pelo Banco Central (M0).",
        "como": "M3 dividido por M0, mês a mês, nas duas definições do BCB (regime 2001 até 2018; Novo desde 2001). Candle anual sobre o M3 Novo / M0.",
        "porque": "Mede quanto dinheiro o sistema bancário cria sobre a base emitida. Subiu de 9 vezes em 2002 para 33 vezes em 2026: a economia se bancarizou e os ativos financeiros cresceram muito mais que o papel-moeda.",
        "cuidado": "Sem leitura de melhor. Um multiplicador alto é sinal de sistema financeiro profundo e também de dependência de crédito; a direção certa depende do que se pergunta.",
    },
    "moeda_pib": {
        "o_que": "Os agregados monetários (M1, M2, M3) como fração do PIB do ano.",
        "como": "Média dos 12 saldos mensais do agregado dividida pelo PIB nominal do ano (regra da emenda 04: na hiperinflação, o saldo de dezembro sozinho mistura preços de meses diferentes). Duas definições do BCB em linhas separadas, nunca emendadas.",
        "porque": "M1/PIB caiu de 14% em 1964 para 3% em 1994 (ninguém segurava dinheiro na hiperinflação) e voltou a 5-6% depois do Real; M3/PIB foi de 27% para 100%: a riqueza financeira do país hoje equivale a um PIB.",
        "cuidado": "Sem leitura de melhor. Série anual, sem candle.",
    },
    "pib": {
        "o_que": "Quanto a economia cresceu: o PIB de um trimestre contra o mesmo trimestre do ano anterior (contas trimestrais do IBGE, 1996+), e a variação real anual desde 1948 como linha.",
        "como": "Crescimento em 4 trimestres = PIB dessazonalizado do trimestre / PIB do mesmo trimestre do ano anterior − 1. Candle anual: abre no 4º trimestre do ano anterior, fecha no 4º trimestre, pavio nos 4 trimestres. A linha anual é a variação oficial do IBGE (2010: 7,5%; 2015: −3,5%; 2021: 4,8%; 2024: 3,4%).",
        "porque": "É a medida mais usada de desempenho econômico. O Brasil cresceu 7% a 10% ao ano no 'milagre' (1968-73), perto de zero nos anos 80 e 90, 4% ao ano em 2004-10 e cerca de 1% ao ano em 2011-24.",
        "cuidado": "O IBGE revisa o PIB a cada mudança de referência (1990, 1995, 2007, 2015) e os níveis mudam; as taxas de crescimento mudam pouco e estão aqui como publicadas hoje. Crescimento não diz quem cresceu: ver renda do trabalho, pobreza e Gini.",
    },
    "salmin": {
        "o_que": "O salário mínimo em reais de hoje: o valor nominal de cada mês deflacionado pelo INPC (série do Ipea).",
        "como": "Valor de dezembro de cada ano corrigido para R$ de set/2026. Candle anual: abre em dezembro anterior, fecha em dezembro, pavio nos meses. Até abr/1984 a série registra o maior mínimo regional (Rio e São Paulo); o mínimo nacional só existe desde mai/1984.",
        "porque": "É o piso do mercado de trabalho e o valor que indexa aposentadorias, BPC e pensões. Em poder de compra pelo INPC, o mínimo de 2026 (R$ 1.621) está no nível de 1960-61 e 80% acima de 1976; em cestas básicas compra metade do que comprava em 1961.",
        "cuidado": "Comparar 1961 com 2026 encadeia quatro índices de preços em 86 anos: a ordem de grandeza vale, a casa decimal não. O PIB per capita quadruplicou desde 1961: o piso igual em termos reais é um quarto em relação à economia.",
    },
    "desemprego": {
        "o_que": "Quem procurou trabalho e não encontrou, como fração da força de trabalho. Três pesquisas do IBGE: PME antiga (1980-2002, seis regiões metropolitanas), PME nova (2002-2015, seis regiões) e PNAD Contínua (2012+, Brasil inteiro).",
        "como": "Candle anual sobre a PNAD Contínua trimestral: abre no 4º trimestre do ano anterior, fecha no 4º trimestre, pavio nos trimestres. As duas PME ficam como linhas; nas sobreposições (2002; 2012-15) as linhas correm juntas e o vão é a diferença de método.",
        "porque": "É o custo humano mais direto de uma recessão. A taxa foi de 6,2% em 2014 a 12,1% em 2016 e 13,2% em 2017, e caiu a 5,1% em 2025, o menor valor da PNAD Contínua.",
        "cuidado": "As três bases medem coisas diferentes (regiões metropolitanas versus Brasil, idade mínima, semana versus 30 dias de procura): a grade por governo nunca mistura duas bases numa célula. Desemprego baixo com informalidade alta é outra história: ver informalidade.",
    },
    "primario": {
        "o_que": "A diferença entre o que o governo arrecada e o que gasta, sem contar juros, em % do PIB. Positivo = superávit, negativo = déficit.",
        "como": "Duas medidas distintas, nunca emendadas: o Tesouro mede o Governo Central pelo caixa (RTN, 1997+); o Banco Central mede todo o setor público pela variação da dívida (NFSP, aqui com o sinal invertido para que positivo seja superávit).",
        "porque": "É o que o governo faz para pagar (ou não) os juros da dívida. Superávits de 2% a 3% do PIB em 1999-2008; déficits de 2% a 3% em 2015-19; o pior ano é 2020 (pandemia).",
        "cuidado": "Maior é melhor para a dívida, não necessariamente para a economia num ano de recessão. Receitas extraordinárias (concessões, dividendos, precatórios) mudam o número sem mudar a estrutura: ver a camada de mecanismos no repositório.",
    },
    "discricionarias": {
        "o_que": "A parte do gasto do Governo Central que não é obrigatória por lei (investimento, custeio das máquinas, programas), em % do PIB.",
        "como": "Linha 4.4.2 do Resultado do Tesouro Nacional, conceito de caixa, desde 2008 (antes a planilha traz zero, tratado como não publicado).",
        "porque": "É o espaço de escolha do orçamento. Caiu de 3,3% do PIB em 2010 para 1,5% em 2022: o gasto obrigatório (previdência, pessoal, saúde e educação mínimos) tomou o lugar.",
        "cuidado": "Sem leitura de melhor: menos discricionária pode ser corte de investimento ou aperto de custeio. As emendas parlamentares (RP 6 a 9) estão dentro desse número e têm regra própria a cada ano.",
    },
    "divida": {
        "o_que": "A dívida bruta do governo geral (União, estados e municípios, sem as estatais) como fração do PIB.",
        "como": "Duas metodologias do Banco Central publicadas em paralelo: a de 2008 (não inclui a carteira de títulos do BC; 2006+) e a antiga (inclui; 2002+). Nunca emendadas no gráfico; no índice composto a antiga é encadeada à nova pela sobreposição (diferença média de −9 pontos, que varia de −5 a −15).",
        "porque": "É o estoque que os juros alimentam. Pela metodologia atual foi de 52% do PIB em 2010 para 79% em 2025, com salto na recessão de 2015-16 e na pandemia.",
        "cuidado": "Antes de dez/2001 o Banco Central não publica dívida bruta (só a líquida, e esta só em % do PIB desde 2001): FHC fica sem valor comparável. Os dois números para o mesmo ano (79% e 93% em 2025) são definições, não erro.",
    },
    "tit": {
        "o_que": "O imposto inflacionário: quanto do poder de compra do dinheiro em mãos do público e dos depósitos à vista a inflação levou no ano, em % do PIB.",
        "como": "Fórmula mensal de Cysne e Coimbra-Lisboa sobre a base M1: perda de valor real de M1 em cada mês, somada no ano e dividida pelo PIB. A linha principal usa o IGP-DI como deflator (existe desde 1947); a segunda usa o IPCA (1981+).",
        "porque": "Era um tributo de 4% a 9% do PIB nos anos 60 e 80, cobrado de quem não tinha conta remunerada (os mais pobres), e caiu a menos de 0,5% do PIB depois do Real.",
        "cuidado": "Com o IGP-DI negativo em 12 meses (2025: −1,2%) o valor fica negativo: é aritmética da fórmula, por isso a variante com IPCA corre ao lado. Fluxo do ano, mostrado em coluna.",
    },
    "pobreza": {
        "o_que": "A fração da população que vive com menos de US$ 6,85 por dia em paridade de poder de compra de 2017 (a linha do Banco Mundial para países de renda média-alta).",
        "como": "Banco Mundial PIP (1981-2024, a partir das PNADs do IBGE) e IBGE Síntese de Indicadores Sociais (2012+). Linhas separadas: a PNAD pulou 1994, 2000 e 2010, e a troca de PNAD por PNAD Contínua em 2012 é quebra de método.",
        "porque": "Caiu de 68% em 1985 para 47% em 2002, 24% em 2014, subiu a 27% em 2016-18 e caiu a 19% em 2024. É a medida internacional mais usada e a mais sensível à linha escolhida.",
        "cuidado": "Mudar a linha ou a paridade de poder de compra (2011, 2017, 2021) muda a contagem de pobres sem que ninguém fique mais rico: a mesma pessoa é pobre numa linha e não é em outra. As linhas do Bolsa Família e do BPC seguem outra régua (camada de assistência).",
    },
    "gini": {
        "o_que": "O índice de Gini da renda domiciliar per capita: 0 seria todos com a mesma renda, 1 seria um só com toda a renda.",
        "como": "Banco Mundial PIP (1981-2024) como base principal; PNAD antiga (Ipeadata, 1976-2014) e PNAD Contínua (IBGE SIS, 2012+) como linhas de conferência.",
        "porque": "O Brasil está entre os dez países mais desiguais do mundo. O Gini caiu de 0,60 (1995) para 0,52 (2014), subiu a 0,54 em 2018 e caiu a 0,50 em 2024.",
        "cuidado": "Mede só renda declarada em pesquisa domiciliar, que capta mal o topo (ver participação do 1% em dados do imposto de renda, ainda não coletada). Diferenças de centésimos entre bases são método, não realidade.",
    },
    "expvida": {
        "o_que": "Quantos anos uma pessoa nascida no ano viveria se as taxas de mortalidade daquele ano valessem a vida inteira.",
        "como": "ONU via Banco Mundial (um vintage, 1960-2024) como linha principal; tábuas do IBGE como publicadas a cada ano e a série vigente de 2025 (reconstrução 1940-2024) como conferência.",
        "porque": "Resume saúde, saneamento, violência e renda num número. Foi de 55 anos em 1964 a 67 em 1994 e 76 em 2024, com a queda da pandemia em 2020-21.",
        "cuidado": "O IBGE revisa as tábuas quando incorpora censos (2013, 2018, 2024): o mesmo ano muda de valor entre edições, por isso as linhas 'como publicada' e 'vigente' aparecem separadas.",
    },
    "homic": {
        "o_que": "Mortes por agressão (homicídios) por 100 mil habitantes, segundo os atestados de óbito (Sistema de Informações sobre Mortalidade, DATASUS).",
        "como": "Óbitos classificados como agressão dividido pela população do ano, vezes 100 mil (Ipeadata, com CID-9 até 1995 e CID-10 desde 1996).",
        "porque": "Foi de 15 por 100 mil em 1985 a 28 em 2002, 31 em 2016-17 e 20 em 2024. É o indicador de violência mais comparável entre países.",
        "cuidado": "Mortes de 'intenção indeterminada' e por 'causa mal definida' não entram e variam por estado e por ano; quando elas sobem, o homicídio registrado pode cair sem que a violência caia (série de conferência no repositório). Menor é melhor; a cor do candle não é nota de governo.",
    },
    "reprov": {
        "o_que": "Quantos alunos dos anos iniciais do ensino fundamental foram reprovados no ano, como fração dos matriculados (Censo Escolar, INEP).",
        "como": "Duas bases: 1997-2005 calculada das contagens da Sinopse para 1ª a 4ª série (fundamental de 8 anos); 2006-2025 como publicada para os anos iniciais do fundamental de 9 anos. 2020 = 0,6% é o ano das normas excepcionais da pandemia.",
        "porque": "Caiu de 15% em 1996 para 1,5% em 2025. Mas reprovação é decisão administrativa: a progressão continuada (São Paulo, 1998) e os ciclos derrubam a taxa sem que o aprendizado mude. Por isso este indicador não entra no índice composto; o Saeb entra.",
        "cuidado": "Compare com o Saeb ao lado. Uma taxa de reprovação baixa pode ser escola melhor ou regra que não reprova; a série sozinha não distingue.",
    },
    "saeb": {
        "o_que": "A proficiência média em matemática dos alunos brasileiros na avaliação nacional do INEP (Saeb), em pontos da escala de 0 a 500, por etapa.",
        "como": "Médias publicadas pelo INEP (press kit 2019 e relatório 2023), bienais, em pontos. No índice composto, um item = média simples das três etapas (5º ano, 9º ano e 3ª série do ensino médio) nos anos em que as três existem.",
        "porque": "É a medida de aprendizado que a regra de aprovação não move. O 5º ano foi de 191 pontos em 1995 a 228 em 2019 e 225 em 2023; o ensino médio ficou perto de 270 por vinte anos.",
        "cuidado": "Bienal (anos ímpares). Em 2005 o Saeb mudou de amostral para censitário (Prova Brasil) e em 2006 o fundamental passou a 9 anos: quebras catalogadas. Escalas por etapa não são comparáveis entre si.",
    },
    "porquinho_reais": {
        "o_que": "O que aconteceu com R$ 100 mil guardados em dezembro de 1994: em dinheiro (só a inflação age), na poupança e na Selic, tudo em reais de poder de compra de dez/1994.",
        "como": "Caixa: 100 mil divididos pelo IPCA acumulado (e pelo IGP-DI, como linha). Poupança: rendimento mensal da caderneta (BCB SGS 25) aplicado e deflacionado. Selic: taxa mensal (SGS 4390) aplicada e deflacionada. Escala de log.",
        "porque": "Em set/2026 o dinheiro parado vale R$ 13.208; na poupança, 231 mil; na Selic, 1,13 milhão. O vão entre caixa e poupança é o custo de não ter conta: o imposto inflacionário em versão doméstica.",
        "cuidado": "Sem candle: dinheiro parado só perde. Selic 'cheia' sem imposto de renda nem custo de fundo: é o teto teórico, não o que um aplicador recebeu.",
    },
    "porquinho_refs": {
        "o_que": "Os mesmos R$ 100 mil de dez/1994 medidos em outras réguas: dólar, franco suíço, DES do FMI e onças de ouro, cada uma descontada a inflação da própria referência. Índice 100 em dez/1994.",
        "como": "Reais convertidos pela cotação de cada mês (PTAX do BCB; ouro pelo Pink Sheet do Banco Mundial) e deflacionados pelo CPI do país da moeda. Escala de log.",
        "porque": "Em dólares o porquinho vale 7% do que valia; em ouro, 1,5% (310 onças viraram 4,5). É a face externa da perda: o real perdeu para todas as referências, e muito mais para o ouro.",
        "cuidado": "O ouro teve alta própria (de US$ 380 a mais de US$ 3.000 a onça); o DES é deflacionado pelo CPI dos EUA por falta de deflator próprio. Nenhuma referência é 'a moeda estável' por decreto.",
    },
    "porquinho_brasil": {
        "o_que": "O porquinho medido no que ele compra no Brasil: em reais pelo IPCA, em salários mínimos e em cestas básicas do DIEESE. Índice 100 em dez/1994.",
        "como": "100 mil divididos pelo salário mínimo do mês (1.429 mínimos em 1994, 62 em 2026) e pelo custo da cesta de São Paulo (1.144 cestas, 111 em 2026). Escala de log.",
        "porque": "Mostra que a perda depende da régua: em salários mínimos o dinheiro parado perdeu mais (o mínimo subiu acima da inflação); em cestas, perdeu menos que em reais no começo e mais no fim.",
        "cuidado": "Cesta de São Paulo, não média do país. A mudança de metodologia do DIEESE em 2016 está no catálogo.",
    },
    "carga": {
        "o_que": "Tudo o que União, estados e municípios arrecadam em tributos e contribuições, como fração do PIB.",
        "como": "Quatro bases que nunca se emendam: Receita Federal edição 2024 (2002-24, definição atual, sem FGTS e Sistema S), Receita edição 2020 (definição anterior, 2 pontos acima), Tesouro Nacional no padrão do FMI (GFSM, 2010-25) e a compilação do Ipea para 1947-96 (literatura). O mesmo ano muda de valor entre edições porque a Receita revisa definição e PIB.",
        "porque": "Foi de 14% do PIB em 1947 a 24% em 1985, 29% em 1994 e 32% em 2024-25: um dos maiores pesos entre países de renda média (a média da OCDE fica perto de 34%). O crescimento concentrou-se em 1994-2005.",
        "cuidado": "Sem leitura de melhor no índice: carga alta financia saúde e previdência e também pesa sobre produção. A diferença de 2 pontos entre edições da Receita é definição (FGTS, Sistema S, restituições), não erro. Lacuna 1997-2001 na compilação longa.",
    },
    "ministerios": {
        "o_que": "Quantos órgãos a lei de organização da Presidência chama de ministério em 1º de janeiro de cada ano, e quantos cargos têm status de ministro (Casa Civil, AGU, BC, etc.).",
        "como": "Contagem na lei ou medida provisória vigente em 1º de janeiro (Planalto), 1995-2026. Pontos, não linha, porque é contagem.",
        "porque": "20 ministérios em 1995, 24 em 2010, 16-17 em 2019-22 e 32 em 2026 (38 com status). Mede a estrutura do governo, não o gasto.",
        "cuidado": "Sem leitura de melhor. Ministério a mais não é gasto a mais em proporção: o custo dos ministérios é pequeno diante da previdência; o que muda é coordenação e cargos.",
    },
    "cargos": {
        "o_que": "Cargos em comissão e funções de confiança (DAS, FCPE, CCE e FCE) por mil servidores ativos do Executivo federal civil, em dezembro.",
        "como": "Painel Estatístico de Pessoal (Ministério da Gestão), 1999-2025, transcrito do painel. Duas bases: até 2020 e desde 2021, porque a contagem cai 74% entre dez/2020 e dez/2021 sem causa no changelog do painel (a Lei 14.204/2021, que criou CCE e FCE, é candidata).",
        "porque": "Foi de 32 por mil em 1999 a 40 em 2010-14 e 18 em 2025 na base nova. Mede o tamanho da camada de livre nomeação.",
        "cuidado": "A queda de 2021 pode ser reclassificação, não corte: até a fonte explicar, as bases ficam separadas e a grade por governo não emenda.",
    },
    "cargos_sem_vinculo": {
        "o_que": "Entre os cargos em comissão, a fração ocupada por quem não tem cargo efetivo (não é servidor de carreira).",
        "como": "Painel Estatístico de Pessoal, dezembro de cada ano, 1999-2025, nas mesmas duas bases do indicador anterior.",
        "porque": "Era 49% em 1999, 48% em 2010, 38% em 2016-18, 26% em 2022 e 33% em 2025. Mede quanto da chefia vem de fora da carreira.",
        "cuidado": "Mesma quebra de 2021. 'Sem vínculo' é ausência de cargo efetivo; não diz nada sobre qualificação.",
    },
    "estatais": {
        "o_que": "O resultado primário das empresas estatais (federais e estaduais) como fração do PIB, pela contabilidade de necessidades de financiamento do Banco Central (sinal invertido: positivo = superávit).",
        "como": "BCB NFSP, 2002+ (estaduais desde 1998). Petrobras sai do perímetro em mai/2009 e Eletrobras em nov/2010: a série federal muda de tamanho ali.",
        "porque": "Mede se as estatais ajudam ou pesam no resultado fiscal: perto de zero na maior parte do período, com superávits pequenos em 2002-06.",
        "cuidado": "Lucro contábil por empresa (Petrobras, BB, Eletrobras) está coletado em unidades e normas diferentes por ano e fica para a camada curada; não entra cru.",
    },
    "libdem": {
        "o_que": "Índice de democracia liberal do projeto Varieties of Democracy (V-Dem), versão 16, variável v2x_libdem, que vai de 0 a 1. Combina a qualidade das eleições com a proteção das liberdades individuais e as restrições ao Executivo.",
        "como": "É o valor anual do índice, em uma base única, sem encadeamento. No índice a direção é maior é melhor, com balizas de 1995 a 2024. A série vem de codificação por especialistas agregada por um modelo estatístico de medição publicado.",
        "porque": "Resume em um número o quanto o sistema político protege direitos e limita o poder. O índice foi de 0,71 em 1995 para 0,78 em 2014, 0,65 em 2016, 0,53 em 2020 e 0,71 em 2024.",
        "cuidado": "A medida reflete avaliações de especialistas, com incerteza própria, e as versões do V-Dem podem revisar valores passados. Não capta preferências nem satisfação da população. A direção segue a definição normativa do próprio índice e o modelo de medição (Marquardt e Pemstein (2018); Coppedge et al. (2011)), referências do pré-registro conferidas no Crossref e com quartil 1 no SJR.",
    },
    "corrupcao": {
        "o_que": "Índice de corrupção política do projeto Varieties of Democracy (V-Dem), versão 16, variável v2x_corr, que vai de 0 a 1. Agrega avaliações sobre corrupção no setor público, no Executivo, no Legislativo e no Judiciário.",
        "como": "É o valor anual do índice, em uma base única, sem encadeamento. No índice a direção é menor é melhor, pois valores altos indicam mais corrupção, com balizas de 1995 a 2024. A série vem de codificação por especialistas agregada por um modelo estatístico de medição publicado.",
        "porque": "Corrupção política afeta a confiança nas instituições e o uso de recursos públicos. O índice foi de 0,51 em 1995 para 0,55 em 2002, 0,49 em 2010, 0,54 em 2020 e 0,42 em 2025.",
        "cuidado": "Mede a percepção de especialistas sobre a corrupção, e não o número de casos descobertos ou punidos; um aumento de investigações pode, em tese, alterar a percepção. Versões do V-Dem podem revisar valores passados. A direção segue a definição normativa do índice e o modelo de medição (Marquardt e Pemstein (2018); Coppedge et al. (2011)), referências do pré-registro conferidas no Crossref e com quartil 1 no SJR.",
    },
    "legcon": {
        "o_que": "Índice de restrições do Legislativo ao Executivo do projeto Varieties of Democracy (V-Dem), versão 16, variável v2xlg_legcon, que vai de 0 a 1. Reflete o grau em que o Legislativo consegue questionar, investigar e limitar o Executivo.",
        "como": "É o valor anual do índice, em uma base única, sem encadeamento. No índice a direção é maior é melhor, com balizas de 1995 a 2024. A série vem de codificação por especialistas agregada por um modelo estatístico de medição publicado.",
        "porque": "Freios e contrapesos entre os poderes são parte central do funcionamento institucional. O índice foi de 0,83 em 1995 para 0,92 em 2014, 0,78 em 2020 e 0,93 em 2024.",
        "cuidado": "Mede capacidade de controle segundo especialistas, e não se os controles foram exercidos bem ou mal em cada caso. Versões do V-Dem podem revisar valores passados. A direção segue a definição normativa do índice e o modelo de medição (Marquardt e Pemstein (2018); Coppedge et al. (2011)), referências do pré-registro conferidas no Crossref e com quartil 1 no SJR.",
    },
    "jucon": {
        "o_que": "Índice de restrições do Judiciário ao Executivo do projeto Varieties of Democracy (V-Dem), versão 16, variável v2x_jucon, que vai de 0 a 1. Reflete o grau em que o Executivo respeita a Constituição e as decisões dos tribunais e em que o Judiciário tem independência.",
        "como": "É o valor anual do índice, em uma base única, sem encadeamento. No índice a direção é maior é melhor, com balizas de 1995 a 2024. A série vem de codificação por especialistas agregada por um modelo estatístico de medição publicado.",
        "porque": "Um Judiciário que consegue limitar o Executivo é parte do desenho de freios e contrapesos. O índice foi de 0,83 em 1995 para 0,93 em 2010, 0,81 em 2020 e 0,95 em 2024.",
        "cuidado": "Mede independência e capacidade de limitar o Executivo segundo especialistas, e não a qualidade das decisões judiciais nem a rapidez dos processos. Versões do V-Dem podem revisar valores passados. A direção segue a definição normativa do índice e o modelo de medição (Marquardt e Pemstein (2018); Coppedge et al. (2011)), referências do pré-registro conferidas no Crossref e com quartil 1 no SJR.",
    },
    "estatal": {
        "o_que": "Propriedade estatal da economia segundo o projeto Varieties of Democracy (V-Dem), versão 16, variável v2clstown, em escala em que valor alto significa menos propriedade do Estado. Reflete a avaliação de especialistas sobre o quanto a economia é controlada pelo Estado.",
        "como": "É o valor anual da variável, em uma base única, sem encadeamento. No índice a direção é maior é melhor, isto é, menos Estado na propriedade, com balizas de 1995 a 2024.",
        "porque": "O papel do Estado na propriedade de empresas e ativos é um tema central de política econômica. A série ficou em 1,03 de 1995 a 2014, subiu para 1,66 em 2016 e 2018 e foi para 1,44 em 2024 e 1,18 em 2025.",
        "cuidado": "Este item é uma premissa econômica declarada pelo autor, do bloco P, e não um consenso. O pré-registro o descreve como premissa, com medida de intervenção distinta do tamanho do Estado, e a literatura a favor e contra está no pré-registro, conferida no Crossref e com quartil 1 no SJR. A série fica constante por longos períodos e muda em saltos de codificação.",
    },
    "industria": {
        "o_que": "Valor adicionado da indústria de transformação como percentual do PIB a preços de mercado. A fonte são as contas nacionais do IBGE: o Sistema de Contas Nacionais com referência 2000 (1995 a 2009) e as contas trimestrais com referência 2010 (1996 a 2025).",
        "como": "A base antiga é ligada à nova pela diferença média nos 14 anos de sobreposição (1996 a 2009): menos 1,33 ponto percentual, com desvio-padrão de 0,55, impresso no item. No índice a direção é maior é melhor, com balizas de 1995 a 2024.",
        "porque": "O peso da manufatura na economia é um tema central do debate sobre desenvolvimento. A participação foi de 14,9% do PIB em 1995 para 12,4% em 2002, 10,3% em 2014, 13,1% em 2022 e 11,8% em 2025.",
        "cuidado": "Este item é uma premissa econômica declarada pelo autor, do bloco P, e não um consenso. A literatura a favor (por exemplo, Rodrik (2016), sobre desindustrialização precoce) e a contra (crescimento puxado por serviços) é citada lado a lado no pré-registro e está no pré-registro, conferida no Crossref e com quartil 1 no SJR. A razão a preços de mercado também muda com preços relativos e câmbio, e o índice é publicado com e sem o bloco P.",
    },
    "governo": {
        "o_que": "Consumo final do governo como percentual do PIB a preços de mercado: despesas correntes das administrações públicas com a produção de serviços como educação e saúde públicas e a administração em si. A fonte são as contas nacionais do IBGE, com referência 2000 (1995 a 2009) e referência 2010 (1996 a 2025).",
        "como": "A base antiga é ligada à nova pela diferença média nos 14 anos de sobreposição (1996 a 2009): menos 0,77 ponto percentual, com desvio-padrão de 0,40, impresso no item. No índice a direção é menor é melhor, com balizas de 1995 a 2024.",
        "porque": "Mostra quanto da produção é absorvido pelo consumo das administrações públicas. A razão foi de 20,3% do PIB em 1995 para 19,0% em 2010, 20,4% em 2016 e 18,4% em 2022.",
        "cuidado": "Este item é uma premissa econômica declarada pelo autor, do bloco P, e não um consenso. A literatura a favor (revisão de Bergh e Henrekson (2011) sobre tamanho do Estado e crescimento) e a contra (resultado incerto em países em desenvolvimento) é citada lado a lado no pré-registro e está no pré-registro, conferida no Crossref e com quartil 1 no SJR. O consumo do governo exclui transferências, previdência, juros e investimento público, e menos gasto não significa serviço melhor.",
    },
    "abertura": {
        "o_que": "Abertura comercial: soma de exportações e importações de bens e serviços (X+M) como percentual do PIB a preços de mercado. A fonte são as contas nacionais do IBGE, com referência 2000 (1995 a 2009) e referência 2010 (1996 a 2025).",
        "como": "A base antiga é ligada à nova pela diferença média nos 14 anos de sobreposição (1996 a 2009): mais 0,61 ponto percentual, com desvio-padrão de 0,38, impresso no item. No índice a direção é maior é melhor, com balizas de 1995 a 2024.",
        "porque": "Mostra o peso do comércio exterior na economia. A razão foi de 16,6% do PIB em 1995 para 27,6% em 2002, 22,8% em 2010, 32,3% em 2020 e 38,8% em 2022.",
        "cuidado": "Este item é uma premissa econômica declarada pelo autor, do bloco P, e não um consenso. A literatura a favor (Frankel e Romer (1999); Wacziarg e Welch (2008)) e a crítica (Rodríguez e Rodrik (2000)) é citada lado a lado no pré-registro e está no pré-registro, conferida no Crossref e com quartil 1 no SJR. A razão mede o fluxo, e não a política comercial, e varia com o câmbio e com os preços das mercadorias.",
    },
    "familias": {
        "o_que": "Endividamento das famílias: saldo de dívida com o sistema financeiro em relação à renda das famílias dos últimos 12 meses, em %, no mês de dezembro. A fonte é o Banco Central do Brasil (BCB), série SGS 29037, disponível a partir de 2005.",
        "como": "É o valor de dezembro de cada ano, em uma base única, sem encadeamento. No índice a direção é menor é melhor, com balizas tiradas do período em que a série existe dentro de 1995 a 2024.",
        "porque": "Dívida alta em relação à renda deixa as famílias mais expostas a choques de renda e de juros. A série foi de 19,6% em 2005 para 34,0% em 2010, 39,2% em 2014, 49,1% em 2022 e 49,7% em 2025.",
        "cuidado": "A direção segue Mian, Sufi e Verner (2017), que associam aumento da dívida das famílias a menor crescimento nos anos seguintes, referência do pré-registro conferida no Crossref e com quartil 1 no SJR. A razão entre dívida e renda não informa o custo de pagar a dívida, o tipo de crédito nem quem deve. A série só começa em 2005.",
    },
    "reservas": {
        "o_que": "Reservas internacionais do país em relação ao tamanho da economia, em % do PIB. O numerador é o saldo de reservas do Banco Central do Brasil (BCB) em dezembro e o denominador é o PIB em dólares correntes do Banco Mundial (WDI).",
        "como": "É a razão anual entre as reservas em dólares e o PIB em dólares, sem encadeamento. No índice a direção é maior é melhor, com balizas de 1995 a 2024.",
        "porque": "Reservas maiores dão ao país um colchão contra saídas bruscas de capital e choques externos. A razão foi de 6,7% do PIB em 1995 para 7,4% em 2002, 13,1% em 2010, 24,1% em 2020 e 15,1% em 2024.",
        "cuidado": "Como o PIB é medido em dólares correntes, a razão varia também com o câmbio, mesmo que as reservas fiquem iguais. Manter reservas tem custo e a literatura discute quanto é suficiente; maior é melhor é a direção declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11).",
    },
    "pd": {
        "o_que": "Gasto em pesquisa e desenvolvimento (P&D) como percentual do PIB, somando setores público e privado. A fonte é o Instituto de Estatística da UNESCO, obtido via Banco Mundial (WDI).",
        "como": "É o percentual anual, em uma base única, sem encadeamento. No índice a direção é maior é melhor, com balizas calculadas sobre os anos disponíveis dentro de 1995 a 2024.",
        "porque": "O esforço em P&D é uma das medidas básicas da capacidade de inovação de um país. O gasto foi de 1,05% do PIB em 2000 para 1,16% em 2010, 1,27% em 2014 e 1,19% em 2023.",
        "cuidado": "Mede o dinheiro gasto, e não a qualidade das pesquisas nem seus resultados. A série começa em 2000 e termina em 2023, e os valores dependem de levantamentos nacionais que podem mudar de método. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "pesquisadores": {
        "o_que": "Número de pesquisadores em P&D por milhão de habitantes. A fonte é o Instituto de Estatística da UNESCO, obtido via Banco Mundial (WDI) até 2014.",
        "como": "É o valor anual por milhão de habitantes, em uma base única, sem encadeamento. No índice a direção é maior é melhor, com balizas calculadas sobre os anos disponíveis dentro de 1995 a 2024.",
        "porque": "Mostra o tamanho da força de trabalho dedicada à produção de conhecimento. A série foi de 299 por milhão em 2000 para 403 em 2002, 696 em 2010 e 903 em 2014.",
        "cuidado": "A série termina em 2014, e os anos seguintes ficam sem o item; nada é estimado. Conta pessoas, e não a qualidade ou a produtividade científica delas, e depende de levantamentos nacionais com definições que podem ter mudado. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "patentes": {
        "o_que": "Pedidos de patente feitos por residentes do país, por milhão de habitantes. A fonte é a Organização Mundial da Propriedade Intelectual (WIPO), obtida via Banco Mundial (WDI), dividida pela população do WDI.",
        "como": "É o número anual de pedidos dividido pela população, em milhões, sem encadeamento. No índice a direção é maior é melhor, com balizas de 1995 a 2024.",
        "porque": "O patenteamento por residentes é um sinal de atividade inventiva local. A série foi de 16,7 por milhão em 1995 para 21,8 em 2010, 25,6 em 2016, 20,9 em 2022 e 27,1 em 2024.",
        "cuidado": "Mede pedidos, e não patentes concedidas nem o valor das invenções; empresas e setores diferem muito na propensão a patentear. Invenções protegidas de outras formas não aparecem. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "eci": {
        "o_que": "Índice de complexidade econômica (ECI): mede a diversidade e a sofisticação dos produtos que o país exporta, a partir de quais países conseguem exportar quais bens. A fonte é o Atlas de Complexidade Econômica do Harvard Growth Lab, versão 12, com produtos classificados em HS92.",
        "como": "É o valor anual do índice no Atlas, em uma base única, sem encadeamento. No índice a direção é maior é melhor, com balizas de 1995 a 2024.",
        "porque": "Países que exportam bens mais complexos tendem a ter mais conhecimento produtivo acumulado. O índice foi de 0,82 em 1995 para 0,84 em 2002, 0,64 em 2014, 0,38 em 2020 e 0,35 em 2024.",
        "cuidado": "Usa só o comércio de bens, sem serviços, e o valor de cada ano depende também das exportações dos demais países. Mudanças na composição das exportações, como o peso de produtos primários, mexem no índice. A direção segue Hidalgo e Hausmann (2009), referência do pré-registro conferida no Crossref e com quartil 1 no SJR.",
    },
    "mortinf": {
        "o_que": "Mortalidade infantil: número de mortes de crianças pequenas por mil nascidos vivos. A fonte são as estimativas do Grupo Interagências da ONU para Mortalidade Infantil (UN IGME), obtidas pelo Banco Mundial nos WDI.",
        "como": "É a taxa anual por mil nascidos vivos, em uma base única, sem encadeamento. No índice a direção é menor é melhor, com balizas de 1995 a 2024.",
        "porque": "Resume condições de saúde, saneamento e acesso a atendimento nos primeiros anos de vida. A taxa foi de 39,9 por mil em 1995 para 25,6 em 2002, 16,0 em 2010 e 12,3 em 2024.",
        "cuidado": "São estimativas modeladas pela ONU a partir de registros e pesquisas, e não a contagem direta do sistema de saúde brasileiro; valores antigos podem ser revistos. A taxa é nacional e esconde diferenças entre regiões. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "mortmat": {
        "o_que": "Razão de mortalidade materna: mortes de mulheres por causas ligadas à gravidez, ao parto ou ao pós-parto, por 100 mil nascidos vivos. Usa a estatística nacional, obtida via Banco Mundial (WDI).",
        "como": "É o valor anual da razão, em uma base única e sem encadeamento. No índice a direção é menor é melhor, com balizas de 1995 a 2024.",
        "porque": "Reflete a qualidade do pré-natal, do parto e do acesso a atendimento de emergência. A razão foi de 115,7 por 100 mil em 1995 para 75,9 em 2002, 68,9 em 2010 e 57,7 em 2022.",
        "cuidado": "A série termina em 2022. O valor de 2020 (74,7) é maior que o de 2018 (59,1) e coincide com o ano do início da pandemia de covid-19; a série não separa causas. Como depende do registro de óbitos e da identificação da causa, parte das mortes pode não ser contada, e o número pequeno de casos por ano oscila. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "dtp3": {
        "o_que": "Cobertura vacinal com a terceira dose da vacina contra difteria, tétano e coqueluche (DTP3), em % das crianças da faixa etária-alvo. A fonte são as estimativas da OMS e do UNICEF (WUENIC, edição de 2025).",
        "como": "É o percentual anual de cobertura, em uma base única, sem encadeamento. No índice a direção é maior é melhor, com balizas de 1995 a 2024.",
        "porque": "A DTP3 é o indicador padrão de cobertura da imunização de rotina no mundo. A cobertura foi de 81% em 1995 para 99% em 2002 e 2010, caiu para 77% em 2020 e 2022 e voltou a 90% em 2024.",
        "cuidado": "A série mistura dados administrativos de doses aplicadas com ajustes da OMS e do UNICEF, e mede cobertura de uma vacina, não a proteção da população contra as doenças. Mudanças no sistema de registro podem afetar os números. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "prenatal": {
        "o_que": "Percentual de nascidos vivos cujas mães fizeram 7 ou mais consultas de pré-natal. A fonte é o Sistema de Informações sobre Nascidos Vivos (SINASC), do Ministério da Saúde.",
        "como": "É o percentual anual calculado sobre os nascidos vivos registrados, em uma base única, sem encadeamento. No índice a direção é maior é melhor, com balizas de 1995 a 2024.",
        "porque": "Mede o acesso das gestantes ao acompanhamento regular durante a gravidez. O percentual foi de 49,0% em 1995 para 61,1% em 2010, 71,1% em 2018 e 79,4% em 2024.",
        "cuidado": "Mede um processo, o número de consultas, e não a qualidade do atendimento nem o desfecho da gestação. Os dados vêm da declaração de nascido vivo, cuja cobertura e preenchimento podem variar entre anos e regiões. Só entram os nascimentos registrados. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "subalimentacao": {
        "o_que": "Prevalência de subalimentação: parcela da população cuja ingestão habitual de calorias fica abaixo do necessário. A fonte é a FAO, via Banco Mundial (WDI).",
        "como": "É o percentual anual da população, em uma base só, sem encadeamento. No índice a direção é menor é melhor, com balizas tiradas de 1995 a 2024.",
        "porque": "É uma medida direta de privação alimentar no país. A série foi de 10,5% em 2001 para 9,1% em 2002, 3,0% em 2010 e 2,5% em 2024.",
        "cuidado": "A FAO estima o indicador a partir de balanços de alimentos e de distribuição de consumo, não de uma contagem de pessoas com fome, e costuma divulgar médias de vários anos. Os valores de 2,5% repetidos em vários anos parecem refletir o menor valor divulgado pela fonte, de modo que diferenças abaixo disso não aparecem. A série não mede qualidade da dieta nem insegurança alimentar moderada. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "analfabetismo": {
        "o_que": "Taxa de analfabetismo da população de 15 anos ou mais, em %. Usa a PNAD (indicador IDS 1187) e a PNAD Contínua (tabela SIDRA 7113), do IBGE.",
        "como": "As duas pesquisas não se sobrepõem no tempo, então não há encadeamento: o item usa só o trecho da base mais longa, a PNAD, e a ausência fica registrada na cobertura. No índice a direção é menor é melhor, com balizas de 1995 a 2024.",
        "porque": "Alfabetização é a base para acessar outros direitos e serviços. A taxa foi de 11,5% em 2004 para 8,3% em 2014 e 8,0% em 2015.",
        "cuidado": "O trecho usado vai só de 2004 a 2015, então os anos seguintes ficam sem o item e nada é estimado. A informação é autodeclarada e não capta o analfabetismo funcional, isto é, quem sabe ler palavras mas não compreende textos. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "anos_estudo": {
        "o_que": "Média de anos de estudo das pessoas de 25 anos ou mais.",
        "como": "Atlas do Desenvolvimento Humano (censos 1991 e 2000).",
        "porque": "Mede estoque de escolaridade.",
        "cuidado": "Só dois pontos na camada curada: fica fora do índice até ter série.",
    },
    "agua": {
        "o_que": "Percentual de domicílios ligados à rede geral de abastecimento de água. Usa a PNAD (tabela SIDRA 1955) e a PNAD Contínua (tabela SIDRA 6731), do IBGE.",
        "como": "As duas bases não se sobrepõem no tempo, então não há encadeamento: o item usa só o trecho da base mais longa, a PNAD. No índice a direção é maior é melhor, com balizas de 1995 a 2024.",
        "porque": "Água encanada é condição básica de saúde e de vida cotidiana. O percentual foi de 81,1% em 2001 para 81,9% em 2002, 85,4% em 2014 e 85,4% em 2015.",
        "cuidado": "O trecho usado termina em 2015, e os anos seguintes ficam sem o item. Estar ligado à rede não garante água de qualidade, nem fornecimento contínuo ou sem racionamento. A série também não cobre população sem domicílio fixo. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "esgoto": {
        "o_que": "Percentual de domicílios com esgotamento sanitário considerado adequado, conforme o critério da pesquisa. Usa a PNAD (tabela SIDRA 1956) e a PNAD Contínua (tabela SIDRA 7192), do IBGE.",
        "como": "As duas bases não se sobrepõem no tempo, então não há encadeamento: o item usa só o trecho da base mais longa, a PNAD. No índice a direção é maior é melhor, com balizas de 1995 a 2024.",
        "porque": "O destino adequado do esgoto reduz doenças e contaminação da água. O percentual foi de 66,7% em 2001 para 68,1% em 2002, 76,8% em 2014 e 80,6% em 2015.",
        "cuidado": "O trecho usado termina em 2015, e os anos seguintes ficam sem o item. O critério de adequado vem da pesquisa de origem e não informa se o esgoto coletado é tratado antes de ser lançado. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "internet": {
        "o_que": "Percentual de domicílios com acesso à internet. Combina três recortes do IBGE: a PNAD de 2003 a 2015 (domicílios com microcomputador ligado à internet), a PNAD de 2013 a 2015 (internet por qualquer equipamento) e a PNAD Contínua TIC de 2016 em diante.",
        "como": "A medida de microcomputador é ligada à de qualquer equipamento pela diferença média de 11,9 pontos percentuais nos 3 anos de sobreposição (2013 a 2015), com variação de 5,6 a 17,3. O elo com a PNAD Contínua TIC não tem sobreposição, então não é emendado. No índice a direção é maior é melhor.",
        "porque": "O acesso à internet condiciona educação, trabalho e serviços públicos digitais. A série emendada foi de 23,3% em 2003 para 54,9% em 2014 e 57,8% em 2015.",
        "cuidado": "A série emendada termina em 2015, e os anos seguintes ficam sem o item. A diferença de 11,9 pontos entre definições variou muito de um ano para outro, o que dá incerteza à parte antiga. Ter acesso no domicílio não mede velocidade, custo nem uso efetivo. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "desmatamento": {
        "o_que": "Área de floresta amazônica derrubada por corte raso em um ano, em km² por ano, medida por satélite. A fonte é o programa PRODES, do Instituto Nacional de Pesquisas Espaciais (INPE).",
        "como": "É o valor anual do PRODES em km², em uma base única e sem encadeamento. No índice a direção é menor é melhor, com balizas de 1995 a 2024.",
        "porque": "O desmatamento é o indicador mais acompanhado da pressão sobre a Amazônia. A série foi de 29.059 km² em 1995 para 7.000 em 2010, 5.012 em 2014, 11.594 em 2022 e 5.731 em 2025.",
        "cuidado": "O PRODES mede corte raso na Amazônia, e não a degradação da floresta, as queimadas nem o desmatamento em outros biomas, como o Cerrado. O ano do PRODES é contado em um ciclo que não coincide com o ano civil. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "informalidade": {
        "o_que": "Proporção de pessoas ocupadas em situação de trabalho informal, segundo a definição das séries de origem. Usa a PNAD (série DISOC_INFI do Ipea) e a PNAD Contínua (tabela SIDRA 4708).",
        "como": "As duas bases não se sobrepõem no tempo, então não há encadeamento: o item usa só o trecho da base mais longa, a PNAD, e a lacuna fica registrada na cobertura. No índice a direção é menor é melhor, com balizas de 1995 a 2024.",
        "porque": "Mostra quanta gente trabalha sem a proteção formal do emprego regulado. A série foi de 57,8% em 1995 para 58,2% em 2002 e 47,3% em 2014.",
        "cuidado": "Como a série usada termina em 2014, os anos seguintes ficam sem este item e aparecem na cobertura como ausentes; nada é estimado. A definição de informal pode diferir entre as pesquisas, por isso elas não são emendadas. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "renda_trab": {
        "o_que": "Renda real do trabalho: rendimento das pessoas ocupadas em valores deflacionados, conforme as pesquisas domiciliares do IBGE. Usa a PNAD (tabela SIDRA 1871) e a PNAD Contínua (tabela SIDRA 4660 deflacionada).",
        "como": "A PNAD antiga é ligada à PNADC pela razão média medida nos 4 anos em que as duas existem (2012 a 2015), com fator de 1,085 impresso no item. No índice a direção é maior é melhor, com balizas de 1995 a 2024.",
        "porque": "É a renda que a maior parte das famílias de fato recebe pelo trabalho. A série foi de 2.378 em 2001 para 3.328 em 2014, caiu para 3.078 em 2022 e chegou a 3.417 em 2024, em valores reais da própria série.",
        "cuidado": "Mede o rendimento médio de quem está ocupado, e não de toda a população; não mostra desigualdade nem captura bem a mudança de quem entra ou sai do emprego. A ligação entre bases supõe que a diferença entre elas seja estável. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "pibpc": {
        "o_que": "Valor da produção de bens e serviços do país dividido pela população, expresso em dólares internacionais de 2021 que igualam o poder de compra entre países (PPC). A fonte é o Banco Mundial, série NY.GDP.PCAP.PP.KD dos Indicadores de Desenvolvimento Mundial (WDI).",
        "como": "É o nível anual da série em dólares PPC constantes de 2021, sem transformação. No índice a direção é maior é melhor: a baliza de 0 ponto é o menor valor de 1995 a 2024 e a de 100 pontos é o maior. A base é única, sem encadeamento.",
        "porque": "É a medida mais usada do volume médio de produção por habitante e dá o pano de fundo de quase todas as outras séries. A série foi de US$ 13.550 em 1995 para US$ 19.183 em 2014, caiu para US$ 17.621 em 2016 e chegou a US$ 19.652 em 2024.",
        "cuidado": "É uma média nacional: não diz como a renda se distribui nem mede ambiente, tempo livre ou produção fora do mercado. O Banco Mundial revisa as séries PPC quando atualiza o ano-base, então valores antigos podem mudar. A direção é a declarada no pré-registro, que só admite itens com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "fbcf": {
        "o_que": "Formação bruta de capital fixo (FBCF): quanto a economia gasta em máquinas, equipamentos, construções e outros ativos duráveis, como percentual do PIB. A fonte é a série da FGV IBRE construída sobre o Sistema de Contas Nacionais (SCN) do IBGE.",
        "como": "É a razão anual entre a FBCF e o PIB, em %. No índice a direção é maior é melhor, com balizas tiradas do período de 1995 a 2024. A série tem uma base só, sem encadeamento.",
        "porque": "O investimento amplia a capacidade de produzir nos anos seguintes. A série foi de 20,3% do PIB em 1995 para 15,5% em 2016 e 16,9% em 2024, passando por 20,5% em 2010.",
        "cuidado": "Mede quanto se investe, não a qualidade nem a produtividade do que foi construído ou comprado. As contas nacionais passam por revisões de metodologia e de ano-base, que podem alterar os percentuais passados. A direção é a declarada no pré-registro, com apoio exigido em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "ptf": {
        "o_que": "Produtividade total dos fatores (PTF): quanto a economia produz além do que se explica só pelo capital e pelo trabalho empregados. A fonte é a Penn World Table (PWT) versão 11.0, variável rtfpna, que é um índice e não uma taxa.",
        "como": "A série é um índice anual em nível, calculado pela PWT a partir de hipóteses sobre capital e participação do trabalho na renda. No índice a direção é maior é melhor, com balizas do período de 1995 a 2024. A base é única, sem encadeamento.",
        "porque": "Crescimento sustentado de renda por habitante depende em boa parte de produzir mais com os mesmos insumos. O índice foi de 1,29 em 1995 para 1,13 em 2014, 1,04 em 2016 e 0,97 em 2022.",
        "cuidado": "A PTF é um resíduo estimado, não um dado observado, e depende das hipóteses da PWT; novas versões da tabela podem mudar os valores. A série termina em 2023, então os anos mais recentes ficam sem este item. A direção é a declarada no pré-registro, com apoio em literatura revisada por pares (pré-registro da fase 2, §4 e §11; referências conferidas no Crossref e com quartil 1 no SJR).",
    },
    "aluguel_saude": {
        "o_que": "Quanto o aluguel residencial e o plano de saúde (subitens do IPCA, IBGE) subiram em relação ao salário mínimo e em relação ao IPCA geral, desde dezembro de 1999 (= 100).",
        "como": "Número-índice de cada subitem encadeado das variações mensais publicadas pelo IBGE (cinco tabelas do SIDRA, 1999-2026), dividido pelo índice do salário mínimo nominal (ou pelo índice do IPCA geral), vezes 100. Acima de 100 = o item pesa mais no salário (ou subiu mais que a inflação) do que em 1999. Candle anual sobre plano de saúde / salário mínimo.",
        "porque": "São os dois itens que mais pesam na classe média e que não estão na lista de produtos. De dez/1999 a dez/2024 o IPCA subiu 347%, o aluguel 225% e o plano de saúde 660%: o plano ficou 70% mais caro em relação a tudo o mais, e o aluguel 27% mais barato. Contra o salário mínimo (que subiu mais que o IPCA), os dois pesam menos do que em 1999; contra a renda mediana, menos vantagem.",
        "cuidado": "É índice de preço, não preço: diz quanto subiu, não quanto custa. O IPCA mede o aluguel de quem já aluga (contratos), não o preço de contrato novo. Em 2000-01 o plano de saúde tem dez meses de variação zero antes de o IBGE adotar o reajuste da ANS; as tabelas do SIDRA não têm mês de sobreposição e foram encadeadas pela continuidade declarada pelo IBGE (catálogo de quebras).",
    },
    "plano_saude": {
        "o_que": "Quanto o plano de saúde foi reajustado em cada ano, em três medidas: o teto que a ANS autoriza para planos individuais, o subitem do IPCA e o reajuste que as operadoras comunicaram à ANS para os planos coletivos (empresariais e por adesão), que não têm teto.",
        "como": "Teto da ANS: percentual anual publicado pela agência (ciclo de maio). IPCA: subitem plano de saúde, dezembro contra dezembro. Coletivos: comunicados de reajuste das operadoras à ANS (dados abertos), média ponderada pelo número de beneficiários, no ano em que o reajuste começa a valer; a linha 'menos de 30 vidas' usa a marca de agrupamento de contratos, que existe desde 2013.",
        "porque": "Responde se o IPCA 'está defasado': não está em relação ao que mede. De 1999 a 2024 o teto da ANS composto deu 652% e o subitem do IPCA 660%. O que o IPCA não mede é a maioria do mercado: de dez/2014 a dez/2024 os coletivos subiram 217% e os contratos pequenos 301%, contra 135% do subitem e 75% do IPCA geral. O IBGE declara que acompanha só contratos individuais e familiares e dilui o reajuste em 12 meses.",
        "cuidado": "A base de coletivos inclui contratos comunicados com reajuste zero (de 32% dos beneficiários em 2005 a 5,5% em 2024); sem eles o composto de 2014-24 sobe a 248%. Beneficiários são somados por linha e podem repetir pessoas. Reajuste por faixa etária, que dobra a mensalidade ao longo da vida, não está em nenhuma das três medidas. Preço de um plano nomeado (ex.: Amil) não tem fonte pública contínua: só quatro tabelas de venda de 2006-10 no Wayback, sem série.",
    },
    "homic_n": {
        "o_que": "Quantas pessoas morreram por agressão (homicídio) em cada ano no Brasil, em número absoluto, segundo os atestados de óbito do Sistema de Informações sobre Mortalidade (DATASUS).",
        "como": "Soma dos óbitos classificados como agressão (CID-9 E960-E969 até 1995; CID-10 X85-Y09 desde 1996), por residência da vítima, via Ipeadata. Série anual, em linha.",
        "porque": "De 13,9 mil mortes em 1980 a 32 mil em 1990, 45,4 mil em 2000, 53 mil em 2010, o pico de 65,6 mil em 2017 e 42,6 mil em 2024. É o número de pessoas; a taxa por 100 mil, no indicador ao lado, desconta o crescimento da população.",
        "cuidado": "Mortes de 'intenção indeterminada' e por 'causa mal definida' ficam fora e variam por estado e ano; quando elas sobem, o homicídio registrado pode cair sem que a violência caia. Menor é melhor.",
    },
    "nascimentos": {
        "o_que": "Quantas pessoas nascem vivas no Brasil por ano, em quatro bases que nunca se emendam: o SINASC (declarações de nascido vivo, DATASUS, 1994+), o Registro Civil do IBGE (cartórios, 1984+, nascidos no ano e registrados no ano) e a estimativa da ONU (1950+).",
        "como": "Contagens publicadas; a ONU estima por modelo demográfico e, a partir de 2024, projeta. O ano corrente fica fora por estar incompleto.",
        "porque": "Nasceram cerca de 3,3 milhões por ano nos anos 60 e 70 (ONU), 3,2 milhões em 2000 (SINASC), 2,9 milhões em 2010 e 2,4 milhões em 2024: a queda de fecundidade é o fato demográfico do período.",
        "cuidado": "Registrados no ano incluem crianças nascidas antes (recuperação de sub-registro), por isso ficam acima dos nascidos no ano; o IBGE troca de tabela em 2003 (+8,9% nos 'ocorridos'). Sem leitura de melhor.",
    },
    "obitos": {
        "o_que": "Quantas pessoas morrem no Brasil por ano, todas as causas, em bases separadas: SIM (atestados de óbito, DATASUS, 1979+, CID-9 até 1995 e CID-10 desde 1996), Registro Civil do IBGE (cartórios, 1984+) e estimativa da ONU (1950+).",
        "como": "Contagens publicadas por ano de ocorrência; a ONU estima e, a partir de 2024, projeta. 2025 é preliminar e o ano corrente fica fora.",
        "porque": "Cerca de 1,0 milhão de mortes por ano de 1964 a 1994 (ONU, com população crescendo e mortalidade caindo), 1,1 milhão em 2010, 1,3 milhão em 2016, 1,56 milhão em 2020 e 1,83 milhão em 2021 (pandemia), 1,53 milhão em 2024. O número sobe com o envelhecimento mesmo quando a mortalidade por idade cai.",
        "cuidado": "Em 1980-2000 o SIM registra só 72% a 87% dos óbitos estimados pela ONU (sub-registro, maior no Norte e Nordeste); comparar SIM antigo com ONU mede cobertura, não mortalidade. Sem leitura de melhor: mais mortes pode ser mais gente e mais velhos.",
    },
}

PRODUTOS = {
    "arroz": "um quilo de arroz",
    "feijao": "um quilo de feijão",
    "carne_bovina": "um quilo de carne bovina",
    "pao_frances": "um quilo de pão francês",
    "leite": "um litro de leite",
    "acucar": "um quilo de açúcar",
    "cafe_em_po": "meio quilo de café em pó",
    "oleo": "uma embalagem de óleo de soja",
    "botijao_glp_13kg": "um botijão de gás de 13 kg",
    "gasolina_comum": "um litro de gasolina comum",
    "energia_residencial": "100 kWh de energia residencial",
    "onibus_sp_tarifa_basica": "uma passagem de ônibus em São Paulo",
}


def explica_produto(produto, fonte):
    """Explanation block for one product measured in hours of work."""
    nome = PRODUTOS[produto]
    return {
        "o_que": f"Quantas horas de trabalho ao salário mínimo (220 horas por mês) compram {nome}, com o preço médio do mês ({fonte}).",
        "como": "Preço do mês dividido pelo salário mínimo nominal do mês (Ipeadata) e multiplicado por 220. Candle anual: abre em dezembro anterior, fecha em dezembro, pavio nos meses. As outras linhas medem o mesmo produto em horas da renda per capita mediana (média dos decis 5 e 6) e do décimo mais rico (Banco Mundial PIP, anual): renda domiciliar por pessoa convertida a reais do ano, régua diferente de um salário.",
        "porque": "É preço relativo ao piso salarial, a medida que o bolso sente. Como o salário mínimo real dobrou desde 1994, quase tudo ficou mais barato em horas ao mínimo, mesmo com preços nominais subindo três ou quatro vezes; em horas da renda do décimo mais rico a queda é menor ou não existe.",
        "cuidado": "Menor é melhor. Preço de São Paulo (DIEESE) ou média nacional (ANP, ANEEL): não é custo de vida nem cesta. Nenhum produto tem elasticidade zero; o preço reage à demanda. Trocas de moeda e de metodologia estão no catálogo de quebras da coleta.",
    }


def explica_mundo(nome, refs):
    """Explanation block for one "Brazil and the world" series (amendment 01 §A)."""
    lista = ", ".join(refs)
    return {
        "o_que": f"{nome} no Brasil ao lado de {lista}, todos lidos da MESMA série da mesma fonte (Banco Mundial WDI ou PIP, UNODC, OMS/UNICEF, V-Dem via Our World in Data). Os grupos de comparação foram fixados antes dos números: mundo, América Latina e Caribe, países de renda média-alta e sete vizinhos.",
        "como": "Uma linha por referência, nos valores publicados pela fonte, sem ajuste. A leitura é a diferença Brasil menos referência: a aba 'Por governo' mostra o quanto essa diferença mudou do ano anterior à posse ao último ano do mandato, e a coleta guarda a média da diferença em cada mandato. Agregados do Banco Mundial (mundo, região, grupo de renda) são médias ponderadas pela população ou pelo PIB, conforme a fonte.",
        "porque": "Responde à pergunta que o dado só do Brasil não responde: o país andou sozinho ou com o mundo? O boom das commodities de 2003 a 2011, a crise de 2008, a recessão de 2015-16 e a pandemia mexeram com todos; o que sobra depois de comparar com os vizinhos é o que se pode discutir como diferença brasileira.",
        "cuidado": "Comparação descritiva: nenhuma causa é atribuída e não há ajuste de 'onda mundial'. A série da fonte internacional pode diferir da série nacional do mesmo conceito (deflatores, PPC, modelos da OIT); por isso ela só aparece aqui, ao lado das referências da mesma fonte, e nunca é emendada à série nacional. Dado faltante fica vazio.",
    }


EXPLICA_INDICE = {
    "o_que": "Um número só por mês e por ano, de 0 a 100, que resume as condições do país em 35 itens (núcleo) ou 39 (com o bloco de premissas econômicas), em 12 ou 13 áreas: preços, atividade e renda, trabalho, fiscal, pobreza e desigualdade, saúde, educação, segurança, moradia, ambiente, instituições, ciência e tecnologia (e premissas).",
    "como": "Cada item vira nota de 0 a 100: 0 é o pior valor do Brasil entre 1995 e 2024, 100 o melhor, com o sinal já virado (homicídio, inflação, dívida entram invertidos). A área é a média dos itens que têm dado no mês; o índice é a média das áreas com pesos iguais (o ajuste por importância efetiva não convergiu e o pré-registro manda declarar). Itens mensais entram pelo mês; anuais, como degrau. O candle anual abre em dezembro anterior e fecha em dezembro; o pavio é o pior e o melhor mês.",
    "porque": "Para responder a uma pergunta só, com regra escrita e selada antes do cálculo: em cada mandato, o país ficou mais perto ou mais longe do melhor que já teve? A robustez (10.000 sorteios de pesos) diz em que faixa o fechamento de cada mandato cai e se a ordem se mantém. Com o bloco de premissas (indústria, Estado, abertura, propriedade estatal) a ordem não muda.",
    "cuidado": "Não é nota de governo nem causalidade. Dez itens são tendências seculares (expectativa de vida, mortalidade infantil, PIB per capita) que sobem quase todo ano: um índice de 'distância ao melhor já visto' favorece quem governa depois. Anos com menos de 70% dos itens publicados ficam sem índice (1996, 1998, 2000); 2025 e 2026 só existem no cenário de último valor carregado, que não é o índice. Os pesos são juízo declarado, não verdade científica: o que é defensável é o procedimento e a robustez publicada.",
}
