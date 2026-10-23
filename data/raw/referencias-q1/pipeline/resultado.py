import json, collections
R=json.load(open('rows.json'))
TEMAS={1:"Médias de janela, tendência linear, volatilidade, aceleração; extrapolar não é prever; ciclo político-econômico",
2:"Quebras de método, emenda de séries, retropolação, vintages e revisões",
3:"Linhas de pobreza internacionais, PPC, linha relativa e absoluta",
4:"Tábuas de mortalidade, excesso de mortes, subregistro de óbitos",
5:"Imposto inflacionário, senhoriagem, regressividade da inflação, moeda e inflação",
6:"Preços administrados represados e ciclo eleitoral de tarifas e combustíveis",
7:"Regra escolar, progressão continuada, repetência, Saeb e aprendizado",
8:"Definição de desemprego e ocupação, subutilização, informalidade",
9:"Homicídios: qualidade do SIM, causa indeterminada, correções",
10:"Índices de democracia (V-Dem): medição por especialistas, incerteza, vintages",
11:"Proveniência, reprodutibilidade, pré-registro, graus de liberdade do pesquisador",
12:"Comparação com o mundo: controle sintético, diferenças em diferenças, termos de troca"}
def first(a): return a.split(",")[0]
def qa(r): return f"{r['scimago_quartil']} ({r['scimago_ano']})" if r['scimago_ano'] else "n/d"
tot=len(R); anc=[r for r in R if r['papel']=='ancora']
anc10=[r for r in anc if r['ano']>=2010]
out=[]
out.append("""# Referências Q1 para as escolhas metodológicas do Raio-X do Brasil

Gerado em 2026-10-19 (pedido do Ulisses: "tudo que eu falar aqui deve ser metodologicamente defensável, com um documento com referências bibliográficas sérias, novas, padrão Q1 de altíssimo nível"). Sem opinião: cada linha diz o que a referência sustenta e o que ela NÃO sustenta.

> [!IMPORTANT]
> Regra de entrada: toda referência passou por DOI conferido no Crossref (registro salvo na cadeia de hashes) E periódico conferido no Scimago (quartil do ano mais recente, 2025, por categoria). **Âncora** = artigo de periódico, Q1 em categoria Scimago compatível com o tema. **Complementar** = o resto (working paper, relatório, periódico fora de Q1, ou Q1 só em área alheia ao tema). Nada entrou de memória sem esses dois conferidos.

## Números

| Medida | Valor |
|---|---|
| Referências conferidas no Crossref | %d |
| Âncoras Q1 (periódico + Q1 em área do tema) | %d |
| das quais de 2010 em diante | %d |
| Complementares (working paper, fora de Q1 ou Q1 em área alheia) | %d |
| Temas pedidos | 12 (todos com ao menos 1 âncora; tema 6 só com âncora teórica) |

Arquivos: `referencias-q1.csv` (16 colunas), `references-q1.bib` (%d entradas, validado com pandoc), `manifest.jsonl` (cadeia de hashes: Crossref, OpenAlex e Scimago), `crossref/`, `openalex/`, `scimago/`.

## Como o Scimago foi lido (limitação declarada)

O Scimago devolve 403 (Cloudflare) para `curl` e `urllib`, então `chain.py add` não consegue baixar. As páginas dos periódicos foram lidas dentro do Chrome real do Ulisses (`fetch()` na própria página). O arquivo guardado na cadeia é um **extrato JSON** (categoria, ano, quartil, sid, título, prefixo de 20 caracteres do SHA-256 do texto da página), registrado com `chain.py add-local`; não é o HTML bruto. Quem quiser conferir abre `https://www.scimagojr.com/journalsearch.php?q=<sid>&tip=sid&clean=0` (o `sid` está no extrato). Cada extrato foi conferido contra o título do periódico no Crossref. O quartil é o do ano mais recente disponível (2025); categorias que o Scimago deixou de listar em anos recentes foram ignoradas.

Outra limitação: o quartil Scimago é por categoria. Um periódico pode ser Q1 numa categoria e Q2 em outra; a coluna `scimago_area` traz todas as categorias do ano com o quartil de cada uma, e a coluna `papel` só diz âncora quando há Q1 numa categoria compatível com o tema (regra no `build`, conjunto de categorias por tema).
""" % (tot,len(anc),len(anc10),tot-len(anc),tot))
for t in range(1,13):
    rs=[r for r in R if r['tema']==t]
    out.append(f"\n## Tema {t}. {TEMAS[t]}\n")
    out.append("| Chave | Autor, ano | Periódico | Scimago | Papel | O que sustenta | O que NÃO sustenta |\n|---|---|---|---|---|---|---|")
    for r in sorted(rs,key=lambda r:(r['papel']!='ancora',-r['ano'])):
        out.append(f"| `{r['chave_bibtex']}` | {first(r['autores'])}, {r['ano']} | {r['periodico']} | {qa(r)} | {r['papel']} | {r['o_que_sustenta']} | {r['o_que_nao_sustenta']} |")
open('resultado_tabelas.md','w').write("\n".join(out)+"\n")
print(len(out))
