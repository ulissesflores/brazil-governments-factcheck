# EMENDA-12: instituições na camada de literatura (autonomia do Banco Central, regras fiscais, imprensa, poderes)

Data: 2026-10-25. Selada na cadeia `preregistro/manifest.jsonl` ANTES de qualquer consulta da rodada 11. Modifica a EMENDA-07 §B2 (lista de episódios), como fizeram a EMENDA-10 e a rodada 10, e nada mais.

## A. Motivo (declarado antes de buscar)

Ao fechar o título do artigo ("Qual foi o melhor governo do Brasil? O que os dados públicos respondem e o que não respondem"), o editor pediu, em 2026-10-25, que a resposta desde o Plano Real trouxesse o que se sabe sobre o piso institucional: a hipótese dele é que a autonomia do Banco Central e os limites legais de gasto "de certa forma impedem de ficar pior", e pediu também um indicador de liberdade de imprensa e de independência dos poderes. Pelo pré-registro da fase 2 (§1), causalidade fica com o leitor e a única camada que fala de causas o faz pela boca de autores de estudos revisados por pares (EMENDA-07). A hipótese do editor, portanto, NÃO é afirmada pela página nem pelo artigo: ela vira episódios declarados, e o que passar pelo filtro a-e é citado, favorável ou não. Os episódios 02 (metas de inflação), 03 (LRF), 13 (teto) e 19 (arcabouço) já existem; na rodada 10 passaram 0, 0, 0 e 1 estudos. O episódio 18 consulta só o Pix, embora o nome cite a autonomia do Banco Central. Esta emenda acrescenta consultas que nomeiam a classe (independência do banco central; regras fiscais) e dois conceitos ausentes (imprensa; poderes). A escolha das consultas, como nas rodadas anteriores, não olhou para quais artigos aparecem: as oito consultas abaixo são as primeiras e únicas desta rodada.

## B. Episódios novos (numeração continua a da EMENDA-10)

| Nº | Episódio | Mandatos | Consulta EN | Consulta PT |
|---|---|---|---|---|
| 24 | Autonomia do Banco Central: de fato desde as metas (1999) e de direito pela LC 179 (2021) | fhc, lula12, dilma, temer, bolsonaro, lula3 | `central bank independence Brazil` | `autonomia do Banco Central` |
| 25 | Regras fiscais como classe: LRF (2000), teto de gastos (2016) e arcabouço (2023) | fhc, lula12, dilma, temer, bolsonaro, lula3 | `fiscal rules Brazil` | `regras fiscais Brasil` |
| 26 | Liberdade de imprensa e de expressão (1995-) | fhc, lula12, dilma, temer, bolsonaro, lula3 | `press freedom Brazil` | `liberdade de imprensa Brasil` |
| 27 | Independência judicial e separação de poderes (1995-) | fhc, lula12, dilma, temer, bolsonaro, lula3 | `judicial independence Brazil` | `independência judicial Brasil` |

Os mandatos listados são os anos em que o episódio esteve em curso; a contagem por mandato continua a refletir anos decorridos e episódios declarados, nunca a qualidade do governo nem o sentido dos resultados (EMENDA-07 §B5). Um estudo devolvido por dois episódios conta uma vez, com os dois números.

## C. Protocolo da rodada 11

1. Parâmetros idênticos aos da EMENDA-09 §B e da rodada 10: `filter=title_and_abstract.search`, tipo `article|review`, ordem por relevância, teto 200 por consulta, lista de desenhos e siglas da EMENDA-08, resumo do Crossref quando o OpenAlex não cede, passos de inclusão a-e da EMENDA-07 §B3.
2. A rodada 11 = os 23 episódios da rodada 10 + os 4 desta emenda (54 consultas). Os 23 anteriores NÃO são reconsultados: o bruto hasheado `bruto/openalex9-NN-xx.json` é reutilizado tal como está; só as 8 consultas novas tocam a rede.
3. Saída em `series/emenda11/`; a página passa a mostrar a rodada 11 como a última completa e mantém publicadas as contagens das rodadas 07 a 10.
4. Toda obra devolvida é listada com status e motivo; sem nota, soma ou veredito; até 2 frases de resultado do resumo, entre aspas.

## D. O que NÃO muda

Passos a-e, desenhos, siglas, teto, ordenação, frase obrigatória da contagem por mandato, regra de que mudança de consulta olha só para quantos trabalhos cada chamada devolveu.

## E. O que esta emenda não faz

Não cria item do índice, não calcula efeito algum, não soma estudos e não escreve veredito sobre a hipótese do editor. O resultado esperado é declarado antes: o filtro exige o Brasil no título ou no resumo e um desenho de identificação nomeado, e a literatura sobre independência de bancos centrais e regras fiscais é majoritariamente comparativa entre países; a rodada pode devolver zero incluídos, e zero será publicado como tal.
