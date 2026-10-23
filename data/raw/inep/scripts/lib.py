"""Funcoes comuns: conversao xls/xlsx -> csv (soffice), leitura de zip, numeros do INEP.

Roda com `python3 -I`; so stdlib; so le `bruto/`; nunca usa rede.
"""
import csv
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRUTO = os.path.join(RAIZ, "bruto")
FILTRO = "csv:Text - txt - csv (StarCalc):44,34,76,1,,0,false,true,false,false,false,-1"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def conferir_cadeia():
    """Confere sha256 de cada arquivo do manifest e o encadeamento prev_hash. Devolve (n, cabeca)."""
    man = os.path.join(RAIZ, "manifest.jsonl")
    linhas = open(man, "rb").read().splitlines(keepends=True)
    prev = hashlib.sha256(b"").hexdigest()
    for i, raw in enumerate(linhas, 1):
        d = json.loads(raw)
        assert d["seq"] == i, ("seq", i)
        assert d["prev_hash"] == prev, ("cadeia quebrada na linha", i)
        arq = os.path.join(RAIZ, d["arquivo"])
        assert sha256(arq) == d["sha256"], ("sha256 diferente", d["arquivo"])
        prev = hashlib.sha256(raw).hexdigest()
    return len(linhas), prev


def extrair_zip(zip_path, destino, so=r"\.xlsx?$"):
    """Extrai com nomes sanitizados (o INEP usa cp437/cp1252 nos nomes). Devolve lista de caminhos."""
    os.makedirs(destino, exist_ok=True)
    saida = []
    with zipfile.ZipFile(zip_path) as z:
        for i in z.infolist():
            if i.is_dir() or "~$" in i.filename or i.filename.endswith("Thumbs.db"):
                continue
            if so and not re.search(so, i.filename, re.I):
                continue
            nome = os.path.basename(i.filename)
            try:
                nome = nome.encode("cp437").decode("cp1252")
            except Exception:
                pass
            nome = re.sub(r"[^A-Za-z0-9_.-]+", "_", nome)
            p = os.path.join(destino, nome)
            with open(p, "wb") as f:
                f.write(z.read(i))
            saida.append(p)
    return saida


def converter(xls, outdir):
    """soffice headless -> um csv por aba em outdir. Devolve lista de csv."""
    os.makedirs(outdir, exist_ok=True)
    subprocess.run(
        ["soffice", "--headless", "--convert-to", FILTRO, "--outdir", outdir, xls],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=900,
    )
    return sorted(glob.glob(os.path.join(outdir, "*.csv")))


def ler_csv(p):
    with open(p, encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.reader(f))


def num(s):
    """Numero do INEP: '12,5' ou '12.5' ou '1.234.567'; '-', '--', '...' -> None."""
    if s is None:
        return None
    s = str(s).strip().replace("\xa0", "")
    if s in ("", "-", "--", "...", "*", "x", "X"):
        return None
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+", s):  # milhar com ponto
        return float(s.replace(".", ""))
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None
