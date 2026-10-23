# Pre-registration: which dimensions the infographic leaves out, and how they will be compared

**Registered:** 2026-10-19T16:58:43Z (UTC), before any data of the dimensions below was downloaded.
**Status of the evidence:** the timestamp is the file's modification time recorded in
`manifest.jsonl` (hash chain). It is a local timestamp, not a third-party one; the repository
DOI deposit (Zenodo) will add an external date.

## Why this file exists

The infographic shows seven indicators (GDP growth, inflation, unemployment, minimum wage,
poverty, Gini, life expectancy). A reader may suspect that what it leaves out was chosen to favour
a side. Intent cannot be measured from data, and the same temptation exists for us: picking
the omitted dimensions after seeing which ones flip the picture would repeat the infographic's
move with the sign reversed. So the list of dimensions, the inclusion rule and the reporting
rule are written here first and are not changed after data arrive, except by a dated amendment
at the bottom.

## Where the list of dimensions comes from (an external anchor, not our taste)

1. **Constitution of Brazil, art. 6** (text in force, `data/raw/preregistro/constituicao-planalto.html`,
   sha256 in the manifest): "São direitos sociais a educação, a saúde, a alimentação, o trabalho,
   a moradia, o transporte, o lazer, a segurança, a previdência social, a proteção à maternidade
   e à infância, a assistência aos desamparados" (wording of Constitutional Amendment 90/2015;
   *alimentação* was added in 2010, *moradia* in 2000, *transporte* in 2015). Single paragraph
   added by Amendment 114/2021: a basic family income.
2. **Art. 215-216** (culture) and **art. 225** (environment), same file.
3. **The infographic's own text** lists, per government, "desafios fiscais", "dependência do
   cenário internacional", "crises cambiais", "ausência de liberdades democráticas": fiscal
   position, external position and democratic freedoms are therefore in scope.

What the infographic already covers of art. 6: *trabalho* (unemployment, minimum wage) and
part of *saúde* (life expectancy). Everything else in the list below is not on the infographic.

## Dimensions and candidate indicators (primary candidate first; availability decides)

| Id | Dimension | Anchor | Candidate indicators (official or documented international series) |
|---|---|---|---|
| edu | Education | CF art. 6 | adult literacy rate (Census/PNAD); mean years of schooling (PNAD/Ipea); IDEB (INEP, from 2005); PISA scores (OECD, 2000-2022); public education spending as % of GDP |
| sau | Health | CF art. 6 | maternal mortality ratio; DTP3 vaccination coverage (WHO/UNICEF WUENIC); public health spending as % of GDP; infant mortality (already collected, shared with maternity/childhood) |
| seg | Security | CF art. 6 | homicide rate per 100,000 (Ministry of Health SIM/DATASUS; Ipea Atlas da Violência) |
| ali | Food | CF art. 6 | prevalence of undernourishment (FAO) |
| mor | Housing | CF art. 6 | household access to piped water, sewage, electricity (Census/PNAD); housing deficit (Fundação João Pinheiro) |
| tra | Transport | CF art. 6 | assessed; kept only if a national series with comparable method exists, otherwise reported as "no comparable series" |
| laz | Leisure | CF art. 6 | assessed; expected "no comparable series" |
| pre | Social security | CF art. 6 | share of 65+ receiving a pension or benefit (PNAD); social-security balance as % of GDP |
| mat | Maternity and childhood | CF art. 6 | infant mortality; births with 7+ prenatal visits (SINASC) |
| ass | Social assistance | CF art. 6 and sole paragraph | social-assistance spending as % of GDP; coverage of cash-transfer programmes (Bolsa Família, BPC) |
| tbl | Work (beyond the two rows shown) | CF art. 6 | informality rate; average real labour income (PNAD/PNADC) |
| cul | Culture | CF art. 215-216 | federal spending on the culture function as % of the budget; if no comparable official series exists, say so and stop |
| amb | Environment | CF art. 225 | Amazon deforestation, km² per year (INPE PRODES) |
| dem | Democratic freedoms | the infographic's own text | V-Dem electoral democracy index (v2x_polyarchy) |
| fis | Fiscal position | the infographic's own text | gross and net public debt as % of GDP; primary balance as % of GDP; real interest rate |
| ext | External position | the infographic's own text | exchange rate, international reserves, current account as % of GDP, external debt |

Excluded on principle (stated now): perception indices (for instance corruption-perception
rankings), because their method changes by design and they are not anchored in the sources above.

## Inclusion rule (written before collecting)

1. The source is an official statistical body or an international body with a documented method
   (IBGE, Ipea, INEP, Ministry of Health, BCB, INPE, FAO, WHO, UNICEF, UNESCO, OECD, World Bank, V-Dem).
2. National coverage, annual frequency (decennial is accepted only for Census-based access
   indicators) and at least 30 years of coverage, or a documented and measured overlap at each
   method break.
3. The primary comparison uses **one homogeneous series** that spans the widest window.
   Other vintages or sources are reported as sensitivity, never mixed into the primary line.
4. A dimension with no qualifying series is reported as "no comparable series". It is not
   dropped silently and it is not forced.

## Reporting rule (written before collecting)

1. Every collected indicator is reported for **every** government, in both directions: where
   the result favours a government and where it does not. No indicator is removed after its
   result is known.
2. Each indicator is shown over the infographic's printed windows **and** over the actual
   term of each government.
3. Each method break found in a series is listed (see `quebras.csv`) with: date, old and new
   method, the source's own stated reason, the measured effect in the overlap (or "no overlap"),
   whether the source presents it as an improvement, and which infographic cells cross it.
4. Alongside any spliced comparison, a comparison **inside a single method** is shown.
5. The text states what is omitted and how the numbers move; it does not state or imply who
   the omission was meant to benefit.

## Amendments

(none)
