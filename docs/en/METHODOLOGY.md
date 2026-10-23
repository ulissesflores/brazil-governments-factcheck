# Methodology

> [!NOTE]
> Canonical language: English. The same document exists in Portuguese (Brazil), Spanish,
> Italian and Hebrew. All numbers in the prose are filled from `output/results.json` by
> `scripts/make_docs.py`, so the five versions cannot disagree. The Hebrew version is a machine
> translation with no human review of right-to-left rendering.

## 1. The question

A viral infographic ("Governos do Brasil: economia, sociedade e marcos importantes", posted on
X on 2026-10-18 with the caption "Perguntei ao ChatGPT…" and forwarded on WhatsApp) prints
57 numbers about eight Brazilian governments. This repository asks one narrow, checkable
question: **can each printed number be reproduced from public data, under a rule fixed in code?**
It does not rank governments, and it does not state or imply whom the infographic was made to
favour: intent cannot be measured from data.

## 2. Data and the acquisition hash chain

Every file downloaded for this study is recorded in a `manifest.jsonl` (one per folder under
`data/raw/`), append-only, one JSON object per line with `seq`, `url`, `timestamp_utc`,
`http_status`, `bytes`, `sha256` of the saved file, and `prev_hash`.

```text
prev_hash(line 1) = sha256("")                       # the empty string
prev_hash(line i) = sha256(exact bytes of line i-1)  # LF included
```

Changing one byte of an old line changes its hash and breaks every later `prev_hash`. The same
idea, applied to the whole repository, gives the seal (`output/provenance.json`):

```text
h_0 = sha256("")
h_i = sha256(h_{i-1} + path_i + sha256(file_i))      # files in lexicographic order of path
chain_hash = h_n
```

The idea of linking records by cryptographic hashes so that history cannot be rewritten without
detection is from Haber and Stornetta (1991, DOI 10.1007/bf00196791). Files that are public
government statistics and small enough are redistributed; large third-party documents (PDF,
ZIP, news pages) are kept as hash plus URL only, and `python -m govfc.chain restore <folder>`
downloads them again and compares the bytes. A live URL may legitimately serve a newer version:
a mismatch means "the source changed or the copy was altered", never "proof of tampering".

Reproducibility here is defined from the **sealed snapshot**, not from re-downloading: some
endpoints (for example the Ipeadata `IGP12_IGPDI12` series) return the whole history up to the
current month, so a download made next month has different bytes.

## 3. Transcription of the infographic

The image is stored with its hash (`data/infographic/`). Each printed number was transcribed
to `data/infographic/infografico-transcrito.csv` with the window or year printed next to it
(for example "1995-2002" or "1990 (referencia)"). A cell with two values ("8.4 -> 6.5")
becomes two rows. A trailing asterisk means "estimates or partial" in the infographic's own
footer.

## 4. Windows: what the infographic prints versus the actual terms

Each indicator is evaluated **over the window printed on the infographic**. The terms of office
(posse and exit dates, `data/curated/mandatos.csv`, with sources) are used to show what the
infographic leaves out and to build windows that match actual terms. The infographic covers 8 of
the 13 heads of government between 1964 and 2026 and omits 34.3% of the months
(257.6 of 750.1): Castelo Branco, Geisel, Figueiredo, Sarney and Collor.
Months are `days / 30.4375`.

## 5. Indicators: primary specification and formulas

For each indicator **one primary specification** is declared (in `code/govfc/build_results.py`,
`ESPECIFICACAO`). Alternatives that were also tried are stored beside it as *sensitivity*
and never change the verdict. They are reported with their count (`n_alternativas`) because
trying many alternatives and keeping the closest one inflates agreement by chance
(multiple comparisons); the primary specification is the one that counts.

| Indicator | Primary specification | Series (owner, code) |
|---|---|---|
| GDP growth | arithmetic mean of annual real growth over the printed window | IBGE national accounts via Ipeadata `SCN10_PIBG10` |
| Inflation | monthly IPCA compounded per calendar year; arithmetic mean over the window | BCB SGS 433 (IPCA); sensitivity: SGS 188 (INPC), 189 (IGP-M), 190 (IGP-DI), Ipeadata `IGP12_IGPDI12` |
| Unemployment | the series whose coverage includes the whole window, never spliced: PME old (to 2002), PME new (2003-2015), PNAD Continua (from 2012) | IBGE via Ipeadata `PME12_TDA12`, `PAN12_TD12`; SIDRA 4562 |
| Minimum wage | real value, December of the last window year over December of the year before | Ipea `GAC12_SALMINRE12` |
| Poverty | one series, US$ 6.85/day (2017 PPP), at the printed year | World Bank Poverty and Inequality Platform (PIP) |
| Gini | one series, household per-capita income, at the printed year | World Bank PIP |
| Life expectancy | one vintage, at the printed year | World Bank WDI `SP.DYN.LE00.IN` (UN World Population Prospects) |

