"""Curated layer: every collected series in ONE long table, with the vintage on every row.

``data/curated/observations.csv`` has one row per (series, vintage, period). Values are the
values the source published (or the deterministic aggregation of published values, flagged in
``natureza``); nothing here is an estimate. A revised value is a NEW row with another vintage:
rows are only ever added, never overwritten.

``natureza`` is one of ``publicado`` (as the source published it), ``derivado_deterministico``
(compounding, annual mean, ratio to GDP, unit conversion: reproducible arithmetic on published
values) or ``modelo_de_terceiro`` (a model estimate published by the source, e.g. maternal
mortality of the UN inter-agency group).

``dependente_de_regra`` is ``sim`` when a policy or norm, not only the measurement, can move the
number (school failure under continuous progression, poverty under a redefined line).
"""

import csv
import json
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw"
CURADO = RAIZ / "data" / "curated"
CAMPOS = [
    "indicador",
    "serie",
    "dominio",
    "periodo",
    "valor",
    "unidade",
    "vintage",
    "natureza",
    "dependente_de_regra",
    "nota",
    "origem",
]

#: indicator -> (domain, name pt-BR, name en, rule-dependent). Extend, never reorder.
CATALOGO = {
    "pib_var_real": ("economia", "PIB, variação real anual", "GDP, annual real growth", "nao"),
    "pib_pc_var_real": (
        "economia",
        "PIB per capita, variação real anual",
        "GDP per capita, annual real growth",
        "nao",
    ),
    "inflacao_mensal": ("economia", "Inflação mensal", "Monthly inflation", "nao"),
    "igpdi_indice": ("economia", "IGP-DI, número-índice", "IGP-DI, index level", "nao"),
    "desemprego": ("trabalho", "Taxa de desemprego", "Unemployment rate", "nao"),
    "salmin_real": ("trabalho", "Salário mínimo real", "Real minimum wage", "sim"),
    "pobreza": ("renda", "Taxa de pobreza", "Poverty rate", "sim"),
    "gini": ("renda", "Índice de Gini", "Gini index", "nao"),
    "expvida": ("saude", "Expectativa de vida ao nascer", "Life expectancy at birth", "nao"),
    "mortinf": ("saude", "Mortalidade infantil", "Infant mortality", "nao"),
    "ali_pou": (
        "alimentacao",
        "Prevalência de subalimentação",
        "Prevalence of undernourishment",
        "nao",
    ),
    "amb_prodes_amz": (
        "ambiente",
        "Desmatamento da Amazônia (PRODES)",
        "Amazon deforestation (PRODES)",
        "sim",
    ),
    "dem_polyarchy": (
        "democracia",
        "Democracia eleitoral (V-Dem)",
        "Electoral democracy (V-Dem)",
        "nao",
    ),
    "dem_polity2": ("democracia", "Polity2", "Polity2", "nao"),
    "dem_fh_direitos_politicos": (
        "democracia",
        "Direitos políticos (Freedom House)",
        "Political rights (Freedom House)",
        "nao",
    ),
    "dem_fh_liberdades_civis": (
        "democracia",
        "Liberdades civis (Freedom House)",
        "Civil liberties (Freedom House)",
        "nao",
    ),
    "sau_mortmat": (
        "saude",
        "Mortalidade materna (modelo OMS/ONU)",
        "Maternal mortality (UN model)",
        "nao",
    ),
    "sau_mortmat_nacional": (
        "saude",
        "Mortalidade materna (estatística nacional)",
        "Maternal mortality (national statistics)",
        "nao",
    ),
    "sau_dtp3": ("saude", "Cobertura vacinal DTP3", "DTP3 vaccination coverage", "nao"),
    "sau_dtp3_admin": (
        "saude",
        "Cobertura vacinal DTP3 (administrativa)",
        "DTP3 coverage (administrative)",
        "nao",
    ),
    "sau_gasto_pub_pib": (
        "saude",
        "Gasto público em saúde, % do PIB",
        "Public health spending, % of GDP",
        "nao",
    ),
    "seg_homic_n": ("seguranca", "Homicídios, número de óbitos", "Homicides, deaths", "sim"),
    "seg_homic_taxa": (
        "seguranca",
        "Taxa de homicídios por 100 mil",
        "Homicide rate per 100k",
        "sim",
    ),
    "seg_homic_taxa_unodc": (
        "seguranca",
        "Taxa de homicídios (UNODC)",
        "Homicide rate (UNODC)",
        "sim",
    ),
    "seg_homic_indet_taxa": (
        "seguranca",
        "Homicídios com causa indeterminada, taxa",
        "Deaths of undetermined intent, rate",
        "sim",
    ),
    "seg_indet_pct": (
        "seguranca",
        "Óbitos de intenção indeterminada, %",
        "Undetermined-intent deaths, %",
        "sim",
    ),
    "seg_maldef_pct": (
        "seguranca",
        "Óbitos por causa mal definida, %",
        "Ill-defined causes of death, %",
        "sim",
    ),
    "agregado_pib": (
        "moeda",
        "Agregados monetários, % do PIB (média de 12 saldos mensais)",
        "Monetary aggregates, % of GDP (mean of 12 month-end balances)",
        "sim",
    ),
    "senhoriagem_pib": (
        "moeda",
        "Senhoriagem e imposto inflacionário, % do PIB",
        "Seigniorage and inflation tax, % of GDP",
        "nao",
    ),
    "selic_over": ("moeda", "Taxa Selic over, média anual", "Selic overnight rate, annual", "nao"),
    "juro_real": ("moeda", "Juro real ex-post", "Ex-post real interest rate", "nao"),
    "cambio": (
        "externo",
        "Câmbio, R$ por US$ no fim do ano",
        "Exchange rate, BRL per USD at year end",
        "nao",
    ),
    "reservas_usd": (
        "externo",
        "Reservas internacionais, US$ milhões",
        "International reserves, USD million",
        "nao",
    ),
    "divida_pib": ("fiscal", "Dívida pública, % do PIB", "Public debt, % of GDP", "sim"),
    "primario_pib": (
        "fiscal",
        "Resultado primário, % do PIB (positivo = superávit)",
        "Primary balance, % of GDP (positive = surplus)",
        "sim",
    ),
    "renda_decil": (
        "renda",
        "Renda per capita por decil, US$ PPC por dia",
        "Per-capita income by decile, PPP USD per day",
        "nao",
    ),
    "bf_limiar_real": (
        "assistencia",
        "Linha de elegibilidade do Bolsa Família, R$ de set/2026",
        "Bolsa Família eligibility line, BRL of Sep 2026",
        "sim",
    ),
    "excesso_monetario": (
        "moeda",
        "Excesso monetário (crescimento da moeda menos PIB real)",
        "Monetary overhang (money growth minus real GDP growth)",
        "nao",
    ),
    "bf_linha_relativa": (
        "assistencia",
        "Linha do Bolsa Família em fração de outras linhas",
        "Bolsa Família line as a fraction of other lines",
        "sim",
    ),
    "ass_bpc_idade_minima": (
        "assistencia",
        "BPC, idade mínima do idoso",
        "BPC, minimum age of the elderly",
        "sim",
    ),
    "ass_bpc_limiar_meio_sm_real": (
        "assistencia",
        "BPC, limiar de 1/2 salário mínimo, R$ de dez/2025",
        "BPC, 1/2 minimum-wage threshold, BRL of Dec 2025",
        "sim",
    ),
    "ass_bpc_limiar_quarto_sm_real": (
        "assistencia",
        "BPC, limiar de 1/4 do salário mínimo, R$ de dez/2025",
        "BPC, 1/4 minimum-wage threshold, BRL of Dec 2025",
        "sim",
    ),
    "ass_bpc_por_mil_hab": (
        "assistencia",
        "BPC, beneficiários por mil habitantes",
        "BPC, beneficiaries per 1,000 inhabitants",
        "sim",
    ),
    "ass_pbf_familias_por_mil_hab": (
        "assistencia",
        "Bolsa Família, famílias por mil habitantes",
        "Bolsa Família, families per 1,000 inhabitants",
        "sim",
    ),
    "ass_pbf_limiar_extrema_pobreza_real": (
        "assistencia",
        "Bolsa Família, linha de extrema pobreza, R$ de dez/2025",
        "Bolsa Família, extreme-poverty line, BRL of Dec 2025",
        "sim",
    ),
    "ass_pbf_limiar_pobreza_real": (
        "assistencia",
        "Bolsa Família, linha de pobreza, R$ de dez/2025",
        "Bolsa Família, poverty line, BRL of Dec 2025",
        "sim",
    ),
    "edu_alfabetizacao_adultos_wdi": (
        "educacao",
        "Alfabetização de adultos (Banco Mundial/UIS)",
        "Adult literacy (World Bank/UIS)",
        "nao",
    ),
    "edu_analfab15": (
        "educacao",
        "Analfabetismo, 15 anos ou mais",
        "Illiteracy, age 15 and over",
        "nao",
    ),
    "edu_anos_estudo_15mais": (
        "educacao",
        "Anos médios de estudo, 15 anos ou mais",
        "Mean years of schooling, 15 and over",
        "nao",
    ),
    "edu_anos_estudo_25mais": (
        "educacao",
        "Anos médios de estudo, 25 anos ou mais",
        "Mean years of schooling, 25 and over",
        "nao",
    ),
    "edu_gasto_publico_pib": (
        "educacao",
        "Gasto público em educação, % do PIB",
        "Public education spending, % of GDP",
        "sim",
    ),
    "edu_persistencia_ultima_serie_primario": (
        "educacao",
        "Persistência até a última série do primário",
        "Persistence to the last grade of primary",
        "sim",
    ),
    "edu_repetentes_primario_pct": (
        "educacao",
        "Repetentes no primário, %",
        "Repeaters in primary school, %",
        "sim",
    ),
    "edu_saeb_LP_EF_5ano_4serie": (
        "educacao",
        "Saeb, português, 5º ano (4ª série)",
        "Saeb, Portuguese, 5th grade",
        "nao",
    ),
    "edu_saeb_LP_EF_9ano_8serie": (
        "educacao",
        "Saeb, português, 9º ano (8ª série)",
        "Saeb, Portuguese, 9th grade",
        "nao",
    ),
    "edu_saeb_LP_EM_3serie": (
        "educacao",
        "Saeb, português, 3ª série do ensino médio",
        "Saeb, Portuguese, 12th grade",
        "nao",
    ),
    "edu_saeb_MT_EF_5ano_4serie": (
        "educacao",
        "Saeb, matemática, 5º ano (4ª série)",
        "Saeb, mathematics, 5th grade",
        "nao",
    ),
    "edu_saeb_MT_EF_9ano_8serie": (
        "educacao",
        "Saeb, matemática, 9º ano (8ª série)",
        "Saeb, mathematics, 9th grade",
        "nao",
    ),
    "edu_saeb_MT_EM_3serie": (
        "educacao",
        "Saeb, matemática, 3ª série do ensino médio",
        "Saeb, mathematics, 12th grade",
        "nao",
    ),
    "mat_prenatal7": (
        "saude",
        "Nascidos com 7 ou mais consultas de pré-natal, %",
        "Births with 7+ prenatal visits, %",
        "nao",
    ),
    "mat_prenatal_ignorado": (
        "saude",
        "Pré-natal ignorado, %",
        "Prenatal visits unknown, %",
        "nao",
    ),
    "mat_prenatal_nenhuma": (
        "saude",
        "Nascidos sem consulta de pré-natal, %",
        "Births with no prenatal visit, %",
        "nao",
    ),
    "mor_agua_encanada_pop": (
        "moradia",
        "Água encanada, % da população",
        "Piped water, % of population",
        "nao",
    ),
    "mor_agua_rede_geral": (
        "moradia",
        "Água por rede geral, % dos domicílios",
        "Water from the public network, % of households",
        "nao",
    ),
    "mor_esgoto_adequado": (
        "moradia",
        "Esgoto adequado, % dos domicílios",
        "Adequate sewage, % of households",
        "nao",
    ),
    "mor_esgoto_rede": (
        "moradia",
        "Esgoto por rede, % dos domicílios",
        "Sewage by network, % of households",
        "nao",
    ),
    "mor_esgoto_rede_ou_fossa_ligada": (
        "moradia",
        "Esgoto por rede ou fossa ligada, %",
        "Sewage by network or connected septic tank, %",
        "nao",
    ),
    "mor_luz": (
        "moradia",
        "Energia elétrica, % dos domicílios",
        "Electricity, % of households",
        "nao",
    ),
    "pre_rgps_arrecadacao_liquida_pib": (
        "previdencia",
        "RGPS, arrecadação líquida, % do PIB",
        "RGPS, net revenue, % of GDP",
        "sim",
    ),
    "pre_rgps_beneficios_pib": (
        "previdencia",
        "RGPS, benefícios, % do PIB",
        "RGPS, benefits, % of GDP",
        "sim",
    ),
    "pre_rgps_resultado_pib": (
        "previdencia",
        "RGPS, resultado, % do PIB",
        "RGPS, balance, % of GDP",
        "sim",
    ),
    "tbl_informalidade": (
        "trabalho",
        "Informalidade, PNAD (1992-2014)",
        "Informality, PNAD (1992-2014)",
        "sim",
    ),
    "tbl_informalidade_ibge": (
        "trabalho",
        "Informalidade, PNADC (2016-2025)",
        "Informality, PNADC (2016-2025)",
        "sim",
    ),
    "tbl_renda_trabalho_real": (
        "trabalho",
        "Renda real do trabalho, R$ de dez/2025",
        "Real labour income, BRL of Dec 2025",
        "nao",
    ),
}

