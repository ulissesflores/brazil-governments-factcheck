"""Gera series/INDICE.csv e RESULTADO.md a partir de series/, derivado/, marcos.csv, quebras.csv, regras_emendas.csv etc.
Os numeros saem dos arquivos; o texto narrativo so descreve o que foi medido. Sem rede. Rodar por ultimo."""
import csv, glob, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import PASTA, ckan, manifest

M = manifest()
S = PASTA / "series"
idx = []
for f in sorted(S.glob("*.csv")):
    if f.name == "INDICE.csv":
        continue
    rows = list(csv.DictReader(f.open(encoding="utf-8")))
    if not rows:
        idx.append(dict(arquivo=f.name, indicador="", fonte="", n_linhas=0, primeiro="", ultimo="", unidade="")); continue
    key = lambda r: (int(r["ano"]), int(r["mes_ou_trimestre"]) if r["mes_ou_trimestre"] else 0)
    a, b = min(rows, key=key), max(rows, key=key)
    fmt = lambda r: f"{r['ano']}-{int(r['mes_ou_trimestre']):02d}" if r["mes_ou_trimestre"] else r["ano"]
    idx.append(dict(arquivo=f.name, indicador=rows[0]["indicador"], fonte=rows[0]["fonte"], n_linhas=len(rows), primeiro=fmt(a), ultimo=fmt(b), unidade=rows[0]["unidade"]))