**Averages.** The infographic says "média anual" (annual average). The literal reading is the
arithmetic mean of the annual rates, which is the primary specification. The geometric mean is
the better summary of compounding rates (Fleming and Wallace 1986, DOI 10.1145/5666.5673) and is
reported as sensitivity; the two differ by less than 0.3 percentage points in every window of
the infographic except hyperinflation (Itamar 1992-94: arithmetic 1504%, geometric 1373%).

**Why one homogeneous source for social indicators.** The infographic compares across
governments, so the comparison is only meaningful inside one method. A first version of the
engine took IBGE where it had the year and the World Bank where it did not; that mixes methods
inside one row and was replaced (see `CHANGELOG.md`).

## 6. The verdict rule

One rule, in `code/govfc/verdict.py`, applied identically to every row and fixed before the
results were read. Let *printed* be the number as printed and *reproduced* the number obtained
under the primary specification.

| Verdict | Condition |
|---|---|
| reproduces | *reproduced* rounds (half up) to *printed* at the printed number of decimals |
| approximates | otherwise, but within 0.3 percentage points (percentage rows) or within 5% relative (any row) |
| does not reproduce | farther than that |
| not verified | no official series covers the printed window or year |

**Stated limitation.** The primary specifications were fixed after an exploratory pass over the
data (the `RESULTADO.md` of each area). The verdicts therefore describe how the printed numbers
relate to public data; they are not a pre-registered hypothesis test. What *was* pre-registered,
before any data were downloaded, is the list of omitted dimensions and how they are reported
(`data/raw/preregistro/PREREGISTRATION.md`).

## 7. The monetary dimension

The infographic has no monetary row. This repository adds one because inflation measured by a
consumer price index is not the only way a government's monetary policy reaches households.

* **Base money (M0)** and **M1** can be spliced over long periods; **M2, M3, M4** exist as
  official series only from July 1988 and in **three definitions** (before 2001; the 2001
  methodology, rebuilt by the Central Bank from 1988 and discontinued in June 2018; and the
  "Novo" definition from December 2001). They are compared as a **ratio to GDP inside each
  regime**, never as levels across regimes.
* **Currency changes.** Brazil cut zeros five times between 1967 and 1994 (the Real is
  CR$ 2,750 = R$ 1.00); levels in the SGS are in the currency of the time and are converted before
  any ratio is taken.
* **Seigniorage and the inflation tax.** The inflation tax is the transfer from money holders
  to the issuer through the loss of purchasing power of base money. We use the monthly formula of
  Cysne and Coimbra-Lisboa (2004, DOI 10.1590/0101-35172004-1602, eq. 2) and report the total
  inflation-tax transfer (TIT, based on M1) because the definition of the monetary base changed
  in 1980. Concepts: Bailey (1956, DOI 10.1086/257766) and Fischer (1982, DOI 10.1086/261057).
  Our implementation reproduces the authors' own Table 1 for 1947-2003 with a mean absolute error
  of 0.18 percentage points of GDP (correlation 0.9986); the annual shortcut
  `pi/(1+pi) x M0/GDP` fails in hyperinflation (1980-1994, correlation about -0.06) and the change
  in base money over GDP is not the inflation tax (in 1994 it is 4.9% of GDP against 1.0%,
  because the Real Plan re-monetised the economy).

## 8. Method breaks and the comparison inside a single method

A series can improve only because the way it is computed changed. For every series used here the
repository records (`data/curated/quebras.csv`) each break: date, old and new method, **the
reason the source itself gives**, the direction of the effect, the effect measured where the two
methods overlap (or "no overlap"), and whether the source presents the change as an improvement.
Next to every comparison that crosses a break, a comparison **inside a single method** is shown
(`comparativo-metodo-constante`). Official breaks, which affect any comparison and are nobody's
fault, are kept apart from choices made by the infographic itself that mix methods in one row.

## 9. Dimensions the infographic omits

