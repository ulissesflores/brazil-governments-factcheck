# Referências da fase 2: verificação do §11 do pré-registro

Gerado em 2026-10-20. Fonte da lista: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/preregistro/PREREGISTRATION-FASE-2.md` §11.

Regra aplicada: artigo de periódico, DOI conferido no Crossref (registro individual salvo e hasheado) e quartil no SJR. Literatura cinzenta não sustenta regra. Nenhum campo veio de memória: os campos de `referencias.csv` e `referencias.bib` são lidos por `montar_referencias.py` dos JSON/CSV de `bruto/`.

## Números

| Medida | Valor |
|---|---|
| Referências do §11 (itens contados um a um) | 23 |
| Referências implícitas buscadas (corrupção V-Dem, desmatamento) | 6 artigos + 2 working papers |
| `confirmada` (DOI Crossref + quartil SJR) | 29 (23 do §11 + 6 implícitas) |
| `doi_sem_quartil` | 0 |
| `nao_encontrada` | 0 |
| `cinzenta` (working paper, só registrado) | 2 |
| Quartil SJR das 29 confirmadas | 29 Q1 (melhor quartil entre as categorias do periódico) |
| Qualis | vazio em todas (ver limitações) |

## Tabela

| Chave | Papel | DOI | Periódico | Ano | SJR | Status |
|---|---|---|---|---|---|---|
| saisana2005 | método | 10.1111/j.1467-985x.2005.00350.x | JRSS Series A | 2005 | Q1 | confirmada |
| paruolo2013 | método | 10.1111/j.1467-985x.2012.01059.x | JRSS Series A | 2013 | Q1 | confirmada |
| becker2017 | método | 10.1016/j.ecolind.2017.03.056 | Ecological Indicators | 2017 | Q1 | confirmada |
| greco2019 | método | 10.1007/s11205-017-1832-9 | Social Indicators Research | 2019 | Q1 | confirmada |
| decancq2013 | método | 10.1080/07474938.2012.690641 | Econometric Reviews | 2013 | Q1 | confirmada |
| mazziotta2016 | método | 10.1007/s11205-015-0998-2 | Social Indicators Research | 2016 | Q1 | confirmada |
| ravallion2012wbro | método | 10.1093/wbro/lkr009 | World Bank Research Observer | 2012 | Q1 | confirmada |
| ravallion2012jde | método | 10.1016/j.jdeveco.2012.01.003 | Journal of Development Economics | 2012 | Q1 | confirmada |
| bohringer2007 | método | 10.1016/j.ecolecon.2007.03.008 | Ecological Economics | 2007 | Q1 | confirmada |
| klugman2011 | método | 10.1007/s10888-011-9178-z | Journal of Economic Inequality | 2011 | Q1 | confirmada |
| fleurbaey2009 | método | 10.1257/jel.47.4.1029 | Journal of Economic Literature | 2009 | Q1 | confirmada |
| ditella2001 | método | 10.1257/aer.91.1.335 | American Economic Review | 2001 | Q1 | confirmada |
| blanchflower2014 | método | 10.1111/jmcb.12154 | Journal of Money, Credit and Banking | 2014 | Q1 | confirmada |
| mian2017 | direção | 10.1093/qje/qjx017 | Quarterly Journal of Economics | 2017 | Q1 | confirmada |
| marquardt2018 | direção | 10.1017/pan.2018.28 | Political Analysis | 2018 | Q1 | confirmada |
| coppedge2011 | direção | 10.1017/s1537592711000880 | Perspectives on Politics | 2011 | Q1 | confirmada |
| hidalgo2009 | direção | 10.1073/pnas.0900943106 | PNAS | 2009 | Q1 | confirmada |
| rodrik2016 | direção | 10.1007/s10887-015-9122-3 | Journal of Economic Growth | 2016 | Q1 | confirmada |
| bergh2011 | direção | 10.1111/j.1467-6419.2011.00697.x | Journal of Economic Surveys | 2011 | Q1 | confirmada |
| frankel1999 | direção | 10.1257/aer.89.3.379 | American Economic Review | 1999 | Q1 | confirmada |
| wacziarg2008 | direção | 10.1093/wber/lhn007 | World Bank Economic Review | 2008 | Q1 | confirmada |
| rodriguez2000 | direção | 10.1086/654419 | NBER Macroeconomics Annual | 2000 | Q1 | confirmada |
| arcand2015 | direção | 10.1007/s10887-015-9115-2 | Journal of Economic Growth | 2015 | Q1 | confirmada |
| mcmann2022 | direção (implícita: corrupção V-Dem) | 10.1017/pan.2021.27 | Political Analysis | 2022 | Q1 | confirmada |
| mcmann2020 | direção (implícita: corrupção V-Dem) | 10.1177/1065912919862054 | Political Research Quarterly | 2020 | Q1 | confirmada |
| nepstad2014 | direção (implícita: desmatamento) | 10.1126/science.1248525 | Science | 2014 | Q1 | confirmada |
| assuncao2023 | direção (implícita: desmatamento) | 10.1257/app.20200196 | AEJ: Applied Economics | 2023 | Q1 | confirmada |
| hansen2013 | direção (implícita: desmatamento) | 10.1126/science.1244693 | Science | 2013 | Q1 | confirmada |
| lovejoy2018 | direção (implícita: desmatamento) | 10.1126/sciadv.aat2340 | Science Advances | 2018 | Q1 | confirmada |
| mcmann2016ssrn | direção (implícita) | 10.2139/ssrn.2727595 | SSRN (working paper) | 2016 | n/a | cinzenta |
| pemstein2018ssrn | direção (implícita) | 10.2139/ssrn.3167764 | SSRN (working paper) | 2018 | n/a | cinzenta |

Contagem: Ravallion 2012 vale por dois itens do §11 (WBRO e JDE); por isso 22 citações de texto viram 23 itens.

## Pontos que o §11 precisa corrigir ou ressalvar

- **Ano de capa x ano online.** Paruolo 2013, Greco 2019, Mazziotta 2016, Ravallion (WBRO) 2012, Rodrik 2016 e McMann 2022 têm o Crossref `issued` no ano online anterior; o ano da edição impressa (usado no CSV e no BIB) bate com o §11. Nenhuma data do §11 está errada.
- **Ravallion no WBRO** é "Mashup Indices of Development" (WBRO 27(1), 2012); no JDE é "Troubling tradeoffs in the Human Development Index" (99(2), 2012). Os dois existem e batem com o §11.
- **Rodríguez e Rodrik** (NBER Macroeconomics Annual 2000) é artigo de uma série anual, registrado como `journal-article` no Crossref e como periódico (Q1) no SJR. Pode ser tratado como periódico; ressalva de que a série é editada, não de submissão aberta.
- **Q1 pode ser só em categoria genérica.** O CSV do SJR dá o melhor quartil entre as categorias. Em `Social Indicators Research` e `Science Advances`, por exemplo, o Q1 vem de categorias amplas (Social Sciences miscellaneous; Multidisciplinary). A coluna `nota` de `referencias.csv` lista todas as categorias com o quartil de cada uma, para a METHODOLOGY escolher a categoria compatível com o tema.
- **Referências implícitas: o que sustentam e o que não sustentam.**
  - Corrupção (`v2x_corr`, menor é melhor): `mcmann2022` valida os dados de corrupção do V-Dem e `mcmann2020` os usa para ligar nível de democracia e corrupção. Nenhum dos dois é o artigo de definição do índice `v2x_corr`; a definição normativa mora no codebook do V-Dem e no modelo de medição (Pemstein et al., só working paper, `pemstein2018ssrn`, cinzenta). Não achei artigo revisado por pares que defina o `v2x_corr` em si: `marquardt2018` e `coppedge2011` (já no §11) cobrem o modelo de medição e a arquitetura dos índices.
  - Desmatamento (menor é melhor): `nepstad2014` e `assuncao2023` documentam que políticas públicas e fiscalização reduziram o desmatamento amazônico; `hansen2013` sustenta a medição global de mudança de cobertura florestal (o PRODES/INPE é a fonte do item, não essa); `lovejoy2018` sustenta o risco de ponto de inflexão da Amazônia, que é a razão de "menos desmatamento é melhor" ter justificativa. Nenhum desses cinco testa a regra "menor é melhor" como hipótese; sustentam a justificativa.
  - O DOI `10.1257/app.20200196` (Assunção, Gandour, Rocha) é o artigo do AEJ: Applied Economics (2023), não o de `Environment and Development Economics` (2015, outro artigo, que apareceu na busca e não foi escolhido).

## Como o SJR foi obtido

O `scimagojr.com` devolve 403 (Cloudflare "Just a moment") para `curl -L -A "Mozilla/5.0" -e https://www.scimagojr.com/`, tanto no CSV quanto na página do periódico. A saída foi o **Wayback Machine**: snapshot de 2025-10-26 do CSV completo `https://www.scimagojr.com/journalrank.php?out=xls` (10,9 MB, 31.136 linhas), baixado pela cadeia de hashes (`bruto/scimago-journalrank-wayback-20251026.csv`).

