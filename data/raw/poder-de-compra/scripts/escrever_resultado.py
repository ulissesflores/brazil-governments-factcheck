#!/usr/bin/env python3
"""Escreve ../RESULTADO.md: as tabelas saem de ../series/*.csv; o texto e fixo. python3 -I escrever_resultado.py (sem rede)."""
import csv
import math
import statistics as st
import subprocess
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
S = RAIZ / "series"
pc = defaultdict(dict)
for x in csv.DictReader(open(S / "poder_de_compra.csv")):
    pc[x["indicador"]][int(x["ano"])] = float(x["valor"])
ex = {int(r["ano"]): r for r in csv.DictReader(open(S / "excesso_monetario.csv"))}
tr = list(csv.DictReader(open(S / "trabalho.csv")))
head = subprocess.run(["python3", "-I", "/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py", "verify", str(RAIZ)], capture_output=True, text=True).stdout.strip()
f = lambda v, c=2: "" if v is None else f"{v:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")
col = lambda n: {a: (float(r[n]) if r[n] != "" else None) for a, r in ex.items()}


def corr(a, b, yrs, rank=False):
    ys = [y for y in yrs if a.get(y) is not None and b.get(y) is not None]
    xs, zs = [a[y] for y in ys], [b[y] for y in ys]
    if rank:
        r = lambda v: [sorted(v).index(x) for x in v]
        xs, zs = r(xs), r(zs)
    mx, mz = st.mean(xs), st.mean(zs)
    return sum((x - mx) * (z - mz) for x, z in zip(xs, zs)) / math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((z - mz) ** 2 for z in zs)), len(ys)


o = []
w = o.append
w("# RESULTADO: poder de compra, excesso monetario e trabalho\n")
w("Colheita de 2026-10-19. Sem opiniao, sem nota, sem ranking: so numeros, fonte e limite. Tudo sai de `python3 -I scripts/construir.py`, `scripts/quebras_gerar.py`, `scripts/bolsa_familia.py`, `scripts/pnad_microdados.py`, `scripts/escrever_md_*.py` e `scripts/escrever_resultado.py`, que leem so arquivos locais. Os brutos baixados nesta pasta entram na cadeia de hash (`manifest.jsonl`; `python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py verify .` -> " + head + "). Pre-registro: `../preregistro/PREREGISTRATION-EMENDA-01.md`, secao B, linhas \"Purchasing power\" e \"Labour\".\n")
w("Legenda: ACHADO = tem numero e fonte aqui; NAO ACHADO = procurei e nao obtive (com onde procurei).\n")

