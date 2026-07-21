import pandas as pd

from framework.strategy.backtest_base import BaseBacktester



class StraddleBacktester(BaseBacktester):

    strategy_name = "long_atm_straddle"

    display_name = "Long ATM Straddle v1.0"



    def run(self) -> pd.DataFrame:
        """
        Simple long straddle backtest.

        Expected columns:

        entry_straddle_price
        exit_straddle_price
        status

        """


        rows = []


        for _, trade in self.trades.copy().iterrows():


            if trade["status"] != "constructed":

                rows.append(
                    {
                        **trade.to_dict(),

                        "status":
                            trade["status"],

                        "option_pnl":
                            None,

                        "option_return":
                            None,
                    }
                )

                continue



            entry_price = (
                trade["entry_straddle_price"]
            )


            exit_price = (
                trade["exit_straddle_price"]
            )



            if (
                pd.isna(entry_price)
                or
                pd.isna(exit_price)
                or
                entry_price <= 0
            ):

                status = "invalid_price"

                pnl = None

                ret = None


            else:

                status = "ok"

                pnl = (
                    exit_price
                    -
                    entry_price
                )

                ret = (
                    pnl
                    /
                    entry_price
                )



            rows.append(
                {
                    **trade.to_dict(),

                    "status":
                        status,

                    "option_pnl":
                        pnl,

                    "option_return":
                        ret,
                }
            )



        return pd.DataFrame(rows)