#: wide file -> (period column, {column: (indicator, series label, unit, nature, vintage, note)})
LARGAS = [
    (
        "economia-real/saida-pib-anual-1948-2025.csv",
        "ano",
        {
            "pib_real_var_pct_SCN10_PIBG10": (
                "pib_var_real",
                "IBGE/SCN via Ipeadata SCN10_PIBG10",
                "%",
                "publicado",
                "Ipeadata SCN10_PIBG10, atualizado 2026-07-10",
                "",
            ),
            "pib_percapita_var_pct_final": (
                "pib_pc_var_real",
                "IBGE (oficial 1996-2023) ou derivado com população",
                "%",
                "derivado_deterministico",
                "SIDRA 6784 v9814 e Ipeadata DEPIS_POP, baixados 2026-10-19",
                "",
            ),
            "sidra_9810": (
                "pib_var_real",
                "IBGE SIDRA 6784 v9810",
                "%",
                "publicado",
                "SIDRA 6784, baixado 2026-10-19",
                "",
            ),
            "sidra_9814": (
                "pib_pc_var_real",
                "IBGE SIDRA 6784 v9814",
                "%",
                "publicado",
                "SIDRA 6784, baixado 2026-10-19",
                "",
            ),
            "sgs_7326": (
                "pib_var_real",
                "BCB SGS 7326 (nome da série não confirmado na fonte)",
                "%",
                "publicado",
                "BCB SGS 7326, baixado 2026-10-19",
                "",
            ),
        },
    ),
    (
        "economia-real/saida-desemprego-anual.csv",
        "ano",
        {
            "PME_antiga_15mais_30d_6RMs": (
                "desemprego",
                "PME antiga, 6 RMs, 15+, referência de 30 dias",
                "%",
                "derivado_deterministico",
                "Ipeadata PME12_TDA12, atualizado 2003-02-18",
                "média anual de séries mensais; só vale com 12 meses",
            ),
            "PME_nova_10mais_semana_6RMs": (
                "desemprego",
                "PME nova, 6 RMs, 10+, semana de referência",
                "%",
                "derivado_deterministico",
                "Ipeadata PAN12_TD12, atualizado 2016-02-02",
                "média anual de séries mensais; só vale com 12 meses",
            ),
            "PNAD_Dese_Pnad_Brasil": (
                "desemprego",
                "PNAD anual, Brasil, 10+, semana de referência",
                "%",
                "publicado",
                "Ipeadata Dese_Pnad, atualizado 2015-11-17",
                "",
            ),
            "PNAD_DISOC_DESE_Brasil": (
                "desemprego",
                "PNAD anual (microdados, Ipea/Disoc)",
                "%",
                "publicado",
                "Ipeadata DISOC_DESE, atualizado 2016-01-06",
                "",
            ),
            "PNADC_SIDRA_4562": (
                "desemprego",
                "PNAD Contínua anual, 14+, semana de referência",
                "%",
                "publicado",
                "SIDRA 4562, baixado 2026-10-19",
                "",
            ),
            "PNADC_media_Ipeadata_PAN_TDESOC": (
                "desemprego",
                "PNAD Contínua, média dos meses (Ipeadata)",
                "%",
                "derivado_deterministico",
                "Ipeadata PAN_TDESOC, atualizado 2026-01-30",
                "",
            ),
        },
    ),
    (
        "economia-real/saida-salmin-real-anual.csv",
        "ano",
        {
            "media_anual_real_R$_set2026": (
                "salmin_real",
                "Ipea GAC12_SALMINRE12, média anual, R$ de set/2026",
                "R$",
                "derivado_deterministico",
                "Ipeadata GAC12_SALMINRE12, atualizado 2026-10-09",
                "deflator IPC-SP, IPC-RJ, IGPC-Mtb e INPC emendados pelo Ipea",
            ),
            "dezembro_real_R$_set2026": (
                "salmin_real",
                "Ipea GAC12_SALMINRE12, dezembro, R$ de set/2026",
                "R$",
                "publicado",
                "Ipeadata GAC12_SALMINRE12, atualizado 2026-10-09",
                "deflator IPC-SP, IPC-RJ, IGPC-Mtb e INPC emendados pelo Ipea",
            ),
        },
    ),
]


