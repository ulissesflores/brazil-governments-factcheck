# RESULTADO - coleta BCB da fase 2 (2026-10-20)

Pasta: `/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/bcb-fase2/`
Cadeia de hash: `manifest.jsonl` (todo download passou por `govfc.chain add` no momento do download). Scripts: `scripts/`. Pre-registro lido: `../preregistro/PREREGISTRATION-FASE-2.md` (§4, §8, Contexto).

## Resultado em uma tabela (valores como publicados pelo SGS em 2026-10-20; mes = mes de referencia)

Series em % do PIB ou % da renda:

| Serie | Inicio | dez/1994 | dez/2002 | dez/2010 | dez/2016 | dez/2018 | dez/2022 | Ultimo mes |
|---|---|---|---|---|---|---|---|---|
| Divida liquida do setor publico, consolidado, % PIB (SGS 4513) | 2001-12 | sem dado | 59.93 | 37.98 | 46.14 | 52.77 | 56.13 | 69.27 (2026-08) |
| DBGG % PIB, metodologia 2008 (SGS 13762) | 2006-12 | sem dado | sem dado | 51.77 | 69.84 | 75.27 | 71.68 | 82.87 (2026-08) |
| DBGG % PIB, metodologia ate 2007 (SGS 4537) | 2002-01 | sem dado | 76.10 | 62.43 | 77.42 | 84.78 | 83.94 | 94.54 (2026-08) |
| Endividamento familias / renda 12m, total (SGS 29037) | 2005-01 | sem dado | sem dado | 33.97 | 38.11 | 39.02 | 49.14 | 49.86 (2026-07) |
| Endividamento familias / renda 12m, exceto habitacional (SGS 29038) | 2005-01 | sem dado | sem dado | 27.04 | 22.22 | 23.21 | 31.16 | 30.81 (2026-07) |
| Comprometimento de renda, total, dessaz. (SGS 29034) | 2005-03 | sem dado | sem dado | 23.96 | 23.22 | 22.58 | 27.57 | 28.72 (2026-07) |
| Comprometimento de renda, exceto habitacional, dessaz. (SGS 29035) | 2005-03 | sem dado | sem dado | 23.17 | 21.13 | 20.52 | 25.48 | 26.43 (2026-07) |
| Endividamento, serie antiga (19882) (SGS 19882) | 2005-01 | sem dado | sem dado | 40.71 | 44.84 | 46.06 | sem dado | 59.90 (2021-08) |
| Endividamento, serie antiga (19881) (SGS 19881) | 2005-03 | sem dado | sem dado | 28.48 | 27.84 | 27.48 | sem dado | 30.15 (2021-08) |

Reservas internacionais, US$ milhoes:

| Serie | Inicio | dez/1994 | dez/2002 | dez/2010 | dez/2016 | dez/2018 | dez/2022 | Ultimo mes |
|---|---|---|---|---|---|---|---|---|
| Reservas, CONCEITO CAIXA, fim de mes (SGS 3546) | 1971-01 | 38 806 | 37 823 | 288 575 | 365 016 | 374 715 | 324 703 | 362 821 (2026-09) |
| Reservas, conceito liquidez, ultimo dia util do mes (SGS 13982, derivado do diario) | 2008-01 | sem dado | sem dado | 288 575 | 372 221 | 386 965 | 337 703 | 368 393 (2026-10-19, MES INCOMPLETO) |

Leitura: "sem dado" = a serie nao existe naquele mes; nada foi estimado nem interpolado. Series de saldos em R$ milhoes (SGS 4468 e 4471) estao em `series/` mas NAO entram aqui: nao sao % do PIB, nao sao consolidadas e os valores de 1991-1994 vem de moedas anteriores convertidas.

## Divida bruta (DBGG): as duas metodologias, sobreposicao mensal

`derivado/sobreposicao_dbgg.csv` (SGS 4537 menos SGS 13762, em pontos percentuais do PIB; sem encadear, so medido).

| Janela | n meses | Diferenca media (antiga menos nova) | Mediana | Desvio-padrao | Minimo | Maximo |
|---|---|---|---|---|---|---|
| 2006-12 a 2025-12 (janela do pre-registro) | 229 | 7.302 pp | 7.63 | 2.876 | 1.68 | 14.69 |
| 2006-12 a 2026-08 (todo o bruto) | 237 | 7.498 pp | 7.73 | 3.022 | 1.68 | 14.78 |

A diferenca NAO e constante; a media anual (pp) mostra tendencia e mudanca de nivel:

| Ano | 2006 | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Media da diferenca | 9.12 | 5.93 | 4.02 | 2.51 | 7.12 | 7.94 | 7.14 | 5.15 | 4.72 | 4.42 | 4.75 | 7.54 | 8.57 | 8.63 | 7.46 | 10.12 | 10.73 | 9.83 | 9.27 | 12.72 | 13.12 |

