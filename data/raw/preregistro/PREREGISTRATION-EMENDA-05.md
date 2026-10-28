# Pré-registro, emenda 05: a página enuncia o achado; correções de dado da revisão de 2026-10-20

Data: 2026-10-20. Escrita depois da revisão ponto a ponto do `terminal.json` (v8.2) e antes de
qualquer código novo. Motivo: a página v8 era um navegador de gráficos sem nenhum achado enunciado
(28 abas antes do gráfico, linhas sem legenda, nota de desenvolvedor no corpo), e a revisão achou
seis problemas de dado que a exibição escondia. Esta emenda corrige regras de exibição e de cálculo;
nenhum número bruto muda e nenhuma série sai da cadeia.

## A. Exibição

1. **Uma página só, dois níveis.** O primeiro nível é a grade por mandato da emenda 03 (sete
   colunas: 1964-1994 agregado, FHC, Lula 1-2, Dilma, Temer, Bolsonaro, Lula 3). O segundo nível é
   o detalhe por ano (terminal da emenda 03 G), aberto a partir da linha. Deixa de haver dois
   artefatos.
2. **O número principal da célula é "início -> fim" na unidade do próprio indicador**
   (ex.: "916% -> 22%"; "15,5 h -> 7,6 h o quilo de carne"; "R$ 100 mil -> R$ 49,8 mil").
   A tendência por ano (emenda 02 B) passa a número secundário, no detalhe. Início = último valor
   publicado antes da posse (dezembro do ano anterior, ou o mês anterior à posse quando a série é
   mensal); fim = último valor publicado do mandato (dezembro do último ano civil, ou o último mês
   disponível no mandato corrente, com a data impressa). Máxima e mínima = extremos dos valores
   publicados dentro do mandato.
3. **Uma frase calculada por indicador**, montada pelo código a partir dos mesmos números, sem
   adjetivo e sem causa: "A carne custava 15,5 horas de salário mínimo em dez/1994 e 7,6 em
   set/2026." A frase é asserção de teste.
4. **Toda linha do terminal entra na grade.** Não há escolha editorial de "manchetes": o conjunto
   da grade é o conjunto dos indicadores pré-registrados nas emendas 01 a 04, agrupados nos sete
   domínios do terminal. Célula sem base única (emenda 02 §3) mostra os valores por base em número
   pequeno e nenhum "início -> fim" principal.
5. **Coluna 1964-1994:** números (início, fim, máxima, mínima) em vez de candle em escala própria;
   o candle por governo pré-Real fica no detalhe.
6. **Legenda visível em todo gráfico com mais de uma linha**; a fita de governos só rotula onde o
   nome cabe, e o nome completo aparece no painel do ano. O texto de "como ler" fica recolhido; a
   nota de versão sai da página (vai para o CHANGELOG do repositório).

## B. Cálculo (correções da revisão de dados de 2026-10-20)

7. **Selic:** o candle anual passa a ser calculado sobre a **meta do Copom** (BCB SGS 432, valor
   de fim de mês, desde 1999), não sobre a taxa over mensal anualizada. Motivo medido: a
   anualização (1 + taxa do mês)^12 − 1 carrega o número de dias úteis do mês (dez/2022: 14,30% a.a.
   com meta de 13,75%; dez/2018: 6,04% com meta de 6,50%), ruído de até 1 ponto que não é política
   monetária. A over (Ipeadata PAN12, desde 1974) continua como linha, com essa ressalva no rótulo.
   Não há candle de Selic antes de 1999.
8. **Base monetária, fev/2001:** a série SGS 1788 do BCB traz em fev/2001 o valor 47.891.196, 13%
   acima de jan e mar/2001 e igual, até a quinta casa, ao de fev/2002 (47.891.206). É erro de
   transcrição na fonte. Regra: o valor bruto fica na cadeia e na série; as variações em 12 meses
   que o usam (fev/2001 e fev/2002) são suprimidas e o fato entra em `quebras.csv` como
   `revisao_de_vintage` com o trecho literal. O candle de 2002 deixa de ter mínima 0,00002%.
9. **Cargos em comissão:** a contagem do Painel Estatístico de Pessoal cai 74% entre dez/2020 e
   dez/2021 (22.542 -> 5.789 em DAS/FCPE/CCE/FCE; 90.086 -> 22.716 em todos os agrupamentos) sem
   causa no changelog do painel. Pela regra de base única (emenda 02 §3), a série vira **duas
   bases**: 1999-2020 e 2021-2025, nunca uma linha contínua; a Lei 14.204/2021 (CCE/FCE) é citada
   como candidata a causa, com a lacuna declarada "não explicada pela fonte".
10. **Imposto inflacionário:** o rótulo declara o deflator (a fórmula mensal de Cysne e
    Coimbra-Lisboa usa o IGP-DI, por isso 2025 é negativo com IGP-DI de −1,2% em 12 meses). A
    variante com IPCA (já na camada curada, 1981+) entra como segunda linha.
11. **Reprovação, anos iniciais:** 1997-2005 (calculada das contagens, 1ª a 4ª série do
    fundamental de 8 anos) e 2006-2025 (como publicada, anos iniciais do fundamental de 9 anos)
    são **duas bases**; 2020 (0,6%) leva o marcador da regra pandêmica.
12. **Produtos em horas de trabalho:** as quebras mostradas são as da coleta de produtos
    (`produtos/quebras.csv`: DIEESE 2015-12, ANP 2020-08, Eletrobras/ANEEL 2003, ônibus 2020-2024),
    mais as do salário mínimo apenas nas datas de troca de moeda; deixa de herdar 1940 e 1944.

## O que não muda

Regra do candle (abertura, fechamento, extremos; verde = fechou acima; cabeçalho diz o que subir
significa), candle só em taxa (emenda 04), marcos só de `marcos.csv`, duas granularidades, escala
linear pós-1996 e símlog só na vista completa, luz de dado (emenda 01 §D), ausência de ranking,
nota ou estimativa. Nenhum dado é estimado.
