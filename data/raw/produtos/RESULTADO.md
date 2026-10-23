# RESULTADO: preços de produtos em horas de trabalho (bloco "produtos", emenda 03, seção F)

Colheita de 2026-10-20. Sem opinião, sem nota, sem atribuição de causa. Produtos do pré-registro, sem acréscimo: arroz, feijão, pão francês, café, açúcar, leite, óleo, carne bovina (DIEESE São Paulo); botijão de 13 kg e gasolina comum (ANP); tarifa residencial de energia; passagem de ônibus de São Paulo. **Nenhum produto tem elasticidade-preço zero** (`elasticidade.md` diz quais são preço de mercado e quais são administrados).

Tudo sai de `python3 -I scripts/construir.py` e `python3 -I scripts/quebras_gerar.py`, que leem só arquivos locais. Os brutos estão na cadeia de hash (`manifest.jsonl`, 63 linhas; `python3 -I .../govfc/chain.py verify . --allow-missing` dá OK).

Legenda: ACHADO = tem número e fonte aqui. NAO ACHADO = procurei e não obtive.

## 1. Correção do ponto de partida do pedido

- **NAO ACHADO no Ipeadata:** não existe série `DIEESE12_*` por item. No catálogo `economia-real/meta/ipeadata-Metadados-catalogo-completo-raw.json` o DIEESE aparece só como cesta total (`DIEESE12_CBSP12`, São Paulo; `CESBTOTAL`, capitais). Procurei por arroz, feijão, pão, café, açúcar, leite, óleo e carne.
- **ACHADO no DIEESE:** o banco de dados público da Pesquisa Nacional da Cesta Básica (`https://www.dieese.org.br/cesta/`) responde a consulta POST por cidade, produto e período, com **preço médio por item de São Paulo de jan/1959 a set/2026**. Foi a fonte usada. A página `notaBancoDados.html` avisa que desde abril de 2018 os preços por produto das cidades não estariam mais públicos; **não observei isso**: os preços de São Paulo vêm até 09/2026 e não há sinal de série congelada (1 a 8 repetições de valor em 128 pares mensais de 2016 em diante, por item).

## 2. O que há (ACHADO)

| Produto | Fonte | Cobertura | Unidade |
|---|---|---|---|
| Arroz, feijão, pão francês, café em pó, açúcar, carne bovina | DIEESE, preço médio de São Paulo | 1959-01 a 2026-09 (faltam 10 meses de 1964) | R$/kg |
| Leite | DIEESE | idem | R$/litro |
| Óleo | DIEESE | idem | R$/embalagem (a fonte usa 1 x preço no gasto; tamanho não declarado, 900 mL presumido) |
| Botijão 13 kg e gasolina comum | ANP, preço médio de revenda, Brasil | 2001-07 a 2026-09 (falta 2020-09) | R$/13 kg; R$/litro |
| Energia residencial | Ipeadata ELETRO12_CEETRES12 (ANEEL desde 2003) | 1994-07 a 2026-06 | R$/kWh |
| Ônibus SP, tarifa básica | Prefeitura de São Paulo (planilha tarifária), fontes secundárias e, para dezembro de 1996 a 2004, níveis DERIVADOS do ICV-DIEESE | 1994-07 a 1995-06; dez/1996 a dez/2004 (só dezembros, derivados); 2005-03 a 2026-09 | R$/passagem |

Unidade do DIEESE: o banco não declara. **Conferida item a item** em dez/2015 (gasto mensal publicado do item dividido pelo preço do item dá a quantidade do Decreto-Lei 399, região 1: arroz 3,0; feijão 4,5; pão 6,0; café 0,6; açúcar 3,0; leite 7,5; carne 6,0) e no agregado em dez datas de 1960 a 2026 (razão 0,9999 a 1,0000). **O óleo não bate com 0,75: o gasto usa 1,0 x preço de 1960 a 2026**, então o preço é por embalagem, não por kg (a primeira conferência agregada, que dava 0,998, escondia isso). Detalhe em `series/_conferencias.txt`.

Valores de referência de horas de trabalho ao salário mínimo (220 h/mês; média anual; `series/produtos_em_horas.csv`):

