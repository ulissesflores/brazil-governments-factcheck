"""Documentation in five languages: same tokens, same code, same numbers, rendered from results."""

import importlib.util
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "code"))
spec = importlib.util.spec_from_file_location("make_docs", RAIZ / "scripts" / "make_docs.py")
make_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(make_docs)

LINGUAS = ["pt-BR", "es", "it", "he"]
MODELOS = ["README.md.tmpl", "METHODOLOGY.md.tmpl"]
TOKEN = re.compile(r"\{\{(\w+)\}\}")
BLOCO = re.compile(r"```[a-z]*\n(.*?)```", re.S)
NUM = re.compile(r"\d+(?:[.,]\d+)?")


def ler(lang, nome):
    return (RAIZ / "docs-src" / lang / nome).read_text(encoding="utf-8")


def numeros(texto):
    sem_codigo = BLOCO.sub("", texto)
    sem_url = re.sub(r"https?://\S+|\(\S+\.(?:svg|md)\)", "", sem_codigo)
    return sorted(n.replace(",", ".") for n in NUM.findall(sem_url))


@pytest.mark.parametrize("nome", MODELOS)
def test_english_template_exists_and_every_token_is_known(nome):
    mapa = make_docs.tokens("en")
    assert set(TOKEN.findall(ler("en", nome))) <= set(mapa)


@pytest.mark.parametrize("lang", LINGUAS)
@pytest.mark.parametrize("nome", MODELOS)
def test_translation_keeps_tokens_code_blocks_and_numbers(lang, nome):
    en, tr = ler("en", nome), ler(lang, nome)
    assert sorted(TOKEN.findall(tr)) == sorted(TOKEN.findall(en)), "tokens differ"
    assert BLOCO.findall(tr) == BLOCO.findall(en), "code blocks differ"
    assert numeros(tr) == numeros(en), "numbers differ"


@pytest.mark.parametrize("lang", ["en", *LINGUAS])
def test_rendered_files_match_the_templates(lang):
    mapa = make_docs.tokens(lang)
    for nome, destino in make_docs.DESTINO.items():
        esperado = make_docs.renderizar(ler(lang, nome), mapa)
        assert (RAIZ / destino(lang)).read_text(encoding="utf-8") == esperado


@pytest.mark.parametrize("lang", LINGUAS)
def test_every_readme_keeps_the_callouts_and_the_language_bar(lang):
    tr, en = ler(lang, "README.md.tmpl"), ler("en", "README.md.tmpl")
    assert tr.count("> [!IMPORTANT]") == en.count("> [!IMPORTANT]") == 1
    assert tr.count("> [!NOTE]") == en.count("> [!NOTE]") == 1
    for alvo in ("README.md", "README.pt-BR.md", "README.es.md", "README.it.md", "README.he.md"):
        assert f"({alvo})" in tr
