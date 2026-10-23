"""Gera RESULTADO.md a partir de janelas.csv, quebras.csv, series/*.csv e saida_medidas.json (sem rede).
Uso: python3 -I .../dominios-2/scripts/montar_resultado.py  (rode depois de construir.py)"""
import csv, json, statistics
from pathlib import Path

R = Path(__file__).resolve().parent.parent
jan = list(csv.DictReader((R / "janelas.csv").open(encoding="utf-8")))
med = json.load((R / "saida_medidas.json").open(encoding="utf-8"))
GOVS = []
for r in jan:
    if r["governo"] not in GOVS:
        GOVS.append(r["governo"])


def cel(ind, vint_prefix, gov, com_ini_fim=False):
    for r in jan:
        if r["indicador"] == ind and r["vintage"].startswith(vint_prefix) and r["governo"] == gov:
            if r["n_anos"] == "0":
                return "sem dado"
            if com_ini_fim:
                return f"{r['media']} (n={r['n_anos']}; {r['valor_inicial']} a {r['valor_final']})"
            return f"{r['media']} (n={r['n_anos']})"
    return "?"


def tabela(colunas, ini_fim=False):
    """colunas = [(titulo, indicador, prefixo_da_vintage)]"""
    h = "| governo | " + " | ".join(c[0] for c in colunas) + " |\n|---|" + "---|" * len(colunas) + "\n"
    for g in GOVS:
        h += f"| {g} | " + " | ".join(cel(c[1], c[2], g, ini_fim) for c in colunas) + " |\n"
    return h


def q_tabela():
    rows = list(csv.DictReader((R / "quebras.csv").open(encoding="utf-8")))
    h = "| indicador | data | tipo | direcao | efeito medido |\n|---|---|---|---|---|\n"
    for r in rows:
        h += f"| {r['indicador']} | {r['data_quebra']} | {r['tipo_de_quebra']} | {r['direcao_do_efeito']} | {r['efeito_medido'][:150].replace('|', '/')} |\n"
    return h


fhc_tab = "| segmento | media (n) | inicial | final |\n|---|---|---|---|\n" + "\n".join(
    f"| {lab} | {r['media']} (n={r['n_anos']}) | {r['valor_inicial']} | {r['valor_final']} |"
    for lab, ind in (("FHC, linha cheia (CRUZA CID-9/CID-10)", "seg_homic_taxa"), ("FHC so CID-10 (1996-2002)", "seg_homic_taxa|SIM-CID10"), ("FHC so CID-9 (1995)", "seg_homic_taxa|SIM-CID9"))
    for r in jan if r["indicador"] == ind and r["governo"] == "fhc" and r["vintage"].startswith("Ipeadata"))

