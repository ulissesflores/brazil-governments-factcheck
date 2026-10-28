# Pré-registro, emenda 07: camada de literatura por governo e candidatos a item

Data: 2026-10-22. Autorização do autor no mesmo dia ("vamos fazer isso sim, com certeza; faça, colete").
Selada na cadeia `data/raw/preregistro/manifest.jsonl` (seq 10) ANTES de qualquer busca. Rascunho
anterior: `PREREGISTRATION-EMENDA-07-RASCUNHO.md` (mantido, não selado). Emendas anteriores não
são reescritas; esta só acrescenta.

## A. O que a página já faz e o que esta emenda acrescenta

A v21 (2026-10-22) lê cada mandato em três camadas descritivas, todas de regras já seladas: o
índice e os itens que mais o moveram (fase 2 §10), o Brasil contra a América Latina na mesma fonte
(emenda 01 §A) e cada indicador na sua unidade (emenda 05). Nenhuma delas diz POR QUE: nenhuma
atribui o movimento a uma política. Esta emenda acrescenta a única camada que pode falar de
causa com honestidade: o que a literatura revisada por pares mediu sobre políticas e episódios de
cada mandato, com desenho de identificação declarado pelos próprios autores.

## B. Camada de literatura por governo (coleta `literatura-fase3`)

### B1. Pergunta por mandato

Para cada mandato de 1995 a 2024 (FHC, Lula 1-2, Dilma, Temer, Bolsonaro, Lula 3): quais artigos
revisados por pares estimam o efeito de uma política ou episódio DESSE mandato sobre um resultado
que o índice mede (renda, pobreza, desigualdade, emprego, saúde, educação, segurança, ambiente,
instituições, fiscal, preços)?

### B2. Episódios (lista fechada; episódio novo exige nova emenda)

| # | Episódio | Mandato(s) | Consulta em inglês | Consulta em português |
|---|---|---|---|---|
| 01 | Plano Real e estabilização | FHC (e Itamar, contexto) | Plano Real stabilization Brazil inflation effect | Plano Real estabilização inflação efeito |
| 02 | Metas de inflação e câmbio flutuante (1999) | FHC | Brazil inflation targeting floating exchange rate effect | metas de inflação câmbio flutuante Brasil efeito |
| 03 | Lei de Responsabilidade Fiscal (2000) | FHC | Brazil Fiscal Responsibility Law effect municipalities | Lei de Responsabilidade Fiscal efeito municípios |
| 04 | Bolsa Escola e Bolsa Família (2001-) | FHC, Lula 1-2, Dilma | Bolsa Familia impact evaluation Brazil | Bolsa Família avaliação de impacto |
| 05 | Valorização do salário mínimo (2005-) | Lula 1-2, Dilma | Brazil minimum wage increase inequality employment effect | salário mínimo Brasil desigualdade emprego efeito |
| 06 | Boom de commodities e crescimento 2003-11 | Lula 1-2 | Brazil commodity boom growth terms of trade | boom de commodities Brasil crescimento termos de troca |
| 07 | Crise de 2008 e resposta | Lula 1-2 | Brazil 2008 financial crisis response credit public banks | crise de 2008 Brasil bancos públicos crédito resposta |
| 08 | Minha Casa Minha Vida (2009-) | Lula 1-2, Dilma | Minha Casa Minha Vida housing program impact | Minha Casa Minha Vida impacto |
| 09 | BNDES subsidiado e conteúdo local (2008-14) | Lula 1-2, Dilma | BNDES subsidized credit firms effect Brazil | BNDES crédito subsidiado efeito empresas |
| 10 | Desonerações e nova matriz econômica (2011-14) | Dilma | Brazil payroll tax exemption employment effect | desoneração da folha emprego efeito Brasil |
| 11 | Recessão de 2014-16 e suas causas | Dilma, Temer | Brazil 2014 2016 recession causes | recessão brasileira 2014 2016 causas |
| 12 | Lava Jato e efeitos econômicos (2014-18) | Dilma, Temer | Lava Jato corruption investigation economic effects Brazil | Lava Jato efeitos econômicos |
| 13 | Teto de gastos (2016) | Temer, Bolsonaro | Brazil spending cap constitutional amendment 95 effect | teto de gastos emenda constitucional 95 efeito |
| 14 | Reforma trabalhista (2017) | Temer, Bolsonaro | Brazil 2017 labor reform effect employment | reforma trabalhista 2017 efeito emprego |
| 15 | Reforma da Previdência (2019) | Bolsonaro | Brazil 2019 pension reform effect | reforma da previdência 2019 efeito |
| 16 | Pandemia, Auxílio Emergencial e vacinação (2020-21) | Bolsonaro | Brazil Auxilio Emergencial cash transfer pandemic effect | Auxílio Emergencial pandemia efeito |
| 17 | Desmatamento e fiscalização (2004-24) | Lula 1-2, Dilma, Temer, Bolsonaro, Lula 3 | Amazon deforestation enforcement policy effect Brazil | desmatamento Amazônia fiscalização política efeito |
| 18 | Pix e autonomia do Banco Central (2020-21) | Bolsonaro | Pix instant payments Brazil effect | Pix pagamentos instantâneos efeito |
| 19 | Arcabouço fiscal (2023) | Lula 3 | Brazil 2023 fiscal framework effect | arcabouço fiscal 2023 efeito |
| 20 | Bolsa Família 2023 e transferências recentes | Lula 3 | Brazil cash transfer 2023 Bolsa Familia effect | Bolsa Família 2023 efeito |

