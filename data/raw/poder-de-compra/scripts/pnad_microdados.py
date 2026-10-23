#!/usr/bin/env python3
"""Taxa de desocupacao (desemprego aberto) da PNAD anual a partir dos MICRODADOS de 1981, 1982, 1984, 1985, 1986 e 1988.

python3 -I pnad_microdados.py     (sem rede; le os zips em ../bruto/pnad-microdados e transmite o arquivo sem extrair)
Escreve ../series/pnad_1981_1990_microdados.csv

Metodo (igual para todos os anos; posicoes e codigos lidos nos dicionarios `Documentacao.zip` de cada ano, ver POS abaixo):
  registro de PESSOA = tipo de registro "3" (a "1" e de domicilio);
  V501 "que fez na semana de referencia?": 1 trabalhou, 2 tinha trabalho mas nao trabalhou, 3 procurou trabalho, 4-7 fora da forca de trabalho,
  em branco = menor de 10 anos, 9 = sem declaracao;
  PEA (forca de trabalho) = V501 em {1,2,3}; desocupada = V501 = 3; taxa = soma dos pesos (V9991 "peso da pessoa") dos desocupados / soma dos pesos da PEA.
1983, 1987, 1989 e 1990 NAO entram: so existem como Dados.zip de 29 MB (1983) ou .DAT de 79 a 103 MB (1987, 1989, 1990), acima do limite de 25 MB por arquivo.
"""
import csv
import io
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MD = RAIZ / "bruto/pnad-microdados"
# ano: (padrao do nome do arquivo no zip, posicao do tipo de registro, posicao do peso original da pessoa, posicao do peso alternativo (Censo 91) ou None, posicao de V501)
POS = {
    1981: (("PNAD81BR.TXT",), 25, 13, None, 48),
    1982: (("PNAD82BR.TXT",), 25, 13, None, 48),
    1984: (("PNAD84BR.DAT",), 25, 13, None, 48),
    1985: (("PNAD1985.DAT",), 26, 22, 14, 49),      # V9971 "PESO DA PESSOA" (22) e V9991 "PESO NOVO PESSOA CENSO" (14)
    1986: (("PNAD1986.DAT",), 30, 14, 22, 53),      # V9991 "PESO DA PESSOA" (14) e V9971 "PESO NOVO PESSOA CENSO 91" (22)
    1988: (tuple(f"PND88RM{i}.DAT" for i in range(1, 9)), 26, 14, None, 49),
}
rows = []
for ano, (nomes, pt, pw, pw2, pv) in POS.items():
    acc = {"pea": 0, "des": 0, "n_pea": 0, "n_des": 0, "pea2": 0, "des2": 0, "n_reg3": 0, "v501_9": 0}
    z = zipfile.ZipFile(MD / str(ano) / "Dados.zip")
    achados = {i.filename.split("/")[-1].upper(): i for i in z.infolist()}
    for nome in nomes:
        info = achados[nome.upper()]
        with z.open(info) as f:
            for linha in io.BufferedReader(f, 1 << 20):
                if linha[pt - 1:pt] != b"3":
                    continue
                acc["n_reg3"] += 1
                v = linha[pv - 1:pv]
                if v == b"9":
                    acc["v501_9"] += 1
                if v not in (b"1", b"2", b"3"):
                    continue
                p = int(linha[pw - 1:pw + 3])
                acc["pea"] += p
                acc["n_pea"] += 1
                if v == b"3":
                    acc["des"] += p
                    acc["n_des"] += 1
                if pw2:
                    p2 = int(linha[pw2 - 1:pw2 + 3])
                    acc["pea2"] += p2
                    if v == b"3":
                        acc["des2"] += p2
    rows.append({
        "ano": ano, "taxa_desocupacao_pct": round(100 * acc["des"] / acc["pea"], 3),
        "taxa_com_peso_alternativo_censo91_pct": round(100 * acc["des2"] / acc["pea2"], 3) if pw2 else "",
        "taxa_sem_peso_pct": round(100 * acc["n_des"] / acc["n_pea"], 3),
        "pea_ponderada": acc["pea"], "desocupados_ponderados": acc["des"], "registros_pessoa": acc["n_reg3"], "pea_amostra": acc["n_pea"], "desocupados_amostra": acc["n_des"], "v501_sem_declaracao": acc["v501_9"],
        "arquivos": ";".join(nomes),
    })
    print(rows[-1])
with open(RAIZ / "series/pnad_1981_1990_microdados.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(rows[0]))
    w.writeheader()
    w.writerows(rows)
