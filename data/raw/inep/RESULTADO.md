# INEP: taxas de rendimento do EF por UF, quebras de definicao e normas de ciclos (1994-2025)

Dossie governos-do-brasil-economia. Colheita e calculo de 2026-10-19/20. Sem opiniao: onde ha queda coincidindo com uma norma, o texto diz "coincide", com data e trecho; causa nao e medida aqui.

## 0. Entregas e como reproduzir

| arquivo | o que e |
|---|---|
| `series/edu_rendimento.csv` | 63.582 linhas (aprovacao, reprovacao, abandono, proxy R/(A+R)) por UF e Brasil |
| `quebras.csv` | 38 linhas: 5 mudancas de definicao da taxa, 3 de cobertura do Censo, 1 sobreposicao de publicacoes, 29 de regra (normas). 21 linhas dependem de fonte secundaria; 20 trazem "NAO LOCALIZADO" (texto da norma ou ato) |
| `comparacao_regra.csv` | 756 linhas (28 localidades x 27 anos), `regra_vigente` (sim/nao/parcial/nd), base e confianca da classificacao, 18 colunas de taxa, flag de qualidade |
| `comparacao_regra.md` | tabelas antes/depois de SP e MG contra a media simples do grupo sem a regra; tabela INEP de 1999; Saeb Brasil |
| `series/ciclos_1999_inep.csv` | matriculas do EF por forma de organizacao (seriado, ciclos, mais de uma forma) por UF, 1999, de `bruto/tabelas_ciclos_2000.xls` |
| `series/gates_quebras.txt` | 43 conferencias: cada `trecho_citado` achado literalmente no arquivo local |
| `normas/` | 17 arquivos novos (normas, artigos, imprensa), todos na cadeia de hash (linhas 45 a 61 do `manifest.jsonl`) |
| `series/ocr/` | texto por OCR (tesseract) das notas tecnicas escaneadas de 2008, 2011 e 2012 (derivado; o PDF e o bruto) |

Reproduzir: `python3 -I scripts/gerar_quebras_comparacao.py` (sem rede; usa `pdftotext`, `textutil` e `soffice` locais). O script para sem escrever se qualquer trecho citado nao for achado. `chain.py verify . --allow-missing` => OK, 61 linhas.

## 1. Anos cobertos por UF e rede

Para todas as 27 UFs e o Brasil (28 localidades), as mesmas faixas de anos:

| serie | anos | observacao |
|---|---|---|
| EF total, anos iniciais (1a-4a / 1o-5o) e anos finais (5a-8a / 6o-9o), redes total, estadual, municipal, privada, federal | 1996-2001, 2004-2005, 2007-2025 (EF total); 1997-2001, 2004-2005, 2007-2025 (anos iniciais e finais, redes estadual, municipal, privada, federal); `publica` so 2007-2025 | rede federal e municipal tem menos UFs (nem toda UF tem). `ef_ai` e `ef_af` em 1996 nao existem (o arquivo do Censo 1997 nao separa) |
| EM total | 1996-2001, 2004-2005, 2007-2025 | mesmas redes |
| proxy reprov/(aprov+reprov), EF total e por recorte, rede total | 1994-2001, 2004-2005, 2007-2025 | 1994 e 1995: so aprovados e reprovados nas Sinopses; nao ha abandono antes de 1996 |
| origem da taxa | 1994-2005: CALCULADA das contagens da Sinopse com X/(APR+REP+ABA); 2007-2025: PUBLICADA pelo INEP | |

Faltam 2002, 2003 e 2006 (secao 5).

## 2. O que `gates.txt` conferiu

56 linhas `OK`, nenhuma falha (`series/gates.txt`):

- cadeia de hash de 43 arquivos (agora 61);
- 2007-2025: cada planilha tem 1 ano e 28 localidades; aprovacao + reprovacao + abandono dentro de [99,7; 100,3] em 11.908 de 11.908 celulas publicadas;
- contagens 1994-2005: Total = Federal + Estadual + Municipal + Privada em 2.518 de 2.518 celulas, e soma das series confere;
- calibracao 2005 (taxa calculada das contagens x tabela 5.5 publicada): 18 de 28 localidades dentro de 0,15 p.p. nas tres taxas; maior erro de reprovacao 0,44 p.p.; maior erro de abandono 4,88 p.p. (MT); proxy R/(A+R) 0,24 p.p.;
- sobreposicao 2007 ("Resultados do Censo Escolar 2007", tabela 6.6.1 x planilha de taxas): 28 localidades, diferenca maxima 0,0 p.p.

