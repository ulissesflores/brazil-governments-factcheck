#!/bin/sh
while pgrep -f "scripts/fila.sh" >/dev/null || pgrep -f "baixar_1_bcb_ipea.py" >/dev/null; do sleep 3; done
python3 -I scripts/baixar_2_planalto.py alvos_4.tsv > baixar_4.log 2>&1
