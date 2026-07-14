import pandas as pd

from framework.strategy.constructor_base import BaseTradeConstructor


class StrangleTradeConstructor(BaseTradeConstructor):
    constructor_version = "v1_1"
    strategy_name = "long_atm_strangle"

    def __init__(self, snapshot: pd.DataFrame):
        super().__init__(snapshot)

    def select_entry_contract(self, entry_date: int):
        available = self.available_on(entry_date)

        if available.empty:
            return None

        return available.sort_values(["T", "expiry_code"]).iloc[0]

    def validate_trade(self, trade: dict) -> dict:
        if (
            trade.get("status") == "constructed"
            and trade.get("entry_strangle_price") is not None
            and trade.get("entry_strangle_price") <= 0
        ):
            trade["status"] = "invalid_entry_price"

        return trade

    def build_trade(self, signal_row, trade_id: int) -> dict:
        entry_date = int(signal_row["entry_date"])
        exit_date = int(signal_row["exit_date"])

        entry_contract = self.select_entry_contract(entry_date)

        if entry_contract is None:
            return {
                "trade_id": trade_id,
                "strategy": self.strategy_name,
                "status": "no_entry_snapshot",
                "entry_date": entry_date,
                "exit_date": exit_date,
                "constructor_version": self.constructor_version,
                "construction_reason": "no_snapshot_available_on_entry_date",
            }

        expiry = int(entry_contract["expiry_code"])

        exit_available = self.snapshot[
            (self.snapshot["trade_date"] == exit_date)
            & (self.snapshot["expiry_code"] == expiry)
        ]

        if exit_available.empty:
            status = "contract_expired"
            exit_price = None
        else:
            status = "constructed"
            exit_price = exit_available.iloc[-1]["strangle_price"]

        return {
            "trade_id": trade_id,
            "strategy": self.strategy_name,
            "status": status,

            "entry_date": entry_date,
            "exit_date": exit_date,
            "holding_days": signal_row.get("holding_days"),

            "expiry_code": expiry,

            "entry_call_strike": entry_contract.get("call_strike"),
            "entry_put_strike": entry_contract.get("put_strike"),
            "entry_strangle_price": entry_contract.get("strangle_price"),

            "exit_strangle_price": exit_price,

            "entry_signal_score": signal_row.get("entry_signal_score"),
            "exit_signal_score": signal_row.get("exit_signal_score"),
            "exit_reason": signal_row.get("exit_reason"),

            "constructor_version": self.constructor_version,
            "construction_reason": "nearest_available_expiry_from_entry_snapshot",
        }


class ButterflyTradeConstructor(BaseTradeConstructor):
    constructor_version = "v1_1"
    strategy_name = "long_call_butterfly"

    def __init__(self, snapshot: pd.DataFrame, min_premium: float = 1.0):
        super().__init__(snapshot)
        self.min_premium = min_premium

    def available_on(self, trade_date: int) -> pd.DataFrame:
        available = super().available_on(trade_date)

        return available[
            available["butterfly_price"] >= self.min_premium
        ].copy()

    def select_entry_contract(self, entry_date: int):
        available = self.available_on(entry_date)

        if available.empty:
            return None

        return available.sort_values(["T", "expiry_code"]).iloc[0]

    def validate_trade(self, trade: dict) -> dict:
        if (
            trade.get("status") == "constructed"
            and trade.get("entry_butterfly_price") is not None
            and trade.get("entry_butterfly_price") < self.min_premium
        ):
            trade["status"] = "below_minimum_premium"

        return trade

    def build_trade(self, signal_row, trade_id: int) -> dict:
        entry_date = int(signal_row["entry_date"])
        exit_date = int(signal_row["exit_date"])

        entry_contract = self.select_entry_contract(entry_date)

        if entry_contract is None:
            return {
                "trade_id": trade_id,
                "strategy": self.strategy_name,
                "status": "no_entry_snapshot",
                "entry_date": entry_date,
                "exit_date": exit_date,
                "constructor_version": self.constructor_version,
                "construction_reason": "no_valid_butterfly_on_entry_date",
                "min_premium": self.min_premium,
            }

        expiry = int(entry_contract["expiry_code"])

        exit_available = self.snapshot[
            (self.snapshot["trade_date"] == exit_date)
            & (self.snapshot["expiry_code"] == expiry)
        ]

        if exit_available.empty:
            status = "contract_expired"
            exit_price = None
        else:
            status = "constructed"
            exit_price = exit_available.iloc[-1]["butterfly_price"]

        return {
            "trade_id": trade_id,
            "strategy": self.strategy_name,
            "status": status,

            "entry_date": entry_date,
            "exit_date": exit_date,
            "holding_days": signal_row.get("holding_days"),

            "expiry_code": expiry,

            "entry_lower_strike": entry_contract.get("lower_strike"),
            "entry_middle_strike": entry_contract.get("middle_strike"),
            "entry_upper_strike": entry_contract.get("upper_strike"),
            "entry_butterfly_price": entry_contract.get("butterfly_price"),

            "exit_butterfly_price": exit_price,

            "entry_signal_score": signal_row.get("entry_signal_score"),
            "exit_signal_score": signal_row.get("exit_signal_score"),
            "exit_reason": signal_row.get("exit_reason"),

            "constructor_version": self.constructor_version,
            "construction_reason": "nearest_available_expiry_from_entry_snapshot_min_premium",
            "min_premium": self.min_premium,
        }
  
    
