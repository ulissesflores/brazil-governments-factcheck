#!/usr/bin/env python3
"""Gera RESULTADO.md a partir de series/*.csv, janelas.csv, quebras.csv, busca-sem-serie.csv e manifest.jsonl (sem rede).
Uso: python3 -I resultado.py   (rode depois de recalcula.py)"""
import csv, collections, json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
rd = lambda f: list(csv.DictReader(open(os.path.join(AQUI, f), encoding="utf-8")))
series = {d: rd(f"series/{d}.csv") for d in ("edu", "mor", "tbl", "pre", "ass", "mat")}
jan, que, busca = rd("janelas.csv"), rd("quebras.csv"), rd("busca-sem-serie.csv")
ev = rd("series/limiares_eventos.csv")
man = [json.loads(l) for l in open(os.path.join(AQUI, "manifest.jsonl"), encoding="utf-8")]
GOV = []
for r in jan:
    if r["governo"] not in GOV: GOV.append(r["governo"])
J = {(r["indicador"], r["governo"]): r for r in jan}


def cel(ind, g, nd=2):
    r = J.get((ind, g))
    if not r or r["n_anos"] == "0": return "-"
    return f"{float(r['media']):.{nd}f} ({r['n_anos']})"


def tabela(cols, titulo_cols, nd=2):
    """cols: ids de janelas.csv; mostra so governos com algum dado em alguma coluna."""
    gs = [g for g in GOV if any(J.get((c, g), {}).get("n_anos", "0") != "0" for c in cols)]
    out = ["| Governo | " + " | ".join(titulo_cols) + " |", "| --- | " + " | ".join("---" for _ in cols) + " |"]
    for g in gs:
        out.append(f"| {g} | " + " | ".join(cel(c, g, nd) for c in cols) + " |")
    return "\n".join(out)


def cobertura():
    por = collections.defaultdict(list)
    for d, rs in series.items():
        for r in rs:
            if not r["nota"].startswith(("PRELIMINAR",)):
                por[(d, r["indicador"], r["fonte"])].append(int(r["ano"]))
    return por


PRIMARIA = {"edu_analfab15": "Atlas-DH-Censo(ADH_T_ANALF15M)", "mor_agua_rede_geral": "IBGE-Censo(SIDRA)", "mor_esgoto_adequado": "IBGE-Censo(SIDRA)",
            "tbl_informalidade": "Ipea-PNAD(DISOC_INFI)", "tbl_renda_trabalho_real": "IBGE-PNAD(SIDRA1871 deflacionado)"}


