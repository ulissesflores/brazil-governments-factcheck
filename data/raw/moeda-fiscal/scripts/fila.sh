#!/bin/sh
# espera o baixar_1 (PID 66006) terminar e roda os lotes 2 e 3, um por vez
while kill -0 66006 2>/dev/null; do sleep 3; done
python3 -I scripts/baixar_2_planalto.py alvos_2.tsv >> baixar_2.log 2>&1
python3 -I scripts/baixar_2_planalto.py alvos_3.tsv > baixar_3.log 2>&1
