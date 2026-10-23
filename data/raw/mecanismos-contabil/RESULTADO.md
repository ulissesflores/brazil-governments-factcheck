# Mecanismos contábeis, fiscais e estatísticos: o que mede, quanto e quem paga

Colheita de 2026-10-19. Pasta: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mecanismos-contabil/`. Sem opinião, sem nota, sem ranking e sem juízo de culpa: cada linha diz o mecanismo, a janela, quem aplicou, quem pagou, **quem decidiu** (`atribuicao`), a magnitude medida e a camada da evidência. Cadeia de hash: `manifest.jsonl` (94 linhas, `chain.py verify` = OK). Entregas: `mecanismos.csv` (31 linhas), `simetria-por-governo.csv` (180 linhas = 12 classes x 15 governos de `mandatos.csv`), `series/*.csv` (4 séries longas).

## 0. Resposta ao exemplo do Ulisses: "incluir tráfico de drogas no PIB"

**O Brasil NÃO incluiu tráfico de drogas no PIB publicado hoje (série de referência 2010).** Para drogas, a resposta é "não se aplica ao Brasil até 2026-10-19": a mudança está **planejada** na nova série (referência 2021) e **ainda não foi aplicada por nenhum governo**.

| evidência | camada | trecho literal | fonte |
|---|---|---|---|
| IBGE, Nota Metodológica nº 1 (SCN ref. 2021, v.1, out/2025) lista como novidade da base nova | dado | "novas estimativas de contrabando e jogos de azar; ... estimativa da comercialização de drogas, estimativa de medidas líquidas e o cálculo de autoprodução de software" | https://biblioteca.ibge.gov.br/visualizacao/livros/liv102216.pdf |
| mesma nota: cronograma | dado | "prevê a finalização e divulgação dos resultados depois das eleições de 2026, em 2027" | idem |
| nota do IBGE a O Povo (29/09/2026) | alegação (reprodução de nota por jornal) | "as discussões sobre a estimativa de comercialização de drogas ilícitas nas Contas Nacionais começaram em 2019. Em 2021 foi feita uma primeira estimativa teste de metodologia" e "os números brasileiros devem ser conhecidos a partir de 2028" | https://mais.opovo.com.br/colunistas/armando-de-oliveira-lima/2026/09/29/ibge-mede-o-peso-das-drogas-na-economia.html |
| Aos Fatos (17/09/2026): a mudança "está prevista para entrar em vigor em 2028"; começou a ser desenvolvida em 2023 | alegação | "Desde 2014 ... Itália, Reino Unido e Espanha passaram a contabilizar tráfico de drogas, prostituição e contrabando" | https://www.aosfatos.org/noticias/mudanca-calculo-pib-brasil-onu/ |
| ausência nas notas da série atual | dado (negativo) | busca por ilegal, ilícit, droga, entorpec, prostitu, contraband, clandestin em 21 das 22 notas metodológicas do SCN ref. 2010: **0 ocorrências para drogas e atividades ilegais**; 1 ocorrência de "contrabando" (Nota 19, ver abaixo) | `bruto/ibge-nm2010-*.pdf` |

Quatro ressalvas, que mudam o tom do texto de quem for citar:

1. **Contrabando já tem estimativa parcial na série atual.** Nota 19 (margens e impostos): "para o imposto de importação foram excluídos da base de cálculo os valores decorrentes das estimativas de contrabando". Não diz se isso entra no PIB nem quanto. A afirmação segura é sobre **drogas**, não sobre "atividades ilegais" em geral (MC02).
2. **Datas divergentes não reconciliadas**: a nota do IBGE diz 2027; O Povo e Aos Fatos dizem 2028. A página "IBGE esclarece SCN" (agência 48080) devolveu 403 e não foi lida.
3. **Atribuição**: `decisao_de_orgao_independente` (IBGE seguindo SNA 2008/2025; o processo é de 2023, com discussão desde 2019). Nenhuma evidência lida de interferência do governo. Pedido de informação na Câmara (RIC 2628/2026, 16/09/2026) é contexto de terceiros.
4. **Prática da UE (só contexto)**: ONS, "Revisions to GDP in Blue Book 2016": "improvements were implemented to the measurement of illegal activities in Blue Book 2014" (ESA 2010). Magnitude da inclusão no Reino Unido não coletada.

**Magnitude**: não medida (o IBGE não publicou estimativa do efeito). Qualquer número sobre "quanto o PIB sobe" seria invenção desta pasta.

## 1. Mecanismos documentados (`mecanismos.csv`)

| id | mecanismo (resumo) | tipo | janela | aplica | paga | atribuição | magnitude medida | camada |
|---|---|---|---|---|---|---|---|---|
| MC01 | PIB com tráfico de drogas | estatística | 2019-2027 | ninguém ainda | n/a | órgão independente | não medida | dado |
| MC04 | cessão onerosa: receita R$ 74,8 bi e capitalização Petrobras R$ 42,9 bi no primário | antecipação | 2010 | Lula 2º | Dilma e seguintes (indeterminado) | ato de governo | 1,93% do PIB de receita; líquido 0,82% | dado |
| MC05 | Fundo Soberano: -R$ 14,2 bi (2008) e +R$ 12,4 bi (2012) | contabilidade | 2008-2012 | Lula e Dilma | indeterminado | ato de governo | 0,46% e 0,26% do PIB | dado |
| MC06 | concessões e permissões: pico em 2019 | antecipação | 2019 | Bolsonaro | indeterminado | indeterminado | 1,26% do PIB (média 1997-2025: 0,26%) | dado |
| MC07 | pedaladas: atrasos a bancos públicos e FGTS | adiamento | 2013-2015 | Dilma | Dilma (quitou em dez/2015) | órgão de controle | ~R$ 40 bi (TCU), R$ 55,6 bi pago em dez/2015, R$ 72,4 bi em 2015 (1,21% do PIB) | controle |
| MC08 | adiantamentos CEF/FGTS/BNDES (2010-2014) | contabilidade | 2010-2014 | Lula (2010) e Dilma | Dilma | órgão de controle | R$ 37,5 bi sem registro no BGU | controle |
| MC09 | BGU 2014: retificação de RAP e contingenciamento | contabilidade | 2014 | Dilma | indeterminado | órgão de controle | R$ 185 bi de passivo subavaliado; R$ 28,54 bi sem contingenciar | controle |
| MC10 | abatimento PAC/PPI da meta, tetos em LDO | contabilidade | 2006-2015 | Lula e Dilma | indeterminado | decisão legislativa | tetos de R$ 3 bi (2006) a R$ 67 bi (2014) e, desde 15/12/2014, sem teto numérico | dado |
| MC11 | meta (art. 2 da LDO) alterada na vigência: 6 leis (2 por governo: Lula, Dilma, Temer); outras 4 leis só mudaram o teto de abatimento (MC10) | contabilidade | 2009-2017 | Lula, Dilma, Temer | indeterminado | decisão legislativa | 2015: de +R$ 66,3 bi para -R$ 48,9 bi; 2016: de +R$ 30,6 bi para -R$ 163,9 bi | dado |
| MC12/13 | Petrobras e Eletrobras fora da meta; LDO 2010 alterada em 30/12/2010 | contabilidade | 2009-2017 | Lula, Dilma, Temer | indeterminado | decisão legislativa | meta 2010 de 3,3% para 3,1% | dado |
| MC14-17 | restos a pagar no fim do mandato | adiamento | 2010-2025 | cada governo | o seguinte | indeterminado | R$ 128,9 / 185,7 / 189,6 / 255,1 / 391,5 bi (3,32 / 3,10 / 2,71 / 2,53 / 3,07% do PIB) | dado |
| MC18 | gasto tributário federal | contabilidade | 2007-2026 | todos | n/a | decisão legislativa | 3,60% a 4,89% do PIB | dado |
| MC19-22 | EC 95 (2016), ECs 113/114 (2021), EC 123 (2022), EC 126 (2022), LC 200 (2023) | contabilidade (regra fiscal) | 2016-2023 | Temer, Bolsonaro, Lula 3 | indeterminado | decisão legislativa | EC 123: R$ 41,25 bi de tetos (0,41% do PIB); EC 126: R$ 145 bi (1,33%) | dado |
| MC23 | Conta Movimento BB-BC e orçamento monetário | contabilidade | 1964-1986(88) | Castelo a Sarney | inflação/senhoriagem e dívida | ato de governo | resíduo 0,5 a 1,6% do PIB/ano por subperíodo; sinal troca em 1981-94 | literatura |
| MC25 | 1973: índice captou preço tabelado | represamento | 1973-74 | Médici | Geisel | ato de governo | IGP-DI 15,5% (1973) e 34,5% (1974); DIEESE-SP 26,68% | literatura |
| MC26/27 | Cruzado 1986; IPC represado 1987 e 1989 | represamento / estatística | 1986-1989 | Sarney | Sarney | ato de governo | coletas de 35 e 12 dias (1987), 51 e 11 dias (1989) | dado |
| MC28 | 1990-91: aluguel = BTN; IPC extinto | estatística | 1990-91 | Collor | indeterminado | ato de governo | não medida | dado |
| MC29-31 | média geométrica 1994; POF 1999-2020; PIB 2007 e 2015 | estatística | 1994-2020 | vários | n/a | órgão independente | ±0,5 p.p./ano (IPCA); +2% a +11% no nível do PIB | dado |

`tipo` conforme o pedido: antecipacao_de_receita, adiamento_de_despesa, contabilidade, represamento_de_preco, mudanca_de_regra_estatistica (as linhas completas usam esses termos exatos).

## 2. Contabilidade fiscal: o que a série do Tesouro mostra

Série anual do Governo Central (RTN, tab. 2.2 e 2.2-A, 1997-2025), em `series/rtn-resultado-primario-extraordinarias.csv`. **Não existe linha oficial "receita não recorrente" na planilha**; as colunas abaixo são **proxies deste dossiê** somando linhas oficiais (1.4.1 concessões e permissões, 1.4.8.1 operações com ativos, 1.4.2 dividendos) e subtraindo-as do resultado primário "acima da linha". Dividendos não são extraordinários por natureza; aparecem separados para quem decidir.

| governo | anos (n) | primario reportado | sem concessoes e ativos | sem concessoes, ativos e dividendos | peso concessoes+ativos | peso dividendos |
|---|---|---|---|---|---|---|
| Fernando Henrique Cardoso | 1997-2002 (6) | 1.39 | 0.92 | 0.74 | 0.47 | 0.18 |
| Lula (1o e 2o mandatos) | 2003-2010 (8) | 2.11 | 1.80 | 1.40 | 0.31 | 0.39 |
| Dilma Rousseff | 2011-2016 (6) | 0.04 | -0.20 | -0.52 | 0.24 | 0.32 |
| Michel Temer | 2017-2018 (2) | -1.80 | -2.25 | -2.34 | 0.45 | 0.10 |
| Jair Bolsonaro | 2019-2022 (4) | -2.75 | -3.24 | -3.67 | 0.49 | 0.43 |
| Lula (3o mandato) | 2023-2025 (3) | -0.98 | -1.07 | -1.56 | 0.09 | 0.49 |

Médias de % do PIB por governo; ano atribuído ao governo que o exerceu na maior parte dos dias. A média de Bolsonaro inclui 2020 (-9,77%). Cada coluna é um fato, não um juízo: a diferença entre "reportado" e "sem" é o peso da linha.

Fatos pontuais da série (R$ mi, RTN): 2010, operações com ativos 74.808 (1,93% do PIB; cessão onerosa, MC04); 2012, 12.400 (igual ao memorando do Fundo Soberano); 2019, concessões 93.281 (1,26%); 2022, dividendos 87.004 (0,86%).

**Restos a pagar** (Tesouro, Relatório de Avaliação dos RAP 2026, tab. 2; `series/restos-a-pagar-estoque-fim-de-ano.csv`): estoque inscrito em 31/12, R$ bi correntes e % do PIB.

| 31/12 do ano | R$ bi | % do PIB | último ano de |
|---|---|---|---|
| 2007 | 62,5 | 2,30 | (primeiro dado) |
| 2010 | 128,9 | 3,32 | Lula 1-2 |
| 2013 | 219,1 | 4,11 | maior % do PIB da série |
| 2014 | 228,0 | 3,95 | maior valor nominal até 2020 |
| 2015 | 185,7 | 3,10 | Dilma (31/12 mais próximo da saída) |
| 2018 | 189,6 | 2,71 | Temer |
| 2022 | 255,1 | 2,53 | Bolsonaro |
| 2025 | 391,5 | 3,07 | Lula 3 (em curso) |

Notas do próprio Tesouro: R$ 34,0 bi do aumento de 2018 para 2019 são mudança na sistemática de pagamento (ordem bancária), não fluxo; 82,7% da alta 2025/2026 é despesa financeira. O TCU registra em 2014 "retificação irregular dos Restos a Pagar não processados, subavaliando o Passivo Não Financeiro em R$ 185 bilhões" (MC09).

**Gasto tributário federal** (Receita Federal, DGT; `series/gastos-tributarios-federais.csv`): 3,95 / 3,78 / 3,65 / 3,60 / 3,68 / 4,15 / 4,66% do PIB em 2007-2013 (Ipea NT 19 citando a RFB), 4,30 / 4,32 / 4,67 / 4,89 / 4,88% em 2019-2023 (bases efetivas) e projeções PLOA 4,59 / 4,40 / 4,43% para 2024-2026. Lacunas: 2003-2006, 2014-2018 e tudo antes de 2003.

**Pedaladas** (MC07): TCU, Acórdão 3297/2015 (09/12/2015, TC 021.643/2014-8): atrasos de repasses em 2013-2014 "aproximadamente R$ 40 bilhões"; Fazenda: R$ 55,6 bi do passivo do Acórdão 825/2015 pagos em dez/2015, R$ 72,4 bi no ano. A LDO 2015 foi alterada em 03/12/2015 (Lei 13.199) para permitir reduzir a meta em até R$ 57,013 bi por esse pagamento: quem pagou foi o próprio governo que criou o passivo. Parecer prévio das contas de 2014 (TC 005.335/2015-9, 07/10/2015): recomenda rejeição, a primeira desde 1937 segundo o TCU. **O "Acórdão 2.461/2015" do pedido não foi confirmado**; os números da cadeia são 825/2015 e 3297/2015.

**Regras alteradas perto de eleições (2022)**: EC 113 e 114 (dez/2021) mudaram o indexador do teto e limitaram precatórios; a IFI (RAF 60, jan/2022) registra deficit projetado de R$ 106,2 bi (1,1% do PIB) contra R$ 79,4 bi do Orçamento, com Auxílio Brasil de R$ 54,6 bi e emendas de relator de R$ 16,5 bi "possibilitados". EC 123 (14/07/2022): despesas do estado de emergência fora da meta e do teto, soma dos limites R$ 41,25 bi (0,41% do PIB). EC 126 (21/12/2022): limite de 2023 acrescido de R$ 145 bi (1,33% do PIB), fora da meta. Todas `decisao_legislativa`.

## 3. Antes de 1988

Ayres, Garcia, Guillen e Kehoe (NBER w25421, 2018, cópia em `../monetario/referencias/ayres.txt`) descrevem que o governo "operated at least three budgets": o discutido no Congresso, o orçamento monetário controlado pelo Conselho Monetário Nacional e o das estatais. A Conta Movimento entre BB e BC foi congelada em 1986 e substituída pela Conta de Suprimentos Especiais até 1988. O Decreto 92.452 (10/03/1986) criou a STN, que "incorporou as funções fiscais até então exercidas pelo Banco Central e pelo Banco do Brasil" (Tesouro). Magnitude disponível: o resíduo da identidade orçamentária do artigo, 0,5 (1960-64), 1,1 (1965-72), 1,6 (1973-80) e -4,5% do PIB/ano (1981-94). É por **subperíodo**, não por mandato, e muda de sinal; por isso na simetria aparece como `medido_no_subperiodo_nao_no_governo` (Ms). Resultado primário oficial antes de 1991: sem série (já registrado em `../monetario/RESULTADO.md`).

## 4. Estatística: quem decidiu

| caso | quem decidiu | evidência | magnitude |
|---|---|---|---|
| 1973: índices registraram preços tabelados | governo tabelou; o cálculo era da FGV (sem evidência lida de interferência na fórmula) | Simonsen, 1977, relatado por Bastos Marques (RBE): "Os índices de preços, entretanto, registraram os preços tabelados e não aqueles praticados no mercado negro" | dez/72-dez/73: FGV/Guanabara 13,71%; Bolsa SP 14,05%; UFMG/BH 13,08%; DIEESE/SP 26,68%; Curitiba 33,33%; IGP-DI 15,5%; IGP-DI 1974: 34,5% |
| 1986-87-89: IPC "represado" | governo (decretos-lei e portarias) | IBGE: coletas de 35 e 12 dias (jun-jul/1987) e 51 e 11 dias (jan-fev/1989) | em dias, não em p.p. |
| 1990-91: aluguel do IRVF = BTN; IPC extinto | governo (MP 189, Lei 8.177/8.178, "orientação ministerial") | IBGE, apêndice SNIPC | não medida |
| 1994, 1999, 2006, 2012, 2014, 2018, 2020: média geométrica, pesos POF, cobertura | IBGE | BCB EE 70 e RI dez/2019 (via `../quebras/`) | +0,71 e +0,06 (1999); +0,40 e -0,34 (2006); -0,49 e -0,56 (2012) p.p./ano: o sinal troca |
| 2007 e 2015: ano-base do PIB | IBGE | releases 132 e 972 (via `../quebras/`) | nível +7,1% a +10,9% (2007); +2,1% (2015) |

O "relatório secreto do Banco Mundial" de 1977 (citado por Atlas FGV e Memória DIEESE) **não foi achado**; a cifra de 22,5% que um blog atribui ao Banco foi ignorada.

## 5. Simetria por governo (`simetria-por-governo.csv`)

Legenda: M = medido; Ms = medido no subperíodo, não no governo; E = evento documentado; NA = não se aplica (razão na linha); NE = não encontrado nas fontes listadas (não prova ausência); SD = sem dado nesta colheita.

| governo | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Castelo Branco | SD | SD | SD | NA | NA | SD | SD | SD | Ms | SD | SD | SD |
| Costa e Silva | SD | SD | SD | NA | NA | SD | SD | SD | Ms | SD | SD | SD |
| Junta Militar | SD | SD | SD | NA | NA | NA | SD | SD | Ms | SD | NA | NA |
| Medici | SD | SD | SD | NA | NA | SD | SD | SD | Ms | SD | E | SD |
| Geisel | SD | SD | SD | NA | NA | SD | SD | SD | Ms | SD | E | SD |
| Figueiredo | SD | SD | SD | NA | NA | SD | SD | SD | Ms | SD | SD | SD |
| Sarney | SD | SD | SD | SD | SD | SD | SD | SD | Ms | SD | M | SD |
| Collor | SD | SD | SD | SD | SD | SD | SD | SD | NA | SD | M | M |
| Itamar Franco | SD | SD | SD | SD | SD | SD | SD | SD | NA | SD | M | NE |
| Fernando Henrique Cardoso | NA | M | M | SD | NE | SD | SD | SD | NA | SD | M | M |
| Lula (1o e 2o mandatos) | NA | M | M | E | M | M | M | E | NA | SD | M | M |
| Dilma Rousseff | NA | M | M | E | M | M | M | M | NA | SD | M | M |
| Michel Temer | NA | M | M | E | NE | M | SD | M | NA | E | M | NE |
| Jair Bolsonaro | NA | M | M | E | SD | M | M | M | NA | E | M | NE |
| Lula (3o mandato) | NA | M | M | SD | SD | M | M | M | NA | E | NE | NE |

| classe | nome |
|---|---|
| C01 | atividade_ilegal_no_PIB |
| C02 | concessoes_e_operacoes_com_ativos_pct_pib |
| C03 | dividendos_e_participacoes_pct_pib |
| C04 | meta_de_resultado_primario_alterada_na_vigencia |
| C05 | teto_de_abatimento_da_meta_por_investimento_pac_ppi |
| C06 | restos_a_pagar_estoque_em_31_12_do_ultimo_ano_do_mandato |
| C07 | gasto_tributario_federal_pct_pib |
| C08 | passivos_do_tesouro_com_bancos_publicos_e_fundos |
| C09 | transferencias_BC_BB_e_operacoes_fora_do_orcamento |
| C10 | emenda_ou_lei_complementar_que_altera_regra_fiscal |
| C11 | indice_de_precos_ato_de_governo_barra_orgao_independente |
| C12 | troca_de_metodo_ou_ano_base_do_PIB |

O que isso diz sobre cobertura, e só isso: C02, C03 e C06 cobrem 6 e 5 dos 15 governos; C07, 4 (parcial); C09 a C12 cobrem eventos, não valores comparáveis. **Antes de 1997 praticamente todas as classes fiscais estão em SD**: a comparação 1964-2026 pedida só é possível hoje para C09 (subperíodos) e C11 (eventos). Classes C02 a C08 não devem ser lidas como "o governo sem número não fez": SD não significa zero.

## 6. O que NÃO foi achado, limites e becos

- **Receita "não recorrente" oficial**: não há linha na planilha RTN; usei proxy (soma de linhas oficiais). Não sei se o Tesouro publica essa categoria fora da planilha; não procurei.
- **Privatizações**: não localizei linha de venda de empresas na tabela do RTN; não decidi se entram no primário. Concessões e operações com ativos estão medidas.
- **Resultado primário do setor público consolidado** comparado às metas: não coletado; só Governo Central. Sem comparação meta x resultado.
- **Valor efetivamente abatido** da meta (PAC/PPI) por ano: não coletado; só o teto legal.
- **LDOs 1995-2000 e 2018-2026**, leis modificadoras de 2001-2006 e 2018+, Decreto Legislativo de calamidade 2020 e exclusões de 2024-2026: não lidos.
- **Restos a pagar antes de 31/12/2007**: sem série oficial achada (Siga Brasil não consultado).
- **Gasto tributário**: lacunas listadas acima; o blog do IBRE cita 2,1% do PIB (2002) e 6,9% (2024 projetado), mas é o total federal + estadual; fora da série federal.
- **Pré-1988**: sem número por mandato; resíduo de Ayres por subperíodo.
- **IFI RAF 60 original no Senado**: a URL devolveu página HTML de verificação de segurança; guardada no `bruto/regra-fiscal/ifi-raf60-jan2022-orcamento.pdf` (que **não é PDF**, linha 'nota' do manifest explica) e substituída pela cópia do Poder360. Os R$ 112,6/117,9 bi de "espaço no teto" que a imprensa cita não foram verificados.
- **Agência IBGE (48080) e TCU (pesquisa de acórdãos)**: 403 ou bloqueio; lidos os documentos equivalentes (notas do TCU, parecer prévio na Câmara, nota da Fazenda por republicação).
- **Atlas FGV verbete 3036**: falha TLS no Python; baixado por curl e registrado com `add-local`.
- **Brasil x UE**: magnitude da inclusão de drogas no Reino Unido não coletada.
- **Atribuição**: `atribuicao` só é `ato_de_governo` quando o próprio texto lido diz que o governo determinou (decretos, MP, tabelamento reconhecido pelo ministro). Para IBGE e BCB, `decisao_de_orgao_independente` sem evidência lida de interferência.
- **Lei 13.291 (25/05/2016)** foi assinada por Michel Temer como interino, no período em que `mandatos.csv` ainda atribui o mandato a Dilma (até 31/08/2016): atribuída a Temer e marcada.

Becos (hipótese descartada): "Acórdão 2.461/2015" como o das pedaladas (não achado); 22,5% do Banco Mundial para a inflação de 1973 (fonte única de blog, descartada); série de gastos tributários 2003-2018 em um único arquivo da Receita (não existe nas páginas lidas); série de RAP desde 2000 no Tesouro (a base aberta começa em 2022; a tabela histórica dos relatórios começa em 2007).

## 7. Reprodução

```bash
cd /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mecanismos-contabil
python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py verify .
python3 -I scripts/xlsx_para_csv.py bruto/tesouro-rtn-serie-historica-jul26.xlsx derivado/rtn   # xlsx -> csv (stdlib)
python3 -I scripts/serie_rtn.py .; python3 -I scripts/serie_rap.py .; python3 -I scripts/serie_gt.py .; python3 -I scripts/serie_igpdi.py .
python3 -I scripts/montar_mecanismos.py .
python3 -I scripts/montar_simetria.py . /Users/ulissesflores/Developer/brazil-governments-factcheck/data/curated/mandatos.csv
```

`derivado/` (texto de PDFs e HTML, CSV das planilhas) é recriável a partir de `bruto/` e não entra na cadeia. Os scripts leem só bruto e derivado, sem rede, com `python3 -I`. `pdftotext` gera os .txt; `html_para_txt.py` os HTMLs.