w("## 1. Resumo\n")
w("1. **ACHADO.** Cesta basica DIEESE de Sao Paulo mensal 1959-2026 (Ipeadata, ja hasheada em `../quebras/bruto/`): quantas cestas 1 salario minimo compra caiu de 3,76 (1959) para 0,95 (1994, minimo) e foi a 2,16 (2017, maximo desde 1995) e 1,76 (2025). Em horas de trabalho (220 h/mes, formula do DIEESE), de 59 h (1959) a 231 h (1994) e 125 h (2025). 1964 fica de fora: a fonte so tem janeiro e fevereiro.")
v80 = {k: pc[k][1980] for k in ("salario_minimo_real_inpc", "salario_minimo_real_ipca", "salario_minimo_real_igpdi", "salario_minimo_real_ipcfipe")}
v25 = {k: pc[k][2025] for k in v80}
icv96, inpc96 = pc["salario_minimo_dezembro_real_icv_dieese"][1996], pc["salario_minimo_dezembro_real_inpc_mesma_base_do_icv"][1996]
w(f"2. **ACHADO com ressalva.** O salario minimo real depende muito do deflator antes de 1995: em 1980, R$ {f(v80['salario_minimo_real_inpc'], 0)} (INPC), R$ {f(v80['salario_minimo_real_ipca'], 0)} (IPCA), R$ {f(v80['salario_minimo_real_igpdi'], 0)} (IGP-DI) e R$ {f(v80['salario_minimo_real_ipcfipe'], 0)} (IPC-Fipe), todos em R$ de set/2026; em 2025 as quatro ficam entre R$ {f(min(v25.values()), 0)} e R$ {f(max(v25.values()), 0)}. O ICV-DIEESE so existe de 1997 a 2019 (pesquisa suspensa em 2020-2023) e **nao encadeia**; neste intervalo o salario minimo de dezembro deflacionado por ele e pelo INPC coincide em 2019 por construcao (mesma base) e difere em 1996 (R$ {f(icv96, 1)} contra R$ {f(inpc96, 1)}).")
w("3. **NAO ACHADO.** IPC-C1 da FGV (renda baixa): a serie historica fica atras de login em `extra-ibre.fgv.br`; nao achei no catalogo do Ipeadata e nao achei codigo no SGS (testei alguns codigos, nao varri o catalogo do SGS). Em seu lugar, e **rotulado como outro indice**, o Indicador Ipea de Inflacao por Faixa de Renda (renda muito baixa e baixa), que so comeca em jul/2006.")
w("4. **ACHADO.** Excesso monetario anual 1948-2025 (crescimento de M0 e de M1 menos crescimento real do PIB, em pontos percentuais), ao lado de IGP-DI e IPCA de dezembro a dezembro. Co-movimento medido, sem causalidade: correlacao de Pearson M1-excesso x IGP-DI de 0,88 em 1948-2025, mas 0,45 em 1995-2025 (secao 4).")
w("5. **ACHADO.** PNAD Continua (2012T1-2026T2): nivel da ocupacao, participacao, desocupacao, subutilizacao e desalento, trimestrais e media anual; quatro quebras de metodo dentro da serie (2015T4, 2016T2, 2020T2, 2021). **PARCIAL**: desocupacao da PNAD de 1981-1990 nao e publicada em tabela digital, mas os microdados existem no FTP do IBGE; **calculei 6 dos 10 anos** (1981, 1982, 1984, 1985, 1986, 1988) de microdados com arquivo de ate 25 MB: 4,26%, 3,93%, 4,26%, 3,37%, 2,43% e 3,80%; 1983, 1987, 1989 e 1990 ficam em branco porque o arquivo passa de 25 MB (29, 79, 100 e 103 MB). **NAO ACHADO**: desocupacao dos Censos de 1970 e 1980 (secao 5).")
w("6. **ACHADO.** Definicoes oficiais (IBGE e OIT, com trecho literal) e resposta: receber beneficio nao muda a classificacao; ninguem cruza beneficio com forca de trabalho em tabela publicada (`definicoes.md`). A linha do Bolsa Familia nao e indexada e tem justificativa escrita minima; contra 1/4 do salario minimo ela vai de 0,77 (2004) a 0,35 (2022) (`bolsa_familia_linhas.md`).\n")

w("## 2. Poder de compra (`series/poder_de_compra.csv`)\n")
w("Formato longo: `indicador,fonte,definicao_linha,ano,valor,unidade,nota,vintage`. 19 indicadores, 929 linhas de valor. Anos completos so (12 meses). Reais atuais = moeda convertida pelo Ipeadata (cinco cortes de zeros 1967-1994); a razao salario minimo/cesta nao depende de deflator. Antes de maio/1984 o salario minimo e o MAIOR regional (fonte Ipea/MTE): a serie e um teto, nao a media.\n")
w("| ano | cestas por SM | horas por cesta | SM real INPC | SM real IPCA | SM real IGP-DI | SM real IPC-Fipe |")
w("|---|---|---|---|---|---|---|")
for y in (1959, 1963, 1970, 1974, 1980, 1985, 1990, 1994, 1995, 2002, 2010, 2014, 2017, 2022, 2025):
    g = lambda k: pc[k].get(y)
    w(f"| {y} | {f(g('cestas_por_salario_minimo'))} | {f(g('horas_de_trabalho_por_cesta'), 0)} | {f(g('salario_minimo_real_inpc'), 0)} | {f(g('salario_minimo_real_ipca'), 0)} | {f(g('salario_minimo_real_igpdi'), 0)} | {f(g('salario_minimo_real_ipcfipe'), 0)} |")
