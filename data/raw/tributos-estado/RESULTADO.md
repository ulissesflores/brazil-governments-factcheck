# Tributos, burocracia e Estado: o que se achou e o que NÃO se achou

Colheita de 2026-10-20. Pasta: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/`. Pré-registro: `../preregistro/PREREGISTRATION-EMENDA-03.md`, seções C e D. Só contagens e valores publicados: sem nota, sem ranking, sem atribuição de causa. Cadeia de hash: `manifest.jsonl` (`chain.py verify` = OK; ver o fim deste arquivo). Regenerar tudo: `scripts/rodar_tudo.sh` (`python3 -I`, só lê bruto). Já cobertos em outra pasta, só referenciados aqui: Cide-combustíveis, receita anual (`../mecanismos-preco/series/cide-combustiveis-receita-anual.csv`), renúncia fiscal e gastos tributários (`../mecanismos-contabil/series/gastos-tributarios-federais.csv`, quadros DGT em `../mecanismos-contabil/bruto/`) e dividendos e participações na RTN (`../mecanismos-contabil/series/rtn-resultado-primario-extraordinarias.csv`, indicador `dividendos_participacoes_*`).

Subpastas de subagentes (cadeia de hash própria, `quebras.csv` própria): `ministerios/` (D1) e `estatais-lucro/` (D3, Caixa, Correios e Petrobras/BB/Eletrobras 1995-2009). Resumo delas na seção 6.

## 1. C1, carga tributária (bases separadas, nunca emendadas)

Cada edição de cada fonte é uma série própria, com o `vintage` na última coluna. Entre edições o mesmo ano muda: isso é dado, não erro (ver `quebras.csv`).

| arquivo | base | cobertura | observação |
|---|---|---|---|
| `series/ipea-td583-carga-tributaria-1947-1996.csv` | Ipea TD 583 (Varsano et al., 1998), Tabela A.1 (literatura) | 1947-1996 (1996 estimativa) | 50 anos; metodologia muda em 1980 e em 1990 |
| `series/receita-ctb-total-por-edicao.csv` | Receita Federal, *Carga Tributária no Brasil*, 30 edições (1995-2024) | 1994-2024 | PDF de 1995 a 2013 (quadro de abertura, 2 anos por edição, mais séries de 5 anos nas edições 2006-2011), planilhas 2014-2024 (série 2002-ano) |
| `series/receita-ctb-por-base-por-edicao.csv` | idem, tabela INC02B, 7 bases e subitens (comércio exterior = código 4300, dentro de Bens e Serviços) | 2002-2024 por edição (2014-2024) | 5.868 linhas; a edição 2023 tem `#REF!` no total de 2023 e em Outros (pulado) |
| `series/receita-ctb-por-esfera-por-edicao.csv` | idem, tabela T01B (federal, estadual, municipal, total) e tabela do PDF de 2006-2013 | 2002-2024 (2014-2024), 2 anos por edição de 2006 a 2013 | 764 linhas |
| `series/tesouro-ctb-governo-geral-por-boletim.csv` | Tesouro Nacional, CTB do governo geral (GFSM 2014), boletins 2018, 2020, 2022 e 2025 | 2017-2025 | Tabela 1 de cada boletim (2 anos); rótulos do Gráfico 1 do boletim 2025 (1 casa decimal) dão 2010-2025; os gráficos dos outros boletins são imagem |

Definições que mudam entre as edições da Receita (cada uma com linha em `quebras.csv`): 1995 (CTB com saques do FGTS deduzidos), 1996-1997 (Carga Fiscal Bruta e Líquida), 1998 (CTB com IRRF estadual/municipal e previdência municipal), 2006 (sem restituições, com atualização monetária, PIB revisto: o texto avisa que a série "não é diretamente comparável" com as anteriores), 2024 (sem FGTS e Sistema S, série recalculada).

Valores sem juízo, só para o leitor localizar a variação entre vintages (todos % do PIB, ver CSV): 2005 = 37,37 na edição 2005 e 33,38 na edição 2006; 2013 = 35,95 na edição 2013 e 33,74 na 2014; 2023 = 32,11 na edição 2023 e 30,22 na 2024; 2002 = 32,16 na edição 2014 e 30,27 na 2024.

