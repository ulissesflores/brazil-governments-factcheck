# Colheita histórica: mandatos, planos monetários, preços administrados, IPCA e circulação do infográfico

Data da colheita e do acesso a todas as URLs: 2026-10-19. Pasta: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/historia/`.
Toda cópia salva fica em `bruto/` e está na cadeia de hash `manifest.jsonl` (103 linhas, `manifest_tool.py verify` = OK; metadata reconstruída, timestamp = mtime). Convenção: ❓ = sem fonte primária lida nesta colheita; "opinião" = interpretação de analista, não dado.

## 0. Achados que mudam o texto do artigo

- O infográfico cobre 8 dos 13 presidentes do período 1964-2026 (convenção: 13 pessoas, Lula contado uma vez, sem Junta Militar e sem Mazzilli) e omite 5 governos inteiros: Castelo Branco, Geisel, Figueiredo, Sarney e Collor (257,6 meses de 750,1, ou 34,3% do tempo entre 15/04/1964 e 19/10/2026). Fonte: tabela 1.
- As janelas de dados não coincidem com os mandatos: a coluna Itamar usa 36 meses (1992-1994) para um governo de 27 meses; Dilma e Temer contam o ano de 2016 inteiro duas vezes; a coluna Lula 3 usa dados de 2023-2025 (36 meses) para um mandato que já corre há 45,6 meses. Fonte: tabela 2.
- "IPCA 1967-73" é rótulo impossível: o IPCA foi criado em dezembro de 1979 (IBGE). Antes, de 1948 a junho de 1978, os índices de preços ao consumidor eram do Ministério do Trabalho. Fonte: seção 4.
- O IPCA foi o indexador oficial único só de novembro/1985 a março/1986, e o IBGE documenta que a inflação anterior aos planos foi "represada" no IPC de junho/1987 e janeiro/1989. Fonte: seção 3.
- A imagem do X é idêntica em pixels à cópia do WhatsApp (mesmas 1312x1199, diferença média de 0,69 em 255, 0% dos pixels com diferença > 20). Nenhuma versão anterior achada. Fonte: seção 5.

## 1. Chefes de governo, 1964-2026

Convenção de datas: posse e saída como a fonte dá. "Cobertura" = o governo é a coluna do infográfico (SIM), aparece só dentro do rótulo de outra coluna (PARCIAL) ou não aparece (NÃO).

| # | Chefe de governo | Posse | Saída | Duração (meses) | Cobertura no infográfico | Fonte principal (cópia local) |
|---|---|---|---|---|---|---|
| 0 | Ranieri Mazzilli (interino) | 02/04/1964 | 15/04/1964 | 0,4 | NÃO | Arquivo Nacional, "Os Presidentes e a República", 3ª ed., 2012: cabeçalho "2.4.1964 - 15.4.1964". https://www.gov.br/arquivonacional/pt-br/servicos/publicacoes/OspresidenteseaRepblica_DeodoroDilma.pdf (`bruto/arquivo-nacional-presidentes-e-a-republica.txt`) |
| 1 | Humberto de Alencar Castelo Branco | 15/04/1964 | 15/03/1967 | 35,0 | NÃO | Arquivo Nacional (mesmo PDF: "15.4.1964 - 15.3.1967"); Câmara dos Deputados https://www2.camara.leg.br/a-camara/conheca/historia/Ex_presidentesCD_Republica/republica5.html (`bruto/noticias/camara-republica5.txt`, "15.04.1964 - Toma posse... 15 de abril de 1964 a 15 de março de 1967"); Secretaria-Geral/Biblioteca da PR https://www.gov.br/secretariageral/pt-br/centrais-de-conteudo/biblioteca-da-pr/galeria-dos-ex-presidentes/castello_branco ("Posse 15.04.1964") |
| 2 | Artur da Costa e Silva | 15/03/1967 | 31/08/1969 | 29,5 | SIM (coluna "Ditadura Militar: Costa e Silva e Médici") | Arquivo Nacional ("15.3.1967 - 31.8.1969"); Câmara (republica5, 15.03.1967) |
| 3 | Junta Militar (Rademaker, Lyra Tavares, Souza e Melo) | 31/08/1969 | 30/10/1969 | 2,0 | NÃO citada (cai dentro da janela do rótulo) | Arquivo Nacional ("Junta militar 31.8.1969 - 30.10.1969"); Câmara (republica5, 31.08.1969, Ato Institucional 12) |
| 4 | Emílio Garrastazu Médici | 30/10/1969 | 15/03/1974 | 52,5 | SIM (mesma coluna) | Planalto, Ato Institucional 16, de 14/10/1969, art. 4º e 5º: posse em 30/10/1969, mandato termina em 15/03/1974. https://www.planalto.gov.br/ccivil_03/ait/ait-16-69.htm (`bruto/planalto-legislacao/planalto-ait-16-69.txt`); Arquivo Nacional ("30.10.1969 - 15.3.1974") |
| 5 | Ernesto Geisel | 15/03/1974 | 15/03/1979 | 60,0 | NÃO (mas o cabeçalho "1967-1974" invade 9,5 meses de 1974) | Arquivo Nacional ("15.3.1974 - 15.3.1979"); Câmara (republica5) |
| 6 | João Baptista de Oliveira Figueiredo | 15/03/1979 | 15/03/1985 | 72,0 | NÃO | Arquivo Nacional ("15.3.1979 - 15.3.1985"); Câmara (republica5) |
| 7 | José Sarney | 15/03/1985 | 15/03/1990 | 60,0 | NÃO | Arquivo Nacional ("15.3.1985 - 15.3.1990"); Secretaria-Geral https://www.gov.br/secretariageral/pt-br/centrais-de-conteudo/biblioteca-da-pr/galeria-dos-ex-presidentes/jose_sarney ("de 15/03/1985 a 15/03/1990"; posse em 15/03/1985; exerce a Presidência por sucessão desde 21/04/1985 pela morte de Tancredo Neves) |
| 8 | Fernando Collor de Mello | 15/03/1990 | afastado em 02/10/1992; renúncia em 29/12/1992 | 30,6 (até o afastamento) | NÃO (mas 9 meses de 1992 e o ano de 1990 entram na coluna Itamar) | Arquivo Nacional ("15.3.1990 - 2.10.1992"); Câmara, "20 anos do impeachment" https://www2.camara.leg.br/atividade-legislativa/plenario/discursos/escrevendohistoria/destaque-de-materias/20-anos-do-impeachment (`bruto/noticias/camara-20anos-impeachment-collor.txt`: afastamento 02/10/1992, renúncia e início do julgamento 29/12/1992, Resolução do Senado 101/1992 em 30/12/1992) |
| 9 | Itamar Franco | 02/10/1992 (interino); 29/12/1992 (posse formal) | 01/01/1995 | 27,0 (desde 02/10/1992) | SIM (coluna "Itamar Franco 1992-1994") | Arquivo Nacional ("2.10.1992 - 1.1.1995"); Secretaria-Geral https://www.gov.br/secretariageral/pt-br/centrais-de-conteudo/biblioteca-da-pr/galeria-dos-ex-presidentes/itamar-augusto-cautiero-franco ("Posse 29/12/1992, empossado formalmente pelo Congresso Nacional") |
| 10 | Fernando Henrique Cardoso | 01/01/1995 | 31/12/2002 (posse do sucessor em 01/01/2003) | 96,0 | SIM | Secretaria-Geral https://www.gov.br/secretariageral/pt-br/centrais-de-conteudo/biblioteca-da-pr/galeria-dos-ex-presidentes/fernando-henrique-cardoso ("01/01/1995 a 31/12/1998" e "01/01/1999 a 31/12/2002"); Arquivo Nacional |
| 11 | Luiz Inácio Lula da Silva (1º e 2º mandatos) | 01/01/2003 | 31/12/2010 (posse da sucessora em 01/01/2011) | 96,0 | SIM | Arquivo Nacional ("1.1.2003 - 1.1.2007" e "1.1.2007 - 1.1.2011"); Secretaria-Geral https://www.gov.br/secretariageral/pt-br/centrais-de-conteudo/biblioteca-da-pr/galeria-dos-ex-presidentes/luiz-inacio-lula-da-silva (posses 01/01/2003 e 01/01/2007) |
| 12 | Dilma Rousseff | 01/01/2011 | afastada em 12/05/2016; perde o mandato em 31/08/2016 | 68,0 (até 31/08/2016); 64,4 (até o afastamento) | SIM (coluna "2011-2016") | Senado Notícias, 31/08/2016 https://www12.senado.leg.br/noticias/materias/2016/08/31/dilma-rousseff-perde-o-mandato-e-temer-e-confirmado-presidente (`bruto/noticias/senado-2016-08-31-dilma-perde-mandato.txt`: 12/05 "afastamento temporário", 31/08 condenada por 61 a 20); Câmara, 12/05/2016 https://www.camara.leg.br/noticias/487742-senado-aprova-abertura-de-processo-de-impeachment-e-afasta-dilma-por-180-dias; Secretaria-Geral https://www.gov.br/secretariageral/pt-br/centrais-de-conteudo/biblioteca-da-pr/galeria-dos-ex-presidentes/dilma-vana-rousseff |
| 13 | Michel Temer | 12/05/2016 (interino); 31/08/2016 (efetivo) | 31/12/2018 (posse do sucessor em 01/01/2019) | 31,6 (desde 12/05/2016); 28,0 (desde 31/08/2016) | SIM (coluna "2016-2018") | Rádio Senado, 12/05/2016 https://www12.senado.leg.br/radio/1/noticia/2016/05/12/michel-temer-ja-e-o-novo-presidente-em-exercicio-da-republica; Câmara, 31/08/2016 https://www.camara.leg.br/noticias/497259-michel-temer-toma-posse-como-presidente-da-republica/ ("mandato que termina em 31 de dezembro de 2018") |
| 14 | Jair Bolsonaro | 01/01/2019 | 31/12/2022 (posse do sucessor em 01/01/2023) | 48,0 | SIM | Câmara/Radioagência, 01/01/2019 https://www.camara.leg.br/radio/radioagencia/550452-saiba-como-foi-a-cerimonia-de-posse-do-presidente-jair-bolsonaro/; Senado Notícias, 01/01/2023, sobre a posse de Lula (marca o fim do mandato anterior) |
| 15 | Lula (3º mandato) | 01/01/2023 | previsto: posse do sucessor em 05/01/2027 | 45,6 até 19/10/2026; 48,1 se cumprir até 05/01/2027 | SIM (coluna "Lula 3º mandato, em andamento") | Senado Notícias, 01/01/2023 https://www12.senado.leg.br/noticias/materias/2023/01/01/congresso-empossa-lula-e-alckmin-na-presidencia-da-republica ("Congresso Nacional deu posse neste domingo (1º)"); Emenda Constitucional 111/2021, art. 4º, https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc111.htm ("mandatos durarão até a posse de seus sucessores, em 5 e 6 de janeiro de 2027") |

Totais (cálculo próprio sobre as datas acima; meses = dias/30,4375): período 15/04/1964 a 19/10/2026 = 750,1 meses. Governos omitidos como coluna: Castelo Branco 35,0 + Geisel 60,0 + Figueiredo 72,0 + Sarney 60,0 + Collor 30,6 = 257,6 meses (34,3%). Cobertos por coluna: 492,5 meses (65,7%). Do regime militar (15/04/1964 a 15/03/1985 = 251 meses), o infográfico cobre Costa e Silva + Junta + Médici = 84,0 meses (33%).

Observações de qualidade das fontes (cada uma é um defeito do próprio site oficial, registrado para não ser copiado):

| Fonte | Defeito observado | Tratamento |
|---|---|---|
| Secretaria-Geral, página de Lula | "01/01/2003 a 31/01/2006" e "01/01/2007 a 31/01/2010" (o dia 31/01 é erro de digitação por 31/12) | Usada a data de 31/12 por coerência com o Arquivo Nacional ("1.1.2007 - 1.1.2011") e com o art. 82 da CF (mandato de 4 anos, início em 1º de janeiro). |
| Secretaria-Geral, página de Dilma | Segundo mandato "Posse 01/01/2011" (deveria ser 01/01/2015) | Posse de 2015 não lida em fonte primária nesta colheita ❓. |
| Secretaria-Geral, página de Castelo Branco | "de 15/03/1964 a 15/03/1967" (início antes do golpe; a própria página dá posse em 15.04.1964) | Usada a posse de 15/04/1964 (Arquivo Nacional e Câmara). |
| Secretaria-Geral, página de Collor | "15/03/1990 a 01/01/1995" (é o período do mandato eleito, não o exercício efetivo) | Usadas as datas do Arquivo Nacional e da Câmara. |
| Secretaria-Geral, página de Itamar | "de 15/03/1990 a 31/12/1994" (período do mandato para o qual foi eleito vice) | Idem; a posse formal de 29/12/1992 é a única data que a página dá para ele. |
| Câmara, república 5 | Para Costa e Silva escreve "período encerrado a 31 de agosto de 1967" (o ano correto é 1969) e atribui à "AI 6" a declaração de vacância de 14/10/1969 (o ato do Planalto é o AI-16) | Usada a data de 31/08/1969 (Arquivo Nacional) e o AI-16 lido no Planalto. |
| Rádio Senado, podcast "Senado 200 anos", Dilma | Diz que em "17 abril de 2016" Dilma foi afastada interinamente. Em 17/04/2016 foi o voto da Câmara; o afastamento foi em 12/05/2016 | Usado o Senado Notícias (12/05/2016). Cópia: `bruto/noticias/senado-governos-pos-1988-parte4.txt`. |
| Arquivo Nacional | Convenção própria: Collor termina em 02/10/1992 e Itamar começa na mesma data (interino); Dilma e Temer não estão no PDF depois de 2011 (edição de 2012) | Anotado na tabela; Dilma 2º mandato e Temer vêm do Senado/Câmara. |

Não consegui abrir a galeria da Presidência (gov.br/planalto/.../galeria-de-presidentes) nem a Biblioteca da Presidência: ambas devolvem captcha ou "página em manutenção" a curl e ao WebFetch. As páginas de Costa e Silva, Médici, Geisel, Figueiredo, Temer e Bolsonaro da Secretaria-Geral não renderizaram sem JavaScript; por isso para esses vão o Arquivo Nacional, a Câmara, o Planalto (AI-16) e o Senado.

## 2. Janelas do infográfico, em meses

Colunas e janelas lidas de `fontes/infografico-transcrito.csv` e da imagem. "Meses do mandato" = tabela 1.

| Coluna do infográfico | Cabeçalho | Meses do cabeçalho (ano-calendário) | Janelas por indicador (meses) | Meses reais do governo | Problema de janela |
|---|---|---|---|---|---|
| Ditadura Militar (Costa e Silva e Médici) | 1967-1974 | 96 | PIB 1968-1973 (72); IPCA 1967-1973 (84); desemprego 1968-1973 (72); salário mínimo 1968-1973 (72); pobreza "1990, referência" (fora do período); Gini "anos 1970"; expectativa de vida 1970 | 84,0 (15/03/1967 a 15/03/1974, incluindo 2 meses de Junta) | O cabeçalho (96 m) inclui 2,5 m de Castelo Branco (1967) e 9,5 m de Geisel (1974). Cada indicador usa uma janela diferente (72 ou 84 m). A pobreza é de 1990, sob Collor. A CPDOC chama o "milagre" de 1967-1973 "e por vezes de forma mais restrita 1968-1973", mas o infográfico mistura as duas dentro da mesma coluna. |
| Itamar Franco | 1992-1994 | 36 | PIB, IPCA, desemprego, salário mínimo 1992-1994 (36); pobreza 1994; Gini 1992; expectativa de vida 1990 | 27,0 (desde 02/10/1992) | 9 m (jan a set/1992) são de Collor. Gini de 1992 e expectativa de vida de 1990 não são de Itamar. |
| FHC | 1995-2002 | 96 | todas 1995-2002 (96) | 96,0 | Casa com o mandato. |
| Lula 1º e 2º mandatos | 2003-2010 | 96 | todas 2003-2010 (96) | 96,0 | Casa com o mandato. |
| Dilma | 2011-2016 | 72 | todas 2011-2016 (72) | 68,0 até 31/08/2016 (64,4 até o afastamento) | Inclui 4 m (set a dez/2016) de Temer. |
| Temer | 2016-2018 | 36 | todas 2016-2018 (36) | 28,0 (desde 31/08/2016); 31,6 desde 12/05/2016 | O ano de 2016 entra inteiro na coluna Dilma e inteiro na coluna Temer (12 m contados duas vezes). |
| Bolsonaro | 2019-2022 | 48 | PIB, IPCA, salário mínimo 2019-2022 (48); desemprego "2019-2020, pico" (24) | 48,0 | Desemprego usa metade do mandato (o pico), enquanto as outras linhas usam o mandato inteiro. |
| Lula 3º mandato | 2023-2026 | 48 | 2023-2025 (36), marcados com asterisco "estimativas ou parciais" | 45,6 corridos até 19/10/2026 (previsto 48,1) | Mandato em curso: não há dado de 2026 completo; o asterisco do rodapé reconhece estimativas. |

## 3. Planos e trocas de moeda

### 3.1 Planos de estabilização (fonte primária e o que ela diz)

| Plano | Instrumento e data | O que o texto legal faz | Fonte primária (URL; cópia local) | Observação |
|---|---|---|---|---|
| Cruzado (1986) | Decreto-Lei 2.283, de 27/02/1986, substituído pelo Decreto-Lei 2.284, de 10/03/1986. BCB e CPDOC dão 28/02/1986 como a data do anúncio e da nova moeda | Art. 1º: cruzado = 1.000 cruzeiros. Congelamento: DL 2.283 art. 36 ("congelados nos níveis do dia 27 de fevereiro de 1986"); DL 2.284 art. 35 ("Ficam congelados todos os preços nos níveis do dia 27 de fevereiro de 1986"). Desindexação (ORTN extinta, OTN) | https://www.planalto.gov.br/ccivil_03/decreto-lei/del2283.htm e https://www.planalto.gov.br/ccivil_03/decreto-lei/del2284.htm (`bruto/planalto-legislacao/*del2283*`, `*del2284*`) | O próprio DL 2.283 consta como "Revogado pelo Decreto-Lei 2.284". CPDOC dá 28/02/1986 como data de implementação. |
| Cruzado II | pacote de novembro/1986 (anunciado após as eleições de 15/11/1986); Decreto-Lei 2.290, de 21/11/1986 (citado pelo IBGE) | CPDOC: aumento de impostos indiretos, reajuste de preços defasados, "expurgou do índice da inflação" supérfluos. IBGE: "O cálculo do IPC passou a ser feito com base no INPC" | CPDOC https://atlas.fgv.br/verbete/6297 (`bruto/cpdoc/atlas_fgv_br_verbete_6297.txt`); IBGE https://biblioteca.ibge.gov.br/visualizacao/livros/liv65477.pdf, apêndice (`bruto/ibge-ipca/liv65477.txt`) | O decreto-lei 2.290 não foi lido no Planalto ❓ (só a citação do IBGE). |
| Bresser (1987) | Decreto-Lei 2.335, de 12/06/1987 | Art. 1º: congelamento de todos os preços "pelo prazo máximo de 90 (noventa) dias" nos níveis de 12/06/1987; URP para reajuste de preços e salários | https://www.planalto.gov.br/ccivil_03/decreto-lei/del2335.htm (`bruto/planalto-legislacao/*del2335*`) | |
| Verão (1989) | Medida Provisória 32, de 15/01/1989 (BCB); Lei 7.730, de 31/01/1989 | Cruzado novo = 1.000 cruzados (art. 1º). Art. 8º: preços "congelados, por prazo indeterminado" nos níveis de 14/01/1989 | https://www.planalto.gov.br/ccivil_03/leis/l7730.htm (`bruto/planalto-legislacao/*l7730*`); data da MP 32 em https://www.bcb.gov.br/content/acessoinformacao/museudocs/pub/SintesePadroesMonetariosBrasileiros.pdf | CPDOC (https://atlas.fgv.br/verbete/6306) situa o lançamento em "14 de janeiro de 1989"; a MP é de 15/01 e o congelamento usa preços de 14/01. |
| Collor I (1990, "confisco") | Medida Provisória 168, de 15/03/1990; Lei 8.024, de 12/04/1990 | Cruzeiro = 1 cruzado novo. Art. 5º e 6º: saldos de depósitos à vista e poupança convertidos em cruzeiros "obedecido o limite de NCz$ 50.000,00"; o excedente é devolvido "a partir de 16 de setembro de 1991, em doze parcelas mensais" | https://www.planalto.gov.br/ccivil_03/leis/l8024.htm (`bruto/planalto-legislacao/*l8024*`) | "Confisco" é termo corrente, não da lei: o texto legal fala em conversão com limite e parcelamento do excedente. |
| Collor II (1991) | Medida Provisória 294, de 31/01/1991 (Diário Oficial de 01/02/1991); Leis 8.177 e 8.178, de 01/03/1991 | Lei 8.177: desindexação; cria a Taxa Referencial (TR). Lei 8.178 art. 1º: preços praticados em 30/01/1991 só podem ser majorados "mediante prévia e expressa autorização do Ministério da Economia". IBGE: extinção de BTN, IPC (por orientação ministerial), IRVF, ICB | https://www.planalto.gov.br/ccivil_03/leis/l8177.htm, https://www.planalto.gov.br/ccivil_03/leis/l8178.htm; MP: https://www2.camara.leg.br/legin/fed/medpro/1991/medidaprovisoria-294-31-janeiro-1991-370770-publicacaooriginal-1-pe.html (`bruto/planalto-legislacao/*`) | Não há confisco no Collor II; a lei é desindexação mais controle de preços. |
| Real (1994) | URV: Medida Provisória 434, de 27/02/1994 (BCB), convertida na Lei 8.880, de 27/05/1994 (que converte a MP 482/1994); Real: MP 542, de 30/06/1994; Lei 9.069, de 29/06/1995 | Lei 8.880 art. 1º §2º: URV em 01/03/1994 = CR$ 647,50. Lei 9.069 art. 1º: "A partir de 1º de julho de 1994, a unidade do Sistema Monetário Nacional passa a ser o REAL"; paridade com o cruzeiro real = a da URV fixada pelo BCB para 30/06/1994, que o BCB tabula como CR$ 2.750,00 = R$ 1,00 | https://www.planalto.gov.br/ccivil_03/leis/l8880.htm e https://www.planalto.gov.br/ccivil_03/leis/l9069.htm (`bruto/planalto-legislacao/*`); BCB Síntese (link acima) | O número 2.750 não está no texto da lei: a lei remete à paridade fixada pelo BCB. Quem cita 2.750 deve citar a tabela do Museu de Valores. A cadeia de reedições 434 -> 457 -> 482 não foi lida ❓. O IBGE cita o Decreto 1.066, de 27/02/1994, para a metodologia da URV. |

### 3.2 Trocas de moeda e cortes de zeros

Fonte única, primária (Banco Central do Brasil, Museu de Valores, "Síntese dos Padrões Monetários Brasileiros", maio de 2007): https://www.bcb.gov.br/content/acessoinformacao/museudocs/pub/SintesePadroesMonetariosBrasileiros.pdf (`bruto/bcb-sintese-padroes-monetarios.txt`). Duas colunas finais são cálculo próprio.

| Moeda (símbolo) | Vigência (BCB) | Fator sobre a anterior (BCB) | Base legal (BCB) | Governo que instituiu (BCB) | Zeros cortados |
|---|---|---|---|---|---|
| Cruzeiro (Cr$), sem centavos | 02/12/1964 a 12/02/1967 | Cr$ 1,00 = Cr$ 1 | Lei 4.511, de 01/12/1964 | Castello Branco | 0 (extingue centavos) |
| Cruzeiro novo (NCr$) | 13/02/1967 a 14/05/1970 | Cr$ 1.000 = NCr$ 1,00 | DL 1, de 13/11/1965; Decreto 60.190 e Resolução 47, ambos de 08/02/1967 | Castello Branco | 3 |
| Cruzeiro (Cr$) | 15/05/1970 a 15/08/1984 | NCr$ 1,00 = Cr$ 1,00 | Resolução 144, de 31/03/1970 | Médici | 0 (volta o nome) |
| Cruzeiro, sem centavos | 16/08/1984 a 27/02/1986 | Cr$ 1,00 = Cr$ 1 | Lei 7.214, de 15/08/1984 | Figueiredo | 0 |
| Cruzado (Cz$) | 28/02/1986 a 15/01/1989 | Cr$ 1.000 = Cz$ 1,00 | DL 2.283, de 27/02/1986; Resolução 1.100, de 28/02/1986; DL 2.284, de 10/03/1986 | Sarney | 3 |
| Cruzado novo (NCz$) | 16/01/1989 a 15/03/1990 | Cz$ 1.000,00 = NCz$ 1,00 | MP 32, de 15/01/1989; Resolução 1.565, de 16/01/1989; Lei 7.730, de 31/01/1989 | Sarney | 3 |
| Cruzeiro (Cr$) | 16/03/1990 a 31/07/1993 | NCz$ 1,00 = Cr$ 1,00 | MP 168, de 15/03/1990; Resolução 1.689, de 18/03/1990; Lei 8.024, de 12/04/1990 | Collor | 0 (volta o nome) |
| Cruzeiro real (CR$) | 01/08/1993 a 30/06/1994 | Cr$ 1.000,00 = CR$ 1,00 | MP 336, de 28/07/1993; Resolução 2.010, de 28/07/1993; Lei 8.697, de 27/08/1993 | Itamar Franco | 3 |
| Real (R$) | desde 01/07/1994 | CR$ 2.750,00 = R$ 1,00 | MP 434, de 27/02/1994; Lei 8.880, de 27/05/1994; MP 542, de 30/06/1994; Lei 9.069, de 29/06/1995 | Itamar Franco | fator 2.750 (não é potência de 10) |

Cálculo próprio (aritmética sobre a coluna de fatores): do cruzeiro de 1964 ao real, o fator acumulado é 1.000 x 1.000 x 1.000 x 1.000 x 2.750 = 2,75 x 10^15; isto é, R$ 1,00 equivale a 2,75 quatrilhões de cruzeiros de 1964-1967 (12 zeros cortados mais o fator 2.750).

## 4. IPCA: origem, metodologia e por que "IPCA 1967-73" é impossível

Fonte principal: IBGE, Série Relatórios Metodológicos, vol. 14, "Sistema Nacional de Índices de Preços ao Consumidor: Métodos de cálculo", 7ª ed.: https://biblioteca.ibge.gov.br/visualizacao/livros/liv65477.pdf (`bruto/ibge-ipca/liv65477.txt`). Segunda fonte do IBGE: "Estatísticas Básicas 1979-95" https://biblioteca.ibge.gov.br/visualizacao/livros/liv25754.pdf (`bruto/ibge-ipca/liv25754.txt`; trecho não lido além do índice).

| Fato | Texto do IBGE (citação curta) | Tipo |
|---|---|---|
| De 1948 a 1978 quem calculava o índice de preços ao consumidor | "No período compreendido entre 1948 e 1978, a produção de índices de preços esteve a cargo do então Ministério do Trabalho", em 14 capitais | dado |
| Quando o IBGE assumiu | "A partir de julho de 1978, o IBGE assumiu integralmente, por deliberação oficial, a responsabilidade" | dado |
| INPC | "março de 1979 - Foi criado, através do próprio Sistema, o Índice Nacional de Preços ao Consumidor - INPC" | dado |
| IPCA | "dezembro de 1979 - Foi criado, também através do SNIPC, o Índice Nacional de Preços ao Consumidor Amplo - IPCA, como medida da inflação brasileira" | dado |
| Cobertura inicial | Rio de Janeiro (jan/1979); Porto Alegre, Belo Horizonte e Recife (jun/1979); São Paulo, Brasília e Belém (jan/1980); Fortaleza, Salvador e Curitiba (out/1980); Goiânia (jan/1991) | dado |
| Ponderação por Endef 1974-1975 | Estrutura de pesos do Endef 1974-1975 nos primeiros anos; POF 1987-1988 depois | dado |
| Indexador único | "novembro de 1985 - ... o IPCA a ser o único indexador oficial do País" (DL 91.990, de 27/11/1985). "março de 1986 - O IPCA deixou de ser o indexador oficial" | dado |
| Corte do Cruzado | O DL 2.284 "determinou o encerramento no dia 28 de fevereiro de 1986 das séries do INPC e do IPCA"; março/1986 vira a base (=100) | dado |
| Período de coleta | Até 1986 o IPCA coletava de ~15 do mês anterior a ~14; depois passou ao mês civil | dado |
| Série do BCB | A série SGS 433 (IPCA) do BCB começa em jan/1980 (primeiro registro do arquivo `fontes/ipca-sgs433-raw.json`: "01/01/1980", 6,62) | dado (arquivo local) |

Conclusão: não existe IPCA para 1967-1973. Qualquer "inflação média 1967-73" posta sob o rótulo IPCA vem de outra série (retropolada ou trocada de nome). Índices existentes na época: Ministério do Trabalho (1948-1978, segundo o IBGE); FGV IGP-DI (série Ipeadata IGP12_IGPDI12 desde jan/1944, no arquivo `fontes/igpdi-ipeadata-raw.json`); ICV da FGV (Rio) e ICV do DIEESE, citados pela CPDOC.

Referência cruzada (cálculo próprio, arquivo de outro colhedor, não revalidado aqui): sobre o IGP-DI dez/dez, 1967-1973 dá média aritmética de 20,0% ao ano (1967: 25,0; 1968: 25,5; 1969: 19,3; 1970: 19,3; 1971: 19,5; 1972: 15,7; 1973: 15,5). Fica perto do 20,3% do infográfico, mas não igual; atribuir 20,3% ao IGP-DI é hipótese não provada ❓.

Controvérsia de medida em 1973, na CPDOC (https://atlas.fgv.br/verbete/6001, Luís Aranha Correia do Lago, Atlas Histórico do Brasil, `bruto/cpdoc/atlas_fgv_br_verbete_6001.txt`): "a partir desse momento os índices oficiais, principalmente em 1973, sofreram o forte impacto de preços tabelados que, na prática, eram amplamente desrespeitados. Nesse ano, a variação média do Índice do Custo de Vida (ICV) do Rio de Janeiro da Fundação Getulio Vargas, de 12,6%, contrastava com a de 26,1% do índice calculado pelo DIEESE." Isso é interpretação de historiador sobre dois índices, não verificação independente; o texto mostra que 1973 é o ano em que as séries mais divergem.

## 5. Preços administrados e represados

### 5.1 1986, 1987 e 1989: o que o IBGE e a CPDOC documentam

| Afirmação | Fonte | Tipo |
|---|---|---|
| Congelamento legal de todos os preços em 27/02/1986 (DL 2.283 art. 36; DL 2.284 art. 35); 12/06/1987 por 90 dias (DL 2.335 art. 1º); 14/01/1989 por prazo indeterminado (Lei 7.730 art. 8º) | Planalto (seção 3.1) | dado (texto legal) |
| Junho/1987: "o governo determinou que a inflação ocorrida até o dia da divulgação do Plano (15.06) seria 'represada' no IPC correspondente ao mês de junho... o IPC de junho captou a inflação ocorrida em 35 dias, e o de julho, em 12 dias" | IBGE, liv65477, apêndice, "julho de 1987" | dado |
| Janeiro/1989: "o IPC de janeiro captou a inflação ocorrida em 51 dias, enquanto o IPC de fevereiro, em 11 dias" | IBGE, mesmo apêndice | dado |
| Cruzado: "como nos planos anteriores" a inflação até a data do plano foi "represada"; a série do IPCA em cruzeiros foi encerrada em 28/02/1986 ("fevereiro-linha") | IBGE, mesmo apêndice | dado |
| Cruzado II: o pacote "expurgou do índice da inflação as variações de preços de produtos considerados supérfluos, como cigarros e bebidas"; em julho/1986 o empréstimo compulsório sobre combustíveis e automóveis foi expurgado do IPC (DL 2.288, 23/07/1986) | CPDOC (6297); IBGE | dado de contexto sobre decisões; a avaliação "medida cosmética" é do autor |
| Distorções do congelamento: "em meados de 1986, o preço de um automóvel Monza com um ano de uso era maior do que o mesmo carro zero quilômetro"; estatais de petróleo, eletricidade e telecomunicações "tornaram-se vítimas do Plano Cruzado" | CPDOC (6297), Fernando de Holanda Barbosa | opinião/leitura do analista (descrição qualitativa, sem série) |
| "o que começa errado não pode dá certo" e "o fracasso... deveu-se única e exclusivamente" à não solução do déficit público | CPDOC (6297), mesmo autor | opinião de analista; CPDOC registra que "alguns analistas atribuem... a erros de administração... Outros... à concepção" (há debate) |
| Reservas internacionais de cerca de US$ 10 bilhões (fev/1986) para menos de US$ 5 bilhões (fev/1987); inflação "517%" anualizada em jan-fev/1986 (IGP/FGV) e "337%" no primeiro bimestre de 1987 | CPDOC (6297) | dado citado pelo texto (série primária não lida) ❓ |
| IPCA mensal 1986 (BCB SGS 433): jan 14,37; fev 12,72; mar 4,77; abr 0,78; mai 1,40; jun 1,27; jul 1,71; ago 3,55; set 1,72; out 1,90; nov 5,45; dez 11,65 | `fontes/ipca-sgs433-raw.json` (BCB) | dado; atenção à nota do IBGE de que o IPCA deixou de ser o indexador em março/1986 e à quebra de série |

### 5.2 2013-2015: o que o próprio BCB diz (dados) e o que é opinião

Todos os dados abaixo vêm dos relatórios do BCB (cópia em `bruto/bcb-relatorios-inflacao/`), que citam o IBGE como fonte. Definição do BCB: preços monitorados são "aqueles que são direta ou indiretamente determinados pelos governos federal, estadual ou municipal" (Relatório Anual 2015, nota 3).

| Dado | Valor | Fonte (URL; cópia) | Tipo |
|---|---|---|---|
| IPCA 2013; preços livres; monitorados | 5,91%; 7,29%; 1,54% | Boletim BCB, Relatório Anual 2014, Quadro "Principais itens do grupo monitorados" https://bcb.gov.br/pec/boletim/banual2014/rel2014p.pdf (`rel2014p.txt`) | dado |
| IPCA 2014; livres; monitorados | 6,41%; 6,72%; 5,32% | idem | dado |
| IPCA 2015; livres; monitorados | 10,67%; 8,51%; 18,07% (4,31 p.p. do IPCA) | Relatório Anual 2015 https://www.bcb.gov.br/pec/boletim/banual2015/rel2015p.pdf (`rel2015p.txt`); Carta Aberta 2015 https://www.bcb.gov.br/content/controleinflacao/controleinflacao_docs/carta_aberta/carta2015.pdf | dado |
| Gasolina (IPCA): 2013, 2014, 2015 | 6,51%; 2,89%; 20,10% | Relatórios Anuais 2014 e 2015 | dado |
| Energia elétrica residencial: 2013, 2014, 2015 | -15,65%; +17,06%; +50,99% | idem | dado |
| Ônibus urbano: 2013, 2014, 2015 | 0,04%; 3,86%; 15,09% | idem | dado |
| Energia, fev/2013 | -15,17% no mês (acumulado do trimestre -18,49%); o BCB atribui a queda dos monitorados à "redução da tarifa de energia elétrica residencial" | Relatório de Inflação de março/2013 https://www.bcb.gov.br/htms/relinf/port/2013/03/ri201303P.pdf (`ri201303P.txt`) | dado |
| Ônibus, 2013 | "a revogação de diversos reajustes em tarifas de ônibus urbano" explica a queda trimestral | Relatório de Inflação de setembro/2013 https://www.bcb.gov.br/content/ri/relatorioinflacao/201309/RELINF201309-ri201309c2p.pdf (`RELINF201309-ri201309c2p.txt`) | dado |
| Monitorados em 12 meses até novembro | 0,95% (nov/2013); 5,83% (nov/2014) | Relatório de Inflação de dezembro/2014 https://www.bcb.gov.br/htms/relinf/port/2014/12/ri201412P.pdf (`ri201412P.txt`) | dado |
| Diagnóstico do Copom | A inflação elevada "reflete, em parte... dois importantes processos de ajustes de preços relativos... realinhamento dos preços domésticos em relação aos internacionais e realinhamento dos preços administrados em relação aos livres" | Relatório de Inflação dez/2014 (mesmo); Carta Aberta de 08/01/2016 do presidente do BCB, Alexandre Tombini, ao ministro Nelson Barbosa: "observados desde o final de 2014" | posição institucional do BCB (diagnóstico), não série |
| Projeção errada | O BCB previa administrados de 7,6% para 2015 (dez/2014); o resultado foi 18,07% | Carta Aberta 2015, parágrafo 4 | dado |
| Lei da redução das tarifas de energia | Lei 12.783, de 11/01/2013 (conversão da MP 579/2012) "sobre a redução dos encargos setoriais e sobre a modicidade tarifária" | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12783.htm (`bruto/planalto-legislacao/*l12783*`) | dado (texto legal) |

Literatura:

| Texto | O que afirma | Tipo |
|---|---|---|
| Arthur Barrionuevo (FGV-SP), "A formação distorcida de preços administrados na experiência brasileira recente", Revista de Economia Política, 35(3), 2015, pp. 475-491. DOI 10.1590/0101-31572015v35n03a06. PDF: https://pesquisa-eaesp.fgv.br/sites/gvpesquisa.fgv.br/files/arquivos/a_formacao_distorcida_de_precos_administrados_na_experiencia_brasileira_recente.pdf (`bruto/literatura/`) | Resumo: os "diferentes níveis de governo, eventualmente, distorcem os preços através de medidas arbitrárias, por objetivos políticos de curto prazo"; o foco é "a necessidade de ajuste... no final do primeiro governo Dilma Rousseff (2011-14)". O próprio autor diz que "o viés deste autor" pesa para a dificuldade de manter o ajuste | artigo acadêmico revisado por pares; interpretação (não dado) |

Notícias de 2013-2015 (Exame, Gazeta do Povo, Novacana, Infomoney) que o buscador devolveu sobre ações do Ministério Público Federal e atas do conselho da Petrobras: não foram lidas por completo nesta colheita ❓. O que é opinião ou alegação de parte, e não dado: (a) a tese de que o governo "represou" preços para a eleição de 2014 (Barrionuevo e a oposição; o BCB fala em "realinhamento", sem atribuir intenção); (b) a alegação de ação do MPF contra dirigentes da Petrobras e da Fazenda (alegação de acusação, não decisão); (c) estimativas de analistas sobre a inflação "sem a artificialidade" (Gianetti: 7 a 7,5% ao ano, segundo o buscador, não lido na fonte ❓). Contra-literatura (defesa da política de preços de 2013-2014, ex. Fazenda ou Petrobras) não achei fonte primária nesta colheita ❓.

## 6. Circulação e autoria do infográfico (complemento ao arquivo do Hermes)

Arquivo do Hermes lido e não alterado: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/comunidade-hermes-2026-10-19.md`.

| Verificação nova | Resultado | Cópia / manifest |
|---|---|---|
| A publicação existe e tem o texto citado | Confirmado sem login pelo oEmbed público do X: autor "Francisco - O sarcástico" (@ffrancisconl), texto "Perguntei ao ChatGPT qual foi o melhor governo do Brasil? A resposta:", data "October 18, 2026". https://publish.twitter.com/oembed?url=https://x.com/ffrancisconl/status/2111905813992513673 | `bruto/proveniencia/oembed-ffrancisconl-2111905813992513673.json` |
| Hora da publicação | Decodificando o identificador (Snowflake) do post: 2026-10-18 19:42:38 UTC, igual à hora que o Hermes registrou. Reposts: 2112196804263530780 = 2026-10-19 14:58:55 UTC; 2112195826592157801 = 14:55:02; 2112192971844333863 = 14:43:41. O oEmbed do repost de @_gnc8 repete o texto e o mesmo link curto | cálculo próprio sobre o ID |
| A imagem do X é a mesma do arquivo do WhatsApp | A mídia https://pbs.twimg.com/media/HU7_JHmWUAAvcKi.jpg?name=orig tem 1312x1199, como `infografico-original-whatsapp-2026-10-19.jpeg`. Comparação em tons de cinza: diferença média de 0,69 em 255; 0,0% dos pixels com diferença acima de 20 (arquivos recodificados: hashes diferentes, conteúdo igual) | `bruto/proveniencia/x-media-HU7_JHmWUAAvcKi.jpg` |
| Marca de procedência embutida (C2PA, "Made with AI", software gerador) | Nenhuma. O WhatsApp só traz perfil de cor sRGB com copyright "Google Inc. 2016" (recodificação) e JFIF; o arquivo do X traz só JFIF. Não há como confirmar nem negar pelos metadados que o ChatGPT gerou a imagem | exiftool nos dois arquivos |
| Versões anteriores da imagem | Wayback Machine: nenhum snapshot do post nem da mídia (consulta à API de disponibilidade e ao CDX em 2026-10-19). Buscas abertas pela frase do título, pelo trecho final ("sem ignorar os avanços importantes de outros períodos") e pelos números (1.088%, 11,1%, 20,3%) não retornaram a peça nem checagem | nada a salvar |

Conclusão: o publicador mais antigo achado continua sendo @ffrancisconl (18/10/2026 19:42 UTC); isso não prova autoria da imagem, nem que o ChatGPT a tenha produzido (alegação do autor do post). Versão anterior: não achei; a API de busca do X do Hermes é recente, e o Wayback não guarda o X.

## 7. NAO COLHIDO / limites

- Galeria oficial da Presidência (gov.br/planalto) e Biblioteca da Presidência: captcha e "em manutenção". Páginas Secretaria-Geral de Costa e Silva, Médici, Geisel, Figueiredo, Temer e Bolsonaro: sem conteúdo renderizável. Datas desses vêm de Arquivo Nacional, Câmara, Planalto (AI-16) e Senado.
- Posse de Dilma em 01/01/2015 e de Collor/Itamar em termos de ata: não lidas em primárias ❓ (a página oficial repete a data de 2011).
- Decreto-Lei 2.290/1986 (Cruzado II), MP 457/1994 (reedição do Real), Decreto 1.066/1994: citados por IBGE e BCB, textos não lidos ❓.
- Dados numéricos da CPDOC (517%, 337%, reservas) são citações de um verbete, não série primária ❓.
- ICV-DIEESE e IPC-FIPE: só aparecem em citação da CPDOC; criação e metodologia não lidas ❓. FGV IGP-DI: início da série em 1944 vem do arquivo Ipeadata (outro colhedor), a história institucional do índice não foi lida em fonte da FGV ❓.
- Contra-literatura sobre a política de preços de 2013-2014 e as notícias sobre as ações do MPF não lidas ❓.
- Sem opinião política: contestações a atribuir causa (milagre, Plano Real, 2013-2015) estão marcadas como opinião do autor da fonte.
