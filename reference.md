# Reference — BudgetSorter

_Last refreshed: 2026-05-29_

## Purpose
Financial data analysis tool for Revolut bank statements. Categorises transactions, calculates monthly/weekly spending trends, predicts next 3 months of spending with linear regression, and parses physical receipts via OCR.space API.

## Stack
- Python 3
- pandas, numpy, matplotlib, scikit-learn (`csv_statement_analysis.py`, `Plot_csv.py`)
- google-generativeai / Gemini (`csv_statement_analysis.py` — AI commentary)
- python-dotenv (API key loaded from `.env`)
- requests (OCR.space HTTP calls in `Recipt_Budget/OCR_Parsing.py`)

## Entry Points
```bash
# Main analysis + predictions (requires google-generativeai installed)
python3 csv_statement_analysis.py

# Plot-only view (pandas + matplotlib, no AI)
python3 Plot_csv.py

# Receipt OCR pipeline (requires OCR.space API key)
cd Recipt_Budget && python3 OCR_Parsing.py
```

## Key Files
| File | Role |
|------|------|
| `csv_statement_analysis.py` | Core analysis — transaction filtering, monthly/weekly breakdown, linear regression predictions, Gemini AI call |
| `Plot_csv.py` | Standalone plotting script — monthly/weekly/category trend charts |
| `Revolut_Sep_to_Jan.csv` | Real bank statement data (301 rows, Sep 2024 – Feb 2025) |
| `Sorted_Revolut_Sep_to_Jan.csv` | Pre-processed/sorted version of the same data |
| `Recipt_Budget/OCR_Parsing.py` | Sends receipt images to OCR.space API, parses results, logs to CSV |
| `Recipt_Budget/main.py` | Parses saved OCR JSON responses from `OCR_parse/` |
| `.env` | Contains `GeminiAPI` key — must not be committed |

## Run Status (2026-05-29)
Core analysis (pandas + sklearn) ran successfully — CSV loaded (301 rows), predictions generated. `google.generativeai` not installed on this machine so the Gemini call at the bottom of `csv_statement_analysis.py` would fail. `plt.show()` skipped (no display). Syntax check passed on all files.

## Security Notes
- No `.gitignore` — `Revolut_Sep_to_Jan.csv` (real bank data) and `.env` (API key) are unprotected from accidental git commits.
- `OCR_Parsing.py:8` has a hardcoded placeholder key `'helloworld'`; the real key should come from `.env`.
