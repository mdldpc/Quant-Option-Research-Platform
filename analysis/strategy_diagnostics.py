"""
Strategy Diagnostics Module v1.1

Supports two modes:

1. Feature-level diagnostics (legacy)
------------------------------------
Input example:

trade_date
signal_score
long_signal


2. Generated-signal diagnostics (current)
------------------------------------
Input example:

entry_date
exit_date
holding_days
entry_signal_score
exit_reason


Used for strategy research and parameter analysis.
"""


import pandas as pd
import numpy as np



class StrategyDiagnostics:


    def __init__(
        self,
        signals: pd.DataFrame,
        score_column: str = "entry_signal_score",
        signal_direction: str = "positive",
    ):

        self.signals = signals.copy()

        self.score_column = score_column

        self.signal_direction = signal_direction


        self.generated_signal_mode = (
            "entry_date"
            in
            self.signals.columns
        )

        self.signals = signals.copy()

        self.score_column = score_column


        # Detect signal type

        self.generated_signal_mode = (
            "entry_date"
            in
            self.signals.columns
        )



    # ==================================================
    # Signal Statistics
    # ==================================================

    def signal_statistics(self):


        # ----------------------------------------------
        # Legacy feature mode
        # ----------------------------------------------

        if not self.generated_signal_mode:


            result = {

                "total_days":
                    len(self.signals),

            }


            if "long_signal" in self.signals.columns:


                signal_days = (
                    self.signals["long_signal"]
                    ==
                    1
                ).sum()


                result["signal_days"] = int(
                    signal_days
                )


                result["signal_frequency"] = (

                    signal_days
                    /
                    len(self.signals)

                )


            return result



        # ----------------------------------------------
        # Generated signal mode
        # ----------------------------------------------

        result = {


            "total_signals":
                len(self.signals),


        }


        if "holding_days" in self.signals.columns:


            result["average_holding_days"] = (

                self.signals["holding_days"]
                .mean()

            )


            result["median_holding_days"] = (

                self.signals["holding_days"]
                .median()

            )


        return result



    # ==================================================
    # Score Distribution
    # ==================================================

    def score_distribution(self):


        score_column = self.score_column



        # fallback for old feature data

        if score_column not in self.signals.columns:


            if "signal_score" in self.signals.columns:

                score_column = "signal_score"


            else:

                return {}



        score = (

            self.signals[score_column]
            .astype(float)

        )



        return {


            "score_min":
                score.min(),


            "score_25pct":
                score.quantile(0.25),


            "score_median":
                score.median(),


            "score_75pct":
                score.quantile(0.75),


            "score_max":
                score.max(),


        }



    # ==================================================
    # Holding Statistics
    # ==================================================

    def holding_statistics(self):


        if "holding_days" not in self.signals.columns:

            return {}



        holding = (

            self.signals["holding_days"]
            .astype(float)

        )


        return {


            "holding_min":
                holding.min(),


            "holding_median":
                holding.median(),


            "holding_max":
                holding.max(),


        }



    # ==================================================
    # Exit Statistics
    # ==================================================

    def exit_statistics(self):


        result = {}


        if "exit_reason" not in self.signals.columns:

            return result



        counts = (

            self.signals["exit_reason"]
            .value_counts()

        )


        for name,count in counts.items():


            result[
                f"exit_{name}"
            ] = int(count)



        return result



    # ==================================================
    # Threshold Analysis
    # ==================================================

    def threshold_analysis(
        self,
        thresholds=None,
    ):


        if thresholds is None:

            thresholds = [

                -3,
                -2,
                -1.5,
                -1,
                -0.5,
                0,
                0.5,
                1,

            ]



        score_column = self.score_column



        # backward compatibility

        if score_column not in self.signals.columns:


            if "signal_score" in self.signals.columns:

                score_column = "signal_score"


            else:

                return pd.DataFrame()



        score = (

            self.signals[score_column]
            .astype(float)

        )



        rows = []



        for threshold in thresholds:


            if self.signal_direction == "negative":

                count = (
                    score <= threshold
                ).sum()

            else:

                count = (
                    score >= threshold
                ).sum()



            rows.append(

                {

                    "threshold":
                        threshold,


                    "signal_count":
                        int(count),


                    "signal_days":
                        int(count),

                }

            )



        return pd.DataFrame(rows)



    # ==================================================
    # Summary
    # ==================================================

    def summary(self):


        result = {}



        result.update(

            self.signal_statistics()

        )



        result.update(

            self.score_distribution()

        )



        result.update(

            self.holding_statistics()

        )



        result.update(

            self.exit_statistics()

        )



        return result