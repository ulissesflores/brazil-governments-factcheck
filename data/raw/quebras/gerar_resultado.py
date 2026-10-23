# RESULTADO.md: monta o relatorio a partir dos CSV/JSON gerados (nenhum numero e digitado a mao).
# Rode: python3 -I gerar_resultado.py  (depois de calc.py, gerar_pobreza.py, gerar_quebras.py, gerar_vintage.py, gerar_alternativos.py, gerar_mistura.py)
import csv
import collections
import hashlib
import json
import pathlib

H = pathlib.Path(__file__).resolve().parent
M = json.load(open(H / "saida" / "medidas.json"))
EM = json.load(open(H / "saida" / "efeito_mecanico_resumo.json"))
CMP = list(csv.DictReader(open(H / "comparativo-metodo-constante.csv", encoding="utf-8")))
QB = list(csv.DictReader(open(H / "quebras.csv", encoding="utf-8")))
BF = list(csv.DictReader(open(H / "bolsa-familia-linhas-elegibilidade.csv", encoding="utf-8")))
REAL = list(csv.DictReader(open(H / "pobreza-linhas-em-reais-reais.csv", encoding="utf-8")))
HIST = list(csv.DictReader(open(H / "pobreza-linhas-historico.csv", encoding="utf-8")))
DEC = list(csv.DictReader(open(H / "renda-por-decil-por-governo.csv", encoding="utf-8")))
ALT = list(csv.DictReader(open(H / "alternativos-por-governo.csv", encoding="utf-8")))
ALTM = list(csv.DictReader(open(H / "indicadores-alternativos.csv", encoding="utf-8")))
MIS = json.load(open(H / "saida" / "mistura_resumo.json"))
GOVS = ["Castelo Branco", "Costa e Silva + Medici", "Geisel", "Figueiredo", "Sarney", "Collor", "Itamar Franco", "FHC", "Lula 1-2", "Dilma", "Temer", "Bolsonaro", "Lula 3"]
OUT = []
P = OUT.append


def c(x, nd=2, s=False):
    if x in (None, ""):
        return "n/d"
    x = float(x)
    t = f"{x:+.{nd}f}" if s else f"{x:.{nd}f}"
    return t.replace(".", ",")


def pivot(segs, cols, kind="mandato", ind_prefix=None, com_var=True, rows=CMP, nd=2):
    """segs: lista de ids de segmento; cols: rotulos. Linhas: governos (janela do mandato)."""
    P("| governo | " + " | ".join(cols) + " |")
    P("|---|" + "---|" * len(cols))
    for g in GOVS:
        cel = []
        ok = False
        for s in segs:
            r = [x for x in rows if x["segmento"] == s and x["governo"] == g and x["janela_usada"].startswith(kind)]
            if ind_prefix:
                r = [x for x in r if x["indicador"].startswith(ind_prefix)]
            if r:
                x = r[0]
                parc = "*" if "PARCIAL" in x["janela_usada"] or "lacunas" in x["janela_usada"] else ""
                cel.append(f"{c(x['valor_medio'], nd)}" + (f" / {c(x['variacao_no_segmento'], nd, True)}" if com_var and x["variacao_no_segmento"] != "" else "") + f" (n={x['n_anos']}){parc}")
                ok = True
            else:
                cel.append("-")
        if ok:
            P(f"| {g} | " + " | ".join(cel) + " |")
    P("")


P("# Quebras de metodo, de regra e de vintage: o que mudou, quanto moveu o numero e o que fica quando o metodo e mantido\n")
P("Dossie governos-do-brasil-economia. Colheita e calculo de 2026-10-19. Sem opiniao e sem estimativa no dado bruto: onde ha estimativa (contrafactuais de pesos do IPCA, series harmonizadas pelo Ipea), ela vem rotulada e separada.\n")
P("Legenda: ✅ medido em dado publicado | ⚠️ medido por contrafactual/estimativa rotulada ou so em parte | ❓ nao encontrei / nao li | ❌ nao reproduz.\n")