txt = f"""# Dominios-2: saude, seguranca, alimentacao, ambiente e democracia

Dossie governos-do-brasil-economia. Coleta em 2026-10-19. Sem opiniao politica: so bruto, vintage e quebra.
Reproduzir (sem rede, confere sha256 do bruto contra o manifest de cada subpasta):
`python3 -I /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-2/scripts/construir.py` e depois `.../scripts/montar_resultado.py`.
Aquisicao (COM rede, nao rode por acaso): `scripts/coletar_tabnet.py` e `scripts/tabnet_lib.py`.

## 0. Achado e nao achado

1. Seis series entram como primarias (mortalidade materna, DTP3, taxa de homicidios, subalimentacao, desmatamento PRODES, democracia V-Dem). Duas NAO atingem 30 anos e ficam marcadas: subalimentacao FAO (2001-2024, 24 anos) e gasto publico em saude (2000-2023, 24 anos). Pela regra 4 do pre-registro, sao "sem serie comparavel de 30 anos": os numeros existem em `series/`, mas nao sustentam leitura de longo prazo.
2. Homicidios cruza uma quebra de classificacao no meio de um mandato: o mandato FHC (1995-2002) tem 1995 em CID-9 e 1996-2002 em CID-10. A tabela de janelas traz a linha cheia e uma linha por metodo (`seg_homic_taxa|SIM-CID10`, `|SIM-CID9`).
3. Nao ha ano duplamente codificado CID-9/CID-10 nos brutos: o efeito da troca de 1996 e `sem sobreposicao` (a propria nota do DATASUS diz que nao ha lista que compatibilize as duas). Nao estimei efeito.
4. Sobreposicoes reais encontradas e medidas: (a) WUENIC revisao 2025 x WDI: 2023 = 86 x 90, 2024 = 90 x 91, demais 43 anos iguais; (b) subalimentacao SOFI 2015 x FAOSTAT 2026: 2000-02 = 11,2 x 10,5; (c) PRODES 2024 estimativa x consolidado: 6.288 x 6.518 (+3,66%); (d) populacao Censo x Projecao rev. 2024: de -0,4% a +3,8% no denominador; (e) homicidios Ipeadata x TabNet: igual de 1996 a 2024 (exceto 2022: -1), diferenca de -61 a +120 obitos/ano em 1979-95.
5. Nao encontrei, nem tentei estimar: serie de cobertura do SIM; gasto publico em saude antes de 2000; PRODES antes de 1988 (Castelo a Figueiredo ficam sem dado); V-Dem v15 e Atlas da Violencia como arquivos proprios (so o Ipeadata, que reproduz o SIM).

## 1. Regra de atribuicao ano -> governo (unica, mecanica)

Cada observacao anual e atribuida ao governo que ocupa MAIS DIAS dentro do intervalo da observacao (ano-calendario; para o PRODES, 1 ago do ano anterior a 31 jul). Consequencias: a Junta Militar (2 meses) nunca fica com ano (n=0); anos de transicao (1990, 1992, 1995, 2003, 2011, 2016...) vao ao governo majoritario. Para o PRODES existe tambem a atribuicao alternativa pelo ano-calendario de inicio (ago-dez): linhas `amb_prodes_amz|atribuicao-alternativa:ano-calendario-de-inicio` em `janelas.csv`. Medias sao simples (sem ponderar). Termino do Lula 3 = 2026-10-19 (mandatos.csv).

## 2. Cadeia de hash (resultado de `manifest_tool.py verify`)

| pasta | resultado | observacao |
|---|---|---|
| dominios-2/ (raiz) | REPROVADO | seq 1 e o JSON do Ipeadata (AVIOL12_HOMIC) de 64.653.700 bytes, baixado por engano sem filtro (o filtro OData `$filter=NIVNOME` foi ignorado pelo servidor); excede o teto de 25 MB, entao foi APAGADO. A linha (sha256 cd8db235c218c0b79b6435cb22e8f32e723b0f3fb5b3d7dc70354ee1c8cda017) fica na cadeia. Sobrevive so o derivado `Brasil` (46 linhas, 6.440 bytes), registrado na raiz (seq 2) e copiado em seguranca/. Recriar o bruto: URL na linha seq 1. |
| saude/ | OK | |
| alimentacao/ | REPROVADO | seq 5 e um download TRUNCADO do SOFI 2015 (597.999 bytes, timeout); o arquivo foi baixado de novo (seq 6, 2.506.724 bytes) sob o mesmo nome e a ferramenta compara cada linha ao arquivo atual. A linha superada nao pode passar: comportamento da ferramenta, nao editei o manifest. |
| seguranca/ | OK | inclui 2 brutos de qualidade ruim mantidos por rastreabilidade: `portaria_svs_116_2009.pdf` e um HTML de erro do MPBA (a copia correta e `portaria_svs_116_2009_es.pdf`) |
| seguranca_unodc/, democracia/ | OK | |
| ambiente/ | OK | 2 arquivos `inpe_nt_prodes_2021/2022_consolidada.pdf` sao HTML (gov.br nao serviu o PDF); mantidos por rastreabilidade, nao usados |

Brutos grandes NAO baixados: V-Dem zip v16 https://v-dem.net/media/datasets/V-Dem-CY-FullOthers-v16_csv.zip (26.867.425 bytes) e v15 https://v-dem.net/media/datasets/V-Dem-CY-FullOthers-v15_csv.zip (25.953.685 bytes): acima de 25 MB; usei a redistribuicao OWID (CC BY 4.0, v16, DOI 10.23696/vdemds26; o arquivo traz todos os paises). Ipeadata AVIOL12_HOMIC completo (64,65 MB): so o derivado Brasil. Ipeadata AVIOL12_THOMIC (taxa do Ipea) NAO baixado (mesmo problema de tamanho; o comentario do metadado dessa serie descreve codigos de suicidio e esta corrompido): a taxa foi calculada aqui. FAOSTAT zip: 2,2 MB baixado; o CSV de 52 MB extraido foi apagado depois de gerar o derivado Brasil.

## 3. Saude

Fontes: mortalidade materna = estimativa MODELADA (OMS/UNICEF/UNFPA/Banco Mundial/ONU), via WDI 2026-10-08; DTP3 = WUENIC revisao 2025 (export oficial da OMS, 2026-10-19); gasto publico = OMS GHED via WDI. Mortalidade infantil ja existe em `social/series/mortinf.csv` (nao refeita).

{tabela([("mort. materna modelada (por 100 mil nv)", "sau_mortmat", "WDI"), ("DTP3 WUENIC 2025 (%)", "sau_dtp3", "WUENIC 2025"), ("gasto publico saude (% PIB)", "sau_gasto_pub_pib", "WDI")])}
Leitura do que existe: mortalidade materna modelada comeca em 1985 e DTP3 em 1980; antes disso, sem dado. Gasto publico: so 2000-2023 (FHC n=3, Lula 3 n=1). `sau_mortmat_nacional` (1995-2022) esta em `series/sau.csv` como sensibilidade; em 2022 a estimativa nacional (57,7) e a modelada (104) divergem (razao 0,55); em 1999 a razao e 1,23 e em 2000, 1,06. Esses saltos nao tem explicacao declarada nos arquivos baixados e nao sao tratados como quebra.
DTP3: a cobertura administrativa menos a WUENIC tem media absoluta de 1,4 pp (1980-94), 1,6 pp (1995-2011) e 0,1 pp (2012-2025).

## 4. Seguranca (homicidios)

Definicao primaria: homicidios (Ipeadata AVIOL12_HOMIC, obitos por residencia, MS/SIM): CID-9 E960-E978 e E990-E999 (1979-95); CID-10 X85-Y09 e Y35 (1996-). Taxa = contagem / populacao projetada IBGE rev. 2024 (1o jul), um unico vintage de denominador 1980-2024 (1979 so tem contagem). Dado final do SIM ate 2024 (extracao DATASUS 02/12/2025). Sensibilidades: UNODC via WDI (1990-2023; diferenca media de -0,83 por 100 mil, em modulo 0,84), homicidios + intencao indeterminada.

{tabela([("taxa por 100 mil (primaria)", "seg_homic_taxa", "Ipeadata"), ("homic. + intencao indeterminada", "seg_homic_indet_taxa", "Ipeadata"), ("UNODC/WDI", "seg_homic_taxa_unodc", "WDI")])}
Comparacao dentro de um unico metodo para o mandato que cruza a quebra:

{fhc_tab}

### 4.1 O que mudou no SIM (cada item em `quebras.csv`, com data, trecho e URL)

| item | data | fonte primaria | efeito medido |
|---|---|---|---|
| CID-9 -> CID-10 | 1996-01-01 | nota DATASUS Mortalidade_Geral_1996_2012.pdf | sem sobreposicao (nenhum ano em duas revisoes). Contagens vizinhas, so descritivas: 1994 {med['cid_1995_1996'][2]}, 1995 {med['cid_1995_1996'][0]}, 1996 {med['cid_1995_1996'][1]}, 1997 {med['cid_1995_1996'][3]} |
| causa de intencao indeterminada (E980-E989 -> Y10-Y34) | 1996 | tabelas TabNet | sem sobreposicao |
| intervencao legal dentro de "homicidios" (rotulo do Ipeadata) | 1996 | metadado Ipeadata | sem sobreposicao; intervencoes legais no CID-10: 35 (1996), 121 (2002), 491 (2003), 2.644 (2024) |
| causa mal definida (cap. XVI -> XVIII) | 1996 | nota DATASUS | sem sobreposicao; proporcao de mal definidas: 1979 {med['maldef']['1979']:.1f}%, 1995 {med['maldef']['1995']:.1f}%, 1996 {med['maldef']['1996']:.1f}%, 2010 {med['maldef']['2010']:.1f}%, 2024 {med['maldef']['2024']:.1f}% |
| fluxo/periodicidade de envio (cobertura) | 2009-02-11 | Portaria SVS 116/2009 | sem sobreposicao; serie de cobertura do SIM nao baixada |
| formulario da DO | 2011 | nota DATASUS | sem sobreposicao |
| CID-10 v2019 no SIM | 2025-01 | nota DATASUS | fora da serie (final ate 2024) |
| denominador (Censo x projecao) | 2022 | Ipeadata POPTOT x POP_PROJE | ver quebras.csv (taxa com projecao x taxa com Censo: -0,4% em 1980, +1,5% em 1991, +2,8% em 2000, +2,1% em 2010, +3,8% em 2022 no denominador) |

### 4.2 Descontinuidades vistas nos dados SEM quebra declarada pela fonte (nao entram em quebras.csv: a tabela exige quebra declarada ou de vintage)

- 1989 -> 1990 (CID-9): homicidios {med['indet_saltos']['1989->1990'][2]} -> {med['indet_saltos']['1989->1990'][3]} (+{med['indet_saltos']['1989->1990'][3]-med['indet_saltos']['1989->1990'][2]}); "lesoes em que se ignora acidente ou intencao" {med['indet_saltos']['1989->1990'][4]} -> {med['indet_saltos']['1989->1990'][5]} ({med['indet_saltos']['1989->1990'][5]-med['indet_saltos']['1989->1990'][4]}); soma {med['indet_saltos']['1989->1990'][0]} -> {med['indet_saltos']['1989->1990'][1]}. Os brutos nao separam reclassificacao de mudanca real.
- 2018 -> 2019 (CID-10): agressoes {med['indet_saltos']['2018->2019'][2]} -> {med['indet_saltos']['2018->2019'][3]} ({med['indet_saltos']['2018->2019'][3]-med['indet_saltos']['2018->2019'][2]}); intencao indeterminada {med['indet_saltos']['2018->2019'][4]} -> {med['indet_saltos']['2018->2019'][5]} (+{med['indet_saltos']['2018->2019'][5]-med['indet_saltos']['2018->2019'][4]}); soma {med['indet_saltos']['2018->2019'][0]} -> {med['indet_saltos']['2018->2019'][1]}. Mesma limitacao.
- 2002 -> 2003: intervencoes legais 121 -> 491 (+306%).

## 5. Alimentacao

FAO, prevalencia de subalimentacao, media trienal atribuida ao ano central (2000-02 -> 2001). Vintage FAOSTAT 2026-07-10. Valores publicados como "<2,5" (9 de 24 medias trienais) entram como 2,5 (teto): as medias de Dilma e Temer sao, portanto, limite superior. SOFI 2015 (1990-92: 14,8; 2000-02: 11,2; demais "<5,0") fica como outra vintage em `series/ali.csv`.

{tabela([("subalimentacao % (FAOSTAT 2026)", "ali_pou", "FAOSTAT"), ("SOFI 2015 (teto 5,0 nos censurados)", "ali_pou", "SOFI 2015")])}
Governos ate 1999: sem dado na vintage atual (a unica cifra anterior, 14,8% em 1990-92, e do SOFI 2015).

## 6. Ambiente (desmatamento da Amazonia Legal, PRODES)

Taxa consolidada, soma dos 9 estados, 1988-2025 (testes: 1988 = 21.050; 2022 = 11.594; 2024 = 6.518; 2025 = 5.731). A estimativa de 2026 (3.335 km2, 271 de 516 tiles, nota de 2026-10-16) e linha a parte e nao entra na media. 1993 e 1994 tem valor identico (14.896). Quebras de metodo do PRODES (analogico, digital, TerraAmazon, ajuste de mascara 2015, poligonos 2008-12 em 2017) estao em `quebras.csv` sem efeito mensurado.

{tabela([("PRODES km2/ano (atribuicao: maioria dos dias do ano ago-jul)", "amb_prodes_amz", "PRODES TerraBrasilis"), ("atribuicao alternativa (ano-calendario de inicio)", "amb_prodes_amz|atribuicao-alternativa:ano-calendario-de-inicio", "PRODES TerraBrasilis")])}
Lula 3 inclui a estimativa de 2026 como linha separada: 3.335 km2 (n=1, vintage "PRODES 2026 estimativa"); a estimativa de 2024 (6.288) e a consolidada (6.518) estao guardadas como duas vintages do mesmo ano.

## 7. Democracia

V-Dem v2x_polyarchy (v16, via OWID). Sensibilidades: Polity5 polity2 (ate 2018) e Freedom House (direitos politicos e liberdades civis, escala 1 = melhor; 1981-89 usam periodos nao-calendario e ficaram fora; edicao 2024; licenca nao verificada, so notas de Brasil).

{tabela([("V-Dem polyarchy 0-1", "dem_polyarchy", "V-Dem"), ("Polity5 polity2 (-10..10)", "dem_polity2", "Polity5"), ("FH direitos politicos (1 melhor)", "dem_fh_direitos_politicos", "Freedom")])}
## 8. Quebras (resumo; `quebras.csv` tem trecho citado, URL e como a direcao foi determinada)

{q_tabela()}
Tipos: `mudanca_de_regra` = a norma/classificacao alterou o que se mede; `metodo_estatistico` = mudanca de metodo de medir/estimar; `revisao_de_vintage` = a mesma coisa medida de novo e publicada com outro valor. A direcao so e "eleva"/"reduz" quando segue de aritmetica sobre dados baixados; nas demais e "desconhecida" ou "ambigua".

## 9. Limites desta entrega

- Nao medi cobertura do SIM, nem subnotificacao de homicidios; so proxies descritivos (mal definidas, intencao indeterminada).
- `janelas.csv` usa mandatos (mandatos.csv); as janelas impressas no infografico nao foram tratadas aqui.
- Nao ha dado de saude/seguranca/alimentacao/ambiente para Castelo, Costa e Silva, Junta, Medici e Geisel (Figueiredo so tem homicidios e DTP3; mortalidade materna comeca no Sarney; PRODES comeca no Sarney). Democracia (V-Dem, Polity) cobre todos exceto a Junta.
- Atlas da Violencia e Freedom House/Polity: licenca/uso nao auditados; nada foi reproduzido alem de series de Brasil.
"""
(R / "RESULTADO.md").write_text(txt, encoding="utf-8")
print("RESULTADO.md", len(txt))
