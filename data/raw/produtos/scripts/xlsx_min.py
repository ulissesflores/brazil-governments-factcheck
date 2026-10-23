"""Leitor minimo de .xlsx (zipfile + xml); sem pandas. Devolve {aba: {(linha, coluna): valor}}."""
import re
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def col_idx(ref):
    letras = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for c in letras:
        n = n * 26 + ord(c) - 64
    return n


def ler(path):
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    alvo = {r.get("Id"): r.get("Target") for r in rels}
    abas = {}
    for s in wb.find("m:sheets", NS):
        rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        t = alvo[rid].lstrip("/")
        t = t if t.startswith("xl/") else "xl/" + t
        cel = {}
        for c in ET.fromstring(z.read(t)).iter("{%s}c" % NS["m"]):
            ref, tp = c.get("r"), c.get("t")
            v = c.find("m:v", NS)
            if tp == "inlineStr":
                val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
            elif v is None:
                continue
            elif tp == "s":
                val = ss[int(v.text)]
            elif tp in ("str", "e", "b"):
                val = v.text
            else:
                val = float(v.text)
            cel[(int(re.search(r"\d+", ref).group(0)), col_idx(ref))] = val
        abas[s.get("name")] = cel
    return abas
