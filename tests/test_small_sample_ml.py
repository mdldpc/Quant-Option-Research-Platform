import numpy as np
import pandas as pd
import pytest

from ml.small_sample import (
    WalkForwardConfig,
    build_market_features,
    run_walk_forward,
    summarize_predictions,
)
from ml.adapters import normalize_trades, parse_trading_date
from ml.evaluation import performance_metrics, stationary_block_bootstrap_ci
from ml.reporting import write_research_report


def synthetic_data(n=90):
    rng = np.random.default_rng(42)
    dates = pd.date_range("2026-01-01", periods=n, freq="B")
    level = np.sin(np.arange(n) / 7) + rng.normal(0, 0.2, n)
    returns = 0.015 * np.sign(level) + rng.normal(0, 0.02, n)
    return pd.DataFrame(
        {"trade_date": dates, "iv_level": level, "term_slope": -level / 3, "option_return": returns}
    )


def test_feature_engineering_uses_prior_window_for_zscore():
    result = build_market_features(synthetic_data(30))
    assert "iv_level__change_1" in result
    assert "iv_level__z20" in result
    assert pd.isna(result.loc[result.index[0], "iv_level__change_1"])


def test_walk_forward_is_chronological_and_embargoed():
    data = synthetic_data()
    config = WalkForwardConfig(min_train_dates=30, test_dates=7, embargo_dates=3)
    result = run_walk_forward(
        data, ["iv_level", "term_slope"], config=config
    )
    assert not result.empty
    assert (result["fold_train_end"] < result["trade_date"]).all()
    assert result["predicted_probability"].between(0, 1).all()
    assert set(result["market_regime"].unique()).issubset({0, 1})
    summary = summarize_predictions(result)
    assert summary["oos_dates"] > 0
    assert 0 <= summary["coverage"] <= 1


def test_too_few_dates_fails_loudly():
    with pytest.raises(ValueError, match="unique dates"):
        run_walk_forward(
            synthetic_data(10),
            ["iv_level"],
            config=WalkForwardConfig(min_train_dates=20),
        )


def test_yyyymmdd_dates_are_not_parsed_as_nanoseconds():
    parsed = parse_trading_date(pd.Series([20260105, "20260106"]))
    assert parsed.dt.strftime("%Y-%m-%d").tolist() == ["2026-01-05", "2026-01-06"]


def test_strategy_adapter_filters_failed_rows():
    raw = pd.DataFrame(
        {
            "entry_date": [20260105, 20260106],
            "exit_date": [20260107, 20260108],
            "status": ["ok", "missing_snapshot"],
            "option_return": [0.1, None],
        }
    )
    out = normalize_trades(raw, "strangle")
    assert len(out) == 1
    assert out.loc[0, "strategy"] == "long_atm_strangle"


def test_portfolio_metrics_and_bootstrap_are_finite():
    returns = pd.Series([0.01, -0.02, 0.03, 0.01, -0.005])
    metrics = performance_metrics(returns)
    interval = stationary_block_bootstrap_ci(returns, samples=100)
    assert metrics["observations"] == 5
    assert np.isfinite(metrics["max_drawdown"])
    assert interval["total_return_low"] <= interval["total_return_high"]


def test_report_has_no_optional_tabulate_dependency(tmp_path):
    output = tmp_path / "report.md"
    write_research_report(
        output,
        summary={"auc": 0.6},
        bootstrap={"low": -0.1},
        stability={"folds": 3},
        regime_table=pd.DataFrame({"market_regime": [0], "return": [0.01]}),
        threshold_table=pd.DataFrame({"threshold": [0.55], "coverage": [0.4]}),
        model_table=pd.DataFrame({"model": ["logistic"], "brier": [0.2]}),
        cost_table=pd.DataFrame({"cost": [0.002], "return": [0.1]}),
        importance_table=pd.DataFrame({"feature": ["iv"], "importance": [0.2]}),
        calibration_table=pd.DataFrame({"bin": ["0.4-0.6"], "win_rate": [0.5]}),
        manifest={"seed": 42},
    )
    text = output.read_text(encoding="utf-8")
    assert "Performance by market regime" in text
    assert "| market_regime | return |" in text


def test_cli_end_to_end_with_existing_v11_shape(tmp_path, monkeypatch):
    from scripts.run_small_sample_ml import main

    data = synthetic_data(70)
    feature_path = tmp_path / "features.csv"
    trade_path = tmp_path / "strangle.csv"
    output = tmp_path / "results"
    data[["trade_date", "iv_level", "term_slope"]].assign(
        trade_date=lambda x: x["trade_date"].dt.strftime("%Y%m%d")
    ).to_csv(feature_path, index=False)
    pd.DataFrame(
        {
            "entry_date": data["trade_date"].dt.strftime("%Y%m%d"),
            "exit_date": (data["trade_date"] + pd.Timedelta(days=2)).dt.strftime("%Y%m%d"),
            "status": "ok",
            "option_return": data["option_return"],
        }
    ).to_csv(trade_path, index=False)
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_small_sample_ml.py",
            "--features", str(feature_path),
            "--trades", str(trade_path),
            "--strategy", "strangle",
            "--exit-date-col", "exit_date",
            "--min-train-dates", "25",
            "--test-dates", "8",
            "--output-dir", str(output),
        ],
    )
    main()
    assert (output / "walk_forward_predictions.parquet").exists()
    assert (output / "manifest.json").exists()
    assert (output / "research_report.md").exists()