_MON = "BCB SGS e Ipeadata, baixados 2026-10-19"
_AGREGADOS = {
    "M0_med12_pib_pct": "M0, base restrita",
    "M1_med12_pib_pct": "M1, conceito antigo (até jun/2018)",
    "PME_med12_pib_pct": "Papel-moeda emitido",
    "BA_med12_pib_pct": "Base ampliada (desde 1994)",
    "M2_2001_med12_pib_pct": "M2, regime 2001",
    "M3_2001_med12_pib_pct": "M3, regime 2001",
    "M4_2001_med12_pib_pct": "M4, regime 2001",
    "M1_novo_med12_pib_pct": "M1, Novo (desde 2002)",
    "M2_novo_med12_pib_pct": "M2, Novo (desde dez/2001)",
    "M3_novo_med12_pib_pct": "M3, Novo (desde dez/2001)",
    "M4_novo_med12_pib_pct": "M4, Novo (desde dez/2001)",
}
_SENHORIAGEM = {
    "a_dM0_pib": "Emissão da base, ΔM0/PIB (inclui demanda real por moeda)",
    "b_anual_igpdi_pib": "Imposto inflacionário, forma anual com IGP-DI",
    "c_II_mensal_pib": "Imposto inflacionário II, fórmula mensal (base M0), Cysne e Coimbra-Lisboa 2004",
    "c_TIT_mensal_pib": "Transferências inflacionárias totais TIT, fórmula mensal (base M1)",
    "c2_II_ipca_pib": "Imposto inflacionário II com IPCA",
    "c2_TIT_ipca_pib": "TIT com IPCA",
    "d1_ayres_seigniorage": "Senhoriagem, Ayres et al. 2019 (d1)",
}
_FISCAL = {
    "dlsp_gf_bc_pib_pct": (
        "divida_pib",
        "Dívida líquida do setor público, governo federal e Banco Central",
    ),
    "dlsp_consolidado_pib_pct_dez": ("divida_pib", "Dívida líquida do setor público consolidado"),
    "dlgg_pib_pct_dez": ("divida_pib", "Dívida líquida do governo geral"),
    "dbgg_pib_pct_dez_metodo_ate_2007": (
        "divida_pib",
        "Dívida bruta do governo geral, metodologia até 2007",
    ),
    "dbgg_pib_pct_dez_metodo_desde_2008": (
        "divida_pib",
        "Dívida bruta do governo geral, metodologia desde 2008",
    ),
    "primario_gf_bc_pib_pct": (
        "primario_pib",
        "Resultado primário, governo federal e Banco Central",
    ),
    "primario_consolidado_pib_pct": ("primario_pib", "Resultado primário consolidado"),
}


