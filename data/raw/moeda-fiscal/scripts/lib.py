"""Utilitarios comuns (stdlib). Le so bruto/derivado em disco; sem rede."""
import csv, json
from pathlib import Path
PASTA = Path(__file__).resolve().parent.parent
DADOS = PASTA.parent
COLS = ["indicador", "fonte", "definicao_linha", "ano", "mes_ou_trimestre", "valor", "unidade", "nota", "vintage"]


def manifest():
    """arquivo -> (timestamp_utc, sha256, url) da cadeia desta pasta (ultima linha por arquivo)."""
    m = {}
    f = PASTA / "manifest.jsonl"
    if f.exists():
        for l in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(l)
            m[r["arquivo"]] = (r["timestamp_utc"], r["sha256"], r["url"])
    return m


def vintage(arq, pasta_manifest=None):
    """Texto de vintage: arquivo, data de aquisicao e 12 primeiros hex do sha256 (da cadeia da propria pasta)."""
    m = manifest()
    if arq in m:
        ts, sh, _ = m[arq]
        return f"{arq} adquirido {ts} sha256 {sh[:12]}"
    return f"{arq} (fora da cadeia desta pasta)"


def ckan(cod):
    """Metadados CKAN do codigo SGS: dict com title, unidade_medida, inicio_periodo, periodicidade, notes."""
    d = json.loads((PASTA / f"bruto/bcb/ckan_{cod}.json").read_text(encoding="utf-8"))
    for r in d["result"]["results"]:
        if str(r.get("codigo_sgs")) == str(cod):
            return r
    return None


def sgs(arq):
    """Le JSON do SGS -> lista de (dd, mm, aaaa, valor float|None)."""
    out = []
    for r in json.loads((PASTA / arq).read_text(encoding="utf-8")):
        dd, mm, aa = r["data"].split("/")
        v = r["valor"]
        out.append((int(dd), int(mm), int(aa), float(v) if v not in ("", None) else None))
    return out


def ipea(arq):
    """Le JSON do Ipeadata -> lista de (aaaa, mm, dd, valor|None)."""
    out = []
    for r in json.loads((PASTA / arq).read_text(encoding="utf-8"))["value"]:
        d = r["VALDATA"][:10]
        a, m, dd = d.split("-")
        out.append((int(a), int(m), int(dd), r["VALVALOR"]))
    return out


def escrever(nome, linhas, sub="series"):
    """Grava series/<nome>.csv no formato longo; linhas = lista de dicts."""
    p = PASTA / sub / f"{nome}.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        for l in linhas:
            w.writerow({c: l.get(c, "") for c in COLS})
    return p


def fmt(v):
    """Numero sem arredondar a fonte; derivados com 12 algarismos significativos."""
    return "" if v is None else repr(float(f"{v:.12g}"))


def html_texto(arq):
    """HTML (bruto/...) -> texto simples (stdlib), a mesma regra de mecanismos-contabil/scripts/html_para_txt.py."""
    import html, re
    b = (PASTA / arq).read_bytes()
    try:
        t = b.decode("utf8")
    except UnicodeDecodeError:
        t = b.decode("cp1252", errors="replace")
    t = re.sub(r"(?s)<(script|style|noscript).*?</\1>", "", t)
    t = re.sub(r"(?i)</(p|div|li|h\d|tr|br)>|<br\s*/?>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"[ \t\xa0]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t)
