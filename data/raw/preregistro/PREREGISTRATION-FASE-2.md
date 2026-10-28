# Pré-registro da fase 2: o índice composto (pontuação por item, uma série, um candle)

Data: 2026-10-20. Escrito depois das decisões do Ulisses na conversa de 2026-10-20 (12ª a 14ª levas) e
ANTES de qualquer código calcular um agregado. Complementa o pré-registro original (fase 1: dado bruto,
hash em cadeia, direção por polaridade, sem nota) e as emendas 01 a 05. Nada aqui altera a fase 1.

## 0. Declaração de honestidade

O pré-registro original pedia a regra antes de ver os dados. Os componentes já foram vistos por quem
escreve e por quem decide (a grade por governo da emenda 05 está publicada). O que este documento ainda
protege: pesos, normalização, agregação, lista de itens e direções são fixados aqui, antes de o agregado
ser calculado; aplicam-se igualmente a todos os governos; e a sensibilidade da ordem dos governos a
pesos e escolhas alternativas é publicada junto com o índice. Qualquer mudança posterior é emenda datada.

## 1. A pergunta que o índice responde

"Em que medida as condições de vida, da economia e das instituições no Brasil, medidas em itens cuja
direção de leitura tem apoio em literatura revisada por pares, estiveram perto do melhor ou do pior
registrado no país desde o Plano Real?" O índice mede condições do país durante cada mandato, não o
mérito do governo; a palavra governo não entra no nome do índice. Causalidade fica com o leitor.

## 2. Três portas de elegibilidade (todo item passa pelas três)

1. **Direção.** O item tem direção "maior é melhor" ou "menor é melhor" estabelecida em artigo revisado
   por pares (quartil 1 no SJR ou A1 no Qualis, DOI conferido no Crossref). Item sem direção acordada é
   contexto, nunca pontua.
2. **Sem composto dentro do composto.** Índices de terceiros que já carregam pesos (IDH, Fraser, Heritage,
   Legatum, CPI da Transparência) não entram; entram os componentes primários deles. Medidas derivadas por
   algoritmo publicado sem pesos arbitrários (índice de complexidade econômica; indicadores do V-Dem com
   modelo de medição publicado) são admitidas como item.
3. **Um conceito, uma vez.** Transformações do mesmo dado (porquinho, produtos em horas, imposto
   inflacionário em relação à inflação; dívida bruta e dívida líquida; as três etapas do Saeb) não entram
   duas vezes: um item por conceito. A importância efetiva de cada item dentro da área é publicada (§5),
   não corrigida.

Regras adicionais: série com quebra de método dentro de 1995-2026 só entra encadeada pela sobreposição
medida (§8); sem sobreposição, o item cobre só o trecho da base mais longa. Indicador que muda por regra
administrativa e não pelo fenômeno (reprovação escolar) não entra.

## 3. Duas camadas publicadas

- **Núcleo consensual (N):** itens cuja direção tem consenso na literatura.
- **Bloco de premissas econômicas (P):** itens cuja direção é premissa declarada do autor (economista),
  com a literatura a favor e contra citada lado a lado. O índice é publicado em duas versões, N e N+P, e a
  página mostra se a ordem dos governos muda entre as duas.
- **Contexto (C):** itens sem direção acordada; aparecem na grade e no detalhe, não pontuam.

## 4. Lista de áreas e itens (direção; medida; fonte; situação)

Situação: "temos" = já na camada curada ou nas coletas hasheadas; "coletar" = coleta nova com cadeia de
hash, disparada depois deste selo. Referências de direção em §11, todas "a verificar".

### Núcleo (N)

