"""
Portfolio Performance Module

Calculate portfolio-level performance
from strategy return matrix and weights.


Input:

Strategy return matrix:

date | strategy_A | strategy_B | strategy_C


Weights:

strategy_A    0.4
strategy_B    0.3
strategy_C    0.3


Output:

portfolio daily return

portfolio equity curve

"""


import pandas as pd
import numpy as np



class PortfolioPerformance:



    def __init__(
        self,
        returns: pd.DataFrame,
        weights: pd.Series,
    ):


        self.returns = returns.copy()


        self.weights = weights.copy()



        # Remove date column if exists

        if "trade_date" in self.returns.columns:

            self.returns = (

                self.returns

                .set_index(
                    "trade_date"
                )

            )



        # Ensure same order

        self.weights = (

            self.weights

            .reindex(
                self.returns.columns
            )

        )



        if self.weights.isna().any():

            raise ValueError(

                "Weights and returns columns do not match"

            )



        # Check weights

        if abs(
            self.weights.sum()-1
        ) > 1e-8:

            raise ValueError(

                "Portfolio weights must sum to 1"

            )



    # =================================================
    # Daily Portfolio Return
    # =================================================


    def calculate_daily_return(self):


        portfolio_return = (

            self.returns

            .mul(
                self.weights,
                axis=1
            )

            .sum(
                axis=1
            )

        )


        portfolio_return.name = (

            "portfolio_return"

        )


        return portfolio_return



    # =================================================
    # Equity Curve
    # =================================================


    def calculate_equity_curve(
        self,
        initial_value=1.0,
    ):


        daily_return = (

            self.calculate_daily_return()

        )


        equity = (

            1
            +
            daily_return

        ).cumprod()



        equity = (

            equity
            *
            initial_value

        )


        result = pd.DataFrame(

            {

                "portfolio_return":
                daily_return,


                "equity":
                equity,

            }

        )


        return result



    # =================================================
    # Performance Summary v1.2
    #
    # Annualization adjusted for option strategies
    # =================================================


    def summary(
        self,
        trading_days=252,
        risk_free_rate=0.0,
    ):


        returns = (

            self.calculate_daily_return()

        )


        # =================================================
        # Calendar Performance
        # =================================================


        total_return = (

            (1 + returns)

            .prod()

            -

            1

        )


        # ---------------------------------------------
        # Annualized return
        #
        # Use arithmetic annualization
        #
        # mean daily return * 252
        #
        # More suitable for sparse option strategies
        # ---------------------------------------------


        annual_return = (

            returns.mean()

            *

            trading_days

        )



        # ---------------------------------------------
        # Volatility
        # ---------------------------------------------


        volatility = (

            returns.std()

            *

            np.sqrt(
                trading_days
            )

        )



        # ---------------------------------------------
        # Sharpe Ratio
        # ---------------------------------------------


        if volatility != 0:


            sharpe = (

                annual_return

                -

                risk_free_rate

            ) / volatility


        else:

            sharpe = np.nan



        # ---------------------------------------------
        # Maximum Drawdown
        # ---------------------------------------------


        equity = (

            self.calculate_equity_curve()

            [
                "equity"
            ]

        )


        drawdown = (

            equity

            /

            equity.cummax()

            -

            1

        )


        max_drawdown = (

            drawdown.min()

        )



        # =================================================
        # Active Performance
        # =================================================


        active_returns = returns[

            returns != 0

        ]



        if len(active_returns) > 0:


            active_total_return = (

                (1 + active_returns)

                .prod()

                -

                1

            )


            active_annual_return = (

                active_returns.mean()

                *

                trading_days

            )


            active_volatility = (

                active_returns.std()

                *

                np.sqrt(
                    trading_days
                )

            )


            if active_volatility != 0:


                active_sharpe = (

                    active_annual_return

                    -

                    risk_free_rate

                ) / active_volatility


            else:

                active_sharpe = np.nan



        else:


            active_total_return = np.nan

            active_annual_return = np.nan

            active_volatility = np.nan

            active_sharpe = np.nan



        return {


            # -----------------------------
            # Calendar metrics
            # -----------------------------


            "total_return":

            total_return,


            "annual_return":

            annual_return,


            "volatility":

            volatility,


            "sharpe_ratio":

            sharpe,


            "max_drawdown":

            max_drawdown,



            # -----------------------------
            # Active metrics
            # -----------------------------


            "active_days":

            len(active_returns),


            "active_total_return":

            active_total_return,


            "active_annual_return":

            active_annual_return,


            "active_volatility":

            active_volatility,


            "active_sharpe":

            active_sharpe,

        }