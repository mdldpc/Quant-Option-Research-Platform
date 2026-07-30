"""
Portfolio Metrics

Analyze strategy return matrix.

Outputs:
- correlation matrix
- covariance matrix
- volatility
- equal weight portfolio statistics
"""


import pandas as pd
import numpy as np



class PortfolioMetrics:



    def __init__(
        self,
        return_matrix,
    ):

        self.data = return_matrix.copy()


        self.returns = (
            self.data
            .drop(
                columns=["trade_date"]
            )
        )



    # ==========================================
    # Correlation
    # ==========================================

    def correlation_matrix(self):

        return (
            self.returns
            .corr()
        )



    # ==========================================
    # Covariance
    # ==========================================

    def covariance_matrix(self):

        return (
            self.returns
            .cov()
            *
            252
        )



    # ==========================================
    # Volatility
    # ==========================================

    def volatility(self):

        return (

            self.returns
            .std()
            *
            np.sqrt(252)

        )



    # ==========================================
    # Equal Weight Portfolio
    # ==========================================

    def equal_weight_performance(self):


        weights = np.ones(

            len(
                self.returns.columns
            )

        ) / len(

            self.returns.columns

        )


        portfolio_return = (

            self.returns
            .values
            @
            weights

        )


        result = pd.Series(

            {

            "annual_return":

            portfolio_return.mean()
            *
            252,


            "annual_volatility":

            portfolio_return.std()
            *
            np.sqrt(252),


            "sharpe_ratio":

            (
                portfolio_return.mean()
                /
                portfolio_return.std()
                *
                np.sqrt(252)
            )

            }

        )


        return result