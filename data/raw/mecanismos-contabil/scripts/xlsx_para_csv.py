"""Converte cada aba de um .xlsx em CSV (so stdlib). Uso: python3 -I xlsx_para_csv.py <xlsx> <pasta_saida>
Le o bruto; sem rede. Valores = como gravados na celula (numeros cheios, datas como serial Excel)."""
import csv, re, sys, zipfile
import xml.etree.ElementTree as ET
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
def col(ref):
    s = re.match(r"[A-Z]+", ref).group(0); n = 0
    for ch in s: n = n * 26 + ord(ch) - 64
    return n - 1
def main(xlsx, saida):
    import pathlib
    out = pathlib.Path(saida); out.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(xlsx)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    for i, sh in enumerate(wb.find("m:sheets", NS)):
        nome = sh.get("name"); alvo = rels[sh.get("{%s}id" % NS["r"])]
        alvo = alvo.lstrip("/"); alvo = alvo if alvo.startswith("xl/") else "xl/" + alvo
        rows = []
        for ev, el in ET.iterparse(z.open(alvo)):
            if el.tag.endswith("}row"):
                r = {}
                for c in el.findall("m:c", NS):
                    v = c.find("m:v", NS); t = c.get("t")
                    if t == "inlineStr":
                        val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                    elif v is None: continue
                    elif t == "s": val = ss[int(v.text)]
                    else: val = v.text
                    r[col(c.get("r"))] = val
                rows.append(r); el.clear()
        w = max((max(r) for r in rows if r), default=-1) + 1
        fn = out / (f"{i:02d}-" + re.sub(r"[^A-Za-z0-9]+", "_", nome) + ".csv")
        with open(fn, "w", newline="", encoding="utf8") as f:
            cw = csv.writer(f)
            for r in rows: cw.writerow([r.get(j, "") for j in range(w)])
        print(fn.name, len(rows), "x", w)
main(sys.argv[1], sys.argv[2])
