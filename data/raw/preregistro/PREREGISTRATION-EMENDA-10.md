# EMENDA-10: dívida externa, reservas e endividamento público na camada de literatura

Data: 2026-10-23. Selada na cadeia `preregistro/manifest.jsonl` ANTES de qualquer consulta da rodada 10. Modifica a EMENDA-07 §B2 (lista de episódios) e nada mais. Autorização do Ulisses no mesmo dia ("tem que ser completo. você faz essas pesquisas, não eu").

## A. Motivo (declarado antes de buscar)

A camada descritiva da dívida externa entrou na página (coleção `externo-fase3`, v24) sob a dimensão `ext` do pré-registro original. A camada de literatura (EMENDA-07 §B, modificada por 08 e 09) tem 20 episódios e nenhum trata de dívida externa, reservas ou trajetória da dívida pública. Esta emenda acrescenta três episódios. A decisão nasce do pedido do autor do projeto, não de resultado das rodadas 07-09: as consultas abaixo foram escritas sem olhar quais artigos essas rodadas devolveram.

## B. Episódios novos (numeração continua a da EMENDA-07)

| Nº | Episódio | Mandatos | Consulta EN | Consulta PT |
|---|---|---|---|---|
| 21 | Dívida externa, reservas internacionais e vulnerabilidade externa (1994-) | fhc, lula12, dilma, temer, bolsonaro, lula3 | `external debt Brazil` | `dívida externa Brasil` |
| 22 | Acumulação de reservas e quitação com o FMI (2005-2008) | lula12 | `international reserves Brazil` | `reservas internacionais Brasil` |
| 23 | Trajetória da dívida pública bruta e custo de carregamento (2014-) | dilma, temer, bolsonaro, lula3 | `public debt Brazil` | `dívida pública Brasil` |

Os mandatos listados são os anos em que o episódio esteve em curso; a contagem por mandato continua a refletir anos decorridos e episódios declarados, nunca a qualidade do governo nem o sentido dos resultados (EMENDA-07 §B5).

## C. Protocolo da rodada 10

1. Parâmetros idênticos aos da EMENDA-09 §B: `filter=title_and_abstract.search`, tipo `article|review`, ordem por relevância, teto 200 por consulta, lista de desenhos e siglas da EMENDA-08, resumo do Crossref quando o OpenAlex não cede, passos de inclusão a-e da EMENDA-07 §B3.
2. A rodada 10 = os 20 episódios da rodada 09 + os 3 desta emenda (46 consultas). Os 20 episódios anteriores NÃO são reconsultados: o bruto hasheado da rodada 09 (`bruto/openalex9-NN-xx.json`) é reutilizado tal como está, porque os parâmetros são os mesmos; só as 6 consultas novas tocam a rede. Os registros do Crossref já hasheados também são reutilizados.
3. Saída em `series/emenda10/` (tabela completa dos 23 episódios); a página passa a mostrar a rodada 10 como a última completa e mantém publicadas as contagens das rodadas 07, 08 e 09.
4. Toda obra devolvida é listada com status e motivo; sem nota, soma ou veredito; até 2 frases de resultado do resumo, entre aspas.

## D. O que NÃO muda

Passos a-e, desenhos, siglas, teto, ordenação, frase obrigatória da contagem por mandato, regra de que mudança de consulta olha só para quantos trabalhos cada chamada devolveu.

## E. Dívida externa como item do índice

NÃO entra por esta emenda. Para entrar precisaria de referência Q1 com direção declarada, da porta "um conceito uma vez" (a DBGG já cobre endividamento público) e de escolha entre os conceitos restrito e BPM6; além disso o BCB descontinuou a dívida externa líquida em fev/2026 e a série termina em 2025T3, sem cobrir o mandato corrente. Reavaliar por emenda própria se o BCB publicar a dívida externa líquida no conceito BPM6 como série.