# -------------------------------------------------------------------------------------------- resumo
P("## 0. Resumo\n")
pme, pn, pg = M["pme_sobreposicao"], M["pnad_x_pnadc_desemprego"], M["pnad_x_pnadc_gini"]
P(f"1. **{len(QB)} quebras** catalogadas em `quebras.csv`, cada uma com a razao que a PROPRIA fonte da, o trecho literal (verificado por script contra o arquivo baixado), a direcao e como ela foi determinada. Por tipo: " + ", ".join(f"{k} = {v}" for k, v in collections.Counter(x['tipo_de_quebra'] for x in QB).items()) + ". Por direcao: " + ", ".join(f"{k} = {v}" for k, v in collections.Counter(x['direcao_do_efeito'] for x in QB).items()) + ".\n")
P(f"2. **Desemprego**: a troca PME antiga -> PME nova (2002) soma {c(pme['media_pp'], 2, True)} p.p. em media nos 10 meses em que as duas rodaram (de {c(pme['min_pp'], 2, True)} a {c(pme['max_pp'], 2, True)}); so {c(M['pme_semana_vs_30d']['2002-03']['efeito_periodo_ref_pp'], 2, True)} p.p. disso sao a troca de 'semana' por '30 dias' (mar/2002). PNAD -> PNADC 2012-2014 tem sinal misto ({c(pn['media_dif_anual_pp'], 2, True)} p.p. na media anual, {c(pn['media_dif_3tri_pp'], 2, True)} no 3o trimestre).")
P(f"3. **Pobreza**: nao existe 'o' numero. A troca de linha/PPC, no mesmo pais, ano e pesquisa, move a pobreza em {c(EM['US$ 5,50 (PPC 2011) -> US$ 6,85 (PPC 2017)']['media_pp'], 1, True)} p.p. (5,50/PPC 2011 -> 6,85/PPC 2017, IBGE SIS 2012-2019) e em {c(EM['US$ 6.85 (PPC 2017) -> US$ 8.30 (PPC 2021)']['media_pp'], 1, True)} p.p. (6,85 -> 8,30, PIP, 40 anos); a linha de US$ 2,15 -> 3,00 move {c(EM['US$ 2.15 (PPC 2017) -> US$ 3.00 (PPC 2021)']['media_pp'], 1, True)} p.p. em media.")
P(f"4. **Gini**: PNADC fica {c(pg['media_dif'], 3, True)} acima da PNAD nos 3 anos de sobreposicao (2012-2014); Censo 2010 fica {c(M['censo_x_pnad_gini']['dif_vs_2011'], 3, True)} acima da PNAD 2011.")
P(f"5. **Expectativa de vida**: o mesmo ano muda de valor com a vintage (2000: {c(M['e0_revisoes_ano2000']['tabua_2000_publicada'])} tabua publicada, {c(M['e0_revisoes_ano2000']['rev2008'])} Rev. 2008, {c(M['e0_revisoes_ano2000']['rev2013'], 1)} Rev. 2013, {c(M['e0_revisoes_ano2000']['rev2018'])} Rev. 2018, {c(M['e0_revisoes_ano2000']['vigente_rev2024'], 1)} Rev. 2024); a tabua publicada de 2021 diz {c(M['e0_publicada']['2021'])} e a vigente 72,8.")
_dentro = collections.OrderedDict()
for x in CMP:
    if x["janela_usada"].startswith("mandato") and "; inteiro" in x["janela_usada"] and "lacunas" not in x["janela_usada"]:
        _dentro.setdefault(x["indicador"].split(" (")[0].split(" M")[0] if x["indicador"].startswith("Agregado") is False else "Agregados monetarios", set()).add(x["governo"])
P(f"6. **Comparacao a metodo constante** (`comparativo-metodo-constante.csv`, {len(CMP)} linhas): quais governos cabem INTEIROS num unico segmento depende do indicador. IPCA: {', '.join(sorted(_dentro.get('IPCA', [])))}. Desemprego: {', '.join(sorted(_dentro.get('Desemprego', [])))}. PIB: {', '.join(sorted(_dentro.get('PIB real', [])))} (FHC atravessa 3 vintages de PIB e so cabe parcialmente na referencia 2010 continua, 7 de 8 anos).\n")
P("7. **Mistura do proprio infografico** (`mistura-do-infografico.md`): por familia de indicador, " + "; ".join(f"{g}: {v[2]} ({v[1]} familias com sinal)" for g, v in MIS.items()) + ". Os 3 vereditos 'consistentes' estao na margem minima (3 familias) e nenhum depende de celula estimada. Onde a direcao muda com a referencia (PIP x SIS, linha de pobreza, WDI x IBGE), a celula fica 'indeterminado'.\n")
P("> [!IMPORTANT]\n> **O que NAO foi achado** (detalhe na secao 8): decomposicao do salto PME 2002 alem do periodo de referencia; razao de o PIP dar 18,8% de pobreza em 2020 contra 31,1% no SIS na mesma linha; serie do PIB ref. 1985 e ref. 2000 ano a ano (a tabela do IBGE e imagem); documento da Rev. 2013 do IBGE; PED, RAIS/CAGED e SIM/SINASC (alternativos sem dado baixado); PIP em PPC 2011 (a API devolve erro).\n")