w("\nSM real = media dos 12 meses do salario minimo mensal deflacionado, em R$ de set/2026. Celula vazia = indice nao existe naquele ano (INPC desde abr/1979, IPCA desde 1980).\n")
w("Pontos de conferencia: (a) a serie INPC coincide com `../economia-real/saida-salmin-real-anual.csv` (Ipea) ate o centavo em 1980, 1990, 2000, 2010, 2020 e 2025, e em 1991-1993 e 1995-1996; em **1994** difere 1,6% (550,39 contra 541,79), por causa da conversao de moeda de julho de 1994 (`quebras.csv`). (b) O indice IGP-DI do Ipeadata tem um salto de nivel de x1,182 em jul/1994 frente as taxas mensais do SGS 190: o indice reproduz a taxa anual de 1994 (1.093,9%) e a cadeia mensal da 909,7%; mantive o do Ipeadata. (c) Nos cinco meses de corte de moeda a cesta convertida varia em linha com o IGP-DI (`series/_conferencias.txt`).\n")
w("Indicadores separados no CSV: `salario_minimo_nominal`, `cesta_basica_dieese_sp_nominal`, `cestas_por_salario_minimo`, `horas_de_trabalho_por_cesta`, `salario_minimo_real_{inpc,igpdi,ipcfipe,ipca,ipea_renda_muito_baixa,ipea_renda_baixa}`, `inflacao_dez_dez_*` (dos mesmos seis indices e do ICV-DIEESE), `salario_minimo_dezembro_real_icv_dieese` e `..._inpc_mesma_base_do_icv` (R$ de dez/2019, 1996-2019).\n")
w("Horas: formula do DIEESE (`bruto/dieese-metodologia-cesta-basica-2016.pdf`, secao 4): custo da cesta x 220 / salario minimo vigente, 220 h/mes \"desde outubro de 1988\". Aqui 220 h em todos os anos e a cesta de Sao Paulo (o DIEESE publica por capital). A cesta e a \"Racao Essencial Minima\" do Decreto-Lei 399/1938, com a quantidade de cada produto fixa; o DIEESE atualizou a pesquisa em jan/2016 (27 capitais, coleta, ponderacao).\n")

w("## 3. ICV-DIEESE e IPC-C1\n")
w("* **ICV-DIEESE**: taxas anuais de 1997-2004 (relatorio do DIEESE, tabela 2) e 2004-2019 (notas anuais), 23 anos, todas conferidas por programa contra o texto do PDF. A pagina antiga do DIEESE diz que o \"Banco de Dados\" do ICV esta \"ainda nao disponivel\"; a nova diz \"há um hiato na série histórica do ICV\" (suspensa em mar/2020, retomada em ago/2023 com ponderacao da POF 2017/18, \"impossível voltar com o índice no tempo\"). Resultado: **sem serie mensal, sem ICV antes de 1997, sem ICV depois de 2019**. 2005: 4,54% na nota de 2005 e 4,55% na de 2006 (revisao de 0,01 p.p.). A tabela de 1997-2004 vem arredondada a 0,1.")
w("* **IPC-C1 (FGV)**: definicao da propria FGV, \"mede a variação do custo de vida para famílias com renda entre 1 e 2,5 salários-mínimos mensais\", serie desde 2004; a \"Série Histórica\" leva a uma pagina de autenticacao para produtos licenciados. Procurei no catalogo do Ipeadata (4.071 series, busca por \"c1\", \"baixa renda\", \"1 a 2,5\"), em alguns codigos do SGS do BCB e na edicao de julho/2025 de \"Conjuntura Estatistica\" da FGV (sem texto de IPC-C1): **nao achei serie aberta**. Nao usei noticias de jornal como fonte.\n")

w("## 4. Excesso monetario (`series/excesso_monetario.csv`)\n")
w("Formula (declarada): `M_cresc(t) = (M_dez(t) / M_dez(t-1) - 1) x 100` com M em saldo de fim de dezembro, na mesma moeda (`../monetario/saida/anual.csv`); `excesso(t) = M_cresc(t) - PIB_real_cresc(t)`, em pontos percentuais, sem deflator. M0 = base monetaria restrita (SGS 1788); M1 = SGS 1827 (conceito antigo) ate 2017 e SGS 27791 (\"Novo\") de 2018 em diante; coluna `M1_novo_cresc_pct` traz o Novo tambem em 2003-2017. PIB real: `../economia-real/saida-pib-anual-1948-2025.csv`. IGP-DI e IPCA: variacao de dezembro a dezembro (IPCA desde 1981). Coincidencia sem importancia: o crescimento de M0 em 2018 (1,784%) e o do PIB (1,784%) tem o mesmo valor ate a terceira casa.\n")
w("| ano | M0 cresc. % | M1 cresc. % | PIB real % | excesso M0 (p.p.) | excesso M1 (p.p.) | IGP-DI dez/dez % | IPCA dez/dez % |")
w("|---|---|---|---|---|---|---|---|")
for y in (1948, 1955, 1964, 1975, 1980, 1985, 1990, 1993, 1994, 1995, 2000, 2008, 2015, 2020, 2021, 2025):
    r = ex[y]
    v = lambda k, c=1: f(float(r[k]), c) if r[k] != "" else ""
    w(f"| {y} | {v('M0_cresc_pct')} | {v('M1_cresc_pct')} | {v('pib_real_cresc_pct')} | {v('excesso_M0_pp')} | {v('excesso_M1_pp')} | {v('igpdi_dez_dez_pct')} | {v('ipca_dez_dez_pct')} |")
