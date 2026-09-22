# Reference — BudgetSorter

_Last refreshed: 2026-09-22 — verdict: **REVIVE**_

## Purpose
Intended: sort personal spending into categories from two sources — Revolut CSV statement exports
and photographed receipts (OCR.space) — and summarise/forecast from there.

Actual, as of today: two overlapping statement-summary scripts and a separate receipt-OCR
experiment. **Nothing categorises anything.** The "sorter" in BudgetSorter does not exist yet.
That gap, not code quality, is the reason this repo has stalled.

## Stack
Python 3 — pandas, numpy, matplotlib, scikit-learn, requests, python-dotenv, opencv-python,
google-generativeai. All unpinned (`requirements.txt`).

## Entry Points
```bash
pip install -r requirements.txt
export BUDGETSORTER_STATEMENT_CSV=/path/to/revolut_export.csv   # no default file is committed
python3 csv_statement_analysis.py     # summary + 3-month linear forecast + blocking plot
python3 Plot_csv.py                   # plots only; no main(), runs on import
cd Recipt_Budget && python3 OCR_Parsing.py   # needs receipt .jpegs that are not in the repo
```

## Files
- `csv_statement_analysis.py` — statement load/filter, monthly+weekly breakdown, LinearRegression
  forecast, unused `run_ai_model()` Gemini helper at `:118-123`
- `Plot_csv.py` — plotting-only variant of the same analysis, entirely at module level
- `Recipt_Budget/OCR_Parsing.py` — OCR.space upload → regex parse → `receipt_log.csv`
- `Recipt_Budget/trial.py` — near-duplicate of the above with an API-response cache
- `Recipt_Budget/main.py` — OCR JSON text extractor; reads a key OCR.space does not return
- `Recipt_Budget/img_crp.py` — unrelated Harris-corner experiment on a missing image

## Current State (verified 2026-09-22)
**The project has never been run.** The working tree is 13 files and nothing else: no statement
CSV, no receipt images, no venv, no cached OCR JSON, nothing ignored-but-present
(`git status --ignored` is empty). `pandas` and `sklearn` are not importable in this environment.
Commits of 2026-05-30, -06-08 and -06-15 were automated sessions that refactored input paths and
verified only with `py_compile` — real refactors, but on code no one had executed, against data
that does not exist. That is the pattern to break; see `todo.md:1`.

## Confirmed Issues
- `Plot_csv.py:23` sums `Amount` unsigned and calls it "Total Spent" — that is net cash flow, not
  spend. `csv_statement_analysis.py:44` takes `.abs()` instead, counting income as spending; the
  keyword filter at `:46` excludes transfers but not salary, top-ups, refunds or cashback.
- `csv_statement_analysis.py:67-69` labels the forecast from the **last observed** month while
  `:63-65` predicts the three months after it — every value at `:103-104` and `:82-89` is off by
  one month. `freq="M"` there is also deprecated in pandas ≥2.2 (`"ME"`), and `requirements.txt:5`
  is unpinned.
- `csv_statement_analysis.py:17-31` group by `Description` (merchant) while naming it "category";
  `.unstack()` therefore produces one column per merchant.
- `Recipt_Budget/OCR_Parsing.py:118` and `Recipt_Budget/trial.py:119` write **different headers**
  to the same `receipt_log.csv`; `OCR_Parsing.py:125` writes `"VARIES"` in place of item price.
- `Recipt_Budget/main.py:28` reads `data['ParsedResults_3']`; OCR.space returns `ParsedResults`.
- `Plot_csv.py:18`, `OCR_Parsing.py:133`, `trial.py:128`, `img_crp.py:3` all do I/O at import —
  nothing here is importable or testable.
- `Plot_csv.py:46-52`, `:63-69`, `:76-82` call `plt.show()`, so any headless run blocks.
- `.gitignore:31` ignores `*.csv` with no negation, so no sample input can be committed.

## Security Notes
- `.env`, bank exports, receipt images and generated logs stay uncommitted — `.gitignore` is
  correct on this and should keep any fixture negation narrow (one named file, not `*.csv`).
- `Recipt_Budget/OCR_Parsing.py:11` and `trial.py:11` fall back to the OCR.space `"helloworld"`
  demo key when `OCR_SPACE_API_KEY` is unset.
