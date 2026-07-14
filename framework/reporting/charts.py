from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


CHART_DIR = Path("research/reports/charts")


def _prepare_dir():
    CHART_DIR.mkdir(parents=True, exist_ok=True)


def _save_plot(path: Path):
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    return path


def _date_labels(df: pd.DataFrame):
    return df["trade_date"].astype(str)


def draw_nav(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    path = CHART_DIR / "nav_curve_v1_2.png"

    df = nav_df.copy()
    df = df.sort_values("trade_date")

    plt.figure(figsize=(8, 4))
    plt.plot(_date_labels(df), df["current_nav"])
    plt.title("Portfolio NAV")
    plt.xlabel("Trade Date")
    plt.ylabel("NAV")
    plt.xticks(rotation=45, ha="right")

    return _save_plot(path)


def draw_pnl(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    path = CHART_DIR / "pnl_v1_2.png"

    df = nav_df.copy()
    df = df.sort_values("trade_date")

    plt.figure(figsize=(8, 4))
    plt.bar(_date_labels(df), df["unrealized_pnl"])
    plt.title("Unrealized PnL")
    plt.xlabel("Trade Date")
    plt.ylabel("PnL")
    plt.xticks(rotation=45, ha="right")

    return _save_plot(path)


def draw_drawdown(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    path = CHART_DIR / "drawdown_v1_2.png"

    df = nav_df.copy()
    df = df.sort_values("trade_date")

    plt.figure(figsize=(8, 4))
    plt.plot(_date_labels(df), df["drawdown"])
    plt.title("Portfolio Drawdown")
    plt.xlabel("Trade Date")
    plt.ylabel("Drawdown")
    plt.xticks(rotation=45, ha="right")

    return _save_plot(path)


def draw_vega(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    path = CHART_DIR / "net_vega_v1_2.png"

    df = nav_df.copy()
    df = df.sort_values("trade_date")

    plt.figure(figsize=(8, 4))
    plt.plot(_date_labels(df), df["net_vega"])
    plt.title("Net Vega Exposure")
    plt.xlabel("Trade Date")
    plt.ylabel("Net Vega")
    plt.xticks(rotation=45, ha="right")

    return _save_plot(path)


def draw_delta(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    path = CHART_DIR / "net_delta_v1_2.png"

    df = nav_df.copy()
    df = df.sort_values("trade_date")

    plt.figure(figsize=(8, 4))
    plt.plot(_date_labels(df), df["net_delta"])
    plt.title("Net Delta Exposure")
    plt.xlabel("Trade Date")
    plt.ylabel("Net Delta")
    plt.xticks(rotation=45, ha="right")

    return _save_plot(path)


def draw_risk_status(nav_df: pd.DataFrame) -> Path:
    _prepare_dir()
    path = CHART_DIR / "risk_status_v1_2.png"

    df = nav_df.copy()

    counts = (
        df["risk_status"]
        .fillna("unknown")
        .value_counts()
        .reindex(["flat", "normal", "warning", "critical"], fill_value=0)
    )

    plt.figure(figsize=(6, 4))
    plt.bar(counts.index, counts.values)
    plt.title("Risk Status Distribution")
    plt.xlabel("Risk Status")
    plt.ylabel("Days")

    return _save_plot(path)