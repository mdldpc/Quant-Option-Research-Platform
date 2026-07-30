"""
Portfolio Optimizer

Research-layer portfolio allocation.

Input:
    Strategy return matrix

Output:
    Portfolio weights


Currently implemented:

1. Minimum Variance Portfolio


Constraints:

sum(weights)=1

weights >= 0

"""


import numpy as np
import pandas as pd

from scipy.optimize import minimize



class PortfolioOptimizer:



    def __init__(
        self,
        returns: pd.DataFrame,
        risk_free_rate: float = 0.0,
    ):

        """
        Parameters
        ----------
        returns :
            Daily strategy return matrix.

            Example:

            date        A       B       C
            20260101    0.1     0       0


        risk_free_rate :
            Annual risk free rate.
        """


        self.returns = returns.copy()

        self.risk_free_rate = risk_free_rate



        if self.returns.empty:

            raise ValueError(
                "Return matrix is empty"
            )



        # Remove date column if exists

        if "trade_date" in self.returns.columns:

            self.returns = (
                self.returns
                .drop(
                    columns=["trade_date"]
                )
            )



        self.strategies = list(
            self.returns.columns
        )



        self.covariance = (
            self.returns
            .cov()
            *
            252
        )

        self.expected_return = (
            self.returns
            .mean()
            *
            252
        )

    # =================================================
    # Minimum Variance Portfolio
    # =================================================


    def minimum_variance(self):


        n = len(
            self.strategies
        )


        cov = (
            self.covariance
            .values
        )



        def portfolio_variance(weights):

            return (
                weights.T
                @
                cov
                @
                weights
            )



        # Initial equal weight

        x0 = np.ones(n) / n



        # Fully invested

        constraints = [

            {
                "type": "eq",

                "fun":
                lambda w:
                np.sum(w)-1

            }

        ]



        # Long only

        bounds = [

            (0,1)

            for _ in range(n)

        ]



        result = minimize(

            portfolio_variance,

            x0,

            method="SLSQP",

            bounds=bounds,

            constraints=constraints,

        )



        if not result.success:

            raise RuntimeError(
                result.message
            )



        weights = pd.Series(

            result.x,

            index=self.strategies,

            name="weight"

        )


        return weights

    # =================================================
    # Maximum Sharpe Portfolio
    # =================================================


    def maximum_sharpe(self):


        n = len(
            self.strategies
        )


        cov = (
            self.covariance
            .values
        )


        expected_returns = (
            self.expected_return
            .values
        )


        rf = (
            self.risk_free_rate
        )



        def negative_sharpe(weights):


            portfolio_return = (
                weights
                @
                expected_returns
            )


            portfolio_variance = (
                weights.T
                @
                cov
                @
                weights
            )


            portfolio_volatility = (
                np.sqrt(
                    portfolio_variance
                )
            )


            if portfolio_volatility == 0:

                return 1e10



            sharpe = (

                portfolio_return
                -
                rf

            ) / portfolio_volatility



            return -sharpe



        # Initial equal weight

        x0 = (
            np.ones(n)
            /
            n
        )



        # Fully invested

        constraints = [

            {
                "type": "eq",

                "fun":
                lambda w:
                np.sum(w)-1

            }

        ]



        # Long only

        bounds = [

            (0,1)

            for _ in range(n)

        ]



        result = minimize(

            negative_sharpe,

            x0,

            method="SLSQP",

            bounds=bounds,

            constraints=constraints,

        )



        if not result.success:

            raise RuntimeError(
                result.message
            )



        weights = pd.Series(

            result.x,

            index=self.strategies,

            name="weight"

        )


        return weights

    # =================================================
    # Risk Parity Portfolio
    # =================================================


    def risk_parity(self):


        n = len(
            self.strategies
        )


        cov = (
            self.covariance
            .values
        )



        def risk_contribution(weights):


            portfolio_variance = (

                weights.T
                @
                cov
                @
                weights

            )


            portfolio_volatility = np.sqrt(
                portfolio_variance
            )


            marginal_contribution = (

                cov
                @
                weights

            ) / portfolio_volatility



            contribution = (

                weights
                *
                marginal_contribution

            )


            return contribution



        def objective(weights):


            contribution = (
                risk_contribution(weights)
            )


            target = (
                np.mean(contribution)
            )


            return np.sum(

                (
                    contribution
                    -
                    target

                )
                **2

            )



        # Initial equal weight

        x0 = (

            np.ones(n)

            /

            n

        )



        # Fully invested

        constraints = [

            {

                "type": "eq",

                "fun":

                lambda w:

                np.sum(w)-1

            }

        ]



        # Long only

        bounds = [

            (0,1)

            for _ in range(n)

        ]



        result = minimize(

            objective,

            x0,

            method="SLSQP",

            bounds=bounds,

            constraints=constraints,

        )



        if not result.success:

            raise RuntimeError(
                result.message
            )



        weights = pd.Series(

            result.x,

            index=self.strategies,

            name="weight"

        )


        return weights