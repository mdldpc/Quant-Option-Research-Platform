"""Run leakage-aware small-sample ML on an existing strategy backtest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

import pandas as pd
from sklearn.metrics import accuracy_score, brier_score_loss, roc_auc_score

# Support the documented ``python scripts/run_small_sample_ml.py`` invocation.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.small_sample import (
    WalkForwardConfig,
    build_market_features,
    run_walk_forward,
    summarize_predictions,
)
from ml.adapters import normalize_trades, parse_trading_date
from ml.evaluation import (
    deflated_sharpe_ratio,
    daily_portfolio_returns,
    fold_stability,
    probabilistic_sharpe_ratio,
    probability_backtest_overfitting,
    stationary_block_bootstrap_ci,
)
from ml.reporting import write_research_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, required=True, help="Daily feature parquet/csv")
    parser.add_argument("--trades", type=Path, required=True, help="Backtest trade parquet/csv")
    parser.add_argument("--output-dir", type=Path, default=Path("research/ml_results"))
    parser.add_argument("--date-col", default="trade_date")
    parser.add_argument("--return-col", default="option_return")
    parser.add_argument("--exit-date-col", default=None)
    parser.add_argument("--strategy", default=None, help="strangle, calendar, or butterfly")
    parser.add_argument(
        "--feature-lag", type=int, default=1,
        help="Trading-date lag applied to all market features; default prevents same-day look-ahead",
    )
    parser.add_argument("--min-train-dates", type=int, default=40)
    parser.add_argument("--test-dates", type=int, default=10)
    parser.add_argument("--embargo-dates", type=int, default=2)
    parser.add_argument("--threshold", type=float, default=0.55)
    parser.add_argument("--transaction-cost", type=float, default=0.0)
    return parser.parse_args()


def read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    return pd.read_parquet(path)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main() -> None:
    args = parse_args()
    features = build_market_features(read_table(args.features), args.date_col)
    if args.feature_lag < 0:
        raise ValueError("feature-lag must be non-negative")
    numeric_features = list(features.select_dtypes(include="number").columns)
    if args.feature_lag:
        features[numeric_features] = features[numeric_features].shift(args.feature_lag)
    trades = normalize_trades(read_table(args.trades), args.strategy)
    if args.date_col != "trade_date":
        features = features.rename(columns={args.date_col: "trade_date"})
    data = trades.merge(features, on="trade_date", how="inner", suffixes=("", "__feature"))
    excluded = {
        "trade_date",
        args.return_col,
        args.exit_date_col,
        "option_pnl",
        "meta_label",
    }
    feature_cols = [c for c in numeric_features if c not in excluded]
    config = WalkForwardConfig(
        min_train_dates=args.min_train_dates,
        test_dates=args.test_dates,
        embargo_dates=args.embargo_dates,
        probability_threshold=args.threshold,
        transaction_cost=args.transaction_cost,
    )
    predictions = run_walk_forward(
        data,
        feature_cols,
        return_col=args.return_col,
        date_col="trade_date",
        exit_date_col=args.exit_date_col if args.exit_date_col in data else None,
        config=config,
    )
    summary = summarize_predictions(predictions)
    raw_importance = pd.DataFrame(predictions.attrs.get("feature_importance", []))
    fold_diagnostics = pd.DataFrame(predictions.attrs.get("fold_diagnostics", []))
    filtered_daily = daily_portfolio_returns(predictions, "filtered_return")
    summary["probabilistic_sharpe_ratio"] = probabilistic_sharpe_ratio(filtered_daily)
    summary["deflated_sharpe_ratio_5_trials"] = deflated_sharpe_ratio(filtered_daily, trials=5)
    summary["probability_backtest_overfitting"] = probability_backtest_overfitting(predictions)
    bootstrap = stationary_block_bootstrap_ci(filtered_daily)
    stability = fold_stability(predictions)
    regime_table = (
        predictions.groupby("market_regime")
        .agg(
            observations=("meta_label", "size"),
            win_rate=("meta_label", "mean"),
            mean_net_return=("net_return", "mean"),
            mean_probability=("predicted_probability", "mean"),
        )
        .reset_index()
    )
    threshold_rows = []
    for threshold in [0.45, 0.50, 0.55, 0.60, 0.65]:
        chosen = predictions["predicted_probability"] >= threshold
        selected = predictions.assign(
            threshold_return=predictions["net_return"].where(chosen, 0.0)
        )
        daily = daily_portfolio_returns(selected, "threshold_return")
        equity = (1 + daily).cumprod()
        threshold_rows.append(
            {
                "threshold": threshold,
                "coverage": float(chosen.mean()),
                "total_return": float(equity.iloc[-1] - 1) if len(equity) else float("nan"),
                "win_rate_when_selected": float((predictions.loc[chosen, "net_return"] > 0).mean()) if chosen.any() else float("nan"),
            }
        )
    threshold_table = pd.DataFrame(threshold_rows)
    y = predictions["meta_label"].astype(int)
    model_rows = []
    for name, column in [
        ("regime_logistic", "logistic_probability"),
        ("shallow_tree", "tree_probability"),
        ("historical_win_rate", "historical_probability"),
    ]:
        probability = predictions[column].clip(1e-8, 1 - 1e-8)
        model_rows.append(
            {
                "model": name,
                "brier": float(brier_score_loss(y, probability)),
                "auc": float(roc_auc_score(y, probability)) if y.nunique() == 2 else float("nan"),
                "accuracy": float(accuracy_score(y, probability >= 0.5)),
            }
        )
    model_table = pd.DataFrame(model_rows)
    cost_rows = []
    for cost in [0.0, 0.001, 0.002, 0.005, 0.01]:
        stressed = predictions[args.return_col] - cost
        selected = stressed.where(predictions["take_trade"], 0.0)
        daily = selected.groupby(predictions["trade_date"]).mean()
        equity = (1 + daily).cumprod()
        cost_rows.append(
            {
                "round_trip_cost": cost,
                "total_return": float(equity.iloc[-1] - 1) if len(equity) else float("nan"),
                "selected_win_rate": float((stressed[predictions["take_trade"]] > 0).mean()) if predictions["take_trade"].any() else float("nan"),
            }
        )
    cost_table = pd.DataFrame(cost_rows)
    if raw_importance.empty:
        importance_table = pd.DataFrame(columns=["feature", "mean_abs_coefficient", "mean_coefficient"])
    else:
        importance_table = (
            raw_importance.groupby("feature")
            .agg(
                mean_abs_coefficient=("absolute_coefficient", "mean"),
                mean_coefficient=("standardized_coefficient", "mean"),
            )
            .sort_values("mean_abs_coefficient", ascending=False)
            .head(20)
            .reset_index()
        )
    calibration = predictions[["predicted_probability", "meta_label"]].copy()
    calibration["probability_bin"] = pd.cut(
        calibration["predicted_probability"], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True
    )
    calibration_table = (
        calibration.groupby("probability_bin", observed=True)
        .agg(observations=("meta_label", "size"), mean_probability=("predicted_probability", "mean"), actual_win_rate=("meta_label", "mean"))
        .reset_index()
    )
    calibration_table["probability_bin"] = calibration_table["probability_bin"].astype(str)
    manifest = {
        "features_file": str(args.features.resolve()),
        "features_sha256": file_sha256(args.features),
        "trades_file": str(args.trades.resolve()),
        "trades_sha256": file_sha256(args.trades),
        "git_commit": git_commit(),
        "python": platform.python_version(),
        "config": vars(args),
        "feature_columns": feature_cols,
        "merged_rows": len(data),
        "merged_dates": int(data["trade_date"].nunique()),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    predictions.to_parquet(args.output_dir / "walk_forward_predictions.parquet", index=False)
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
    regime_table.to_csv(args.output_dir / "regime_analysis.csv", index=False)
    threshold_table.to_csv(args.output_dir / "threshold_sensitivity.csv", index=False)
    model_table.to_csv(args.output_dir / "model_comparison.csv", index=False)
    cost_table.to_csv(args.output_dir / "cost_sensitivity.csv", index=False)
    importance_table.to_csv(args.output_dir / "feature_importance.csv", index=False)
    calibration_table.to_csv(args.output_dir / "calibration.csv", index=False)
    fold_diagnostics.to_csv(args.output_dir / "fold_diagnostics.csv", index=False)
    write_research_report(
        args.output_dir / "research_report.md",
        summary=summary,
        bootstrap=bootstrap,
        stability=stability,
        regime_table=regime_table,
        threshold_table=threshold_table,
        model_table=model_table,
        cost_table=cost_table,
        importance_table=importance_table,
        calibration_table=calibration_table,
        manifest=manifest,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
