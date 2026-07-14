from pathlib import Path
import pandas as pd

from framework.data.loader import DataLoader


def load_trade_file(path: Path) -> pd.DataFrame:
    df = DataLoader.read_csv(path)
    df["entry_date"] = df["entry_date"].astype(int)
    df["exit_date"] = df["exit_date"].astype(int)
    return df


def load_snapshot(path: Path) -> pd.DataFrame:
    df = DataLoader.read_parquet(path)
    df["trade_date"] = df["trade_date"].astype(int)
    return df


def open_trades_on(trades: pd.DataFrame, trade_date: int) -> pd.DataFrame:
    trade_date = int(trade_date)

    x = trades[
        (trades["status"] == "constructed")
        & (trades["entry_date"] <= trade_date)
        & (trades["exit_date"] >= trade_date)
    ].copy()

    return x.reset_index(drop=True)


def _match_strangle_position(trade, snapshot: pd.DataFrame, trade_date: int):
    expiry = int(trade["expiry_code"])

    x = snapshot[
        (snapshot["trade_date"] == int(trade_date))
        & (snapshot["expiry_code"].astype(int) == expiry)
    ]

    if x.empty:
        return None

    row = x.iloc[-1].to_dict()
    row["strategy"] = "long_atm_strangle"
    row["source_trade_id"] = trade["trade_id"]
    row["position_status"] = "open"

    row["entry_price"] = trade.get("entry_strangle_price")
    row["entry_trade_date"] = trade.get("entry_date")
    row["exit_trade_date"] = trade.get("exit_date")

    return row


def _match_butterfly_position(trade, snapshot: pd.DataFrame, trade_date: int):
    expiry = int(trade["expiry_code"])

    x = snapshot[
        (snapshot["trade_date"] == int(trade_date))
        & (snapshot["expiry_code"].astype(int) == expiry)
    ]

    if x.empty:
        return None

    row = x.iloc[-1].to_dict()
    row["strategy"] = "long_call_butterfly"
    row["source_trade_id"] = trade["trade_id"]
    row["position_status"] = "open"

    row["entry_price"] = trade.get("entry_butterfly_price")
    row["entry_trade_date"] = trade.get("entry_date")
    row["exit_trade_date"] = trade.get("exit_date")

    return row


def _match_calendar_position(trade, snapshot: pd.DataFrame, trade_date: int):
    near_expiry = int(trade["near_expiry"])
    next_expiry = int(trade["next_expiry"])

    x = snapshot[
        (snapshot["trade_date"] == int(trade_date))
        & (snapshot["near_expiry"].astype(int) == near_expiry)
        & (snapshot["next_expiry"].astype(int) == next_expiry)
    ]

    if x.empty:
        return None

    row = x.iloc[-1].to_dict()
    row["strategy"] = "calendar_spread"
    row["source_trade_id"] = trade["trade_id"]
    row["position_status"] = "open"

    entry_price = trade.get("entry_calendar_price")
    row["entry_price"] = abs(entry_price) if pd.notna(entry_price) else entry_price
    row["entry_trade_date"] = trade.get("entry_date")
    row["exit_trade_date"] = trade.get("exit_date")

    return row


def build_positions_for_strategy(
    strategy_name: str,
    trade_file: Path,
    snapshot_file: Path,
    trade_date: int,
) -> pd.DataFrame:
    trades = load_trade_file(trade_file)
    snapshot = load_snapshot(snapshot_file)

    open_trades = open_trades_on(trades, trade_date)

    rows = []

    for _, trade in open_trades.iterrows():
        if strategy_name == "long_atm_strangle":
            row = _match_strangle_position(trade, snapshot, trade_date)
        elif strategy_name == "long_call_butterfly":
            row = _match_butterfly_position(trade, snapshot, trade_date)
        elif strategy_name == "calendar_spread":
            row = _match_calendar_position(trade, snapshot, trade_date)
        else:
            raise KeyError(f"Unknown strategy: {strategy_name}")

        if row is not None:
            rows.append(row)

    return pd.DataFrame(rows)


def build_portfolio_positions(
    strategy_configs: dict,
    trade_date: int,
) -> pd.DataFrame:
    frames = []

    for strategy_name, cfg in strategy_configs.items():
        frame = build_positions_for_strategy(
            strategy_name=strategy_name,
            trade_file=cfg["trade_output"],
            snapshot_file=cfg["snapshot"],
            trade_date=trade_date,
        )

        if not frame.empty:
            frames.append(frame)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)