| Área | Item | Direção | Medida e fonte | Situação |
|---|---|---|---|---|
| Preços | Inflação (IPCA, dez/dez) | menor | IBGE via BCB SGS 433 | temos |
| Atividade e renda | PIB per capita real (nível, US$ PPC constantes de 2021) | maior | Banco Mundial WDI | temos (mun_pibpc_ppc) |
| Atividade e renda | Investimento (FBCF/PIB) | maior | IBGE SCN | temos (cc_fbcf_pib) |
| Atividade e renda | Produtividade total dos fatores | maior | PWT (rtfpna) | temos (cc_ptf_pwt) |
| Atividade e renda | Salário mínimo real | maior | Ipea (deflator INPC) | temos |
| Atividade e renda | Renda real do trabalho | maior | PNAD/PNADC (duas bases) | temos (encadear §8) |
| Trabalho | Taxa de desemprego | menor | PME antiga, PME nova, PNADC (três bases) | temos (encadear §8) |
| Trabalho | Informalidade | menor | PNAD 1992-2014 e PNADC 2016+ | temos (sem sobreposição: dois trechos) |
| Fiscal e vulnerabilidade | Dívida bruta do governo geral/PIB | menor | BCB: metodologia 2008 (2006+) encadeada à antiga (2002+) pela sobreposição 2006-2025 (§8) | temos |
| Fiscal e vulnerabilidade | Resultado primário/PIB | maior | Tesouro RTN; BCB NFSP | temos |
| Fiscal e vulnerabilidade | Reservas internacionais/PIB | maior | BCB (reservas, temos); PIB em US$ correntes (WDI) | coletar o denominador |
| Fiscal e vulnerabilidade | Endividamento das famílias/renda | menor | BCB SGS 29037 e 19882 | coletar |
| Pobreza e desigualdade | Pobreza (US$ 6,85/dia PPC 2017) | menor | Banco Mundial PIP; IBGE SIS | temos |
| Pobreza e desigualdade | Gini | menor | PIP; PNAD; PNADC | temos |
| Pobreza e desigualdade | Subalimentação (prevalência) | menor | FAO via WDI | temos (ali_pou) |
| Saúde | Expectativa de vida ao nascer | maior | IBGE; ONU | temos |
| Saúde | Mortalidade infantil | menor | IBGE/DATASUS; WDI | temos (mortinf) |
| Saúde | Mortalidade materna (estatística nacional) | menor | DATASUS | temos |
| Saúde | Cobertura vacinal DTP3 | maior | OMS/UNICEF; administrativa | temos |
| Saúde | Pré-natal com 7+ consultas | maior | SINASC | temos |
| Educação | Saeb matemática (um item: média simples das três etapas, 5º, 9º e 3ª série EM, nos anos em que as três existem) | maior | INEP | temos |
| Educação | Analfabetismo 15+ | menor | IBGE | temos |
| Educação | Anos médios de estudo 25+ | maior | IBGE | temos |
| Segurança | Homicídios por 100 mil | menor | SIM/DATASUS (com % de causa indeterminada como ressalva) | temos |
| Moradia e infraestrutura | Água por rede geral (% domicílios) | maior | PNAD/PNADC | temos |
| Moradia e infraestrutura | Esgoto adequado (% domicílios) | maior | PNAD/PNADC | temos |
| Moradia e infraestrutura | Energia elétrica (% domicílios) | maior | PNAD/PNADC | temos |
| Moradia e infraestrutura | Acesso à internet (% domicílios) | maior | PNAD 2005+/PNADC | coletar |
| Ambiente | Desmatamento da Amazônia (km²/ano) | menor | INPE PRODES | temos |
| Instituições | Democracia liberal (v2x_libdem) | maior | V-Dem | coletar |
| Instituições | Corrupção política (v2x_corr) | menor | V-Dem | coletar |
| Instituições | Restrições legislativas ao Executivo (v2xlg_legcon) | maior | V-Dem | coletar |
| Instituições | Restrições judiciais ao Executivo (v2x_jucon) | maior | V-Dem | coletar |
| Ciência e tecnologia | Gasto em P&D/PIB | maior | UNESCO via WDI | coletar |
| Ciência e tecnologia | Pesquisadores por milhão de habitantes | maior | UNESCO via WDI | coletar |
| Ciência e tecnologia | Patentes de residentes por milhão | maior | WIPO | coletar |
| Ciência e tecnologia | Índice de complexidade econômica | maior | Atlas/OEC (algoritmo publicado) | coletar |

### Bloco de premissas econômicas (P), direção declarada pelo autor

| Item | Direção | Medida e fonte | A favor / contra (a verificar) |
|---|---|---|---|
| Indústria de transformação/PIB | maior | IBGE SCN (quebra 2010) | desindustrialização precoce / crescimento puxado por serviços |
| Consumo do governo/PIB | menor | IBGE SCN | revisão sobre tamanho do Estado e crescimento / resultado incerto em países em desenvolvimento |
| Abertura comercial (X+M)/PIB | maior | IBGE SCN; WDI | comércio e renda; episódios de liberalização / crítica às medidas de abertura |
| Propriedade estatal da economia (v2clstown) | menor | V-Dem (conjunto completo; se só a versão resumida for acessível sem cadastro, o item fica em contexto) | premissa; medida de intervenção distinta de tamanho |

