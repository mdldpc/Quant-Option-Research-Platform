# Small-Sample Regime-Aware ML

This experiment adds an honest machine-learning filter to an existing option
strategy. It is deliberately designed for the short 2026H1 history.

## Design

- A trading date, not a contract row, is the validation unit.
- Expanding walk-forward folds replace random train/test splitting.
- An embargo separates training and test dates.
- If an exit-date column is supplied, overlapping training labels are purged.
- Imputation, scaling and PCA are refitted inside every fold.
- PCA + Gaussian mixtures assign a market regime using training data only.
- Regime identifiers are ordered by the first principal component and are fed
  into the classifier, so the model is genuinely regime-aware.
- Regularized, class-balanced logistic regression supplies interpretable
  out-of-sample probabilities.
- A shallow histogram gradient-boosting model and the expanding historical win
  rate are retained as nonlinear and naive probability benchmarks.
- A fixed probability threshold filters the original strategy. The unfiltered
  strategy remains the benchmark.

This is a research experiment, not evidence of live profitability. With a
short history, stability across folds and uncertainty matter more than a high
in-sample score.

## Run

Run from the project root, substituting files produced by the existing data and
backtest pipelines:

```powershell
python scripts/run_small_sample_ml.py `
  --features research/signals/daily_signal_features.parquet `
  --trades research/backtest/option_strategy_backtest.parquet `
  --exit-date-col exit_date `
  --transaction-cost 0.002
```

All market features are lagged by one trading date by default. Use
`--feature-lag 0` only when the entry timestamp is demonstrably later than the
feature timestamp.

If the trade table has no `exit_date`, omit that argument. The output directory
contains `walk_forward_predictions.parquet` and `summary.json`.

It also writes:

- `research_report.md`: methodology, OOS results, regime and sensitivity tables
- `manifest.json`: input hashes, Git revision, configuration and exact features
- `regime_analysis.csv`: conditional performance by ordered PCA/GMM state
- `threshold_sensitivity.csv`: diagnostic coverage and return comparison
- `model_comparison.csv`: logistic, shallow-tree, and historical-rate baselines
- `cost_sensitivity.csv`: fixed-policy stress under higher round-trip costs
- `feature_importance.csv`: fold-averaged standardized logistic coefficients
- `calibration.csv`: predicted probability versus realized win rate
- `fold_diagnostics.csv`: train/test sizes and PCA variance retained by fold

Reported portfolio returns use one equal-weight return per entry date and
compound through time. Uncertainty uses a stationary block bootstrap. The report
also includes probabilistic and deflated Sharpe ratios; these are diagnostics,
not a substitute for more history.
When at least four folds are available, a CSCV-style probability of backtest
overfitting diagnostic checks whether the best probability threshold tends to
fall below the median on complementary folds.

## Existing strategy adapters

`ml.adapters.normalize_trades` understands the v1.1 Strangle, Calendar, and
Butterfly output convention (`entry_date`, `exit_date`, `status`,
`option_return`). YYYYMMDD integers are parsed explicitly rather than being
mistaken for Unix nanoseconds.

When daily position marks exist, `ml.adapters.add_path_labels` can attach MAE,
MFE, and the first profit-target/stop-loss barrier. Those path-dependent labels
cannot be reconstructed honestly from entry/exit summaries alone.

Important: the daily features must be observable when the trade is entered. If
a feature is calculated after entry time, shift it by one trading date before
running the experiment.
