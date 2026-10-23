# leitor minimo de xlsx por zipfile+xml (sem pandas/openpyxl). Importado por outros scripts: so le bruto.
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def _col(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def abrir(caminho):
    """Devolve {nome_da_aba: [[celulas...], ...]} (valores como str; numeros crus)."""
    z = zipfile.ZipFile(caminho)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    alvo = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for s in wb.find("m:sheets", NS):
        rid = s.get("{%s}id" % NS["r"])
        t = alvo[rid].lstrip("/")
        t = t if t.startswith("xl/") else "xl/" + t
        rows = []
        for row in ET.fromstring(z.read(t)).iter("{%s}row" % NS["m"]):
            r = {}
            for c in row.findall("m:c", NS):
                v = c.find("m:v", NS)
                if c.get("t") == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                elif v is None:
                    continue
                elif c.get("t") == "s":
                    val = ss[int(v.text)]
                else:
                    val = v.text
                r[_col(c.get("r"))] = val
            if r:
                rows.append([r.get(i, "") for i in range(max(r) + 1)])
        out[s.get("name")] = rows
    return out


if __name__ == "__main__":
    d = abrir(sys.argv[1])
    for k, rows in d.items():
        print("##", k, len(rows))
        for r in rows[: int(sys.argv[2]) if len(sys.argv) > 2 else 6]:
            print("   ", r[:12])