O que `gates.txt` NAO pegou, achado nesta etapa: **a reprovacao do recorte anos finais (5a-8a serie) de 2000 esta inconsistente.** Em 18 de 28 localidades a taxa do EF total fica fora do intervalo entre anos iniciais e anos finais (ex.: SP estadual, anos finais 27,90%, EF total 4,47%, anos iniciais 2,61%; DF 60,8% nos anos finais). Provavel defeito de extracao da Sinopse 2001 (`bruto/sinopse_2001.zip`), nao corrigido (fora do escopo). `comparacao_regra.csv` mantem os valores e marca `flag_qualidade`; `comparacao_regra.md` mostra "suspeito". EF total e anos iniciais de 2000 passam na checagem.

## 3. As quebras (`quebras.csv`)

Definicao da taxa e do Censo (9 linhas):

1. **2005 -> 2007, Educacenso** (Sinopse 2007: "Em 2005 teve inicio um ciclo de reformulacao operacional e metodologica do Censo Escolar ... que culminou, em 2007, com a implantacao do sistema Educacenso"). Medido: Brasil, EF total, todas as redes, abandono 7,5 -> 4,8 (-2,7 p.p.) e reprovacao 13,0 -> 12,1 (-0,9 p.p.); o abandono caiu nas 28 localidades e a reprovacao em 23; media das variacoes -2,85 p.p. (abandono) e -0,97 p.p. (reprovacao). Referencia com metodo constante: BR 2007 -> 2009, abandono -1,10 p.p. e reprovacao -1,00 p.p. O passo de abandono entre 2005 e 2007 e maior que a variacao de 2 anos com metodo constante; mistura mudanca de metodo e mudanca real e nao ha 2006 para separar.
2. **2007, cobertura e data de referencia**: o INEP diz que a mudanca "reduziu de maneira drastica a dupla contagem de alunos"; matriculas da educacao basica -5,2% (quase tres milhoes) entre 2006 e 2007, "em parte" demografia, "em parte" metodo; a parcela de cada uma nao e informada. Referencia antiga em 30/3 (tabela 5.4 de 2005), nova na ultima quarta-feira de maio.
3. **Taxa calculada x publicada em 2005** (maior erro de abandono 4,88 p.p. em MT): afeta as 63.582 linhas com ano <= 2005, todas calculadas.
4. **Regra 5 das notas tecnicas (abandono na origem)**: NT 2008, 2009, 2010, 2011/2013 trazem criterios sucessivamente mais estreitos para contar abandono quando o aluno aparece em outra escola. Direcao: menos abandono classificado; magnitude nao medida (a NT 2008 so conta casos, todas as etapas: 3.966.400 na regra 6 e 4.766 na regra 5).
5. **2009, Educacao Especial** deixa de ter "sem informacao" a pedido da SEESP; nao medido.
6. **TNR** muda de formula (2010 -> 2016); nao afeta as tres taxas.
7. **EF de 9 anos** (Lei 11.114/2005; Lei 11.274 de 6/2/2006, art. 32 "duracao de 9 anos ... iniciando-se aos 6 anos"): os recortes anos iniciais/finais passam de 1a-4a/5a-8a para 1o-5o/6o-9o; as planilhas 2007-2010 misturam 8 e 9 anos; nao medido.
8. **1994-1995**: so aprovados e reprovados.
9. **Sobreposicao 2007**: as duas publicacoes de 2007 coincidem (0,0 p.p.); nao ha quebra entre elas.

Normas de ciclos e progressao continuada (29 linhas, tipo `mudanca_de_regra`; "FONTE SECUNDARIA" marcada na coluna `fonte_primaria_url`):

