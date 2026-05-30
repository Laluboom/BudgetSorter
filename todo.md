# TODOs

1. **Keep `.gitignore` current** — `.env`, real bank CSV exports, receipt images, OCR JSON output, and generated logs are ignored. Revisit this whenever new export folders or generated artifacts are added.

2. **Move the top-level `run_ai_model()` call in `csv_statement_analysis.py:84`** — `run_ai_model("Write what comes after C")` fires on every execution of the script, burning API quota. Wrap it in a `if __name__ == "__main__":` guard or remove the test call entirely.

3. **Improve OCR configuration** — `Recipt_Budget/OCR_Parsing.py` and `Recipt_Budget/trial.py` now read `OCR_SPACE_API_KEY` from `.env`, falling back to OCR.space's demo key. Next step: centralize file paths so receipt images and OCR caches are configurable instead of hard-coded.

---

## Future Ideas

4. **Auto-categorise transactions with a text classifier** — the `Description` field has raw merchant names (e.g. "J D Wetherspoon", "Uber", "Viva Falafel Wembley"). A small scikit-learn text classifier (TF-IDF + LogisticRegression, already a dependency) could map these into spending categories like Food, Transport, Entertainment, Subscriptions. You'd hand-label ~30–50 transactions to seed it, then let it predict the rest. Would make the monthly/weekly breakdowns far more meaningful than grouping by raw merchant name.

5. **Build a Streamlit dashboard** — currently everything runs as print-to-console scripts. A Streamlit app (same stack as AI_Researcher) would let you interactively filter by date range, category, or transaction type and see charts update live. Open question: do you want a local-only tool or something you could share/host?

6. **Anomaly / unusual spend detection** — use scikit-learn's `IsolationForest` or a simple Z-score threshold to flag transactions that are unusually large for a given merchant or category. 301 rows is enough to get useful signals. Could output a weekly "anything suspicious?" list.

7. **Match receipt OCR items to bank transactions** — the `Recipt_Budget/` pipeline and the main statement analysis currently live in completely separate silos. If you OCR a Tesco receipt and the bank statement shows a Tesco card payment on the same date for the same total, you can link them and see line-item breakdown inside the transaction history. Needs a fuzzy date+amount matching step.

8. **Gemini-powered monthly summary** — instead of the current `run_ai_model("Write what comes after C")` test, feed it a real prompt: pass the top spending categories and totals for the month and ask for a plain-English summary and one saving suggestion. The infrastructure (`run_ai_model()`) already exists — just needs a meaningful prompt built from the actual analysis output.

9. **Automate data refresh** — the CSV is a static snapshot (Sep 2024 – Feb 2025). Revolut supports statement exports; a short script that watches a downloads folder for a new Revolut CSV export and merges it into the master dataset would keep the analysis current without manual effort. Open question: do you want this as a cron job or a manual trigger?