### B3. Protocolo de busca (fixado antes de buscar; executado por código, não por leitura humana)

1. Base de busca: OpenAlex (API pública, `works?search=<consulta>&filter=type:article|review&sort=cited_by_count:desc&per_page=40`, com `mailto`), uma chamada por consulta, resposta inteira salva em `bruto/` e hasheada. Base de confirmação: Crossref (`works/<doi>`, polite pool com `mailto` e pausa entre chamadas), registro salvo e hasheado, só para os trabalhos que passam os passos a a d. Nenhuma lista de memória. Nenhum filtro de "tem resumo" na API: tudo que a consulta devolve entra na lista.
2. Teto: 40 trabalhos por consulta (os mais citados); 2 consultas por episódio; o corte é declarado por consulta (`total_count` da API fica no bruto).
3. Inclusão, nesta ordem, cada passo com o motivo gravado quando reprova:
   a. tem DOI (`sem DOI`);
   b. o periódico (qualquer ISSN que o OpenAlex devolve, normalizado sem hífen e com X maiúsculo, contra a coluna `Issn` do SJR normalizada do mesmo jeito) está no SJR, edição 2024 (`referencias-fase2/bruto/scimago-journalrank-wayback-20251026.csv`, o mesmo arquivo da fase 2), com `SJR Best Quartile = Q1` (`periódico fora do SJR 2024` | `quartil Qn`); a edição do ano de publicação não foi obtida e isso fica declarado (limitação);
   c. título ou resumo contém `Brazil`, `Brazilian`, `Brasil` ou `brasileir` (`não é sobre o Brasil`);
   d. existe resumo no OpenAlex (`sem resumo no OpenAlex`, motivo distinto: não é "sem desenho") e o resumo reconstruído do índice invertido contém pelo menos uma expressão da lista de desenhos, casada em limite de palavra e sem distinguir maiúsculas, exceto as siglas, que são casadas como escritas: `difference-in-differences`, `differences-in-differences`, `diff-in-diff`, `regression discontinuity`, `instrumental variable`, `instrumental variables`, `synthetic control`, `randomized`, `randomised`, `natural experiment`, `event study`, `event-study`, `fixed effects`, `fixed-effects`, `panel data`, `propensity score`, `matching estimator`, `structural model`, `general equilibrium`, `calibrated`, `calibration`, `vector autoregress`, `DSGE`, `VAR model`, `diferenças em diferenças`, `diferenças-em-diferenças`, `descontinuidade`, `variável instrumental`, `variáveis instrumentais`, `controle sintético`, `experimento natural`, `efeitos fixos`, `dados em painel`, `escore de propensão`, `equilíbrio geral` (`sem desenho declarado no resumo`);
   e. o registro do Crossref existe e tem `type = journal-article` (`Crossref: tipo X` | `Crossref sem registro`).
   Working papers, relatórios e livros ficam fora por construção (ISSN no SJR + Crossref `journal-article`); um artigo de revisão em periódico Q1 cujo resumo cite um desenho da lista entra (por isso `type:article|review`), e o campo `desenho` mostra o que foi encontrado.
4. Tudo que as consultas devolvem é listado em `series/literatura_todos.csv` com `status` (`incluido` | `excluido`) e `motivo`. Não há seleção à mão depois da lista. Um trabalho devolvido por mais de uma consulta aparece uma vez, com todos os episódios.
5. Reprodutibilidade: a partir do `bruto/` hasheado, nunca de uma nova consulta (o OpenAlex muda de edição como o Ipeadata; ver NEG do STATE).

