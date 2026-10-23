"""Compara, faixa a faixa, colunas de tabelas Amil PF RJ capturadas no Wayback. Pares escolhidos por RÓTULO igual no documento
(2006-05 x 2006-11) ou por VALOR identico em todas as faixas (2009-02 x 2010-01, produto renomeado: so observacao)."""
import csv, pathlib
BASE = pathlib.Path(__file__).resolve().parent.parent
R = list(csv.DictReader(open(BASE/"series/amil_pf_rj_tabelas_wayback.csv", encoding="utf8")))
def col(data, rot, secao_contem=None):
    return {r["faixa_etaria"]: float(r["mensalidade_rs"]) for r in R if r["data_captura_wayback"] == data and r["coluna_rotulo_no_documento"] == rot and (secao_contem is None or secao_contem in r["secao"].upper()) and "NEXT" not in r["produto_titulo"].upper()}
pares = [("2006-05-11","AMIL 40 101 QP","2007-02-28","Amil 40 101 QP","mesmo rotulo (caixa diferente)"),
         ("2006-05-11","AMIL 40 PLUS","2007-02-28","Amil 40 PLUS QP","rotulo quase igual (+ 'QP')"),
         ("2006-05-11","AMIL 30 Especial","2007-02-28","AMIL 30 ESPECIAL","mesmo rotulo (caixa diferente)"),
         ("2006-05-11","AMIL 20","2007-02-28","Amil 20 QP","rotulo quase igual (+ 'QP')"),
         ("2009-03-06","Amil 110 Nacional QP","2010-06-02","Amil Blue II Nacional QP","SO observacao: produto renomeado; comparo valores, nao afirmo que seja o mesmo plano"),
         ("2009-03-06","Amil 120 Nacional QP","2010-06-02","Amil Blue III Nacional QP","SO observacao: idem"),
         ("2009-03-06","Amil 130 Nacional QP","2010-06-02","Amil Blue IV Nacional QP","SO observacao: idem")]
out = [["data_a","rotulo_a","data_b","rotulo_b","tipo_do_par","faixa_etaria","mensalidade_a_rs","mensalidade_b_rs","variacao_pct"]]
for da, ra, db, rb, tp in pares:
    a, b = col(da, ra), col(db, rb)
    assert len(a) == 10 and len(b) == 10, (ra, rb, len(a), len(b))
    for fx in a: out.append([da, ra, db, rb, tp, fx, f"{a[fx]:.2f}", f"{b[fx]:.2f}", f"{(b[fx]/a[fx]-1)*100:.2f}"])
csv.writer(open(BASE/"derivado/amil_comparacoes_rotulo.csv", "w", newline="", encoding="utf8")).writerows(out)
import statistics
for da, ra, db, rb, tp in pares:
    v = [float(r[8]) for r in out[1:] if r[1] == ra and r[3] == rb]
    print(ra, "->", rb, "variacao min/max:", min(v), max(v))
