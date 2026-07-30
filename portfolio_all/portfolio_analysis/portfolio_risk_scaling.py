"""
Portfolio Risk Scaling Module v1.0

Apply volatility targeting to portfolio returns.


Input:

portfolio daily return series


Output:

scaled portfolio return series


Formula:

scale =
target_vol / realized_vol


scaled_return =
return * scale

"""


import pandas as pd
import numpy as np



class PortfolioRiskScaler:



    def __init__(
        self,
        returns: pd.Series,
        target_volatility: float = 0.15,
        trading_days: int = 252,
    ):


        self.returns = returns.copy()


        self.target_volatility = (
            target_volatility
        )


        self.trading_days = (
            trading_days
        )



    # =================================================
    # Calculate realized volatility
    # =================================================


    def realized_volatility(self):


        return (

            self.returns.std()

            *

            np.sqrt(
                self.trading_days
            )

        )



    # =================================================
    # Scaling factor
    # =================================================


    def scaling_factor(self):


        realized_vol = (

            self.realized_volatility()

        )


        if realized_vol == 0:

            return 0


        return (

            self.target_volatility

            /

            realized_vol

        )



    # =================================================
    # Apply scaling
    # =================================================


    def scale_returns(self):


        factor = (

            self.scaling_factor()

        )


        scaled = (

            self.returns

            *

            factor

        )


        scaled.name = (

            "scaled_portfolio_return"

        )


        return scaled



    # =================================================
    # Equity Curve
    # =================================================


    def equity_curve(
        self,
        initial_value=1.0,
    ):


        returns = (

            self.scale_returns()

        )


        equity = (

            (1 + returns)

            .cumprod()

            *

            initial_value

        )


        return pd.DataFrame(

            {

                "return":
                returns,


                "equity":
                equity,

            }

        )



    # =================================================
    # Summary
    # =================================================


    def summary(self):


        returns = (

            self.scale_returns()

        )


        equity = (

            self.equity_curve()

            [
                "equity"
            ]

        )


        total_return = (

            equity.iloc[-1]

            -

            1

        )


        volatility = (

            returns.std()

            *

            np.sqrt(
                self.trading_days
            )

        )


        annual_return = (

            returns.mean()

            *

            self.trading_days

        )


        sharpe = (

            annual_return

            /

            volatility

        )


        drawdown = (

            equity

            /

            equity.cummax()

            -

            1

        )


        return {


            "total_return":

            total_return,


            "annual_return":

            annual_return,


            "volatility":

            volatility,


            "sharpe_ratio":

            sharpe,


            "max_drawdown":

            drawdown.min(),


            "scaling_factor":

            self.scaling_factor(),

        }