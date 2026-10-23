# RESULTADO: nascimentos e obitos por ano no Brasil (fase 2, populacao)

> Gerado por `scripts/montar_resultado.py` a partir dos CSV; tabelas nao foram digitadas. Aquisicao em 2026-10-21, cadeia de hash em `manifest.jsonl`. Sem nota, sem ranking, sem atribuicao de causa. Cada base e uma serie separada: nenhuma foi emendada com outra. Legenda: [OK] obtido e reproduzivel; [PARCIAL] com limite declarado; [NAO ACHADO] nao obtido.

## 0. Resumo

1. [OK] DATASUS SIM, obitos totais por ocorrencia e por residencia: 1979-1995 (CID-9, base `obt09uf`) e 1996-2026 (CID-10, base `obt10uf`), duas bases separadas. Final ate 2024, 2025 preliminar, 2026 e previa incompleta (nao e total anual).
2. [OK] DATASUS SINASC, nascidos vivos por ocorrencia e por residencia da mae: 1994-2026 (mesmos carimbos: final ate 2024, 2025 preliminar, 2026 parcial).
3. [PARCIAL] IBGE Registro Civil (SIDRA, 10 tabelas): nascidos registrados no ano e ocorridos no ano, obitos registrados no ano e ocorridos no ano, 1984-2024, mais mensal 2003-2024. NAO ACHADO: qualquer ano anterior a 1984 (a menor data das tabelas SIDRA e 1984, nao 1974).
4. [OK] Banco Mundial WDI: taxa bruta de natalidade, taxa bruta de mortalidade e populacao, 1960-2024 (2025 vem nulo). Derivado declarado: nascimentos e obitos estimados = taxa x populacao / 1000, 1960-2024 (cobre 1964-1978).
5. [OK] ONU World Population Prospects 2024 (variante Medium), Brasil 1950-2026 recortado (2026 e projecao; fora dos derivados) em `series/onu_wpp2024.csv`; arquivo completo (16,5 MB, todos os paises) so em `bruto/` e no hash.
6. [PARCIAL] 1964-1978: so existe estimativa (WDI derivado e ONU). Nenhum registro administrativo (SIM comeca em 1979, SINASC em 1994, Registro Civil/SIDRA em 1984).
7. Achado de conferencia: o WDI nao e uma segunda fonte, e a mesma estimativa da ONU: nascimentos e obitos derivados do WDI diferem do WPP 2024 em no maximo 0,003% e 0,008% (calculado, 1960-2024). A conferencia independente e SIM x Registro Civil x ONU.

## 1. Tabela dos anos-chave (valores absolutos, pessoas)

`-` = a base nao cobre o ano. Ultimo ano: SIM e SINASC 2025 (preliminar); Registro Civil 2024; WDI 2024; ONU 2025. O ano 2026 do DATASUS e parcial e fica de fora desta tabela.

| Base | 1964 | 1970 | 1980 | 1990 | 1994 | 2000 | 2010 | 2016 | 2020 | 2021 | 2024 | ultimo ano |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SIM obitos (ocorrencia) | - | - | 750.727 | 817.284 | 887.594 | 946.686 | 1.136.947 | 1.309.774 | 1.556.824 | 1.832.649 | 1.532.015 | 2025: 1.534.588 |
| SINASC nascidos (ocorrencia) | - | - | - | - | 2.571.571 | 3.206.761 | 2.861.868 | 2.857.800 | 2.730.145 | 2.677.101 | 2.389.325 | 2025: 2.456.688 |
| IBGE RC nascidos registrados no ano | - | - | - | 3.651.464 | 3.726.761 | 4.120.649 | 2.985.406 | 2.903.933 | 2.728.273 | 2.708.884 | 2.442.726 | 2024: 2.442.726 |
| IBGE RC nascidos ocorridos no ano | - | - | - | 2.419.927 | 2.472.325 | 2.613.764 | 2.747.373 | 2.793.995 | 2.673.913 | 2.630.703 | 2.370.945 | 2024: 2.370.945 |
| IBGE RC obitos registrados no ano | - | - | - | 862.951 | 929.549 | 949.293 | 1.132.701 | 1.288.856 | 1.524.949 | 1.802.487 | 1.516.381 | 2024: 1.516.381 |
| IBGE RC obitos ocorridos (1984-2002: ocorr.+reg. no ano) | - | - | - | 793.613 | 850.996 | 928.484 | 1.112.227 | 1.268.646 | 1.510.086 | 1.781.370 | 1.490.857 | 2024: 1.490.857 |
| WDI nascimentos estimados | 3.341.114 | 3.360.180 | 3.929.182 | 3.693.532 | 3.587.444 | 3.459.309 | 2.971.000 | 2.874.723 | 2.711.548 | 2.672.604 | 2.572.179 | 2024: 2.572.179 |
| WDI obitos estimados | 1.002.636 | 998.106 | 1.041.415 | 1.040.572 | 1.054.494 | 1.087.266 | 1.123.665 | 1.265.236 | 1.565.374 | 1.753.098 | 1.498.406 | 2024: 1.498.406 |
| ONU WPP nascimentos | 3.341.148 | 3.360.206 | 3.929.237 | 3.693.601 | 3.587.423 | 3.459.239 | 2.970.979 | 2.874.734 | 2.711.546 | 2.672.684 | 2.572.100 | 2025: 2.528.724 |
| ONU WPP obitos | 1.002.601 | 998.070 | 1.041.387 | 1.040.554 | 1.054.529 | 1.087.228 | 1.123.718 | 1.265.251 | 1.565.282 | 1.753.027 | 1.498.363 | 2025: 1.532.002 |

