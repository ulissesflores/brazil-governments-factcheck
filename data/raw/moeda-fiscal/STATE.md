# STATE moeda-fiscal (2026-10-20)

Pasta: /Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/moeda-fiscal/
Pedido: blocos A (moeda) e B (fiscal) do PREREGISTRATION-EMENDA-03; escrever so nesta pasta. RESULTADO.md e o laudo.

## Estado
- Cadeia: manifest.jsonl; `python3 -I /Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py verify <pasta>`. Baixar SEMPRE sequencial (um writer).
- Ordem de reconstrucao (sem rede, le so bruto): scripts/construir_A_moeda.py, construir_B_fiscal.py, construir_C_textos.py, construir_D_quebras.py, montar_resultado.py.
- Downloads: scripts/baixar_1_bcb_ipea.py (lista interna), baixar_2_planalto.py <alvos_N.tsv> [forcar].

## Falta
- Emendas pagas por RP/ano: bloqueado pelo teto de 25 MB (CGU 32,5 MB; Tesouro 67 MiB). Retomar se o teto for liberado.
- FMI PR 02/40 (2002) e 8-K Lehman (SEC): HTTP 403 com o agente da cadeia.
- LDO 2026, SIOP.

NEG:v1 2026-10-20: SGS 433/190 fora do CKAN (volta se o BCB indexar); Portal da Transparencia HTML = verificacao humana, API = chave (volta com chave); PAN12_TJOVER12 e anualizada, nao mensal (nao voltar a tratar como % a.m.); SGS 432 janela > 10 anos = HTTP 406.
Nota: dois 'kill' por PID proprio (fila.sh) foram feitos apos pgrep -f com padrao relativo; nenhum processo de outro agente foi tocado.
