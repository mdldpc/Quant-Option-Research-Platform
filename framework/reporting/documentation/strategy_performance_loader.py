from pathlib import Path
import pandas as pd


EXPORT_DIR = Path("research/exports")


STRATEGY_ALIASES = {
    "long_atm_strangle": [
        "long_atm_strangle",
        "ATM Strangle",
        "Long ATM Strangle",
    ],
    "long_call_butterfly": [
        "long_call_butterfly",
        "Long Call Butterfly",
        "call_butterfly",
    ],
    "calendar_spread": [
        "calendar_spread",
        "Calendar Spread",
    ],
}


CANDIDATE_FILES = [
    EXPORT_DIR / "portfolio_pnl_timeseries_v1_1.csv",
    EXPORT_DIR / "portfolio_status_pnl_v1_1.csv",
    EXPORT_DIR / "pnl_engine_position_pnl_v1_1.csv",
]


def _read_existing_files() -> list[pd.DataFrame]:
    dfs = []

    for path in CANDIDATE_FILES:
        if path.exists():
            df = pd.read_csv(path)
            df["_source_file"] = str(path)
            dfs.append(df)

    return dfs


def _normalize_strategy_name(value: str) -> str:
    return str(value).strip().lower().replace(" ", "_")


def _match_strategy(df: pd.DataFrame, strategy_key: str) -> pd.DataFrame:
    if "strategy" not in df.columns:
        return pd.DataFrame()

    aliases = [
        _normalize_strategy_name(x)
        for x in STRATEGY_ALIASES.get(strategy_key, [strategy_key])
    ]

    x = df.copy()
    x["_strategy_norm"] = x["strategy"].map(_normalize_strategy_name)

    return x[x["_strategy_norm"].isin(aliases)].copy()


def load_strategy_evidence(strategy_key: str) -> list[list[str]]:
    dfs = _read_existing_files()

    matched = []

    for df in dfs:
        m = _match_strategy(df, strategy_key)
        if not m.empty:
            matched.append(m)

    if not matched:
        return [
            ["Backtest / Portfolio Evidence", "No matching exported result file found"],
            ["Current Status", "Strategy implemented; dynamic metrics not yet connected"],
        ]

    data = pd.concat(matched, ignore_index=True)

    pnl_col = None
    for c in ["unrealized_pnl", "pnl", "total_pnl"]:
        if c in data.columns:
            pnl_col = c
            break

    ret_col = None
    for c in ["unrealized_return", "return", "strategy_return"]:
        if c in data.columns:
            ret_col = c
            break

    rows = []

    rows.append(["Evidence Source", ", ".join(sorted(data["_source_file"].unique()))])
    rows.append(["Observations", len(data)])

    if "trade_date" in data.columns:
        rows.append(["Trading Dates", data["trade_date"].nunique()])

    if pnl_col:
        pnl = pd.to_numeric(data[pnl_col], errors="coerce").fillna(0.0)

        rows.append(["Total PnL", f"{pnl.sum():,.2f}"])
        rows.append(["Average PnL", f"{pnl.mean():,.2f}"])
        rows.append(["Best PnL", f"{pnl.max():,.2f}"])
        rows.append(["Worst PnL", f"{pnl.min():,.2f}"])
        rows.append(["Positive Observations", int((pnl > 0).sum())])
        rows.append(["Negative Observations", int((pnl < 0).sum())])

        non_zero = pnl[pnl != 0]
        if len(non_zero) > 0:
            win_rate = (non_zero > 0).mean()
            rows.append(["Win Rate", f"{win_rate:.2%}"])

    if ret_col:
        ret = pd.to_numeric(data[ret_col], errors="coerce").dropna()

        if len(ret) > 0:
            rows.append(["Average Return", f"{ret.mean():.4%}"])
            rows.append(["Best Return", f"{ret.max():.4%}"])
            rows.append(["Worst Return", f"{ret.min():.4%}"])

    rows.append(["Interpretation", "Backtested / evaluated on current 2026 sample"])
    rows.append(["Research Reliability", "Preliminary due to limited historical coverage"])

    return rows