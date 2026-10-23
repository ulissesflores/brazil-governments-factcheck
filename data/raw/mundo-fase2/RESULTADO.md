# Coleta internacional, fase 2 (WDI, WIPO, ECI Atlas e OEC, UNESCO UIS), Brasil, anual

Coletado em 2026-10-20. Pré-registro: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/preregistro/PREREGISTRATION-FASE-2.md` (áreas "Ciência e tecnologia" e "Fiscal e vulnerabilidade", bloco P). Nada foi estimado nem interpolado: ano sem valor na fonte fica sem linha.

Pasta: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mundo-fase2/`

| Parte | Caminho |
|---|---|
| Brutos selados (69 arquivos) | `bruto/` + `manifest.jsonl` |
| Séries (CSV longo: indicador, fonte, definicao_linha, ano, mes_ou_trimestre, valor, unidade, nota, vintage) | `series/wdi_brasil.csv`, `series/wipo_brasil.csv`, `series/unesco_uis_brasil.csv`, `series/eci_atlas_brasil.csv`, `series/eci_oec_brasil.csv` |
| Derivados | `derivado/patentes_por_milhao.csv`, `derivado/conferencia_patentes.csv`, `derivado/reservas_wdi_pct_pib_wdi.csv`, `derivado/eci_atlas_revisoes_entre_versoes.csv`, `derivado/eci_atlas_v11_v12_todos_paises_media_dp.csv`, `derivado/eci_atlas_v12_vs_oec.csv` |
| Quebras (cabeçalho idêntico ao de `moeda-fiscal/quebras.csv`, 11 linhas) | `quebras.csv` |
| Scripts (stdlib, rodam sobre `bruto/`) | `scripts/construir_series.py`, `scripts/comparar_versoes_atlas.py`, `scripts/comparar_atlas_oec.py`, `scripts/escrever_quebras.py` |

## Vintages (versão e data de cada base)

| Base | Versão / data | Como foi obtida |
|---|---|---|
| Banco Mundial WDI | `lastupdated` 2026-10-08 (fonte 2); metadados longos da série via `/v2/sources/2/series/<código>/metadata` | API v2, 9 indicadores + metadados do indicador + metadados longos |
| WIPO IP Statistics Data Center | "Last updated: May 2026" (arquivo `bruto/wipo_last_updated_patent.txt`) | API pública do próprio site (`api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public/ips-search`), descoberta no código JS do site; sem sessão de navegador |
| UNESCO UIS (extra, fonte primária do WDI para P&D e pesquisadores) | versão `20260507-91260335`, release de fev/2026 | API pública `api.uis.unesco.org` |
| ECI Atlas (Harvard Growth Lab) | Dataverse doi:10.7910/DVN/XTAQMC, versão 12.0, publicada 2026-02-08; também as versões 3 a 11 | API de acesso do Dataverse |
| ECI OEC | API `api-v2.oec.world/tesseract`, baixada em 2026-10-20; **a API não declara versão** | cubos `legacy_complexity_eci_a` e `complexity_eci_a_hs{92,96,02,07,12,17,22}_hs{4,6}` |

## Valores por item (Brasil)

"—" = a fonte não tem valor nesse ano (ver "Não achado").