m1, m0, ig, ip = col("excesso_M1_pp"), col("excesso_M0_pp"), col("igpdi_dez_dez_pct"), col("ipca_dez_dez_pct")
w("\nCo-movimento entre o excesso e a inflacao do ano (so descricao; correlacao nao e causa; os anos de hiperinflacao dominam as medias; 78 anos de dados, nao 78 observacoes independentes):\n")
w("| periodo | excesso M1 x IGP-DI (Pearson / Spearman) | excesso M0 x IGP-DI | excesso M1 x IPCA | n (IGP-DI) |")
w("|---|---|---|---|---|")
for nome, yrs in (("1948-2025", range(1948, 2026)), ("1948-1979", range(1948, 1980)), ("1980-1994", range(1980, 1995)), ("1995-2025", range(1995, 2026))):
    a, n1 = corr(m1, ig, yrs); a2, _ = corr(m1, ig, yrs, True); b, _ = corr(m0, ig, yrs); b2, _ = corr(m0, ig, yrs, True)
    try:
        c, _ = corr(m1, ip, yrs); c2, _ = corr(m1, ip, yrs, True); cs = f"{f(c, 2)} / {f(c2, 2)}"
    except Exception:
        cs = "n/d (IPCA so desde 1981)"
    w(f"| {nome} | {f(a, 2)} / {f(a2, 2)} | {f(b, 2)} / {f(b2, 2)} | {cs} | {n1} |")
neg = [y for y in range(1948, 2026) if m1.get(y) is not None and m1[y] < 0]
w(f"\nAnos com excesso de M1 negativo (M1 cresceu menos que o PIB real): {', '.join(map(str, neg))}. Os maiores: {', '.join(f'{y} ({f(m1[y], 0)} p.p.)' for y in sorted((y for y in m1 if m1[y] is not None), key=lambda y: -m1[y])[:4])}. Limite: a mudanca de conceito do M1 em 2018 (dez/2017: +5,2% so pelo conceito, ver `../monetario/RESULTADO.md`) cai dentro do periodo, e o crescimento em 1980-1994 e nominal em hiperinflacao.\n")

w("## 5. Trabalho (`series/trabalho.csv`)\n")
w("Colunas: `indicador,fonte,definicao_linha,ano,trimestre,valor,unidade,nota,vintage` (`trimestre` = T1-T4 ou `ano` para a media simples dos quatro trimestres; 2026 so tem T1 e T2, sem media). Tabelas SIDRA conferidas na pagina de metadados: 4093 (variaveis 1641 pessoas de 14+, 4088 forca de trabalho, 4090 ocupadas, 4092 desocupadas, 4094 fora da forca, 4096 participacao, 4097 nivel da ocupacao, 4099 desocupacao), 4099 (4116, 4118 subutilizacao composta, 4114) e 6813 (9869 percentual de desalentados na forca de trabalho ou desalentada). Trimestre fixo, nao movel.\n")
yrs = sorted({int(x["ano"]) for x in tr if x["trimestre"] == "ano" and x["indicador"] == "nivel_da_ocupacao"})
T = {k: {int(x["ano"]): float(x["valor"]) for x in tr if x["trimestre"] == "ano" and x["indicador"] == k} for k in ("nivel_da_ocupacao", "taxa_de_participacao", "taxa_de_desocupacao", "taxa_composta_de_subutilizacao", "percentual_de_desalentados")}
w("| ano (media de 4 trimestres) | nivel da ocupacao % | participacao % | desocupacao % | subutilizacao composta % | desalentados % |")
w("|---|---|---|---|---|---|")
for y in yrs:
    w(f"| {y} | " + " | ".join(f(T[k][y], 1) for k in T) + " |")
