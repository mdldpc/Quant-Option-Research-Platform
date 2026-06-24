import numpy as np
import pandas as pd


def calculate_drawdown(equity: pd.Series) -> pd.Series:
    running_max = equity.cummax()
    return (equity - running_max) / running_max


def summarize_returns(returns: pd.Series) -> dict:
    returns = returns.dropna()

    if len(returns) == 0:
        return {}

    win_rate = (returns > 0).mean()
    avg_return = returns.mean()
    median_return = returns.median()
    std_return = returns.std()

    sharpe_per_trade = (
        np.nan
        if std_return == 0
        else avg_return / std_return * np.sqrt(len(returns))
    )

    profit = returns[returns > 0].sum()
    loss = -returns[returns < 0].sum()
    profit_factor = np.inf if loss == 0 else profit / loss

    return {
        "trade_count": len(returns),
        "win_rate": win_rate,
        "avg_return": avg_return,
        "median_return": median_return,
        "std_return": std_return,
        "sharpe_per_trade": sharpe_per_trade,
        "profit_factor": profit_factor,
    }


def summarize_backtest(equity: pd.Series, returns: pd.Series) -> dict:
    drawdown = calculate_drawdown(equity)
    stats = summarize_returns(returns)

    stats["total_return"] = equity.iloc[-1] / equity.iloc[0] - 1
    stats["max_drawdown"] = drawdown.min()

    return stats