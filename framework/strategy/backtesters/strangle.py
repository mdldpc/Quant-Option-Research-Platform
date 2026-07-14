import pandas as pd

from framework.strategy.backtest_base import BaseBacktester


class StrangleBacktester(BaseBacktester):
    strategy_name = "long_atm_strangle"
    display_name = "Long ATM Strangle v1.1"

    def run(self) -> pd.DataFrame:
        rows = []

        trades = self.trades.copy()

        for _, trade in trades.iterrows():
            if trade["status"] != "constructed":
                rows.append({
                    **trade.to_dict(),
                    "status": trade["status"],
                    "option_pnl": None,
                    "option_return": None,
                })
                continue

            entry_price = trade["entry_strangle_price"]
            exit_price = trade["exit_strangle_price"]

            if pd.isna(entry_price) or pd.isna(exit_price) or entry_price <= 0:
                status = "invalid_price"
                pnl = None
                ret = None
            else:
                status = "ok"
                pnl = exit_price - entry_price
                ret = pnl / entry_price

            rows.append({
                **trade.to_dict(),
                "status": status,
                "option_pnl": pnl,
                "option_return": ret,
            })

        return pd.DataFrame(rows)

