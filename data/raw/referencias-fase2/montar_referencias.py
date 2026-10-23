# (chave, papel, citacao_no_prereg, query bibliografica, ano esperado, sobrenome do 1o autor esperado, periodico esperado (substring))
REFS = [
 ("saisana2005","metodo","Saisana, Saltelli e Tarantola, JRSS A 2005","Saisana Saltelli Tarantola Uncertainty and sensitivity analysis techniques as tools for the quality assessment of composite indicators 2005",2005,"Saisana","Royal Statistical Society"),
 ("paruolo2013","metodo","Paruolo, Saisana e Saltelli, JRSS A 2013","Paruolo Saisana Saltelli Ratings and rankings: voodoo or science? 2013",2013,"Paruolo","Royal Statistical Society"),
 ("becker2017","metodo","Becker et al., Ecological Indicators 2017","Becker Paruolo Saisana Saltelli Weights and importance in composite indicators: Closing the gap 2017",2017,"Becker","Ecological Indicators"),
 ("greco2019","metodo","Greco et al., Social Indicators Research 2019","Greco Ishizaka Tasiou Torrisi On the Methodological Framework of Composite Indices: A Review of the Issues of Weighting, Aggregation, and Robustness 2019",2019,"Greco","Social Indicators Research"),
 ("decancq2013","metodo","Decancq e Lugo, Econometric Reviews 2013","Decancq Lugo Weights in Multidimensional Indices of Wellbeing: An Overview 2013",2013,"Decancq","Econometric Reviews"),
 ("mazziotta2016","metodo","Mazziotta e Pareto, Social Indicators Research 2016","Mazziotta Pareto On a Generalized Non-compensatory Composite Index for Measuring Socio-economic Phenomena 2016",2016,"Mazziotta","Social Indicators Research"),
 ("ravallion2012wbro","metodo","Ravallion, World Bank Research Observer 2012","Ravallion Mashup Indices of Development 2012",2012,"Ravallion","World Bank Research Observer"),
 ("ravallion2012jde","metodo","Ravallion, Journal of Development Economics 2012","Ravallion Troubling tradeoffs in the Human Development Index 2012",2012,"Ravallion","Journal of Development Economics"),
 ("bohringer2007","metodo","Bohringer e Jochem, Ecological Economics 2007","Bohringer Jochem Measuring the immeasurable A survey of sustainability indices 2007",2007,"B","Ecological Economics"),
 ("klugman2011","metodo","Klugman, Rodriguez e Choi, Journal of Economic Inequality 2011","Klugman Rodriguez Choi The HDI 2010: new controversies, old critiques 2011",2011,"Klugman","Economic Inequality"),
 ("fleurbaey2009","metodo","Fleurbaey, Journal of Economic Literature 2009","Fleurbaey Beyond GDP: The Quest for a Measure of Social Welfare 2009",2009,"Fleurbaey","Journal of Economic Literature"),
 ("ditella2001","metodo","Di Tella, MacCulloch e Oswald, AER 2001","Di Tella MacCulloch Oswald Preferences over Inflation and Unemployment: Evidence from Surveys of Happiness 2001",2001,"Di Tella","American Economic Review"),
 ("blanchflower2014","metodo","Blanchflower et al., Journal of Money, Credit and Banking 2014","Blanchflower Bell Montagnoli Moro The Happiness Trade-Off between Unemployment and Inflation 2014",2014,"Blanchflower","Journal of Money, Credit"),
 ("mian2017","direcao","Mian, Sufi e Verner, QJE 2017","Mian Sufi Verner Household Debt and Business Cycles Worldwide 2017",2017,"Mian","Quarterly Journal of Economics"),
 ("marquardt2018","direcao","Marquardt e Pemstein, Political Analysis 2018","Marquardt Pemstein IRT Models for Expert-Coded Panel Data 2018",2018,"Marquardt","Political Analysis"),
 ("coppedge2011","direcao","Coppedge et al., Perspectives on Politics 2011","Coppedge Gerring Altman Bernhard Fish Hicken Kroenig Lindberg McMann Paxton Semetko Skaaning Staton Teorell Conceptualizing and Measuring Democracy: A New Approach 2011",2011,"Coppedge","Perspectives on Politics"),
 ("hidalgo2009","direcao","Hidalgo e Hausmann, PNAS 2009","Hidalgo Hausmann The building blocks of economic complexity 2009",2009,"Hidalgo","Proceedings of the National Academy"),
 ("rodrik2016","direcao","Rodrik, Journal of Economic Growth 2016","Rodrik Premature deindustrialization 2016",2016,"Rodrik","Journal of Economic Growth"),
 ("bergh2011","direcao","Bergh e Henrekson, Journal of Economic Surveys 2011","Bergh Henrekson Government size and growth: a survey and interpretation of the evidence 2011",2011,"Bergh","Journal of Economic Surveys"),
 ("frankel1999","direcao","Frankel e Romer, AER 1999","Frankel Romer Does Trade Cause Growth? 1999",1999,"Frankel","American Economic Review"),
 ("wacziarg2008","direcao","Wacziarg e Welch, World Bank Economic Review 2008","Wacziarg Welch Trade Liberalization and Growth: New Evidence 2008",2008,"Wacziarg","World Bank Economic Review"),
 ("rodriguez2000","direcao","Rodriguez e Rodrik, NBER Macroeconomics Annual 2000","Rodriguez Rodrik Trade Policy and Economic Growth: A Skeptic's Guide to the Cross-National Evidence 2000",2000,"Rodr","NBER Macroeconomics Annual"),
 ("arcand2015","direcao","Arcand, Berkes e Panizza, Journal of Economic Growth 2015","Arcand Berkes Panizza Too much finance? 2015",2015,"Arcand","Journal of Economic Growth"),
 # implicitas
 ("mcmann2022","direcao","(implicita) corrupcao politica V-Dem: McMann et al., Political Analysis 2022","McMann Pemstein Seim Teorell Lindberg Assessing Data Quality: An Approach and An Application 2022",2022,"McMann","Political Analysis"),
 ("mcmann2020","direcao","(implicita) corrupcao V-Dem: McMann et al., Political Research Quarterly 2020","McMann Seim Teorell Lindberg Why Low Levels of Democracy Promote Corruption and High Levels Diminish It 2020",2020,"McMann","Political Research Quarterly"),
 ("nepstad2014","direcao","(implicita) desmatamento da Amazonia: Nepstad et al., Science 2014","Nepstad Slowing Amazon deforestation through public policy and interventions in beef and soy supply chains 2014",2014,"Nepstad","Science"),
 ("assuncao2023","direcao","(implicita) desmatamento da Amazonia: Assuncao, Gandour e Rocha, Environment and Development Economics 2023","Assuncao Gandour Rocha DETERring Deforestation in the Amazon: Environmental Monitoring and Law Enforcement 2023",2023,"Assun","Environment and Development Economics"),
 ("hansen2013","direcao","(implicita) desmatamento: Hansen et al., Science 2013","Hansen High-Resolution Global Maps of 21st-Century Forest Cover Change 2013",2013,"Hansen","Science"),
]

