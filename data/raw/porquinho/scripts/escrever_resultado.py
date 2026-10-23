#!/usr/bin/env python3
"""Escreve ../RESULTADO.md: tabelas saem de ../series/*.csv; texto fixo. python3 -I escrever_resultado.py (sem rede; so chama o verify da cadeia)."""
import csv
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
S = RAIZ / "series"
head = subprocess.run(["python3", "-I", "/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py", "verify", str(RAIZ)], capture_output=True, text=True).stdout.strip()
f = lambda v, c=0: "" if v in (None, "") else f"{float(v):,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")
L = {}
for r in csv.DictReader(open(S / "porquinho.csv")):
    L.setdefault(r["linha"], {})[(int(r["ano"]), int(r["mes"]) if r["mes"] else None)] = float(r["valor"])
G = {}
for r in csv.DictReader(open(S / "porquinho_por_governo.csv")):
    G.setdefault(r["linha"], {})[r["governo_id"]] = r
GOV = [("fhc", "FHC"), ("lula12", "Lula 1-2"), ("dilma", "Dilma"), ("temer", "Temer"), ("bolsonaro", "Bolsonaro"), ("lula3", "Lula 3")]


def ult(lin):
    k = max(k for k in L[lin] if k[1] is not None)
    return k, L[lin][k]


def base(lin):
    return L[lin][(1994, 12)] if (1994, 12) in L[lin] else None


def cel(lin, g, anual=False):
    r = G[lin][g]
    if r["variacao_pct"] == "" and r["valor_fim"] == "":
        return "sem dado"
    if r["variacao_pct"] == "":
        return f"{f(r['variacao_abs'])} R$"
    return f"{f(r['variacao_pct'], 1)}% ({f(r['variacao_anualizada_pct_aa'], 1)}% a.a.)"


o = []
w = o.append
w("# RESULTADO: o porquinho (R$ 100.000 em dinheiro desde 1 de janeiro de 1995)\n")
w("Colheita de 2026-10-20. Sem opiniao, sem nota, sem ranking: so numeros, fonte e limite. Pre-registro: `../preregistro/PREREGISTRATION-EMENDA-03.md`, secao E (mapa linha -> item registrado na secao 1.1). Tudo sai de `python3 -I scripts/construir.py`, `scripts/quebras_gerar.py` e `scripts/escrever_resultado.py`, que leem so arquivos locais; as formulas estao no cabecalho de `scripts/construir.py`. Os brutos entram na cadeia de hash (`manifest.jsonl`; `python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py verify .` -> " + head + "). O imposto inflacionario nunca e somado a inflacao: nao e calculado em lugar nenhum.\n")
w("Legenda: ACHADO = tem numero e fonte aqui; NAO ACHADO = procurei e nao obtive (com onde procurei).\n")
w("## 1. Resumo\n")
k, v = ult("caixa_real_ipca")
w(f"1. **ACHADO.** R$ 100.000 em dinheiro vivo em 1 jan 1995 compram, em set/2026, o que R$ {f(v)} compravam em dez/1994 pelo IPCA ({f(L['caixa_real_inpc'][k])} pelo INPC, {f(L['caixa_real_igpdi'][k])} pelo IGP-DI, {f(L['caixa_real_ipcfipe'][k])} pelo IPC-Fipe).")
kp, vp = ult("poupanca_real_ipca")
ks, vs = ult("selic_real_ipca")
kd, vd = ult("caixa_menos_poupanca_real_ipca")
w(f"2. **ACHADO.** A mesma quantia na poupanca (SGS 25, regra de deposito ate 03/05/2012, aniversario no dia 1) vale em set/2026 R$ {f(vp)} (reais de dez/1994, IPCA) e na Selic R$ {f(vs)}; diferenca caixa menos poupanca = R$ {f(vd)}. Se a regra nova (SGS 195) valesse desde jun/2012 o saldo nominal de set/2026 seria R$ 1.563.850 em vez de R$ 1.752.040 (`series/_conferencias.txt`).")
ksm, vsm = ult("caixa_em_salarios_minimos")
kc, vc = ult("caixa_em_cestas_dieese_sp")
kpib, vpib = ult("caixa_em_anos_pib_per_capita_nominal") if False else (None, None)
pib = L["caixa_em_anos_pib_per_capita_nominal"]
w(f"3. **ACHADO.** Em unidades relativas: R$ 100.000 eram {f(base('caixa_em_salarios_minimos'))} salarios minimos em dez/1994 e {f(vsm, 1)} em set/2026; {f(base('caixa_em_cestas_dieese_sp'))} cestas DIEESE-SP e {f(vc, 1)} em ago/2026; {f(pib[(1994, None)], 1)} anos de PIB per capita nominal (1994) e {f(pib[(2024, None)], 2)} (2024, ultimo ano publicado).")
w("4. **ACHADO.** Quatro referencias externas, cada uma deflacionada pelo CPI da propria referencia (EUA para dolar, DES e ouro; Suica para o franco): " + "; ".join(f"{n} {f(base(l))} -> {f(ult(l)[1])} ({ult(l)[0][0]}-{ult(l)[0][1]:02d})" for n, l in (("US$ de dez/1994", "usd_poder_compra_ref"), ("CHF de dez/1994", "chf_poder_compra_ref"), ("DES de dez/1994", "sdr_poder_compra_ref"), ("onças de ouro (sem deflator)", "ouro_oncas"))) + ".")
w("5. **ACHADO com ressalva.** Ouro: a LBMA (preco PM diario) esta bloqueada para este IP (HTTP 403, Cloudflare, tambem no Chrome real) e o FRED retirou a serie (404). Usei a media mensal do Pink Sheet do Banco Mundial; a partir de jun/2025 o proprio Banco Mundial passa a usar o preco a vista medio em vez do fixing da tarde de Londres (`quebras.csv`, Q06 e Q07).")
w("6. **ACHADO com ressalva.** ICV-DIEESE e Ipea renda muito baixa nao cobrem 1995-2026 (ICV: so taxa anual de 1997 a 2019; Ipea: jul/2006 a jul/2026). A parte sem fonte nao e preenchida: as linhas comecam com emenda no IPCA (dez/1996 e dez/2006) e o por-governo so mostra os mandatos com as duas pontas.\n")


