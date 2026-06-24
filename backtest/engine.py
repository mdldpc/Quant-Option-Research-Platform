import pandas as pd

from config.settings import (
    INITIAL_CAPITAL,
    TOTAL_TRANSACTION_COST,
)

from backtest.metrics import calculate_drawdown, summarize_backtest
from backtest.transaction import apply_total_cost


def run_option_backtest(
    trades: pd.DataFrame,
    return_col: str = "option_return",
    initial_capital: float = INITIAL_CAPITAL,
    total_transaction_cost: float = TOTAL_TRANSACTION_COST,
) -> tuple[pd.DataFrame, dict]:
    """
    Reusable option strategy backtest engine.

    Input:
        trades: option trade dataset
        return_col: column used as gross trade return

    Output:
        backtest_df: trade-level backtest table
        stats: performance statistics
    """

    df = trades.copy()

    if "status" in df.columns:
        df = df[df["status"] == "ok"].copy()

    if df.empty:
        return df, {}

    df = df.sort_values("entry_date").reset_index(drop=True)

    df["gross_return"] = df[return_col]
    df["net_return"] = df["gross_return"].apply(
        lambda x: apply_total_cost(
            x,
            total_cost=total_transaction_cost,
        )
    )

    df["equity"] = (
        (1 + df["net_return"]).cumprod()
        * initial_capital
    )

    df["drawdown"] = calculate_drawdown(df["equity"])

    stats = summarize_backtest(
        equity=df["equity"],
        returns=df["net_return"],
    )

    if "holding_days" in df.columns:
        stats["avg_holding_days"] = df["holding_days"].mean()

    stats["initial_capital"] = initial_capital
    stats["transaction_cost"] = total_transaction_cost

    return df, stats


def format_backtest_report(stats: dict, title: str = "OPTION BACKTEST REPORT") -> str:
    lines = []
    lines.append("============================")
    lines.append(title)
    lines.append("============================")
    lines.append("")

    for key, value in stats.items():
        lines.append(f"{key}: {value}")

    return "\n".join(lines)