| UF | norma | data | fonte | texto |
|---|---|---|---|---|
| todas | LDB art. 32 §1o (facultado desdobrar o EF em ciclos) | 1996-12-20 | primaria (planalto) | sim |
| SP | Ciclo Basico (2 series iniciais) | 1984; vigente em 1997 | primaria (Indicacao CEE 8/97 diz "O atual ciclo basico") | ato de 1984 nao localizado |
| SP | Deliberacao CEE 09/97 (progressao continuada, 8 anos, um ou mais ciclos) | aprovada 30/7/1997; homologada Res. SE de 4/8/97, DOE 5/8/97 | primaria (ceesp.sp.gov.br) | sim |
| SP | Indicacao CEE 08/97 | 30/7/1997 | primaria | sim |
| SP | Indicacao CEE 22/97 | 17/12/1997 | primaria | sim |
| SP | Resolucao SE 4/98 (2 ciclos, reprovacao so ao fim do ciclo e por frequencia < 75%) | 15/1/1998 | SECUNDARIA (ANPEd) | NAO LOCALIZADO |
| SP | Resolucao SE 84/2003 (extingue recuperacao intensiva nas ferias) | 15/8/2003 | SECUNDARIA (Redalyc) | NAO LOCALIZADO |
| SP | tres ciclos, retencao possivel no 3o, 6o e 9o ano | anunciado 8/11/2013, em vigor 2014 | SECUNDARIA (imprensa; Indicacao ALESP 1929/2015) | numero NAO LOCALIZADO |
| SP municipio | Regimento Comum, 3 ciclos | 1992 | SECUNDARIA (Barretto e Sousa 2004) | NAO LOCALIZADO |
| SP municipio | decreto: 2 ciclos de 4 anos | 1997-2000 | SECUNDARIA | decreto NAO LOCALIZADO |
| MG | Res. SEE 5231/84 (CBA) | 6/12/1984 | SECUNDARIA (dissertacao UFU) | NAO LOCALIZADO |
| MG | Res. 6806/91 (CBA retomado) | 1991 | SECUNDARIA | NAO LOCALIZADO |
| MG | Res. 7915 (CBA em 3 series) | publ. 20/12/1996; 1997 | SECUNDARIA | NAO LOCALIZADO |
| MG | Res. 8086/97 (2 ciclos, obrigatorio) | 1997; obrigatoria desde 1998 | SECUNDARIA | NAO LOCALIZADO |
| MG | Res. 12/99 (escola decide a organizacao em 1999) — **restringe a regra** | 1999 | SECUNDARIA | NAO LOCALIZADO |
| MG | Res. 006/2000 (3 ciclos) | 20/1/2000 | SECUNDARIA | NAO LOCALIZADO |
| MG | revogacao/restricao em 2004 (hipotese do briefing) | - | nenhuma fonte baixada a registra | NAO LOCALIZADA |
| PR | Decreto 2545 (Ciclo Basico de Alfabetizacao) | 14/3/1988 | SECUNDARIA (FCC) | NAO LOCALIZADO |
| CE | ciclos graduais (40% das escolas em 1998; ~60% em 2000) | 1997-2000 | SECUNDARIA (Barretto e Mitrulis 2001) | documento "Ceara, 1997" NAO LOCALIZADO |
| CE | Parecer CEC 1014/98 | 1998 | SECUNDARIA (ANPUH) | NAO LOCALIZADO |
| MS | Res. SED 1.222/98 (EF de 9 anos em 3 ciclos) | 10/2/1998 | SECUNDARIA (dissertacao UFMS) | NAO LOCALIZADO |
| MS | Res. SED 1.452/00 (EF de 8 anos, ciclos so nos anos iniciais) — **restringe a regra** | 18/12/2000, vale 2001 | SECUNDARIA | NAO LOCALIZADO |
| MT | Res. 262/02-CEE/MT (ciclos de formacao; adesao opcional) | 5/11/2002 | primaria | sim |
| RJ | "bloco unico" na proposta curricular do estado | 1994 | SECUNDARIA | ato NAO LOCALIZADO |
| PE | niveis na escola primaria | 1968 (fora da janela) | SECUNDARIA | NAO LOCALIZADO |
| RS | classes de recuperacao ("progressao continuada") | 1958 (fora da janela) | SECUNDARIA | NAO LOCALIZADO |
| ES, RN, RJ, MG, MS | adesao medida no Censo 2000: MS 96,9%, ES 93,4%, RN 88,1%, RJ 78,7%, MG 73,6% das escolas estaduais; SP 100% | 2000 | SECUNDARIA | normas de ES e RN NAO LOCALIZADAS |
| Brasil, UF | tabela INEP de matriculas por forma de organizacao | 1999 | primaria (bruto) | - |