NÃO achado em C1:
- **Ipeadata não tem a série**: nenhuma das 4.071 séries do catálogo (`bruto/ipeadata-metadados-catalogo-2026-10-20.json`) traz "carga tributária" no nome. A compilação longa do Ipea aqui é o TD 583 (literatura), até 1996.
- **Lacuna 1997-2001** na compilação de 1947: há só os valores de cada edição da Receita (1997 e 1998 em duas definições, 1999 a 2001 do quadro de abertura).
- **Tesouro, os boletins de 2010 a 2024 exceto 2018, 2020 e 2022** não foram baixados: o Tesouro Transparente derrubou as conexões e as URLs numéricas do `cdn.tesouro.gov.br` não são deriváveis. Só 4 boletins entraram.
- **Receita 1995-2005 por base e por esfera**: só o total (o texto dos PDFs de 1995-2005 não traz as tabelas por base em formato extraível); 2006-2013 só as esferas.
- Série de 5 anos no PDF de 1998-2005: o quadro "Tabela 2" não saiu no texto extraído (provavelmente imagem), então ficaram os dois anos do quadro de abertura.

## 2. C2, eventos tributários (`eventos_tributarios.csv`, 41 linhas)

Cada linha: data do ato, instrumento, tributo, sentido (`cria`, `aumenta`, `reduz`, `extingue`, mais `prorroga` e `altera`), a base do sentido, governo da data, URL do Planalto, trecho literal (extraído por regex do HTML baixado, e conferido contra o cabeçalho do arquivo), hash do bruto e vintage.

- Cobre tudo o que o pedido listou: CPMF (EC 12/1996, Lei 9.311/1996, EC 21/1999, EC 37/2002, EC 42/2003 e o fim em 2007, com a votação do Senado de 13/12/2007: 45 votos a favor, 34 contra, faltaram 4), Cide (Lei 10.336/2001), Simples (Lei 9.317/1996), Simples Nacional (LC 123/2006), MEI (LC 128/2008), desoneração da folha (Leis 12.546/2011, 12.715/2012, 13.161/2015, 13.670/2018, 14.784/2023, 14.973/2024), LC 192 e 194/2022, EC 132/2023 e LC 214/2025.
- Amostra de IR, IPI e IOF com texto lido: IR (Leis 9.249 e 9.250/1995, 11.482/2007, 12.469/2011, 13.149/2015, 14.663/2023, 15.270/2025), IPI (Decretos 6.696/2008, 7.567/2011, 10.979/2022), IOF (Decretos 6.339/2008, 6.983/2009, 7.323, 7.330 e 7.412/2010, 10.997/2022, 12.466, 12.467 e 12.499/2025).
- **A lista de IR, IPI e IOF NÃO é exaustiva**: o pedido é de "aumentos/reduções com data", mas o Planalto não tem uma lista única e este bloco leu 18 atos. Contagem de linhas por governo não é comparável e não deve ser usada.
- **Sentido não verificado** quando o texto lido não traz o valor anterior: Decretos 6.339/2008 e 12.466/2025 estão como `altera`, não `aumenta`; o Decreto 7.567/2011 e as leis de tabela do IRPF também. Só `aumenta` onde dois textos lidos se comparam (Decretos 7.323 e 7.330; Lei 13.161 contra a Lei 12.715) ou onde o texto traz o verbo.
- O Decreto Legislativo 176/2025, que sustou os decretos do IOF de 2025, **não foi baixado** (404 no padrão de URL do Planalto); o texto original da Lei 9.649/1998 também deu 404 em `/leis/l9649.htm` (só a versão compilada foi baixada); a sustação aparece apenas como "Vide" na anotação dos decretos.
- Textos consolidados do Planalto podem ter redação posterior à da data do ato (coluna `vintage`).

## 3. C3, burocracia