| Produto (unidade) | 1995 | 2002 | 2010 | 2016 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|---|
| Arroz (1 kg) | 1,43 | 1,29 | 0,88 | 0,76 | 0,68 | 0,71 | 0,77 |
| Feijão (1 kg) | 2,40 | 2,63 | 1,61 | 2,15 | 0,88 | 1,42 | 1,00 |
| Pão francês (1 kg) | 4,77 | 4,39 | 2,74 | 2,71 | 2,76 | 3,03 | 2,78 |
| Café (1 kg) | 16,9 | 7,27 | 4,49 | 4,55 | 4,80 | 7,30 | 9,73 |
| Açúcar (1 kg) | 1,51 | 1,02 | 0,90 | 0,71 | 0,55 | 0,75 | 0,69 |
| Leite (1 L) | 1,44 | 1,26 | 0,95 | 0,99 | 0,92 | 1,17 | 0,99 |
| Óleo (1 embalagem) | 2,36 | 2,05 | 1,01 | 0,87 | 0,79 | 1,73 | 1,19 |
| Carne bovina (1 kg) | 10,5 | 7,83 | 6,00 | 5,98 | 5,60 | 8,24 | 7,35 |
| Botijão 13 kg | | 27,4 | 16,5 | 13,5 | 15,7 | 19,9 | 15,7 |
| Gasolina (1 L) | | 1,96 | 1,11 | 0,92 | 1,02 | 1,11 | 0,90 |
| Energia (1 kWh) | 0,186 | 0,236 | 0,130 | 0,114 | 0,118 | 0,118 | 0,117 |
| Ônibus (1 passagem) | | | 1,17 | 0,95 | 0,92 | 0,80 | 0,73 |

Óleo: horas por 1 embalagem. Ônibus: sem média anual de 1995 a 2004 (só dezembros derivados); em dezembro, 1,57 h (1994, R$ 0,50), 1,54 h (2002, R$ 1,40 derivado) e 1,16 h (2010, R$ 2,70).

Razão entre as duas rendas: horas ao salário mínimo dividido por horas à renda do décimo mais rico é **a mesma para todos os produtos** no mesmo ano (é renda do decil 10 dividida pelo salário mínimo, por construção). Valores (PPC 2017): 11,4 (1995), 9,2 (2002), 6,8 (2009), 6,6 (2015), 6,9 (2018), 6,1 (2021), 6,6 (2024). A coluna existe em `produtos_em_horas.csv` e não traz informação por produto.

Variação das horas ao salário mínimo (média anual) e à renda do decil 10, por governo (ano de base = último ano civil completo antes da posse; ano final = último ano civil completo do mandato; `series/produtos_por_governo.csv` traz também a variação nominal, a variação mensal e % ao ano):

| Produto | FHC SM | FHC D10 | Lula1-2 SM | Lula1-2 D10 | Dilma SM | Dilma D10 | Temer SM | Temer D10 | Bolsonaro SM | Bolsonaro D10 | Lula3 SM | Lula3 D10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Arroz | -32% | -16% | -32% | -1% | -15% | -19% | -9% | -12% | +4% | +7% | +9% | +32% |
| Feijão | -34% | -2% | -39% | -28% | -17% | -3% | -34% | -36% | +61% | +65% | -30% | -19% |
| Pão francês | -17% | -2% | -38% | -10% | +5% | +2% | -5% | -8% | +10% | +13% | -8% | -4% |
| Café | -68% | -45% | -38% | 0% | -4% | -17% | +11% | +7% | +52% | +56% | +33% | -6% |
| Açúcar | -55% | -35% | -12% | -1% | -40% | -26% | +2% | -1% | +37% | +41% | -8% | -5% |
| Leite | -27% | -22% | -25% | +11% | -8% | -14% | +7% | +3% | +27% | +31% | -16% | -9% |
| Óleo | -30% | -15% | -51% | -25% | -19% | -27% | -3% | -6% | +118% | +124% | -31% | -37% |
| Carne bovina | -37% | -20% | -23% | +4% | +7% | +10% | -13% | -16% | +47% | +51% | -11% | -20% |
| Botijão 13 kg | NA | NA | -40% | -15% | -18% | -19% | +16% | +13% | +27% | +31% | -21% | -18% |
| Gasolina | NA | NA | -43% | -16% | -16% | -21% | +9% | +5% | +9% | +12% | -19% | -16% |
| Energia | NA | NA | -45% | -19% | -7% | -13% | -2% | -5% | 0% | +3% | -1% | -7% |
| Ônibus SP | NA | NA | NA | NA | -16% | -9% | -6% | -9% | -13% | -11% | -9% | -13% |

