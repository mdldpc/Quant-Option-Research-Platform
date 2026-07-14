import pandas as pd


class BaseTradeConstructor:
    """
    Base class for all trade constructors.

    Provides:
    - Snapshot filtering
    - Trade iteration
    - Common validation hooks
    """

    constructor_version = "v1_1"
    strategy_name = "base_strategy"

    def __init__(self, snapshot: pd.DataFrame):
        self.snapshot = snapshot.copy()

        self.snapshot["trade_date"] = self.snapshot["trade_date"].astype(int)

        if "expiry_code" in self.snapshot.columns:
            self.snapshot["expiry_code"] = self.snapshot["expiry_code"].astype(int)

    # -----------------------------
    # Core utilities
    # -----------------------------

    def available_on(self, trade_date: int) -> pd.DataFrame:
        """
        Return snapshot rows available on a given trade date.
        """
        return self.snapshot[self.snapshot["trade_date"] == int(trade_date)].copy()

    def validate_trade(self, trade: dict) -> dict:
        """
        Basic validation hook.

        Can be overridden in subclasses.
        """
        return trade

    # -----------------------------
    # Build interface
    # -----------------------------

    def build_all(self, signals: pd.DataFrame) -> pd.DataFrame:
        """
        Iterate over signals and build trades.
        """
        rows = []

        for i, row in signals.reset_index(drop=True).iterrows():
            trade = self.build_trade(row, trade_id=i + 1)
            trade = self.validate_trade(trade)
            rows.append(trade)

        return pd.DataFrame(rows)

    # -----------------------------
    # Must override
    # -----------------------------

    def build_trade(self, signal_row, trade_id: int) -> dict:
        """
        Must be implemented in subclass.
        """
        raise NotImplementedError("build_trade must be implemented in subclass")