Notas de leitura: "registrados no ano" usa o lugar do registro de 2003 em diante (tab. 2679/2684) e a unica tabela disponivel antes disso; "ocorridos no ano" de obitos em 1984-2002 e "ocorridos e registrados no mesmo ano" (definicao mais estreita, ver `quebras.csv`). ONU 2024 e 2025 sao anos de projecao segundo a documentacao do WPP 2024, que nao verifiquei no arquivo.

## 2. Saldo (nascimentos menos obitos) e razao obitos/nascimentos, por base

Calculados em `derivado/saldo_e_razao_por_base.csv`. Cada linha usa so as duas series da mesma base, no mesmo ano. DATASUS: 1994-2025. IBGE RC: 1984-2024.

| Base | 1964 | 1970 | 1980 | 1990 | 1994 | 2000 | 2010 | 2016 | 2020 | 2021 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DATASUS (SIM obitos por ocorrencia x SINASC nascidos por ocorrencia) | - | - | - | - | 1.683.977 | 2.260.075 | 1.724.921 | 1.548.026 | 1.173.321 | 844.452 | 857.310 |
| IBGE Registro Civil, registrados no ano (nasc. registrados x obitos registrados, lugar do registro/ residencia) | - | - | - | 2.788.513 | 2.797.212 | 3.171.356 | 1.852.705 | 1.615.077 | 1.203.324 | 906.397 | 926.345 |
| IBGE Registro Civil, ocorridos no ano (nascidos ocorridos x obitos ocorridos; 1984-2002 obitos = ocorridos E registrados) | - | - | - | 1.626.314 | 1.621.329 | 1.685.280 | 1.635.146 | 1.525.349 | 1.163.827 | 849.333 | 880.088 |
| Banco Mundial WDI (derivado, estimativa) | 2.338.478 | 2.362.074 | 2.887.767 | 2.652.960 | 2.532.950 | 2.372.043 | 1.847.335 | 1.609.487 | 1.146.174 | 919.506 | 1.073.773 |
| ONU WPP 2024 (estimativa) | 2.338.547 | 2.362.136 | 2.887.850 | 2.653.047 | 2.532.894 | 2.372.011 | 1.847.261 | 1.609.483 | 1.146.264 | 919.657 | 1.073.737 |

Razao obitos / nascimentos:

| Base | 1964 | 1970 | 1980 | 1990 | 1994 | 2000 | 2010 | 2016 | 2020 | 2021 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DATASUS (SIM obitos por ocorrencia x SINASC nascidos por ocorrencia) | - | - | - | - | 0,3452 | 0,2952 | 0,3973 | 0,4583 | 0,5702 | 0,6846 | 0,6412 |
| IBGE Registro Civil, registrados no ano (nasc. registrados x obitos registrados, lugar do registro/ residencia) | - | - | - | 0,2363 | 0,2494 | 0,2304 | 0,3794 | 0,4438 | 0,5589 | 0,6654 | 0,6208 |
| IBGE Registro Civil, ocorridos no ano (nascidos ocorridos x obitos ocorridos; 1984-2002 obitos = ocorridos E registrados) | - | - | - | 0,3279 | 0,3442 | 0,3552 | 0,4048 | 0,4541 | 0,5647 | 0,6771 | 0,6288 |
| Banco Mundial WDI (derivado, estimativa) | 0,3001 | 0,297 | 0,265 | 0,2817 | 0,2939 | 0,3143 | 0,3782 | 0,4401 | 0,5773 | 0,656 | 0,5825 |
| ONU WPP 2024 (estimativa) | 0,3001 | 0,297 | 0,265 | 0,2817 | 0,294 | 0,3143 | 0,3782 | 0,4401 | 0,5773 | 0,6559 | 0,5825 |

