"""
Portfolio Allocation Module

Combine different portfolio allocation methods.

Methods:

1. Equal Weight
2. Minimum Variance
3. Maximum Sharpe
4. Risk Parity


Input:

Strategy return matrix


Output:

Strategy weights dataframe

"""


import pandas as pd
import numpy as np


from portfolio_all.portfolio_analysis.portfolio_optimizer import (
    PortfolioOptimizer
)



class PortfolioAllocator:



    def __init__(
        self,
        returns: pd.DataFrame,
        risk_free_rate: float = 0.0,
    ):


        self.returns = returns.copy()


        self.optimizer = PortfolioOptimizer(

            self.returns,

            risk_free_rate=risk_free_rate

        )


        self.strategies = list(

            self.optimizer.strategies

        )



    # =================================================
    # Equal Weight
    # =================================================


    def equal_weight(self):


        n = len(
            self.strategies
        )


        weights = pd.Series(

            np.ones(n) / n,

            index=self.strategies,

            name="weight"

        )


        return weights



    # =================================================
    # Minimum Variance
    # =================================================


    def minimum_variance(self):


        return (

            self.optimizer
            .minimum_variance()

        )



    # =================================================
    # Maximum Sharpe
    # =================================================


    def maximum_sharpe(self):


        return (

            self.optimizer
            .maximum_sharpe()

        )



    # =================================================
    # Risk Parity
    # =================================================


    def risk_parity(self):


        return (

            self.optimizer
            .risk_parity()

        )



    # =================================================
    # Generate Allocation Table
    # =================================================


    def generate_allocation_table(self):


        result = pd.DataFrame(

            {

                "equal_weight":
                self.equal_weight(),


                "minimum_variance":
                self.minimum_variance(),


                "maximum_sharpe":
                self.maximum_sharpe(),


                "risk_parity":
                self.risk_parity(),

            }

        )


        return result