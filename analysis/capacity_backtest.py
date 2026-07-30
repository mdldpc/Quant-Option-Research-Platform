"""
Capacity Backtest Engine

Compare strategy performance
under different position capacities.

Input:
    raw signals

Output:
    executed trades under capacity constraint
"""


import pandas as pd
import numpy as np



class CapacityBacktester:


    def __init__(
        self,
        signals: pd.DataFrame,
        capacity=1,
    ):

        self.signals = signals.copy()

        self.capacity = capacity


        if len(self.signals):

            self.signals = (
                self.signals
                .sort_values(
                    "entry_idx"
                )
                .reset_index(drop=True)
            )



    # --------------------------------------------------
    # Execute trades under capacity constraint
    # --------------------------------------------------

    def execute(self):


        selected = []


        active_positions = []



        for _, row in self.signals.iterrows():


            entry = row["entry_idx"]

            exit_ = row["exit_idx"]



            # remove expired positions

            active_positions = [

                x for x in active_positions

                if x > entry

            ]



            # unlimited

            if self.capacity is None:

                selected.append(row)

                active_positions.append(
                    exit_
                )

                continue



            # capacity available

            if len(active_positions) < self.capacity:


                selected.append(row)

                active_positions.append(
                    exit_
                )



        if len(selected):

            return pd.DataFrame(
                selected
            )


        return pd.DataFrame(
            columns=self.signals.columns
        )



    # --------------------------------------------------
    # Calculate capacity statistics
    # --------------------------------------------------

    def summarize(
        self,
        trades=None,
    ):


        if trades is None:

            trades = self.execute()



        result = {


            "capacity":

                "unlimited"
                if self.capacity is None
                else self.capacity,


            "raw_opportunities":

                len(self.signals),


            "executed_trades":

                len(trades),

        }



        if "return" in trades.columns:


            returns = (
                trades["return"]
                .astype(float)
            )


            equity = (
                1 + returns
            ).cumprod()



            result.update(

                {


                "final_equity":

                    float(
                        equity.iloc[-1]
                    ),



                "total_return":

                    float(
                        equity.iloc[-1]-1
                    ),



                "average_return":

                    float(
                        returns.mean()
                    ),



                }

            )


        else:


            result.update(

                {

                "final_equity":
                    np.nan,


                "total_return":
                    np.nan,


                "average_return":
                    np.nan,

                }

            )



        return result