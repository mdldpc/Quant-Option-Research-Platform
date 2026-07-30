"""
Strategy Evaluation

Analyze trade-level performance.

Input:
    Trade dataframe

Output:
    Performance statistics
"""


import pandas as pd
import numpy as np


class StrategyEvaluator:


    def __init__(
        self,
        trades: pd.DataFrame,
        return_column="return",
        holding_column="holding_days",
    ):

        self.trades = trades.copy()

        self.return_column = return_column

        self.holding_column = holding_column

    def _calculate_sortino(
        self,
        returns,
    ):


        downside = returns[
            returns < 0
        ]


        if len(downside) == 0:

            return 0


        downside_std = (
            downside.std()
        )


        if downside_std == 0:

            return 0


        return (
            returns.mean()
            /
            downside_std
        )

    def _calculate_recovery_time(
        self,
        equity_curve,
    ):


        running_max = (
            equity_curve
            .cummax()
        )


        drawdown = (
            equity_curve
            /
            running_max
            - 1
        )


        if drawdown.min() == 0:

            return 0



        max_dd_index = (
            drawdown.idxmin()
        )


        recovery = (
            equity_curve[
                max_dd_index:
            ]
            >=
            running_max[
                max_dd_index
            ]
        )


        if recovery.any():

            return (
                recovery
                .idxmax()
                -
                max_dd_index
            )


        return None

    # --------------------------------------------------
    # Main evaluation interface
    # --------------------------------------------------

    def evaluate(self):


        if self.trades.empty:

            return {

                "total_trades": 0,

                "winning_trades": 0,

                "losing_trades": 0,

                "win_rate": 0,

                "average_return": 0,

                "median_return": 0,

                "total_return": 0,

                "volatility": 0,

                "sharpe_ratio": 0,

                "max_drawdown": 0,

                "profit_factor": None,

                "average_holding_days": 0,

            }



        returns = (
            self.trades[
                self.return_column
            ]
            .astype(float)
        )



        total_trades = len(
            returns
        )



        winning_returns = returns[
            returns > 0
        ]


        losing_returns = returns[
            returns < 0
        ]



        # ----------------------------------------------
        # Equity curve
        # ----------------------------------------------

        equity_curve = (
            (1 + returns)
            .cumprod()
        )


        total_return = (
            equity_curve.iloc[-1]
            - 1
        )



        # ----------------------------------------------
        # Volatility
        # ----------------------------------------------

        volatility = (
            returns.std()
        )



        # ----------------------------------------------
        # Sharpe Ratio
        # rf = 0
        # ----------------------------------------------

        if volatility != 0:

            sharpe_ratio = (
                returns.mean()
                /
                volatility
            )

        else:

            sharpe_ratio = 0



        # ----------------------------------------------
        # Maximum Drawdown
        # ----------------------------------------------

        running_max = (
            equity_curve
            .cummax()
        )


        drawdown = (
            equity_curve
            /
            running_max
            -
            1
        )


        max_drawdown = (
            drawdown.min()
        )

        sortino_ratio = (
            self._calculate_sortino(
                returns
            )
        )


        recovery_time = (
            self._calculate_recovery_time(
                equity_curve
            )
        )


        skewness = (
            returns.skew()
        )


        kurtosis = (
            returns.kurt()
        )

        # ----------------------------------------------
        # Profit Factor
        # ----------------------------------------------

        gross_profit = (
            winning_returns.sum()
        )


        gross_loss = (
            abs(
                losing_returns.sum()
            )
        )



        if gross_loss != 0:

            profit_factor = (
                gross_profit
                /
                gross_loss
            )

        else:

            profit_factor = None



        # ----------------------------------------------
        # Final result
        # ----------------------------------------------

        result = {


            "total_trades":
                total_trades,


            "winning_trades":
                len(
                    winning_returns
                ),


            "losing_trades":
                len(
                    losing_returns
                ),


            "win_rate":
                len(winning_returns)
                /
                total_trades,


            "average_return":
                returns.mean(),


            "median_return":
                returns.median(),


            "total_return":
                total_return,


            "volatility":
                volatility,


            "sharpe_ratio":
                sharpe_ratio,


            "max_drawdown":
                max_drawdown,


            "profit_factor":
                profit_factor,


            "average_holding_days":
                self.trades[
                    self.holding_column
                ].mean(),


            "sortino_ratio":
                sortino_ratio,


            "skewness":
                skewness,


            "kurtosis":
                kurtosis,


            "recovery_time":
                recovery_time,
        }


        return result