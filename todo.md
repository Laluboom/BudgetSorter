# TODOs

1. Refactor `csv_statement_analysis.py:9-82` into a `main()` flow so importing the module does not immediately read files, fit a model, print reports, and open matplotlib windows.
2. Replace the hard-coded statement CSV paths in `csv_statement_analysis.py:10` and `Plot_csv.py:5` with a shared configurable input path.
3. Add a headless output mode for `Plot_csv.py:30-36`, `Plot_csv.py:47-53`, and `Plot_csv.py:60-66` so cron or SSH sessions can save charts instead of blocking on `plt.show()`.
4. Move the receipt input/output configuration out of constants in `Recipt_Budget/OCR_Parsing.py:12-15` so receipt image paths and `receipt_log.csv` are not fixed in code.
5. Validate and, if needed, correct the OCR JSON schema assumption in `Recipt_Budget/main.py:28` and the sample file path in `Recipt_Budget/main.py:43` before relying on that parser for new OCR exports.
