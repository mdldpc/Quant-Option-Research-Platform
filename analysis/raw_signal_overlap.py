"""
Raw Signal Overlap Diagnostics

Analyze potential trading opportunities
before signal generator position filtering.

Purpose:

Measure whether low trade frequency is caused by:

1. Few raw opportunities
2. Non-overlapping constraint

"""

import pandas as pd



class RawSignalOverlapDiagnostics:


    def __init__(
        self,
        signals: pd.DataFrame,
    ):

        self.signals = signals.copy()


        # ----------------------------------------
        # Determine index columns
        # ----------------------------------------

        if (
            "entry_idx" in self.signals.columns
            and
            "exit_idx" in self.signals.columns
        ):

            self.entry_column = "entry_idx"
            self.exit_column = "exit_idx"


        elif (
            "entry_date" in self.signals.columns
            and
            "exit_date" in self.signals.columns
        ):

            self.entry_column = "entry_date"
            self.exit_column = "exit_date"


        else:

            raise ValueError(
                "Signals must contain either "
                "(entry_idx, exit_idx) or "
                "(entry_date, exit_date)"
            )



        if len(self.signals):

            self.signals = (
                self.signals
                .sort_values(
                    self.entry_column
                )
                .reset_index(drop=True)
            )



    # ----------------------------------------
    # Raw opportunity count
    # ----------------------------------------

    def raw_count(self):

        return len(self.signals)



    # ----------------------------------------
    # Single position simulation
    # ----------------------------------------

    def simulate_non_overlap(self):

        selected = []

        current_exit = None


        for _, row in self.signals.iterrows():

            entry = row[self.entry_column]

            exit_ = row[self.exit_column]


            if current_exit is None:

                selected.append(row)

                current_exit = exit_

                continue



            if entry >= current_exit:

                selected.append(row)

                current_exit = exit_



        if len(selected):

            return pd.DataFrame(selected)


        return pd.DataFrame(
            columns=self.signals.columns
        )



    # ----------------------------------------
    # Blocked opportunities
    # ----------------------------------------

    def blocked_count(self):

        selected = (
            self.simulate_non_overlap()
        )

        return (
            self.raw_count()
            -
            len(selected)
        )



    def overlap_ratio(self):

        if self.raw_count()==0:

            return 0.0


        return (

            self.blocked_count()

            /

            self.raw_count()

        )



    def summary(self):

        selected = (
            self.simulate_non_overlap()
        )


        return {

            "raw_opportunities":
                self.raw_count(),


            "executable_trades":
                len(selected),


            "blocked_opportunities":
                self.blocked_count(),


            "overlap_ratio":
                self.overlap_ratio(),

        }