### Contexto (C), não pontua

Selic (meta e over), juro real, M3/M0, moeda/PIB, excesso monetário, imposto inflacionário, carga
tributária, ministérios, cargos em comissão, resultado das estatais, câmbio, termos de troca, crédito a
empresas/PIB, reprovação, porquinho, produtos em horas, investimento público/PIB, gasto público em saúde
e educação (insumo, não resultado), previdência, dívida líquida do setor público (BCB, 1991+; coletar
para dar "início -> fim" a FHC na grade, não para o índice), emissões de CO2 per capita (direção
contestada para país de renda média).

## 5. Pesos

1. **Juízo declarado:** cada área importa igual. Dentro da área, cada item importa igual.
2. **Implementação:** pesos nominais iguais são o ponto de partida; depois ajustam-se os pesos nominais
   das áreas até a importância efetiva de cada área sobre o índice (razão de correlação de Pearson entre
   área e índice, Paruolo, Saisana e Saltelli 2013) ficar igual entre áreas, com tolerância de 0,02. O
   ajuste é calculado uma vez, na primeira edição, sobre o período-base (§6), e os pesos resultantes ficam
   congelados e publicados com a edição. Restrições pré-fixadas: cada peso de área fica entre metade e o
   dobro do peso nominal igual (1/K); no máximo 100 iterações; se a tolerância não for atingida dentro das
   restrições, o padrão passa a ser os pesos nominais iguais, e isso é declarado na edição (não é emenda).
3. **Cenários publicados:** (S1) pesos nominais iguais sem ajuste; (S2) pesos por bem-estar para o núcleo
   econômico, com a razão desemprego/inflação da literatura de satisfação com a vida (dois valores
   publicados, o menor e o maior, como limites); (S3) sorteio de 10.000 vetores de pesos de área (Dirichlet
   simétrica) com a faixa de 5% a 95% do fechamento de cada mandato e a fração de sorteios em que cada
   governo mantém a posição.
4. A página oferece controle de pesos ao leitor; o padrão e os cenários acima não mudam com isso.

## 6. Normalização

1. Direção aplicada primeiro: item "menor é melhor" entra multiplicado por -1.
2. **Balizas congeladas, escala 0 a 100, sem corte.** Para cada item, baliza 0 = pior valor observado no
   Brasil no período-base e 100 = melhor valor observado; pontuação = 100 x (valor - pior) / (melhor -
   pior). Valores fora do período-base podem passar de 100 ou ficar abaixo de 0 e são mostrados assim.
3. **Período-base:** 1995 a 2024 (anual) e jan/1996 a dez/2024 (pulso mensal; 1995 ainda carrega a
   inflação em 12 meses da hiperinflação, que esmagaria os 30 anos seguintes na escala, o mesmo motivo da
   emenda 04 §5), fixado na primeira edição. As balizas são gravadas com a edição (vintage) e não mudam
   quando entra dado novo. Mudar baliza é emenda.
4. Item com menos de 10 anos no período-base não entra na primeira edição (fica em contexto até ter).
5. Cenário publicado: balizas nos percentis 5 e 95 do período-base (robustez a extremos).

## 7. Agregação

1. Dentro da área: média aritmética dos itens disponíveis no ano (§9), pesos de §5.
2. Entre áreas: **média aritmética ponderada** (padrão). Tradeoff explícito e constante: um ponto numa área
   vale um ponto em outra. Os tradeoffs implícitos entre itens (quantas unidades de um item equivalem a uma
   unidade de outro, nas unidades originais) são publicados em tabela.
3. Cenários publicados: média geométrica entre áreas (penaliza desequilíbrio; indefinida com área em 0, o
   que é dito) e agregação não compensatória de Mazziotta e Pareto (média menos penalidade pelo coeficiente
   de variação entre áreas).

## 8. Quebras de método (encadeamento)

Onde duas bases se sobrepõem, a base antiga é ligada à nova pela diferença média (itens em taxa ou
proporção) ou pela razão média (itens em nível) medida nos períodos de sobreposição, e o efeito é impresso
no item (como nos índices de preços encadeados). Onde não há sobreposição, não há encadeamento: o item
cobre só o trecho da base mais longa e a cobertura (§9) registra a ausência. Nada é estimado.

