"""
Trade Metrics Module

Metrics calculated on trade-level basis.

Different from PerformanceMetrics:

PerformanceMetrics:
    return series based
    assumes each return is one period

TradeMetrics:
    option trade based
    each return represents one completed trade
"""


import pandas as pd
import numpy as np



class TradeMetrics:


    def __init__(
        self,
        trades: pd.DataFrame,
        return_column: str = "realized_return",
    ):

        self.trades = trades.copy()


        # ==========================================
        # Determine return column
        # ==========================================

        if return_column not in self.trades.columns:

            # backward compatibility
            if (
                return_column == "realized_return"
                and "option_return" in self.trades.columns
            ):

                return_column = "option_return"

            else:

                raise ValueError(
                    f"Missing return column: {return_column}"
                )


        self.return_column = return_column



        # ==========================================
        # Keep trades with valid returns
        #
        # Status filtering is handled upstream
        # by TradePerformanceAdapter
        # ==========================================

        self.trades = self.trades[
            self.trades[self.return_column]
            .notna()
        ].copy()



        self.returns = (
            self.trades[self.return_column]
            .astype(float)
        )



    # --------------------------------------------------
    # Basic Trade Statistics
    # --------------------------------------------------

    def total_trades(self):

        return len(self.trades)



    def win_rate(self):

        if len(self.returns) == 0:
            return np.nan

        return (
            self.returns > 0
        ).mean()



    def average_return(self):

        if len(self.returns) == 0:
            return np.nan

        return self.returns.mean()



    def median_return(self):

        if len(self.returns) == 0:
            return np.nan

        return self.returns.median()



    # --------------------------------------------------
    # Holding Period
    # --------------------------------------------------

    def average_holding_days(self):

        if "holding_days" not in self.trades.columns:

            return np.nan


        return (
            self.trades["holding_days"]
            .mean()
        )



    # --------------------------------------------------
    # Win / Loss Analysis
    # --------------------------------------------------

    def average_win(self):

        wins = self.returns[
            self.returns > 0
        ]

        if len(wins) == 0:
            return np.nan

        return wins.mean()



    def average_loss(self):

        losses = self.returns[
            self.returns < 0
        ]

        if len(losses) == 0:
            return np.nan

        return losses.mean()



    def profit_factor(self):

        gains = (
            self.returns[
                self.returns > 0
            ]
            .sum()
        )


        losses = abs(
            self.returns[
                self.returns < 0
            ]
            .sum()
        )


        if losses == 0:

            return np.inf


        return gains / losses



    # --------------------------------------------------
    # Trade Frequency
    # --------------------------------------------------

    def trades_per_year(
        self,
        trading_days=252,
    ):

        if "holding_days" not in self.trades.columns:

            return np.nan


        avg_days = (
            self.average_holding_days()
        )


        if avg_days <= 0:

            return np.nan


        return trading_days / avg_days



    # --------------------------------------------------
    # Trade Sequence Annualized Return
    # --------------------------------------------------

    def annualized_return(
        self,
        trading_days=252,
    ):

        """
        CAGR based on sequential trades.

        Example:

        Initial capital = 1

        Trade 1:
            capital *= (1+r1)

        Trade 2:
            capital *= (1+r2)

        Annualize based on total holding period.
        """


        if len(self.returns) == 0:

            return np.nan


        if "holding_days" not in self.trades.columns:

            return np.nan


        total_return = (
            (1 + self.returns)
            .prod()
            -
            1
        )


        total_days = (
            self.trades["holding_days"]
            .sum()
        )


        if total_days <= 0:

            return np.nan


        years = (
            total_days
            /
            trading_days
        )


        return (
            (1 + total_return)
            **
            (1 / years)
            -
            1
        )



    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):

        return {

            "trade_count":
                self.total_trades(),


            "win_rate":
                self.win_rate(),


            "average_return":
                self.average_return(),


            "median_return":
                self.median_return(),


            "average_holding_days":
                self.average_holding_days(),


            "trades_per_year":
                self.trades_per_year(),


            "annualized_return":
                self.annualized_return(),


            "average_win":
                self.average_win(),


            "average_loss":
                self.average_loss(),


            "profit_factor":
                self.profit_factor(),

        }