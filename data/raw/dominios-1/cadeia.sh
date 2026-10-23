#!/bin/zsh
cd /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1
until grep -q FIM-LOTE2 lote2.log; do sleep 5; done
./baixar-lote3.sh > lote3.log 2>&1
./baixar-lote4.sh > lote4.log 2>&1
echo FIM-CADEIA > cadeia.log
