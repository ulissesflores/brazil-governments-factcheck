#!/bin/bash
# Baixa o conjunto 'Reajuste de Planos Coletivos' (PDA-043 RPC) da ANS pela cadeia de hash. Serial (a cadeia nao aceita escrita concorrente).
P=/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/ans-planos-fase2
B=https://dadosabertos.ans.gov.br/FTP/PDA/RPC
cd /Users/ulissesflores/Developer/brazil-governments-factcheck || exit 1
export PYTHONPATH=code
nomes="pda-043-rpc-2005_2009.csv pda-043-rpc-2010_2014.csv"
for a in $(seq 2015 2026); do for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
  [ "$a$m" -le 202608 ] && nomes="$nomes pda-043-rpc-$a$m.csv"; done; done
for n in $nomes; do
  [ "$n" = "pda-043-rpc-201501.csv" ] && continue   # ja baixado e registrado (seq 4)
  python3 -m govfc.chain add "$P" "$B/$n" "$P/bruto/ans/rpc/$n" --nota "ANS dados abertos PDA-043 RPC (reajuste de planos coletivos): $n" | python3 -c "import sys,json;d=json.loads(sys.stdin.readline());print(d['seq'],d['bytes'],d['sha256'][:12],d['arquivo'].split('/')[-1],flush=True)" || echo "FALHA $n"
done
echo FIM
