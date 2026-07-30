"""
Strategy Return Series Builder

Convert strategy trades into
daily strategy return series.
"""


import pandas as pd


from analysis.portfolio_valuation import (
    StrategyValuator,
)



class StrategyReturnBuilder:



    def __init__(
        self,
        trades,
        snapshot,
    ):

        self.trades = trades.copy()

        self.valuator = StrategyValuator(
            snapshot
        )



    def build(self):


        nav_frames = []


        for _, trade in self.trades.iterrows():


            nav = (
                self.valuator
                .value_trade(
                    trade
                )
            )


            if not nav.empty:

                nav_frames.append(
                    nav
                )



        if not nav_frames:

            return pd.DataFrame()



        all_nav = pd.concat(
            nav_frames
        )


        # -----------------------
        # Equal capital allocation
        # -----------------------

        strategy_nav = (

            all_nav

            .groupby(
                "trade_date"
            )

            ["nav"]

            .mean()

            .reset_index()

        )


        strategy_nav = (
            strategy_nav
            .sort_values(
                "trade_date"
            )
        )


        strategy_nav["return"] = (
            strategy_nav["nav"]
            .pct_change()
            .fillna(0)
        )


        return strategy_nav