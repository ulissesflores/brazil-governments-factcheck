#!/bin/bash
cd "$(dirname "$0")/../.."
for y in $(seq 2010 2025); do
  ./scripts/baixar.sh "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_$y.zip" "bruto/cvm-dfp/dfp_cia_aberta_$y.zip" "CVM Dados Abertos, DFP anual $y (todas as cias abertas)"
done
