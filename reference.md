# Reference — BudgetSorter

_Last refreshed: 2026-10-30 — verdict: **PARK**_

## Purpose
Intended: sort personal spending into categories from two sources — Revolut CSV exports and
photographed receipts (OCR.space) — then summarise and forecast. Actual: two overlapping
statement-summary scripts and a four-file receipt-OCR experiment. **Nothing categorises
anything.** The "sorter" in BudgetSorter does not exist.

## Why PARK, not REVIVE
1. **The statement half is redundant with its own data source.** Input is a Revolut export,
   and the Revolut app already shows category breakdowns, merchant totals and monthly trend.
   `csv_statement_analysis.py` + `Plot_csv.py` (~210 lines) rebuild a free feature.
2. **The receipt half is the only novel part** — no bank gives you line items — and it is in
   the worst shape: one regex parser copied into two files, an extractor reading a key the API
   never returns, an unrelated OpenCV experiment, no input images, demo API key.
3. **No human has committed here since 2026-05-30.** All five later commits are automation.
4. The last review's unblocking task — commit a runnable fixture — landed 2026-09-22 and was
   never used. Run on it, the pipeline forecasts *negative* spending.

**What would have to be true to start:** a recurring need for item-level spend data Revolut
cannot answer, plus real receipt photos and an OCR path (paid OCR.space key or local Tesseract)
committed as fixtures. Until then: a solved problem bolted to an unstaffed hard one.

## Stack
Python 3 — pandas, numpy, matplotlib, scikit-learn, requests, python-dotenv, opencv-python,
google-generativeai. All unpinned (`requirements.txt`).

## Entry Points
```bash
pip install -r requirements.txt
python3 csv_statement_analysis.py     # summary + 3-month forecast + blocking plt.show()
python3 Plot_csv.py                   # plots only; no main(), runs on import
# BUDGETSORTER_STATEMENT_CSV=/path/to/export.csv overrides the committed sample
cd Recipt_Budget && python3 OCR_Parsing.py   # needs receipt .jpegs not present in the repo
```
Note: `pandas`/`sklearn` are not importable in this environment and `python3 -m venv` fails
(`ensurepip` missing on python3.14), so the code still cannot be executed here.

## Files
- `csv_statement_analysis.py` — load/filter, monthly+weekly breakdown, LinearRegression
  forecast, dead `run_ai_model()` Gemini helper at `:118-123`
- `Plot_csv.py` — plotting-only variant of the same analysis, entirely at module level
- `sample_statement.csv` — 15-row synthetic Revolut export (added 2026-09-22, never used)
- `Recipt_Budget/OCR_Parsing.py` — OCR.space upload → regex parse → `receipt_log.csv`;
  `trial.py` is a near-duplicate plus a response cache
- `Recipt_Budget/main.py` — OCR JSON extractor; reads a key OCR.space does not return.
  `img_crp.py` — unrelated Harris-corner experiment on a missing image
- No `README.md`.

## Confirmed Issues
Full detail with line numbers in `todo.md`. Headlines, replayed over `sample_statement.csv`:
`Plot_csv.py:23` prints "Total Spent: £7129.69" where real debit spend is £370.31;
`csv_statement_analysis.py:44` counts the three £2500 income rows as spend, so `:103-104`
prints £34.07, −£735.33, −£1504.73 as *predicted spending*; `:67-69` labels the forecast one
month early; `:17-31` group by merchant while calling it "category". In `Recipt_Budget/`,
`OCR_Parsing.py:118` and `trial.py:119` write different headers to one `receipt_log.csv`.
Every file here does I/O at import, so nothing is importable or testable.

## Security Notes
- `.env`, bank exports, receipt images and generated logs stay uncommitted; `.gitignore:29-30`
  ignores `*.csv` with a narrow negation for `sample_statement.csv` only. Keep it narrow.
- `Recipt_Budget/OCR_Parsing.py:11` and `trial.py:11` fall back to the OCR.space `"helloworld"`
  demo key when `OCR_SPACE_API_KEY` is unset.