| arquivo | conteúdo | observação |
|---|---|---|
| `series/mapa-empresas-tempo-abertura-por-quadrimestre.csv` (coluna `ano` traz `2020-Q1` ou `2019-01`: as pastas vizinhas só têm séries anuais e não há convenção sub-anual) | tempo médio de abertura de empresas, Mapa de Empresas/Redesim, em horas | 2019-01 (ponto mensal lido de rótulo de gráfico: 5 dias e 9 horas) e 2020-Q1 a 2025-Q2 (15 boletins); **falta 2019 inteiro, 2024-Q3, 2025-Q1 e Q3**: as URLs deles não existem no padrão do gov.br; método muda em 2024-Q2 |
| `series/ibpt-normas-tributarias.csv` | normas tributárias e gerais editadas desde 5/10/1988: acumulado (transcrito de imagem), mais o fluxo anual derivado por subtração | **FONTE SECUNDÁRIA**: cópia do release do IBPT hospedada pelo Poder360 (nov/2022); o PDF no site do IBPT não foi baixado; 2022 até 30/09; valor transcrito da tabela-imagem e conferido contra o único âncora legível (7.129.074) |
| `series/doing-business-brasil.csv` | Doing Business, Brasil (linha BRA), edições 2004-2020: pontuação, abrir empresa, impostos | duas vintages lado a lado (`DB20 Data` completa, `DB21 Data` revisada, só 2014-2020); o ano é o da edição |
| `eventos_burocracia.csv` | Lei 11.598/2007 (Redesim), Lei 13.874/2019 (Liberdade Econômica) e a nota oficial do Banco Mundial de 16/09/2021 | trecho literal e URL |