## 9. Dados ausentes e cobertura

Sem imputação. Item ausente num ano sai da média da área naquele ano; a página mostra a cobertura (fração
de itens presentes) por ano e por área. O índice não é calculado para ano com menos de 70% dos itens
do núcleo. Cenário publicado: último valor carregado (carry-forward) para itens bienais e anos sem
pesquisa, rotulado como cenário.

## 10. Frequência, candles e pontuação por governo

1. **Índice anual completo:** todos os itens; uma observação por ano, de 1995 em diante (o índice não
   existe para 1994 nem antes: as balizas são pós-Real). Candle por mandato pela regra da emenda 05
   (abertura = valor do ano anterior à posse; fechamento = último ano do mandato; pavio = extremos dos
   anos do mandato), com uma exceção impressa: o primeiro mandato (FHC) abre no primeiro valor calculado
   (1995), porque não há 1994.
2. **Pulso mensal:** só itens mensais ou trimestrais com direção (inflação em 12 meses, salário mínimo
   real, desemprego, crescimento do PIB em 4 trimestres), mesma regra de balizas e pesos, de jan/1996 em
   diante; o valor de um item trimestral vale para os três meses do seu trimestre (atribuição declarada,
   não estimativa; §9 não se aplica a isso). Candle por ano (abertura = dezembro anterior, fechamento =
   dezembro, pavio = meses; 1996 abre no primeiro valor calculado) e por mandato.
3. O candle é desenhado sobre o índice; cor = direção bruta (subiu verde, caiu vermelho); "maior é melhor"
   vale para o índice inteiro por construção. Ao passar o cursor, o ano mostra a contribuição de cada área e
   o item que mais puxou.
4. Não há nota, ranking de mérito nem estimativa. A ordem dos governos pelo fechamento é descrição e vem
   sempre acompanhada da estabilidade dessa ordem nos cenários de §5 e §7.

## 11. Referências do método e das direções (TODAS a verificar: DOI no Crossref e quartil no SJR antes de entrar na METHODOLOGY)

Método: incerteza e sensibilidade de indicadores compostos (Saisana, Saltelli e Tarantola, JRSS A 2005);
importância efetiva e pesos (Paruolo, Saisana e Saltelli, JRSS A 2013; Becker et al., Ecological
Indicators 2017); revisão de pesos e agregação (Greco et al., Social Indicators Research 2019); famílias
de pesos (Decancq e Lugo, Econometric Reviews 2013); agregação não compensatória (Mazziotta e Pareto,
Social Indicators Research 2016); críticas que o método responde (Ravallion, World Bank Research
Observer 2012 e Journal of Development Economics 2012; Böhringer e Jochem, Ecological Economics 2007);
defesa da geométrica no IDH (Klugman, Rodríguez e Choi, Journal of Economic Inequality 2011); por que
agregar exige função de bem-estar explícita (Fleurbaey, Journal of Economic Literature 2009); pesos por
bem-estar de inflação e desemprego (Di Tella, MacCulloch e Oswald, AER 2001; Blanchflower et al., Journal
of Money, Credit and Banking 2014).
Direções: dívida das famílias e crescimento (Mian, Sufi e Verner, QJE 2017); direção dos itens do V-Dem
pela definição normativa dos próprios índices e pelo modelo de medição do V-Dem (Marquardt e Pemstein, Political Analysis 2018; Coppedge et al., Perspectives
on Politics 2011); complexidade econômica (Hidalgo e Hausmann, PNAS 2009); desindustrialização precoce
(Rodrik, Journal of Economic Growth 2016); tamanho do Estado e crescimento (Bergh e Henrekson, Journal of
Economic Surveys 2011); abertura e renda (Frankel e Romer, AER 1999; Wacziarg e Welch, World Bank
Economic Review 2008; crítica: Rodríguez e Rodrik, NBER Macroeconomics Annual 2000); finança demais
(Arcand, Berkes e Panizza, Journal of Economic Growth 2015, para manter crédito a empresas em contexto).
Literatura cinzenta (manuais de organismos, working papers) não sustenta nenhuma regra deste documento.

## 12. O que o índice não afirma

Não afirma causalidade entre governo e resultado; não afirma que os pesos são verdadeiros, só que são
declarados e testados; não compara o Brasil com outros países (balizas são brasileiras); não é ranking
de mérito; não contém estimativa, imputação nem extrapolação.
