# Amendment 01 to the pre-registration

**Registered:** 2026-10-19T19:00:28Z (UTC), before any data of the items below was downloaded.
**Amends:** `PREREGISTRATION.md` (registered earlier the same day). The original is not rewritten; this amendment is dated and registered in the same hash chain.
**Why:** the requester asked, during review, for (1) comparison with "the world that makes sense", (2) descriptive measures of oscillation and acceleration inside each term, (3) data-confidence warning lights, (4) indicators that do not depend on the deflator or on a rule, and (5) legacy-versus-harvest context for growth. Fixing the definitions now, before the numbers are seen, keeps the choice from depending on the result.

## A. Comparison groups ("the world")

The Brazil series is always shown beside these references; "Brazil minus reference" is the reading. Fixed now:

1. **World** (World Bank code WLD).
2. **Latin America and the Caribbean** (LCN, World Bank aggregate).
3. **Upper-middle-income countries** (UMC, World Bank aggregate; membership is the World Bank's own, taken as published).
4. **Latin American countries individually**: Argentina, Chile, Colombia, Mexico, Peru, Uruguay, Venezuela. All seven are shown when the series exists; none is dropped after seeing the result, and Venezuela's data problems are flagged, not hidden.
5. **External driver for Brazil:** the terms-of-trade index (export prices over import prices), from the source with the longest series, because the commodity boom is the main "wave of the world" candidate for the 2003-2010 window.

Sources: World Bank WDI and PIP; UNODC; WHO and UNICEF (WUENIC); V-Dem; Penn World Table and Maddison Project Database for GDP levels in constant purchasing-power-parity dollars (cross-check against WDI). A country-year without a value stays empty; no interpolation across a break.

## B. Added indicators (primary candidate first)

| Block | Indicators |
|---|---|
| Growth context | gross fixed capital formation as % of GDP (IBGE national accounts); public investment as % of GDP; capital stock and total factor productivity (Penn World Table); GDP per capita in constant PPP dollars (PWT, Maddison, WDI) and in constant reais, never in current dollars |
| Purchasing power | cost of the basic food basket (DIEESE) and the minimum wage measured in baskets and in hours of work needed to buy one; alternative price indices beside the official one: INPC, IGP-DI, IPC-Fipe, DIEESE index, FGV IPC-C1 (low-income households); monetary overhang = growth of M1 (and of M0) minus real GDP growth |
| Labour | employment-to-population ratio; labour-force underutilisation and discouraged workers (PNADC); unemployment from the PNAD for 1981-1990 and from the Censuses of 1970 and 1980 where the microdata allow; the ILO treatment of benefit recipients, documented |
| Education | approval, failure and dropout rates by state (INEP, recovered from the web archive if the original files are gone); Saeb proficiency as the rule-independent partner |

## C. Descriptive dynamics inside each term (no forecasting)

For every indicator and every term, computed on the annual values of the homogeneous primary series:

* **Start and end:** value of the year before the term and value of the last year of the term.
* **Trend:** ordinary-least-squares slope over the term's years, with its standard error; reported with the number of years used. Terms with fewer than 4 annual values report "too short".
* **Acceleration:** slope of the second half of the term minus slope of the first half.
* **Volatility:** standard deviation of the annual changes (for rates, of the annual values).
* **End-of-term deviation:** value of the last year minus the mean of the term, divided by the standard deviation.
* **Post-term reversal:** value of the first year after the term minus value of the last year of the term.

Extrapolating a trend several years ahead is NOT a forecast and is not part of this layer. If it is ever shown, it is labelled "linear extrapolation of the term's slope", carries an interval, and is accompanied by the back-test of how that rule performed in the past.

## D. Data-confidence lights (rule v1, categorical)

A light says something about the DATA, not about the government. Each (indicator, term) cell gets none, yellow or red, from the break catalogue only:

* **Red:** a break of type `mudanca_de_regra` or `metodo_estatistico` inside the term whose effect was not measured by overlap; or a break whose measured effect is as large as the term's start-to-end change; or fewer than half of the term's years have data.
* **Yellow:** a break of any type inside the term whose effect was measured and is smaller than the start-to-end change; a vintage revision inside the term; a series that is a model estimate published by the source; 50 % to 80 % of the term's years with data.
* **None:** otherwise.

A numeric effect column for the catalogue is a backlog item; until then "measured" means the catalogue cites a number measured on overlapping data.

## E. Not defined here

No score, no ranking of merit, no "method-integrity" points. They need a rule written and pre-registered separately, applied to every government, with sensitivity to alternative weights.

## Amendment log

* 01 (this file): sections A to E.
