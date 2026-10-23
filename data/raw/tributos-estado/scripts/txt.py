# converte HTML do Planalto em texto limpo (decodifica utf-8/cp1252). So le bruto.
import html
import re
import sys


def ler(caminho):
    b = open(caminho, "rb").read()
    try:
        t = b.decode("utf-8")
    except UnicodeDecodeError:
        t = b.decode("cp1252", errors="replace")
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", t)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>|</li>|</h\d>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t).replace("\xa0", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t


if __name__ == "__main__":
    print(ler(sys.argv[1]))
