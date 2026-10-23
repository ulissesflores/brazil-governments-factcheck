#!/bin/zsh
# Reconstroi tudo a partir de ../bruto (e das pastas irmas), sem rede. Ordem importa: pnad_microdados antes de construir.
cd "$(dirname "$0")" || exit 1
for s in pnad_microdados.py construir.py bolsa_familia.py quebras_gerar.py escrever_md_bf.py escrever_md_definicoes.py escrever_resultado.py; do
  python3 -I "$s" > /dev/null || { echo "FALHOU $s"; exit 1; }
done
python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py verify ..
