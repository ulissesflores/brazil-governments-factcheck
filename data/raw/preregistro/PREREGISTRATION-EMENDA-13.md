# EMENDA-13: liberdade de expressão e de imprensa (V-Dem) entra como contexto no terminal, não pontua

Data: 2026-10-25. Selada na cadeia `preregistro/manifest.jsonl`. Modifica a EMENDA-03 (visão de terminal: acrescenta um indicador de contexto) e nada do índice.

## A. O fato e a ordem dos acontecimentos (declarados)

1. O pré-registro da fase 2 (§4, área Instituições) tem quatro itens do V-Dem: democracia liberal, corrupção política, restrições legislativas e restrições judiciais ao Executivo. Não há item de liberdade de imprensa.
2. Em 2026-10-25, depois da publicação do índice (v1.0.0, 2026-10-23), o editor pediu "um indicador de mídia ou liberdade de imprensa". Antes de escrever esta emenda, a série do Brasil foi inspecionada no arquivo já selado `vdem-fase2/bruto/vdemdata_v16_vdem.RData` (V-Dem v16): a variável `v2x_freexp_altinf` (Freedom of Expression and Alternative Sources of Information index, 0-1, intervalar) existe, com `codelow` e `codehigh`, e os valores 1990-2025 foram vistos.
3. Por isso o item é pós-hoc: foi escolhido com o resultado do índice publicado e a série à vista. O pré-registro existe para impedir exatamente isso de mudar uma nota.

## B. A decisão

1. `v2x_freexp_altinf` (estimativa, codelow, codehigh; V-Dem v16, Brasil) é derivada do mesmo RData selado para `vdem-fase2/series/vdem_brasil_v16.csv`, pela mesma rotina `gerar_series.py`, e entra no terminal como indicador de CONTEXTO no domínio "Instituições (V-Dem)", com a marca "contexto: não pontua".
2. NÃO entra no índice composto nesta edição: nem na camada N, nem na P. As balizas, os pesos, os sorteios e as leituras por mandato publicados em v1.0.0 não mudam por esta emenda.
3. A porta 1 (direção em artigo Q1) não é invocada nem necessária: "item sem direção acordada é contexto, nunca pontua" (fase 2, §2). A porta 3 ("um conceito, uma vez") é respeitada no terminal: das variáveis de mídia do mesmo arquivo (`v2mecenefm`, esforço de censura; `v2meharjrn`, assédio a jornalistas; `v2mecrit`, `v2merange`, `v2mebias`, `v2meslfcen`) nenhuma entra; o índice `v2x_freexp_altinf` já as agrega pelo modelo de medição publicado do V-Dem.
4. Reavaliação por emenda própria quando houver nova edição do índice com novo período-base; aí o item concorre pelas três portas antes de qualquer cálculo, e com a direção sustentada em artigo Q1 com DOI.

## C. O que a página e o artigo dizem

O terminal mostra a série com os limites de incerteza publicados pelo V-Dem e a versão (v16). O artigo pode descrever a trajetória (valores e anos), nunca atribuir causa a governo. A sobreposição conceitual com `v2x_libdem` (que contém a liberdade de expressão pelo componente eleitoral) é declarada onde a série aparecer.
