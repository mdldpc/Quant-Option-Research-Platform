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

        total_trades = len(self.trades)


        completed_trades = (
            self.trades["status"]
            == "ok"
        ).sum()


        skipped_trades = (
            total_trades
            -
            completed_trades
        )


        return {

            "total_trades":
                total_trades,


            "completed_trades":
                int(completed_trades),


            "skipped_trades":
                int(skipped_trades),


            "win_rate":
                float(
                    (self.returns > 0).mean()
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
            {
                **self.performance(),

                **self.equity_statistics(),
            },


            "trade_statistics":
                self.trade_statistics(),

        }
    
    def equity_statistics(self):
        """
        Calculate equity related statistics.
        """

        equity = (
            1 + self.returns
        ).cumprod()


        return {

            "final_equity":
                float(equity.iloc[-1]),


            "average_return":
                float(self.returns.mean()),

        }