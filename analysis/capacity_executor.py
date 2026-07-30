"""
Capacity Execution Layer

Transforms raw signal opportunities
into executable signals under
position capacity constraints.
"""


import pandas as pd



class CapacityExecutor:



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



    def execute(self):


        selected = []


        active_positions = []



        for _, row in self.signals.iterrows():


            entry = row["entry_idx"]

            exit_ = row["exit_idx"]



            # remove expired positions

            active_positions = [

                x

                for x in active_positions

                if x > entry

            ]



            # unlimited capacity

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