The list of omitted dimensions, the inclusion rule and the reporting rule were written before any
of those data were downloaded (`data/raw/preregistro/PREREGISTRATION.md`), anchored on the
Constitution of Brazil (art. 6, 215-216, 225) and on the infographic's own text. Every collected
indicator is reported for every government, in both directions.

## 10. Limitations

1. Verdicts depend on the primary specification; the sensitivity lists show how much.
2. Some series have gaps by construction (no official unemployment series for 1968-73; the IPCA
   starts in 1980; no PNAD for 1994).
3. Third-party sites changed during collection are recorded by hash, not archived.
4. The hash chain proves that a file has not changed since it was recorded here; it does not
   prove that the source was right.
5. Intent is not measured. Nothing here says whom the infographic was meant to favour.

## 11. Phase 2: the composite index

Phase 1 (sections 1 to 10) scores nothing: it reproduces printed numbers and shows raw series with
their method breaks. Phase 2 adds **one composite index of living conditions**, whose rules were
written and sealed in the hash chain (`data/raw/preregistro/PREREGISTRATION-FASE-2.md`) before any
aggregate was computed. The index measures conditions in the country during each term, not the merit
of a government; the word "government" is not in its name, and causality is left to the reader.

* **Three doors.** An item enters only if (1) its reading direction ("higher is better" or "lower is
  better") is established in a peer-reviewed article with a DOI checked on Crossref and quartile 1 in
  the SJR; (2) it is not a third-party composite that already carries weights; (3) its concept is not
  already counted ("one concept, once"). Grey literature supports no rule.
* **Two published layers.** The consensual core (N, 12 areas) and the block of economic premises (P),
  whose directions are the declared premises of the author (more manufacturing, less government
  consumption, more trade openness, less state ownership of the economy), with the literature for and
  against cited side by side. The index is published as N and N+P; today 39 items in 13 areas.
* **Frozen goalposts.** Polarity first (a "lower is better" item enters multiplied by -1), then a 0-100
  scale per item: 0 = worst and 100 = best value observed in Brazil in the base period 1995-2024, no
  clipping (a value outside the base period can exceed 100 or fall below 0 and is shown as such).
* **Weights.** The declared judgement is equal importance of every area and, inside an area, of every
  item. The pre-registration then tunes area weights until each area's effective importance (the
  correlation ratio between area and index, Paruolo, Saisana and Saltelli 2013) is equal, within
  bounds; in this edition that tuning did not converge within the bounds, so the index uses the equal
  nominal weights and says so, exactly as the pre-registration prescribes. Scenarios published with the
  index: equal weights, geometric and non-compensatory aggregation (Mazziotta and Pareto 2016),
  percentile goalposts, carry-forward, and 10,000 Dirichlet draws of area weights giving the 5 % to
  95 % band of each term's closing value and the share of draws in which each term keeps its rank.
* **Breaks and gaps.** A method break is chained only through a measured overlap (mean difference for
  rates and shares, mean ratio for levels, the effect printed on the item); without overlap the longest
  base is kept and the item simply stops. No imputation: a missing item leaves that year's area mean,
  and the index is not computed for a year with fewer than 70 % of the core items.
* **Frequency.** An annual index from 1995 and a monthly index from January 1996 (amendment 06), with a
  yearly candle (open = previous December, close = December) and a candle per term (open = the year
  before inauguration, close = the last year of the term; FHC opens on 1995 because no 1994 exists).
* **Closing values of the core index (N), per term, as published:** FHC 33.6, Lula 1-2 75.4,
  Dilma 57.5, Temer 58.8, Bolsonaro 63.9, Lula 3 83.0. The middle of the table does not
  separate under the weight draws; the first and the last positions do. This is description of
  conditions, with secular trends (life expectancy, schooling) pushing every later term up.

Implementation decisions recorded after the seal, which are not amendments: the V-Dem item
`v2clstown` enters with its scale as the codebook defines it (a higher value means less state
ownership), so the sealed premise is preserved; the economic premises form one area of their own in
N+P; GDP shares use the denominator at market prices.

## 12. Dated amendments to the pre-registration

