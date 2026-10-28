# Amendment 02: the candle view, the pre-Real window and the per-year rule

**Registered:** 2026-10-20T14:52:02Z (UTC). **Amends:** `PREREGISTRATION-EMENDA-01.md` section C (dynamics). Requested
during review (2026-10-20): "terms of 8 and 4 years cannot be compared by their totals; use open,
close, high and low like a candlestick, annualised; collapse everything before the Real Plan into one
column". No new metric is created; the display is fixed here before the pictures are drawn.

## A. The candle (one per indicator, base and term)

* **Open** = value of the year before the term (as in C: start). **Close** = last year of the term.
* **High / Low** = maximum and minimum of the annual values inside the term.
* **Number shown with the candle** = the trend per year already defined in C (OLS slope over the
  term's years, with its standard error). Alternative shown in the tooltip: (close − open) / years.
* **Flows** (growth rates, inflation, deforestation, inflation tax): the candle shows the dispersion
  of the annual rates (open = first year, close = last, high/low = extremes) and the strong mark is
  the **term mean**, which is already an annual rate. The compounded total of the term goes to the
  tooltip.
* **Colour of the candle body** = direction in the usual reading sense of the indicator (improved /
  worsened / stable), the same rule as C. It is not a merit colour, and it is never green or red:
  red and yellow remain the data-confidence lights.

## B. The per-year rule, by unit

| Unit of the indicator | Trend per year expressed as |
|---|---|
| percentage or rate (unemployment, poverty, Gini, failure rate, coverage) | percentage points per year |
| monetary level or index (real minimum wage, baskets, GDP per capita level) | geometric % per year: (close / open)^(1/years) − 1 |
| years of life, per 100,000, Saeb points, index 0-1 | units per year |

## C. The pre-Real window

One aggregated column **1964-1994 (calendar years)**: open = 1964 (or first year with data), close =
1994, high/low/mean over the window, with the number of years with data. The Real Plan started on
1 July 1994; the window closes on the last calendar year before the first full year of the Real.
From **FHC (1995) onwards** every term is its own candle. The governments of 1964-1994 are not
removed: the aggregated column is the default view and opens into the per-government candles on
request, so the reporting rule of section E ("every indicator for every government") still holds.
Itamar Franco (Oct 1992 - Dec 1994) is inside the aggregated column.

## D. Logarithmic axis, by rule

The axis of a chart is logarithmic when every value is positive and max / min > 20 (hyperinflation,
nominal values); never for a flow that takes negative values (GDP growth) and never for indices
bounded in 0-1 or 0-100.

## E. Front page

The front page shows one grid: 8 to 10 headline indicators (one or two per domain) × 7 columns
(pre-Real, FHC, Lula 1-2, Dilma, Temer, Bolsonaro, Lula 3). Everything else (full matrix, world,
mechanisms, vintages, glossary) is one level below. The headline set is fixed here: GDP per capita
growth, inflation (IGP-DI), real minimum wage in baskets, unemployment, poverty (US$ 6.85), Gini,
life expectancy, homicides, failure rate beside Saeb, inflation tax.

## Amendment log

* 02 (this file): sections A to E.