w("\nGlosas: **nivel da ocupacao** = ocupados / pessoas de 14 anos ou mais (todas, inclusive quem esta fora da forca de trabalho); **desocupacao** = desocupados / forca de trabalho; **subutilizacao composta** = (desocupados + subocupados por insuficiencia de horas + forca de trabalho potencial) / (forca de trabalho + forca de trabalho potencial); **desalentados** = quem quer trabalhar e esta disponivel mas nao procura por achar que nao vai achar.\n")
w("Quebras dentro da PNAD Continua (`quebras.csv`): 2015T4 (conceito de ocupada ajustado a OIT), 2016T2 (conceito de desocupada: quem ja arranjou trabalho para comecar so conta se comeca em menos de 4 meses), 2020T2 (coleta so por telefone) e 2021 (reponderacao). Entre a PNAD anual e a PNAD Continua ha sobreposicao 2012-2014: PNADC menos PNAD = +0,67, +0,15 e -0,54 p.p. (quebra de sinal, ver `quebras.csv`).\n")
m = {int(r["ano"]): r for r in csv.DictReader(open(S / "pnad_1981_1990_microdados.csv"))}
pme = {int(r["ano"]): r["valor"] for r in tr if r["indicador"] == "desemprego_PME_antiga_6RMs" and int(r["ano"]) <= 1990}
w("### 5.1 Desocupacao da PNAD 1981-1990 calculada de microdados (`series/pnad_1981_1990_microdados.csv`)\n")
w("Metodo (igual em todos os anos; posicoes e codigos lidos no dicionario `Documentacao.zip` de cada ano): registro de pessoa = tipo de registro `3`; variavel V501 \"que fez na semana de referencia?\": 1 trabalhou, 2 tinha trabalho mas nao trabalhou, 3 procurou trabalho, 4 a 7 fora da forca de trabalho, em branco menor de 10 anos; PEA = V501 em {1,2,3}; desocupado = V501 = 3; taxa = soma do peso da pessoa (V9991 ou equivalente) dos desocupados sobre a soma da PEA. Idade minima 10 anos (V501 em branco abaixo disso). **NAO e numero publicado pelo IBGE**; sem validacao contra um numero publicado do mesmo ano (as PNAD de 1992 e 1993, unicas com tabela publicada para comparar, tem Dados.zip de 27 MB, acima do limite). Checagens de plausibilidade: a PEA ponderada cresce de 47,5 milhoes (1981) a 61,0 milhoes (1988); a queda de 1984 para 1985 e 1986 vai no mesmo sentido da PME (6 regioes metropolitanas); o nivel nacional (2,4% a 4,3%) e menor que o da PME (4,0% a 8,1%); as duas pesquisas medem populacoes e janelas de procura diferentes (a PNAD inclui areas rurais; a PME so 6 regioes metropolitanas), entao os niveis nao sao comparaveis, so o sentido.\n")
w("| ano | desocupacao PNAD derivada % | sem peso % | peso reponderado Censo 91 % | registros de pessoa | PME 6 RMs % (publicada, outra pesquisa) |")
w("|---|---|---|---|---|---|")
for y in range(1981, 1991):
    if y in m:
        r = m[y]
        w(f"| {y} | {f(float(r['taxa_desocupacao_pct']), 2)} | {f(float(r['taxa_sem_peso_pct']), 2)} | {f(float(r['taxa_com_peso_alternativo_censo91_pct']), 2) if r['taxa_com_peso_alternativo_censo91_pct'] else ''} | {f(float(r['registros_pessoa']), 0)} | {f(float(pme[y]), 2) if y in pme else ''} |")
    else:
        w(f"| {y} | nao calculado (arquivo acima de 25 MB) | | | | {f(float(pme[y]), 2) if y in pme else ''} |")
