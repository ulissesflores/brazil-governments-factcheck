import json, subprocess, sys, urllib.parse, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cands import C, C2, D

PASTA = Path("/Users/ulissesflores/Developer/redacao/dossies/governos-do-brasil-economia/fontes/dados/referencias-q1")
CHAIN = "/Users/ulissesflores/Developer/brazil-governments-factcheck/code/govfc/chain.py"
SEL = "DOI,title,author,issued,container-title,type,ISSN"

def add(url, dest, nota):
    if (PASTA / dest).exists():
        return True
    r = subprocess.run(["python3", "-I", CHAIN, "add", str(PASTA), url, dest, "--nota", nota],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FALHA", dest, r.stderr.strip()[-200:]); return False
    return True

def doi_dest(doi):
    return "crossref/crossref-doi-" + re.sub(r"[^A-Za-z0-9.\-]", "_", doi) + ".json"

def fetch_doi(doi, nota):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
    return add(url, doi_dest(doi), nota)

def search(key, q, jart=False):
    url = "https://api.crossref.org/works?query.bibliographic=" + urllib.parse.quote(q) + ("&filter=type:journal-article" if jart else "") + "&rows=5&select=" + SEL
    return add(url, f"crossref/busca-{key}.json", "busca bibliografica Crossref: " + q)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "init":
        for tema, key, doi, q, sn, yr in C:
            if doi:
                fetch_doi(doi, f"tema {tema} {key}: registro do DOI")
            else:
                search(key, q)
        print("ok")
    elif mode == "r2":
        for tema, key, doi, q, sn, yr in C2:
            search(key+"-r2", q, jart=True)
        for tema, key, doi in D:
            fetch_doi(doi, f"tema {tema} {key}: registro do DOI")
        print("ok")
    elif mode == "doi":   # fetch additional dois: key doi
        fetch_doi(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "registro do DOI")
