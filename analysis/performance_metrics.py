"""
Performance Metrics Module

Standardized evaluation metrics
for quantitative trading strategies.

Metrics included:

- Total Return
- Annualized Return
- Annualized Volatility
- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Win Rate
- Profit Factor
"""


import numpy as np
import pandas as pd


class PerformanceMetrics:
    """
    Calculate performance statistics
    from strategy returns.
    """

    def __init__(
        self,
        returns,
        periods_per_year=252,
        risk_free_rate=0.0,
    ):
        """
        Parameters
        ----------
        returns :
            Strategy return series.

            Accepts:
            - list
            - numpy array
            - pandas Series

        periods_per_year :
            Trading periods per year.
            Default:
            252 trading days.

        risk_free_rate :
            Annual risk-free rate.
            Default:
            0.
        """

        self.returns = (
            pd.Series(returns)
            .dropna()
            .astype(float)
        )

        self.periods_per_year = periods_per_year

        self.risk_free_rate = risk_free_rate


    # --------------------------------------------------
    # Basic Returns
    # --------------------------------------------------

    def total_return(self):
        """
        Cumulative return.
        """

        return (
            np.prod(1 + self.returns)
            - 1
        )


    def annualized_return(self):
        """
        Annualized geometric return.
        """

        n_periods = len(self.returns)

        if n_periods == 0:
            return np.nan


        return (
            (1 + self.total_return())
            **
            (
                self.periods_per_year
                /
                n_periods
            )
            - 1
        )


    # --------------------------------------------------
    # Risk Metrics
    # --------------------------------------------------

    def volatility(self):
        """
        Annualized volatility.
        """

        return (
            self.returns.std()
            *
            np.sqrt(
                self.periods_per_year
            )
        )


    def sharpe_ratio(self):
        """
        Annualized Sharpe ratio.
        """

        excess_return = (
            self.returns.mean()
            -
            self.risk_free_rate
            /
            self.periods_per_year
        )


        std = self.returns.std()


        if std == 0:
            return np.nan


        return (
            excess_return
            /
            std
            *
            np.sqrt(
                self.periods_per_year
            )
        )


    def sortino_ratio(self):
        """
        Annualized Sortino ratio.

        Uses downside deviation only.
        """

        downside = self.returns[
            self.returns < 0
        ]


        downside_std = (
            downside.std()
        )


        if downside_std == 0:
            return np.nan


        excess_return = (
            self.returns.mean()
            -
            self.risk_free_rate
            /
            self.periods_per_year
        )


        return (
            excess_return
            /
            downside_std
            *
            np.sqrt(
                self.periods_per_year
            )
        )


    # --------------------------------------------------
    # Drawdown
    # --------------------------------------------------

    def max_drawdown(self):
        """
        Maximum portfolio drawdown.
        """

        cumulative = (
            1 + self.returns
        ).cumprod()


        running_max = (
            cumulative
            .cummax()
        )


        drawdown = (
            cumulative
            /
            running_max
            - 1
        )


        return drawdown.min()


    # --------------------------------------------------
    # Trade Statistics
    # --------------------------------------------------

    def win_rate(self):
        """
        Percentage of positive return periods.
        """

        return (
            self.returns.gt(0)
            .mean()
        )


    def profit_factor(self):
        """
        Gross profit / gross loss.
        """

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
    # Summary
    # --------------------------------------------------

    def summary(self):
        """
        Return all metrics.
        """

        return {

            "total_return":
                self.total_return(),

            "annualized_return":
                self.annualized_return(),

            "annualized_volatility":
                self.volatility(),

            "sharpe_ratio":
                self.sharpe_ratio(),

            "sortino_ratio":
                self.sortino_ratio(),

            "max_drawdown":
                self.max_drawdown(),

            "win_rate":
                self.win_rate(),

            "profit_factor":
                self.profit_factor(),
        }