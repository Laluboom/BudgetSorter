# BudgetSorter — review 2026-09-22

**Verdict: REVIVE** (conditionally — see the last paragraph).

I read all six Python files, the git history, `.gitignore`, `requirements.txt`, and the tracking
files left by the previous automated runs. No browser check — this is a CLI/pandas project.

The tier assumption is wrong for this repo. It is not templated scaffolding: there are ~670 lines
of real Python doing real work across two areas — Revolut statement analysis with a linear-regression
forecast, and a receipt OCR pipeline against OCR.space. The problem is different and more specific.

**Two things define the current state.** First, the feature the project is named after does not
exist. Nothing in this codebase categorises anything. `csv_statement_analysis.py:28-31` is called
`average_spending_per_category` but groups by `Description` — the raw merchant string from the
export — so the monthly `.unstack()` at `:17-18` produces one column per merchant rather than a
budget breakdown. Second, **the project has never been run.** The working tree is 13 files and
nothing else: no statement CSV, no receipt images, no venv, and `git status --ignored` comes back
empty, so there isn't even a local untracked copy. `.gitignore:31` ignores `*.csv` with no
negation, which means a sample input *cannot* be committed even if someone wanted to.

That second point explains the history. The commits of 2026-05-30, 06-08 and 06-15 were automated
sessions that moved input paths around and verified with `py_compile` — legitimate refactors, but
on code nobody had executed against data that does not exist. Predictably, the bugs that only
show up on real rows survived untouched. The clearest is sign handling: `Plot_csv.py:23` sums
`Amount` unsigned and labels it "Total Spent" (that is net cash flow — near zero once a salary row
is present), while `csv_statement_analysis.py:44` takes `.abs()` and counts income *as* spending.
Two scripts, the same column, two different wrong answers. The forecast is also mislabelled:
`:63-65` predicts the three months after the data ends, `:67-69` labels them starting from the last
observed month, so every printed and plotted point is off by one. And in `Recipt_Budget/`,
`OCR_Parsing.py:118` and `trial.py:119` write different headers into the same `receipt_log.csv`
from a duplicated copy of the same parser.

**What I'm proposing** is ordered to break that pattern rather than continue it. The quick win is
a `.gitignore` negation plus a ~15-row synthetic Revolut CSV with deliberately mixed-sign rows —
15 minutes, and it is the blocker under everything else, because until it lands no change here can
be verified by anything stronger than `py_compile`. Then the one session that actually revives this:
a substring→category map applied in `load_statement_data()`, regrouping on `Category`, and printing
what fraction of spend fell through to `Uncategorised`. That number is the project's real metric.
The two sign/forecast bugs and the `Recipt_Budget/` consolidation follow, and each becomes testable
once the fixture exists.

I say REVIVE because the idea is concrete, personally useful, and about 70% plumbed — but I'd hold
it to the condition. If that one session hasn't happened by the next review, the honest call is
RETIRE: a fourth cycle of refactoring code that has never executed would just be a slower way of
reaching the same answer.

Next review: 2026-10-02.