## 3. Conferencia no mesmo ano: SIM x Registro Civil x ONU

Absolutos (`derivado/conferencia_mesmo_ano.csv`, 1979-2025 completo):

| Ano | SIM obitos | IBGE RC obitos ocorridos | IBGE RC obitos registrados | ONU WPP obitos | SINASC nascidos | IBGE RC nascidos ocorridos | IBGE RC nascidos registrados | ONU WPP nascimentos |
|---|---|---|---|---|---|---|---|---|
| 1990 | 817.284 | 793.613 | 862.951 | 1.040.554 | - | 2.419.927 | 3.651.464 | 3.693.601 |
| 2000 | 946.686 | 928.484 | 949.293 | 1.087.228 | 3.206.761 | 2.613.764 | 4.120.649 | 3.459.239 |
| 2010 | 1.136.947 | 1.112.227 | 1.132.701 | 1.123.718 | 2.861.868 | 2.747.373 | 2.985.406 | 2.970.979 |
| 2016 | 1.309.774 | 1.268.646 | 1.288.856 | 1.265.251 | 2.857.800 | 2.793.995 | 2.903.933 | 2.874.734 |
| 2020 | 1.556.824 | 1.510.086 | 1.524.949 | 1.565.282 | 2.730.145 | 2.673.913 | 2.728.273 | 2.711.546 |
| 2021 | 1.832.649 | 1.781.370 | 1.802.487 | 1.753.027 | 2.677.101 | 2.630.703 | 2.708.884 | 2.672.684 |
| 2022 | 1.544.266 | 1.501.233 | 1.524.731 | 1.585.581 | 2.561.922 | 2.537.078 | 2.621.015 | 2.640.391 |
| 2023 | 1.465.610 | 1.425.920 | 1.450.421 | 1.494.154 | 2.537.576 | 2.518.039 | 2.598.289 | 2.601.670 |
| 2024 | 1.532.015 | 1.490.857 | 1.516.381 | 1.498.363 | 2.389.325 | 2.370.945 | 2.442.726 | 2.572.100 |

Razao de cada base sobre a ONU WPP 2024 (1,00 = igual; a ONU e estimativa, nao verdade-terreno):

| Ano | SIM / ONU | RC obitos ocorridos / ONU | RC obitos registrados / ONU | SINASC / ONU | RC nascidos ocorridos / ONU | RC nascidos registrados / ONU |
|---|---|---|---|---|---|---|
| 1980 | 0,7209 | - | - | - | - | - |
| 1990 | 0,7854 | 0,7627 | 0,8293 | - | 0,6552 | 0,9886 |
| 2000 | 0,8707 | 0,854 | 0,8731 | 0,927 | 0,7556 | 1,1912 |
| 2010 | 1,0118 | 0,9898 | 1,008 | 0,9633 | 0,9247 | 1,0049 |
| 2016 | 1,0352 | 1,0027 | 1,0187 | 0,9941 | 0,9719 | 1,0102 |
| 2020 | 0,9946 | 0,9647 | 0,9742 | 1,0069 | 0,9861 | 1,0062 |
| 2021 | 1,0454 | 1,0162 | 1,0282 | 1,0017 | 0,9843 | 1,0135 |
| 2022 | 0,9739 | 0,9468 | 0,9616 | 0,9703 | 0,9609 | 0,9927 |
| 2023 | 0,9809 | 0,9543 | 0,9707 | 0,9754 | 0,9679 | 0,9987 |
| 2024 | 1,0225 | 0,995 | 1,012 | 0,9289 | 0,9218 | 0,9497 |

Leitura (so fatos medidos, sem causa):

