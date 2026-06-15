# TODOs

1. Add a headless output mode for `Plot_csv.py:46-52`, `Plot_csv.py:63-69`, and `Plot_csv.py:76-82` so cron or SSH sessions can save charts instead of blocking on `plt.show()`.
2. Move the receipt input/output configuration out of constants in `Recipt_Budget/OCR_Parsing.py:12-15` so receipt image paths and `receipt_log.csv` are not fixed in code.
3. Validate and, if needed, correct the OCR JSON schema assumption in `Recipt_Budget/main.py:28` and the sample file path in `Recipt_Budget/main.py:43` before relying on that parser for new OCR exports.
4. Document or bundle the expected statement CSV input so the default `Revolut_Sep_to_Jan.csv` path resolves without requiring `BUDGETSORTER_STATEMENT_CSV`.
