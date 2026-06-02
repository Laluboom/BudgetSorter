# Reference — BudgetSorter

_Last refreshed: 2026-06-02_

## Purpose
Financial data analysis tool for Revolut bank statements. It summarizes transaction history, predicts the next three months of spending with linear regression, and includes a separate receipt OCR workflow backed by OCR.space.

## Stack
- Python 3
- pandas, numpy, matplotlib, scikit-learn (`csv_statement_analysis.py`, `Plot_csv.py`)
- google-generativeai / Gemini (`csv_statement_analysis.py`)
- python-dotenv (`csv_statement_analysis.py`, `Recipt_Budget/OCR_Parsing.py`)
- requests (`Recipt_Budget/OCR_Parsing.py`)

## Entry Points
```bash
python3 csv_statement_analysis.py
python3 Plot_csv.py
cd Recipt_Budget && python3 OCR_Parsing.py
```

## Confirmed Files
- `csv_statement_analysis.py`: core statement analysis, prediction output, optional Gemini helper
- `Plot_csv.py`: plotting-only statement analysis
- `Recipt_Budget/OCR_Parsing.py`: OCR.space upload and receipt CSV logging
- `Recipt_Budget/main.py`: OCR JSON text extraction helper
- `last_run.json`: latest inspection status
- `todo.md`: grounded next tasks

## Run Status (2026-06-02)
The hard-coded Gemini smoke test was removed from `csv_statement_analysis.py`, so running the analysis script no longer triggers an API call just because the file executes. `python3 -m py_compile` passed for all inspected Python sources. Remote sync could not be verified: `git pull --ff-only` failed against the configured SSH remote because the local SSH configuration/permissions prevented repository access.

## Confirmed Issues
- `csv_statement_analysis.py:9-10` and `Plot_csv.py:5` still depend on a hard-coded CSV filename and current working directory.
- `csv_statement_analysis.py:9-82` still executes analysis work at import time, which makes reuse and testing awkward.
- `Plot_csv.py:36`, `Plot_csv.py:53`, and `Plot_csv.py:66` still require a graphical display because they call `plt.show()` directly.
- `Recipt_Budget/OCR_Parsing.py:12-15` still hard-codes both the output CSV path and the input receipt image list.
- `Recipt_Budget/main.py:28` expects a `ParsedResults_3` key, which is non-standard for OCR.space responses and was not validated in this run.

## Security Notes
- `.env`, bank exports, receipt images, OCR output, and generated logs must remain uncommitted.
- `Recipt_Budget/OCR_Parsing.py:11` falls back to the OCR.space demo key when `OCR_SPACE_API_KEY` is unset.
