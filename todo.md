# TODOs — BudgetSorter

_Verdict: **PARK**. See `reference.md` for the reasoning._

The 2026-09-22 review said REVIVE and set one unblocking task: commit a sample statement CSV
so the project could be run for the first time. The doer landed it (`sample_statement.csv`,
commit `b58d7de`). **Seven weeks later nobody has run it.** Running the analysis on that
fixture prints a *negative* spending forecast (−£735, −£1505) and `Plot_csv.py` reports
"Total Spent: £7129.69" against real spend of £370.31. The blocker was never the missing
fixture; it was that no one needs this.

And there is a reason no one needs it: the statement half of this repo reproduces what
Revolut's own app already shows — category and merchant breakdowns, monthly trend — from a
Revolut export. The receipt-OCR half is the only part that does something no bank gives you.

So nothing below is a roadmap. These are the small, self-contained things that make the park
state honest and keep the one salvageable asset salvageable. Do them or don't; just don't
build the category dictionary the last review asked for until the "what would have to be
true" list in `reference.md` is actually true.

---

### 1. `[DONE 2026-10-30]` `[DOCS]` There is no README — add one, carrying the park verdict

The repo has `reference.md`, `todo.md` and `cron_brief_latest.md`, all written by automation,
and **no `README.md` at all**. Anyone landing here (including the next review agent, or
future-you in 2027) sees a tree of Python files named `csv_statement_analysis.py` and
`Recipt_Budget/` and has to reverse-engineer intent from source.

Write ~15 lines: what this was meant to be, that the statement half duplicates Revolut's
in-app analytics, that the receipt line-item extraction is the only novel part, and that the
repo is parked as of 2026-10-30. One sentence on how to run it (`sample_statement.csv` is
committed; `BUDGETSORTER_STATEMENT_CSV` overrides).

**Why it matters:** a park decision that lives only in an automation-written `todo.md` gets
re-litigated by the next automated review. In a README it survives.

---

### 2. `[CHORE]` Collapse `Recipt_Budget/` to one working parser — this is the salvage

`parse_receipt_data` exists near-identically twice: `Recipt_Budget/OCR_Parsing.py:45-107` and
`Recipt_Budget/trial.py:62-112` — same two regexes, same `ignore_keywords` list. Both append
to the same `receipt_log.csv` with **different headers**: `OCR_Parsing.py:118` writes
`['Date','Item Name','Item Price','Receipt Total','Total Items Count']`, `trial.py:119` writes
`['Date','Items List','Total Items','Grand Total']`. Whichever runs first fixes the header and
the other's rows then mean something else entirely. `OCR_Parsing.py:125` also writes the
literal string `"VARIES"` into the `Item Price` column, so per-item prices — the whole point
of reading receipts — are never recorded.

One module, one header, one row per item (the commented-out loop at `OCR_Parsing.py:128-129`
is already the right shape), parser behind a `main()` guard. Keep `trial.py`'s JSON cache
(`trial.py:20-60`) — it is the only thing here that lets you iterate on the regexes without
burning OCR.space calls — and commit one real cached response as a fixture so the parser is
testable offline.

**Why it matters:** if any part of BudgetSorter gets picked up again it is this one. Right now
it is unpickupable: four files, two of them duplicates, no input data.

---

### 3. `[BUG]` `csv_statement_analysis.py:4` imports a retired Google SDK for a function that cannot work

`import google.generativeai as genai` sits at module level, so the main analysis script cannot
start without it — but its only consumer is `run_ai_model()` at `:118-123`, which nothing
calls, and which asks for model `"gemini-pro"`. That model name is long retired and
`google-generativeai` has been superseded by the `google-genai` SDK, so this code path is dead
twice over. `requirements.txt:1` pulls the dep in for every install.

Delete `run_ai_model()` and the import, or (if the Gemini idea is worth keeping as a note) move
the import inside the function and say in a comment what it was for. Drop
`google-generativeai` from `requirements.txt`.

---

### 4. `[BUG]` The forecast prints negative spending on the repo's own committed fixture

Verified by replaying the pipeline's arithmetic over `sample_statement.csv`:

- `csv_statement_analysis.py:44` does `df["Amount"] = df["Amount"].abs()`, and the keyword
  filter at `:46` excludes "transfer/friend/reimbursement/split/payback" but **not** salary or
  top-ups — so the three £2500.00 `TOPUP`/Salary rows are counted as spending. Monthly totals
  become 2587.69 / 2628.08 / 2573.24 / 41.30 (December has one row), the regression at
  `:60-61` fits slope −769.40, and `:103-104` prints **£34.07, −£735.33, −£1504.73**.
- `Plot_csv.py:23` has the opposite bug — a plain `.sum()` labelled "Total Spent" — printing
  **£7129.69** where actual debit spend is **£370.31**.
- Separately, `:63-65` predicts positional indices `n, n+1, n+2` while `:67-69` labels them
  with `pd.date_range(start=monthly_totals.index[-1].to_timestamp(), periods=3, freq="M")`,
  which month-ends from the **last observed** month: labels `[2024-12, 2025-01, 2025-02]`
  against values for `[2025-01, 2025-02, 2025-03]`. `freq="M"` is also deprecated since pandas
  2.2 (`"ME"`) and `requirements.txt:5` is unpinned, so a fresh install warns or fails here.

Fix: select debits explicitly (`df[df["Amount"] < 0]`), negate once for display, and derive
labels from the period index (`monthly_totals.index[-1] + 1` etc.), not a timestamp range.

**Why it matters:** these are the only two user-facing numbers the project produces, and both
are wrong by more than an order of magnitude. It is also the cheapest possible demonstration
that nobody has executed this code.

---

### 5. `[CHORE]` Delete the two files in `Recipt_Budget/` that have never worked

- `Recipt_Budget/main.py:28` reads `data['ParsedResults_3'][0]`. OCR.space returns
  `ParsedResults`. There is no version of this API that returns that key, so this extractor has
  never produced output — it always falls through to the structure-error print at `:38-40`. It
  also runs on import (`:43-46`) against `OCR_parse/Tesco_OCR.json`, a path not in the repo.
- `Recipt_Budget/img_crp.py` is an unrelated Harris-corner experiment that reads
  `./test/Sainsbury.jpeg` at `:3` (absent, so `cv.imread` returns `None` and `:4` raises), and
  at `:26-27` writes the same thresholded array to two different filenames while discarding the
  `img` it just annotated at `:23-24`.

Remove both; drop `opencv-python` from `requirements.txt:4` with `img_crp.py`. If the corner
detection was going toward receipt deskewing, that is a sentence in the README (task 1), not
27 lines of dead code.
