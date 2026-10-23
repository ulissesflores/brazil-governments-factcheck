"""Leitor minimo de .xlsx (zipfile + xml), sem dependencias. Devolve linhas como listas de str."""
import re, zipfile
import xml.etree.ElementTree as ET
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

def col_idx(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1

def ler(caminho, folha=None):
    z = zipfile.ZipFile(caminho)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    nomes = [s.get("name") for s in wb.find("m:sheets", NS)]
    alvo = "xl/worksheets/sheet%d.xml" % ((nomes.index(folha) + 1) if folha else 1)
    for _, el in ET.iterparse(z.open(alvo)):
        if el.tag.endswith("}row"):
            linha = []
            for c in el.findall("m:c", NS):
                i = col_idx(c.get("r"))
                while len(linha) < i: linha.append("")
                v = c.find("m:v", NS)
                if c.get("t") == "s" and v is not None: val = ss[int(v.text)]
                elif c.get("t") == "inlineStr": val = "".join(t.text or "" for t in c.iter("{%s}t" % NS["m"]))
                else: val = v.text if v is not None else ""
                linha.append(val)
            yield linha
            el.clear()
