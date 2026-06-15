# Reference — BudgetSorter

_Last refreshed: 2026-06-15_

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

## Run Status (2026-06-15)
`csv_statement_analysis.py` and `Plot_csv.py` now resolve their default statement CSV relative to the project folder and share the same `BUDGETSORTER_STATEMENT_CSV` override, so both scripts no longer depend on the current working directory or a duplicated hard-coded filename string. Verification passed with `python3 -m py_compile Vellai/BudgetSorter/csv_statement_analysis.py Vellai/BudgetSorter/Plot_csv.py`. A direct file check also confirmed that `Revolut_Sep_to_Jan.csv` is not currently present in the project root, so local runs still need either that file or an explicit `BUDGETSORTER_STATEMENT_CSV` value. This content-only run did not execute any git commands.

## Confirmed Issues
- `Plot_csv.py:46-52`, `Plot_csv.py:63-69`, and `Plot_csv.py:76-82` still require a graphical display because they call `plt.show()` directly.
- `Recipt_Budget/OCR_Parsing.py:12-15` still hard-code both the output CSV path and the input receipt image list.
- `Recipt_Budget/main.py:28` expects a `ParsedResults_3` key, which is non-standard for OCR.space responses and was not validated in this run.
- `Revolut_Sep_to_Jan.csv` is not present in the project root, so the new default statement path only works after the file is supplied or `BUDGETSORTER_STATEMENT_CSV` is set.

## Security Notes
- `.env`, bank exports, receipt images, OCR output, and generated logs must remain uncommitted.
- `Recipt_Budget/OCR_Parsing.py:11` falls back to the OCR.space demo key when `OCR_SPACE_API_KEY` is unset.
