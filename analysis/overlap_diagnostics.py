"""
Overlap Diagnostics

Analyze how many trading opportunities
are lost because of non-overlapping constraint.

Current strategy assumption:

max_positions = 1

This module compares:

1. Raw signals
2. Executable non-overlapping trades
3. Blocked signals
"""


import pandas as pd



class OverlapDiagnostics:


    def __init__(
        self,
        signals: pd.DataFrame,
        entry_column="entry_date",
        exit_column="exit_date",
    ):

        self.signals = signals.copy()

        self.entry_column = entry_column
        self.exit_column = exit_column


        if len(self.signals):

            self.signals = (
                self.signals
                .sort_values(
                    self.entry_column
                )
                .reset_index(drop=True)
            )



    def raw_signal_count(self):

        return len(self.signals)



    def non_overlapping_selection(self):

        """
        Simulate current framework:

        max_positions = 1

        Keep first available signal,
        ignore overlapping signals.
        """

        selected = []

        current_exit = None


        for _, row in self.signals.iterrows():

            entry = row[self.entry_column]
            exit_ = row[self.exit_column]


            if current_exit is None:

                selected.append(row)

                current_exit = exit_

                continue



            if entry > current_exit:

                selected.append(row)

                current_exit = exit_



        if len(selected):

            return pd.DataFrame(selected)

        else:

            return pd.DataFrame(
                columns=self.signals.columns
            )



    def blocked_signal_count(self):

        selected = self.non_overlapping_selection()

        return (
            len(self.signals)
            -
            len(selected)
        )



    def overlap_ratio(self):

        total = self.raw_signal_count()


        if total == 0:

            return 0.0


        return (

            self.blocked_signal_count()

            /

            total

        )



    def summary(self):

        selected = (
            self.non_overlapping_selection()
        )


        return {

            "raw_signals":

                self.raw_signal_count(),


            "non_overlapping_trades":

                len(selected),


            "blocked_signals":

                self.blocked_signal_count(),


            "overlap_ratio":

                self.overlap_ratio(),

        }