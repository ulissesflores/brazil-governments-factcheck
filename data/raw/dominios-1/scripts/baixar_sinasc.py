#!/usr/bin/env python3
"""POST ao TabNet/DATASUS (SINASC): nascidos vivos por residencia da mae, por ano x consultas de pre-natal, Brasil.
Uso: python3 -I baixar_sinasc.py <destino.csv>   (depois: manifest_tool.py add-local ... --url ... --nota ...)"""
import sys, urllib.parse, urllib.request
arqs = [f"nvuf{y % 100:02d}.dbf" for y in range(1994, 2026)]
pairs = [("Linha", "Ano_do_nascimento"), ("Coluna", "Consult_pré-natal"), ("Incremento", "Nascim_p/resid.mãe")] \
    + [("Arquivos", a) for a in arqs] \
    + [("pesqmes1", ""), ("SRegião", "TODAS_AS_CATEGORIAS__"), ("SUnidade_da_Federação", "TODAS_AS_CATEGORIAS__"),
       ("formato", "prn"), ("mostre", "Mostra")]
body = urllib.parse.urlencode(pairs, encoding="latin-1").encode()
req = urllib.request.Request("http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinasc/cnv/nvuf.def", data=body,
    headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"})
open(sys.argv[1], "wb").write(urllib.request.urlopen(req, timeout=180).read())
