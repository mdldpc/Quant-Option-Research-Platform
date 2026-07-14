from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


CHART_DIR = Path("research/reports/charts_v3")


def _prepare_dir():
    CHART_DIR.mkdir(parents=True, exist_ok=True)


def _prepare_dates(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    x["date"] = pd.to_datetime(x["trade_date"].astype(str), format="%Y%m%d")
    return x.sort_values("date")


def _format_month_axis(ax):
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha="right")


def _save(path: Path):
    plt.tight_layout()
    plt.savefig(path, dpi=170)
    plt.close()
    return path


def nav_curve(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    df = _prepare_dates(nav_df)
    path = CHART_DIR / "nav_curve_v3.png"

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["date"], df["current_nav"], linewidth=1.8)
    ax.set_title("Portfolio NAV Curve")
    ax.set_xlabel("Month")
    ax.set_ylabel("NAV")
    _format_month_axis(ax)

    return _save(path)


def pnl_bar(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    df = _prepare_dates(nav_df)
    path = CHART_DIR / "pnl_bar_v3.png"

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df["date"], df["unrealized_pnl"], width=2.5)
    ax.set_title("Daily Unrealized PnL")
    ax.set_xlabel("Month")
    ax.set_ylabel("PnL")
    _format_month_axis(ax)

    return _save(path)


def drawdown_curve(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    df = _prepare_dates(nav_df)
    path = CHART_DIR / "drawdown_curve_v3.png"

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["date"], df["drawdown"], linewidth=1.8)
    ax.set_title("Portfolio Drawdown")
    ax.set_xlabel("Month")
    ax.set_ylabel("Drawdown")
    _format_month_axis(ax)

    return _save(path)


def vega_curve(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    df = _prepare_dates(nav_df)
    path = CHART_DIR / "vega_curve_v3.png"

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["date"], df["net_vega"], linewidth=1.8)
    ax.set_title("Net Vega Exposure")
    ax.set_xlabel("Month")
    ax.set_ylabel("Net Vega")
    _format_month_axis(ax)

    return _save(path)


def delta_curve(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    df = _prepare_dates(nav_df)
    path = CHART_DIR / "delta_curve_v3.png"

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["date"], df["net_delta"], linewidth=1.8)
    ax.set_title("Net Delta Exposure")
    ax.set_xlabel("Month")
    ax.set_ylabel("Net Delta")
    _format_month_axis(ax)

    return _save(path)


def risk_status_bar(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    path = CHART_DIR / "risk_status_v3.png"

    counts = (
        nav_df["risk_status"]
        .fillna("unknown")
        .value_counts()
        .reindex(["flat", "normal", "warning", "critical"], fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(counts.index, counts.values)
    ax.set_title("Risk Status Distribution")
    ax.set_xlabel("Risk Status")
    ax.set_ylabel("Trading Days")
    ax.grid(True, axis="y", alpha=0.3)

    return _save(path)