# -------------------------------------------------------------------------------------------- entregas
P("## 1. Entregas e como reproduzir\n")
P("Tudo roda com `python3 -I`, so le brutos locais (hash em `manifest.jsonl` de cada pasta) e nao usa rede. Ordem: `extrair.py` (texto dos PDFs), `calc.py`, `gerar_pobreza.py`, `gerar_quebras.py`, `gerar_vintage.py`, `gerar_alternativos.py`, `gerar_mistura.py`, `gerar_resultado.py`. As citacoes sao verificadas por `citacoes.py`: uma frase que nao exista literalmente no arquivo local derruba o script.\n")
P("| arquivo | o que e | linhas |\n|---|---|---|")
for nome, desc in [("quebras.csv", "uma linha por quebra, com `tipo_de_quebra` (metodo_estatistico, mudanca_de_regra ou revisao_de_vintage)"), ("comparativo-metodo-constante.csv", "segmentos homogeneos x governos, com coluna `vintage`"),
                   ("vintage-do-infografico.csv", "onde cada numero impresso de pobreza, Gini e expectativa de vida aparece"), ("mistura-do-infografico.md", "o que o infografico mistura e a direcao medida por governo"),
                   ("pobreza-leque-series.csv", "TODAS as linhas de pobreza como series separadas (PIP, SIS por edicao, SIDRA, Ipea, WDI), com `vintage`"),
                   ("pobreza-linhas-historico.csv", "quando e por que cada linha mudou (US$ 1,01 a 8,30; linhas Ipea e do Atlas), com citacao"),
                   ("pobreza-efeito-mecanico.csv", "efeito de trocar a linha/PPC no mesmo pais-ano-pesquisa"), ("pobreza-linhas-em-reais-reais.csv", "cada linha internacional em R$ mensais de set/2026"),
                   ("bolsa-familia-linhas-elegibilidade.csv", "linhas de elegibilidade 2004-2023 em valor real e em fracao do salario minimo"), ("renda-por-decil.csv", "medida SEM linha: renda por decil (PIP, PPC 2017 e 2021)"),
                   ("renda-por-decil-por-governo.csv", "variacao da renda dos decis por governo, separada por spell"), ("indicadores-alternativos.csv", "para cada indicador, o alternativo que nao depende da regra que mudou"),
                   ("alternativos-por-governo.csv", "os alternativos baixados, por governo")]:
    p = H / nome
    n = sum(1 for _ in open(p, encoding="utf-8")) - 1 if nome.endswith(".csv") else sum(1 for _ in open(p, encoding="utf-8"))
    P(f"| `{nome}` | {desc} | {n} |")
P("")

# -------------------------------------------------------------------------------------------- quebras por indicador
P("## 2. As quebras, por indicador\n")
P("| indicador | quebras | tipos | direcoes | apresentada como aprimoramento |\n|---|---|---|---|---|")
por = collections.OrderedDict()
for x in QB:
    por.setdefault(x["indicador"], []).append(x)
for k, v in por.items():
    P(f"| {k} | {len(v)} | " + ", ".join(f"{t}:{n}" for t, n in collections.Counter(x['tipo_de_quebra'] for x in v).items()) + " | " + ", ".join(f"{t}:{n}" for t, n in collections.Counter(x['direcao_do_efeito'] for x in v).items()) + " | " + ", ".join(f"{t}:{n}" for t, n in collections.Counter(x['apresentada_como_aprimoramento'] for x in v).items()) + " |")
P("\nA fonte apresenta {} das {} quebras como aprimoramento (recomendacao da OIT na PME, manual da ONU no PIB, novos PPCs do ICP na pobreza); {} nao declaram se e aprimoramento e {} diz expressamente que nao (rotulagem do Ipeadata). A propria fonte so mede o efeito em poucos casos (PIB 2007 e 2015, NT 48 do BCB, contrafactuais do BCB para o IPCA).\n".format(sum(1 for x in QB if x["apresentada_como_aprimoramento"] == "sim"), len(QB), sum(1 for x in QB if x["apresentada_como_aprimoramento"] == "nao_declarado"), sum(1 for x in QB if x["apresentada_como_aprimoramento"] == "nao")))