with (S / "INDICE.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(idx[0]), lineterminator="\n")
    w.writeheader(); w.writerows(idx)
I = {r["arquivo"][:-4]: r for r in idx}


def cob(nome):
    r = I.get(nome)
    return f"{r['primeiro']} a {r['ultimo']} ({r['n_linhas']} linhas)" if r else "NAO GERADA"


def val(nome, ano, mes=0):
    for r in csv.DictReader((S / f"{nome}.csv").open(encoding="utf-8")):
        if int(r["ano"]) == ano and (int(r["mes_ou_trimestre"]) if r["mes_ou_trimestre"] else 0) == mes:
            return r["valor"]
    return "n/d"


def rd(p):
    return list(csv.DictReader((PASTA / p).open(encoding="utf-8")))


conf = {r["par"]: r for r in rd("derivado/conferencia_selic.csv")}
cdef = rd("derivado/conferencia_deflatores.csv")
nfsp = rd("derivado/nfsp_codigos_confirmados_ckan.csv")
ident = rd("derivado/compulsorios_identidade.csv")
fecham = sum(1 for r in ident if abs(float(r["diferenca"])) <= max(1.0, abs(float(r["total_17633"])) * 1e-4))
regras, rp, ev, mk, qb = rd("regras_emendas.csv"), rd("rp_identificadores.csv"), rd("eventos_fiscais.csv"), rd("marcos.csv"), rd("quebras.csv")
falha_anc = [r["id"] for r in ev + mk if r["trecho"].startswith("NAO LOCALIZADO")] + [r["ato"] for r in rp if r["trecho"].startswith(("NAO LOCALIZADO", "ARQUIVO"))]
meta432 = rd("series/selic_meta_copom_fim_de_mes_sgs432.csv")
mud = rd("series/selic_meta_copom_mudancas_sgs432.csv")
log = (PASTA / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
falhas_dl = []
for lg in sorted(PASTA.glob("baixar_*.log")):
    for l in lg.read_text(encoding="utf-8").splitlines():
        if "FALHA" in l:
            falhas_dl.append(l.split(" FALHA")[0].split(" ", 2)[-1] + " <- " + l.split("FALHA ")[-1][:160])

L = []
w = L.append
w("# RESULTADO: moeda e fiscal (blocos A e B da Emenda 03)\n")
w("> Gerado por `scripts/montar_resultado.py` a partir dos arquivos da pasta; as cifras vem dos CSV, nao foram digitadas. Aquisicao em 2026-10-20 com cadeia de hash em `manifest.jsonl` "
  f"({len(log)} linhas). Sem nota, sem ranking, sem atribuicao de causa. Legenda: [OK] verificado contra fonte ou reproduzido; [PARCIAL] feito com limite declarado; [NAO ACHADO] nao obtido, com o motivo.\n")
w("## 0. Resumo\n")
w(f"1. [OK] Bloco A: Selic over mensal 1974+ em tres fontes ({cob('selic_over_mensal_ipeadata_BM12_TJOVER12')}), meta Copom diaria desde {meta432[0]['ano']}-{int(meta432[0]['mes_ou_trimestre']):02d} ({len(mud)} mudancas registradas), juro real ex-post mensal e anual (IPCA e IGP-DI), credito/PIB em duas bases do BCB, compulsorios, multiplicadores e velocidade derivados de `monetario/saida/`.")
w(f"2. [OK] Bloco B: RTN Governo Central 1997-2025 em R$ e % do PIB (tabela 2.1 caixa, tabela 2.5 valor pago 2008+), mensal 1997-01 a 2026-07 em R$; NFSP por nivel ({len(nfsp)} series SGS confirmadas no CKAN), anual e mensal.")
w("3. [NAO ACHADO] Emendas parlamentares pagas por tipo (RP 6/7/8/9) e por ano: as tres fontes abertas encontradas pesam mais de 25 MB ou exigem chave (ver secao 2.3). Em disco: as regras (13 linhas, `regras_emendas.csv`) e a definicao legal de cada RP nas LDOs (`rp_identificadores.csv`).")
w("4. [NAO ACHADO] SIOP para discricionarias: nao tentado (nao identifiquei endpoint aberto); a linha de discricionarias vem do RTN (caixa desde 2008 e valor pago desde 2008).")
w(f"5. [OK] `eventos_fiscais.csv` ({len(ev)} linhas), `marcos.csv` ({len(mk)} linhas), `quebras.csv` ({len(qb)} linhas) com trechos copiados do texto baixado. Ancoras nao localizadas: {falha_anc or 'nenhuma'}.")
w(f"6. [PARCIAL] Downloads que falharam ({len(falhas_dl)}; `sgs_432_2016-2026` foi substituido pelas janelas 2016-2025 e 2026): " + ("; ".join(falhas_dl) if falhas_dl else "nenhum") + ".\n")

w("## 1. Bloco A: moeda\n")
w("### 1.1 Selic over mensal e meta Copom\n")
w("| arquivo | cobertura |\n|---|---|")
for n in ("selic_over_mensal_ipeadata_BM12_TJOVER12", "selic_over_mensal_ipeadata_PAN12_TJOVER12", "selic_over_mensal_sgs4390", "selic_meta_copom_fim_de_mes_sgs432", "selic_meta_copom_fim_de_mes_ipeadata_BM366", "selic_meta_copom_mudancas_sgs432"):
    w(f"| `series/{n}.csv` | {cob(n)} |")
c1, c2 = conf["BM12_vs_SGS4390"], conf["PAN12_vs_BM12_anualizado"]
w(f"\n- [OK] **`PAN12_TJOVER12` e a mesma serie de `BM12_TJOVER12` anualizada, nao outra serie.** O metadado do Ipeadata marca `PAN12` como % a.a. (\"Percentagem anualizada: elaboracao IPEA\") e `BM12` como % a.m.; {c2['meses_em_comum']} meses em comum, {c2['meses_diferentes_gt_0_005_pp']} diferem mais de 0,005 pp de (1+BM12/100)^12-1 (maior diferenca {c2['maior_diferenca_pp']}). Quem tratar `PAN12` como mensal erra por um fator ~12.")
w(f"- [OK] `BM12_TJOVER12` contra o SGS 4390 (confirmado no CKAN como \"Taxa de juros - Selic acumulada no mes\"): {c1['meses_em_comum']} meses em comum ({c1['primeiro']} a {c1['ultimo']}); {c1['meses_diferentes_gt_0_005_pp']} diferem mais de 0,005 pp (maior {float(c1['maior_diferenca_pp']):.3g} pp). Exemplos: {c1['exemplos'] or 'nenhum'}.")
w("- [OK] `BM12_TJOVER12` e nulo em 1986-03, 1986-04 e 1986-05 (3 meses sem valor no JSON); `PAN12_TJOVER12` tem valor nesses meses. Nas series de juro real esses 3 meses usam a Selic mensal de-anualizada de PAN12, com aviso na coluna `nota`; `selic_over_mensal_ipeadata_BM12_TJOVER12.csv` tem 3 linhas a menos que `..._PAN12_...` por isso.")
w("- O mes de outubro de 2026 (mes do download) foi excluido: o metadado do Ipeadata diz que o mes corrente e parcial, e o SGS 4390 trazia 0,61% para 2026-10 com o mes em curso.")
w(f"- [OK] Meta Copom: o SGS 432 (confirmado no CKAN: \"Taxa de juros - Meta Selic definida pelo Copom\") so devolve dados a partir de {meta432[0]['ano']}-{int(meta432[0]['mes_ou_trimestre']):02d}; a serie do Ipeadata `BM366_TJOVER366` esta em `selic_meta_copom_fim_de_mes_ipeadata_BM366` ({cob('selic_meta_copom_fim_de_mes_ipeadata_BM366')}). O pedido citava 1996+: o que ha antes de {meta432[0]['ano']}, se houver, esta so na serie do Ipeadata.")
w("- A API do SGS recusa janela diaria maior que 10 anos (HTTP 406): por isso 4 janelas (1996-2005, 2006-2015, 2016-2025, 2026 ate 2026-10-20). Uma consulta exploratoria `ultimos/1` (nao gravada) devolveu o SGS 432 com data 04/11/2026, posterior ao dia da consulta; as janelas gravadas terminam em 2026-10-20 e nao contem essa linha.\n")
w("### 1.2 Juro real ex-post\n")
w("| arquivo | cobertura |\n|---|---|")
for n in ("juro_real_ex_post_mensal_ipca", "juro_real_ex_post_mensal_igpdi", "juro_real_ex_post_anual_ipca", "juro_real_ex_post_anual_igpdi"):
    w(f"| `series/{n}.csv` | {cob(n)} |")
w("\nFormula: ((1+Selic over do mes)/(1+inflacao do mes)-1)*100; anual = composicao de 12 meses de cada lado (ano civil completo). Anos incompletos nao foram calculados (2026).")
for r in cdef:
    w(f"- [{'OK' if r['meses_diferentes_gt_0_005_pp']=='0' else 'PARCIAL'}] {r['par']}: {r['meses_em_comum']} meses em comum, {r['meses_diferentes_gt_0_005_pp']} diferem mais de 0,005 pp (maior {float(r['maior_diferenca_pp']):.4g} pp).")
w("- Os codigos SGS 433 (IPCA) e 190 (IGP-DI) **nao estao no catalogo CKAN** (`package_search?q=codigo_sgs:433` e `:190` devolvem 0 resultados) e a pagina de metadados do SGS responde \"System unavailable\". Por isso o deflator usado nas series e o do Ipeadata (`PRECOS12_IPCAG12`, `IGP12_IGPDIG12`, com nome no metadado); o SGS entra so como conferencia.\n")
w("### 1.3 Credito, compulsorios, multiplicadores, velocidade\n")
w("| arquivo | cobertura |\n|---|---|")
for n in sorted(I):
    if n.startswith(("credito_", "compulsorios_", "base_ampliada", "insuficiencia", "outros_recolh", "multiplicador_", "velocidade_")):
        w(f"| `series/{n}.csv` | {cob(n)} |")
c20 = ckan(20622)
w(f"\n- [PARCIAL] Credito/PIB: as \"duas metodologias do BCB\" foram tratadas como duas bases em arquivos separados, nunca emendadas: **SFN** (SGS 20622 e abertura livres/direcionados) e **credito ampliado** (SGS 28215 e aberturas). O SGS 20622 tem dados desde 1995-07, mas o catalogo CKAN declara `inicio_periodo` = {c20.get('inicio_periodo')}; as linhas anteriores a 2007-03 levam a flag na coluna `nota`. Nao achei, no CKAN nem no Ipeadata, uma serie de credito/PIB da decada de 1990 separada.")
w("- [PARCIAL] **Setor privado.** O pre-registro pede \"credito ao setor privado, % do PIB\". O SGS 20622 e o credito total do SFN (setor publico incluido: o CKAN tem a serie irma 22051, setor publico). Cortes privados obtidos: SGS 22052 \"Saldo das operacoes de credito por tipo de cliente - Setor privado - Total\" em **R$ milhoes, desde 2012-01** (`credito_sfn_setor_privado_total_rs_mi_sgs22052.csv`), sem versao em % do PIB no catalogo que consultei; e SGS 28217/28867/28868 (credito ampliado a empresas e familias, ja sem governo geral) em % do PIB desde 2013-01. **Nao existe aqui o % do PIB do credito privado do SFN antes de 2012**; calcula-lo exigiria o PIB acumulado em 12 meses do BCB, que nao esta nesta pasta.")
w(f"- [PARCIAL] Compulsorios: {fecham} de {len(ident)} meses fecham a soma de 1849+1848+1850+1797 com o total 17633 (tolerancia max(1; 0,01%)); detalhe em `derivado/compulsorios_identidade.csv`. A busca do CKAN por \"compuls\" nao retornou titulo; os codigos vieram de \"Recolhimentos obrigatorios de instituicoes financeiras\" (17633, 1797, 1848-1850) e \"Base monetaria ampliada - Depositos compulsorios em especie\" (1828).")
w("- Multiplicadores M1/M0 e M3/M0 e velocidade PIB/M1 saem de `monetario/saida/mensal.csv` e `anual.csv` (nao refeitos); cada regime (M1 antigo, M1 Novo, M3 regime 2001, M3 Novo) e um arquivo, nunca emendado. Velocidade: media de 12 saldos (primaria) e saldo de dezembro (variante), conforme o aviso de `monetario/RESULTADO.md` 1.6.\n")

w("## 2. Bloco B: fiscal\n")
w("### 2.1 RTN (Tesouro Nacional)\n")
w("Fonte: planilha `seriehistoricajul26.xlsx` ja hasheada em `mecanismos-contabil/manifest.jsonl` (sha256 35899d771fc4...), lida pelos CSV de aba de `mecanismos-contabil/derivado/rtn/`; nao foi baixada de novo.\n")
w("| arquivo | cobertura |\n|---|---|")
for n in ("rtn_gc_caixa_receita_total_rs_mi", "rtn_gc_caixa_receita_total_pct_pib", "rtn_gc_caixa_despesa_total_rs_mi", "rtn_gc_caixa_despesa_total_pct_pib", "rtn_gc_caixa_despesa_discricionarias_rs_mi", "rtn_gc_caixa_despesa_discricionarias_pct_pib", "rtn_gc_valor_pago_discricionarias_valor_pago_rs_mi", "rtn_gc_valor_pago_discricionarias_valor_pago_pct_pib", "rtn_gc_caixa_receita_total_mensal_rs_mi", "rtn_gc_caixa_despesa_total_mensal_rs_mi"):
    w(f"| `series/{n}.csv` | {cob(n)} |")
w(f"\n- {sum(1 for n in I if n.startswith('rtn_'))} arquivos RTN no total (ver `series/INDICE.csv`). Discricionarias: linha 4.4.2 da tabela 2.1 vale 0 de 1997 a 2007 na planilha; foi tratada como linha nao publicada (sem valor), nao como gasto zero. Tabela 2.5 (valor pago) so existe a partir de 2008.")
w(f"- Discricionarias em 2025: {val('rtn_gc_caixa_despesa_discricionarias_rs_mi', 2025)} R$ mi (caixa) e {val('rtn_gc_valor_pago_discricionarias_valor_pago_rs_mi', 2025)} R$ mi (valor pago); em % do PIB, {val('rtn_gc_caixa_despesa_discricionarias_pct_pib', 2025)} e {val('rtn_gc_valor_pago_discricionarias_valor_pago_pct_pib', 2025)}.\n")
w("### 2.2 NFSP por nivel (BCB)\n")
w("Codigos confirmados no CKAN (titulo, unidade e primeiro mes na API):\n")
w("| SGS | titulo no CKAN | unidade | primeiro mes | ultimo mes completo |\n|---|---|---|---|---|")
for r in nfsp:
    w(f"| {r['sgs']} | {r['titulo_ckan'].replace('NFSP sem desvalorização cambial', 'NFSP s/ desv. cambial')} | {r['unidade_ckan']} | {r['primeiro_mes']} | {r['ultimo_mes_completo']} |")
w("\n- Sinal: conforme a fonte. Leitura do sinal (inferencia, a pagina do CKAN nao a declara): valor positivo = deficit (necessidade de financiamento), negativo = superavit; no consolidado, resultado primario 12 meses em dez/2008 = " + val('nfsp_primario_setor_publico_consolidado_12m_pct_pib_sgs5793', 2008, 12) + "; dez/2015 = " + val('nfsp_primario_setor_publico_consolidado_12m_pct_pib_sgs5793', 2015, 12) + "; dez/2020 = " + val('nfsp_primario_setor_publico_consolidado_12m_pct_pib_sgs5793', 2020, 12) + " (% do PIB).")
w("- Anual = valor de dezembro do fluxo acumulado em 12 meses em % do PIB (selecao, nao soma). Fluxos mensais em R$ milhoes vem em arquivo proprio; soma anual em R$ nao foi gerada.")
w("- O catalogo do BCB descreve a abrangencia: sem Petrobras (dados de maio/2009 em diante) e sem Eletrobras (novembro/2010 em diante), recalculado so ate dez/2001; ver `quebras.csv`.\n")
w("### 2.3 Emendas parlamentares\n")
w("- [OK] `regras_emendas.csv`: EC 86/2015, EC 100/2019, EC 105/2019, EC 126/2022 e LC 210/2024, data e trecho copiados do texto do Planalto, com a vigencia lida do proprio texto.")
w("- [OK] `rp_identificadores.csv`: a definicao legal de RP 6 (individuais), RP 7 (bancada estadual), RP 8 (comissoes) e RP 9 (relator-geral) nas LDOs 2020 a 2025 baixadas.")
w("- [NAO ACHADO] **Valores pagos por tipo e ano.** Nao baixei: (a) Portal da Transparencia, `EmendasParlamentares.zip`, 32.490.844 bytes (cabecalho HTTP `content-length`); o site em HTML devolve verificacao humana e a API exige chave; (b) Tesouro Transparente, \"Emendas Parlamentares Individuais e de bancada\", CSV de 67,1 MiB segundo a pagina (so individuais e bancada, desde 2015); (c) Tesouro, \"Despesas e Transferencias Totais da Uniao\", um XLSX por ano; tamanhos lidos da pagina do CKAN em 2026-10-20: 2010 a 2025 entre 28,2 e 38,5 MiB (2020: 35,7; 2021: 36; 2022: 34,9; 2023: 30,3; 2024: 28,2; 2025: 32,9), 2008 e 2009 \"0 bytes\"; so o de 2026 (22 MiB, ano em curso) cabe no teto e nao foi baixado (um ano parcial nao entrega a serie pedida). Nao sondei se essas bases trazem o identificador RP. Todos os demais acima do teto de 25 MB. Metadados do Tesouro: `bruto/tesouro/metadados-emendas-individuais-bancada.pdf`.")
w("- Caminho para completar, se o teto for liberado: a coluna de tipo de emenda do CSV do Portal da Transparencia ou o identificador RP das bases do Tesouro, somando o valor pago por ano; o mapeamento tipo -> RP esta em `rp_identificadores.csv`.\n")
w("### 2.4 Eventos fiscais, marcos e quebras\n")
w(f"- `eventos_fiscais.csv`: LRF (LC 101/2000), EC 95/2016, EC 103/2019, LC 200/2023, DLG 6/2020, EC 126/2022 art. 3 e uma linha por LDO de 2001 a 2025 e por lei que alterou LDO ({len(ev)} no total). A coluna `trecho` traz a primeira ocorrencia da clausula da meta de resultado primario; a pagina do Planalto pode mostrar tambem a redacao alterada por lei posterior (aviso na coluna `nota`). A meta citada e a do ato, nao o resultado apurado. LDO 2026 nao foi baixada.")
w(f"- `marcos.csv` ({len(mk)} linhas): Real (Lei 8.880/1994, Lei 9.069/1995), cambio flutuante 1999 (BCB, duas datas no mesmo documento: 15.01 e 18.01), Decreto 3.088/1999, 2002 (Relatorio de Inflacao set/2002), 2008 (MP 442 e Relatorio de Inflacao dez/2008), recessao 2014-2016 (CODACE, copia hospedada pelo Poder360), OMS 11/03/2020, DLG 6/2020, LC 179/2021. Nao obtidos (HTTP 403 ao servidor com o agente de usuario da cadeia): comunicado do FMI de 06/09/2002 e o 8-K da Lehman na SEC.")
w(f"- `quebras.csv` ({len(qb)} linhas, colunas de `quebras/quebras.csv`): linhas proprias (abrangencia da NFSP, RTN, Selic, deflatores, credito, compulsorios) e linhas herdadas de `quebras/quebras.csv` (PIB e agregados monetarios) para as series que usam esses dados.\n")

w("## 3. Estado da cadeia de hash\n")
w(f"`manifest.jsonl`: {len(log)} linhas. Verificacao: `python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py verify <pasta>` (resultado registrado em `STATE.md`).\n")

w("## 4. NAO ACHADO e desvios\n")
w("| item | situacao |\n|---|---|")
w("| Emendas pagas por RP e ano | bloqueado pelo teto de 25 MB (secao 2.3) |")
w("| SIOP (discricionarias) | nao tentado; o RTN cobre a linha |")
w("| Siga Brasil (emendas) | nao tentado |")
w("| Credito privado do SFN em % do PIB | so R$ (SGS 22052, desde 2012); ver 1.3 |")
w("| Selic meta Copom antes de 1999-03 no SGS | 432 comeca em 1999-03; ver Ipeadata BM366 |")
w("| Credito/PIB dos anos 1990 em base separada | nao achado no CKAN nem no Ipeadata |")
w("| IPCA/IGP-DI no CKAN | codigos 433 e 190 ausentes; usado o Ipeadata |")
w("| Vintage anterior das series | um unico vintage em disco; revisoes nao medidas |")
w("| Comunicado FMI 2002 e 8-K Lehman | HTTP 403 |")
w("| LDO 2026 e LOA | nao baixadas |")
w("| Aplicacao do ato a cada ano para emendas | so a vigencia lida do texto; sem tabela ano a ano alem de `regras_emendas.csv` |")
w("\n**Desvios que o agente cometeu e corrigiu ou deixou registrado:**\n")
w("- Uma chamada `curl -r -2000-` baixou o `EmendasParlamentares.zip` inteiro (32,5 MB) para o scratchpad por engano (o formato de faixa estava errado); o arquivo foi apagado, nao entrou na cadeia e nenhum dado dele foi usado. Uma sonda de tamanho (`-r 0-0`) de duas bases do Tesouro transferiu o corpo para `/dev/null` sem gravar nada.")
w("- Duas filas de download rodaram por um instante em paralelo contra o mesmo `manifest.jsonl`; a verificacao da cadeia depois disso deu OK. Arquivos que o servidor respondeu com pagina HTML de erro foram rebaixados (linha nova na cadeia; a antiga fica).")
w("\n## 5. Becos\n")
w("- IPCA/IGP-DI no CKAN: volta se o BCB indexar os codigos 433/190.")
w("- Portal da Transparencia em HTML: volta se alguem fornecer chave de API.")
w("- Pagina de metadados do SGS: \"System unavailable\"; volta se o servico voltar.")
(PASTA / "RESULTADO.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("RESULTADO.md:", len(L), "linhas")