The original pre-registration is never rewritten. Each change is a dated amendment, sealed in the
same hash chain before the data it governs is downloaded or computed (0 so far, in
`data/raw/preregistro/`): 01, the comparison groups ("the world": world, Latin America and the
Caribbean, upper-middle income and seven Latin American countries, one source per indicator), the
descriptive dynamics inside each term and the data-confidence lights; 02, the candle view, the pre-Real
window and the per-year rule; 03, money, fiscal, taxes, bureaucracy, the state, the "piggy bank"
(R$ 100 thousand of December 1994 followed through time), product prices in hours of work and the
terminal view; 04, yearly candles on rates, never on levels that only rise; 05, one page with two
levels, the "start -> end" cell and the data corrections of the 2026-10-20 review; 06, the monthly
index; 07, 08, 09 and 10, the literature layer (section 14). Parameters chosen after amendment 05 and
declared here: a start or end value may lag the term boundary by at most 13 months for sub-annual
series and 35 months for annual series (the PNAD skipped 1994, 2000 and 2010, and the Saeb is
biennial); the term in course ends on the latest published value, with its date printed; when two
bases cover a term, the one with the smallest total lag is the principal one, otherwise the cell says
"no single base" and shows the value under each base.

## 13. Reading by term and the terminal

The question "was a government good or bad" is answered only by description, in three separate
layers that the page shows side by side and never sums: (1) the index and the items that moved most
inside the term's candle window, in 0-100 points within the goalposts; (2) Brazil minus Latin America
and the Caribbean on the same series of the same source, in the year before inauguration and in the
last year of the term; (3) the grid of every indicator, "start -> end" on one homogeneous base per
cell. An exploratory "versus trend" aggregate was computed and discarded, because it was not
pre-registered and the trend included the term's own years. The terminal carries 101 indicators in
19 domains; a series with two bases is drawn as two lines and never read across the break.

## 14. The literature layer

The only layer that speaks of causes does so in the words of the authors of peer-reviewed studies,
under a search protocol sealed before searching (amendment 07, modified by 08, 09 and 10). For each
declared episode (Plano Real, inflation targeting, Bolsa Família, the 2008 crisis, the 2014-16
recession, the labour and pension reforms, deforestation enforcement, external debt and reserves,
among others; 23 episodes), two short queries (English and Portuguese) go to OpenAlex, and every
returned work is listed with its status and the reason for exclusion. A work is included only if
(a) it has a DOI; (b) its journal is quartile 1 in the 2024 edition of the SJR; (c) Brazil appears in
the title or the abstract; (d) an identification design from a closed list is named in the abstract
(difference-in-differences, regression discontinuity, instrumental variables, synthetic control,
randomised, natural experiment, event study, propensity score, structural or general-equilibrium
model, among others, matched on word boundaries); (e) Crossref records it as a journal article. Up to
two result sentences are quoted from the abstract. There is no score, no sum and no verdict; the count
per term reflects the years elapsed and the episodes declared, never the quality of the government nor
the direction of the results.

Four rounds are published with their numbers, and the choice of queries between rounds looked only at
how many works each call returned, never at which articles appeared: round 07 (full-text search sorted
by citations, cap 40) returned 1,329 works and included 7; round 08 (title and abstract, by
relevance, cap 100) returned 532 and included 14; round 09 (short queries, cap 200) returned
5,457 and included 36; round 10 (the raw of round 09 plus three episodes on external debt,
reserves and public debt) returned 6,497 and included 38. The page shows the last round.
Declared limitations: many Brazilian journals are outside the SJR or publish without DOI; a design
matched by word admits works that only mention it (a cohort profile, an obituary, a call to action),
which stay listed because removing them by hand would be a judgement; several episodes have a
declared absence, including the external-debt episode.

## 15. External debt and the carrying cost of public debt

The "external position" dimension of the original pre-registration names external debt, so this is a
descriptive layer of phase 1 (collection `data/raw/externo-fase3/`), with every series code taken
from the Central Bank's own explanatory note of 24 February 2026, which names them one by one. The
Central Bank publishes two concepts of gross external debt, shown as two labelled lines that are
never added nor spliced: the restricted concept (loans, bonds issued abroad and trade credit,
SGS 3684, quarterly since 1972), which is the one in the headlines, and the BPM6 concept (the
restricted one plus intercompany loans and domestic-market securities held by non-residents,
SGS 25563, since 2002), which the Central Bank calls "the Brazilian external debt". At 2026-06
they stood at US$ 407.1 billion and US$ 869.5 billion. Three ratios the Central Bank
discontinued in February 2026 are shown as published and never extended: gross external debt over
GDP (SGS 11407), **net external debt over GDP (SGS 11409)** and the public sector's share
(SGS 11408); the net international investment position over GDP (SGS 12506) completes the set.

