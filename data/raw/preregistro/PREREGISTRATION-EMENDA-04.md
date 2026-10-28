# Pré-registro, emenda 04: o candle anual é em taxa, não em nível

Data: 2026-10-20. Escrita depois de a primeira versão do terminal (v7) mostrar candles em nível de
preços e em saldos monetários nominais, e antes de qualquer ingestão das coletas da emenda 03 na
camada curada. Esta emenda corrige a seção G da emenda 03, que dizia "candles no nível".

## O que muda

1. **Candle só em grandeza que sobe e desce de verdade.** Um nível de preços ou um saldo nominal
   de moeda só sobe (o candle seria sempre verde) e, em moeda da época, atravessa oito unidades
   monetárias sem significado. O candle anual passa a ser calculado sobre:
   - inflação: taxa acumulada em 12 meses (IPCA; INPC e IGP-DI como linhas);
   - emissão: variação em 12 meses da base monetária M0 (uma base contínua desde 1946), com o
     IPCA em 12 meses e o M1 (as duas definições, sem emenda) como linhas, e a diferença
     M0 menos IPCA como faixa com sinal;
   - dinheiro criado pelos bancos: razão M3 / M0 (M3 Novo; regime 2001 como linha);
   - PIB: crescimento contra o mesmo trimestre do ano anterior (contas trimestrais);
   - Selic: taxa over anualizada mensal (Ipeadata PAN12), meta do Copom como linha, juro real
     ex-post do ano como faixa com sinal;
   - salário mínimo real e taxa de desemprego: no próprio nível, porque sobem e descem.
2. **Regra do candle (inalterada da emenda 03 G):** abertura = último valor do ano anterior,
   fechamento = último valor do ano, máxima e mínima = extremos dos valores mensais ou trimestrais
   do ano; cor = direção bruta (fechamento acima da abertura = verde); o cabeçalho diz o que
   "subir" significa e se "menor é melhor".
3. **Duas granularidades coexistem por desenho:** a grade da primeira tela (emenda 02 A) é um
   candle por mandato; o terminal (emenda 03 G) é um candle por ano. As duas usam a mesma regra
   de abertura/fechamento/extremos, só muda a janela.
4. **Faixa com sinal só onde há segunda variável com sinal** (emissão menos inflação; juro real).
   Não há barra de "variação do ano" repetindo o corpo do candle.
5. **Escala:** linear na vista pós-Real (1996 em diante; 1995 ainda abre a 916% no IPCA de 12
   meses); simétrica de log (sinal x log10(1 + |x|)) só na vista completa, onde 5.000% e 2%
   precisam caber no mesmo eixo. O eixo mostra sempre o valor real.
6. **Moeda em relação ao PIB:** média dos 12 saldos mensais sobre o PIB do ano, não o saldo de
   dezembro (na hiperinflação dezembro sozinho mistura preços de meses diferentes).
7. **Marcos:** só os de `moeda-fiscal/marcos.csv` (uma data por acontecimento, com fonte
   primária), filtrados por indicador; nenhum marco digitado de memória.
8. **Séries anuais:** linha com ponto por ano; Saeb como pontos (bienal); imposto inflacionário
   como coluna (é fluxo).

## O que não muda

A regra de veredito, a camada curada, a dinâmica por mandato, a comparação com o mundo e o
catálogo de quebras seguem como pré-registrados. Nenhum dado é estimado: tudo que o terminal
mostra sai de valores publicados ou de operações aritméticas declaradas aqui.