# ----- escolha do registro certo (DOI) por referencia, decidida lendo bruto/busca-<chave>.json -----
DOI = {
"saisana2005":"10.1111/j.1467-985x.2005.00350.x","paruolo2013":"10.1111/j.1467-985x.2012.01059.x","becker2017":"10.1016/j.ecolind.2017.03.056",
"greco2019":"10.1007/s11205-017-1832-9","decancq2013":"10.1080/07474938.2012.690641","mazziotta2016":"10.1007/s11205-015-0998-2",
"ravallion2012wbro":"10.1093/wbro/lkr009","ravallion2012jde":"10.1016/j.jdeveco.2012.01.003","bohringer2007":"10.1016/j.ecolecon.2007.03.008",
"klugman2011":"10.1007/s10888-011-9178-z","fleurbaey2009":"10.1257/jel.47.4.1029","ditella2001":"10.1257/aer.91.1.335","blanchflower2014":"10.1111/jmcb.12154",
"mian2017":"10.1093/qje/qjx017","marquardt2018":"10.1017/pan.2018.28","coppedge2011":"10.1017/s1537592711000880","hidalgo2009":"10.1073/pnas.0900943106",
"rodrik2016":"10.1007/s10887-015-9122-3","bergh2011":"10.1111/j.1467-6419.2011.00697.x","frankel1999":"10.1257/aer.89.3.379","wacziarg2008":"10.1093/wber/lhn007",
"rodriguez2000":"10.1086/654419","arcand2015":"10.1007/s10887-015-9115-2","mcmann2022":"10.1017/pan.2021.27","mcmann2020":"10.1177/1065912919862054",
"nepstad2014":"10.1126/science.1248525","assuncao2023":"10.1257/app.20200196","hansen2013":"10.1126/science.1244693","lovejoy2018":"10.1126/sciadv.aat2340",
}
LOVEJOY = ("lovejoy2018","direcao","(implicita) desmatamento da Amazonia: Lovejoy e Nobre, Science Advances 2018","",2018,"Lovejoy","Science Advances")
# working papers que so existem como literatura cinzenta (registro vem da busca, nao ha artigo de periodico): (chave, papel, citacao, arquivo de busca, DOI)
CINZENTAS = [
 ("mcmann2016ssrn","direcao","(implicita) corrupcao V-Dem: McMann, Pemstein, Seim, Teorell, Strategies of Validation, SSRN 2016 (working paper)","busca-mcmann2022.json","10.2139/ssrn.2727595"),
 ("pemstein2018ssrn","direcao","(implicita) modelo de medicao do V-Dem: Pemstein et al., V-Dem Working Paper / SSRN 2018","busca-marquardt2018.json","10.2139/ssrn.3167764"),
]