The net concept matters for a 2026 headline that said Brazil "became a net debtor again" because
gross external debt had passed international reserves. The Central Bank's own definition subtracts
from the restricted gross debt not only reserves but also Brazilian credits abroad and commercial
banks' assets abroad (US$ 36.6 billion at 2025-12); under it, the last official value
(2025-12) was still a creditor position of US$ -17.2 billion, and the last official ratio was
-0.9 % of GDP at 2025-09. Because the indicator no longer exists, there is no official
2026 value under any concept, and this repository computes none: the page draws gross debt and
reserves together and states that their difference is not the Central Bank's net external debt.
The cost of carrying public debt enters through the nominal interest and the nominal result of the
consolidated public sector over 12 months as a share of GDP (BCB, NFSP), beside the gross and net
public debt already shown. The world comparison uses a third concept, the World Bank's external debt
stocks over gross national income, for Brazil and the upper-middle-income group only, because that
source has no aggregate for the world or for Latin America and covers no high-income country.

## 16. Limitations of phases 2 and 3

1. The components of the index had been seen before the phase-2 rules were sealed (the per-term grid
   was already published); what the seal protects is the list, the directions, the goalposts, the
   weights and the aggregation, fixed before the aggregate was computed and applied equally to every
   term.
2. Five items of the index stop in 2014-2015 because the PNAD Contínua does not overlap the PNAD and
   the pre-registration forbids chaining without overlap; later terms are read with fewer items, and
   the coverage says so.
3. The literature filter is severe and mechanical; it measures what Q1 journals with a named design
   published about Brazil, not what is known.
4. The effective-importance tuning of the weights did not converge; equal nominal weights are the
   declared fallback, and the importance actually exerted by each area is published, not corrected.

## 17. References

* Atkinson, A. B. (1970). On the measurement of inequality. *Journal of Economic Theory* 2(3),
  244-263. DOI 10.1016/0022-0531(70)90039-6
* Bailey, M. J. (1956). The welfare cost of inflationary finance. *Journal of Political Economy*
  64(2), 93-110. DOI 10.1086/257766
* Cysne, R. P.; Coimbra-Lisboa, P. C. (2004). Imposto inflacionário e transferências
  inflacionárias no Brasil: 1947-2003. *Revista de Economia Política* 24(4), 632-637.
  DOI 10.1590/0101-35172004-1602
* Fischer, S. (1982). Seigniorage and the case for a national money. *Journal of Political
  Economy* 90(2), 295-313. DOI 10.1086/261057
* Fleming, P. J.; Wallace, J. J. (1986). How not to lie with statistics: the correct way to
  summarize benchmark results. *Communications of the ACM* 29(3), 218-221.
  DOI 10.1145/5666.5673
* Haber, S.; Stornetta, W. S. (1991). How to time-stamp a digital document. *Journal of
  Cryptology* 3, 99-111. DOI 10.1007/bf00196791
* Barrionuevo, A. (2015). A formação distorcida de preços administrados na experiência
  brasileira recente. *Revista de Economia Política* 35(3), 475-491.
  DOI 10.1590/0101-31572015v35n03a06
* Peng, R. D. (2011). Reproducible research in computational science. *Science* 334(6060),
  1226-1227. DOI 10.1126/science.1213847
* Wilkinson, M. D. et al. (2016). The FAIR Guiding Principles for scientific data management and
  stewardship. *Scientific Data* 3, 160018. DOI 10.1038/sdata.2016.18

Method and direction references of phase 2 (29 articles, all quartile 1 in the SJR, each
Crossref record saved with its hash in `data/raw/referencias-fase2/`):

