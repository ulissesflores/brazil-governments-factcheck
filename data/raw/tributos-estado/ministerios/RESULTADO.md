# D1 — Ministérios no Brasil em 1º de janeiro, 1995-2026 (normas do Planalto)

Só contagem, norma e lista. Cada linha vem do texto baixado do Planalto (cadeia de hash em `manifest.jsonl` desta pasta). Gerado por `scripts/gerar.py`.

## Achado

| Ano | Norma vigente em 1/1 | Ministérios | A | B | C | Ministérios + status |
|---|---|---:|---:|---:|---:|---:|
| 1995 | MP 813 (1/1/1995) | 20 | 2 | 1 | 4 | 27 |
| 1996 | MP 1.226 (14/12/1995) | 20 | 2 | 1 | 5 | 28 |
| 1997 | MP 1.549 (18/12/1996) | 20 | 2 | 2 | 5 | 29 |
| 1998 | MP 1.549-38 (31/12/1997) | 20 | 2 | 2 | 5 | 29 |
| 1999 | MP 1.795 (1/1/1999) | 20 | 2 | 2 | 2 | 26 |
| 2000 | MP 1.999-13 (14/12/1999) | 20 | 4 | 0 | 1 | 25 |
| 2001 | MP 2.049-26 (21/12/2000) | 20 | 5 | 0 | 1 | 26 |
| 2002 | MP 2.216-37 (31/8/2001) + Dec. 4.046 | 20 | 5 | 0 | 1 | 26 |
| 2003 | MP 103 (1/1/2003) | 23 | 6 | 1 | 4 | 34 |
| 2004 | Lei 10.683 (28/5/2003) | 23 | 6 | 1 | 5 | 35 |
| 2005 | Lei 10.683 + Leis 10.869 e 11.036 | 23 | 8 | 0 | 5 | 36 |
| 2006 | Lei 10.683 + Lei 11.204 (5/12/2005) | 23 | 7 | 0 | 4 | 34 |
| 2007 | idem 2006 | 23 | 7 | 0 | 4 | 34 |
| 2008 | Lei 10.683 + Leis 11.497 e 11.518 (2007) | 23 | 8 | 0 | 5 | 36 |
| 2009 | Lei 10.683 + Leis 11.693 e 11.754 (2008) | 23 | 10 | 0 | 4 | 37 |
| 2010 | Lei 10.683 + Lei 11.958 (26/6/2009) | 24 | 10 | 0 | 3 | 37 |
| 2011 | Lei 10.683 + Lei 12.314 (19/8/2010) | 24 | 13 | 0 | 0 | 37 |
| 2012 | Lei 10.683 + Leis 12.462 e 12.545 (2011) | 24 | 14 | 0 | 0 | 38 |
| 2013 | idem 2012 | 24 | 14 | 0 | 0 | 38 |
| 2014 | Lei 10.683 + Lei 12.792 (28/3/2013) | 24 | 15 | 0 | 0 | 39 |
| 2015 | idem 2014 | 24 | 15 | 0 | 0 | 39 |
| 2016 | MP 696 (2/10/2015) | 23 | 8 | 0 | 0 | 31 |
| 2017 | Leis 13.341 e 13.345 (2016) | 21 | 5 | 0 | 0 | 26 |
| 2018 | Lei 13.502 (1/11/2017) | 22 | 6 | 0 | 0 | 28 |
| 2019 | MP 870 (1/1/2019) | 16 | 6 | 0 | 0 | 22 |
| 2020 | Lei 13.844 (18/6/2019) | 16 | 6 | 0 | 0 | 22 |
| 2021 | Lei 13.844 + Lei 14.074 (2020) | 17 | 6 | 0 | 0 | 23 |
| 2022 | Lei 13.844 + Leis 14.261 e LC 179 (2021) | 18 | 5 | 0 | 0 | 23 |
| 2023 | MP 1.154 (1/1/2023) | 31 | 6 | 0 | 0 | 37 |
| 2024 | Lei 14.600 + MP 1.187 (13/9/2023) | 32 | 6 | 0 | 0 | 38 |
| 2025 | idem 2024 (Lei 14.816) | 32 | 6 | 0 | 0 | 38 |
| 2026 | idem 2024 (Lei 14.816) | 32 | 6 | 0 | 0 | 38 |

