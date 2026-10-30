# Daily brief — BudgetSorter (2026-10-30)

**Verdict: PARK.** Reversing the previous review's REVIVE.

## What I looked at

Full git history (10 commits), both statement scripts end to end, all four files in
`Recipt_Budget/`, the fixture that last session's doer committed, `requirements.txt`,
`.gitignore` and `.env.example`. Not a web project, so no browser check. I tried to actually
execute the pipeline — `pandas` isn't importable here and `python3 -m venv` fails because
`ensurepip` is missing on python3.14 — so instead I replayed the pipeline's arithmetic over
`sample_statement.csv` with stdlib `csv` to get real numbers rather than guesses.

## What I found

The previous review (2026-09-22) correctly identified the blocker as "this has never been
run," and set one task: commit a sample statement CSV so it could be. The doer did it
(`b58d7de`). **Nobody ran it.** Seven weeks, zero commits.

And the fixture it added proves the point loudly. Replaying the numbers:

- `Plot_csv.py:23` prints `Total Spent: £7129.69`. Real debit spend in that file is **£370.31**.
  It's summing signed amounts, so three £2500 salary rows swamp the result — it's reporting net
  cash flow under a "Total Spent" label.
- `csv_statement_analysis.py:44` has the mirror-image bug: `.abs()` everything, and the exclude
  filter at `:46` catches "transfer/friend/..." but not salary or top-ups. So the £2500 rows
  become *spending*. Monthly totals come out 2587.69 / 2628.08 / 2573.24 / 41.30 (December has
  one row), the regression fits slope −769.40, and `:103-104` prints **£34.07, −£735.33,
  −£1504.73** as predicted spending. The headline feature of this repo outputs negative money
  on the repo's own test data. The labels are off by one month on top of that (`:63-69`).

But the fixable bugs aren't the real finding. The real finding is **what this project is
competing with**. Its input is a Revolut CSV export, and the Revolut app already gives you
category breakdowns, merchant totals and monthly trend for free. `csv_statement_analysis.py`
and `Plot_csv.py` — 210 lines, the bulk of the "working" code — rebuild a feature that ships
with the data source. The last review's headline task was to add a `CATEGORIES` dict to make
the "sorter" real; that would be 45 minutes spent reproducing a free screen.

The part that *isn't* redundant is receipt line items — no bank tells you that you bought £12
of beer inside a £45 Tesco shop. That's `Recipt_Budget/`, and it's the half in the worst shape:
`parse_receipt_data` copied near-identically into `OCR_Parsing.py:45-107` and `trial.py:62-112`,
both appending to one `receipt_log.csv` under **different headers** (`:118` vs `:119`), with
`"VARIES"` written where the item price should go (`:125`) — so per-item price, the entire
point, is never recorded. `main.py:28` reads `data['ParsedResults_3']`, a key OCR.space has
never returned, so that extractor has never produced output. `img_crp.py` is an unrelated
Harris-corner experiment on an image that isn't in the repo.

Last thing worth noting: all five commits after the 2026-05-30 initial pair are automation.
The human contribution to this repo was one sitting, five months ago.

## What I'm proposing

Not a roadmap — five self-contained items that make the park honest and keep the salvageable
part salvageable. Quick win is the one that makes the decision durable: **there is no
`README.md` in this repo at all**, only automation-written `todo.md`/`reference.md`, which is
exactly how a park verdict gets re-litigated by the next review agent. Then: collapse
`Recipt_Budget/` to one parser with a committed offline OCR fixture (the salvage); drop the
module-level `google.generativeai` import at `:4`, which blocks the main script from starting
for a dead function asking for the retired `gemini-pro`; fix the two sign bugs; delete
`main.py` and `img_crp.py`.

`next_review` is set to 2026-11-09 per the routine, but a parked repo doesn't merit a full
review in 10 days — I'd demote BudgetSorter out of the daily rotation.
