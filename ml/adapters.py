"""Adapters for the three strategy backtest formats used by this project."""

from __future__ import annotations

import numpy as np
import pandas as pd


STRATEGY_ALIASES = {
    "strangle": "long_atm_strangle",
    "long_atm_strangle": "long_atm_strangle",
    "calendar": "calendar_spread",
    "calendar_spread": "calendar_spread",
    "butterfly": "long_call_butterfly",
    "long_call_butterfly": "long_call_butterfly",
}


def parse_trading_date(values: pd.Series) -> pd.Series:
    """Parse YYYYMMDD integers/strings without treating them as nanoseconds."""
    text = values.astype("string").str.replace(r"\.0$", "", regex=True)
    compact = text.str.fullmatch(r"\d{8}", na=False)
    result = pd.Series(pd.NaT, index=values.index, dtype="datetime64[ns]")
    result.loc[compact] = pd.to_datetime(text.loc[compact], format="%Y%m%d", errors="coerce")
    result.loc[~compact] = pd.to_datetime(values.loc[~compact], errors="coerce")
    return result


def normalize_trades(frame: pd.DataFrame, strategy: str | None = None) -> pd.DataFrame:
    """Normalize v1.1 backtest CSVs to the ML experiment contract."""
    data = frame.copy()
    if "entry_date" not in data and "trade_date" in data:
        data["entry_date"] = data["trade_date"]
    required = {"entry_date", "option_return"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"trade table missing columns: {sorted(missing)}")
    data["trade_date"] = parse_trading_date(data["entry_date"])
    if "exit_date" in data:
        data["exit_date"] = parse_trading_date(data["exit_date"])
    if "status" in data:
        data = data[data["status"].isin(["ok", "constructed"])].copy()
    if strategy:
        normalized = STRATEGY_ALIASES.get(strategy.lower())
        if normalized is None:
            raise ValueError(f"unknown strategy: {strategy}")
        data["strategy"] = normalized
    elif "strategy" not in data:
        data["strategy"] = "unknown"
    data["option_return"] = pd.to_numeric(data["option_return"], errors="coerce")
    return data.dropna(subset=["trade_date", "option_return"]).reset_index(drop=True)


def add_path_labels(
    trades: pd.DataFrame,
    marks: pd.DataFrame,
    *,
    trade_id_col: str = "trade_id",
    mark_date_col: str = "trade_date",
    mark_return_col: str = "mark_return",
    profit_target: float | None = None,
    stop_loss: float | None = None,
) -> pd.DataFrame:
    """Attach MAE/MFE and, optionally, the first profit/stop barrier hit."""
    required = {trade_id_col, mark_date_col, mark_return_col}
    missing = required.difference(marks.columns)
    if missing:
        raise ValueError(f"mark table missing columns: {sorted(missing)}")
    paths = marks.copy()
    paths[mark_date_col] = parse_trading_date(paths[mark_date_col])
    paths[mark_return_col] = pd.to_numeric(paths[mark_return_col], errors="coerce")
    grouped = paths.sort_values(mark_date_col).groupby(trade_id_col)[mark_return_col]
    labels = grouped.agg(mae="min", mfe="max").reset_index()
    if profit_target is not None or stop_loss is not None:
        def first_hit(series: pd.Series) -> str:
            for value in series.dropna():
                if profit_target is not None and value >= profit_target:
                    return "profit_target"
                if stop_loss is not None and value <= stop_loss:
                    return "stop_loss"
            return "neither"

        barriers = grouped.apply(first_hit).rename("first_barrier").reset_index()
        labels = labels.merge(barriers, on=trade_id_col, how="left")
    return trades.merge(labels, on=trade_id_col, how="left")