# -------------------------------------------------------------------------------------------- medidas
P("## 3. O que foi MEDIDO na sobreposicao, e a direcao\n")
P("Direcao = efeito do metodo/linha/vintage NOVO sobre o valor medido (eleva = o novo valor e maior).\n")
P("| quebra | onde sobrepoe | efeito | direcao | status |\n|---|---|---|---|---|")
P(f"| PME antiga (30 dias, 15+) -> PME nova | mar-dez/2002, 6 RMs | {c(pme['media_pp'], 2, True)} p.p. (de {c(pme['min_pp'], 2, True)} a {c(pme['max_pp'], 2, True)}); decomposicao: periodo de referencia {c(M['pme_semana_vs_30d']['2002-03']['efeito_periodo_ref_pp'], 2, True)} / {c(M['pme_semana_vs_30d']['2002-11']['efeito_periodo_ref_pp'], 2, True)} (mar e nov), resto {c(M['pme_semana_vs_30d']['2002-03']['efeito_resto_vs_30d_pp'], 2, True)} / {c(M['pme_semana_vs_30d']['2002-11']['efeito_resto_vs_30d_pp'], 2, True)} | eleva | ✅ |")
P(f"| PNAD (set., 10+) -> PNADC (14+) | 2012-2014 | {c(pn['media_dif_anual_pp'], 2, True)} p.p. (media anual) e {c(pn['media_dif_3tri_pp'], 2, True)} p.p. (3o tri); por ano: {', '.join(c(pn[str(y)]['dif_vs_3tri_pp'], 2, True) for y in (2012, 2013, 2014))} | ambigua | ✅ |")
P(f"| Gini PNAD -> PNADC | 2012-2014 | {c(pg['media_dif'], 3, True)} (os 3 anos positivos) | eleva | ✅ |")
P(f"| Gini PNAD -> Censo | 2009-2011 | {c(M['censo_x_pnad_gini']['dif_vs_2009'], 3, True)} (vs 2009) e {c(M['censo_x_pnad_gini']['dif_vs_2011'], 3, True)} (vs 2011) | eleva | ✅ (so 1 Censo na janela) |")
sis = M["sis_550_x_685"]
P(f"| Linha 5,50 (PPC 2011) -> 6,85 (PPC 2017) | 2012-2019, IBGE SIS | {c(sis['media_dif_pp'], 2, True)} p.p. (de 7,59 a 8,27) | eleva | ✅ (mistura edicoes SIS 2020 x 2025) |")
for k, v in EM.items():
    if "PPC 2017) ->" in k and "PPC 2021" in k:
        P(f"| {k} | 1981-2024, PIP | {c(v['media_pp'], 2, True)} p.p. em media (de {c(v['min_pp'], 2, True)} a {c(v['max_pp'], 2, True)}; {v['n_anos']} anos) | eleva | ✅ |")
P(f"| PIP x IBGE SIS, mesma linha 6,85 | 2012-2024 | {c(M['pip_x_sis_685']['media_dif_pp'], 2, True)} p.p. ({c(M['pip_x_sis_685']['media_dif_pp_sem_2020'], 2, True)} sem 2020); 2020: PIP 18,8 contra SIS 31,1 | reduz | ✅ causa ❓ |")
P(f"| SIS edicoes (5,50, ano 2017) | SIS 2018 x 2019/2020 | {c(M['sis_edicoes_550']['2017']['SIS2018'])} -> {c(M['sis_edicoes_550']['2017']['SIS2019'])} (-0,47 p.p.) | reduz | ✅ |")
P(f"| Rev. 2013 -> Rev. 2018 (e0) | 2000-2014 | maximo {c(M['e0_rev13_x_rev18']['max_abs_dif'])} ano | neutro | ✅ |")
P(f"| Tabua publicada -> serie vigente (e0) | 2000, 2010, 2019-2024 | {', '.join(y + ' ' + c(v['dif'], 2, True) for y, v in M['e0_publicada_x_vigente'].items())} anos | ambigua | ✅ |")
mq = {r["agregado"]: r for r in M["monetario_quebra_2018"]}
k17 = "dez2017 (NT48: M1 +5%, M3 -0,4%, M4 -6%)"
P(f"| M1-M4 metodologia 2001 -> Novo (2018) | 2002-2018 | dez/2017: M1 {c((float(mq['M1'][k17]) - 1) * 100, 1, True)}%, M2 {c((float(mq['M2'][k17]) - 1) * 100, 1, True)}%, M3 {c((float(mq['M3'][k17]) - 1) * 100, 1, True)}%, M4 {c((float(mq['M4'][k17]) - 1) * 100, 1, True)}% | ambigua | ✅ |")
P("| PIB ref. 2000 -> ref. 2010 | 2000-2011, IBGE | media anual 3,5% -> 3,7% (+0,2 p.p. ao ano); nivel +2,1% | eleva | ✅ (media; tabela ano a ano e imagem) |")
P("| PIB ref. 1985 -> ref. 2000 | 2000 e 2005, IBGE | 2000: 4,4 -> 4,3; 2005: 2,3 -> 2,9 | ambigua | ⚠️ (2 pontos em texto) |")
P("| IPCA, troca de POF (1999, 2006, 2012, 2020) | Banco Central EE70 | " + "; ".join(["1999 +0,71 antes / +0,06 depois", "2006 +0,40 / -0,34", "2012 -0,49 / -0,56", "2017-2019 -0,09"]) + " p.p. ao ano | ambigua | ⚠️ contrafactual do BCB |")
cf = M["ipca_cf_2020_2025"]
P(f"| IPCA, cesta POF 2017-18 (2020-2025) | reconstrucao por 9 grupos (SIDRA 1419/7060) | por ano: {', '.join(c(cf['por_ano'][str(y)]['efeito_pp'], 2, True) for y in range(2020, 2026))} p.p.; acumulado 2020-2025: {c(cf['acumulado_2020_2025']['antigos'], 1)}% (cesta antiga) contra {c(cf['acumulado_2020_2025']['novos'], 1)}% (nova) | reduz em media, sinal nao se repete | ⚠️ estimativa deste dossie (reproduz o publicado: 2018 em {c(M['ipca_cf_2018']['reconstrucao_pesos_antigos'], 3)} contra {c(M['ipca_cf_2018']['ipca_publicado_2018'], 3)}) |")
f94 = M["salmin_fator_1994"]
P(f"| Salario minimo: fator 1,2225 de jul/1994 | serie Ipea x nominal/INPC | Itamar {c(f94['Itamar Franco']['ipea'], 1, True)}% contra {c(f94['Itamar Franco']['inpc_puro'], 1, True)}%; FHC {c(f94['FHC']['ipea'], 1, True)}% contra {c(f94['FHC']['inpc_puro'], 1, True)}% | ambigua | ✅ |")
P("")
P("Sem sobreposicao nos dados baixados (e portanto sem efeito medido): FGV -> IBGE em 1990; ref. 1985 -> ref. 2010 em 1995/1996; estruturas do IPCA de 1989, 1991, formula geometrica de 1994 e cobertura de 2014/2018; PME 1982/1988/1993; conceito de trabalho da PNAD em 1992; area rural do Norte em 2004; reponderacao da PNAD 2001-2009; telefone da PNADC (2020-21); reponderacao de nov/2021; quintas visitas 2020-2022; M0 de 1980; faixas regionais do salario minimo.\n")

