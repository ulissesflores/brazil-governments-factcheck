# Pré-registro, emenda 09: terceira rodada da camada de literatura (consultas curtas, teto 200)

Data: 2026-10-22, depois de executada e guardada a rodada 08 (bruto hasheado `openalex8-*`, saída em
`series/emenda08/`). Não reescreve as emendas 07 e 08; as três rodadas ficam publicadas, cada uma com
seus números.

## A. O que a rodada 08 mostrou

40 consultas em título e resumo, 532 trabalhos distintos, 14 incluídos. A busca `title_and_abstract.search`
exige todas as palavras da consulta no título ou no resumo: consultas de 5 a 7 palavras devolveram
0 a 22 trabalhos em 29 das 40 chamadas (episódios 01, 02, 05, 06, 07, 09, 10, 11, 12, 13, 17, 18, 19, 20
com menos de 20 em inglês). O corte de 100 nunca foi atingido, salvo em "Minha Casa Minha Vida" em
português (191). Exclusões: 258 periódico fora do SJR (periódicos e repositórios brasileiros sem SJR),
166 sem DOI, 52 quartil 2 a 4, 28 sem desenho, 7 não é sobre o Brasil, 6 sem resumo. A rede ficou
estreita demais, não o filtro: a consulta é que não alcança a literatura.

## B. Rodada 09 (prefixo `openalex9-`)

Igual à 08 em tudo que não está listado aqui (passos a a e, desenhos ampliados, resumo do Crossref,
extração, página, limitações).

1. Consultas curtas, o nome próprio do episódio ou o par política + Brasil, fixadas aqui:

| # | Inglês | Português |
|---|---|---|
| 01 | Plano Real | Plano Real |
| 02 | inflation targeting Brazil | metas de inflação Brasil |
| 03 | Fiscal Responsibility Law Brazil | Lei de Responsabilidade Fiscal |
| 04 | Bolsa Familia | Bolsa Família |
| 05 | minimum wage Brazil | salário mínimo Brasil |
| 06 | commodity boom Brazil | commodities Brasil crescimento |
| 07 | Brazil 2008 crisis | crise de 2008 Brasil |
| 08 | Minha Casa Minha Vida | Minha Casa Minha Vida |
| 09 | BNDES | BNDES |
| 10 | payroll tax Brazil | desoneração da folha |
| 11 | Brazil recession 2015 | recessão 2015 Brasil |
| 12 | Lava Jato | Lava Jato |
| 13 | spending cap Brazil | teto de gastos |
| 14 | labor reform Brazil | reforma trabalhista |
| 15 | pension reform Brazil | reforma da previdência |
| 16 | Auxilio Emergencial | Auxílio Emergencial |
| 17 | Amazon deforestation policy | desmatamento Amazônia política |
| 18 | Pix Brazil | Pix Banco Central |
| 19 | fiscal framework Brazil | arcabouço fiscal |
| 20 | cash transfer Brazil 2023 | Bolsa Família 2023 |

2. `per_page=200` (máximo da API); teto 200 por consulta, ordem por relevância; `meta.count` no bruto.
3. Tudo o mais igual à 08. A consulta curta devolve mais trabalhos fora do tema; os passos b (Q1), c
   (Brasil) e d (desenho) são o filtro, e a lista com motivo continua completa.

## C. Regra para rodadas futuras

Uma rodada nova só por emenda nova, sempre depois de a anterior estar guardada e com os números
escritos. A escolha das consultas nunca olha para QUAIS artigos apareceram, só para QUANTOS a chamada
devolveu; esta emenda cita apenas contagens.