def de_monetario():
    """Rows from the monetary collection (``data/raw/monetario/saida``).

    Returns
    -------
    list of dict
        Aggregates as a ratio to GDP (each definition regime is its own series: they are never
        spliced), seigniorage series, fiscal and external series. Levels in the currency of the
        time are not repeated here; the raw files and the conversion factors are in
        ``data/raw/monetario``.
    """
    base, linhas = RAW / "monetario" / "saida", []
    for r in _lido(base / "anual.csv"):
        for col, nome in _AGREGADOS.items():
            v = _num(r.get(col))
            if v is not None:
                linhas.append(
                    _linha(
                        "agregado_pib",
                        nome,
                        r["ano"],
                        v,
                        "% do PIB",
                        _MON,
                        "derivado_deterministico",
                        "razão ao PIB nominal do ano",
                        "data/raw/monetario/saida/anual.csv",
                    )
                )
    for r in _lido(base / "senhoriagem_anual.csv"):
        for col, nome in _SENHORIAGEM.items():
            v = _num(r.get(col))
            if v is not None:
                linhas.append(
                    _linha(
                        "senhoriagem_pib",
                        nome,
                        r["ano"],
                        v,
                        "% do PIB",
                        _MON,
                        "derivado_deterministico",
                        "",
                        "data/raw/monetario/saida/senhoriagem_anual.csv",
                    )
                )
        for col in ("cysne_II", "cysne_TI", "cysne_TIT"):
            v = _num(r.get(col))
            if v is not None:
                linhas.append(
                    _linha(
                        "senhoriagem_pib",
                        f"{col} como publicado na Tabela 1 de Cysne e Coimbra-Lisboa (2004)",
                        r["ano"],
                        v,
                        "% do PIB",
                        "Cysne e Coimbra-Lisboa 2004, DOI 10.1590/0101-35172004-1602",
                        "publicado",
                        "transcrição da tabela do artigo",
                        "data/raw/monetario/saida/senhoriagem_anual.csv",
                    )
                )
    for r in _lido(base / "extras_anual.csv"):
        simples = (
            (
                "cambio_fim_RS_por_USD",
                "cambio",
                "Câmbio comercial, venda, fim de período",
                "R$/US$",
                "publicado",
            ),
            (
                "selic_over_ano_pct",
                "selic_over",
                "Selic over, produto das taxas mensais",
                "% a.a.",
                "derivado_deterministico",
            ),
            (
                "juro_real_ipca_pct",
                "juro_real",
                "Juro real ex-post com IPCA",
                "%",
                "derivado_deterministico",
            ),
            (
                "juro_real_igpdi_pct",
                "juro_real",
                "Juro real ex-post com IGP-DI",
                "%",
                "derivado_deterministico",
            ),
            (
                "reservas_USDmi_dez",
                "reservas_usd",
                "Reservas internacionais, dezembro",
                "US$ milhões",
                "publicado",
            ),
        )
        for col, ind, nome, unid, nat in simples:
            v = _num(r.get(col))
            if v is not None:
                linhas.append(
                    _linha(
                        ind,
                        nome,
                        r["ano"],
                        v,
                        unid,
                        _MON,
                        nat,
                        "",
                        "data/raw/monetario/saida/extras_anual.csv",
                    )
                )
        for col, (ind, nome) in _FISCAL.items():
            v = _num(r.get(col))
            if v is not None:
                linhas.append(
                    _linha(
                        ind,
                        nome,
                        r["ano"],
                        v,
                        "% do PIB",
                        _MON,
                        "publicado",
                        "",
                        "data/raw/monetario/saida/extras_anual.csv",
                    )
                )
    return linhas


