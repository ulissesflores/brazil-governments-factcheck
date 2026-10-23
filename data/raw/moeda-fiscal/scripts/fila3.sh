#!/bin/sh
while pgrep -f "scripts/fila.sh|scripts/fila2.sh|baixar_1_bcb_ipea.py|baixar_2_planalto.py" >/dev/null; do sleep 3; done
python3 -I scripts/baixar_2_planalto.py alvos_5.tsv forcar > baixar_5.log 2>&1
