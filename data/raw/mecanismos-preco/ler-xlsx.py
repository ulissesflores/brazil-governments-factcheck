#!/usr/bin/env python3
"""Leitor minimo de .xlsx (stdlib): imprime ou filtra linhas de uma planilha. Uso: python3 -I ler-xlsx.py ARQ [ABA_IDX] [REGEX]"""
import sys, zipfile, re, xml.etree.ElementTree as ET
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

def abrir(arq):
    z = zipfile.ZipFile(arq)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    nomes = [s.get("name") for s in wb.find("m:sheets", NS)]
    return z, ss, nomes

def linhas(z, ss, idx):
    raiz = ET.fromstring(z.read(f"xl/worksheets/sheet{idx}.xml"))
    for row in raiz.iter("{%s}row" % NS["m"]):
        cel = {}
        for c in row.findall("m:c", NS):
            ref = re.match(r"[A-Z]+", c.get("r")).group()
            v = c.find("m:v", NS)
            if v is None:
                t = c.find("m:is", NS)
                val = "".join(x.text or "" for x in t.iter("{%s}t" % NS["m"])) if t is not None else ""
            else:
                val = ss[int(v.text)] if c.get("t") == "s" else v.text
            cel[ref] = val
        yield int(row.get("r")), cel

if __name__ == "__main__":
    z, ss, nomes = abrir(sys.argv[1])
    if len(sys.argv) < 3:
        for i, n in enumerate(nomes, 1): print(i, n)
        sys.exit()
    rx = re.compile(sys.argv[3], re.I) if len(sys.argv) > 3 else None
    for r, c in linhas(z, ss, int(sys.argv[2])):
        txt = " | ".join(f"{k}={v}" for k, v in c.items() if v != "")
        if txt and (rx is None or rx.search(txt)): print(r, txt[:400])