- Ano do SJR: **2024** (a coluna do CSV é "Total Docs. (2024)"; a edição SJR 2025 só sai em meados de 2026, depois do snapshot).
- Casamento por ISSN (qualquer um dos ISSN do Crossref contra a coluna `Issn` do CSV); o título do periódico no SJR está na `nota` de cada linha e confere com o `container-title` do Crossref nas 29.
- Conferência cruzada: 76 periódicos do trabalho anterior (`referencias-q1/scimago`, extraídos no Chrome real em 2025) também estão neste CSV; o melhor quartil bate em 72 de 76. As 4 diferenças são de edição (SJR 2025 x 2024), não de erro de leitura. Não investiguei periódico a periódico.
- Limitação: o CSV traz o quartil por categoria na edição 2024, não série histórica. A coluna `sjr_quartil` é o melhor quartil da edição 2024.

## Qualis: o que não foi possível

- A Plataforma Sucupira (`sucupira.capes.gov.br/.../listaConsultaGeralPeriodicos.jsf`) responde a `curl`, lista os eventos "Quadriênio 2017-2020" e "Quadriênio 2021-2024", mas não tem API. Tentei emular o formulário JSF (evento 236, ISSN do AER) por POST; a página volta sem tabela de resultados, sem mensagem de erro. Não insisti: sem estrato lido, `qualis` ficou vazio, nunca chutado.
- A única planilha oficial achada (gov.br/CAPES, Metodologia do Qualis Referência 2017-2020, `reaMeListaFinalQualisV2.xlsx`, salva em `bruto/`) lista periódicos e **área-mãe**, não o estrato (A1 etc.). Serve para saber a área; não para o estrato. Não a usei para preencher `qualis`.
- Consequência: a regra "SJR **ou** A1" fica cumprida pelo SJR nas 29; nenhuma referência depende do Qualis.

