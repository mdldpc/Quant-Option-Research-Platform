from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

CHART_DIR = Path(
    "research/reports/backtest_charts"
)


def _prepare_dir():

    CHART_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def _save_plot(path: Path):

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=160
    )

    plt.close()

    return path



def draw_equity_curve(
    trades: pd.DataFrame
) -> Path:
    """
    Generate equity curve chart.
    """

    _prepare_dir()

    path = (
        CHART_DIR
        /
        "equity_curve.png"
    )


    df = trades.copy()


    plt.figure(
        figsize=(8,4)
    )


    plt.plot(
        df["equity"]
    )


    plt.title(
        "Strategy Equity Curve"
    )

    plt.xlabel(
        "Trade"
    )

    plt.ylabel(
        "Equity"
    )


    return _save_plot(path)



def draw_drawdown(
    trades: pd.DataFrame
) -> Path:
    """
    Generate drawdown chart.
    """

    _prepare_dir()

    path = (
        CHART_DIR
        /
        "drawdown.png"
    )


    df = trades.copy()


    plt.figure(
        figsize=(8,4)
    )


    plt.plot(
        df["drawdown"]
    )


    plt.title(
        "Strategy Drawdown"
    )

    plt.xlabel(
        "Trade"
    )

    plt.ylabel(
        "Drawdown"
    )


    return _save_plot(path)



def draw_return_distribution(
    trades: pd.DataFrame
) -> Path:
    """
    Generate return distribution.
    """

    _prepare_dir()

    path = (
        CHART_DIR
        /
        "return_distribution.png"
    )


    df = trades.copy()


    plt.figure(
        figsize=(8,4)
    )


    plt.hist(
        df["option_return"].dropna(),
        bins=30
    )


    plt.title(
        "Return Distribution"
    )


    plt.xlabel(
        "Return"
    )


    plt.ylabel(
        "Frequency"
    )


    return _save_plot(path)