if __name__ == "__main__":
    import csv, html, json, re, sys
    from pathlib import Path
    D = Path(__file__).resolve().parent
    B = D / "bruto"
    # SJR: CSV do Wayback (edicao SJR 2024), indexado por ISSN sem hifen
    sjr = list(csv.DictReader(open(B / "scimago-journalrank-wayback-20251026.csv", encoding="utf-8"), delimiter=";"))
    idx = {}
    for r in sjr:
        for i in r["Issn"].replace('"', "").split(","):
            if i.strip():
                idx.setdefault(i.strip(), r)
    limpa = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
    bib_esc = lambda s: s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")
    todas = REFS + [LOVEJOY]
    linhas, bibs = [], []
    for ch, papel, cit, q, ano_prereg, _au, _per in todas:
        m = json.load(open(B / f"crossref-{ch}.json"))["message"]
        doi = m["DOI"]
        assert doi.lower() == DOI[ch].lower(), (ch, doi)
        tit = limpa((m.get("title") or [""])[0])
        aut = "; ".join(f"{a.get('family','')}, {a.get('given','')}".strip(", ") for a in m.get("author", []))
        per = limpa((m.get("container-title") or [""])[0])
        dp = lambda k: (m.get(k, {}).get("date-parts") or [[None]])[0][0]
        ano = dp("published-print") or dp("issued")
        online = dp("published-online") or dp("issued")
        issn = "; ".join(m.get("ISSN", []))
        s = next((idx[i.replace("-", "")] for i in m.get("ISSN", []) if i.replace("-", "") in idx), None)
        notas = [f"crossref=bruto/crossref-{ch}.json", f"tipo={m['type']}", f"vol={m.get('volume','')}({m.get('issue','')}) p.{m.get('page','')}"]
        if online and online != ano:
            notas.append(f"primeiro online {online}; ano de capa {ano}")
        if ano_prereg and ano != ano_prereg:
            notas.append(f"ATENCAO ano do prereg {ano_prereg} difere do Crossref {ano}")
        if s:
            qt = s["SJR Best Quartile"]
            notas.append(f"SJR={s['SJR']} (periodico no SJR: {s['Title']}); categorias: {s['Categories']}; fonte=bruto/scimago-journalrank-wayback-20251026.csv")
            if qt != "Q1":
                notas.append("quartil nao e Q1")
            status = "confirmada" if m["type"] == "journal-article" else "cinzenta"
        else:
            qt, status = "", "doi_sem_quartil"
            notas.append("periodico nao encontrado no CSV SJR por ISSN")
        linhas.append(dict(chave=ch, papel_no_prereg=papel, citacao_no_prereg=cit, doi=doi, titulo=tit, autores=aut, periodico=per, ano=ano, issn=issn,
                           sjr_quartil=qt, sjr_ano=2024 if s else "", qualis="", status=status, url_registro=f"https://api.crossref.org/works/{doi}", nota=" | ".join(notas)))
        if status == "confirmada":
            au = " and ".join(f"{a.get('family','')}, {a.get('given','')}" for a in m.get("author", []))
            campos = [("author", au), ("title", "{" + tit + "}"), ("journal", per), ("year", str(ano)), ("volume", m.get("volume", "")),
                      ("number", m.get("issue", "")), ("pages", (m.get("page") or "").replace("-", "--")), ("doi", doi), ("issn", issn)]
            corpo = ",\n".join(f"  {k} = {{{bib_esc(v) if k != 'title' else '{' + bib_esc(tit) + '}'}}}" for k, v in campos if v and v != "{" + tit + "}" or k == "title")
            bibs.append(f"@article{{{ch},\n{corpo}\n}}\n")
    for ch, papel, cit, arq, doi in CINZENTAS:
        it = next(i for i in json.load(open(B / arq))["message"]["items"] if i["DOI"].lower() == doi.lower())
        dp = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
        linhas.append(dict(chave=ch, papel_no_prereg=papel, citacao_no_prereg=cit, doi=doi, titulo=limpa(it["title"][0]),
                           autores="; ".join(f"{a.get('family','')}, {a.get('given','')}" for a in it.get("author", [])),
                           periodico=limpa((it.get("container-title") or [""])[0]), ano=dp, issn="", sjr_quartil="", sjr_ano="", qualis="", status="cinzenta",
                           url_registro=f"https://api.crossref.org/works/{doi}", nota=f"working paper/preprint (SSRN); registro vem de bruto/{arq}; nao sustenta regra"))
    cols = ["chave","papel_no_prereg","citacao_no_prereg","doi","titulo","autores","periodico","ano","issn","sjr_quartil","sjr_ano","qualis","status","url_registro","nota"]
    with open(D / "referencias.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(linhas)
    (D / "referencias.bib").write_text("\n".join(bibs), encoding="utf-8")
    from collections import Counter
    print(Counter(l["status"] for l in linhas), Counter(l["sjr_quartil"] for l in linhas))
