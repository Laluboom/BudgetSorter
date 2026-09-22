# TODOs — BudgetSorter

_Verdict: **REVIVE**. Ranked best-first. See `reference.md` for why._

The through-line: this repo has ~670 lines of real Python and **has never been run**. There is
no input data anywhere in the tree, no venv, and `.gitignore:31` (`*.csv`) makes it impossible to
commit even a test fixture. Three prior automated sessions (2026-05-30, -06-08, -06-15) refactored
file paths on code nobody had executed. Every task below is ordered to end that.

---

### 1. `[QUICK WIN ~15min]` Make the repo runnable for the first time — commit a synthetic statement CSV

`.gitignore:31` ignores `*.csv` wholesale, so the sample input this project needs can never be
tracked. Add a negation (e.g. `!sample_statement.csv`) directly under that rule, then commit a
~15-row hand-written CSV with the exact Revolut header both scripts parse:
`Type, Product, Started Date, Completed Date, Description, Amount, Fee, Currency, State, Balance`
(required by `csv_statement_analysis.py:43`, `Plot_csv.py:18-21`, `Plot_csv.py:27`, `Plot_csv.py:37`).

Include deliberately mixed signs: negative rows for spend, at least one positive salary/top-up row,
and one "Transfer to friend" row — those three cases are what tasks 3 and 2 depend on. Point
`DEFAULT_STATEMENT_CSV` (`csv_statement_analysis.py:11`, `Plot_csv.py:7`) at it.

**Why it matters:** this is the single blocker under every other task. Until it lands, no change to
this repo can be verified by anything stronger than `py_compile` — which is exactly how it drifted.

---

### 2. `[DESIGN]` Add the actual sorting — the thing the repo is named after

There is no categorisation anywhere in this codebase. `csv_statement_analysis.py:28-31` is called
`average_spending_per_category` but groups by `Description`, which in a Revolut export is the raw
merchant string ("Tesco", "Uber", "TFL Travel Charge"). Same for the `Month`/`Week` breakdowns at
`csv_statement_analysis.py:17-18` and `:24-25` — `.unstack()` on a merchant column yields one
column per distinct merchant, i.e. a table with hundreds of columns and one number in each.

Smallest end-to-end version: a `CATEGORIES` dict of substring → category ("tesco|sainsbury|lidl"
→ Groceries, "tfl|uber|trainline" → Transport, …), a `categorise(description)` helper defaulting to
`"Uncategorised"`, and a `Category` column applied in `load_statement_data()`
(`csv_statement_analysis.py:41-49`). Then regroup the three functions above on `Category`.

**Done means:** running against the task-1 fixture prints a monthly table of ~6 category rows, and
reports what fraction of spend landed in `Uncategorised`. That number is the project's real metric.

---

### 3. `[BUG]` The two statement scripts disagree about what a negative Amount means

`csv_statement_analysis.py:44` does `df["Amount"] = df["Amount"].abs()`; `Plot_csv.py:23` does a
plain `.sum()`. On the same file these produce two different wrong answers:

- `Plot_csv.py:23` prints net cash flow (spend minus income) and labels it "Total Spent" — with a
  salary row present this is near zero or positive.
- `csv_statement_analysis.py:44` flips income to positive and counts it *as spending*. The keyword
  filter at `:46` catches "transfer/friend/reimbursement/split/payback" but not salary, top-up,
  refund, or cashback — so income inflates every total and drags the regression trend in task 4.

Fix: keep the sign, select debits explicitly (`df[df["Amount"] < 0]`), negate once for display.
`Plot_csv.py:37` (`Fee`) should stay a separate line — fees are real spend but not a category.

---

### 4. `[BUG]` Forecast months are labelled one month early

`csv_statement_analysis.py:63-65` predicts for positional indices `n, n+1, n+2` — the three months
*after* the data ends. But `csv_statement_analysis.py:67-69` builds the labels with
`pd.date_range(start=monthly_totals.index[-1].to_timestamp(), periods=3, freq="M")`, which starts
at the **last observed** month. With data ending 2026-01 you get labels `[2026-01, 2026-02, 2026-03]`
against values for `[2026-02, 2026-03, 2026-04]`: every printed line (`:103-104`) and every plotted
point (`:82-89`) is off by one, and the first "prediction" overwrites a month you already have
actuals for.

Fix: derive labels from the period index, not a timestamp range —
`monthly_totals.index[-1] + [1, 2, 3]`. Separately, `freq="M"` is deprecated as of pandas 2.2
(use `"ME"`); `requirements.txt:5` is unpinned, so a fresh install already warns and pandas 3 breaks.

---

### 5. `[CHORE]` Collapse `Recipt_Budget/` — two copies of one parser, writing conflicting rows to one file

`parse_receipt_data` exists near-identically in `Recipt_Budget/OCR_Parsing.py:45-107` and
`Recipt_Budget/trial.py:62-112` (same regexes, same ignore list). Both append to the same
`receipt_log.csv`, but with **different headers**: `OCR_Parsing.py:118` writes
`['Date','Item Name','Item Price','Receipt Total','Total Items Count']` while `trial.py:119` writes
`['Date','Items List','Total Items','Grand Total']`. Whichever runs first sets the header; the other
then appends rows whose columns mean something else. `OCR_Parsing.py:125` also writes the literal
string `"VARIES"` into the `Item Price` column, so the per-item price is never actually recorded.

Keep one module with the parser behind a `main()` guard (all four files run on import today:
`OCR_Parsing.py:133`, `trial.py:128`, `Plot_csv.py:18`, `img_crp.py:3`). While here:
`Recipt_Budget/main.py:28` reads `data['ParsedResults_3']`, but OCR.space returns `ParsedResults` —
that helper cannot ever have worked. `img_crp.py` is an unrelated Harris-corner experiment reading a
file that does not exist; delete it or move it out.