def de_quebras_dir():
    """Rows from the line-free and eligibility-line tables of the method-break audit."""
    linhas = []
    for r in _lido(RAW / "quebras" / "renda-por-decil.csv"):
        linhas.append(
            _linha(
                "renda_decil",
                f"PIP decil {r['decil']} ({r['pesquisa']}, {r['welfare_type']}, PPC {r['ppc_base']})",
                r["ano"],
                _num(r["renda_per_capita_ppc_dolar_dia"]),
                "US$ PPC/dia",
                r["vintage"][:60],
                "derivado_deterministico",
                "renda = participação x 10 x média (PIP)",
                "data/raw/quebras/renda-por-decil.csv",
            )
        )
    for r in _lido(RAW / "quebras" / "bolsa-familia-linhas-elegibilidade.csv"):
        for col, nome in (
            ("pobreza_R$_set2026_INPC", "linha de pobreza"),
            ("extrema_R$_set2026_INPC", "linha de extrema pobreza"),
        ):
            linhas.append(
                _linha(
                    "bf_limiar_real",
                    f"Bolsa Família, {nome}, deflacionada pelo INPC",
                    r["inicio_dos_efeitos"],
                    _num(r[col]),
                    "R$ de set/2026",
                    "decretos do Planalto; INPC SGS 188",
                    "derivado_deterministico",
                    r["instrumento"],
                    "data/raw/quebras/bolsa-familia-linhas-elegibilidade.csv",
                )
            )
    return linhas


MEC_AREAS = ("mecanismos-preco", "mecanismos-contabil")
#: Collections whose series carry a ``pais_ou_grupo`` column (country or aggregate code).
MUNDO_AREAS = ("mundo",)
#: Collections in the long format whose series register themselves (no code change per series).
LONGAS_AUTO = ("poder-de-compra", "inep")
DOMINIO_AUTO = {
    "mecanismos-preco": "mecanismos",
    "mecanismos-contabil": "mecanismos",
    "mundo": "mundo",
    "poder-de-compra": "poder_de_compra",
    "inep": "educacao",
}


@lru_cache(maxsize=1)
def catalogo():
    """The indicator catalogue: the hand-written entries plus the register of price/fiscal mechanisms.

    Series of the mechanism collections are registered automatically (domain ``mecanismos``,
    name taken from the series definition), so a new collected series needs no code change.

    Returns
    -------
    dict
        ``indicator -> (domain, name pt-BR, name en, rule flag)``.
    """
    todo = dict(CATALOGO)
    for area in MEC_AREAS + MUNDO_AREAS + LONGAS_AUTO:
        for f in sorted((RAW / area / "series").glob("*.csv")):
            for r in _lido(f):
                if (
                    "indicador" in r
                    and r["indicador"] not in todo
                    and _num(r.get("valor")) is not None
                ):
                    nome = r["definicao_linha"][:110]
                    regra = r.get("dependente_de_regra") or ("sim" if area in MEC_AREAS else "nao")
                    regra = "sim" if str(regra).lower().startswith("s") else "nao"
                    todo[r["indicador"]] = (DOMINIO_AUTO[area], nome, nome, regra)
    return todo