Regra de contagem (a mesma em todos os anos):

- **Ministérios** = itens do artigo que a norma abre com "Os Ministérios são os seguintes" (art. 13 da Lei 9.649/1998 e MPs de 1995-2002; art. 25 da Lei 10.683/2003; art. 21 da Lei 13.502/2017; art. 19 da Lei 13.844/2019; art. 17 da Lei 14.600/2023). A Controladoria-Geral da União conta como Ministério nos anos em que a norma a põe nesse artigo (2016-2026, com redações diferentes) e como órgão A nos anos 2003-2015.
- **A** = órgão fora dessa lista cujo titular a norma declara Ministro de Estado (parágrafo "São Ministros de Estado ..." ou cargo "Ministro de Estado Chefe da ...").
- **B** = cargo ou gabinete de "Ministro de Estado Extraordinário" (Esportes, Política Fundiária, Projetos Especiais, Segurança Alimentar); a norma não o lista como Ministério (exceto o Ministério Extraordinário da Segurança Pública, 2018, que está no artigo da lista e conta como Ministério).
- **C** = titular com "prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado".
- **Ministérios + status** = soma das quatro colunas. Cada órgão conta uma vez. As colunas A, B e C estão separadas para quem preferir outra definição de "status".

Série em uma linha (Ministérios + status): 1995:27, 1996:28, 1997:29, 1998:29, 1999:26, 2000:25, 2001:26, 2002:26, 2003:34, 2004:35, 2005:36, 2006:34, 2007:34, 2008:36, 2009:37, 2010:37, 2011:37, 2012:38, 2013:38, 2014:39, 2015:39, 2016:31, 2017:26, 2018:28, 2019:22, 2020:22, 2021:23, 2022:23, 2023:37, 2024:38, 2025:38, 2026:38.
Só Ministérios: 1995:20, 1996:20, 1997:20, 1998:20, 1999:20, 2000:20, 2001:20, 2002:20, 2003:23, 2004:23, 2005:23, 2006:23, 2007:23, 2008:23, 2009:23, 2010:24, 2011:24, 2012:24, 2013:24, 2014:24, 2015:24, 2016:23, 2017:21, 2018:22, 2019:16, 2020:16, 2021:17, 2022:18, 2023:31, 2024:32, 2025:32, 2026:32.

## Quebras (a série não é comparável em linha reta)

`series/quebras.csv` traz 28 eventos com o trecho citado. Os que mais mudam a definição:

- 1999-06-10: Exército, Marinha e Aeronáutica viram o Ministério da Defesa (3 itens -> 1; MP 1.799-6).
- 1999-12-14: o Gabinete do Ministro Extraordinário de Política Fundiária (B) vira Ministério (item da lista).
- 2008-2010: Igualdade Racial, Direitos Humanos, Mulheres e Portos passam de C (equivalência) a A (Ministro de Estado Chefe); em 2011 o parágrafo deixa de listar nomes e passa a dizer "os titulares das Secretarias da Presidência da República" (mudança na regra de definição).
- 2016: a Controladoria-Geral da União passa de A para item da lista de Ministérios; desde 2019 consta como "Controladoria-Geral da União" (sem a palavra "Ministério") no artigo dos Ministérios.
- 2018: um Ministério Extraordinário (Segurança Pública, 26/2 a 31/12/2018) existiu entre duas fotos de 1/1 e não aparece na série.
- 2021: o Presidente do Banco Central deixa de ser Ministro de Estado (LC 179, 25/2/2021); contava em A desde 2004-2005.

