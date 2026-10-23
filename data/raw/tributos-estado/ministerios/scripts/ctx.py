# uso: ctx.py arquivo regex [antes] [depois] [n]  -- trechos (texto limpo) com o padrao
import re,sys
sys.path.insert(0,"/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/tributos-estado/scripts")
import txt
t=re.sub(r"\s+"," ",txt.ler(sys.argv[1]))
a=int(sys.argv[3]) if len(sys.argv)>3 else 150
d=int(sys.argv[4]) if len(sys.argv)>4 else 250
n=int(sys.argv[5]) if len(sys.argv)>5 else 20
last=-10**9
for m in re.finditer(sys.argv[2],t,re.I):
    if m.start()<last+d: continue
    last=m.start(); print("  >>",t[max(0,m.start()-a):m.end()+d]); n-=1
    if n<=0: break