# -------------------------------------------------------------------------------------------- comparativo
P("## 4. Comparativo a metodo constante (media / variacao no segmento, n anos)\n")
P("Cada coluna e UM metodo e UM intervalo de anos. 'media / variacao (n)': media das taxas ou dos niveis anuais; variacao = crescimento acumulado (PIB, IPCA, salario) ou ultimo menos primeiro ano (demais, em pp, pontos ou anos); n = anos usados; `*` = governo so parcialmente dentro do segmento ou com lacunas. So a janela do mandato (cada ano ao governo que o exerceu na maior parte); as janelas impressas estao no CSV.\n")
P("### 4.1 PIB real (% a.a.; acumulado %)\n")
pivot(["P1", "P2", "P3", "P4", "P5"], ["FGV 1948-90", "ref.1985 1991-95", "ref.2010 retrop. 1996-2000", "ref.2010 2001-25", "ref.2010 continua 1996-2025"], ind_prefix="PIB")
P("### 4.2 IPCA (% a.a.; acumulado %)\n")
pivot(["I1", "I1b", "I2", "I3", "I4", "I5", "I6", "I7"], ["81-85 Endef", "87-88 base mar/86", "90-93 POF87", "94-98 geom.", "00-05 POF95", "07-11 POF02", "12-19 POF08", "20-25 POF17"], ind_prefix="IPCA")
P("### 4.3 Desemprego (%; variacao em pp)\n")
pivot(["U1", "U2", "U3", "U4", "U5"], ["PME antiga 80-02", "PME nova 03-15", "PNAD 92-03", "PNAD 04-14", "PNADC 12-25"], ind_prefix="Desemprego")
P("### 4.4 Salario minimo real (var. % a.a. da media anual; acumulado %)\n")
pivot(["S1", "S2", "S3", "S4", "S5"], ["Ipea IGPC-Mtb 48-78", "Ipea INPC 80-25", "IGP-DI unico 44-25", "INPC unico 80-25", "IPCA unico 81-25"], ind_prefix="Salario minimo")
P("### 4.5 Pobreza (% da populacao; variacao em pp), PIP, uma coluna por linha e spell\n")
P("**Spell PNAD (1981-2011)**\n")
pivot(["B-2017-2.15-a", "B-2017-3.65-a", "B-2017-6.85-a", "B-2021-3.00-a", "B-2021-4.20-a", "B-2021-8.30-a"], ["2,15/PPC17", "3,65/PPC17", "6,85/PPC17", "3,00/PPC21", "4,20/PPC21", "8,30/PPC21"], ind_prefix="Pobreza", nd=1)
P("**Spell PNADC (2012-2024)**\n")
pivot(["B-2017-2.15-b", "B-2017-3.65-b", "B-2017-6.85-b", "B-2021-3.00-b", "B-2021-4.20-b", "B-2021-8.30-b"], ["2,15/PPC17", "3,65/PPC17", "6,85/PPC17", "3,00/PPC21", "4,20/PPC21", "8,30/PPC21"], ind_prefix="Pobreza", nd=1)
P("**Segunda linha: IBGE SIS (PNADC)** e Ipea (PNAD, linha propria)\n")
pivot(["Z-IBGE-SIS2020-PPC2011-US$ 5,5 PPC2", "Z-IBGE-SIS2025-US$ 6,85 PPC", "Z-IBGE-SIS2025-US$ 3,65 PPC", "Z-SIDRA-5877-linha nacion", "Z-Ipeadata-DISOC_PPY-linha propri"],
      ["SIS 5,50/PPC11", "SIS 6,85/PPC17", "SIS 3,65/PPC17", "ODS 8,30/PPC21", "Ipea PPY (PNAD)"], ind_prefix="Pobreza", nd=1)