## O que não foi achado ou não foi verificado

- Ato que criou o Gabinete do Ministro Extraordinário de Política Fundiária (existência confirmada nos Decretos 1.888, 1.918 e 2.321, de 1996-1997) e o de Projetos Especiais (citado na MP 1.795): não localizados. A classe B de 1997, 1998 e 1999 é por continuidade (linhas marcadas `nao_verificado`).
- Lei 9.649/1998 original (27/5/1998) não foi baixada; só o compilado de 2001 e as MPs. Não afeta as fotos de 1/1/1998 e 1/1/1999 (a MP 1.795 reescreve o art. 13), mas o art. 23 (equivalência da Casa Militar, 1999) foi lido só no compilado.
- Cargos de Ministro Extraordinário criados fora da lei de organização: não houve busca sistemática em 1995-1998. Tentativa de achar o ato de criação de Política Fundiária: WebSearch, varredura das MPs 1.385 a 1.449 (26 existem em `/MPV/Antigas/`, nenhuma trata do tema; baixadas em memória, sem registro) e dos Decretos 1.880 a 1.892 de 1996: nada. Outro Ministro Extraordinário do período, se houver, não está na série.
- Texto original da Lei 10.683/2003 não existe em arquivo próprio no Planalto: lido no compilado, onde o trecho sem anotação é o original.
- Decretos que extinguem ou criam cargos ministeriais fora das leis lidas: só o Decreto 4.046/2001 foi achado (pela remissão no compilado). Outros podem existir para anos não cobertos pelas anotações.
- Data de publicação no DOU: lida só quando o rodapé do Planalto a traz (coluna `verificacao`). Se a MP 1.549-38 saiu em 1-2/1/1998, vale a -37, de lista idêntica.
- Exposições de motivos das MPs não foram lidas: a coluna "razão declarada" de `quebras.csv` diz isso.
- 2026: o texto compilado da Lei 14.600 baixado em 20/10/2026 não mostra mudança do art. 17 ou 18 em 2025-2026 (já inclui a Lei 15.352 de 25/2/2026 em outro dispositivo); atos que o Planalto ainda não anotou não estariam refletidos.
- Efeitos de estrutura (decretos de estrutura regimental) das MPs 696/2015, 726/2016 e da Lei 13.502/2017 dependem de decretos não lidos; a lista de Ministérios vale desde a publicação.

## Ressalvas

- 2002: o texto do § 1º da MP 2.216-37 ainda cita o Chefe da Secretaria de Comunicação de Governo como Ministro; o Decreto 4.046 (10/12/2001) extinguiu o cargo e a série desconta (A=5, total 26). Leitura literal do parágrafo, sem o decreto: A=6, total 27.
- "Ministério" é o que a norma lista; "Ministro de Estado" inclui o Presidente do Banco Central (2005-2021) e o Advogado-Geral da União (2001-2026) por determinação legal.
- Reedições de MP (1995-2001): só as versões baixadas entram na comparação de listas; reedições intermediárias não baixadas (ex.: 1.549-25, 1.799-2, 1.799-3, 1.799-5, 1.999-11, 1.999-12) podem ter lista diferente das vizinhas. Em cada 1º de janeiro a versão usada é a última baixada com data <= 1/1, e o intervalo até a seguinte baixada é de ~30 dias (ciclo de reedição), então nenhuma versão vigente em 1/1 ficou de fora. A comparação é automatizada e tolera erros de numeração romana do texto do Planalto (anotados em `verificacao`).
- Cadeia de hash: `bruto/mpv-0111.html` tem uma linha antiga errada (baixei por engano a Lei 10.678 com esse nome) e foi re-baixado como MP 111 verdadeira; duas cópias de arquivos de outro agente (`l9649-compilada`, `l13502-compilada`) foram re-registradas para corrigir a URL. `chain.py verify` dá OK com 3 linhas "superseded".
