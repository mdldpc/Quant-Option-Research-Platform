"""
Equity Curve Based Risk Report
"""


from pathlib import Path

import pandas as pd
import numpy as np



class EquityRiskReport:



    def __init__(
        self,
        equity_files,
    ):

        self.equity_files = equity_files



    def _max_drawdown(
        self,
        equity,
    ):


        peak = equity.cummax()

        dd = (
            equity / peak
            -
            1
        )

        return dd.min()



    def generate(self):


        results=[]



        for strategy, file in self.equity_files.items():


            df = pd.read_csv(
                file
            )


            returns = df[
                "daily_return"
            ]


            equity = df[
                "equity"
            ]



            total_return = (

                equity.iloc[-1]

                -

                1

            )


            annual_return = (

                equity.iloc[-1]

                **

                (
                    252 /
                    len(df)
                )

                -

                1

            )


            volatility = (

                returns.std()

                *

                np.sqrt(252)

            )


            sharpe=np.nan


            if returns.std()!=0:

                sharpe=(

                    returns.mean()

                    /

                    returns.std()

                    *

                    np.sqrt(252)

                )



            results.append(

                {

                "strategy":
                strategy,


                "days":
                len(df),


                "total_return":
                total_return,


                "annual_return":
                annual_return,


                "volatility":
                volatility,


                "sharpe_ratio":
                sharpe,


                "max_drawdown":

                self._max_drawdown(
                    equity
                ),

                }

            )



        return pd.DataFrame(results)