## O que não foi feito

- Não conferi retratações nem erratas além do que o registro Crossref traz (nenhum dos 29 registros tem campo `updated-by` nem `update-to` no JSON do Crossref, e nenhum tem `relation` de retratação; Hansen 2013 tem comentário e resposta publicados na Science em 2014, não alteram o artigo).
- Não li os artigos: o que cada um sustenta aqui vem do título e do periódico, não de leitura do texto. A METHODOLOGY precisa dizer o que cada um sustenta só depois de leitura (como foi feito em `referencias-q1/RESULTADO.md`, que tem resumo lido).
- A cadeia de hashes usa o User-Agent fixo do `govfc.chain`; o `mailto` do pedido foi para a URL do Crossref (`mailto=`), não para o cabeçalho.

## Arquivos

- `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/referencias-fase2/referencias.csv`
- `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/referencias-fase2/referencias.bib` (29 entradas, validado com pandoc)
- `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/referencias-fase2/bruto/` (busca Crossref x29, registro individual x29, CSV SJR, planilha CAPES)
- `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/referencias-fase2/montar_referencias.py` (gera CSV e BIB a partir do `bruto/`)
- `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/referencias-fase2/manifest.jsonl`

## Cadeia de hashes

Saída de `PYTHONPATH=code python3 -m govfc.chain verify` (rodada em `/Users/ulissesflores/Developer/brazil-governments-factcheck`):

```text
60 lines; head 4e69502649f8a7bf9c4c1cbac6634329af23bbe859c76d63764c21cf8cb187aa; OK
```