| Item | 1994 | 2002 | 2010 | 2016 | 2018 | 2022 | último ano (valor) | cobertura |
|---|---|---|---|---|---|---|---|---|
| P&D, % do PIB (WDI/UNESCO) | — | 1.010 | 1.160 | 1.196 | 1.150 | 1.189 | 2023: 1.194 | 2000-2023 |
| P&D, % do PIB (UIS direto) | — | 1.010 | 1.160 | 1.196 | 1.150 | 1.189 | 2023: 1.194 | 2000-2023 |
| Pesquisadores por milhão (WDI/UNESCO, FTE) | — | 403.2 | 696.1 | — | — | — | 2014: 903.2 | 2000-2014 |
| Pedidos de patente de residentes (WDI/WIPO) | 2,269 | 3,481 | 4,228 | 5,200 | 4,980 | 4,398 | 2024: 5,752 | 1980-2024 |
| Patentes de residentes por milhão (derivado) | 14.25 | 19.50 | 21.83 | 25.59 | 24.16 | 20.91 | 2024: 27.13 | 1980-2024 |
| Residentes por milhão (cálculo da WIPO) | 14.2 | 19.5 | 21.8 | 25.6 | 24.2 | 20.9 | 2024: 27.1 | 1990-2024 |
| Residentes por 100 bi US$ PIB PPC 2017 (WIPO) | 107.9 | 136.7 | 120.8 | 145.2 | 134.9 | 112.7 | 2024: 138.1 | 1990-2024 |
| PIB, US$ correntes (WDI) | 525.4 bi | 509.8 bi | 2,208.8 bi | 1,795.7 bi | 1,916.9 bi | 1,951.9 bi | 2025: 2,279.9 bi | 1960-2025 |
| População (WDI) | 159.3 mi | 178.5 mi | 193.7 mi | 203.2 mi | 206.1 mi | 210.3 mi | 2025: 212.8 mi | 1960-2025 |
| Comércio (X+M) % PIB (WDI) | 18.67 | 27.62 | 22.77 | 24.53 | 28.88 | 38.82 | 2025: 35.29 | 1960-2025 |
| Indústria de transformação % PIB (WDI) | 23.72 | 12.36 | 12.72 | 10.79 | 10.53 | 13.07 | 2025: 11.77 | 1960-2025 |
| Consumo do governo % PIB (WDI) | 17.87 | 19.81 | 19.02 | 20.38 | 19.90 | 18.40 | 2025: 19.13 | 1960-2025 |
| Reservas totais, US$ (WDI) | 38.8 bi | 37.8 bi | 288.6 bi | 365.0 bi | 374.7 bi | 324.7 bi | 2025: 358.5 bi | 1960-2025 |
| Reservas/PIB, %, ambos WDI (só conferência) | 7.39 | 7.42 | 13.06 | 20.33 | 19.55 | 16.63 | 2025: 15.72 | 1960-2025 |
| ECI Atlas v12, valor HS92 | — | 0.843 | 0.762 | 0.647 | 0.532 | 0.432 | 2024: 0.349 | 1995-2024 |
| ECI Atlas v12, posição HS92 | — | 34 | 38 | 43 | 49 | 52 | 2024: 59 | 1995-2024 |
| ECI Atlas v12, valor SITC | — | 0.697 | 0.602 | 0.412 | 0.363 | 0.169 | 2024: 0.114 | 1995-2024 |
| ECI Atlas v12, posição SITC | — | 39 | 44 | 53 | 55 | 69 | 2024: 78 | 1995-2024 |
| ECI Atlas v12, valor HS12 | — | — | — | 0.658 | 0.553 | 0.454 | 2024: 0.370 | 2012-2024 |
| ECI OEC HS92 HS6, valor | — | 0.632 | 0.651 | 0.629 | 0.616 | 0.374 | 2024: 0.322 | 1995-2024 |
| ECI OEC HS92 HS6, posição | — | 28 | 32 | 38 | 39 | 47 | 2024: 47 | 1995-2024 |
| ECI OEC HS92 HS4, valor | — | 0.583 | 0.466 | 0.304 | 0.345 | 0.042 | 2024: -0.054 | 1995-2024 |
| ECI OEC legado (SITC, 1964-2017), valor | 0.512 | 0.450 | 0.248 | 0.648 | — | — | 2017: 0.608 | 1964-2017 |

Observação: ECI da OEC existe também em HS96, HS02, HS07, HS12, HS17 e HS22 (valor e posição), todos em `series/eci_oec_brasil.csv`; só HS92 e o legado aparecem acima por serem os que cobrem 1994-2022.

### Patentes por milhão (derivado)

Fórmula: `patentes_por_milhao = IP.PAT.RESD / SP.POP.TOTL x 1e6` (WDI, mesmo ano); está também na coluna `definicao_linha` de `derivado/patentes_por_milhao.csv`. Conferência (`derivado/conferencia_patentes.csv`):

- `IP.PAT.RESD` do WDI é igual ao total de pedidos de residentes no INPI do IPSDC da WIPO (escritório BR x origem BR) em 45 de 45 anos (1980-2024).
- O derivado difere do "residentes por milhão" calculado pela WIPO em no máximo 0.049 em 35 anos comuns (1990-2024), isto é, só o arredondamento de 0.1 da WIPO. O derivado cobre 1980-1989, onde a WIPO não publica a razão.

## Não achado e por quê

| Item | Lacuna | Motivo |
|---|---|---|
| P&D % PIB | antes de 2000 (inclui 1994) | WDI e UIS começam em 2000 para o Brasil; a UIS foi consultada desde 1990 |
| Pesquisadores por milhão | antes de 2000 e de 2015 em diante (2016, 2018, 2022 e último ano) | WDI e UIS (release fev/2026) têm 2000-2014 e idêntico; o Brasil não tem registro depois de 2014 na fonte primária. Item do índice fica com cobertura parcial (§9) |
| ECI Atlas | antes de 1995 (inclui 1994) | o dataset começa em 1995 |
| ECI OEC por revisão do HS | antes de 1995 (HS92) e conforme a revisão (HS96 1998, HS02 2003, HS07 2008, HS12 2012, HS17 2018, HS22 2022) | cada cubo cobre desde o ano de início da revisão |
| ECI OEC legado | depois de 2017 | série descontinuada pela OEC; é a única com 1994 (0.512), mas é outra classificação (SITC-4 rev. 2, Feenstra et al. 2005 + Comtrade) e não se move com as séries HS (correlação -0.45 com HS92 HS6 em 1995-2017). Não está encadeada |
| WIPO "por milhão" oficial | antes de 1990 | a WIPO não publica a razão antes de 1990 (valor nulo); o derivado cobre |
| Pedidos por origem BR em qualquer escritório (WIPO indicador 1, relatório por origem) | baixado e selado (`bruto/wipo_ind10_rt13_ori-BR.json` e `.csv`), mas **não parseado** | cada célula traz 5 subvalores sem rótulo e em ordem variável por ano; sem rótulo não se sabe qual é qual. Conceito distinto de "residentes no INPI", que é o usado |
| Quebras com data declarada para o Brasil nos metadados do WDI | nenhuma encontrada | os metadados longos só trazem limitações genéricas (pesquisas de P&D, SCN 1993 ou 2008); registradas em `quebras.csv` com direção "desconhecida" |
| Série de comércio, indústria e consumo do governo: comparação com o IBGE | não feita aqui | fica com o agente do IBGE; aqui só a série WDI |
| Reservas/PIB para o índice | não calculada | o pré-registro manda usar reservas do BCB sobre o PIB em US$ do WDI; aqui estão o denominador (`wdi_pib_usd_correntes`) e uma razão de conferência 100% WDI |
| Atlas of Economic Complexity (site) | não coletado | os dados públicos do Atlas são o dataset do Dataverse; não usei o site (aplicação de página única) |

