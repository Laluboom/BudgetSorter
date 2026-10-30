# BudgetSorter

Intended to sort personal spending into categories from two sources — Revolut CSV
exports and photographed receipts (OCR.space) — then summarise and forecast.
Despite the name, nothing here actually categorises anything yet.

Two halves, uneven value:
- **Statement analysis** (`csv_statement_analysis.py`, `Plot_csv.py`) summarises a
  Revolut export — monthly/weekly totals, a forecast, a plot. Revolut's own app
  already shows category and merchant breakdowns, so this duplicates a feature the
  data source gives you for free.
- **Receipt line-item extraction** (`Recipt_Budget/`) parses OCR'd receipts into
  per-item spend. No bank statement gives you that — this is the only novel part of
  the project, and the only piece worth salvaging if this is ever picked back up.

**Status: parked as of 2026-10-30.** See `reference.md` for the full verdict and
`todo.md` for the open (non-roadmap) cleanup items.

## Running it

```bash
pip install -r requirements.txt
python3 csv_statement_analysis.py
```

Runs against the committed `sample_statement.csv` by default; set
`BUDGETSORTER_STATEMENT_CSV=/path/to/export.csv` to point it at a real export instead.