_EXCESSO = {
    "excesso_M0_pp": (
        "Excesso monetário de M0: crescimento de M0 menos crescimento real do PIB",
        "p.p.",
    ),
    "excesso_M1_pp": (
        "Excesso monetário de M1: crescimento de M1 menos crescimento real do PIB",
        "p.p.",
    ),
    "M1_cresc_pct": ("Crescimento nominal de M1 (conceito antigo até 2018)", "% a.a."),
    "M0_cresc_pct": ("Crescimento nominal de M0", "% a.a."),
}
_BF = {
    "pobreza_/_SM": ("Linha de pobreza do Bolsa Família em fração do salário mínimo", "fração"),
    "extrema_/_um_quarto_SM": (
        "Linha de extrema pobreza do Bolsa Família em fração de 1/4 do salário mínimo",
        "fração",
    ),
    "pobreza_/_US$3,65": (
        "Linha de pobreza do Bolsa Família em fração da linha de US$ 3,65 PPC 2017",
        "fração",
    ),
    "extrema_/_US$2,15": (
        "Linha de extrema pobreza do Bolsa Família em fração da linha de US$ 2,15 PPC 2017",
        "fração",
    ),
}


def de_poder_de_compra_largos():
    """Rows from the two wide tables of the purchasing-power collection (monetary overhang, BF lines)."""
    base, linhas = RAW / "poder-de-compra" / "series", []
    vint = "BCB SGS, Ipeadata e Planalto, baixados 2026-10-19"
    f = base / "excesso_monetario.csv"
    if f.exists():
        for r in _lido(f):
            for col, (nome, unid) in _EXCESSO.items():
                v = _num(r.get(col))
                if v is not None:
                    linhas.append(
                        _linha(
                            "excesso_monetario",
                            nome,
                            r["ano"],
                            v,
                            unid,
                            vint,
                            "derivado_deterministico",
                            r.get("nota", ""),
                            "data/raw/poder-de-compra/series/excesso_monetario.csv",
                        )
                    )
    f = base / "bolsa_familia_linhas_anual.csv"
    if f.exists():
        for r in _lido(f):
            for col, (nome, unid) in _BF.items():
                v = _num(r.get(col))
                if v is not None:
                    linhas.append(
                        _linha(
                            "bf_linha_relativa",
                            nome,
                            r["ano_dezembro"],
                            v,
                            unid,
                            vint,
                            "derivado_deterministico",
                            r.get("instrumento", ""),
                            "data/raw/poder-de-compra/series/bolsa_familia_linhas_anual.csv",
                        )
                    )
    return linhas


def _num(txt):
    """Float of a CSV cell, or ``None`` when empty."""
    return None if txt in ("", None) else float(txt)


def _linha(indicador, serie, periodo, valor, unidade, vintage, natureza, nota, origem):
    """Build one observation row (domain and rule flag come from the catalogue)."""
    dom, _, _, regra = catalogo()[indicador]
    return {
        "indicador": indicador,
        "serie": serie,
        "dominio": dom,
        "periodo": str(periodo),
        "valor": valor,
        "unidade": unidade,
        "vintage": vintage,
        "natureza": natureza,
        "dependente_de_regra": regra,
        "nota": nota,
        "origem": origem,
    }


def de_longos():
    """Rows from the long-format CSVs of the social and omitted-domain collections.

    Returns
    -------
    list of dict
        Observation rows. Files without a ``vintage`` column use the ``fonte`` string, which
        in those files already encodes the edition (for example ``IBGE-SIS2025``).
    """
    achados = sorted((RAW / "social" / "series").glob("*.csv"))
    for area in ("dominios-1", "dominios-2", *MEC_AREAS, *MUNDO_AREAS, *LONGAS_AUTO):
        achados += sorted((RAW / area / "series").glob("*.csv"))
    linhas = []
    for f in achados:
        for r in _lido(f):
            if "indicador" not in r or r["indicador"] not in catalogo():
                continue  # for example limiares_eventos.csv, an event table, not a series
            if _num(r["valor"]) is None:
                continue  # a gap row (no value): the gap is the absence of the row
            modelo = "modelo_de_terceiro" if "MODELO" in r.get("nota", "") else "publicado"
            serie = f"{r['fonte']} | {r['definicao_linha']}"
            periodo = r["ano"]
            if r.get("trimestre") and r["trimestre"] != "ano":
                periodo = f"{r['ano']}-{r['trimestre']}"  # quarterly rows keep their quarter
            if r.get("pais_ou_grupo"):
                serie += f" | {r['pais_ou_grupo']}"  # country or aggregate code is part of the key
            if r.get("uf"):
                serie += f" | {r['uf']}"  # the state code (or BR) is part of the key
            linhas.append(
                _linha(
                    r["indicador"],
                    serie,
                    periodo,
                    _num(r["valor"]),
                    r["unidade"],
                    r.get("vintage") or r["fonte"],
                    modelo,
                    r.get("nota", ""),
                    f"data/raw/{f.relative_to(RAW).as_posix()}",
                )
            )
    return linhas