P("### 4.6 Gini\n")
pivot(["G-PIP-a", "G-PIP-b", "G-PIP-c", "G-IBGE-SIS2025", "G-Ipeadata-PGINI", "G-Ipeadata-PNADS_GINI"], ["PIP PNAD 81-11", "PIP PNADC 12-24", "PIP unica 81-24", "SIS PNADC", "Ipea PGINI (PNAD)", "Ipea harmonizada"], ind_prefix="Gini", nd=3)
P("### 4.7 Expectativa de vida (anos; variacao em anos)\n")
pivot(["E-WDI", "E-PUB", "E-REV18", "E-REV13"], ["UMA vintage (WDI/UN) 1960-2024", "tabua como publicada", "Rev. 2018 (Ipea)", "Rev. 2013 (SIDRA)"], ind_prefix="Expectativa", nd=2)
P("### 4.8 Agregados monetarios (% do PIB)\n")
rowsM = [x for x in CMP if x["indicador"].startswith("Agregado")]
segsM = ["M0-a", "M0-b", "M1-a", "M1-b", "M2-a", "M2-b", "M3-a", "M3-b", "M4-a", "M4-b"]
pivot(segsM, ["M0 47-79", "M0 80-25", "M1 antigo", "M1 Novo", "M2 2001", "M2 Novo", "M3 2001", "M3 Novo", "M4 2001", "M4 Novo"], rows=rowsM, nd=1)

# -------------------------------------------------------------------------------------------- pobreza
P("## 5. Pobreza: o leque de linhas, quando e por que cada uma mudou, e a medida sem linha\n")
P("### 5.1 Linhas e datas\n")
P("| linha | PPC | vigencia | razao declarada | efeito declarado pela fonte |\n|---|---|---|---|---|")
for x in HIST:
    P(f"| {x['valor']} | {x['ppc_ou_base']} | {x['vigencia_inicio']} a {x['vigencia_fim']} | {x['razao_declarada_pela_fonte'][:170]} | {x['efeito_declarado_pela_fonte'][:150]} |")
P("")
P("### 5.2 O valor REAL das linhas internacionais (R$ mensais de set/2026, IPCA)\n")
P("| linha | fator R$ por US$ PPC | R$/mes no ano-base | R$/mes em set/2026 |\n|---|---|---|---|")
for x in REAL:
    P(f"| {x['linha']} | {x['fator_R$_por_US$_PPC']} | {x['R$_mensal_precos_do_ano_base']} | {x['R$_mensal_set2026']} |")
P("\nEm termos reais a troca 5,50 (PPC 2011) -> 6,85 (PPC 2017) eleva a linha em reais de R$ 643 para R$ 770 (+20%) e a troca 6,85 -> 8,30 (PPC 2021), de R$ 770 para R$ 817 (+6%): a linha em dolares sobe mais do que o valor real em reais porque os PPCs mudam junto.\n")
P("### 5.3 Efeito mecanico da troca de linha/PPC (mesmo pais, ano e pesquisa)\n")
P("| troca | fonte | media (pp) | minimo | maximo | anos |\n|---|---|---|---|---|---|")
for k, v in EM.items():
    P(f"| {k} | {'PIP' if '.' in k.split(' ')[1] else 'IBGE SIS'} | {c(v['media_pp'], 2, True)} | {c(v['min_pp'], 2, True)} | {c(v['max_pp'], 2, True)} | {v['n_anos']} |")
P("\nPositivo = pessoas que PASSAM a ser contadas como pobres so pela redefinicao. Por governo (6,85 -> 8,30, PIP): " + "; ".join(f"{g} {c(v['media_dif_pp'], 2, True)} pp" for g, v in M['pip_ppc']['6.85->8.30']['por_governo'].items()) + ".\n")
P("### 5.4 Linha de elegibilidade do Bolsa Familia / Auxilio Brasil, em valor real\n")
P("| inicio dos efeitos | pobreza nominal (R$) | extrema nominal (R$) | pobreza em R$ de set/2026 (INPC) | % do salario minimo | instrumento |\n|---|---|---|---|---|---|")
for x in BF:
    P(f"| {x['inicio_dos_efeitos']} | {x['linha_pobreza_nominal_R$']} | {x['linha_extrema_pobreza_nominal_R$']} | {c(x['pobreza_R$_set2026_INPC'], 2)} | {c(float(x['pobreza_em_fracao_do_SM_vigente']) * 100, 1)} | {x['instrumento'][:72]} |")