Achado que muda o uso do §8: um unico deslocamento medio (7.302 pp) superestima a diferenca em 2007-2009 e em 2013-2016 (medias anuais de 2,5 a 5,9 pp) e a subestima em 2021-2026 (9,3 a 13,1 pp). A diferenca e a carteira de titulos do BC menos as compromissadas, que se movem com a politica monetaria (leitura minha do texto oficial, nao testada). O pre-registro diz "diferenca media"; o efeito impresso no item precisa declarar tambem o desvio-padrao (2.876 pp) e a nao estacionariedade.

Conferencia contra a fonte primaria: o boxe do Relatorio de Inflacao de marco/2008 (hasheado) diz que a diferenca entre os conceitos recuou "de 9,2 p.p., ao final de 2006, para 3,8 p.p. em janeiro de 2008". Nos dados do SGS de hoje: dez/2006 = 9,12 pp e jan/2008 = 3,79 pp. Coincide. Os niveis de dez/2007 no boxe (novo 57,4% e antigo 63,8% do PIB) diferem dos de hoje (56,72 e 63,02): o SGS atual esta em outra vintage (hipotese nao testada: revisao do PIB).

## Mudanca de metodologia de 2008 (texto oficial)

Citada literalmente em `quebras.csv` (linha 1), com URLs. Fontes primarias hasheadas: `bruto/doc_ri_2008_03_boxe_dbgg.pdf` (Relatorio de Inflacao, marco/2008, boxe "Alteracao na Metodologia de Calculo da Divida Bruta do Governo Geral (DBGG)") e `bruto/doc_nota_tecnica_47_2018.pdf` (Nota Tecnica BCB 47). Em resumo: ate 2007 a DBGG incluia toda a carteira de titulos publicos do BC e nao incluia as operacoes compromissadas; desde 2008 inclui as compromissadas e exclui os "titulos livres" na carteira do BC; a serie nova comeca em dez/2006.

## Endividamento das familias: series antigas x novas

`derivado/sobreposicao_endividamento_familias.csv`. Pares inferidos pela ordem de grandeza (hipotese: 19882 = total, 19881 = exceto habitacional; o nome oficial das series antigas nao foi achado).

| Par | n | Diferenca media (antiga menos nova) | Min | Max | Meses iguais |
|---|---|---|---|---|---|
| 19882 x 29037 | 200 | 7.151 pp | 2.81 | 15.52 | 0 |
| 19881 x 29038 | 198 | 3.342 pp | 0.92 | 6.12 | 0 |

Diferenca media por ano, par total: 2005: 3.01, 2006: 3.47, 2007: 4.44, 2008: 5.42, 2009: 6.02, 2010: 6.6, 2011: 7.31, 2012: 7.96, 2013: 8.81, 2014: 9.49, 2015: 8.2, 2016: 6.9, 2017: 6.98, 2018: 7.06, 2019: 6.98, 2020: 10.62, 2021: 14.87. As series antigas terminam em ago/2021; as novas (SGS 29037/29038) cobrem 2005-01 a 2026-07. As duas series (antiga e nova) comecam em 2005; portanto ligar 19882 a 29037 NAO amplia a cobertura para tras. O §4 cita "SGS 29037 e 19882" como se a antiga estendesse a serie; nao estende. Cobertura de familias: 2005-01 a 2026-07 (total), 2005-03 a 2026-07 (comprometimento).

## Reservas internacionais (bonus): o SGS 3546 e conceito CAIXA, nao liquidez

`derivado/conferencia_reservas_3546_vs_13621_13982.csv`. Comparei o SGS 3546 com o ultimo dia util de cada mes das series diarias do BCB: conceito caixa (SGS 13621, desde 1998-09) coincide em 331 de 337 meses (os demais diferem de 1 a 67 US$ milhoes); conceito liquidez (SGS 13982, desde 2008-01) coincide em 73 de 225 meses e passa a divergir a partir de 2008-09. Portanto o pedido ("conceito liquidez, SGS 3546") esta rotulado errado: 3546 e caixa. Para liquidez entreguei `series/reservas_internacionais_liquidez_fim_de_mes_usd_mi_sgs13982.csv` (valor observado do ultimo dia util com dado; so de 2008). Nao verifiquei o nome oficial do 3546 (o CKAN nao tem registro).

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
- `series/`: um CSV longo por serie (`indicador,fonte,definicao_linha,ano,mes_ou_trimestre,valor,unidade,nota,vintage`); 13 arquivos.
- `derivado/`: `sobreposicao_dbgg.csv`, `sobreposicao_endividamento_familias.csv`, `conferencia_reservas_3546_vs_13621_13982.csv`, `_resumo.json` (numeros desta pagina).
- `quebras.csv`: 3 linhas (DBGG 2008; DLSP/Petrobras-Eletrobras; familias 19881/19882 -> 29037/29038).

## Verificacao da cadeia (`python3 -m govfc.chain verify`)

```text
42 lines; head 0e1ecf0e261da95bbafcc01af6586c5d959dc1f0057a7b36e5b5afff4e3114c6; OK
```
