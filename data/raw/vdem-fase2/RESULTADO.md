# V-Dem, Brasil, itens da fase 2 (coleta de 2026-10-20)

## O que foi achado

Os cinco itens do pré-registro (`v2x_libdem`, `v2x_corr`, `v2xlg_legcon`, `v2x_jucon`, `v2clstown`) e o bônus `v2x_polyarchy`, com estimativa pontual, `_codelow` e `_codehigh`, versão V-Dem **v16 (março de 2026)**, Brasil, 1789-2025. `v2clstown` também em escala original (`v2clstown_osp` e limites). Dados nas séries longas em `series/vdem_brasil_v16.csv` (4.863 linhas, nenhuma interpolada; valor ausente fica sem linha).

Fonte efetiva: `vdem.RData` do pacote oficial `vdemdata` (repositório GitHub `vdeminstitute/vdemdata`, tag V16, `DESCRIPTION` Version 16.0, commit "v16 release" de 2026-03-17), que contém o conjunto Country-Year Full+Others. Leitura com o pacote Python `rdata` (puro, sem executar código R).

| Item | Cobertura (anos com valor) | Lacunas entre extremos |
|---|---|---|
| v2x_libdem | 1789-2025 (235) | 1824, 1825 |
| v2x_corr | 1789-2025 (237) | nenhuma |
| v2xlg_legcon | 1823-2025 (203) | nenhuma |
| v2x_jucon | 1789-2025 (237) | nenhuma |
| v2clstown (+ _osp) | 1789-2025 (237) | nenhuma |
| v2x_polyarchy (bônus) | 1789-2025 (235) | 1824, 1825 |

## Valores (estimativa [codelow, codehigh], v16)

| Item | 1994 | 2002 | 2010 | 2016 | 2018 | 2022 | 2025 (último) |
|---|---|---|---|---|---|---|---|
| v2x_libdem (mais alto = mais democrático) | 0,707 [0,659; 0,764] | 0,721 [0,670; 0,775] | 0,776 [0,737; 0,822] | 0,653 [0,608; 0,709] | 0,608 [0,555; 0,663] | 0,540 [0,489; 0,590] | 0,704 [0,650; 0,759] |
| v2x_corr (mais alto = MAIS corrupto) | 0,511 [0,457; 0,563] | 0,545 [0,496; 0,591] | 0,494 [0,465; 0,520] | 0,535 [0,512; 0,567] | 0,535 [0,502; 0,559] | 0,545 [0,514; 0,574] | 0,423 [0,390; 0,457] |
| v2xlg_legcon | 0,831 [0,752; 0,932] | 0,831 [0,752; 0,932] | 0,902 [0,860; 0,979] | 0,830 [0,762; 0,945] | 0,792 [0,708; 0,906] | 0,822 [0,747; 0,928] | 0,933 [0,902; 0,990] |
| v2x_jucon | 0,825 [0,760; 0,937] | 0,825 [0,760; 0,937] | 0,930 [0,900; 0,984] | 0,872 [0,823; 0,956] | 0,859 [0,797; 0,942] | 0,827 [0,764; 0,936] | 0,954 [0,932; 0,993] |
| v2clstown (escala do modelo; mais alto = MENOS propriedade estatal) | 1,185 [0,721; 1,652] | 1,031 [0,752; 1,253] | 1,031 [0,752; 1,253] | 1,659 [1,297; 1,989] | 1,659 [1,297; 1,989] | 1,313 [0,986; 1,634] | 1,182 [0,799; 1,525] |
| v2clstown_osp (escala original 0-4) | 3,011 [2,776; 3,286] | 2,925 [2,774; 3,057] | 2,925 [2,774; 3,057] | 3,264 [3,092; 3,446] | 3,264 [3,092; 3,446] | 3,080 [2,922; 3,276] | 3,011 [2,815; 3,217] |
| v2x_polyarchy (bônus) | 0,846 [0,809; 0,896] | 0,856 [0,821; 0,903] | 0,871 [0,836; 0,908] | 0,781 [0,735; 0,830] | 0,749 [0,703; 0,810] | 0,699 [0,644; 0,753] | 0,784 [0,733; 0,839] |

Valores repetidos entre anos (ex.: `v2clstown` 2002 = 2010, 2016 = 2018; `v2xlg_legcon`/`v2x_jucon` 1994 = 2002) estão assim na fonte; não foram preenchidos por mim.

## Conferência

