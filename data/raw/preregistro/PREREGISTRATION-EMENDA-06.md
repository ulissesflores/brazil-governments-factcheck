# Pré-registro, emenda 06: o candle do índice é por ano, sobre o índice mensal

Data: 2026-10-20 (noite). Escrita depois da primeira publicação do índice (v10), em que o candle por
mandato foi desenhado como caixa cobrindo os anos do mandato, e o Ulisses apontou que o pedido era
"ano a ano". Esta emenda complementa o §10 do pré-registro da fase 2; não altera itens, direções,
balizas, pesos nem agregação.

## O que muda

1. **O índice completo passa a ser calculado mês a mês, de jan/1996 em diante**, com a mesma regra
   de balizas, pesos e agregação do índice anual. Cada item entra no mês assim:
   - item com dado mensal ou trimestral (inflação em 12 meses, salário mínimo real, desemprego,
     endividamento das famílias, dívida bruta): pelo valor do mês, com as balizas anuais congeladas do
     próprio item (o valor de um mês pode ficar fora de 0-100, sem corte); valor trimestral vale para os
     três meses do trimestre (atribuição declarada, como no §10.2);
   - item anual: pelo valor do ano, igual nos doze meses (degrau). Não é imputação: é o dado do ano
     atribuído ao próprio ano.
   Cobertura mínima de 70% por mês, como no §9. O índice anual continua existindo e é, por construção,
   o valor de dezembro do índice mensal: para isso o item "taxa de desemprego" passa a usar o valor de
   dezembro (PME) ou do 4º trimestre (PNAD Contínua) em vez da média do ano.
2. **O candle do índice é anual:** abertura = dezembro do ano anterior (quando não existe, o primeiro
   mês do ano, impresso), fechamento = dezembro (ou o último mês disponível no ano corrente, impresso),
   máxima e mínima = extremos dos doze meses. Cor = direção bruta (fechou acima da abertura = verde).
   O pavio reflete só o que se move dentro do ano (os itens mensais); os anuais entram como degrau, e
   isso fica dito na página.
3. **O candle por mandato** (§10.1) continua calculado e publicado na tabela de robustez, mas deixa de
   ser desenhado como caixa sobre o gráfico; os governos aparecem como faixas de fundo e a faixa de
   robustez (5%-95% do fechamento) fica no dezembro final de cada mandato.
4. O "pulso mensal" do §10.2 (só itens mensais) fica como cenário publicado, não como gráfico próprio.

## O que não muda

Portas de elegibilidade, duas camadas, balizas 1995-2024, encadeamento por sobreposição, ausência de
imputação, pesos, cenários, sorteios de robustez, e a leitura obrigatória sobre tendências seculares.
