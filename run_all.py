#!/usr/bin/env python3
"""Single entry point: results, tests, provenance (Track 1); restore and derive first (--full).

Track 1 (default, no network): rebuild ``output/results.json`` from the sealed derived series,
run the tests, verify the SHA-256 seal and every acquisition chain.
Track 2 (``--full``): first re-download the evidence that is hashed but not redistributed
(``govfc.chain restore``), then re-run the derivation scripts that turn raw files into the
sealed series; any difference then fails the seal check. See ``REPRODUCIBILITY.md``.
"""

import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
#: Derivation scripts, run in place with ``python3 -I`` (they read only the files next to them).
DERIVACAO = ["data/raw/economia-real/recalcula.py", "data/raw/social/recalcula.py"]


def rodar(titulo, cmd, cwd=RAIZ):
    """Run one step and return its exit code.

    Parameters
    ----------
    titulo : str
        Label printed before the step.
    cmd : list of str
        Command to execute.
    cwd : pathlib.Path
        Working directory of the step.

    Returns
    -------
    int
        Exit code of the command.
    """
    print(f"\n=== {titulo} ===", flush=True)
    env = {**os.environ, "PYTHONPATH": str(RAIZ / "code")}
    return subprocess.run(cmd, cwd=cwd, env=env).returncode


def main(argv):
    """Run every step; all steps run even if an earlier one fails.

    Parameters
    ----------
    argv : list of str
        Command-line arguments; ``--full`` selects Track 2.

    Returns
    -------
    int
        ``0`` if all steps exit with zero, ``1`` otherwise.
    """
    cheio = "--full" in argv
    codigos = []
    if cheio:
        for man in sorted((RAIZ / "data" / "raw").glob("*/manifest.jsonl")):
            codigos.append(
                rodar(
                    f"restore {man.parent.name}",
                    [sys.executable, "-m", "govfc.chain", "restore", str(man.parent)],
                )
            )
        for script in DERIVACAO:
            codigos.append(
                rodar(
                    f"derive {script}",
                    [sys.executable, "-I", Path(script).name],
                    cwd=RAIZ / Path(script).parent,
                )
            )
    modo = "Track 2 (full)" if cheio else "Track 1 (sealed series, no network)"
    codigos += [
        rodar(f"1/10 curated layer [{modo}]", [sys.executable, "-m", "govfc.curate"]),
        rodar("2/10 results", [sys.executable, "-m", "govfc.build_results"]),
        rodar("3/10 dynamics", [sys.executable, "-m", "govfc.dinamica"]),
        rodar("4/10 world", [sys.executable, "-m", "govfc.mundo"]),
        rodar("5/10 terminal", [sys.executable, "-m", "govfc.terminal"]),
        rodar("6/10 indice", [sys.executable, "-m", "govfc.indice"]),
        rodar("7/10 auditoria", [sys.executable, "-m", "govfc.auditoria"]),
        rodar("8/10 literatura", [sys.executable, "-m", "govfc.literatura"]),
        rodar("9/10 pytest", [sys.executable, "-m", "pytest"]),
        rodar("10/10 provenance", [sys.executable, "make_provenance.py", "--verify"]),
    ]
    ok = not any(codigos)
    print("\nrun_all: " + ("OK" if ok else f"FAILED (codes {codigos})") + f" [{modo}]")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