def tab_cobertura():
    por = cobertura()
    linhas = ["| Dominio | Indicador (primario) | Fonte | Primeiro-ultimo ano | Pontos | Cobertura (anos) | Extensao >= 30 anos | Fonte homogenea (regra 3) | dependente_de_regra |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    dep = {(r["indicador"]): r["dependente_de_regra"] for rs in series.values() for r in rs}
    for (d, ind, fonte), anos in sorted(por.items()):
        if ind in PRIMARIA and PRIMARIA[ind] != fonte: continue
        if ind.startswith("edu_saeb_") and "Relatorio" in fonte: continue
        if ind in ("mor_esgoto_rede", "edu_analfab15") and False: continue
        a0, a1 = min(anos), max(anos)
        if ind.startswith("edu_saeb_"):
            anos = sorted(set(anos) | {int(r["ano"]) for r in series["edu"] if r["indicador"] == ind and "Relatorio" in r["fonte"]}); a1 = max(anos)
        span = a1 - a0 + 1
        hom = 'nao verificada (compilacao UIS de fontes nacionais)' if fonte.startswith('Banco Mundial') else 'sim (uma so fonte/metodo)'
        linhas.append(f"| {d} | {ind} | {fonte[:48]} | {a0}-{a1} | {len(anos)} | {span} | {'sim' if span >= 30 else 'NAO'} | {hom} | {dep[ind]} |")
    return "\n".join(linhas)


def n(k): return sum(1 for r in que if r["tipo_de_quebra"] == k)


nlin = sum(len(v) for v in series.values())
md = []
A = md.append
A("# Dominios-1: educacao, moradia, previdencia, assistencia, trabalho (alem de 2 linhas), maternidade, e o que nao tem serie")
A("")
A("Dossie: governos-do-brasil-economia. Coleta e conferencia em 2026-10-19. Sem opiniao politica: so bruto como publicado, vintage e quebra. Nenhum numero daqui foi comparado com o infografico (estes dominios nao estao nele), por isso nao ha marcas de conferencia (certo/aproximado/errado/nao verificado).")
A("")
A("Como reproduzir: `python3 -I /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1/recalcula.py` (sem rede; confere o sha256 de cada bruto e a cadeia do `manifest.jsonl`; grava `series/*.csv`, `janelas.csv`, `quebras.csv`, `busca-sem-serie.csv`) e depois `python3 -I resultado.py` (grava este arquivo). Verificacao da cadeia: `python3 /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/manifest_tool.py verify /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1`.")
A("")
A("## 0. Achado e nao achado")
A("")
q30 = [("edu_analfab15", "analfabetismo 15+ (Censos 1991-2022; 1970-2022 com o Atlas 1998)"), ("mor_agua_rede_geral", "agua por rede geral (Censos 1991-2022)"),
       ("mor_esgoto_adequado", "esgoto adequado (Censos 1991-2022)"), ("mat_prenatal7", "7+ consultas de pre-natal (SINASC 1995-2024)")]
por = cobertura()
passam = sorted({ind for (d, ind, f), an in por.items() if (max(an) - min(an) + 1) >= 30 and not ind.startswith(("ass_bpc_idade", "ass_bpc_limiar")) and not (ind.startswith("edu_saeb_"))})
A(f"1. **Achado.** {nlin} linhas em 6 arquivos de serie, {len({r['indicador'] for rs in series.values() for r in rs})} indicadores, cada linha com `vintage` e `dependente_de_regra`. Tem extensao de 30 anos ou mais (ultimo - primeiro ano + 1), entre os indicadores de dados: {', '.join(passam)}. Cumprem tambem a regra de fonte homogenea (uma so fonte/metodo para o primario) apenas os de Censo e SINASC: edu_analfab15, mor_agua_rede_geral, mor_esgoto_adequado e mat_prenatal*; os tres do WDI/UIS ficam como 'nao verificada'. A extensao nao e densidade: os Censos dao 4 pontos em 32 anos (1991-2022; mais 1970 e 1980 pelo Atlas 1998), o WDI/UIS 20 a 30 pontos esparsos, o SINASC 30 anos completos. Na maior parte dos governos de 1964-1989 so ha 1970 e 1980 (analfabetismo e esgoto) e, para repetencia e persistencia, os pontos do WDI.")
A("2. **Quase passam.** Saeb (proficiencia media, 1995-2023, escala equalizada pela TRI) tem 29 anos de cobertura e o BPC por mil habitantes (1996-2024) tem 29: ficam a um ano do corte e entram marcados como `NAO` na tabela 2, nao omitidos.")
A("3. **Nao achado (sem serie comparavel):** cultura, lazer, transporte; Ideb e Pisa (cobertura <30 anos, arquivo do INEP nao localizado); deficit habitacional da Fundacao Joao Pinheiro; proporcao de 65+ com aposentadoria/pensao; gasto federal em assistencia; **taxas de aprovacao, reprovacao, abandono e distorcao idade-serie (nao coletadas: planilhas do INEP nao localizadas)**. Evidencia da busca: `busca-sem-serie.csv` e secao 5.")
A(f"4. **Quebras:** {len(que)} linhas em `quebras.csv` ({n('metodo_estatistico')} de metodo estatistico, {n('mudanca_de_regra')} de mudanca de regra, {n('revisao_de_vintage')} de revisao de vintage). So em {sum(1 for r in que if re.match(r'^(?:[+-]\d|0 em)', r['efeito_medido']))} ha efeito medido (sobreposicao real nos dados baixados); nas demais a coluna diz `sem sobreposicao`. Maiores efeitos medidos: costura PDIAE em 1991 (+9,07 p.p. contra o recalculo do SIDRA), PNADC contra Censo no esgoto de 2022 (+8,00 p.p. no mesmo universo), 'ligacao a rede' contra 'rede como principal forma' em 2022 (+7,10 p.p.), PNADC contra Censo no analfabetismo de 2022 (-1,40 p.p.).")
A("5. **Regra que move o indicador:** a linha de pobreza do Bolsa Familia/Auxilio Brasil em R$ de dez/2025 vai de 309 (2004) a 218 (2025), com duas linhas ate 2022 e uma so (R$ 218) desde a Lei 14.601/2023; a idade minima do BPC por idade cai de 70 para 67 (1998) e 65 (2004). Esses limiares estao em `series/ass.csv` e `series/limiares_eventos.csv`.")
A("6. **Saeb:** as duas vintages (Press Kit 2019 e Relatorio 2023) coincidem em 30 de 30 pontos de 2011-2019; o INEP declara que a escala 'permaneceu a mesma'. Mesmo assim ha quebras de desenho (Aneb + Prova Brasil em 2005; ensino fundamental de 9 anos desde a Lei 11.274/2006), sem sobreposicao para medir.")
A("")
A("## 1. Fontes e cadeia de hash")
A("")
A(f"`manifest.jsonl`: {len(man)} arquivos, cabeca da cadeia = sha256 da ultima linha (conferida por `recalcula.py`). Fontes principais (URL completa, tipo):")
A("")
A("| Fonte | URL / consulta | Onde esta o bruto | Observacao |")
A("| --- | --- | --- | --- |")
for fonte, url, arq, obs in (
    ("Ipeadata OData (series e metadados)", "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='X') e .../Metadados('X')", "bruto/ipea_*.json, bruto/meta/ipea_meta_*.json", "a vintage de cada serie = SERATUALIZACAO do metadado"),
    ("IBGE SIDRA (API agregados v3)", "https://servicodados.ibge.gov.br/api/v3/agregados/{tabela}/periodos/.../variaveis/...?localidades=N1[all]&classificacao=...", "bruto/sidra_*.json, bruto/meta/sidra_meta_*.json", "o servidor devolve gzip mesmo sem pedir; o arquivo guardado e exatamente o que veio (gzip), o leitor descompacta"),
    ("DATASUS TabNet (SINASC)", "http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinasc/cnv/nvuf.def (POST; parametros em scripts/baixar_sinasc.py)", "bruto/tabnet_sinasc_prenatal_ano_1994_2025.html", "registrado com `add-local` (POST nao e coberto pelo `add`); dados finais ate 2024, 2025 preliminar"),
    ("INEP (Saeb)", "https://download.inep.gov.br/educacao_basica/saeb/2019/presskit/PressKit_Saeb_2019.pdf; https://download.inep.gov.br/saeb/resultados/relatorio-saeb_volume_1_2023.pdf", "bruto/doc/inep_*.pdf", "baixados com curl e registrados com `add-local` (urllib falhou na verificacao do certificado); valores lidos dos rotulos dos graficos com `pdftotext -bbox`"),
    ("Banco Mundial WDI", "https://api.worldbank.org/v2/country/BRA/indicator/{codigo}?format=json&per_page=20000", "bruto/wb_*.json", "repetentes, persistencia, gasto em educacao, alfabetizacao de adultos"),
    ("MPS (AEPS 2018) e fluxo de caixa", "http://www.ipeadata.gov.br/doc/AEPS-2018.pdf", "bruto/doc/mps_aeps_2018.pdf", "documento de quebra (7,4 MB)"),
    ("Planalto (leis, decretos, emendas)", "https://www.planalto.gov.br/ccivil_03/...", "bruto/doc/*.htm, bruto/doc/leg/*.htm", "texto compilado; datas de vigencia lidas do proprio texto"),
    ("BCB SGS 433 (IPCA)", "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json", "bruto/bcb_sgs433_ipca_mensal.json", "deflator dos limiares (R$ de dez/2025)"),
):
    A(f"| {fonte} | {url} | {obs and arq} | {obs} |")
A("")
A("Catalogos de busca: listagem de tabelas do SIDRA em `bruto/sidra_catalogo_agregados.json` (nesta cadeia) e catalogo Ipeadata de 4.071 series em `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/social/bruto/ipea_metadados_all.json` (cadeia da pasta social; `recalcula.py` confere o sha256 contra o manifest de la).")
A("")
A("## 2. Indicadores, cobertura e corte de 30 anos")
A("")
A("Regra pre-registrada: fonte oficial, cobertura nacional, frequencia anual (decenal aceita para Censo), pelo menos 30 anos de cobertura ou sobreposicao medida em cada quebra, e uma serie homogenea para o primario (regra 3). 'Cobertura' = ultimo ano - primeiro ano + 1 da serie primaria; pontos = anos com valor.")
A("")
A(tab_cobertura())
A("")
A("Series de sensibilidade (outras fontes, nunca emendadas na primaria) ficam em `series/*.csv` com `fonte` diferente e em `janelas.csv` com o sufixo `__<fonte>` no identificador.")
A("")
A("## 3. Resultado por governo (media na janela do mandato, entre parenteses o numero de anos com dado)")
A("")
A("Regra fixa de atribuicao: o ano pertence ao governo que ocupa o cargo em 1o de julho. Datas de `brazil-governments-factcheck/data/curated/mandatos.csv` (inclui os cinco governos que o infografico omite: Castelo Branco, Geisel, Figueiredo, Sarney, Collor; a Junta Militar de 1969 nao contem 1o de julho e sempre fica sem dado). `-` = nenhum ano com dado na janela; nao ha interpolacao. Anos sinalizados `ANOMALIA`, `PRELIMINAR` ou `FORA_DA_JANELA` ficam na serie e fora das janelas (secao 8). Cada indicador esta nos dois sentidos: nenhum foi retirado depois de ver o resultado.")
A("")
A("### 3.1 Educacao: alfabetizacao")
A("")
A(tabela(["edu_analfab15", "edu_analfab15__Ipea_Atlas1998_TXA15M7091", "edu_analfab15__IBGE_PNAD_IDS1187", "edu_analfab15__IBGE_PNADC_SIDRA7113"],
         ["Analfabetismo 15+ %, Atlas DH (primaria)", "idem, Atlas 1998 (1970-1991)", "idem, PNAD 2004-2015", "idem, PNADC 2016+"]))
A("")
A("### 3.2 Educacao: Saeb, proficiencia media (pontos, escala 0-500; Press Kit 2019 ate 2009, Relatorio 2023 de 2011 em diante)")
A("")
A(tabela(["edu_saeb_LP_EF_5ano_4serie", "edu_saeb_LP_EF_9ano_8serie", "edu_saeb_LP_EM_3serie", "edu_saeb_MT_EF_5ano_4serie", "edu_saeb_MT_EF_9ano_8serie", "edu_saeb_MT_EM_3serie"],
         ["LP 5o ano", "LP 9o ano", "LP 3a EM", "MT 5o ano", "MT 9o ano", "MT 3a EM"], 1))
A("")
A("### 3.3 Educacao: indicadores que dependem de regra (`dependente_de_regra=sim`) e outros")
A("")
A(tabela(["edu_repetentes_primario_pct", "edu_persistencia_ultima_serie_primario", "edu_gasto_publico_pib", "edu_alfabetizacao_adultos_wdi", "edu_anos_estudo_25mais", "edu_anos_estudo_15mais"],
         ["Repetentes, primario, % (WDI)", "Persistencia ate a ultima serie, % (WDI)", "Gasto em educacao, % PIB (WDI)", "Alfabetizacao de adultos % (WDI)", "Anos de estudo 25+ (Censo)", "Anos de estudo 15+ (PNADC)"]))
A("")
A("### 3.4 Moradia")
A("")
A(tabela(["mor_agua_rede_geral", "mor_esgoto_adequado", "mor_esgoto_adequado__Ipea_PDIAE_Atlas1998_1991_SIDRA_2000", "mor_agua_encanada_pop", "mor_luz"],
         ["Agua por rede geral %, Censo IBGE", "Esgoto adequado %, Censo IBGE", "Esgoto adequado %, Ipea PDIAE (1970+; ver quebra 17)", "Agua encanada %, Atlas DH", "Luz eletrica %, Atlas DH"]))
A("")
A("### 3.5 Trabalho (alem de desemprego e salario minimo, que ja estao na pasta economia-real)")
A("")
A(tabela(["tbl_informalidade", "tbl_informalidade_ibge", "tbl_renda_trabalho_real", "tbl_renda_trabalho_real__IBGE_PNADC_SIDRA4660_nominal_deflacionado", "tbl_renda_trabalho_real__IBGE_PNAD_SIDRA427_real_divulgado"], ["Informalidade % (Ipea, PNAD 1992-2014)", "Informalidade % (IBGE, PNADC 2016+)", "Renda real do trabalho, R$ dez/2025 (PNAD 2001-2015)", "idem, PNADC 2012-2025 (nominal deflacionado)", "idem, PNAD 1996-2006 como publicado (base de precos nao declarada)"]))
A("")
A("### 3.6 Previdencia (RGPS, % do PIB nominal; 2004-2025)")
A("")
A(tabela(["pre_rgps_arrecadacao_liquida_pib", "pre_rgps_beneficios_pib", "pre_rgps_resultado_pib"], ["Arrecadacao liquida", "Beneficios previdenciarios", "Resultado primario (negativo = deficit)"]))
A("")
A("### 3.7 Assistencia: cobertura e limiares de elegibilidade")
A("")
A(tabela(["ass_bpc_por_mil_hab", "ass_pbf_familias_por_mil_hab", "ass_bpc_idade_minima", "ass_bpc_limiar_quarto_sm_real", "ass_pbf_limiar_pobreza_real", "ass_pbf_limiar_extrema_pobreza_real"],
         ["BPC (idosos+deficiencia) por mil hab., dez", "Bolsa Familia/Auxilio Brasil por mil hab., dez", "Idade minima do BPC idoso", "1/4 do SM em R$ dez/2025", "Linha de pobreza do PBF, R$ dez/2025", "Linha de extrema pobreza do PBF, R$ dez/2025"]))
A("")
A("### 3.8 Maternidade e infancia (mortalidade infantil ja existe em `social/series/mortinf.csv`, nao refeita)")
A("")
A(tabela(["mat_prenatal7", "mat_prenatal_ignorado", "mat_prenatal_nenhuma"], ["7+ consultas, % dos informados", "Numero de consultas ignorado, % dos nascimentos", "Nenhuma consulta, % dos informados"]))
A("")
A("## 4. Regras de politica que mudam o que o indicador mede (educacao)")
A("")
A("| Data | Regra | Fonte primaria (URL) | Indicador afetado |")
A("| --- | --- | --- | --- |")
for d, regra, url, ind in (
    ("1996-12-20", "LDB (Lei 9.394): ciclos e progressao continuada permitidos (art. 23; art. 32, par. 2)", "https://www.planalto.gov.br/ccivil_03/leis/l9394.htm", "repetentes, persistencia (dependente_de_regra=sim)"),
    ("1998 (SP)", "Progressao continuada em ciclos na rede estadual de Sao Paulo (Deliberacao CEE 9/97; Resolucao SE 4/98). Texto oficial nao localizado; citado por artigo (fonte SECUNDARIA)", "https://www.scielo.br/pdf/pp/v21n3/v21n3a12.pdf", "repetentes"),
    ("1998-01-01", "Fundef (EC 14/1996; Lei 9.424/1996)", "https://www.planalto.gov.br/ccivil_03/leis/l9424.htm", "gasto em educacao"),
    ("2005-03-21", "Portaria MEC 931/2005: Saeb = Aneb (amostral) + Anresc/Prova Brasil (censitaria nas escolas publicas)", "https://download.inep.gov.br/educacao_basica/saeb/documentos_edicoes_antigas/coletanea_de_documentos_de_edicoes_antigas.pdf", "Saeb"),
    ("2006-02-06", "Lei 11.274: ensino fundamental de 9 anos, matricula aos 6 anos (implantacao ate 2010)", "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11274.htm", "Saeb 5o e 9o anos (rotulo 4a/8a serie ate entao)"),
    ("2007-01-01", "Fundeb (EC 53/2006; Lei 11.494/2007)", "https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2007/lei/l11494.htm", "gasto em educacao"),
    ("2009-11-11", "EC 59/2009: educacao basica obrigatoria dos 4 aos 17 anos", "https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc59.htm", "gasto, anos de estudo, Saeb EM"),
    ("2020-08-26", "Fundeb permanente (EC 108/2020; Lei 14.113/2020)", "https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc108.htm", "gasto em educacao"),
):
    A(f"| {d} | {regra} | {url} | {ind} |")
A("")
A("Os valores brutos de repetentes (WDI/UIS) foram publicados assim e nao foram atribuidos a regra nenhuma: " + ", ".join(f"{r['ano']}={float(r['valor']):.1f}" for r in series["edu"] if r["indicador"] == "edu_repetentes_primario_pct" and int(r["ano"]) in (1992, 1996, 2000, 2004, 2008, 2011)) + " (% da matricula; anos ausentes na fonte nao foram preenchidos).")
A("")
A("### Definicao de 'alfabetizado' em cada fonte (o que cada metadado diz)")
A("")
A("| Fonte | O que a fonte diz | Onde |")
A("| --- | --- | --- |")
A("| Atlas DH (ADH_T_ANALF15M, Censos 1991-2022) | razao entre a populacao de 15+ que 'nao sabe ler nem escrever um bilhete simples' e o total de 15+ | `bruto/meta/ipea_meta_ADH_T_ANALF15M.json` |")
A("| Atlas 1998 (TXA15M7091, Censos 1970-1991) | 'pessoas de 15 ou mais anos de idade que nao sabem ler nem escrever um bilhete simples' | `bruto/meta/ipea_meta_TXA15M7091.json` |")
A("| IBGE SIDRA (Censo 2022, tab. 9542; PNAD IDS 1187; PNADC 7113) | os metadados baixados trazem so o titulo da tabela ('taxa de alfabetizacao/analfabetismo das pessoas de 15 anos ou mais'); a pergunta do questionario nao esta nos arquivos baixados | `bruto/meta/sidra_meta_*.json` |")
A("")
A("A diferenca de -1,40 p.p. entre PNADC e Censo em 2022 (quebra 2) e a unica medida, no mesmo ano, de quanto a pesquisa amostral se afasta do recenseamento nesta pergunta; a definicao de 'alfabetizado' do IBGE nao foi lida em documento do questionario, entao nao atribuo a diferenca a ela.")
A("")
A("## 5. O que nao tem serie comparavel (evidencia da busca)")
A("")
A("| Dominio | Candidato | Onde procurei | O que apareceu | Conclusao |")
A("| --- | --- | --- | --- | --- |")
for r in busca:
    A((f"| {r['dominio']} | {r['indicador_candidato']} | {r['onde_procurado']} ({r['termo']}) | {r['o_que_apareceu'][:240]} | {r['conclusao']} |").replace("|", "/").replace("/ ", "| ", 0) if False else "| " + " | ".join(c.replace("|", "/") for c in (r['dominio'], r['indicador_candidato'], f"{r['onde_procurado']} ({r['termo']})", r['o_que_apareceu'][:240], r['conclusao'])) + " |")
A("")
A("Fora dessas linhas: a lista de 'cultura' do Ipeadata so tem a funcao 'educacao e cultura' somada (DFEDUCE/DFEDUCM) e so estadual/municipal; a funcao Cultura separada nasce na Portaria MOG 42/1999 (funcoes 13 Cultura e 27 Desporto e Lazer, `bruto/doc/portaria_mog_42_1999.odt`); DFDELE (desporto e lazer, estadual) comeca em 2002. Parei ai: nao forcei uma serie.")
A("")
A("## 6. Limiares de elegibilidade em valor real (R$ de dez/2025, IPCA)")
A("")
A("| Vigencia | Instrumento | Pobreza nominal | Extrema pobreza nominal | Pobreza real | Extrema real |")
A("| --- | --- | --- | --- | --- | --- |")
for r in ev:
    A(f"| {r['data_vigencia']} | {r['instrumento']} | {r['linha_pobreza_nominal']} | {r['linha_extrema_pobreza_nominal'] or '-'} | {float(r['linha_pobreza_real_dez2025']):.0f} | {float(r['linha_extrema_pobreza_real_dez2025']):.0f} |" if r['linha_extrema_pobreza_real_dez2025'] else
      f"| {r['data_vigencia']} | {r['instrumento']} | {r['linha_pobreza_nominal']} | - | {float(r['linha_pobreza_real_dez2025']):.0f} | - |")
A("")
A("BPC: idade minima do idoso 70 anos (texto original, 1996), 67 desde 1/1/1998 (Lei 9.720/1998, art. 38), 65 desde o Estatuto do Idoso (Lei 10.741/2003, art. 34, vigencia 2004). Renda familiar per capita: 1/4 do salario minimo no texto original (art. 20, par. 3); Lei 13.981/2020 traz 1/2; Lei 14.176/2021 volta a 1/4 com possibilidade de ampliar ate 1/2 por regulamento; o texto compilado remete a ADPF 662 (aplicacao efetiva nao verificada). Valores reais anuais em `series/ass.csv` (`ass_bpc_limiar_quarto_sm_real`, `ass_bpc_limiar_meio_sm_real`).")
A("")
A("## 7. Quebras (resumo; texto completo em `quebras.csv`)")
A("")
A("| # | Indicador | Quebra | Tipo | Direcao | Efeito medido |")
A("| --- | --- | --- | --- | --- | --- |")
for i, r in enumerate(que, 1):
    A(f"| {i} | {r['indicador']} | {r['data_quebra']} | {r['tipo_de_quebra']} | {r['direcao_do_efeito']} | {r['efeito_medido'][:150]} |")
A("")
A("## 8. Decisoes fixas e anomalias (para o leitor poder refazer)")
A("")
A("- **BPC_defi 2016 = 74** no Ipeadata (2015 = 2.323.808; 2017 = 2.527.257). Mantido na serie como publicado, marcado `ANOMALIA`, fora das janelas. Nao corrigi.")
A("- **SINASC:** 1994 tem 100% de 'ignorado' (fora). Anos com mais de 10% de nascimentos com numero de consultas ignorado (1995 a 1998) ficam na serie e fora das janelas; 2025 e preliminar e tambem fica fora. Limite de 10% fixado antes de ver o efeito nas medias.")
A("- **Saeb:** os valores sao rotulos de grafico, arredondados a inteiro; o proprio INEP informa o erro amostral da media nacional de 2023 na 3a serie do ensino medio: 1,0 ponto em Lingua Portuguesa e 1,3 em Matematica (Relatorio Saeb 2023 vol. 1). Diferencas de 1-2 pontos entre edicoes nao sao distinguiveis de ruido de amostra.")
A("- **PNADC:** os indicadores anuais de educacao, agua e esgoto nao existem para 2020 e 2021 nas tabelas baixadas (coleta por telefone).")
A("- **PDIAE (Ipea):** os pontos de 2000, 2010 e 2022 batem com o meu recalculo a partir do SIDRA (diferenca <= 0,01 p.p.); o ponto de 1991 (Atlas 1998) nao bate (quebra 17). Por isso a serie primaria de esgoto e o recalculo do SIDRA e o PDIAE entra como extensao 1970-1991.")
A("- **Censos 1970/1980 de agua e luz** nao foram achados em tabela nacional comparavel (so contagens de domicilios 1940-1960 no Ipeadata, baixadas e nao usadas por cairem antes de 1964).")
A("- **Anos de estudo:** so ha Censos 1991 e 2000 (Ipea/PNUD, 25+) e PNADC 2016+ (15+): sem serie de 30 anos. Conclusao por idade (por exemplo, 19 anos com ensino medio) nao foi coletada: nao localizei tabela agregada nacional com metodo unico.")
A("")
A("## 9. Becos (evidencia negativa, para ninguem repetir)")
A("")
for b in ("`seriesestatisticas.ibge.gov.br` devolve a tela de verificacao do Cloudflare (403); `agenciadenoticias.ibge.gov.br` barra a leitura direta e as URLs de noticia testadas deram 404 (pagina do Censo 2022 sobre analfabetismo nao lida).",
          "`download.inep.gov.br`: o `urllib` do manifest_tool falha na verificacao do certificado; resolvido com `curl` + `add-local` (nota na linha do manifest). Planilhas do Ideb e das taxas de rendimento: 404 em todas as URLs tentadas; paginas gov.br/inep carregam o conteudo por JavaScript.",
          "`.odt` do gov.br so baixa com `/@@download/file` no fim da URL; a URL sem isso devolve HTML.",
          "SIDRA devolve gzip sem ser pedido (o bruto guardado e o gzip exato); o filtro `$filter` do Ipeadata e ignorado (o arquivo vem inteiro, com todos os niveis territoriais; filtro de nivel Brasil e feito no codigo).",
          "TabNet/DATASUS so por POST (fora do `add`); `old.scielo.br` falha no certificado, `www.scielo.br` serve o mesmo PDF.",
          "Nao localizados: texto oficial da Deliberacao CEE 9/97 e da Resolucao SE 4/98 (SP); documento 'Consolidacao do SINASC 2011'; relatorios da FJP; microdados PNAD 1981-1999 (rendimento nacional so 1996-2006, tabela 427, sem 2000).",
          "O catalogo Ipeadata local nao lista a PNAD antiga de rendimento (ela esta no SIDRA); busca so por palavra no catalogo perdeu essa serie na primeira passada."):
    A("- " + b)
A("")
A("## 10. Inventario do que foi entregue")
A("")
A("| Arquivo | Conteudo |")
A("| --- | --- |")
for a, c in (("series/edu.csv, mor.csv, tbl.csv, pre.csv, ass.csv, mat.csv", "formato longo: indicador, fonte, definicao_linha, ano, valor, unidade, nota, vintage, dependente_de_regra"),
             ("series/limiares_eventos.csv", "cada decreto/lei dos limiares do PBF com valor nominal e real"),
             ("janelas.csv", "indicador, governo, inicio, fim, media, valor_inicial, valor_final, n_anos, segmento_metodo"),
             ("quebras.csv", "uma linha por quebra, com tipo_de_quebra, trecho citado e fonte primaria"),
             ("busca-sem-serie.csv", "evidencia da busca onde nao ha serie comparavel"),
             ("manifest.jsonl, bruto/, recalcula.py, resultado.py, scripts/, baixar-lote*.sh", "cadeia de hash, brutos, codigo e roteiros de download")):
    A(f"| `{a}` | {c} |")
open(os.path.join(AQUI, "RESULTADO.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print("RESULTADO.md:", len(md), "linhas")
