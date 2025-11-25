# scripts

This directory contains lightweight utilities and one-off scripts used during
development and experimentation. Typical uses include:

- Downloading or updating raw data (e.g., price history or news data)
- Preprocessing, cleaning, and transforming raw datasets
- Aggregation or export utilities (e.g., create a subset for notebooks)
- Small runners for tasks like reproducing a particular analysis or plot

Best practices
--------------

- Keep scripts idempotent: running the same script twice should result in the
	same final state.
- Prefer adding CLI flags (via `argparse`) rather than hard-coding values.
- When a script grows beyond a few lines, consider moving logic into
	`src/` as importable functions and keeping the script simply as a thin CLI.
- Avoid storing secrets and credentials in scripts. Use environment variables
	or configuration files that are ignored by Git.

How to structure scripts
------------------------

Examples of good script names:
- `download_prices.py` — downloads updated stock price CSVs into `data/`
- `preprocess_news.py` — cleans and normalizes the news dataset
- `compute_indicators.py` — computes TA indicators and writes to `data/` or
	`outputs/`
- `aggregate_sentiment.py` — computes daily sentiment aggregates

Running scripts (examples)
--------------------------

If you're using the repository's Python environment and `scripts` is a module
(`scripts/__init__.py` exists), run scripts with `python -m` to ensure the
package imports behave the same as in notebooks and CI:

```powershell
# Activate virtual environment (PowerShell example)
venv\Scripts\Activate.ps1

# Run a script as a module
python -m scripts.download_prices --start 2022-01-01 --end 2022-12-31

# Or run a script directly
python scripts\preprocess_news.py --input data/raw_analyst_ratings.csv --out data/news_clean.csv
```

Testing and logging
-------------------

- Keep scripts small and add unit-tests where suitable. For example, put
	reusable parsing logic inside `src/` and test it in `tests/`.
- Log progress and errors with the `logging` module instead of using prints.
- Use an `outputs/` or `data/processed/` folder and add generated files to
	`.gitignore` if they are large or transient.

Contribution guidelines
-----------------------

1. Add or update scripts in this folder following the naming conventions above.
2. If the script requires heavy dependencies, note that in a brief comment at
	 the top and add instructions in the top-level `README.md`.
3. Add a small test for any core logic that is moved into `src/`.

Notes
-----
This folder is intentionally simple; for larger automation use a task runner
or a Makefile to provide consistent commands across environments.
