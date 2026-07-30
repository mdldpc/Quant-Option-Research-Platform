"""
Improved Strategy Risk Report

Risk attribution for option strategies.

Separates:
- calendar time risk
- active holding risk
"""


import pandas as pd
import numpy as np



class StrategyRiskReport:



    def __init__(
        self,
        return_matrix,
        trade_files,
    ):

        self.return_matrix = (
            return_matrix.copy()
        )

        self.trade_files = trade_files



    # --------------------------------------
    # NAV Drawdown
    # --------------------------------------

    def _max_drawdown(
        self,
        returns,
    ):


        nav = (
            1 + returns
        ).cumprod()


        peak = (
            nav.cummax()
        )


        drawdown = (
            nav / peak - 1
        )


        return drawdown.min()



    # --------------------------------------
    # Main Report
    # --------------------------------------

    def generate(self):


        results = []


        calendar_days = len(
            self.return_matrix
        )



        for strategy in self.trade_files:


            returns = (
                self.return_matrix[
                    strategy
                ]
            )


            active_returns = (
                returns[
                    returns != 0
                ]
            )



            # --------------------------
            # Returns
            # --------------------------

            total_return = (

                (1 + returns)

                .prod()

                -

                1

            )


            annual_return = (

                (1 + total_return)

                **

                (
                    252 /
                    calendar_days
                )

                -

                1

            )



            # --------------------------
            # Volatility
            # --------------------------

            calendar_vol = (

                returns.std()

                *
                np.sqrt(252)

            )


            active_vol = np.nan


            if len(active_returns) > 1:

                active_vol = (

                    active_returns.std()

                    *
                    np.sqrt(252)

                )



            # --------------------------
            # Sharpe
            # --------------------------

            calendar_sharpe = np.nan

            if returns.std() != 0:

                calendar_sharpe = (

                    returns.mean()

                    /

                    returns.std()

                    *
                    np.sqrt(252)

                )



            active_sharpe = np.nan


            if (

                len(active_returns) > 1

                and

                active_returns.std()!=0

            ):


                active_sharpe = (

                    active_returns.mean()

                    /

                    active_returns.std()

                    *
                    np.sqrt(252)

                )



            # --------------------------
            # Drawdown
            # --------------------------

            max_dd = self._max_drawdown(
                returns
            )



            # --------------------------
            # Trades
            # --------------------------

            trades = pd.read_csv(

                self.trade_files[
                    strategy
                ]

            )


            completed = trades[

                trades["status"]

                ==

                "constructed"

            ]



            active_days = int(

                (
                    returns != 0
                )

                .sum()

            )


            results.append(

                {


                "strategy":

                strategy,


                "generated_trades":

                len(trades),



                "completed_trades":

                len(completed),



                "calendar_days":

                calendar_days,



                "active_days":

                active_days,



                "active_ratio":

                active_days
                /
                calendar_days,



                "total_return":

                total_return,



                "annual_return":

                annual_return,



                "calendar_volatility":

                calendar_vol,



                "active_volatility":

                active_vol,



                "calendar_sharpe":

                calendar_sharpe,



                "active_sharpe":

                active_sharpe,



                "max_drawdown":

                max_dd,


                }

            )



        return pd.DataFrame(results)