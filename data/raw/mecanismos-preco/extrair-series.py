#!/usr/bin/env python3
"""Series de apoio (formato longo). Le so o bruto desta pasta (e historia/RESULTADO.md por transcricao), sem rede.

Uso: python3 -I extrair-series.py   (a partir da pasta mecanismos-preco)
Saidas em series/: cide-combustiveis-receita-anual.csv, receita-gastos-tributarios-folha-cide.csv,
receita-desoneracoes-instituidas-combustiveis.csv, cde-receitas-orcadas-cgu.csv, petrobras-resultado-derivados-ipea.csv,
ipca-itens-administrados-bcb.csv.
Linhas "transcrito" vem de tabela em PDF lida a olho (pdftotext -layout); a pagina/tabela esta na coluna nota.
"""
import csv, json, collections, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
VINT = "2026-10-19"
COLS = ["indicador", "fonte", "definicao_linha", "ano", "valor", "unidade", "nota", "vintage"]
spec = importlib.util.spec_from_file_location("lx", HERE / "ler-xlsx.py")
lx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lx)


def limpa(v):
    return " ".join(str(v).split())


def grava(nome, linhas):
    with (HERE / "series" / nome).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in linhas:
            r.setdefault("vintage", VINT)
            w.writerow({k: limpa(v) for k, v in r.items()})
    print(nome, len(linhas), "linhas")


# 1. CIDE-combustiveis, receita bruta anual (Ipeadata; fonte primaria Receita Federal)
d = json.loads((HERE / "bruto/ipeadata-SRF12_CIDE12-raw.json").read_text())["value"]
soma, n = collections.defaultdict(float), collections.Counter()
for r in d:
    y = int(r["VALDATA"][:4]); soma[y] += r["VALVALOR"]; n[y] += 1
def nota_cide(y):
    if n[y] < 12:
        return "parcial: %d meses" % n[y]
    return {2012: "Decreto 7.764 (22/06/2012) zera as aliquotas", 2015: "Decreto 8.395 (28/01/2015) restabelece aliquotas"}.get(y, "")


grava("cide-combustiveis-receita-anual.csv", [dict(
    indicador="cide_combustiveis_receita_bruta_anual", fonte="Ipeadata SRF12_CIDE12 (Min. Economia/SRF)",
    definicao_linha="soma dos 12 meses da receita bruta da CIDE-combustiveis", ano=y, valor=f"{soma[y]:.1f}",
    unidade="R$ milhoes correntes", nota=nota_cide(y)) for y in sorted(soma)])

# 2. Receita Federal, DGT bases efetivas 2016 (serie 2014-2019), quadro XXVI = aba 27
z, ss, _ = lx.abrir(HERE / "bruto/receita/dgt-bases-efetivas-2016-serie-2014-a-2019-quadros.bin")
alvo = {"Desoneração da Folha de Salários": "gasto_tributario_desoneracao_folha",
        "Contribuição de Intervenção no Domínio Econômico - CIDE": "gasto_tributario_cide",
        "TOTAL": "gasto_tributario_total"}
out, vistos = [], set()
for r, c in lx.linhas(z, ss, 27):
    nome = c.get("A", "")
    if nome in alvo and r >= 288 or nome == "TOTAL":
        for col, ano in zip("BCDEFG", range(2014, 2020)):
            out.append(dict(indicador=alvo[nome], fonte="Receita Federal, DGT Bases Efetivas 2016 (serie 2014-2019), Quadro XXVI",
                            definicao_linha=nome, ano=ano, valor=f"{float(c[col]) / 1e6:.1f}", unidade="R$ milhoes",
                            nota="2014-2015: estimativa em bases efetivas; 2016-2019: projecao (cabecalho do quadro). CIDE aparece perto de zero porque a aliquota zero por decreto nao e contada como gasto tributario"
                            if nome != "TOTAL" else "soma de todos os gastos tributarios do quadro"))
        vistos.add(nome)
assert vistos == set(alvo), vistos
grava("receita-gastos-tributarios-folha-cide.csv", out)