w("### 1.1 Mapa das linhas emitidas para os itens do pre-registro (secao E)\n")
w("| item registrado | linhas em `series/porquinho.csv` | intermediarios (so para montar a linha registrada) |")
w("|---|---|---|")
w("| E.1 poder de compra por IPCA, INPC, IGP-DI, IPC-Fipe, ICV-DIEESE, Ipea renda muito baixa | `caixa_real_ipca`, `caixa_real_inpc`, `caixa_real_igpdi`, `caixa_real_ipcfipe`, `caixa_real_icv_dieese`, `caixa_real_ipea_renda_muito_baixa` | |")
w("| E.2 poupanca e Selic deflacionadas pelo IPCA; caixa menos poupanca | `poupanca_real_ipca`, `selic_real_ipca`, `caixa_menos_poupanca_real_ipca` | `poupanca_nominal`, `selic_nominal` |")
w("| E.3 anos de PIB per capita, salarios minimos, cestas DIEESE | `caixa_em_anos_pib_per_capita_nominal`, `caixa_em_salarios_minimos`, `caixa_em_cestas_dieese_sp` | |")
w("| E.4 dolar, franco suico, DES, ouro, cada um deflacionado pela referencia | `usd_poder_compra_ref`, `chf_poder_compra_ref`, `sdr_poder_compra_ref`, `ouro_preco_real_usd_oz` | `usd_nominal`, `chf_nominal`, `sdr_nominal`, `ouro_oncas` (quantidade) |")
w("\nOuro: deflacionar a quantia em ouro pelo CPI dos EUA da exatamente a linha do dolar (numerador e denominador levam o mesmo deflator), portanto seria redundante; a referencia ouro deflacionada pelo CPI dos EUA e o preco, emitido como `ouro_preco_real_usd_oz`; `ouro_oncas` e a quantidade fisica, sem deflator. Total: 22 indicadores = 16 linhas registradas + 6 intermediarios (a quantidade `ouro_oncas` entra entre os intermediarios).\n")
w("## 2. Tabela por governo (variacao de dez 1994 / inicio do mandato ate o fim, % e % ao ano)\n")
w("Valores em `series/porquinho_por_governo.csv` (inicio e fim usados, valores, variacao absoluta, n_meses). Fronteira do mandato = fim do mes anterior (dia 1) ou do proprio mes (31/08/2016); Lula (3o mandato) termina no ultimo mes da linha (set/2026 ou antes, conforme a fonte; o mandato esta registrado ate 2026-10-19). Linha anual (PIB per capita): ano completo mais recente antes da fronteira. Variacao % = fim/inicio - 1; % a.a. = composta sobre n_meses.\n")
w("| linha | " + " | ".join(n for _, n in GOV) + " |")
w("|---|" + "---|" * len(GOV))
for lin in G:
    w(f"| `{lin}` | " + " | ".join(cel(lin, g) for g, _ in GOV) + " |")
w("\nNotas da tabela: `caixa_menos_poupanca_real_ipca` e uma diferenca em R$ (comeca em zero em dez/1994), por isso mostra a variacao absoluta; \"sem dado\" = a fonte nao tem observacao em uma das pontas (ICV so em dezembros de 1996 a 2019; Ipea so desde dez/2006).\n")

w("## 3. Estado das linhas na data-base e no ultimo mes\n")
w("| linha | dez/1994 | ultimo mes | valor no ultimo mes | unidade |")
w("|---|---|---|---|---|")
unid = {}
for r in csv.DictReader(open(S / "porquinho.csv")):
    unid[r["linha"]] = r["unidade"]
for lin in L:
    kk, vv = ult(lin) if any(m is not None for _, m in L[lin]) else (None, None)
    b = base(lin)
    w(f"| `{lin}` | {f(b, 2) if b is not None else ''} | {kk[0]}-{kk[1]:02d} | {f(vv, 2)} | {unid[lin]} |" if kk else f"| `{lin}` | | anual | | {unid[lin]} |")
