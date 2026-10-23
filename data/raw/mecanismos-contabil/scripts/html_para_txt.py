"""HTML -> texto simples (stdlib). Uso: python3 -I html_para_txt.py <entrada.html> <saida.txt>. Sem rede."""
import html, re, sys
b = open(sys.argv[1], "rb").read()
try: t = b.decode("utf8")
except UnicodeDecodeError: t = b.decode("cp1252", errors="replace")
t = re.sub(r"(?s)<(script|style|noscript).*?</\1>", "", t)
t = re.sub(r"(?i)</(p|div|li|h\d|tr|br)>|<br\s*/?>", "\n", t)
t = html.unescape(re.sub(r"<[^>]+>", " ", t))
t = re.sub(r"[ \t]+", " ", t); t = re.sub(r"\n\s*\n+", "\n", t)
open(sys.argv[2], "w", encoding="utf8").write(t)