- Obitos, 2010-2023: SIM, Registro Civil (ocorridos e registrados) e ONU ficam dentro de 6% da ONU em cada ano de 2010 a 2023 (SIM/ONU de 0,97 a 1,05; Registro Civil ocorridos/ONU de 0,95 a 1,02); o SIM fica acima do Registro Civil "ocorridos no ano" em todos os anos de 2003 a 2024 (conferido ano a ano; por exemplo 2024: 1.532.015 contra 1.490.857).
- Obitos, 1980-2000: SIM e Registro Civil ficam bem abaixo da ONU (SIM/ONU de 0,72 em 1980 a 0,87 em 2000); a razao sobe quase todo ano. Nao ha na nota do DATASUS texto sobre cobertura de obitos, entao nao atribuo a diferenca a cobertura: so registro que a razao e menor que 1.
- Nascimentos, 1994-2002: SINASC/ONU entre 0,72 (1994) e 0,93 (2002); nota do DATASUS: implantacao gradual, coleta nao cobria todos os municipios de algumas UF. Registro Civil "registrados no ano" fica acima da ONU em varios anos de 1996-2002 (1,18 em 1996; 1,19 em 2000); registro tardio e a leitura da propria nota do IBGE (gratuidade desde 1997), nao testada aqui.
- Nascimentos, 2010-2023: SINASC, Registro Civil e ONU ficam entre 0,92 e 1,03 da ONU em cada ano de 2010 a 2023. Em 2024 a ONU (projecao) esta 7,7% acima do SINASC e 5% acima do Registro Civil registrado: a diferenca aparece justo no primeiro ano de projecao do WPP 2024.
- 2021: SIM 1.832.649 obitos contra ONU 1.753.027 (+4,5%).
- Salto de definicao: Registro Civil nascidos ocorridos no ano 2002 = 2.584.543 e 2003 = 2.814.763 (+8,9%) enquanto SINASC cai 0,7% e a ONU cai 2,5% (calculado); e uma troca de tabela (706 para 2612), nao um fato demografico. Ver `quebras.csv`.

## 4. O que nao foi achado

| Item | Situacao |
|---|---|
| Registro Civil antes de 1984 (a ordem falava em 1974) | [NAO ACHADO] as tabelas SIDRA/API do IBGE comecam em 1984; o portal de series historicas (`seriesestatisticas.ibge.gov.br`) devolveu 403 do Cloudflare. Nao consultei outra fonte. |
| Pagina `sidra.ibge.gov.br/pesquisa/registro-civil`, `desctabapi.aspx` e paginas do portal `ibge.gov.br` | [NAO ACHADO] 403 do Cloudflare (sem navegador). Usei a API `apisidra.ibge.gov.br/values` e `servicodados.ibge.gov.br/api/v3/agregados/<tab>/metadados`, que responderam. Notas de rodape das tabelas SIDRA nao foram lidas. |
| Pagina de noticia da Agencia IBGE sobre sub-registro 2022 | [NAO ACHADO] HTML 403 (tentativa falhou, nada gravado no manifest). A nota tecnica sobre sub-registro foi obtida por outro caminho (secao 5). |
| Serie anual de estimativa de sub-registro de nascimentos e obitos do IBGE | [NAO ACHADO] como arquivo de dados. Em disco: a nota tecnica 01/2020 (texto) e dois decks de slides (2019 e 2020), onde os percentuais estao em graficos de imagem, nao extraidos. |
| Documentos "Consolidacao SIM 2011" e "Consolidacao SINASC 2011" citados nas notas do DATASUS | [NAO ACHADO] nao baixados; efeito da mudanca de formulario de 2011 nao medido. |
| Obitos 1964-1978 e nascimentos 1964-1993 registrados | [NAO ACHADO] sem base administrativa aberta na coleta; so estimativa (WDI/ONU). |
| Limite estimativa/projecao do WPP 2024 | Nao verificado no arquivo (so contem variante Medium). Uso a documentacao conhecida (estimativa ate 2023), marcada como nao verificada. |
| WDI 2025 | Valor nulo na API (ultima atualizacao do WDI 2026-10-08), logo fora do derivado. |

## 5. Nota sobre sub-registro e cobertura (IBGE, texto salvo)

Fonte: `bruto/ibge_rc_2018_publicacao.pdf` (o nome do arquivo e o da URL; o conteudo e a Nota Tecnica 01/2020, "Esclarecimentos sobre o Sub-Registro de Nascimentos", 9/12/2020). Trechos:

- "O sub-registro de nascimentos refere-se ao conjunto de nascimentos nao registrados no mesmo ano de sua ocorrencia ou no primeiro trimestre do ano subsequente."
- A gratuidade do registro de nascimento "passou a vigorar em 1997 (Art. 30 da Lei n. 9.534, de 10.12.1997)".
- "A convergencia do numero total de nascimentos das duas bases de dados, a partir de meados da decada de 2000, somada a reducao dos registros tardios, evidenciam, assim, a melhora da cobertura do registro de nascimentos."
- Pareamento de 2015: "98,3% dos nascimentos registrados nos Cartorios [...] foram encontrados na base do Ministerio da Saude, e que 96,9% das notificacoes do SINASC foram captadas na base do IBGE".
- "As estimativas de sub-registro levarao em consideracao os nascimentos ocorridos e nao registrados ate o 1o trimestre do ano subsequente [...] sem a incorporacao dos registros tardios."

