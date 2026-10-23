#!/bin/sh
while pgrep -f "scripts/fila.sh|scripts/fila2.sh|scripts/fila3.sh|baixar_2_planalto.py" >/dev/null; do sleep 3; done
python3 -I scripts/baixar_2_planalto.py alvos_6.tsv > baixar_6.log 2>&1
