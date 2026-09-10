"""Leakage-aware models designed for short option histories.

The unit of validation is a trading date, not an option-contract row.  Every
test block is strictly later than its training block and an embargo is applied
between them.  PCA and the classifier are fitted again inside every fold.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, roc_auc_score
from sklearn.mixture import GaussianMixture
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .adapters import parse_trading_date
from .evaluation import daily_portfolio_returns, performance_metrics


@dataclass(frozen=True)
class WalkForwardConfig:
    """Controls the expanding-window experiment."""

    min_train_dates: int = 40
    test_dates: int = 10
    embargo_dates: int = 2
    probability_threshold: float = 0.55
    transaction_cost: float = 0.0
    max_pca_components: int = 5
    random_state: int = 42


def build_market_features(frame: pd.DataFrame, date_col: str = "trade_date") -> pd.DataFrame:
    """Create conservative, backward-looking features from a daily table.

    Existing numeric columns are retained.  Changes and rolling z-scores use
    only observations available on or before each date; callers should lag the
    table explicitly if their signal is formed before the source observation.
    """
    if date_col not in frame:
        raise ValueError(f"missing date column: {date_col}")
    out = frame.copy()
    out[date_col] = parse_trading_date(out[date_col])
    out = out.sort_values(date_col).drop_duplicates(date_col, keep="last")
    numeric = [c for c in out.select_dtypes(include=np.number).columns if c != date_col]
    for col in numeric:
        values = pd.to_numeric(out[col], errors="coerce")
        out[f"{col}__change_1"] = values.diff()
        history = values.shift(1).rolling(20, min_periods=10)
        out[f"{col}__z20"] = (values - history.mean()) / history.std().replace(0, np.nan)
    return out.replace([np.inf, -np.inf], np.nan)


def _model(n_rows: int, n_features: int, config: WalkForwardConfig) -> Pipeline:
    components = max(1, min(config.max_pca_components, n_features, n_rows - 1))
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=components, random_state=config.random_state)),
            (
                "classifier",
                LogisticRegression(
                    class_weight="balanced",
                    C=0.5,
                    max_iter=2_000,
                    random_state=config.random_state,
                ),
            ),
        ]
    )


def _regimes(
    train_x: pd.DataFrame, test_x: pd.DataFrame, random_state: int
) -> tuple[np.ndarray, np.ndarray]:
    """Fit PCA + GMM on training data only and return stable ordered labels."""
    prep = Pipeline(
        [("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
    )
    train_scaled = prep.fit_transform(train_x)
    test_scaled = prep.transform(test_x)
    n_components = max(1, min(3, train_scaled.shape[1], train_scaled.shape[0] - 1))
    pca = PCA(n_components=n_components, random_state=random_state)
    train_latent = pca.fit_transform(train_scaled)
    test_latent = pca.transform(test_scaled)
    n_regimes = 2 if len(train_x) >= 30 else 1
    gmm = GaussianMixture(n_components=n_regimes, covariance_type="full", random_state=random_state)
    gmm.fit(train_latent)
    train_raw = gmm.predict(train_latent)
    test_raw = gmm.predict(test_latent)
    # GMM labels are arbitrary. Order states by mean first PC so regime IDs are
    # comparable across folds (0=lower first-factor state).
    means = {label: train_latent[train_raw == label, 0].mean() for label in range(n_regimes)}
    mapping = {old: new for new, old in enumerate(sorted(means, key=means.get))}
    return (
        np.asarray([mapping[x] for x in train_raw]),
        np.asarray([mapping[x] for x in test_raw]),
    )


def run_walk_forward(
    frame: pd.DataFrame,
    feature_cols: Iterable[str],
    *,
    return_col: str = "option_return",
    date_col: str = "trade_date",
    exit_date_col: str | None = None,
    config: WalkForwardConfig | None = None,
) -> pd.DataFrame:
    """Generate honest out-of-sample meta-label probabilities.

    If ``exit_date_col`` is supplied, a training trade is admitted only when it
    has exited before the embargo boundary.  This purges overlapping labels.
    """
    config = config or WalkForwardConfig()
    cols = list(feature_cols)
    missing = [c for c in [date_col, return_col, *cols] if c not in frame]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    if not cols:
        raise ValueError("at least one feature column is required")

    data = frame.copy()
    data[date_col] = parse_trading_date(data[date_col])
    data[return_col] = pd.to_numeric(data[return_col], errors="coerce")
    if exit_date_col:
        if exit_date_col not in data:
            raise ValueError(f"missing exit date column: {exit_date_col}")
        data[exit_date_col] = parse_trading_date(data[exit_date_col])
    data = data.dropna(subset=[date_col, return_col]).sort_values(date_col).reset_index(drop=True)
    data["meta_label"] = (data[return_col] > config.transaction_cost).astype(int)
    dates = np.array(sorted(data[date_col].unique()))
    if len(dates) < config.min_train_dates + config.embargo_dates + 1:
        raise ValueError(
            f"only {len(dates)} unique dates; need at least "
            f"{config.min_train_dates + config.embargo_dates + 1}"
        )

    predictions: list[pd.DataFrame] = []
    importance_rows: list[dict[str, float | str]] = []
    fold_rows: list[dict[str, float | int | str]] = []
    first_test = config.min_train_dates + config.embargo_dates
    for start in range(first_test, len(dates), config.test_dates):
        test_dates = dates[start : start + config.test_dates]
        embargo_boundary = dates[start - config.embargo_dates]
        train = data[data[date_col] < embargo_boundary]
        if exit_date_col:
            train = train[train[exit_date_col] < embargo_boundary]
        test = data[data[date_col].isin(test_dates)].copy()
        if train.empty or test.empty or train["meta_label"].nunique() < 2:
            continue

        train_regime, test_regime = _regimes(train[cols], test[cols], config.random_state)
        train_x = train[cols].copy()
        test_x = test[cols].copy()
        train_x["__market_regime"] = train_regime
        test_x["__market_regime"] = test_regime

        model = _model(len(train), len(train_x.columns), config)
        model.fit(train_x, train["meta_label"])
        test["logistic_probability"] = model.predict_proba(test_x)[:, 1]
        pca_step = model.named_steps["pca"]
        classifier_step = model.named_steps["classifier"]
        original_space_coefficient = classifier_step.coef_[0] @ pca_step.components_
        for feature, coefficient in zip(train_x.columns, original_space_coefficient):
            importance_rows.append(
                {
                    "fold_train_end": str(pd.Timestamp(embargo_boundary).date()),
                    "feature": feature,
                    "standardized_coefficient": float(coefficient),
                    "absolute_coefficient": float(abs(coefficient)),
                }
            )
        fold_rows.append(
            {
                "fold_train_end": str(pd.Timestamp(embargo_boundary).date()),
                "train_rows": int(len(train)),
                "test_rows": int(len(test)),
                "pca_components": int(pca_step.n_components_),
                "pca_explained_variance": float(pca_step.explained_variance_ratio_.sum()),
            }
        )

        tree = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "classifier",
                    HistGradientBoostingClassifier(
                        max_depth=2,
                        max_iter=60,
                        learning_rate=0.05,
                        l2_regularization=2.0,
                        random_state=config.random_state,
                    ),
                ),
            ]
        )
        counts = train["meta_label"].value_counts()
        weights = train["meta_label"].map({label: len(train) / (2 * count) for label, count in counts.items()})
        tree.fit(train_x, train["meta_label"], classifier__sample_weight=weights)
        test["tree_probability"] = tree.predict_proba(test_x)[:, 1]
        test["historical_probability"] = float(train["meta_label"].mean())
        # Logistic is the primary model: regularization is a safer default for
        # this short history. Tree predictions are retained as a nonlinear benchmark.
        test["predicted_probability"] = test["logistic_probability"]
        test["take_trade"] = test["predicted_probability"] >= config.probability_threshold
        test["market_regime"] = test_regime
        test["fold_train_end"] = pd.Timestamp(embargo_boundary)
        test["fold_train_rows"] = len(train)
        test["net_return"] = test[return_col] - config.transaction_cost
        test["filtered_return"] = np.where(test["take_trade"], test["net_return"], 0.0)
        predictions.append(test)

    if not predictions:
        raise ValueError("no valid fold had both positive and negative training labels")
    result = pd.concat(predictions, ignore_index=True)
    result.attrs["feature_importance"] = importance_rows
    result.attrs["fold_diagnostics"] = fold_rows
    return result


def summarize_predictions(predictions: pd.DataFrame) -> dict[str, float | int]:
    """Return compact classification and trading metrics."""
    y = predictions["meta_label"].astype(int)
    p = predictions["predicted_probability"].clip(1e-8, 1 - 1e-8)
    chosen = predictions["take_trade"].astype(bool)
    raw_daily = daily_portfolio_returns(predictions, "net_return")
    filtered_daily = daily_portfolio_returns(predictions, "filtered_return")
    raw_perf = performance_metrics(raw_daily)
    filtered_perf = performance_metrics(filtered_daily)
    result: dict[str, float | int] = {
        "oos_rows": int(len(predictions)),
        "oos_dates": int(predictions["trade_date"].nunique()),
        "base_win_rate": float(y.mean()),
        "brier_score": float(brier_score_loss(y, p)),
        "accuracy": float(accuracy_score(y, p >= 0.5)),
        "coverage": float(chosen.mean()),
        "raw_total_return": float(raw_perf.get("total_return", np.nan)),
        "filtered_total_return": float(filtered_perf.get("total_return", np.nan)),
        "raw_sharpe": float(raw_perf.get("sharpe", np.nan)),
        "filtered_sharpe": float(filtered_perf.get("sharpe", np.nan)),
        "raw_max_drawdown": float(raw_perf.get("max_drawdown", np.nan)),
        "filtered_max_drawdown": float(filtered_perf.get("max_drawdown", np.nan)),
        "tree_brier_score": float(brier_score_loss(y, predictions["tree_probability"])),
        "historical_brier_score": float(brier_score_loss(y, predictions["historical_probability"])),
    }
    result["roc_auc"] = float(roc_auc_score(y, p)) if y.nunique() == 2 else float("nan")
    result["filtered_win_rate"] = (
        float((predictions.loc[chosen, "net_return"] > 0).mean()) if chosen.any() else float("nan")
    )
    return result
