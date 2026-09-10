"""Portfolio-level and small-sample uncertainty metrics."""

from __future__ import annotations

import math
from itertools import combinations
import numpy as np
import pandas as pd
from scipy.stats import norm


def daily_portfolio_returns(
    frame: pd.DataFrame, return_col: str, date_col: str = "trade_date"
) -> pd.Series:
    """Equal-weight concurrent entries, then produce one return per date."""
    values = frame[[date_col, return_col]].dropna().copy()
    values[date_col] = pd.to_datetime(values[date_col])
    return values.groupby(date_col)[return_col].mean().sort_index()


def performance_metrics(returns: pd.Series, annualization: int = 252) -> dict[str, float | int]:
    r = pd.Series(returns, dtype=float).dropna()
    if r.empty:
        return {"observations": 0}
    equity = (1.0 + r).cumprod()
    drawdown = equity / equity.cummax() - 1.0
    std = r.std(ddof=1)
    downside = r[r < 0].std(ddof=1)
    sharpe = np.nan if not np.isfinite(std) or std == 0 else r.mean() / std * math.sqrt(annualization)
    return {
        "observations": int(len(r)),
        "total_return": float(equity.iloc[-1] - 1.0),
        "annualized_return": float(equity.iloc[-1] ** (annualization / len(r)) - 1.0),
        "annualized_volatility": float(std * math.sqrt(annualization)) if np.isfinite(std) else np.nan,
        "sharpe": float(sharpe),
        "sortino": float(r.mean() / downside * math.sqrt(annualization)) if downside and np.isfinite(downside) else np.nan,
        "max_drawdown": float(drawdown.min()),
        "win_rate": float((r > 0).mean()),
        "cvar_95": float(r[r <= r.quantile(0.05)].mean()),
    }


def stationary_block_bootstrap_ci(
    returns: pd.Series,
    *,
    samples: int = 1_000,
    mean_block: int = 5,
    confidence: float = 0.95,
    random_state: int = 42,
) -> dict[str, float]:
    """Bootstrap dependent returns using random contiguous circular blocks."""
    x = pd.Series(returns, dtype=float).dropna().to_numpy()
    if len(x) < 2:
        return {"total_return_low": np.nan, "total_return_high": np.nan, "sharpe_low": np.nan, "sharpe_high": np.nan}
    rng = np.random.default_rng(random_state)
    totals, sharpes = [], []
    for _ in range(samples):
        draw: list[float] = []
        while len(draw) < len(x):
            start = rng.integers(0, len(x))
            length = max(1, int(rng.geometric(1.0 / max(1, mean_block))))
            draw.extend(x[(start + j) % len(x)] for j in range(length))
        sample = np.asarray(draw[: len(x)])
        totals.append(np.prod(1 + sample) - 1)
        std = sample.std(ddof=1)
        sharpes.append(np.nan if std == 0 else sample.mean() / std * np.sqrt(252))
    alpha = (1 - confidence) / 2
    return {
        "total_return_low": float(np.nanquantile(totals, alpha)),
        "total_return_high": float(np.nanquantile(totals, 1 - alpha)),
        "sharpe_low": float(np.nanquantile(sharpes, alpha)),
        "sharpe_high": float(np.nanquantile(sharpes, 1 - alpha)),
    }


def fold_stability(predictions: pd.DataFrame) -> dict[str, float | int]:
    grouped = predictions.groupby("fold_train_end")["filtered_return"].sum()
    return {
        "folds": int(len(grouped)),
        "positive_fold_fraction": float((grouped > 0).mean()) if len(grouped) else np.nan,
        "worst_fold_return": float(grouped.min()) if len(grouped) else np.nan,
        "best_fold_return": float(grouped.max()) if len(grouped) else np.nan,
    }


def probabilistic_sharpe_ratio(returns: pd.Series, benchmark: float = 0.0) -> float:
    """Probability that the observed Sharpe exceeds a benchmark Sharpe."""
    r = pd.Series(returns, dtype=float).dropna()
    if len(r) < 3 or r.std(ddof=1) == 0:
        return float("nan")
    sr = r.mean() / r.std(ddof=1)
    skew = r.skew()
    kurtosis = r.kurtosis() + 3.0
    denominator = np.sqrt(max(1e-12, (1 - skew * sr + ((kurtosis - 1) / 4) * sr**2) / (len(r) - 1)))
    return float(norm.cdf((sr - benchmark) / denominator))


def deflated_sharpe_ratio(returns: pd.Series, trials: int = 1) -> float:
    """Conservative PSR adjustment for trying multiple strategy variants."""
    r = pd.Series(returns, dtype=float).dropna()
    if len(r) < 3:
        return float("nan")
    # Expected maximum of N standard-normal trials (Bailey/Lopez de Prado approximation).
    n = max(1, trials)
    gamma = 0.5772156649015329
    expected_max = (1 - gamma) * norm.ppf(1 - 1 / n) + gamma * norm.ppf(1 - 1 / (n * np.e)) if n > 1 else 0.0
    benchmark = expected_max / np.sqrt(max(1, len(r) - 1))
    return probabilistic_sharpe_ratio(r, benchmark)


def probability_backtest_overfitting(
    predictions: pd.DataFrame,
    thresholds: tuple[float, ...] = (0.45, 0.50, 0.55, 0.60, 0.65),
    max_splits: int = 200,
) -> float:
    """CSCV-style estimate that the best threshold fails out of sample.

    Each walk-forward fold is already out of sample. Half of those folds select
    a threshold and the complementary folds assess whether it ranks below the
    median. This diagnostic is undefined with fewer than four folds.
    """
    folds = list(pd.unique(predictions["fold_train_end"]))
    if len(folds) < 4:
        return float("nan")
    half = len(folds) // 2
    splits = list(combinations(folds, half))[:max_splits]

    def score(subset: pd.DataFrame, threshold: float) -> float:
        values = subset["net_return"].where(subset["predicted_probability"] >= threshold, 0.0)
        return float(values.groupby(subset["trade_date"]).mean().sum())

    failures = 0
    valid = 0
    all_folds = set(folds)
    for train_folds in splits:
        test_folds = all_folds.difference(train_folds)
        inside = predictions[predictions["fold_train_end"].isin(train_folds)]
        outside = predictions[predictions["fold_train_end"].isin(test_folds)]
        inside_scores = {t: score(inside, t) for t in thresholds}
        selected = max(inside_scores, key=inside_scores.get)
        outside_scores = {t: score(outside, t) for t in thresholds}
        selected_rank = pd.Series(outside_scores).rank(pct=True, method="average").loc[selected]
        failures += int(selected_rank <= 0.5)
        valid += 1
    return float(failures / valid) if valid else float("nan")
