# Changelog

Format: Keep a Changelog; versioning: SemVer. 1.0.0 is the first release and the one that mints the DOI (concept DOI added at the final tag).

## [Unreleased]

## [1.0.1] - 2026-10-28

Concept DOI 10.5281/zenodo.23604103 (unchanged); this release mints a new version DOI that supersedes 1.0.0, which archives the text with the external-debt error corrected below.

### Added
* **Literature round 11 (amendment 12, 2026-10-25).** Four institutional episodes (central bank independence, fiscal rules as a class, press freedom, judicial independence) under the same sealed protocol: 54 queries, 7,487 distinct works, 43 included (1, 4, 1 and 0 for the new episodes). The editor's hypothesis that central bank autonomy and spending limits "keep things from getting worse" is recorded in the amendment and is neither asserted nor tested here: only included studies speak.
* **Press and expression freedom (V-Dem v2x_freexp_altinf, amendment 13) as a CONTEXT series in the terminal**, with the published uncertainty bounds, derived from the already-sealed v16 file. It does not score in the index: it was chosen after the index was published, which is what the pre-registration forbids for a scoring item.
* **Figure `areas`:** index area scores at the opening and closing of each term, in five languages, read from `output/indice.json`.
* **The texts of the 13 dated amendments and of the phase-2 pre-registration are now redistributed in `data/raw/preregistro/`** (they were hash-only in 1.0.0; the hashes in `manifest.jsonl` are unchanged, so every text can be checked against the seal of 2026-10-23).

### Fixed
* **Correction (2026-10-24).** The external debt layer, the page and section 15 of the methodology stated that the Central Bank had no official 2026 value of net external debt under any concept and that the October 2026 headline ("Brazil is a net debtor again") computed "gross debt minus reserves". Both statements were wrong. The level series SGS 3685 (gross restricted debt minus reserves, Brazilian credits abroad and commercial banks' assets abroad: column M of Table 31) is still published, matches Table 31 on every overlapping quarter, and reads +US$ 5.08 billion in 2026-06, the first positive value since 2007-09; the headline quoted that official number, and its "US$ 402 billion of reserves" is the set of assets the Central Bank subtracts, not cash reserves (US$ 367.6 billion). Added the series to the collection (`externo-fase3`, chain line 23), the indicator `divext_liquida` to the terminal, four tokens to the methodology in five languages and the tests that pin the values. December 2025, published as an estimate of -17.2 in the January note, is -8.7 in the series.

## [1.0.0] - 2026-10-23

Concept DOI 10.5281/zenodo.23604103 (Zenodo; the rc1 release minted the deposit, the final tag carries this DOI in the files).

### Added
* Verdict rule applied to the 57 numbers printed on the infographic (`code/govfc/verdict.py`, `build_results.py`).
* Acquisition hash chain per folder (`manifest.jsonl`) with `verify`, `--allow-missing`, `restore`; repository seal `chain_hash`.
* Curated layer: observations with vintage on every row, indicator catalogue, method-break catalogue, terms of office.
* Redone infographic as code in five languages with a fit check in the real font and a bidi rule for Hebrew.
* Monetary block: aggregates as a ratio to GDP by regime, seigniorage and inflation tax (reproduces Table 1 of Cysne and Coimbra-Lisboa 2004).
* Pre-registration of the omitted dimensions (`data/raw/preregistro/PREREGISTRATION.md`).
* Documentation in pt-BR, English, Spanish, Italian and Hebrew rendered from one source with numbers from the results.
* Phase 2: composite index of living conditions (`code/govfc/indice.py`, `output/indice.json`), sealed pre-registration (`PREREGISTRATION-FASE-2.md`), three doors, frozen goalposts 1995-2024, equal weights with the effective-importance tuning declared, published scenarios and weight draws; monthly index and yearly candles (amendments 04 to 06).
* Terminal and page (`scripts/page/raiox.html`, `scripts/build_page.py`): one homogeneous base per cell, yearly candles on rates, per-term grid "start -> end", reading by term in three layers, world comparison on one source per indicator (amendment 01), audit of every series (`output/auditoria.json`).
* Literature layer (`code/govfc/literatura.py`, `output/literatura.json`, collection `literatura-fase3`): protocol sealed before searching (amendments 07 to 10), four published rounds, every returned work listed with its reason for exclusion.
* External debt and the cost of public debt (collection `externo-fase3`): the Central Bank's two concepts of gross external debt, the discontinued net-debt ratios as published, nominal interest and nominal result; world comparison on the World Bank's IDS.
* Amendment-03 collections on the page: tax burden by base of incidence, net profit of five state-owned companies by accounting basis, parliamentary amendments paid by type (Portal da Transparência) and tax and bureaucracy acts read on planalto.gov.br.
* Method-break catalogue: the 2020 emergency education rules (Lei 14.040/2020) behind the fall of the retention rate.
* Amendment 11: the five index items that stop in 2014-2015 stay as they are (no chaining without overlap).

### Changed
* **Correction.** The first engine used IBGE where it had the printed year and the World Bank where it did not, mixing methods in one row. It now uses one homogeneous source per indicator and keeps the others as sensitivity. Effect: the two exact reproductions moved from life expectancy (2021, 2023) to the Gini (2014, 2018).
* **Correction.** The inflation row of the Temer term had been described as reproducing. Under the fixed rule it does not (IPCA 2016-18 gives 4.33 against 3.4 printed); it only approximates with the window shifted to 2017-18.
* The hash-chain rule: a file re-downloaded under the same path keeps its old line as history; only the last line must match the disk.