## Achados que mudam o uso do ECI

1. **O ECI do Atlas é revisado de uma versão para outra, e a v12 (fev/2026) reposiciona o Brasil.** Brasil, diferença v12 menos v11 positiva em 29 de 29 anos comuns (1995-2023): SITC +0.356 em média (máx +0.589); HS92 +0.297 (máx +0.556). Exemplos HS92: 2010 0.352 -> 0.762; 2022 0.017 -> 0.432. Média e desvio-padrão entre todos os países ficam ~0 e ~1 nas duas versões (`derivado/eci_atlas_v11_v12_todos_paises_media_dp.csv`), então não é deslocamento global de nível. O dataset não traz nota de versão (`versionNote` vazio). Antes da v12, as versões v7 a v11 tinham ECI do Brasil bem mais baixo (2010 HS92 0.352-0.388). Consequência para a pontuação: o ranking do Brasil e a tendência dependem da versão; a versão e a data devem ser impressas junto do item.
2. **Atlas e OEC discordam.** Atlas v12 HS92 contra OEC HS92 HS6: correlação 0.699, diferença média +0.071; contra OEC HS92 HS4: correlação 0.922, diferença média +0.256 (`derivado/eci_atlas_v12_vs_oec.csv`). Bases separadas, nunca misturadas.
3. **O nível do ECI muda com o nível de agregação:** OEC HS92 HS4 contra HS6, correlação 0.78 e diferença média -0.185 (HS4 menos HS6). Entre revisões consecutivas do HS no mesmo nível HS6, a correlação é 0.99.
4. **A posição (ranking) muda com a amostra de países**, não só com o valor: no Atlas v9 para v10 o valor do Brasil não muda e a posição HS92 de 2010 vai de 94 para 51. Usar o valor do ECI, não a posição, para qualquer comparação entre versões.

## Desvios declarados

1. O argumento `<arquivo-destino>` da cadeia foi passado **relativo à pasta** (`bruto/...`), não absoluto: é assim que `govfc.chain` grava o campo `arquivo` e como `verify` o localiza.
2. **9 arquivos da WIPO entraram com `add-local`, não `add`:** a API da WIPO responde 400 sem o cabeçalho `Accept-Language`, que `govfc.chain add` não envia. Baixei com `curl` (cabeçalho `Accept-Language: en`) e registrei na hora; para esses 9, o `timestamp_utc` do manifesto é o `mtime` do arquivo (segundos após o download) e o campo `nota` diz isso. Os outros 60 arquivos foram baixados pelo próprio `chain add`.
3. Além do pedido, coletei: UNESCO UIS direto (conferir WDI e achar dado de pesquisadores além de 2014; não achou), metadados longos do WDI (limitações e metodologia), as versões 3 a 11 do dataset do Atlas (medir revisão), a página da OEC que descreve a série legada, e o catálogo de cubos da API da OEC.
4. A API da OEC não declara versão; o `vintage` das linhas OEC é a data do download.
5. Scripts, derivados, séries e `quebras.csv` não estão no manifesto (são reproduzíveis a partir de `bruto/`, que está); `verify` cobre só `bruto/`.
6. O WDI traz 2025 para PIB, população, comércio, indústria, consumo do governo e reservas; não verifiquei se o Banco Mundial marca esses valores como preliminares.
7. Nada em `/tmp`: intermediários descartáveis ficaram no scratchpad da sessão.

## Cadeia de hash (saída de `verify`)

```text
$ cd /Users/ulissesflores/Developer/brazil-governments-factcheck && PYTHONPATH=code python3 -m govfc.chain verify /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/mundo-fase2
69 lines; head 9a46c3b9f2ba9452f4ed7c91da375b8a7e539d0f268252e810cf33a2529e7a4e; OK
```
