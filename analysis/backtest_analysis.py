"""
Backtest Analysis Module

Provides standardized analysis
for quantitative strategy backtests.

Combines:

- Trade statistics
- Performance metrics
"""


import pandas as pd

from analysis.performance_metrics import (
    PerformanceMetrics,
)


class BacktestAnalyzer:
    """
    Analyze backtest results.

    Parameters
    ----------
    trades : pandas.DataFrame

        Backtest trade result table.

    return_column : str

        Column containing trade returns.

    """


    def __init__(
        self,
        trades,
        return_column="net_return",
    ):

        self.trades = trades.copy()

        self.return_column = return_column


        if self.return_column not in self.trades.columns:
            raise ValueError(
                f"Missing return column: {self.return_column}"
            )


        self.returns = (
            self.trades[self.return_column]
            .dropna()
            .astype(float)
        )



    # --------------------------------------------------
    # Performance Metrics
    # --------------------------------------------------

    def performance(self):
        """
        Calculate performance metrics.
        """

        metrics = PerformanceMetrics(
            self.returns
        )

        return metrics.summary()



    # --------------------------------------------------
    # Trade Statistics
    # --------------------------------------------------

    def trade_statistics(self):
        """
        Calculate trade-level statistics.
        """

        total_trades = len(
            self.trades
        )


        winning_trades = (
            self.returns > 0
        ).sum()


        losing_trades = (
            self.returns < 0
        ).sum()


        return {

            "num_trades":
                total_trades,


            "winning_trades":
                int(winning_trades),


            "losing_trades":
                int(losing_trades),


            "win_rate":
                (
                    winning_trades
                    /
                    total_trades
                    if total_trades > 0
                    else 0
                ),

        }



    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):
        """
        Return complete backtest analysis.
        """

        return {

            "performance":
                self.performance(),


            "trade_statistics":
                self.trade_statistics(),

        }