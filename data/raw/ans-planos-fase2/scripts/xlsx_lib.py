import zipfile, re
def ler_xlsx(path):
    """Devolve {aba: [[valores por coluna]]} lendo so o XML (sem dependencia)."""
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        ss = [re.sub(r"<[^>]+>","",s) for s in re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode(), flags=re.S)]
    wb = z.read("xl/workbook.xml").decode()
    nomes = re.findall(r'<sheet [^>]*name="([^"]*)"[^>]*r:id="([^"]*)"', wb)
    rels = dict(re.findall(r'<Relationship [^>]*Id="([^"]*)"[^>]*Target="([^"]*)"', z.read("xl/_rels/workbook.xml.rels").decode()))
    rels.update({k: v for v, k in re.findall(r'<Relationship [^>]*Target="([^"]*)"[^>]*Id="([^"]*)"', z.read("xl/_rels/workbook.xml.rels").decode())})
    out = {}
    for nome, rid in nomes:
        alvo = rels[rid].lstrip("/"); alvo = alvo if alvo.startswith("xl/") else "xl/" + alvo
        sh = z.read(alvo).decode(); linhas = []
        for row in re.findall(r"<row [^>]*>(.*?)</row>", sh, flags=re.S):
            d = {}
            for attrs, inner in re.findall(r"<c ([^>]*?)(?:/>|>(.*?)</c>)", row, flags=re.S):
                m = re.search(r"<v>([^<]*)</v>", inner or "")
                if not m:
                    m2 = re.search(r"<t[^>]*>([^<]*)</t>", inner or "")
                    if not m2: continue
                    v = m2.group(1)
                else:
                    v = m.group(1)
                    if 't="s"' in attrs: v = ss[int(v)]
                col = re.search(r'r="([A-Z]+)\d+"', attrs).group(1); d[col] = v
            linhas.append(d)
        out[nome] = linhas
    return out