class CalendarTradeConstructor(BaseTradeConstructor):
    constructor_version = "v1_1"
    strategy_name = "calendar_spread"

    def __init__(self, snapshot: pd.DataFrame):
        super().__init__(snapshot)

        self.snapshot["near_expiry"] = self.snapshot["near_expiry"].astype(int)
        self.snapshot["next_expiry"] = self.snapshot["next_expiry"].astype(int)

    def select_entry_contract(self, entry_date: int):
        available = self.available_on(entry_date)

        if available.empty:
            return None

        return available.sort_values(
            ["near_T", "next_T", "near_expiry", "next_expiry"]
        ).iloc[0]

    def validate_trade(self, trade: dict) -> dict:
        if (
            trade.get("status") == "constructed"
            and trade.get("capital_base") is not None
            and trade.get("capital_base") <= 0
        ):
            trade["status"] = "invalid_capital_base"

        return trade

    def build_trade(self, signal_row, trade_id: int) -> dict:
        entry_date = int(signal_row["entry_date"])
        exit_date = int(signal_row["exit_date"])

        entry_contract = self.select_entry_contract(entry_date)

        if entry_contract is None:
            return {
                "trade_id": trade_id,
                "strategy": self.strategy_name,
                "status": "no_entry_snapshot",
                "entry_date": entry_date,
                "exit_date": exit_date,
                "constructor_version": self.constructor_version,
                "construction_reason": "no_calendar_pair_on_entry_date",
            }

        near_expiry = int(entry_contract["near_expiry"])
        next_expiry = int(entry_contract["next_expiry"])

        exit_available = self.snapshot[
            (self.snapshot["trade_date"] == exit_date)
            & (self.snapshot["near_expiry"] == near_expiry)
            & (self.snapshot["next_expiry"] == next_expiry)
        ]

        if exit_available.empty:
            status = "calendar_pair_expired"
            exit_price = None
        else:
            status = "constructed"
            exit_price = exit_available.iloc[-1]["calendar_price"]

        entry_price = entry_contract.get("calendar_price")
        capital_base = abs(entry_price) if entry_price is not None else None

        return {
            "trade_id": trade_id,
            "strategy": self.strategy_name,
            "status": status,

            "entry_date": entry_date,
            "exit_date": exit_date,
            "holding_days": signal_row.get("holding_days"),

            "near_expiry": near_expiry,
            "next_expiry": next_expiry,

            "entry_calendar_price": entry_price,
            "exit_calendar_price": exit_price,
            "capital_base": capital_base,

            "entry_iv_spread": entry_contract.get("iv_spread"),

            "entry_signal_score": signal_row.get("entry_signal_score"),
            "exit_signal_score": signal_row.get("exit_signal_score"),
            "exit_reason": signal_row.get("exit_reason"),

            "constructor_version": self.constructor_version,
            "construction_reason": "nearest_available_calendar_pair_from_entry_snapshot",
        }