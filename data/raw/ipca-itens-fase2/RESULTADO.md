# IPCA por subitem (fase 2): aluguel residencial, plano de saude e IPCA geral

Coleta de 2026-10-20, cadeia de hash desde o primeiro download. Pasta: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/ipca-itens-fase2/`.

## Valores (variacao acumulada, sobre o numero-indice encadeado, dez/1999 = 100)

| Janela | IPCA geral | Aluguel residencial | Plano de saude | Preco relativo do aluguel (aluguel/geral) | Preco relativo do plano (plano/geral) |
| --- | --- | --- | --- | --- | --- |
| dez/1999 a dez/2024 | +346,98% | +225,02% | +660,34% | -27,29% | +70,11% |
| dez/2014 a dez/2024 | +74,90% | +55,46% | +134,59% | -11,11% | +34,13% |
| dez/2018 a dez/2022 | +26,93% | +24,02% | +21,32% | -2,29% | -4,42% |
| (sensibilidade) dez/2001 a dez/2024 | +291,72% | +229,25% | +591,61% | -15,95% | +76,56% |

- Fonte dos numeros: `derivado/acumulados_janelas.csv` (4 casas decimais); indices em `derivado/indice_ipca_*_dez1999_100.csv`, razoes em `derivado/razao_ipca_*_sobre_geral_dez1999_100.csv`.
- Pontos do indice (dez/1999 = 100): geral 255,57 (dez/2014), 321,09 (dez/2018), 407,55 (dez/2022), 446,98 (dez/2024), 484,46 (set/2026); aluguel 209,07 / 245,50 / 304,46 / 325,02 / 355,06; plano de saude 324,12 / 521,01 / 632,10 / 760,34 / 842,78.
- Preco relativo = acumulado do subitem dividido pelo acumulado do geral, menos 1. Negativo = o subitem subiu menos que o IPCA.
- A linha de sensibilidade existe porque o plano de saude muda de metodo em 2001 (ver quebras): a janela que comeca em dez/1999 atravessa 2000, quando a serie tem +3,65% em ago/2000 e 10 meses de zero (set/2000 a jun/2001). Os +660,34% dependem desse trecho; nao o trate como medida homogenea.
- Conferencia do IPCA geral: o acumulado pelo BCB SGS 433 (composicao dos 300 relativos mensais) bate com o SIDRA ate a ultima casa em todas as janelas (346,98 / 74,90 / 26,93 / 291,72).

## Tabelas SIDRA (cada uma e uma base)

| Base | Periodo | Geral | Aluguel residencial | Plano de saude | Variavel |
| --- | --- | --- | --- | --- | --- |
| t58 | 1991-01 a 1999-07 | c72/2640 | c72/1935 | nao ha na lista de categorias | v63 variacao mensal |
| t655 (+656 pesos) | 1999-08 a 2006-06 | c315/7169 | c315/7448 | c315/7696 | v63 (655), v66 peso (656) |
| t2938 | 2006-07 a 2011-12 | c315/7169 | c315/7448 | c315/7696 | v63, v66 |
| t1419 | 2012-01 a 2019-12 | c315/7169 | c315/7448 | c315/7696 | v63, v66, v2265 (12 meses) |
| t7060 | 2020-01 a 2026-09 | c315/7169 | c315/7448 | c315/7696 | v63, v66, v2265 |

Os codigos c315 coincidem nas quatro tabelas c315; o unico codigo que muda e o do aluguel entre t58 (1935) e t655 (7448). Series em `series/` (uma linha por base, nome `ipca_<subitem>_<variavel>_sidra<tabela>.csv`).

## Regra de encadeamento (escrita antes de calcular)

1. Cadeia principal: t655 -> t2938 -> t1419 -> t7060. Nenhuma tabela se sobrepoe a outra (cada uma comeca no mes seguinte ao fim da anterior; verificado no script, que aborta se houver mes duplicado ou ausente), entao NAO existe mes de sobreposicao para testar a emenda.
2. A emenda se apoia na continuidade declarada pelo IBGE, nao em teste empirico: o Metodos de calculo 6a ed. descreve o indice de cada nivel como acumulacao de relativos mensais que resulta no indice de Laspeyres do periodo (formulas XI-XIII, "fica assegurada a coerencia da formula (XI), utilizada para calculo dos indices mensais"), e as notas tecnicas 01/2011 e 02/2019 declaram que a atualizacao de estruturas deixa "inalterada" a concepcao geral, a coleta e o metodo de calculo. Cada taxa mensal e relativa ao mes anterior dentro da propria estrutura; compor taxas mensais e o mesmo procedimento do IBGE.
3. Limite: a emenda assume que o subitem nas tres tabelas e o mesmo objeto (mesmo codigo c315 e mesmo nome). Isso e o que o SIDRA mostra; nao ha prova independente. A definicao do subitem pode ter mudado dentro da cesta (nomenclaturas "atualizadas" segundo as notas).
4. t58 NAO e emendada a t655: o aluguel muda de codigo (1935 -> 7448), nao ha plano de saude na t58, e a t58 tem lacunas (abaixo). Fica so como serie bruta. Nenhum numero-indice da t58 foi construido.
5. Formula: `I(t) = I(t-1) * (1 + r(t)/100)`, `I(dez/1999) = 100`, r = variacao mensal publicada. Preco relativo: `R(t) = 100 * I_subitem(t) / I_geral(t)`. Esta na coluna `nota` de cada arquivo de `derivado/`.
6. Precisao: as taxas publicadas tem 2 casas; a composicao acumula esse arredondamento. Contra o acumulado em 12 meses publicado pelo IBGE (v2265, meses com 12 meses dentro da mesma tabela), a maior diferenca da composicao foi: geral 0,005 pp, aluguel 0,024 pp, plano de saude 0,042 pp (pior mes: geral 2018-05; aluguel e plano de saude 2017-04). Nos acumulados de 25 anos o efeito pode ser maior; nao foi medido separadamente.

## Quebras registradas (`quebras.csv`, 7 linhas, cabecalho identico ao de moeda-fiscal)

- 1999-08: corte t58 -> t655 (estrutura; a data de implantacao nao foi confirmada em nota tecnica baixada, so no corte do SIDRA).
- 1991 (abr e ago/set): lacunas na t58.
- 2001-07 (aprox.): metodo do plano de saude ("desde 2001", Metodos de calculo 6a ed.).
- 2006-07: POF 2002-2003 (t2938); 2012-01: POF 2008-2009 (nota tecnica 01/2011); 2020-01: POF 2017-2018 (nota tecnica 02/2019). Trechos citados conferidos literalmente contra os PDFs baixados.
- 2020-09 a 2021-12: plano de saude e a suspensao/recomposicao dos reajustes da ANS (notas tecnicas 03/2020 e 05/2020): set/2020 = -2,31%, out-dez/2020 = 0,00%, jan/2021 = +0,66%.
- Efeito de cada troca de estrutura sobre os niveis: NAO medido (sem mes de sobreposicao). Medi apenas o salto do peso mensal publicado: aluguel 3,7804 -> 2,6907 (2006), 2,9408 -> 3,6971 (2012), 3,8193 -> 3,7845 (2020); plano de saude 2,7911 -> 3,1642, 3,5112 -> 3,0481, 4,3414 -> 4,0243.

## O que nao foi achado

- BCB SGS: nenhuma serie pronta de subitem de IPCA (aluguel ou plano de saude). O catalogo CKAN do BCB (`bruto/bcb/ckan_busca_*.json`) devolve para "IPCA aluguel" 4 series de renda deflacionada, para "plano saude" e "aluguel residencial" zero resultados, e para "IPCA" 21 series de agregados (servicos, duraveis, nucleos), nenhuma de subitem. O portal `sgspub` e uma aplicacao JS e nao foi consultado (sem navegador); a ausencia vale so para o catalogo CKAN, que e evidencia fraca: ele nem indexa o SGS 433 (a busca por codigo_sgs:433 em `moeda-fiscal/bruto/bcb/ckan_433.json` tem 223 bytes, sem resultado). Nao e prova de que a serie nao exista no SGS. O unico dado do BCB usado e o SGS 433 (IPCA geral), como conferencia.
- Plano de saude antes de ago/1999 (t58 nao tem o subitem).
- Mes de implantacao da estrutura POF 1995-1996 (ago/1999) em nota tecnica do IBGE.
- Acumulado em 12 meses (v2265) nos 11 primeiros meses de cada tabela (t1419 e t7060): a fonte devolve "..." (inclusive para o IPCA geral, logo e artefato da tabela SIDRA, nao declaracao de descontinuidade do IBGE) e nada foi preenchido.

## Becos e desvios declarados

- Tabela 58, ago/1991 nao existe (periodos da tabela em `bruto/ibge/agregado-58-periodos.json`); set/1991 do geral na t58 e 33,71%, igual a dois meses de 15,63% compostos (33,70%). No SGS 433 ago e set trazem 15,63 cada, ou seja, o BCB parece ter dividido o acumulado de dois meses. Isso e inferencia minha, marcada como tal na `nota` da linha. O aluguel tem "-" em abr/1991 (simbolo SIDRA preservado, valor vazio; nao assumi que "-" seja zero). A divergencia SIDRA x SGS 433 em set/1991 e a unica entre as duas fontes no IPCA geral (101 meses da t58 comparaveis iguais; 0 diferencas em t655, t2938, t1419 e t7060).
- Os arquivos `bruto/ibge/agregado-*-metadados.json` sao gzip (o servidor do IBGE comprime a resposta mesmo sem pedir); estao guardados exatamente como chegaram, com extensao `.json`. Leia com `gzip` (testado: t655 e t7060 abrem e mostram 593 e 457 categorias).
- O `govfc.chain add` baixa com urllib e o agente do usuario do proprio pacote, nao com `curl -L -A "Mozilla/5.0"`. Para guardar a cadeia no momento do download usei o `add` em todos os arquivos. As paginas de noticia do IBGE (www.ibge.gov.br e agenciadenoticias) devolveram 403 por qualquer via; os arquivos HTML de erro foram apagados e nao entraram na cadeia. As fontes metodologicas vieram de `ftp.ibge.gov.br` (notas tecnicas e Metodos de calculo).
- O manifest guarda caminho ABSOLUTO em `arquivo` (passei destino absoluto), diferente de `moeda-fiscal`; `verify` funciona assim. Mudar o caminho da pasta exige reescrever a cadeia.
- Tres buscas CKAN falharam na primeira tentativa (resposta "Requisicao Invalida" do servidor: `%20` e a palavra "de" na consulta). Os arquivos de erro continuam na cadeia (`ckan_busca_IPCA%20aluguel.json`, `ckan_busca_plano%20de%20sa%C3%BAde.json`, mesmo tamanho, 6402 bytes) e as buscas foram refeitas com `+` (`ckan_busca_ipca_aluguel.json`, `ckan_busca_plano_saude.json`, `ckan_busca_aluguel_residencial.json`).
- O `derivado/_resumo_construcao.json` e saida de trabalho do script (conferencias e pontos), sem entrada na cadeia.
- Fim de serie: set/2026 (ultimo mes publicado em 2026-10-20).

## Reproducao

`scripts/baixar.sh` (downloads, primeira rodada), `scripts/construir.py` (series/ e derivado/), `scripts/quebras.py` (quebras.csv; confere cada citacao contra os PDFs). Rode com `python3 -I`.

## Cadeia de hash (`govfc.chain verify`)

```
28 lines; head 415397b3b665b62f42d7d9b1e57638ed1ae4fdd4ee9917923194fae8b5fef56b; OK
```