# 3. Receita Federal, Desoneracoes Instituidas: atos sobre combustiveis (ano do arquivo, linha, texto que tem de bater)
ATOS = [
    (2021, 14, "Decreto nº 10.638", "PIS/Cofins diesel (reduz a zero a partir de 1/3/2021; prazo 30/04/2021)"),
    (2021, 15, "Decreto nº 10.638", "PIS/Cofins GLP domestico ate 13 kg (Decreto 10.638/2021)"),
    (2022, 26, "Lei Complementar nº 192", "PIS/Cofins zero sobre diesel, GLP, querosene de aviacao e biodiesel ate 31/12/2022"),
    (2022, 39, "Lei Complementar nº 194", "PIS/Cofins e CIDE zero sobre diesel, biodiesel, GLP e querosene de aviacao ate 31/12/2022"),
    (2023, 11, "Medida Provisória nº 1.157", "PIS/Cofins reduzido: diesel, biodiesel, GLP, alcool, QAV, GNV e gasolina (prazo 31/12/2023)"),
    (2023, 13, "Medida Provisória nº 1.163", "PIS/Cofins/CIDE: gasolina, alcool, GNV e QAV (reducao de aliquotas, prazo 31/12/2023)"),
]
out = []
for ano_arq, linha, texto, defin in ATOS:
    z, ss, _ = lx.abrir(HERE / f"bruto/receita/desoneracoes-instituidas-{ano_arq}.bin")
    for r, c in lx.linhas(z, ss, 1):
        if r == linha:
            assert texto in c["C"], (ano_arq, linha, c["C"])
            for col, k in zip("HIJK", range(4)):
                v = c.get(col, "-").strip()
                if v not in ("-", "*", "") and not v.startswith("*"):
                    out.append(dict(indicador="estimativa_renuncia_ato", fonte=f"Receita Federal, Desoneracoes Instituidas {ano_arq} (linha {linha})",
                                    definicao_linha=f"{c['C'].strip()}: {defin}", ano=ano_arq + k, valor=v.replace(",", "."), unidade="R$ milhoes",
                                    nota=f"estimativa da RFB no ano de instituicao (+{k}); medida de compensacao na planilha: {c.get('L','').strip()[:80]}; gasto tributario: {c.get('G','').strip()}"))
assert out
grava("receita-desoneracoes-instituidas-combustiveis.csv", out)

# 4. CGU (PCPR 2019), Relatorio de Avaliacao da CDE, Tabela 1 (R$ milhoes correntes, receitas ORCADAS; fonte Aneel) - transcrito
CDE = {"Recursos da União": [8460, 11805, 0, 0, 0, 0], "Quotas CDE - Uso": [1024, 1700, 18920, 11853, 9348, 14160],
       "Quotas CDE - Energia": [0, 0, 3137, 3472, 3690, 3796], "Total": [14121, 18074, 25246, 18291, 15989, 20053]}
out = []
for nome, vals in CDE.items():
    for ano, v in zip(range(2013, 2019), vals):
        out.append(dict(indicador="cde_receita_orcada", fonte="CGU, Relatorio de Avaliacao da CDE (PCPR 2019), Tabela 1, p. 7; dados Aneel",
                        definicao_linha=nome, ano=ano, valor=v, unidade="R$ milhoes correntes",
                        nota="transcrito; valores orcados, nao executados"))
grava("cde-receitas-orcadas-cgu.csv", out)

# 5. Ipea Radar n. 53, Tabela 1 (US$ bilhoes correntes) - transcrito; linha 5.1 = lucro liquido com derivados de petroleo (segmento)
PET = {"2006": 2.5, "2010": 2.1, "2011": -5.7, "2012": -11.7, "2013": -8.2, "2014": -15.4, "2015": 5.7, "2016": 5.7}
out = [dict(indicador="petrobras_lucro_liquido_derivados", fonte="Ipea Radar n. 53 (out/2017), Tabela 1 linha 5.1; Petrobras DFP/RMF",
            definicao_linha="Lucro liquido do segmento derivados de petroleo (Petrobras)", ano=int(a), valor=v, unidade="US$ bilhoes correntes",
            nota="transcrito; o texto do Ipea atribui a queda 'aos controles que o governo federal vinha exercendo nos precos'; soma 2011-2014 = -41,0")
       for a, v in PET.items()]
out.append(dict(indicador="petrobras_lucro_liquido_derivados_soma_2011_2014", fonte="calculo proprio sobre a linha acima", definicao_linha="soma acumulada 2011-2014 (linha posta no ano final)",
                ano=2014, valor=round(sum(PET[a] for a in ("2011", "2012", "2013", "2014")), 1), unidade="US$ bilhoes correntes",
                nota="o Ipea escreve 'somou US$ 41 bilhoes'"))
grava("petrobras-resultado-derivados-ipea.csv", out)

# 6. BCB (Relatorios Anuais 2014 e 2015; transcritos em historia/RESULTADO.md secao 5.2) - ja existe a copia local em historia/bruto/bcb-relatorios-inflacao
BCB = [("ipca_gasolina", "IPCA gasolina", {2013: 6.51, 2014: 2.89, 2015: 20.10}),
       ("ipca_energia_eletrica_residencial", "IPCA energia eletrica residencial", {2013: -15.65, 2014: 17.06, 2015: 50.99}),
       ("ipca_onibus_urbano", "IPCA onibus urbano", {2013: 0.04, 2014: 3.86, 2015: 15.09}),
       ("ipca_livres_publicado", "IPCA itens livres (publicado pelo BCB)", {2013: 7.29, 2014: 6.72, 2015: 8.51}),
       ("ipca_monitorados_publicado", "IPCA precos monitorados (publicado pelo BCB)", {2013: 1.54, 2014: 5.32, 2015: 18.07})]
out = [dict(indicador=i, fonte="BCB, Relatorios Anuais 2014 e 2015 (via fontes/dados/historia/RESULTADO.md secao 5.2)", definicao_linha=d, ano=a, valor=v,
            unidade="% no ano", nota="transcrito de historia/RESULTADO.md; copia local do relatorio em historia/bruto/bcb-relatorios-inflacao") for i, d, s in BCB for a, v in s.items()]
grava("ipca-itens-administrados-bcb.csv", out)
