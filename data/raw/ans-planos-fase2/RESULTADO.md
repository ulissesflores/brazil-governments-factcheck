# Plano de saude: teto da ANS, reajustes de planos coletivos e o IPCA (fase 2)

Coleta de 2026-10-21. Pasta: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/ans-planos-fase2/`. Cadeia de hash: `manifest.jsonl` (197 aquisicoes, todas com URL, sha256 e timestamp). Nada estimado: todo numero abaixo sai de arquivo baixado e hasheado, por script em `scripts/`.

## Resposta curta

1. **O IPCA de plano de saude NAO esta defasado em relacao ao teto da ANS para planos individuais.** De dez/1999 a dez/2024 o teto da ANS, composto (cada reajuste aplicado em maio), da +652,41%; o subitem do IPCA da +660,34%. O IBGE usa, "em geral", o reajuste fixado pela ANS (trecho abaixo): as duas series sao a mesma informacao. Ressalva de fase: o teto sobe de uma vez em maio, e o IPCA dilui cada ciclo nos 12 meses seguintes; numa janela dez/dez o IPCA carrega so cerca de 8/12 do ultimo ciclo (e 4/12 do anterior), entao a igualdade de longo prazo vale apesar do descompasso nas pontas, nao por alinhamento exato. A coluna abr-abr da tabela por ano, que alinha os ciclos, mostra a mesma correspondencia ano a ano (9,04 x 9,06 em 2013; 13,55 x 13,45 em 2015).
2. **A defasagem aparece nos planos COLETIVOS, que o subitem do IPCA nao mede.** Janela mais limpa, dez/2014 a dez/2024 (agrupamento ja consolidado): reajustes comunicados a ANS para coletivos medico-hospitalares, ponderados por beneficiarios e compostos, dao +216,77% (+248,43% se os contratos comunicados como "sem reajuste" ou manutencao, percentual zero, forem tirados da conta; IPCA plano de saude +134,59%; teto individual +132,40%; IPCA geral +74,90%). Nos contratos com menos de 30 vidas (agrupamento) o composto e +301,27% (arquivo de comunicados) e +304,18% (outra tabela da ANS, por operadora; +303,22% sem zeros): em nivel, 1,71 vez o do subitem do IPCA. Desde dez/2012 (agrupamento ainda em implantacao em 2013-2014): +291,89% para todos os coletivos medicos e +433,26% / +436,55% para os de menos de 30 vidas.
3. O exemplo nomeado ficou limitado: nao achei preco rastreavel do "Amil 400" medico. Achei, e tabulei, quatro tabelas de venda de planos individuais Amil (RJ, 2006 a 2010) em capturas do Wayback de PDFs da propria Amil (outros 12 PDFs da Amil foram baixados e hasheados, sem tabular). Elas mostram preco de VENDA para contrato novo, nao o que paga quem ja e cliente (secao 4).

## 1. ANS: teto de reajuste dos planos individuais/familiares, 2000 a 2026

Fonte: tabela oficial linkada na pagina "Reajuste anual de planos individuais/familiares" da ANS (`bruto/ans/tabela_reajustes_individuais_2026.xlsx`, sha256 `4cbae67e6d1b9efbb402238f4e330aadaa0c3406d78a0010dd4fa803b5383876`; pagina `bruto/ans/pagina-reajuste-individuais-familiares.html`, sha256 `1498de234604238c06a0e4b32cb13c201d6233d21c1e5d21f623a20fee4bf99e`, atualizada pela ANS em 30/06/2026). 27 ciclos, cada um de maio a abril, de maio/2000 a abril/2027. Series: `series/ans_teto_individual_anual.csv`; indice composto (dez/1999 = 100): `derivado/indice_ans_teto_individual_dez1999_100.csv`.

Escopo declarado pela ANS: planos individuais/familiares de assistência médico-hospitalar "contratados após 1º de janeiro de 1999 ou adaptados à Lei nº 9.656/98". Os planos antigos (anteriores a 1999) tem regra propria (pagina `bruto/ans/pagina-planos-antigos.html`, salva e hasheada, NAO lida nesta coleta).

Indice composto do teto (dez/1999 = 100): dez/2004 = 150,70; dez/2012 = 270,78; dez/2018 = 521,49; dez/2022 = 641,96; dez/2024 = 752,41; apos maio/2026 = 838,79 (IPCA plano de saude em set/2026: 842,78).

Ressalvas: (a) e indice de TETOS em sequencia, nao preco pago; (b) 2020-2021: a ANS suspendeu os reajustes em set/2020 e recompos em 12 parcelas em 2021, e o teto do ciclo 2021 e -8,19%; o indice composto aplica 8,14% em maio/2020 e -8,19% em maio/2021 sem modelar a suspensao; (c) desde o ciclo 2019 o teto combina 80% de uma variacao de despesas assistenciais (IVDA) com 20% do IPCA SEM o subitem plano de saude (RN 441, dez/2018; pagina de metodologia `bruto/ans/pagina-metodologia-calculo-individuais.html`, sha256 `37f78e55e2635e3ab46f5e316f617d1c79c3eed9d93fa89db32ec6358b74d273`). Ver `quebras.csv`.

## 2. Planos coletivos (empresariais e por adesao): sem teto

### O que a ANS diz que existe

Pagina "Reajuste anual de planos coletivos" (`bruto/ans/pagina-reajuste-coletivos.html`, sha256 `e4e4467f6bb83685490a483a00e9ebf00d061dbf3168a15d4d0ea363fd706f83`; atualizada em 09/08/2024):

> "As regras para aplicação do percentual de reajuste anual dos planos coletivos são diferentes para os planos coletivos com menos de 30 beneficiários e para os planos com 30 ou mais beneficiários."

> "As operadoras devem reunir em um grupo único todos os seus contratos coletivos com menos de 30 beneficiários para aplicação do mesmo percentual de reajuste."

> "As cláusulas de reajuste dos planos coletivos com 30 ou mais beneficiários são estipuladas por livre negociação entre a pessoa jurídica contratante e a operadora ou administradora de benefícios contratada."

> "Os percentuais acordados devem ser informados pelas operadoras à ANS a cada trimestre, de acordo com os prazos definidos no Art. 2º da IN nº 13/2006."

### Nota da ANS sobre o que o painel cobre

O "Painel de Reajuste dos Planos Coletivos" da ANS e uma aplicacao Power BI; a pagina salva (`bruto/ans/pagina-painel-reajuste-planos-coletivos.html`, sha256 `06dcab6a6bebaced27b36344b2cfa05c1727019fa0bb23c6679161d7808fbe72`) so contem o texto "Microsoft Power BI", sem a nota. Sem navegador, NAO li a nota do painel. O que achei de literal sobre a cobertura esta numa noticia que reproduz o comunicado da ANS de 27/07/2021 (**fonte secundaria**: `bruto/ans/cqcs-ans-divulga-painel-rpc-2021-07-27.html`, sha256 `b5f49539d028e4e3894a3e358833b1068fd3d5858cb585a8d9591363ba9f99e8`):

> "Estão disponíveis dados de janeiro de 2016 a maio de 2021 dos reajustes aplicados aos contratos coletivos em vigor no mercado brasileiro que apresentam formação de preço preestabelecida, ou seja, com valor pré-fixado da mensalidade."

> "reajuste médio: média dos percentuais de reajustes aplicados ponderados pela quantidade de beneficiários no contrato no mês de início de aplicação do reajuste, excluindo-se valores atípicos (outliers) e negociações de reajustes com alteração de fator moderador"

Fonte primaria da ANS sobre o que o sistema recebe: pagina "Reajuste de planos coletivos - RPC" (`bruto/ans/pagina-manual-rpc.html`, sha256 `51e1865d531ba73ce960730d673a6450beefef3369c2268b75ec41ceecf5ccc6`): "As operadoras devem informar os reajustes por variação de custo aplicados sobre os contratos coletivos." E o Manual RPC v3.1.7 de 27/03/2026 (`bruto/ans/Manual_RPC_3.1.7.pdf`, sha256 `9a26c115d535fa14b0ac9b9645ca1e24d9373ce64a562bdcd977cf19578bdee0`, pagina 2): "A Agência Nacional de Saúde Suplementar disponibiliza o aplicativo de comunicado de reajuste de planos coletivos – RPC, como instrumento de envio das informações solicitadas para os comunicados de reajustes que incidirão sobre os planos coletivos privados de assistência à saúde." Campo "Percentual de Reajuste" do manual: "É o percentual referente ao reajuste, revisão ou manutenção incidente no valor da contraprestação pecuniária da contratante no período de aplicação informado." e "Característica do Reajuste": '1' Variação de Custos Assistenciais, '2' Variação no Índice de Utilização, '3' Sem Reajuste, '4' Outra. O manual NAO diz se contratos de preco pos-estabelecido entram; a noticia de 2021 acima diz que o painel cobre os de preco preestabelecido.

O dicionario de dados do arquivo aberto (`bruto/ans/dicionario-pda-043-rpc.ods`, sha256 `bc1217e70d2dcb4d719494bf43ee07cd7f0b6f47dcf0682a6bd359211de2ce6c`) define `QT_BENEF_COMUNICADO` como "o número de beneficiários em cada contrato de um determinado plano, mensurado no último dia útil do mês anterior à aplicação do reajuste", `PC_PERCENTUAL` como "o percentual referente ao reajuste que incide sobre o valor da contraprestação pecuniária da contratante", e `CD_AGRUPAMENTO` (0 = fora do agrupamento; 1 = agrupamento com percentual unico; 2 = agrupamento com sub-agrupamentos).

### Os arquivos baixados

| Arquivo (ANS dados abertos) | Conteudo | Tamanho | Estado |
|---|---|---|---|
| `PDA/RPC/pda-043-rpc-2005_2009.csv` | comunicados de reajuste, inicio de aplicacao 2005-2009 | 422.893.663 bytes | baixado, hasheado |
| `PDA/RPC/pda-043-rpc-2010_2014.csv` | idem 2010-2014 | 856.335.921 bytes | baixado, hasheado |
| `PDA/RPC/pda-043-rpc-AAAAMM.csv` (jan/2015 a ago/2026, 140 arquivos) | idem, um arquivo por mes de inicio | 14 a 61 MB cada | baixados, hasheados |
| total RPC (142 arquivos) | 40.839.792 linhas de 2005 a ago/2026 (contagem por arquivo em `scripts/agregar_rpc.log`) | 6,19 GB | o repositorio guarda so o hash (`.gitignore`; `chain restore` rebaixa) |
| `PDA/percentuais_de_reajuste_de_agrupamento-055/...csv` | percentual de reajuste do agrupamento por operadora e ciclo, 2013-2025 | 608.033 bytes | sha256 `3bba6a6dcc66627184df367757c3048219deb4d96019f494933a5dae8421954c` |
| `PDA/caracteristicas_produtos_saude_suplementar-008/...csv` | cadastro de produtos: cobertura (medica/odontologica) e tipo de contratacao | 74.926.411 bytes | sha256 `dfc3172cd2ccd858858878a0e72d3a2bed65bd0fdd6e8bd2f31c681b82529a73` |
| 7 planilhas xlsx "pool de risco" 2013-2020 e 1 de 2022 | as mesmas operadoras do arquivo 055, como a ANS as publicou nas paginas | pequenas | conferencia: o arquivo 055 bate 100% (518/518 em 2013, 520/520 em 2016, 411/411 em 2022) |

O arquivo de comunicados NAO traz um campo "ate 29 vidas / 30 ou mais". O que distingue e `CD_AGRUPAMENTO`: 1 ou 2 = contrato no agrupamento = coletivo com menos de 30 beneficiarios (grupo "<30 vidas" abaixo); 0 = fora do agrupamento (grupo "fora do agrupamento"), que mistura contratos de 30 ou mais vidas com as excecoes legais de contratos menores listadas pela ANS (anteriores a 1999 e nao adaptados, so odontologicos, ex-empregados, preco pos-estabelecido, anteriores a 2013 nao aditados). Antes de maio/2013 nao ha agrupamento: o grupo "fora do agrupamento" de 2005-2012 inclui contratos pequenos. Empresarial x adesao vem do cadastro de produtos (`GR_CONTRATACAO`, retrato atual de 21/10/2026, por `ID_PLANO`); cobertura medico-hospitalar x odontologica tambem. Todas as linhas do RPC cruzaram com o cadastro (0 linhas sem correspondencia).

Criterios: ano = ano do inicio da aplicacao (`DT_INIC_APLICACAO`); excluidas as linhas `LG_NEGOCIACAO = 1` (aviso de reajuste em negociacao: de 7.206 em 2005 a 95.108 em 2013, 5.717 em 2014 e zero a partir de 2015); mediana "por linha" = uma observacao por contrato-plano comunicado; media ponderada = por `QT_BENEF_COMUNICADO`. Percentuais ZERO ("manutencao" / sem reajuste, ver manual) ficaram DENTRO da conta principal: pesam 32% dos beneficiarios medicos em 2005, 22% em 2013, 16% em 2020 e 5,5% em 2024, entao puxam a media ponderada para baixo; as duas ultimas colunas da tabela de janelas mostram o composto sem zeros. Valores atipicos (reajuste acima de 100%) ficaram DENTRO: pesam menos de 0,25% dos beneficiarios em todo ano (maximo 0,212% em 2013; 0,050% em 2024). Nao exclui contratos com alteracao de fator moderador.

### Tabela por ano

Colunas: teto individual da ANS do ciclo que comeca em maio do ano; IPCA plano de saude no ciclo (abril do ano a abril do ano seguinte, para comparar com o teto) e dez/dez; IPCA geral dez/dez; agrupamento (arquivo 055), media ponderada por beneficiarios das operadoras com percentual unico; planos coletivos MEDICO-HOSPITALARES do arquivo RPC: mediana por linha, media ponderada por beneficiarios, media ponderada so dos contratos com menos de 30 vidas, media ponderada dos contratos fora do agrupamento, e soma de `QT_BENEF_COMUNICADO` no ano (soma de linhas, pode contar a mesma pessoa mais de uma vez). Todos em %, salvo a ultima coluna. 2026 e parcial (jan a ago) e o ciclo 2026 do IPCA ainda nao fechou.

| Ano | Teto indiv. ANS | IPCA plano saude (abr-abr) | IPCA plano saude (dez/dez) | IPCA geral (dez/dez) | Agrupamento 055, pond. | Coletivos med., mediana linha | Coletivos med., pond. benef. | Coletivos med. <30 vidas, pond. | Coletivos med. fora do agrup., pond. | Benef. comunicados (soma) |
|---|---|---|---|---|---|---|---|---|---|---|
| 2000 | 5,42 | 3,79 | 5,42 | 5,97 |  |  |  |  |  |  |
| 2001 | 8,71 | 7,22 | 4,28 | 7,67 |  |  |  |  |  |  |
| 2002 | 7,69 | 8,20 | 8,42 | 12,53 |  |  |  |  |  |  |
| 2003 | 9,27 | 9,11 | 8,66 | 9,30 |  |  |  |  |  |  |
| 2004 | 11,75 | 11,25 | 10,51 | 7,60 |  |  |  |  |  |  |
| 2005 | 11,69 | 13,54 | 12,03 | 5,69 |  | 11,69 | 7,67 |  | 7,67 | 24.007.455 |
| 2006 | 8,89 | 10,07 | 12,29 | 3,14 |  | 9,30 | 7,06 |  | 7,06 | 30.929.536 |
| 2007 | 5,76 | 7,12 | 8,13 | 4,46 |  | 8,89 | 6,39 |  | 6,39 | 31.221.140 |
| 2008 | 5,48 | 5,98 | 6,17 | 5,90 |  | 8,66 | 5,81 |  | 5,81 | 32.427.565 |
| 2009 | 6,76 | 6,62 | 6,39 | 4,31 |  | 8,37 | 7,00 |  | 7,00 | 36.965.122 |
| 2010 | 6,73 | 7,12 | 6,87 | 5,91 |  | 9,96 | 7,87 |  | 7,87 | 33.441.706 |
| 2011 | 7,69 | 7,60 | 7,55 | 6,50 |  | 10,95 | 9,07 |  | 9,07 | 32.283.794 |
| 2012 | 7,93 | 7,97 | 7,76 | 5,84 |  | 11,00 | 10,11 |  | 10,11 | 35.012.265 |
| 2013 | 9,04 | 9,06 | 8,73 | 5,91 | 14,45 | 13,06 | 10,68 | 16,13 | 10,67 | 37.664.844 |
| 2014 | 9,65 | 9,65 | 9,46 | 6,41 | 15,99 | 15,00 | 11,78 | 14,43 | 11,77 | 36.780.290 |
| 2015 | 13,55 | 13,45 | 12,16 | 10,67 | 14,62 | 16,31 | 13,30 | 15,24 | 13,13 | 33.093.933 |
| 2016 | 13,57 | 13,61 | 13,57 | 6,29 | 17,72 | 16,49 | 16,57 | 17,09 | 16,52 | 30.170.091 |
| 2017 | 13,55 | 13,49 | 13,53 | 2,95 | 17,96 | 18,49 | 14,64 | 17,31 | 14,30 | 30.186.627 |
| 2018 | 10,00 | 10,01 | 11,16 | 3,75 | 14,80 | 15,76 | 12,26 | 15,22 | 11,71 | 31.024.404 |
| 2019 | 7,35 | 7,39 | 8,24 | 4,31 | 13,00 | 13,20 | 10,54 | 14,02 | 10,01 | 31.799.003 |
| 2020 | 8,14 | 2,75 | 2,47 | 4,52 | 10,74 | 11,76 | 8,00 | 11,87 | 7,39 | 32.126.484 |
| 2021 | -8,19 | -3,08 | 2,33 | 10,06 | 8,59 | 8,63 | 6,88 | 9,16 | 6,49 | 33.900.117 |
| 2022 | 15,50 | 15,27 | 6,89 | 5,78 | 16,07 | 12,50 | 12,38 | 13,60 | 12,12 | 34.811.415 |
| 2023 | 9,63 | 9,57 | 11,50 | 4,62 | 19,82 | 18,10 | 14,40 | 18,40 | 13,51 | 33.852.840 |
| 2024 | 6,91 | 7,06 | 7,88 | 4,83 | 17,04 | 16,97 | 13,60 | 17,48 | 12,69 | 33.490.020 |
| 2025 | 6,06 | 6,10 | 6,44 | 4,26 | 14,01 | 15,11 | 11,42 | 14,47 | 10,75 | 35.006.320 |
| 2026 | 5,11 |  |  |  |  | 12,47 | 9,96 | 12,34 | 9,37 | 21.840.461 |

Nota: a coluna "<30 vidas" fica em branco antes de 2013 porque o agrupamento so existe a partir de maio/2013 (2012 tem 25 linhas medicas com a marca de agrupamento). Em 2013 e 2014 a marca cobre so 12.350 e 16.923 linhas medicas, contra 564 mil em 2015: adesao gradual dos contratos anteriores a 2013, que era opcional. O arquivo 055 (coluna "Agrupamento 055") cobre as operadoras inteiras desde 2013, e o composto dele (+436,55% desde dez/2012) fica proximo ao do RPC (+433,26%).

Arquivos: `derivado/tabela_por_ano.csv` (todas as colunas, inclusive empresarial, adesao, odontologico e "todos"), `series/ans_rpc_coletivos_por_ano.csv`, `series/ans_agrupamento_pda055.csv`. Sub-agrupados (3 percentuais por operadora, 3 a 24 operadoras por ciclo) ficaram fora da coluna "Agrupamento 055" e estao em `derivado/agrupamento_por_ciclo.csv`.

### Acumulados por janela (%; coletivos = reajustes anuais compostos, media ponderada por beneficiarios)

| Janela | Teto indiv. ANS | IPCA plano saude | IPCA geral | Coletivos med. (todos) | Coletivos med. <30 vidas (RPC) | Coletivos med. fora do agrup. | Coletivos med. empresariais | Coletivos med. por adesao | Agrupamento 055 (<30 vidas) | Coletivos med. (todos), sem zeros | Coletivos med. <30 vidas, sem zeros |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dez/1999-dez/2024 | 652,41 | 660,34 | 346,98 |  |  |  |  |  |  |  |  |
| dez/2001-dez/2024 | 556,54 | 591,61 | 291,72 |  |  |  |  |  |  |  |  |
| dez/2004-dez/2024 | 399,27 | 431,24 | 195,99 | 604,91 |  | 575,72 | 564,93 | 810,97 |  | 907,26 |  |
| dez/2012-dez/2024 | 177,86 | 179,19 | 97,10 | 291,89 | 433,26 | 275,67 | 283,56 | 338,03 | 436,55 | 353,12 | 435,86 |
| dez/2014-dez/2024 | 132,40 | 134,59 | 74,90 | 216,77 | 301,27 | 203,69 | 211,58 | 244,04 | 304,18 | 248,43 | 303,22 |
| dez/2018-dez/2022 | 23,10 | 21,32 | 26,93 | 43,40 | 58,19 | 41,06 | 43,20 | 44,58 | 57,73 | 49,88 | 58,56 |

Como ler: o composto dos coletivos aplica, a cada ano, a media ponderada dos reajustes com inicio de aplicacao naquele ano, a partir de uma base (dez do ano anterior ao primeiro ano com dado). E ordem de grandeza do que os contratos receberam de reajuste, nao o preco de uma mensalidade. Janelas que comecam antes de 2013 atravessam a criacao do agrupamento e a entrada de dados mais completos (a base comeca em 2005): para comparar coletivos com o IPCA use dez/2012-dez/2024 e dez/2014-dez/2024. A janela dez/2004-dez/2024 e a que o Ulisses pode ver como "toda a serie", mas 2005-2012 vem de um periodo de comunicacao menos completa (nao medido) e o agrupamento nao existia. Indices anuais completos: `derivado/indices_compostos_coletivos.csv`. Para dez/2018-dez/2022 a conta de cada coluna inclui os anos 2019 a 2022 (os reajustes de 2020 e 2021 foram afetados pela suspensao da ANS).

Conferencia de ordem de grandeza (secundaria, nao hasheada): uma busca na web reportou, para jan-ago/2025, reajuste medio de 11,15% nos coletivos e 14,81% nos de menos de 30 vidas, do Painel da ANS. Recalculei jan-ago/2025 no arquivo bruto com os criterios do painel (medico-hospitalar, sem negociacao, sem alteracao de fator moderador, sem reajuste acima de 100%): 11,64% (todos) e 15,22% (<30 vidas). Diferenca de ate 0,5 ponto; a pagina que trazia os numeros respondeu HTTP 500 quando tentei baixa-la, entao nao a citei como prova.

## 3. IBGE: como o subitem "plano de saude" do IPCA e calculado

Fonte: IBGE, "Sistema Nacional de Indices de Precos ao Consumidor: Metodos de calculo, 7a edicao" (27/08/2013, a mais recente da pasta do FTP; a pasta tem tambem as edicoes 4 a 6). URL: `https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/Sistema_de_Indices_de_Precos_ao_Consumidor/Metodos_de_calculo/2013_08_27_srm_calculo_7ed.zip` (zip com um PDF), sha256 do zip `90746f9c1b42c41dce68fc3e8b59aed4047299cc1336a925dba61921ade88c52`, pagina 35 do PDF; texto em `derivado/texto-ibge/Metodos_de_Calculo_7ed.txt`. Corroboracao: o paragrafo e identico na 6a edicao (2012), pagina 39 do PDF, `https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/Sistema_de_Indices_de_Precos_ao_Consumidor/Metodos_de_calculo/Metodos_de_Calculo_6ed.pdf`, sha256 `022f367e72b9adc30e6d18b6681f9421b446aaf2e69aaaf6a51f73674ce56177`. Na 7a edicao a unica ocorrencia de "coletiv" e "negociacao coletiva" (politica salarial de 1991) e "faixa et" nao ocorre.

> "Com vistas a estimar a variação das mensalidades dos contratos individuais e familiares dos planos de saúde para cálculo dos índices de preços ao consumidor, o IBGE, desde 2001, apropria os percentuais de reajuste incidentes sobre os contratos assinados num período de um ano ou mais, abrangendo a maioria dos usuários."

> "A pesquisa consiste em visitar, a cada mês, as operadoras mais representativas, ou seja, aquelas que, notoriamente, agregam o maior número de clientes. Em cada uma delas, obtém-se a informação do percentual de reajuste aplicado sobre as mensalidades dos contratos que estão fazendo aniversário no mês da pesquisa. O percentual informado, em geral, baseia-se no reajuste fixado pela Agência Nacional de Saúde Suplementar - ANS. Um reajuste anual é normalmente fixado no mês de maio com vistas a vigorar nos 12 meses seguintes. A aplicação tem início para os usuários de acordo com a data de aniversário de cada plano."

> "- identificam-se quais os planos novos (aqueles posteriores a 1o de janeiro de 1999) e os planos antigos (anteriores a essa mesma data); - calcula-se, por operadora, a variação total média anual ponderada pelas participações dos planos novos e antigos, conforme informação obtida junto à ANS; - extrai-se a raiz 12 do valor obtido no item anterior, chegando-se, assim, à variação média mensal, por operadora; e - aplica-se a média geométrica sobre as variações mensais de todas as operadoras da região."

Nota técnica 05/2020 do IBGE (`bruto/ibge/snipc_nota_tecnica_2020_05.pdf`, sha256 `520caec248279d675e295fa9c4ff587e1d06425f984f8e64c43ee80c0e955db2`): "Cabe ressaltar que a ANS define os percentuais máximos de reajuste tanto para planos individuais novos (posteriores a 1º de janeiro de 1999, regidos pela lei 9.656/98) como para os planos anteriores a essa lei, que têm o reajuste regulamentado por Termos de Compromisso. O IBGE incorpora os percentuais efetivamente aplicados pelas operadoras pertencentes à amostra de cada região pesquisada." Nota técnica 03/2020 (`bruto/ibge/snipc_nota_tecnica_2020_03.pdf`, sha256 `a0e696eb84024af4ac37c19983cc73c5d4fff89ac694d1612225a8e95e697fda`): "a ANS decidiu suspender a aplicação de reajustes aos contratos de planos de saúde para todos os tipos de plano até o fim de 2020".

Respostas as perguntas:

| Pergunta | Resposta pelo texto do IBGE |
|---|---|
| O reajuste da ANS e diluido em 12 meses? | Sim: tira-se a raiz 12 do reajuste anual medio e aplica-se a fracao mensal (a nota 05/2020 confirma a fracao mensal, inclusive 12 parcelas em 2021). |
| Planos coletivos entram? | Nao. O texto (7a e 6a edicoes) fala em "contratos individuais e familiares". Das notas tecnicas do SNIPC que baixei (2018-04, 2019-01, 2020-02 a 05, 2026-01), so a 03/2020 e a 05/2020 falam de plano de saude, e nenhuma menciona coletivo ou reajuste por faixa etaria. |
| Desde quando? | "desde 2001" (aprox. jul/2001 pelos dados; antes, o comportamento e outro, ver `quebras.csv`). |
| Reajuste por mudanca de faixa etaria entra? | O texto so descreve o reajuste anual do contrato; nao menciona faixa etaria. Ausencia de mencao, nao prova de exclusao. |
| E o reajuste fixado ou o aplicado? | "Em geral" o fixado pela ANS (Metodos); "os percentuais efetivamente aplicados pelas operadoras" da amostra (NT 05/2020). |

## 4. Exemplo nomeado, ILUSTRATIVO: planos individuais Amil (RJ), tabelas de venda 2006-2010

Rotulo: **fonte primaria da empresa, via Wayback; preco de venda para contrato novo; ilustracao, nao serie de preco pago.** Todas as capturas sao PDFs da propria Amil em `amil.com.br`, baixados na forma crua do Wayback (`.../web/<timestamp>id_/<url original>`), com sha256 na cadeia (`bruto/amil-wayback/`, 16 PDFs; texto extraido com pdftotext em `derivado/texto-amil/`). CDX consultado: dominio `amil.com.br`, status 200, 14.443 URLs (a propria consulta esta hasheada em `bruto/amil-wayback/cdx-amil.com.br-status200.txt`, sha256 `ea73ed7a7c5f105ea75534041b03c603bdf9b0dfc9c2dc9a93ceea626f45b9fc`). Cada linha de `series/amil_pf_rj_tabelas_wayback.csv` traz `url_arquivada` e `sha256_do_pdf`.

Tabelas de preco PF (individual) com valor por faixa etaria extraidas (`series/amil_pf_rj_tabelas_wayback.csv`: arquivo, data da captura, validade, plano, faixa, acomodacao QC/QP, valor, linha do texto):

| Captura (Wayback) | Documento | Validade segundo o documento | sha256 |
|---|---|---|---|
| 2006-05-11 | `AMIL-TabVendasPF200605-RJ.pdf` | a partir de maio de 2006 | `ed814195ce5f...` |
| 2007-02-28 | `AMIL-tabPF200611-RJ.pdf` | a partir de novembro (de 2006, pelo nome) | `6e7ab543920f...` |
| 2009-03-06 | `Amil-TabVendas-PF200902-RJ.pdf` | fevereiro de 2009 (pelo nome) | `8b6113a10f7a...` |
| 2010-06-02 | `Tabela_PF_RJ_012010.pdf` | "Preços e planos válidos até 28/2/2010" | `9c94fa90f03d...` |

Hashes completos no `manifest.jsonl`. Os outros 12 PDFs (`v-0377-miolo-tab-vendas6` 2009-08 e `v-0868-02-Tab-Amil-Dez` 2010-02, que tem tabelas de preco; `individual920`; `RD400`; `Amil-instVendas-*`, circulares de vendas; cinco aditivos PRC) foram baixados e hasheados, mas NAO tabulados.

**O plano "Amil 400" nao aparece.** O unico "400" em PDFs da Amil nesse CDX e `RD400.pdf` (captura 2010-11-22), que e um contrato odontologico ("cobertura dos custos dos procedimentos de assistência odontológica"), nao o plano medico. Os nomes comerciais mudam: Amil 20/30/40/50/60 (2006), Amil 110 a 160 (2009), Amil Blue I a IV (2010). Nao ha serie continua de um mesmo produto de 2006 a 2024.

Comparacoes possiveis (`derivado/amil_comparacoes_rotulo.csv`; pares por rotulo ou, onde marcado, so por valor; PF individual, RJ, acomodacao QP):

| Captura A -> B | Plano A -> B | Faixa | Valor (R$/mes) A -> B | Variacao % |
|---|---|---|---|---|
| 2006-05-11 -> 2007-02-28 | AMIL 40 101 QP -> Amil 40 101 QP | 0 a 18 | 175.00 -> 180.25 | 3.00 |
| 2006-05-11 -> 2007-02-28 | AMIL 40 101 QP -> Amil 40 101 QP | 44 a 48 | 428.75 -> 441.62 | 3.00 |
| 2006-05-11 -> 2007-02-28 | AMIL 40 101 QP -> Amil 40 101 QP | 59+ | 1050.00 -> 1081.50 | 3.00 |
| 2006-05-11 -> 2007-02-28 | AMIL 40 PLUS -> Amil 40 PLUS QP | 0 a 18 | 197.00 -> 202.91 | 3.00 |
| 2006-05-11 -> 2007-02-28 | AMIL 40 PLUS -> Amil 40 PLUS QP | 44 a 48 | 482.64 -> 497.11 | 3.00 |
| 2006-05-11 -> 2007-02-28 | AMIL 40 PLUS -> Amil 40 PLUS QP | 59+ | 1182.00 -> 1217.46 | 3.00 |
| 2006-05-11 -> 2007-02-28 | AMIL 30 Especial -> AMIL 30 ESPECIAL | 0 a 18 | 162.75 -> 167.63 | 3.00 |
| 2006-05-11 -> 2007-02-28 | AMIL 30 Especial -> AMIL 30 ESPECIAL | 44 a 48 | 398.75 -> 410.68 | 2.99 |
| 2006-05-11 -> 2007-02-28 | AMIL 30 Especial -> AMIL 30 ESPECIAL | 59+ | 976.50 -> 1005.78 | 3.00 |
| 2006-05-11 -> 2007-02-28 | AMIL 20 -> Amil 20 QP | 0 a 18 | 126.79 -> 130.59 | 3.00 |
| 2006-05-11 -> 2007-02-28 | AMIL 20 -> Amil 20 QP | 44 a 48 | 310.63 -> 319.96 | 3.00 |
| 2006-05-11 -> 2007-02-28 | AMIL 20 -> Amil 20 QP | 59+ | 760.74 -> 783.54 | 3.00 |
| 2009-03-06 -> 2010-06-02 | Amil 110 Nacional QP -> Amil Blue II Nacional QP | 0 a 18 | 132.50 -> 132.50 | 0.00 |
| 2009-03-06 -> 2010-06-02 | Amil 110 Nacional QP -> Amil Blue II Nacional QP | 44 a 48 | 324.62 -> 324.62 | 0.00 |
| 2009-03-06 -> 2010-06-02 | Amil 110 Nacional QP -> Amil Blue II Nacional QP | 59+ | 795.00 -> 795.00 | 0.00 |
| 2009-03-06 -> 2010-06-02 | Amil 120 Nacional QP -> Amil Blue III Nacional QP | 0 a 18 | 153.70 -> 153.70 | 0.00 |
| 2009-03-06 -> 2010-06-02 | Amil 120 Nacional QP -> Amil Blue III Nacional QP | 44 a 48 | 376.55 -> 376.55 | 0.00 |
| 2009-03-06 -> 2010-06-02 | Amil 120 Nacional QP -> Amil Blue III Nacional QP | 59+ | 922.20 -> 922.20 | 0.00 |
| 2009-03-06 -> 2010-06-02 | Amil 130 Nacional QP -> Amil Blue IV Nacional QP | 0 a 18 | 174.90 -> 174.90 | 0.00 |
| 2009-03-06 -> 2010-06-02 | Amil 130 Nacional QP -> Amil Blue IV Nacional QP | 44 a 48 | 428.50 -> 428.50 | 0.00 |
| 2009-03-06 -> 2010-06-02 | Amil 130 Nacional QP -> Amil Blue IV Nacional QP | 59+ | 1049.40 -> 1049.40 | 0.00 |

Leitura: entre a tabela de maio e a de novembro de 2006 o preco de venda dos planos de mesmo rotulo subiu 3,0% em todas as faixas; de fev/2009 a jan/2010 a tabela de venda ficou igual nos tres produtos renomeados (ate onde os valores coincidem). Isso e preco de tabela para quem contrata, nao reajuste de contrato em vigor (o teto da ANS no ciclo 2006 foi 8,89% e em 2009, 6,76%) e nao inclui reajuste por faixa etaria.

## 5. O que nao foi achado ou nao foi feito

- Preco do Amil 400 medico, ou qualquer preco de plano individual Amil entre 2011 e 2024: nao ha tabela de preco no CDX do Wayback para `amil.com.br` nesse periodo (as paginas de tabela de 2011-2015 sao telas de login, sem valores). Documentos da ANS (NIP, decisoes) que citem valores de mensalidade Amil: NAO pesquisados. Tabelas de corretoras: nao usadas.
- A nota literal do Painel de Reajuste (Power BI) da ANS: nao lida (sem navegador). Usei o comunicado da ANS reproduzido por noticia (secundaria) e o dicionario de dados (primario).
- Cobertura da base RPC antes de 2013: nao ha total de beneficiarios coletivos na base para medir; a soma de `QT_BENEF_COMUNICADO` por ano (27,6 milhoes em 2005, 59 milhoes em 2025 contando odonto) e soma de linhas, nao pessoas. Participacao dos coletivos no mercado: nao medida aqui.
- Duplicidades: em jan/2015, 341 de 93.511 linhas (0,4%) repetem a chave plano-contrato-operadora-inicio; nao deduplicado nas demais.
- Efeito de excluir outliers e fator moderador nos anos todos: so verificado em jan-ago/2025.
- Planos individuais antigos (pre-1999): pagina salva, nao lida. Reajuste por faixa etaria: nao coletado.
- Empresarial x adesao: so planos com tipo de contratacao unico no cadastro atual; planos "mistos" ou "nao identificados" ficam fora dessas duas colunas.
- Tabelas de venda 2006: nomes de produto no PDF mudam de coluna para coluna; a coluna `produto_titulo` do CSV pode estar errada (ex.: a coluna "AMIL 30 Especial" aparece sob o titulo "AMIL 40"); use `coluna_rotulo_no_documento`.

## 6. Verificacao da cadeia

```
197 lines; head 0894b3ac0b307ab130ae24546f22cc3e88363026a224cb83fdd2209d0725f8a4; OK
(exit 0; manifest com 197 linhas)
```

Reproducao: as aquisicoes fora do RPC (paginas e arquivos da ANS, IBGE, Wayback) foram feitas uma a uma com `govfc.chain add` (URL de cada uma no `manifest.jsonl`); `scripts/baixar_rpc.sh` (RPC), `construir_individual.py`, `construir_agrupamento.py`, `agregar_rpc.py` (~3 min), `consolidar.py`, `blocos_amil.py`/`construir_amil.py`/`comparar_amil.py`, `gerar_resultado.py`. Historico e becos: `quebras.csv` (5 linhas, cabecalho igual ao de `moeda-fiscal/quebras.csv`).