Consequencia para os dados: "registrados no ano" contem registro tardio de anos anteriores; "ocorridos no ano" nao esta corrigido de sub-registro. Nenhum numero deste dossie e corrigido de sub-registro.

## 6. Desvios declarados

1. Registro Civil via API (SIDRA/agregados), nao via paginas `sidra.ibge.gov.br`, por causa do bloqueio. Alem das tabelas 2609 e 2679 pedidas, usei 192, 706, 2612, 363, 367, 2654, 2682, 2684 para fechar 1984-2024 em nascidos e obitos. Duas matrizes (2609, 2682) guardam ano de registro x ano de nascimento/ocorrencia; delas sai `derivado/ibge_rc_por_ano_de_ocorrencia_soma_matriz.csv` (soma dos registros 2003-2024; anos recentes incompletos).
2. Em `series/ibge_registro_civil.csv` o mesmo nome de indicador aparece em duas tabelas (ex.: `nascidos_vivos_registrados_no_ano` nas tab. 192 e 2609). As duas ficam em linhas separadas com a tabela na coluna `fonte`; o salto de 2002 para 2003 esta em `quebras.csv`. Quem usar a serie deve filtrar por `fonte`, nao empilhar sem olhar.
3. Tabelas 2609/2682 sao por residencia (excluem residentes no exterior); 2679/2684 sao por lugar do registro. As quatro estao na serie e diferem em 0,4% a 0,5% em 2003.
4. DATASUS: `obt09uf` e `obt10uf` sao bases distintas e nao foram emendadas; obitos por ocorrencia e por residencia sao identicos no total Brasil em todos os anos.
5. Os arquivos `bruto/sidra_meta_*.json` (metadados do agregado) foram gravados em gzip pela ferramenta de cadeia; o hash e do arquivo como esta (comprimido); leitura exige `gzip`.
6. `bruto/ibge_sub_registro_2022_a.pdf` e `_b.pdf` tem esse nome porque a busca os associou a "2022"; o conteudo sao decks do Registro Civil 2019 (9/12/2020) e 2020 (18/11/2021). Nomes mantidos para nao quebrar o hash.
7. Consulta TabNet exploratoria (1996-2026) rodei antes numa pasta de rascunho, sem hash; a registrada na cadeia usa os mesmos parametros (corpo do POST gravado ao lado: `bruto/*.post-body.txt`). Os valores batem.
8. O envio do POST usou `curl --data-binary` com o corpo em ISO-8859-1 (os nomes de campo do TabNet tem acentos), nao `--data-urlencode`.
9. Anos 2026 do DATASUS estao nas series com nota de incompleto e fora de todos os derivados.
10. ONU: `series/onu_wpp2024.csv` guarda so o Brasil, 1950-2026, em pessoas (original em milhares, x1000). O WPP e estimativa, nao registro, e nao foi tratado como verdade.

## 7. Arquivos

- `bruto/`: respostas originais (TabNet HTML, SIDRA JSON, WDI JSON, WPP csv.gz, PDFs, xlsx do FTP do IBGE de 2024: indice, nascidos vivos, obitos).
- `series/`: `datasus_sim_obitos.csv`, `datasus_sinasc_nascidos.csv`, `ibge_registro_civil.csv`, `wdi_banco_mundial.csv`, `onu_wpp2024.csv` (colunas: indicador,fonte,definicao_linha,ano,mes_ou_trimestre,valor,unidade,nota,vintage).
- `derivado/`: `wdi_nascimentos_obitos_estimados.csv` (formula declarada), `saldo_e_razao_por_base.csv`, `conferencia_mesmo_ano.csv`, `ibge_rc_por_ano_de_ocorrencia_soma_matriz.csv`.
- `quebras.csv`: 12 quebras (CID-9 para CID-10 em 1996 no SIM; cobertura do SIM e do SINASC; formularios de 2011; vintage preliminar; registro tardio e gratuidade; trocas de tabela do IBGE; sub-registro; vintage da ONU).
- `scripts/`: `tabnet_post.py`, `construir_series.py`, `conferencia.py`, `montar_quebras.py`, `tabela_anos_chave.py`, `montar_resultado.py`, `RESULTADO.template.md`.
- Os xlsx de 2024 do IBGE (FTP) foram baixados e hasheados, mas as series vem do SIDRA; os xlsx servem de conferencia (Tabela 1.1: linha Total 2.442.726 em 2024 = tab. SIDRA 2679; linha Brasil 2.421.079 = tab. 2609, conferido).

## 8. Verificacao da cadeia de hash

```text
42 lines; head 0dd2c99119bafeddf2842653a52a92e9777b98143ce66740bf7df2fcf8bd1aed; OK (codigo de saida 0)
```