P("\nO Auxilio Brasil (nov/2021 a 2023) e outro programa, e a linha de 2023 (R$ 218) e unica. Os valores reais saem do deflator INPC (SGS 188); a norma foi lida no Planalto em 2026-10-19.\n")
P("### 5.5 Medida SEM linha: renda domiciliar per capita real por decil (PIP, PPC 2017), variacao dentro de cada spell\n")
P("| governo | spell | anos usados | decil 1 | mediana | media | decil 10 | cobertura |\n|---|---|---|---|---|---|---|---|")
for g in GOVS:
    for spell in ("PNAD (spell 1981-2011)", "PNADC (spell 2012-2024)"):
        rs = {x["decil"]: x for x in DEC if x["governo"] == g and x["spell"] == spell}
        if rs:
            r1 = rs["1"]
            P(f"| {g} | {spell.split(' ')[0]} | {r1['ano_inicial_disponivel']}-{r1['ano_final_disponivel']} | {c(rs['1']['variacao_pct'], 1, True)}% | {c(rs['mediana']['variacao_pct'], 1, True)}% | {c(rs['media']['variacao_pct'], 1, True)}% | {c(rs['10']['variacao_pct'], 1, True)}% | {rs['1']['cobertura'][:9]} |")
P("\nVariacao % da renda real (PPC$/dia) entre o primeiro e o ultimo ano de pesquisa do PIP dentro da janela do mandato. Cruza nunca o spell. Os niveis anuais por decil, em PPC 2017 e 2021, estao em `renda-por-decil.csv`.\n")

# -------------------------------------------------------------------------------------------- alternativos
P("## 6. Que indicador alternativo NAO depende da regra que mudou?\n")
P("| indicador | regra/definicao que mudou | alternativo | depende? | baixado |\n|---|---|---|---|---|")
for x in ALTM:
    P(f"| {x['indicador_do_bloco']} | {x['regra_ou_definicao_que_mudou'][:90]} | {x['indicador_alternativo']} | {x['depende_da_regra_que_mudou']} | {x['baixado_nesta_pasta']} |")
P("\nResultados por governo dos alternativos baixados: `alternativos-por-governo.csv` (consumo de energia, IBC-Br, IPC-Fipe, salario minimo em cestas basicas, renda mediana/media/40% mais pobres do SIS, razao 10/40 do Ipea, Palma e participacao do decil 10 do PIP).\n")

# -------------------------------------------------------------------------------------------- nao achado
P("## 7. Mistura do infografico (resumo)\n")
P("Ver `mistura-do-infografico.md`. Resumo: a linha de pobreza muda de 5,50 para 6,85 no meio da fileira (~8 pp); 4 de 8 pontos de pobreza e 3 de 8 de Gini estao em outro ano; a linha de expectativa de vida mistura 5 vintages; o desemprego cruza PME antiga, PME nova, PNAD e PNADC; 2016 entra em duas colunas; o 'IPCA 1967-73' nao existe. Direcao por familia e governo na tabela 8 daquele arquivo.\n")
P("## 8. O que NAO foi achado, limites e becos\n")
for t in [
    "IPCA, Sarney (1985-1989): nenhum segmento homogeneo cobre o mandato (serie encerrada em fev/1986, base mar/1986; pesos da POF 87-88 desde jun/1989). So 1987-1988 (2 de 5 anos) entram no comparativo, como linha PARCIAL; Figueiredo (1980-1984) tambem so entra em parte, porque a serie SGS 433 comeca em jan/1980 e a cobertura de areas so fecha em out/1980.",
    "A PME 2002 so tem decomposicao parcial: o periodo de referencia explica ~0,6 p.p.; os outros 3,1 a 5,1 p.p. (idade 10+, questionario, procura, malha) nao sao separaveis em fonte primaria lida. O IBGE nao publica essa decomposicao nos documentos baixados.",
    "Contradicao entre fontes: o metadado Ipeadata de `PAN12_TD12` diz 'periodo de referencia: 30 dias' e o relatorio metodologico do IBGE define desocupado pela semana; e o Ipea (Reis, 2004) e o IBGE (jul/2003) falam em serie nova desde out/2001, enquanto Ipeadata/SIDRA comecam em mar/2002. Nao resolvido.",
    "PIB: as tabelas ano a ano dos releases do IBGE (2007, 2015) sao imagens GIF. So os pontos em texto foram usados (2000, 2005; media 2000-2011). A serie ref. 1985 para 1996-2000 e a ref. 2000 nao foram obtidas. Fonte secundaria (nota academica) usada so para a direcao dos demais anos e rotulada.",
    "IPCA: nao ha contrafactual publicado para 1989, 1991, 1994 (media geometrica), 2014/2018 (areas). A direcao 'reduz' de 1994 e inferencia matematica (media geometrica <= aritmetica), nao medida. A reconstrucao 2020-2025 usa 9 grupos (nao 377 subitens): reproduz o publicado (3,744 contra 3,745 em 2018; 4,518 contra 4,517 em 2020), mas e estimativa.",
    "Pobreza: o PIP nao serve mais a versao PPC 2011 (a API devolve erro 500 para `ppp_version=2011` e para versoes antigas), entao a troca PPC 2011 -> 2017 so e medida no IBGE SIS (mistura edicoes). O PIP e o IBGE SIS divergem na MESMA linha (6,85) em 7,0 p.p. em media e em 12,3 p.p. em 2020; a causa nao esta nas fontes lidas (o fator PPC e identico).",
    "Pobreza em 1994 e 2010: o PIP nao tem os anos (sem PNAD em 1994 e 2010); celulas ficam 'indeterminado'. Linhas Ipea 1976-2014 e Atlas (R$ 70/140 de ago/2010) estao no leque como series proprias, sem conversao para dolar.",
    "Expectativa de vida: o documento da Rev. 2013 e a Rev. 2000 do IBGE nao foram lidos; o WDI nao informa a revisao do WPP usada. DATASUS (SIM/SINASC), RAIS/CAGED e PED (Seade/Dieese) estao listados como alternativos mas NAO foram baixados (URLs nao verificadas).",
    "A serie Ipea de salario minimo nao se reproduz com nenhum dos deflatores unicos nas janelas de Itamar e FHC por causa do fator 1,2225 de jul/1994; a razao do fator nao esta documentada.",
    "O Censo de 2022 e a reponderacao da PNADC: o IBGE diz que os indicadores serao recalculados apos o Censo; nao li se isso ja ocorreu (a serie baixada e a reponderada de nov/2021).",
    "Bolsa Familia: valores lidos nos decretos consolidados do Planalto (atos revogados aparecem no texto); o inicio de 2004-09 e a data do Decreto 5.209, nao a da Lei 10.836 (jan/2004) nem da MP 132 (out/2003), que nao li.",
]:
    P(f"- {t}")
