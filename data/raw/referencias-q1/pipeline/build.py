import json, csv, sys, html, re
sys.path.insert(0,'.')
from sel import SEL
from texts import T
from fetch import PASTA, doi_dest
G=json.load(open('groups.json')); R=json.load(open('scim_parsed.json'))
def norm(i): return i.replace('-','')
issn2grp={}
for gi,g in enumerate(G):
    for i in g[0]: issn2grp[norm(i)]=gi
ECON={"Economics and Econometrics","Economics, Econometrics and Finance (miscellaneous)","Development"}
POL={"Political Science and International Relations","Sociology and Political Science"}
HEALTH={"Epidemiology","Public Health, Environmental and Occupational Health","Medicine (miscellaneous)","Demography","Health Policy","Multidisciplinary"}
STAT={"Statistics and Probability","Statistics, Probability and Uncertainty","Applied Mathematics"}
PSY={"Psychology (miscellaneous)","Multidisciplinary"}
CS={"Computer Science (miscellaneous)","Computer Science Applications","Information Systems","Library and Information Sciences"}
AREA={1:ECON|POL|STAT|CS|{"Management Science and Operations Research","Business and International Management"},
 2:ECON|STAT|{"Epidemiology","History"},3:ECON|POL,4:HEALTH,5:ECON,6:ECON|POL,7:ECON|{"Education"},8:ECON,9:HEALTH,10:POL,11:ECON|PSY|STAT|CS,12:ECON|STAT}
def clean(s): return html.unescape(s or "").strip()
rows=[]; missing=[k for k in T if k not in {x[1] for x in SEL}]; print("textos sem ref:",missing, "| refs sem texto:",[x[1] for x in SEL if x[1] not in T])
for tema,key,doi in SEL:
    m=json.loads((PASTA/doi_dest(doi)).read_text())["message"]
    au=m.get("author",[])
    names=[ (a.get("family") or a.get("name") or "?")+((", "+a["given"]) if a.get("given") else "") for a in au]
    autores="; ".join(names[:6])+("; et al." if len(names)>6 else "")
    ano=((m.get("published-print") or m.get("issued") or {}).get("date-parts") or [[None]])[0][0]
    titulo=clean((m.get("title") or [""])[0]); per=clean((m.get("container-title") or [""])[0])
    typ=m.get("type"); issns=m.get("ISSN",[])
    gi=None
    for i in issns:
        if norm(i) in issn2grp: gi=issn2grp[norm(i)]; break
    sc=R[str(gi)] if gi is not None else None
    if sc:
        mx=max(y for c,y,q in sc["cats"]); cats=[(c,q) for c,y,q in sc["cats"] if y==mx]
        best=min(q for c,q in cats)
        area="; ".join(f"{c} ({q})" for c,q in cats); sq=best; sy=mx
        sfile=f"scimago/scimago-sid{sc['sid']}.json"
        q1set={c for c,q in cats if q=="Q1"}
        ok_area=bool(q1set & AREA[tema])
    else:
        sq,area,sy="n/d","sem correspondência no Scimago","" ; ok_area=False
        sfile=f"scimago/scimago-nomatch-{norm(issns[0])[:4]}-{norm(issns[0])[4:]}.json" if issns else ""
        if gi is not None: sfile=f"scimago/scimago-nomatch-{G[gi][0][0]}.json"
        if not issns: sfile=""
    papel="ancora" if (typ=="journal-article" and sc and ok_area) else "complementar"
    s,n=T[key]
    if ano and ano<2010 and papel=="ancora": s="[clássico, pré-2010] "+s
    rows.append(dict(tema=tema,chave_bibtex=key,autores=autores,ano=ano,titulo=titulo,periodico=per,doi=m["DOI"],crossref_conferido="sim",
        scimago_quartil=sq,scimago_area=area,scimago_ano=sy,o_que_sustenta=s,o_que_nao_sustenta=n,papel=papel,
        arquivo_crossref=doi_dest(doi),arquivo_scimago=sfile,_type=typ,_names=names,_m=m))
cols="tema,chave_bibtex,autores,ano,titulo,periodico,doi,crossref_conferido,scimago_quartil,scimago_area,scimago_ano,o_que_sustenta,o_que_nao_sustenta,papel,arquivo_crossref,arquivo_scimago".split(",")
with open(PASTA/"referencias-q1.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore"); w.writeheader()
    for r in rows: w.writerow(r)
# bibtex
def esc(s): return s.replace("\\","\\textbackslash{}").replace("&","\\&").replace("%","\\%").replace("#","\\#").replace("_","\\_")
out=[]
for r in rows:
    m=r["_m"]; names=r["_names"]
    au=" and ".join(names[:10]) + (" and others" if len(names)>10 else "")
    typ={"journal-article":"article"}.get(r["_type"],"techreport" if r["_type"] in("report","monograph") else "misc")
    f=[("author",au),("title","{"+clean((m.get("title") or [""])[0])+"}"),("year",str(r["ano"]))]
    if typ=="article":
        f.append(("journal",r["periodico"]))
        for k,b in (("volume","volume"),("number","issue"),("pages","page")):
            if m.get(b): f.append((k,str(m[b]).replace("-","--")))
    else:
        if r["periodico"]: f.append(("howpublished",r["periodico"]))
        else: f.append(("note","Working paper / relatório; "+m.get("publisher","")))
    f.append(("doi",m["DOI"]))
    body=",\n".join(f"  {k} = {{{esc(v) if not v.startswith('{') else '{'+esc(v[1:-1])+'}'}}}" for k,v in f)
    out.append(f"@{typ}{{{r['chave_bibtex']},\n{body}\n}}\n")
(PASTA/"references-q1.bib").write_text("\n".join(out),encoding="utf-8")
json.dump([{k:v for k,v in r.items() if not k.startswith('_')} for r in rows],open('rows.json','w'),ensure_ascii=False)
import collections
c=collections.Counter((r["tema"],r["papel"]) for r in rows)
for t in range(1,13): print(t, "ancora",c[(t,"ancora")], "compl",c[(t,"complementar")], "ancoras>=2010:", sum(1 for r in rows if r["tema"]==t and r["papel"]=="ancora" and r["ano"]>=2010))
print("total ancoras",sum(1 for r in rows if r["papel"]=="ancora"),"de",len(rows))
