from pathlib import Path

import pandas as pd
import numpy as np


class SignalSensitivity:


    def __init__(
        self,
        signals: pd.DataFrame,
        score_column: str,
        direction: str = "positive",
    ):

        self.signals = signals.copy()

        self.score_column = score_column

        self.direction = direction


        if self.score_column not in self.signals.columns:
            raise ValueError(
                f"Missing score column: {self.score_column}"
            )


    # --------------------------------------------------
    # Filter signals by threshold
    # --------------------------------------------------

    def apply_threshold(
        self,
        threshold,
    ):

        score = self.signals[
            self.score_column
        ]


        if self.direction == "negative":

            result = self.signals[
                score <= threshold
            ].copy()


        else:

            result = self.signals[
                score >= threshold
            ].copy()


        return result



    # --------------------------------------------------
    # Basic sensitivity
    # --------------------------------------------------

    def analyze(
        self,
        thresholds,
    ):

        rows = []


        for threshold in thresholds:


            selected = self.apply_threshold(
                threshold
            )


            rows.append(
                {

                    "threshold":
                        threshold,


                    "signal_count":
                        len(selected),


                    "signal_frequency":
                        len(selected)
                        /
                        len(self.signals),


                    "average_score":
                        (
                            selected[self.score_column]
                            .mean()
                            if len(selected)
                            else np.nan
                        ),

                }
            )


        return pd.DataFrame(rows)



    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    def save(
        self,
        df: pd.DataFrame,
        path: Path,
    ):

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(
            path,
            index=False,
            encoding="utf-8-sig",
        )