- OWID (5 slugs: `liberal-democracy-index`, `political-corruption-index`, `legislative-constraints-on-the-executive-index`, `judicial-constraints-on-the-executive-index`, `electoral-democracy-index`) x pacote oficial v16, Brasil: **0 anos divergentes** nos cinco índices (metadados OWID: V-Dem "Democracy report v16", lastUpdated 2026-03-17). O arquivo OWID de `v2x_polyarchy` baixado agora tem o mesmo sha256 (`a0843a64...5afc`) do que já está em `/Users/ulissesflores/Developer/brazil-governments-factcheck/data/raw/mundo/vdem_owid/bruto/owid_electoral_democracy_index_8paises.csv`; ou seja, a série que já tínhamos é a v16 e bate com o pacote.
- Vintage (efeito medido, Brasil): v15 -> v16, mediana de |diferença| 1960+ entre 0,001 (`v2x_corr`) e 0,006 (`v2clstown`); máxima 0,031 (`v2clstown`, 2018). v12 -> v16 (1960-2020): máxima 0,193 (`v2clstown`, 2020) e 0,164 (`v2x_jucon`, 1987). Detalhe em `quebras.csv` e `series/conferencia-saida.txt`.

## O que NÃO foi achado, e por quê

- **Download oficial do portal v-dem.net**: as páginas `https://v-dem.net/data/the-v-dem-dataset/country-year-v-dem-fullothers-v16/` e `...country-year-v-dem-core-v16/` (HTTP 200) servem um formulário (e-mail, gênero, aceite de privacidade, formato, anti-robô) antes do ZIP. Não usado; registrado como não acessível sem cadastro. Consequência: o ZIP com codebook completo, "What's New" e "Cautionary Notes" da v16 não foi lido. O texto oficial sobre as revisões entre versões, portanto, não está colhido (declarado em `quebras.csv`).
- **v2clstown no OWID**: não existe nos 5 slugs de democracia; o slug candidato `state-ownership-of-economy` devolveu 404 (só esse foi testado). Não é necessário: veio completo do conjunto Full+Others.
- Wayback não foi preciso.

## Desvios e atenções declarados

1. **Direção de `v2clstown` no pré-registro.** O pré-registro (§ bloco P) lista "Propriedade estatal da economia (v2clstown) | menor". No codebook v16, a escala vai de 0 ("virtualmente todo o capital valioso pertence ao Estado") a 4 ("muito pouco"): **valor mais alto = MENOS propriedade estatal**. "Menor propriedade estatal" é, portanto, v2clstown mais ALTO. O sinal tem de ser invertido na fase de pontuação se o item entrar. Não alterei o pré-registro. O codebook diz também que a variável não mede receita/despesa como % do produto.
2. **`v2x_corr` tem direção invertida em relação aos demais** (mais alto = mais corrupto, codebook); coerente com "menor" do pré-registro.
3. **Fonte alternativa ao formulário:** o pacote `vdemdata` é distribuição do próprio V-Dem Institute (licença CC BY-SA 4.0 declarada no portal), não um contorno técnico do formulário; ainda assim é um caminho diferente do ZIP do portal, e o dado equivale ao "Full+Others" v16 só na medida em que o pacote o declara ("most recent full V-Dem data set plus external variables").
4. **Arquivos grandes:** `vdemdata_v16_vdem.RData` (33.878.255 bytes), `vdemdata_V15_vdem.RData` (33.163.029) e `vdemdata_V12_vdem.RData` (29.063.644) passam de 25 MB, são o único caminho para o conjunto completo, e `bruto/.gitignore` deixa só o hash no repositório (`manifest.jsonl`; recuperar com `govfc.chain restore`).
5. **Limites de incerteza:** `codelow`/`codehigh` são os publicados pelo V-Dem; a largura nominal (por exemplo, 68%) não foi verificada nos documentos colhidos, então não é afirmada aqui.
6. Os arquivos OWID baixados contêm todos os países (o parâmetro `country=BRA` foi ignorado pelo servidor), por isso ~1 MB cada.
7. Cada release do V-Dem reestima a série histórica inteira; valores citados valem para **v16**. Citar sempre a versão.

## Cadeia de hash (`govfc.chain verify`)

```text
15 lines; head d41e0030353d912fc454e8f807bf4b05c53d38f0018c7981417d2936d9564d45; OK
```

## Arquivos

- `manifest.jsonl` (cadeia, 15 linhas), `bruto/` (15 downloads, mais `.gitignore`), `series/vdem_brasil_v16.csv`, `series/conferencia-saida.txt`, `quebras.csv` (7 linhas, cabeçalho idêntico ao de `moeda-fiscal/quebras.csv`), `gerar_series.py` (reproduz tudo a partir de `bruto/`; precisa de `rdata` e `pandas`).