* Arcand, J. L.; Berkes, E.; Panizza, U. (2015). Too much finance? *Journal of Economic Growth*. DOI 10.1007/s10887-015-9115-2
* Assunção, J.; Gandour, C.; Rocha, R. (2023). DETER-ing deforestation in the Amazon. *American Economic Journal: Applied Economics*. DOI 10.1257/app.20200196
* Becker, W.; Saisana, M.; Paruolo, P.; Vandecasteele, I. (2017). Weights and importance in composite indicators. *Ecological Indicators*. DOI 10.1016/j.ecolind.2017.03.056
* Bergh, A.; Henrekson, M. (2011). Government size and growth: a survey. *Journal of Economic Surveys*. DOI 10.1111/j.1467-6419.2011.00697.x
* Blanchflower, D. G.; Bell, D. N. F.; Montagnoli, A.; Moro, M. (2014). The happiness trade-off between unemployment and inflation. *Journal of Money, Credit and Banking*. DOI 10.1111/jmcb.12154
* Böhringer, C.; Jochem, P. E. P. (2007). Measuring the immeasurable: a survey of sustainability indices. *Ecological Economics*. DOI 10.1016/j.ecolecon.2007.03.008
* Coppedge, M. et al. (2011). Conceptualizing and measuring democracy: a new approach. *Perspectives on Politics*. DOI 10.1017/s1537592711000880
* Decancq, K.; Lugo, M. A. (2013). Weights in multidimensional indices of wellbeing: an overview. *Econometric Reviews*. DOI 10.1080/07474938.2012.690641
* Di Tella, R.; MacCulloch, R. J.; Oswald, A. J. (2001). Preferences over inflation and unemployment. *American Economic Review*. DOI 10.1257/aer.91.1.335
* Fleurbaey, M. (2009). Beyond GDP: the quest for a measure of social welfare. *Journal of Economic Literature*. DOI 10.1257/jel.47.4.1029
* Frankel, J. A.; Romer, D. (1999). Does trade cause growth? *American Economic Review*. DOI 10.1257/aer.89.3.379
* Greco, S.; Ishizaka, A.; Tasiou, M.; Torrisi, G. (2019). On the methodological framework of composite indices. *Social Indicators Research*. DOI 10.1007/s11205-017-1832-9
* Hansen, M. C. et al. (2013). High-resolution global maps of 21st-century forest cover change. *Science*. DOI 10.1126/science.1244693
* Hidalgo, C. A.; Hausmann, R. (2009). The building blocks of economic complexity. *Proceedings of the National Academy of Sciences*. DOI 10.1073/pnas.0900943106
* Klugman, J.; Rodríguez, F.; Choi, H.-J. (2011). The HDI 2010: new controversies, old critiques. *Journal of Economic Inequality*. DOI 10.1007/s10888-011-9178-z
* Lovejoy, T. E.; Nobre, C. (2018). Amazon tipping point. *Science Advances*. DOI 10.1126/sciadv.aat2340
* Marquardt, K. L.; Pemstein, D. (2018). IRT models for expert-coded panel data. *Political Analysis*. DOI 10.1017/pan.2018.28
* Mazziotta, M.; Pareto, A. (2016). On a generalized non-compensatory composite index. *Social Indicators Research*. DOI 10.1007/s11205-015-0998-2
* McMann, K. et al. (2020). Why low levels of democracy promote corruption and high levels diminish it. *Political Research Quarterly*. DOI 10.1177/1065912919862054
* McMann, K. et al. (2022). Assessing data quality: an approach and an application. *Political Analysis*. DOI 10.1017/pan.2021.27
* Mian, A.; Sufi, A.; Verner, E. (2017). Household debt and business cycles worldwide. *Quarterly Journal of Economics*. DOI 10.1093/qje/qjx017
* Nepstad, D. et al. (2014). Slowing Amazon deforestation through public policy. *Science*. DOI 10.1126/science.1248525
* Paruolo, P.; Saisana, M.; Saltelli, A. (2013). Ratings and rankings: voodoo or science? *Journal of the Royal Statistical Society, Series A*. DOI 10.1111/j.1467-985x.2012.01059.x
* Ravallion, M. (2012). Mashup indices of development. *World Bank Research Observer*. DOI 10.1093/wbro/lkr009
* Ravallion, M. (2012). Troubling tradeoffs in the Human Development Index. *Journal of Development Economics*. DOI 10.1016/j.jdeveco.2012.01.003
* Rodríguez, F.; Rodrik, D. (2000). Trade policy and economic growth: a skeptic's guide. *NBER Macroeconomics Annual*. DOI 10.1086/654419
* Rodrik, D. (2016). Premature deindustrialization. *Journal of Economic Growth*. DOI 10.1007/s10887-015-9122-3
* Saisana, M.; Saltelli, A.; Tarantola, S. (2005). Uncertainty and sensitivity analysis techniques as tools for the quality assessment of composite indicators. *Journal of the Royal Statistical Society, Series A*. DOI 10.1111/j.1467-985x.2005.00350.x
* Wacziarg, R.; Welch, K. H. (2008). Trade liberalization and growth: new evidence. *World Bank Economic Review*. DOI 10.1093/wber/lhn007

The direction references of every index item and the method references of the terminal (135
entries, each with its DOI) are in `docs/references-q1.bib`. Each DOI was checked against the Crossref
record, saved with its hash in `data/raw/referencias/` and `data/raw/referencias-fase2/`.
