import pandas as pd

from config.settings import (
    LONG_SIGNAL_THRESHOLD,
    MAX_HOLDING_DAYS,
    TOTAL_TRANSACTION_COST,
)


# =========================
# 1. Threshold Experiment
# =========================
def threshold_experiment(
    trades: pd.DataFrame,
    threshold: int = LONG_SIGNAL_THRESHOLD,
):
    df = trades.copy()

    score_col = "signal_score" if "signal_score" in df.columns else "entry_signal_score"

    df = df[df[score_col] >= threshold].copy()

    if len(df) == 0:
        return {
            "threshold": threshold,
            "trade_count": 0,
            "avg_return": 0,
            "sharpe": 0,
        }

    avg_return = df["option_return"].mean()
    sharpe = df["option_return"].mean() / (df["option_return"].std() + 1e-8)

    return {
        "threshold": threshold,
        "trade_count": len(df),
        "avg_return": avg_return,
        "sharpe": sharpe,
    }


# =========================
# 2. Holding Experiment
# =========================
def holding_experiment(
    trades: pd.DataFrame,
    holding_days: int = MAX_HOLDING_DAYS,
):
    df = trades.copy()

    df = df[df["holding_days"] <= holding_days].copy()

    if len(df) == 0:
        return {
            "holding_days": holding_days,
            "trade_count": 0,
            "avg_return": 0,
            "sharpe": 0,
        }

    avg_return = df["option_return"].mean()
    sharpe = df["option_return"].mean() / (df["option_return"].std() + 1e-8)

    return {
        "holding_days": holding_days,
        "trade_count": len(df),
        "avg_return": avg_return,
        "sharpe": sharpe,
    }


# =========================
# 3. Transaction Cost Experiment
# =========================
def cost_experiment(
    trades: pd.DataFrame,
    cost: float = TOTAL_TRANSACTION_COST,
):
    df = trades.copy()

    df["net_return"] = df["option_return"] - cost

    avg_return = df["net_return"].mean()
    sharpe = df["net_return"].mean() / (df["net_return"].std() + 1e-8)

    return {
        "cost": cost,
        "trade_count": len(df),
        "avg_return": avg_return,
        "sharpe": sharpe,
    }