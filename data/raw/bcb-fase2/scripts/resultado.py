"""Gera RESULTADO.md a partir de derivado/_resumo.json e do verify. Roda depois de construir.py e quebras.py."""
import json, subprocess
from pathlib import Path
P = Path(__file__).resolve().parent.parent
R = json.load(open(P / "derivado/_resumo.json"))
T = R["tab"]
def f(v, nd=2):
    return "sem dado" if v is None else (f"{v:,.{nd}f}".replace(",", " ") if abs(v) >= 1000 else f"{v:.{nd}f}")
def linha(c, rot, nd=2):
    t = T[str(c)]; ch = t["chaves"]
    ult = f"{f(t['ult_v'], nd)} ({t['ult'][0]}-{t['ult'][1]:02d})"
    return f"| {rot} (SGS {c}) | {t['ini'][0]}-{t['ini'][1]:02d} | " + " | ".join(f(ch[k], nd) for k in ("1994-12", "2002-12", "2010-12", "2016-12", "2018-12", "2022-12")) + f" | {ult} |"
env = {"PYTHONPATH": "/Users/ulissesflores/Developer/brazil-governments-factcheck/code", "PATH": "/usr/bin:/opt/homebrew/bin"}
ver = subprocess.run(["python3", "-m", "govfc.chain", "verify", str(P)], capture_output=True, text=True, cwd="/Users/ulissesflores/Developer/brazil-governments-factcheck", env=env)
vtxt = (ver.stdout + ver.stderr).strip()
sob = R["sob"]; sa = R["sob_ano"]; res = R["reservas"]; fam = R["fam"]; fa = R["fam_ano"]
cab = "| Serie | Inicio | dez/1994 | dez/2002 | dez/2010 | dez/2016 | dez/2018 | dez/2022 | Ultimo mes |\n|---|---|---|---|---|---|---|---|---|"
ln = lambda xs: "\n".join(xs)
liq = res["liq_dez"]; lu = res["liq_ult"]
md = f"""# RESULTADO - coleta BCB da fase 2 (2026-10-20)

Pasta: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/bcb-fase2/`
Cadeia de hash: `manifest.jsonl` (todo download passou por `govfc.chain add` no momento do download). Scripts: `scripts/`. Pre-registro lido: `../preregistro/PREREGISTRATION-FASE-2.md` (§4, §8, Contexto).

## Resultado em uma tabela (valores como publicados pelo SGS em 2026-10-20; mes = mes de referencia)

Series em % do PIB ou % da renda:

{cab}
{ln([linha(4513,"Divida liquida do setor publico, consolidado, % PIB"), linha(13762,"DBGG % PIB, metodologia 2008"), linha(4537,"DBGG % PIB, metodologia ate 2007"), linha(29037,"Endividamento familias / renda 12m, total"), linha(29038,"Endividamento familias / renda 12m, exceto habitacional"), linha(29034,"Comprometimento de renda, total, dessaz."), linha(29035,"Comprometimento de renda, exceto habitacional, dessaz."), linha(19882,"Endividamento, serie antiga (19882)"), linha(19881,"Endividamento, serie antiga (19881)")])}

Reservas internacionais, US$ milhoes:

{cab}
{ln([linha(3546,"Reservas, CONCEITO CAIXA, fim de mes", 0)])}
| Reservas, conceito liquidez, ultimo dia util do mes (SGS 13982, derivado do diario) | 2008-01 | sem dado | sem dado | {f(liq['2010-12'][1],0)} | {f(liq['2016-12'][1],0)} | {f(liq['2018-12'][1],0)} | {f(liq['2022-12'][1],0)} | {f(lu[1][1],0)} (2026-10-{lu[1][0]:02d}, MES INCOMPLETO) |

Leitura: "sem dado" = a serie nao existe naquele mes; nada foi estimado nem interpolado. Series de saldos em R$ milhoes (SGS 4468 e 4471) estao em `series/` mas NAO entram aqui: nao sao % do PIB, nao sao consolidadas e os valores de 1991-1994 vem de moedas anteriores convertidas.

## Divida bruta (DBGG): as duas metodologias, sobreposicao mensal

`derivado/sobreposicao_dbgg.csv` (SGS 4537 menos SGS 13762, em pontos percentuais do PIB; sem encadear, so medido).

| Janela | n meses | Diferenca media (antiga menos nova) | Mediana | Desvio-padrao | Minimo | Maximo |
|---|---|---|---|---|---|---|
| 2006-12 a 2025-12 (janela do pre-registro) | {sob['2006-12 a 2025-12']['n']} | {sob['2006-12 a 2025-12']['media']} pp | {sob['2006-12 a 2025-12']['mediana']} | {sob['2006-12 a 2025-12']['dp']} | {sob['2006-12 a 2025-12']['min']} | {sob['2006-12 a 2025-12']['max']} |
| 2006-12 a 2026-08 (todo o bruto) | {sob['2006-12 a ultimo mes']['n']} | {sob['2006-12 a ultimo mes']['media']} pp | {sob['2006-12 a ultimo mes']['mediana']} | {sob['2006-12 a ultimo mes']['dp']} | {sob['2006-12 a ultimo mes']['min']} | {sob['2006-12 a ultimo mes']['max']} |

A diferenca NAO e constante; a media anual (pp) mostra tendencia e mudanca de nivel:

| Ano | {" | ".join(sa)} |
|{"---|" * (len(sa) + 1)}
| Media da diferenca | {" | ".join(str(sa[a][0]) for a in sa)} |

Achado que muda o uso do §8: um unico deslocamento medio ({sob['2006-12 a 2025-12']['media']} pp) superestima a diferenca em 2007-2009 e em 2013-2016 (medias anuais de 2,5 a 5,9 pp) e a subestima em 2021-2026 (9,3 a 13,1 pp). A diferenca e a carteira de titulos do BC menos as compromissadas, que se movem com a politica monetaria (leitura minha do texto oficial, nao testada). O pre-registro diz "diferenca media"; o efeito impresso no item precisa declarar tambem o desvio-padrao ({sob['2006-12 a 2025-12']['dp']} pp) e a nao estacionariedade.

Conferencia contra a fonte primaria: o boxe do Relatorio de Inflacao de marco/2008 (hasheado) diz que a diferenca entre os conceitos recuou "de 9,2 p.p., ao final de 2006, para 3,8 p.p. em janeiro de 2008". Nos dados do SGS de hoje: dez/2006 = 9,12 pp e jan/2008 = 3,79 pp. Coincide. Os niveis de dez/2007 no boxe (novo 57,4% e antigo 63,8% do PIB) diferem dos de hoje (56,72 e 63,02): o SGS atual esta em outra vintage (hipotese nao testada: revisao do PIB).

## Mudanca de metodologia de 2008 (texto oficial)

Citada literalmente em `quebras.csv` (linha 1), com URLs. Fontes primarias hasheadas: `bruto/doc_ri_2008_03_boxe_dbgg.pdf` (Relatorio de Inflacao, marco/2008, boxe "Alteracao na Metodologia de Calculo da Divida Bruta do Governo Geral (DBGG)") e `bruto/doc_nota_tecnica_47_2018.pdf` (Nota Tecnica BCB 47). Em resumo: ate 2007 a DBGG incluia toda a carteira de titulos publicos do BC e nao incluia as operacoes compromissadas; desde 2008 inclui as compromissadas e exclui os "titulos livres" na carteira do BC; a serie nova comeca em dez/2006.

## Endividamento das familias: series antigas x novas

`derivado/sobreposicao_endividamento_familias.csv`. Pares inferidos pela ordem de grandeza (hipotese: 19882 = total, 19881 = exceto habitacional; o nome oficial das series antigas nao foi achado).

| Par | n | Diferenca media (antiga menos nova) | Min | Max | Meses iguais |
|---|---|---|---|---|---|
| 19882 x 29037 | {fam['19882_vs_29037']['n']} | {fam['19882_vs_29037']['media']} pp | {fam['19882_vs_29037']['min']} | {fam['19882_vs_29037']['max']} | {fam['19882_vs_29037']['n_iguais']} |
| 19881 x 29038 | {fam['19881_vs_29038']['n']} | {fam['19881_vs_29038']['media']} pp | {fam['19881_vs_29038']['min']} | {fam['19881_vs_29038']['max']} | {fam['19881_vs_29038']['n_iguais']} |

Diferenca media por ano, par total: {", ".join(f"{a}: {v}" for a, v in fa['19882_vs_29037'].items())}. As series antigas terminam em ago/2021; as novas (SGS 29037/29038) cobrem 2005-01 a 2026-07. As duas series (antiga e nova) comecam em 2005; portanto ligar 19882 a 29037 NAO amplia a cobertura para tras. O §4 cita "SGS 29037 e 19882" como se a antiga estendesse a serie; nao estende. Cobertura de familias: 2005-01 a 2026-07 (total), 2005-03 a 2026-07 (comprometimento).

## Reservas internacionais (bonus): o SGS 3546 e conceito CAIXA, nao liquidez

`derivado/conferencia_reservas_3546_vs_13621_13982.csv`. Comparei o SGS 3546 com o ultimo dia util de cada mes das series diarias do BCB: conceito caixa (SGS 13621, desde 1998-09) coincide em {res['caixa_iguais']} de {res['n_caixa']} meses (os demais diferem de {res['caixa_dif_min']:.0f} a {res['caixa_dif_max']:.0f} US$ milhoes); conceito liquidez (SGS 13982, desde 2008-01) coincide em {res['liq_iguais']} de {res['n_liq']} meses e passa a divergir a partir de {res['liq_primeira_dif'][0]}-{res['liq_primeira_dif'][1]:02d}. Portanto o pedido ("conceito liquidez, SGS 3546") esta rotulado errado: 3546 e caixa. Para liquidez entreguei `series/reservas_internacionais_liquidez_fim_de_mes_usd_mi_sgs13982.csv` (valor observado do ultimo dia util com dado; so de 2008). Nao verifiquei o nome oficial do 3546 (o CKAN nao tem registro).

## O que nao foi achado

- Divida liquida do setor publico em % do PIB ANTES de dez/2001: nao existe no SGS (SGS 4513 e todas as irmas 4503-4513 comecam em 2001-12; o proprio pedido dizia dez/1991). A serie antiga, com Petrobras, esta nas "tabelas especiais" do BCB (pagina `https://www.bcb.gov.br/estatisticas/tabelasespeciais`), que e uma aplicacao JavaScript: nao foi lida sem navegador. Existem saldos em R$ milhoes desde 1991 (SGS 4468 governo federal e BC; SGS 4471 estaduais e municipais; sem estatais, sem % do PIB). Dez/1994 para a divida liquida em % do PIB: sem dado. FHC na grade (inicio -> fim) fica sem o inicio pela fonte SGS; proximo passo: tabelas especiais por navegador autorizado ou por Ipeadata (nao testado).
- Nome oficial, unidade e metodo das series 19881 e 19882: o CKAN do BCB nao as lista (duas tentativas) e a pagina de metadados do SGS (testada para o 3546) respondeu "System unavailable".
- Nome oficial do SGS 3546: idem.
- Nota do BCB sobre a troca 19881/19882 -> 29037/29038: nao localizada.
- Series de comprometimento (29034/29035) tem versao sem ajuste sazonal (SGS 29265/29266) que nao foi coletada; as coletadas sao as com ajuste sazonal, como pedido.

## Desvios declarados em relacao ao pedido

1. SGS 4513 comeca em dez/2001, nao dez/1991 (acima).
2. SGS 4537 tem o primeiro dado em jan/2002 (o catalogo diz 31-12-2001); o pedido dizia dez/2001. Sobreposicao medida a partir de dez/2006.
3. SGS 3546 e conceito caixa, nao liquidez (acima). Liquidez entregue a parte, derivada do diario.
4. As series 19881/19882 existem e terminam em ago/2021; sua identidade e uma hipotese pela ordem de grandeza.
5. Extras nao pedidos, mantidos porque sustentam o pedido: SGS 13621 e 13982 (diarias, so para a conferencia do conceito), 29029 (denominador RNDBF, nao usado), 4468 e 4471 (saldos em R$ milhoes 1991+), `doc_*` (fontes primarias da mudanca de 2008).
6. Falhas da API: o CKAN do SGS 4471 veio vazio na 1a tentativa (`bruto/ckan_4471.json` e invalido; repeticao em `bruto/ckan_4471_repeticao.json`, ok); a janela 2018-2026 do SGS 13621 voltou HTML "Requisicao invalida" (`bruto/sgs_13621_2018-2026.json` e HTML; repeticao em `bruto/sgs_13621_2018-2026_repeticao.json`, ok). Metadados CKAN de 3546, 19881 e 19882 vieram vazios nas duas tentativas. O `chain add` aceitou os arquivos defeituosos (nao valida o conteudo), por isso ficam na cadeia; nenhuma serie usa esses dois arquivos.
7. Antes do primeiro download hasheado fiz sondas `ultimos/2` e `ultimos/1` (sem salvar) para ver se os codigos respondiam, e consultas ao CKAN para localizar series (resultados nao salvos, so usados para decidir o que baixar). Nenhum numero das sondas entrou nas tabelas.

## Arquivos

- `bruto/`: JSON do SGS (serie completa sem janela para as mensais), metadados CKAN, fontes primarias em PDF/HTML.
- `series/`: um CSV longo por serie (`indicador,fonte,definicao_linha,ano,mes_ou_trimestre,valor,unidade,nota,vintage`); {len(list((P / 'series').glob('*.csv')))} arquivos.
- `derivado/`: `sobreposicao_dbgg.csv`, `sobreposicao_endividamento_familias.csv`, `conferencia_reservas_3546_vs_13621_13982.csv`, `_resumo.json` (numeros desta pagina).
- `quebras.csv`: 3 linhas (DBGG 2008; DLSP/Petrobras-Eletrobras; familias 19881/19882 -> 29037/29038).

## Verificacao da cadeia (`python3 -m govfc.chain verify`)

```text
{vtxt}
```
"""
(P / "RESULTADO.md").write_text(md)
print(vtxt)
