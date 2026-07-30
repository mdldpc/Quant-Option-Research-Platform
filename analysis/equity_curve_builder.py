"""
Equity Curve Builder v1.2

Build daily equity curve from
standardized trade performance.

Input:
    backtest trade dataframe

Process:
    TradePerformanceAdapter
        |
        v
    realized_return

Output:
    date
    equity
    daily_return
"""


import pandas as pd
import numpy as np


from analysis.trade_performance_adapter import (
    TradePerformanceAdapter,
)



class EquityCurveBuilder:



    def __init__(
        self,
        trades,
        strategy_name=None,
    ):

        self.trades = trades.copy()

        self.strategy_name = strategy_name



    # =========================================
    # Build
    # =========================================

    def build(self):


        # -------------------------------------
        # Convert to standardized performance
        # -------------------------------------

        if "strategy" in self.trades.columns:

            trades = (
                TradePerformanceAdapter
                .adapt(
                    self.trades
                )
            )

        else:

            trades = self.trades.copy()

            trades["realized_return"] = (

                trades["exit_price"]

                -

                trades["entry_price"]

            ) / trades["entry_price"]



        # -------------------------------------
        # Keep trades with realized return
        # -------------------------------------

        trades = trades[

            trades["realized_return"]

            .notna()

        ].copy()



        if trades.empty:

            raise ValueError(
                "No valid realized trades"
            )



        # -------------------------------------
        # Date range
        # -------------------------------------

        start = int(

            trades["entry_date"]

            .min()

        )


        end = int(

            trades["exit_date"]

            .max()

        )



        dates = pd.date_range(

            start=str(start),

            end=str(end),

            freq="B"

        )



        curve = pd.DataFrame(

            {

                "date":
                dates

            }

        )



        curve["date_int"] = (

            curve["date"]

            .dt.strftime("%Y%m%d")

            .astype(int)

        )



        curve["equity"] = 1.0



        # -------------------------------------
        # Apply trade returns
        # -------------------------------------

        equity = 1.0



        for _, trade in trades.iterrows():


            trade_return = float(

                trade["realized_return"]

            )


            exit_date = int(

                trade["exit_date"]

            )



            equity *= (

                1

                +

                trade_return

            )



            curve.loc[

                curve["date_int"]

                >=

                exit_date,

                "equity"

            ] = equity



        # -------------------------------------
        # Daily return
        # -------------------------------------

        curve["daily_return"] = (

            curve["equity"]

            .pct_change()

            .fillna(0)

        )



        return curve[

            [

                "date",

                "equity",

                "daily_return",

            ]

        ]