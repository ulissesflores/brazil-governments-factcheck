# Reproducibility

The repository has two seals with different guarantees, so a reader knows exactly what can be redone alone and what depends on third-party material.

## Seal 1: reproducible derivation (any machine, no network)

What can be re-executed without the third-party files:

* the curated layer: `python -m govfc.curate` rebuilds `data/curated/*.csv` and `output/series.json` from the series already derived and sealed in `data/raw/`;
* the verdict of every infographic number: `python -m govfc.build_results` rebuilds `output/results.json`;
* the tests, which pin every published number and recompute IPCA and GDP straight from the raw JSON by independent code;
* the SHA-256 seal (`output/provenance.json`) and every acquisition chain (`manifest.jsonl`).

```bash
python3 run_all.py
```

The same seal covers phases 2 and 3: `python -m govfc.indice` (composite index), `govfc.terminal`
(terminal bundle), `govfc.mundo` (world comparison), `govfc.auditoria`, `govfc.literatura`
(literature layer, reshaped from the hashed tables of the collection `literatura-fase3`, never from a
new query) and the external-debt series of `externo-fase3`. `run_all.py` runs them in order; the page
`output/raio-x.html` is rendered by `scripts/build_page.py` from the sealed JSON and is informational
(not hashed).

## Seal 2: frozen evidence, not redistributed

Large third-party documents (PDF, ZIP, spreadsheets, news pages) are not stored here. Each is recorded in a `manifest.jsonl` with its URL, byte count and sha256. To refetch them and re-run the scripts that turn them into the sealed series:

```bash
python3 run_all.py --full
```

A live URL may serve a newer version. A mismatch means "the source changed or the copy was altered", never "proof of tampering"; the run reports it and does not hide it.

## The verdict rule (constants)

`code/govfc/verdict.py`: reproduces if the reproduced value rounds half up to the printed value at the printed precision; approximates if within **0.3 percentage points** (percentage rows) or **5 % relative** (any row); does not reproduce otherwise; not verified if no official series covers the printed window or year. The constants were fixed before the results were read and are pinned by `tests/test_verdict.py`.

## What cannot be re-run

* The original infographic image and the capture of the X post (frozen evidence).
* The pre-registration timestamp: it is the file modification time recorded in the hash chain, not a third-party date. The Zenodo deposit at the first release adds an external date.
* Any value a source revised after collection: the sealed snapshot keeps the value as collected; a later download is a new vintage, added as new rows.

## Known limitations

1. The primary specifications were fixed after an exploratory pass over the data; the verdicts are descriptive, not a pre-registered test.
2. A first version of the engine mixed sources inside one row (IBGE where it had the year, the World Bank where it did not). It was replaced by one homogeneous source per indicator; see `CHANGELOG.md`.
3. Some official series do not exist for the printed window (unemployment 1968-73, IPCA before 1980, PNAD in 1994).