def _lido(caminho):
    """Read a CSV into a list of dicts."""
    with open(caminho, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def de_largos():
    """Rows from the wide annual files of the real-economy collection."""
    linhas = []
    for rel, col_ano, mapa in LARGAS:
        for r in _lido(RAW / rel):
            for col, (ind, serie, unid, nat, vint, nota) in mapa.items():
                v = _num(r.get(col))
                if v is None:
                    continue
                n = nota
                if col == "pib_percapita_var_pct_final" and r.get("percapita_origem") == "oficial":
                    nat = "publicado"
                linhas.append(
                    _linha(ind, serie, r[col_ano], v, unid, vint, nat, n, f"data/raw/{rel}")
                )
    return linhas


def de_inflacao():
    """Monthly price indices (BCB SGS 433, 188, 189, 190 and Ipeadata IGP-DI level)."""
    linhas = []
    for arq, nome, sgs in (
        ("ipca-sgs433-raw.json", "IPCA", 433),
        ("inpc-sgs188-raw.json", "INPC", 188),
        ("igpm-sgs189-raw.json", "IGP-M", 189),
        ("igpdi-sgs190-raw.json", "IGP-DI", 190),
    ):
        for r in json.loads((RAW / "inflacao" / arq).read_text()):
            ym = f"{r['data'][-4:]}-{r['data'][3:5]}"
            linhas.append(
                _linha(
                    "inflacao_mensal",
                    f"{nome} (BCB SGS {sgs})",
                    ym,
                    float(r["valor"]),
                    "% ao mês",
                    f"BCB SGS {sgs}, baixado 2026-10-19",
                    "publicado",
                    "",
                    f"data/raw/inflacao/{arq}",
                )
            )
    j = json.loads((RAW / "inflacao" / "igpdi-ipeadata-raw.json").read_text())["value"]
    for r in j:
        linhas.append(
            _linha(
                "igpdi_indice",
                "IGP-DI número-índice (Ipeadata IGP12_IGPDI12)",
                r["VALDATA"][:7],
                r["VALVALOR"],
                "índice",
                "Ipeadata IGP12_IGPDI12, baixado 2026-10-19",
                "publicado",
                "moeda da época; só a razão entre datas tem sentido",
                "data/raw/inflacao/igpdi-ipeadata-raw.json",
            )
        )
    return linhas


def observacoes():
    """All observation rows, sorted and unique by (indicator, series, vintage, period).

    A key that the source itself publishes twice keeps its first row; the other value is
    recorded in ``nota`` (nothing is dropped silently).
    """
    linhas = (
        de_longos()
        + de_largos()
        + de_inflacao()
        + de_monetario()
        + de_quebras_dir()
        + de_poder_de_compra_largos()
    )
    linhas.sort(key=lambda r: (r["indicador"], r["serie"], r["vintage"], r["periodo"]))
    vistos, unicas = {}, []
    for r in linhas:
        k = (r["indicador"], r["serie"], r["vintage"], r["periodo"])
        if k in vistos:
            vistos[k]["nota"] = (
                vistos[k]["nota"] + f" | a fonte publica também {r['valor']} para esta chave"
            ).strip(" |")
            continue
        vistos[k] = r
        unicas.append(r)
    return unicas


def indicadores():
    """The indicator catalogue as rows (id, domain, names, rule flag, unit, series count)."""
    obs = observacoes()
    conta = {}
    for r in obs:
        c = conta.setdefault(r["indicador"], {"series": set(), "unidade": r["unidade"], "n": 0})
        c["series"].add(r["serie"])
        c["n"] += 1
    saida = []
    for ind, (dom, pt, en, regra) in catalogo().items():
        c = conta.get(ind)
        saida.append(
            {
                "indicador": ind,
                "dominio": dom,
                "nome_pt": pt,
                "nome_en": en,
                "dependente_de_regra": regra,
                "unidade": c["unidade"] if c else "",
                "n_series": len(c["series"]) if c else 0,
                "n_observacoes": c["n"] if c else 0,
            }
        )
    return saida


#: Labels some collections used for the break type, mapped to the four canonical ones
#: (the original label is kept in ``tipo_original``).
TIPO_CANONICO = {
    "definicao_taxa": "metodo_estatistico",
    "cobertura_censo": "metodo_estatistico",
    "sobreposicao_de_publicacoes": "revisao_de_vintage",
}
QUEBRA_CAMPOS = [
    "id",
    "tipo_original",
    "indicador",
    "serie",
    "data_quebra",
    "tipo_de_quebra",
    "metodo_antigo",
    "metodo_novo",
    "razao_declarada_pela_fonte",
    "fonte_primaria_url",
    "trecho_citado",
    "direcao_do_efeito",
    "como_a_direcao_foi_determinada",
    "efeito_medido",
    "como_medido",
    "apresentada_como_aprimoramento",
    "celulas_do_infografico_afetadas",
    "origem",
]


def quebras():
    """Merge the method-break catalogues of every collection into one table with stable ids.

    Returns
    -------
    list of dict
        One row per break; ``tipo_de_quebra`` is ``metodo_estatistico``, ``mudanca_de_regra``,
        ``revisao_de_vintage`` or ``mudanca_de_unidade`` (currency change). ``id`` is ``q001``... in file order, so ids never change when a
        collection is appended at the end.
    """
    linhas = []
    for area in ("quebras", "dominios-1", "dominios-2", "mundo", "poder-de-compra", "inep"):
        f = RAW / area / "quebras.csv"
        if not f.exists():
            continue
        for r in _lido(f):
            linha = {k: r.get(k, "") for k in QUEBRA_CAMPOS if k not in ("id", "origem")}
            linha["tipo_original"] = r.get("tipo_de_quebra", "")
            linha["tipo_de_quebra"] = TIPO_CANONICO.get(
                linha["tipo_original"], linha["tipo_original"]
            )
            linha["origem"] = f"data/raw/{area}/quebras.csv"
            linhas.append(linha)
    for i, r in enumerate(linhas, 1):
        r["id"] = f"q{i:03d}"
    return linhas


MEC_CAMPOS = [
    "id",
    "mecanismo",
    "tipo",
    "janela_inicio",
    "janela_fim",
    "governo_que_aplica",
    "governo_que_paga",
    "atribuicao",
    "magnitude_medida",
    "unidade",
    "como_medida",
    "reversao_medida",
    "fonte_primaria_url",
    "trecho_citado",
    "camada_de_evidencia",
    "vintage",
    "nota",
    "origem",
]
SIM_CAMPOS = ["mecanismo", "governo", "status", "valor", "unidade", "razao", "detalhe", "origem"]


def mecanismos():
    """Merge the mechanism registers of the price and the accounting collections.

    Returns
    -------
    tuple of list
        ``(mecanismos, simetria)``: one row per documented mechanism, and one row per
        (mechanism class, government) saying whether it was measured, had no data, or does not
        apply. Coverage is NOT symmetric by search effort, so counting rows is not a measure of
        behaviour; only classes measured with the same rule for every government can be scored.
    """
    meca, sim = [], []
    for area in MEC_AREAS:
        f = RAW / area / "mecanismos.csv"
        if f.exists():
            for r in _lido(f):
                linha = {k: r.get(k, "") for k in MEC_CAMPOS if k != "origem"}
                linha["origem"] = f"data/raw/{area}/mecanismos.csv"
                meca.append(linha)
        g = RAW / area / "simetria-por-governo.csv"
        if g.exists():
            for r in _lido(g):
                chaves = list(r)
                linha = {
                    "mecanismo": r.get("classe") or r[chaves[0]],
                    "governo": r.get("governo", ""),
                    "status": r.get("status", ""),
                    "valor": r.get("valor", ""),
                    "unidade": r.get("unidade", ""),
                    "razao": r.get("razao", ""),
                    "detalhe": r.get("detalhe") or r.get("janela_dos_dados", ""),
                    "origem": f"data/raw/{area}/simetria-por-governo.csv",
                }
                sim.append(linha)
    return meca, sim


def bundle():
    """Build the data bundle the X-ray page reads (``output/series.json``).

    Returns
    -------
    dict
        ``mandatos``, ``indicadores`` (each with its series, vintages and points) and ``quebras``.
        No verdict, no score, no ranking: the raw layer only.
    """
    from govfc.mandatos import carregar

    por_ind = {}
    for r in observacoes():
        serie = por_ind.setdefault(r["indicador"], {}).setdefault(
            (r["serie"], r["vintage"]), {"natureza": r["natureza"], "pontos": []}
        )
        serie["pontos"].append([r["periodo"], r["valor"]])
    catalogo = {r["indicador"]: r for r in indicadores()}
    saida = []
    for ind, series in por_ind.items():
        c = catalogo[ind]
        saida.append(
            {
                "id": ind,
                "dominio": c["dominio"],
                "nome_pt": c["nome_pt"],
                "nome_en": c["nome_en"],
                "dependente_de_regra": c["dependente_de_regra"],
                "unidade": c["unidade"],
                "series": [
                    {
                        "serie": k[0],
                        "vintage": k[1],
                        "natureza": v["natureza"],
                        "pontos": v["pontos"],
                    }
                    for k, v in sorted(series.items())
                ],
            }
        )
    mand = [
        {
            "id": m["id"],
            "nome": m["nome"],
            "posse": m["posse"].isoformat(),
            "saida": m["saida"].isoformat(),
            "no_infografico": m["no_infografico"],
        }
        for m in carregar()
    ]
    meca, sim = mecanismos()
    return {
        "schema": 1,
        "mandatos": mand,
        "indicadores": saida,
        "quebras": quebras(),
        "mecanismos": meca,
        "simetria": sim,
    }


def eh_uf(r):
    """True for a state-level education row (goes to ``observations_educacao_uf.csv``)."""
    return r["origem"].endswith("edu_rendimento.csv") and not r["serie"].endswith("| BR")


def gravar():
    """Write ``observations.csv`` and ``indicators.csv`` under ``data/curated``.

    Returns
    -------
    tuple of int
        Number of observation rows, catalogue indicators and method breaks. Also writes
        ``output/series.json``, the bundle the page reads.
    """
    CURADO.mkdir(parents=True, exist_ok=True)
    obs = observacoes()

    # state-level education rows (27 UFs x years x rates) go to a side table: they are 70 % of all
    # rows and the national table must stay small enough to read and to diff
    for nome, sub in (
        ("observations.csv", [r for r in obs if not eh_uf(r)]),
        ("observations_educacao_uf.csv", [r for r in obs if eh_uf(r)]),
    ):
        with open(CURADO / nome, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=CAMPOS, lineterminator="\n")
            w.writeheader()
            for r in sub:
                w.writerow({k: ("" if r[k] is None else r[k]) for k in CAMPOS})
    ind = indicadores()
    with open(CURADO / "indicators.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ind[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(ind)
    qs = quebras()
    with open(CURADO / "quebras.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=QUEBRA_CAMPOS, lineterminator="\n")
        w.writeheader()
        w.writerows(qs)
    meca, sim = mecanismos()
    for nome, campos, linhas in (("mecanismos", MEC_CAMPOS, meca), ("simetria", SIM_CAMPOS, sim)):
        with open(CURADO / f"{nome}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=campos, lineterminator="\n")
            w.writeheader()
            w.writerows(linhas)
    (RAIZ / "output").mkdir(exist_ok=True)
    (RAIZ / "output" / "series.json").write_text(
        json.dumps(bundle(), ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    return len(obs), len(ind), len(qs)


if __name__ == "__main__":
    n_obs, n_ind, n_q = gravar()
    print(f"observations: {n_obs} rows, indicators: {n_ind}, breaks: {n_q}")
