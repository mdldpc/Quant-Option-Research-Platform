"""
Portfolio Valuation

Convert strategy trades into
daily mark-to-market NAV series.
"""


import pandas as pd



class StrategyValuator:



    PRICE_COLUMN = {


        "long_atm_strangle":
            (
                "entry_strangle_price",
                "exit_strangle_price",
                "strangle_price",
            ),


        "long_call_butterfly":
            (
                "entry_butterfly_price",
                "exit_butterfly_price",
                "butterfly_price",
            ),


        "calendar_spread":
            (
                "entry_calendar_price",
                "exit_calendar_price",
                "calendar_price",
            ),

    }



    def __init__(
        self,
        snapshot,
    ):

        self.snapshot = snapshot.copy()

        self.snapshot[
            "trade_date"
        ] = (
            self.snapshot[
                "trade_date"
            ]
            .astype(str)
        )



    def value_trade(
        self,
        trade,
    ):


        strategy = trade["strategy"]


        entry_col, exit_col, price_col = (
            self.PRICE_COLUMN[strategy]
        )



        entry_date = str(
            int(trade["entry_date"])
        )


        exit_date = str(
            int(trade["exit_date"])
        )


        entry_price = trade[
            entry_col
        ]



        data = self.snapshot[

            (
                self.snapshot["trade_date"]
                >=
                entry_date
            )

            &

            (
                self.snapshot["trade_date"]
                <=
                exit_date
            )

        ].copy()



        if data.empty:

            return pd.DataFrame()



        data["nav"] = (

            data[price_col]

            /

            entry_price

        )



        data["trade_id"] = (
            trade["trade_id"]
        )


        data["strategy"] = strategy


        return data[
            [
                "trade_date",
                "nav",
                "trade_id",
                "strategy",
            ]
        ]