w("")
w("## 4. Conferencias (todas em `series/_conferencias.txt`)\n")
conf = [x[6:] for x in (S / "_conferencias.txt").read_text().splitlines() if x.startswith("CONF: ")]
for x in conf[:14]:
    w(f"* {x}")
w("\n(As conferencias acima sao copia literal de `_conferencias.txt`: a formatacao de numeros e a de la.)\n")
w("Arquivos de erro na cadeia (nao sao dados): `bruto/sgs25-poupanca-ate-2004.json`, `bruto/sgs195-poupanca-2012-2022.json` e `bruto/sgs25-poupanca-2018-2026.json` contem a pagina HTML \"Requisicao invalida\" do SGS (janela de 10 anos exatos, e uma consulta que falhou e funcionou minutos depois); os dados vieram das janelas refeitas (`sgs25-poupanca-1995-2000/2001-2004/2012-2017/2018-2026-refeito`, `sgs195-poupanca-2012-2017/2018-2022/2022-2026`). Os pacotes CKAN `ckan_1.json` e `ckan_3696.json` tambem sao pagina de erro.\n")
w("Codigos SGS: a pagina de metadados do SGS respondeu \"System unavailable\" (3698). SGS 25, 195 e 4390: nome e periodicidade lidos no CKAN do BCB (`bruto/ckan_25.json`, `ckan_195.json`, `ckan_4390.json`; a SGS 25 e 195 sao diarias, \"percentual ao mes\"). SGS 3698 = dolar venda, media do mes e SGS 3696 = dolar venda, fim do mes: confirmados por igualdade com o Ipeadata BM12_ERV12 e BM12_ERVF12 (91 meses diferem na 4a ou 5a casa na media; so fev/1998 difere no fim do mes), nao pela pagina do SGS. Os pacotes CKAN de 3695, 3697, 3698 e 3694 voltaram vazios (`bruto/ckan_36*.json`); 3696 e 1 voltaram pagina de erro (ficam na cadeia).\n")

w("## 5. NAO ACHADO e limites\n")
for x in (
    "**LBMA PM diario** (pre-registro): HTTP 403 por curl e pelo Chrome real; FRED GOLDPMGBD228NLBM, 404. Nao contornei o bloqueio. Fonte usada no lugar: Banco Mundial Pink Sheet, media mensal (Q06).",
    "**ICV-DIEESE mensal, antes de 1997 ou depois de 2019**: nao existe em tabela aberta (`../poder-de-compra/RESULTADO.md` secao 3). Linha de dezembros 1996-2019, sem interpolacao.",
    "**Ipea renda muito baixa antes de jul/2006** e depois de jul/2026: a serie nao existe; emenda no IPCA em dez/2006 (o pre-registro diz 2007+).",
    "**PIB per capita nominal de 2025 e 2026**: o Ipeadata GAC_PIBCAPN termina em 2024 (atualizada em 2025-08-20); Lula (3o mandato) usa 2024.",
    "**IPC suico e DES de set/2026**: SNB e IMF ainda nao publicaram; as linhas deflacionadas em franco e em DES terminam em ago/2026 (o franco nominal vai a set/2026 e o DES nominal a ago/2026).",
    "**CPI dos EUA de out/2025**: vazio no FRED; sem linha nesse mes (causa nao verificada).",
    "**Efeito das mudancas de metodo da PTAX, do ouro (jun/2025) e da cesta do DES sobre o nivel das linhas**: nao medi (sem serie sobreposta).",
    "**Cesta do DES antes de 2016**: nao verifiquei as trocas (euro no lugar de marco e franco, revisoes de 2006 e 2011).",
    "**Poupanca**: a linha e bruta de imposto e tarifa, na regra antiga (SGS 25); a regra nova esta so como conferencia.",
    "**Imposto inflacionario**: por pre-registro nao e somado a inflacao e nao e calculado.",
):
    w(f"* {x}")
w("\n## 6. Arquivos\n")
w("* `series/porquinho.csv` (formato longo linha,ano,mes,valor,unidade,nota,vintage), `series/porquinho_por_governo.csv`, `series/_conferencias.txt`, `quebras.csv` (24 quebras), `manifest.jsonl` e `bruto/`, `baixar.sh` (downloads pela cadeia), `scripts/`.")
w("* Reuso, sem copia: `../inflacao/{ipca-sgs433,inpc-sgs188,igpdi-sgs190}-raw.json` (ate 2025-12), `../inflacao/igpdi-ipeadata-raw.json`, `../poder-de-compra/bruto/ipeadata-{FIPE12_FIPE0001,FIPE12_IPCFIPE12,DIMAC12_INF1}-raw.json`, `../poder-de-compra/series/poder_de_compra.csv` (ICV), `../economia-real/ipeadata-{MTE12_SALMIN12,GAC_PIBCAPN}-raw.json`, `../quebras/bruto/ipeadata-DIEESE12_CBSP12-raw.json`.")
(RAIZ / "RESULTADO.md").write_text("\n".join(o) + "\n")
print(len(o), "linhas")
