import pandas as pd

from framework.strategy.backtest_base import BaseBacktester


class CalendarBacktester(BaseBacktester):
    strategy_name = "calendar_spread"
    display_name = "Calendar Spread v1.1"

    def run(self) -> pd.DataFrame:
        rows = []

        for _, trade in self.trades.copy().iterrows():
            if trade["status"] != "constructed":
                rows.append({
                    **trade.to_dict(),
                    "status": trade["status"],
                    "option_pnl": None,
                    "option_return": None,
                })
                continue

            entry_price = trade["entry_calendar_price"]
            exit_price = trade["exit_calendar_price"]
            capital_base = abs(entry_price)

            if (
                pd.isna(entry_price)
                or pd.isna(exit_price)
                or capital_base <= 0
            ):
                status = "invalid_price"
                pnl = None
                ret = None
            else:
                status = "ok"
                pnl = exit_price - entry_price
                ret = pnl / capital_base

            rows.append({
                **trade.to_dict(),
                "status": status,
                "option_pnl": pnl,
                "option_return": ret,
            })

        return pd.DataFrame(rows)