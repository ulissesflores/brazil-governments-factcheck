# Pré-registro, emenda 08: segunda rodada da camada de literatura (busca por relevância em título e resumo)

Data: 2026-10-22, mesmo dia da emenda 07 e DEPOIS de a rodada da emenda 07 ter sido executada e
guardada (bruto hasheado em `literatura-fase3/`, resultado em `series/emenda07/`). Esta emenda não
reescreve a 07: declara o que a rodada 07 mostrou e fixa a rodada 08 antes de executá-la. As duas
rodadas ficam publicadas.

## A. O que a rodada 07 mostrou (números, não juízo)

40 consultas, 1.329 trabalhos distintos, 7 incluídos. Motivos de exclusão: 384 "não é sobre o
Brasil", 489 quartil 2 a 4, 300 periódico fora do SJR, 106 sem desenho no resumo, 30 sem DOI, 13
sem resumo. Causa visível na lista: o `search` do OpenAlex casa texto completo e a ordenação por
citações traz trabalhos muito citados que só tangenciam as palavras da consulta (Fujimori, dividendos
bancários, catálise química); os artigos sobre os episódios ficam abaixo do teto de 40. A regra
"citações como corte" (07 §B3 2) era a limitação declarada em 07 §B6 e se confirmou.

## B. Rodada 08 (coleta `literatura-fase3`, prefixo `openalex8-`)

Igual à 07 em tudo que não está listado aqui (episódios §B2, inclusão a, b, c, e; extração §B4;
página §B5; limitações §B6).

1. Consulta: `works?filter=title_and_abstract.search:<consulta>,type:article|review&sort=relevance_score:desc&per_page=100`. A busca casa só título e resumo, e a ordem é a relevância do OpenAlex, não citações.
2. Teto: 100 trabalhos por consulta; `meta.count` fica no bruto.
3. Passo d: a lista de desenhos da 07 mais `difference in differences`, `differences in differences`, `triple differences`, `two-way fixed effects`, `quasi-experimental`, `quasi-experiment`, `counterfactual`, `causal effect`, `causal effects`, `regression kink`, `bunching`, `quase-experimental`, `contrafactual`, `efeito causal`, `efeitos causais`; siglas `DiD`, `RDD`, `RCT`, `IV`, `DSGE`, `VAR model`, casadas como escritas.
4. Resumo ausente no OpenAlex: antes de reprovar, o registro do Crossref é consultado e o campo `abstract` do Crossref, se existir, é usado nos passos c e d (com a marca `resumo: Crossref` no campo `desenho`). Só então o motivo `sem resumo` se aplica.
5. Tudo o mais igual: lista completa com motivo, nenhuma seleção à mão, reprodução a partir do bruto.

## C. O que não muda

A camada continua fora do índice; sem nota, soma ou veredito. A rodada 07 permanece publicada
como evidência do protocolo que falhou e do porquê.
