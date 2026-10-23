"""Acquisition chain: append, tamper detection, and the empty-string genesis."""

import hashlib

from govfc.chain import VAZIO, registrar_local, verificar


def test_genesis_is_sha256_of_empty_string():
    assert VAZIO == hashlib.sha256(b"").hexdigest()


def test_chain_links_and_detects_tampering(tmp_path):
    for nome in ("a.json", "b.json"):
        (tmp_path / nome).write_text(nome)
        registrar_local(tmp_path, tmp_path / nome)
    assert verificar(tmp_path) == 0
    linhas = (tmp_path / "manifest.jsonl").read_bytes().splitlines(keepends=True)
    assert b'"prev_hash":"' + hashlib.sha256(linhas[0]).hexdigest().encode() in linhas[1]
    (tmp_path / "a.json").write_text("tampered")
    assert verificar(tmp_path) == 1


def test_editing_an_old_line_breaks_the_next_link(tmp_path):
    for nome in ("a.json", "b.json"):
        (tmp_path / nome).write_text(nome)
        registrar_local(tmp_path, tmp_path / nome)
    man = tmp_path / "manifest.jsonl"
    man.write_bytes(man.read_bytes().replace(b"metadata reconstruida", b"metadata alterada", 1))
    assert verificar(tmp_path) == 1


def test_hash_only_files_are_tolerated_but_present_files_must_match(tmp_path):
    for nome in ("a.json", "b.json"):
        (tmp_path / nome).write_text(nome)
        registrar_local(tmp_path, tmp_path / nome)
    (tmp_path / "a.json").unlink()
    assert verificar(tmp_path) == 1  # strict: a missing file is an error
    assert verificar(tmp_path, permitir_ausentes=True) == 0
    (tmp_path / "b.json").write_text("tampered")
    assert verificar(tmp_path, permitir_ausentes=True) == 1


def test_redownload_under_the_same_path_keeps_history_and_checks_only_the_last_line(tmp_path):
    (tmp_path / "a.json").write_text("truncated")
    registrar_local(tmp_path, tmp_path / "a.json")
    (tmp_path / "a.json").write_text("complete")  # same path, new bytes, new line
    registrar_local(tmp_path, tmp_path / "a.json")
    assert verificar(tmp_path) == 0
    (tmp_path / "a.json").write_text("tampered")
    assert verificar(tmp_path) == 1


def test_command_line_verify_and_allow_missing(tmp_path):
    from govfc.chain import main

    (tmp_path / "a.json").write_text("x")
    registrar_local(tmp_path, tmp_path / "a.json")
    assert main(["verify", str(tmp_path)]) == 0
    (tmp_path / "a.json").unlink()
    assert main(["verify", str(tmp_path)]) == 1
    assert main(["verify", str(tmp_path), "--allow-missing"]) == 0
