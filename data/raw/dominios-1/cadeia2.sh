#!/bin/zsh
cd /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/dominios-1
until [ -f cadeia.log ]; do sleep 5; done
./baixar-lote5.sh > lote5.log 2>&1
echo FIM-CADEIA2 > cadeia2.log