Ônibus, dezembro contra dezembro com níveis derivados do ICV-DIEESE (`renda = sm_mensal_horas`): FHC, R$ 0,50 (1994-12) a R$ 1,40 (2002-12), nominal +180%, horas ao salário mínimo -2%; Lula 1-2, R$ 1,40 a R$ 2,70, nominal +93%, horas -24%. Média anual e decil 10 seguem NA para esses dois mandatos.

Como ler os anos de ponta (`nota` na linha de cada resultado): o PIP não tem pesquisa em 1991, 1994, 2000 e 2010, então o ano usado para o decil 10 pode ser o anterior (FHC: 1993 em vez de 1994; Lula 1-2: 2009 em vez de 2010; Dilma: 2009 em vez de 2010; Lula 3: 2024 em vez de 2025). A passagem de 2011 para 2012 troca PNAD por PNAD Continua na fonte. Lula 3 está truncado (a série mensal acaba em 2026-09, a anual em 2025 ou 2024).

A variação mensal (mês de dezembro anterior contra o último mês do mandato) está no arquivo e dá números diferentes dos anuais em alguns itens, porque preço de alimento é volátil (feijão: -7% no FHC mensal contra -34% anual; +80% na Dilma mensal contra -17% anual). **A escolha do ponto muda o sinal em alguns casos**; a coluna `renda` do arquivo identifica a base de cada linha.

Conversão da renda do decil 10 (declarada): PIP, renda domiciliar per capita média do décimo mais rico, US$ PPC 2017 por dia (`quebras/renda-por-decil.csv`) x 365/12 x R$ 2,3273771 por US$ PPC (IBGE SIS, consumo privado, `quebras/pobreza-linhas-em-reais-reais.csv`) = R$ por mês a preços de 2017; x IPCA médio do ano / IPCA médio de 2017 (SGS 433 encadeado, `inflacao/ipca-sgs433-raw.json`) = R$ nominais do ano. É renda domiciliar per capita, não salário de um trabalhador, e a comparação com o salário mínimo (rendimento individual) é de natureza diferente. Sensibilidade em PPC 2021 (fator R$ 2,4498362, Ipeadata) na coluna `horas_decil10_ppc2021`.

## 3. NAO ACHADO

- Série `DIEESE12_*` por item no Ipeadata (ver seção 1).
- Tarifa de ônibus de São Paulo de jul/1995 a fev/2005 **como série observada**: não localizei tabela aberta (só R$ 0,50 em 1994, R$ 0,65 em jun/1995 pela Wikipedia, e R$ 2,00 em mar/2005 pela Prefeitura). O que há é a reconstrução de dezembro de 1996 a 2004 a partir das taxas anuais do ICV-DIEESE (`bruto/onibus/dieese-icv-2006-12-transporte.pdf`, tabela 8) ancoradas em R$ 2,00 de 2005: 0,80, 0,90, 1,00, 1,15, 1,15, 1,40, 1,40, 1,70, 1,70. Os degraus caem em valores redondos e o produto das taxas dá 150,05% (publicado 150,00%), mas é **derivado, não observado**, e o mês do reajuste dentro do ano é desconhecido.
- Botijão e gasolina antes de jul/2001 em série mensal de revenda. Há a série anual EPE/BEN do Ipeadata (`ANP_PRGASOL`, `ANP_PRGLP`) que coincide com a média anual da ANP nos anos testados de 2002 a 2025 (razão 1,000; 0,988 em 2005) e traz 1973-2000; **1973-1993 é estimado pela própria fonte** por variação do preço em dólar. Está em `produtos.csv` e `produtos_em_horas.csv` como `*_epe_ben_anual`, mas **não entrou em `produtos_por_governo.csv`** (FHC fica NA para botijão e gasolina).
- Tarifa de energia antes de jul/1994: a série do Ipeadata mistura moedas; não usada.
- IPCA "energia elétrica residencial" como índice alternativo: não coletado.
- Elasticidade: nenhuma estimativa por item de alimento com número lido; nenhuma estimativa revisada por pares para o botijão; nenhuma só para São Paulo nos ônibus; quartil dos periódicos não conferido (SCImago bloqueou com HTTP 403). Detalhe em `elasticidade.md`.
- Causa de qualquer variação: nada atribuído.

