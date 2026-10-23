#!/usr/bin/env python3
"""Acquisition hash chain: append-only ``manifest.jsonl`` (``add``, ``add-local``, ``verify``).

Each line is one compact JSON object (sorted keys, UTF-8, LF-terminated). ``prev_hash`` of
line i is the sha256 of the exact BYTES of line i-1 (LF included); for line 1 it is
sha256(b""). Changing any byte of any old line breaks every line after it.

Usage (from the repository root, with ``PYTHONPATH=code``)::

    python3 -m govfc.chain add <folder> <url> <destination-file> [--nota "..."]
    python3 -m govfc.chain add-local <folder> <existing-file> [--url URL] [--nota "..."]
    python3 -m govfc.chain verify <folder> [--allow-missing]
    python3 -m govfc.chain restore <folder>
"""

import argparse
import datetime
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

#: ``prev_hash`` of the first line: sha256 of the empty string.
VAZIO = hashlib.sha256(b"").hexdigest()
UA = "Mozilla/5.0 (compatible; brazil-governments-factcheck/0.1)"


def _linhas(man):
    """Return the raw lines (bytes, LF kept) of a manifest, or ``[]`` if it does not exist."""
    return man.read_bytes().splitlines(keepends=True) if man.exists() else []


def _anexar(pasta, reg):
    """Append ``reg`` to the folder manifest, filling ``seq`` and ``prev_hash``."""
    man = pasta / "manifest.jsonl"
    linhas = _linhas(man)
    reg["seq"] = len(linhas) + 1
    reg["prev_hash"] = hashlib.sha256(linhas[-1]).hexdigest() if linhas else VAZIO
    linha = (
        json.dumps(reg, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    ).encode()
    with man.open("ab") as f:
        f.write(linha)
    return reg


def _agora():
    """Return the current UTC time as ``YYYY-MM-DDTHH:MM:SSZ``."""
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def baixar(pasta, url, destino, nota=""):
    """Download ``url`` (up to 4 attempts), save it to ``pasta/destino``, log it in the manifest."""
    pasta = Path(pasta)
    ultimo = None
    for tentativa in range(1, 5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                corpo, status = r.read(), r.status
            if corpo.strip():
                break
            ultimo = "corpo vazio"
        except Exception as e:  # noqa: BLE001 - registramos o motivo e tentamos de novo
            ultimo = repr(e)
        time.sleep(2 * tentativa)
    else:
        sys.exit(f"falhou apos 4 tentativas: {url} ({ultimo})")
    alvo = pasta / destino
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_bytes(corpo)
    return _anexar(
        pasta,
        {
            "arquivo": destino,
            "bytes": len(corpo),
            "http_status": status,
            "nota": nota,
            "sha256": hashlib.sha256(corpo).hexdigest(),
            "timestamp_utc": _agora(),
            "url": url,
        },
    )


def registrar_local(pasta, arquivo, url="", nota=""):
    """Log an already-present file (reconstructed metadata: timestamp = mtime)."""
    pasta, arq = Path(pasta), Path(arquivo)
    corpo = arq.read_bytes()
    mt = datetime.datetime.fromtimestamp(arq.stat().st_mtime, datetime.UTC)
    return _anexar(
        pasta,
        {
            "arquivo": arq.resolve().relative_to(pasta.resolve()).as_posix(),
            "bytes": len(corpo),
            "http_status": None,
            "nota": ("metadata reconstruida (timestamp = mtime). " + nota).strip(),
            "sha256": hashlib.sha256(corpo).hexdigest(),
            "timestamp_utc": mt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "url": url,
        },
    )


def verificar(pasta, permitir_ausentes=False):
    """Recompute the chain and check every file on disk; return 0 if everything matches.

    Parameters
    ----------
    pasta : str or pathlib.Path
        Folder that holds ``manifest.jsonl``.
    permitir_ausentes : bool
        When true, a file that is not on disk (evidence that is hashed but not redistributed)
        is counted and reported but is not an error; any file that IS present must still match.
    """
    pasta = Path(pasta)
    linhas = _linhas(pasta / "manifest.jsonl")
    erros, prev, ausentes, antigas = [], VAZIO, 0, 0
    # a file re-downloaded under the same path: only its LAST line has to match the disk;
    # the earlier lines stay in the chain as history (the old bytes are gone, the record is not)
    ultima = {json.loads(b)["arquivo"]: i for i, b in enumerate(linhas, 1)}
    for i, bruta in enumerate(linhas, 1):
        reg = json.loads(bruta)
        if reg["seq"] != i:
            erros.append(f"seq {i}: valor {reg['seq']}")
        if reg["prev_hash"] != prev:
            erros.append(f"seq {i}: prev_hash quebrado")
        arq = pasta / reg["arquivo"]
        if ultima[reg["arquivo"]] != i:
            antigas += 1
        elif not arq.exists():
            ausentes += 1
            if not permitir_ausentes:
                erros.append(f"seq {i}: arquivo ausente {reg['arquivo']}")
        elif hashlib.sha256(arq.read_bytes()).hexdigest() != reg["sha256"]:
            erros.append(f"seq {i}: sha256 diverge {reg['arquivo']}")
        prev = hashlib.sha256(bruta).hexdigest()
    for e in erros:
        print("DIVERGE:", e)
    extra = f"; {ausentes} hash-only (not redistributed)" if ausentes else ""
    extra += f"; {antigas} superseded (same path re-downloaded)" if antigas else ""
    print(f"{len(linhas)} lines; head {prev}{extra}; {'OK' if not erros else 'FAILED'}")
    return 1 if erros else 0


def restaurar(pasta):
    """Re-download the files that are hashed but not redistributed and compare their sha256.

    A mismatch is reported, not hidden: a live URL may legitimately serve a newer version, so
    a mismatch means "the source changed or the copy was altered", never "proof of tampering".

    Parameters
    ----------
    pasta : str or pathlib.Path
        Folder that holds ``manifest.jsonl``.

    Returns
    -------
    int
        Number of files that could not be restored byte for byte.
    """
    pasta = Path(pasta)
    falhas = 0
    for bruta in _linhas(pasta / "manifest.jsonl"):
        reg = json.loads(bruta)
        alvo = pasta / reg["arquivo"]
        if alvo.exists() or not reg["url"]:
            continue
        try:
            req = urllib.request.Request(reg["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                corpo = r.read()
        except Exception as e:  # noqa: BLE001 - report and go on
            print(f"UNREACHABLE {reg['arquivo']}: {e!r}")
            falhas += 1
            continue
        if hashlib.sha256(corpo).hexdigest() != reg["sha256"]:
            print(f"CHANGED AT SOURCE {reg['arquivo']} (sha256 differs from the sealed one)")
            falhas += 1
            continue
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_bytes(corpo)
        print(f"restored {reg['arquivo']}")
    return falhas


def main(argv=None):
    """Command-line entry point (``add``, ``add-local``, ``verify``, ``restore``).

    Parameters
    ----------
    argv : list of str or None
        Arguments; ``None`` means ``sys.argv[1:]``.

    Returns
    -------
    int
        Process exit code.
    """
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("pasta")
    a.add_argument("url")
    a.add_argument("destino")
    a.add_argument("--nota", default="")
    b = sub.add_parser("add-local")
    b.add_argument("pasta")
    b.add_argument("arquivo")
    b.add_argument("--url", default="")
    b.add_argument("--nota", default="")
    c = sub.add_parser("verify")
    c.add_argument("pasta")
    c.add_argument("--allow-missing", action="store_true")
    d = sub.add_parser("restore")
    d.add_argument("pasta")
    x = ap.parse_args(argv)
    if x.cmd == "add":
        print(json.dumps(baixar(x.pasta, x.url, x.destino, x.nota), ensure_ascii=False))
        return 0
    if x.cmd == "add-local":
        print(json.dumps(registrar_local(x.pasta, x.arquivo, x.url, x.nota), ensure_ascii=False))
        return 0
    if x.cmd == "restore":
        return 1 if restaurar(x.pasta) else 0
    return verificar(x.pasta, x.allow_missing)


if __name__ == "__main__":
    sys.exit(main())
