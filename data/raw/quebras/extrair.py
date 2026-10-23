# Extrai texto dos PDFs/HTML/xlsx citados em quebras.csv para quebras/derivado/ (derivados, recriaveis: pdftotext + html->texto).
# Rode: python3 -I extrair.py   (usa o binario pdftotext; nao usa rede)
import html
import json
import pathlib
import re
import subprocess
import zipfile

H = pathlib.Path(__file__).resolve().parent
D = H.parent
OUT = H / "derivado"
OUT.mkdir(exist_ok=True)

PDFS = {
    "ibge-liv1259": H / "bruto/ibge-liv1259.pdf",
    "ibge-pme-2002-mar": H / "bruto/ibge-pme-2002-mar.pdf",
    "ibge-pme-2002-nov": H / "bruto/ibge-pme-2002-nov.pdf",
    "ibge-liv101823": H / "bruto/ibge-liv101823.pdf",
    "ibge-liv101866": H / "bruto/ibge-liv101866.pdf",
    "ibge-liv101874": H / "bruto/ibge-liv101874.pdf",
    "ibge-liv101960": H / "bruto/ibge-liv101960.pdf",
    "ibge-sis2012-notas-tecnicas": H / "bruto/ibge-sis2012-notas-tecnicas.pdf",
    "ibge-liv102111": H / "bruto/ibge-liv102111.pdf",
    "ibge-liv101597": H / "bruto/ibge-liv101597.pdf",
    "bcb-ee070": H / "bruto/bcb-ee070-impacto-cesta-ipca.pdf",
    "bcb-ri201912": H / "bruto/bcb-ri-201912-box-ponderacao-ipca.pdf",
    "ibge-scn2010-nota17": H / "bruto/ibge-scn2010-nota17-retropolacao.pdf",
    "ibge-snipc-nt-2005-02": H / "bruto/ibge-snipc-nota-tecnica-2005-02.pdf",
    "puc-rio-revisao-pib": H / "bruto/puc-rio-revisao-pib-2007.pdf",
    "ipea-bmt23": H / "bruto/ipea-bmt23-mudancas.pdf",
    "reddy-minoiu-0509005": H / "bruto/ravallion-0509005.pdf",
    "ibge-liv98593": D / "social/bruto/ibge_liv98593.pdf",
    "bcb-nt48": D / "monetario/referencias/bcb-NT48-Dstat-Dimob-nov2018.pdf",
    "bcb-nm-2001": D / "monetario/referencias/bcb-NM-MeiosPagAmpl-reformulacao-2001.pdf",
    "bcb-nt03-2001": D / "monetario/referencias/bcb-NT03-2001-reformulacao-meios-pagamento.pdf",
    "bcb-museu-padroes": D / "monetario/referencias/bcb-museu-sintese-padroes-monetarios.pdf",
}
for nome, arq in PDFS.items():
    for modo, suf in (("-layout", ".txt"), ("-raw", ".raw.txt")):
        r = subprocess.run(["pdftotext", modo, str(arq), "-"], capture_output=True)
        (OUT / (nome + suf)).write_bytes(r.stdout)


def html_texto(arq):
    t = pathlib.Path(arq).read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"(?s)<(script|style).*?</\1>", "", t)
    t = re.sub(r"<[^>]+>", "\n", t)
    return re.sub(r"\n\s*\n+", "\n", html.unescape(t))


for nome, arq in {"wb-blog-updating-ipl-2017-ppps": H / "bruto/wb-blog-updating-ipl-2017-ppps.html",
                  "wb-blog-new-lines-2021-prices": H / "bruto/wb-blog-new-lines-2021-prices.html"}.items():
    (OUT / (nome + ".txt")).write_text(html_texto(arq), encoding="utf-8")

# xlsx: textos compartilhados (notas de rodape das tabelas do SIS 2025)
for nome, arq in {"sis2025-t2-17": D / "social/bruto/xlsx2025/Tabela 2.17 (PobrCarac_BR).xlsx",
                  "sis2025-t2-13": D / "social/bruto/xlsx2025/Tabela 2.13 (Indice_Gini_Geo).xlsx"}.items():
    z = zipfile.ZipFile(arq)
    ss = z.read("xl/sharedStrings.xml").decode("utf-8")
    (OUT / (nome + ".txt")).write_text("\n".join(html.unescape(s) for s in re.findall(r"<t[^>]*>(.*?)</t>", ss, re.S)), encoding="utf-8")

# metadados WDI
(OUT / "wdi-meta.txt").write_text(json.dumps(json.load(open(H / "bruto/wdi-meta-SP.DYN.LE00.IN.json")), ensure_ascii=False)
                                  + "\n" + json.dumps(json.load(open(H / "bruto/wdi-meta-SI.POV.GINI.json")), ensure_ascii=False), encoding="utf-8")
print("ok", len(list(OUT.glob("*"))), "arquivos")
