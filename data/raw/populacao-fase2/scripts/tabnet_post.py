#!/usr/bin/env python3
"""POST ao TabNet (DATASUS). Uso: tabnet_post.py <def> <linha> <incrementos(,)> <ano_ini> <ano_fim> <destino> [prefixo_arquivo] 
Le o formulario ao vivo para listar Arquivos (anos) e SX (filtros) e envia 'todas as categorias'."""
import re, subprocess, sys, urllib.parse
deff, linha, incs, a0, a1, dest = sys.argv[1:7]
pref = sys.argv[7] if len(sys.argv) > 7 else None
base = "http://tabnet.datasus.gov.br"
page = subprocess.run(["curl","-sL","-m","90","-A","Mozilla/5.0",f"{base}/cgi/deftohtm.exe?{deff}"],capture_output=True).stdout.decode("latin-1")
arqs = re.search(r'<SELECT NAME="Arquivos".*?</SELECT>', page, re.S|re.I).group(0)
files = re.findall(r'VALUE="([^"]+)"\s*(?:SELECTED)?\s*>\s*(\d{4})', arqs, re.I)
sel = [f for f,y in files if a0 <= int(y) <= a1] if False else [f for f,y in files if int(a0) <= int(y) <= int(a1)]
print("arquivos:", sel, file=sys.stderr)
items = [("Linha", linha), ("Coluna", "--Não-Ativa--")]
for i in incs.split(","): items.append(("Incremento", i))
for f in sel: items.append(("Arquivos", f))
for m in re.finditer(r'<SELECT[^>]*NAME="(S[^"]+)"', page, re.I):
    items.append((m.group(1), "TODAS_AS_CATEGORIAS__"))
items += [("formato","table"),("mostre","Mostra")]
body = "&".join(urllib.parse.quote(k, encoding="latin-1")+"="+urllib.parse.quote(v, encoding="latin-1") for k,v in items)
open(dest+".post-body.txt","w").write(urllib.parse.unquote(body, encoding="latin-1").replace("&","\n&"))
r = subprocess.run(["curl","-sL","-m","300","-A","Mozilla/5.0","-o",dest,"-w","%{http_code}","--data-binary",body,f"{base}/cgi/tabcgi.exe?{deff}"],capture_output=True)
print(r.stdout.decode(), file=sys.stderr)