Nota exigida: o Doing Business foi **descontinuado em 2021**. A nota oficial do Banco Mundial (`bruto/bm-nota-descontinuacao-doing-business-2021-09-16.html`, https://www.worldbank.org/en/news/statement/2021/09/16/world-bank-group-to-discontinue-doing-business-report) diz: "After data irregularities on Doing Business 2018 and 2020 were reported internally in June 2020, World Bank management paused the next Doing Business report ...". O relatório de investigação citado na nota não foi baixado. As séries aqui são citadas só com essa nota.

NÃO achado em C3: série anual de normas tributárias **por ano** direto da fonte (só o acumulado; o fluxo é derivado); tempo de abertura de empresas antes de 2019 pelo Mapa de Empresas; o relatório de investigação do Banco Mundial.

## 4. D2, cargos em comissão (DAS, FCPE, CCE, FCE)

`series/pep-cargos-comissionados.csv`: dezembro de cada ano de 1999 a 2025 e o último mês disponível (setembro de 2026), do Painel Estatístico de Pessoal (Ministério da Gestão): total de ocupações de DAS, FCPE, CCE e FCE (soma dos agrupamentos "DAS, FCPE e correlatas" e "CCE & FCE" do painel), por 1.000 servidores ativos do Executivo civil (medida "Quantidade de ativos" do próprio PEP; no último mês reproduz o KPI do painel, 579.849), parcela sem cargo efetivo registrado (`Grupo Cargo = S/cargo`, aproximação do "sem vínculo": o PEP não usa esse rótulo), e a quebra por família (DAS, FCPE, CCE, FCE e outras).

Como foi colhido: pela página do PEP no Chrome (Qlik Sense, `app.createCube`), porque a API do dados.gov.br pede token e o painel não oferece arquivo estável. Os valores foram **transcritos do retorno do console** (`bruto/pep/pep-dezembro-e-ultimo-mes-transcrito-do-qlik.csv` e `bruto/pep/LEIA-ME-consulta.txt`, ambos na cadeia). O mensal 1999-2026 existe no painel; aqui está só dezembro e o último mês.

Marcos medidos (todos em `quebras.csv`): a queda de 2020-12 para 2021-01 (90.086 para 23.654 no total geral e 22.542 para 5.888 em DAS+FCPE, -74%) tem **causa não identificada** (o changelog do próprio app, 59 entradas, foi lido: nenhuma entrada de 2020-12 a 2021-03 menciona mudança de cobertura; trechos em `bruto/pep/pep-changelog-trechos-lidos.txt`); a troca DAS por FCPE em 2016-2017 (Lei 13.346/2016); a troca DAS e FCPE por CCE e FCE (Lei 14.204/2021).

NÃO achado em D2: **1996-1998** (o PEP começa em 1999; o Boletim Estatístico de Pessoal em PDF não está acessível: `gov.br/servidor/.../arquivos/YYYYMMparte1.pdf` devolve uma página HTML genérica de 55.843 bytes para qualquer nome, guardada como evidência negativa; a página antiga do Ministério do Planejamento não resolve DNS e o Wayback Machine estava fora do ar); a tabela de DAS por nível do BEP em PDF (nenhuma extraída); "sem vínculo" com o rótulo do próprio painel.

## 5. D3, estatais

| arquivo | conteúdo | cobertura |
|---|---|---|
| `series/nfsp-estatais-bcb.csv` | NFSP das empresas estatais (total, federais, estaduais, municipais): resultado primário e nominal (soma dos fluxos mensais do ano, R$ milhões), % do PIB (dezembro, acumulado em 12 meses), saldo da dívida líquida; mais duas séries do Ipeadata | **2001-12 a 2026-08** (SGS 4645-4648, 4579-4582, 5789-5792, 5723-5726, 4474-4477) |
| `series/cvm-lucro-petrobras-bb-eletrobras.csv` | lucro líquido consolidado e atribuído à controladora, DFP da CVM, exercício ÚLTIMO e PENÚLTIMO lado a lado | 2009-2025 (192 linhas) |
| `series/sest-raeef-estatais.csv` | SEST/MGI, RAEEF 19-20 e 21-22: resultado líquido de BB, Caixa, Correios, Eletrobras e Petrobras (R$ mil), mais 4 agregados citados no texto da edição 21-22 (lucro de 2021 R$ 187,7 bi e de 2020 R$ 60,6 bi; dividendos e JCP pagos R$ 101,0 bi, dos quais R$ 43 bi à União) | 2015-2021 |
| `series/tesouro-dividendos-2015-2020.csv` | Tesouro Transparente, dividendos, JCP e prêmio de debêntures arrecadados pela União: total por ano e por empresa | 2015 a abril de 2020 (2020 é ANO PARCIAL) |

Convenção do BCB, conferida contra o consolidado (SGS 5793: 2015 = +1,86; 2008 = -3,33): positivo é necessidade de financiamento (déficit); negativo é superávit.

NÃO achado em D3:
- **NFSP das estatais antes de dezembro de 2001**: nem o SGS nem o Ipeadata têm (janelas 1980-1999 do SGS: HTTP 404, guardado na cadeia). O Ipeadata tem 10 linhas datadas de 1953-12 a 1954-09 numa série do BCB que começa em 2001-12: datas implausíveis, excluídas da agregação.
- **Boletim das Empresas Estatais Federais** (SEST, trimestral) e **Relatório de Dividendos** do Tesouro: as páginas do gov.br/economia devolvem página de login e o Tesouro Transparente só tem a planilha 2015-abril/2020. Não há lucro líquido consolidado nem dividendos pagos à União por ano **antes de 2015 nem depois de abril de 2020** em fonte primária baixada aqui (para dividendos 1997-2025, ver o indicador `dividendos_participacoes_*` da RTN na pasta `mecanismos-contabil`, referência e não réplica). As edições do RAEEF posteriores à de 2021 (exercício 2021) não foram achadas no gov.br.
- Lucro por empresa **antes de 2009** e Caixa/Correios depois de 2021: ver `estatais-lucro/` (seção 6).

## 6. Subagentes (cadeia de hash e `quebras.csv` próprias; `chain.py verify` = OK nas duas e nesta pasta)

**D1, `ministerios/` (`ministerios/RESULTADO.md`, `ministerios/series/ministerios-1-de-janeiro.csv`, `ministerios-por-ano.csv`, `quebras.csv` com 28 eventos).** Número de órgãos que a norma vigente em 1º de janeiro chama de "Ministérios" (`n_ministerios`) e, à parte, mais os órgãos cujos titulares a norma declara Ministro de Estado, Ministro Extraordinário ou com prerrogativas equivalentes (`n_ministerios_mais_status`), cada classe também como indicador separado. Ano:ministérios — 1995-2002: 20; 2003-2009: 23; 2010-2015: 24; 2016: 23; 2017: 21; 2018: 22; 2019-2020: 16; 2021: 17; 2022: 18; 2023: 31; 2024-2026: 32. Ministérios + status — 1995: 27; 1999: 26; 2003: 34; 2010: 37; 2015: 39; 2016: 31; 2019: 22; 2022: 23; 2023: 37; 2024-2026: 38 (série completa no CSV). Marcado `nao_verificado`: 1997, 1998, 1999 (falta o ato de criação de dois gabinetes de Ministro Extraordinário, contados por continuidade) e 2026 (texto compilado do Planalto pode estar atrasado). A definição de "status" é do agente e está no `ministerios/RESULTADO.md`; em 2002 há duas leituras (26 pelo texto descontado do Decreto 4.046/2001, 27 pelo parágrafo literal da MP 2.216-37). Um Ministério Extraordinário (Segurança Pública, 26/2 a 31/12/2018) existiu entre duas fotos de 1º de janeiro e não aparece. NÃO achado: o ato de criação dos gabinetes de Política Fundiária e de Projetos Especiais; nove MPs antigas (404 em `/MPV/Antigas/`); a Lei 10.683 original (o Planalto só tem o compilado); as exposições de motivos das MPs.

**D3 parcial, `estatais-lucro/` (`estatais-lucro/RESULTADO.md`, `series/lucro-liquido-<empresa>.csv`, `quebras.csv` com 29 linhas).** Lucro líquido anual pelas demonstrações da própria empresa, cada edição/vintage em linha própria, sem emendar, na unidade e moeda do documento: Banco do Brasil 1995-2009 (15 anos), Petrobras 1997-2009 (13), Eletrobras 2000-2009 (10), Caixa 2001-2025 (25), Correios 2000-2025 (26). Definições mudam (BR GAAP consolidado ou controladora, IFRS, US GAAP em R$, R$ mil, milhões ou unidades, US$ milhões na Petrobras de 1997-2008): leia a coluna `definicao_linha` antes de comparar anos. NÃO achado: Petrobras 1995-1996; Eletrobras 1995-1999; Caixa 1995-2000; Correios 1995-1999; as edições originais de 1998 e 2000 da Petrobras e de 2000 da Eletrobras. Alguns PDFs de Correios e Caixa são imagem: valores lidos por OCR ou visualmente, marcados na nota da linha. A Wayback Machine foi usada para Petrobras e Eletrobras antigas (URL registrada no formato `web.archive.org/web/...id_/`).

## 7. Cadeia de hash e arquivos

Cada arquivo baixado tem uma linha em `manifest.jsonl` (seq, url, timestamp, sha256, nota, prev_hash). Reabertos por falha: `bruto/bep/201612parte1.pdf` (página HTML, não PDF), seis janelas do BCB que devolveram HTML de erro e foram baixadas de novo, e `bruto/bcb-sgs/sgs4645-b.json` (404 do BCB guardado como evidência negativa). Os zips da CVM (16 arquivos, 8,9 a 13,3 MB cada) ficam na cadeia; os valores usados saem de `scripts/cvm_lucro.py`. `derivado/txt/` = `pdftotext -layout` dos PDFs (não hasheado, regenerável). **Tamanho em disco**: `bruto/` 305 MB aqui (16 zips da CVM somam cerca de 165 MB), `estatais-lucro/` 445 MB e `ministerios/` 15 MB; nenhum arquivo passa de 25 MB. Se o repositório precisar ser leve, os brutos podem ficar só como hash (`chain.py verify --allow-missing`, `restore`).

## 8. Quebras (`quebras.csv`, 24 linhas)

C1 (13 linhas: 10 da Receita por edição ou par de edições, Tesouro, Receita x Tesouro, Ipea), C3 (4: Mapa de Empresas, Mapa x Doing Business, Doing Business DB20 x DB21, IBPT), D2 (3), D3 (4: NFSP sem série antes de 2001, Ipeadata, CVM, dividendos do Tesouro). Colunas iguais às de `../mundo/quebras.csv`. `tipo_de_quebra` entre `metodo_estatistico`, `mudanca_de_regra`, `revisao_de_vintage` e `mudanca_de_unidade`. Onde a causa não está no texto da fonte, a linha diz "causa NÃO identificada".
