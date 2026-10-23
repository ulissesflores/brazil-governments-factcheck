"""Extrai blocos de tabela de precos (faixa etaria x colunas) do texto pdftotext -layout das tabelas Amil.
Uso: python3 -I blocos_amil.py <arquivo.txt>   -> imprime blocos (indice, cabecalho bruto, linhas)."""
import re, sys, json
FAIXAS = ["0 a 18","19 a 23","24 a 28","29 a 33","34 a 38","39 a 43","44 a 48","49 a 53","54 a 58","59+"]
ROW = re.compile(r"^\s*(?:(\d{1,2})\s*(?:a|-)\s*(\d{2})|>\s*=\s*(59))\s+((?:\d+(?:\.\d{3})*,\d{2}\s*)+)\s*$")
def num(s): return float(s.replace(".","").replace(",","."))
def blocos(path):
    out=[]; cab=[]; atual=[]
    for ln in open(path,encoding="utf8",errors="replace"):
        ln=ln.rstrip("\n")
        m=ROW.match(ln)
        if m:
            if m.group(3): faixa="59+"
            else:
                a,b=int(m.group(1)),int(m.group(2)); faixa=f"{a} a {b}"
            vals=[num(x) for x in re.findall(r"\d+(?:\.\d{3})*,\d{2}",m.group(4))]
            atual.append((faixa,vals))
            if faixa=="59+":
                out.append({"cabecalho":" | ".join(re.sub(r"\s+"," ",c).strip() for c in cab if c.strip())[-600:],"linhas":atual}); cab=[]; atual=[]
        else:
            if atual: # linha de texto no meio de um bloco (ex.: rodape intercalado): ignora
                continue
            cab.append(ln)
    return out
if __name__=="__main__":
    for i,b in enumerate(blocos(sys.argv[1])):
        print(i, len(b["linhas"]), "ncols", {len(v) for _,v in b["linhas"]}, "|", b["cabecalho"][-330:])