## 4. Comparacao antes/depois (rede estadual, EF; `comparacao_regra.md`)

Grupo sem a regra: 12 UFs (AC, AL, AM, GO, MA, PA, PB, PE, RR, RS, SC, SE), por um criterio unico: ciclos + escolas com mais de uma forma <= 10% das matriculas em 1999 (tabela INEP), e nenhuma norma localizada. 1996-1998 e 2000-2001 sao extrapolacao sem prova direta.

Reprovacao, EF total, rede estadual (%):

| ano | SP | MG | grupo sem a regra |
|---|---|---|---|
| 1996 | 9,04 | 8,75 | 17,40 |
| 1997 | 4,09 | 3,03 | 14,86 |
| 1998 | 2,29 | 0,99 | 12,34 |
| 1999 | 3,48 | 4,13 | 12,38 |
| 2000 | 4,47 | 5,75 | 12,88 |
| 2001 | 5,26 | 4,98 | 12,92 |
| 2004 | 6,01 | 10,77 | 14,75 |

Abandono, EF total, rede estadual (%) (1996-2005 calculado; erro de abandono calculado pode chegar a 4,88 p.p. numa UF):

| ano | SP | MG | grupo sem a regra |
|---|---|---|---|
| 1996 | 6,80 | 9,84 | 15,46 |
| 1997 | 4,22 | 9,47 | 13,82 |
| 1998 | 4,18 | 8,44 | 13,58 |
| 1999 | 4,33 | 9,91 | 12,89 |
| 2000 | 4,67 | 8,67 | 13,53 |
| 2001 | 3,11 | 6,37 | 11,72 |
| 2004 | 2,52 | 7,47 | 11,60 |

O que o dado mostra:

- Em SP a reprovacao do EF total cai de 4,09 (1997) para 2,29 (1998), o ano da Res. SE 4/98: a queda coincide com a norma. O grupo sem a regra tambem cai no mesmo intervalo (14,86 -> 12,34), -2,52 p.p. contra -1,80 p.p. em SP; a diferenca das variacoes e +0,72 p.p. (SP caiu menos em pontos, partindo de base cerca de tres vezes menor).
- Em SP a reprovacao sobe depois: 3,48 (1999), 4,47 (2000), 5,26 (2001), 6,01 (2004); em 2001 esta +1,17 p.p. acima de 1997 enquanto o grupo esta -1,94 p.p. abaixo. A diferenca entre SP e o grupo fica entre -7,7 e -10,8 p.p. em todos os anos da janela.
- **A maior queda de SP e MG ocorre ANTES da Res. SE 4/98**: de 1996 para 1997, SP 9,04 -> 4,09 e MG 8,75 -> 3,03, contra 17,40 -> 14,86 no grupo. Os dois valores vem de arquivos diferentes (1996: `censo_1997.zip`; 1997: PDF do Censo 1998), e a Deliberacao CEE 09/97 so e de 30/7/1997. Nao ha como separar aqui efeito de norma, efeito de arquivo e efeito de ano.
- Abandono em SP: 4,22 (1997), 4,18 (1998), 4,33 (1999), 3,11 (2001), 2,52 (2004); nao ha queda no ano da norma (-0,04 p.p.).
- MG: reprovacao 3,03 (1997) -> 0,99 (1998, ano em que a Res. 8086/97 e obrigatoria), depois 4,13 (1999, Res. 12/99 devolve a decisao a escola), 5,75 (2000), 4,98 (2001), 10,77 (2004). A subida de 1998 para 1999 (+3,14 p.p.) coincide com a Res. 12/99; o grupo ficou estavel no mesmo intervalo (+0,04 p.p.). Nenhuma norma de MG posterior a 2000 foi localizada.
- SP, anos iniciais: 3,90 (1997), 1,39 (1998), 2,37, 2,61, 3,70 (2001), 3,29 (2004). Anos finais: 4,26 (1997), 2,99 (1998), 4,18 (1999), 2000 suspeito, 6,21 (2001), 7,60 (2004).
- SP 2014 (tres ciclos): reprovacao EF total estadual 4,50 (2013), 4,60 (2014), 3,50 (2017); grupo sem a regra 12,65, 12,67, 9,88. A reprovacao em SP nao sobe no primeiro ano da norma que amplia a possibilidade de retencao (+0,10 p.p.); o grupo foi definido em 1999 e nao foi reverificado em 2014.
- MS: reprovacao EF total estadual 18,18 (1997) -> 11,38 (1998), ano da Res. SED 1.222/98 (grupo sem a regra -2,52 p.p.); 16,37 (2000) -> 17,29 (2001) -> 24,23 (2007) depois da Res. 1.452/00, que limitou os ciclos aos anos iniciais (grupo: +0,04 p.p. de 2000 a 2001).
- CE: reprovacao EF total estadual 8,56 (1997) -> 6,65 (1998) -> 7,32 (2001); abandono 12,72 -> 12,53 -> 12,61; ciclos implantados so em parte das escolas (cerca de 60% em 2000).
- Cada linha de norma em `quebras.csv` traz o mesmo calculo (ano-base, primeiro ano posterior, ano + 3, variacao da UF e do grupo).
- **Saeb**: Saeb por UF 1995-2005 nao foi obtido em arquivo pequeno do INEP. Usei `../dominios-1/series/edu.csv` (so Brasil, Press Kit Saeb 2019, escala 0-500; abrangencia varia por edicao): 4a serie LP 188, 187, 171, 165, 169, 172 e Mat 191, 191, 181, 176, 177, 182 (1995, 1997, 1999, 2001, 2003, 2005). Nao serve para comparar SP com outras UFs.