### B4. Extração por artigo (campos fixos, de código)

`chave, doi, openalex_id, titulo, autores, periodico, issn, ano, quartil_sjr, sjr_edicao, citacoes_openalex,
episodios, mandatos, desenho (expressões encontradas), frases_resultado (até 2 frases do resumo que contêm,
em limite de palavra e sem distinguir maiúsculas, uma das expressões: effect, effects, impact, impacts,
increase, increased, increases, decrease, decreased, reduce, reduced, reduces, reduction, raise, raised,
cause, caused, led to, associated with, efeito, efeitos, impacto, aumento, aumentou, redução, reduziu,
diminuiu, causou), status, motivo`. Nenhum campo é inferido: tudo vem do
registro do OpenAlex ou do Crossref. O resumo inteiro fica no bruto (hasheado), não na página.

### B5. O que a página mostra e o que não mostra

Aba própria "Estudos": por episódio e por mandato, a lista dos artigos incluídos com título (link
do DOI), autores, periódico, ano, desenho encontrado e as frases de resultado entre aspas; e, por
episódio, a lista dos excluídos com o motivo. NÃO há nota, soma, contagem de "estudos a favor" nem
veredito: a camada diz o que foi medido e como, e o leitor julga. A ausência de artigo Q1 sobre um
episódio é dita como ausência. Na aba "Por governo", cada cartão mostra só quantos artigos
incluídos tocam o mandato e leva à aba, sempre com a frase de que o número reflete os anos
decorridos desde o mandato e os episódios declarados, nunca a qualidade do governo nem o sentido
dos resultados.

### B6. Limitações declaradas

Citações como ordem de corte favorecem artigos antigos e em inglês; a consulta em português
compensa em parte. A lista de desenhos é por palavra, não por leitura: um artigo que descreve o
desenho sem nenhuma dessas expressões fica fora, e um que só as menciona entra; o campo `desenho`
deixa o leitor ver o que foi encontrado. Quartil da edição 2024 do SJR, não do ano de publicação.
Editoras que não cedem o resumo ao OpenAlex (parte da Elsevier e da Wiley) ficam subcontadas: o
motivo `sem resumo no OpenAlex` aparece na lista para que o leitor veja o tamanho desse buraco.

## C. Candidatos a item e a contexto (três portas da fase 2 §2; nada entra sem elas; nenhuma coleta disparada por esta emenda)

| Candidato | Fonte | Porta de direção (Q1 a confirmar) | Destino provável |
|---|---|---|---|
| Investimento público / PIB | STN, IBGE SCN | literatura de crescimento e capital público | item N se Q1 confirmar; senão contexto |
| Crédito ao setor privado / PIB | BCB SGS | direção contestada (Arcand et al. 2015 já na lista) | contexto |
| Inadimplência do crédito | BCB SGS | menor é melhor (estabilidade financeira) | item N candidato |
| Risco-país (EMBI+ Brasil) | JP Morgan via Ipeadata 1994+ | menor é melhor (custo de capital) | item N candidato |
| Câmbio real efetivo | BCB | sem direção | contexto |
| Termos de troca | FUNCEX/Ipeadata | sem direção; "motor externo" da emenda 01 §A5 | contexto, ao lado do índice |
| Anos médios de estudo 25+ | IBGE | maior é melhor | já previsto na fase 2 §4; verificar por que não pontua |
| PISA (2000+) | OCDE | maior é melhor | item N candidato (trienal) |
| Mortalidade por causas evitáveis | DATASUS | menor é melhor | item N candidato |
| População carcerária por 100 mil | Senappen | sem direção acordada | contexto |
| Emissões de CO2 per capita | Global Carbon Project | direção contestada para renda média | contexto |
| Água, esgoto, internet, informalidade, analfabetismo 2016+ | PNAD Contínua | param em 2014/2015 porque a PNAD Contínua não se sobrepõe à PNAD e §8 proíbe emendar | decisão pendente: (a) manter o corte e declarar (hoje); (b) fonte alternativa contínua (SNIS 1995+) como item separado; (c) nada |

## D. O que esta emenda não muda

Balizas, pesos, agregação, cobertura, encadeamento e as duas camadas N e P ficam como na fase 2.
A camada de literatura não entra no índice.
