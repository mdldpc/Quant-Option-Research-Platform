import pandas as pd


def project_snapshot(nav_df: pd.DataFrame, clean_df: pd.DataFrame) -> pd.DataFrame:
    if nav_df.empty:
        trading_days = 0
        active_days = 0
        final_nav = 0
        max_dd = 0
    else:
        trading_days = len(nav_df)
        active_days = int((nav_df["positions"] > 0).sum())
        final_nav = float(nav_df["current_nav"].iloc[-1])
        max_dd = float(nav_df["drawdown"].min())

    return pd.DataFrame(
        [
            ["Document Version", "v3.0"],
            ["Trading Days", trading_days],
            ["Filtered Sessions", len(clean_df)],
            ["Active Position Days", active_days],
            ["Strategies", "ATM Straddle Prototype, Long ATM Strangle, Butterfly, Calendar"],
            ["Final NAV", f"{final_nav:,.2f}"],
            ["Max Drawdown", f"{max_dd:.4%}"],
            ["Daily Pipeline", "Completed"],
            ["Word Report", "Completed"],
        ],
        columns=["Item", "Value"],
    )


def strategy_cards() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [
                "ATM Straddle Prototype",
                "Original volatility signal strategy",
                "Long call + long put",
                "Backtested in Phase I",
            ],
            [
                "Long ATM Strangle",
                "Long volatility exposure",
                "Near-ATM call + put",
                "Integrated into portfolio/risk layer",
            ],
            [
                "Long Call Butterfly",
                "Defined-risk convexity structure",
                "Lower/middle/upper call structure",
                "Integrated into strategy library",
            ],
            [
                "Calendar Spread",
                "Term-structure strategy",
                "Near vs next expiry options",
                "Integrated into portfolio/risk layer",
            ],
        ],
        columns=["Strategy", "Objective", "Structure", "Current Status"],
    )


def phase1_backtest_metrics() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Total Trades", "4"],
            ["Winning Trades", "3"],
            ["Losing Trades", "1"],
            ["Win Rate", "75%"],
            ["Final Equity", "1.305"],
            ["Cumulative Return", "30.5%"],
            ["Maximum Drawdown", "-0.92%"],
            ["Average Holding Period", "Approximately 4 trading days"],
        ],
        columns=["Metric", "Value"],
    )


def risk_summary(nav_df: pd.DataFrame) -> pd.DataFrame:
    counts = (
        nav_df["risk_status"]
        .fillna("unknown")
        .value_counts()
        .reindex(["flat", "normal", "warning", "critical"], fill_value=0)
    )

    return pd.DataFrame(
        [
            ["Trading Days", len(nav_df)],
            ["Flat Days", int(counts["flat"])],
            ["Normal Days", int(counts["normal"])],
            ["Warning Days", int(counts["warning"])],
            ["Critical Days", int(counts["critical"])],
            ["Max Absolute Delta", f"{nav_df['net_delta'].abs().max():.6f}"],
            ["Max Absolute Vega", f"{nav_df['net_vega'].abs().max():.2f}"],
            ["Max Absolute Theta", f"{nav_df['net_theta'].abs().max():.2f}"],
        ],
        columns=["Metric", "Value"],
    )


def portfolio_summary(nav_df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            ["Final NAV", f"{float(nav_df['current_nav'].iloc[-1]):,.2f}"],
            ["Highest NAV", f"{float(nav_df['current_nav'].max()):,.2f}"],
            ["Lowest NAV", f"{float(nav_df['current_nav'].min()):,.2f}"],
            ["Maximum Drawdown", f"{float(nav_df['drawdown'].min()):.4%}"],
            ["Best Daily PnL", f"{float(nav_df['unrealized_pnl'].max()):,.2f}"],
            ["Worst Daily PnL", f"{float(nav_df['unrealized_pnl'].min()):,.2f}"],
            ["Active Position Days", int((nav_df["positions"] > 0).sum())],
            ["Total Trading Days", len(nav_df)],
        ],
        columns=["Metric", "Value"],
    )