## 5. O que NAO foi achado

**Anos sem taxa: 2002, 2003, 2006.**

- **2002**: as tabelas de aprovados e reprovados de 2002 existem em `bruto/sinopse_2003_miolo3.pdf` (154 paginas, "5.1.1 ... segundo a Regiao Geografica e a Unidade da Federacao - 2002"), mas `pdftotext` devolve so os titulos: as tabelas nao tem camada de texto. Nao foram lidas por OCR (fora do escopo desta etapa); e a unica entrada para recuperar 2002.
- **2003**: nenhum arquivo de rendimento de 2003 esta em `bruto/`. `internet_2003.zip` (Censo Escolar 2003) tem uma unica aba, "Total de Alunos por Municipios". A Sinopse que traria o rendimento de 2003 nao foi baixada; a consulta ao indice do Wayback (CDX) deu tempo esgotado em 2026-10-20 e nao foi repetida.
- **2006**: a Sinopse do Censo 2006 traz o rendimento de 2005; a Sinopse/Resultados de 2007 traz o de 2007. A nota tecnica do INEP de 2013 diz que o calculo vale "a partir de 2007" para dados de situacao do aluno. Nenhum dos 44 brutos originais nem os novos contem taxas de 2006. Nao verifiquei se o INEP publicou 2006 em arquivo que nao esta em `bruto/`.

**Normas nao localizadas (texto primario):** Resolucao SE 4/98 (SP), Resolucao SE 84/2003, ato de 2014 de SP (numero), Res. SEE/MG 5231/84, 6806/91, 7915, 8086/97, 12/99, 006/2000, Decreto 2545/88 (PR), documento "Ceara, 1997" e Parecer CEC 1014/98, Res. SED 1.222/98, 1.401/00 e 1.452/00 (MS), Res. 118/01 e 150/99 do CEE/MT, ato do RJ de 1994, normas de ES e RN (ciclos), norma de PE e BA dos anos 1990, norma do RS dos anos 1990, Escola Candanga (DF). Tentativas: site do CEE-SP (achou so Deliberacao 09/97, Indicacoes 08/97 e 22/97), Wayback (fora do ar nesta sessao), `escolas.educacao.ba.gov.br` (Resolucao CEE 127/97 da Bahia: DNS esgotou), buscas de web. Nenhuma foi inventada: cada uma esta marcada `NAO LOCALIZADO` com a fonte secundaria que a cita e o trecho.

**Outros:** nao foi localizada revogacao ou restricao em MG em 2004; a restricao documentada de MG e de 1999. Nao ha serie da rede municipal de SP (capital) em `series/`. Saeb por UF nao foi obtido. O criterio do grupo sem a regra vem de uma unica tabela de 1999.