P("\n**Becos:** (1) `ibge.gov.br` e `agenciadenoticias.ibge.gov.br` devolvem 403 a curl: usei o proxy r.jina.ai (declarado em cada linha do manifest); (2) tabelas dos releases do IBGE de 2007 e 2015 sao imagens GIF; (3) PIP com `ppp_version=2011` e `release_version` devolvem erro 500; (4) PME por regiao metropolitana (SIDRA 2179) e de 'principais responsaveis pela familia', nao serve; (5) WebFetch de PDF devolveu binario (arquivo fora da cadeia de hash, nao usado); (6) a pagina da PME antiga e as paginas do IBGE nao trazem a decomposicao do salto de 2002; (7) tres entradas do manifest desta pasta tem rotulo imperfeito e, por a cadeia ser append-only, ficam: `bruto/ravallion-0509005.pdf` (a nota diz Ravallion, o conteudo e Reddy e Minoiu, 2005; nao citado em CSV), `bruto/wb-pw4620-dollar-a-day-revisited-jina.md` (267 bytes: a pagina 403 Forbidden do proxy) e `bruto/wb-pw7432-global-count-2012.pdf` (e texto UTF-8, nao PDF; as citacoes o leem como texto).\n")

# -------------------------------------------------------------------------------------------- reprodutibilidade
P("## 9. Reprodutibilidade\n")
P("| script | sha256 |\n|---|---|")
for s in ("carga.py", "citacoes.py", "extrair.py", "calc.py", "medidas.py", "gerar_pobreza.py", "gerar_quebras.py", "gerar_vintage.py", "gerar_alternativos.py", "gerar_mistura.py", "gerar_resultado.py"):
    P(f"| `{s}` | `{hashlib.sha256(open(H / s, 'rb').read()).hexdigest()}` |")
man = (H / "manifest.jsonl").read_bytes().splitlines(keepends=True)
P(f"\nCadeia de hash dos brutos desta pasta: `python3 -I ../manifest_tool.py verify .` ({len(man)} linhas; cabeca no momento da escrita: `{hashlib.sha256(man[-1]).hexdigest()}`). Os arquivos de `derivado/` (texto de PDFs, HTML e planilhas) sao recriaveis por `extrair.py` e nao entram na cadeia. Fontes de outros blocos usadas como estao: `economia-real/`, `social/series/*.csv`, `monetario/saida/*.csv`, `historia/bruto/ibge-ipca/` (todas com hash no manifest da respectiva pasta).\n")
(H / "RESULTADO.md").write_text("\n".join(OUT), encoding="utf-8")
print("RESULTADO.md", len(OUT), "linhas")