w("\nAvisos: (a) 1986 e 1988 tem cerca de 290 mil e 298 mil registros de pessoa contra 523 mil em 1985 (a amostra e menor; nao investiguei o motivo; as taxas usam os pesos de cada ano). (b) De 1981 a 1990 a PNAD cobre o pais menos a area rural da antiga Regiao Norte (nota do IBGE em `bruto/wayback-series-estatisticas/FDT222.html`). (c) O IBGE reponderou 1984-1990 pela projecao do Censo 91 (mesma pagina): para 1985 e 1986 o arquivo traz as duas ponderacoes e a diferenca e de 0,002 e 0,012 p.p.; para 1984 e 1988 so ha uma e usei a do arquivo. (d) Antes de 1992 a PNAD nao contava como ocupados quem produzia para o proprio consumo (ver `../quebras/quebras.csv`).\n")
w("**NAO ACHADO, com onde procurei:**\n")
w("* **PNAD 1981-1990 publicada em tabela**: o SIDRA e o FTP de tabelas do IBGE (`Pesquisa_Nacional_por_Amostra_de_Domicilios_anual`) comecam em 1992; o Ipeadata `Dese_Pnad` e `DISOC_DESE` comecam em 1992; no \"Series Estatisticas\" do IBGE (via Wayback, 21 paginas de series de trabalho conferidas) a PNAD de desocupacao cobre 1992-2007 e 2001-2011; o Anuario Estatistico do Brasil (1983 a 1992) esta em PDF escaneado acima de 25 MB; a API da OIT (ILOSTAT) devolveu resposta vazia. **O que existe**: microdados da PNAD de 1976 a 1990 em `.../PNAD_anual/microdados/<ano>/` (`bruto/ibge-ftp-pnad-microdados-listagem.html`), e o que foi calculado esta na secao 5.1.")
w("* **Desocupacao nos Censos 1970 e 1980**: nenhuma tabela digital achada; das 17 tabelas do SIDRA com condicao de atividade dos Censos cujo metadado conferi, a mais antiga comeca em 1991 (tabela 616; as outras, 2000 e 2010); o Ipeadata tem so a PEA por setor (`PEA_*`, sem desocupados). Nao verifiquei microdados dos Censos de 1970 e 1980.")
w("* **Cruzamento beneficio x forca de trabalho**: nao existe em tabela oficial (`definicoes.md`, secao 4).")
w("* **ICV-DIEESE** antes de 1997 e depois de 2019; **IPC-C1** (acima).")
w("* **Justificativa escrita do R$ 218** (Lei 14.601/2023): a Exposicao de Motivos da MP 1.164/2023 nao cita o valor (`bolsa_familia_linhas.md`).\n")

w("## 6. Quebras (`quebras.csv`)\n")
w("10 linhas, mesmas colunas de `../quebras/quebras.csv`. Todo trecho citado foi conferido por programa contra o arquivo hasheado. Uma categoria nova de `tipo_de_quebra`, `mudanca_de_unidade` (conversao de moeda de 1994), alem de `metodo_estatistico` e `mudanca_de_regra`: se o consumidor das tres categorias antigas for estrito, mapear para `mudanca_de_regra`.\n")
w("| quebra | data | tipo | efeito medido |")
w("|---|---|---|---|")
for r in csv.DictReader(open(RAIZ / "quebras.csv")):
    w(f"| {r['serie']} | {r['data_quebra']} | {r['tipo_de_quebra']} | {r['efeito_medido'][:150]} |")
w("\n## 7. Arquivos desta pasta\n")
w("* `series/poder_de_compra.csv`, `series/excesso_monetario.csv`, `series/trabalho.csv`, `series/pnad_1981_1990_microdados.csv`, `series/bolsa_familia_linhas.csv`, `series/bolsa_familia_linhas_anual.csv`, `series/_conferencias.txt`")
w("* `definicoes.md`, `bolsa_familia_linhas.md`, `quebras.csv`, `RESULTADO.md`")
nb = sum(1 for x in (RAIZ / "bruto").rglob("*") if x.is_file())
w(f"* `bruto/` ({nb} arquivos hasheados em `manifest.jsonl`: Ipeadata, SIDRA, DIEESE, OIT, IBGE incl. microdados da PNAD 1981-1988 de ate 25 MB em `bruto/pnad-microdados` (~125 MB), Planalto, FGV, Wayback), `scripts/`")
w("* Reutilizados sem copiar (ja hasheados em suas pastas): `../economia-real` (salario minimo nominal, IGP-DI, INPC, IPCA, PIB, desemprego, catalogo Ipeadata), `../quebras/bruto` (cesta DIEESE e notas do IBGE), `../monetario/saida` (M0 e M1), `../dominios-1/bruto/doc/leg` (leis e decretos).")
(RAIZ / "RESULTADO.md").write_text("\n".join(o) + "\n", encoding="utf-8")
print("ok")