## 4. Quebras (`quebras.csv`, 38 linhas)

- **DIEESE, metodologia 2016** (leite in natura -> UHT, banana prata, locais de coleta pela POF 2008/2009, três marcas por produto): o banco usa o método antigo até dez/2015 e o novo desde jan/2016. **Medi a sobreposição em dez/2015** com a consulta por data e a caixa "metodologia 2016": cesta total 412,12 -> 418,13 (+1,5%); leite +4,6%; pão -4,6%; café +1,0%; açúcar +1,7%; carne -0,2%; feijão +0,2%; arroz 0,0%; óleo -0,3% (banana +24,5% e tomate +1,2%, fora do pré-registro). Isso é uma medida em um mês, não um fator de emenda; as séries não foram emendadas.
- **DIEESE, cortes de moeda** (1967-01, 1986-03, 1989-01, 1993-08, 1994-07) e 10 meses ausentes em 1964.
- **ANP:** cobertura geográfica reduzida de 501 para 459 municípios (30/07 a 30/12/2017); greve dos caminhoneiros (revendas pesquisadas -85%, 27/05 a 02/06/2018); sem pesquisa de 18/08 a 17/10/2020 (falta setembro/2020); preço com duas casas desde mai/2022; número de postos da amostra de 1 392 a 61 607.
- **Energia:** pico atípico de +72% em jul/2025 e out/2025, mantido como publicado e marcado; salto de -13,4% em fev/2013 (causa não verificada).
- **Ônibus:** R$ 3,20 de 2013 publicada e revogada; datas de vigência aproximadas pelo mês da publicação (±1 mês; o R$ 2,30 de 18/11/2006 entra em dezembro porque o ICV-DIEESE registra 0,00% no ônibus até novembro); R$ 5,30 de 2026 vem de reportagem.

## 5. Incidentes e limites do procedimento

- Baixei por engano um PDF de 29,7 MB (`prefeitura-tarifa2025.pdf`, relatório técnico da SMT de dez/2024), acima do limite de 25 MB. Apaguei o arquivo e deixei a linha na cadeia (sha256 mantido; é a "1 hash-only" do `verify`). Não foi usado.
- Baixei também cinco itens fora do pré-registro (farinha, batata, tomate, banana, manteiga) e a cesta total (gasto e tempo de trabalho) **só para conferir unidades** e medir a sobreposição de dez/2015. Não foram analisados.
- Duas consultas ao formulário "data" do DIEESE falharam com HTTP 500 (faltava o campo `produtos`); as respostas de erro estão na cadeia como linhas superadas; as consultas refeitas valem.
- O banco do DIEESE foi consultado por POST; o carimbo de tempo na cadeia é o `mtime` do arquivo logo após o download (`add-local`), não o cabeçalho HTTP.
- Fontes secundárias nos ônibus (Band, Wikipedia, ANTP, Terra): são o que existe aberto para 1994-1995 e 2026; as tarifas de 2005 a 2025 vêm da Prefeitura.
- A primeira checagem de unidade (soma agregada) deu 0,998 e eu a aceitei; a checagem item a item (sugerida na revisão) mostrou que o óleo usa quantidade 1,0 e não 0,75. Corrigido antes da entrega.

## 6. Arquivos

| Arquivo | Conteúdo |
|---|---|
| `series/produtos.csv` | formato longo (14 222 linhas): produto, fonte, definição da linha, ano, mês, valor, unidade, nota, vintage. Inclui a moeda da época dos oito itens do DIEESE e as séries anuais EPE/BEN |
| `series/produtos_em_horas.csv` | horas ao salário mínimo (mensal e anual), à renda do decil 10 (anual, PPC 2017 e sensibilidade PPC 2021) e a razão |
| `series/produtos_por_governo.csv` | por mandato (FHC em diante): início, fim, variação e % ao ano, em nominal, SM mensal, SM anual e decil 10 anual |
| `series/_conferencias.txt` | unidades do DIEESE, lacunas da ANP, comparação BEN x ANP |
| `quebras.csv` | catálogo de quebras |
| `elasticidade.md` | literatura de elasticidade-preço, DOIs conferidos no Crossref |
| `bruto/` | dieese, anp, energia, onibus, literatura (todos na cadeia) |
| `scripts/` | `baixar_dieese.sh`, `cadeia.sh`, `xlsx_min.py`, `construir.py`, `quebras_gerar.py` |
