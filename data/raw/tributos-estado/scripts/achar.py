# uso: achar.py <arquivo> <regex> [antes] [depois] [n]  -- mostra trechos (texto limpo, espacos normalizados)
import re, sys
sys.path.insert(0, "/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/scripts")
import txt
t = re.sub(r"\s+", " ", txt.ler(sys.argv[1]))
a = int(sys.argv[3]) if len(sys.argv) > 3 else 80
d = int(sys.argv[4]) if len(sys.argv) > 4 else 300
n = int(sys.argv[5]) if len(sys.argv) > 5 else 3
for m in list(re.finditer(sys.argv[2], t, re.I))[:n]:
    print("  >>", t[max(0, m.start() - a): m.end() + d])
