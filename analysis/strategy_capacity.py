"""
Strategy Capacity Analysis

Compare different execution capacities.

capacity = maximum simultaneous positions

Examples:
    capacity=1:
        current single position model

    capacity=2:
        allow two overlapping trades

    capacity=None:
        unlimited positions
"""


import pandas as pd



class StrategyCapacityAnalyzer:


    def __init__(
        self,
        signals: pd.DataFrame,
    ):

        self.signals = signals.copy()


        if len(self.signals):

            self.signals = (
                self.signals
                .sort_values(
                    "entry_idx"
                )
                .reset_index(drop=True)
            )



    # --------------------------------------------------
    # Single capacity simulation
    # --------------------------------------------------

    def simulate(
        self,
        capacity=1,
    ):


        if len(self.signals) == 0:

            return pd.DataFrame(
                columns=self.signals.columns
            )


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



            # unlimited positions

            if capacity is None:


                selected.append(row)

                active_positions.append(
                    exit_
                )

                continue



            # capacity available

            if len(active_positions) < capacity:


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
    # Capacity summary
    # --------------------------------------------------

    def analyze(
        self,
        capacities=[
            1,
            2,
            3,
            None,
        ],
    ):


        rows = []


        total = len(
            self.signals
        )



        for c in capacities:


            result = self.simulate(
                capacity=c
            )


            executed = len(
                result
            )


            blocked = (
                total
                -
                executed
            )


            if total:

                utilization = (
                    executed
                    /
                    total
                )

            else:

                utilization = 0



            rows.append(

                {

                    "capacity":
                        "unlimited"
                        if c is None
                        else c,


                    "raw_opportunities":
                        total,


                    "executed_trades":
                        executed,


                    "blocked_trades":
                        blocked,


                    "execution_ratio":
                        utilization,

                }

            )



        return pd.DataFrame(rows)